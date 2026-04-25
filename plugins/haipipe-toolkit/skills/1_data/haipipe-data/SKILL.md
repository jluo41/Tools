---
name: haipipe-data
description: "Run any Stage 1-4 data pipeline work. Parses intent (stage + function) and dispatches to the right specialist (haipipe-data-source/-record/-case/-aidata). Use for SourceFn/RecordFn/CaseFn/TfmFn/SplitFn builds, pipeline runs, dashboards, reviews, or any natural-language data-pipeline question. Trigger: data pipeline, source, record, case, aidata, fn build, cook, /haipipe-data."
argument-hint: [stage] [function] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-data (orchestrator)
===================================

User-facing entry for Stages 1-4. Parses intent, dispatches to the right
specialist via `Skill()`. The user types one of:

```
/haipipe-data                       -> cross-stage dashboard
/haipipe-data <stage>               -> ref-only view of one stage
/haipipe-data <stage> <fn> [args]   -> dispatch to specialist
/haipipe-data <fn> <stage> [args]   -> same (flexible order)
/haipipe-data <fn>                  -> run <fn> with no stage scoping
/haipipe-data explain [question]    -> handled inline (cross-stage)
/haipipe-data "<natural language>"  -> infer stage + fn from keywords, dispatch
```

---

Specialists
-----------

```
haipipe-data-source     Stage 1: SourceFn, HumanFn, 1-SourceStore
haipipe-data-record     Stage 2: RecordFn, TriggerFn, 2-RecStore
haipipe-data-case       Stage 3: CaseFn, 3-CaseStore
haipipe-data-aidata     Stage 4: TfmFn, SplitFn, 4-AIDataStore
```

---

Stage Keyword Map
------------------

When parsing free-form input, infer stage from these keywords:

```
SourceFn, HumanFn, ingest, raw frame, source layer    -> source
RecordFn, TriggerFn, record, record-centered          -> record
CaseFn, case, cohort, sampling, trigger event         -> case
TfmFn, SplitFn, AIData, tensor, split, model input    -> aidata
```

Stage aliases (positional):
```
1, 1-source, source         -> source
2, 2-record, record         -> record
3, 3-case, case             -> case
4, 4-aidata, aidata         -> aidata
0, overview, 0-overview     -> umbrella inline (cross-stage explainer)
rawdata, 0-rawdata          -> source (dashboard rawdata mode)
```

---

Function Verb Map
------------------

```
build, create, design, scaffold, new          -> design-chef
modify pipeline, change pipeline, kitchen     -> design-kitchen
run, execute, cook, process                   -> cook
review, audit, check, validate, verify        -> review
load, inspect, show, view, look               -> load
status, dashboard, what's there               -> dashboard
explain, what is, why, how does               -> explain (umbrella inline)
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve (stage, function):
  - First positional matches stage alias?     -> stage = that
  - Else first positional matches verb?       -> function = that
  - Scan keyword maps for any unmatched terms.
  - If neither stage nor function resolves    -> ask user to clarify.

Step 3: Decide handling:
  - No args                                   -> CROSS-STAGE DASHBOARD (inline)
  - function = explain                        -> EXPLAIN (inline)
  - stage resolved, no function               -> dispatch to <stage> with arg "(none)"
                                                 -> specialist returns ref-only summary
  - both resolved                             -> dispatch to specialist
  - function resolved, no stage               -> ASK which stage (don't guess)

Step 4: Dispatch:
    Skill("haipipe-data-<stage>", args="<function> <remaining_args>")

Step 5: Capture the specialist's structured tail (status / summary /
        artifacts / next), present it to the user.
```

---

Cross-Stage Dashboard (no-arg case)
------------------------------------

When invoked with no arguments, fan out to every specialist's dashboard
in a single message (parallel) and concatenate their summary tails:

```
Skill("haipipe-data-source",  args="dashboard")
Skill("haipipe-data-record",  args="dashboard")
Skill("haipipe-data-case",    args="dashboard")
Skill("haipipe-data-aidata",  args="dashboard")
```

Then emit a 4-line summary (one per stage) plus an overall header that
points the user at their next likely command.

---

Explain Mode (inline)
----------------------

`/haipipe-data explain [question]` is handled inline (NOT dispatched), since
explanations often span stages.

  1. Read `ref/0-overview.md` (cross-stage explainer kept in this umbrella).
  2. If the question references a specific stage, also Read that
     specialist's `ref/concepts.md` for context.
  3. Answer the question. Cite which ref docs informed the answer.

---

Disambiguation Rules
---------------------

  - Stage unclear and no keywords match -> list 4 stage options, wait.
  - Verb unclear, stage clear -> default to `dashboard` for that stage.
  - Both clear, but extra free-form context present -> pass full context as
    trailing arg so specialist can use it.
  - Multi-stage request ("run stages 1 to 3") -> dispatch sequentially:
    source(cook) -> record(cook) -> case(cook), reporting after each.

---

Specialist Return Contract
---------------------------

Every specialist emits a tail block this orchestrator parses:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done at the stage
artifacts: [paths created, read, or modified]
next:      suggested next command
```

If `status != ok`, surface the specialist's `summary` and stop — do not
chain into the next stage automatically.

---

Files Owned by This Umbrella
-----------------------------

```
ref/0-overview.md       cross-stage architecture + cooking metaphor
fn/fn-0-dashboard.md    dashboard procedure (used by every specialist)
fn/fn-1-load.md         load procedure
fn/fn-2-cook.md         cook procedure
fn/fn-3-design-chef.md  design-chef procedure
fn/fn-4-design-kitchen.md   design-kitchen procedure
fn/fn-explain.md        explain procedure (used inline by this skill)
fn/fn-review.md         review procedure
```

These fn docs are SHARED across specialists. Each specialist reads its own
`ref/concepts.md` plus the relevant umbrella fn doc.
