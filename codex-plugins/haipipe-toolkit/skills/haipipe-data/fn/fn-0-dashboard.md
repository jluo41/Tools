fn-dashboard: Data Pipeline Status Dashboard
=============================================

Full visibility scan across 3 dimensions:

  Panel A -- Registered Fn Inventory  ("what is on the shelf")
  Panel B -- Asset Status Table       ("what has been built")
  Panel C -- Asset Detail Report      ("what is inside each asset")

Run this before any pipeline cook, before any debugging. Read-only -- no
files are modified.

---

Overview
========

**Purpose:** Full pipeline visibility at a glance. Three panels give
increasing levels of detail -- from registered Fns to asset existence to
per-asset schema and settings.

**Entry point:** Always run the full dashboard at the start of a session.
It orients you to both what is available (Fns) and what has been produced
(assets) before taking any action.

---

Stage-Filtered Mode
====================

If invoked with a stage qualifier (e.g., "dashboard 1-source"):

  - Run ONLY the Panel A step for that stage (e.g., A1 for 1-source)
  - Run ONLY the Panel B row for that stage directory
  - Run ONLY the Panel C detail for that stage (if PRESENT)
  - Skip all other stages entirely

This is the fast path. Use it when you already know which stage to inspect.

  dashboard 0-rawdata ->  Panel 0 only (raw files, no manifest check)
  dashboard 1-source  ->  A1 + B(SourceStore only)  + C1
  dashboard 2-record  ->  A2 + B(RecStore only)      + C2
  dashboard 3-case    ->  A3 + B(CaseStore only)     + C3
  dashboard 4-aidata  ->  A4 + B(AIDataStore only)   + C4

Full dashboard (no stage) still runs all panels in order.
Stage-filtered dashboard is always fast -- no confirmation needed.

---

Full-Dashboard Confirmation Gate
==================================

When invoked WITHOUT a stage qualifier (full dashboard), STOP before running
any commands and do the following:

Step G1: Check for cached results.

```bash
ls _WorkSpace/.haipipe_dashboard_cache.md 2>/dev/null
```

If cache exists, read the first 3 lines (metadata: timestamp, scope).

Step G2: Ask the user ONE of these prompts depending on cache state:

  If cache EXISTS:
    "Full dashboard scans all 5 stages (0-rawdata through 4-aidata) and may
     take a while. A cached version exists from <timestamp> (scope=<scope>).
     Options:
       1. load-cache  -- show cached results instantly
       2. yes         -- run fresh full scan (overwrites cache)
       3. <stage>     -- e.g. '1-source' to check one stage only (fast)"

  If cache MISSING:
    "Full dashboard scans all 5 stages and may take a while.
     Tip: use 'dashboard 1-source' etc. for a single stage (much faster).
     Run full scan now? (yes / <stage name>)"

Step G3: Wait for user response before proceeding.
  - "load-cache" or "cache" -> load and display cache file, stop
  - "yes" or "full"         -> proceed with full scan
  - stage name              -> switch to stage-filtered mode for that stage
  - anything else           -> ask again

Skip this gate entirely when a stage qualifier is given.

---

Cache
=====

After completing ANY dashboard run (full or stage-filtered), save output to:

  _WorkSpace/.haipipe_dashboard_cache.md

Format:

  # Dashboard Cache
  # Generated: <ISO datetime e.g. 2026-02-25T14:32:00>
  # Scope: full | 0-rawdata | 1-source | 2-record | 3-case | 4-aidata
  <full dashboard output text below this line>

When loading from cache, prepend this line to the output:

  [Cached: <timestamp>, scope=<scope>. To refresh: run dashboard and confirm 'yes'.]

---

The Three Panels
================

**Panel A: Registered Fn Inventory**

  Shows what Fns are registered in code/haifn/ at each stage -- the "shelf"
  of available Chefs. For each Fn, shows key attributes: file formats,
  ProcName list, column schemas, ROName config, vocab keys, etc.

  Answers: "What can I use?" and "What does each Fn produce?"

**Panel B: Asset Status Table**

  Shows what assets exist in _WorkSpace/ and whether each is complete
  (PRESENT), broken (EMPTY), or not yet run (MISSING).

  Answers: "What has been built?" and "What is missing?"

**Panel C: Asset Detail Report**

  For each PRESENT asset, inspects the actual data: columns, row counts,
  case functions, split sizes, config settings. Goes deeper than Panel B.

  Answers: "What is inside this asset?" and "Does it match expectations?"

---

Panel 0: RawDataStore Scan
==========================

