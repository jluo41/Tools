---
name: dikw-context
description: "DIKW context engineering skill. Load context + evaluate readiness for a specific task. Decides: READY (execute), BLOCKED (fix first), or SKIP (unnecessary). Use when preparing context for a DIKW task, checking if a task can proceed, or says /dikw-context. Trigger: load context, build context, evaluate task, can we proceed, context for task, is this task ready."
argument-hint: [task_type] [task_name] [project_dir]
---

# DIKW Context Builder + Evaluator

Two jobs in one:
  1. BUILD a focused context package for a specific task
  2. EVALUATE whether the task should execute, be blocked, or be skipped

Every task goes through /dikw-context BEFORE execution.
The evaluation decides what happens next.

## Arguments: $ARGUMENTS

Parse: task_type (explore/plan/D/I/K/W/review/report), task_name, project_dir.


## The Flow

```
/dikw-context {task_type} {task_name} {project_dir}
    |
    ├── Step 1-5: Load 6 context layers (question, plan, reports, ...)
    |
    ├── Step 6: EVALUATE readiness
    |     |
    |     ├── READY    → context sufficient, execute the task
    |     ├── BLOCKED  → context reveals a gap, fix before executing
    |     └── SKIP     → task unnecessary, move to next
    |
    └── Output: context package + evaluation verdict
```

/dikw-session uses the verdict to decide:
  READY   → run /dikw-{level} {task_name}
  BLOCKED → update plan (add task, go back, revise), then re-evaluate
  SKIP    → mark task as skipped, move to next task


## What This Skill Produces

A structured CONTEXT PACKAGE with 6 layers + an EVALUATION verdict:

```
CONTEXT FOR: {task_type} task "{task_name}"
═══════════════════════════════════════════

QUESTION:
  {the original research question from the session}

PLAN CONTEXT:
  {this task's entry from plan-raw.yaml — name + description}

SESSION STATE:
  {phase, completed tasks, pending tasks, revisions}

RELEVANT PRIOR REPORTS:
  {selected and summarized reports from prior levels}

DATA CONTEXT:
  {from explore notes — data overview relevant to this task}

GATE HISTORY:
  {prior gate decisions, gaps found, tasks added}
```

---

## Steps

### Step 1: Read Session Foundation

Read these files (they always exist if session is running):

```
{project_dir}/sessions/{aim}/DIKW_STATE.json     → session state
{project_dir}/sessions/{aim}/plan/plan-raw.yaml   → the plan
{project_dir}/sessions/{aim}/exploration/explore_notes.md → data context
```

Extract:
  - question (from DIKW_STATE.json or plan goal)
  - current phase and completed/pending tasks
  - this task's plan entry (name + description)

### Step 2: Select Relevant Reports

Based on the task_type, decide which prior reports to include:

```
task_type=explore:
  reports: none (nothing exists yet)

task_type=plan:
  reports: none (explore notes are the input, handled separately)

task_type=D:
  reports: other D reports that already exist (avoid duplicate work)
  relevance: ALL existing D reports (same level = always relevant)

task_type=I:
  reports: RELEVANT D reports (not all)
  relevance: match task description keywords against D report titles
  example: I "arm_effectiveness" → include D "engagement_baseline" (topic: arms)
           but skip D "data_quality" (topic: nulls, not arms)

task_type=K:
  reports: RELEVANT D + I reports (summarized)
  relevance: keyword matching + include any report mentioned in plan

task_type=W:
  reports: RELEVANT D + I + K reports (summarized)
  relevance: keyword matching + all K reports (K is always relevant to W)

task_type=review:
  reports: ALL reports from the level being reviewed (full text)
  + the full plan (all levels, not just current)

task_type=report:
  reports: ALL reports across all levels (summarized to key findings)
```

### Step 3: Summarize Long Reports

For each selected report:

```
if report < 2KB:
  include FULL TEXT

if report 2KB - 10KB:
  include:
    - first paragraph (task summary)
    - lines containing numbers, percentages, p-values
    - markdown table headers + first 5 rows
    - bullet points with "key finding", "conclusion"
  skip:
    - methodology details
    - code references
    - verbose descriptions

if report > 10KB:
  include KEY FINDINGS ONLY:
    - first 3 sentences
    - all lines with statistical results
    - conclusion section
```

