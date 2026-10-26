s00 · Background and index
==========================

**Stage:** shaping

**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL 2026-10-16: "for every block, we also want to have the s00-overview").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-overview/
├── s00-overview.md          this face; its yaml is the Background frame
├── s00-overview.excalidraw  the drawing: Background, then Index; a person's marks are kept
├── build_s00_overview.py  rebuild using the current shared Tools generator
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
    - haipipe-display makes, checks and places one real display (the b21 Overview Figure) and one table from a work
      Run through display/;
  - 📖 What it is about:
    - 'JL 261016: "and also the display?'
    - could you call another session for the b34_display?
    - Do you know what the display want to have?
    - Please think about it".
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-16: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
