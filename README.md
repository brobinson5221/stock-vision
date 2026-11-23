# Stock Vision

A stock screener being built with a Python/FastAPI backend and React/TypeScript
frontend. The first version will use explicitly labeled sample data.

Currently this repository provides an installable Python package, development
tooling, and convention checks.
The packaged sample source contains six fictional companies with synthetic USD
values, explicitly labeled `synthetic-sample`; these are not market quotes.
The sample API runs locally; frontend and Docker image are still pending. See the
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

Make focused Conventional Commits with working code and its tests together.
Use `uv run cz commit` for prompts, or `git commit -m "ci: validate conventions"`.
Separate independently reviewable tooling, feature, and documentation changes.

Keep one PR open at a time. Finish its checks and review, then wait for the user
to merge it before branching from updated `main` for the next PR. Use squash
merging with the Conventional Commit PR title; development commits remain
reviewable within the PR. Follow the boundaries in the task checklist.

## GitHub verification

The [Checks workflow](.github/workflows/checks.yml) runs locked installation,
Ruff, pytest tests, and existing pre-commit hooks on pushes and PRs.
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
