---
name: dikw-session
description: "Full DIKW analysis session. Runs phases plan → D → I → K → W → report with a gate at the end of each phase for review. Handles iteration: a gate outcome can revise the current phase, go back to an earlier phase, rewrite the plan, or jump to report. Use when user says 'run DIKW', 'full analysis', 'DIKW session', 'analyze this dataset end-to-end', or /dikw-session. Trigger: DIKW session, full analysis, end-to-end analysis, analyze dataset."
argument-hint: [snapshot_dir] [questions]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
---

# DIKW Analysis Session

End-to-end DIKW analysis pipeline for: **$ARGUMENTS**

The first argument, `snapshot_dir`, is a `_agent_dikw_space/snapshot-<date>/`
folder produced by `/dikw`. If you run `/dikw-session` directly, pass the
snapshot dir yourself.

## Constants

- `AUTO_PROCEED = false` — *default.* Pause at every gate for human
  acceptance. Set `true` via `--auto` for unattended runs (the gate's
  proposed outcome is auto-accepted).
- `MAX_REVISIONS = 3` — caps `revise plan` loops; after exceeding, the
  session force-approves with a warning.
- `MAX_TASKS_PER_LEVEL = 4` — cap per D/I/K/W phase.

Override: `/dikw-session "questions" --auto` or `/dikw-session "questions" --max-tasks 2`.

---

## Runtime model (vocabulary)

Five concepts, no more:

| Term | Values |
|------|--------|
| **Stage** | `S0`..`S5` — `/dikw` outer workspace setup (one-time, before this skill runs) |
| **Phase** | `plan` / `D` / `I` / `K` / `W` / `report` / `done` — session state |
| **Step**  | `task` / `gate` — the two steps inside every phase, in order |
| **Task**  | a specific item run during `step=task` (one for `plan`/`report`; 2–3 for D/I/K/W) |
| **Gate**  | a specific checkpoint run during `step=gate`; identifier `G-<phase>`; outcome is one of `approve` / `revise <phase> [feedback]` / `done` |

Every phase follows the same 2-step shape:

```
phase=<X>  ─▶  step=task  ─▶  step=gate  ─▶  (outcome routes next phase)
                  │               │
                  │               └─ /dikw-gate produces the gate proposal,
                  │                  user (or --auto) accepts → outcome applied
                  │
                  └─ for each task in pending_tasks[X]:
                       /dikw-context X <task>    (load the task's context)
                       /dikw-<skill> <task>       (run the task; writes report)
```

## State machine

Phases are nodes; gate outcomes are edges.

```
 plan ─G-plan─▶ D ─G-D─▶ I ─G-I─▶ K ─G-K─▶ W ─G-W─▶ report ─G-report─▶ done
                 ╲        ╲        ╲        ╲
                  ╲        ╲        ╲        ╲── revise <earlier_phase> | revise plan
                   ╲────────╲────────╲──────────  (any back-edge permitted)

 Outcome semantics (produced at any gate):
   approve              → current_phase = next_forward(current_phase)
   revise <phase> [fb]  → current_phase = <phase>
                          if <phase> == plan: plan_version += 1
                          add new/changed task(s) from feedback to pending_tasks[<phase>]
   done                 → current_phase = "report"
```

## Orchestrator loop

**CRITICAL — sub-skill invocation is mandatory, not suggested.** Each task
inside a phase is work that belongs to a sub-skill (`/dikw-context` +
`/dikw-<phase>`). The orchestrator's ONLY role during `step=task` is to
call those sub-skills, one task at a time. The orchestrator itself MUST
NOT perform the analysis inline.

Forbidden shortcuts (common failure mode — do NOT do any of these):
  - Writing a multi-task Bash heredoc that runs pandas on all D-tasks at
    once and writes each `report.md` directly.
  - Invoking `Write` or `Edit` to create `report.md` without first
    invoking the `/dikw-<phase>` skill.
  - Batching N tasks into one Python script because "they share the same
    data load."
  - Skipping `/dikw-context` because "the context seems obvious."

