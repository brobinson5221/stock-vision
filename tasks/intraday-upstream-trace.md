# Upstream refresh trace

Reference revision `f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94`.

- The [bundle service](https://github.com/xang1234/stock-screener/blob/f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94/backend/app/services/daily_price_bundle_service.py)
  checks the manifest's market, `as_of_date`, and `bar_period` and verifies
  the bundle checksum before import. The [U.S. manifest](https://github.com/xang1234/stock-screener/releases/download/daily-price-data/daily-price-latest-us.json)
  reported `daily-price-manifest-v1`, `as_of_date` of 2026-11-25, a `2y`
  history window, 10,040 symbols, and SHA-256 and coverage fields. This trace
  read metadata only.
- The [refresh workflow](https://github.com/xang1234/stock-screener/blob/f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94/backend/app/services/price_refresh_workflow.py)
  plans the refresh first, runs the required live fetches in batches, and
  accounts for failed symbols separately. The [operations guide](https://github.com/xang1234/stock-screener/blob/f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94/docs/OPERATIONS.md)
  describes seven-day top-ups for stale symbols and two-year backfills for
  symbols without history during bootstrap.
- The [pipeline dispatcher](https://github.com/xang1234/stock-screener/blob/f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94/backend/app/tasks/daily_market_pipeline_tasks.py)
  resolves the last completed trading session, then builds the daily chain.
  That establishes daily freshness. It does not establish that the same
  provider can deliver timely intraday bars across the pilot universe.

The replay will model the decisions that matter for Stock Vision. It uses a
synthetic bundle format and a strict full-coverage gate to keep the results
easy to inspect. Provider entitlement, call counts, and deadline behavior
need a later authorized probe.

## Offline replay results

Run `uv run --locked pytest tests/unit/test_refresh_replay.py -q`. All nine
scenarios passed with 500 fixture symbols and up to 100 symbols per simulated
call. A cold, stale, or invalid-checksum bundle fetched all 500 in five calls.
A warm bundle with 480 fresh symbols fetched 20 in one call, and a fully fresh
bundle needed zero calls. Partial top-up and timeout kept the prior snapshot.
A cold refresh with missing bars left the snapshot unavailable.

A complete daily bundle still needed five calls when the requested interval
was intraday. The savings depend on how many cached bars actually meet the
intraday freshness cutoff. This replay uses an in-memory publication decision.
File replacement, concurrent refreshes, API/browser integration, and live feed
entitlement and coverage still need tests.
