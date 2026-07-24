haipipe-end-input2src — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.2.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.1.0; older entries below keep their original numbers).

## [2.1.0] — 2026-07-08

- skill-diagnose fixes: concepts.md caught up with the v2.0.0 platform-specific contract — "two supported formats in one Fn" replaced by one-Fn-per-platform (--platform, default sagemaker); "NOT inside MetaDict" contradiction fixed (top-level AND mirrored into MetaDict); phantom DatabricksV1 marked placeholder; entry-point wording qualified (Step 2, after TrigFn). Records the 7-08 builder-dir edit.

## [2.0.0] — 2026-07-05

### Changed (JL: "方案 A: 一个平台一个 Fn. I choose this one.", decided on the ASCII diagram showing envelope-only diff + both L14/L16 incidents)

- CONTRACT FLIPPED to PLATFORM-SPECIFIC, superseding LESSON L16 (now carries a supersession banner): ONE wire-Fn per deploy platform per use-case; platform goes in the impl name; --platform now SELECTS which platform's Fn design/review targets (default sagemaker), no longer a conformance-check-only flag.
- Pair invariant is per-platform: the SAME-platform pair must roundtrip (mirrored in haipipe-end-src2input 2.0.0).
- Scope: the ruling covers the wire I/O pair only; MetaFn/TrigFn/PostFn stay shared and TrigFn keeps the L14 dataframe_records unwrap. 0-overview + deploy-overview flipped to match.
- Review threads closed and removed (decision archived here).

## [1.2.0] — 2026-07-05

### Changed (JL: "platform可以当作一个optional的，你可以加。而且我们想要什么样子的payload，其实要跟平台相关的。不能随意发挥payload长什么样子")

- Platform contract refined after JL review of 1.1.0 (mirrors haipipe-end-src2input 1.2.0): ONE Fn per endpoint stays (L16), but the payload is platform-CONSTRAINED, conforming to the deploy platform's wire format (SageMaker flat JSON vs Databricks dataframe_records, L14); the one Fn must unwrap both envelopes.
- `--platform sagemaker|databricks` re-added as an OPTIONAL design/review conformance-check argument (omitted = check both); never selects a variant to build.
- Use-case snapshot: 🚩 relabeled "retired pre-L16 per-platform variant (inventory only)"; omitted-use_case fallback now points at disk as the truth.

## [1.1.0] — 2026-07-04

- PLATFORM-AGNOSTIC contract restored per LESSON L16 (was TARGET-AWARE e1_/f1_ with --target flag); flag retired throughout.

## [1.0.0] — 2026-05-31

- baseline metadata added.
