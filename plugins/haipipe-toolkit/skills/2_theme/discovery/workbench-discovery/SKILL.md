---
name: workbench-discovery
description: >-
  Open and interpret a Discovery Block Workbench, in the same style as the Task and
  CoWork workbenches: Scope (Block, Questions, Resources, RoadMap Draw), Work (Papers:
  every Paper Run with its Result card; Tasks: each Task Page and its synthesis;
  Questions as Logic │ Work │ Report rows), Check (Runs, Citations, Reports) and
  Delivery (Reports, BibTeX), each with the shared Runs panel, and the shared Guide.
  Also the Project view: every Discovery Block of a Project in one table. Use to see
  which papers a Block has read, which Runs are blocked, which citations still need a
  person, or a Block's Questions. The Block contract and the Runs belong to
  haipipe-discovery; report writing to haipipe-page.
metadata:
  version: "0.3.0"
  last_updated: "2026-10-07"
---

# Discovery Block Workbench

One `discoveries/bNN_*/board.md` declaring `board-kind: discovery-block` opens one
Workbench (`haipipe-discovery` owns the Block, its Jobs, Task Pages and Paper Runs). It is
drawn as the Task and CoWork workbenches are (JL 261004: separate workbenches, one style):
the title alone in the header, the Block band, the Spaces Guide · Scope · Work · Check ·
Delivery, every View opened by a heading and one lead line, and each Space's content in
one box beside its Runs panel. Guide lives with the server: `servers/workbench-discovery/guide/`
(`guide.yaml`, `method.md` with its cards in `methods/`, `methods.excalidraw`) and `related/papers.md`
(Guide › Related Paper); `workbench/guide_families.py` loads it. This skill keeps only the run-type
contract, `ref/workbench-table.md`.

## Open

Use the existing shared host; do not start another when one is running.

```text
/_board/discovery-board?path=<Block>/board.md        one Block
/w/<block-folder>                                    the same, short
/_board/discovery-board?path=<Project>/discoveries   every Block of a Project
/_board/discovery-board                              every Discovery Block under the root
```

The host is `<plugin>/servers/_host/serve.py`; the presenter is
`<plugin>/servers/workbench-discovery/` (`discoveryboard.py` reads, `discovery_views.py`
draws). It reads the Block on every open and stores nothing. Task Pages and their Runs are
read with the Task Workbench's reader (`live.taskboard.task_snapshot`), so a Paper Run's
status is its receipt's status exactly as for a Task Run.

## Spaces and Views

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | state, spine, close condition, the Jobs and their Tasks, board.md | `board.md`; the tree |
| Scope › Questions | the Question register | `board.md` Questions |
| Scope › Resources | Related resources and the add form | `board.md` Related resources |
| Scope › RoadMap Draw | the Block's drawings, each a folding row | `studio/*.excalidraw` |
| Work › Papers | one row per Paper Run: the paper (its Result card), subject kind, reading depth, verification, status | `results/rNN_*/` card + `runtime.yaml` |
| Work › Tasks | one row per Task Page: Runs complete, papers verified, its synthesis file | Task Pages; `summary.md`, `verdict.md`, `landscape.md` |
| Work › Questions | one row per Question: Logic │ Work (Tasks and their papers) │ Report | `board.md` Questions; `reports/` |
| Check › Runs | every Run and its receipt status, blocked and failed first | `runtime.yaml` |
| Check › Citations | papers whose card says NEEDS-VERIFICATION, or whose claim is not supported | Result cards; receipts |
| Check › Reports | each report's answer status, findings and next action | report Pages |
| Delivery › Reports | answered reports, word for word | report Pages |
| Delivery › BibTeX | every one-entry `.bib` of the Block, together | `results/rNN_*/rNN_*.bib` |

Each Space has the shared Runs panel on the right (`servers/workbench/runs_panel.py`),
folded at first; its run types are the rows of `ref/workbench-table.md` for that Space,
each with its agent, skill and a prompt to copy. Nothing starts a run.

A Paper Run's Result card is `results/rNN_<paper>/rNN_<paper>.md`: its `#` title, then
`- cite:`, `- subject:`, `- venue:`, `- verification:` lines, then Question and Readout.
The receipt `runtime.yaml` gives `status`, `subject.kind`, `analysis.reading_depth` and
`analysis.claim_support`.

## Boundary

The Workbench reads; `haipipe-discovery` and its agents write the Block, its Task Pages
and Runs; `haipipe-question` the Questions; `haipipe-page` the reports. The Project view
only lists Blocks and their counts.
