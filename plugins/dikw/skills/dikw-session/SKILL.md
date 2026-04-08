---
name: dikw-session
description: "Full DIKW analysis session. Chains explore → plan → D → I → K → W → report with review gates between each level. Handles iteration: go back, add tasks, revise plan. Use when user says 'run DIKW', 'full analysis', 'DIKW session', 'analyze this dataset end-to-end', or /dikw-session. Trigger: DIKW session, full analysis, end-to-end analysis, analyze dataset."
argument-hint: [project_dir] [questions]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
---

# DIKW Analysis Session

End-to-end DIKW analysis pipeline for: **$ARGUMENTS**

## Constants

- **AUTO_PROCEED = true** — When true, gate reviews auto-decide (like aris). When false, pause at each gate for human input.
- **MAX_REVISIONS = 3** — Maximum number of plan revisions before forcing forward.
- **MAX_TASKS_PER_LEVEL = 4** — Cap tasks per level to control scope.

> Override: `/dikw-session "questions" — AUTO_PROCEED: false, MAX_TASKS_PER_LEVEL: 2`

## Overview

```
/dikw-explore → /dikw-plan → /dikw-data → /dikw-information → /dikw-knowledge → /dikw-wisdom → /dikw-report
                    ↑              ↑              ↑                ↑                ↑
                    └──── /dikw-review gates ─────┴────────────────┴────────────────┘
                          (can go back, add tasks, or revise plan at any gate)
```

This skill orchestrates the full DIKW lifecycle, calling sub-skills and review
gates. It handles iteration: if a gate review says "go back" or "add tasks",
the session loops back and re-runs the needed work.

## State File

Persist state to `{project_dir}/sessions/{aim}/DIKW_STATE.json` after every phase.
This survives context compaction and allows resuming.

```json
{
  "status": "running",
  "current_phase": "I",
  "plan_version": 1,
  "aim": "run1",
  "questions": "What patterns exist in this DrFirst dataset?",
  "completed_tasks": {
    "D": ["col_overview", "quality_check"],
    "I": []
  },
  "pending_tasks": {
    "I": ["statistical_summary", "correlation_analysis"]
  },
  "gates": [],
  "revisions": [],
  "round": 1
}
```

**On startup:** Check if DIKW_STATE.json exists. If so, RESUME from where we left off.
Do not re-run completed tasks.

## Pipeline

### Phase 0: Setup

1. Determine project_dir from `$ARGUMENTS` or cwd
2. Determine aim name (from args, or use "run1")
3. Create session directory: `{project_dir}/sessions/{aim}/`
4. Check for existing DIKW_STATE.json — if found, resume

### Phase 1: Explore

```
/dikw-explore {project_dir}
```

Output: `sessions/{aim}/exploration/explore_notes.md`

**Gate 0:** Read explore notes. Is the data understood?
- If data files couldn't be read or notes are empty → re-explore with different approach
- If good → proceed to plan

Update DIKW_STATE.json: `"current_phase": "plan"`

### Phase 2: Plan

```
/dikw-plan {project_dir}
```

Output: `sessions/{aim}/plan/plan-raw.yaml`

**Gate 1 — Human Checkpoint:**

Present the plan:
```
📋 DIKW Plan (version {N}):

Goal: {goal from yaml}
D: {list tasks}
I: {list tasks}
K: {list tasks}
W: {list tasks}

Total: {N} tasks across 4 levels.
Proceed? (yes / revise: "feedback" / skip levels)
```

If AUTO_PROCEED=true: auto-approve after presenting.
If AUTO_PROCEED=false: wait for human.

Human can:
- **Approve** → proceed to D
- **Revise** → pass feedback to `/dikw-plan`, re-generate, re-present
- **Skip levels** → mark levels as skipped, proceed
- **Add/remove tasks** → modify plan yaml directly

Update DIKW_STATE.json with plan and pending tasks.

### Phase 3: Execute Levels (D → I → K → W)

For each level in [D, I, K, W] (unless skipped):

