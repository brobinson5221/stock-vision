# Stock Vision task checklist

Status: tasks 1-3 complete; PR #2 awaits user review and merge before task 4.

Baseline checks (from repository root): `uv run --locked ruff check .`,
`uv run --locked ruff format --check .`, `uv run --locked pre-commit run --all-files`.
Commands for tools introduced below become executable contracts in their tasks.
Every task includes its coherent implementation and tests in the same commit;
messages below are intent examples and must be regenerated from staged diffs.
File lists are estimates; split work further before exceeding about five files.

## Task 1: Establish project identity

**Description:** Rename template metadata and lock it without changing the Python pin.

**Acceptance criteria:**
- [x] Project name is stock-vision
- [x] locked install succeeds.

**Verification:**
- [x] uv sync --locked; baseline checks.

Completed task 1: renamed metadata and refreshed the lockfile; Python 3.15 is
unchanged. Locked sync and baseline checks passed. At this task's revision, Ruff
found no Python source and pre-commit skipped its Python hooks.

**Dependencies:** None

**Files likely touched:** `pyproject.toml`, `uv.lock`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `chore: initialize stock vision metadata`.

## Task 2: Validate contribution conventions

**Description:** Add CI validation for branch names, all PR commit messages, and existing hooks.

**Acceptance criteria:**
- [x] Valid examples pass and invalid examples fail
- [x] PR base-to-head range is checked
- [x] existing lint/title jobs remain.

**Verification:**
- [x] Run branch validator self-check; exercise Commitizen with valid and invalid messages; inspect Actions.

Two unittest cases cover 16 valid/invalid branch inputs. Commitizen accepted
valid messages and rejected an invalid message. GitHub push and PR checks passed
with branch validation, full PR commit-range validation, and existing hooks.

**Dependencies:** 1

**Files likely touched:** `.github/workflows/checks.yml`, `scripts/check_branch.py`, `tests/test_branch.py`, `.pre-commit-config.yaml`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: validate branch and commit conventions`.

## Task 3: Document the contribution loop

**Description:** Replace template setup instructions with the actual project workflow.

**Acceptance criteria:**
- [x] README covers uv, hooks, commit boundaries and serial PRs
- [x] AGENTS reflects current scope.

**Verification:**
- [x] Follow setup instructions; baseline checks; verify latest Actions.

**Dependencies:** 2

**Files likely touched:** `README.md`, `AGENTS.md`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `docs: describe sequential contribution workflow`.

## Checkpoint: after task 3

- [x] All currently applicable tests, lint and builds pass; no checks bypassed.
- [x] Review diff and verify the capability introduced above manually.
- [x] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

Locked setup, hook installation, Ruff, unittest, pre-commit, and Commitizen checks
passed locally and in GitHub Actions. Scoped self-review found no blockers.
There is no application build yet. Continue with task 4 only after PR #2 merges.

## Task 4: Establish the installable Python package

**Description:** Configure the root project to install `src/stock_vision` with a build backend, FastAPI runtime dependencies, and pytest tooling.

**Acceptance criteria:**
- [ ] Locked install imports `stock_vision` without path overrides.
- [ ] Wheel builds and imports in a clean environment outside the checkout.

**Verification:**
- [ ] uv sync --locked; uv build; clean-environment wheel import check; baseline checks.

**Dependencies:** 3

**Files likely touched:** `pyproject.toml`, `uv.lock`, `src/stock_vision/__init__.py`, `tests/integration/test_installed_package.py`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: establish installable src package`.

## Task 4a: Define the sample-data boundary

**Description:** Add stock and paginated-query schemas plus a source function loading validated package data independently of HTTP.

**Acceptance criteria:**

- [ ] Stock fields, nullable metrics, USD units and sample provenance have explicit contracts.
- [ ] Sample data loads from the installed wheel without relying on the working directory.
- [ ] Page inputs enforce default 50, maximum 100, positive limit, and nonnegative offset.

**Verification:**

- [ ] Unit schema/source tests and wheel package-data check pass.

**Dependencies:** 4

**Files likely touched:** `src/stock_vision/stocks/__init__.py`, `src/stock_vision/stocks/schemas.py`, `src/stock_vision/stocks/source.py`, `src/stock_vision/stocks/sample_stocks.json`, `tests/unit/test_stock_source.py`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `feat: define validated sample stock source`.

## Checkpoint: after tasks 4-4a

- [ ] Installed package and sample resource work outside the checkout.
- [ ] Baseline checks and source/schema tests pass; continue within the same PR.

## Task 4b: Expose paginated stock browsing

**Description:** Compose a feature router into the app, delegating pagination and stable ordering to HTTP-independent screening functions.

