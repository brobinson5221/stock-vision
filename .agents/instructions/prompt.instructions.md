# Reusable prompt instructions

Adapted from [Awesome Copilot Prompt](https://awesome-copilot.github.com/instruction/prompt/) for Codex.

## Runtime and placement

Identify the requested runtime and follow the repository's existing prompt conventions. For Codex instructions, use plain Markdown in AGENTS.md at the requested scope, or a separate instruction file explicitly referenced by AGENTS.md. Separate .instructions.md files are not automatically discovered by Codex. Preserve existing global and repository instructions.

For a reusable standalone prompt, use a descriptive kebab-case Markdown filename at the requested location. Create a skill only when the user requests a skill. When the user explicitly requests a Copilot prompt, use .github/prompts/<action>.prompt.md with supported Copilot frontmatter and validate it for that runtime.

## Copilot compatibility

Copilot metadata such as agent, model, tools, argument-hint, and applyTo does not configure Codex instructions. Translate file-glob scope into explicit conditions in AGENTS.md and the instruction body. Express tool needs as capabilities available in the current environment; instruction text cannot grant permissions or select a model.

Replace VS Code substitutions such as ${input:variableName}, ${selection}, ${file}, and ${workspaceFolder} with named inputs and concrete directions for obtaining them from the user's request or workspace. Codex does not automatically expand those substitutions. Preserve Copilot syntax only in an artifact explicitly intended for Copilot.

## Content and workflow

- State the mission, scope, necessary inputs, defaults, workflow, output format and location, and acceptance criteria. Use only sections that help the task.
- Use direct, concise instructions with a clear flow from context through actions to validation. Keep requirements unambiguous and resolve conflicting instructions.
- Infer missing inputs from available context when reasonable. Ask for required information that cannot be inferred; identify the blocker rather than inventing values.
- Use tools appropriate to the task and preserve authorization boundaries. Do not add publishing, messaging, or unrelated mutations. Define bounded retries and failure conditions when external operations require them.
- Link related instructions and authoritative references. Include small examples or reusable templates only when they clarify non-obvious requirements; avoid copied manuals and unnecessary boilerplate.
- Keep prompts portable across repositories by obtaining project-specific paths and commands from the current workspace.

## Validation and maintenance

Check that file paths and references resolve, inputs have defaults or a clear missing-input path, outputs are reviewable, and success checks can actually be executed. For Codex instructions, verify the AGENTS.md entry point and scope; do not treat VS Code's Chat: Run Prompt as a Codex test.

Walk through one representative request and one missing-input case. Run any new executable helpers safely and report the checks actually performed. Keep prompts with the code they affect where appropriate, and update references when runtime behavior or project conventions change.