Target: ~500 words per summarized report.

### Step 4: Read Gate History

If any gate reviews exist in sessions/{aim}/gates/:

```
Read each gate_{level}.md
Extract: decision (PROCEED/ADD_TASKS/GO_BACK/REVISE), reason, new tasks
```

Include gate history if:
  - Current task was ADDED by a gate (explain why it exists)
  - A GO_BACK happened (explain what was wrong)
  - Plan was REVISED (explain what changed)

Skip gate history if:
  - All gates said PROCEED with no issues (nothing interesting)

### Step 5: Assemble the Context Package

Combine all layers into a structured text block.

### Step 6: EVALUATE Readiness

Given the assembled context, evaluate: can this task execute successfully?

Check these conditions:

```
READY conditions (ALL must be true):
  ✓ Task description is clear (plan entry exists)
  ✓ Required input data exists (source/raw/ has files, or prior reports exist)
  ✓ Prior-level reports provide what this task needs
  ✓ No blocking gaps identified in the context
  ✓ Task hasn't already been completed (report doesn't already exist)

BLOCKED conditions (ANY one triggers BLOCKED):
  ✗ A prior report says "needs X" but no task produced X
    Example: dedup_analysis says "use deduped data" but no clean dataset exists
  ✗ Task description references data that doesn't exist
    Example: plan says "compare arms" but no arm column found in D reports
  ✗ A gate decision says GO_BACK but the fix hasn't been done yet
  ✗ Context reveals the task's approach won't work
    Example: task says "run correlation" but D reports show only 1 numeric column

SKIP conditions (ANY one triggers SKIP):
  ○ Report already exists at the output path (and >100 bytes)
  ○ A prior task in this session already covered this analysis
  ○ The plan was revised and this task is no longer in the current plan
  ○ A gate explicitly marked this task as unnecessary
```

Produce the verdict:

```
EVALUATION:
  Verdict: READY | BLOCKED | SKIP
  Reason: {one sentence explaining why}
  Action: {what to do next}

  If BLOCKED:
    Blocker: {specific gap or missing prerequisite}
    Fix: ADD_TASKS {task_name} | GO_BACK {level} | REVISE_PLAN
    Fix description: {what needs to happen before this task can run}

  If SKIP:
    Skip reason: {why this task is unnecessary}
    Existing output: {path to existing report, if applicable}
```


### Output

Print both the context package AND the evaluation:

```
CONTEXT FOR: {task_type} task "{task_name}"
═══════════════════════════════════════════

QUESTION: ...
PLAN CONTEXT: ...
SESSION STATE: ...
RELEVANT PRIOR REPORTS: ...
DATA CONTEXT: ...
GATE HISTORY: ...

───────────────────────────────────────────
EVALUATION:
  Verdict: READY
  Reason: All prior D reports provide sufficient context for this I task.
  Action: Execute /dikw-information arm_effectiveness
───────────────────────────────────────────
```

---

## How /dikw-session Uses the Verdict

```
for each task in plan:

    result = /dikw-context {task_type} {task_name} {project_dir}

    if result.verdict == READY:
        run /dikw-{level} {task_name}    # execute the task
        continue to next task

    elif result.verdict == BLOCKED:
        if result.fix == ADD_TASKS:
            add the suggested task to the plan
            run the new task first
            re-evaluate the original task
        elif result.fix == GO_BACK:
            go back to the specified level
            run the fix task
            come back and re-evaluate
        elif result.fix == REVISE_PLAN:
            run /dikw-plan with feedback
            restart from appropriate level

    elif result.verdict == SKIP:
        mark task as skipped in DIKW_STATE.json
        continue to next task
```

---

## Context Budget (target sizes)

