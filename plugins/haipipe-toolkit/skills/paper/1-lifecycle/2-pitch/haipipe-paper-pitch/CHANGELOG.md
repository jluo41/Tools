haipipe-paper-pitch — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (wiki/08): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [3.1.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.1.1] — 2026-07-03

- converted canonical template to ref/pitch-template.md (plain markdown, no LaTeX, no compile); deleted ref/pitch-template.tex.

## [3.1.0] — 2026-07-03

- pitch becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Comment lifecycle wired in (wiki/02). Shared Protocols section removed.

## [3.0.0] — 2026-07-01

- pitch is now venue-ALIGNED = cover letter. Absorbs Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing from claims. Claims is now venue-FREE (pure evidence inventory). Pitch reframes venue-neutral hypotheses (H1→RQ1) for the target editor.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. PITCH_LOG.md merged into _LOG_2-pitch.md. Argument documents are markdown; only display compiles to PDF.

## [unversioned]

- v1.5.2: extracted template to ref/pitch-template.tex; inline replaced with reading-order summary

## [unversioned]

- v1.5.1: added mandatory compile-after-edit rule; venue awareness note

## [1.5.0] — 2026-06-22

- added Title section, multi-hook candidates, template enforcement, quality gate; wired illuminate+gate+compile protocols

## [1.4.0] — 2026-06-22

- readability rules, section cues, hook catalog
