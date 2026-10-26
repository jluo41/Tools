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
    - Every Job's questions have a report Page with an answer status, and every answered question names the skill,
      server or file change that settled it.
  - 📖 What it is about:
    - 'The shared foundations of plugins/haipipe-toolkit: utility and base skills, skill folders and chat.'
    - Each area is a Job inside this Block.
    - The project ladder and shared workbench have their own peer Block, b10_project_workbench.
    - Each Theme has its own peer Block under blueprints/ (261010), with its own questions, reports, studio topics
      and Runs.
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-12: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
