---
name: haipipe-data
description: "Run any Stage 1-4 data pipeline work: parses intent (stage + function) and dispatches to the right specialist (source/record/case/aidata, plus raw/external/remote). Use for SourceFn/RecordFn/CaseFn/TfmFn/SplitFn builds, runs, dashboards, reviews, or any data-pipeline question. Trigger: data pipeline, source, record, case, aidata, fn build, cook, /haipipe-data."
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "0.3.4"
  last_updated: "2026-09-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data (orchestrator)
===================================

User-facing entry for Stages 1-4.
Parses intent, dispatches to the right specialist via `Skill()`.
The user types one of:

```
/haipipe-data                       -> cross-stage dashboard
/haipipe-data <stage>               -> ref-only view of one stage
/haipipe-data <stage> <fn> [args]   -> dispatch to specialist
/haipipe-data <fn> <stage> [args]   -> same (flexible order)
/haipipe-data <fn>                  -> run <fn> with no stage scoping
/haipipe-data explain [question]    -> handled inline (cross-stage)
/haipipe-data space-check [--root P] -> is this SPACE up to date? (inline, read-only)
/haipipe-data "<natural language>"  -> infer stage + fn from keywords, dispatch
```

---

Specialists
-----------

```
haipipe-data-raw        Stage 0' (raw cohort): single-data-point timeline, 0-RawDataStore
haipipe-data-source     Stage 1: SourceFn, 1-SourceStore
haipipe-data-record     Stage 2: HumanFn, RecordFn, 2-RecStore
haipipe-data-case       Stage 3: TriggerFn, CaseFn, 3-CaseStore
haipipe-data-aidata     Stage 4: TfmFn, SplitFn, 4-AIDataStore
haipipe-data-external   External assets (ZIP/NPI/NDC/NCPDP/engagement, feature store, APIs): contract, build/freeze/lock/parity, lookup preview, ExternalStore
haipipe-data-remote     Remote storage sync (rclone/GDrive): status/pull/push, all stores
```

---

★ Notebook Templates (Databricks / papermill) ── code/scripts/haistepnb/
--------------------------------------------------------------------------

Per-stage parameterized notebooks.
Each is a cell-based `.py` that converts to `.ipynb` and runs three ways: **Databricks** (widgets), **papermill** (`-p CONFIG ...`), and plain `python`.

```
code/scripts/haistepnb/
  a1_source_nb.py   Stage A1 — no partitions
  a2_record_nb.py   Stage A2 — multi-partition (NUM_PARTITIONS, PARTITION_INDEX)
  a3_case_nb.py     Stage A3 — multi-partition + parallel (NUM_WORKERS)
  a4_aidata_nb.py   Stage A4 — auto-discovers CaseSet partitions
  b_model_nb.py     Stage B  — model training (+ ExampleConfig)
  c_endpoint_nb.py  Stage C  — endpoint packaging (+ payload.json)
```

**Partition parameters** (Stage 2-4):
```python
NUM_PARTITIONS = 0      # 0 = use config / auto-discover; >0 = override
PARTITION_INDEX = ""    # "" = all; int = run one partition (1-based)
NUM_WORKERS    = 1      # >1 = parallel (Stage 3 Case only)
```

Recipe — create a job instance:

```
1. cp code/scripts/haistepnb/<N>_<stage>_nb.py  <task>/scripts/<worker>.py
2. set the CONFIG default to <task>/scripts/config/rNN_<run>.yaml
3. update the docstring with project-specific info
4. bash <task>/runs/rNN_<run>.sh
```

The `.py` is source of truth.
The `.ipynb` is auto-generated at runtime by `convert_to_notebooks.py` — it is intermediate output, not source.

In a PHI SPACE (REACH) none of this applies: no `.ipynb` is ever made. Every
Run is a `.cmd` Databricks ticket running the Task's one entry
`scripts/run_<task>.py` inline (see `haipipe-task-for-data` § SourceFn Block
pattern). The Fns of b01 to b03 and b10 are generated from Run configs; each stage
skill names its generator. Topic Jobs share a generator through the Block's
`src/`: `code/haiutils/haistep/task_entry.py` merges the Block's
`src/config-defaults.yaml` under the Job's own and puts the Block's `src/`
on `sys.path`.

CLI alternative (supports `--num-workers` for parallel execution):
```
python -m scripts.haistepcli.record --config <config> --num-partitions 20 --use-cache
python code/scripts/haistepcli/case.py   --config <config> --num-partitions 0 --num-workers 4
python code/scripts/haistepcli/aidata.py --config <config>
```

Legacy examples may use pre-BJTR paths; new work uses
`tasks/bNN_<block>/jNN_<job>/tNN_<task>/`: Blocks `b00` raw to `b03` case (per dataset) and `b10` aidata (per question),
topic Jobs `j01`-`j49` for Fns, dataset Jobs `j51`-`j99` (see
`haipipe-data/ref/0-overview.md` § Current Builder Structure).

Source, Record and Case Fns may share one version folder,
`code/haifn/fn_<stage>/<fn_version>/`, picked by the Run config's
`fn_version:`. Every b01-b03 Run of one dataset Job carries the same one; a
changed `ProcName_to_ProcDf` shape means a new version for all three stages.
Without `fn_version:` the flat folders are used. Rules and the builder
pattern: `haipipe-data/ref/0-overview.md` § Fn Versions. What another SPACE
does to follow a change like this: `haipipe-data/ref/migration.md`; whether a
SPACE is behind: `/haipipe-data space-check`.
  - `02_record_mimiciv/2_record_mimiciv31.py` (from `a2_record_nb.py`, 80 partitions)
  - `03_case_mimiciv_mortality/3_case_mimiciv31_mortality.py` (from `a3_case_nb.py`, auto-discover)

