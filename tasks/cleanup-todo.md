# Screener cleanup checklist

## Task 1 — Establish the baseline

Run `uv run --locked pytest tests` and the frontend `lint`, `build`, and
`test:e2e` scripts from the README. Record any setup failures separately.

- [ ] Results are recorded against the starting commit before any screener edit.

Dependencies and scope. None. Verification only.

## Task 2 — Simplify text-filter updates

Update only the edited text filter and reset the offset through the existing
query transition. Keep request and loading behavior the same.

- [ ] Search and sector compose with range filters and preserve sorting.
- [ ] Filter changes reset the offset, and Clear filters still clears every filter.
- [ ] Frontend lint, build, and browser filter and cancellation checks pass.

Dependencies and scope. Task 1. Small change in `Screener.tsx`.

## Task 3 — Derive the announced page range once

Compute the start and end from the returned page in the ready state. Preserve
the live region, singular wording, and both empty-state messages.

- [ ] Before editing, verify browser coverage for both empty states. Add focused
  assertions in `frontend/tests/screener.spec.ts` where coverage is missing.
- [ ] First, subsequent, and single-result pages announce the same range and count.
- [ ] Both empty states announce `0–0`. A filter with no matches shows “No stocks
  found.” An out-of-range page shows “No stocks on this page. Use Previous to
  return.” and keeps **Previous** enabled. Frontend lint, build, and browser checks pass.

Dependencies and scope. Tasks 1 and 2. Small change in `Screener.tsx` and
possibly its browser spec.

## Checkpoint after tasks 1–3

- [ ] Compare results against the baseline and verify the screener in Chromium.
- [ ] Build the Docker image and run the README smoke check.

## Task 4 — Clarify sorting in the README

In the sample API section, describe symbol ascending as the default and state
that explicit sorting is applied before pagination.

- [ ] Confirm the wording against `src/stock_vision/stocks/service.py` and the
  existing API sorting tests.

Dependencies and scope. None. Small change in `README.md`.

## Final checkpoint

- [ ] Review the scoped diff and open one PR once the existing PR gate clears.
