haipipe-end-endpointset — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.3.0] — 2026-07-08

- skill-diagnose fixes: store paths corrected to {endpoint_name}/ (no Endpoint- prefix exists on disk); dashboard external/ demoted required->conditional (absent from all real XGB sets — dashboard flagged every real endpoint broken); fn-1-package layout restatement -> pointer to 0-overview per its own no-restate rule; fn-3-profile ProjA example -> illustrative; fn_endpoint noted as 5 Fn-types + fn_example helper; platforms/ prefix.

## [1.2.0] — 2026-07-04

- Endpoint_Set layout block aligned to the canonical 0-overview Stage-6 layout (was drifted: fn_endpoint/ModelInstance/manifest.yaml); fn-3-profile: retired /haipipe-task-for-inference routes -> /haipipe-task-for-endpoint, off-by-one hub path fixed; C-series line letter-neutral.

## [1.1.0] — 2026-06-01

- added `profile` verb (latency breakdown + per-arm decomposition; fn-3-profile.md). Durable/reproducible version of the same profile lives in task /haipipe-task-for-inference.

## [1.0.0] — 2026-05-31

- baseline metadata added.
