---
name: dikw-session
description: "Full DIKW analysis session. Runs phases plan → D → I → K → W → report with a gate at the end of each phase for review. Handles iteration: a gate's `revise [feedback]` outcome routes back to plan (the single router), which rewrites the plan; pipeline restarts from plan. Use when user says 'run DIKW', 'full analysis', 'DIKW session', 'analyze this dataset end-to-end', or /dikw-session. Trigger: DIKW session, full analysis, end-to-end analysis, analyze dataset."
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

> ⚠ **Sibling skill**: `/dikw-session-agent` is a parallel implementation
> that dispatches each task to a subagent instead of running it inline.
> Any change to state machine, `DIKW_STATE.json` schema, gate contract,
> `MAX_REVISIONS` handling, banner format, pre-gate check, or resume
> logic **must be applied to the sibling too** — otherwise the two
> modes will silently diverge. See
> `skills/dikw-session-agent/SKILL.md`.

---

## Runtime model (vocabulary)

Five concepts, no more:

| Term | Values |
|------|--------|
| **Stage** | `S0`..`S5` — `/dikw` outer workspace setup (one-time, before this skill runs) |
| **Phase** | `plan` / `D` / `I` / `K` / `W` / `report` / `done` — session state |
| **Step**  | `task` / `gate` — the two steps inside every phase, in order |
| **Task**  | a specific item run during `step=task` (one for `plan`/`report`; 2–3 for D/I/K/W) |
| **Gate**  | a specific checkpoint run during `step=gate`; identifier `G-<phase>`; outcome is one of `approve` / `revise [feedback]` / `done` (revise always routes back to plan) |

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

Phases are nodes; gate outcomes are edges. Plan is the SINGLE
router — every non-forward outcome routes back to plan, never
directly cross-phase.

