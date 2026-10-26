---
mindmap: 1
title: s01 · How work climbs the ladder · structured
built: from-topic .
written: 261026, from the drawing s01-work-ladder.excalidraw, frame by frame
---

# s01 · How work climbs the ladder

Q01, proposed 261007 and open until JL settles it: each level of the work Theme, its folder and its six Spaces, against today's Task workbench.

- [Q01 grid] One grid: six Spaces at every level <!-- n01 -->
  → Then where does each of today's views go?
  - [rule] Every level gets the same six Spaces <!-- n02 -->
    Description · Idea Studio · Audience Report · Work Details · Runs · Delivery, at Block, Job and Task alike (b03 s01-D20, D22); the Run types panel on the right lists each level's buttons.
  - [Block] Questions as rows; Jobs open to their Tasks <!-- n03 -->
    **Description** the face (spine · close · the Question register), third row Scope · Resources · Related. **Idea Studio** one drawing after another; the question map is generated. **Audience Report** one row per Question: Question │ Work │ Report. **Work Details** Jobs ▾, each open to its Tasks, with Plan · Build · Run · Report chips; third row the Job series j0N · j1N · j5N. **Runs** its own soft Runs (run-draw-, run-report-, run-check-qNN, run-delivery-) and, from below, its Tasks' hard Runs. **Delivery** optional: built reports, released reports from below.
  - [Job] Its Tasks and its shared code; no reports <!-- n04 -->
    **Description** the face: goal · state · next, task_groups t0N · t1N; third row Scope · Shared code (red: open). **Audience Report** red: no reports/ at a Job, only a filter of the Block's Questions its Tasks feed. **Work Details** its Tasks with chips; pick one → the Task tab. **Runs** run-plan-tasks, run-review-src, run-launch-<group> (sbatch/), and from below. **Delivery** optional: an export its Tasks share.
  - [Task] Its Page, its code, its hard Runs <!-- n05 -->
    **Description** its Page: goal, plan (inputs → worker → Runs), close. **Audience Report** Question │ Work │ Report for this Task's Questions only (red: the Block's qNN Page, not a Task Page). **Work Details** how the work is done: Code · Review · Notebooks. **Runs** hard rNN_<slug>/ (the evidence), soft run-build-, run-report-, run-check-<task>. **Delivery** cards: Reports · Exports.
  - [Run] No tab: a pop-out with card, ticket, result <!-- n06 -->
    Opened from Task › Runs (or Block › Runs, from below): run.yaml (the card) · the ticket · config.yaml (frozen inputs) · result/ (metrics, tables, figures; heavy output to ProjectResult) · passes/pNN-<MMDD>/, one per execution of the same ticket. New inputs make a new rNN.
- [moves] Each of today's views gets one home <!-- n07 -->
  → And what must each level hold on disk to feed those screens?
  - [Scope] Block, Questions, Resources → Block's Description and Report <!-- n08 -->
  - [Draw] RoadMap Draw → Block › Idea Studio <!-- n09 -->
    The question map becomes a generated Studio topic.
  - [Task] Question groups → Audience Report's third row <!-- n10 -->
  - [Work] The Task Work tree → Work Details, Jobs ▾ Tasks <!-- n11 -->
  - [Check] Runs, Tasks, Reports → Runs and state chips <!-- n12 -->
    Check › Runs → Block › Runs (☐ from below); Check › Tasks → state chips on Work Details rows, Check a Task = run-check-<task>; Check › Reports → run-check-qNN in Block › Runs, the release check in Delivery. The Check Space goes away.
  - [new] A Job tab and a Task tab, where none exist today <!-- n13 -->
- [Block frame] The Block: its folder, its skills, its screens <!-- n14 -->
  → What changes one level down?
  - [folder] Face, studio/, reports/, related/, runs/, delivery/ <!-- n15 -->
    bNN_<topic>.md (was board.md) · studio/sNN-<topic>/ (face, drawing, builder, chat/) · reports/qNN_<topic>/ · related/related.md · runs/ (soft only: run-draw-<sNN>, run-report-<qNN>, run-delivery-<lane>) · delivery/ (optional) · jNN_<job>/.
  - [skills] haipipe-task, haipipe-report, excalidraw-report own it <!-- n16 -->
  - [shows] workbench-work draws it <!-- n17 -->
  - [screens] Each Space proposed, over today's board page <!-- n18 -->
