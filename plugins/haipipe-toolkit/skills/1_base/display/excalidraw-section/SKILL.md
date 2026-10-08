---
name: excalidraw-section
description: >-
  Draw a paper's Sections, or one Section, as an Excalidraw map read left to right: the
  paper, its groups (Main, Appendix, Round), its Sections in board order, each Section's
  paragraphs by their one-line job, each Bullet a row, then a Text column left empty for
  writing and an Evidence column with one card per Evidence Item on its Bullet's row. It
  shows where each part sits; it is generated from the Draft plans and Evidence Items,
  never edited by hand. Use for a paper map, a Section map, "draw the sections", "draw the
  paper and paragraphs", section structure drawing, evidence cards per Bullet,
  /excalidraw-section.
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md
---

# /excalidraw-section · paper → Sections → paragraphs → Bullets → evidence

A **Section map** shows what a paper is made of and in what order, so a reader sees where
each part sits and what evidence each point still waits for (JL 261003: "for drawing the
sections only, I mean the paper and paragraph"; "in the right part add the evidence card as
well"). It is the companion of `draw-logic-tree`: the logic tree shows why a Section's
claim holds and is the person's to edit; the Section map shows where each part sits and is
redrawn from the files.

```text
paper ─┬ Main ─────┬ Abstract ─── P1 · the whole claim ─┬ B1 · Setting   │ Text │ (none)
       │           │                                    ├ B4 · Design    │      │ E09 · VALUE · valuePop
       │           │                                    ├ B5 · Method    │      │ E08 · CITE · citeHuch
       │           ├ 1 · Introduction  (no plan yet)    …
       ├ Appendix ─┼ …
       └ Round
```


Rules
-----

1. **Left to right, one column a level.** Paper, group, Section, part (only when a Section
   has more than one), paragraph, Bullet; each Bullet its own row; a parent sits level with
   the middle of what it holds.
2. **Order is the paper's.** Sections in the order of the board's `## Pages`, groups as the
   board lists them, the Story group left out; paragraphs and Bullets in plan order.
3. **Right of the Bullets: Text, then Evidence.** The Text column is empty, for writing each
   point's content; the Evidence column holds one card per Evidence Item on its Bullet's
   row (`E<nn> · VALUE|CITE|DISPLAY · label`, what it needs, where it comes from). The
   cards are drawn by `draw-logic-tree`'s card code, so both drawings show evidence alike.
4. **Colors say the state.** A Bullet and its cards are solid green once every item is
   verified, dashed orange while one waits; a Section with no Draft plan yet is a dashed
   grey box, "no plan yet"; structure boxes are blue.
5. **Generated, never edited.** The map comes from each Section's latest Draft plan
   (`draft/<stem>-draft-v<G>.<S>.md`, `## 1 Structure`) and its Evidence Items
   (`draft/<stem>-evidence-items.md`). Change those and redraw. Its `source` names the
   script; a map someone edited on the canvas is replaced only with `--force`.


Draw
----

```bash
X=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-section/ref/excalidraw_section.py
.venv/bin/python $X <page.md>                   # one Section → <page>/studio/<stem>-sections.excalidraw
.venv/bin/python $X --paper <paper folder>      # the paper → <paper>/studio/paper-sections.excalidraw
    --depth section|paragraph|bullet|evidence   # paper default: paragraph; a Section: evidence
    --check                                     # build and print counts; write nothing
```

The paper map stops at paragraphs by default, so a paper of twenty Sections stays
readable; `--depth evidence` draws every Bullet and card. Story › RoadMap Draw lists every
drawing in the paper's `studio/`, so the paper map shows there.


Boundary
--------

This skill draws the structure; it writes nothing else. The plan and its Bullets belong to
`haipipe-page-structure`; the Evidence Items to `haipipe-page-evidence`; the Section order
to the paper board (`haipipe-paper`). Why a Section's claim holds is `draw-logic-tree`. A
manuscript figure is a display unit (`haipipe-display`); this map is a working drawing.
