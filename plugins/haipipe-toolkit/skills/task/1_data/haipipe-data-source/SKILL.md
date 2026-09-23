---
name: haipipe-data-source
description: "Stage 1 (Source) specialist: builds/runs/reviews SourceFn, maps Raw Data plus pinned ExternalStore assets into stable ProcessName-to-ProcessDF tables, and inspects 1-SourceStore. Called by /haipipe-data; direct invocation works stage-scoped."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.1"
  last_updated: "2026-09-23"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data-source
==========================

Stage 1 specialist.
Owns all SourceFn work and the 1-SourceStore layer of the pipeline.
Called by the `/haipipe-data` orchestrator; can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-source                        -> dashboard: 1-SourceStore status
/haipipe-data-source dashboard              -> same
/haipipe-data-source dashboard rawdata      -> 0-RawDataStore inventory (no manifest check)
/haipipe-data-source load                   -> load and inspect existing Source_Set
/haipipe-data-source cook                   -> run Source_Pipeline with config
/haipipe-data-source design-chef            -> create new SourceFn via builder (HumanFn routes to haipipe-data-record)
/haipipe-data-source design-kitchen         -> modify Source_Pipeline infrastructure
/haipipe-data-source review [file_path]     -> structural review of a Source-layer file
```

---

Dispatch Table
--------------

After parsing, read these files:

```
Invocation             This skill's ref            Umbrella's fn doc
---------------------- --------------------------- ---------------------------------------------------
dashboard              ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
dashboard rawdata      ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
load                   ref/concepts.md             ../haipipe-data/fn/fn-1-load.md
cook                   ref/concepts.md             ../haipipe-data/fn/fn-2-cook.md
design-chef            ref/concepts.md +
                       ../haipipe-data-record/
                         ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen         ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review                 ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)            ref/concepts.md             (ref-only mode)
```

Why `design-chef` reads the next stage's ref: a SourceFn contract is satisfied by what RecordFn downstream expects.
You need both ref docs to design correctly.

---

Step-by-Step Protocol
----------------------

Step 0: Read the cross-stage overview FIRST (it has the 6-layer map and
        cooking metaphor): `../haipipe-data/ref/0-overview.md`. Mandatory.

Step 1: Parse args after `/haipipe-data-source`.
Extract:
          function  in { dashboard, load, cook, design-chef, design-kitchen, review, (none) }
          extras    e.g. `rawdata` for dashboard, file_path for review
        If no args -> dashboard.
        If the ask is concept-level only -> read `ref/concepts.md`, summarize, stop.

Step 2: Read THIS skill's `ref/concepts.md` for stage-1 specifics.

Step 3: Read the umbrella fn doc per the dispatch table above.

Step 4: For `design-chef`, also read `../haipipe-data-record/ref/concepts.md`
        so you know the downstream contract.

Step 5: Execute the procedure described by the fn doc, scoped to Stage 1.

Step 6: Emit the structured tail (orchestrator parses this):

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done at Stage 1
artifacts: [paths created, read, or modified]
next:      suggested next command (often a /haipipe-data-record action)
```

---

D-prefix dictionary tables
---------------------------

SourceFn defines D-prefix lookup tables (`DRGCode`, `DLabItems`, `DIcdDiagnoses`, `DIcdProcedures`, `DHcpcs`, `DItems`) as part of `ProcName_List`.
Key rules:

- These are **full-database dictionary tables**, NOT patient-specific data.
- They flow through Source -> Record pipeline but are **NEVER read by any CaseFn**.
- `extract_example_from_source` SKIPS D-prefix tables (they bloat examples by 37x).
- `Src2InputFn` SKIPS D-prefix tables (they bloat payloads beyond the
  Databricks 33 MB limit).
- If a future CaseFn needs D-prefix data, load it from the endpoint's
  `external/` dir, not from the per-request payload.


Stage Scope
------------

Owns:
  - SourceFn builders in `tasks/b01_sourcestore/j5N_<cohort>_v<yymmdd>_source/t01_sourcefn_develop_and_use/scripts/`; ProcName contracts in `b01_sourcestore/j01_procdf_<topic>/tNN_procdf_<ProcName>/` (rule: `haipipe-task/ref/hierarchy.md` § Block number ranges) (legacy workspaces: `code-dev/1-PIPELINE/1-Source-WorkSpace/`)
  - Generated `code/haifn/fn_source/`
  - `_WorkSpace/1-SourceStore/` typed frames
  - `templates/config.yaml` for Source_Pipeline runs

Does not own:
  - 0-RawDataStore content (that's source data, owned by the dataset)
  - 2-RecStore (`/haipipe-data-record`) and beyond

Hand-off contract (Stage 1 -> 2):
  Each Source frame must carry the keys RecordFn needs to bucket rows into
  records. Confirm by reading `../haipipe-data-record/ref/concepts.md` before
  finalizing any SourceFn.

External-data contract (model: `../haipipe-data-external/ref/asset-model.md`):
  STATUS: `code/haipipe/external_base/` is NOT built yet. Check
  (`ls code/haipipe/external_base`) before writing a lookup block; if absent,
  use the v4 attach helpers (`<field>_ids`, `<field>_matched`,
  `external_release`) against a pinned legacy `@{tag}` release. The rules
  below are the target and apply once it exists.
  SourceFn is the only place external fields enter the pipeline (ZIP, NPI,
  NDC, NCPDP, engagement, feature-store, third-party assets).
  - One explicit lookup block per asset, every field assigned by name:
    `lock.asset('npi', env=env).lookup(keys=..., obs_dt=df['DT'], fields=[...])`
    then `df['npi_specialty'] = f['Specialty']`. No generic attach loop.
  - `obs_dt` is each row's time; temporal assets attach only to tables with a
    row time, and a one-row-per-patient table uses the first observation time.
  - Versions come from a lock (`ExternalStore/_locks/<LockName>.yaml`) named by
    the builder; every new column is listed in `ProcName_to_columns`.
  - Put the blocks in one plain `enrich_<table>()` per table so Input2SrcFn
    reuses them with `env='serve'`, `obs_dt='now'`.
  - Write `external-dependency.json` beside the SourceSet (lock, versions,
    provider, match rate, leak-dropped count).
  - Emit scalar, list, or fixed-order vector fields as stable data
    representations; declare dtype, ordering, and missing behavior.
  - Training reads frozen local versions only. No live API or feature-store
    call inside a training SourceFn; freeze the pull into ExternalStore first
    (`/haipipe-data-external freeze`).

Contract-generated SourceFn (REACH PD2D, JL 260923):
  - With written ProcName contracts (b01 topic Jobs), the SourceFn is
    GENERATED from them instead of hand-editing a seed builder; the test is
    the build Run's committed-file check plus a selftest, not `RUN_TEST`.
    Name it `<Family>V<yymmdd>` (`REACHPD2DV260922`).
  - Do not read a huge store back: `Source_Pipeline.run(load_tables=[])`
    writes the tables and returns without loading them (default None = load
    all; `code/haipipe/source_base/source_pipeline.py`).
  - Open question, not settled: PD2D's shared tables (Encounter, Dx, Social,
    Questionnaire) carry more columns than ADHD's. That breaks MUST rule 3
    below until JL rules on supersets.
