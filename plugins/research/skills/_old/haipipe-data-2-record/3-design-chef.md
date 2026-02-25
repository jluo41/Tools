Subcommand: design-chef
=======================

Purpose: Create a new HumanFn or RecordFn via the builder pattern.

This skill documents FRAMEWORK PATTERNS only. It does not catalog
project-specific state (which Fns exist, column names, cohort names).
That state is always discovered at runtime from the filesystem.

---

Workflow
========

0. Inspect source table (see Step 0 below)
1. Present plan to user -> get approval
2. Activate environment: source .venv/bin/activate && source env.sh
3. Decide what to build: HumanFn or RecordFn? (see Which to Build below)
4. Discover existing builders:
   ```bash
   ls code-dev/1-PIPELINE/2-Record-WorkSpace/h*.py   # HumanFn builders
   ls code-dev/1-PIPELINE/2-Record-WorkSpace/r*.py   # RecordFn builders
   ```
5. Copy the builder most similar to yours as starting point
6. Edit [CUSTOMIZE] sections only; keep [BOILERPLATE] unchanged
7. Run builder: python code-dev/1-PIPELINE/2-Record-WorkSpace/<builder>.py
8. Verify: RUN_TEST = True in the builder confirms the generated file loads
9. Register in config YAML under HumanRecords
10. Run Record Pipeline test end-to-end

---

Step 0: Inspect Source Table
==============================

Before writing any logic, examine the raw data:

```python
source_set = SourceSet.load_asset('<cohort>/@<SourceFnName>', SPACE=SPACE)
print(list(source_set.ProcName_to_ProcDf.keys()))  # what tables exist
df = source_set['<TableName>']
print(df.dtypes)
print(df.describe())
print(df.head(3))
```

---

Which to Build: HumanFn or RecordFn?
======================================

```
Is this about defining the ENTITY itself (who/what is tracked)?
    YES  -->  HumanFn  (see Part 1 below)
    NO   -->  RecordFn (see Part 2 below)
```

**HumanFn** -- build one when:
- The entity type is new (animal, device, subject, patient with different ID scheme)
- The raw entity ID column name differs from any existing HumanFn
- You need a different ID length or namespace
- In practice: one HumanFn per entity type per project; most new data just needs a RecordFn

**RecordFn** -- build one when:
- You have a new data table to process for an existing entity type
- The entity type already has a HumanFn; you only need to add the time-series data

---

Part 1: HumanFn Builder
=========================

A HumanFn defines the top-level entity: who is being tracked, how their
raw ID is identified across tables, and which source tables contain one row
per entity (for building the entity roster) vs. many rows (event tables to exclude).

**Three things to customize:**

```
OneHuman_Args              HumanName: name of this HumanFn
                           HumanID: internal ID column name in the RecordSet
                           RawHumanID: ID column name in raw source data
                           HumanIDLength: integer length for ID generation

get_RawHumanID_from_       Given a list of column names from any source table,
dfRawColumns(dfRawColumns) return the column that identifies the entity.
                           Return None if the table does not contain entity rows.
                           This lets the pipeline auto-detect entity IDs across
                           tables with different schemas.

Excluded_RawNameList       Source table names to EXCLUDE from entity roster building.
                           Exclude all event/time-series tables (many rows per entity).
                           Include only demographic/static tables (one row per entity).
```

**Template:**

```python
# [CUSTOMIZE] OneHuman_Args
OneHuman_Args = {
    'HumanName':     '<HumanFnName>',   # e.g., HmAnimal, HmPatient, HmSubject
    'HumanID':       '<InternalIDCol>', # e.g., AID, PID, SID
    'RawHumanID':    '<RawIDCol>',      # e.g., AnimalID, PatientID, SubjectID
    'HumanIDLength': <N>,               # integer, e.g., 10
}

# [CUSTOMIZE] get_RawHumanID_from_dfRawColumns
def get_RawHumanID_from_dfRawColumns(dfRawColumns):
    """
    Return the entity ID column name if this table contains entity-level rows.
    Return None if the table does not contain the entity ID (skip it).
    """
    if '<RawIDCol>' in dfRawColumns:
        return '<RawIDCol>'
    # Optional: check for alternative column names if sources vary
    # if '<AltIDCol>' in dfRawColumns:
    #     return '<AltIDCol>'
    return None

# [CUSTOMIZE] Excluded_RawNameList
# List every event/time-series table by its SourceSet ProcName.
# These have many rows per entity and should NOT define the entity roster.
Excluded_RawNameList = [
    '<EventTable1>',   # e.g., 'Readings', 'GPS', 'HeartRate'
    '<EventTable2>',   # e.g., 'Sightings', 'Diet', 'Medication'
    # ... all tables except the one demographic/static table
]
```

