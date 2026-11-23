# Python research and implementation

Adapted for Codex from [Awesome Copilot: Codexer](https://awesome-copilot.github.com/instruction/codexer/). Apply to Python library research and evidence-based Python implementation. This is a task-specific workflow, not a replacement identity for every Codex task.

## Research before choosing

Inspect the problem, existing Python version, dependency manifests, environment, interfaces, and tests. Prefer existing capabilities and the standard library before adding dependencies. For library/API questions, use the Context7 workflow in root AGENTS.md and current query-docs tool; the source's get-library-docs, #websearch, #think, #todos, and VS Code extension commands are not portable Codex APIs.

Use available search/retrieval tools for missing official references, real implementation issues, or comparisons. Prefer owning documentation/source and relevant supported-version evidence. Repository popularity, star count, or a recent commit is not proof of quality, compatibility, or security. Check maintenance, license, vulnerabilities, platform support, and operational costs proportionate to the choice.

## Match the project

Use the existing isolated environment and package manager, whether venv, conda, uv, Poetry, or another established workflow. Avoid modifying system Python or installing dependencies globally as incidental development work. Preserve the project's manifest and lockfile strategy; do not overwrite requirements.txt with pip freeze from an unrelated environment or create duplicate dependency formats.

Follow configured formatting, linting, typing, naming, and supported language versions. Use descriptive names and focused functions, but do not reject correct code by an arbitrary line-count limit or force new module directories into a small script. Prefer useful interface annotations and the project's modern typing conventions. Preserve public interfaces and intended global constants.

Use specific exceptions where callers can recover, meaningful error messages, context managers, validation at trust boundaries, and appropriate logging without sensitive content. A broad exception handler at a justified boundary must still preserve or report failures. Keep CLI output distinct from diagnostic logging. Document public interfaces and non-obvious decisions without boilerplate docstrings on trivial private helpers.

## Implement and verify

Deliver the smallest complete solution, including affected callers, examples, tests, and configuration. Use built-ins and installed dependencies where they fit. Profile with tools such as cProfile or timeit before performance changes and compare realistic workloads; a shorter comprehension is not inherently better than a clear loop.

Run relevant existing checks and meaningful tests for non-trivial behavior and failure paths. Do not ask whether to test work that already requires verification, or add an entire pytest/linter/type-checker stack when the project has another appropriate approach. Report research findings, the chosen approach, dependency changes, test evidence, and unresolved limitations at a useful length. Do not claim production readiness from a prototype or an unexecuted example.