```
  plan ──▶ D ──▶ I ──▶ K ──▶ W ──▶ report ──▶ done
   ▲       │     │     │     │       │
   │       │     │     │     │       │
   └───────┴─────┴─────┴─────┴───────┘
        every "revise" routes here, regardless of which gate fired
        (plan re-decides pending_tasks; pipeline restarts from plan)

 Outcome semantics (produced at any gate):
   approve         → current_phase = next_forward(current_phase)
   revise [fb]     → current_phase = "plan"
                     plan_version += 1
                     /dikw-plan reads `fb` and rewrites the plan
                     (may add new tasks at any phase, or mark
                      existing tasks for re-run with applied changes)
   done            → current_phase = "report"
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
            #   SKIP    → remove task.name from pending_tasks[current_phase] and
            #             append { name, status: "skipped", plan_version }
            #             to completed_tasks[current_phase]; clear current_task;
            #             continue loop. SKIP carries no artifact requirement.
            #   BLOCKED → record the blocker in DIKW_STATE, break out of the
            #             task loop, jump straight to step=gate. /dikw-gate
            #             will see the blocker in state and propose
            #             `revise [feedback]` (always back to plan) with
            #             the blocker text as feedback. Plan must
            #             disambiguate: missing-task blocker → add task;
            #             pending-upstream blocker → keep plan, fix ordering.
        Skill(name="dikw-<current_phase>",  args="<task.name> <snapshot_dir>")
            # where <current_phase> ∈ {data, information, knowledge, wisdom, plan, report}

        # Announce in the banner which sub-skill was invoked so the
        # transcript makes cheating visible (see Banner rules below).

        mark task completed in DIKW_STATE.json
          (remove from pending_tasks[current_phase] AND append
           { name, status: "done", plan_version } to
           completed_tasks[current_phase] in the same write — never let
           the two lists drift. If the phase skill returned an error,
           append with status: "failed" instead.)
    current_task = null

    # ─── pre-gate verification ─────────────────────────────────
    # Before calling /dikw-gate, scan every completed task folder for
    # this phase and assert the artifact contract holds. Any missing
    # artifact auto-routes to `revise "task X missing <file>; re-run /dikw-<phase> <task>"`
    # at the upcoming gate. See "Pre-gate artifact check" below.

    # ─── step=gate ──────────────────────────────────────────────
    # CRITICAL — gate-proposal delegation is mandatory.
    # The orchestrator MUST NOT write its own "Proposed: approve" summary
    # inline. The sole purpose of step=gate is to invoke /dikw-gate,
    # which (a) reads every report across all phases + explore notes +
    # plan + prior gates, (b) assesses completeness / sufficiency /
    # surprises, and (c) proposes exactly one outcome of
    # {approve | revise [fb] | done}. Without /dikw-gate the
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

    # Attendance check — see "Gate attendance" rule below
    timeout = DIKW_STATE.unattended_timeout    # null | 0 | N seconds
    if timeout is None:
        wait_for_user_indefinitely()           # 🧑 attended (default)
    elif timeout == 0:
        auto_accept_proposal_verbatim()        # 🤖 unattended (immediate)
    else:
        # ⏳ timed — print countdown banner, wait up to N seconds.
        # Banner shows "awaiting (auto in {timeout}s)".
        # If a human reply arrives before the timeout, use it.
        # If the timer elapses with no reply, auto-accept the
        # proposal verbatim (treat as reply A).
        reply = wait_for_user(timeout_seconds=timeout)
        if reply is None:                      # timer fired
            auto_accept_proposal_verbatim()
        else:
            apply_user_reply(reply)
    # Auto-accepted gate files include an "AUTO-ACCEPTED" banner
    # (see /dikw-gate § "Auto-accept audit"). The proposal itself is
    # not modified — `done`/`revise` constraints still apply.

    outcome = <accepted gate outcome>
    apply outcome:
        if approve:           current_phase = next_forward(current_phase)
        elif revise feedback:
            # Order matters — see "Plan-version write ordering" rule below.
            # 1. Load full revision context for the planner
            /dikw-context plan <snapshot_dir>
            # 2. Run the planner (writes plan-raw-v{N}.yaml AND updates
            #    plan-raw.yaml symlink before returning)
            /dikw-plan <snapshot_dir> "<feedback>"
            # 3. Post-plan reconciliation: read the new plan's
            #    revision.changes.removed list and mark each removed task
            #    in completed_tasks[phase] with status = "invalidated".
            #    Tasks marked invalidated are no longer counted toward
            #    pre-gate artifact checks or the final report; their
            #    folders remain on disk for audit.
            for phase in [D, I, K, W]:
                for name in new_plan.revision.changes.removed.get(phase, []):
                    if entry exists in completed_tasks[phase] with name == name:
                        set entry.status = "invalidated"
            # 4. Recompute pending_tasks from the new plan (see
            #    "pending_tasks recomputation" rule below)
            recompute_pending_tasks(new_plan)
            # 5. Bump plan_version in DIKW_STATE.json AFTER the plan file
            #    and symlink are on disk — never before
            plan_version += 1
            current_phase = "plan"
            revisions_count += 1
            if revisions_count >= MAX_REVISIONS: force approve, warn
        elif done:
            # `done` is only valid at G-K, G-W, or G-report (see Rules).
            # If the gate proposed `done` from G-plan / G-D / G-I, the
            # orchestrator MUST reject it before reaching this branch.
            current_phase = "report"
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
- `{status}` — only at gates. Vocabulary depends on `unattended_timeout`:
    - 🧑 attended (`null`):  `awaiting` → `approved` / `revise→plan` / `done`
    - ⏳ timed (`N>0`):       `awaiting (auto in {N}s)` → `approved` / `revise→plan` / `done` / `auto-accepted`
    - 🤖 unattended (`0`):    `auto-accepted` (no awaiting state — gate accepts immediately)
  `auto-accepted` always means "proposal applied verbatim because no human reply arrived". The proposal's actual outcome (approve / revise / done) is still recorded in `gates[]`. Task steps omit `{status}`. Terminal phase: `Done` line has no status.

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
  "execution_mode": "inline",             // inline | agent — WRITE ONCE at session creation; locks which session skill may run/resume
  "current_phase": "D",                   // plan | D | I | K | W | report | done
  "current_step": "task",                 // task | gate
  "current_task": "cgm_quality_sampling", // non-null during step=task
  "current_gate": null,                   // non-null during step=gate: "G-D" etc
  "plan_version": 2,
  "completed_tasks": {
    "D": [
      { "name": "cgm_normalize_profile", "status": "done", "plan_version": 1 }
    ],
    "I": [], "K": [], "W": []
  },
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
    { "gate": "G-D",    "outcome": "revise", "feedback": "wrong data grain",
      "routes_to": "plan", "timestamp": "..." },
    { "gate": "G-plan", "plan_version": 2, "outcome": "approve", "routes_to": "D" }
  ],
  "revisions_count": 1,
  "gate_persona": {                       // set once at /dikw Stage 4; locked for the session
    "preset": "balanced",                 // strict | balanced | creative | lenient
    "strictness": 5,                      // 0-10; seeded from preset, optional override
    "ambition": 5,                        // 0-10; seeded from preset, optional override
    "notes": ""                           // free-text voice; optional, may be ""
  },
  "unattended_timeout": null              // null = attended (wait forever) | 0 = immediate auto | N = wait N seconds then auto-accept
}
```

