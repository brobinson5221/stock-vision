# Agent instructions

## Project context

Read `README.md`, `pyproject.toml`, and `.github/workflows/` before making changes.
Discover source layout, run commands, and test commands from the current project.
Keep this guidance updated as the project grows.

Stock Vision has an installable `src/stock_vision/` package and pytest tests,
including standard-library unittest cases for its branch validator. A minimal
React/TypeScript Vite frontend lives in `frontend/src/`, with a stock table and
page controls. The Chromium browser test exercises the built frontend and real
API routes. The container remains pending. Follow
`tasks/plan.md` and `tasks/todo.md`.
Keep Python tests separate in `tests/`.
Create modules only when their task introduces behavior.

Run the sample API with `uv run --locked uvicorn stock_vision.main:app --reload`.
Health is `/api/health`; browsing is `/api/stocks`. Routes delegate ordering and
pagination to `stocks/service.py`, using the injectable sample source.

Use Node.js 24 for frontend work. Run `npm --prefix frontend ci`, then follow
the [two-terminal launch steps](README.md#run-the-sample-api). Validate with
`npm --prefix frontend run lint` and `npm --prefix frontend run build`
(TypeScript checking plus Vite production build). Keep npm's lockfile with
dependency changes. `App.tsx` composes the page; `features/screener/` owns API
validation and request state. Vite proxies `/api` to `127.0.0.1:8000`; run both
processes for local verification. Preserve cancellation and stale-result guards.
After building, run `npm --prefix frontend run test:e2e` with Chromium installed
and ports 8000 and 4173 free. See [frontend verification](README.md#verify-the-frontend).

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

## Repository-local guidance

Use the linked project copies for matching work unless the user specifies another
source. Read only applicable instruction files and skill entrypoints, then any
supporting references that task needs. Do not load the entire toolkit for every
request. These files supplement project rules and do not grant tool access or
authorization. Global copies are not required.

| When working on | Read and follow |
| --- | --- |
| Codebase context or changes across files | [context-engineering](.agents/instructions/context-engineering.instructions.md) |
| Library/tool documentation through Context7 | [context7](.agents/instructions/context7.instructions.md), with the workflow above |
| Code and its comments | [self-explanatory-code-commenting](.agents/instructions/self-explanatory-code-commenting.instructions.md) |
| Application code, interfaces, dependencies, or configuration | [update-docs-on-code-change](.agents/instructions/update-docs-on-code-change.instructions.md) |
| A scoped diff, PR, commit, or source review | [code-review-generic](.agents/instructions/code-review-generic.instructions.md) |
| Markdown editing or review | [markdown](.agents/instructions/markdown.instructions.md) |
| GitHub Actions workflows | [github-actions-ci-cd-best-practices](.agents/instructions/github-actions-ci-cd-best-practices.instructions.md) |
| Python library research or implementations using it | [codexer](.agents/instructions/codexer.instructions.md) |
| Browser HTML/CSS, styling, or colors | [html-css-style-color-guide](.agents/instructions/html-css-style-color-guide.instructions.md) |
| TypeScript Playwright specs, fixtures, or page objects | [playwright-typescript](.agents/instructions/playwright-typescript.instructions.md) |
| Dockerfiles, builds, Compose, or container configuration | [containerization-docker-best-practices](.agents/instructions/containerization-docker-best-practices.instructions.md) |
| AGENTS.md or custom instruction files | [instructions](.agents/instructions/instructions.instructions.md) |
| Reusable prompts or instruction authoring | [prompt](.agents/instructions/prompt.instructions.md) |

| Task | Local skill entrypoint |
| --- | --- |
| Plan or revise multi-step work | [planning-and-task-breakdown](.agents/skills/planning-and-task-breakdown/SKILL.md) |
| Name, validate, or create a branch | [conventional-branch](.agents/skills/conventional-branch/SKILL.md) |
| Write a commit message | [commit-message-storyteller](.agents/skills/commit-message-storyteller/SKILL.md) |
| Review code/configuration changes | [ponytail-review](.agents/skills/ponytail-review/SKILL.md) |
| Prepare a PR body or submission | [pr](.agents/skills/pr/SKILL.md), [create-pr](.agents/skills/create-pr/SKILL.md) |
| Build or modify frontend UI | [frontend-ui-engineering](.agents/skills/frontend-ui-engineering/SKILL.md) |
| Browser HTML/CSS/JavaScript behavior | [modern-web-guidance](.agents/skills/modern-web-guidance/SKILL.md); use bundled guides first |
| React component implementation or review | [react-best-practices](.agents/skills/react-best-practices/SKILL.md); apply React/Vite-relevant rules |
| Create or refresh README | [create-readme](.agents/skills/create-readme/SKILL.md) |

See [toolkit sources and verification](.agents/toolkit.md) for licenses, snapshots,
prerequisites, and update procedure. If a required tool is unavailable, report it
and use a documented fallback where possible; do not silently install tools or
change global configuration. File/link checks do not prove automatic skill
discovery or selection in a fresh session.
