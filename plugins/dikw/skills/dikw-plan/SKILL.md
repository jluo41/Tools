---
name: dikw-plan
description: "DIKW analysis plan skill. Design a structured DIKW analysis plan based on exploration findings. Use when the user asks to create a plan, design analysis tasks, write a DIKW plan, or says /dikw-plan. Trigger: plan, analysis plan, design tasks, task plan, DIKW plan."
---

Skill: dikw-plan
==================

Design a DIKW analysis plan based on exploration findings.

On invocation, use `$ARGUMENTS` to get the project path and aim.
Read the exploration notes, then write a YAML plan.

---

Steps
-----

1. Find the exploration notes:
   - If `$ARGUMENTS` has a path, use it as project_dir
   - Read `{project_dir}/sessions/{aim}/exploration/explore_notes.md`
   - If not found, ask the user to run /dikw-explore first

2. Design the analysis plan:
   - Based on what the data actually contains
   - 2-3 tasks per DIKW level (D, I, K, W)
   - Each task: name (short_lowercase) + description (specific to this data)

3. Write the plan:
   - Output path: `{project_dir}/sessions/{aim}/plan/plan-raw.yaml`
   - Create parent directories if needed

Required YAML format:

```yaml
goal: <one sentence describing the analysis goal>
D:
  - name: understand_columns
    description: Understand all columns — types, meaning, characteristics
  - name: quality_assessment
    description: Assess data quality — nulls, duplicates, anomalies
I:
  - name: statistical_summary
    description: Distributions, central tendencies, variability measures
  - name: correlation_analysis
    description: Identify relationships between variables
K:
  - name: rule_extraction
    description: Extract rules, principles, causal relationships
W:
  - name: strategic_recommendations
    description: Prioritized recommendations based on findings
```

---

Rules
-----

- 2-3 tasks per level (no more)
- Task names: short lowercase with underscores (e.g., col_overview)
- NO session prefix in task names — they are project-wide, reusable
- Base the plan on what explore_notes.md actually found, not generic templates
- Each task description should be specific to THIS dataset