**`completed_tasks[phase]` entry shape.** Each entry is
`{ name, status, plan_version }` where `status` ∈:
- `done` — task ran successfully this session; artifacts exist on disk
- `reused` — task carried over from a prior session run; artifacts exist
- `skipped` — task explicitly skipped via `/dikw-context` SKIP verdict; no artifact requirement
- `failed` — task ran and failed; artifacts may be partial
- `invalidated` — task was dropped by a later plan revision; its folder may still exist but is not counted toward gate completion or the final report

The pre-gate artifact check enforces artifact existence ONLY for entries
with status `done` or `reused`. When recomputing `pending_tasks` after
a `revise` outcome, the orchestrator excludes any name already in
`completed_tasks[phase]` with status in `{done, reused, skipped}`.
Names with status `failed` or `invalidated` are eligible to re-enter
`pending_tasks` if the new plan re-adds them.

**`gate_persona` is locked for the whole session by default.** It is
written once at `/dikw` Stage 4 and is normally not modified between
phases. `/dikw-gate` reads this field at every firing to compose its
reviewer voice. A user MAY request a one-off persona override at a
single gate; the override applies only to that gate firing and the
`gate_persona` in state remains unchanged. If the field is missing
(legacy state), default to `{preset: "balanced", strictness: 5,
ambition: 5, notes: ""}` and log a migration note.

**`unattended_timeout` controls who clicks the accept button at each
gate.** Set once at `/dikw` Stage 4 from CLI flags; locked for the
session.

| Value | Mode | Behavior at every gate |
|-------|------|------------------------|
| `null` | 🧑 attended (default) | Wait indefinitely for human reply (A/B/C/D/E) |
| `N > 0` | ⏳ timed | Print proposal + countdown; wait up to N seconds; if no reply, auto-accept the proposal verbatim (reply A) |
| `0` | 🤖 unattended | No wait; auto-accept the proposal immediately |

The field is read by both session skills before every gate firing.
Auto-acceptance applies the gate's proposed outcome verbatim — the
gate's proposal logic (and its `revise [feedback]`, `done` constraints)
is unchanged. MAX_REVISIONS enforcement still fires; if the gate
auto-accepts a `revise` past the cap, the force-approve audit trail
records it normally.

If the field is missing (legacy state), default to `null` (attended)
and log a migration note. The deprecated `--auto` flag is accepted as
an alias for `unattended_timeout=0`.

Update after every task completion, every gate outcome, and every state
transition. This file is the only source of truth for resume-after-compaction.

## Pre-session requirement

