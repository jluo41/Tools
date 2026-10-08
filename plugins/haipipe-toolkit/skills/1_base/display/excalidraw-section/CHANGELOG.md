# Changelog

## 0.1.0 · 2026-10-03 · Paper and Section maps (JL 261003)

- New skill (JL 261003: "for drawing the sections only, I mean the paper and paragraph",
  "in the right part add the evidence card as well", "Maybe call it as this": excalidraw-section).
- `ref/excalidraw_section.py`: a Section map (Section → paragraphs → Bullets, each a row,
  then a Text column and an Evidence column of cards) and a paper map (paper → Main ·
  Appendix · Round → Sections in board order → paragraphs, deeper with `--depth`). Left to
  right, labels wrapped to their box; generated (`source` names the script), never replaced
  after a canvas edit without `--force`. Cards come from `draw-logic-tree`.
- First maps: S-ManSci-Main-Abstract (12 boxes, 9 cards) and Paper-MessageTradeOffEgm (19
  Sections in three groups; only the Abstract has a plan yet).
