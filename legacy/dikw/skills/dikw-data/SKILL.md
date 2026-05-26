---
name: dikw-data
description: "DIKW D-level data analysis skill. Read raw data, write Python analysis code, produce report. Use when the user asks to run a D-level task, analyze data, run data analysis, profile columns, check quality, or says /dikw-data. Trigger: data analysis, D-level, data task, analyze data, column analysis, quality check."
---

Skill: dikw-data
==================

Runs during **`step=task`** of **`phase=D`**, once per D-task.
D-level data analysis: read raw data, write Python analysis code, produce report.

On invocation, use `$ARGUMENTS` to get: task_name, snapshot_dir.
Format: `/dikw-data <task_name> [snapshot_dir]`

Note: `snapshot_dir` is a `_agent_dikw_space/snapshot-<date>/` folder.


DIKW Boundary — What D-level IS and IS NOT
--------------------------------------------

  D-level answers: WHAT is in the data?

  D IS:
    - Describing what exists (columns, types, counts, distributions)
    - Measuring quality (nulls, duplicates, anomalies)
    - Computing basic statistics (mean, median, range per column)
    - Profiling the structure (what each row represents, grain)
    - Writing Python code that reads raw data and produces facts

  D IS NOT:
    - Finding patterns or correlations (that's I-level)
    - Explaining why something exists (that's K-level)
    - Recommending actions (that's W-level)
    - Interpreting what numbers mean (that's I or K)

  D output is FACTS: "42% of rows have null values in column X"
  NOT interpretations: "the high null rate suggests data quality issues"

  Execution mode: CODE EXECUTION (write and run Python scripts)
  Reads: raw data files in source/ ONLY
  Context: none (D is the first analysis level)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS` (e.g., "col_overview")
   - snapshot_dir: from args or cwd
   - source_dir: `{snapshot_dir}/source/`

2. Resolve the task folder name (D-level prefix is `D` + NN, e.g. D01, D02):
   - List existing `{snapshot_dir}/insights/data/*/` folders
   - If one matches `D*-{task_name}/` → reuse that folder (re-run)
   - Else → assign NN = next available two-digit index within the D-level
     (01, 02, …) and form folder name `D{NN}-{task_name}` (D01, D02, D03, …)
   - Task folder: `{snapshot_dir}/insights/data/D{NN}-{task_name}/`
     (example: `insights/data/D01-cgm_overview/`)

3. Check if report already exists:
   - Path: `{snapshot_dir}/insights/data/D{NN}-{task_name}/report.md`
   - If exists and non-empty: print "Report exists, skipping." and stop

4. Read and analyze data:
   - List files in source_dir
   - Read data with python3 and pandas
   - Perform the analysis (based on task_name)

5. Save code and artifacts:
   - Create `{snapshot_dir}/insights/data/D{NN}-{task_name}/`
   - Save all Python scripts as `analysis.py` (or additional names if needed)
   - Save charts as PNG in the same folder

6. Write report:
   - Path: `{snapshot_dir}/insights/data/D{NN}-{task_name}/report.md`
   - Concise and accurate; max ~1000 words

Report format:

  Task Summary — 1-2 sentences: what was measured

  Key Findings — bullet points with specific numbers, markdown tables

  Methodology — analysis approach, any data transformations

  Data Tables — markdown tables for key statistics

  Conclusions — factual summary (no interpretation)

---

Definition of done (all must be true before declaring success)
---------------------------------------------------------------

- [ ] `analysis.py` **written** to `insights/data/D{NN}-{task_name}/analysis.py`
      (the canonical, re-runnable script for this task)
- [ ] `analysis.py` **executed** (`python3 analysis.py` ran to completion
      — not merely drafted). The script should produce `report.md` when
      run; any charts are saved as sibling PNGs.
- [ ] `report.md` **exists** in the same folder, is non-empty, and covers the task scope concisely (max ~1000 words)
- [ ] Any charts referenced in the report exist as PNGs in the same folder

Writing `report.md` directly via `Write`/`Edit` without a corresponding
`analysis.py` is a skill failure, not a skill success. The orchestrator's
pre-gate check will flag it and the task will be re-run.

If the task is purely descriptive (no computation worth scripting — rare
at D-level), `analysis.py` still exists as a tiny script that prints the
facts it cites; D-level is specifically the CODE-EXECUTION tier.

Rules
-----

- Use python3 ONLY (never "python")
- Create task folder if it does not exist: `insights/data/D{NN}-{task_name}/`
- Report, code, and charts all live in the SAME folder (one folder per task)
- Report MUST be written to: `insights/data/D{NN}-{task_name}/report.md`
- `analysis.py` MUST be saved AND executed — not inlined in a heredoc that
  writes the report via stdout redirection or `Write`.
- Include specific numbers (counts, percentages, means)
- STAY DESCRIPTIVE — report facts, not interpretations

---

Example tasks
--------------

  understand_columns
    Understand all columns — meaning, types, characteristics, data dictionary.
    1. Load dataset and list all column names
    2. Identify data type of each column
    3. Understand what each column represents
    4. Document column relationships
    5. Create data dictionary

  interpret_observations
    Interpret what each row represents — unit of observation, grain, time dimension.

  describe_missing_values
    Analyze missing value patterns — counts, percentages, systematic vs random.
    1. Calculate missing value counts per column
    2. Identify patterns in missingness
    3. Analyze if missingness correlates with other variables
    4. Recommend handling strategies

  quality_assessment
    Data quality check — duplicates, outliers, type consistency, value ranges.

  col_overview
    Column overview — types, distributions, top values, null rates.
