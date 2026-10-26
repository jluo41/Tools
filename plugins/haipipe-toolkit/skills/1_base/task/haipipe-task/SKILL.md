---
name: haipipe-task
description: >-
  Owns the Task level of Block → Job → Task → Run and is the door to every kind of Task.
  A Task is one folder, tNN_<task>/: its face (state, goal, close, task-type), its scripts/,
  one folder per Run in runs/ (ticket, config, run.yaml card, result/ with its runtime.yaml
  receipt), and a draft/ when it writes (a Task may hold a draft; a Task is not a Page). It
  owns the folder contract, the Task's life (plan ▶ build ▶ run ▶ read ▶ close), the Task Page
  and its displays, and the ticket body every type shares; its task-type: sends the work to
  the type skill (data, raw, description, algo, fit, eval, display, individual, endpoint,
  agent, evidence, stata, draft, labeling). Use to create, build, run, audit or close a Task,
  pick its type, write its face or Task Page, or check a work/ tree. Trigger: task, task
  folder, tNN, task-type, task face, Task Page, plan, build, execute, report, ticket,
  run-sh-template, runtime.yaml, heavy.yaml, check_task_tree, GPU queue, /haipipe-task.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "2.0.2"
  last_updated: "2026-10-25"
  folder_owner: canonical
  folder_kind: task
  primary_face: task
  page_ruling: local
  outline:
    mode: grammar
    source: "ref/task-page.md"
    shape: "FLAT or NESTED; first word from {Introduction, Concept, Landscape, Data, Method, Result, Conclusion}; Introduction when present is division 1 and appears once; Concept, Landscape, Data may sit page-level; Method, Landscape and Result repeat; a residual earns its own Result-role division; Conclusion is one page-level division, always last"
---

# haipipe-task · the Task level, and the door to every kind of Task

This skill does two jobs. **A. The Task level**: what one `tNN_<task>/` folder holds, how its Runs
sit in it, and how it lives and closes. **B. The type door**: its face's `task-type:` sends the work
to the type skill that knows that kind of Task. Between them sit the parts every type shares.

```text
haipipe-task
  ├─ A  the Task level    face · folder · life · Task Page      ref/task-folder.md, lifecycle.md, task-page.md
  ├─ B  the type door     task-type: ─▶ haipipe-task-for-<type>  ref/types.md
  └─ shared by all types  ticket · runtime.yaml · metrics.json · heavy.yaml · authoring rules
```

> ⛔ **Generated files: never modify them directly; change the code that writes them, then rerun it**
> (JL 260928; AGENTS.md rule 6). Here: a ticket a `gen_*.py` writes, a notebook, a figure, a Table
> Card, everything in a Run's `result/`.

## Who owns what around a Task

```text
level   folder            face            owner
Block   work/bNN_<topic>/ board.md        haipipe-block · haipipe-project ref/ladder.md (shape, today's rules)
Job     jNN_<job>/        jNN_<job>.md    haipipe-job (Tasks in order, emoji, ## Deliverables)
Task    tNN_<task>/       tNN_<task>.md   haipipe-task (this skill)
Run     runs/<run>/       run.yaml        haipipe-run (identity, card, role, receipt rules, prune, Workflow)
```

A Block's whole shape, today's rules included, is brought up to date by `/wb update <Block>`; this
skill is what that door reads for the Task level. Delivery belongs to the Block (`delivery/` at the
Block only; haipipe-delivery).

## A · The Task level

### The folder

```text
tNN_<task>/
├── tNN_<task>.md          the face: state · goal · close · task-type · Opening
├── scripts/               this Task's code; scripts/config/ for settings Runs share
├── runs/rNN_<run>/        one folder per Run: ticket · config · run.yaml · result/ · passes/
├── draft/                 only when the Task writes
├── notebooks/ sbatch/     generated papermill copies · a supervisor for this Task's tickets
└── workflow/ studio/      optional: plan.yaml and report.yaml · kept chat sessions
```

The contract, with what earns a Task, a Run inside a Task, the output modes, supervisors and names,
is `ref/task-folder.md`. A Block not yet moved keeps `runs/<run>.sh` beside `results/<run>/` until
`haipipe-project` `ladder.py update` moves it.

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