**Acceptance criteria:**

- [ ] Health and stock endpoints return validated responses with items, total, limit, offset, and provenance.
- [ ] Multiple pages, invalid bounds, empty/out-of-range pages, and stable ordering are tested.
- [ ] Source dependency can be replaced in tests; request handling does not mutate shared data.

**Verification:**

- [ ] uv run --locked pytest tests; baseline checks; HTTP tests use more than one page of data.

**Dependencies:** 4a

**Files likely touched:** `src/stock_vision/main.py`, `src/stock_vision/stocks/router.py`, `src/stock_vision/stocks/service.py`, `tests/integration/test_stocks_api.py`, `tests/unit/test_screening.py`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `feat: expose paginated sample stock browsing`.

## Task 5: Set up the frontend build

**Description:** Create a minimal React/TypeScript Vite build without unused template assets.

**Acceptance criteria:**
- [ ] Locked npm install works
- [ ] production build passes
- [ ] root page renders.

**Verification:**
- [ ] npm --prefix frontend ci; npm --prefix frontend run build.

**Dependencies:** 4b

**Files likely touched:** `frontend/package.json`, `frontend/package-lock.json`, `frontend/index.html`, `frontend/tsconfig.json`, `frontend/src/main.tsx`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: configure React frontend tooling`.

## Task 6: Connect the screener feature

**Description:** Add a typed feature API client and a screener container, leaving the app shell responsible only for page composition.

**Acceptance criteria:**
- [ ] Screener requests the paginated API through the development proxy.
- [ ] Loading/error/empty states exist and stale requests cannot overwrite current results.
- [ ] App composition is separate from screener request state.

**Verification:**
- [ ] Frontend build; manually test desktop/mobile, API outage and empty response.

**Dependencies:** 5

**Files likely touched:** `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/features/screener/api.ts`, `frontend/src/features/screener/Screener.tsx`, `frontend/vite.config.ts`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: connect the screener feature to the stock API`.

## Task 6a: Display accessible paginated results

**Description:** Add the feature's stock table and next/previous controls with responsive styles.

**Acceptance criteria:**

- [ ] Table shows sample provenance, USD units, and unavailable values explicitly.
- [ ] Pagination preserves queries, reports result counts, and disables invalid navigation.
- [ ] Keyboard operation and narrow layouts work.

**Verification:**

- [ ] Frontend build; manually traverse multiple pages and test API error/empty states at desktop/mobile sizes.

**Dependencies:** 6

**Files likely touched:** `frontend/src/features/screener/StockTable.tsx`, `frontend/src/features/screener/Screener.tsx`, `frontend/src/styles.css`.

**Estimated scope:** Medium (3 files).

**Commit intent:** `feat: display accessible paginated stock results`.

## Checkpoint: after tasks 5-6a

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Continue within the same sample-browsing PR after this internal checkpoint.

## Task 7: Verify source builds in CI

**Description:** Add API tests and frontend lint/type-check/build checks when sources exist.

**Acceptance criteria:**
- [ ] Backend tests plus a wheel build/install smoke check run in CI without source-path overrides
- [ ] frontend checks run from locked dependencies
- [ ] reports remain available after failures.

**Verification:**
- [ ] uv run --locked pytest tests; npm --prefix frontend run lint; npm --prefix frontend run build; inspect Actions.

**Dependencies:** 6a

**Files likely touched:** `.github/workflows/checks.yml`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/eslint.config.js`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: verify API tests and frontend builds`.

## Task 8: Test the browser-to-API path

**Description:** Add a small browser test against the real local API and built frontend.

**Acceptance criteria:**
- [ ] Browser loads sample rows and traverses multiple pages
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

**Description:** Implement the backend half of search/sector filtering; Task 10a completes the same vertical slice.

**Acceptance criteria:**
- [ ] Case-insensitive symbol/name search combines with sector
- [ ] filtering precedes pagination and totals describe all matching results
- [ ] API and unit tests cover combinations and empty matches.

**Verification:**
- [ ] API and unit tests pass; full browser verification follows in Task 10a.

**Dependencies:** 9

