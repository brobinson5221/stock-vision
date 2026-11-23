# Authoring custom instructions

Adapted for Codex from [Awesome Copilot: Instructions](https://awesome-copilot.github.com/instruction/instructions/). Apply when creating, editing, or reviewing AGENTS.md or custom instruction files.

## Choose the runtime and scope

For Codex, use plain Markdown in AGENTS.md at the intended scope. Global instructions live in the active CODEX_HOME (normally ~/.codex); project instructions belong at the appropriate repository/directory level. Check for AGENTS.override.md and existing instructions before changing the entry point. Preserve unrelated rules and follow the runtime's actual instruction precedence.

A separate `<topic>.instructions.md` file is useful for substantial conditional guidance, but Codex does not discover it merely because of its name or location. Link it from the relevant AGENTS.md with an explicit condition telling the agent when to read and follow it. Use portable repository-relative references for shared project instructions and resolvable paths for personal global instructions. Keep the entry point within the runtime's instruction budget.

Copilot's `.github/instructions/` location and YAML `description`/`applyTo` fields are Copilot configuration, not automatic Codex scoping. Translate their intent into a plain-language scope and an AGENTS.md read condition. Keep Copilot metadata only when the requested artifact targets Copilot. Create skills only when the user asks for them or that format is explicitly in scope.

## Write the minimum complete guidance

Start with a descriptive title, purpose, and applicability. State the project-specific outcomes and constraints an agent cannot reliably infer from the code. Use focused sections for conventions, architecture, dependencies, error handling, security, performance, testing, or documentation only where they add useful guidance.

Use direct, actionable sentences and distinguish requirements from recommendations or context-dependent choices. Explain non-obvious reasons briefly. Prefer a small example that resolves ambiguity over exhaustive tables or copied manuals. Include version constraints when real, and obtain current framework/API documentation through the configured documentation workflow when needed.

Keep each rule in one authoritative place. Link detailed references with clear read conditions; avoid circular dependencies or instructions that require repeatedly re-reading themselves. Refer to actual project commands/configuration rather than inventing scripts or caching facts that change frequently.

Start with the smallest rule set that defines the desired outcome. Add constraints for demonstrated failures or concrete risks, not speculative edge cases. Preserve user choices and authorization boundaries; instructions cannot grant tool access, change permissions, or silently authorize publishing or external messages.

## Validate and maintain

Check instruction precedence, read conditions, paths, links, contradictions, and duplicated rules. Verify examples and available build/lint/test commands against their owning sources. Walk through a representative applicable task and an unrelated task to assess scope; include a missing-input case where the workflow requires inputs.

Distinguish file/link checks from observed behavior in a new Codex session. Test in the requested runtime when practical and report untested behavior accurately; a VS Code/Copilot run does not verify Codex behavior. Update instructions and examples when their owning interfaces change, and remove obsolete guidance without expanding the task into a general documentation rewrite.
