---
name: create-readme
description: Create or refresh a project README.md by inspecting the repository and writing concise, accurate onboarding and usage documentation.
---

# Create README

Create an appealing, informative README.md that helps a new reader understand the project and get started. Balance comprehensive coverage of essential information with concise prose.

## Review the project

Review the project and workspace broadly enough to understand its purpose, components, and supported workflows. Inspect existing documentation, manifests, entry points, scripts, configuration examples, tests, CI, and relevant assets. Focus detailed reading on files that substantiate README content; skip generated files and dependency directories.

Derive commands, prerequisites, configuration names, features, and paths from the repository. Preserve useful existing documentation and user edits when refreshing a README. Do not invent capabilities, badges, URLs, version requirements, or successful verification. Ask about material gaps that cannot be resolved from the project.

## Write the README

Use these READMEs as inspiration for structure, tone, and presentation. Read them when accessible, adapting their approach to the project's size and audience rather than copying prose or imposing their full structure:

- https://raw.githubusercontent.com/Azure-Samples/serverless-chat-langchainjs/refs/heads/main/README.md
- https://raw.githubusercontent.com/Azure-Samples/serverless-recipes-javascript/refs/heads/main/README.md
- https://raw.githubusercontent.com/sinedied/run-on-output/refs/heads/main/README.md
- https://raw.githubusercontent.com/sinedied/smoke/refs/heads/main/README.md

Lead with the project name, a short explanation of what it does, and its value to the reader. If an existing project logo or icon is available, use it in the header with a working path and appropriate alt text.

Choose sections that the project actually needs, such as key features, prerequisites, quick start, configuration, usage examples, development, architecture, deployment, or troubleshooting. Make the shortest supported path to first use easy to find. Link to detailed documentation rather than repeating it. Add a table of contents only when it improves navigation.

- Use GitHub Flavored Markdown, readable headings, and fenced code blocks with language tags.
- Use emojis sparingly.
- Use GitHub alerts where they clarify a relevant note, tip, prerequisite, or warning:

  ```markdown
  > [!NOTE]
  > Brief, useful context.
  ```

- Do not add LICENSE, CONTRIBUTING, CHANGELOG, or equivalent sections; those topics belong in dedicated files.
- Keep instructions concrete and concise. Distinguish required setup from optional workflows.
- Use placeholder values for secrets and explain required configuration without exposing credentials.

## Verify and deliver

Write README.md at the project root unless the user specifies another location. Check relative links, asset paths, heading anchors, and command examples against the repository. Run lightweight, relevant verification when feasible; writing documentation alone does not authorize deployment or other external changes. Report what was created or updated and any material information or commands that remain unverified.
