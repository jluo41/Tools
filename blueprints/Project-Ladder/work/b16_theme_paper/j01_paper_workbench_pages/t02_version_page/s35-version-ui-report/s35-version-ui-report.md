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

(none yet: a decision is one line, s35-D01 · <what was decided> (<who> <date>))


Open
----

? (proposed 261101) a version's Report shows the frame's own Job views as today (focus_page.py: MindMap, the version and its Sections as a map; Status, its Tasks and where each stands; Findings, its takeaways), each regrouped as 📊 Results then ⚙️ Process (1 · 🙋 Interactions). The live regroup is focus_page.py's, the shared frame's owner (the Basic-Design-BJTR-v2 session): a hook like the Board's paper_board_report would let paper_version draw it. Recorded: t02 runs/r04_collect_version_work_decisions.

1. ? Text: the whole manuscript, or the built PDF

(write here, or mark the drawing in red)
