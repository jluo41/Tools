---
name: dikw-explore
description: "DIKW data exploration skill. Profile raw data files, assess quality, check for prior analysis. Use when the user asks to explore data, profile a dataset, start a DIKW session, or says /dikw-explore. Trigger: explore, profile data, data overview, check data quality."
---

Skill: dikw-explore
====================

Profile raw data, assess quality, note prior work. First phase of any DIKW session.

On invocation, use `$ARGUMENTS` to get the project path. If not provided, look for
data files in the current working directory under `source/raw/`.

---

Steps
-----

1. Find the project directory and data files:
   - If `$ARGUMENTS` contains a path, use it as project_dir
   - Otherwise use cwd as project_dir
   - List all files in `{project_dir}/source/raw/`

2. Profile every data file:
   - Use python3 with pandas
   - For each file: print shape, columns, dtypes, null counts, sample rows
   - Check for duplicates, outliers, missing values

3. Check for prior analysis:
   - Look in `{project_dir}/reports/` for existing D/I/K/W reports
   - Note what levels already have work

4. Write exploration notes:
   - Output path: `{project_dir}/sessions/{aim}/exploration/explore_notes.md`
   - If no aim provided, use `default` as aim name
   - Create parent directories if needed

Report structure:

  Data Overview
    What files exist, total rows/columns, file sizes

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
- Write the report as clean markdown with sections, tables, and bullet points
- Be thorough but concise — focus on what matters for analysis
- Do NOT propose a plan — just explore and report findings

---

Example tasks this skill handles
---------------------------------

  - Profile all data files in a project
  - Check data quality (nulls, duplicates, types)
  - Assess what analysis has already been done
  - Write exploration notes for a new DIKW session
