s54 · Job UI: Report
====================

**Tags:** `Job UI`

**Stage:** shaping

**For:** a deck, and the Report screen of a labeling Job (one dataset × one label) on the focus page (`delivery/ui/job-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the label, then each Task type's result; its views, each one full screen: A Label · B Items · C Ground truth · D Meaning · E Expression · F Scanning · G Score.

**Excluded:** the other eight cells of the 3 × 3 (s51, s52, s53, s55, s56, s57, s58, s59); the engine's own Labeling workbench, where a person labels (s02); every Theme's shared frame (b10).

**Topic:** A Job's Report: the label, then each Task type's result; one cell of the labeling 3 × 3, a labeling Job (one dataset × one label) × Report (check), copied from the paper theme's (b16 j01; JL 261031: "please go ahead and update them"). Its drawing is haipipe-studio's five parts, drawn by `build_s54_job_ui_report.py` through j01's `labeling_ui_cells.py`; its Design is every view as the same full screen, lettered, settled one round each. Names are the public DICES-350 dataset's; no item text is drawn.

**Feeds:** `reports/` q01_labeling_ladder


Files
-----

```text
s54-job-ui-report/
├── s54-job-ui-report.md                 this face
├── build_s54_job_ui_report.py         the builder (../../labeling_ui_cells.py draws it)
├── s54-job-ui-report.excalidraw         the five parts: Idea · Now · Design · Process · Delivery
├── s54-job-ui-report.earlier-job-centered-v1.excalidraw   the earlier sketch (was s04, 261031): Job-centred content
├── s54-job-ui-report.png                its card
└── delivery/ui/                      the agreed screens, one per letter, once agreed
```


Decided
-------

s54-D01 · s04 (job-centered content v1) folds into this topic as its earlier sketch, kept beside the drawing (JL 261031).


Open
----

1. ? Label first, or Building first
2. Which letter to settle first.

(write here, or mark the drawing in red)
