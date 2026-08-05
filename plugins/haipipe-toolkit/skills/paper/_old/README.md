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
round-duplicates/   paper-rebuttal · rebuttal-response (pre-family duplicates of the phase3-retired rebuttal skill)
container-merged/   haipipe-paper-scaffold · haipipe-paper-restructure (merge candidates, see debts below)
phase-remnants/     phase/ README files and haipipe-paper-revise-content
                    (REF/ did NOT retire: live skills still read it, so it lives at paper/workers/REF/)
quality/            earlier retirement round (claim-audit, optimizer, polish, reviewer)
phase3-260806/      thin-paper PHASE 3 (JL ruling 260806: ONE registered skill, the door).
                    haipipe-paper-folder -> fn/folder.md · haipipe-paper-conform ->
                    fn/conform.md + scripts/check_structure.sh · the five S09-build skills
                    (compile, diffpdf, project, to-overleaf, to-word) -> fn/<verb>.md +
                    scripts/{diffpdf,project,to-word}/ · haipipe-paper-round +
                    haipipe-paper-rebuttal -> the round STAGE (S10-round/round/stage.md +
                    template.md + ../rebuttal-craft.md, row in stages/index.yml)
```

## Debts: what the door's folder and conform fns still owe

(Heirs repointed 260806, thin-paper phase 3: the folder/conform/compile skills named
below retired to `phase3-260806/`; their fn heirs inherit the debts unchanged.)

- FROM `container-merged/haipipe-paper-scaffold` → owed by the door's `fn/folder.md`:
  the on-request manuscript upgrade (plan → compileable LaTeX skeleton in the ruled
  layout: driver.tex, sections/ leaves, 2-src/compile.sh, the templates/*.tpl set).
  folder today ships only the minimal Board-first scaffold and points at scaffold
  for this upgrade; that pointer now lands here until folder absorbs it.
- FROM `routers/haipipe-paper-deliver` → owed by the door's `fn/compile.md`
  (natural heir): a live home for the Lifecycle TeX Quality Standard (deliver
  SKILL.md was THE home of its full text; two live files cited the standard by
  name and state its one-line rule inline: haipipe-paper-enter/SKILL.md and
  haipipe-paper-stage/ref/09-stage-illuminate.md, both themselves now in _old/;
  the illuminate ref lives on at paper/haipipe-paper/ref/09-stage-illuminate.md).
- FROM `container-merged/haipipe-paper-restructure` → owed by the door's `fn/conform.md`:
  the FIX half of conformance (existing paper → ruled layout with prose
  byte-identical, compile verified, delete test passing). conform today is
  report-only; the repair flow it reports against lived in restructure.

## Note on REF/

The old `phase/REF/` shared prose docs are still read by live skills
(paper/workers/haipipe-paper-revise-results, writing/haipipe-paper-revise-humanizer,
the paper/haipipe-paper router), and the stage router's law says nothing under
_old/ may be referenced by a live file. So REF/ moved to `paper/workers/REF/`,
not here. Phase 2 may still relocate or absorb it.