**When `get_RawHumanID_from_dfRawColumns` returns None:**
The pipeline skips that table for entity identification. It will still be
available for RecordFn processing via RawName_to_RawConfig.

**Builder naming:**

```
Builder: h<N>_build_human_<HumanFnName>.py
Output:  code/haifn/fn_record/human/<HumanFnName>.py
```

**Test:** The builder's RUN_TEST runs the pipeline with only the static/demographic
RecordFn to verify the entity roster is built correctly.

---

Part 2: RecordFn Builder
=========================

A RecordFn processes one source table into temporally-aligned records for
entities already defined by a HumanFn.

**Signal Type Decision Tree**

```
Q1: Readings expected at regular high-frequency intervals?
    (e.g., sensor fires every fixed interval)
    YES  -->  Pattern A: Dense/Continuous
    NO   -->  Q2

Q2: When two events land in the same time slot, combine by:
    SUM    -->  Pattern B: Sparse/Additive
    MEAN   -->  Pattern C: Sparse/Mean
    FIRST  -->  Pattern D: Sparse/First
```

Aggregation intuition:

```
SUM    quantities that accumulate in a window (intake, distance, count)
MEAN   repeat measurements of the same physical thing (weight, BP, temperature)
FIRST  discrete administered events where only one logically occurs (dose, draw)
```

**Before picking a pattern, answer from Step 0:**

- Primary datetime column? Separate entry datetime?
- Timezone column? (offset in minutes, named zone, or IANA string)
- Signal density (rows per entity per day)?
- If two rows land in the same slot: sum / average / first?
- Valid value range for each numeric field?

---

**Processing Skeleton** (all 4 patterns share this; only aggregation differs)

Replace all <Placeholders> with actual values from your source table.

```python
def get_RawRecProc_for_HumanGroup(df_RawRec_for_HumanGroup, OneRecord_Args, df_Human):
    import pandas as pd, numpy as np
    df = df_RawRec_for_HumanGroup

    # Define empty return schema once; reuse at every early-exit point
    EMPTY_COLS = ['<RawHumanID>', 'DT_s', 'DT_r', 'DT_tz',
                  '<ValueCol>', 'time_to_last_entry']

    # 1. Timezone filter
    # strict: abs < 840  (±14h, single-country cohorts)
    # loose:  abs < 1000 (~±16.7h, international cohorts)
    df = df[df['<TimezoneCol>'].abs() < <THRESHOLD>].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 2. Parse datetime
    df['<DatetimeCol>'] = pd.to_datetime(df['<DatetimeCol>'], format='mixed', errors='coerce')
    df = df[df['<DatetimeCol>'].notna()].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 3. Resolve timezone: merge -> prefer offset -> fallback to user_tz -> default 0
    a = len(df)
    df = pd.merge(df, df_Human[['<RawHumanID>', 'user_tz']], how='left')
    assert len(df) == a
    df['DT_tz'] = df['<TimezoneCol>'].replace(0, None).fillna(df['user_tz']).infer_objects(copy=False)

    # 4. Build DT_s (observation time in local timezone); filter implausible dates
    df['DT_s'] = pd.to_datetime(df['<DatetimeCol>'], format='mixed', errors='coerce')
    df = df[df['DT_s'] > pd.to_datetime('<DATE_CUTOFF>')].reset_index(drop=True)
    df['DT_tz'] = df['DT_tz'].fillna(0).astype(int)
    df['DT_s'] = df['DT_s'] + pd.to_timedelta(df['DT_tz'], 'm')
    df = df[df['DT_s'].notna()].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 5. DT_r: record entry time (same as DT_s if no separate entry datetime exists)
    df['DT_r'] = df['DT_s']
    # If a separate entry datetime column exists:
    # df['DT_r'] = pd.to_datetime(df['<EntryDatetimeCol>'], ...) + pd.to_timedelta(df['DT_tz'], 'm')

    # 6. Value filter (set range to what is physically plausible for this field)
    df['<ValueCol>'] = pd.to_numeric(df['<ValueCol>'], errors='coerce')
    df = df[(df['<ValueCol>'] > <MIN>) & (df['<ValueCol>'] < <MAX>)].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 7. Round DT_s and DT_r to domain time unit
    for col in ['DT_s', 'DT_r']:
        date = df[col].dt.date.astype(str)
        hour = df[col].dt.hour.astype(str)
        mins = ((df[col].dt.minute / <INTERVAL_MINUTES>).astype(int) * <INTERVAL_MINUTES>).astype(str)
        df[col] = pd.to_datetime(date + ' ' + hour + ':' + mins + ':00')

    # 8. Aggregate by (RawHumanID, DT_s) -- only this line changes per pattern
    RawHumanID = OneRecord_Args['RawHumanID']
    df = df.groupby([RawHumanID, 'DT_s']).agg({
        'DT_r':        'first',
        'DT_tz':       'first',
        '<ValueCol>':  '<AGG>',   # see pattern table below
        # Additional optional columns: use 'first'
    }).reset_index()

    # 9. time_to_last_entry in domain time units
    df = df.sort_values([RawHumanID, 'DT_s'])
    df['time_to_last_entry'] = (
        df.groupby(RawHumanID, group_keys=False)['DT_s']
        .diff().dt.total_seconds() / 60 / <INTERVAL_MINUTES>
    )
    return df
```

