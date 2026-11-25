# Stock screener scalability benchmark

Measure the existing `/api/stocks` path before choosing where to optimize for
live data. Keep this separate from the delivered sample and cleanup plans.
See the [benchmark checklist](benchmark-todo.md) for execution and acceptance.

## Design

- Generate deterministic, local synthetic datasets of 1,000, 10,000, and
  100,000 stocks with repeated sectors, tied values, and missing metrics.
- Exercise the default first page, a broad combined filter, and a sorted page
  beyond offset zero. Record platform, commit, worker count, dataset seed,
  warmup, request counts, and concurrency. Start with one worker and use 1,
  8, and 32 concurrent clients as exploratory levels.
- Compare requests that read and validate a packaged-format JSON fixture with
  requests using the existing injected source seam and an already validated
  dataset. Measure source loading and screening independently if HTTP results
  cannot show which stage dominates. Label the injected-source results as
  excluding input loading and validation.
- Record median and p95 latency, throughput, errors and timeouts, and peak
  server memory with the measurement method. Check totals, order, and page
  contents outside timing samples so a fast wrong response cannot pass.

## Decision after measurement

Choose the dataset size, traffic level, and latency target before interpreting
capacity. If per-request loading dominates, test reusing a validated snapshot.
If filtering and sorting dominate at the intended size, compare an indexed
storage query. If neither dominates, inspect the HTTP and concurrency results
before making architectural changes. Keep full runs advisory until results
are repeatable on a controlled environment.