**Files likely touched:** Backend step: `src/stock_vision/stocks/schemas.py`, `src/stock_vision/stocks/router.py`, `src/stock_vision/stocks/service.py`, `tests/unit/test_screening.py`, `tests/integration/test_stocks_api.py`. Then complete Task 10a below before the feature is done.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: filter stocks by company and sector`.

## Task 10a: Connect search controls

**Description:** Complete the search/sector slice in the screener feature.

**Acceptance criteria:**

- [ ] Search and sector controls call the typed API and reset offset when changed.
- [ ] Browser tests cover combined filters, empty/reset behavior and stale responses.

**Verification:**

- [ ] Frontend lint/build and focused browser tests pass.

**Dependencies:** 10

**Files likely touched:** `frontend/src/features/screener/api.ts`, `frontend/src/features/screener/Filters.tsx`, `frontend/src/features/screener/Screener.tsx`, `frontend/tests/screener.spec.ts`.

**Estimated scope:** Medium (4 files).

**Commit intent:** `feat: connect stock search controls`.

## Checkpoint: after tasks 10-10a

- [ ] API and browser tests verify filtering before pagination and page reset.
- [ ] Complete the vertical feature within the current PR before starting numeric filters.

## Task 11: Filter financial ranges

**Description:** Implement numerical filter contracts and screening logic; Task 11a completes the same vertical slice.

**Acceptance criteria:**
- [ ] Bounds are inclusive and combine with search
- [ ] malformed or reversed ranges return a consistent validation response
- [ ] null metrics are excluded from active ranges.

**Verification:**
- [ ] API boundary tests for equal/reversed/missing/nonfinite values and filtering before pagination; browser checks follow in Task 11a.

**Dependencies:** 10a

**Files likely touched:** Backend step: `src/stock_vision/stocks/schemas.py`, `src/stock_vision/stocks/router.py`, `src/stock_vision/stocks/service.py`, `tests/unit/test_screening.py`, `tests/integration/test_stocks_api.py`. Then complete Task 11a below.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: filter stocks by financial ranges`.

## Task 11a: Connect financial range controls

**Description:** Complete numerical filtering in the screener feature.

**Acceptance criteria:**

- [ ] Controls preserve search/sector and reset offset when bounds change.
- [ ] Validation errors are visible and null metrics obey the API contract.

**Verification:**

- [ ] Frontend lint/build and combined-filter browser tests pass.

**Dependencies:** 11

**Files likely touched:** `frontend/src/features/screener/api.ts`, `frontend/src/features/screener/Filters.tsx`, `frontend/src/features/screener/Screener.tsx`, `frontend/tests/screener.spec.ts`.

**Estimated scope:** Medium (4 files).

**Commit intent:** `feat: connect financial range controls`.

## Checkpoint: after tasks 11-11a

- [ ] API and browser tests pass for inclusive/reversed bounds and multi-page results.
- [ ] Finish this vertical feature before starting sort controls.

## Task 12: Sort screening results

**Description:** Add validated sort keys and direction with deterministic results.

**Acceptance criteria:**
- [ ] Sorting preserves filters
- [ ] null values sort last both ways
- [ ] ties use symbol consistently across page boundaries.

**Verification:**
- [ ] API and unit sort/tie/null tests pass; browser sort/reset tests follow in Task 12a.

**Dependencies:** 11a

**Files likely touched:** Backend step: `src/stock_vision/stocks/schemas.py`, `src/stock_vision/stocks/router.py`, `src/stock_vision/stocks/service.py`, `tests/unit/test_screening.py`, `tests/integration/test_stocks_api.py`. Then complete Task 12a below.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: sort filtered stock results`.

## Task 12a: Connect sorting controls

**Description:** Complete sorting in the table and verify the complete screening flow.

**Acceptance criteria:**

- [ ] Sort controls preserve filters, reset offset, and support keyboard interaction.
- [ ] Browser tests verify ordering and stable page boundaries, including nulls/ties.

**Verification:**

- [ ] Full API, frontend, browser checks and latest PR CI pass.

**Dependencies:** 12

**Files likely touched:** `frontend/src/features/screener/api.ts`, `frontend/src/features/screener/StockTable.tsx`, `frontend/src/features/screener/Screener.tsx`, `frontend/tests/screener.spec.ts`, `tasks/todo.md`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `feat: connect stock sorting controls`.

## Checkpoint: after tasks 12-12a

- [ ] All currently applicable tests, lint and builds pass; no checks bypassed.
- [ ] Review diff and verify the capability introduced above manually.
- [ ] Open/update the single scoped PR, verify latest CI, and wait for user review and merge before the next PR.

## Task 13: Package the application

**Description:** Build frontend assets and serve them with FastAPI in a final runtime image.

**Acceptance criteria:**
- [ ] Image installs the built Python package and starts without development dependencies or source-path overrides
- [ ] sample page and API work on one origin
- [ ] API errors remain JSON and are not masked by frontend fallback.

**Verification:**
- [ ] docker build -t stock-vision:local .; start image and run smoke assertions for health, API and HTML/assets; stop container.

**Dependencies:** 12a

**Files likely touched:** `Dockerfile`, `.dockerignore`, `src/stock_vision/main.py`, `tests/integration/test_stocks_api.py`, `scripts/smoke_container.py`.

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
