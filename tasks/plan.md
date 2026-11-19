# Implementation Plan: Stock Vision

## Overview

Build a stock screener with a Python/FastAPI API and a React/TypeScript frontend.
Start with clearly labeled, deterministic sample data, as selected by the user.
Ship small verified changes through one open PR at a time. This document is a
proposal for review; no application implementation is included in the planning PR.

## Current state

The repository contains a Python template, not an application. Python is pinned
to 3.15. uv, Ruff, pre-commit, and Commitizen are configured, with a tracked
uv.lock. Actions currently checks Ruff and Conventional Commit PR titles.
There are no source files, application tests, frontend, or Docker configuration.

## Architecture decisions

- Keep one repository: `backend/` for FastAPI, `frontend/` for React, and root
  Python tooling. Use Vite and TypeScript for the frontend, with an npm lockfile.
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
  The small sample universe does not need pagination or a database.
- Use pytest with FastAPI TestClient for API checks and browser tests for the
  actual frontend/API flow. Add frontend unit tests only for isolated logic that
  browser tests do not adequately cover.
- Package the frontend build and Python API in a multi-stage Docker image, with
  FastAPI serving the built assets on the same origin. Use a development proxy
  for local frontend work. Confirm exact Docker and Vite setup with current docs
  during implementation. Do not use the development server as the runtime image.
- Keep Python 3.15 unless a reproducible dependency compatibility failure requires
  a deliberate version change across the pin, metadata, lockfile, CI, and image.

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
| 2 | Browse sample stocks | 4-9 | API + tests; frontend setup; table; frontend checks; browser check; docs |
| 3 | Screen stocks | 10-12 | Search/sector slice; numeric filter slice; sorting slice |
| 4 | Run the verified container | 13-15 | Container + smoke check; Docker CI; runbook |

Checkpoints after every two or three tasks verify progress within a PR; the PR
boundary is the human review/merge gate. A task checkpoint is not another PR.

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

- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/): synchronous
  TestClient tests with pytest and httpx.
- [React from scratch](https://react.dev/learn/build-a-react-app-from-scratch):
  Vite/TypeScript as a supported client application starting point.
- [Actions artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data):
  retain test/build output for diagnosis, including failed runs.

Fetched through Context7 during planning. Fetch focused current documentation
for implementation-specific tooling and configuration when those tasks begin.
