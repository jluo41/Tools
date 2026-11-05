s51 · Block UI: Report
======================

**Tags:** `Block UI`

**Stage:** shaping

**For:** a deck, and the work Block's Report screen on the focus page (`delivery/ui/block-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the Block's Report: A · MindMap (1 The map: each Job, what it makes, its Tasks; no state words), then one view per delivery type, B · Data and C · Display in the example (1 Deliveries as side tabs: each tab its name, version word and Job; the open one's thing to read, its For line, its tags); 🙋 Interactions at the bottom.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** The Block's Report: the map and its deliveries by type; one cell of the work theme's 3 × 3, the work Block × Report (check) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s51_block_ui_report.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s51-block-ui-report/
├── s51-block-ui-report.md            this face
├── build_s51_block_ui_report.py      the builder (../../work_ui_cells.py draws it)
├── s51-block-ui-report.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s51-block-ui-report.png           its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s51-D01 · The Report's views are the MindMap, then one per delivery type (Skill · UI), never one per delivery's name (JL 261031, r01_collect_report_and_delivery Q2: C, changed from my pick A: "we groups things by the types, not the full name").

s51-D02 · A delivery opens from the tags below its sNN (Slide · Draw · Mind map · Work · Delivery); it needs no view of its own (JL 261031, r01_collect_report_and_delivery Q3, own decision: "we just need to click the tags below the sNN, then we are good").

s51-D03 · A delivery not made yet shows its planned look, marked planned (JL 261031, r01_collect_report_and_delivery Q4: A).

s51-D04 · No Questions: Findings, Answers and Questions go, and a work Block keeps no Questions (JL 261031, r01_collect_report_and_delivery Q5: A, with its note "we will not have the questions").

s51-D05 · Each delivery carries one word, its current version (JL 261031, r01_collect_report_and_delivery Q6: A, with its note "we just need the current version").

s51-D06 · This cell designs the work theme's Report, not the paper's (JL 261031, r01_collect_report_and_delivery Q1, own decision: "Ignore this question, you don't need to think about how does the paper do, you will focus on the work_theme").

s51-D07 · A · MindMap passed the drawing review (haipipe-ui Design loop, stage 1) in round 2, mean 8.9/10: `review/A-s1-r02.md` (round 1: `review/A-s1-r01.md`); today's page scored 6.5 and did not pass (`review/today-261101.md`). Proposed by the agent; it waits for JL's one look in `runs/r02_collect_block_report_views` (261101).

s51-D08 · B · Data passed the drawing review (haipipe-ui Design loop, stage 1) in round 2, mean 9.3/10: `review/B-s1-r02.md` (round 1: `review/B-s1-r01.md`); today's page scored 6.5 and did not pass (`review/today-261101.md`). Proposed by the agent; it waits for JL's one look in `runs/r02_collect_block_report_views` (261101).

s51-D09 · C · Display passed the drawing review (haipipe-ui Design loop, stage 1) in round 2, mean 9.1/10: `review/C-s1-r02.md` (round 1: `review/C-s1-r01.md`); today's page scored 6.5 and did not pass (`review/today-261101.md`). Proposed by the agent; it waits for JL's one look in `runs/r02_collect_block_report_views` (261101).

s51-D10 · A Block's Status: numbered sections per band, closed; one row per Job, opening to its Tasks and Runs; no next-step sentences (JL 261104, on b01_clm_foundation_model: "这个做得很好", "just delete them"). Built in `focus_page.py` `band_board`; the rule is in haipipe-ui.


Open
----

Your one look: `../runs/r02_collect_block_report_views` shows each screen beside today's page: build it as drawn, or keep today's.

Still open after the review (its reviewers' asks):

1. Data and Display show what the right-rail Delivery also lists (rubric 5, r02 asks): Delivery could keep only what was sent.

The earlier questions, my picks now drawn in, are in `../runs/r02_collect_block_report_views/passes/p01-1031/`; the full proposal is `result/views-proposal.md`.

(write here, or mark the drawing in red)
