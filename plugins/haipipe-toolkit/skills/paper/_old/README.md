# paper/_old/: retired skills (moved, never deleted)

Retirements from the thin-paper restructure, ruled A on
`diagrams/01-haipipe-paper-260725/QC-engine/QC6-paper-skill-folder.md` (JL 260805).
Nothing here is registered by `install.sh` (underscore prefix is pruned).

## What lives where

```text
phase-hubs/         haipipe-paper-draft · haipipe-paper-revise · haipipe-paper-check
                    (page logic now lives in board/page-phases/haipipe-board-page-draft / -revise / -check;
                     worker dispatch now goes straight to paper/workers/*)
routers/            haipipe-paper-deliver (redundant router; its leaves live on in S09-build/)
round-duplicates/   paper-rebuttal · rebuttal-response (pre-family duplicates of S10-round/haipipe-paper-rebuttal)
container-merged/   haipipe-paper-scaffold · haipipe-paper-restructure (merge candidates, see debts below)
phase-remnants/     phase/ README files and haipipe-paper-revise-content
                    (REF/ did NOT retire: live skills still read it, so it lives at paper/workers/REF/)
quality/            earlier retirement round (claim-audit, optimizer, polish, reviewer)
```

## Debts: what container/haipipe-paper-folder and container/haipipe-paper-conform still owe

- FROM `container-merged/haipipe-paper-scaffold` → owed by `haipipe-paper-folder`:
  the on-request manuscript upgrade (plan → compileable LaTeX skeleton in the ruled
  layout: driver.tex, sections/ leaves, 2-src/compile.sh, the templates/*.tpl set).
  folder today ships only the minimal Board-first scaffold and points at scaffold
  for this upgrade; that pointer now lands here until folder absorbs it.
- FROM `routers/haipipe-paper-deliver` → owed by `S09-build/haipipe-paper-compile`
  (natural heir): a live home for the Lifecycle TeX Quality Standard (deliver
  SKILL.md was THE home of its full text; two live files cite the standard by
  name and state its one-line rule inline: haipipe-paper-enter/SKILL.md and
  haipipe-paper-stage/ref/09-stage-illuminate.md).
- FROM `container-merged/haipipe-paper-restructure` → owed by `haipipe-paper-conform`:
  the FIX half of conformance (existing paper → ruled layout with prose
  byte-identical, compile verified, delete test passing). conform today is
  report-only; the repair flow it reports against lived in restructure.

## Note on REF/

The old `phase/REF/` shared prose docs are still read by live skills
(paper/workers/haipipe-paper-revise-results, writing/haipipe-paper-revise-humanizer,
the paper/haipipe-paper router), and the stage router's law says nothing under
_old/ may be referenced by a live file. So REF/ moved to `paper/workers/REF/`,
not here. Phase 2 may still relocate or absorb it.
