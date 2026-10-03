Page Workbench Table
====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output: the Guide, then Draft, Evidence and Delivery, the order a Page
moves.

The Page Workbench (`servers/workbench-page/outline.py`, route `/_board/draft`)
shows one Page, so every row is Level `page`. Each working row is one
`🔘 BUTTON` of `haipipe-page-workflow/ref/run-cards.md`; its Skill is the
card's `🧩 SKILL` (one skill: a writing skill the card also names is loaded by
it). The Guide rows have no card: Guide's own Runs panel reads them from this
table.

Makers and judges stay apart: Check is done by `haipipe-page-check-agent`,
which makes nothing on this screen and cannot approve a version it produced.
`(new)` marks an agent or skill planned but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| page | Guide | Description | none | none | none | none |
| page | Guide | Method | none | none | none | none |
| page | Guide | RoadMap Draw | Redraw the Workbench design | haipipe-studio-agent (new) | haipipe-workbench-page | none |
| page | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |
| page | Draft | Table | Context | haipipe-page-context-agent | haipipe-page-context | none |
| page | Draft | Table | Structure revise | haipipe-page-structure-agent | haipipe-page-structure | the plan |
| page | Draft | Scratch | Scratch | haipipe-page-writing-agent | haipipe-page-scratch | none |
| page | Draft | RoadMap Draw | Draw the logic | haipipe-studio-agent (new) | draw-logic-tree | the logic |
| page | Draft | Revise | Section revise | haipipe-page-writing-agent | haipipe-page-writing | none |
| page | Draft | Revise | Paragraph revise | haipipe-page-writing-agent | haipipe-page-writing | none |
| page | Draft | Revise | Revise edits | haipipe-page-writing-agent | haipipe-page-revise | the edits kept |
| page | Draft | Reading | Auto write | haipipe-page-writing-agent | haipipe-page-writing | adopting the draft |
| page | Draft | Table | Evidence embed | haipipe-page-evidence-agent | haipipe-page-evidence | none |
| page | Evidence | Citations | Bind / update citation | haipipe-page-evidence-agent | haipipe-page-evidence | the source check |
| page | Evidence | Displays | Build figure / table | haipipe-display-unit-agent | haipipe-display | accepting the display |
| page | Evidence | Values | Bind / update value | haipipe-page-evidence-agent | haipipe-page-evidence | none |
| page | Delivery | Preview · Artifacts | Build | haipipe-page-writing-agent | haipipe-page-delivery | none |
| page | Delivery | Checks | Check | haipipe-page-check-agent | haipipe-page-check | release |

Notes
-----

- **Structure.** The Draft Space's Structure fold has no button of its own: the
  plan is changed by Structure revise, and the person approves it (`approved:`).
- **Supporting Runs.** The Evidence Space also lists the Page's Supporting Runs
  (Task and Discovery Results an item cites). They are run by their own owners
  (`haipipe-task`, `haipipe-discovery`) and are not rows here.
- **One Page, many families.** Section Pages, Task Pages, Discovery Pages and
  Insight pages all open this workbench; a family adds its own runs on its own
  Board screen, never here.
