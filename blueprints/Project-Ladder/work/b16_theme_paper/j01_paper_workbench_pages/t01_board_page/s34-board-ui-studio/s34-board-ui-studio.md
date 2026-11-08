s34 · Board UI: Studio
======================

**Tags:** `Block UI`

**Stage:** explore

**For:** a deck, and the paper Board's Studio screen on the focus page (`delivery/ui/board-studio`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the Board's Studio: the paper's topics, by group.

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** The Board's Studio: the paper's topics, by group; one cell of the paper's 3 × 3, the paper Board × Studio (think) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is haipipe-studio's five parts,
drawn by `build_s34_board_ui_studio.py` through j01's `paper_ui_cells.py`; its Design is the screen as proposed
(A) and what it leans on (B). Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** `reports/` q01_paper_ladder


Files
-----

```text
s34-board-ui-studio/
├── s34-board-ui-studio.md            this face
├── build_s34_board_ui_studio.py      the builder (../../paper_ui_cells.py draws it)
├── s34-board-ui-studio.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s34-board-ui-studio.png           its card
└── delivery/ui/                     the agreed screen, once agreed
```


Decided
-------

s34-D01 · The Board Studio's buttons stay the Block's own groups, its topics' Tags; they need not match the Report's views (JL 261104: "sutdio, not need that, I get confused. But if possible, we can make them consistent as well, that is flexible"; r03 Q1 B).

s34-D02 · Skills is a right-rail section on every page, between Timeline and Files (261106). Live: focus_page.render.


Open
----

(none: s34-D01 settled it, the buttons are the topics' Tags)

(write here, or mark the drawing in red)
