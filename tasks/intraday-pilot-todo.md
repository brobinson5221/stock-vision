# xang1234 refresh and intraday checklist

Use commit-message-storyteller on each staged diff. Commit the focused change
and its checks together before moving to the next task.

## Task 1 — Trace the reference refresh

- [ ] Pin the upstream revision and trace bundle import, freshness checks,
  missing/stale top-up, and publication after refresh validation.
- [ ] Identify whether the referenced price path requests daily or sub-day
  bars. Record the manifest format and any limits observed in source.
- [ ] Document what is confirmed from code and what still requires a run.

No dependencies beyond the merged plan. Scope is the upstream trace notes.
Commit the findings separately.

## Task 2 — Replay bundle-first versus full fetch

- [ ] With a fixed synthetic fixture, verify cold start, valid warm start,
  bad checksum or stale bundle, partial top-up, and failed refresh.
- [ ] Verify that warm runs fetch only stale or missing symbols and preserve
  the last good snapshot when a refresh fails.
- [ ] Record fixture call counts for both refresh modes.

Depends on Task 1. Scope is a local harness, fixture, and focused pytest
coverage. Run pytest and Ruff before committing.

## Checkpoint after Tasks 1–2

- [ ] Record which parts of the reference behavior the replay reproduced.
- [ ] Confirm the fixtures run in existing CI. Verify authorization and
  entitlements before attempting a real provider probe.

## Task 3 — Test intraday freshness and publication

- [ ] Replay a sequence of completed intraday bars and verify that a daily
  bundle does not make an intraday price fresh. Test missing and old bars,
  retry handling, and overlapping refreshes.
- [ ] Verify that snapshot publication is atomic, failed refreshes preserve
  data, and multiple screener requests trigger zero provider calls.
- [ ] Verify the source and timestamp in Chromium using an offline fixture.

Depends on Task 2. Scope includes the refresh harness, source boundary, and
tests. Run pytest, frontend lint/build, and Chromium before committing.

## Task 4 — Probe and measure the live session

- [ ] Confirm bar coverage, real request counts, and delay on a small set
  using an authorized source. Keep any unavailable upstream path explicitly
  unverified.
- [ ] Run the 500-stock trial if the probe passes. Report freshness, coverage,
  refresh duration, request volume, and missing-symbol causes.
- [ ] Commit reproducible commands and findings without credentials or payloads.

Depends on Task 3 and provider access. Scope is pilot notes and results.
No time-based CI gate.

## PR checkpoint

- [ ] After the plan merges, branch from refreshed origin/main.
- [ ] Run the full pytest and Chromium suites, benchmark smoke, and Docker smoke.
- [ ] Use pr to write the description and create-pr to open one implementation
  PR and verify its latest CI. Leave squash merge to the user.
