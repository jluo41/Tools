---
name: hai-task
description: "Owns the Task level and is the door to every kind of Task: the numbered tNN Task folder (face, scripts/, runs/; a Task may hold a draft), its life plan, build, run, read, close, and task-type routing to the type skills. Use to create or run a Task. Trigger: task, tNN, task-type, task face, /hai-task."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "2.0.4"
  last_updated: "2026-11-27"
  folder_owner: canonical
  folder_kind: task
  primary_face: task
  page_ruling: local
  outline:
    mode: grammar
    source: "ref/task-page.md"
    shape: "FLAT or NESTED; first word from {Introduction, Concept, Landscape, Data, Method, Result, Conclusion}; Introduction when present is division 1 and appears once; Concept, Landscape, Data may sit page-level; Method, Landscape and Result repeat; a residual earns its own Result-role division; Conclusion is one page-level division, always last"
---

# hai-task · the Task level, and the door to every kind of Task

In an Idea Job, each Task answers a bounded development/evaluation question
and may use several skills. Local reviews use shared soft assessment Runs;
new scientific computation stays in Work and source acquisition in Discovery.
Read the [Idea Block contract](../../ideation/hai-ideation/references/idea-block.md)
for ownership. Authored idea assessments use the registered `task-type: ideation`
and route plan/build/run to `hai-ideation`'s `references/assessment-task.md`.
Scientific experiments and separate prose Pages retain their existing types.


This skill does two jobs. **A. The Task level**: what one `tNN_<task>/` folder holds, how its Runs
sit in it, and how it lives and closes. **B. The type door**: its face's `task-type:` sends the work
to the type skill that knows that kind of Task. Between them sit the parts every type shares.

```text
hai-task
  ├─ A  the Task level    face · folder · life · Task Page      ref/task-folder.md, lifecycle.md, task-page.md
  ├─ B  the type door     task-type: ─▶ hai-task-for-<type>  ref/types.md
  └─ shared by all types  ticket · runtime.yaml · metrics.json · heavy.yaml · authoring rules
```

> ⛔ **Generated files: never modify them directly; change the code that writes them, then rerun it**
> This includes a ticket a `gen_*.py` writes, a notebook, a figure, a Table Card and generated Run Results.
> Authored content and accepted human feedback remain with their owning writer; never regenerate them as disposable output.

## Who owns what around a Task

```text
level   folder            face            owner
Block   work/bNN_<topic>/ board.md        hai-block · hai-project ref/ladder.md (shape, today's rules)
Job     jNN_<job>/        jNN_<job>.md    hai-job (Tasks in order, emoji, ## Deliverables)
Task    tNN_<task>/       tNN_<task>.md   hai-task (this skill)
Run     runs/<run>/       run.yaml        hai-run (identity, card, role, receipt rules, prune, Workflow)
```

The Block type's contract determines which Job and Task levels apply. This skill owns the Task
records and their execution; it does not invent Task levels for types that have none. The Block owns
the workbench page: Job and Task selections stay inside it, retaining its route and title. Delivery
belongs to the Block (`delivery/` at the Block only; `hai-delivery`).

## A · The Task level

### New Task

1. **Scaffold**: `python Tools/plugins/haipipe-toolkit/skills/1_base/project/hai-job/scripts/new_job.py task <job> --slug <task> --title '<what it delivers>' --type <task-type> [--nn NN] [--answers Q01.E1]`.
2. **What it makes**: the next `tNN_〈task〉/`, its face and its line in the Job's `## Tasks`. The scaffold also creates `scripts/config/` and `runs/` for execution Tasks; for `draft` and `ideation`, their owner creates content and Runs when needed.
3. **Fill the face**: `goal:`, `close:`, `owner:`; `task-type:` is a value from `ref/types.md`, which names the type skill that builds it.
4. **First Run**: for an execution Task, `/hai-task run <task-folder> r01_<noun>_first` follows `fn/run.md`. For an authored Task, follow its type owner's Run contract. A scaffold does not mean a Run has executed or produced a receipt.

### The folder

```text
tNN_<task>/
├── tNN_<task>.md          the face: state · goal · close · task-type · Opening
├── scripts/               this Task's code; scripts/config/ for settings Runs share
├── runs/rNN_<run>/        one folder per Run: ticket · config · run.yaml · result/ · passes/
├── draft/                 only when the Task writes
├── notebooks/ sbatch/     generated papermill copies · a supervisor for this Task's tickets
└── workflow/              optional: plan.yaml and report.yaml
```

The contract, with what earns a Task, a Run inside a Task, the output modes, supervisors and names,
is `ref/task-folder.md`. Only create code, workflow and Run material required by the selected type.

### The face

Every Task face starts with its header lines, then its Opening:

```markdown
# <what this Task delivers, in three to five words>
state: 🔴 OPEN
goal: <what this Task delivers, one line a stranger reads>
close: <what must be true for this Task to close, one line>
owner: <who>
folder-kind: task
task-type: <a value from ref/types.md>
task: .
```

`goal:` and `close:` identify the intended output and its completion condition. A Task that a reader
studies can carry the authored face in `ref/task-page.md` (Opening, content divisions, displays and
READING), started from `ref/task-page-template.md`; a quick worker Task keeps its header and Opening.
The authored face is content inside the Task record, not an independent workbench route.

### The life

