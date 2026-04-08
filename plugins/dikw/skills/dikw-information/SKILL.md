---
name: dikw-information
description: "DIKW I-level information extraction skill. Extract patterns, correlations, statistical insights from data. Use when the user asks to run an I-level task, extract patterns, find correlations, run statistics, or says /dikw-information. Trigger: information extraction, I-level, patterns, correlations, statistics, outliers, segments."
---

Skill: dikw-information
========================

I-level information extraction. Extract patterns, correlations, statistical insights.

On invocation, use `$ARGUMENTS` to get: task_name, project path.
Format: `/dikw-information <task_name> [project_dir]`


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
  Reads: raw data in source/raw/ + D-level reports for context
  Context sources: reports/data/ (understand what D found before extracting patterns)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS`
   - project_dir: from args or cwd
   - source_dir: `{project_dir}/source/raw/`

2. Check if report already exists:
   - Path: `{project_dir}/reports/information/{task_name}.md`
   - If exists and >100 bytes: print "Report exists, skipping." and stop

3. Read context:
   - Read D-level reports from `{project_dir}/reports/data/` for context
   - Read raw data from source_dir

4. Extract patterns:
   - Use statistical methods appropriate to the task
   - Build on D-level findings (don't repeat D-level work)

5. Save code:
   - Create `{project_dir}/code/information/{task_name}/`
   - Save Python scripts and chart PNGs

6. Write report:
   - Path: `{project_dir}/reports/information/{task_name}.md`
   - Minimum 300 words

Report format:

  Task Summary — what patterns were looked for

  Statistical Findings — metrics with p-values, effect sizes

  Visualizations — reference saved charts

  Pattern Description — named patterns with quantitative evidence

  Implications — what patterns suggest (but NOT recommendations)

---

Rules
-----

- Use python3 ONLY
- Read D-level reports FIRST for context
- Include statistical significance (p-values) where applicable
- Report MUST be written to: reports/information/{task_name}.md
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
