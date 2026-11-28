# The type door · one `task-type:`, one type skill

A Task face says what kind of work it is in one line, `task-type: <type>`. That value picks the
skill that knows how to build and run it. hai-task owns the folder and the shared ticket body
(`ref/task-folder.md`); each type skill owns its worker, its config keys, its ticket template when
it needs its own, and its Result gate.

## The types

```text
task-type    type skill                        what one Task does                          its Runs' ticket
raw          hai-task-for-raw              extract a cohort to RawStore, or profile it  .sh (Databricks), .cmd (PHI server)
description  hai-task-for-description      one stored table's Table Card                .sh
data         hai-task-for-data             one Stage 1-4 build: Source, Record, Case,   .sh, .cmd (PHI server)
                                               AIData
algo         hai-task-for-algo             smoke-test a new algorithm class             .sh
fit          hai-task-for-fit              train a model into a ModelInstance           .sh (+ GPU companions)
eval         hai-task-for-eval             score a pinned ModelInstance on a split      .sh
individual   hai-task-for-individual       one subject's data over a time window        .sh
display      hai-task-for-display          a display-safe summary table for a Page      .sh
endpoint     hai-task-for-endpoint         package a model set into an Endpoint_Set     .sh (papermill)
agent        hai-task-for-agent            an LLM agent call or campaign                .sh (+ hai-task-for-agent/_parts/llm-engine)
evidence     hai-task-for-evidence         the values one Board Page owes               .sh
ideation     hai-ideation                  authored assessment of one Idea question     shared soft Run .md
stata-cms · stata-case · stata-data · stata-reg
             hai-task-for-stata            one stage of the CMS Medicare Stata pipeline .ps1 (Windows server)
draft        hai-draft                     a Section, report, email or page: its plan,  no ticket: the draft's
                                               sentences and evidence                       own Runs in draft/
labeling · labeling-building · labeling-scanning
             hai-labeling                  one labeling corpus (a labeling Block);      run-labeling-* (engine)
                                               its workbench is workbench-task-labeling
```

1. **GPU** is not a type: it is how a fit Task executes. `hai-task-for-fit` owns the companions
   `hai-task-for-fit/_parts/gpu` (queue, preflight, receipts) and `hai-task-for-fit/_parts/gpu-training` (checkpoint,
   resume, OOM fallbacks).
2. **A Block number never says the type** (`ref/pipeline-blocks.md` numbers stages, not types).
3. **A draft Task** follows Plan ▶ Write ▶ Evidence ▶ Display ▶ Revise ▶ Delivery in its `draft/`,
   not this file's ticket rules; every theme's workbench opens it on the base draft layout
   (`servers/workbench/workbench-task-draft/`).

## Choosing the type

An authored assessment of a research idea in an Idea Job uses `ideation`.
Load its owner's `references/assessment-task.md` for plan/build/run. That
route precedes broad words such as "evaluate" or "agent": `eval` measures a
ModelInstance and `agent` executes an LLM campaign. An idea assessment can use
multiple skills without becoming either. A separate requested prose Page
uses `draft`; new scientific computation remains a Work Task.

First match wins: the face's `task-type:`; then the Task's code (a `.do` file is Stata, an import of
`haipipe.data` is data, a call into `code/haiutils/llm_engine/` is agent); then the request's words:

```text
raw          raw · ingest · extract table · databricks pull · catalog · 0-RawDataStore
description  table card · describe table · column meanings · synth_df
data         build · source · record · case · aidata · dataset · fn build · pipeline 1-4
algo         smoke · verify algorithm · algo class · forward pass · loss class
fit          train · fit · sweep · hyperparam · epoch · pretrain · finetune
eval         eval · evaluate · score · metrics · mae · rmse · accuracy · horizon
display      figure · table · plot · paper figure · panel · ablation table
individual   subject · patient · one user · single subject · cgm trace · treatment event
agent        agent · llm · prompt · claude · gpt · tool use · campaign
endpoint     endpoint · deploy · package · serve · sagemaker · mlflow · Endpoint_Set
evidence     page values · values.yaml · what a page owes
ideation     idea assessment · novelty of an Idea · falsifiability · research-idea feasibility
stata-*      stata · do-file · .do · cms · case pipeline · reg · ols · iv · did
```

Stata words hand the whole request to `hai-task-for-stata`, which picks the stage. When nothing
resolves, ask once; in an automatic run return `status: blocked` naming the missing type.

## Asked or silent

The hard-Run fields below apply to executable work types. For `ideation`,
the type owner returns the same status/job/task/files/missing fields, a soft
Run name when commissioned (otherwise null), and authored assessment paths.
It does not create a shell Ticket, generated Result or OUTPUT_ROOT for prose
assessment. The soft Ticket freezes inputs and acceptance criteria.

Every type skill runs one body two ways, chosen by whether its inputs are complete, not by who calls:

1. **Silent**: the Run name (`rNN_<noun>_<qualifier>`), `_meta.purpose`, the Job, the Task folder and
   the type's own settings are all given. Ask nothing; use them as given.
2. **Asked**: something is missing and a person is present. Ask only for what is missing.
3. **Blocked**: something is missing and no person is present. Return `status: blocked` naming it;
   never invent a `purpose`.

`_meta.note`, `input` and `output` are recommended, never blocking. `_meta.notebook: full | thin |
off` keeps the papermill copy whole, thin (heavy compute) or not at all. Every call ends with:

```text
status:       ok | blocked | failed
job:          <absolute path of the jNN_<job>/>
task_folder:  <absolute path of the tNN_<task>/>
run_name:     <rNN_<run>>
files:        [runs/<run>/<run>.sh, runs/<run>/config.yaml or scripts/config/<run>.yaml, runs/<run>/run.yaml]
result:       $OUTPUT_ROOT/<task>/runs/<run>/result/
missing:      [<field>, …]       # when blocked
note:         <one line>
```

A creator agent reads `task_folder` for where to write `scripts/<worker>` and the face; `job` only
for shared `src/`, a Job supervisor, and the resolved output root.

## The type contract

Each type skill's `SKILL.md` carries one `## Type contract` section holding one fenced `yaml` block
with exactly these keys, so every type reads the same way and `tests/test_type_contracts.py` can
check them:

```yaml
task-type: <the value a face writes>
skill: <the type skill's name>
does: <one plain sentence>
worker: <where its code lives, and its language>
config: <where one Run's settings live: runs/<run>/config.yaml, or scripts/config/<run>.yaml in a
        Block not yet moved>
ticket: <runs/<run>/<run>.sh (or .ps1, .cmd), and the template it starts from>
result: <runs/<run>/result/, and the files that must be there before the receipt says complete>
heavy: <where its big outputs go, or none>
roles: [<the roles its Runs usually take: trial make fix check describe figures evidence publish>]
companions: [<the skills it loads or hands to>]
plan_sample: <its workflow-plan sample, relative to its folder, or none>
```

The block states the current layout only. When a type's own pages disagree with it, the pages are
fixed, never the block.

Authored soft types, including `ideation`, declare their authored receipt
paths in `result` and their Markdown Ticket in `ticket`. They do not inherit
the executable Work types' generated `result/` requirement. Their owner loads
the shared soft-Run contract and returns actual authored outcomes.