```text
plan ─▶ build ─▶ run ─▶ read ─▶ close
Job item, goal/close, planned Run cards ─▶ worker, config, ticket ─▶ receipt ─▶ headline, describe
and figures Runs, reading ─▶ close: true and the Job's items tick
```

`ref/lifecycle.md` says what each step leaves on disk and who writes it. A paid, long or shared-store
Run waits for a person to press Run (the SPACE's AGENTS.md § Working rules); a quick local unpaid one is run and reported.

### Commands

```text
/hai-task <task-folder>                  the whole life of one Task
/hai-task plan|build|execute|report <task-folder>   one step (fn/stage-plan.md, fn/stage-report.md)
/hai-task <job> | <block>                every Task under it, in path order
/hai-task run <task-folder> [run-name]   make or run one Run (fn/run.md)
/hai-task audit <task|job|block>         pair tickets, configs, receipts, Results (fn/audit.md)
/hai-task block <block-path|name>        a new work Block, on hai-block's scaffold (fn/block.md)
/hai-task job <type> [args…]             a new Job through its type skill
/hai-task feedback | digest              feedback capture and session harvest (fn/feedback.md, fn/digest.md)
```

The whole-life command runs the Workflow script `ref/task-lifecycle.workflow.js` with
`{task_folder, type, stages, autoExecute}`, once per Task at Job or Block scope, continuing after a
failure and gathering every verdict. Three agents keep the duties apart:
`hai-task-orchestrator-agent` coordinates, `hai-task-creator-agent` writes the plan, code and
report, `hai-task-reviewer-agent` judges them (`pass`, `warn`, `revise`, `blocked`, `fail`); creator and
reviewer are never the same agent.

## B · The type door

`task-type:` on the face picks the type skill; the table, the rules for choosing, the asked-or-silent
contract and the `## Type contract` block every type skill carries are `ref/types.md`.

Read the type owner's SKILL.md selected by `ref/types.md`, including specialists hidden from
automatic invocation with `disable-model-invocation: true`. A person can invoke a specialist
explicitly; this door also routes the Task to that same owner.

```text
task-type                         read
raw                               ../1_data/hai-task-for-raw/SKILL.md
description                       ../1_data/hai-task-for-description/SKILL.md
data                              ../1_data/hai-task-for-data/SKILL.md
algo                              ../2_nn/hai-task-for-algo/SKILL.md
endpoint                          ../3_end/hai-task-for-endpoint/SKILL.md
individual                        ../4_individual/hai-task-for-individual/SKILL.md
fit (+ GPU parts)                 ../5_fit/hai-task-for-fit/SKILL.md
eval                              ../6_eval/hai-task-for-eval/SKILL.md
display                           ../7_display/hai-task-for-display/SKILL.md
stata-cms · -case · -data · -reg  ../8_stata/hai-task-for-stata/SKILL.md
agent (+ LLM engine part)         ../9_agent/hai-task-for-agent/SKILL.md
evidence                          ../10_evidence/hai-task-for-evidence/SKILL.md
draft                             hai-draft (authored content and its Run contract)
ideation                          hai-ideation (references/assessment-task.md)
labeling · -building · -scanning  hai-labeling (a listed skill)
```

GPU is how a fit Task executes, not a type: `hai-task-for-fit` owns `hai-task-for-fit/_parts/gpu` and
`hai-task-for-fit/_parts/gpu-training` (preflight the exact GPUs, never kill an unowned process, one ticket after
the last receipt is terminal, finite OOM fallbacks, every queue step recorded). A staged pipeline
Project numbers its Blocks by stage (`ref/pipeline-blocks.md`); the number never says the type.

## Shared by every type

```text
ref/run-sh-template.sh         the ticket body: finds its address, writes the receipt, gates the Result
ref/runtime-yaml-schema.md     the receipt, result/runtime.yaml
ref/metrics-json-schema.md     result/metrics.json
ref/authoring-conventions.md   worker cells, notebooks, artifact placement (HEAVY_DIR + heavy.yaml)
ref/config-meta-template.yaml  a config's _meta block
ref/intent-docstring-template.py  a worker's opening docstring
ref/databricks-execution.md    a ticket that runs on Databricks
scripts/check_task_tree.py     the folder checker (ref/task-tree-checklist.md lists its rows)
```

## Questions, Insight and literature

A Block Question and its report are `hai-report`'s (`reports/qNN_<topic>/`, written through
`hai-draft`); they are not this skill's `workflow/report.yaml`. New executable evidence for a
question is an ordinary Run: reuse an exact Result first, else make a new Run. Literature goes to
`hai-discovery`; reading across Results goes to `hai-page-insight`.

## Definition of done

1. For an execution Task, the folder passes `scripts/check_task_tree.py` (shown to fail first on
   a broken scratch copy) and the applicable `hai-project` structural audit.
2. For execution changes, a representative ticket ran and its receipt and required Results
   support the claimed outcome. A dry run can verify command wiring, not output correctness.
3. The owning Block's Job/Task view shows this Task's actual records and output evidence; check
   the selected Task, its source links and completion conditions without leaving the Block.
4. For an authored Task, apply its owner-specific writing/assessment gates instead of requiring
   a computational ticket or Result schema that does not apply.

Return:

```text
status:    ok | blocked | failed
summary:   what changed and what the checks proved
artifacts: exact paths made or changed
next:      one safe command or reader action
```
