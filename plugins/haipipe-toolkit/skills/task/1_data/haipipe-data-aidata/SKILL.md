---
name: haipipe-data-aidata
description: "Stage 4 (AIData) specialist. Builds, runs, and reviews TfmFn / SplitFn; inspects 4-AIDataStore; loads AIData-layer assets and tensors. Supports multi-partition CaseSet merge via streaming HF Dataset. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work."
argument-hint: "[function] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.3.0"
  last_updated: "2026-07-05"
  summary: "Stage 4 (AIData) specialist with multi-partition CaseSet merge."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data-aidata
==========================

Stage 4 specialist. Owns TfmFn / SplitFn work and the 4-AIDataStore layer
(model-ready tensors and splits). Called by the `/haipipe-data` orchestrator;
can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-aidata                        -> dashboard: 4-AIDataStore status
/haipipe-data-aidata dashboard              -> same
/haipipe-data-aidata load                   -> load and inspect existing AIData_Set
/haipipe-data-aidata cook                   -> run AIData_Pipeline with config
/haipipe-data-aidata design-chef            -> create new TfmFn / SplitFn via builder
/haipipe-data-aidata design-kitchen         -> modify AIData_Pipeline infrastructure
/haipipe-data-aidata review [file_path]     -> structural review of an AIData-layer file
```

Notebook / Databricks run: use `code/scripts/haistepnb/a4_aidata_nb.py`
as the template. Supports multi-partition CaseSet discovery via
`NUM_PARTITIONS` parameter. See the ★ Notebook Templates section in the
`haipipe-data` umbrella SKILL.

---

Dispatch Table
--------------

```
Invocation       This skill's ref            Umbrella's fn doc
---------------- --------------------------- ---------------------------------------------------
dashboard        ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
load             ref/concepts.md             ../haipipe-data/fn/fn-1-load.md
cook             ref/concepts.md             ../haipipe-data/fn/fn-2-cook.md
design-chef      ref/concepts.md             ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

Stage 4 is the terminal data stage — `design-chef` does NOT need a downstream
ref because the next stage (`/haipipe-nn`) consumes whatever AIData produces.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md`. Mandatory.
Step 1: Parse args after `/haipipe-data-aidata`.
Step 2: Read this skill's `ref/concepts.md` for stage-4 specifics.
Step 3: Read the umbrella fn doc.
Step 4: Execute, scoped to Stage 4.
Step 5: Emit the structured tail.

---

Stage Scope
------------

Owns:
  - TfmFn / SplitFn builders in the project's `NN_aidata_fn_develop_<cohort>/` task folder (legacy workspaces: `code-dev/1-PIPELINE/4-AIData-WorkSpace/`)
  - Generated `code/haifn/fn_aidata/`
  - `_WorkSpace/4-AIDataStore/` tensors and split definitions
  - `templates/config.yaml` for AIData_Pipeline runs

Upstream dependency (Stage 3):
  Reads `_WorkSpace/3-CaseStore/`. Tensorization issues usually trace back to
  inconsistent CaseFn output schemas — escalate to `/haipipe-data-case review`.

Hand-off contract (Stage 4 -> 5):
  AIData_Set is the input contract for `/haipipe-nn`. Splits, tensor shapes,
  and target column conventions must match what the hainn algorithm
  classes expect (layout is workspace-dependent; see /haipipe-nn).


Multi-partition Mode
---------------------

When upstream RecordSet is partitioned (@i{i}n{n}), AIData auto-discovers
all CaseSet partitions and merges them into a single AIDataSet.

**CLI:**
```bash
python -m scripts.haistep.aidata --config <config>
python -m scripts.haistep.aidata --config <config> --use-cache  # skip if exists
```

**Config (multi-partition mode):**
```yaml
record_set_name: "mimiciv-3.1_v3RecSet"   # triggers partition discovery
CaseArgs:
  case_set_version: 0
  Case_Args:
    - TriggerName: 'MimicAdmissionEntry'
      TriggerArgs: { TriggerFolderName: "MimicAdmissionEntry" }
