# How does a labeling job climb the ladder?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

Proposed (261007), waiting for JL: the engine's one labeling job is a **Task**, not the Job. The
labeling Task (`tNN_<dataset>_labeling/`, holding `labeling/`) gets today's page-level workbench,
recast into the six Spaces. The **Job** is one dataset × one label: four step Tasks
(prepare · keys · label · score) and a new, thin Job tab. The **Block** groups these Jobs by label.
The Run is one operation, `rNN_<operation>_<target>/`.

**Where this Page sits:** [Q01 · What do the labeling Block, a dataset × label Job, a step Task and an operation Run each hold and show on screen, and which of today's four Spaces (Data · Labeling · Quality · Delivery) moves to which level?](../../board.md).

**Why it matters:** the folder contract and the scaffold (new Block · Job · Task · Run) and the
workbench views are built from this answer, level by level.

## Content

### Answer

The board's hypothesis was "the Job is today's page-level workbench". It does not hold. Two
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

- [labeling ladder](../../studio/s01-labeling-ladder/s01-labeling-ladder.excalidraw): the Block,
  Job and Task frames, each with its folder, skills and proposed screens above today's (dashed).
  Red = open.
- The rows are b03's shared definitions, labeling entries only:
  `Tools/blueprints/b03_project_workbench/studio/s01-overall-tree-structure/build_ladder_v4.py` (the trees,
  skills, Block views, the Job's six Spaces) and `level_views.py` (the Job and Task screens,
  today's rows).
- Contracts read: `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/ref/project-structure.md`
  (`labelings/`), `skills/2_theme/labeling/haipipe-labeling-building/ref/ref-assets.md` (the job's disk
  layout), `ref-space-mapping.md` (today's Spaces and 26 Run types),
  `servers/workbench-labeling/labeling.py` (`_labeling_job`: the page already finds its Job's
  data and gold Tasks).

### Limits

Open, red in the drawing:

1. **Real Blocks differ.** The labeling Blocks under `examples-6-labeling/` sit in `tasks/`,
   keep `schema.yaml` at the Block, and name Jobs by side (`j01_building_corpus/`, a planned
   j02 for Scanning), with one labeling Task per corpus. Moving them to
   `labelings/bNN_<topic>/jNN_<dataset>_<label>/` changes real Project folders: JL's call.
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
   26 Run types all write `labeling/…`. The workbench's `_labeling_job` (`labeling.py`) checks
   only for `labelings`; it must read both names through `haipipe-page/src/themes.py` at
   build time.

### Next

- JL: agree or mark the drawing; decide whether the real labeling Blocks move (limit 1).
- Then Q02 and Q03, then build: the skill contract and scaffold (new Block · Job · Task · Run),
  then the workbench views, on a demo Block in a temp dir.
