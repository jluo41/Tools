---
name: dikw
description: "Run DIKW analysis on any folder. Detects the folder type, creates a dated snapshot, shows the path layout, confirms once, then runs the full D→I→K→W pipeline against the snapshot. Use when the user says /dikw, 'run DIKW on this folder', 'analyze this patient', 'run DIKW analysis end-to-end'. Trigger: dikw, run dikw, analyze folder, DIKW on Subject, DIKW on dataset."
argument-hint: [folder] [question]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Skill
---

Skill: dikw
===========

Top-level DIKW entry point. One command to run end-to-end analysis on any
folder — Subject-*/ data, raw dataset dumps, or existing DIKW projects.

`/dikw {folder} [question]`


Constants
---------

- **AUTO_PROCEED = false** — *default.* Pause at every DIKW gate for human
  approval (`G-plan` after the plan is written, and each post-phase gate). Set true
  (`--auto`) to let gates auto-decide for unattended runs.
- **NEW_SNAPSHOT = false** — default reuses the latest `snapshot-<date>/` if
  one exists. Set true (`--new-snapshot`) to force a fresh snapshot folder.
- **COPY_MODE = "copy"** — default `source/` contains real file copies (the
  snapshot is self-contained and archivable). Set to `"symlink"` via
  `--symlink` when the data is large and you want to avoid duplication.
- **DRY_RUN = false** — set true (`--dry-run`) to print the layout + what would
  happen, then exit without running anything.
- **USE_AGENTS = false** — *default.* Delegate Stage 6 to `/dikw-session`
  (inline skill mode). Set true (`--agents`) to delegate to
  `/dikw-session-agent` instead — same state machine, but each task
  (plan, D, I, K, W) is dispatched to a phase-specific subagent for
  context isolation and optional parallel dispatch. The report phase
  stays inline in both modes. File outputs are identical across modes.


Pipeline
--------

```
/dikw {folder} [question]
  │
  ├─ Stage 0 — Resolve & detect
  │    detect Subject / plain-data / existing DIKW project
  │    compute resolved project root
  │
  ├─ Stage 1 — Snapshot
  │    reuse latest existing snapshot, or create snapshot-<date>/
  │
  ├─ Stage 2 — Scaffold workspace
  │    create snapshot-<date>/{manifest.yaml, source/, insights/, sessions/, tmp/}
  │    COPY data files into source/ (or symlink if --symlink)
  │
  ├─ Stage 2.5 — Generate session aim
  │    compute aim string NN_{slug} (see Stage 2.5 body for full rules)
  │
  ├─ Stage 3 — Layout preview
  │    delegate: /dikw-workspace layout {snapshot_dir}
  │    prints path contract with ✅/⬜ markers, using the concrete {aim}
  │
  ├─ Stage 4 — Gate (one confirm, human)
  │    Part A — Gate persona (locked for whole session; see Stage 4 body below)
  │      Ask: "Gate reviewer persona? (A) strict  (B) balanced [default]
  │             (C) creative  (D) lenient  (E) custom"
  │      If E: follow-up for strictness (0-10), ambition (0-10), notes (free text)
  │      Write to {snapshot_dir}/sessions/{aim}/DIKW_STATE.json → gate_persona
  │    Part B — Proceed confirm
  │      "Proceed? (yes / dry-run / revise "question" / revise-aim "slug" / cancel)"
  │
  ├─ Stage 4.5 — Initial explore (if no snapshot-level exploration/ exists)
  │    delegate: /dikw-explore {snapshot_dir}
  │    writes snapshot-level exploration/explore_notes.md
  │    (one-time per snapshot; reused by all sessions)
  │
  └─ Stage 5 — Run session
       if USE_AGENTS (--agents):
           delegate: /dikw-session-agent {snapshot_dir} {aim} [question]
       else:
           delegate: /dikw-session       {snapshot_dir} {aim} [question]
       runs phases plan → D → I → K → W → report → done.
       Each phase has 2 steps: task (execute work) then gate (review + outcome).
       Gate outcomes: approve / revise <phase> [feedback] / done.
       Writes into insights/ + sessions/{aim}/.
```


