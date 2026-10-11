s11 · Block level
=================

**Topic:** the paper Board's tab on the shared frame (Guide · Block · Job · Task): its six Spaces as full
screens, "on disk" under each, two pop-outs, then Guide › Method opened from the Block tab (JL
261007: "add the s11 s12 s13 like b11"). It draws Q01's proposal for the Board (`../s05-board-job-task-boundary/`).

**Source:** the screens are drawn by `../_build/paper_ui.py`, shared by s11 · s12 · s13; the Guide's
steps and method cards are read from `servers/workbench-paper/guide/method.md` and its `methods/`
(and the Page Task's `guide.yaml` at Task level) at build time. Placeholders only.

**Feeds:** `../../reports/` q01_paper_ladder (and the open marks of q02, q03).


Files
-----

```text
s11-paper-block/
├── s11-paper-block.md         this notes file
├── build_s11_paper_block.py   the builder; marks are kept on rebuild
├── s11-paper-block.excalidraw the drawing: today → proposed, one frame per Space, Guide › Method, open notes
└── s11-paper-block.png        its preview
```

Rebuild: `python build_s11_paper_block.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s11-paper-block.excalidraw s11-paper-block.png 0.4`.


Proposed (261007)
-----------------

1. Description has four groups: Scope (the face, which Story it tells, the target now) · Venue
   (`venues/<venue>/`) · Resources · Related (`related/related.md`).
2. Idea Studio: one drawing after another; the RoadMap Draw is its first topic.
3. Audience Report: Ideation · Spine · High-level logic + Low-level work, read from the Story Pages and `reports/`.
4. Work Details: the Jobs (story · versions · grants · slides), each version open to its Sections.
5. Runs: the Board's own soft Runs; Delivery: each version's build, from below (Q02 open).
6. Guide › Method from this tab: the Block section open (frame the question, write the Story, fix
   the evidence), Job and Task folded.


Open
----

See the drawing's red notes (open ?).

(write here, or mark the drawing in red)
