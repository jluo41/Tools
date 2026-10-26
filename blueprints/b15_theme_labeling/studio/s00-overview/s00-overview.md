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
    - Each recorded question has a report Page with an answer status, and every answered question names the skill,
      workbench or builder change that settled it.
  - 📖 What it is about:
    - 'The labeling Theme teaches and freezes what one identified person means by a vague label (Building: contract,
      definition, calibration rounds, guideline, the signed Label Handoff), then qualifies executors on a sealed
      …'
    - Its Block holds one Job per dataset × label (jNN_<dataset>_<label>/, its schema.yaml);
    - Today the Labeling workbench shows a job at page level in four Spaces (Data · Labeling · Quality · Delivery),
      and a board level lists the jobs.
    - The skills came from the subjective-label plugin (b04 q03).
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-12: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
