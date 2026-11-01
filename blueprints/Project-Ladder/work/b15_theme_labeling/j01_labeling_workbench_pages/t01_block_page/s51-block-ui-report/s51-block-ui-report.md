s51 · Block UI: Report
======================

**Tags:** `Block UI`

**Stage:** shaping

**For:** a deck, and the Report screen of the labeling Block (one dataset) on the focus page (`delivery/ui/block-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the dataset, its labels, Handoffs and scores; its views, each one full screen: A Dataset · B Labels · C Handoffs · D Scores.

**Excluded:** the other eight cells of the 3 × 3 (s52, s53, s54, s55, s56, s57, s58, s59); the engine's own Labeling workbench, where a person labels (s02); every Theme's shared frame (b10).

**Topic:** The Block's Report: the dataset, its labels, Handoffs and scores; one cell of the labeling 3 × 3, the labeling Block (one dataset) × Report (check), copied from the paper theme's (b16 j01; JL 261031: "please go ahead and update them"). Its drawing is haipipe-studio's five parts, drawn by `build_s51_block_ui_report.py` through j01's `labeling_ui_cells.py`; its Design is every view as the same full screen, lettered, settled one round each. Names are the public DICES-350 dataset's; no item text is drawn.

**Feeds:** `reports/` q01_labeling_ladder


Files
-----

```text
s51-block-ui-report/
├── s51-block-ui-report.md               this face
├── build_s51_block_ui_report.py       the builder (../../labeling_ui_cells.py draws it)
├── s51-block-ui-report.excalidraw       the five parts: Idea · Now · Design · Process · Delivery
├── s51-block-ui-report.png              its card
└── delivery/ui/                      the agreed screens, one per letter, once agreed
```


Decided
-------

(none yet: a decision is one line, s51-D01 · <what was decided> (<who> <date>))


Open
----

1. A · Dataset passed stage 1 of the design loop at round 2 (mean 8.7; review/A-s1-r01.md 7.2, review/A-s1-r02.md 8.7); waits for JL to look once before it is built.
2. ? Scores as its own view, or inside Labels
3. Which letter to settle next.

(write here, or mark the drawing in red)
