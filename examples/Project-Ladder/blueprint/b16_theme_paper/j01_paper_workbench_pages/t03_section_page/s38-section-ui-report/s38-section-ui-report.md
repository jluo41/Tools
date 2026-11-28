s38 · Section UI: Report
========================

**Tags:** `Task UI`

**Stage:** explore

**For:** a deck, and a Section (a draft Task)'s Report screen on the focus page (`delivery/ui/section-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Section page's Report, its only section now: Draft, Plan, Evidence, Display (Draft itself is s39).

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** A Section's Report, the Section page's only section since Work was retired (261113); one cell of the paper's 3 × 3, a Section (a draft Task) × Report (check) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is hai-studio's five parts,
drawn by `build_s38_section_ui_report.py` through j01's `paper_ui_cells.py`; its Design is the screen as proposed
(A) and what it leans on (B). Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** Q01


Files
-----

```text
s38-section-ui-report/
├── s38-section-ui-report.md            this face
├── build_s38_section_ui_report.py      the builder (../../paper_ui_cells.py draws it)
├── s38-section-ui-report.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s38-section-ui-report.png           its card
└── delivery/ui/                     the agreed screen, once agreed
```


Decided
-------

s38-D01 · Superseded 261113: no bar carries a state word now, and Text, MindMap and Status are gone from the Section page (s38-D02).
The 261101 proposal to regroup MindMap, Text and Status (Results, then Process) · Superseded 261113: those views are retired.
s38-D02 · A Section page has Report only (Work is retired); its views are 1 · Draft (opens first), 2 · Plan, 3 · Evidence, 4 · Display, and Display shows only when the Section has one (261113). Live: focus_draft_steps.work_views.
s38-D03 · Draft is drawn in s39; edits are accepted in place there, on the Draft Lab's cards (261113). Live: draft_step_revise._text_and_cards.


Open
----

1. ? the drawing still shows MindMap · Text · Status: redraw it as Plan, Evidence and Display (Draft stays in s39)

(write here, or mark the drawing in red)
