s51 · Block UI: Report
======================

**Tags:** `Block UI`

**Stage:** shaping

**For:** a deck, and the work Block's Report screen on the focus page (`delivery/ui/block-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the Block's Report, as the live page draws it: A · MindMap (its Questions with their answer pills, its topic groups, its Jobs under their bands; every node closed), B · Status (a closed numbered section per band, its state word and bar; a row per Job, opening to its Tasks and Runs), C · Findings (closed numbered sections with side tabs: 🔢 Values, the Questions by `group:`, 🌐 Service with a live page, 🧠 Maps, 📦 Delivery with tabs Models · Data · Website); 🙋 Interaction each view's last section.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** The Block's Report: its map, its Status, its Findings; one cell of the work theme's 3 × 3, the work Block × Report (check) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s51_block_ui_report.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

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

s51-D11 · The Report's views are MindMap · Status · Findings, drawn as the live page draws them (asked 261104: "the quick overview of the results we get from that block"; redrawn 261105). A · MindMap follows the live map: the Questions with their answer pills, the topic groups, the Jobs under their bands, every node closed.

s51-D12 · B · Data and C · Display fold into Findings' 📦 Delivery, tabs Models · Data · Website (asked 261104: "fold / merge the delivery to the Findings"; 261105). This settles the still-open line "Data and Display show what the right-rail Delivery also lists": the Report shows a delivery once, in Findings, and the rail keeps its Delivery.

s51-D13 · C · Findings is closed numbered sections, each with side tabs, the list on the left and the open one on the right: 🔢 Values, the Questions by `group:`, 🌐 Service (only with a live page, each tab a website), 🧠 Maps, 📦 Delivery (asked 261104: "left tab panel right content"; a new section named Service; 261105). It changes s51-D04 in part: no Questions view (asked 261104: "we don't need the questions"), and the Questions return inside Findings as the frame for what was found.

s51-D14 · Every section starts closed (asked 261104: "默认的话，大家都是合着的"); 🙋 Interaction is each view's last section, numbered after its sections, never a Process step (decided for this round, 261105).

s51-D15 · Redrawn to the live page of 261106: every closed bar carries its state word on its right, and a bar that waits on the person shows its waiting line under it (C · Findings' Outcomes reads "waits for you", the question under the bar); each view's 🙋 Interaction holds its own forms (`focus_page.view_items`: MindMap the Block's own, Status the forms below it, Findings the forms at its Questions' work); the right rail gains Skills between Timeline and Files (261106).

Open
----

Your one look: `../runs/r02_collect_block_report_views` asks one thing now: agree A to C as drawn (they follow the live page).

Nothing else is open after the 261105 redraw: the line on Data and Display repeating the rail's Delivery is settled (s51-D12).

The earlier questions, my picks now drawn in, are in `../runs/r02_collect_block_report_views/passes/p01-1031/`; the full proposal is `result/views-proposal.md`; the 261101 screens' form is in `passes/p02-1101/`.

(write here, or mark the drawing in red)
