# Delayed intraday market data pilot

Test whether Alpaca Basic can refresh Stock Vision for 500 U.S. stocks during
a regular trading session. Use completed one-minute historical SIP bars, a
five-minute refresh interval, and a query end at least 16 minutes behind the
clock. The extra minute keeps the request beyond the published 15-minute
restriction. Measure actual age from the bar's end time. The app should label
the feed as delayed and identify the session and data timestamp.

## Data flow

1. A local refresh command reads a fixed 500-symbol manifest and requests bars
   in batches. Follow pagination and choose the latest eligible completed bar
   per symbol. Use a bounded search window and timeouts. Respect provider rate
   limits and stop or back off on throttling.
2. Join prices to a local reference manifest for ticker, company name, and
   sector. Start with a documented source or a curated pilot manifest. Label
   unknown sectors explicitly. Preserve missing market cap and P/E as null.
   Adding and validating a slower fundamentals pipeline is separate work.
3. Validate a complete candidate before atomically replacing the last good
   local snapshot. Preserve the old snapshot when a refresh fails or falls
   below the coverage threshold. Keep refresh time separate from market data
   time and retain per-symbol bar timestamps for auditing. Use the oldest
   included bar end for the API's dataset timestamp so the label does not
   overstate freshness. Do not fill gaps with prior-session prices silently.
4. Keep the packaged synthetic sample as the default. An explicit local pilot
   setting serves the saved snapshot through the existing `/api/stocks` path.
   Searches, filters, sorting, and paging make zero upstream requests. If the
   pilot is enabled before its first successful refresh, show it as unavailable.

## Pilot decision

Measure one regular U.S. session, from the first eligible window through the
last delayed refresh. Use the market calendar so holidays and early closes do
not count as outages. Report per-cycle coverage, p50/p95 and maximum price age,
upstream calls including retries, 429s, refresh duration, and the reasons for
missing symbols. Spot-check several named symbols and compare the results with
the API and browser labels.

Proposed pass criteria are at least 95% of the fixed universe with eligible
bars in at least 95% of scheduled cycles, p95 bar age at most 25 minutes for
published rows during scheduled windows, and at most 10 calls per ordinary
cycle with no sustained throttling. Keep the denominator and the rules for
halts and thin trading fixed before the run. Record misses and classify gaps
instead of substituting a different feed mid-pilot. These are trial thresholds.

Keep the trial private. Verify account entitlements and applicable storage
terms before capturing actual provider data. Confirm display rights separately
before making price data available to others. Keep credentials and live
snapshots out of Git and CI. Existing Python and Chromium jobs should run
deterministic fixture checks without credentials.

See the [implementation checklist](intraday-pilot-todo.md). Provider assumptions
come from the [plan limits](https://docs.alpaca.markets/us/docs/about-market-data-api),
[historical SIP FAQ](https://docs.alpaca.markets/us/docs/market-data-faq),
[multi-symbol bars reference](https://docs.alpaca.markets/us/reference/stockbars),
and [redistribution guidance](https://alpaca.markets/support/redistribute-alpaca-api).
