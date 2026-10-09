s31 · design Guide
==================

**Topic:** the design workbench's Guide tab, cut by level (JL 261007: "follow
b16_theme_paper/studio/s31-paper-guide … and Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide"), in
the style of b03's s31-guide: four Views, Description · Method · RoadMap Draw · Related Paper, each in
three folding sections Block · Job · Task, its items as cards of one shape per View. One frame per level:
the four Views opened from that level's tab, its section open and the other two folded, "on disk" under
each, then that level's open points in red.

**Source:** read at build time from the live design Guide (`servers/workbench-design/guide/guide.yaml`,
`guide/method.md`: the six steps, the 13 method cards, the five tests; `related/papers.md`: its group
column) and the design theme's Spaces on the frame, over a placeholder design ladder that the design
scaffold makes in a temp folder, by `design_guide_live.py`. Each level's file adds its proposals, marked
"?" (red), from s00 and s11 to s13. The screen and card shapes are s31's
(`../../../b03_project_workbench/studio/s31-guide/`); the builder is b16's s31, with the design Guide's words.

**Feeds:** `../../reports/` q01_design_ladder · q02_design_workbench; the proposed Guide text goes into
`guide.yaml` (a `levels:` section) and `method.md` once JL agrees.


Files
-----

```text
s31-design-guide/
├── s31-design-guide.md          this notes file
├── build_s31_design_guide.py    the builder; marks are kept on rebuild
├── design_guide_live.py         what the live design Guide says at one level, as s31 card items
├── guide_block.py               the Block level
├── guide_job.py                 the Job level
├── guide_task.py                the Task level
├── s31-design-guide.excalidraw  the drawing: one frame per level
└── s31-design-guide.png         its preview
```

Rebuild: `python build_s31_design_guide.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s31-design-guide.excalidraw s31-design-guide.png 0.4`.


Proposed (261007)
-----------------

1. Block: a step 0, Set the inputs (rules · theory · handoff as one version a Job pins); step 1 split,
   the goal list on the Block and each goal's aim and N on its Job; a step 7, Score the predictions
   (predicted against observed per method version, its verdicts sent to the methods Block). The
   Block's RoadMap Draw lists s00, s01, s11 and s02.
2. Job: the thirteen method cards; check overall (the method's part 5) on the N together; a card grows
   from three parts to the design unit's five; the Job pins a method version, method.md is not copied.
   Its papers show under each method card.
3. Task: step 4 and the five tests T0 to T4; a step for the sources (T1: every cited source is in the
   Job's inputs/manifest.yaml); a step for the numbers (tokens, time, rounds, length, a prediction that
   is a draft until a person releases the design, frozen then); draft 1 comes from the Job's Generate;
   T4 comes back as totals for an arm that names its design, never rows.
4. Across levels: the six steps' "where today" names the old board and page; the design Guide gains a
   `levels:` section in guide.yaml and a level column in method.md and papers.md, as the paper Guide has.


Open
----

See each frame's red "open at the … level" lines.

(write here, or mark the drawing in red)
