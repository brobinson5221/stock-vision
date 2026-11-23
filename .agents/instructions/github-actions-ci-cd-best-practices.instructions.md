# GitHub Actions CI/CD best practices

Adapted for Codex from [Awesome Copilot: GitHub Actions CI/CD Best Practices](https://awesome-copilot.github.com/instruction/github-actions-ci-cd-best-practices/). Apply when creating, modifying, reviewing, or debugging GitHub Actions workflows, composite actions, or reusable workflows. Choose practices appropriate to the repository and authorized task; do not add every suggested service or deployment stage.

## Ground changes in the repository

Read existing workflows, package scripts, lockfiles, supported runtimes, runner requirements, required check names, and deployment conventions. Use Context7 and current official GitHub/action documentation to confirm syntax, action revisions, runtime requirements, and platform differences. Verify action SHAs against their owning repositories rather than copying stale hashes or inventing pins.

## Workflow structure

- Use descriptive workflow, job, and step names. Preserve required check names unless the associated rules are updated within the authorized scope.
- Select triggers, branch/path filters, and conditions for the intended events. Check their effects on required checks; filtering out a workflow can leave an expected check pending. Validate event payload assumptions and manual input types/defaults.
- Use `needs` for real dependencies and outputs for small values. Jobs have separate filesystems: transfer build outputs through artifacts rather than passing a local path and assuming the file exists elsewhere.
- Use appropriate runner labels, shells, working directories, and timeouts. Check compatibility with GitHub Enterprise Server or self-hosted runners when applicable.
- Use concurrency groups for shared resources and redundant CI runs. Cancel superseded CI when safe; avoid cancelling a production deployment midway without a safe cancellation strategy.
- Reuse existing actions or reusable workflows when useful. Keep secret and permission propagation explicit; avoid an abstraction for a single simple job.

## Security and credentials

- Set explicit least-privilege `permissions`, typically `contents: read` or `{}` at workflow level, with only necessary job-level increases. Default token permissions vary by organization/repository settings and event; do not assume universal write access.
- Pin external actions and reusable workflows to verified full commit SHAs, with readable version comments. Preserve valid same-repository relative action/workflow references. Pin container images by digest where immutability is required and arrange updates according to existing policy.
- Keep credentials in GitHub secrets or supported short-lived identity flows. Use narrowly scoped OIDC trust policies for cloud authentication where available; grant `id-token: write` only to jobs that need it. Do not print secrets or assume masking covers derived values.
- Treat PR titles, branch names, issue bodies, workflow inputs, artifacts, and contributed code as untrusted. Pass untrusted values through action inputs or environment variables and quote them for the chosen shell, rather than interpolating expressions into executable scripts.
- Keep untrusted PR code separate from privileged execution. In `pull_request_target` or privileged `workflow_run` flows, do not check out/run untrusted code or execute untrusted artifacts with secrets or write tokens. Avoid persistent self-hosted runners for untrusted contributions; use isolated environments appropriate to the trust boundary.
- Avoid persisting checkout credentials when later steps do not need authenticated Git operations. Grant secrets at the narrowest useful scope and preserve configured environment protections.
- Reuse project security scanning where appropriate: dependency review, SAST, secret scanning, signing, and attestations should match project needs and available permissions/plans. Do not introduce subscriptions, hooks, or organization setting changes as incidental workflow cleanup.

## Efficient and reproducible builds

- Use supported project runtimes and lockfile-based installation. Prefer package-manager download caches or setup-action caching; cache keys should include OS/runtime and relevant lockfile hashes. Avoid a unique run ID in a reusable dependency key. Restored caches must not replace dependency integrity checks.
- Treat caches as accelerators, not trusted artifacts or secret stores. Consider who can create and restore them; avoid cross-trust cache poisoning and overly broad restore fallbacks.
- Use matrices for supported configurations with purposeful include/exclude, max parallelism, and fail-fast settings. Install dependencies before invoking tools, and ensure each matrix dimension actually controls execution.
- Keep checkout history shallow when sufficient; fetch required history/tags when release/version calculations or diff-based tools depend on them.
- Upload build/test artifacts with unique names for matrix jobs and appropriate retention. Use the same verified artifact for deployment rather than silently rebuilding it. Check artifact action support for the actual GitHub platform and runner.

## Tests and diagnostics

Run the repository's actual lint, unit, integration, and E2E commands as appropriate. Isolated local services and a CI-hosted application are valid E2E targets; a deployed staging environment is useful when the deployment itself needs testing. Provision services with health/readiness checks and disposable test data.

Keep failures visible. Use retries only for understood transient failures, not as a substitute for fixing nondeterminism. Publish relevant logs, coverage, screenshots, and traces with bounded retention and without secrets. Apply failure/cancellation conditions deliberately; cleanup/reporting must not hide the failed job or hang indefinitely.

Diagnose skipped jobs from trigger/filter/condition evaluation; permission failures from effective token scope, environment access, or OIDC trust; cache misses from paths/keys; slow runs from timings; and flaky tests from isolation and readiness. Inspect only needed context fields and sanitized logs rather than dumping entire event/token contexts.

## Deployments

When deployment is in scope, preserve environment reviewers, branch restrictions, and existing approval policy. Separate build/test from promotion, verify artifact provenance, and add appropriate health/smoke checks. Choose rolling, blue/green, canary, or feature flags only when justified by the application's needs.

Document a compatible rollback path, accounting for database migrations and irreversible changes. Run deployments, rollback, credential changes, and external notifications only within the user's authorization and configured workflow rules; writing workflow instructions does not authorize those actions.

## Verification

Check YAML and workflow semantics with existing tooling such as actionlint when available. Ordinary YAML parsing alone cannot prove GitHub expression, trigger, or action-input validity. Run affected local commands when practical, inspect the diff for permission/trust changes, and report which checks ran. Do not claim a successful hosted workflow, deployment, or rollback without observing its result; dispatch runs only when authorized by the task.
