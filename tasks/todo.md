# Stock Vision task checklist

Status: toolkit PR #7 and tasks 6a–7 in PR #8 have merged. Task 8 is implemented.
Next: task 9 in the browser-test PR. Fresh-session toolkit discovery
remains explicitly unverified.

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
- [x] Locked install imports `stock_vision` without path overrides.
- [x] Wheel builds and imports in a clean environment outside the checkout.

**Verification:**
- [x] uv sync --locked; uv build; clean-environment wheel import check; baseline checks.

Packaging smoke test first failed with ModuleNotFoundError, then passed after
adding the src package and uv_build backend. All three pytest tests and both
legacy unittest cases pass. The wheel installed in a temporary Python 3.15
environment outside the checkout; isolated Python imported stock_vision from
that environment's site-packages, along with FastAPI and Uvicorn. Temporary
environment removed. CI now runs pytest so the packaging test is included.

**Dependencies:** 3

**Files likely touched:** `pyproject.toml`, `uv.lock`, `src/stock_vision/__init__.py`, `tests/integration/test_installed_package.py`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: establish installable src package`.

## Task 4a: Define the sample-data boundary

**Description:** Add stock and paginated-query schemas plus a source function loading validated package data independently of HTTP.

**Acceptance criteria:**

- [x] Stock fields, nullable metrics, USD units and sample provenance have explicit contracts.
- [x] Sample data loads from the installed wheel without relying on the working directory.
- [x] Page inputs enforce default 50, maximum 100, positive limit, and nonnegative offset.

**Verification:**

- [x] Unit schema/source tests and wheel package-data check pass.

Twenty-four tests pass, including invalid and nonfinite metrics, null values,
immutable records, malformed resource data, and page bounds. The rebuilt wheel
loads all six synthetic rows in isolated Python outside the checkout. Temporary
verification environment removed; no HTTP handlers introduced.

**Dependencies:** 4

**Files likely touched:** `src/stock_vision/stocks/__init__.py`, `src/stock_vision/stocks/schemas.py`, `src/stock_vision/stocks/source.py`, `src/stock_vision/stocks/sample_stocks.json`, `tests/unit/test_stock_source.py`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `feat: define validated sample stock source`.

## Checkpoint: after tasks 4-4a

- [x] Installed package and sample resource work outside the checkout.
- [x] Baseline checks and source/schema tests pass; continue within the same PR.

## Task 4b: Expose paginated stock browsing

**Description:** Compose a feature router into the app, delegating pagination and stable ordering to HTTP-independent screening functions.

**Acceptance criteria:**

- [x] Health and stock endpoints return validated responses with items, total, limit, offset, and provenance.
- [x] Multiple pages, invalid bounds, empty/out-of-range pages, and stable ordering are tested.
- [x] Source dependency can be replaced in tests; request handling does not mutate shared data.

**Verification:**

- [x] uv run --locked pytest tests; baseline checks; HTTP tests use more than one page of data.

All 40 tests pass. HTTP tests traverse 105 unsorted rows over three pages using
a dependency override, check bounds/empty sources, and verify unchanged input.
Baseline checks and wheel build pass. TestClient emits the upstream httpx
deprecation warning; tests pass without suppressing it.

**Dependencies:** 4a

**Files likely touched:** `src/stock_vision/main.py`, `src/stock_vision/stocks/router.py`, `src/stock_vision/stocks/service.py`, `tests/integration/test_stocks_api.py`, `tests/unit/test_screening.py`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `feat: expose paginated sample stock browsing`.

## Task 5: Set up the frontend build

**Description:** Create a minimal React/TypeScript Vite build without unused template assets.

**Acceptance criteria:**
- [x] Locked npm install works
- [x] production build passes
- [x] root page renders.

**Verification:**
- [x] npm --prefix frontend ci; npm --prefix frontend run build.

Verified with Node 24.14.1/npm 11.19.1. Production build type-checks with strict
TypeScript, and browser assertions confirmed the page heading and sample label
with no console errors. Browser session closed and verification server stopped.
No template assets or API connection added; frontend CI follows in task 7.

**Dependencies:** 4b

**Files likely touched:** `frontend/package.json`, `frontend/package-lock.json`, `frontend/index.html`, `frontend/tsconfig.json`, `frontend/src/main.tsx`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `build: configure React frontend tooling`.

## Task 6: Connect the screener feature

**Description:** Add a typed feature API client and a screener container, leaving the app shell responsible only for page composition.

**Acceptance criteria:**
- [x] Screener requests the paginated API through the development proxy.
- [x] Loading/error/empty states exist and stale requests cannot overwrite current results.
- [x] App composition is separate from screener request state.

**Verification:**
- [x] Frontend build; manually test desktop/mobile, API outage and empty response.

Browser assertions verified six real API rows through Vite, 375px layout without
overflow, loading/empty/malformed-response states, API outage and recovery.
A controlled fetch that ignored aborts resolved old requests after the newest
result; the newest result stayed visible. Browser closed and both servers stopped.
No dependencies added. Table and pagination controls remain task 6a.

**Dependencies:** 5

**Files likely touched:** `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/features/screener/api.ts`, `frontend/src/features/screener/Screener.tsx`, `frontend/vite.config.ts`.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `feat: connect the screener feature to the stock API`.

## Task T1: Inventory the repository toolkit

**Description:** Inventory the selected skill packages and instruction sources
from the plan before copying. Preserve the four existing repository skills.

**Acceptance criteria:**

- [x] `.agents/toolkit.md` records sources, versions/revisions, licenses, destinations, required support files, and external-tool prerequisites.
- [x] Review content and identify personal paths, cross-package references, conflicting rules, and any redistribution gaps.
- [x] Expand T2/T3 into named batches of about five files before copying; keep required skill support files together and record any larger atomic package.

**Verification:** Inspect source packages and license files; compare existing
local copies; confirm each selected resource has a destination and source record.

Inventory: [repository toolkit](../.agents/toolkit.md). Six skill sources and
13 instruction snapshots are identified; four existing skill packages remain
untouched. Source hashes pin snapshots with incomplete adaptation history.
Planning/frontend cross-package references must be bundled locally. Readme
attribution and Vercel packaging-version/notice details must be recorded in T2.
Large web/React documentation packages are explicit atomic-copy exceptions;
this inventory does not claim a full independent security audit or discovery test.

**Dependencies:** 6; user-requested plan amendment.

**Files likely touched:** `.agents/toolkit.md`, `tasks/todo.md`.

**Estimated scope:** Small (2 files).

**Commit intent:** `docs: inventory repository agent toolkit`.

## Task T2: Add the selected local skill packages

**Description:** Copy the complete, reviewed packages in T1's named batches.
Add `planning-and-task-breakdown`, `conventional-branch`, `frontend-ui-engineering`,
`create-readme`, `modern-web-guidance`, and `react-best-practices` under
`.agents/skills/`. Retain existing `commit-message-storyteller`, `ponytail-review`,
`pr`, and `create-pr` rather than installing duplicates.

**Acceptance criteria:**

- [x] Each package includes SKILL.md and the support files it actually requires, with license/attribution preserved.
- [x] Personal absolute paths are adapted; required references resolve locally or name an explicit external prerequisite.
- [x] No unrelated skills, plugin caches, credentials, machine config, or optional agent registrations are copied.

**Verification:** Compare each package with its recorded source; inspect all
adaptations; validate metadata, links, and referenced scripts. Do not execute
copied helpers until their content and side effects have been reviewed.

Completed T2a–T2f in six focused commits. All six entrypoints pass the structural
skill validator; 305 copied package files include required references, licenses,
and source notices. Supporting files were byte-compared against their source
snapshots. The existing four skills are unchanged. Web-guidance CLI commands were not run;
web guidance is local-first with its optional CLI version pinned. Root routing
and fresh-session discovery remain T4. Full Git whitespace checking flags
inherited upstream document formatting; authored entrypoints/source notes pass.

**Dependencies:** T1.

**Files likely touched:** T1's named batches under `.agents/skills/` and source records.

**Estimated scope:** Repeat focused batches; one coherent commit per package/batch.

Execute these named batches with the shared acceptance/verification above and
the exact source records in `.agents/toolkit.md`:

| Batch | Package and required files | Scope |
| --- | --- | --- |
| T2a | planning-and-task-breakdown: entry, definition-of-done reference, LICENSE, SOURCE.md | 4 files |
| T2b | conventional-branch: complete package with source/license/UI metadata | 4 files |
| T2c | frontend-ui-engineering: entry, accessibility reference, LICENSE, SOURCE.md | 4 files |
| T2d | create-readme: entry, upstream license, explicit adaptation/source note | 3 files; finish attribution first |
| T2e | modern-web-guidance: entry plus 210 guides, LICENSE, SOURCE.md | 213 files; documented atomic-package exception |
| T2f | react-best-practices: entry, compiled guide, 72 rules, UI metadata, license/source notice | 77 files; documented atomic-package exception |

T2a–T2f run sequentially. Required supporting content stays in the same package;
do not split a package into commits with broken references just to hit a count.

**Commit intent:** `chore: vendor selected project skills` (scope per batch).

## Task T3: Add repository-local instruction files

**Description:** Copy the plan's applicable instruction files into
`.agents/instructions/` in T1's named batches, preserving attribution and adapting
references to repository paths.

Required topics: `context-engineering`, `context7`, `self-explanatory-code-commenting`,
`update-docs-on-code-change`, `code-review-generic`, `markdown`,
`github-actions-ci-cd-best-practices`, `codexer`, `html-css-style-color-guide`,
`playwright-typescript`, `containerization-docker-best-practices`, `instructions`,
and `prompt` (each named `<topic>.instructions.md`).

**Acceptance criteria:**

- [x] All selected instruction files and required references are present and portable.
- [x] Existing project conventions and user authorization boundaries remain intact.
- [x] Source records explain adaptations; files do not require the author's home directory or duplicate the full global router.

**Verification:** Check paths and attribution, review conflicting instructions,
and compare every copied file against its recorded source.

Completed T3a–T3c as three focused commits: 13 instructions and a shared upstream
MIT license. Source hashes matched the inventory before copying. Eleven files
are byte-identical; context7 and codexer only replace global Context7 references
with root AGENTS.md. Expected-content comparisons, attribution, personal-path,
file-count, and license checks passed. Root routing remains T4; files are not
claimed automatically loaded merely because they exist.

**Dependencies:** T2.

**Files likely touched:** T1's named instruction batches and source records.

**Estimated scope:** Repeat batches of about 3-5 files with focused commits.

| Batch | Instruction topics (each `<topic>.instructions.md`) | Scope |
| --- | --- | --- |
| T3a | context-engineering, context7, self-explanatory-code-commenting, update-docs-on-code-change; shared MIT LICENSE | 5 files |
| T3b | code-review-generic, markdown, github-actions-ci-cd-best-practices, codexer, html-css-style-color-guide | 5 files |
| T3c | playwright-typescript, containerization-docker-best-practices, instructions, prompt | 4 files |

T3a–T3c run sequentially with the shared acceptance/verification above. Preserve
source attribution and adapt the global-router reference in context7.

**Commit intent:** `docs: add project instruction guidance` (scope per batch).

## Task T4: Route and verify the local toolkit

**Description:** Wire conditional repository-relative instruction links into
AGENTS.md and update plan/README references to the actual local packages.

**Acceptance criteria:**

- [x] AGENTS.md tells agents when to read each instruction and how to use local skills, without requiring global copies.
- [x] README/toolkit records explain prerequisites and deliberate update procedure.
- [x] Representative backend, frontend, CI, and documentation tasks resolve their guidance; unrelated tasks do not load the whole toolkit.
- [x] Fresh-session local skill discovery is tested where available, with any untested runtime behavior reported explicitly.

**Verification:** Run a focused local path/reference check; inspect representative
task routing and missing-tool behavior; run baseline checks. A file existing is
not proof of fresh-session discovery. Keep one open PR and leave merge to the user.

Local link/route checks and all ten skill metadata validations passed. Manual
routing walkthroughs cover backend, frontend, CI, README, instruction authoring,
unrelated questions, and missing Context7. Fresh-session automatic discovery and
selection were not tested; no new Codex session was started, and the inventory
records this limit rather than inferring discovery from file presence.

**Dependencies:** T3.

**Files likely touched:** `AGENTS.md`, `README.md`, `.agents/toolkit.md`, `tasks/plan.md`, `tasks/todo.md`.

**Estimated scope:** Medium (5 files).

**Commit intent:** `docs: route and verify repository agent toolkit`.

## Checkpoint: after T1-T4

- [x] Selected skills and instructions are tracked locally with portable references and source/license records.
- [x] Required support resources resolve; runtime/tool prerequisites and unverified discovery are documented.
- [x] Baseline checks pass; submit the toolkit PR and wait for user merge before task 6a.

## Task 6a: Display accessible paginated results

**Description:** Add the feature's stock table and next/previous controls with responsive styles.

**Acceptance criteria:**

- [x] Table shows sample provenance, USD units, and unavailable values explicitly.
- [x] Pagination preserves queries, reports result counts, and disables invalid navigation.
- [x] Keyboard operation and narrow layouts work.

**Verification:**

- [x] Frontend build; manually traverse multiple pages and test API error/empty states at desktop/mobile sizes.

Browser assertions checked six live API rows, USD/null display, and three-page
navigation over a 105-row response fixture. Query parameters were preserved;
keyboard Enter and horizontal scrolling worked. Layouts at 320/768/1024/1440px
had no page overflow. Text contrast measured at least 6.48:1; border/focus at
least 4.75:1. Empty/out-of-range pages, simulated 503 errors, and recovery passed
on desktop/mobile. Native semantics and focus were checked; no screen-reader
session was run. Verification browser and servers were closed.

**Dependencies:** 6, T4

**Files likely touched:** `frontend/src/features/screener/StockTable.tsx`, `frontend/src/features/screener/Screener.tsx`, `frontend/src/styles.css`.

**Estimated scope:** Medium (3 files).

**Commit intent:** `feat: display accessible paginated stock results`.

## Checkpoint: after tasks 5-6a

- [x] All currently applicable tests, lint and builds pass; no checks bypassed.
- [x] Review diff and verify the capability introduced above manually.
- [x] Continue within the same sample-browsing PR after this internal checkpoint.

## Task 7: Verify source builds in CI

**Description:** Add API tests and frontend lint/type-check/build checks when sources exist.

**Acceptance criteria:**

- [x] Backend tests plus a wheel build/install smoke check run in CI without source-path overrides.
- [x] Frontend checks run from locked dependencies.
- [x] The workflow uploads pytest reports even when tests fail.

**Verification:**

- [x] Verify pytest, an isolated wheel install, and clean frontend install, lint, and build locally.
- Inspect the latest Actions run and its `pytest-results` artifact before review.

**Dependencies:** 6a

**Implementation:** The Checks workflow adds the wheel smoke check, JUnit report,
and Node.js job. `frontend/package.json` runs Oxlint without a separate config file.

**Estimated scope:** Medium (3-5 files maximum; task 1 is small).

**Commit intent:** `ci: verify API tests and frontend builds`.

## Task 8: Test the browser-to-API path

**Description:** Add a small browser test against the real local API and built frontend.

**Acceptance criteria:**
- [x] Browser loads sample rows and traverses multiple pages from the real API.
- [x] Reload recovers after a single HTTP 503.
- [x] Failure traces are retained and services cleaned up.

**Verification:**
- [x] `npm --prefix frontend run test:e2e` passes. A deliberate local assertion
  failure retained a trace with network and DOM snapshots. Both ports were
  released after the test run.

**Dependencies:** 7

**Implementation:** Playwright starts Vite preview and `tests/e2e_server.py`,
which extends the packaged sample through FastAPI's dependency override.
The frontend CI job installs Chromium, runs the test, and uploads failure traces.

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
