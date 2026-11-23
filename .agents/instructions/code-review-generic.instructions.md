# General code review

Adapted for Codex from [Awesome Copilot: Code Review Generic](https://awesome-copilot.github.com/instruction/code-review-generic/). Apply when reviewing a diff, pull request, commit, or explicitly scoped source code.

## Establish scope and evidence

Identify the exact diff/base and applicable repository guidance. Read changed code with its callers, tests, data models, configuration, and contracts. Review the final implementation rather than only a summary. Keep review read-only unless fixes are requested; do not post external comments or approve/merge a PR merely because a local review is requested.

Prioritize security vulnerabilities, data loss/corruption, incorrect behavior, races, and broken public contracts. Then assess demonstrated performance/resource problems, test gaps on important behavior, and material deviations from established architecture. Separate optional readability/style suggestions from defects; arbitrary function-size limits, SOLID terminology, and preferred abstractions are not proof of a bug.

## Check affected behavior

- Trace normal and failure paths, boundary conditions, null/empty inputs, cancellation/retries, and state transitions relevant to the change.
- Verify input validation, parameterized queries, authentication/authorization, secret handling, dependencies, and trust boundaries where they are actually involved.
- Inspect test assertions and isolation, not just coverage percentages. Identify meaningful missing cases rather than tests that mirror implementation or blanket demands for tests on trivial changes.
- Assess N+1 access, algorithmic growth, pagination, memory/resource cleanup, caching freshness, and concurrency using realistic workload evidence. Do not prescribe caching or lazy loading without a relevant bottleneck or behavior need.
- Check module/interface compatibility and established project structure. Verify affected setup, API, configuration, migration, and example documentation. Do not require new abstractions, comments, or changelogs unrelated to the change.

Run focused existing checks when useful and within scope. Distinguish observed failures, supported source reasoning, and uncertainty. Do not turn hypothetical risks or unrelated pre-existing issues into findings introduced by the patch; report them separately only if needed.

## Report actionable findings

Lead with findings ordered by severity. For each, give a short issue title, the precise file/line, triggering condition, concrete impact, and a focused fix direction. Use a small reproducible example when it materially clarifies the defect. Group one root cause into one finding and use the requested review format or inline-comment tooling when applicable.

State no findings when none meet the evidence bar, followed by material testing limitations if any. Do not invent issues to fill categories, assert a successful test that was not run, or claim an exhaustive security audit from an ordinary review. Use the user's language and requested detail; default to clear English when none is specified.