**Pattern aggregation table** -- only step 8 `<AGG>` changes:

```
Pattern A: Dense/Continuous   'first'   sensor readings; duplicate in slot is rare
Pattern B: Sparse/Additive    'sum'     quantities that accumulate per time window
Pattern C: Sparse/Mean        'mean'    repeat measurements of the same quantity
Pattern D: Sparse/First       'first'   discrete events; later ones in slot discarded
```

For optional / secondary columns: always use `'first'` regardless of pattern.

---

**RecordFn Processing Invariants**

Every get_RawRecProc_for_HumanGroup must satisfy these, for any domain:

1. Define EMPTY_COLS once at top; return it at every filter that empties the DataFrame
2. Parse datetimes with: pd.to_datetime(..., format='mixed', errors='coerce')
3. Filter implausible dates; use a filter, not an assertion
4. Assert row count unchanged after merging df_Human
5. Resolve timezone: prefer explicit offset -> fallback user_tz -> default 0
6. Round both DT_s and DT_r to the domain time unit
7. Return only columns listed in attr_cols -- no extras

---

**What You Customize in a RecordFn Builder**

```
OneRecord_Args           RecordName, RecID, RawHumanID, ParentRecName,
                         RecDT, RawNameList, human_group_size, rec_chunk_size

RawName_to_RawConfig     raw_columns (subset of source table to load),
                         rec_chunk_size, raw_datetime_column

attr_cols                Final output column list -- must exactly match
                         what get_RawRecProc_for_HumanGroup returns

get_RawRecProc_          Use skeleton above; fill in <Placeholders>;
for_HumanGroup           pick aggregation from the pattern table
```

**Builder naming:**

```
Builder: r<N>_build_record_<RecordFnName>.py
Output:  code/haifn/fn_record/record/<RecordFnName>.py
```

---

Naming Conventions
===================

```
HumanFn builder:  h<N>_build_human_<HumanFnName>.py
RecordFn builder: r<N>_build_record_<RecordFnName>.py

Generated HumanFn: code/haifn/fn_record/human/<HumanFnName>.py
Generated RecordFn: code/haifn/fn_record/record/<RecordFnName>.py
```

N is the next available number. Check before choosing:
```bash
ls code-dev/1-PIPELINE/2-Record-WorkSpace/ | grep '^[hr][0-9]'
```

---

MUST DO
=======

- Present plan -> get approval -> execute
- Activate .venv and load env.sh before running builder
- Inspect source table (Step 0) before writing any code
- Decide HumanFn or RecordFn before starting (see Which to Build)
- Set RUN_TEST = True
- For RecordFn: assert row count unchanged after merging df_Human
- Register in config YAML after building

---

MUST NOT
=========

- NEVER edit code/haifn/fn_record/ directly (100% generated)
- NEVER skip RUN_TEST
- NEVER use SUM for physical measurements; NEVER use MEAN for discrete events
- NEVER change attr_cols without updating all downstream CaseFn
- NEVER run builder without .venv activated and env.sh loaded
- NEVER build a RecordFn for a new entity type without a matching HumanFn
