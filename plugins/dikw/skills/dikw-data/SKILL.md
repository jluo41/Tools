---
name: dikw-data
description: "DIKW D-level data analysis skill. Read raw data, write Python analysis code, produce report. Use when the user asks to run a D-level task, analyze data, run data analysis, profile columns, check quality, or says /dikw-data. Trigger: data analysis, D-level, data task, analyze data, column analysis, quality check."
---

Skill: dikw-data
==================

D-level data analysis. Read raw data, write Python analysis code, produce report.

On invocation, use `$ARGUMENTS` to get: task_name, project path, source_dir.
Format: `/dikw-data <task_name> [project_dir]`


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
  Reads: raw data files in source/raw/ ONLY
  Context: none (D is the first analysis level)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS` (e.g., "col_overview")
   - project_dir: from args or cwd
   - source_dir: `{project_dir}/source/raw/`

2. Check if report already exists:
   - Path: `{project_dir}/reports/data/{task_name}.md`
   - If exists and >100 bytes: print "Report exists, skipping." and stop

3. Read and analyze data:
   - List files in source_dir
   - Read data with python3 and pandas
   - Perform the analysis (based on task_name)

4. Save code:
   - Create `{project_dir}/code/data/{task_name}/`
   - Save all Python scripts there
   - Save charts as PNG there

5. Write report:
   - Path: `{project_dir}/reports/data/{task_name}.md`
   - Minimum 300 words

Report format:

  Task Summary — 1-2 sentences: what was measured

  Key Findings — bullet points with specific numbers, markdown tables

  Methodology — analysis approach, any data transformations

  Data Tables — markdown tables for key statistics

  Conclusions — factual summary (no interpretation)

---

Rules
-----

- Use python3 ONLY (never "python")
- Create code directory if it does not exist
- Report MUST be written to: reports/data/{task_name}.md
- Include specific numbers (counts, percentages, means)
- Save chart PNGs to code/data/{task_name}/
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
