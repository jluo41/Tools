haipipe-paper-claims — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [4.2.0] — 2026-07-09

- Optional **Data Context** preamble added to the artifact spec + template (absorbed D/I rungs): a few anchored description lines (statistic + task-result pointer + as-of date) grounding the Hypotheses when needed; never raw data or inline computation. Ruling context (JL 2026-07-09, application ladder restage): for a paper the dataset is frozen by writing time and the manuscript's Methods/Results carry D/I, so descriptions/themes stay ABSORBED here (Hypotheses play the theme role); the application family externalizes them as full stages 1a-descriptions/1b-themes (intentional twin delta — see application/SOP-ladder-restage.md; its alignment watch maps paper claims-stage changes onto rung 1c).

## [4.1.0] — 2026-07-07

Added (skillset-diagnose T3, JL: "同意。")
- FORWARD reader clause: the `[FORWARD -> CLAIMS]` pointers that seed/draft register in `_LOG_0-seed.md` (internal-data probes deferred out of seed) now have a consumer — claims DRAFT opens by grepping seed's `_LOG` for them; each becomes a PP entry in Probes or is explicitly declined; a new done-criterion fails CHECK on any unconsumed pointer. Closes the writer-without-reader gap (A5/B9): the deferred probe used to die silently at the seed→claims handoff.

## [4.0.0] — 2026-07-06

Changed (major restructure: claims as evidence campaign brain)
- Claims is now the evidence campaign brain: plans evidence needs, commissions work (tasks/discoveries), tracks results. Three jobs: plan, outsource, collect.
- Content structure changed from (Hypotheses, Claims with inline design, Pending Evidence, H-C Alignment) to three sections + summary: Hypotheses, Claims (short: statement + status + probe ref), Probes (full evidence plan per PP number), Evidence Campaign (dispatch order + summary).
- Removed Hypothesis-Claim Alignment section (alignment visible in tags: `C1 (H1)`, `PP03 (C1/C3/C7)`).
- Removed Discussion-Only Interpretations, Robustness, and Pending Evidence sections (probes absorb these roles).
- Added _VALUES_ satellite file for verified numbers backing each supported claim.
- Heading style changed from `#`/`##`/`###` to `=====`/`-----` underlines + `**bold**` sub-items for paper artifacts.
- One-sentence-per-line convention added as a formatting principle.
- Updated ref/claims-template.md to match.

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