Folder Layout (what Stage 2 creates)
-------------------------------------

```
{folder}/
└── _agent_dikw_space/                         ← agent-owned, do not hand-edit
    └── snapshot-2026-04-21/                   ← one per data state
        ├── manifest.yaml                      ← file list + hashes + sizes
        ├── exploration/                       ← SNAPSHOT-LEVEL (one-time per snapshot)
        │   └── explore_notes.md               ← produced by /dikw-explore at Stage 4.5
        ├── source/                            ← mirrors original tree (copies by default)
        │   ├── 1-SourceStore/
        │   │   ├── CGM.parquet
        │   │   └── ...
        │   └── 2-RecStore/
        │       └── Record-HmPtt.Diet5Min/RecAttr.parquet
        ├── insights/                          ← DIKW outputs, per-task folders
        │   ├── data/                          ← D (folder prefix: D01, D02, …)
        │   │   └── D01-col_overview/
        │   │       ├── report.md
        │   │       ├── analysis.py
        │   │       └── chart.png
        │   ├── information/                   ← I (folder prefix: I01, I02, …)
        │   │   └── I01-cgm_trend/
        │   │       ├── report.md
        │   │       └── analysis.py
        │   ├── knowledge/                     ← K (folder prefix: K01, K02, …)
        │   │   └── K01-pattern_synthesis/
        │   │       └── report.md
        │   └── wisdom/                        ← W (folder prefix: W01, W02, …)
        │       └── W01-recommendations/
        │           └── report.md
        ├── sessions/                          ← per-question runs
        │   └── NN_{slug}/                     ← e.g. 01_dawn-phenomenon-presence
        │       ├── question.md
        │       ├── plan/
        │       │   ├── plan-raw.yaml              ← symlink to latest version
        │       │   ├── plan-raw-v1.yaml           ← initial
        │       │   └── plan-raw-v2.yaml           ← after revise plan
        │       ├── gates/                         ← sequential NN counter across whole session
        │       │   ├── 00-G-plan.md               ← e.g. first gate: plan v1 approval
        │       │   ├── 01-G-D.md
        │       │   ├── 02-G-I.md                  ← (→ if this returns "revise plan", next is 03-G-plan.md for v2)
        │       │   └── …
        │       ├── output/final_output.md
        │       └── DIKW_STATE.json
        └── tmp/                               ← temp execution logs
```

Numbering rules:
  - Task folders are `{L}{NN}-{task_name}` where:
      - `L` is the level letter (`D` for data, `I` for information,
        `K` for knowledge, `W` for wisdom)
      - `NN` is `01`, `02`, … in execution order within that level
    Examples: `D01-cgm_overview`, `I02-diurnal_profile`, `K01-pattern_synthesis`,
    `W01-recommendations`. Gate-added tasks get the next number within their level.
  - Task name (without `{L}{NN}-`) stays the canonical key in `plan-raw.yaml`.


Stage 0 — Resolve & detect
---------------------------

**FIRST: resolve `{folder}` to an absolute path.** Shell cwd can drift between
turns (after `/compact`, after subshell exits, after prior `cd` commands), so
relative paths passed as `{folder}` are unsafe. Run once:

```
FOLDER_ABS=$(realpath "{folder}")   # or: cd "{folder}" && pwd
```

Use `FOLDER_ABS` (and `SNAPSHOT_DIR` derived from it — also absolute) in
EVERY subsequent `mkdir`, `ln`, `cat >`, or path reference. Never pass the
raw `{folder}` arg to a shell command after this stage. Never `cd` without
`cd "$FOLDER_ABS"` first.

Then inspect `$FOLDER_ABS`:

```
if $FOLDER_ABS/manifest.yaml exists with subject_id + 1-SourceStore/:
    kind = "subject"
    source_roots = [$FOLDER_ABS/1-SourceStore/, $FOLDER_ABS/2-RecStore/]

elif $FOLDER_ABS/_agent_dikw_space/ exists:
    kind = "existing_dikw"
    source_roots = derived from existing manifest.yaml

else:
    kind = "plain"
    source_roots = [$FOLDER_ABS]   ← treat all files in folder as data
```

