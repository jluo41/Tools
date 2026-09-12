---
name: haipipe-task
description: >-
  Canonical Task-family door for creating, running, auditing, and closing
  Task Folders. Task Folder = Page Folder at the tNN Task level. The hierarchy
  is Project → bNN Block/Board → jNN Job/Group → tNN Task Folder/Page → rNN Run.
  Use for Task Board work, Plan → Build → Execute → Report, Run/Result
  interpretation, block or job iteration, and task-side Insight routing.
  Trigger: task, job, block, task folder, Task Board, plan, build, execute,
  report, run, audit, insight, /haipipe-task.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "1.0.0"
  last_updated: "2026-09-08"
  folder_owner: canonical
  folder_kind: task
  primary_face: task
  page_ruling: local
  outline:
    mode: grammar
    source: "ref/task-page.md"
    shape: "FLAT or NESTED; first word from {Introduction, Concept, Landscape, Data, Method, Result, Conclusion}; Introduction when present is division 1 and appears once; Concept, Landscape, Data may sit page-level; Method, Landscape and Result repeat; a residual earns its own Result-role division; Conclusion is one page-level division, always last"
---

# haipipe-task

`haipipe-task` owns one executable hierarchy and one lifecycle:

```text
Project
└── tasks/
    └── bNN_<block>/                       Block = Task Board
        ├── board.md                       board-kind: task-block
        └── jNN_<job>/                     Job = Board Group
            ├── src/                       code shared by two or more Tasks
            ├── tNN_<task>/                Task Folder = Page Folder = Board Page
            │   ├── tNN_<task>.md          reader-facing Page
            │   ├── outline/               human-facing Page record
            │   ├── workflow/              Plan/Report receipts
            │   ├── scripts/
            │   │   ├── <worker>.py
            │   │   └── config/rNN_<run>.yaml
            │   ├── runs/rNN_<run>.sh      authored Ticket
            │   ├── sbatch/                optional, serves only this Task
            │   └── studio/                optional, the Page's kept chat and draw
            ├── sbatch/                    optional, spans two or more Tasks
            ├── <task>/results/<run>/      generated Result + runtime.yaml
            └── <task>/notebooks/<run>.ipynb
```

Every directory level uses `<level><NN>_<noun>_<qualifier>` with level letters
`b`, `j`, `t`, and `r`. A full execution address is read directly from the
path, for example `b02j01t03r04`. Run is an execution identity represented by
the matching config, Ticket, Result directory, and optional notebook; it is not
an authored folder beneath the Task.

Read `ref/hierarchy.md` before acting. It is the conceptual authority.
`ref/task-structure.md` owns the concrete tree, and
`ref/authoring-conventions.md` owns the cross-engine authoring rules.

## Board mapping

```text
Block = Board  →  Job = Group  →  Task Folder = Page Folder = Page
                                      └── Run = execution record
```

Every Block contains `board.md` with `board-kind: task-block`. The disk tree
owns membership and default order. Board rendering belongs to `haipipe-board`;
this Skill owns executable identity, P-B-E-R, Run/Result pairing, and closure.

A Task Page declares `folder-kind: task`. The Task state becomes settled only
when P-B-E-R is terminal, every load-bearing Result receipt is current, and the
Task Page's `#### READING · current` gate passes. A new Run reopens every
dependent reading.

## Commands

Each verb's detailed contract lives in its cited `fn/` file.

```text
/haipipe-task plan <task-folder-path>             Plan only
/haipipe-task build <task-folder-path>            Build only
/haipipe-task execute <task-folder-path>          Execute only
/haipipe-task report <task-folder-path>           Report only

/haipipe-task <task-folder-path>                  full lifecycle
/haipipe-task <job-path>                          iterate direct Task Folders
/haipipe-task <block-path>                        iterate every Task Folder
/haipipe-task <phase> <job-or-block-path>         iterate one phase

/haipipe-task job <type> [args...]                scaffold a Job through a specialist
/haipipe-task block <block-path|name>             scaffold a Block (`fn/block.md`)
/haipipe-task run <task-folder-path> [run-name]    create/execute one Run (`fn/run.md`)
/haipipe-task audit <task|job|block-path>          inspect pairing (`fn/audit.md`)
/haipipe-task insight "<topic>" [<board>]          route an Insight item (`fn/insight.md`)
/haipipe-task feedback <...>                       feedback operations (`fn/feedback.md`)
/haipipe-task digest <...>                         session digest (`fn/digest.md`)
```

## Four phases

All lifecycle work targets one exact `tNN_<task>/` Task Folder.

```text
Plan     workflow/plan.yaml + workflow/plan-script-<worker>.yaml
Build    scripts/<worker>.py + scripts/config/<run>.yaml
         + runs/<run>.sh + CODE_REVIEW.md
Execute  $OUTPUT_ROOT/<task>/results/<run>/{runtime.yaml, metrics.json, ...}
         + $OUTPUT_ROOT/<task>/notebooks/<run>.ipynb
Report   workflow/report.yaml + workflow/report-script-<worker>.yaml
         + RUN_AUDIT.md
```

Plan and Report use the IPO schema from `haipipe-workflow`. Build changes only
authored Task files. Execute changes only generated projections. Report reads
the Plan, code review, Run receipt, and Results before making claims.

Three agents implement separation of duties:

```text
haipipe-task-orchestrator-agent  coordinates the lifecycle
haipipe-task-creator-agent       creates Plan, code, and Report artifacts
haipipe-task-reviewer-agent      evaluates intent, implementation, and evidence
```

