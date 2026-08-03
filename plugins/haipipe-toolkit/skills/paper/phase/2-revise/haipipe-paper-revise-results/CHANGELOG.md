haipipe-paper-revise-results — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.4] — 2026-07-26

- Venue guidance now reads `S-Venue-0-venue.md`.
- DRAFT is a CHECK restart target, not a separate human gate.
- Preserved the invocation hint under `metadata.argument_hint`, which conforms to
  the current Skill frontmatter schema.

## [0.2.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.3.0; older entries below keep their original numbers).

## [2.3.0] — 2026-07-08

Changed (venue lockfile wiring)
- Venue results conventions now read from the paper's `0-lifecycle/2a-venue/2a-venue.md` (Structural Blueprint Results block + Writing Principles); pinned `_venue/playbook-*` pack demoted to fallback when 2a-venue.md is absent; no pack -> skip venue norms.

## [2.2.0] — 2026-07-07

Fixed (skillset-diagnose C5/C6)
- Frontmatter normalized to the family baseline: added `argument-hint` + `allowed-tools` (leaf worker, no Skill dispatch) — was the only worker of 12 without them (defaulted to an all-tool grant).
- Added the `../../REF/prose-quality.md` Before-you-start pointer: the router asserts ALL revise workers read the universal rules; this worker was silently omitting them.

## [2.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC; skill renamed haipipe-paper-polish-results -> haipipe-paper-revise-results.

## [2.0.0] — 2026-07-03

- aligned with DGPC architecture. POLISH is fully automatic (apply directly, leave explanatory comments for CHECK). No human gate.

## [1.1.0] — 2026-06-05

- renamed from results-section-revision to haipipe-paper-polish-results; consolidated into 2-section-edit/ (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.
