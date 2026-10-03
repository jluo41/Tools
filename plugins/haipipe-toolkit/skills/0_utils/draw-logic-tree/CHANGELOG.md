# Changelog

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
