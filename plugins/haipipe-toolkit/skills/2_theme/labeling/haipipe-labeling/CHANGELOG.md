# haipipe-labeling · CHANGELOG

## 0.10.0 · 2026-10-07

Renamed from `subjective-label` to `haipipe-labeling`, the door name every theme
uses (`haipipe-<theme>`, JL 261007); the folder is `skills/2_theme/labeling/haipipe-labeling/`.
The view skills (`subjective-label-<view>`), schema ids (`subjective-label/v2`, ...)
and the receipt `domain` keep their names. `workbench-labeling` moved up to
`skills/2_theme/labeling/workbench-labeling/` in the same change.

## 0.9.1 · 2026-09-29

Clarify that a View context Skill is one of several Skills declared by a Run
Type. The Run Type table names shared workflow, domain, and procedure Skills
as well; a historical Run's actual Skill usage is not inferred from that table.

## 0.9.0 · 2026-09-29

Add the VIEW layer: eleven view skills, one per workbench view, never shared
(JL 260929). A Run card names only its view skill; route a Run request there.

## 0.7.0 · 2026-09-01

Replace four phase-sized Runs with 25 independently closable P0-P5 operation
kinds. Keep episodes and human gate events outside the Run count, and separate
planned counts from receipt-backed actual inventory.

## 0.6.0 · 2026-09-01

Separate the Level-3 Labeling job from its Level-4 Runs and route allocation,
resume, presentation, and audit through the new Labeling Run dialect.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
