Page Workbench Table
====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output: the Guide, then Draft, Evidence and Delivery, the order a Page
moves.

The Page Workbench (`servers/workbench/workbench-task-draft/plan_outline/outline.py`, route `/_board/draft`)
shows one Page, so every row is Level `page`. Each working row is one
`🔘 BUTTON` of `hai-draft-workflow/ref/run-cards.md`; its Skill is the
card's `🧩 SKILL` (one skill: a writing skill the card also names is loaded by
it). The Guide rows have no card: Guide's own Runs panel reads them from this
table.

Makers and judges stay apart: Check is done by `hai-draft-check-agent`,
which makes nothing on this screen and cannot approve a version it produced.
`(new)` marks an agent or skill planned but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| page | Guide | Description | none | none | none | none |
| page | Guide | Method | Add a method | hai-draft-writing-agent | workbench-task-draft | none |
| page | Guide | RoadMap Draw | Redraw the Workbench design | hai-studio-agent (new) | workbench-task-draft | none |
| page | Guide | Related Paper | Add a paper | hai-discovery-orchestrator-agent | hai-discovery | the source check |
| page | Draft | Table | Context | hai-draft-context-agent | hai-draft-logic | none |
| page | Draft | Table | Structure revise | hai-draft-structure-agent | hai-draft-logic | the plan |
| page | Draft | Scratch | Scratch | hai-draft-writing-agent | hai-draft-logic | none |
| page | Draft | RoadMap Draw | Draw the logic | hai-studio-agent (new) | draw-logic-tree | the logic |
| page | Draft | RoadMap Draw | Redraw the Section map | hai-studio-agent (new) | hai-draw draft | none |
| page | Draft | Revise | Section revise | hai-draft-writing-agent | hai-draft-writing | none |
| page | Draft | Revise | Paragraph revise | hai-draft-writing-agent | hai-draft-writing | none |
| page | Draft | Revise | Revise edits | hai-draft-writing-agent | hai-draft-writing | the edits kept |
| page | Draft | Reading | Auto write | hai-draft-writing-agent | hai-draft-writing | adopting the draft |
| page | Draft | Table | Evidence embed | hai-draft-evidence-agent | hai-evidence | none |
| page | Evidence | Citations | Bind / update citation | hai-draft-evidence-agent | hai-evidence | the source check |
| page | Evidence | Displays | Build figure / table | hai-display-unit-agent | hai-display | accepting the display |
| page | Evidence | Values | Bind / update value | hai-draft-evidence-agent | hai-evidence | none |
| page | Delivery | Preview · Artifacts | Build | hai-draft-writing-agent | hai-delivery | none |
| page | Delivery | Checks | Check | hai-draft-check-agent | hai-draft-review | release |

Notes
-----

- **Structure.** The Draft Space's Structure fold has no button of its own: the
  plan is changed by Structure revise, and the person approves it (`approved:`).
- **Supporting Runs.** The Evidence Space also lists the Page's Supporting Runs
  (Task and Discovery Results an item cites). They are run by their own owners
  (`hai-task`, `hai-discovery`) and are not rows here.
- **One Page, many families.** Section Pages, Task Pages, Discovery Pages and
  Insight pages all open this workbench; a family adds its own runs on its own
  Board screen, never here.
- **Add a method.** Guide › Method's run writes one card in `ref/methods/<family>/`, adds
  its row to `servers/workbench/workbench-task-draft/guide/method.md`, and its papers to `servers/workbench/workbench-task-draft/related/papers.md` (checked
  `--online` first). The methods canvas, `guide/methods.excalidraw`, is then edited on
  the canvas: it is the source, and `method-canvas.py --force` redraws it only when the
  person asks.
