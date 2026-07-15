haipipe-end-src2input — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [2.1.0] — 2026-07-08

- skill-diagnose fixes: concepts.md caught up with the v2.0.0 platform-specific contract — Output section now shows BOTH shapes (sagemaker flat JSON = default, databricks envelope) instead of presenting the envelope as the only form; phantom DatabricksV1 marked placeholder; example_000 naming (no uuid suffix). Records the 7-08 builder-dir edit.

## [2.0.0] — 2026-07-05

### Changed (JL: "方案 A: 一个平台一个 Fn. I choose this one.", decided on the ASCII diagram showing envelope-only diff + both L14/L16 incidents)

- CONTRACT FLIPPED to PLATFORM-SPECIFIC, superseding LESSON L16 (now carries a supersession banner): ONE wire-Fn per deploy platform per use-case; platform goes in the impl name; --platform now SELECTS which platform's Fn design/review targets (default sagemaker), no longer a conformance-check-only flag.
- Pair invariant is per-platform: the SAME-platform pair must roundtrip (mirrored in haipipe-end-input2src 2.0.0).
- Scope: the ruling covers the wire I/O pair only; MetaFn/TrigFn/PostFn stay shared and TrigFn keeps the L14 dataframe_records unwrap. 0-overview + deploy-overview flipped to match.
- Review threads closed and removed (decision archived here).

## [1.2.0] — 2026-07-05

### Changed (JL: "payload最终是要符合databricks的格式，或者sagemaker的格式，而不是让他随心所欲发挥任何payload的格式" / "platform可以当作一个optional的，你可以加")

- Platform contract refined after JL review of 1.1.0: ONE Fn per endpoint stays (L16), but the "identical wire contract on every deploy target" wording was WRONG. The payload is platform-CONSTRAINED: it must conform to the deploy platform's wire format (SageMaker flat JSON vs Databricks dataframe_records, L14), and the one Fn must satisfy both envelopes.
- `--platform sagemaker|databricks` re-added as an OPTIONAL design/review argument: scopes the wire-format conformance check to one target (omitted = check both). It never selects a per-platform variant to build.
- Use-case snapshot: 🚩 relabeled "retired pre-L16 per-platform variant (inventory only)"; omitted-use_case fallback now says disk is the truth (snapshot goes stale).

## [1.1.0] — 2026-07-04

- PLATFORM-AGNOSTIC contract restored per LESSON L16 + 0-overview (was TARGET-AWARE with per-target d1_/f2_ builders and --target flag, contradicting 'one Fn set per endpoint'); --target retired from description, hint, verb axis, commands.

## [1.0.0] — 2026-05-31

- baseline metadata added.
