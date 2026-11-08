s54 · Job UI: Report
====================

**Tags:** `Job UI`

**Stage:** shaping

**For:** a deck, and the work Job's Report screen on the focus page (`delivery/ui/job-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Job's Report, as the live page draws it: A · MindMap (its topic, its Tasks, their Runs with their marks), B · Status (its Tasks, each opening to its Runs; its topics' stages), C · Findings when it has questions or takeaways (its takeaways); 🙋 Interaction each view's last section. Red, kept proposals: one table across its Tasks, the figure.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** A Job's Report: its map, its Status, its Findings; one cell of the work theme's 3 × 3, the work Job × Report (check) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s54_job_ui_report.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s54-job-ui-report/
├── s54-job-ui-report.md              this face
├── build_s54_job_ui_report.py        the builder (../../work_ui_cells.py draws it)
├── s54-job-ui-report.excalidraw      the five parts: Idea · Now · Design · Process · Delivery
├── s54-job-ui-report.png             its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s54-D01 · Redrawn 261101 the way b16 and b15 draw theirs: each view one step of the work, input → who works → output, your part, then the results (JL 261101: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI); the steps are haipipe-task's life, plan ▶ build ▶ run ▶ read ▶ close (ref/lifecycle.md). The earlier screens' rounds stay in `review/` (r01, r02).

s54-D02 · A · MindMap passed the drawing review (stage 1), mean 9.7/10 in `review/A-s1-r03.md` (rounds: `review/A-s1-r03.md`); today's page scored 8.1 and failed One job 5. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_job_report_views` (261101).

s54-D03 · B · Display passed the drawing review (stage 1), mean 9.0/10 in `review/B-s1-r03.md` (rounds: `review/B-s1-r03.md`); today's page scored 8.1 and failed One job 5. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_job_report_views` (261101).

s54-D04 · The Report's views are MindMap · Status · Findings (Findings when it has questions or takeaways), drawn as the live page draws them (redrawn 261105). A · MindMap: its topic, its Tasks, their Runs with their marks; B · Status: its Tasks, each opening to its Runs; C · Findings: its takeaways.

s54-D05 · B · Display becomes C · Findings: its delivery card leaves, since a delivery shows in the Block's Findings (asked 261104: "fold / merge the delivery to the Findings"), and What it found is the Job's takeaways. One table across the Tasks and the figure stay in red, as open proposals (261105).

s54-D06 · Every section starts closed (asked 261104: "默认的话，大家都是合着的"); 🙋 Interaction is each view's last section (decided for this round, 261105).

s54-D07 · A · MindMap draws each Task with what it finds out (its goal, a leaf) and its topics, never its Runs with their marks, which Status shows (as the live `parts_mindmap`, 261106); this changes s54-D04's "their Runs with their marks". It was decided on the lean, so `runs/r01_collect_job_report_views` Q2 asks it once.

s54-D08 · Status's Runs read ✅ done · ⏳ running · ⬜ planned; each bar carries its state word; each view's 🙋 Interaction holds its own forms (MindMap the Job's own, Status the forms below it, Findings none: the Job has no Questions); the right rail gains Skills (261106).

Open
----

Your one look: `../runs/r01_collect_job_report_views` asks whether to build the red table across the Tasks and the figure, beside today's page.

Still open after the redraw's reviews:

1. One table across the Tasks (drawn) or one table per Task (r03 asks on B).
2. The figure, each outcome's coefficient side by side, under the table (red on the drawing).

The earlier questions, my picks now drawn in, are in `../runs/r01_collect_job_report_views/passes/p01-1031/` and the round 2 screens' form in `passes/p02-1101/`; the full proposal is `result/views-proposal.md`; the 261101 screens' form is in `passes/p03-1101/`.

(write here, or mark the drawing in red)
