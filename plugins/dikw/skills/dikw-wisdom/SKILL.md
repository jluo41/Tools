---
name: dikw-wisdom
description: "DIKW W-level wisdom skill. Strategic recommendations, action items, decisions based on all DIKW findings. Use when the user asks to run a W-level task, make recommendations, create strategy, write action items, or says /dikw-wisdom. Trigger: wisdom, W-level, recommendations, strategy, action items, decisions, best practices."
---

Skill: dikw-wisdom
====================

Runs during **`step=task`** of **`phase=W`**, once per W-task.
W-level wisdom synthesis: strategic recommendations and action items.

On invocation, use `$ARGUMENTS` to get: task_name, snapshot_dir.
Format: `/dikw-wisdom <task_name> [snapshot_dir]`


DIKW Boundary — What W-level IS and IS NOT
--------------------------------------------

  W-level answers: WHAT SHOULD WE DO about it?

  W IS:
    - Recommending specific actions (with expected impact)
    - Prioritizing decisions by impact and feasibility
    - Identifying trade-offs and risks of each option
    - Creating decision frameworks based on K-level principles
    - Producing actionable guidelines (not abstract advice)
    - Judging which findings matter most for the stakeholder

  W IS NOT:
    - Analyzing raw data (that's D)
    - Finding patterns (that's I)
    - Explaining causation (that's K)
    - Executing the recommendations (that's the Human's job)

  W output is DECISIONS: "disable retry mechanism for confirmed deliveries
    to reduce 42% duplication — estimated 30% cost savings, low risk"
  NOT explanations: "duplicates are caused by retries"
  NOT patterns: "duplication correlates with message_type"

  Execution mode: LLM REASONING (reads all prior reports, no code execution)
  Reads: D-level + I-level + K-level reports
  Context sources: insights/data/*/report.md + insights/information/*/report.md
    + insights/knowledge/*/report.md
  Does NOT read: raw data files

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS`
   - snapshot_dir: from args or cwd

2. Resolve the task folder name (W-level prefix is `W` + NN, e.g. W01, W02):
   - List existing `{snapshot_dir}/insights/wisdom/*/` folders
   - If one matches `W*-{task_name}/` → reuse (re-run)
   - Else → assign NN = next available two-digit index within the W-level
     (01, 02, …) and form folder name `W{NN}-{task_name}` (W01, W02, …)
   - Task folder: `{snapshot_dir}/insights/wisdom/W{NN}-{task_name}/`
     (example: `insights/wisdom/W01-recommendations/`)

3. Check if report already exists:
   - Path: `{snapshot_dir}/insights/wisdom/W{NN}-{task_name}/report.md`
   - If exists and >100 bytes: skip

4. Read all prior reports:
   - ALL D-level: `{snapshot_dir}/insights/data/*/report.md`
   - ALL I-level: `{snapshot_dir}/insights/information/*/report.md`
   - ALL K-level: `{snapshot_dir}/insights/knowledge/*/report.md`

5. Produce strategic recommendations:
   - Prioritize by impact and feasibility
   - Ground in evidence from K-level insights

6. Write report:
   - Path: `{snapshot_dir}/insights/wisdom/W{NN}-{task_name}/report.md`
   - Minimum 400 words

Report format:

  Executive Recommendations — top 3-5, ranked by impact
    Each with: specific action, rationale, expected impact, effort level

  Strategic Opportunities — what can be done with these findings

  Decision Points — key decisions with trade-offs and recommended paths

  Risk Assessment — risks of acting vs not acting

  Implementation Guidelines — practical steps for top recommendations

  Limitations — what the analysis cannot support

---

Rules
-----

- Read ALL D, I, K reports before writing
- Every recommendation grounded in K-level evidence
- No new data analysis — reason from existing findings
- Be SPECIFIC: "increase X by doing Y" not "consider improving X"
- Include expected impact and effort for each recommendation
- W task folders contain only `report.md` (no code, no charts)
- Report MUST be written to: `insights/wisdom/W{NN}-{task_name}/report.md`

---

Example tasks
--------------

  strategic_recommendations
    Prioritized recommendations based on knowledge synthesis.

  decision_framework
    Decision-making framework with criteria, pathways, trade-offs.

  best_practices
    Best practices and implementation guidelines.
