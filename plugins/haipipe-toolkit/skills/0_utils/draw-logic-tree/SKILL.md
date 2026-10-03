---
name: draw-logic-tree
description: >-
  Draw, revise or check the logic of one Page as a top-down tree on its RoadMap canvas:
  the claim on top, each box splitting into the reasons it rests on, the Page's Bullets as
  leaves on one shared row, colored by their evidence. The drawing is the source of the
  logic (the person edits it on the canvas); this skill writes its first version, revises
  only what is asked, and checks an edited drawing against the rules. Use for a Section's
  argument map, Draft › RoadMap Draw, "draw the logic", "make the logic clear", logic tree,
  argument tree, claim and reasons, /draw-logic-tree.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md
---

# /draw-logic-tree · claim → reasons → Bullets, top to bottom

A **logic tree** shows why a Page's claim holds, so that reading the boxes alone tells
what the Page argues (JL 261003: "concise and high level, after reading the structure of
the draw, we know what it is about"; "make it deeper"; "make the logic clear"). It lives
in the Page's RoadMap drawing, `<page folder>/studio/<stem>-roadmap.excalidraw`, which
Draft › RoadMap Draw shows on an editable canvas (JL 261003: "the logic just go to the
roadmap draw").

```text
              One price, the opt-out, settles which message to send · B8      ← the claim
        ┌──────────────────────┼─────────────────────────┐
  Why a rule is needed   How messages are measured   What decides the choice  ← reasons
     ┌─────┴─────┐                 │                      │
 The firm's goal  Goal unseen      │                 Why it happens          ← parts
   ┌──┴──┐          │          ┌───┴───┐        │      ┌──┴──┐
  B1    B2         B3         B4      B5       B7     B9    B10              ← Bullets, one row
                                       │
                                      B6                                     ← a Bullet under a Bullet
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
4. **Bullets start on one row.** The Bullets that hang from a reason share one row, just
   under the deepest reason; a Bullet that supports another Bullet sits one row below it
   (JL 261003: "make the Bullet point to be in the same start in the same level").
5. **Evidence is the outline, not more boxes.** A Bullet whose Evidence Items are all
   verified, or that needs none, is solid green; one still waiting is dashed orange; the
   items stay in the Evidence Space. Reasons and the claim are blue.
6. **Studio style.** Transparent boxes, colored strokes, every label bound inside its box,
   every connector bound at both ends, Comic Shanns (`haipipe-workbench-studio/ref/draw.md`).
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


Check a drawing
---------------

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py <page.md> --check-scene
```

It fails on a plan Bullet that no box names, Bullets under a reason that do not share a
row, a Bullet that does not sit below the Bullet it supports, a filled shape, and a
connector not bound at both ends. Run it after the person edits the canvas and before a
release that cites the logic.


Boundary
--------

This skill owns the logic tree's shape, its first draw and its check. The Page's Bullets
and their wording belong to the Draft plan (`haipipe-page-structure`, `haipipe-page-writing`);
when the tree exposes a missing or misplaced Bullet, route a Structure revise rather than
inventing a Bullet in the drawing. The canvas and its saving belong to the shared Studio
(`haipipe-workbench-studio`); the View that shows the drawing to `haipipe-workbench-page`.
