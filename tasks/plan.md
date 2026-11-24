# Implementation Plan: Stock Vision

## Overview

Build a stock screener with a Python/FastAPI API and a React/TypeScript frontend.
Start with clearly labeled, deterministic sample data, as selected by the user.
Ship small verified changes through one open PR at a time. This document is a
proposal for review; no application implementation is included in the planning PR.

## Current state

Tasks 1–9, including 4a/4b and 6a, are implemented: the Python 3.15 src package exposes
a sample browsing API, and the React/TypeScript frontend displays a paginated table.
Forty Python tests pass; locked frontend install/build and request-state browser
checks have passed locally. CI checks Python tests, Ruff, hooks, branch/commit
conventions, PR titles, clean wheel installation, and the locked frontend build.
The browser test covers the built frontend and real API pagination, with traces
retained on failure. The Docker image runs the installed backend wheel and
serves the built frontend from the same origin. The Docker smoke workflow tests
the built image and retains container logs on failure. The local
toolkit is copied and routed in merged PR #7;
fresh-session automatic discovery remains unverified.

## Architecture decisions

- Keep one repository: an installable `src/stock_vision/` Python package,
  separate root `tests/`, and `frontend/src/` for React. Root `pyproject.toml`
  and `uv.lock` own Python tooling; frontend has its own npm lockfile.
- Serve a small checked-in sample dataset through `GET /api/stocks`. Include
  symbol, name, sector, USD price, USD market capitalization, and nullable P/E.
  Mark API metadata and the screen as sample data, not live quotes.
- Use an explicit response model and validate query inputs at the API boundary.
  Missing financial values remain null and display as unavailable, never zero.
- Start with a table, loading/error/empty states, then add search, sector,
  market-cap bounds, P/E bounds, and sorting through complete API-to-UI slices.
  Apply combined filters with AND; numerical bounds are inclusive. Exclude
  unknown values from active numeric filters; sort nulls last in both directions.
- Keep filtering on the backend. Use a deterministic symbol tie-break for sorting.
  Return an envelope with items, total, limit, offset, and sample provenance.
  Bound page size from the first endpoint (default 50, maximum 100); apply
  filtering and stable sorting before pagination. A database can come later.
- Use pytest with FastAPI TestClient for API checks and browser tests for the
  actual frontend/API flow. Add frontend unit tests only for isolated logic that
  browser tests do not adequately cover.
- Package the frontend build and Python API in a multi-stage Docker image, with
  FastAPI serving the built assets on the same origin. Use a development proxy
  for local frontend work. Confirm exact Docker and Vite setup with current docs
  during implementation. Do not use the development server as the runtime image.
- Keep Python 3.15 unless a reproducible dependency compatibility failure requires
  a deliberate version change across the pin, metadata, lockfile, CI, and image.

## Source layout and growth boundaries

Build one modular application, organized by feature. Create each module when
its task introduces real behavior; this tree is the target, not empty scaffolding.

```text
pyproject.toml                  # package/build configuration and Python tools
uv.lock
src/stock_vision/
  __init__.py
  main.py                      # app creation, router registration, asset mounting
  stocks/
    __init__.py
    router.py                  # HTTP validation and response mapping
    schemas.py                 # stock, query, and paginated response contracts
    service.py                 # filtering, ordering, pagination; no HTTP objects
    source.py                  # sample loading; future provider integration point
    sample_stocks.json         # packaged deterministic data
tests/
  unit/                        # screening rules and source validation
  integration/                 # HTTP contracts and installed-package smoke checks
frontend/
  src/
    main.tsx                   # React bootstrap
    App.tsx                    # page composition only
    features/screener/
      api.ts                   # typed stock requests and API error handling
      Screener.tsx             # query state and request lifecycle
      StockTable.tsx           # accessible rows and pagination controls
      Filters.tsx              # search, sector and numerical controls when added
    styles.css
  tests/                       # browser flows
scripts/                       # development and CI utilities, not application code
tasks/                         # plan and implementation checklist
.github/workflows/
.agents/
  skills/                      # complete selected skill packages, including support files
  instructions/                # task-specific instructions routed from AGENTS.md
  toolkit.md                   # sources, revisions, licenses, and update procedure
Dockerfile
.dockerignore
```