Record `FOLDER_ABS`, `kind`, and `source_roots` for later stages.


Stage 1 — Snapshot
-------------------

```
SNAPSHOT_ROOT = {folder}/_agent_dikw_space
latest = newest snapshot-*/ folder under SNAPSHOT_ROOT (or none)

if NEW_SNAPSHOT=true OR latest is None:
    today = YYYY-MM-DD
    if {SNAPSHOT_ROOT}/snapshot-{today}/ exists:
        suffix = next letter (b, c, d...)
        snapshot_dir = {SNAPSHOT_ROOT}/snapshot-{today}-{suffix}/
    else:
        snapshot_dir = {SNAPSHOT_ROOT}/snapshot-{today}/
    is_new = true
else:
    snapshot_dir = latest
    is_new = false
```


Stage 2 — Scaffold workspace
-----------------------------

If `is_new`:

  1. `mkdir -p` the snapshot directory tree:
     ```
     {snapshot_dir}/source/
     {snapshot_dir}/insights/{data,information,knowledge,wisdom}/
     {snapshot_dir}/sessions/
     {snapshot_dir}/tmp/
     ```
     Note: `exploration/` is NOT created here. `/dikw-explore` creates it at
     Stage 4.5 and writes `exploration/explore_notes.md`.

  2. Mirror each `source_root` into `{snapshot_dir}/source/` preserving its
     full relative directory structure. For a Subject folder, this gives:
     ```
     source/
     ├── 1-SourceStore/
     │   ├── CGM.parquet
     │   └── ...
     └── 2-RecStore/
         └── Record-HmPtt.Diet5Min/RecAttr.parquet
     ```
     - If `COPY_MODE=="copy"` (default): copy files, preserving the tree.
       `cp -r` or `rsync -a` works; keep directory structure intact.
     - If `COPY_MODE=="symlink"` (via `--symlink`): recreate the directory
       tree with `mkdir -p`, then symlink each file into its mirrored path.
     - For structured `source_roots` (e.g. Subject `1-SourceStore/` +
       `2-RecStore/`), never flatten names — the tree IS the namespace, so
       collisions are impossible.
     - For `kind="plain"` (single flat `source_root` with no meaningful
       subtree), flat basenames in `source/` ARE allowed; on basename
       collision append a numeric suffix (`CGM.parquet` →
       `CGM-2.parquet`). See "Plain folder" in *Input detection details*.

  3. Write `{snapshot_dir}/manifest.yaml`:
     ```yaml
     created_at: "2026-04-21T14:30:00"
     created_by: "/dikw v0.1"
     folder: "{absolute path to {folder}}"
     kind: "subject"  # or "plain" / "existing_dikw"
     copy_mode: "copy"  # or "symlink"
     source_roots:
       - "1-SourceStore/"
       - "2-RecStore/"
     files:
       - path: "CGM.parquet"
         abs: "/WellDoc-SPACE/.../Subject-559/1-SourceStore/CGM.parquet"
         bytes: 12345
         sha256: "abcd..."
       - ...
     ```

If not `is_new`, skip this stage (reuse existing scaffolding).


Stage 2.5 — Generate session aim
---------------------------------

Generate the session aim **before** the layout preview so Stages 3 and 4 can
show the concrete name (not a `NN_{slug}` placeholder) and the gate can offer
a `revise-aim` option.

```
NN = (max NN across existing {snapshot_dir}/sessions/NN_* folders) + 1
     zero-padded to 2 digits ("01", "02", …); "01" if no prior sessions.

slug = 3–5 kebab-case tokens of shape {domain}-{phenomenon}-{intent}
       - name the specific phenomenon, not the topic area
       - drop stopwords: what / is / are / the / does / do / exist / have / how / why
       - forbid generic suffixes: -analysis, -study, -check, -review, -exploration
       - model-generated by intent from the question; literal-token fallback on failure
       (full rules: dikw-session/SKILL.md § "Session naming")

aim = "{NN}_{slug}"          e.g. "01_cgm-pattern-inventory"
```

