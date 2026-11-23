# Agent instructions

## Project context

Read `README.md`, `pyproject.toml`, and `.github/workflows/` before making changes.
Discover source layout, run commands, and test commands from the current project.
Keep this guidance updated as the project grows.

Stock Vision has an installable `src/stock_vision/` package and pytest tests,
including standard-library unittest cases for its branch validator. A minimal
React/TypeScript Vite frontend lives in `frontend/src/`; table controls and the
container remain pending. Follow `tasks/plan.md` and `tasks/todo.md`.
Keep Python tests separate in `tests/`.
Create modules only when their task introduces behavior.

Run the sample API with `uv run --locked uvicorn stock_vision.main:app --reload`.
Health is `/api/health`; browsing is `/api/stocks`. Routes delegate ordering and
pagination to `stocks/service.py`, using the injectable sample source.

Use Node.js 24 for frontend work. Run `npm --prefix frontend ci`, then
`npm --prefix frontend run dev`. Validate with `npm --prefix frontend run build`
(TypeScript checking plus Vite production build). Keep npm's lockfile with
dependency changes. `App.tsx` composes the page; `features/screener/` owns API
validation and request state. Vite proxies `/api` to `127.0.0.1:8000`; run both
processes for local verification. Preserve cancellation and stale-result guards.

## Setup and dependencies

Run commands from the repository root. Use uv and follow the Python version in
`.python-version` and `project.requires-python`.

```sh
uv sync --locked
uv run pre-commit install
```

Use `uv run` for project commands, `uv add PACKAGE` for runtime dependencies, and
`uv add --dev PACKAGE` for development tools. Commit `pyproject.toml` and `uv.lock`
together when dependencies change.

## Validation

Follow the Ruff configuration in `pyproject.toml`. Before submitting changes:

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m unittest discover -s tests -v
uv run --locked pytest tests
uv run --locked pre-commit run --all-files
```

Apply formatting with `uv run ruff format .`. Review hook changes and stage them
before retrying a commit. Run relevant tests when the project has them; report
what ran and what could not be checked. Lint success is not a passing test suite.

## Commits and pull requests

Work on a `codex/<type>/<lowercase-kebab-description>` feature branch, preserve
unrelated user edits, and submit changes through pull requests. Validate branch
names with `uv run --locked python scripts/check_branch.py BRANCH`.
Push, create PRs, and merge only within the user's authorization.

Use Conventional Commits for commit subjects and PR titles, such as
`feat: add CSV import` or `docs: explain setup`. Always use the
`commit-message-storyteller` skill when available and base messages on the staged
diff.

Keep focused commits with working code and its tests together. Keep one PR open
at a time at the plan's PR boundaries; leave merging to the user. After it merges,
fetch updated main before starting the next PR. Use the repository `pr` and
`create-pr` skills for submissions and review the scoped diff with `ponytail-review`.

Build the package with `uv build`. Verify wheel imports in a clean environment
outside the checkout when changing packaging; never add source-path overrides.

The workflows check Ruff, pytest, hooks, PR branch names, all PR commit messages,
and PR titles. Locally validate commits with
`uv run --locked cz check --rev-range origin/main..HEAD` after fetching main.
Use squash merging with the PR title as the commit message. Verify current
rulesets before assuming checks are required. Add regression checks for observed
failures; extend CI only where coverage is missing.

## Current documentation

Use Context7 MCP for library, framework, SDK, API, CLI, and cloud-service
documentation, including setup, syntax, configuration, and library-specific bugs.
Prefer Context7 over web search even for familiar APIs.

1. Call `resolve-library-id` first unless an exact `/org/project` ID is supplied.
2. Select the most relevant reputable match, using a version-specific ID when
   appropriate. Refine mismatched searches.
3. Call `query-docs` with that ID and a focused query per concept.
4. Base the implementation or answer on the fetched documentation.

General programming concepts, business-logic debugging, and refactoring or review
without library-specific questions do not need Context7. If it is unavailable,
use official documentation and disclose the fallback.
