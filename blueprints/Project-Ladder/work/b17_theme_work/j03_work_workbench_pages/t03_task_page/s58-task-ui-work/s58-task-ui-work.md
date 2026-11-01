s58 · Task UI: Work
===================

**Tags:** `Task UI`

**Stage:** shaping

**For:** a deck, and the work Task's Work screen on the focus page (`delivery/ui/task-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Task's Work: one view per step of its life (haipipe-task ref/lifecycle.md): A Plan, B Build, C Run, D Read, E Close; each ⚙️ Process (In → who works → Out, your part), then 📊 Results, then the next step.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** A Task's Work: one view per step of its life, plan to close; one cell of the work theme's 3 × 3, the work Task × Work (do) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s58_task_ui_work.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s58-task-ui-work/
├── s58-task-ui-work.md               this face
├── build_s58_task_ui_work.py         the builder (../../work_ui_cells.py draws it)
├── s58-task-ui-work.excalidraw       the five parts: Idea · Now · Design · Process · Delivery
├── s58-task-ui-work.png              its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s58-D01 · Redrawn 261101 the way b16 and b15 draw theirs: each view one step of the work, input → who works → output, your part, then the results (JL 261101: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI); the steps are haipipe-task's life, plan ▶ build ▶ run ▶ read ▶ close (ref/lifecycle.md). The earlier screens' rounds stay in `review/` (r01, r02).

s58-D02 · A · Plan passed the drawing review (stage 1), mean 8.3/10 in `review/A-s1-r03.md` (rounds: `review/A-s1-r03.md`); today's page scored 8.8 and failed Salience 5. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_task_work_views` (261101).

s58-D03 · B · Build passed the drawing review (stage 1), mean 8.4/10 in `review/B-s1-r03.md` (rounds: `review/B-s1-r03.md`); today's page scored 8.8 and failed Salience 5. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_task_work_views` (261101).

s58-D04 · C · Run passed the drawing review (stage 1), mean 9.0/10 in `review/C-s1-r03.md` (rounds: `review/C-s1-r03.md`); today's page scored 8.8 and failed Salience 5. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_task_work_views` (261101).

s58-D05 · D · Read passed the drawing review (stage 1), mean 8.7/10 in `review/D-s1-r04.md` (rounds: `review/D-s1-r03.md`, `review/D-s1-r04.md`); today's page scored 8.8 and failed Salience 5. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_task_work_views` (261101).

s58-D06 · E · Close passed the drawing review (stage 1), mean 8.9/10 in `review/E-s1-r05.md` (rounds: `review/E-s1-r03.md`, `review/E-s1-r04.md`, `review/E-s1-r05.md`); today's page scored 8.8 and failed Salience 5. Proposed by the agent; it waits for JL's one look in `runs/r02_collect_task_work_views` (261101).

Open
----

Your one look: `../runs/r02_collect_task_work_views` shows each screen beside today's page: build it as drawn, or keep today's.

Still open after the redraw's reviews:

1. Step buttons could carry each step's state word and Work open on the step in progress, as a draft Task's do (r03 asks); asked in the form.
2. Read could put its headline above the flow (r04 asks on D); the shared step shape keeps the flow first.

The earlier questions, my picks now drawn in, are in `../runs/r02_collect_task_work_views/passes/p01-1031/` and the round 2 screens' form in `passes/p02-1101/`; the full proposal is `result/views-proposal.md`.

(write here, or mark the drawing in red)