### Dependency rules

- `main.py` composes modules. Stock routes call screening functions and an
  injectable source function; source code and screening logic never import
  routers. Keep the seam a simple function until multiple implementations need
  a formal interface. No generic repository classes or dependency container.
- The frontend uses the HTTP contract, never sample files or backend internals.
  Keep feature-specific components inside `features/screener/`; extract shared
  components only when a second feature actually reuses them.
- Python tests import `stock_vision` from the installed package. Configure a
  build backend and package data explicitly; no `sys.path` edits or `PYTHONPATH`
  workaround. CI builds a wheel and smoke-tests it outside the source checkout,
  including access to the packaged sample data. Docker installs that package.
- Keep requests stateless: immutable sample data, request-local filter state,
  no user state or correctness-critical cache in process globals. Cancel stale
  frontend requests so old responses cannot replace newer filter results.

### Scaling path and verification

Bound responses now and test page limits, empty/out-of-range pages, stable ties,
null handling, and combined filters across pages. Reset pagination when filters
change. Tests must use more than one page of data. The sample implementation may
scan its small in-memory dataset; bounded output does not imply bounded query cost.

Before connecting a large/live universe, implement the source boundary with
indexed database queries that perform filtering, sorting, and pagination. Add
ingestion and provider rate-limit handling outside request handlers when needed.
Use shared persistence/cache only once their consistency and freshness rules are
defined. Stateless API instances can then be replicated behind a load balancer;
static assets can move to a CDN without changing the frontend API contract.

Before claiming production capacity, choose an explicit universe size, request
rate, concurrency, and latency target; measure latency percentiles, errors, and
memory against representative data. No capacity target or load result is assumed
for the sample version. Microservices, queues, Kubernetes, and distributed caches
are not prerequisites for this structure.

## Sequential delivery and commits

Branches follow `codex/<type>/<short-kebab-description>`; commits and PR titles
follow Conventional Commits. Allowed types: feat, fix, docs, style, refactor,
perf, test, build, ci, chore, revert. Validate the whole PR commit range in CI.

Use the requested commit-message-storyteller skill against the staged diff for
every commit. Keep feature code and its tests together. Commit independently
reviewable tooling, UI, CI, and documentation changes separately; never split
working code merely to increase the count. Preserve hooks and unrelated edits.

Use the repository pr and create-pr skills for every submission. At each gate:
finish checks, inspect the scoped diff, open the single PR, verify its latest CI,
and leave merging to the user. Do not start the next PR until this one is merged;
fetch updated main and branch from it. Do not stack PRs or force-push history.

The current agent guidance calls for squash merging. This preserves a linear
main history but collapses the individual development commits there; those
commits remain reviewable in the PR. Keeping every commit on main would require
an explicit switch to rebase merging and updated repository guidance.

## Task list and PR gates

Detailed acceptance criteria, verification, dependencies, and file scope are in
[todo.md](todo.md). Commands for future tools are proposed contracts, not claims
that those tools or scripts already exist.

