---
name: draw-logic-tree
description: >-
  Draw, revise or check the logic of one Page as a tree read left to right on its RoadMap
  canvas: the claim at the left, each box splitting into the reasons it rests on, the
  Page's Bullets as leaves, each its own row in one column with room to write beside it,
  colored by their evidence. The drawing is the source of the
  logic (the person edits it on the canvas); this skill writes its first version, revises
  only what is asked, and checks an edited drawing against the rules. Use for a Section's
  argument map, Draft › RoadMap Draw, "draw the logic", "make the logic clear", logic tree,
  argument tree, claim and reasons, /draw-logic-tree.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.4.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md
---

# /draw-logic-tree · claim → reasons → Bullets, left to right

A **logic tree** shows why a Page's claim holds, so that reading the boxes alone tells
what the Page argues (JL 261003: "concise and high level, after reading the structure of
the draw, we know what it is about"; "make it deeper"; "make the logic clear"). It lives
in the Page's RoadMap drawing, `<page folder>/studio/<stem>-roadmap.excalidraw`, which
Draft › RoadMap Draw shows on an editable canvas (JL 261003: "the logic just go to the
roadmap draw").

```text
claim         reasons          parts              Bullets, each its own row    room to write
                             ┌ The firm's goal ──┬ B1 · Setting           │
            ┌ Why a rule ────┤                   └ B2 · Objective         │
            │  is needed     └ Goal unseen ─────── B3 · Measurement gap   │
One price,  ├ How messages ──────────────────────┬ B4 · Design            │
the opt-out │  are measured                      └ B5 · Method            │
settles…·B8 │                                       └ B6 · Precision      │  ← under the
            └ What decides ──────────────────────┬ B7 · Frontier          │    Bullet it
               the choice    └ Why it happens ───┼ B9 · Mechanism         │    supports
                                                 └ B10 · Cost             │
```


Rules
-----

1. **The claim is the root.** One box on top states what the Page establishes; when one
   Bullet carries it, the box names that Bullet (`· B8`).
2. **Each box splits into the reasons it rests on.** One to three children; a reason is a
   short phrase that answers "why does the box above hold?", never a heading or a section
   name.
3. **Every Bullet is a box.** A Bullet leaf shows `B<n> · <role>` and the gist of its
   sentence; a claim box may name its Bullet instead.
4. **Each Bullet is a row, in one column.** Left to right is the default (JL 261003: "where
   is the left to right? and each bullet to be a row"): the claim at the left, every first
   Bullet in one shared column at the right, read top to bottom in
   the Section's order, and a supporting Bullet below it, stepped in, so nothing sits right
   of the column and that space stays free for writing each point's content (JL 261003:
   "from left to right… this might be better", "I want to write the content in the right
   side of each point"). A Bullet's box is wide there, so its
   sentence reads in full.
   Drawn top down (`--direction tb`), the same rule turns: the Bullets share one row under
   the deepest reason, and a supporting Bullet sits one row below it.
5. **Evidence is a card on the Bullet's row.** Right of the Bullets come two columns (JL
   261003, sketched on the Abstract's canvas): **Text**, left empty for the person to write
   each point's content, then **Evidence**, one card per Evidence Item on its Bullet's row
   (`E<nn> · VALUE|CITE|DISPLAY · label`, what it needs, where it comes from). A card is
   solid green once verified, dashed orange while waiting, and so is its Bullet's outline.
   A claim that names a Bullet carries that Bullet's cards under the claim. Reasons and the
   claim are blue.
6. **Studio style.** Transparent boxes, colored strokes, every label bound inside its box,
   every connector bound at both ends, Comic Shanns (`workbench-studio/ref/draw.md`).
   Connectors run down from the parent and across just above the child's row.
7. **The drawing is the source.** After the first draw the person edits the logic on the
   canvas. Never replace an existing RoadMap without the person asking (`--force`); to
   revise, change only what was asked and keep every other box where the person put it.


Draw the first version
----------------------

Read the Page's latest Draft plan (`draft/<stem>-draft-v<G>.<S>.md`, its `## 1 Structure`
Bullets with their roles). Write the logic as an indented outline, two spaces a level:
`- <reason>` for a box, `- <reason> · B<n>` for a box that names a Bullet, `- B<n>` for a
Bullet leaf. The outline is a working note; it is not kept in the Page.

```text
- One price, the opt-out, settles which message to send · B8
  - Why a rule is needed
    - The firm's goal
      - B1
      - B2
    - The goal is unseen
      - B3
  - How the messages are measured
    - B4
    - B5
      - B6
  - What decides the choice
    - B7
    - Why it happens
      - B9
      - B10
```

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py <page.md> --logic <outline.md>
    --check         # build and print counts; write nothing
    --force         # replace an existing RoadMap: only when the person asks
```

Without `--logic` the script draws a plain tree of the plan's paragraphs and Bullets, a
starting point when the logic is not yet clear.


Refresh the evidence cards
--------------------------

The cards come from the Page's Evidence Items (`draft/<stem>-evidence-items.md`); when an
item is bound or verified, redraw only them. `--cards` replaces every element whose id
starts `ev-` and leaves the person's boxes, moves and Text column exactly as they are:

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py <page.md> --cards
```


Turn a drawing on its side
--------------------------

The person's drawing holds the logic, so a new direction is drawn from it, not from an old
outline: `--from-scene` reads the boxes and connectors of the current RoadMap (siblings in
the order the person placed them) and redraws that logic. Draw a preview beside it first;
the RoadMap itself is replaced only when the person picks the new direction.

```bash
D=Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py
.venv/bin/python $D <page.md> --from-scene --direction lr --out <page folder>/studio/<stem>-roadmap-lr-preview.excalidraw
.venv/bin/python $D <page.md> --from-scene --direction lr --force     # only when the person says so
```


Check a drawing
---------------

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py <page.md> --check-scene
```

It fails on a plan Bullet that no box names, an Evidence Item with no card, Bullets under a reason that do not share a
row (a column, when the drawing runs left to right), a Bullet that does not sit below the
Bullet it supports, a filled shape, and a
connector not bound at both ends. Run it after the person edits the canvas and before a
release that cites the logic.


Boundary
--------

This skill owns the logic tree's shape, its first draw and its check. The Page's Bullets
and their wording belong to the Draft plan (`haipipe-page-structure`, `haipipe-page-writing`);
when the tree exposes a missing or misplaced Bullet, route a Structure revise rather than
inventing a Bullet in the drawing. The canvas and its saving belong to the shared Studio
(`workbench-studio`); the View that shows the drawing to `workbench-page`.
