---
name: haipipe-data-record
description: "Stage 2 (Record) specialist: builds/runs/reviews HumanFn / RecordFn, inspects 2-RecStore, loads record-layer assets, supports multi-partition via patient_ids predicate pushdown. Called by /haipipe-data; direct invocation works stage-scoped."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.1"
  last_updated: "2026-09-24"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data-record
==========================

Stage 2 specialist.
Owns all HumanFn / RecordFn work and the 2-RecStore layer.
Called by the `/haipipe-data` orchestrator; can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-record                        -> dashboard: 2-RecStore status
/haipipe-data-record dashboard              -> same
/haipipe-data-record load                   -> load and inspect existing Record_Set
/haipipe-data-record cook                   -> run Record_Pipeline with config
/haipipe-data-record design-chef            -> create new HumanFn / RecordFn via builder
/haipipe-data-record design-kitchen         -> modify Record_Pipeline infrastructure
/haipipe-data-record review [file_path]     -> structural review of a Record-layer file
```

---

Dispatch Table
--------------

```
Invocation       This skill's ref            Umbrella's fn doc
---------------- --------------------------- ---------------------------------------------------
dashboard        ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
load             ref/concepts.md             ../haipipe-data/fn/fn-1-load.md
cook             ref/concepts.md             ../haipipe-data/fn/fn-2-cook.md
design-chef      ref/concepts.md +
                 ../haipipe-data-case/
                   ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

`design-chef` reads `../haipipe-data-case/ref/concepts.md` because a RecordFn's output schema must satisfy what CaseFn expects downstream.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md` for cross-stage context.
Mandatory.
Step 1: Parse args after `/haipipe-data-record`.
Same vocabulary as the source
        specialist — see its dispatch table.
Step 2: Read this skill's `ref/concepts.md` for stage-2 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `design-chef`, also read `../haipipe-data-case/ref/concepts.md`.
Step 5: Execute, scoped to Stage 2.
Step 6: Emit the structured tail (`status / summary / artifacts / next`).

---

Stage Scope
------------

Owns:
  - HumanFn / RecordFn builders in `tasks/b02_recordstore/j01_recordfn_<topic>/tNN_{humanfn,recordfn}_<Fn>/scripts/` (same topic number as `b01`); the RecordSet is cooked in `b02_recordstore/j5N_<cohort>_v<yymmdd>_record/` (rule: `haipipe-task/ref/hierarchy.md` § Block number ranges) (legacy workspaces: `code-dev/1-PIPELINE/2-Record-WorkSpace/`)
  - Generated `code/haifn/fn_record/{human,record}/`, or `code/haifn/fn_record/<fn_version>/{human,record}/` when the Run config sets `fn_version:` (the same version as the dataset's SourceFn; see `haipipe-data/ref/0-overview.md` § Fn Versions)
  - `_WorkSpace/2-RecStore/` records
  - `templates/config.yaml` for Record_Pipeline runs

Upstream dependency (Stage 1):
  Reads `_WorkSpace/1-SourceStore/`. If a RecordFn is empty/wrong, root cause
  is often a Source-layer issue — escalate to `/haipipe-data-source review`.

External-data boundary:
  RecordFn consumes and preserves external scalar/list/vector fields already
  attached by SourceFn. It does not independently reopen ExternalStore or
  rebuild those representations. For time-varying engagement data, align using
  `snapshot_as_of`/window bounds and reject future information.

Hand-off contract (Stage 2 -> 3):
  Each Record's columns and time grid must match the keys CaseFn samples on.
  Verify against `../haipipe-data-case/ref/concepts.md` before locking schema.

Record rules (REACH PD2D, JL 260923):
  - One ProcName per RecordFn. The framework keeps only patients present in
    EVERY RawName a RecordFn lists and joins them on patient, so two tables
    in one RecordFn silently drop patients and multiply rows. Combining is
    b03's job.
  - Each project owns its HumanFn (`HmREACHPD2DPtt`): roster = one ProcName,
    and its `Excluded_RawNameList` is generated from the b01 contracts, so a
    new ProcName never changes who counts as a patient.
  - An event RecordFn keeps a date window (`date_min` in
    `b02_recordstore/src/config-defaults.yaml`, up to now): out-of-range
    dates such as 1900 are dropped and counted, not passed through.
  - One Run builds the WHOLE RecordSet (every RecordFn under `HumanRecords`)
    and counts it into `records.json`; the per-Fn Tasks only regenerate and
    check code, they touch no data.
  - Memory on big stores: `RecordArgs.load_read_tables_only: true` loads just
    the ProcNames some RecordFn reads (opt-in, in
    `code/haiutils/haistep/record_utils.py`).


Partition Support
------------------

Record supports multi-partition processing for large datasets.
Each partition processes a subset of patients, reducing peak memory.

**CLI:**
```bash
python -m scripts.haistepcli.record --config <config> --num-partitions 20 --use-cache
python -m scripts.haistepcli.record --config <config> --num-partitions 20 --partition-index 5  # retry one
```

**Notebook parameter:** `NUM_PARTITIONS` in the `# %% [parameters]` cell.

**How it works:**
- Reads `Ptt.parquet` (tiny) to get all patient IDs
- Computes the i/n slice for this partition
- Loads SourceSet with `patient_ids` predicate pushdown (pyarrow filters)
- Peak memory: ~30GB per partition vs 120GB+ full load (MIMIC-IV scale)
- Sequential recommended: each partition reads SourceSet from disk (I/O heavy)

**Output naming:** `2-RecStore/{name}_v{N}RecSet/@i{i}n{n}/` (1-based)

**Config:**
```yaml
RecordArgs:
  partition_number: 20    # number of partitions
  use_cache: true         # skip existing partitions on re-run
```
