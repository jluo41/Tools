s52 · Block UI: Work
====================

**Tags:** `Block UI`

**Stage:** shaping

**For:** a deck, and the work Block's Work screen on the focus page (`delivery/ui/block-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the Block's Work: the same views as its Report, A · MindMap, B · Status, C · Findings, each ⚙️ Process first (closed: 🚧 Jobs not finished on Status, ✍️ Answers to write or agree on Findings, 🧰 the skills that do it), then 📊 Results, the Report's view by the same code (Status adds each Task's output and the Interaction button); 🙋 Interaction each view's last section. Red, kept proposals: 📍 Where it stands as Status's main point, the Block's own Runs.

**Excluded:** the other eight cells of the 3 × 3 (j03's other sNN); what every work page shares (b17-s04).

**Topic:** The Block's Work: Process, then the Report's views; one cell of the work theme's 3 × 3, the work Block × Work (do) (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Its drawing is haipipe-studio's five parts, drawn by `build_s52_block_ui_work.py` through j03's `work_ui_cells.py`; Its Design is its section's views, lettered A, B …, each one full screen (haipipe-ui "one view, one screen"), every review round in `review/`.

**Feeds:** none: a work Block keeps no Questions (JL 261031, r01 Q5)


Files
-----

```text
s52-block-ui-work/
├── s52-block-ui-work.md              this face
├── build_s52_block_ui_work.py        the builder (../../work_ui_cells.py draws it)
├── s52-block-ui-work.excalidraw      the five parts: Idea · Now · Design · Process · Delivery
├── s52-block-ui-work.png             its card
├── review/                         each review round: <L>-s1-rNN.md, its picture; today-261101.md
└── delivery/ui/                      the agreed screen, once agreed
```


Decided
-------

s52-D01 · Where things stand lives in Work, as rows; the Report keeps one word per delivery (JL 261031, r01_collect_report_and_delivery Q6: A, "the rows stay in Work").

s52-D02 · Redrawn 261101 the way b16 and b15 draw theirs: each view one step of the work, input → who works → output, your part, then the results (JL 261101: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI); the steps are haipipe-task's life, plan ▶ build ▶ run ▶ read ▶ close (ref/lifecycle.md). The earlier screens' rounds stay in `review/` (r01, r02).

s52-D03 · A · Progress passed the drawing review (stage 1), mean 8.9/10 in `review/A-s1-r04.md` (rounds: `review/A-s1-r03.md`, `review/A-s1-r04.md`); today's page scored 7.8 and failed Words 6 and One job 6. Proposed by the agent; it waits for JL's one look in `runs/r03_collect_block_work_views` (261101).

s52-D04 · Work has the same views as Report, A · MindMap, B · Status, C · Findings: each ⚙️ Process first, then 📊 Results, the Report's view drawn by the same code; the single A · Progress view is gone (asked 261104: "why we have the progress? it should have the same view to the report"; redrawn 261105). Its 261101 rounds stay in `review/`.

s52-D05 · The Jobs' card tabs give way to Status's rows, one per Job, each opening to its Tasks and Runs (asked 261104: "each job each row, and we can collapse them out to see the tasks and runs"; 261105). This settles the still-open line on which Job the card tabs open on.

s52-D06 · Every section starts closed (asked 261104: "默认的话，大家都是合着的"); 🙋 Interaction shows once, as each view's last section, numbered after its band's, never a Process step "🙋 Waiting on you"; the drawn 🙋 Interactions helper after a dashed rule became that section (decided for this round, 261105).

s52-D07 · 📍 Where it stands and the Block's own Runs stay on the drawing in red, as open proposals: no 261104 ask overruled them (261105).

s52-D08 · Redrawn to the live page of 261106: the right rail gains Skills, so 🧰 Skills that do it leaves every Process, and A · MindMap has no Process at all (it has no step); each bar carries its state word (Jobs not finished "1 of 3 done"), Findings' Answers to write or agree its waiting line; each view's 🙋 Interaction holds its own forms, as the Report's (261106).

Open
----

Your one look: `../runs/r03_collect_block_work_views` asks about the two red proposals.

Still open after the 261105 redraw:

1. 📍 Where it stands as Status's main point, one large sentence above Process (red on the drawing).
2. The Block's own Runs as a Process section (red on the drawing).

The earlier questions, my picks now drawn in, are in `../runs/r03_collect_block_work_views/passes/p01-1031/` and the round 2 screens' form in `passes/p02-1101/`; the full proposal is `result/views-proposal.md`; the 261101 screens' form is in `passes/p03-1101/`.

(write here, or mark the drawing in red)
