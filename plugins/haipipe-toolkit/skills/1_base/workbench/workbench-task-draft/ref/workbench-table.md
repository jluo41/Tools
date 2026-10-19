Page Workbench Table
====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output: the Guide, then Draft, Evidence and Delivery, the order a Page
moves.

The Page Workbench (`servers/workbench/workbench-task-draft/outline.py`, route `/_board/draft`)
shows one Page, so every row is Level `page`. Each working row is one
`🔘 BUTTON` of `haipipe-draft-workflow/ref/run-cards.md`; its Skill is the
card's `🧩 SKILL` (one skill: a writing skill the card also names is loaded by
it). The Guide rows have no card: Guide's own Runs panel reads them from this
table.

Makers and judges stay apart: Check is done by `haipipe-draft-check-agent`,
which makes nothing on this screen and cannot approve a version it produced.
`(new)` marks an agent or skill planned but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| page | Guide | Description | none | none | none | none |
| page | Guide | Method | Add a method | haipipe-draft-writing-agent | workbench-task-draft | none |
| page | Guide | RoadMap Draw | Redraw the Workbench design | haipipe-studio-agent (new) | workbench-task-draft | none |
| page | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |
| page | Draft | Table | Context | haipipe-draft-context-agent | haipipe-draft-logic | none |
| page | Draft | Table | Structure revise | haipipe-draft-structure-agent | haipipe-draft-logic | the plan |
| page | Draft | Scratch | Scratch | haipipe-draft-writing-agent | haipipe-draft-logic | none |
| page | Draft | RoadMap Draw | Draw the logic | haipipe-studio-agent (new) | draw-logic-tree | the logic |
| page | Draft | RoadMap Draw | Redraw the Section map | haipipe-studio-agent (new) | excalidraw-draft | none |
| page | Draft | Revise | Section revise | haipipe-draft-writing-agent | haipipe-draft-writing | none |
| page | Draft | Revise | Paragraph revise | haipipe-draft-writing-agent | haipipe-draft-writing | none |
| page | Draft | Revise | Revise edits | haipipe-draft-writing-agent | haipipe-draft-writing | the edits kept |
| page | Draft | Reading | Auto write | haipipe-draft-writing-agent | haipipe-draft-writing | adopting the draft |
| page | Draft | Table | Evidence embed | haipipe-draft-evidence-agent | haipipe-evidence | none |
| page | Evidence | Citations | Bind / update citation | haipipe-draft-evidence-agent | haipipe-evidence | the source check |
| page | Evidence | Displays | Build figure / table | haipipe-display-unit-agent | haipipe-display | accepting the display |
| page | Evidence | Values | Bind / update value | haipipe-draft-evidence-agent | haipipe-evidence | none |
| page | Delivery | Preview · Artifacts | Build | haipipe-draft-writing-agent | haipipe-delivery | none |
| page | Delivery | Checks | Check | haipipe-draft-check-agent | haipipe-draft-review | release |

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
- **Add a method.** Guide › Method's run writes one card in `ref/methods/<family>/`, adds
  its row to `servers/workbench/workbench-task-draft/guide/method.md`, and its papers to `servers/workbench/workbench-task-draft/related/papers.md` (checked
  `--online` first). The methods canvas, `guide/methods.excalidraw`, is then edited on
  the canvas: it is the source, and `method-canvas.py --force` redraws it only when the
  person asks.
