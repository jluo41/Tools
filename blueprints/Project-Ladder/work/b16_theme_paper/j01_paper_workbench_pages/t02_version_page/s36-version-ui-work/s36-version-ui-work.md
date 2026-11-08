s36 · Version UI: Work
======================

**Tags:** `Job UI`

**Stage:** explore

**For:** a deck, and a version (a Job)'s Work screen on the focus page (`delivery/ui/version-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a version's Work: its Sections and their steps.

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** A version's Work: its Sections and their steps; one cell of the paper's 3 × 3, a version (a Job) × Work (do) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is haipipe-studio's five parts,
drawn by `build_s36_version_ui_work.py` through j01's `paper_ui_cells.py`; its Design is the screen as proposed
(A) and what it leans on (B). Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** `reports/` q01_paper_ladder


Files
-----

```text
s36-version-ui-work/
├── s36-version-ui-work.md            this face
├── build_s36_version_ui_work.py      the builder (../../paper_ui_cells.py draws it)
├── s36-version-ui-work.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s36-version-ui-work.png           its card
└── delivery/ui/                     the agreed screen, once agreed
```


Decided
-------

s36-D01 · A Section row shows its five step words, each opening that step (JL 261031, runs/r02_collect_version_ui_work Q1 A: "Yes, we can do this.")

s36-D02 · A version's views are Draft-Main · Draft-Appendix · Display-Main · Display-Appendix, with more to come such as Citations; making each Job's view its Studio is for later (JL 261031, runs/r02_collect_version_ui_work Q2 A: "we will choose A, and even more of them. like the citations? and for each job's view button, later we can make them to be the studio as well. But that can be later.")

s36-D03 · Each Work view is ⚙️ Process then 📊 Results, 🙋 Interaction last: Draft-Main and Draft-Appendix 🪜 Sections, each with its five step words, then 📝 Text, each Section's text in side tabs; Display, Values and Citations their Where each stands, then their items (261106). It settles the 261101 regroup proposal (recorded: t02 runs/r04_collect_version_work_decisions). Live: paper_version.version_work_views.

s36-D04 · The evidence and submission Jobs' own Work pages are drawn here under Other Jobs, G to O, one row a Job, each view ⚙️ Process then 📊 Results (261106). Live: paper_jobs.job_views.

s36-D05 · Every closed bar shows its state word on its right, read from what it holds, and a section that waits on you shows its one waiting line under the closed bar; Skills is a right-rail section on every page, between Timeline and Files (261106). Live: ui_parts._section, focus_page.render.


Open
----

1. ✓ five words a row (s36-D01)

(write here, or mark the drawing in red)