Lists what raw cohort data is available before any pipeline processing.
RawDataStore has no manifest.json -- status is PRESENT (files exist) or
MISSING (no directory). No EMPTY state.

Step P0: Scan cohorts and files.

```bash
ls _WorkSpace/0-RawDataStore/
```

For each cohort found:

```bash
# Directory structure (depth 2)
ls _WorkSpace/0-RawDataStore/<CohortName>/
ls _WorkSpace/0-RawDataStore/<CohortName>/Source/

# Total file count
find "_WorkSpace/0-RawDataStore/<CohortName>" -type f | wc -l

# File format breakdown
find "_WorkSpace/0-RawDataStore/<CohortName>" -type f | sed 's/.*\.//' | sort | uniq -c
```

Cross-reference each cohort against SourceStore:

```bash
ls _WorkSpace/1-SourceStore/<CohortName>/ 2>/dev/null
```

Output format:

```
PANEL 0 -- RawDataStore
========================
Cohort: <CohortName>
  Structure:     Source/<subdir>/...
  Total files:   <N>
  Formats:       .xml (N)  |  .csv (N)  |  .parquet (N)
  SourceFn:      <SourceFnName> (registered) / NONE
  SourceSet:     PRESENT (@<SourceFnName>) / MISSING
```

---

Panel A: Registered Fn Inventory
=================================

Run all discovery commands first, then inspect each Fn.

**Step A1: List all registered Fns at each stage**

```bash
# Stage 1 -- SourceFns
ls code/haifn/fn_source/

# Stage 2 -- HumanFns and RecordFns
ls code/haifn/fn_record/human/
ls code/haifn/fn_record/record/

# Stage 3 -- TriggerFns and CaseFns
ls code/haifn/fn_case/fn_trigger/
ls code/haifn/fn_case/case_casefn/

# Stage 4 -- Input TfmFns, Output TfmFns, SplitFns
ls code/haifn/fn_aidata/entryinput/
ls code/haifn/fn_aidata/entryoutput/
ls code/haifn/fn_aidata/split/
```

**Step A2: Inspect each SourceFn (Stage 1)**

For each .py file found in code/haifn/fn_source/:

```bash
# Read the top of each SourceFn to see its attributes
head -40 code/haifn/fn_source/<SourceFnName>.py
```

Report these per SourceFn:

  - `SourceFile_SuffixList`  -- input file format(s) (e.g., ['.xml'], ['.csv'])
  - `ProcName_List`           -- list of output table names
  - `ProcName_to_columns`     -- column schema per table (list of column names)

Output table format for SourceFns:

```
STAGE 1 -- Registered SourceFns
================================
SourceFn: <SourceFnName>
  Input formats:    ['.xml']
  ProcNames:        ['CGM', 'Medication', 'Diet', 'Exercise', 'Ptt']
  Columns per ProcName:
    CGM:            [PatientID, DT_s, BGValue, ...]           (N cols)
    Medication:     [PatientID, MedAdministrationID, ...]     (11 cols)
    Diet:           [PatientID, CarbsEntryID, ...]            (15 cols)
    Exercise:       [PatientID, ExerciseEntryID, ...]         (13 cols)
```

**Step A3: Inspect RecordFns (Stage 2)**

For each RecordFn in code/haifn/fn_record/record/:

```bash
head -40 code/haifn/fn_record/record/<RecordFnName>.py
```

Report per RecordFn:

  - `OneRecord_Args['RecordName']`      -- canonical name
  - `attr_cols`                          -- the columns that CaseFns can access
  - `RawName_to_RawConfig` keys          -- which source tables this RecordFn reads

For HumanFns in code/haifn/fn_record/human/:

```bash
head -30 code/haifn/fn_record/human/<HumanFnName>.py
```

Report: `OneHuman_Args['HumanName']`, `OneHuman_Args['HumanID']`,
`Excluded_RawNameList` (tables skipped when building entity roster).

Output format:

```
STAGE 2 -- Registered RecordFns
================================
HumanFn: <HumanFnName>
  HumanID col:      <HumanIDCol>
  Excludes tables:  [<Table1>, <Table2>]

RecordFn: <RecordFnName>
  attr_cols:        [<EntityID>, <DatetimeCol>, <ValueCol>, ...]   (N cols)
  Reads from:       <SourceTableName>
  Signal pattern:   Dense/Continuous | Sparse/Additive | ...
```

**Step A4: Inspect CaseFns and TriggerFns (Stage 3)**

For each CaseFn in code/haifn/fn_case/case_casefn/:

