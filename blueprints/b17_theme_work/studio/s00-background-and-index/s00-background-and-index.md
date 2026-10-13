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
    - Each recorded question has a report Page with an answer status, and every answered question names the skill,
      workbench or builder change that settled it.
  - 📖 What it is about:
    - 'The work Theme runs bounded execution work: a Task plans, builds, executes and reports, and each Run is one
      hard ticket (rNN_<noun>_<qualifier>.sh) with its Result and receipt.'
    - Its Block is a task Block (tasks/bNN_<topic>/), a Job groups Tasks by series (j0N, j1N, j5N), and a Block's
      Questions are answered by report Pages that read the Tasks' Runs.
    - 'Today the Task workbench shows it at Block level in four Spaces (Scope · Task · Check · Delivery): the Question
      groups are Views of Task.'
    - Its server is moving to servers/workbench-work and its skills to 2_theme/work/ (in progress, 261007).
  - '❓ Seeded from the Block''s face: rewrite it as the tree a newcomer needs'
```


Open
----

1. The background was seeded from the Block's face on 2026-10-12: a person rewrites it as the tree a newcomer needs.

(write here, or mark the drawing in red)
