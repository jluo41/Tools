haipipe-paper-section-edit — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.1.2] — 2026-07-03

Fixed
- Closing-block example phase line `probe: cite 🚀` corrected to `probe: cite 🔥🚀` (exactly-one-marker rule: active sub-track at the frontier collapses both markers).

## [3.1.1] — 2026-07-03

Fixed
- "Dual status strip" section renamed to "Closing block (section-aware)" and aligned with the umbrella Closing Block spec: simplified tail (status merged with stage + section, no paper_root), stage/phase line labels, marker legend replaced by a pointer to the umbrella (keeping only the local ⚠️ re-sync marker).

## [3.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers 2-phase/1-probe/haipipe-paper-probe-*, 2-phase/2-revise/haipipe-paper-revise-*); phase strip sub-tracks now render as 'probe: cite/val/disp'.

## [3.0.1] — 2026-07-03

- per-paper folder renamed 5-editing -> 5-section-edit; all paths and trigger words updated. No workflow changes.

## [3.0.0] — 2026-07-02

- two-axis restructure. Phase workers moved to 2-phase/ (shared across stages). GATHER becomes agent-only (flag issues, no mid-phase human gate; PLACE moves to CHECK). POLISH works on both outline .md and tex (outline is primary, tex is compiled output). CHECK becomes the single human gate (verify citations on Scholar, verify values, approve displays, 6-axis pass/fail). _LOG format gets [PHASE] tags. Per-stage files: narrative and pitch also get _CITATION_. Citation: no bibtex in _CITATION_ (plain text only), provenance tracking.

## [2.1.0] — 2026-06-29

- renamed phases PLAN→DRAFT, WRITE→POLISH (DRAFT includes draft sentences, POLISH is venue-quality rewrite not cold-start). Added dual status strip (paper-level + section-level). Added section dashboard showing all sections' layer status. Per-stage _PROBE/ folders with 1-probe-plans/ as cross-paper index. Added _EVIDENCE_ for claims, _DISPLAY_ for narrative.

## [2.0.0] — 2026-06-29

- combined haipipe-paper-editing + haipipe-paper-edit into one skill.

## [unversioned]

- 1.4.0-1.0.0: see prior changelog.
