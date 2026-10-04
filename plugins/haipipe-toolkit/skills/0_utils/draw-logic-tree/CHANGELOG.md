# Changelog

## 0.4.0 · 2026-10-03 · Text and Evidence columns

- Right of the Bullets, a Text column left empty for the person and an Evidence column
  (JL 261003: "in the right part add the evidence card as well", sketched as "text" and
  "evidence" on the Abstract's canvas): one card per Evidence Item on its Bullet's row
  (id · type · label, what it needs, where it comes from), green verified, dashed orange
  waiting; a Bullet's row grows to hold its stack; a claim's own cards sit under the claim.
- `--cards` redraws only the Evidence column (`ev-*` elements) of an edited drawing;
  `outline_from_scene` ignores cards; `--check-scene` fails an Evidence Item with no card.
- S-ManSci-Main-Abstract: 9 cards on 7 Bullets plus the claim (E04 under B8), check PASS.

## 0.3.0 · 2026-10-03 · Left to right is the default

- `--direction lr` is now the default (JL 261003: "where is the left to right? and each
  bullet to be a row", then "go ahead and update them"); `--direction tb` keeps the
  top-down tree. The skill, its agent prompt, the Page workbench's RoadMap Draw text, the
  "By logic tree" card, the Page method's step and the "Draw the logic" run card now
  describe the logic read left to right, each Bullet a row.
- S-ManSci-Main-Abstract's RoadMap is drawn left to right again, from JL's top-down canvas
  (`--from-scene`), after a rollback restored that canvas when an editable methods canvas
  in Guide had saved its own drawing into the RoadMap file.

## 0.2.0 · 2026-10-03 · Left to right (JL 261003)

- `--direction lr`: the same logic tree on its side (JL 261003: "how do you think we can
  make it from left to right?", then "this might be better, could you try"): the claim at
  the left, reasons in the middle columns, every first Bullet in one shared column at the
  right (300px wide, so a sentence reads in two lines, not cut), a supporting Bullet one
  column further right; each parent level with the middle of what it rests on, a gap
  between the claim's reasons, right-then-up-or-down connectors bound at both ends.
- `--from-scene`: the logic read back from the current drawing (`outline_from_scene`: its
  boxes, its bound connectors, siblings in the drawing's own reading order), so a person's
  edits carry over to the new direction. `--out` writes a preview instead of the RoadMap.
- A supporting Bullet sits below the Bullet it supports, stepped in 40px, its right edge on
  the column's (JL 261003: "I want to write the content in the right side of each point";
  JL had moved B6 under B5 on the canvas to show it), joined by a down-then-right connector;
  nothing is drawn right of the Bullet column. `outline_from_scene` reads the direction from
  the first Bullets only, so a moved sub-Bullet does not change the sibling order.
- `--check-scene` knows both directions: one row of Bullets top down, one column left to
  right. First preview: S-ManSci-Main-Abstract, from JL's arranged canvas, 48 elements,
  check PASS; the canvas itself is unchanged.

## 0.1.0 · 2026-10-03 · The logic tree of a Page (JL 261003)

- A Page's logic drawn as a top-down tree in its RoadMap (`studio/<stem>-roadmap.excalidraw`,
  Draft › RoadMap Draw): claim on top, reasons below, Bullets as leaves on one shared row,
  a Bullet under a Bullet one row below, evidence as the outline (green verified, dashed
  orange waiting). JL 261003: "could you make it like a tree plot? up to bottom", "make it
  deeper", "make the logic clear", "the logic just go to the roadmap draw", "make the
  Bullet point to be in the same start in the same level", "could you make a skill for it?".
- `ref/draw_logic_tree.py` (moved from `haipipe-page/cli/page_roadmap.py`): `--logic` draws
  an indented outline; `--force` is required to replace an existing drawing; `--check-scene`
  checks an edited drawing (every Bullet named, one Bullet row, sub-Bullets below, no fills,
  bound connectors). Checked: PASS on S-ManSci-Main-Abstract as JL arranged it; a copy with
  B2 removed and B4 lifted fails on both.
- Lives in `0_utils` beside `table-workbench` and `table-papers`, not in `display/`: a
  RoadMap is a working drawing on a Page's canvas, not a manuscript display unit.