```bash
head -60 code/haifn/fn_case/case_casefn/<CaseFnName>.py
```

Report per CaseFn:

  - `CaseFnName`                         -- naming follows <Feature><Window>
  - `RO_to_ROName` values                -- which ROName (h.r.c) it accesses
  - `Ckpd_to_CkpdObsConfig` keys         -- window name(s) and time ranges
  - `COVocab['tid2tkn']` length           -- vocabulary size (token count)
  - return suffixes inferred from MetaDict or fn body (--tid, --wgt, --val, --str)

For TriggerFns in code/haifn/fn_case/fn_trigger/:

```bash
head -40 code/haifn/fn_case/fn_trigger/<TriggerFnName>.py
```

Report: `Trigger`, key `Trigger_Args` fields (case_id_columns, HumanID_list,
ObsDT, ROName_to_RONameArgs keys, and any LTS-specific fields like
`min_segment_length`, `stride`).

Output format:

```
STAGE 3 -- Registered TriggerFns + CaseFns
==========================================
TriggerFn: <TriggerFnName>
  Trigger ID:       <TriggerFnName>
  case_id_columns:  ['<EntityID>', '<ObsDT>']
  HumanID:          <EntityID>
  RONames:          ['h<Human>.r<Record>']
  LTS settings:     stride=12  min_segment=288  buffer=240/240  (if applicable)

CaseFn: <CaseFnName>           (e.g., CGMValueBf24h)
  ROName:           h<Human>.r<Record>.c<Ckpd>
  Window:           Bf24h  [DistStart=-1440 min, DistEnd=5 min]
  Vocab size:       290 tokens
  Return suffixes:  --tid
```

**Step A5: Inspect TfmFns and SplitFns (Stage 4)**

List only (no deep inspection needed for dashboard):

```bash
ls code/haifn/fn_aidata/entryinput/    # Input TfmFn names
ls code/haifn/fn_aidata/entryoutput/   # Output TfmFn names
ls code/haifn/fn_aidata/split/         # SplitFn names
```

Output format:

```
STAGE 4 -- Registered TfmFns + SplitFns
========================================
Input TfmFns:   <InputTfmFnName1>  <InputTfmFnName2>  ...
Output TfmFns:  <OutputTfmFnName1>  ...
SplitFns:       <SplitFnName1>  ...
```

---

Panel B: Asset Status Table
============================

**Step B1: Scan all stage directories**

```bash
ls _WorkSpace/1-SourceStore/
ls _WorkSpace/2-RecStore/
ls _WorkSpace/3-CaseStore/
ls _WorkSpace/4-AIDataStore/
```

For each asset found, check for manifest.json:

```bash
ls _WorkSpace/<stage>/<asset>/manifest.json   2>/dev/null
```

**Step B2: Build the status table**

Status definitions:

  `PRESENT` = directory exists AND `manifest.json` is present
  `EMPTY`   = directory exists but no `manifest.json` (incomplete run)
  `MISSING` = no directory found

```
ASSET STATUS TABLE
==================

 Stage    | Asset Name                                     | Status  | Notes
 ---------+------------------------------------------------+---------+------------------
 1-source | <CohortName>/@<SourceFnName>                  | PRESENT | N ProcNames
 2-record | <CohortName>_v<N>RecSet                       | PRESENT | M entities
 3-case   | <RecSetName>/@v<N>CaseSet-<Trigger>           | MISSING | Run: cook 3-case
 4-aidata | <aidata_name>/@v<N>                           | PRESENT | train=X test=Y
```

**Step B3: Gap analysis**

After the table, print gap analysis:

```
GAP ANALYSIS
============
Complete:   list each PRESENT asset
Incomplete: list each EMPTY/MISSING asset with reason
Next action: exact haistep-* command for the first gap
```

---

Panel C: Asset Detail Report
=============================

For each PRESENT asset, run a deeper inspection. This answers the per-stage
questions the dashboard is designed to reveal.

**Step C1: Stage 1 (Source) -- ProcName detail**

For each PRESENT SourceSet:

```bash
# List files in the asset (shows ProcName parquets)
ls _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/

# Inspect each ProcName parquet
source .venv/bin/activate && source env.sh
python -c "
import pandas as pd, os
base = '_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>'
for f in os.listdir(base):
    if f.endswith('.parquet'):
        df = pd.read_parquet(os.path.join(base, f))
        print(f'  {f.replace(\".parquet\",\"\")}: {len(df)} rows, {len(df.columns)} cols')
        print(f'    Columns: {list(df.columns)}')
"
```

