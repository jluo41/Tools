---
name: haipipe-application-ask
description: "Research-question driver of the haipipe-application family. Takes one question, scans the project's KB, plans batches of C_task work (for D+I) and D_experiment work (for K+W), dispatches them, files DIKW cards via E_insight, writes a session report. The only kind in G_application authorized to trigger /haipipe-experiment + /haipipe-task from outside. Use when the user asks a research question (no specific external artifact wanted). Trigger: ask, research question, /haipipe-application ask, what do we know about X, does X hold."
argument-hint: [question] [--project <path>] [--auto] [--unattended[=Ns]] [--persona strict|balanced|creative|lenient]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task
---

Skill: haipipe-application-ask
===============================

The **question driver**. One user intent → one closed case file under
`applications/ask/<NN_slug>/`. Walks the 4-phase ask shape end-to-end,
calling the shared session machinery (plan / gate / context) at each
boundary. Only kind in G_application authorized to trigger
`/haipipe-experiment` and `/haipipe-task` from outside.


Phase shape — 4 phases × 2 steps
==================================

```
                       ask kind, 4 phases
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │   Phase 1   design       Skill("haipipe-application-plan")   │
   │             step=task    → SCAN existing KB                  │
   │                          → SANITY-CHECK data sufficiency      │
   │                          → write plans/plan-v{N}.yaml         │
   │             step=gate    Skill("haipipe-application-gate"    │
   │                                  args="G-design")             │
   │                          SOFT, persona-driven, 3 outcomes     │
   │                                                              │
   │   Phase 2   observe      dispatch task_batch:                │
   │             step=task    for each T in plan.task_batch:      │
   │                            Skill("haipipe-application-context"│
   │                                   args="observe T")          │
   │                            ↓ READY/BLOCKED/SKIP              │
   │                            Skill("haipipe-task <type>")      │
   │                              → writes results/<RUN>/         │
   │             step=gate    G-observe SOFT                      │
   │                          (skip Phase 2 entirely if            │
   │                           task_batch is empty)                │
   │                                                              │
   │   Phase 3   claim        dispatch experiment_batch:          │
   │             step=task    for each E in plan.experiment_batch:│
   │                            Skill("haipipe-application-context"│
   │                                   args="claim E")            │
   │                            Skill("haipipe-experiment design")│
   │                            Skill("haipipe-experiment bridge")│
   │                              → HARSH gates inside D_experiment│
   │                            Skill("haipipe-experiment result")│
   │             step=gate    G-claim SOFT on G-side              │
   │                          (skip Phase 3 entirely if            │
   │                           experiment_batch is empty)          │
   │                                                              │
   │   Phase 4   report       for each card C in plan.insight_yield:│
   │             step=task    Skill("haipipe-insight-<layer>"     │
   │                                  args="--scope ...")         │
   │                            → writes insights/<layer>/C##_*.md│
   │                          rebuild insights/INDEX.md            │
   │                          Skill("haipipe-application-plan"    │
   │                                  args="compose report")      │
   │                            → writes applications/ask/<NN>/   │
   │                              report.md                       │
   │             step=gate    G-report HARSH                      │
   │                          (final answer truly addresses Q?)   │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
   
   Every gate's `revise [feedback]` outcome → back to Phase 1 (plan)
   Plan is the SOLE router for non-forward motion.
```

DIKW is a card-labeling lens applied at Phase 4, NOT a phase order.
The session never runs phase=D → phase=I → phase=K → phase=W in
sequence. Phases 2 (observe) and 3 (claim) collect *evidence*; Phase
4 (report) labels the evidence into D / I / K / W cards.


Phase 1 — design (detail)
==========================

Scan + sanity-check + plan, in this order:

```
A. SCAN KB (Phase 0 of the old vocabulary, now a sub-step of design)
   - Read examples/<project>/insights/INDEX.md if present
   - If INDEX.md missing: KB is empty, set existing_relevant: {} and
     CONTINUE. Empty KB is NOT a blocker for ask sessions; it is the
     normal starting state for a new project.
   - Filter KB by tags matching the question; load K + I that look
     relevant. Skim frontmatter only (≤ 13 lines each); read bodies
     only if needed.

B. SANITY-CHECK question vs data (THIS WAS MISSING — bug #11)
   - If question is per-subject ("understand Subject-X"), verify
     CGM density ≥ 1000 rows under the subject's 1-SourceStore
     before planning task_batch. Sparse-sample subjects → ASK user
     whether to (a) pick a denser subject or (b) reframe to cohort
     scope.
   - If question is cross-experiment, verify experiments/ has at
     least one confirmed experiment with matching tags.
   - If a required data source is missing entirely, gate the plan
     to BLOCKED and surface to user.

C. WRITE plan-v{N}.yaml
   - Location: applications/ask/<NN_slug>/plans/plan-v{N}.yaml
   - Maintain plans/plan.yaml symlink → plan-v{N}.yaml
   - Schema: see haipipe-application-plan/SKILL.md (task_batch +
     experiment_batch + insight_yield + dag + gates + revise_history)
   - Atomic: write to .tmp then mv; never partial write.

D. UPDATE SESSION_STATE.json (always atomic, .tmp + mv)
   - current_phase = "design", current_step = "task"
   - completed_tasks.design = [{name:"plan-v1", status:"done",
     plan_version:1}]
   - pending_tasks.design = []
   - plan_version = N
```