Do NOT create `sessions/{aim}/` here — that is `/dikw-session`'s job in
Stage 5. Stage 2.5 only computes the aim string.

**Announce the aim prominently to the user** as a standalone line before
Stage 3 (layout preview), so the session slug is visible as a first-class
artifact rather than buried inside the SESSION block. Format:

```
📛 Session aim: {aim}
   slug rationale: {domain} + {phenomenon} + {intent}
   (from question "{question}")
```

Example:

```
📛 Session aim: 01_cgm-pattern-inventory
   slug rationale: cgm + pattern + inventory
   (from question "What CGM patterns exist")
```

Under `--auto` (AUTO_PROCEED=true): if the model-generated slug fails
validation (too short/long, banned suffix, stopword-only), fall back to the
literal-token slug from `dikw-session/SKILL.md § "Session naming"` and
proceed — do NOT prompt. Under interactive mode (default), a failing slug
triggers one re-generation attempt; if it still fails, surface the error at
the Stage 4 gate so the user can `revise-aim "..."`.


Stage 3 — Layout preview
-------------------------

Delegate to `/dikw-workspace layout {snapshot_dir}`. It prints:

```
DIKW Workspace: {snapshot_dir}

SOURCE (✅ frozen at 2026-04-21T14:30:00)
  ✅ source/CGM.parquet          →  ../../../1-SourceStore/CGM.parquet
  ✅ source/Diet.parquet          →  ../../../1-SourceStore/Diet.parquet
  ... (N files total)

INSIGHTS (to be produced this session)
  ⬜ insights/data/D{NN}-{task}/           — D-level reports + code
  ⬜ insights/information/I{NN}-{task}/    — I-level reports + code
  ⬜ insights/knowledge/K{NN}-{task}/      — K-level reasoning
  ⬜ insights/wisdom/W{NN}-{task}/         — W-level reasoning

SESSION (new — aim generated in Stage 2.5)
  ⬜ sessions/{aim}/                         ← e.g. 01_cgm-pattern-inventory
       ├── question.md
       ├── plan/{plan-raw.yaml, plan-raw-v1.yaml, …}
       ├── gates/{00-G-plan.md, 01-G-D.md, 02-G-I.md, …}  ← sequential NN counter
       ├── output/final_output.md
       └── DIKW_STATE.json

TEMP (auto-cleaned)
  ⬜ tmp/
```


Stage 4 — Gate (one confirm)
-----------------------------

Two parts, presented in order: (A) pick gate persona, (B) confirm proceed.

**Part A — Gate persona selection.** The reviewer voice for every
`/dikw-gate` firing in this session is chosen once here and locked.
Use `AskUserQuestion` with these four presets (plus the automatic
"Other" option for custom):

| Letter | Preset      | Tendency                                              |
|--------|-------------|-------------------------------------------------------|
| A      | `strict`    | Harsh on evidence gaps; defaults to `revise plan`     |
| B      | `balanced`  | Current default; revises when surprises found         |
| C      | `creative`  | Tolerates directional claims; pushes for richer K/W   |
| D      | `lenient`   | Approves unless artifact is missing                   |

If user picks `Other` (custom), ask three follow-ups via AskUserQuestion:
  1. `strictness` 0–10 (integer) — evidence bar
  2. `ambition`   0–10 (integer) — richness bar
  3. `notes` — free-text voice (may be empty); e.g. "Act as Reviewer 2"

Write the choice into `{snapshot_dir}/sessions/{aim}/DIKW_STATE.json`
under key `gate_persona` with shape:

```json
{"preset": "balanced", "strictness": 5, "ambition": 5, "notes": ""}
```

For the four presets, use these seeded axes:

| preset   | strictness | ambition |
|----------|-----------:|---------:|
| strict   |          8 |        4 |
| balanced |          5 |        5 |
| creative |          3 |        8 |
| lenient  |          2 |        3 |

The user's custom overrides (if any) replace the seeded values for
the axes they specified. `notes` is always optional.