- [Job frame] The Job: shared code, soft Runs only <!-- n19 -->
  → And the level where the work is done?
  - [folder] Face, src/, sbatch/, studio/, runs/ <!-- n20 -->
    jNN_<job>.md (red: no Job face on disk yet) · src/ (code its Tasks share) · sbatch/ · studio/ (optional) · runs/ soft only, no evidence at a Job: run-plan-tasks, run-launch-<group> · tNN_<task>/.
  - [skills] haipipe-task and its type skills work here <!-- n21 -->
  - [today] No Job screen: a Job is spread over three places <!-- n22 -->
- [Task frame] The Task: the Page, the code, the evidence <!-- n23 -->
  → What about the Page Job and Page Task rows?
  - [folder] Page, code review, scripts/, runs/, notebooks/ <!-- n24 -->
    tNN_<task>.md (the Page) · CODE_REVIEW.md · scripts/<worker>.py · runs/rNN_<slug>/ (run.yaml · ticket · config.yaml · result/ · passes/) · notebooks/rNN_<run>.ipynb (generated) · workflow/ (plan.yaml · report.yaml) · studio/ · sbatch/ (optional).
  - [evidence] A hard Run writes only its own result/ <!-- n25 -->
  - [today] No Task screen: a line in the Task Work tree <!-- n26 -->
- [Page frames] Page Job and Page Task: not work rows <!-- n27 -->
  → What is still open in the drawing?
  - [why] No work Block on disk has one <!-- n28 -->
  - [proposal] Drop them here: a Page Task is the base's Task <!-- n29 -->
    A Page Task is the base's Task level (servers/workbench/task), not a work row.
- [open] Nine red points <!-- n30 -->
  → And what has happened since it was drawn?
  - [1] What fills a Job beyond the vanilla Spaces? <!-- n31 -->
  - [2] A Job's Report: a filter of the Block's Questions? <!-- n32 -->
  - [3] A Task's report: the Block's qNN Page or its own? (Q03) <!-- n33 -->
  - [4] Keep a Task's draft/records and workflow/? (Q02) <!-- n34 -->
  - [5] Notebooks: in the Task, or in runs/rNN_/? <!-- n35 -->
  - [6] Drop Page Job and Page Task here? <!-- n36 -->
  - [7] Job series read from the face, never hard-coded? <!-- n37 -->
  - [8] A Run opens as a pop-out, not a fifth tab? <!-- n38 -->
  - [9] A wet Task: ticket and signed receipt in one Run? <!-- n39 -->
- [since] Since 261007, checked on 261026 <!-- n40 -->
  - [adopted] The disk layout is now the ladder's rule <!-- n41 -->
    One folder per Run (run.yaml, the ticket, result/, passes/pNN-<MMDD>/): [ladder.md](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/ref/ladder.md).
  - [replaced] Work Blocks now open on Goal · Plan · Execution · Results <!-- n42 -->
    Since 261021 (LLMRec b01, b02), with `workbench-layout: workflow` in board.md: [README](../../../../plugins/haipipe-toolkit/servers/workbench-work/README.md).
  - [open] Q01 is still marked open <!-- n43 -->
    Its report: [q01_work_ladder](../../reports/q01_work_ladder/q01_work_ladder.md). b17's own face lacks the workflow line.
- [files] What the folder holds <!-- @files #6ce6c5 -->
  - [py] [build_s01_work_ladder.py](build_s01_work_ladder.py) <!-- @files/0 #c3da0c -->
  - [excalidraw] [s01-work-ladder.excalidraw](s01-work-ladder.excalidraw) <!-- @files/1 #7b5eab -->
  - [md] [s01-work-ladder.md](s01-work-ladder.md) <!-- @files/2 #f08117 -->
  - [png] [s01-work-ladder.png](s01-work-ladder.png) <!-- @files/3 #031882 -->
    ![s01-work-ladder.png](s01-work-ladder.png)
