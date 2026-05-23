---
name: dikw-information
description: "DIKW I-level information extraction skill. Extract patterns, correlations, statistical insights from data. Use when the user asks to run an I-level task, extract patterns, find correlations, run statistics, or says /dikw-information. Trigger: information extraction, I-level, patterns, correlations, statistics, outliers, segments."
---

Skill: dikw-information
========================

Runs during **`step=task`** of **`phase=I`**, once per I-task.
I-level information extraction: patterns, correlations, statistical insights.

On invocation, use `$ARGUMENTS` to get: task_name, snapshot_dir.
Format: `/dikw-information <task_name> [snapshot_dir]`


DIKW Boundary — What I-level IS and IS NOT
--------------------------------------------

  I-level answers: WHAT PATTERNS exist in the data?

  I IS:
    - Finding correlations between variables (r values, p-values)
    - Detecting statistical patterns (trends, clusters, segments)
    - Running hypothesis tests (chi-square, t-test, ANOVA)
    - Detecting outliers with statistical methods (IQR, z-score)
    - Comparing groups and segments quantitatively
    - Writing Python code that computes statistics and produces visualizations

  I IS NOT:
    - Describing basic data properties (that's D-level)
    - Explaining WHY patterns exist (that's K-level)
    - Recommending what to do about patterns (that's W-level)

  I output is PATTERNS: "message_type correlates with click_rate (r=0.7, p<0.01)"
  NOT explanations: "the correlation is because longer messages engage users better"
  NOT recommendations: "use message_type B for better engagement"

  Execution mode: CODE EXECUTION (write and run Python scripts)
  Reads: raw data in source/ + D-level reports for context
  Context sources: insights/data/*/report.md (understand what D found)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS`
   - snapshot_dir: from args or cwd
   - source_dir: `{snapshot_dir}/source/`

2. Resolve the task folder name (I-level prefix is `I` + NN, e.g. I01, I02):
   - List existing `{snapshot_dir}/insights/information/*/` folders
   - If one matches `I*-{task_name}/` → reuse (re-run)
   - Else → assign NN = next available two-digit index within the I-level
     (01, 02, …) and form folder name `I{NN}-{task_name}` (I01, I02, I03, …)
   - Task folder: `{snapshot_dir}/insights/information/I{NN}-{task_name}/`
     (example: `insights/information/I01-glycemic_metrics/`)

3. Check if report already exists:
   - Path: `{snapshot_dir}/insights/information/I{NN}-{task_name}/report.md`
   - If exists and non-empty: print "Report exists, skipping." and stop

4. Read context:
   - Read D-level reports from `{snapshot_dir}/insights/data/*/report.md`
   - Read raw data from source_dir

5. Extract patterns:
   - Use statistical methods appropriate to the task
   - Build on D-level findings (don't repeat D-level work)

6. Save code and artifacts:
   - Create `{snapshot_dir}/insights/information/I{NN}-{task_name}/`
   - Save Python scripts (`analysis.py`, additional names if needed)
   - Save chart PNGs in the same folder

7. Write report:
   - Path: `{snapshot_dir}/insights/information/I{NN}-{task_name}/report.md`
   - Concise and accurate; max ~1000 words

Report format:

  Task Summary — what patterns were looked for

  Statistical Findings — metrics with p-values, effect sizes

  Visualizations — reference saved charts (file names relative to the task folder)

  Pattern Description — named patterns with quantitative evidence

  Implications — what patterns suggest (but NOT recommendations)

---

Definition of done (all must be true before declaring success)
---------------------------------------------------------------

- [ ] `analysis.py` **written** to `insights/information/I{NN}-{task_name}/analysis.py`
- [ ] `analysis.py` **executed** (`python3 analysis.py` ran to completion)
- [ ] `report.md` **exists** in the same folder, is non-empty, and covers the task scope concisely (max ~1000 words)
- [ ] Any charts referenced in the report exist as PNGs in the same folder

Writing `report.md` directly without a corresponding `analysis.py` is a
skill failure. I-level is a CODE-EXECUTION tier (like D); the orchestrator's
pre-gate check will flag a missing `analysis.py` and re-run the task.

Rules
-----

- Use python3 ONLY
- Read D-level reports FIRST for context: `insights/data/*/report.md`
- Include statistical significance (p-values) where applicable
- Report, code, charts all live in `insights/information/I{NN}-{task_name}/`
- `analysis.py` MUST be saved AND executed — not inlined in a heredoc.
- STAY ANALYTICAL — report patterns, not explanations or recommendations

---

Example tasks
--------------

  statistical_summary
    Comprehensive statistical summaries — distributions, central tendencies.
    1. Read D-level reports for key column context
    2. Compute descriptive statistics for numeric variables
    3. Generate frequency distributions for categorical variables
    4. Create summary statistics tables

  correlation_analysis
    Identify relationships between variables — correlation matrices, key pairs.
    1. Compute correlation matrix for numeric variables
    2. Identify strongly correlated pairs (|r| > 0.5)
    3. Create correlation heatmap
    4. Document significant correlations with p-values

  outlier_detection
    Detect statistical outliers using IQR and z-score methods.

  segment_analysis
    Segment data by key categorical variables and compare groups.

  trend_analysis
    Time-based patterns, seasonal effects, temporal trends.
