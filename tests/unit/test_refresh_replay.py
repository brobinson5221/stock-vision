# ruff: noqa: INP001, S101 -- Offline experiment run by the existing pytest job.
import hashlib
import json
from itertools import batched

import pytest

UNIVERSE = tuple(f"TEST{index:03d}" for index in range(500))
BATCH_SIZE = 100
CUTOFF = 100
NOW = 105


def fresh(bars, interval):
    return {
        symbol: bar
        for symbol, bar in bars.items()
        if bar["interval"] == interval and CUTOFF <= bar["end"] <= NOW
    }


def replay(payload, checksum, fetch, previous, *, interval):
    seed = {}
    if payload is not None and hashlib.sha256(payload).hexdigest() == checksum:
        seed = fresh(json.loads(payload), interval)
    missing = (symbol for symbol in UNIVERSE if symbol not in seed)
    try:
        for batch in batched(missing, BATCH_SIZE, strict=False):
            fetched = fresh(fetch(batch), interval)
            seed.update({symbol: fetched[symbol] for symbol in batch if symbol in fetched})
    except TimeoutError:
        return previous
    return seed if len(seed) == len(UNIVERSE) else previous


@pytest.mark.parametrize(
    ("scenario", "expected_calls", "expected_symbols", "publishes"),
    [
        ("cold", 5, 500, True),
        ("fresh", 0, 0, True),
        ("warm", 1, 20, True),
        ("stale", 5, 500, True),
        ("bad-checksum", 5, 500, True),
        ("partial", 1, 20, False),
        ("timeout", 1, 20, False),
        ("cold-missing", 5, 500, False),
        ("daily-for-intraday", 5, 500, True),
    ],
)
def test_bundle_first_refresh_replay(scenario, expected_calls, expected_symbols, publishes):
    interval = "1min" if scenario == "daily-for-intraday" else "1day"
    provider_bar = {"interval": interval, "end": NOW}
    bundle_bar = {"interval": "1day", "end": CUTOFF - 1 if scenario == "stale" else CUTOFF}
    cached_symbols = (
        UNIVERSE if scenario in {"fresh", "stale", "daily-for-intraday"} else UNIVERSE[:-20]
    )
    payload = json.dumps(dict.fromkeys(cached_symbols, bundle_bar)).encode()
    checksum = hashlib.sha256(payload).hexdigest()
    prior = (
        {} if scenario == "cold-missing" else {symbol: {"end": CUTOFF - 1} for symbol in UNIVERSE}
    )
    calls = []

    def fetch(batch):
        calls.append(batch)
        if scenario == "timeout":
            raise TimeoutError
        if scenario in {"partial", "cold-missing"}:
            batch = batch[:-1]
        return dict.fromkeys(batch, provider_bar)

    if scenario in {"cold", "cold-missing"}:
        payload = None
    if scenario == "bad-checksum":
        checksum = "invalid"
    result = replay(payload, checksum, fetch, prior, interval=interval)

    assert len(calls) == expected_calls
    assert sum(map(len, calls)) == expected_symbols
    requested = {symbol for batch in calls for symbol in batch}
    assert requested == set(UNIVERSE[len(UNIVERSE) - expected_symbols :])
    if publishes:
        assert set(result) == set(UNIVERSE)
        assert fresh(result, interval) == result
    else:
        assert result is prior
