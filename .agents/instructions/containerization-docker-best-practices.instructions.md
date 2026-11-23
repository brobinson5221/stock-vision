# Docker containerization

Adapted for Codex from [Awesome Copilot: Containerization Docker Best Practices](https://awesome-copilot.github.com/instruction/containerization-docker-best-practices/). Apply when creating, modifying, reviewing, or debugging Dockerfiles, image builds, Compose services, or container runtime configuration.

## Inspect the target

Read the application runtime, package/lockfiles, build commands, Dockerfiles, ignore rules, Compose/orchestration configuration, supported architectures, and persistent storage needs. Confirm version-sensitive Docker/Compose/BuildKit syntax with Context7 and official documentation. Preserve the project's deployment model; containerization does not imply a Kubernetes migration.

## Build reproducible, focused images

- Use maintained trusted base images compatible with the application and target architecture. Pin appropriate versions/digests with an update strategy; avoid production latest tags. Alpine, slim, and distroless have different libc, native-extension, debugging, certificate, and runtime tradeoffs. Smaller is not automatically safer or compatible.
- Separate build tools/tests from runtime artifacts with named multi-stage builds where beneficial. Copy only required artifacts and runtime dependencies, checking ABI/runtime compatibility. A multi-stage build is unnecessary if it adds no useful separation.
- Copy dependency manifests and lockfiles before frequently changed source to reuse cache. Use deterministic installation commands and appropriate BuildKit caches. Combine related package installation/cleanup so temporary files do not persist in earlier filesystem layers; not every Dockerfile instruction creates a filesystem layer.
- Maintain .dockerignore for the actual build context. Exclude secrets, local environments, VCS metadata, and unnecessary output without excluding files required by builds, tests, or versioning tools. Prefer explicit COPY and avoid remote/unverified ADD behavior unless required.
- Use ARG/ENV for appropriate non-secret configuration only. Build credentials belong in supported BuildKit secret/SSH mounts, not build arguments, copied files, or image environment defaults. Multi-stage builds and deletion do not make secrets in build caches/intermediate images safe. Avoid leaking mounted secrets through logs or generated output.

## Runtime correctness and isolation

- Run the final application as a suitable non-root user and give it only necessary filesystem permissions. Reuse a suitable base-image user when available. Check volume ownership and writable paths rather than broadly granting permissions.
- Prefer exec-form CMD/ENTRYPOINT for predictable argument passing and signal delivery. Startup wrappers should forward signals, normally by exec-ing the application. Use a clear primary process and proper child reaping when needed; multiple worker processes are not inherently wrong.
- EXPOSE documents ports; it does not publish them. Bind/listen/publish only what the target environment needs. Use service discovery and appropriate network separation rather than hardcoded container IPs or unnecessary host networking.
- Externalize runtime configuration and validate required values. Inject secrets through the deployment platform's supported mechanism with suitable access control; do not bake them into images.
- Use appropriate resource constraints and least privilege. Avoid privileged mode, unnecessary capabilities, host mounts, or Docker socket exposure. Consider read-only root filesystems, specific writable mounts, and runtime security profiles where compatible. Containers share kernel/runtime trust and are not complete security boundaries.
- Keep persistent data in deliberate storage with backup/migration behavior. Preserve existing volumes and user data. Do not run destructive prune, down-with-volume-removal, or cleanup operations without task authorization and verified targets.

## Health, operations, and supply chain

Use lightweight health/readiness checks that reflect actual service behavior, with realistic startup periods and timeouts. Docker HEALTHCHECK status alone does not guarantee a restart, and Kubernetes probes are configured separately rather than inheriting Dockerfile HEALTHCHECK. Do not add curl to a minimal image just for a probe if an existing runtime can perform it.

Send application logs to stdout/stderr with redaction and appropriate retention. Use existing vulnerability scans, linting, signing, SBOM, and provenance processes as relevant; verify current tooling rather than copying deprecated signing advice. Build once and promote an identified artifact. A previous image does not automatically roll back database or external-state changes.

## Verify and diagnose

Run available Dockerfile lint/build checks, validate Compose configuration, and build/run the affected target when a daemon is available and execution is in scope. Test startup, non-root permissions, required files, actual port access, graceful shutdown, health, and persistence as appropriate. Protect secrets when rendering resolved Compose config or inspecting container metadata.

Inspect build logs/cache behavior for slow builds, layers for image bloat, and logs/exit status/dependencies/permissions for crashes. Use no-cache rebuilds only to test a cache hypothesis. Check service names, listener addresses, networks, and published ports for connectivity problems. Report syntax/config inspection separately from an observed build or running-container test. Publishing images, deploying, changing infrastructure, or deleting stored data requires authorization beyond editing these instructions.
