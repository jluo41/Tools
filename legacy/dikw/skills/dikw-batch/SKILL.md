---
name: dikw-batch
description: "Run /dikw on a list of independent questions from a file. Resolves the snapshot ONCE (one-time exploration), then fans out to the dikw-question-runner subagent — one runner per question, sequential by default. Each question gets its own sessions/NN_{slug}/ folder; insights/ is shared so D/I work is reused across runs via status=reused. Forces --unattended for every runner. Use when the user says /dikw-batch, 'run DIKW on this list of questions', 'batch DIKW', 'questions.md → DIKW pipeline'. Trigger: dikw-batch, batch dikw, list of questions, multi-question dikw, run questions file, fan out dikw."
argument-hint: [folder] [questions_file] [--unattended=Ns] [--agents]
allowed-tools: Bash(*), Read, Grep, Glob, Skill, Agent
---

Skill: dikw-batch
=================

Fan a list of independent DIKW questions across N isolated subagent
runs against ONE shared snapshot. Each question gets its own session
folder; the snapshot, exploration notes, and `insights/` task tree are
shared so cross-question reuse happens automatically (a D-task that
already ran for question 1 is reused via `status=reused` for
question 2 instead of being rerun).

`/dikw-batch {folder} {questions_file} [--unattended=Ns] [--agents]`


Constants
---------

- **UNATTENDED_TIMEOUT_DEFAULT = 0** — batch implies no human at the
  gates, so a non-null `unattended_timeout` is *forced* on every
  runner. The internal type is **integer seconds** (matches the JSON
  schema in `DIKW_STATE.json`: `null | 0 | N`). The CLI surface form
  `30s` is parsed once at Step 3 into the integer `30`. If the caller
  passes `--unattended=Ns`, the integer `N` is forwarded; if they
  omit the flag, the default is `0` (🤖 immediate auto-accept).
  Attended mode (`null` / `--unattended=inf` / no-flag-explicit) is
  rejected with a warning — a 12-question batch with attended gates
  would block on the first question forever. The runner only ever
  sees a non-negative integer; `null` is never forwarded.
- **USE_AGENTS = false** — *default.* Each runner runs `/dikw` in
  inline mode. Set true (`--agents`) to forward `--agents` to every
  runner; the runner then invokes `/dikw {folder} ... --agents`,
  which routes the inner pipeline to `/dikw-session-agent` so each
  D/I/K/W task is dispatched to a phase-specific subagent inside the
  runner's isolated context. (The runner is itself a subagent; `--agents`
  controls only the second hop, the per-task dispatch inside the runner.)
- **PARALLEL = false** — sequential dispatch is the only supported
  mode in v1. Reason: parallel runners against the *same* snapshot
  race on `insights/{D,I,K,W}/` NN allocation (the monotonic counter
  is shared across sessions). A future flag `--parallel=N` will land
  once a file-based NN lock exists. Until then, sequential is correct.
- **MAX_QUESTIONS_WARN = 20** — soft warning, not a hard cap. Beyond
  20, batches commonly take long enough that the user should be
  reminded they can split + run two batches in different terminals.


Pipeline
--------

```
/dikw-batch {folder} {questions_file} [flags]
  │
  ├─ Step 1 — Parse questions
  │    accept .txt (one per line) or .md (list items: -, *, 1.)
  │    strip blanks, comments (#...), and exact duplicates
  │    refuse if 0 questions; warn if > MAX_QUESTIONS_WARN
  │
  ├─ Step 2 — Resolve snapshot ONCE
  │    delegate: /dikw-workspace status {folder}        → does a snapshot exist?
  │    if no:
  │       run /dikw {folder} --dry-run --unattended      → creates snapshot + scaffolding
  │                                                        (--dry-run exits before Stage 5)
  │    if exists but {snapshot}/exploration/explore_notes.md missing:
  │       delegate: /dikw-explore {snapshot}             → one-time exploration
  │    record SNAPSHOT_DIR (absolute) for every runner
  │
  ├─ Step 3 — Force gating mode
  │    parse --unattended=Ns from $ARGUMENTS into integer seconds
  │    if absent or attended → set unattended_timeout = 0   (integer)
  │    if --agents present   → set use_agents = true
  │
  ├─ Step 4 — Sequential fan-out
  │    for i, question in enumerate(questions):
  │        Agent(
  │          subagent_type="dikw-question-runner",
  │          description=f"DIKW {i+1}/{N}: {question[:40]}",
  │          prompt=(
  │            f"folder={FOLDER_ABS}\n"
  │            f"question={question}\n"
  │            f"unattended_timeout={unattended_timeout}\n"
  │            f"use_agents={use_agents}\n"
  │            f"snapshot_dir={SNAPSHOT_DIR}\n"
  │          )
  │        )
  │        record returned summary into rows[]
  │        if runner returns status=failed → flag in rows[], do NOT abort
  │
  └─ Step 5 — Aggregate summary
       print one markdown table:
       | # | aim | revisions | final outcome | auto-accepts | report path | conclusion |
       failed rows show the failure_reason in the conclusion column
```