```
for level in [D, I, K, W]:
    if level is skipped:
        continue

    tasks = plan[level]  # or pending_tasks from state

    for task in tasks:
        if task already completed (report exists):
            skip

        # Run the appropriate skill
        if level == "D":
            /dikw-data {task.name} {project_dir}
        elif level == "I":
            /dikw-information {task.name} {project_dir}
        elif level == "K":
            /dikw-knowledge {task.name} {project_dir}
        elif level == "W":
            /dikw-wisdom {task.name} {project_dir}

        # Update state after each task
        mark task as completed in DIKW_STATE.json

    # ═══ GATE REVIEW after each level ═══
    /dikw-review {project_dir}

    gate_decision = read gate review result

    if gate_decision == "PROCEED":
        continue to next level

    elif gate_decision == "ADD_TASKS":
        add new tasks to current level in plan
        re-run current level (only new tasks)
        re-run gate review

    elif gate_decision == "GO_BACK":
        go back to specified level
        run the new tasks there
        then re-run from that level forward

    elif gate_decision == "REVISE_PLAN":
        increment plan_version
        /dikw-plan {project_dir} — with revision feedback
        restart from the appropriate level
        (check MAX_REVISIONS — if exceeded, force proceed)

    elif gate_decision == "DONE":
        skip remaining levels, go to report
```

### Phase 4: Report

```
/dikw-report {project_dir} {aim}
```

Output: `sessions/{aim}/output/final_output.md`

**Gate 6 — Final Check:**
- Read the final report
- Does it answer the original questions?
- If gaps remain and we haven't exceeded MAX_REVISIONS → go back
- Otherwise → done

### Phase 5: Complete

Update DIKW_STATE.json: `"status": "completed"`

Print summary:
```
✅ DIKW Session Complete

Project: {project}
Aim: {aim}
Questions: {questions}

Reports produced:
  D: {list with paths}
  I: {list}
  K: {list}
  W: {list}
  Final: sessions/{aim}/output/final_output.md

Revisions: {N} plan revisions
Gates: {N} gate reviews, {N} go-backs, {N} added tasks

Read the final report: {path}
```

---

## Iteration Patterns (how backtracking works)

### Pattern 1: Add tasks to current level

```
D tasks complete → Gate review → "click_rate nulls not handled"
→ ADD_TASKS: null_imputation_strategy
→ Run /dikw-data null_imputation_strategy
→ Gate review again → PROCEED
→ Continue to I
```

### Pattern 2: Go back to prior level

```
I tasks complete → Gate review → "D never profiled the time column"
→ GO_BACK to D: time_dimension_profile
→ Run /dikw-data time_dimension_profile
→ Gate review D → PROCEED
→ Re-run I tasks that depend on time data (or all I tasks if unclear)
→ Gate review I → PROCEED
→ Continue to K
```

### Pattern 3: Revise plan

```
D tasks complete → Gate review → "Data is 42% duplicates.
  The plan assumed clean data. All I/K/W tasks are based on wrong counts."
→ REVISE_PLAN: "Must deduplicate first. I tasks need to use deduped data."
→ /dikw-plan with feedback → plan-raw-v2.yaml
→ Present new plan to human
→ Run D tasks from new plan (skip already-done tasks that are still valid)
→ Continue through I/K/W with new plan
```

### Pattern 4: Skip to report

```
I tasks complete → Gate review → "Patterns are clear and actionable.
  K/W synthesis won't add much — the findings speak for themselves."
→ DONE: skip K, W
→ /dikw-report (synthesizes from D + I only)
```

---

## Recovery from Context Compaction

If context is compacted mid-session:

1. Read DIKW_STATE.json — know where we are
2. Read the latest gate review — know what was decided
3. Resume from the current_phase with pending_tasks
4. Do NOT re-run completed tasks (check report file existence)

---

## Rules

- ALWAYS update DIKW_STATE.json after every task and gate
- NEVER re-run a task whose report already exists (unless gate says GO_BACK with explicit re-run)
- Present gate decisions clearly — human should understand why
- If MAX_REVISIONS exceeded, force PROCEED with a warning
- If a skill fails (claude -p error), retry once, then mark task as failed and continue
- The final report MUST address the original questions — if it doesn't, the gate catches it
- Save all gate reviews to sessions/{aim}/gates/ for audit trail

---

## Estimated Duration

| Phase | Time | Interactive? |
|---|---|---|
| Explore | 2-5 min | Auto |
| Plan | 1-2 min | Gate (human approves) |
| D tasks (2-3) | 3-8 min each | Auto, gate after |
| I tasks (2-3) | 3-8 min each | Auto, gate after |
| K tasks (1-2) | 2-5 min each | Auto, gate after |
| W tasks (1-2) | 2-5 min each | Auto, gate after |
| Report | 3-5 min | Final gate |
| **Total** | **30-60 min** | **Gates at each level** |

With AUTO_PROCEED=true, the entire session runs unattended.
With AUTO_PROCEED=false, human reviews at each gate (~5 gates).