**Lock rule:** once Stage 4 Part A is accepted, `gate_persona` must
NOT be modified for the rest of this session. `/dikw-session` treats
it as read-only. A future session (new `/dikw` invocation) can set a
different persona.

If `AUTO_PROCEED=true` and no persona has been set on the CLI, default
to `balanced` and skip the prompt.

**Part B — Proceed confirm.** Present:

```
📋 About to run DIKW on {folder}
   Kind:     {kind}
   Snapshot: {snapshot_dir} ({is_new ? "new" : "reused"})
   📛 Aim:   {aim}          ← session folder: sessions/{aim}/
   Question: {question}
   👓 Gate persona: {preset} (strictness={N}, ambition={N}{, notes=…})

Proceed?  (yes / dry-run / revise "new question" / revise-aim "new-slug" / cancel)
```

If `DRY_RUN=true`: print the above and EXIT (do not run Stage 5).
If `AUTO_PROCEED=true`: pause 10 seconds, default to yes.
Else: wait for explicit user input.

User responses:
  - `yes` → Stage 4.5 → Stage 5
  - `dry-run` → exit
  - `revise "..."` → update question, re-derive aim from new question, re-show, re-ask
  - `revise-aim "..."` → override slug only (keep NN); validate against the
    naming rules in `dikw-session/SKILL.md § "Session naming"`, then re-show
  - `cancel` → abort (keep the scaffolded snapshot for later use)

CLI shortcuts (skip the AskUserQuestion prompts):
  - `/dikw {folder} "{question}" --persona strict|balanced|creative|lenient`
  - `/dikw {folder} "{question}" --persona custom --strictness 8 --ambition 4 --persona-notes "..."`


Stage 5 — Run session
----------------------

**Before delegating**, initialize the session folder (once, only on first
run of this aim):

```
mkdir -p {snapshot_dir}/sessions/{aim}/{plan,gates,output}
write    {snapshot_dir}/sessions/{aim}/question.md  ← the literal question text
write    {snapshot_dir}/sessions/{aim}/DIKW_STATE.json with:
  {
    "status": "running",
    "aim": "{aim}",
    "questions": "{question}",
    "execution_mode": "agent" if USE_AGENTS else "inline",
    "current_phase": "plan",
    "current_step": "task",
    "current_task": null,
    "current_gate": null,
    "plan_version": 0,
    "completed_tasks": {"D": [], "I": [], "K": [], "W": []},
    "pending_tasks":   {"D": [], "I": [], "K": [], "W": []},
    "phase_history": [],
    "gates": [],
    "revisions_count": 0,
    "gate_persona": {<from Stage 4 Part A>}
  }
```

The `execution_mode` field locks which session skill is allowed to run
or resume this session. It's set once at session creation from
`USE_AGENTS` and NEVER rewritten. On resume, the invoked session skill
(`/dikw-session` or `/dikw-session-agent`) must match this field, or
refuse to start.

If `question.md` or `DIKW_STATE.json` already exists (resume after
compaction), leave them alone — the user is picking up a prior run.
If the existing state's `execution_mode` disagrees with `USE_AGENTS`
for this invocation, abort with a message telling the user to either
pass the matching flag or start a new session.

Then delegate to the session skill, passing the aim computed in Stage 2.5.
The session skill is chosen by the `USE_AGENTS` constant:

```
if USE_AGENTS (--agents):
    /dikw-session-agent {snapshot_dir} {aim} {question}
else:
    /dikw-session       {snapshot_dir} {aim} {question}
```

Both session skills handle:
  - explore → plan → gate → D → gate → I → gate → K → gate → W → gate → report
  - writes into `{snapshot_dir}/insights/` + `{snapshot_dir}/sessions/{aim}/`
  - DIKW_STATE.json updates for resume-after-compaction

The only difference is execution of task steps: `/dikw-session` invokes
the phase skill inline (`Skill(dikw-<phase>)`), while
`/dikw-session-agent` dispatches each task to a phase-specific subagent
(`dikw-planner`, `dikw-data-executor`, `dikw-information-executor`,
`dikw-knowledge-executor`, `dikw-wisdom-executor`). The report phase
stays inline in both modes. File outputs are identical.