Step 1 — Parse questions file
------------------------------

Accept two formats. The orchestrator picks by extension; mixing rules
within a single file is allowed but discouraged.

**`.txt` — one question per line:**
```
What CGM patterns exist in the morning hours?
Does meal timing predict post-prandial spikes?
# this is a comment line — stripped
How does exercise interact with insulin dosing?
```

**`.md` — markdown list items:**
```
- What CGM patterns exist in the morning hours?
- Does meal timing predict post-prandial spikes?
1. How does exercise interact with insulin dosing?
* Are there outlier days the model should ignore?
```

Parser:
1. Strip BOM + trailing whitespace per line.
2. Drop blank lines.
3. Drop lines starting with `#` (comments).
4. For `.md`, strip leading `-`, `*`, `1.`, `2.` etc. and surrounding whitespace.
5. Dedupe by **lowercase normalized whitespace** (collapse runs of
   spaces, lowercase). Keep the first occurrence's original casing.
6. Refuse with a clear error if 0 questions remain.
7. Warn if `len(questions) > MAX_QUESTIONS_WARN` (20). Continue anyway.


Step 2 — Resolve snapshot ONCE
-------------------------------

Batch mode runs N questions against **one shared snapshot**. This is
the whole point: D/I findings produced for question 1 are reused
verbatim for question 2 (via the existing `status=reused` mechanism in
`completed_tasks`), saving compute and keeping insights consistent.

Resolution order:

```
FOLDER_ABS = realpath({folder})

if {FOLDER_ABS}/_agent_dikw_space/snapshot-*/ exists:
    SNAPSHOT_DIR = newest snapshot
else:
    Skill(name="dikw", args=f"{FOLDER_ABS} --dry-run --unattended")
    # Under --dry-run + --unattended, /dikw runs Stages 0..4
    # NON-INTERACTIVELY:
    #   - Stage 4 Part A (persona) auto-defaults to `balanced`
    #     (UNATTENDED_TIMEOUT=0 skips the prompt).
    #   - Stage 4 Part B (proceed?) does NOT prompt at all under
    #     DRY_RUN=true — Stage 4 just prints the layout and returns.
    # The scaffold (manifest.yaml, source/, insights/, sessions/, tmp/)
    # is written during Stage 2 before any prompt would fire, so the
    # snapshot is on disk when /dikw returns. See dikw/SKILL.md § "Stage 4".
    SNAPSHOT_DIR = newest snapshot just created

if not exists {SNAPSHOT_DIR}/exploration/explore_notes.md:
    Skill(name="dikw-explore", args=SNAPSHOT_DIR)
```

Print a one-line confirmation:
```
📷 Snapshot:    {SNAPSHOT_DIR}     (reused | created-during-batch)
🔍 Exploration: {SNAPSHOT_DIR}/exploration/explore_notes.md
🧑 Questions:   {len(questions)}    (from {questions_file})
```

When `--new-snapshot` is desired *per question* (rare — usually you
want shared insights), do not use `/dikw-batch`; loop yourself in the
shell:

```bash
while IFS= read -r q; do
    /dikw {folder} "$q" --new-snapshot --unattended
done < questions.txt
```


Step 3 — Force gating mode
---------------------------

Parse the orchestrator's flags:

| Caller flag | Internal value (integer seconds) |
|---|---|
| `--unattended` | `unattended_timeout = 0` (🤖 immediate auto-accept) |
| `--unattended=Ns` | `unattended_timeout = N` (⏳ timed grace) |
| `--unattended=inf` | rejected with warning, falls back to `0` (attended is forbidden in batch) |
| `--auto` | legacy alias → `unattended_timeout = 0` |
| (no flag) | `unattended_timeout = 0` (forced default) |
| `--agents` | `use_agents = true` |

The runner receives the integer; it re-emits the CLI form
(`--unattended` for `0`, `--unattended={N}s` for `N>0`) when invoking
`/dikw`. There is no stringified `"30s"` value crossing the
agent-boundary — only integers and the JSON `null` (which batch
never produces).

Natural-language equivalents accepted by `/dikw` are also accepted
here ("run unattended", "wait 30s at gates", "use agents"). The
orchestrator parses them once into the canonical form before
dispatching.

Reason for the forced default: a batch with attended gates blocks on
the first question's plan-gate forever. There is no human at the
console answering each gate prompt across N pipelines.


Step 4 — Sequential fan-out
----------------------------

Dispatch the runner sequentially, one question at a time. Each call
is a single `Agent` tool invocation:

```
rows = []
for i, question in enumerate(questions, start=1):
    summary = Agent(
        subagent_type="dikw-question-runner",
        description=f"DIKW {i}/{N}: {question[:40]}",
        prompt=(
            f"folder={FOLDER_ABS}\n"
            f"question={question}\n"
            f"unattended_timeout={unattended_timeout}\n"
            f"use_agents={use_agents}\n"
            f"snapshot_dir={SNAPSHOT_DIR}\n"
        )
    )
    rows.append({
        "i": i, "question": question, **summary
    })
    print one-line progress: f"[{i}/{N}] {summary.aim} → {summary.final_outcome}"
```

**Why sequential and not parallel:** within one snapshot, the
`insights/{D,I,K,W}/` folders share a monotonic NN counter (see
`docs/5-snapshot-layout.txt` § "NN-monotonic"). Two parallel runners
that both want to allocate `D03-...` for different work would race.
Until a file-based NN lock exists, sequential is the only safe mode.

**Failure handling — continue, don't abort.** If a runner returns
`status=failed`, the row is flagged in the summary table but the
remaining questions still run. One bad question (e.g. a force-approve
at MAX_REVISIONS, or a crashed phase skill) does not kill the batch.

The orchestrator does NOT track its own state file — there is no
`DIKW_BATCH_STATE.json`. If `/dikw-batch` is interrupted, the user
re-invokes it on the same folder + questions file; questions whose
session folders already exist with `status=complete` in their
`DIKW_STATE.json` are skipped (a one-line note appears in the
summary). Per-question resumability is already guaranteed by the
existing per-session `DIKW_STATE.json`; nothing extra is needed.


Step 5 — Aggregate summary
---------------------------

Print one markdown table to the transcript:

```
DIKW Batch Summary — {len(questions)} questions, snapshot {SNAPSHOT_DIR}

| # | aim | rev | outcome | auto | report | conclusion |
|---|-----|----:|---------|----:|--------|------------|
| 1 | 01_cgm-pattern-inventory  | 0 | approve         | 6 | sessions/01_.../output/final_output.md | Found 3 dawn patterns, ... |
| 2 | 02_meal-spike-presence    | 1 | approve         | 7 | sessions/02_.../output/final_output.md | Meal timing predicts ... |
| 3 | 03_exercise-insulin-shift | — | failed (Step 4) | — | —                                       | force-approved at MAX_REVISIONS=3 |
| 4 | 04_outlier-day-screen     | 0 | done (G-K)      | 5 | sessions/04_.../output/final_output.md | Two days flagged, ... |
```

Columns:
- `#` — input order
- `aim` — `NN_{slug}` of the session
- `rev` — `revisions_count`; `—` for failed runs
- `outcome` — last gate outcome (`approve` / `revise` / `done` / `force-approved`)
- `auto` — count of AUTO-ACCEPTED gate banners
- `report` — relative path under the snapshot to `final_output.md`
- `conclusion` — first 1–2 sentences from `final_output.md` (truncate to ~120 chars)

After the table, print the snapshot path and a one-line tip:

```
📂 Snapshot: {SNAPSHOT_DIR}
💡 Re-run a single question: /dikw {folder} "<question>" --unattended
🔍 Inspect a session:        /dikw-workspace status {SNAPSHOT_DIR}/sessions/{aim}
```


Commands
--------

```
/dikw-batch {folder} questions.md                       → 🤖 unattended (forced), inline runners
/dikw-batch {folder} questions.txt --unattended=30s     → ⏳ timed grace per gate (30s)
/dikw-batch {folder} questions.md --agents              → forward --agents to every runner
/dikw-batch {folder} questions.md --unattended=60s --agents
```

Natural-language equivalents are also accepted ("run this list of
questions", "batch these unattended", "use agents on each"). The
orchestrator parses them into the canonical CLI form before Step 3.


Rules
-----

- ALWAYS resolve `{folder}` to an absolute path before any shell
  command (same reason as `/dikw` Stage 0 — relative paths drift
  between turns).
- ALWAYS resolve the snapshot ONCE before fanning out. Running
  exploration N times defeats the entire point of batch mode.
- ALWAYS force `unattended_timeout` to a non-null value. Attended
  batches deadlock.
- Sequential dispatch only in v1. Do NOT parallelize until a
  file-based NN lock for `insights/` exists.
- Continue on per-question failure. The summary flags rows; the run
  does not abort. The user re-runs failed questions individually.
- Never write a batch-level state file. Per-question state files
  already make the work resumable.
- Never short-circuit a runner — always go through
  `Agent(dikw-question-runner)`. Inlining the loop in the main
  conversation defeats context isolation, the only reason agent mode
  is worth using here.
- The runner may itself use `--agents` (two-level nesting). The
  outer batch passes the flag through; the runtime handles the
  nested dispatch fine.