Report per SourceSet:

```
SOURCE DETAIL: <CohortName>/@<SourceFnName>
-------------------------------------------
  CGM:        48,210 rows  |  cols: [PatientID, DT_s, BGValue, ...]
  Medication:  3,142 rows  |  cols: [PatientID, MedAdministrationID, ...]
  Diet:        8,901 rows  |  cols: [PatientID, CarbsEntryID, ...]
  Exercise:    1,204 rows  |  cols: [PatientID, ExerciseEntryID, ...]
  Ptt:            12 rows  |  cols: [PatientID, ...]
```

**Step C2: Stage 2 (Record) -- entity count and record columns**

For each PRESENT RecordSet:

```bash
# List Human and Record directories
ls _WorkSpace/2-RecStore/<RecordSetName>/

# Inspect Human entity count and Record columns
source .venv/bin/activate && source env.sh
python -c "
import pandas as pd
base = '_WorkSpace/2-RecStore/<RecordSetName>'

# Human entity count
for d in os.listdir(base):
    if d.startswith('Human-'):
        df = pd.read_parquet(f'{base}/{d}/df_Human.parquet')
        print(f'  {d}: {len(df)} entities')
        print(f'    Columns: {list(df.columns)}')

# Record columns (df_RecAttr.parquet)
for d in os.listdir(base):
    if d.startswith('Record-'):
        df = pd.read_parquet(f'{base}/{d}/df_RecAttr.parquet')
        print(f'  {d}: {len(df)} rows')
        print(f'    RecAttr cols: {list(df.columns)}')
"
```

Report per RecordSet:

```
RECORD DETAIL: <CohortName>_v0RecSet
--------------------------------------
  Human-<HumanFnName>:    12 entities
    Columns: [PatientID, RawPatientID, ...]

  Record-<HumanFnName>.<RecordFnName>:    48,210 rows
    RecAttr cols: [PatientID, DT_s, BGValue, ...]

  Record-<HumanFnName>.<OtherRecordFn>:   3,142 rows
    RecAttr cols: [PatientID, DT_s, Dose, ...]
```

**Step C3: Stage 3 (Case) -- trigger definition and CaseFn list**

For each PRESENT CaseSet:

```bash
# List files at ROOT (df_case.parquet + @CaseFn.parquet files)
ls _WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>/

# Inspect case count, columns, CaseFn list
source .venv/bin/activate && source env.sh
python -c "
import pandas as pd, json, os
base = '_WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>'

# Base case count and columns
df_case = pd.read_parquet(f'{base}/df_case.parquet')
print(f'  df_case: {len(df_case)} rows')
print(f'  Trigger columns: {list(df_case.columns)}')

# CaseFn list and column counts
casefn_files = [f for f in os.listdir(base) if f.startswith('@') and f.endswith('.parquet')]
print(f'  Registered CaseFns: {len(casefn_files)}')
for f in sorted(casefn_files):
    df_cf = pd.read_parquet(f'{base}/{f}')
    cf_name = f[1:].replace('.parquet','')
    cols = [c for c in df_cf.columns if c != 'idx']
    suffixes = list({c.split('--')[1] for c in cols if '--' in c})
    print(f'  {cf_name}: {len(df_cf)} rows  suffixes={suffixes}')

# Vocabulary token counts
with open(f'{base}/cf_to_cfvocab.json') as fp:
    vocabs = json.load(fp)
for cf, vocab in vocabs.items():
    tkn_count = len(vocab.get('tid2tkn', []))
    print(f'  Vocab [{cf}]: {tkn_count} tokens')
"
```

Report per CaseSet:

```
CASE DETAIL: <RecSetName>/@v0CaseSet-<Trigger>
-----------------------------------------------
  df_case:       48,210 rows
  Trigger cols:  [PatientID, ObsDT, lts_id, ...]

  CaseFns registered: 5
    CGMValueBf24h:      48,210 rows  suffixes=[--tid]        vocab=290 tokens
    CGMInfoBf24h:       48,210 rows  suffixes=[--val]        vocab=8 tokens
    PAge5:              48,210 rows  suffixes=[--tid]        vocab=12 tokens
    Pgender:            48,210 rows  suffixes=[--tid]        vocab=4 tokens
    InvCrntTimeFixedLen: 48,210 rows suffixes=[--tid, --wgt] vocab=24 tokens
```

**Step C4: Stage 4 (AIData) -- split sizes and settings**

For each PRESENT AIDataSet:

