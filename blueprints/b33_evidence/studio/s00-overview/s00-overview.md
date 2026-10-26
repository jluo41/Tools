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
    - haipipe-evidence reads, checks and proposes for one real Section (b21 C2) and one other kind of page;
  - 📖 What it is about:
    - 'JL 261016: "I think we need to put them out, like we also have the haipipe-draft and haipipe-display, so
      it will be natural to have the haipipe-evidence, like we can find the evidence we need, in many other scenarios";'
    - The skill was born inside b32_draft (s41, s21) and on b21's C2 Section canvas (WellDoc-SPACE, Project-SHIFT-Study,
      b21 s05);
    - 'What is settled so far (261016): two kinds of card by where the evidence comes from, CITE (a discovery Task
      or Job: papers, and any value or figure a paper reports;'
    - 'The skill: plugins/haipipe-toolkit/skills/1_base/evidence/haipipe-evidence/.'
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-16: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
