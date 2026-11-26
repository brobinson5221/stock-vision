# Upstream refresh trace

Reference revision `f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94`.

- The [bundle service](https://github.com/xang1234/stock-screener/blob/f28e4c1b22288f865a51c97b2ec9fcbcd9a2eb94/backend/app/services/daily_price_bundle_service.py)
  checks the manifest's market, `as_of_date`, and daily `bar_period` and
  verifies the bundle checksum before import. The GitHub release lists
  bundles. This trace did not retrieve a separate U.S. manifest asset.
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
