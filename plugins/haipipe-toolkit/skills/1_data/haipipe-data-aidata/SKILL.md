---
name: haipipe-data-aidata
description: "Stage 4 (AIData) specialist. Builds, runs, and reviews TfmFn / SplitFn; inspects 4-AIDataStore; loads AIData-layer assets and tensors. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry."
argument-hint: "[function] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Stage 4 (AIData) specialist."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
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

Notebook / Databricks run: to run Stage 4 (or full 1-4) as a parameterized
Databricks/papermill notebook, use `code/scripts/haistepnb/4_aidata_nb.py`
(or `0_data_nb.py` for 1-4) — see the ★ Notebook Wrappers section in the
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
  - TfmFn / SplitFn builders under `code-dev/1-PIPELINE/4-AIData-WorkSpace/`
  - Generated `code/haifn/fn_aidata/`
  - `_WorkSpace/4-AIDataStore/` tensors and split definitions
  - `templates/config.yaml` for AIData_Pipeline runs

Upstream dependency (Stage 3):
  Reads `_WorkSpace/3-CaseStore/`. Tensorization issues usually trace back to
  inconsistent CaseFn output schemas — escalate to `/haipipe-data-case review`.

Hand-off contract (Stage 4 -> 5):
  AIData_Set is the input contract for `/haipipe-nn`. Splits, tensor shapes,
  and target column conventions must match what algorithms in
  `code/hainn/algo/` expect.

---

Mandatory: describe the datapoint with selection criteria
----------------------------------------------------------

For ANY AIData (new build OR review of an existing one), the specialist
MUST produce a written description of what a single row in the dataset
represents, including ALL the following pieces. Vague descriptions like
"clicks dataset" or "patient features" are not acceptable.

Required elements (use the OptTime template below as a model):

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


Worked example — OptTime v2 fu7d (the template's canonical "good" instance)
---------------------------------------------------------------------------

   A datapoint is one specific patient who was enrolled in DrFirst's
   "2026_Optimal_Timing_Personalization" experiment, who received an
   initial SMS invitation at time `ObsDT` (`invitation_type=N/A`, the
   LINKMESSAGE type), who did NOT click the initial within the
   cancellation window so a follow-up SMS was queued, who was then
   UNIFORMLY RANDOMLY assigned (`π(T|X) = 1/20`) to one of 20 follow-up
   send-time arms `T ∈ {FT_08_00, FT_08_30, ..., FT_17_30}` (column
   `experiment_config`, every 30 min from 08:00 to 17:30 local), and
   for whom the follow-up was actually delivered (`minutes_to_followup > 0`,
   `follow_up_invitation_id` set, `follow_up_deliver_on_date` recorded);
   the binary outcome `Y = clicked_follow_up_7d` answers "did the patient
   click any link in the FOLLOW-UP message within 7 days of
   `follow_up_deliver_on_date`" (verified by checking
   `first_follow_up_clicked_date` falls inside that window), with
   population mean Y ≈ 0.459 on test.

   The input features X are 12 CaseFn groups encoded as one 1,995-dim
   sparse vector with ~58 non-zero entries per row:
     - PAge5                 — age in 5-yr buckets, from DfPtt.ageBucketBy5
     - Pgender               — M/F/U, from DfPtt.gender
     - PZip3FixedLen         — first-3 zip digits, from DfPtt.zipcode3
     - InvCrntTimeFixedLen   — ★ THE TREATMENT — one-hot of FT_HH_MM from
                               DfInv.experiment_config (S-Learner pattern:
                               treatment folded into X; for counterfactual
                               inference this slot is re-set to other arms)
     - PhmFixedLen           — patient's pharmacy NCPDP code
     - NPIFixedLen           — prescribing provider NPI
     - NPITraitFixedLen      — provider attributes (specialty, taxonomy)
     - RxCrntNDCRxFixedLen   — current Rx (NDC + dosage form + refill bucket)
     - Zip3EngFixedLen       — HISTORICAL engagement aggregated by zip3
     - NcpdpEngFixedLen      — HISTORICAL engagement by pharmacy
     - NpiEngFixedLen        — HISTORICAL engagement by provider
     - NdcEngFixedLen        — HISTORICAL engagement by drug

   (The 4 *Eng* features are HISTORICAL, not contemporaneous, so they
   do not leak the current invitation's click.)

   Selection filters (Stage 4 SplitArgs.Split_to_Selection, applied to
   BOTH train and test):
     1. messaged == 1                          — SMS was actually sent
     2. experiment_config in {20 FT_HH_MM arms} — valid OptTime arm
     3. minutes_to_followup > 0                 — FU was actually delivered
                                                  (not cancelled because the
                                                  patient clicked the initial
                                                  inside the cancel window)

   INTENTIONALLY NOT FILTERED ON:
     - `clicked` (whether they ever clicked the original invitation) —
       deliberately KEPT IN the cohort. The label clicked_follow_up_7d
       is specifically about the FU message, not the original, so filtering
       on `clicked` would be selection-on-a-correlated-outcome and is bias-
       inducing. Two patients can have clicked=1 AND clicked_follow_up_7d=1
       (clicked both) or clicked=1 AND clicked_follow_up_7d=0 (clicked only
       the original) or clicked=0 AND clicked_follow_up_7d=1 (FU-only) —
       all three are valid datapoints in this cohort.

   Split policy:
     SplitMethod = RandomByStratum
     Stratification columns: [experiment_config, clicked_follow_up_7d,
                              authenticated_follow_up_7d]
     Ratio = 80/20, seed = 42
     Train: 99,206 rows  |  Test: 24,845 rows
     Per-arm test counts: 1,193 - 1,297 (verified uniform-random)
     Label positive rate: ≈ 45.9% in both splits

   Worked example row (test idx 0):
     PID 10000000012, Male, age 70.  ObsDT = 2026-04-06 17:21.
     T = FT_10_30 (arm idx 5).  FU delivered 2026-04-07 13:55 (~20.6 hrs later).
     7-day window: 2026-04-07 13:55 → 2026-04-14 13:55.
     first_follow_up_clicked_date = NaT → Y = 0.


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
