# Dataset metadata hardening checklist

## Task 1 — Enforce the sector length boundary

Share the existing 100-character maximum across stock dataset validation and
the `sector` query parameter. Preserve trimming and case-insensitive matching.

- [x] A sector of 100 characters validates and can be used to filter its stock.
- [x] A sector of 101 characters fails dataset validation and returns HTTP 422
  when sent as a query. The dataset regression test failed before the fix.
- [x] All 71 focused tests passed. Ruff lint and format checks passed.

Scope includes `schemas.py` and the stock source and API tests. No dependencies
beyond the merged metadata PR. After verification, use commit-message-storyteller
to prepare `fix: align stock and filter sector length limits` from the staged diff.

## Task 2 — Cover first-load recovery in Chromium

Use a new browser test that returns HTTP 503 for the first stock request only.

- [x] The error appears and Sector is disabled until a response succeeds.
- [x] Reload stocks restores the source and sector options. Selecting a sector
  filters the results.
- [x] The focused browser test, frontend lint, and production build passed.

Scope is `frontend/tests/screener.spec.ts`. After Task 1, verify and commit this
independent test with commit-message-storyteller. Proposed subject is
`test: cover sector recovery after an initial load failure`.

## PR checkpoint

- [x] All 78 Python tests, seven Chromium tests, benchmark smoke, and Docker smoke passed locally.
- [ ] Check the scoped diff and validate the commit range with Commitizen.
- [ ] Use `pr` for the description and `create-pr` to publish one PR and verify
  its latest CI. The existing Python and frontend jobs run these tests.
- [ ] Leave merging to the user. Fetch updated `origin/main` before the next branch.
