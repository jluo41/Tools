haipipe-task-for-endpoint — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [2.3.0] — 2026-07-08

- skill-diagnose fixes: config-seed build pointer -> endpoint fn_develop task folder (was unqualified retired code-dev path); ref/inference-perf-notes.md retitled as the knowledge base behind /haipipe-end profile (kept — endpointset fn-3-profile reads it; task-side profiling scope was retired in 2.2.0).

## [2.2.0] — 2026-07-04

- CONFIRMED by JL 2026-07-05 ("ok 我同意。"); review thread removed from fn/scaffold.md.
- fn/scaffold.md + ref/workflow-plan-sample.yaml REWRITTEN from the retired inference-profiling scope (P-groups, ProfileArgs, latency.json, skill: haipipe-task-for-inference) to the 2.x endpoint-packaging scope (c_endpoint_nb.py, Endpoint_Pipeline, Setup->Package->Verify->Report); profiling pointer now /haipipe-end profile; metadata summary + body letter-neutral; store layout points at the canonical 0-overview; CHANGELOG reordered newest-first.

## [2.1.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow; reviewer name haipipe-task-reviewer-agent; fn relative hub path ../../../haipipe-task.

## [2.0.0] — 2026-06-12

- rewritten from inference-profiling to endpoint-building scope. Renamed from haipipe-task-for-inference.
## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.

## [1.0.0] — 2026-06-01

- created as haipipe-task-for-inference (latency profiling).

