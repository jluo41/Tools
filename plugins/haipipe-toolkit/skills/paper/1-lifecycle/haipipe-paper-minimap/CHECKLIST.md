# haipipe-paper-minimap — Done Checklist

The minimap stage is done when ALL hold. Present each as check/fail at the exit gate (`../../ref/stage-gate.md`); advance only on explicit user confirm.

## Form (paper-in-miniature)

- [ ] `5-minimap.tex` is the paper IN MINIATURE, not a job table: every manuscript paragraph is a `\pspine` head + sentence-points, not a table row.
- [ ] Every paragraph has **4-5 sentence-points** (one point = one manuscript sentence; ~6 is the hard ceiling; not 2-3). [R4]
- [ ] Section order + abstract form match the pinned venue's `-> Minimap` mapping in the resolved `_venue/playbook-<venue>` pack.

## The 7 build rules (2026-06-24 digest)

- [ ] **R1 title** — `\title` is the paper title only, short, shaped to the venue; no descriptive subtitle.
- [ ] **R2 claim tags** — every `\cl{Cn}` shows a content gloss `[C1: <phrase>]`, never a bare `[C1]`; the `clg@Cn` lookup is seeded from `2-claims.tex`.
- [ ] **R3 notes lean** — every `\nnote` is one clause and carries NO "verb, role." editorial prefix (no keep/add/demoted).
- [ ] **R5 no coverage check** — there is NO printed Coverage Check crosswalk; the orphan claim/display check ran as a silent lint instead.
- [ ] **R6 supplement synced** — the eAppendix is derived from the real SI (`0-sections/{A..}*.tex` + any `0-Supplementary-*.tex`); each item maps to a main beat; a planned-but-undrafted item is a `\wt`.
- [ ] **R7 advisor feedback** — advisor comments are baked below the note they concern via `\pfb{status}{comment}{resolution}` (pulled from `3-narrative.tex` `\fb`); still-open ones appear in Write-Time Reconciliations.

## Anchors + coverage

- [ ] Every `supported` claim in `2-claims` is carried by >=1 paragraph.
- [ ] Every planned display in `4-display` is placed via `\dcall` + `\input` (inline thumbnail) in the paragraph where it is first discussed.
- [ ] Every `[PENDING]`/`[GAP]` evidence need surfaces as a `\wt` Write-Time Reconciliation, routed (probe/task/citation).

## Compile

- [ ] `5-minimap.pdf` compiled from the paper root (thumbnails resolve), current, no errors (font-shape substitution warnings are fine).
- [ ] `STATUS.md` updated on confirm (`current_layer`, `maturity: section-map`, Gate Ledger).