aidata_name: "MimicMortality"
aidata_version: "v0001"
InputArgs: { ... }
```

**Config (single CaseSet mode — backward compatible):**
```yaml
case_set_name: "mimiciv-3.1_v3RecSet/@v0CaseSet-MimicAdmissionEntry"
```

**How it works:**
- Globs `LOCAL_CASE_STORE/{RecSet}/@i*n*/@v{ver}CaseSet-{Trigger}/`
- Loads all non-empty CaseSets (skips empty partitions)
- Passes `case_set_list=[...]` to `AIData_Pipeline.run()`
- Streaming HF Dataset conversion (memory-efficient, no pandas concat)
- Output: `4-AIDataStore/{name}/@{version}/`

---

Mandatory: describe the datapoint with selection criteria
----------------------------------------------------------

For ANY AIData (new build OR review of an existing one), the specialist
MUST produce a written description of what a single row in the dataset
represents, including ALL the following pieces. Vague descriptions like
"clicks dataset" or "patient features" are not acceptable.

Required elements (blank template at the end of this file; full worked instance: `ref/worked-example.md`):

  1. EXPERIMENTAL / COLLECTION CONTEXT
     - What experiment / data source produced the underlying records?
     - Is treatment assignment randomized? If so, what is π(T|X)?
     - What identifies the subject (patient_id, session_id, ...)?
     - What identifies the unit of observation (one invitation? one visit?)?

  2. SELECTION FILTERS — be VERY explicit (this is where bugs hide)
     Every Rule in `SplitArgs.Split_to_Selection` must be NAMED and
     JUSTIFIED. The cohort that survives all filters IS the dataset.
     For each filter list:
       - The filter column
       - The operator + value
       - Why this filter is applied (one sentence)
     If a filter is conceptually "the cohort we care about" (e.g.
     FU-was-delivered, opted-in patients only), call that out explicitly.

     Common selection bugs to flag during review:
       - Filtering on an OUTCOME column or proxy (e.g., dropping clicked==1
         when label is clicked_follow_up_7d) → selection-on-outcome → bias
       - Filtering on a SIDE EFFECT of treatment (e.g., dropping cases where
         the action was changed mid-flight) → biases π(T|X) estimates
       - Missing-data filters that correlate with the label

     Also list "INTENTIONALLY NOT FILTERED ON" columns — anything that
     could have been filtered but was deliberately left in, with the reason.

  3. FEATURES (X) — list every feature group with its source column
     For each CaseFn in `InputArgs.input_casefn_list`:
       - Source DfXyz column in the upstream RecordSet
       - Cardinality / vocab size after binning
       - Whether it's HISTORICAL (pre-observation) or contemporaneous
       - Whether it could carry TEMPORAL LEAK relative to the label

  4. TREATMENT (T) — how it enters the model
     - What's the treatment / action column (e.g., experiment_config)?
     - K = number of arms; list them or summarize the encoding
     - For S-Learner-style models: which CaseFn slot contains the treatment
       one-hot (e.g., InvCrntTimeFixedLen for FT_HH_MM); this slot is
       what gets re-set during counterfactual inference

  5. LABEL (Y) — exact derivation
     - Source column (e.g., clicked_follow_up_7d)
     - Definition in words ("clicked the FU SMS within 7 calendar days of
       follow_up_deliver_on_date")
     - Window boundary check (verify click-timestamps fall in named window)
     - Empirical class-balance on test

  6. SPLIT POLICY
     - SplitMethod (RandomByStratum / temporal / patient-block / etc.)
     - Stratification columns
     - Per-arm test counts (uniform-random verification for RCTs)
     - Train / test sizes + label-positive rate per split

  7. ONE WORKED EXAMPLE ROW
     Show one real row's metadata + treatment + label, so the reader can
     verify by-hand what the model sees.


Worked example — see ref/worked-example.md
-------------------------------------------

A full "good" instance of this contract lives in `ref/worked-example.md`:
an SMS follow-up send-time RCT with 20 uniform arms, 12 CaseFn feature
groups (one of them THE TREATMENT slot, S-Learner pattern), a 1,995-dim
sparse X, a binary 7-day-click label, and a RandomByStratum 80/20 split.
It fills in every required element above, including named selection
filters with reasons and an intentionally-NOT-filtered-on column (a
correlated-outcome trap). Read it before writing your first datapoint
description.


Template — drop in `examples/{project}/tasks/{task}/diagram/datapoint.txt`
-------------------------------------------------------------------------

   ─── DATAPOINT DESCRIPTION ───────────────────────────────────────
   Dataset:           {AIData name + version}
   Experiment/source: {experiment_name + source table}
   Subject ID:        {patient_id_encoded / session_id / ...}
   Unit of obs.:      {one invitation? one visit? one Rx fill?}

   Treatment T:
     Column:                {e.g. experiment_config}
     Encoding slot in X:    {e.g. InvCrntTimeFixedLen / dedicated col}
     K arms:                {list or summarize}
     Randomization:         π(T|X) = ... {uniform / observed / propensity-est}

   Selection filters (Split_to_Selection):
     1. {column == value}    — {one-sentence reason}
     2. {column > value}     — {reason}
     ...
   Intentionally NOT filtered on:
     - {column} — {reason it's deliberately kept}

   Features X (CaseFn groups, each with source DfXyz column):
     - {CaseFn name}  ←  {source column}  —  {historical? leak risk?}
     ...
     Total vocab dim = ...     Non-zero per row = ...

   Label Y:
     Column:        {label_column}
     Definition:    {one-sentence description in words}
     Window:        {if temporal, [start, end]}
     Pos rate (test): {value}

   Split:
     Method:        {SplitMethod}
     Stratify cols: [...]
     Seed:          {seed}
     Sizes:         train {N} / test {N}
     Per-arm test counts: {range or list}

   Worked example row (test idx 0):
     {dump the key fields and their values}
   ─────────────────────────────────────────────────────────────────
