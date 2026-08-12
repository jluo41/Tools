haipipe-application-check — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.4.3] — 2026-08-04

- Layers the application checker on the Stage Page Type and generic `haipipe-page-check` routing contract.
- Leaves application checkers, comment seeding, and the Gate Ledger local while the shared phase owns judgment boundaries.


## [0.4.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 4.2.0; older entries below keep their original numbers).

## [4.2.0] — 2026-07-17

- Back-port paper-check's checker hardening: replace the fragile hard-coded `../../1-probe/...check-probe-cards.sh` path with a layout-agnostic `find … -path "*haipipe-application-probe*" -name check-probe-cards.sh` glob (path-filtered so it cannot resolve to the paper family's checker) + a not-found FAIL. A missing checker is a FAIL, never a silent skip.

## [1.0.0] — 2026-05-31

- baseline.

## [2.0.0] — 2026-06-23

- venue-gated; updated stage names to paper vocabulary; simplified for lifecycle model.

## [3.0.0] — 2026-07-06

- renamed from haipipe-application-gate, re-homed shared/ -> 2-phase/3-check/ as the CHECK phase worker; Gate Ledger protocol (STATUS.md, By column); stage list on the new spine; persona/attendance kept (unattended stand-in only) (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.1.0] — 2026-07-06

- 765696f port: claims exit criteria read the Evidence Campaign (C<n>/PP<nn> sub-items, dispatch order + deps) instead of the old prose-subsection/_EVIDENCE_ shape.

## [4.0.0] — 2026-07-07

- paper-check 1.7.0 enforcement port (alignment round 2, SOP §3 R2 / §4 rows 4-5): step 1 Run now executes `./checks.sh <artifact-or-dir> [--md ...] [--depth N]` (NEW in-folder script, markdown-safe subset of paper's: em-dash ❌ house rule, AI-voice tells ⚠️ with the mawk-safe tolower()+boundary-class grep, TODO/FIXME ❌, bibtex-in-markdown ❌; tex machinery — \cite/\ref/\label orphans, Pn.Sn sequence, --compile — deliberately NOT ported) AND the probe-card checker `../../1-probe/haipipe-application-probe/check-probe-cards.sh <intervention_root>`; any ❌/FAIL blocks the gate green, and no persona preset, --unattended timeout, or venue override can approve over it (mechanics fire at every venue depth; scaling governs report verbosity only).
- `> CHECK:` comment seeding in 0-lifecycle STAGE DOCS ONLY (R2c RULED, JL 2026-07-07: stage-docs-only over artifact HTML-comments and over keeping check fully read-only): 0-artifacts/*.md stay clean because the artifact IS the deliverable text; artifact-level findings land in the Gate Ledger notes column with file:line; on revise the restarted phase reads the stage-doc threads + `> USER:` replies (paper's restart pattern); resolved threads archive to the stage `_LOG`. Risk profile updated (was fully READ-ONLY on stage docs); return contract gains `mechanical:` + `seeded:` lines.
- Kept untouched: persona presets (gate-persona.md), attendance modes (attendance-modes.md), venue-scaled gate depth, Gate Ledger row format. Housekeeping: 3.1.0 landed in this changelog without a frontmatter bump; resolved by this version.

## [4.1.0] — 2026-07-09

- New `grow` verdict for GROW-loop rungs (JL: "after the check, they can think about adding more probes in the draft"): the gate asks "which data topics / probes are still missing?"; grow converts the user's answers to new slots + planned probe skeletons and re-opens DRAFT as [ROUND n+1]. Approve at these rungs = saturated AND the user added nothing.
