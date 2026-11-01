s57 · Task UI: Report
=====================

**Tags:** `Task UI`

**Stage:** shaping

**For:** a deck, and the work Task's Report screen on the focus page (`delivery/ui/task-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Task's Report: A · MindMap (its topic, its Runs by what they do), then each step's results, read only: B · Plan (done when, large; what it makes, who makes it; where it lands), C · Build (the code review, large; how it was built; the review), D · Read (the headline, the Table Card, the coefficient plot); Run and Close stay in Work.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** A Task's Report: its plan, its code and what it found, read only; one cell of the work theme's 3 × 3, the work Task × Report (check) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s57_task_ui_report.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s57-task-ui-report/
├── s57-task-ui-report.md             this face
├── build_s57_task_ui_report.py       the builder (../../work_ui_cells.py draws it)
├── s57-task-ui-report.excalidraw     the five parts: Idea · Now · Design · Process · Delivery
├── s57-task-ui-report.png            its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s57-D01 · Redrawn 261101 the way b16 and b15 draw theirs: each view one step of the work, input → who works → output, your part, then the results (JL 261101: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI); the steps are haipipe-task's life, plan ▶ build ▶ run ▶ read ▶ close (ref/lifecycle.md). The earlier screens' rounds stay in `review/` (r01, r02).

s57-D02 · A · MindMap passed the drawing review (stage 1), mean 9.4/10 in `review/A-s1-r03.md` (rounds: `review/A-s1-r03.md`); today's page scored 7.8 and failed One job 5 and Salience 6. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_task_report_views` (261101).

s57-D03 · B · Plan passed the drawing review (stage 1), mean 9.1/10 in `review/B-s1-r05.md` (rounds: `review/B-s1-r03.md`, `review/B-s1-r04.md`, `review/B-s1-r05.md`); today's page scored 7.8 and failed One job 5 and Salience 6. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_task_report_views` (261101).

s57-D04 · C · Build passed the drawing review (stage 1), mean 8.9/10 in `review/C-s1-r06.md` (rounds: `review/C-s1-r03.md`, `review/C-s1-r04.md`, `review/C-s1-r05.md`, `review/C-s1-r06.md`); today's page scored 7.8 and failed One job 5 and Salience 6. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_task_report_views` (261101).

s57-D05 · D · Read passed the drawing review (stage 1), mean 9.1/10 in `review/D-s1-r03.md` (rounds: `review/D-s1-r03.md`); today's page scored 7.8 and failed One job 5 and Salience 6. Proposed by the agent; it waits for JL's one look in `runs/r01_collect_task_report_views` (261101).

Open
----

Your one look: `../runs/r01_collect_task_report_views` shows each screen beside today's page: build it as drawn, or keep today's.

Still open after the redraw's reviews:

1. Read could come first after the MindMap, the result a reader wants most; drawn in the life's order.

The earlier questions, my picks now drawn in, are in `../runs/r01_collect_task_report_views/passes/p01-1031/` and the round 2 screens' form in `passes/p02-1101/`; the full proposal is `result/views-proposal.md`.

(write here, or mark the drawing in red)
