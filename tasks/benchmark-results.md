# Stock endpoint benchmark results

The application baseline was `f2ef112`. The benchmark uses one Uvicorn worker
and sends requests over loopback. No provider, external network, or browser is
in the measured path. Commands ran on Windows 11 build 26300 with Python 3.15.0,
an AMD Ryzen AI 7 350 with 8 cores and 16 logical processors, and 31.3 GiB RAM.
The fixture seed was `2026`.

```sh
uv run --locked python scripts/benchmark_stocks.py --smoke
uv run --locked python scripts/benchmark_stocks.py --sizes 1000 10000 100000 --requests 32 --warmup 4
uv run --locked python scripts/benchmark_stocks.py --sizes 100000 --requests 32 --warmup 4
uv run --locked python scripts/benchmark_stocks.py --sizes 10000 --clients 1 --requests 32 --warmup 4
```

The original full command provided the 1,000- and 10,000-stock measurements.
After a saturated 100,000-stock disk group, the large-only command reran that
size with the runner's stop-on-error behavior. Each measured cell uses 32
requests after four warmups. Concurrency is the maximum number of client
threads. Each thread reuses its connection within a timed cell. Latency is
wall-clock time through receipt of the response body, measured for successful
requests only. Throughput includes elapsed time spent waiting for failures.

Windows peak working set is the server process lifetime high-water mark for
each dataset and source pair. It includes server startup and all workloads in
that group. Disk-backed runs include reading and validating fixture JSON on
each request. Prevalidated runs still include filtering, sorting, serialization,
and HTTP.

## Measurements

Each source cell reports **p50 ms / p95 ms / successful requests per second /
timed errors**. The 24 errors in the large disk-backed rerun were socket
timeouts. Its remaining disk-backed cells were skipped. No warmups failed
in the reported matrix. In the preceding attempt, the same 32-client
disk-backed workload had 28 measured timeouts and four warmup timeouts.

| Stocks | Workload | Clients | Disk-backed | Prevalidated |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | default | 1 | 12.09 / 18.26 / 77.54 / 0 | 5.34 / 8.36 / 163.01 / 0 |
| 1,000 | default | 8 | 79.43 / 107.65 / 91.65 / 0 | 36.99 / 42.94 / 210.72 / 0 |
| 1,000 | default | 32 | 293.63 / 391.05 / 74.47 / 0 | 90.20 / 112.88 / 228.73 / 0 |
| 1,000 | filtered | 1 | 9.92 / 11.95 / 99.94 / 0 | 4.42 / 6.19 / 214.69 / 0 |
| 1,000 | filtered | 8 | 65.69 / 87.49 / 117.95 / 0 | 22.28 / 31.30 / 312.12 / 0 |
| 1,000 | filtered | 32 | 168.91 / 261.73 / 110.59 / 0 | 95.48 / 122.62 / 209.26 / 0 |
| 1,000 | sorted | 1 | 9.52 / 15.06 / 96.97 / 0 | 6.08 / 7.98 / 159.40 / 0 |
| 1,000 | sorted | 8 | 68.14 / 134.62 / 95.29 / 0 | 34.69 / 48.87 / 208.84 / 0 |
| 1,000 | sorted | 32 | 234.61 / 343.38 / 87.49 / 0 | 89.49 / 117.23 / 233.04 / 0 |
| 10,000 | default | 1 | 78.91 / 106.61 / 12.39 / 0 | 17.21 / 24.44 / 56.64 / 0 |
| 10,000 | default | 8 | 582.22 / 762.65 / 13.16 / 0 | 119.70 / 145.75 / 62.01 / 0 |
| 10,000 | default | 32 | 1902.87 / 2594.22 / 12.21 / 0 | 361.41 / 542.85 / 56.75 / 0 |
| 10,000 | filtered | 1 | 61.68 / 77.46 / 15.95 / 0 | 7.51 / 12.98 / 119.56 / 0 |
| 10,000 | filtered | 8 | 560.92 / 682.72 / 15.30 / 0 | 58.18 / 85.39 / 121.96 / 0 |
| 10,000 | filtered | 32 | 1792.66 / 2277.08 / 13.87 / 0 | 166.97 / 217.48 / 133.03 / 0 |
| 10,000 | sorted | 1 | 90.24 / 119.94 / 10.56 / 0 | 26.37 / 42.33 / 35.45 / 0 |
| 10,000 | sorted | 8 | 828.16 / 953.84 / 9.93 / 0 | 221.96 / 277.35 / 34.06 / 0 |
| 10,000 | sorted | 32 | 2430.65 / 3238.03 / 9.80 / 0 | 668.81 / 939.07 / 33.26 / 0 |
| 100,000 | default | 1 | 684.96 / 738.55 / 1.45 / 0 | 155.98 / 189.16 / 6.21 / 0 |
| 100,000 | default | 8 | 6032.68 / 8139.33 / 1.28 / 0 | 1244.03 / 1637.84 / 6.18 / 0 |
| 100,000 | default | 32 | 8490.67 / 16434.64 / 0.49 / 24 | 3511.46 / 5090.37 / 6.26 / 0 |
| 100,000 | filtered | 1 | Skipped | 57.13 / 67.27 / 17.32 / 0 |
| 100,000 | filtered | 8 | Skipped | 455.59 / 504.13 / 17.21 / 0 |
| 100,000 | filtered | 32 | Skipped | 1252.20 / 1807.47 / 17.45 / 0 |
| 100,000 | sorted | 1 | Skipped | 360.67 / 458.53 / 2.73 / 0 |
| 100,000 | sorted | 8 | Skipped | 2773.57 / 3470.40 / 2.86 / 0 |
| 100,000 | sorted | 32 | Skipped | 7622.99 / 10655.32 / 3.00 / 0 |

### Server peak working set

| Stocks | Disk-backed | Prevalidated |
| ---: | ---: | ---: |
| 1,000 | 77.0 MiB | 63.7 MiB |
| 10,000 | 212.4 MiB | 75.9 MiB |
| 100,000 | 1674.3 MiB | 248.2 MiB |

### Repeat at 10,000 stocks

At one client, the disk-backed default p50 moved from 78.91 to 79.28 ms
and p95 from 106.61 to 98.49 ms. The prevalidated default p50 moved from
17.21 to 22.71 ms and p95 from 24.44 to 38.87 ms. All six repeated cells
completed without errors. The direction held while tail latency varied,
especially with the smaller prevalidated timings.

## Recommendation

Test reuse of a validated snapshot first. At 10,000 stocks and one client,
removing per-request JSON loading and validation cut default p95 from
106.61 to 24.44 ms in the matrix. At 100,000 stocks and 32 clients,
it removed the observed default-page timeouts and reduced peak memory,
but the prevalidated sorted page still had a 10.66-second p95. If the
intended deployment needs that universe size under concurrent sorting,
compare an indexed storage query next.

These results are exploratory. The 32-client cells have one timed request
per client, and p95 for a cell with many timeouts reflects only its successful
responses. Set a deployment-specific latency and traffic target and rerun
with a larger sample before setting a performance gate. CI runs the
deterministic correctness smoke check without a timing threshold.
