haipipe-insight-knowledge — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [2.0.0] — 2026-07-05

- `claim_type` (associational | causal, REQUIRED on K since layer 3.1.0) added everywhere the writer works: Input, hard rules, workflow Steps 2-3, quick-reminder frontmatter, DoD, argument-hint. The writer previously emitted K cards the K reviewer's claim_type check would fail.
- Back-links corrected: K{NN} goes into cited I cards' `ref_by:` (was "cited P/D entries' Cross-references": no P layer exists and no such body section exists).
- Supersede aligned to schema: frontmatter `supersedes:`/`superseded_by:` + `## Change log` (was "in body via supporting evidence section"); nonexistent `contradicts` field dropped (live disagreement = `status: contested`).
- Description recut to generalization-claim language (was "judged claim as a validated belief").
- Mandatory-read paths fixed: `../../ref/` → `../ref/` (3 sites).
- Backfill note: the body had already been recut on 2026-06-22 (no probe gate, negative K, `--id`) without a version bump; changelog also reordered newest-first (was 1.1.0, 1.0.0, 1.2.0).

## [1.2.0] — 2026-06-20

- repositioned as review-called judged-source writer API.

## [1.1.0] — 2026-05-31

- K sources a confirmed probe's claim (was >=1 I card); cites supporting I cards in the body.

## [1.0.0] — 2026-05-31

- baseline metadata added.
