# Scalability benchmark checklist

See the [benchmark results](benchmark-results.md) for commands, measurements,
the saturation cutoff, and the recommended follow-up.

## Task 1 — Build a repeatable fixture and runner

Use local synthetic data and the existing source override. Keep the benchmark
outside the app's normal request path and document how to run it.

- [x] A fixed seed reproduces each fixture and its expected page results.
- [x] A tiny smoke run verifies totals, stable order, and paged results.

Scope is small. Expected files are under `scripts/` and, if needed, `tests/`.
Dependencies are none.

## Task 2 — Measure the existing endpoint

Run the workload matrix in the plan with warmup and repeated runs. Shorten or
stop a cell if error rates or timeouts make further timing uninformative.

- [x] Publish per-workload p50, p95, throughput, errors, and peak server memory.
- [x] Compare disk-backed and prevalidated source runs under matching settings.
- [x] Record the command, environment, revision, and fixture seed.

Scope is small. Record results and commands under `tasks/`. Depends on Task 1.

## Checkpoint after Tasks 1–2

- [x] Independently rerun a sample workload and check the variance.
- [x] Review latency and memory against the exploratory scenarios. Deployment
  capacity remains unverified pending a traffic and latency target.

## Task 3 — Decide what to change and what to check in CI

Use the baseline to recommend the next implementation step. Put any missing
deterministic correctness check in an existing suite and CI job.

- [x] Name the measured bottleneck or record why the evidence is inconclusive.
- [x] Keep full benchmarks advisory until repeatability and a target support a gate.

Scope is small. Update the findings and any owning test. Depends on Task 2.
