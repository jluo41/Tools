s51 · Board UI: Report
======================

**Tags:** `Block UI`

**Stage:** explore

**For:** a deck, and the Report screen of the insight Board (one dataset) on the focus page (`delivery/ui/block-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** each question across the Jobs, newest closed first: A Answers (questions × Jobs) · B Questions · C Jobs · D Data · E Handoff; each view its numbered sections only.

**Excluded:** the other eight cells of the 3 × 3 (s52, s53, s54, s55, s56, s57, s58, s59); the old five-Space Insight page (s02); every Theme's shared frame (b10).

**Topic:** One cell of the insight 3 × 3, the insight Board (one dataset) × Report (check), copied from the paper theme's (b16 j01) and the labeling theme's (b15 j01) (JL 261101: "Please understand the above two sessions and then work on the insights"). Its drawing is haipipe-studio's five parts, drawn by `build_s51_block_ui_report.py` through j01's `insight_ui_cells.py`; its Design is every view as the same full screen, lettered, settled one round each. Names are placeholders (`<dataset>`, `<d>`): a real Board holds one person's health data, and Tools is public.

**Feeds:** `reports/` q01_insight_ladder


Files
-----

```text
s51-block-ui-report/
├── s51-block-ui-report.md           this face
├── build_s51_block_ui_report.py           the builder (../../insight_ui_cells.py draws it)
├── s51-block-ui-report.excalidraw           the five parts: Idea · Now · Design · Process · Delivery
├── s51-block-ui-report.png                  its card
└── delivery/ui/                     the agreed screens, one per letter, once agreed
```


Decided
-------

s51-D01 · One grid per level (Board question × Job, Job question × cut, Task cut × step); Report opens on the answer; Work opens on what waits on the person; no Task asks the person (JL 261101: "go ahead", on the proposal in chat).

s51-D02 · A Report view is its numbered sections only: no ⚙️ Process and 📊 Results bands and no "Nothing waits on you"; those are Work's (JL 261101: "the Process and Results will only be availabe in the Work Section"; as b16 s32-D27). The helpers stay last.


s51-D03 · A Answers opens on the matrix: analysis plans down, data freezes across, one cell a Job, alive (its pages as a bar, its levels X D I K W as a strip, the newest marked, which clock each Job moved), an empty cell where the next Job goes (JL 261102: "more active, and vivid"); under it the newest Job's Overall Report, then what each question found (JL 261102: "we have a matrix for that", and drawn by hand on s51: p1, p2 down, v1, v2, v3 across).

s51-D04 · B Questions opens on a canvas: a card per question in DIKW bands, a line per citation in its evidence plan; hover lights what it rests on and what uses it, a click pins it, a `#q=<id>` link opens it pinned; Executive as a row on top, then a column per level, Data → Information → Knowledge → Wisdom, so the evidence builds left to right (JL 261102: "should we start from the Executive, and the Data, and then I, K, W"); the plan's lists follow, folded by DIKW level (JL 261102: "how to make the questions to be a canvas, to show their relationships?", "group them by topics ... open and close them").

s51-D05 · Every screen spells the names out: analysis plan 1 × data freeze 1, never AP1 × F1 (JL 261102: "why still AP1 x F1?").


Open
----

1. ? Open on the newest closed Job (proposed), or on the newest Job as a preview.
2. 🙋 Passed stage 1, waiting on your look: A Answers 8.3 (review/A-s1-r03.md), B Questions 8.6 (B-s1-r03.md), C Jobs 8.3 (C-s1-r03.md), D Data 8.3 (D-s1-r04.md).
3. ❗ E Handoff did not pass after round 4 (7.4; Lean, Words, Salience 6; review/E-s1-r04.md). The loop stops here: your call on its three fixes: the plan and freeze by name, the two Wisdom questions one a line with their states, 'not written' said once in the headline with an Open the Job verb.
4. ❗ Walk 261102 (the live page, every view opened and clicked; 30 views measured): A Answers is about 11,500 px and 2,300 words: the whole Overall Report sits inside it. Plan: the answers in one line each, the matrix, then the report's six figures as side tabs (one open), then what each question found folded by level. Asked: Interaction Q1.
5. ❗ The live matrix is still the plain table; the drawing's alive cell (pages bar, X D I K W strip, the clock each Job moved) is not built. Plan: build it from s51-D03.
6. ❗ C Jobs is a table of folder names and one long fold of Tasks. Plan: one row per Job with a dot row per DIKW level (as B), the clock it moved as a word. Asked: Q2.
7. ❗ D Data prints the cohort summary as raw text and full folder paths, and 'accumulates: ?'. Plan: each data freeze a card (rows, dates, messages, Jobs on it); the paths and raw summary behind one Files click; cuts as chips with their rows. Asked: Q3.
8. ⚠️ E Handoff says only 'No handoff yet'. Plan: the two Wisdom questions with their draft answers and state under it. Asked: Q4.
9. ✅ Walked and fixed today: a pinned question's share link (#q=) now follows the pin; a chip or search scrolls its card into view; question ids read as links; phone: the view buttons wrap (focus.css, every theme).

(write here, or mark the drawing in red)
