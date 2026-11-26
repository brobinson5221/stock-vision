# xang1234 refresh pipeline and intraday trial

Reproduce the refresh decisions in xang1234/stock-screener, then test whether
the same approach can keep Stock Vision current during a U.S. trading session.

## What the reference does

The default mode imports verified daily price and weekly reference bundles
from GitHub Releases, then fetches missing or stale symbols through live
providers. The alternative mode bypasses the bundles. The public demo is
a daily static export. The scheduled daily pipeline warms the cache before
running scans and publishing results. In its daily workflow, live means
fetching from a provider on demand. It does not establish sub-day freshness.

See the [operations guide](https://github.com/xang1234/stock-screener/blob/main/docs/OPERATIONS.md),
[cache tasks](https://github.com/xang1234/stock-screener/blob/main/backend/app/tasks/cache_tasks.py),
and [static site guide](https://github.com/xang1234/stock-screener/blob/main/docs/STATIC_SITE.md).

## What to test

1. Inspect a published release manifest and pin the upstream Git revision used
   to trace the importer, freshness checks, fallback, and refresh guard.
2. Replay the same decisions locally using synthetic bundles and a recorded or
   simulated top-up provider. Run cold, warm, partial, and failed refreshes.
   Compare requests and coverage with a full-fetch run. Verify that fresh
   symbols are skipped and failed refreshes preserve the previous snapshot.
3. Replace daily freshness with completed intraday bar freshness. Daily
   bundles can seed history and reference data. They cannot satisfy a missing
   or stale intraday bar. Keep price, reference, and fundamental refreshes on
   separate clocks, with missing market cap and P/E left null initially.
4. Verify the upstream sources independently. yfinance documents sub-day
   intervals. Check what the referenced project actually uses, and what any
   authorized test feed returns, before choosing the feed. Yahoo requires
   express prior permission for automated collection. Check Finviz access and
   data-use terms separately before automating its use. If access is unavailable,
   run the offline replay and record what remains unverified.

See [yfinance interval documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html)
and [Yahoo's U.S. terms](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html).

## Trial and success criteria

Use a fixed list of 500 U.S. stocks and a five-minute refresh interval during
one regular session once an authorized intraday source is available. Start
with a small symbol probe. Record the bar interval, feed delay, completed bar
end, coverage, actual upstream requests including retries, 429s, and refresh
duration. Use the exchange calendar and keep missing-symbol rules fixed.

Proposed thresholds are 95% coverage in 95% of scheduled cycles, each refresh
finishing before the next one, and no sustained throttling. Pick a price-age
target after confirming the actual feed delay, before the full session starts.
Report call counts for both full refresh and top-up. Compare cold and warm
runs separately. Reject prior-session prices as intraday observations.

Serve the last validated snapshot through the existing Stock Vision API with
source and timestamp metadata. A failed refresh keeps the previous snapshot,
and screener queries make zero upstream requests. Keep the demo as the default.
Fixture tests run in existing CI. Live requests and raw provider data stay
outside CI and Git. See the [implementation checklist](intraday-pilot-todo.md).
