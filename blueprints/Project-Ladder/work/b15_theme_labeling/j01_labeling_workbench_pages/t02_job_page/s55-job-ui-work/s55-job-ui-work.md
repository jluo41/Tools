s55 · Job UI: Work
==================

**Tags:** `Job UI`

**Stage:** shaping

**For:** a deck, and the Work screen of a labeling Job (one dataset × one label) on the focus page (`delivery/ui/job-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** its Tasks by type, and their steps; its views, each one full screen: A Label · B Items · C Ground truth · D Meaning · E Expression · F Scanning · G Score.

**Excluded:** the other eight cells of the 3 × 3 (s51, s52, s53, s54, s56, s57, s58, s59); the engine's own Labeling workbench, where a person labels (s02); every Theme's shared frame (b10).

**Topic:** A Job's Work: its Tasks by type, and their steps; one cell of the labeling 3 × 3, a labeling Job (one dataset × one label) × Work (do), copied from the paper theme's (b16 j01; JL 261031: "please go ahead and update them"). Its drawing is haipipe-studio's five parts, drawn by `build_s55_job_ui_work.py` through j01's `labeling_ui_cells.py`; its Design is every view as the same full screen, lettered, settled one round each. Names are the public DICES-350 dataset's; no item text is drawn.

**Feeds:** `reports/` q01_labeling_ladder


Files
-----

```text
s55-job-ui-work/
├── s55-job-ui-work.md                   this face
├── build_s55_job_ui_work.py           the builder (../../labeling_ui_cells.py draws it)
├── s55-job-ui-work.excalidraw           the five parts: Idea · Now · Design · Process · Delivery
├── s55-job-ui-work.png                  its card
└── delivery/ui/                      the agreed screens, one per letter, once agreed
```


Decided
-------

(none yet: a decision is one line, s55-D01 · <what was decided> (<who> <date>))


Open
----

1. ? split t03 into building and scanning, or keep one
2. Which letter to settle first.

(write here, or mark the drawing in red)
