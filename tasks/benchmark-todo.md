# Scalability benchmark checklist

## Task 1 — Build a repeatable fixture and runner

Use local synthetic data and the existing source override. Keep the benchmark
outside the app's normal request path and document how to run it.

- [ ] A fixed seed reproduces each fixture and its expected page results.
- [ ] A tiny smoke run verifies totals, stable order, and paged results.

Scope is small. Expected files are under `scripts/` and, if needed, `tests/`.
Dependencies are none.

## Task 2 — Measure the existing endpoint

Run the workload matrix in the plan with warmup and repeated runs. Shorten or
stop a cell if error rates or timeouts make further timing uninformative.

- [ ] Publish per-workload p50, p95, throughput, errors, and peak server memory.
- [ ] Compare disk-backed and prevalidated source runs under matching settings.
- [ ] Record the command, environment, revision, and fixture seed.

Scope is small. Record results and commands under `tasks/`. Depends on Task 1.

## Checkpoint after Tasks 1–2

- [ ] Independently rerun a sample workload and check the variance.
- [ ] Review the latency and memory results against the intended usage.

## Task 3 — Decide what to change and what to check in CI

Use the baseline to recommend the next implementation step. Put any missing
deterministic correctness check in an existing suite and CI job.

- [ ] Name the measured bottleneck or record why the evidence is inconclusive.
- [ ] Keep full benchmarks advisory until repeatability and a target support a gate.

Scope is small. Update the findings and any owning test. Depends on Task 2.