Creator and reviewer remain separate. A reviewer returns `pass`, `warn`,
`revise`, or `fail`; `revise` and the first `warn` return specific feedback to
the creator. `fail` stops for human judgment.

## Output root

A Job chooses one of two first-class modes:

```text
self-serving      OUTPUT_ROOT = <job>/
consumer-serving  OUTPUT_ROOT = <store>/<job-path-under-tasks>/
```

Resolution order is `RESULT_STORE` from a dispatching consumer, then the Job's
`store:` declaration in `src/config-defaults.yaml`, then the Job itself. The
Task layer receives a path, not the consumer's identity. Every generated,
data-dependent artifact lands under `$OUTPUT_ROOT`; authored code, config, and
Tickets remain in the Task Folder. `CODE_REVIEW.md` stays with the Task code.

The one Page-authority exception is a PHI-safe DISPLAY unit admitted by LAND
under `outline/evidence/display/<unit>/`. Its Result envelope and receipt still
live under `$OUTPUT_ROOT/<task>/results/<run>/` and record the projection hash.

## Question and Insight routing

A question is an ordinary Run request. Reuse an exact immutable Run Result
first. When evidence is missing, enter the shallowest honest lifecycle depth
and create a new Run identity. A consumer records full Supporting Run ids and
owns any Local Run needed to produce its focal evidence item.

Literature work routes to `haipipe-discovery`. Consumer-neutral interpretation
across Results routes through `haipipe-page-insight`. An Insight Item may cite
Task Pages, Task Run Results, Discovery Pages, or prior Insight Results, but it
never executes a producing Folder invisibly.

## Task types

```text
type        specialist                         related Skill
data        haipipe-task-for-data              haipipe-data
raw         haipipe-task-for-raw               haipipe-data-raw
algo        haipipe-task-for-algo              haipipe-nn-algo
fit         haipipe-task-for-fit               haipipe-nn-tuner + instance
eval        haipipe-task-for-eval              project-local evaluation
display     haipipe-task-for-display           display family
individual  haipipe-task-for-individual        haipipe-individual
agent       haipipe-task-for-agent             haipipe-task-llm-engine
endpoint    haipipe-task-for-endpoint          haipipe-end
page        haipipe-task-for-page              one Board Page's evidence route
```

Stata execution routes wholly to `haipipe-task-for-stata`. A Block prefix does
not encode type. Infer type from explicit input, then Task code, then request
keywords. If none resolves, ask once or return `blocked` in auto mode.

## Scope resolution

Resolve by structure and enforce the prefix at the same time:

- Task Folder: direct Job child named `tNN_*`, with same-stem Page,
  `scripts/`, and `runs/`.
- Job: direct Block child named `jNN_*`, containing `src/` and one or more
  valid Task Folders.
- Block: direct `tasks/` child named `bNN_*`, containing `board.md` and one or
  more Jobs; it has no runnable lanes of its own.

For a Job, enumerate direct `tNN_*` children. For a Block, enumerate
`bNN_*/jNN_*/tNN_*`. Validate every candidate before dispatch. A container
with no valid Task Folder is malformed and returns `failed`; it is never
treated as an executable Task.

## Protocol

1. Read `ref/hierarchy.md`.
2. Parse utility verbs before lifecycle scope.
3. Resolve the exact Task Folder(s) by the structural rules above.
4. For new names, apply the stranger test: a concrete noun plus the qualifier
   that distinguishes it from siblings.
5. For lifecycle work call:

```javascript
Workflow(
  { scriptPath: "Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/task-lifecycle.workflow.js" },
  {
    task_folder: "<path-to-tNN-task-folder>",
    type: null,
    stages: ["plan", "build", "execute", "report"],
    autoExecute: false
  }
)
```

6. For Job or Block scope, call the same workflow once per resolved Task Folder
   in path order. Continue after one child fails and aggregate all verdicts.
7. After creating or renaming any Block, Job, Task, config, or Ticket, run
   `ref/check_task_tree.py` on the touched Block or `tasks/` directory.
8. Before trusting a new gate, prove it fires against a deliberately broken
   scratch copy, then run it against the target tree.

## Guardrails

- A Task is one computation, one output contract, and one code path.
- A new cohort, segment, or parameter set creates a config and Run, not a Task.
- A different output contract creates a Task; a separately submittable unit
  with its own shared code boundary creates a Job.
- Every config and Ticket share the exact `rNN_<run>` stem.
- Every Run writes `runtime.yaml` before expensive work and finalizes it only
  after its declared Result gate passes.
- A zero process exit without an evidence comparison is a smoke test.
- A configured name that does not resolve raises and names the missing entry.
- Heavy artifacts belong in `_WorkSpace/`, never `results/`.
- Do not create lifecycle artifacts at Job or Block level.
- Do not create `README.md` at Project, Block, Job, or Task roots. Use the Board
  head, Page, and `diagram/` surfaces.
- Refuse overwrites and name collisions.

## Definition of done

Run the structural checker on a broken scratch copy with `--expect-fail`, then
on the target tree with zero findings. Execute at least one representative
Ticket for each affected Task type and verify its `runtime.yaml` plus required
Result files. Render the Task Block Board and confirm that every Job becomes a
Group and every Task Folder becomes a Page.

Return:

```text
status:    ok | blocked | failed
summary:   what changed and what the gates proved
artifacts: exact paths created or modified
next:      one safe command or reader action
```