| Order | PR boundary | Tasks | Intended commits |
| --- | --- | --- | --- |
| 0 | Plan and review | This plan | Architecture plan; executable task checklist |
| 1 | Development conventions | 1-3 | Project identity; commit/branch CI; contributor guide |
| 2 | Sample browsing foundations (merged PRs #3-5) | 4-6, including 4a/4b | Package; source; API; connected frontend |
| 3 | Repository toolkit (PR #7) | T1-T4 | Inventory; skill packages; instruction batches; routing verification |
| 4 | Complete sample browsing | 6a-9 | Paginated table; source/browser CI; sample runbook |
| 5 | Screen stocks | 10-12, including 10a/11a/12a | Search/sector slice; numeric filter slice; sorting slice |
| 6 | Run the verified container | 13-15 | Container + smoke check; Docker CI; runbook |

Checkpoints after every two or three tasks verify progress within a PR; the PR
boundary is the human review/merge gate. A task checkpoint is not another PR.
Lettered tasks split larger work into focused commits while preserving existing
task identifiers. Finish each API-to-UI feature pair before beginning the next.

## Toolkit by phase

Ship repository-local copies of the selected skills and instructions below so
a checkout carries its working guidance. Tasks T1-T4 in [todo.md](todo.md) are
implemented in toolkit PR #7, following merged plan amendment #6. Root
[AGENTS.md](../AGENTS.md) routes matching tasks to local files. Toolkit file,
metadata, and routing checks are recorded in [the inventory](../.agents/toolkit.md);
fresh-session automatic discovery remains unverified. PR #7 has merged; task 6a
and build verification have merged in PR #8. Browser coverage merged in PR #9.
The runnable sample guide merged in PR #10, and search and sector filtering
merged in PR #11. Tasks 11 and 11a add financial ranges to the API and browser.
Financial ranges merged in PR #12. Tasks 12 and 12a add API and table sorting.
Sorting merged in PR #13. Docker packaging merged in PR #14. Task 14 adds
Docker smoke checks, and Task 15 finishes the runbook.

Keep skills in `.agents/skills/<name>/` and instructions in
`.agents/instructions/`. Preserve the four existing repository skills and their
user edits; add only missing packages. Copy required references, scripts, assets,
agent metadata, and license/attribution files along with each `SKILL.md`.
Do not copy unrelated global skills or the entire plugin cache.

Inventory the installed source versions first and review content before use.
Record upstream source URLs, revisions/versions, licenses, local destinations,
support-file dependencies, and deliberate adaptations in `.agents/toolkit.md`.
Respect redistribution terms; flag unavailable or non-redistributable resources
instead of silently substituting or claiming them installed. Rewrite personal
absolute paths and required cross-package links into portable repository-relative
references. Keep instructions in one owning file and route them conditionally
from root `AGENTS.md`; separate instruction files are not automatically loaded.

The local toolkit is a reviewed snapshot. Update it deliberately, with source
diffs and validation; do not add automatic synchronization. Skills requiring MCP
connections, plugins, CLIs, or credentials must document those prerequisites.
Vendoring their guidance does not provision tools or grant permissions.

### Shared workflow

| When | Resource | Purpose |
| --- | --- | --- |
| Revising the plan | [planning-and-task-breakdown](../.agents/skills/planning-and-task-breakdown/SKILL.md) | Keep tasks, dependencies, acceptance criteria, and PR gates aligned. |
| Starting a branch | [conventional-branch](../.agents/skills/conventional-branch/SKILL.md) | Apply this project's `codex/<type>/<description>` policy and validate the Git ref. |
| Each commit | [commit-message-storyteller](../.agents/skills/commit-message-storyteller/SKILL.md) | Base a coherent Conventional Commit on the staged diff. |
| Reviewing code/configuration | [ponytail-review](../.agents/skills/ponytail-review/SKILL.md) | Check connected code for defects, missing tests, and unnecessary complexity. |
| Each PR | [pr](../.agents/skills/pr/SKILL.md) and [create-pr](../.agents/skills/create-pr/SKILL.md) | Provide evidence, follow latest CI, and leave merging to the user. |

Apply `context-engineering.instructions.md` when gathering context and
`context7.instructions.md` for library/tool documentation. Code changes use
`self-explanatory-code-commenting.instructions.md` and
`update-docs-on-code-change.instructions.md`; scoped reviews use
`code-review-generic.instructions.md`. Markdown edits use
`markdown.instructions.md`. All filenames in this paragraph resolve in the local
`.agents/instructions/` directory. Documentation-only reviews need link and command
accuracy checks, not an application test suite.

### Implementation stages

| Phase / tasks | Skills and instructions to load | Intended use |
| --- | --- | --- |
| Conventions, tasks 1-3 | `github-actions-ci-cd-best-practices.instructions.md` | Branch/commit checks, hooks in CI, action pins, and existing required checks. |
| Backend, task 4 and tasks 10-12 | `codexer.instructions.md` plus Context7 guidance | Python/FastAPI dependencies, response contracts, validation, and focused tests. |
| Frontend, tasks 5-6a and tasks 10-12 | Local skills `frontend-ui-engineering`, `modern-web-guidance`, `react-best-practices`; `html-css-style-color-guide.instructions.md` | Accessible tables and controls, responsive layout, contrast, request states, and React review. |
| Source and browser CI, tasks 7-8 and tasks 10-12 | `github-actions-ci-cd-best-practices.instructions.md`; `playwright-typescript.instructions.md` | Real API/browser verification, resilient locators, and diagnostic artifacts. |
| Container, tasks 13-14 | `containerization-docker-best-practices.instructions.md`; GitHub Actions guidance | Build the final image, verify startup and runtime permissions, and retain failure logs. |
| Documentation, tasks 3, 9, 15 | [create-readme](../.agents/skills/create-readme/SKILL.md); Markdown and documentation-impact guidance | Keep setup, run commands, and limitations consistent with implemented behavior. |

Instruction filenames in the table resolve under `.agents/instructions/`.
If AGENTS.md itself is edited, also load `instructions.instructions.md` and
`prompt.instructions.md`, as required by the user's instruction routing.
Use only the relevant parts of broad skills: no speculative infrastructure,
framework migration, state library, deployment, or security service is implied.

### Optional agents

These roles were available during toolkit discovery. Recheck availability when
needed; finding a TOML file alone does not prove a role is registered. Listing a
role here does not authorize spawning it. Delegate only when explicitly requested
or otherwise authorized by applicable instructions, with bounded ownership and
the same sequential PR gates.

| Agent definition under `~/.codex/agents/` | Use when delegated | Boundary |
| --- | --- | --- |
| `ai-team-dev.toml` | Implement one coherent backend/frontend feature slice. | Default implementation role; preserve other edits and avoid extra architecture. |
| `github-actions-expert.toml` | Implement or diagnose a specific CI job. | Keep broader scanning and deployment recommendations within authorized scope. |
| `playwright-tester.toml` | Explore the running screener and add browser tests. | Requires a runnable app and browser access; report missing prerequisites. |

No extra coordinator, model changes, agent registration, or duplicate resource
installation outside this selected toolkit is required. Optional agent definitions
remain outside the copying tasks; the user requested skills and instructions.
Verify local skill discovery in a fresh Codex session where possible. Separately
check that AGENTS.md routes matching tasks and leaves unrelated tasks unaffected;
report any unavailable fresh-session check without claiming runtime discovery.

## CI and failure feedback

Grow the existing workflows as each capability appears: conventions and hooks,
API tests, frontend lint/type-check/build, browser integration, then Docker smoke.
Use locked dependencies, minimal job permissions, and pinned third-party action
revisions. Keep existing status names stable where possible and inspect required
checks before changing jobs. Add timeouts and clean up started services.

For each real failure: read logs, reproduce it, add the smallest regression check,
fix the cause, and verify the failing-then-passing case. Extend the existing job
when it fits; add a job or workflow when the failure exposes a distinct unchecked
boundary (for example, source tests pass but the container fails to start).
Retain test reports, browser traces/screenshots, and container logs on failure.
Do not generate arbitrary workflows for every failure or build a self-modifying
CI bot. Do not hide failures by removing checks or adding skip markers.

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Sample values mistaken for market data | High | Persistent sample label and API provenance |
| Python 3.15 dependency support | Medium | Check locked install and API tests early |
| UI/API filter mismatch | Medium | Boundary cases plus real browser integration |
| Docker differs from local execution | Medium | Build and smoke-test the final image in CI |
| CI exists but is not required | Medium | Read rulesets and report actual enforcement |
| Too many unrelated changes per PR | Medium | Explicit PR gates and coherent commits |

## Deferred scope and open decisions

No accounts, saved screens, trading, payments, live provider, database, charts,
scheduled ingestion, or cloud deployment in the first version. Choose a licensed
market-data provider, supported universe, refresh cadence, and hosting target in
a later plan. No credentials are needed for this sample-data version.

Review decision: approve or adjust the proposed first filters and PR boundaries.
Clarify only if individual commits must survive on main rather than in each PR.

## Documentation consulted

- [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/):
  installable packages with a `src` layout and package build configuration.
- [FastAPI larger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/):
  feature routers composed into the application with explicit dependencies.
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/): synchronous
  TestClient tests with pytest and httpx.
- [React from scratch](https://react.dev/learn/build-a-react-app-from-scratch):
  Vite/TypeScript as a supported client application starting point.
- [Actions artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data):
  retain test/build output for diagnosis, including failed runs.

Fetched through Context7 during planning. Fetch focused current documentation
for implementation-specific tooling and configuration when those tasks begin.
