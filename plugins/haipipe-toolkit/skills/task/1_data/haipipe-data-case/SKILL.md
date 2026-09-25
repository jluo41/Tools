---
name: haipipe-data-case
description: "Stage 3 (Case) specialist: builds/runs/reviews TriggerFn / CaseFn, inspects 3-CaseStore, loads case-layer assets, runs multi-partition in parallel (embarrassingly parallel). Called by /haipipe-data; direct invocation works stage-scoped."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.3"
  last_updated: "2026-09-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data-case
========================

Stage 3 specialist.
Owns CaseFn work and the 3-CaseStore layer.
Called by the `/haipipe-data` orchestrator; can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-case                          -> dashboard: 3-CaseStore status
/haipipe-data-case dashboard                -> same
/haipipe-data-case load                     -> load and inspect existing Case_Set
/haipipe-data-case cook                     -> run Case_Pipeline with config
/haipipe-data-case design-chef              -> create new CaseFn via builder
/haipipe-data-case design-kitchen           -> modify Case_Pipeline infrastructure
/haipipe-data-case review [file_path]       -> structural review of a Case-layer file
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
                 ../haipipe-data-aidata/
                   ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

`design-chef` reads `../haipipe-data-aidata/ref/concepts.md` because a CaseFn must produce keys/shapes that TfmFn / SplitFn can consume.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md`.
Mandatory.
Step 1: Parse args after `/haipipe-data-case`.
Step 2: Read this skill's `ref/concepts.md` for stage-3 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `design-chef`, also read `../haipipe-data-aidata/ref/concepts.md`.
Step 5: Execute, scoped to Stage 3.
Step 6: Emit the structured tail.

---

Stage Scope
------------

Owns:
  - TriggerFn / CaseFn builders in `tasks/b03_casestore/jNN_{triggerfn,casefn}_<family>/tNN_{triggerfn,casefn}_<Fn>/scripts/`; one CaseSet per raw dataset in `b03_casestore/j5N_<cohort>_v<yymmdd>_case/` (rule: `haipipe-task/ref/hierarchy.md` § Block number ranges) (legacy workspaces: `code-dev/1-PIPELINE/3-Case-WorkSpace/`)
  - Generated `code/haifn/fn_case/{fn_trigger,case_casefn}/`, or `code/haifn/fn_case/<fn_version>/{fn_trigger,case_casefn}/` when the Run config sets `fn_version:` (the same version as the dataset's SourceFn and RecordFns; the CaseSet cook Run sets it too; see `haipipe-data/ref/0-overview.md` § Fn Versions)
  - `_WorkSpace/3-CaseStore/` cases (cohort sampling)
  - `templates/config.yaml` for Case_Pipeline runs

Upstream dependency (Stage 2):
  Reads `_WorkSpace/2-RecStore/`. Empty cases usually mean upstream record
  rows didn't satisfy the trigger condition.

Hand-off contract (Stage 3 -> 4):
  Each Case must expose the fields TfmFn will tensorize. Verify against
  `../haipipe-data-aidata/ref/concepts.md`.

Feature boundary:
  In the current implementation CaseFn fulfills the conceptual FeatFn role.
  It may consume scalar or list/vector data preserved from Source through
  Record, then select/window/aggregate/encode it into `--tid`, `--wgt`, and
  `--val`. Do not rename CaseFn without an explicit migration plan.
  External fields arrive only through Source (`../haipipe-data-external/ref/
  asset-model.md` § Downstream boundaries). A CaseFn never opens ExternalStore
  and never calls `context.get_external_path`; it encodes the Source fields
  it is given. Legacy CaseFns that read `@{tag}` folders directly stay valid
  until their SourceFn moves to the lookup model, proven by an identical
  AIDataSet.

Facts, not labels (REACH PD2D, JL 260923):
  - The CaseSet holds FACTS. An outcome is an event CaseFn over ONE signal
    record: every row from the case date on as `{n_events, days, values}` in
    `<CaseFn>--val` (days 0 to 7300; `values` only when the record has a value
    column). The window starts one day early (`DistStartToPredDT: -1440`) so
    day 0 is never lost. An event CaseFn decides nothing. The label (within 1 year, 2 years, time to event) is a
    rule over those lists and lives in b10 (`/haipipe-data-aidata`), so a new
    outcome is a new label Fn, never a new CaseSet.
  - No clinical threshold here: a signal table already says present, absent
    or unclear. The TriggerFn and CaseFns combine signal records; b02 keeps
    them one RecordFn each.
  - Trigger kinds: one case per patient (first qualifying signal, prior
    outcome flagged not dropped, e.g. `ExcludedPriorDiab = 1`), or the long
    `all_visit` kind (the long df_case), one case per patient per visit day
    (`REACHEncounterDay`) with `NEncounters` and `Phase` = `before_prediab`,
    `prediab` or `after_diab` against `IndexDate` and `FirstDiabDate`.
    Nothing is dropped in either. Each is its own TriggerFn.
  - A CaseSet VERSION is a Run: `j5N_<cohort>_v<yymmdd>_case/
    t01_casestore_materialize/` has one Run per TriggerFn
    (`r01_prediabvisit`, `r02_allvisit`), never a new Task or Job. It is
    stored as `@v<case_set_version>CaseSet-<TriggerFolderName>`.
  - Record names bind the HumanFn: a CaseFn reads `h<HumanFn>.r<RecordFn>`
    (`hHmREACHPD2DPtt.rREACHDxDay.cBf90d`). A project with its own HumanFn
    cannot reuse another project's feature CaseFns as they are; it rebinds
    them under its own name (`REACHDxStatsBf90d` -> `REACHPD2DDxStatsBf90d`),
    with the HumanFn set once in `b03_casestore/src/config-defaults.yaml`
    (`human_fn`).
  - Generated, never hand-edited: `b03_casestore/src/casefn_build.py` writes
    each Fn from its Run config, and the build Run fails unless the committed
    `code/haifn/fn_case/<Fn>.py` matches byte for byte.
  - Reference: REACH-SPACE `examples/Project-REACH-PD2D/tasks/b03_casestore/`.


Partition Support
------------------

Case follows RecordSet partitions.
Each RecordSet partition (@i{i}n{n}) produces one independent CaseSet.
**Embarrassingly parallel** — each partition loads a small RecordSet (~100MB), no shared state.

**CLI:**
```bash
python -m scripts.haistepcli.case --config <config> --num-partitions 0 --num-workers 4
python -m scripts.haistepcli.case --config <config> --num-partitions 0 --partition-index 5  # retry one
```

`--num-partitions 0` = auto-discover from `2-RecStore/{name}/@i*n*`.

**Notebook parameters:** `NUM_PARTITIONS`, `PARTITION_INDEX`, `NUM_WORKERS`

**Parallelism:**
- `--num-workers 4` gives ~4x speedup (each worker: ~100MB memory)
- Safe because each partition is fully independent (no shared data)
- Notebook mode: sequential by default; set `NUM_WORKERS > 1` for parallel

**Output naming:** `3-CaseStore/{RecSet}/@i{i}n{n}/@v{ver}CaseSet-{Trigger}/`

**Discovery:** `glob.glob(LOCAL_RECORD_STORE/{name}/@i*n*)` sorts by partition index.
