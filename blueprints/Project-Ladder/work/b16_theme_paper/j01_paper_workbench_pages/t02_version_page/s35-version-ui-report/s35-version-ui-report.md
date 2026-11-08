s35 · Version UI: Report
========================

**Tags:** `Job UI`

**Stage:** explore

**For:** a deck, and a version (a Job)'s Report screen on the focus page (`delivery/ui/version-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a version's Report: which Section waits.

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** A version's Report: which Section waits; one cell of the paper's 3 × 3, a version (a Job) × Report (check) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is haipipe-studio's five parts,
drawn by `build_s35_version_ui_report.py` through j01's `paper_ui_cells.py`; its Design is the screen as proposed
(A) and what it leans on (B). Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** `reports/` q01_paper_ladder


Files
-----

```text
s35-version-ui-report/
├── s35-version-ui-report.md            this face
├── build_s35_version_ui_report.py      the builder (../../paper_ui_cells.py draws it)
├── s35-version-ui-report.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s35-version-ui-report.png           its card
└── delivery/ui/                     the agreed screen, once agreed
```


Decided
-------

s35-D01 · A version's Report is MindMap, then the same six views as its Work, results only: Draft-Main · Draft-Appendix · Display-Main · Display-Appendix · Values · Citations, lettered A to G; a Draft view's Results are each Section's text, one side tab per Section (261106). It replaces the frame's MindMap · Status · Findings and settles the 261101 proposal to regroup them (recorded: t02 runs/r04_collect_version_work_decisions). Live: paper_version.version_report_views.

s35-D02 · A Job's MindMap shows each Task with its goal leaf, finds out and what it must find out, never the Run tree (261106). Live: focus_page.parts_mindmap.

s35-D03 · The evidence and submission Jobs' own Reports are drawn here under Other Jobs, H to T, one row a Job: display (MindMap · Plan · Displays · Examples), value (MindMap · Values · Check), citation (MindMap · Citations · Check), submission (MindMap · Cover letter · Portal), each view its Results alone, drawn from the Board's own pieces (261106). Live: paper_jobs.job_views.

s35-D04 · Every closed bar shows its state word on its right, read from what it holds, and a section that waits on you shows its one waiting line under the closed bar; Skills is a right-rail section on every page, between Timeline and Files (261106). Live: ui_parts._section, focus_page.render.


Open
----

1. ? Text: the whole manuscript, or the built PDF

(write here, or mark the drawing in red)