`goal:` and `close:` are the Task's two lines on the workflow layout's Goal tree; `haipipe-project
audit --today` reports a work Task without them. A Task that a reader studies gets the full Task
Page (`ref/task-page.md`: Opening, Content divisions, displays, the READING table), started from
`ref/task-page-template.md`; a quick worker Task keeps the header and its Opening.

### The life

```text
plan ─▶ build ─▶ run ─▶ read ─▶ close
Job item, goal/close, planned Run cards ─▶ worker, config, ticket ─▶ receipt ─▶ headline, describe
and figures Runs, reading ─▶ close: true and the Job's items tick
```

`ref/lifecycle.md` says what each step leaves on disk and who writes it. A paid, long or shared-store
Run waits for a person to press Run (AGENTS rule 2); a quick local unpaid one is run and reported.

### Commands

```text
/haipipe-task <task-folder>                  the whole life of one Task
/haipipe-task plan|build|execute|report <task-folder>   one step (fn/stage-plan.md, fn/stage-report.md)
/haipipe-task <job> | <block>                every Task under it, in path order
/haipipe-task run <task-folder> [run-name]   make or run one Run (fn/run.md)
/haipipe-task audit <task|job|block>         pair tickets, configs, receipts, Results (fn/audit.md)
/haipipe-task block <block-path|name>        a new work Block, on haipipe-block's scaffold (fn/block.md)
/haipipe-task job <type> [args…]             a new Job through its type skill
/haipipe-task insight "<topic>" [<board>]    the older name of /haipipe-insight task (fn/insight.md)
/haipipe-task feedback | digest              feedback capture and session harvest (fn/feedback.md, fn/digest.md)
```

The whole-life command runs the Workflow script `ref/task-lifecycle.workflow.js` with
`{task_folder, type, stages, autoExecute}`, once per Task at Job or Block scope, continuing after a
failure and gathering every verdict. Three agents keep the duties apart:
`haipipe-task-orchestrator-agent` coordinates, `haipipe-task-creator-agent` writes the plan, code and
report, `haipipe-task-reviewer-agent` judges them (`pass`, `warn`, `revise`, `fail`); creator and
reviewer are never the same agent.

## B · The type door

`task-type:` on the face picks the type skill; the table, the rules for choosing, the asked-or-silent
contract and the `## Type contract` block every type skill carries are `ref/types.md`.

```text
raw · description · data          haipipe-task-for-raw · -description · -data  (1_data/)
algo                              haipipe-task-for-algo                        (2_nn/)
endpoint                          haipipe-task-for-endpoint                    (3_end/)
individual                        haipipe-task-for-individual                  (4_individual/)
fit (+ GPU companions)            haipipe-task-for-fit                         (5_fit/)
eval                              haipipe-task-for-eval                        (6_eval/)
display                           haipipe-task-for-display                     (7_display/)
stata-cms · -case · -data · -reg  haipipe-task-for-stata                       (8_stata/)
agent (+ LLM engine)              haipipe-task-for-agent                       (9_agent/)
evidence                          haipipe-task-for-evidence                    (10_evidence/)
draft                             haipipe-draft (its own Runs in draft/)
labeling · -building · -scanning  haipipe-labeling
```

GPU is how a fit Task executes, not a type: `haipipe-task-for-fit` owns `haipipe-task-for-fit/_parts/gpu` and
`haipipe-task-for-fit/_parts/gpu-training` (preflight the exact GPUs, never kill an unowned process, one ticket after
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

A Block Question and its report are `haipipe-report`'s (`reports/qNN_<topic>/`, written through
`haipipe-draft`); they are not this skill's `workflow/report.yaml`. New executable evidence for a
question is an ordinary Run: reuse an exact Result first, else make a new Run. Literature goes to
`haipipe-discovery`; reading across Results goes to `haipipe-page-insight`.

## Definition of done

1. The Task's folder passes `scripts/check_task_tree.py` (shown to fail first on a broken scratch
   copy) and `haipipe-project` `ladder.py audit <block> --today`.
2. At least one ticket per affected type ran (a dry run is enough for a layout change), and its
   `result/runtime.yaml` and required Result files are there.
3. The Job's Goal view shows the Task's items with the ticks the disk supports.

Return:

```text
status:    ok | blocked | failed
summary:   what changed and what the checks proved
artifacts: exact paths made or changed
next:      one safe command or reader action
```