```bash
# List splits and vocab files
ls _WorkSpace/4-AIDataStore/<aidata_name>/@<version>/

# Inspect split sizes and vocab
source .venv/bin/activate && source env.sh
python -c "
from haipipe.aidata_base.aidata_set import AIDataSet
import os, json

base = '_WorkSpace/4-AIDataStore/<aidata_name>/@<version>'
aidata_set = AIDataSet.load_from_disk(path=base, SPACE=SPACE)

# Split sizes
for split_name, ds in aidata_set.dataset_dict.items():
    print(f'  {split_name}: {len(ds)} samples  features={len(ds.column_names)} cols')

# Input method from manifest
with open(f'{base}/manifest.json') as fp:
    manifest = json.load(fp)
print(f'  input_method:     {manifest.get(\"input_method\", \"unknown\")}')
print(f'  input_casefn_list:{manifest.get(\"input_casefn_list\", [])}')
print(f'  output_method:    {manifest.get(\"output_method\", \"unknown\")}')

# Vocab key counts
print(f'  feat_vocab keys:  {len(aidata_set.feat_vocab)} entries')
print(f'  CF_to_CFVocab:    {list(aidata_set.CF_to_CFVocab.keys())}')
"
```

Report per AIDataSet:

```
AIDATA DETAIL: <aidata_name>/@v0001
-------------------------------------
  train:       2,475 samples  |  features: 48 cols
  validation:    618 samples  |  features: 48 cols
  test-id:       636 samples  |  features: 48 cols
  test-od:         0 samples  |  (empty -- no OD split)

  input_method:      <InputTfmFnName>
  input_casefn_list: ['CGMValueBf24h', 'CGMInfoBf24h', 'PAge5', 'Pgender']
  output_method:     <OutputTfmFnName>
  feat_vocab keys:   1,995 entries
  CF_to_CFVocab:     ['CGMValueBf24h', 'CGMInfoBf24h', 'PAge5', 'Pgender']
```

---

Full Dashboard Output Order
============================

Run and report in this order:

```
0. Panel 0 -- RawDataStore Scan
   P0. Cohort list, file counts, format breakdown, cross-ref to SourceStore

1. Panel A -- Registered Fn Inventory
   A1. Stage 1 SourceFns  (ProcName list + column schemas)
   A2. Stage 2 HumanFns + RecordFns  (entity ID, attr_cols)
   A3. Stage 3 TriggerFns + CaseFns  (ROName, window, vocab)
   A4. Stage 4 TfmFns + SplitFns  (names only)

2. Panel B -- Asset Status Table
   B1. Scan _WorkSpace/ at all 4 stages (1-4)
   B2. Print status table (PRESENT / EMPTY / MISSING)
   B3. Gap analysis + next recommended action

3. Panel C -- Asset Detail Report
   C1. Source detail  (ProcName rows + columns)
   C2. Record detail  (entity count + record columns)
   C3. Case detail    (trigger cols, CaseFn list, suffixes, vocab)
   C4. AIData detail  (split sizes, input_method, casefn_list, vocab)

4. Save results to _WorkSpace/.haipipe_dashboard_cache.md
```

Panel C only runs for assets with status PRESENT in Panel B. Skip EMPTY
and MISSING assets in Panel C (nothing to inspect).

---

MUST DO
=======

1. Run Panel 0 first (RawDataStore), then Panel A, B, C in order
2. Always activate .venv and source env.sh before any Python inspection
   NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
   Always chain: source .venv/bin/activate && source env.sh && python -c "..."
3. Run ls _WorkSpace/ first; if missing, stop and report workspace not initialized
4. For Stage 3, look for @-prefixed .parquet files at ROOT (NOT in subdirectory)
5. For Stage 4, check cf_to_cfvocab.json and feat_vocab.json at ROOT (NOT in vocab/)
6. Present all panels in order before making recommendations
7. Report BOTH registered Fn counts AND asset counts at the top of the output
8. After completing ANY dashboard run, save output to _WorkSpace/.haipipe_dashboard_cache.md
9. For full dashboard (no stage): ALWAYS run the Confirmation Gate first -- never skip

---

MUST NOT
========

1. NEVER modify any files -- this is read-only
2. NEVER assume assets exist without running ls commands
3. NEVER skip Panel A -- Fn inventory is half the dashboard
4. NEVER skip EMPTY assets in Panel B (they need re-run, different from MISSING)
5. NEVER look for case_data.parquet -- the file is df_case.parquet
6. NEVER assume a vocab/ subdirectory in Stage 4 -- files are at ROOT
