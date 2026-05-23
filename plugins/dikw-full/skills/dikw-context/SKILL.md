---
name: dikw-context
description: "DIKW context engineering skill. Load context + evaluate readiness for a specific task. Decides: READY (execute), BLOCKED (fix first), or SKIP (unnecessary). Use when preparing context for a DIKW task, checking if a task can proceed, or says /dikw-context. Trigger: load context, build context, evaluate task, can we proceed, context for task, is this task ready."
argument-hint: [task_type] [task_name] [project_dir]
---

# DIKW Context Builder + Evaluator

Runs inside **`step=task`** of any phase, once per task, BEFORE the task's
phase-skill executes. Two jobs:

  1. BUILD a focused context package for the task
  2. EVALUATE whether the task should execute, be blocked, or be skipped

The evaluation verdict (READY / BLOCKED / SKIP) is a per-task readiness
check — distinct from gate outcomes (approve / revise / done), which are
phase-level and produced by `/dikw-gate` at `step=gate`.

## Arguments: $ARGUMENTS

Parse: `task_type` (one of `plan` | `D` | `I` | `K` | `W` | `report`), `task_name`, `project_dir`.

Note: `task_type=explore` is NOT supported — exploration is a one-time
snapshot-level artifact produced by `/dikw-explore` at `/dikw` Stage 4.5,
before the session starts. `exploration/explore_notes.md` lives at snapshot
level (not under `sessions/{aim}/`) and is READ by this skill as input for
every phase, but never itself produced by a session phase.

Note: `project_dir` is the DIKW snapshot directory — i.e. a
`_agent_dikw_space/snapshot-<date>/` folder produced by `/dikw`. All paths
below are relative to that snapshot.

## Freshness rule (load-every-call)

ALWAYS re-read every input file on every invocation. Never cache across
calls. The context is **incremental by design**: tasks complete, gates fire,
plans revise — and the next call must see all of that. The caller (`/dikw-session`)
does not pass state; it is always re-read from disk.


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

A structured CONTEXT PACKAGE with 8 layers + an EVALUATION verdict:

```
CONTEXT FOR: {task_type} task "{task_name}"     (plan_v{N}, round {M})
═══════════════════════════════════════════════════════════════════════

QUESTION:
  {the original research question from the session}

TRIGGERING GATE:                                  ← only present if this
  gate: G-{X}                                       phase was re-entered
  outcome:  revise {phase} "<feedback>"             via a gate outcome
  plan_version_before → after: {N-1} → {N}          (empty on first entry)

PLAN CONTEXT:
  {this task's entry from plan-raw-v{N}.yaml — name + description}
  {for task_type=plan: the full plan goal + prior plan version if any}

SESSION STATE:
  phase={current}, plan_v{N}, gate={current_gate or —}
  completed: {D:[...], I:[...], K:[...], W:[...]}
  pending:   {...}
  revisions_count: {M}

RELEVANT PRIOR REPORTS:
  {selected & summarized reports from prior levels — per-task_type rules}

DATA CONTEXT:
  {from snapshot-level exploration/explore_notes.md — data overview}

GATE HISTORY:
  {full history of gate outcomes with feedback, ALWAYS included when
   any gates exist; highlights which gate triggered this re-entry}

OUTPUT CONTRACT:
  Write to:   {exact path for this task's report}
  Required:   {what the report MUST contain}
  Format:     {markdown, sections, artifacts}
  Artifacts:  D / I tasks MUST produce BOTH report.md AND analysis.py
              (the saved, executable Python source — not an inlined heredoc).
              K / W tasks produce report.md only (reasoning-only phases).
              Missing artifacts fail the pre-gate artifact check in
              /dikw-session and force a `revise` (back to plan).
```

---

## Steps

### Step 1: Read Session Foundation

Read these files FRESH (they always exist if session is running):

```
{project_dir}/exploration/explore_notes.md             → snapshot-level data context (one-time, shared)
{project_dir}/sessions/{aim}/DIKW_STATE.json           → session state
{project_dir}/sessions/{aim}/plan/plan-raw.yaml        → symlink to latest plan version
{project_dir}/sessions/{aim}/plan/plan-raw-v*.yaml     → all plan versions (for revision history)
{project_dir}/sessions/{aim}/gates/*.md                → all gate outcomes to date (files named {NN}-G-{phase}.md)
```

Extract:
  - question (from DIKW_STATE.json or plan goal)
  - current phase, current_gate, plan_version, revisions_count
  - completed_tasks, pending_tasks
  - gate_persona (locked at session start; pass through unchanged — /dikw-gate reads it)
  - this task's plan entry (name + description) — from plan-raw.yaml
  - the TRIGGERING GATE (if any): the most recent gate whose `routes_to`
    equals the current phase AND fired after the current phase's last
    entry. That gate's `feedback` drives this context. (Field name is
    `routes_to` in `gates[]` — matches the schema in `dikw-session/SKILL.md`
    and what `/dikw-gate` writes; `to_phase` does not exist.)

### Step 2: Select Relevant Reports

Based on the task_type, decide which prior reports to include:

