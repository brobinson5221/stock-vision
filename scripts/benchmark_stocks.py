# ruff: noqa: INP001, S101, S603 -- Standalone local benchmark with a correctness self-check.
import argparse
import json
import math
import os
import platform
import random
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from http.client import HTTPConnection, HTTPException
from pathlib import Path

import uvicorn

from stock_vision.main import create_app
from stock_vision.stocks.schemas import StockDataset
from stock_vision.stocks.source import load_sample_stocks

SEED = 2026
MIN_PRICE, MAX_PRICE = 25, 75
WORKLOADS = {
    "default": "",
    "filtered": f"?q=benchmark&sector=Technology&min_price={MIN_PRICE}&max_price={MAX_PRICE}",
    "sorted": "?sort_by=market_cap&sort_dir=desc&offset=50",
}


def fixture(size: int) -> list[dict]:
    rng = random.Random(SEED)  # noqa: S311 -- Reproducible synthetic fixture.
    rows = [
        {
            "symbol": f"BENCH{index:06d}",
            "name": f"Benchmark {index}",
            "sector": ("Technology", "Energy", "Healthcare", "Industrials")[index % 4],
            "price": rng.randint(1, 100),
            "market_cap": None if index % 7 == 0 else (index % 20) * 100_000_000,
            "pe_ratio": None if index % 11 == 0 else index % 20 - 5,
        }
        for index in range(size)
    ]
    rng.shuffle(rows)
    return rows


def expected_page(rows: list[dict], workload: str) -> tuple[int, int, list[dict]]:
    ordered = sorted(rows, key=lambda row: row["symbol"])
    offset = 0
    if workload == "filtered":
        ordered = [
            row
            for row in ordered
            if row["sector"] == "Technology" and MIN_PRICE <= row["price"] <= MAX_PRICE
        ]
    elif workload == "sorted":
        offset = 50
        ordered.sort(key=lambda row: (row["market_cap"] is None, -(row["market_cap"] or 0)))
    return len(ordered), offset, ordered[offset : offset + 50]


def serve(path: Path, mode: str, port: int) -> None:
    app = create_app()

    def read() -> StockDataset:
        return StockDataset.model_validate_json(path.read_text(encoding="utf-8"))

    if mode == "disk":
        app.dependency_overrides[load_sample_stocks] = read
    else:
        dataset = read()
        app.dependency_overrides[load_sample_stocks] = lambda: dataset
    # Windows virtualenv launchers may have a different PID from the server.
    path.with_suffix(".pid").write_text(str(os.getpid()), encoding="utf-8")
    uvicorn.run(app, host="127.0.0.1", port=port, workers=1, log_level="warning")


def request(connection: HTTPConnection, path: str) -> tuple[int, bytes]:
    connection.request("GET", path)
    response = connection.getresponse()
    return response.status, response.read()


def exercise(port: int, path: str, clients: int, requests: int) -> dict:
    def worker(index: int) -> tuple[list[float], Counter]:
        connection = HTTPConnection("127.0.0.1", port, timeout=15)
        times = []
        errors = Counter()
        try:
            for _ in range(index, requests, clients):
                started = time.perf_counter()
                try:
                    status, _ = request(connection, path)
                except (OSError, HTTPException) as error:
                    errors[type(error).__name__] += 1
                    connection.close()
                else:
                    if status == HTTPStatus.OK:
                        times.append((time.perf_counter() - started) * 1000)
                    else:
                        errors[str(status)] += 1
        finally:
            connection.close()
        return times, errors

    errors = Counter()
    times = []
    with ThreadPoolExecutor(max_workers=clients) as pool:
        started = time.perf_counter()
        for durations, failures in pool.map(worker, range(clients)):
            times.extend(durations)
            errors.update(failures)
        elapsed = time.perf_counter() - started
    times.sort()
    return {
        "p50_ms": round(times[math.ceil(0.50 * len(times)) - 1], 2) if times else None,
        "p95_ms": round(times[math.ceil(0.95 * len(times)) - 1], 2) if times else None,
        "successful_rps": round(len(times) / elapsed, 2),
        "errors": dict(errors),
    }


