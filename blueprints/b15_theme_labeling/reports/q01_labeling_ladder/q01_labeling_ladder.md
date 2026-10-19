# How does a labeling job climb the ladder?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

Agreed with JL (261014): the **Job** is one dataset × one label, and its Tasks come in five
**types**, each named by the Task face's `task-type:` line: 📦 items (`data`), 🔑 keys (`raw`),
🏗 building (`labeling-building`), 🔍 scanning (`labeling-scanning`), 📊 score (`eval`). Building and
scanning meet only at the signed Label Handoff; today's one labeling Page (`task-type: labeling`) is
both. The workbench shows this since 261014: Job › Work gives each Task its type and state and a
dashed card for each type still to make; the items Task's Report opens on Itemization · Embedding.
Drawn in [s13-labeling-task](../../studio/s13-labeling-task/s13-labeling-task.md). The 261007 proposal
below (four step Tasks, prepare · keys · label · score) is the earlier form of these types. The
**Block** groups the Jobs; the Run is one operation, `rNN_<operation>_<target>/`.

**Where this Page sits:** [Q01 · What do the labeling Block, a dataset × label Job, a step Task and an operation Run each hold and show on screen, and which of today's four Spaces (Data · Labeling · Quality · Delivery) moves to which level?](../../board.md).

**Why it matters:** the folder contract and the scaffold (new Block · Job · Task · Run) and the
workbench views are built from this answer, level by level.

## Content

### Answer

**The Task types (261014).** One Job, five Task types, as a design Job has three (b12 s13:
`t00` · `tNN_d<NN>` · `t99`). The type is the face's `task-type:` line, never the number, since keys
and score are optional and the numbers shift.

```text
type        task-type            what it does                                       on screen
📦 items     data                 raw rows become items; ground truth kept apart     Report: Itemization · Embedding
🔑 keys      raw                  the dataset's own labels; optional; fenced         vanilla, a fence note
🏗 building  labeling-building    Contract → Rounds → G0 → Freeze → signed Handoff   Work: Preparation … Guideline
🔍 scanning  labeling-scanning    reads the Handoff: Test → Scan → Audit → labels    Work: Test · Evaluation · Scan · Audit
📊 score     eval                 final labels against the keys, raters' spread      vanilla, a note
(today)     labeling             one Page that is building and scanning at once     both rows of views
```

A Job needs items, building and scanning to close, and score once it has keys. The three real Jobs
read as they are: dices350 j01 shows ✅ t01 items · ✅ t02 keys · 🔶 t03 building + scanning · ⬜ t04
score (not made yet); aci_bench and redsm5 have items and a labeling Page, no keys.

**Earlier (261007).** The board's hypothesis was "the Job is today's page-level workbench". It does not hold. Two
existing contracts put the engine's job in a Task:

- haipipe-project (`labelings/`, JL 261005): a Job is one dataset with one label and **many
  Tasks**: its data preparation, its keys, its labeling Page (the engine's `labeling/` lane),
  its scoring.
- the engine (`haipipe-labeling-building/ref/ref-assets.md`): `{project_dir}` is a Page's `labeling/`
  folder, and the job's Runs sit in that Page folder. Under the ladder (b03 s01-D15) hard Runs
  belong to a Task only.

So the page workbench belongs to the labeling Task, and the Job tab is new.

```text
level   folder                       holds                                  its tab, six Spaces
-----   --------------------------   ------------------------------------   ------------------------------------
Block   bNN_<topic>/                 face · studio/ · reports/ · runs/      Work Details = its Jobs, grouped by
                                     (soft) · delivery/ ? · its Jobs        label; each opens to its 4 Tasks
Job     jNN_<dataset>_<label>/       face · schema.yaml · src/ · runs/      Audience Report = ours vs the keys
                                     (soft) · delivery/ ? · t01-t04         Work Details = prepare · keys ·
                                                                            label · score
Task    tNN_<dataset>_labeling/      face (page-type: labeling) ·           today's page workbench, recast
                                     labeling/ · runs/ (hard) · delivery/ ?
Run     runs/rNN_<operation>_<target>/   run.yaml · ticket · result/ ·      a row in Task › Runs, grouped
                                         passes/pNN-<MMDD>/                 Building · Scanning
```

The Job's other three Tasks (items, keys, scoring) are plain work Tasks with hard `rNN_` Runs;
they use the work Task row. A Job that only scans a second dataset is its own
`jNN_<dataset2>_<label>/`, and its labeling Task starts from the first Job's handoff.

**Where today's four Spaces go**

```text
today (page level)        →  proposed
-----------------------      ---------------------------------------------------------------
Data › Preparation        →  Job › Work Details › prepare (the data Tasks it already lists)
Data › Contract           →  Task › Description › Contract
Data › Embedding          →  Task › Work Details › Embedding           ┐
Labeling › Definition     →  Task › Work Details › Definition          │ Building
Labeling › Rounds         →  Task › Work Details › Rounds              │
Labeling › Guideline      →  Task › Work Details › Guideline           ┘
Quality › Test            →  Task › Work Details › Test                ┐
Quality › Evaluation      →  Task › Work Details › Evaluation          │ Scanning
Delivery › Scan           →  Task › Work Details › Scan                │
Quality › Audit           →  Task › Work Details › Audit               ┘
Quality › External gold   →  Job › Audience Report (ours vs the dataset's keys; t04's Runs)
Delivery › Handoff        →  Task › Delivery › Handoff   (rolls up to Job › Delivery)
Delivery › Final labels   →  Task › Delivery › Final labels (rolls up to Job and Block)
REPORT.md (no tab today)  →  Task › Audience Report › Report
board level › Jobs        →  Block › Work Details
```

Scan moves out of Delivery: it is work, and Delivery holds only what leaves the folder (the
handoff, D*, the audit report). The Runs panel keeps the 26 operation types; Task › Runs lists
the Runs with a Building · Scanning third row.

### Evidence

- [labeling Task types](../../studio/s13-labeling-task/s13-labeling-task.excalidraw): the five types as
  one flow, the dices350 Job's Work list, and the items Task's Itemization (261014).
- Code: `Tools/plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py` (`TYPES`,
  `types_of`, `option`, `work_meta`, `_job_spaces`, `_itemization`), tested in
  `servers/workbench-labeling/tests/test_labeling_theme.py` (12 passed, 261014).
- [labeling ladder](../../studio/s01-labeling-ladder/s01-labeling-ladder.excalidraw): the Block,
  Job and Task frames, each with its folder, skills and proposed screens above today's (dashed).
  Red = open.
- The rows are b03's shared definitions, labeling entries only:
  `Tools/blueprints/b10_project_workbench/studio/s01-overall-tree-structure/build_ladder_v4.py` (the trees,
  skills, Block views, the Job's six Spaces) and `level_views.py` (the Job and Task screens,
  today's rows).
- Contracts read: `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/ref/project-structure.md`
  (`labelings/`), `skills/2_theme/labeling/haipipe-labeling-building/ref/ref-assets.md` (the job's disk
  layout), `ref-space-mapping.md` (today's Spaces and 26 Run types),
  `servers/workbench-labeling/workbench-task-labeling/labeling.py` (`_labeling_job`: the page already finds its Job's
  data and gold Tasks).

### Limits

Open, red in the drawing:

1. **Real Jobs keep one labeling Page.** Since 261010 the real Blocks sit at
   `examples-6-labeling/<Project>/labeling/bNN_<dataset>/jNN_<dataset>_<label>/` with `schema.yaml` per
   Job (aci_bench, dices350, redsm5), and each holds one `task-type: labeling` Page that is building and
   scanning at once. Splitting it into a building and a scanning Task at the Handoff changes real
   Project folders and the engine's one lane per Page: JL's call (s13 Open 1, 2).
2. **schema.yaml: Block or Job?** The contract says per Job; the real Blocks hold one schema at
   the Block and teach it on one corpus. Settled in Q03.
3. **Is a labeling Run hard?** Its canonical output lands in the Task's `labeling/` lane, not
   in its own `result/`; the Result would be `result.yaml` with pointers. The ladder's rule
   ("hard or soft by where the output lands") says soft, but its records are evidence (human
   gold, scorecards). Proposed: hard, with the lane read like `heavy.yaml`.
4. **Building | Scanning as the third row** of Task › Work Details, and where the gates show:
   Q02.
5. **delivery/** at Job and Task: the handoff and D* already have canonical places in
   `labeling/`; a `delivery/` folder would hold only reader exports.
6. **Two `labeling/` folders.** The Theme folder becomes singular, `labelings/` →
   `labeling/` (b03 s01-D29, `theme-rename-plan.md`), so a job sits at
   `<Project>/labeling/bNN_<topic>/jNN_<dataset>_<label>/tNN_<dataset>_labeling/labeling/`.
   Depth tells them apart (the Theme's parent is the Project; the lane's parent is a `tNN_`
   folder with its own `.md`). Proposed: keep the lane's name, since the engine, receipts and
   26 Run types all write `labeling/…`. The workbench's `_labeling_job` (`labeling.py`) now reads
   both `labeling` and `labelings`; its `_task_runs` reads one folder per Run,
   `runs/<run>/result/`, since 261014.

### Next

- JL: mark s13's drawing; decide whether the real Jobs' labeling Page splits at the Handoff (limit 1).
- Then the skill contract and scaffold: `haipipe-labeling` names the five types and adds a Task of
  each; Q03 settles where a scanning Task's records live.
