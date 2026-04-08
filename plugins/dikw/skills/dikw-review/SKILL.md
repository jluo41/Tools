---
name: dikw-review
description: "DIKW gate review skill. After each level completes, review results and decide: proceed to next level, add more tasks to current level, go back to a prior level, or revise the plan. Use when the user asks to review DIKW results, check quality of analysis, decide next step, or says /dikw-review. Trigger: review results, gate check, quality check, next step, should we proceed, go back, revise plan."
argument-hint: [project_dir]
---

# DIKW Gate Review

Review completed level results and decide the next action.

This skill is called BETWEEN levels. It reads what was produced, assesses quality,
and recommends one of 5 actions. Called by `/dikw-session` at each gate, or
manually by the user at any point.

## Context: $ARGUMENTS

## Constants

- AUTO_PROCEED = false — When true, auto-decide without waiting for human. When false, present findings and wait.

## What This Skill Does

After a DIKW level completes (e.g., all D tasks done), this skill:

1. Reads ALL reports produced so far
2. Reads the current plan (plan-raw.yaml)
3. Assesses: are the results sufficient for the NEXT level to work?
4. Recommends one of 5 actions
5. If AUTO_PROCEED=false, presents the recommendation and waits for human

## The 5 Gate Actions

```
PROCEED     → Results are sufficient. Move to next level.
ADD_TASKS   → Current level needs more work. Add specific tasks and re-run.
GO_BACK     → A prior level is missing something. Go back and fix it.
REVISE_PLAN → The plan itself needs changes based on what we learned.
DONE        → Analysis is complete. Skip remaining levels, go to report.
```

## Steps

### Step 1: Gather Context

Read the current state:

```
{project_dir}/sessions/{aim}/plan/plan-raw.yaml    — the current plan
{project_dir}/sessions/{aim}/exploration/           — explore notes
{project_dir}/reports/data/*.md                     — D-level reports
{project_dir}/reports/information/*.md              — I-level reports
{project_dir}/reports/knowledge/*.md                — K-level reports
{project_dir}/reports/wisdom/*.md                   — W-level reports
```

Also read DIKW_STATE.json if it exists (for revision history).

### Step 2: Identify the Current Gate

Determine which level just completed by checking which reports exist:

```
If D reports exist but no I reports  → Gate after D
If I reports exist but no K reports  → Gate after I
If K reports exist but no W reports  → Gate after K
If W reports exist                   → Gate after W (go to report)
If no D reports                      → Gate after explore/plan
```

### Step 3: Assess Quality

For each completed level, check:

**Completeness:**
- Did every planned task produce a report?
- Are reports non-trivial (>300 bytes for D/I, >400 for K/W)?
- For D/I: was code produced alongside the report?

**Sufficiency for next level:**
- D→I gate: Does D provide enough data understanding for pattern extraction?
  Check: Are key columns profiled? Are data quality issues documented?
  Check: Does the next I task have the data it needs?

- I→K gate: Does I provide enough patterns for knowledge synthesis?
  Check: Are statistical findings specific (with p-values, effect sizes)?
  Check: Are there enough patterns to synthesize into knowledge?

- K→W gate: Does K provide enough knowledge for recommendations?
  Check: Are causal claims supported with evidence?
  Check: Are knowledge gaps documented?

- W→report gate: Does W provide actionable recommendations?
  Check: Are recommendations specific (not vague)?

**Surprises:**
- Did any task reveal something that changes the plan?
- Was a key assumption invalidated?
- Is there a data quality issue that affects everything?

### Step 4: Produce the Gate Decision

Write the decision to: `{project_dir}/sessions/{aim}/gates/gate_{level}.md`

Format:

```markdown
Gate Review: After {level}
==========================

Completed tasks:
  - D: col_overview ✓ (4.2K), quality_check ✓ (3.8K)

Assessment:
  Completeness: ALL planned tasks produced reports
  Quality: Reports contain specific numbers and tables
  Sufficiency: D reports provide enough for I-level pattern extraction

  Issues found:
  - click_rate column has 42% nulls (not addressed by any D task)
  - No task examined the time dimension (invitation_date)

Decision: ADD_TASKS
Reason: Two gaps need D-level work before I can proceed effectively

New tasks to add:
  D:
    - name: null_imputation_strategy
      description: Analyze click_rate nulls — are they MCAR/MAR/MNAR? Propose handling.
    - name: time_dimension_profile
      description: Profile invitation_date — distribution, range, seasonality.

Plan revision needed: No
```

### Step 5: Present to Human (if AUTO_PROCEED=false)

Print a clear summary:

```
🔍 Gate Review: D-level complete

✅ Completed: col_overview, quality_check
⚠️  Gaps found:
  1. click_rate has 42% nulls — no handling strategy yet
  2. Time dimension (invitation_date) not profiled

📋 Recommendation: ADD_TASKS
  → Add: null_imputation_strategy, time_dimension_profile
  → Then re-run gate review

Proceed with recommendation? (yes / modify / skip to I / revise plan)
```

Wait for human input. If AUTO_PROCEED=true, execute the recommendation automatically.

---

## Gate Decision Logic (detailed)

### PROCEED — move forward

Use when:
- All planned tasks completed with substantial reports
- No critical gaps for the next level
- No surprises that invalidate the plan

### ADD_TASKS — current level needs more

Use when:
- A specific gap was found that THIS level should fill
- The gap is concrete (not vague "needs more analysis")
- The new task(s) can be described precisely

When adding tasks, specify:
- task name and description
- WHY it's needed (what gap it fills)
- Which existing task revealed the gap

### GO_BACK — prior level needs fixing

Use when:
- Current level's work revealed that a PRIOR level missed something
- Example: I-level tried to correlate X with Y, but D never profiled Y
- The fix must happen at the prior level (can't be done at current level)

When going back, specify:
- Which level to go back to
- What task to add there
- WHY current level can't handle it

### REVISE_PLAN — plan needs structural changes

Use when:
- A fundamental assumption changed (e.g., data is completely different than expected)
- The plan's task structure doesn't match the data
- Multiple levels need new tasks (not just one)

When revising, specify:
- What changed and why
- Which parts of the plan are affected
- Suggested new plan structure

### DONE — skip to report

Use when:
- Enough analysis is complete to answer the research questions
- Remaining levels would not add significant value
- The human explicitly says "enough, write the report"

---

## State Update

After the gate decision, update DIKW_STATE.json:

```json
{
  "current_phase": "D",
  "plan_version": 1,
  "completed_tasks": {
    "D": ["col_overview", "quality_check"]
  },
  "pending_tasks": {
    "D": ["null_imputation_strategy", "time_dimension_profile"]
  },
  "gates": [
    {
      "after_level": "D",
      "decision": "ADD_TASKS",
      "reason": "click_rate nulls and time dimension not profiled",
      "new_tasks": ["null_imputation_strategy", "time_dimension_profile"],
      "timestamp": "2026-04-08T10:30:00"
    }
  ],
  "revisions": []
}
```

---

## Rules

- Read ALL available reports before making a decision
- Be specific about gaps — name the column, the missing analysis, the exact issue
- NEVER recommend ADD_TASKS for vague reasons ("needs more analysis")
- Every ADD_TASKS must specify concrete task names and descriptions
- Every GO_BACK must explain why the current level can't fix it
- Gate review file MUST be written to: sessions/{aim}/gates/gate_{level}.md
