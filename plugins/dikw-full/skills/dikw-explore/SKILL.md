---
name: dikw-explore
description: "DIKW data exploration skill. Profile raw data files, assess quality, check for prior analysis. Use when the user asks to explore data, profile a dataset, start a DIKW session, or says /dikw-explore. Trigger: explore, profile data, data overview, check data quality."
---

Skill: dikw-explore
====================

Profile raw data, assess quality, note prior work. Produces a **snapshot-level**
artifact (`exploration/explore_notes.md`) that all sessions on the snapshot
reuse. NOT a session phase.

When this runs:
  - Automatically by `/dikw` at Stage 4.5, once per new snapshot
  - Manually via `/dikw {folder} --re-explore` when data has materially
    changed and the existing exploration is stale
  - Standalone: `/dikw-explore {snapshot_dir}` for ad-hoc profiling

On invocation, use `$ARGUMENTS` to get the snapshot_dir. If not provided, look for
data files in the current working directory under `source/`.

---

Steps
-----

1. Find the snapshot directory and data files:
   - If `$ARGUMENTS` contains a path, use it as snapshot_dir
   - Otherwise use cwd as snapshot_dir
   - List all files in `{snapshot_dir}/source/`

2. Profile every data file:
   - Use python3 with pandas
   - For each file: print shape, columns, dtypes, null counts, sample rows
   - Check for duplicates, outliers, missing values

3. Check for prior analysis:
   - Look in `{snapshot_dir}/insights/` for existing D/I/K/W task folders
   - Note what levels already have work (sorted by `{L}{NN}-` prefix, L=D/I/K/W)
   - `insights/` is **snapshot-scoped and shared across sessions** — prior
     sessions' outputs live here. Record their existence as reference only;
     do NOT let them shape the new explore notes as if they were part of
     this snapshot's raw data. The explore notes should reflect the
     source/ files, not the derived insights.

4. Write exploration notes:
   - Output path: `{snapshot_dir}/exploration/explore_notes.md`  ← SNAPSHOT LEVEL
     (NOT `sessions/{aim}/exploration/…` — this artifact is shared across sessions)
   - Create `{snapshot_dir}/exploration/` if needed
   - If the file already exists and `--re-explore` was not requested, print
     a notice and exit without overwriting.

Report structure:

  Data Overview
    What files exist in source/, total rows/columns, file sizes

  File Profiles
    Per-file: schema, column types, sample values

  Quality Assessment
    Nulls: count and percentage per column
    Duplicates: exact row duplicates, near-duplicates
    Anomalies: outliers, unexpected values, type mismatches

  Initial Observations
    Interesting patterns visible in the data
    Potential issues that need attention

  Analysis Opportunities
    What analyses would be valuable for this dataset

---

Rules
-----

- Use python3 ONLY (never "python")
- Read from `{snapshot_dir}/source/` (symlinks resolve to the actual data)
- Write the report as clean markdown with sections, tables, and bullet points
- Be thorough but concise — focus on what matters for analysis
- Do NOT propose a plan — just explore and report findings

---

Example tasks this skill handles
---------------------------------

  - Profile all data files in a snapshot's source/
  - Check data quality (nulls, duplicates, types)
  - Assess what analysis has already been done (by scanning insights/)
  - Write exploration notes for a new DIKW session
