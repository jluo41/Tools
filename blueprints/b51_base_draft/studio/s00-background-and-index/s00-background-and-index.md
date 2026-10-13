s00 · Background and index
==========================

**Stage:** shaping

**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL 2026-10-12: "for every block, we also want to have the s00-background-and-index").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-background-and-index/
├── s00-background-and-index.md          this face; its yaml is the Background frame
├── s00-background-and-index.excalidraw  the drawing: Background, then Index; a person's marks are kept
└── s00-background-and-index.png         its preview
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
    - 'JL 261011: "How do we really think about haipipe-page, it is more like the haipipe-draft, which contains
      the logic, sentences, and evidence, and have a subfolder of draft to work on." What the Page skills manage
      today …'
    - The Page is the face a reader opens.
    - This Block asks whether the base layer should be named and taught as the Draft, what a draft folder holds,
      and how every theme (a paper Section, a report, a cowork email, a discovery or insight page) uses the same
      draft.
    - 'Excluded: the ladder and the shared screen (b10_project_workbench);'
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-12: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
