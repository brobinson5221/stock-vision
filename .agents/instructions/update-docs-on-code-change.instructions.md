# Update documentation with code changes

Adapted for Codex from [Awesome Copilot: Update Docs on Code Change](https://awesome-copilot.github.com/instruction/update-docs-on-code-change/). For code or configuration changes, assess documentation impact and update affected documentation as part of the same change.

## Identify affected documentation

Inspect the actual diff, public interfaces, setup scripts, configuration, and existing documentation structure. Check for changes to features, endpoints, signatures, authentication, dependencies, installation, CLI commands, environment variables, deployment behavior, examples, and compatibility. Search for references to renamed or changed interfaces.

An internal refactor with no change to documented behavior may need no documentation edit. Avoid rewriting an unrelated README or creating empty documentation files to satisfy a checklist.

## Update the owning sources

- README: update affected overview, setup, prerequisites, quick start, usage, and feature sections; maintain an existing table of contents if headings change.
- API documentation and schemas: keep methods, paths, parameters, responses, errors, authentication, and OpenAPI definitions aligned with the implementation.
- Configuration and deployment docs: describe names, types, defaults, required values, secret handling, and compatibility. Update example config files and .env.example when present, using placeholders rather than real credentials.
- Examples and tutorials: update imports, function calls, commands, request/response bodies, and expected outputs affected by the change. Include necessary setup and relevant error handling.
- Breaking changes and deprecations: explain old and new behavior, provide a migration path, and document supported alternatives. Use removal dates or release versions only when established by the project.
- Changelogs/release notes: follow the repository's existing policy and categories. Do not invent a release version, date, issue, or removal timeline.

Preserve the project's organization and terminology. Keep one authoritative explanation and link to it instead of duplicating it. Scale examples and detail to the feature; advanced usage sections are useful only when they clarify real behavior.

## Validate

Use existing documentation build, lint, link, schema, and example checks when relevant. Discover their real commands from project configuration; commands such as `npm run docs:check` are not guaranteed to exist. Check internal links, anchors, paths, configuration defaults, and public signatures against the actual code. Run changed examples in a safe environment when practical and distinguish executed checks from inspection.

Prefer existing generators for generated references, editing their owning source instead of generated output. Treat generated documentation and build artifacts according to repository policy.

Review the final diff to ensure documentation describes implemented behavior and required migration steps, with no secret values or speculative features. Report any verification that could not run.

## Keep automation in scope

Documentation maintenance does not by itself authorize adding hooks, dependencies, CI jobs, recurring reviews, release automation, commits, or publishing. Use existing tooling; add new tooling only when requested or necessary for the authorized change. The source's configurable-section pseudocode is authoring guidance, not executable Codex configuration. Apply the relevant documentation rules directly without inventing a configuration engine.