Each of these bypasses the artifact contract (see Rules §"Task is
complete iff …") and produces incomplete task folders — no
`analysis.py`, no re-runnability, no skill-level QA.

Concrete invocation shape (pseudocode → real tool calls):

```
while current_phase != "done":

    # ─── step=task ──────────────────────────────────────────────
    current_step = "task"
    for task in pending_tasks[current_phase]:
        if task already completed (see "Task is complete iff…" rule): skip
        current_task = task.name

        # These two lines are NOT pseudocode — they map 1:1 to Skill tool calls:
        Skill(name="dikw-context",          args="<current_phase> <task.name> <snapshot_dir>")
            # dikw-context returns a verdict: READY / BLOCKED / SKIP.
            # Handle each before invoking the phase skill:
            #   READY   → proceed to Skill(dikw-<phase>) below
            #   SKIP    → record skip reason in DIKW_STATE, remove from pending,
            #             add to completed_tasks with status=skipped, current_task=null, continue loop
            #   BLOCKED → record the blocker in DIKW_STATE, break out of the
            #             task loop, jump straight to step=gate. /dikw-gate
            #             will see the blocker in state and propose
            #             `revise plan` (or `revise <earlier_phase>`) with
            #             the blocker text as feedback.
        Skill(name="dikw-<current_phase>",  args="<task.name> <snapshot_dir>")
            # where <current_phase> ∈ {data, information, knowledge, wisdom, plan, report}

        # Announce in the banner which sub-skill was invoked so the
        # transcript makes cheating visible (see Banner rules below).

        mark task completed in DIKW_STATE.json
          (remove from pending_tasks[current_phase] AND append to
           completed_tasks[current_phase] in the same write — never let
           the two lists drift)
    current_task = null

    # ─── pre-gate verification ─────────────────────────────────
    # Before calling /dikw-gate, scan every completed task folder for
    # this phase and assert the artifact contract holds. Any missing
    # artifact auto-routes to `revise <phase> "task X missing <file>"`
    # at the upcoming gate. See "Pre-gate artifact check" below.

    # ─── step=gate ──────────────────────────────────────────────
    # CRITICAL — gate-proposal delegation is mandatory.
    # The orchestrator MUST NOT write its own "Proposed: approve" summary
    # inline. The sole purpose of step=gate is to invoke /dikw-gate,
    # which (a) reads every report across all phases + explore notes +
    # plan + prior gates, (b) assesses completeness / sufficiency /
    # surprises, and (c) proposes exactly one outcome of
    # {approve | revise <phase> [fb] | done}. Without /dikw-gate the
    # "should we revise the plan?" question is never actually asked —
    # the orchestrator just rubber-stamps its own progress.

    current_step = "gate"
    current_gate = "G-" + current_phase

    # This line is NOT pseudocode — it maps 1:1 to a Skill tool call:
    Skill(name="dikw-gate", args="<snapshot_dir>")
        # writes {snapshot_dir}/sessions/{aim}/gates/{NN}-G-<phase>.md
        #   where NN = count(existing gates/*.md) at write time, zero-padded 2 digits.
        # prints the proposed outcome with assessment + tables

    # Banner MUST show the gate invocation:
    #   [… · {Phase}-Gate · G-{phase} · invoking /dikw-gate]
    # If the banner does not show this before the proposed outcome
    # appears, the orchestrator wrote the gate decision itself —
    # fail-closed: treat the outcome as invalid and re-run.

    if AUTO_PROCEED: auto-accept proposal
    else:             wait for user (approve / revise <phase> [fb] / done)

    outcome = <accepted gate outcome>
    apply outcome:
        if approve:         current_phase = next_forward(current_phase)
        elif revise <p> fb: if p == plan:
                                plan_version += 1
                                /dikw-context plan <snapshot_dir>        # full-like-report load
                                /dikw-plan <snapshot_dir> "<feedback>"   # writes plan-raw-v{N}.yaml
                            else:
                                add new task(s) from fb to pending_tasks[p]
                            current_phase = p
                            revisions_count += 1  (if p == plan)
                            if revisions_count >= MAX_REVISIONS: force approve, warn
        elif done:          current_phase = "report"
    current_gate = null

status = "complete"
```

## Per-phase contract (uniform — all use the same 2 steps)

| Phase    | `step=task` skill                   | tasks        | `step=gate` skill | Forward next |
|----------|-------------------------------------|--------------|-------------------|--------------|
| `plan`   | `/dikw-plan`                         | 1 (the plan) | `/dikw-gate`    | `D`          |
| `D`      | `/dikw-data`                         | 2–3          | `/dikw-gate`    | `I`          |
| `I`      | `/dikw-information`                  | 2–3          | `/dikw-gate`    | `K`          |
| `K`      | `/dikw-knowledge`                    | 1–2          | `/dikw-gate`    | `W`          |
| `W`      | `/dikw-wisdom`                       | 1–2          | `/dikw-gate`    | `report`     |
| `report` | `/dikw-report`                       | 1 (final)    | `/dikw-gate`    | `done`       |
| `done`   | — (terminal, no steps)                | —            | —                 | —            |

Every phase loads context via `/dikw-context <phase> <task>` before each task's run.

## Banner (shown at every session message)

```
[{subject} · {snapshot} · {aim} · plan-v{N} · {Phase}-{Step} · {task|gate} · {status}]
```

Field rules:
- `{subject}` — last segment of the original folder path (e.g. `Subject-6`). Fall back to the folder basename for non-subject inputs.
- `{snapshot}` — snapshot folder name abbreviated as `snap-YYYY-MM-DD` (drop the leading `snapshot-`).
- `{aim}` — session name, auto-generated at creation as `NN_slug` (see *Session naming* below).
- `plan-v{N}` — current plan version (matches `plan-raw-v{N}.yaml`).
- `{Phase}-{Step}` — capitalized phase + step: `Plan-Task`, `Plan-Gate`, `D-Task`, `D-Gate`, `I-Task`, `I-Gate`, `K-Task`, `K-Gate`, `W-Task`, `W-Gate`, `Report-Task`, `Report-Gate`, or terminal `Done`.
- `{task|gate}` — for multi-task phases during Task: `i/n task_name`. For single-task phases (Plan, Report): the artifact (`writing plan-raw-v1`, `final_output.md`). At gates: the gate id (`G-D`, `G-plan`, …).
- `{status}` — only at gates: `awaiting` / `approved` / `revise→plan` / `revise→D` / `done`. Task steps omit it. Terminal phase: `Done` line has no status.

Examples (abstract):
```
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v1 · Plan-Task · writing plan-raw-v1]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v1 · Plan-Gate · G-plan · awaiting]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · D-Task · 2/3 {task_name}]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · D-Gate · G-D · awaiting]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · D-Gate · G-D · revise→plan]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · Plan-Task · writing plan-raw-v2]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · Report-Task · final_output.md]
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v2 · Done]
```

ALWAYS prefix session-turn messages with this banner.

## Session naming (aim generation)

On session creation, `aim = next_index() + "_" + slug(question)`:

- **`next_index()`** = `(max NN across existing sessions/NN_*) + 1`, starting at `01`, zero-padded to 2 digits.

- **`slug(question)`** — 3–5 tokens, lowercase, kebab-case. Must name the
  **specific phenomenon + intent** of the question, not the generic topic.
  Stopwords dropped (`what/is/are/the/does/do/exist/have/how/why/a/an`).
  Forbidden generic suffixes: `-analysis`, `-study`, `-check`, `-review`.
  For genuinely open-ended "what patterns exist" questions, use a scope
  marker like `-landscape` or `-survey` with the domain noun in front.
  Slug is model-generated by intent; fall back to literal stopword-filtered
  tokens on model failure.

- **User override** via `/dikw --name my-slug`: still prepend the `NN_` index.

- **Legacy `sessions/run*/` dirs** are left untouched; next new session gets
  the correct NN.

Abstract shape: `NN_{domain}-{phenomenon}-{intent}`
  where `{intent}` ∈ {`presence`, `response`, `assessment`, `shift`,
                       `landscape`, `survey`, `comparison`, …}.

## DIKW_STATE.json schema

```json
{
  "status": "running",                    // running | complete
  "aim": "NN_{slug}",                     // e.g. "01_dawn-phenomenon-presence"
  "questions": "What CGM patterns exist",
  "current_phase": "D",                   // plan | D | I | K | W | report | done
  "current_step": "task",                 // task | gate
  "current_task": "cgm_quality_sampling", // non-null during step=task
  "current_gate": null,                   // non-null during step=gate: "G-D" etc
  "plan_version": 2,
  "completed_tasks": { "D": ["cgm_normalize_profile"], "I": [], "K": [], "W": [] },
  "pending_tasks":   { "D": ["cgm_quality_sampling", "context_streams_align"], ... },
  "phase_history": [
    { "phase": "plan", "plan_version": 1, "entered": "...", "exited": "..." },
    { "phase": "D",    "entered": "...", "exited": "..." },
    { "phase": "plan", "plan_version": 2, "entered": "...", "exited": "...",
      "via_gate": "G-D", "triggering_feedback": "wrong data grain" }
  ],
  "gates": [
    { "gate": "G-plan", "plan_version": 1, "outcome": "approve",
      "routes_to": "D", "timestamp": "..." },
    { "gate": "G-D",    "outcome": "revise plan", "feedback": "wrong data grain",
      "routes_to": "plan", "timestamp": "..." },
    { "gate": "G-plan", "plan_version": 2, "outcome": "approve", "routes_to": "D" }
  ],
  "revisions_count": 1,
  "gate_persona": {                       // set once at /dikw Stage 4; locked for the session
    "preset": "balanced",                 // strict | balanced | creative | lenient
    "strictness": 5,                      // 0-10; seeded from preset, optional override
    "ambition": 5,                        // 0-10; seeded from preset, optional override
    "notes": ""                           // free-text voice; optional, may be ""
  }
}
```

**`gate_persona` is locked for the whole session.** It is written once
at `/dikw` Stage 4 and must not be modified between phases. `/dikw-gate`
reads this field at every firing to compose its reviewer voice. If the
field is missing (legacy state), default to `{preset: "balanced",
strictness: 5, ambition: 5, notes: ""}` and log a migration note.

Update after every task completion, every gate outcome, and every state
transition. This file is the only source of truth for resume-after-compaction.

## Pre-session requirement

Before entering the first phase, verify `{snapshot_dir}/exploration/explore_notes.md`
exists (produced by `/dikw` at Stage 4.5, snapshot-level, shared across sessions).
If missing, run `/dikw-explore {snapshot_dir}` once before starting the loop.

## Gate presentation (mandatory tables)

Any gate that proposes or adds tasks MUST render them as **one markdown
table per affected phase** with full descriptions — never a comma list.
Columns: `#` / `Task` / `Description`. This applies to:
- `G-plan` (every plan version, v1 and v2+)
- `G-D` / `G-I` / `G-K` / `G-W` when outcome is `revise <phase>` with new tasks
- `G-report` final check

Third-column header variant: when the outcome is `revise <current_phase>`
or `revise <earlier_phase>` (re-run existing tasks with applied feedback),
the third column is labelled **`Change`** instead of **`Description`** —
same table shape, different semantics: "what's changing about this
task" vs "the full task spec." `revise plan` always uses `Description`
(tasks are fresh).

End every human gate message with the A/B/C/D/E option block (see the
"Gate option mapping" rule below). The A–E letters map internally to
outcomes (`approve / revise <phase> [feedback] / done / cancel`) — do
not show the free-text vocabulary in the prompt line.

Under `--auto`, print the same tables + auto-accept line ("Auto-accepting
the proposed outcome under `--auto`").

## Iteration patterns

### Pattern 1 — Add tasks to current phase

```
phase=D · step=gate · G-D · proposal: revise D "click_rate nulls not handled"
  → user approves proposal
  → current_phase stays D; new D-task added to pending_tasks
  → next loop iteration: step=task runs the new task
  → step=gate G-D again → approve
  → current_phase = I
```

### Pattern 2 — Go back to an earlier phase

```
phase=I · step=gate · G-I · proposal: revise D "time column not profiled"
  → current_phase = D
  → run new D task, G-D → approve
  → current_phase = I (re-enter; skip already-valid I tasks)
```

### Pattern 3 — Rewrite the plan

```
phase=D · step=gate · G-D · proposal: revise plan "wrong data grain"
  → plan_version 1 → 2
  → /dikw-context plan  (full load: explore + all reports + full gate history)
  → /dikw-plan "<feedback>"  writes plan-raw-v2.yaml
  → current_phase = plan
  → G-plan v2 → present new plan tables → user approves
  → current_phase = D, continue (skip already-valid tasks)
```

### Pattern 4 — Multi-hop back (K → D)

```
phase=K · step=gate · G-K · proposal: revise D "K needs hourly profile"
  → current_phase = D  (skip right past I)
  → run new D task, G-D → approve
  → current_phase = I → approve
  → current_phase = K (re-run K with richer evidence)
```

### Pattern 5 — Jump to report

```
phase=I · step=gate · G-I · proposal: done "findings are already clear"
  → current_phase = report
  → /dikw-report produces final_output.md
```

## Recovery from context compaction

On startup, read `DIKW_STATE.json`:
1. `current_phase` + `current_step` + `current_task|current_gate` = exact position
2. Re-enter the orchestrator loop at that position
3. Never re-run completed tasks (check `report.md` existence)
4. `/dikw-context` is always re-run — it's cheap and picks up any state drift

## Legacy state upgrade (one-time migration)

Sessions started before the 2026-04-22 vocab rework may have a
pre-migration `DIKW_STATE.json` and `plan-raw.yaml` + session-level
`exploration/`. On startup, detect-and-upgrade in place — do NOT delete:

```
If {snapshot}/exploration/explore_notes.md does NOT exist, but
   {snapshot}/sessions/{aim}/exploration/explore_notes.md exists:
     mkdir -p {snapshot}/exploration
     mv {snapshot}/sessions/{aim}/exploration/explore_notes.md \
        {snapshot}/exploration/explore_notes.md

If {snapshot}/sessions/{aim}/plan/plan-raw.yaml is a regular file
   (not a symlink) and plan-raw-v1.yaml does NOT exist:
     mv   plan-raw.yaml  plan-raw-v1.yaml
     ln -s plan-raw-v1.yaml plan-raw.yaml

If {snapshot}/sessions/{aim}/gates/gate_D.md (etc.) exist (old naming):
     rename each to {NN}-G-<phase>.md (keep contents — review text still valid)
     where {NN} is assigned by timestamp order: earliest gate = 00, next = 01, …
     (zero-padded 2 digits). Use file mtime as the tiebreaker when the
     original names don't imply order.

If {snapshot}/sessions/{aim}/gates/G-<phase>.md or G-<phase>-v{N}.md files
   exist (intermediate naming, pre-NN sweep): prepend the NN prefix the
   same way (timestamp order), dropping the -v{N} suffix.

If DIKW_STATE.json lacks current_step / current_task / current_gate
   / gate_outcome / phase_history fields:
     ADD them with sensible defaults:
       current_step  ← "task" if a phase-skill was running, else "gate"
       current_task  ← null
       current_gate  ← null
     Map old gate records:
       decision=PROCEED      → outcome=approve
       decision=ADD_TASKS    → outcome=revise <current_phase> "<reason>"
       decision=GO_BACK <X>  → outcome=revise <X> "<reason>"
       decision=REVISE_PLAN  → outcome=revise plan "<reason>"
       decision=DONE         → outcome=done
     Preserve phase_history, gates[], revisions_count — never delete them.

If DIKW_STATE.json lacks gate_persona (pre-persona session):
     ADD {preset: "balanced", strictness: 5, ambition: 5, notes: ""}
     and log the default in the migration note.
```

After upgrade, write a short note to `{snapshot}/tmp/migration-2026-04-22.log`
summarizing what was changed, so the upgrade is auditable.

## Rules

- ALWAYS update `DIKW_STATE.json` after every task and every gate outcome.
- **Task is complete iff all required files exist and are >100 bytes.**
  Required files per phase (matches each sub-skill's contract):
  - **D** (`insights/data/D{NN}-.../`): `report.md` + `analysis.py`
  - **I** (`insights/information/I{NN}-.../`): `report.md` + `analysis.py`
  - **K** (`insights/knowledge/K{NN}-.../`): `report.md` only (reasoning-only phase)
  - **W** (`insights/wisdom/W{NN}-.../`): `report.md` only (reasoning-only phase)
  For D/I, a folder holding `report.md` but no `analysis.py` is **not
  complete** — the orchestrator took a shortcut or the sub-skill failed
  its contract. The pre-gate check (below) must override the gate's
  proposal with
  `revise <phase> "task X missing analysis.py — re-run /dikw-<phase> <task>"`.
- NEVER re-run a task that meets the "complete iff" rule above
  unless the gate explicitly invalidated it.
- **Pre-gate artifact check (runs automatically before `/dikw-gate`):**
  For every task in `completed_tasks[current_phase]`, verify its folder
  contains both required files. Missing artifacts → override the
  gate's proposed outcome with `revise <current_phase>` and list
  each offending task in the gate feedback. Do this inside the
  orchestrator before calling `/dikw-gate`, not after.
- **Sub-skill invocation is mandatory.** The orchestrator MUST invoke
  `/dikw-context` and `/dikw-<phase>` once per task. It MUST NOT
  perform the analysis itself via Bash/Write/Edit. Violations are
  caught by the pre-gate check but should not get that far — see the
  "forbidden shortcuts" list in the Orchestrator loop section.
- **Gate-review delegation is mandatory.** The orchestrator MUST invoke
  `/dikw-gate` once per gate (`G-plan`, `G-D`, `G-I`, `G-K`, `G-W`,
  `G-report`). It MUST NOT write a "Proposed: approve" summary inline.
  `/dikw-gate` is the step that genuinely asks "given all evidence so
  far, should we revise the plan, revise the current phase, jump to
  report, or approve?" Skipping it turns every gate into an
  orchestrator self-rubber-stamp and defeats the purpose of gates.
  Forbidden shortcuts at step=gate:
    - Writing the gate file (`gates/G-<phase>.md`) via Write/Edit.
    - Presenting "Proposed: approve" in a message without the
      `invoking /dikw-gate` banner line appearing first.
    - Deciding the outcome based only on task counts / artifact checks
      (the pre-gate artifact check is a precondition, NOT the gate).
- **Banner must name the sub-skill being invoked** during each task,
  so the transcript makes bypass-attempts visible. Format during
  `step=task`:
  `[… · {Phase}-Task · {i}/{n} {task_name} · invoking /dikw-<phase>]`
  If the banner does not show `invoking /dikw-<phase>` before the
  report appears, the orchestrator cheated — fail-closed at the gate.
- Render tables with FULL task descriptions at every task-proposing gate.
- End every human gate with the outcome options line.
- If `MAX_REVISIONS` exceeded on `revise plan`, force `approve` with warning.
- If a task skill fails, retry once; then mark the task failed and continue.
- Save every gate file to `sessions/{aim}/gates/{NN}-G-<phase>.md` where
  `{NN}` is the **sequential gate counter** across the whole session
  (zero-padded two digits, starts at `00`). Every firing gets the next
  NN; revise-plan loops produce distinct filenames naturally, so no
  `-v{plan_version}` suffix is needed. See `dikw-gate/SKILL.md` Step 4.
- Every human gate presentation MUST end with the five lettered options:
  `(A) accept gate's recommendation · (B: <feedback>) override with your
  own feedback · (C) approve as-is · (D) done / jump to report · (E) cancel`.
  Do NOT use the verbose free-text vocabulary (`approve / revise <phase>
  [feedback] / done / cancel`) in the prompt line — the letters map to
  those outcomes internally (see `dikw-gate/SKILL.md` Step 5 mapping table).
- The final report MUST address the original question — if it doesn't,
  `G-report` should return `revise <phase>` with feedback on what's missing.

## Estimated duration

| Phase  | `step=task` time | gate pause |
|--------|------------------|------------|
| plan   | 1–2 min (or 3–5 min for v2+ with full context)| Gate (human approves) |
| D      | 3–8 min / task   | Gate |
| I      | 3–8 min / task   | Gate |
| K      | 2–5 min / task   | Gate |
| W      | 2–5 min / task   | Gate |
| report | 3–5 min          | Final gate |

Total: 30–60 min end-to-end. With `AUTO_PROCEED=false` (default), ~6 gate
interactions. With `--auto`, 0 gate interactions but outcomes still logged.