```
task_type    target words    what's included
─────────    ────────────    ───────────────
explore      300             question + data file listing
plan         500             question + full explore notes
D            1000            question + plan entry + data context + other D reports
I            1500            question + plan entry + relevant D summaries
K            2000            question + plan entry + relevant D+I summaries
W            2500            question + plan entry + relevant D+I+K summaries
review       3000            question + full plan + full reports from current level
report       4000            question + summaries of ALL levels
```

These are targets. Better to include a critical finding than to trim for size.

---

## Relevance Matching

How to decide if a prior report is relevant to the current task:

```python
# Pseudo-code for relevance matching
def is_relevant(task_description, report_title, report_content):
    task_keywords = extract_keywords(task_description)
    report_keywords = extract_keywords(report_title + first_paragraph(report_content))
    overlap = task_keywords & report_keywords
    return len(overlap) >= 2  # at least 2 shared keywords

def extract_keywords(text):
    # Remove stopwords, extract nouns and domain terms
    # Examples: "engagement", "arm", "patient", "click", "segment"
    ...
```

When in doubt: INCLUDE the report. Missing context is worse than extra context.

---

## How Other Skills Use This

/dikw-session calls /dikw-context before each task:

```
For each task:
  1. /dikw-context {task_type} {task_name} {project_dir}
     → produces context package (printed to stdout)
  2. Prepend context package to the skill prompt
  3. /dikw-{level} {task_name} {project_dir}
     → skill runs with full context awareness
```

In Claude Code (local):
  /dikw-session runs /dikw-context internally.
  Context package is part of the conversation.

On Mattermost (cloud):
  EXEC-bot's load_context node runs this logic.
  Context package is included in the kickoff message to Claude Code.

---

## Example Context Packages

### For D task "engagement_baseline":

```
CONTEXT FOR: D task "engagement_baseline"
═══════════════════════════════════════════

QUESTION:
  How to improve engagement for low-engagement patients?

PLAN CONTEXT:
  engagement_baseline: Baseline click/auth/optout rates by arm.
  Part of D-level (2 tasks total: dedup_analysis, engagement_baseline).

SESSION STATE:
  Phase D, task 2 of 2. dedup_analysis complete.

RELEVANT PRIOR REPORTS:
  D "dedup_analysis" (full, 1.2KB):
    4,243 of 10,000 rows are exact duplicates (42.4%).
    Caused by retry mechanism. 5,757 unique invitations.
    Recommendation: use deduped data for accurate metrics.

DATA CONTEXT:
  10K rows, 96 cols. 13 message arms. Key cols: patient_id,
  invitation_id, message, clicked, authenticated, opted_out.

GATE HISTORY:
  (no prior gates — this is the first level)

───────────────────────────────────────────
EVALUATION:
  Verdict: READY
  Reason: dedup_analysis complete. Raw data available. Task can proceed.
  Action: Execute /dikw-data engagement_baseline
───────────────────────────────────────────
```


### For I task "arm_effectiveness":

```
CONTEXT FOR: I task "arm_effectiveness"
═══════════════════════════════════════════

QUESTION:
  How to improve engagement for low-engagement patients?

PLAN CONTEXT:
  arm_effectiveness: Compare 13 arms statistically (chi-square, effect sizes).
  Part of I-level (2 tasks: arm_effectiveness, patient_segmentation).

SESSION STATE:
  Phase I, task 1 of 2. D complete (3 tasks).

RELEVANT PRIOR REPORTS:
  D "engagement_baseline" (summary):
    13 arms, click rates 38-67%. Top: authority (67%), emotionalCue (62%).
    Bottom: timeliness (38%). Overall: 57.8% click, 23.1% auth.

  D "dedup_analysis" (summary):
    42% dupes from retry. Use 5,757 unique invitations for accurate counts.

  (skipped: D "null_handling_strategy" — topic: nulls, not relevant to arm comparison)

DATA CONTEXT:
  10K rows, 96 cols. 13 arms. 3,608 unique patients.

GATE HISTORY:
  Gate D: PROCEED. All D tasks sufficient. One task added by gate
  (null_handling_strategy) but not relevant to this I task.

───────────────────────────────────────────
EVALUATION:
  Verdict: READY
  Reason: D reports provide arm-level engagement data. Sufficient for comparison.
  Action: Execute /dikw-information arm_effectiveness
───────────────────────────────────────────
```


