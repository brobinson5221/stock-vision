# Context engineering

Adapted for Codex from [Awesome Copilot: Context Engineering](https://awesome-copilot.github.com/instruction/context-engineering/). Apply when gathering context for a code change, planning a change across multiple files, or improving agent-facing project context.

## Gather the relevant evidence

Read applicable AGENTS.md instructions and inspect the owning implementation, callers, tests, fixtures, configuration, and public exports. Use focused file/text searches, then follow dependencies and existing patterns. Establish the user's objective, constraints, current state, and verification command before a substantial change.

Prefer current owning files over stale summaries, open-editor assumptions, or pasted excerpts. Codex does not necessarily see every open tab or cursor position. Explicit paths and targeted reads provide dependable context. External documentation clarifies library behavior; it does not replace the repository's actual version and configuration.

## Make context useful

Use semantic names, meaningful paths, clear module boundaries, public contracts, and non-obvious rationale where the task calls for them. Explicit interface types and named constants help when they clarify contracts or domain meaning; redundant annotations and constants for obvious literals do not. Preserve existing module/export conventions rather than introducing barrel files or reorganizing a project merely for agent convenience.

Keep essential shared guidance in AGENTS.md and conditional detail in linked references with precise read conditions. A COPILOT.md file is not automatically a Codex instruction entry point. Avoid duplicating source facts, copying whole manuals, or creating an architecture document without a concrete need.

## Changes and continuity

Identify every affected interface and update related code/tests/docs as a coherent change. Verify in small meaningful increments; one-file-at-a-time editing is not required when correctness spans files. Reuse repository patterns without importing unrelated features.

For long work, retain a compact summary of the objective, accepted decisions, modified paths, verified results, unresolved blockers, and next action. Refresh files when evidence suggests they changed. If output becomes generic or wrong, locate the missing context or stale assumption before adding more global rules. Ask only for required context that cannot be found from available sources, and keep user data out of external documentation queries.