def peak_memory(pid: int) -> int | None:
    if sys.platform == "win32" and (powershell := shutil.which("powershell.exe")):
        result = subprocess.check_output(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"(Get-Process -Id {pid}).PeakWorkingSet64",
            ],
            text=True,
        )
        return int(result.strip())
    if sys.platform.startswith("linux"):
        status = Path(f"/proc/{pid}/status").read_text(encoding="utf-8")
        return (
            int(next(line for line in status.splitlines() if line.startswith("VmHWM:")).split()[1])
            * 1024
        )
    return None


def wait_for_server(server: subprocess.Popen, port: int) -> None:
    health = HTTPConnection("127.0.0.1", port, timeout=1)
    try:
        for _ in range(100):
            try:
                if request(health, "/api/health")[0] == HTTPStatus.OK:
                    return
            except OSError:
                health.close()
            if server.poll() is not None:
                msg = "Benchmark server exited during startup"
                raise RuntimeError(msg)
            time.sleep(0.1)
        msg = "Benchmark server did not become ready"
        raise RuntimeError(msg)
    finally:
        health.close()


def run_group(path: Path, rows: list[dict], mode: str, args: argparse.Namespace) -> bool:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    command = [sys.executable, __file__, "--serve", str(path), mode, str(port)]
    failed = False
    with subprocess.Popen(command) as server:
        try:
            wait_for_server(server, port)
            for name, query in WORKLOADS.items():
                endpoint = f"/api/stocks{query}"
                connection = HTTPConnection("127.0.0.1", port, timeout=15)
                try:
                    status, body = request(connection, endpoint)
                finally:
                    connection.close()
                total, offset, items = expected_page(rows, name)
                assert status == HTTPStatus.OK
                assert json.loads(body) == {
                    "items": items,
                    "total": total,
                    "offset": offset,
                    "limit": 50,
                    "provenance": "synthetic-sample",
                    "source_name": None,
                    "as_of": None,
                    "sectors": sorted({row["sector"] for row in rows}),
                    "currency": "USD",
                }
                for clients in args.clients:
                    warmup = exercise(port, endpoint, clients, args.warmup)
                    metrics = exercise(port, endpoint, clients, args.requests)
                    failed |= bool(warmup["errors"] or metrics["errors"])
                    print(
                        json.dumps(
                            {
                                "size": len(rows),
                                "mode": mode,
                                "workload": name,
                                "clients": clients,
                                "warmup_errors": warmup["errors"],
                                **metrics,
                            },
                        ),
                        flush=True,
                    )
                    if failed:
                        break
                if failed:
                    break
            if not args.smoke:
                pid = int(path.with_suffix(".pid").read_text(encoding="utf-8"))
                print(
                    json.dumps(
                        {"size": len(rows), "mode": mode, "peak_bytes": peak_memory(pid)},
                    ),
                )
        finally:
            server.terminate()
    return failed


def main() -> int:
    if sys.argv[1:2] == ["--serve"]:
        _, _, path, mode, port = sys.argv
        serve(Path(path), mode, int(port))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 10000, 100000])
    parser.add_argument("--clients", type=int, nargs="+", default=[1, 8, 32])
    parser.add_argument("--requests", type=int, default=64)
    parser.add_argument("--warmup", type=int, default=8)
    parser.add_argument("--smoke", action="store_true", help="Check both source modes with 80 rows")
    args = parser.parse_args()
    if args.smoke:
        args.sizes, args.clients, args.requests, args.warmup = [80], [1], 2, 1
    if min(*args.sizes, *args.clients, args.requests, args.warmup) < 1:
        parser.error("sizes, clients, requests, and warmup must be positive")
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "seed": SEED,
                "workers": 1,
                "requests": args.requests,
                "warmup": args.warmup,
            },
        ),
    )
    failed = False
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "stocks.json"
        for size in args.sizes:
            rows = fixture(size)
            path.write_text(json.dumps({"items": rows}), encoding="utf-8")
            for mode in ("disk", "validated"):
                failed |= run_group(path, rows, mode, args)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
