---
name: conventional-branch
description: Suggest, validate, or create Git branch names using Conventional Branch types and agent prefixes. Use for branch naming or creation requests while respecting repository and user conventions.
license: MIT
---

# Conventional branch names

Use the [Conventional Branch](https://conventionalbranch.org/) convention while respecting explicit user names and repository rules. For Codex-created branches, default to `codex/` unless applicable instructions or the user specify otherwise.

## Name format

Use `<type>/<description>`. Purpose types are feature/feat, bugfix/fix, hotfix, release, and chore. Agent source prefixes include ai, copilot, cursor, claude, and codex. Existing trunk names such as main/master/develop need no prefix; do not recreate or rename them during a feature-branch task.

Descriptions use lowercase letters, digits, hyphens, and dots. Avoid spaces, underscores, consecutive hyphens/dots, hyphen-dot adjacency, and leading/trailing hyphens or dots. Use a concise meaningful phrase, normally two to five words; dots are useful for versions such as `release/v1.2.0`. Include a relevant issue/ticket identifier when requested and compatible with the chosen policy. These are convention rules, not Git's complete reference-name validation.

Examples: `codex/add-oauth-login`, `bugfix/header-overflow`, `chore/update-ci-config`, `release/v1.2.0`. Invalid convention examples include `Feature/Add-Login`, `feature/new--login`, and `fix/header_bug`.

## Suggest or validate

Infer intent and a description from the request and existing conventions. Ask only when an essential ambiguity remains. For naming-only requests, return the suggested name or validation result without changing Git state. Do not silently normalize an explicit name and then create a different branch without explaining the change.

Check the convention and use Git's actual reference validation, such as `git check-ref-format --branch <name>`, with arguments passed safely. Check existing branches/ref-prefix collisions before creation. A convention-compliant-looking name can still violate Git restrictions, for example a description ending in `.lock`.

## Create only when requested or authorized by the task

Inspect the current checkout/worktree, status, active branch, and requested starting point. Follow applicable worktree tooling instructions. Prefer a suitable current checkout; do not create a new worktree unnecessarily. Existing changes must be preserved, and unrelated work must not be reassigned to a new task accidentally.

Use an explicit start point when given. Otherwise inspect repository guidance and the remote default branch reference; distinguish the default branch from a known release/development base. If needed, inspect remote metadata rather than assuming origin, main, or develop exists. Resolve only consequential uncertainty with the user.

Do not automatically check out a trunk branch and run git pull, merge, rebase, reset, stash, or clean. Refresh remote refs when needed and authorized, then create the new branch directly from the verified start point, for example with `git switch -c <name> <start-point>` when supported. If the repository has no initial commit, handle the unborn branch explicitly rather than pretending a base exists.

Verify the active branch and status after creation. Report the created branch and starting point. Push only when authorized; a branch-naming request does not authorize publishing it. Use existing validation tooling if present rather than installing hooks or CI checks solely to enforce the name.
