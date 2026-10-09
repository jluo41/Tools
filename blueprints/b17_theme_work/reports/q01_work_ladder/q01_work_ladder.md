# How does work climb the ladder?
state: 🟡 DRAFT
answers: Q01
answer-status: open

## Opening

Proposed (261007), open until JL settles it: the work Theme climbs the shared ladder unchanged.
Block, Job and Task each get the same six Spaces, Description | Idea Studio · Audience Report |
Work Details | Runs · Delivery, and a Run is no tab of its own: it opens from a Runs list. Today's
Task workbench shows everything on the Block in four Spaces (Scope · Task · Check · Delivery); each
of its views gets one home on the ladder, and the Check Space goes away (b03 s01-D18).

**Where this Page sits:** [Q01 · What do the task Block, a work Job, a work Task and a hard Run each hold and show on screen, and which of today's Scope, Task, Check and Delivery Views moves to which level?](../../board.md).

**Why it matters:** the folder contract and the scaffold (new Block · Job · Task · Run) and the
work workbench's level tabs are built from this answer, level by level.

## Content

### Answer

Each level: its folder, then what each Space shows. Red in the drawing = open.

```text
level  folder                 Description          Idea Studio     Audience Report         Work Details           Runs                       Delivery
-----  ---------------------  -------------------  --------------  ----------------------  ---------------------  -------------------------  -----------------
Block  bNN_<topic>/           face: spine, close,  sNN-<topic>/,   one row per Question:   Jobs, each open to     own soft Runs (draw,       optional; own built
                              the Question         one after       Question | Work |       its Tasks; Plan·Build  report, check, delivery)   reports + released
                              register; Scope ·    another; the    Report; third row =     ·Run·Report chips;     + "from below" its Tasks'  reports from below
                              Resources · Related  question map    question groups         third row = j0N·j1N..  hard Runs; third row=types
Job    jNN_<job>/             face jNN_<job>.md:   optional        open: a filter of the   its Tasks, with chips; own soft Runs (plan the    optional
                              goal, state,                         Block's Questions its   third row = task       Tasks, review src/, launch
                              task_groups; shared                  Tasks feed              groups t0N·t1N         a group) + from below
                              src/ · sbatch/
Task   tNN_<task>/            its Page: goal,      optional        Question | Work |       Code · Review ·        hard rNN_<slug>/ +         cards: Reports ·
                              plan (inputs →                       Report for its own      Notebooks              soft run-build-,           Exports
                              worker → Runs)                       Questions; Draft·Report                        run-report-, run-check-
Run    runs/rNN_<slug>/       no tab: a pop-out from Task › Runs (or Block › Runs, from below): run.yaml card · ticket · config ·
                              result/ preview (metrics, tables, figures) · passes/pNN-<MMDD>/ (one per execution of the same ticket)
```

On disk, per level (b03 s01-D14, D15, D17):

- **Block** `bNN_<topic>/`: `bNN_<topic>.md` (was `board.md`) · `studio/sNN-<topic>/` · `reports/qNN_<topic>/` ·
  `related/related.md` · `runs/` (soft only, with `README.md`) · `delivery/` (optional) · `jNN_<job>/`.
- **Job** `jNN_<job>/`: `jNN_<job>.md` (today it sits in `diagram/`) · `src/` · `sbatch/` · `CODE_REVIEW.md`
  (of `src/`) · `studio/` (optional; today's `diagram/*.excalidraw` moves here) · `runs/` (soft only) ·
  `delivery/` (optional) · `tNN_<task>/`.
- **Task** `tNN_<task>/`: `tNN_<task>.md` · `scripts/` · `CODE_REVIEW.md` · `runs/` (hard and soft) ·
  `notebooks/` (generated) · `workflow/` · `studio/`, `sbatch/`, `delivery/` (optional).
- **Run** `runs/rNN_<slug>/`: `run.yaml` · `rNN_<slug>.sh` · `config.yaml` · `result/` (generated; heavy output
  through `heavy.yaml` to `ProjectResult`) · `passes/pNN-<MMDD>/` (log, `runtime.yaml`). Today a Run is two
  places, `runs/rNN_<slug>.sh` and `results/rNN_<slug>/`; tools read both until the move.

Where today's Task workbench views go:

```text
today (Task workbench, board level)          proposed
-------------------------------------------  ------------------------------------------------------------
Guide › Description · Method · RoadMap Draw  Guide, unchanged
  · Related Paper
Scope › Block                                Block › Description › Scope
Scope › Questions                            Block › Audience Report (the rows); the register stays in the face
Scope › Resources                            Block › Description › Resources
Scope › RoadMap Draw                         Block › Idea Studio (the question map is a generated topic)
Task › <group A> · <group B>                 Block › Audience Report, its third row
Task › a row's Task Work tree                Block › Work Details (Jobs, each open to its Tasks)
Task › Not under a Question                  Work Details: a Task with no Question chip
Task › Plan · Build · Run · Report buttons   the Task tab's Run types
Check › Runs                                 Block › Runs, "from below"
Check › Tasks                                state chips on Work Details rows; Check a Task = run-check-<task>
Check › Reports                              run-check-qNN in Block › Runs; the release check in Delivery
Delivery › Reports                           Block › Delivery
a Task's "Task Page" link (pop-out)          the Task tab
(no Job screen)                              the Job tab
```

Run types, one `runs/README.md` per level (the buttons in the Run types panel):

- **Block**: Ask a Question · Review the questions · Add a resource · Draw · Draw the question map ·
  Write the report · Check a report · Build the report.
- **Job**: Plan its Tasks · Review the shared code · Launch a group · Update the Job.
- **Task**: Plan a Task · Review the plan · Build the Task · Review the Task code · Run a Task (hard) ·
  Report the Run · Check a Task.
- **Run**: Rerun (a new pass) · Open the Result.

### Evidence

- [work ladder](../../studio/s01-work-ladder/s01-work-ladder.excalidraw), frame "work ladder · Q01" (the
  grid, the moves, the open points); the frames below it are b03's work rows (s06, s07, s08).
- The shared ladder: `Tools/blueprints/b03_project_workbench/studio/s01-overall-tree-structure/s01-overall-tree-structure.md`
  (s01-D13 to D23, D28) and the s08 decisions in `Tools/blueprints/b03_project_workbench/studio/s13-task-variants/s13-task-variants.md`.
- Today's workbench: `Tools/plugins/haipipe-toolkit/skills/2_theme/work/workbench-work/ref/workbench-table.md`.
- Folder names read off a real task Block (names only, no data): its Job keeps its face in `diagram/`, its
  Tasks keep `runs/rNN_<slug>.sh` beside `results/rNN_<slug>/`, and no task Block holds a Page Job.

### Limits

Open, red in the drawing; each needs JL:

1. What does work fill in at the Job? Settled by the frame (b02, 261007): every level, the Job too, gets
   the six Spaces; what a theme leaves out shows the vanilla default (face, studio/, reports/, its Tasks,
   runs/, delivery/). Still open: the Job's own content beyond vanilla, proposed as Description › Scope ·
   Shared code (`src/`, `sbatch/`, `CODE_REVIEW.md`) and the Job's soft Runs. b03's work Job row still
   draws the older Overview · Studio · Reports | Tasks | Runs · Delivery and should follow.
2. Job › Audience Report: a filter of the Block's Questions, with no `reports/` at a Job?
3. Task › Audience Report: the Block's qNN Page, or a Task Page of its own? Today some Tasks keep a Page in
   `workflow/` (`qNN_<topic>.md`, `page.toml`). Settled with Q03.
4. A Task's `draft/records/` and `workflow/`: kept, or folded into `runs/` and the face? Settled with Q02.
5. `notebooks/rNN_<run>.ipynb`: stays in the Task, or moves into `runs/rNN_<slug>/`?
6. Page Job and Page Task are not work rows: no task Block on disk has one, and a Page Task is the base's
   Task level (`servers/workbench/task`). Drop them from the work frames?
7. The Job series (j0N · j1N · j5N): read from the face, never hard-coded?
8. A Run opens as a pop-out, not a fifth tab?
9. A wet Task (a procedure run by a person, b03 s01-D28): its protocol ticket and signed receipt in the same
   `runs/rNN_<slug>/`?

### Next

Once JL settles the open points: the work skill's folder contract and its scaffold (new Block · Job ·
Task · Run), then the work workbench's level tabs on the base frame (`servers/workbench`), tested on a
placeholder demo Block in a temp folder. Real Blocks move only when JL asks.