Before entering the first phase, verify `{snapshot_dir}/exploration/explore_notes.md`
exists (produced by `/dikw` at Stage 4.5, snapshot-level, shared across sessions).
If missing, run `/dikw-explore {snapshot_dir}` once before starting the loop.

### Execution-mode check (at session start / resume)

Read `DIKW_STATE.json.execution_mode`:

- `"inline"` → this skill (`/dikw-session`) is the correct executor. Proceed.
- `"agent"`  → this session was created by `/dikw-session-agent`. **Abort**
               with a message: *"This session's execution_mode is 'agent'.
               Run `/dikw-session-agent {snapshot_dir} {aim}` (or
               `/dikw {folder} --agents`) to resume it, or start a new
               session."*
- missing    → legacy session (created before mode-locking). Assume
               `"inline"` and write it back to DIKW_STATE on next state
               update.

This check prevents the two session skills from stomping on each
other's sessions when resuming.

## Gate presentation (mandatory tables)

Any gate that proposes or adds tasks MUST render them as **one markdown
table per affected phase** with full descriptions — never a comma list.
Columns: `#` / `Task` / `Description`. This applies to:
- `G-plan` (every plan version, v1 and v2+)
- `G-D` / `G-I` / `G-K` / `G-W` when outcome is `revise` (the next G-plan
  will own the actual task table; this gate just shows the trigger)
- `G-report` final check

End every human gate message with the A/B/C/D/E option block (see the
"Gate option mapping" rule below). The A–E letters map internally to
outcomes (`approve / revise [feedback] / done / cancel`) — do
not show the free-text vocabulary in the prompt line.

