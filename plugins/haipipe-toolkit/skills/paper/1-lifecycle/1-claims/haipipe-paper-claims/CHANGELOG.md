haipipe-paper-claims — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.2.0] - 2026-07-05

Changed
- Ledger is now PROSE ONLY, no tables. Dropped both markdown tables from ref/claims-template.md: the Claim-Evidence Matrix (`| ID | Claim | Status |`) is replaced by a `## Claims` section of one `### C<n> - <title> (<H>, <role>) - <status>` prose subsection per claim, and the Hypothesis-Claim Alignment table is replaced by a paragraph. Scrubbed all "matrix"/"row" language from SKILL.md (Artifact Spec, done-criteria, DRAFT step, template reading order, gates, Ledger Maintenance) and rewrote principle 6 as "Prose subsections, no tables". Codifies JL's standing rule (papers/ledgers never group claims/evidence in tables) so the template stops regenerating them.

## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (wiki/08): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [3.1.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.1.1] — 2026-07-03

- converted canonical template to ref/claims-template.md (plain markdown, no LaTeX, no compile); deleted ref/claims-template.tex.

## [3.1.0] — 2026-07-03

- claims becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Removed inline workflow steps and shared-protocol references. Comment lifecycle wired in (wiki/02).

## [3.0.0] — 2026-07-01

- claims is now venue-FREE. Editor's Chair Test, [primary] designation, and venue-shaped RQs migrated to pitch (the cover letter). Claims keeps venue-neutral hypotheses (H1, H2, H3) and a pure evidence inventory reusable across venues.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF. Claims create PP probe plans in 1-probe-plans/ for evidence gaps.

## [unversioned]

- v1.3.0: added editor's chair test, RQs in claims (not pitch), RQ→Claim→Answer alignment table, probe plans buffer convention, extracted template to ref/claims-template.tex

## [unversioned]

- v1.2.0: added illuminate protocol + cross-refs to stage-gate, tex-quality
