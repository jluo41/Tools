---
name: workbench-discovery
description: >-
  Open and interpret a Discovery Block on the shared workbench frame (the work shape
  every Block, Job and Task page takes). Use to see which papers a Block has read,
  which Runs are blocked, which citations still need a person, or a Block's Questions.
  The older discovery-board page (Scope, Work, Check, Delivery) is retired and described
  only for reading old links. The Block contract and the Runs belong to
  haipipe-discovery; report writing to haipipe-draft.
metadata:
  version: "0.3.2"
  last_updated: "2026-10-11"
---

# Discovery Block Workbench

One `discovery/bNN_*/board.md` declaring `board-kind: discovery-block` opens one
Workbench (`haipipe-discovery` owns the Block, its Jobs, Task Pages and Paper Runs). It opens
on the shared focus page every work-shaped theme uses (`servers/workbench/page/focus_page.py`;
`focus_base.py` `WORK_SHAPE` holds work, discovery and cowork): the views Overview · Plan + Results ·
Findings · Delivery, as `workbench-work` describes them. The theme's own page (the Spaces Guide ·
Scope · Work · Check · Delivery) is retired: its server folder is now
`servers/_old/workbench-discovery/` (presenter, `guide/`, `related/papers.md`) and nothing loads it.
This skill keeps the run-type contract, `ref/workbench-table.md`.

## Open

Use the existing shared host; do not start another when one is running.

```text
/wb <Block | Job | Task>                             the focus page (the `workbench` skill's door)
/w/<block-folder>                                    the same Block, short
```

The host is `<plugin>/servers/_host/serve.py`; the page is the shared frame in
`<plugin>/servers/workbench/page/`. It reads the Block on every open and stores nothing.
A Paper Run's status is its receipt's status exactly as for a Task Run. The older route
`/_board/discovery-board` is no longer registered (`servers/_host/host_registry.py`).

## Spaces and Views (the retired page)

This table describes the retired theme page, kept to read an old link: `frame_nav.py`
`OLD_VIEW_SPACE` maps its views to the frame (Scope to Description, Work to Work Details,
Questions, Reports and Check to Audience Report, Runs, Delivery).

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | state, spine, close condition, the Jobs and their Tasks, board.md | `board.md`; the tree |
| Scope › Questions | the Question register | `board.md` Questions |
| Scope › Resources | Related resources and the add form | `board.md` Related resources |
| Scope › RoadMap Draw | the Block's drawings, each a folding row | `studio/*.excalidraw` |
| Work › Papers | one row per Paper Run: the paper (its Result card), subject kind, reading depth, verification, status | `runs/rNN_*/result/` card + `runtime.yaml` |
| Work › Tasks | one row per Task Page: Runs complete, papers verified, its synthesis file | Task Pages; `summary.md`, `verdict.md`, `landscape.md` |
| Work › Questions | one row per Question: Logic │ Work (Tasks and their papers) │ Report | `board.md` Questions; `reports/` |
| Check › Runs | every Run and its receipt status, blocked and failed first | `runtime.yaml` |
| Check › Citations | papers whose card says NEEDS-VERIFICATION, or whose claim is not supported | Result cards; receipts |
| Check › Reports | each report's answer status, findings and next action | report Pages |
| Delivery › Reports | answered reports, word for word | report Pages |
| Delivery › BibTeX | every one-entry `.bib` of the Block, together | `runs/rNN_*/result/rNN_*.bib` |

The retired page showed the shared Runs panel beside each Space; its run types are the rows of
`ref/workbench-table.md`, each with its agent and skill. Nothing starts a run.

A Paper Run's Result card is `runs/rNN_<paper>/result/rNN_<paper>.md` (an older Task: `results/rNN_<paper>/`): its `#` title, then
`- run:`, `- address:`, `- cite:`, `- subject:`, `- venue:`, `- status:` and `- citation verification:` lines, then Question and Readout.
The receipt `runtime.yaml` gives `status`, `subject.kind`, `analysis.reading_depth` and
`analysis.claim_support`.

## Boundary

The Workbench reads; `haipipe-discovery` and its agents write the Block, its Task Pages
and Runs; `haipipe-report` the Questions; `haipipe-draft` the reports.
