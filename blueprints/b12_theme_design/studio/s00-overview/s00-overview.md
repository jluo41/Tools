s00 · Background and index
==========================

**Stage:** shaping

**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL 2026-10-12: "for every block, we also want to have the s00-overview").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-overview/
├── s00-overview.md          this face; its yaml is the Background frame
├── s00-overview.excalidraw  the drawing: Background, then Index; a person's marks are kept
└── s00-overview.png         its preview
```

Rebuild: `python <haipipe-studio>/scripts/block_index.py <this Block> --draw`, haipipe-studio being
`Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/`.


Background
----------

One frame per entry, two at most, each a folder tree: a string is a leaf, `{label: [children]}` a branch; an emoji
leads each node (🧭 📖 🎯 🧱 …), and a leaf that starts with "❓" is still open and draws red. Without an `intro`, the
first frame opens with the Block's spine.

```yaml
background:
- title: 🧭 What this Block stands on
  cols: 2
  tree:
  - 🎯 Done when:
    - Each recorded question has a report Page with an answer status;
  - 📖 What it is about:
    - The design theme makes N designs for one goal by one method, checks them, and releases the ones that pass;
    - 'This Block designs that theme''s place on the ladder: The method (13 methods in 3 families, the six steps)
      is the theme''s own: plugins/haipipe-toolkit/servers/workbench-design/guide/method.md.'
    - Today's folder contract is haipipe-design/ref/method-folders.md beside it, where the method alone is the Job.
    - The trees, skills and screens are defined once with every other theme's, in ../b10_project_workbench/studio/s01-overall-tree-structure/
      (build_ladder_v4.py, level_views.py);
  - 👉 Read next:
    - 's04-design-structure, the thinking behind the design ladder: what a design method is and how it evolves (it was s00 until 2026-10-12)'
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-12: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