Important: per-task artifacts (`analysis.py`, `report.md`, charts) are
produced by `/dikw-<phase>` sub-skills invoked by the session orchestrator
— NOT by `/dikw` itself, and NOT by batched Bash/pandas heredocs. The
session enforces a pre-gate artifact check that rejects tasks with missing
`analysis.py` (for D and I). See `dikw-session/SKILL.md` → Rules.

On completion, print the final report path:
```
✅ DIKW session complete.
   Final report: {snapshot_dir}/sessions/{aim}/output/final_output.md
   Insights:     {snapshot_dir}/insights/
```


Input detection details
------------------------

**Subject-*/ folder** (haipipe-subject):
  - Has `manifest.yaml` at folder root with `subject_id` key
  - Has `1-SourceStore/` with parquet files
  - Has `2-RecStore/` with record folders
  - `source/` mirrors the original tree (copies by default):
    - `source/1-SourceStore/CGM.parquet`
    - `source/2-RecStore/Record-HmPtt.CGM5Min/RecAttr.parquet`
  - `kind: "subject"` in manifest

**Plain folder** (any data directory):
  - No `manifest.yaml` or no `subject_id` key
  - Walk for `*.parquet`, `*.csv`, `*.xml`, `*.json`, `*.jsonl`
  - Symlink each into `source/` (basename only; suffix on collision)
  - `kind: "plain"` in manifest

**Existing DIKW project**:
  - Already has `_agent_dikw_space/` at root
  - Detect the latest snapshot; prompt to reuse or create new


Snapshot reuse semantics
-------------------------

Default: reuse latest snapshot. Insights accumulate across runs on the same
snapshot (e.g., first run explores + D; second run with new question uses the
cached D reports and only runs new I/K/W).

`--new-snapshot`: force fresh snapshot. Insights start empty. Use when:
  - Source data changed meaningfully and you want a clean slate
  - You want an archival frozen record (e.g., "state as of 2026-04-21")

Snapshots are never auto-invalidated. Data drift is the user's call.


Commands
--------

```
/dikw {folder}                        → interactive, prompts for question
/dikw {folder} "question"             → runs with question
/dikw {folder} --dry-run              → layout preview only, no execution
/dikw {folder} --new-snapshot         → force new snapshot
/dikw {folder} --symlink              → symlink data in source/ (skip copy; saves disk for large data)
/dikw {folder} --auto                 → run unattended (AUTO_PROCEED=true); default is to pause at every gate
/dikw {folder} --agents               → use /dikw-session-agent (subagent dispatch); default is /dikw-session (inline)
```


Rules
-----

- ALWAYS resolve `{folder}` to an absolute path at Stage 0 (`realpath`) and use
  that absolute form in every shell command. Relative paths are unsafe because
  shell cwd can drift between turns. One skipped `realpath` has created
  double-nested `Subject-6/_WorkSpace/.../Subject-6/_agent_dikw_space/` junk.
- NEVER write into `{folder}` outside of `_agent_dikw_space/`. User data is untouched.
- ALWAYS write manifest.yaml on snapshot creation — it's the provenance record.
- ALWAYS go through Stage 3 (layout preview) + Stage 4 (confirm gate) before Stage 5.
- If a snapshot exists but `source/` is empty or stale (files removed from user's
  folder), warn and suggest `--new-snapshot`.
- Copies (default) make snapshots truly self-contained — archive + move works
  with no broken links. Only use `--symlink` when source data is too large to
  duplicate and you accept the fragility tradeoff.
- When `--symlink` is used, write relative symlinks (relative to snapshot dir)
  so the snapshot tree is still relocatable together with its data root.
- Compute the session aim exactly ONCE, in Stage 2.5. Stages 3–5 consume it.
  `/dikw-session` must not re-derive or rename the aim; if a user wants a
  different name they must `revise-aim` at the Stage 4 gate before Stage 5
  starts, or edit `sessions/{aim}/` manually after the session completes.