---

Stage Keyword Map
------------------

When parsing free-form input, infer stage from these keywords:

```
raw, RawStore, raw cohort, lifecycle, data point      -> raw
visit timeline, fog of war, single data point         -> raw
SourceFn, HumanFn, ingest, raw frame, source layer    -> source
RecordFn, TriggerFn, record, record-centered          -> record
CaseFn, case, cohort, sampling, trigger event         -> case
TfmFn, SplitFn, AIData, tensor, split, model input    -> aidata
external, NDC, NPI, reference data, join external     -> external
asset, asset.yaml, lock, feature store, vendor API    -> external
obs_dt, ValidFromDT, snapshot version, backfill       -> external
remote, rclone, gdrive, sync, pull, push              -> remote
```

Stage aliases (positional):
```
0-raw, raw, 0-rawstore, rawstore -> raw
1, 1-source, source         -> source
2, 2-record, record         -> record
3, 3-case, case             -> case
4, 4-aidata, aidata         -> aidata
0, overview, 0-overview     -> umbrella inline (cross-stage explainer)
rawdata, 0-rawdata          -> raw dashboard Panel 0 (raw store scan; see fn/fn-0-dashboard.md)
external                    -> external
remote                      -> remote
```

---

Function Verb Map
------------------

```
build, create, design, scaffold, new          -> design-chef
modify pipeline, change pipeline, kitchen     -> design-kitchen
run, execute, cook, process                   -> cook
notebook, nb, papermill, databricks notebook   -> notebook-wrapper (see ★ section; code/scripts/haistepnb/ — workspace-dependent, absent in some repos)
review, audit, check, validate, verify        -> review   (needs a path; bare "check" -> space-check)
space-check, space check, up to date, behind,
  follow other SPACE, what to update          -> space-check (umbrella inline)
load, inspect, show, view, look               -> load
status, dashboard, what's there               -> dashboard
explain, what is, why, how does               -> explain (umbrella inline)
understand, frame, lifecycle, walk through    -> understand (raw-only)
hand off, handoff, downstream contract        -> hand-off (raw-only)
freeze, snapshot a pull, freeze feature store -> freeze   (external-only)
lock, pin versions, lock file                 -> lock     (external-only)
parity, frozen vs live                        -> parity   (external-only)
join, preview join, lookup preview            -> join     (external-only)
refresh, rebuild stale                        -> refresh  (external-only)
```

An external-only verb with no stage resolves to `external` without asking.

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
  - function = space-check                    -> SPACE CHECK (inline, fn/fn-space-check.md)
  - stage resolved, no function               -> dispatch to <stage> with arg "(none)"
                                                 -> specialist returns ref-only summary
  - both resolved                             -> dispatch to specialist
  - function resolved, no stage               -> ASK which stage (don't guess),
                                                 except external-only verbs -> external

Step 4: Dispatch:
    Skill("haipipe-data-<stage>", args="<function> <remaining_args>")

Step 5: Capture the specialist's structured tail (status / summary /
        artifacts / next), present it to the user.
```

---

Cross-Stage Dashboard (no-arg case)
------------------------------------

When invoked with no arguments, first print the SPACE status line, then fan out to every specialist's dashboard in a single message (parallel) and concatenate their summary tails:

```bash
python3 <this skill's dir>/cli/space_check.py --brief    # one line, local, read-only
```

Put that line above the stage summaries. If it is not `OK`, the header's
next-command pointer is `/haipipe-data space-check`.


```
Skill("haipipe-data-raw",     args="dashboard")
Skill("haipipe-data-source",  args="dashboard")
Skill("haipipe-data-record",  args="dashboard")
Skill("haipipe-data-case",    args="dashboard")
Skill("haipipe-data-aidata",  args="dashboard")
```

Then emit a 5-line summary (one per stage) plus an overall header that points the user at their next likely command.

DELIBERATE EXCLUSION: external and remote are NOT fanned into the dashboard — they are sideways/transport specialists, not pipeline stages, and the remote probe needs network round-trips that would slow the default no-arg path.
Inspect them explicitly: `/haipipe-data external` / `/haipipe-data remote`.

---

Explain Mode (inline)
----------------------

`/haipipe-data explain [question]` is handled inline (NOT dispatched), since explanations often span stages.

  1. Read `ref/0-overview.md` (cross-stage explainer kept in this umbrella).
  2. If the question references a specific stage, also Read that
     specialist's `ref/concepts.md` for context.
  3. Answer the question. Cite which ref docs informed the answer.

Cross-stage ownership boundary:

```
ExternalStore  acquires, snapshots, versions, and documents reusable data
SourceFn       Raw + pinned ExternalStore -> stable ProcessName-to-ProcessDF
RecordFn       aligns entity/time and enforces point-in-time validity
CaseFn         applies feature selection/window/aggregation/encoding
AIData         assembles the final model-ready vector and splits
```

Source list/vector fields are allowed when they are stable data representations;
they are not the final model vector. Training SourceFn and serving Input2SrcFn
must reproduce the same Source contract for the same raw input and external
release.

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

If `status != ok`, surface the specialist's `summary` and stop — do not chain into the next stage automatically.

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
fn/fn-space-check.md    SPACE up-to-date check (used inline by this skill)
cli/space_check.py      the check itself (stdlib, read-only; --brief for the dashboard)
ref/migration.md        what another SPACE does to follow a change
```

These fn docs are SHARED across specialists.
Each specialist reads its own `ref/concepts.md` plus the relevant umbrella fn doc.
