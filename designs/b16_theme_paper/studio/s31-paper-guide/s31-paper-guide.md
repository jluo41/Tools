s31 · paper Guide
=================

**Topic:** the paper workbench's Guide tab, cut by level, in the style of b03's s31-guide (four
Views, Description · Method · RoadMap Draw · Related Paper, each in three folding sections Block ·
Job · Task, its items as cards of one shape per View). One frame per level: the four Views opened
from that level's tab, its section open and the other two folded, "on disk" under each, then that
level's open points in red (JL 261007: one session per level).

**Source:** read at build time from the live paper Guide (`servers/workbench-paper/guide/guide.yaml`,
`guide/method.md`, `related/papers.md`) and the paper theme's Spaces on the frame (over a placeholder
Board in a temp folder), by `paper_guide_live.py`; each level's file adds its proposals, marked "?"
(red). The screen and card shapes are s31's (`../../../b03_project_workbench/studio/s31-guide/`).

**Feeds:** `../../reports/` q01_paper_ladder; the proposed Guide text goes into `guide.yaml` and
`method.md` once JL agrees.


Files
-----

```text
s31-paper-guide/
├── s31-paper-guide.md          this notes file
├── build_s31_paper_guide.py    the shared builder (Block session); marks are kept on rebuild
├── paper_guide_live.py         what the live Guide says at one level, as s31 card items
├── guide_block.py              the Block level (design_b16_theme_paper-block)
├── guide_job.py                the Job level (design_b16_theme_paper-job)
├── guide_task.py               the Task level (design_b16_theme_paper-task)
├── s31-paper-guide.excalidraw  the drawing: one frame per level
└── s31-paper-guide.png         its preview
```

Rebuild: `python build_s31_paper_guide.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s31-paper-guide.excalidraw s31-paper-guide.png 0.4`.


Proposed at the Block level (261007)
------------------------------------

1. A step 0, Set up the paper: its scope, the venues it writes for, the related work it sits beside
   (Description › Scope · Venue · Related; runs Add a venue · Add a related item · Read a paper),
   signed by naming the target venue. Today the Board has the Spaces and the run types but no step.
2. Skills by level: the Block section names the Board's own skills (haipipe-paper owns;
   haipipe-paper-story, -ideation, -venue and haipipe-question work; workbench-paper shows).
3. Two pairs of words kept apart: Description › Related (what one paper sits beside) and Guide ›
   Related Paper (the papers behind the method); the Guide's RoadMap Draw (the theme's drawings) and a
   paper's own RoadMap drawing (its Idea Studio).
4. After the Q01 migration, the Audience Report reads j00_story/, not A1-Story/.

The Job session proposes steps 4 to 7 (Open the send · Write the Sections · Deliver · Close on the
decision); with step 0 the Block keeps 0 to 3.


Open
----

See each frame's red "open at the … level" lines.

(write here, or mark the drawing in red)
