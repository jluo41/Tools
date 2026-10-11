s11 · Block variants
====================

**Tags:** `Structure`

**Topic:** each Block variant: its folder, what it holds, its skills, and one screen per view of the Block tab. One row per variant, top to bottom: folder → what it holds → skills (owns ·
works · shows) → screens. Each variant is its own frame. Its screens come in two rows:

- **proposed**: the Block tab, one screen per Space (teal, solid);
- **today**: the same variant in the current workbench, its Spaces, views and run buttons
  (gray, dashed), as the server code renders it (`Tools/plugins/haipipe-toolkit/servers/`),
  with how today differs in red.

**Source:** the trees, skills and screens are defined once, in
`../s01-overall-tree-structure/build_ladder_v4.py` (`BLOCK_TREES`); the screens per Space and today's
screens come from `../s01-overall-tree-structure/level_views.py`. This topic draws them on
their own canvas.

**Feeds:** `reports/` q02_bjtr_across_themes · q03_block_questions · q07_workbench_mapping.

Under the four groups, two close-up frames draw Idea Studio and Audience Report large, on the
Block, Job and Task tabs: every level has both, while Work Details may be empty (s04-D05).

Pilot of the new style (261007, JL: "update the s11 to s13 to follow the same style"): the frame
"work Block · on screen", right of everything, draws the work Block's six Spaces as full screens
(`_build/screens.py`, shared with s02-workbench-shared): under each, in teal what the work theme
changes, in gray "same as the base", then what today shows instead and the files behind it; the
Run and report pop-outs last. The older frames stay as they are until the new style is agreed and
JL has carried over the marks on them.


Files
-----

```text
s11-block-variants/
├── s11-block-variants.md          this notes file
├── s11-block-variants.excalidraw           JL's own copy: JL marks and moves it; no script writes it
├── s11-block-variants-proposed.excalidraw  the proposal, drawn by the builder
├── s11-block-variants.png · -proposed.png  previews
└── build_s11_block_variants.py            draws the proposal from the shared definitions
```

Rebuild the proposal: `python build_s11_block_variants.py` (or `../_build/make.sh`). The loop, as in
s01: JL marks their copy; the agent folds the marks into the shared definitions and redraws the
proposal beside it; JL carries over what they keep.


Decided so far
--------------

(none yet)


Open
----

(write here, or mark the drawing in red)