Phase 2 — observe (detail)
===========================

Dispatches task_batch. Skip entirely if task_batch is empty (then
go straight to Phase 3 → 4).

```
For each T in plan.task_batch:
  1. SESSION_STATE: current_step="task", current_task=T.id
  2. Skill("haipipe-application-context", args="observe <T.id>")
     → returns READY | BLOCKED | SKIP
       READY   — context OK; proceed
       BLOCKED — log blocker in SESSION_STATE; break out, jump to gate
       SKIP    — entry exists; remove from pending, append to
                 completed_tasks.observe with status="skipped"
  3. Skill("haipipe-task <T.type>", args=T.notes ...)
     → writes tasks/<G##_group>/<##_task>/results/<RUN>/
  4. Update task_calls[] in SESSION_STATE.json (atomic)
  5. Mark completed_tasks.observe += {name:T.id, status:"done",
     plan_version:N, yields:T.yields}

After all T done (or blocker reached):
  Pre-gate artifact check (mandatory before G-observe fires):
    For every entry in completed_tasks.observe with status ∈
    {done,reused}: assert each yield's expected artifact exists.
    Missing → override gate outcome to revise.

  Skill("haipipe-application-gate", args="G-observe")
    → SOFT, 3 outcomes
    → revise → back to Phase 1 (plan_version += 1)
    → approve → Phase 3
```


Phase 3 — claim (detail)
=========================

Dispatches experiment_batch. Skip entirely if experiment_batch is
empty. K and W cards CANNOT be filed unless an experiment validates
them — this is the strict rule from MENTAL_MODEL.md.

```
For each E in plan.experiment_batch:
  1. SESSION_STATE: current_step="task", current_task=E.id
  2. Skill("haipipe-application-context", args="claim <E.id>")
     → checks E.needs (D/I cards required as input) all resolved
  3. Skill("haipipe-experiment design", args="new <E.id> --auto")
  4. Skill("haipipe-experiment bridge", args="<E.id>")
     → scaffolds runs/ + invokes Run Script Reviewer
       (HARSH gate inside C_task; bridge handles its own gates)
     → deploys runs (GPU work; may take hours)
  5. WAIT for results to land (poll experiment.yaml.result.status)
  6. Skill("haipipe-experiment result aggregate", args="<E.id>")
     → fills result block; status: pending → confirmed
  7. Skill("haipipe-experiment review", args="<E.id>")
     → HARSH structural + Codex verdict
  8. Update experiment_calls[] in SESSION_STATE.json

Pre-gate artifact check (G-claim):
  For every K/W in plan.insight_yield: verify the sourcing
  experiment's result.status == "confirmed". If any "pending" or
  "refuted", override gate to revise.

Skill("haipipe-application-gate", args="G-claim")
  → SOFT-on-G-side (HARSH already happened upstream in D_experiment)
  → revise → back to Phase 1
  → approve → Phase 4
```


Phase 4 — report (detail)
==========================

```
A. FILE DIKW cards (one card per entry in plan.insight_yield)
   For each C, layer = C.layer ∈ {D, I, K, W}:
     Skill("haipipe-insight-<layer>", args="--scope <C.sources>")
       → writes insights/<L>_*/C##_<slug>.md
   D + I cards source from C_task results/.
   K + W cards source from D_experiment experiment.yaml.

B. REBUILD insights/INDEX.md
   Aggregate all cards (incl. existing ones), regenerate top INDEX
   per ref/index-templates.md. K_knowledge/INDEX.md and
   W_wisdom/INDEX.md also rebuilt if those folders gained entries.

C. COMPOSE final report
   Skill("haipipe-application-plan", args="compose report")
     → writes applications/ask/<NN_slug>/report.md
     → MUST cite the K/W (or D/I if no K/W) entries it relies on
     → MUST honestly answer "did we answer the original question?"

D. UPDATE SESSION_STATE.json to status="complete", current_phase="done"

E. G-report (HARSH)
   Skill("haipipe-application-gate", args="G-report")
     → checks: report.md cites filed cards; truly answers Q
     → revise → back to Phase 1
     → approve → terminal: session complete
```


Empty-batch shortcuts
=====================

Plan can produce 4 different batch shapes — each follows the same
4-phase shape but skips empty phases:

```
shape                            phases run
─────────────────────────────────────────────
descriptive (D/I only)           1 → 2 → 4   (skip 3, no K/W)
KB lookup (no new evidence)      1 → 4       (skip 2 + 3; report from KB)
experiment-only (K/W only)       1 → 3 → 4   (skip 2, no new D/I)
full (D + I + K + W)             1 → 2 → 3 → 4
```

Plan declares which shape via task_batch / experiment_batch
emptiness. The orchestrator detects this automatically; no special
flag needed.