Under `--auto`, print the same tables + auto-accept line ("Auto-accepting
the proposed outcome under `--auto`").

## Iteration patterns

Every non-forward outcome is `revise [feedback]` and routes to plan.
What differs is what plan-v{N+1} chooses to do with the feedback.

### Pattern 1 — Revise (any non-forward correction)

The gate flags an issue; plan decides how to address it.

```
phase=D · step=gate · G-D · proposal: revise "click_rate nulls not handled"
  → current_phase = plan; plan_version 1 → 2
  → /dikw-context plan  (full load: explore + all reports + gates)
  → /dikw-plan "<feedback>"  writes plan-raw-v2.yaml
  → plan-v2 may add a new D-task, modify the existing D-task spec,
    or mark earlier-phase tasks for re-run
  → G-plan v2 → user approves
  → current_phase = (earliest changed phase, e.g. D)
  → resume forward (skip already-valid tasks)
```

```
phase=I · step=gate · G-I · proposal: revise "time column not profiled in D"
  → current_phase = plan; plan-v1 → plan-v2
  → plan-v2 includes a fresh D-task to profile the time column
  → G-plan v2 → approve
  → current_phase = D, run new D-task, G-D approve
  → I, K, ... continue forward
```

```
phase=K · step=gate · G-K · proposal: revise "K needs hourly profile from D"
  → current_phase = plan; plan-v2 reframes D and may re-spec I
  → G-plan v2 → approve
  → current_phase = D (earliest changed phase; skip past valid I/K
    if plan-v2 didn't touch them)
```

### Pattern 2 — Jump to report

`done` is only valid at G-K, G-W, or G-report. From earlier gates,
propose `revise [feedback]` and let the planner compress.

```
phase=K · step=gate · G-K · proposal: done "K findings + W not needed; question is descriptive"
  → current_phase = report
  → /dikw-report produces final_output.md
```

## Recovery from context compaction

On startup, read `DIKW_STATE.json`:
1. `current_phase` + `current_step` + `current_task|current_gate` = exact position
2. **State-vs-disk consistency check** (mandatory, runs before re-entering the loop):
   for each entry in `completed_tasks[phase]` whose status is `done` or `reused`:
     - resolve the task's expected folder (`insights/<level>/{L}{NN}-{name}/`)
     - if the folder is missing, OR a required artifact is missing
       (D/I: `report.md` + `analysis.py`; K/W: `report.md`),
       demote the entry: set `status = "failed"`, append the task name back
       to `pending_tasks[phase]`, and log a one-line recovery note to
       `tmp/recovery-{ISO-date}.log` recording what was demoted and why.
   This step must run **before** the orchestrator loop is re-entered, so the
   loop never trusts `completed_tasks` against a disk that has drifted (user
   deletion, partial write on prior crash, external cleanup).
3. Re-enter the orchestrator loop at the recorded position
4. Never re-run a task that still satisfies the "complete iff" rule above
5. `/dikw-context` is always re-run — it's cheap and picks up any further
   state drift that occurred since the consistency check

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
     Map old gate records (all revise-flavors collapse to a single
     `revise` outcome that routes back to plan; the original feedback
     is preserved in the `feedback` field):
       decision=PROCEED      → outcome=approve
       decision=ADD_TASKS    → outcome=revise "<reason>"   (back to plan)
       decision=GO_BACK <X>  → outcome=revise "<reason>"   (back to plan)
       decision=REVISE_PLAN  → outcome=revise "<reason>"   (back to plan)
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
- **Plan-version write ordering (revise plan).** When applying a `revise`
  outcome, the orchestrator MUST do these steps in this order, with
  `DIKW_STATE.json` written LAST:
  1. Run `/dikw-plan {snapshot_dir} "<feedback>"`. The plan skill writes
     `plan/plan-raw-v{N}.yaml` AND updates `plan/plan-raw.yaml` symlink
     to point at the new file before returning.
  2. Read the new plan's `revision.changes.removed` list and mark each
     removed task in `completed_tasks[phase]` with status `invalidated`.
  3. Recompute `pending_tasks` from the new plan (see "pending_tasks
     recomputation" below).
  4. Write `DIKW_STATE.json` with `plan_version` bumped to N,
     `current_phase = "plan"`, `revisions_count` incremented, and the
     reconciled `completed_tasks` / `pending_tasks` from steps 2–3.
  Never bump `plan_version` in state before the new `plan-raw-v{N}.yaml`
  is on disk. A crash between (1) and (4) leaves the new plan file
  authoritative; on resume, the consistency check + `plan_version` read
  from the symlink target will recover cleanly.
- **`pending_tasks` recomputation.** After a plan write (initial or
  revision), recompute as:
  `pending_tasks[phase] = {task names in new_plan[phase]} − {names in completed_tasks[phase] with status ∈ {done, reused, skipped}}`.
  Names with status `failed` or `invalidated` are eligible to re-enter
  pending if the new plan re-adds them.
- **`done` outcome is restricted to late gates.** Valid only when
  `current_gate ∈ {G-K, G-W, G-report}`. If the gate skill proposes
  `done` at G-plan, G-D, or G-I (or the user picks reply `D` at one of
  those gates — option D should be suppressed there), the orchestrator
  MUST reject the outcome with the message *"`done` is not valid at
  this gate; propose `revise [feedback]` instead so the planner can
  compress the remaining phases"* and re-prompt. This prevents an
  early `done` from skipping K/W reasoning and producing an
  incomplete final report.
- **Gate attendance (`unattended_timeout`).** Read once per gate from
  DIKW_STATE.json. Three modes:
    - `null` — 🧑 attended (default). Wait indefinitely for a human
      reply. The banner status reads `awaiting`.
    - `N > 0` — ⏳ timed. Print the gate proposal, then wait up to
      N seconds for a human reply. Banner status reads
      `awaiting (auto in {N}s)`. If the timer fires first, auto-accept
      the proposal verbatim (equivalent to reply `A`). If a reply
      arrives, use it.
    - `0` — 🤖 unattended. No wait. Auto-accept the proposal
      immediately. Banner status reads `auto-accepted`.
  Auto-acceptance never alters the gate's proposal — the gate's own
  rules (`done` only at G-K/G-W/G-report; `revise` always to plan)
  still apply. MAX_REVISIONS still fires; if the auto-accepted
  outcome is `revise` past the cap, the force-approve audit trail
  records it as usual.
  The deprecated `--auto` CLI flag is accepted as an alias for
  `unattended_timeout=0`.
- **Force-approve audit trail (MAX_REVISIONS cap).** When
  `revisions_count >= MAX_REVISIONS` and the gate proposes `revise`,
  the orchestrator force-downgrades the outcome to `approve` so the
  pipeline can advance. The audit trail MUST capture this clearly:
  1. The gate file `gates/{NN}-G-<phase>.md` is written with a
     `**FORCED APPROVAL**` banner at the top, recording the original
     proposed outcome (`revise`), the feedback text, and the cap
     value (e.g. *"Forced approve at MAX_REVISIONS=3; original
     proposal was `revise "<feedback>"`"*).
  2. The `gates[]` entry in `DIKW_STATE.json` adds two fields:
     `"forced_by_cap": true` and `"original_outcome": "revise"` (with
     the feedback preserved under `"original_feedback"`). The
     `outcome` field stays `"approve"` so resume logic still routes
     forward.
  3. The user is shown a one-line warning in the banner:
     *"⚠️ MAX_REVISIONS reached; auto-advancing. See gate file for
     original proposal."*
  Without this audit trail, a user reading the gate transcript sees
  the gate suggest `revise` but the pipeline move forward with no
  visible reason — looks like a bug.
- **Task is complete iff all required files exist, are non-empty, and cover the task scope concisely (max ~1000 words).**
  Required files per phase (matches each sub-skill's contract):
  - **D** (`insights/data/D{NN}-.../`): `report.md` + `analysis.py`
  - **I** (`insights/information/I{NN}-.../`): `report.md` + `analysis.py`
  - **K** (`insights/knowledge/K{NN}-.../`): `report.md` only (reasoning-only phase)
  - **W** (`insights/wisdom/W{NN}-.../`): `report.md` only (reasoning-only phase)
  For D/I, a folder holding `report.md` but no `analysis.py` is **not
  complete** — the orchestrator took a shortcut or the sub-skill failed
  its contract. The pre-gate check (below) must override the gate's
  proposal with
  `revise "task X missing analysis.py — re-run /dikw-<phase> <task>"`.
- NEVER re-run a task that meets the "complete iff" rule above
  unless the gate explicitly invalidated it.
- **Pre-gate artifact check (runs automatically before `/dikw-gate`):**
  For every entry in `completed_tasks[current_phase]` whose status is
  `done` or `reused`, verify its folder contains the required files
  (D/I: report.md + analysis.py; K/W: report.md). Entries with status
  `skipped`, `failed`, or `invalidated` are NOT checked here — they
  carry no artifact contract. Missing artifacts on a `done`/`reused`
  entry → override the gate's proposed outcome with `revise` (back to
  plan) and list each offending task in the gate feedback. Do this
  inside the orchestrator before calling `/dikw-gate`, not after.
- **Sub-skill invocation is mandatory.** The orchestrator MUST invoke
  `/dikw-context` and `/dikw-<phase>` once per task. It MUST NOT
  perform the analysis itself via Bash/Write/Edit. Violations are
  caught by the pre-gate check but should not get that far — see the
  "forbidden shortcuts" list in the Orchestrator loop section.
- **Gate-review delegation is mandatory.** The orchestrator MUST invoke
  `/dikw-gate` once per gate (`G-plan`, `G-D`, `G-I`, `G-K`, `G-W`,
  `G-report`). It MUST NOT write a "Proposed: approve" summary inline.
  `/dikw-gate` is the step that genuinely asks "given all evidence so
  far, should we revise (back to plan), jump to report, or approve?"
  Skipping it turns every gate into an
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
  Do NOT use the verbose free-text vocabulary (`approve / revise
  [feedback] / done / cancel`) in the prompt line — the letters map to
  those outcomes internally (see `dikw-gate/SKILL.md` Step 5 mapping table).
- The final report MUST address the original question — if it doesn't,
  `G-report` should return `revise` with feedback on what's missing.

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
