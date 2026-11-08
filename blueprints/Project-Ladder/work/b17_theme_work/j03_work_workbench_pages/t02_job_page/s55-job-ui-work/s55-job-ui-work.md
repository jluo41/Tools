s55 · Job UI: Work
==================

**Tags:** `Job UI`

**Stage:** shaping

**For:** a deck, and the work Job's Work screen on the focus page (`delivery/ui/job-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Job's Work: the same views as its Report, A · MindMap, B · Status, C · Findings, each ⚙️ Process first (🚧 Tasks not finished, 🧰 the skills that do it), then 📊 Results, the Report's view by the same code (Status adds each Task's output and the Interaction button); 🙋 Interaction each view's last section. Red, a kept proposal: each Task against the five steps of a Task's life.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** A Job's Work: Process, then the Report's views; one cell of the work theme's 3 × 3, the work Job × Work (do) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s55_job_ui_work.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s55-job-ui-work/
├── s55-job-ui-work.md                this face
├── build_s55_job_ui_work.py          the builder (../../work_ui_cells.py draws it)
├── s55-job-ui-work.excalidraw        the five parts: Idea · Now · Design · Process · Delivery
├── s55-job-ui-work.png               its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s55-D01 · Redrawn 261101 the way b16 and b15 draw theirs: each view one step of the work, input → who works → output, your part, then the results (JL 261101: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI); the steps are haipipe-task's life, plan ▶ build ▶ run ▶ read ▶ close (ref/lifecycle.md). The earlier screens' rounds stay in `review/` (r01, r02).

s55-D02 · A · Progress passed the drawing review (stage 1), mean 8.7/10 in `review/A-s1-r04.md` (rounds: `review/A-s1-r03.md`, `review/A-s1-r04.md`); today's page scored 8.0 and failed Phone 6 and Salience 6. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_job_work_views` (261101).

s55-D03 · Work has the same views as Report, A · MindMap, B · Status, C · Findings, each ⚙️ Process then 📊 Results; the A · Progress view is gone, and with it its Where it stands sentence and its own Runs (asked 261104: "why we have the progress? it should have the same view to the report"; redrawn 261105).

s55-D04 · The Tasks × five steps grid stays on B · Status, under its Tasks, in red, as an open proposal: no 261104 ask overruled it (261105).

s55-D05 · Every section starts closed (asked 261104: "默认的话，大家都是合着的"); 🙋 Interaction shows once, as each view's last section, never a Process step (decided for this round, 261105).

s55-D06 · Redrawn to the live page of 261106: the right rail gains Skills, so 🧰 Skills leaves Process; A · MindMap and C · Findings have no Process now (the map has no step, the Job has no Questions to answer); Tasks not finished reads "0 of 3 done"; each view's 🙋 Interaction holds its own forms (261106).

Open
----

Your one look: `../runs/r02_collect_job_work_views` asks whether to keep the red Tasks × steps grid, beside today's page.

Still open after the redraw's reviews:

1. A Task's Read can wait on you while its other Runs still run, as t01's does (r04 asks).
2. The Tasks × steps grid under Status's Tasks (red on the drawing).

The earlier questions, my picks now drawn in, are in `../runs/r02_collect_job_work_views/passes/p01-1031/` and the round 2 screens' form in `passes/p02-1101/`; the full proposal is `result/views-proposal.md`; the 261101 screens' form is in `passes/p03-1101/`.

(write here, or mark the drawing in red)
