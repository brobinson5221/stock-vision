# Screener cleanup checklist

## Task 1 — Establish the baseline

Run `uv run --locked pytest tests` and the frontend `lint`, `build`, and
`test:e2e` scripts from the README. Record any setup failures separately.

- [x] At `b004431`, 75 Python tests and five Chromium tests passed. Frontend
  lint and build passed. pytest reported the Starlette `httpx` deprecation.

Dependencies and scope. None. Verification only.

## Task 2 — Simplify text-filter updates

Update only the edited text filter and reset the offset through the existing
query transition. Keep request and loading behavior the same.

- [x] Search and sector compose with range filters and preserve sorting.
- [x] Filter changes reset the offset, and Clear filters still clears every filter.
- [x] Frontend lint, build, and browser filter and cancellation checks pass.

Dependencies and scope. Task 1. Small change in `Screener.tsx`.

## Task 3 — Derive the announced page range once

Compute the start and end from the returned page in the ready state. Preserve
the live region, singular wording, and both empty-state messages.

- [x] Added focused assertions for both empty states in
  `frontend/tests/screener.spec.ts` and ran them before editing the screener.
- [x] First, subsequent, and single-result pages announce the same range and count.
- [x] Both empty states announce `0–0`. A filter with no matches shows “No stocks
  found.” An out-of-range page shows “No stocks on this page. Use Previous to
  return.” and keeps **Previous** enabled. Frontend lint, build, and browser checks pass.

Dependencies and scope. Tasks 1 and 2. Small change in `Screener.tsx` and
possibly its browser spec.

## Checkpoint after tasks 1–3

- [x] Compare results against the baseline and verify the screener in Chromium.
- [x] Build the Docker image and run the README smoke check.

## Task 4 — Clarify sorting in the README

In the sample API section, describe symbol ascending as the default and state
that explicit sorting is applied before pagination.

- [x] Confirm the wording against `src/stock_vision/stocks/service.py` and the
  existing API sorting tests.

Dependencies and scope. None. Small change in `README.md`.

## Task 5 — Update the Python test transport

Use `httpx2` in the development dependency group and refresh `uv.lock`.

- [x] `uv run --locked pytest tests -W error` passes all 75 tests, including
  both branch validator tests, without the prior Starlette warning.

Dependencies and scope. Task 1. Small change in `pyproject.toml` and `uv.lock`.

## Task 6 — Remove duplicate validation commands

Keep direct CI Ruff checks, pytest, the PR Commitizen check, and the local
hooks. Remove the CI hooks step that repeats Ruff and drop the separate
`unittest` command from the standard README and AGENTS.md checklists.

- [x] The workflow keeps the direct checks and runs the Chromium suite through
  the existing frontend job. Local pre-commit hooks pass.

Dependencies and scope. Tasks 3 and 5. Changes in the workflow and contributor docs.

## Final checkpoint

- [x] Review the scoped diff and run the local verification commands.