SESSION_STATE.json — single source of truth
=============================================

Read and update on every phase / step / gate transition. Atomic
write (`.tmp` + `mv`) is MANDATORY (not just recommended) — survives
context compaction + crashes.

See `../haipipe-application/ref/session-state-schema.md` for the
complete schema. Key fields for ask:

```
kind: ask
current_phase: design | observe | claim | report | done
current_step:  task | gate
current_task:  <task id like T1, E07, plan-v1, report.md>
current_gate:  G-design | G-observe | G-claim | G-report
plan_version:  N
completed_tasks: {design:[], observe:[], claim:[], report:[]}
pending_tasks:   {design:[], observe:[], claim:[], report:[]}
experiment_calls: [{phase, exp_id, via, ts, status}, ...]
task_calls:       [{phase, task_path, via, ts, status}, ...]
gate_persona:    {preset, strictness, ambition, notes}
unattended_timeout: null | N | 0
```


Commands
========

```
/haipipe-application-ask <question>
  Full flow starting from Phase 1.

/haipipe-application-ask continue
  Resume in-progress session (reads SESSION_STATE.json).

/haipipe-application-ask status
  Print last session's phase + outstanding gate.
```


Constants
==========

```
MAX_REVISIONS    default 3      Cap on revise→plan cycles. Hitting cap
                                triggers FORCED APPROVAL with audit banner
                                (see ../haipipe-application/ref/gate-persona.md).

MAX_EXPERIMENTS  default 3      Cap on new experiments triggered per session.
                                Exceeding asks user to confirm continuation.

Flags:
  --persona strict|balanced|creative|lenient   maps to SESSION_STATE.gate_persona
                                                (see ref/gate-persona.md)
  --unattended[=Ns]                            maps to SESSION_STATE.unattended_timeout
                                                (see ref/attendance-modes.md)
  --auto                                       legacy alias for --unattended=0
  --project <path>                             override project root
```


Stop conditions
================

```
✅ complete       all 4 phases done; G-report approved
🟡 budget        MAX_EXPERIMENTS or MAX_REVISIONS hit
🔴 blocked       Phase 1 sanity-check failed and user provided no fix
🛑 paused        user invoked /haipipe-application-ask pause; resume later
```


Recovery from compaction
=========================

On resume, read SESSION_STATE.json, then:

1. State-vs-disk consistency check (mandatory before re-entering loop):
   For each `done`/`reused` entry in completed_tasks.*, verify the
   yield artifacts exist on disk (D/I → tasks/.../results/; K/W →
   experiment.yaml.result.status=="confirmed" + corresponding
   insight card filed). Missing → demote entry to status="failed",
   name re-enters pending_tasks. Log demotions to
   `applications/ask/<NN>/tmp/recovery-<ISO>.log`.

2. Re-enter loop at recorded (current_phase, current_step, current_task | current_gate).

3. Never re-run a task whose entry still satisfies the artifact contract.

4. `haipipe-application-context` is always re-run on resume — cheap.


Boundary
=========

```
haipipe-application-ask     bridges INSIGHT base ↔ EXPERIMENT base
                            via /haipipe-experiment + /haipipe-task

haipipe-experiment-loop     iterates ONE experiment thread
haipipe-experiment-bridge   scaffolds tasks for ONE experiment

Session NEVER writes tasks/ directly — always via /haipipe-task or
/haipipe-experiment-bridge. The one-way dependency
(experiments → tasks; ask → both) stays clean.
```


Risk profile
=============

WRITES:
- insights/ (heavy — files D/I/K/W cards, rebuilds INDEX)
- applications/ask/<NN>/ (plans, gates, SESSION_STATE.json, report.md)
- via dispatch: tasks/, experiments/ (through C_task / D_experiment)

CALLS:
- External LLM (Codex MCP) indirectly via experiment-bridge's
  Run Script Reviewer + review claim. Budget via MAX_EXPERIMENTS.

GATES:
- 4 SOFT gates inside this session (G-design / G-observe / G-claim /
  G-report) — persona + attendance driven.
- HARSH gates downstream:
  - C_task: CODE_REVIEW.md (bridge invokes Run Script Reviewer)
  - D_experiment: review structural + integrity + claim
  - Phase 4: G-report (this session's HARSH gate)


Specialist tail
================

```
status:    complete | blocked | failed | budget | paused
summary:   "Q answered via [K05, K07] (new) + W03 (next-step) — see
            applications/ask/03_film-test-od/report.md"
artifacts: [applications/ask/<NN_slug>/{SESSION_STATE.json, plans/, gates/,
                                       invocations.log, report.md},
            insights/D_data/D*.md (new),
            insights/I_information/I*.md (new),
            insights/K_knowledge/K*.md (new / updated),
            insights/W_wisdom/W*.md (if any),
            experiments/<NN>_<slug>/ (if new experiments scaffolded),
            tasks/<G##>/<##>/results/<RUN>/ (per dispatched task)]
next:      "review report.md + KB updates; if external artifact needed,
            /haipipe-application {message|ui|report}"
```