```
task_type=plan:
  plan_version == 1 (initial plan):
    reports: none (explore notes are the only input)
    budget:  ~500 words
  plan_version >= 2 (revised plan — triggered by a gate's `revise plan`):
    reports: ALL existing D+I+K+W reports (summarized, like task_type=report)
    plus:    FULL gate history, with the triggering gate highlighted
    budget:  ~4000 words (matches `report` budget)
    rationale: a revised plan must see everything that was already produced,
      plus the feedback that drove the revision. Otherwise it either repeats
      existing work or misses the gap that triggered the revise.

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

### Step 4: Read Gate History (MANDATORY when gates exist)

Read EVERY gate file in `sessions/{aim}/gates/*.md` — no filtering by
"interestingness". Gate decisions are causal: they determine why the current
phase is running, what tasks were added, and what feedback must be addressed.

For each gate, extract:
  - gate name (`G-plan`, `G-D`, ...)
  - plan_version at time of gate (if applicable)
  - outcome: `approve` | `revise [feedback]` | `done`
  - feedback text (free-form)
  - routes_to (where the outcome routed)
  - timestamp

Always include the full gate history in the context. Additionally:
  - Identify the **TRIGGERING GATE** — the most recent gate whose outcome
    caused the current phase to be (re-)entered. Surface its `feedback` in
    a dedicated TRIGGERING GATE section at the top of the context.
  - If no triggering gate exists (first entry into the phase), omit that
    section but still include the full GATE HISTORY section.

### Step 5: Assemble the Context Package

Combine all layers into a structured text block.

### Step 6: EVALUATE Readiness

Given the assembled context, evaluate: can this task execute successfully?

Check these conditions:

```
READY conditions (ALL must be true):
  ✓ Task description is clear (plan entry exists)
  ✓ Required input data exists (source/ has files, or prior insight reports exist)
  ✓ Prior-level reports provide what this task needs
  ✓ No blocking gaps identified in the context
  ✓ Task hasn't already been completed (report doesn't already exist)

BLOCKED conditions (ANY one triggers BLOCKED):
  ✗ A prior report says "needs X" but no task produced X
    Example: dedup_analysis says "use deduped data" but no clean dataset exists
  ✗ Task description references data that doesn't exist
    Example: plan says "compare arms" but no arm column found in D reports
  ✗ A gate outcome said `revise ...` (back to plan) but the plan re-run
    hasn't produced the needed output yet
  ✗ Context reveals the task's approach won't work
    Example: task says "run correlation" but D reports show only 1 numeric column

SKIP conditions (ANY one triggers SKIP):
  ○ Report already exists at the output path (and is non-empty)
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
    Fix: recommend gate outcome `revise "<feedback>"` (always back to plan);
         `feedback` should describe what plan-v{N+1} needs to add or change
         so the pipeline produces the missing evidence before re-entering
         this phase.
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
        append { name, status: "done", plan_version } to completed_tasks
        continue to next task

    elif result.verdict == BLOCKED:
        # Match the orchestrator contract in dikw-session(-agent)/SKILL.md
        # § "Orchestrator loop": BLOCKED short-circuits the task loop.
        record verdict.reason as the blocker in DIKW_STATE
        break out of the task loop      # do NOT continue to next task
        jump straight to step=gate      # /dikw-gate sees the blocker,
                                        # proposes `revise [feedback]`
                                        # (always routes to plan); plan
                                        # disambiguates missing-task vs
                                        # pending-upstream — see /dikw-plan

    elif result.verdict == SKIP:
        append { name, status: "skipped", plan_version } to completed_tasks
        # NOTE: do NOT leave the task in pending_tasks (the orchestrator
        # removes it from pending_tasks in the same write — see the
        # state schema rule about lists never drifting)
        continue to next task
```

---

## Context Budget (target sizes)

```
task_type            target words    what's included
─────────            ────────────    ───────────────
plan (v1)            500             question + full explore notes
plan (v2+)           4000            question + explore + ALL reports + full gate history
                                      + triggering gate's feedback (highlighted)
D                    1000            question + plan entry + explore + other D reports
I                    1500            question + plan entry + explore + relevant D summaries
K                    2000            question + plan entry + relevant D+I summaries
W                    2500            question + plan entry + relevant D+I+K summaries
report               4000            question + summaries of ALL levels + full gate history
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
  Gate G-D: approve. All D tasks sufficient. One task added by a prior gate
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
  Gate G-D: approve.
  Gate G-I: approve. Strong statistical evidence. Segments clear.

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
  Only source/df_etl_sample.parquet exists (with duplicates).
  No cleaned/deduped version available.

───────────────────────────────────────────
EVALUATION:
  Verdict: BLOCKED
  Reason: dedup_analysis says "use deduped data" but no deduped dataset exists.
          engagement_baseline was computed on duplicated data (numbers unreliable).
          Running arm comparison on this data would produce wrong results.

  Blocker: No deduped dataset available
  Fix: recommend gate outcome `revise "D-phase profiled raw rows
         including ~12% duplicates by invitation_id; engagement_baseline
         numbers are inflated and the arm comparison cannot run on this
         data — plan needs a deduplication step before any I-phase
         comparison."` (gate outcome routes to plan; plan-v{N+1} reads
         the feedback and rewrites pending_tasks accordingly — typically
         adding a new D-task and re-running engagement_baseline)
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
  insights/data/D01-col_overview/report.md exists (4.2KB, from prior session run0)

───────────────────────────────────────────
EVALUATION:
  Verdict: SKIP
  Reason: Report already exists at insights/data/D01-col_overview/report.md (4.2KB).
          Produced by a prior session against the same snapshot. Still valid.
  Skip reason: Prior session already completed this task.
  Existing output: insights/data/D01-col_overview/report.md
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