### For K task "behavioral_drivers":

```
CONTEXT FOR: K task "behavioral_drivers"
═══════════════════════════════════════════

QUESTION:
  How to improve engagement for low-engagement patients?

PLAN CONTEXT:
  behavioral_drivers: Why do some arms outperform? Causal mechanisms.
  Only K task. Should synthesize all D+I findings.

SESSION STATE:
  Phase K, task 1 of 1. D complete (3 tasks), I complete (2 tasks).

RELEVANT PRIOR REPORTS:
  D "engagement_baseline" (summary):
    13 arms, click rates 38-67%. authority=67%, timeliness=38%.

  I "arm_effectiveness" (summary):
    authority vs default: chi-sq=45.2, p<0.001, V=0.19.
    3 arms outperform default (p<0.01). timeliness underperforms (p=0.03).

  I "patient_segmentation" (summary):
    3 segments: High (23%, age>50, authority works), Medium (35%, mixed,
    emotionalCue works), Low (42%, younger, no arm helps significantly).

DATA CONTEXT:
  SMS experiment. 13 behavioral nudge arms. 3,608 patients.

GATE HISTORY:
  Gate D: PROCEED.
  Gate I: PROCEED. Strong statistical evidence. Segments clear.

───────────────────────────────────────────
EVALUATION:
  Verdict: READY
  Reason: D+I reports provide strong statistical evidence and clear segments.
          Sufficient for causal synthesis.
  Action: Execute /dikw-knowledge behavioral_drivers
───────────────────────────────────────────
```


### BLOCKED example — I task needs deduped data that doesn't exist:

```
CONTEXT FOR: I task "arm_effectiveness"
═══════════════════════════════════════════

QUESTION:
  How to improve engagement for low-engagement patients?

PLAN CONTEXT:
  arm_effectiveness: Compare 13 arms statistically.

SESSION STATE:
  Phase I, task 1 of 2. D complete (2 tasks).

RELEVANT PRIOR REPORTS:
  D "dedup_analysis" (full):
    42% duplicates found. "Use deduped data for accurate metrics."
    ⚠️ No deduped dataset was created. Only raw data exists.

  D "engagement_baseline" (full):
    Computed on raw data (10K rows including duplicates).
    ⚠️ These numbers are inflated by duplicate counting.

DATA CONTEXT:
  Only source/raw/df_etl_sample.parquet exists (with duplicates).
  No cleaned/deduped version available.

───────────────────────────────────────────
EVALUATION:
  Verdict: BLOCKED
  Reason: dedup_analysis says "use deduped data" but no deduped dataset exists.
          engagement_baseline was computed on duplicated data (numbers unreliable).
          Running arm comparison on this data would produce wrong results.

  Blocker: No deduped dataset available
  Fix: ADD_TASKS
  Fix task: D "create_deduped_dataset" — deduplicate by invitation_id,
            save clean parquet, recompute engagement_baseline on clean data.
───────────────────────────────────────────
```


### SKIP example — report already exists from prior session:

```
CONTEXT FOR: D task "col_overview"
═══════════════════════════════════════════

QUESTION:
  How to improve engagement for low-engagement patients?

SESSION STATE:
  Phase D, task 1 of 3. No tasks complete yet.

CHECK:
  reports/data/col_overview.md exists (4.2KB, from prior session run0)

───────────────────────────────────────────
EVALUATION:
  Verdict: SKIP
  Reason: Report already exists at reports/data/col_overview.md (4.2KB).
          Produced by a prior session. Still valid for this project.
  Skip reason: Prior session already completed this task.
  Existing output: reports/data/col_overview.md
───────────────────────────────────────────
```

---

## Rules

- ALWAYS include the question (Layer 1) — it shapes everything
- ALWAYS include the plan entry (Layer 2) — the task needs to know its purpose
- SELECT relevant reports, don't dump everything
- SUMMARIZE long reports — extract findings, skip methodology
- When in doubt, INCLUDE — missing context is worse than extra context
- Context package should be READABLE — a human should understand it too
