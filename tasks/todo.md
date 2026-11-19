# Stock Vision task checklist

Status: proposed; implementation awaits plan review. Task list target: this file.

Baseline checks (from repository root): `uv run --locked ruff check .`,
`uv run --locked ruff format --check .`, `uv run --locked pre-commit run --all-files`.
Commands for tools introduced below become executable contracts in their tasks.
Every task includes its coherent implementation and tests in the same commit;
messages below are intent examples and must be regenerated from staged diffs.
File lists are estimates; split work further before exceeding about five files.

## Task 1: Establish project identity

**Description:** Rename template metadata and lock it without changing the Python pin.

**Acceptance criteria:**
- [ ] Project name is stock-vision
- [ ] locked install succeeds.

**Verification:**
- [ ] uv sync --locked; baseline checks.

**Dependencies:** None

**Files likely touched:** `pyproject.toml`, `uv.lock`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `chore: initialize stock vision metadata`.

## Task 2: Validate contribution conventions

**Description:** Add CI validation for branch names, all PR commit messages, and existing hooks.

**Acceptance criteria:**
- [ ] Valid examples pass and invalid examples fail
- [ ] PR base-to-head range is checked
- [ ] existing lint/title jobs remain.

**Verification:**
- [ ] Run branch validator self-check; exercise Commitizen with valid and invalid messages; inspect Actions.

**Dependencies:** 1

**Files likely touched:** `.github/workflows/checks.yml`, `scripts/check_branch.py`, `tests/test_branch.py`, `.pre-commit-config.yaml`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: validate branch and commit conventions`.

## Task 3: Document the contribution loop

**Description:** Replace template setup instructions with the actual project workflow.

**Acceptance criteria:**
- [ ] README covers uv, hooks, commit boundaries and serial PRs
- [ ] AGENTS reflects current scope.

**Verification:**
- [ ] Follow setup instructions; baseline checks; verify latest Actions.

**Dependencies:** 2

**Files likely touched:** `README.md`, `AGENTS.md`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `docs: describe sequential contribution workflow`.

## Checkpoint: after task 3

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

## Task 4: Expose tested sample stocks

**Description:** Add FastAPI and a deterministic small dataset with an explicit API contract.

**Acceptance criteria:**
- [ ] Health and stocks endpoints return validated responses
- [ ] metadata labels sample USD data
- [ ] nullable fields and fixture schema are tested.

**Verification:**
- [ ] uv run --locked pytest backend; baseline checks; locked install.

**Dependencies:** 3

**Files likely touched:** `pyproject.toml`, `uv.lock`, `backend/main.py`, `backend/sample_stocks.json`, `backend/test_main.py`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: expose sample stocks through FastAPI`.

## Task 5: Set up the frontend build

**Description:** Create a minimal React/TypeScript Vite build without unused template assets.

**Acceptance criteria:**
- [ ] Locked npm install works
- [ ] production build passes
- [ ] root page renders.

**Verification:**
- [ ] npm --prefix frontend ci; npm --prefix frontend run build.

**Dependencies:** 4

**Files likely touched:** `frontend/package.json`, `frontend/package-lock.json`, `frontend/index.html`, `frontend/tsconfig.json`, `frontend/src/main.tsx`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: configure React frontend tooling`.

## Task 6: Show the sample stock table

**Description:** Connect a small React view to the API through the development proxy.

**Acceptance criteria:**
- [ ] Accessible table shows sample label and USD units
- [ ] loading/error/empty states exist
- [ ] missing values are unavailable.

**Verification:**
- [ ] Frontend build; manually test desktop/mobile, API outage and empty response.

**Dependencies:** 5

**Files likely touched:** `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/styles.css`, `frontend/vite.config.ts`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: display sample stocks in the browser`.

## Checkpoint: after task 6

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Continue within the same sample-browsing PR after this internal checkpoint.

## Task 7: Verify source builds in CI

**Description:** Add API tests and frontend lint/type-check/build checks when sources exist.

**Acceptance criteria:**
- [ ] Backend tests run in CI
- [ ] frontend checks run from locked dependencies
- [ ] reports remain available after failures.

**Verification:**
- [ ] uv run --locked pytest backend; npm --prefix frontend run lint; npm --prefix frontend run build; inspect Actions.

**Dependencies:** 6

**Files likely touched:** `.github/workflows/checks.yml`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/eslint.config.js`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: verify API tests and frontend builds`.

## Task 8: Test the browser-to-API path

**Description:** Add a small browser test against the real local API and built frontend.

**Acceptance criteria:**
- [ ] Browser loads sample rows
- [ ] error recovery is tested
- [ ] failure traces are retained and services cleaned up.

**Verification:**
- [ ] npm --prefix frontend run test:e2e; inspect a deliberate local failure artifact.

