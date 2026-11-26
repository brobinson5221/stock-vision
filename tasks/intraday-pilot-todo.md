# Intraday market data pilot checklist

Each task has its own commit checkpoint. Use `commit-message-storyteller` on
the scoped staged diff after the task passes its checks. Keep code and its
regression tests together.

## Task 1 — Verify free-account access

Use a server-side free-account key for a small multi-symbol probe of completed
one-minute SIP bars. Confirm feed, timestamps, pagination, entitlement and
local storage terms. Fix the pilot manifest and coverage rules before timing.

- [ ] Record status, call count, bar dates, and symbol coverage without keys
  or raw payloads. Stop at this checkpoint if Basic access does not work.
- [ ] Record the reproducible probe command and approved usage scope.

Depends on the merged plan. Small scope in pilot notes. Commit the access findings.

## Task 2 — Fetch and validate a candidate snapshot

Use a one-shot Python refresh command. Match the last eligible bar to each
symbol, calculate freshness, and produce a validated candidate with provenance.

- [ ] Fixture tests cover pagination, duplicates, timestamps, missing rows,
  throttling, and partial failure. Verify pagination with an actual response.
- [ ] Candidate generation reports coverage, price age, and request counts.

Depends on Task 1. Medium scope in the refresh command, fixture, and Python
tests. Run focused pytest and Ruff, then commit the refresh command and tests.

## Checkpoint after Tasks 1–2

- [ ] Confirm the fixture checks run in existing CI and the provider probe fits
  the rate budget. Record blockers before wiring the snapshot into the app.

## Task 3 — Serve the last good snapshot

Publish a validated snapshot atomically and load it through the existing
source boundary. Keep the demo default and preserve the last good data on failure.

- [ ] API tests cover a successful replacement, a failed replacement, and
  startup before a snapshot exists. Multiple queries trigger zero provider calls.
- [ ] Chromium verifies the delayed label, timestamp, and existing controls.

Depends on Task 2. Medium scope in snapshot storage, the source boundary, and
tests. Run pytest, frontend lint/build, and Chromium, then commit the serving
change with tests. Use the existing CI jobs for these checks.

## Task 4 — Run and report the session trial

Invoke the same refresh command every five minutes during the trial, using
the U.S. market calendar. Test failure recovery offline before the session.

- [ ] Report calls, latency, coverage, freshness, gaps, and success against the
  proposed thresholds. Include the clock, feed, date, and manifest revision.
- [ ] Confirm last-good behavior and document how to reproduce the trial.

Depends on Task 3. Small scope in the runbook and results. Commit the results
separately from runtime changes. Keep timing and provider access advisory in CI.

## PR checkpoint

- [ ] After the planning PR merges, fetch `origin/main` and branch from it.
- [ ] Run the full Python and Chromium suites, benchmark smoke, and Docker smoke.
- [ ] Use `pr` for the description and `create-pr` to publish one implementation
  PR and verify its latest CI. Leave squash merge to the user, then refresh main
  before starting another PR.
