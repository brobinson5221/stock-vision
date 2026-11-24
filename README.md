# Stock Vision

A stock screener being built with a Python/FastAPI backend and React/TypeScript
frontend. The first version will use explicitly labeled sample data.

Currently this repository provides an installable Python package, development
tooling, and convention checks.
The packaged sample source contains six fictional companies with synthetic USD
values, explicitly labeled `synthetic-sample`; these are not market quotes.
The sample API and paginated stock table run locally and are tested in Chromium.
Docker packaging is still pending. See the
[implementation plan](tasks/plan.md) and [task checklist](tasks/todo.md).

## Set up locally

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
git clone https://github.com/brobinson5221/stock-vision.git
cd stock-vision
uv sync --locked
uv run --locked pre-commit install
```

uv follows the Python 3.15 pin in [.python-version](.python-version) and installs
development tools into `.venv`. Hook installation enables both pre-commit and
commit-message checks; repeat it in each checkout.

## Development loop

Start a branch from updated `main` using `codex/<type>/<description>`, for example
`codex/feat/sample-screener`. Descriptions use lowercase letters and digits
separated by single hyphens. Allowed types are `feat`, `fix`, `docs`, `style`,
`refactor`, `perf`, `test`, `build`, `ci`, `chore`, and `revert`.

Run checks from the repository root:

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest tests
uv run --locked pre-commit run --all-files
uv run --locked python scripts/check_branch.py codex/feat/sample-screener
```

Tests cover branch validation, package imports, sample data, and schema bounds. The existing
branch tests also run with `uv run --locked python -m unittest discover -s tests -v`.
Format with `uv run ruff format .`.
Hooks can change files; review and stage those edits before retrying a commit.

Use `uv add PACKAGE` for runtime dependencies and `uv add --dev PACKAGE` for
development tools. Commit `pyproject.toml` and `uv.lock` together when they change.

The package lives in `src/stock_vision/` and installs during locked sync. Verify
it with `uv run --locked python -c "import stock_vision"`. Build a source archive
and wheel with `uv build`; outputs go to the ignored `dist/` directory. FastAPI
and Uvicorn are runtime dependencies; pytest and httpx are development tools.

`stock_vision.stocks.source.load_sample_stocks()` loads validated, immutable
records from package resources, independent of the working directory. Price is
USD per share and market capitalization is USD; unavailable market cap and P/E
remain `None`. Pagination inputs default to limit 50 and offset 0, with limit
1–100 and nonnegative offset.

## Run the sample API

```sh
uv run --locked uvicorn stock_vision.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API explorer.
`GET /api/health` returns `{"status":"ok"}`. `GET /api/stocks?limit=2&offset=0`
returns `items`, `total`, `limit`, `offset`, `provenance`, and `currency`.
Results are ordered by symbol before pagination; out-of-range pages are empty
with the total preserved. Invalid page bounds return HTTP 422.

## Run the frontend

Use Node.js 24 and npm (verified with Node 24.14.1 and npm 11.19.1).
From the repository root:

```sh
npm --prefix frontend ci
npm --prefix frontend run dev
```

Keep the sample API running on `127.0.0.1:8000` in another terminal, then open the
local URL printed by Vite. Its development proxy forwards `/api` requests to the
backend. The screener displays a table with synthetic-data provenance, USD prices
and market capitalization, and explicit unavailable metrics. Previous/Next
controls browse 50-row pages, preserve the API query, announce result ranges,
and disable invalid navigation. On narrow screens, focus the table region and
use arrow keys to scroll horizontally; row and column headers stay visible.
Loading, empty, and retryable error states remain available. Reload cancels the
previous request; late responses cannot replace current results.

```sh
npm --prefix frontend run lint
npm --prefix frontend run build
npm --prefix frontend run preview
```

The build runs strict TypeScript checking and writes static assets to
`frontend/dist/`. Preview serves those assets locally for verification.

Run the browser test after installing dependencies and building the frontend:

```sh
npm --prefix frontend exec -- playwright install chromium
npm --prefix frontend run test:e2e
```

Leave ports 8000 and 4173 free. Playwright starts and stops the sample API and
Vite preview. The test extends the sample to 51 rows to exercise real pagination
and injects a single HTTP 503 to verify recovery. Failed runs retain `trace.zip`
under `dist/e2e-results/`. CI uploads available traces as `browser-failure-traces`.

Make focused Conventional Commits with working code and its tests together.
Use `uv run cz commit` for prompts, or `git commit -m "ci: validate conventions"`.
Separate independently reviewable tooling, feature, and documentation changes.

Keep one PR open at a time. Finish its checks and review, then wait for the user
to merge it before branching from updated `main` for the next PR. Use squash
merging with the Conventional Commit PR title; development commits remain
reviewable within the PR. Follow the boundaries in the task checklist.

## GitHub verification

The [Checks workflow](.github/workflows/checks.yml) runs locked installation,
Ruff, pytest, and existing pre-commit hooks on pushes and PRs. It also builds and
installs a wheel outside the checkout to verify the API import and packaged sample
data. The frontend job uses Node.js 24 and `npm ci` before linting, checking types,
and building. Download the `pytest-results` artifact from the workflow run for
the JUnit report, including when tests fail.
On PRs it also validates the branch name and every commit in the PR base-to-head
range with Commitizen. The [PR title workflow](.github/workflows/pr-title.yml)
checks Conventional Commit titles.

To check the local commit range after fetching `origin/main`:

```sh
uv run --locked cz check --rev-range origin/main..HEAD
```

For an observed failure, reproduce it and add a focused regression check when
coverage is missing. Extend existing CI where it fits; add a job only for a
distinct unchecked boundary. Inspect the latest PR checks before review.

## Repository agent guidance

[AGENTS.md](AGENTS.md) routes tasks to the checked-in skills and instructions in
`.agents/`; matching guidance can be read directly from those repository-relative
links without personal global copies. Use only the files relevant to the task.

The [toolkit inventory](.agents/toolkit.md) records source snapshots, licenses,
adaptations, prerequisites, and verification limits. Updates are deliberate:
compare against a named source snapshot, preserve local edits and required support
files, review license/dependency changes, validate references and skill metadata,
then submit focused commits through the normal PR workflow. No automatic sync.

Guidance does not install or authenticate external tools. Context7 needs its MCP
connection; use official documentation and disclose the fallback if unavailable.
Web guidance uses bundled references first; its optional networked CLI is not
installed by this repository. Verify skill availability in a fresh Codex session
separately from file/link validation.