**Dependencies:** 7

**Files likely touched:** `frontend/playwright.config.ts`, `frontend/tests/screener.spec.ts`, `frontend/package.json`, `frontend/package-lock.json`, `.github/workflows/checks.yml`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `test: verify sample stock browsing end to end`.

## Task 9: Document the runnable sample

**Description:** Record exact launch/test commands and sample limitations.

**Acceptance criteria:**
- [ ] Fresh checkout instructions launch both processes
- [ ] AGENTS and checklist describe actual commands and state.

**Verification:**
- [ ] Follow run instructions; baseline, API, frontend and browser checks; latest CI.

**Dependencies:** 8

**Files likely touched:** `README.md`, `AGENTS.md`, `tasks/todo.md`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `docs: document the sample screener`.

## Checkpoint: after task 9

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

## Task 10: Search by company and sector

**Description:** Add one complete query/filter slice across API and UI.

**Acceptance criteria:**
- [ ] Case-insensitive symbol/name search combines with sector
- [ ] no results can be reset
- [ ] API and browser tests cover combinations.

**Verification:**
- [ ] API tests; frontend lint/build; browser search/sector flow.

**Dependencies:** 9

**Files likely touched:** `backend/main.py`, `backend/test_main.py`, `frontend/src/App.tsx`, `frontend/tests/screener.spec.ts`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: filter stocks by company and sector`.

## Task 11: Filter financial ranges

**Description:** Add market-cap and P/E bounds across API and UI.

**Acceptance criteria:**
- [ ] Bounds are inclusive and combine with search
- [ ] malformed or reversed ranges are rejected visibly
- [ ] null metrics are excluded from active ranges.

**Verification:**
- [ ] API boundary tests for equal/reversed/missing/nonfinite values; browser combined-filter flow; frontend checks.

**Dependencies:** 10

**Files likely touched:** `backend/main.py`, `backend/test_main.py`, `frontend/src/App.tsx`, `frontend/tests/screener.spec.ts`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: filter stocks by financial ranges`.

## Task 12: Sort screening results

**Description:** Add validated sort keys and direction with deterministic results.

**Acceptance criteria:**
- [ ] Sorting preserves filters
- [ ] null values sort last both ways
- [ ] ties use symbol and keyboard controls work.

**Verification:**
- [ ] API sort/tie/null tests; browser sort/reset test; full source checks and CI.

**Dependencies:** 11

**Files likely touched:** `backend/main.py`, `backend/test_main.py`, `frontend/src/App.tsx`, `frontend/tests/screener.spec.ts`, `tasks/todo.md`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: sort filtered stock results`.

## Checkpoint: after task 12

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

## Task 13: Package the application

**Description:** Build frontend assets and serve them with FastAPI in a final runtime image.

**Acceptance criteria:**
- [ ] Image starts without development dependencies
- [ ] sample page and API work on one origin
- [ ] API errors remain JSON and are not masked by frontend fallback.

**Verification:**
- [ ] docker build -t stock-vision:local .; start image and run smoke assertions for health, API and HTML/assets; stop container.

**Dependencies:** 12

**Files likely touched:** `Dockerfile`, `.dockerignore`, `backend/main.py`, `backend/test_main.py`, `scripts/smoke_container.py`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: package the screener with Docker`.

## Task 14: Verify the runtime image in Actions

**Description:** Build and test the final container in CI.

**Acceptance criteria:**
- [ ] CI tests the image it built
- [ ] waits are bounded
- [ ] container logs are retained on failure and cleanup always runs.

**Verification:**
- [ ] Run container job; verify health/API/static assets; inspect latest Actions.

**Dependencies:** 13

**Files likely touched:** `.github/workflows/docker.yml`, `scripts/smoke_container.py`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: smoke test the Docker runtime`.

## Task 15: Complete the local runbook

**Description:** Document container usage and the failure-to-regression workflow.

**Acceptance criteria:**
- [ ] README covers source/container startup and troubleshooting
- [ ] task status matches evidence
- [ ] sample limitations are prominent.

**Verification:**
- [ ] Follow fresh checkout runbook; all source/browser/container checks; verify required checks on latest PR revision.

**Dependencies:** 14

**Files likely touched:** `README.md`, `AGENTS.md`, `tasks/plan.md`, `tasks/todo.md`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `docs: document verified screener operation`.

## Checkpoint: after task 15

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

## Failure-driven work during every task

- [ ] For observed failures, retain the logs and reproduce the cause.
- [ ] Add a focused regression test; extend CI only when coverage is missing.
- [ ] Demonstrate the check fails before the fix and passes after it.
- [ ] Record unavailable checks honestly; infrastructure outages are not code passes.
