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

- **AUTO_PROCEED = true** — gates inside `/dikw-session` auto-decide. Set false
  to pause at each DIKW level gate for human review.
- **NEW_SNAPSHOT = false** — default reuses the latest `snapshot-<date>/` if
  one exists. Set true (`--new-snapshot`) to force a fresh snapshot folder.
- **FREEZE = false** — default `source/` contains symlinks. Set true
  (`--freeze`) to copy actual data bytes (reproducible but larger).
- **DRY_RUN = false** — set true (`--dry-run`) to print the layout + what would
  happen, then exit without running anything.

Override example:
  `/dikw Subject-559 "CGM patterns" --new-snapshot --interactive`


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
  │    symlink source/ entries to the actual data files
  │
  ├─ Stage 3 — Layout preview
  │    delegate: /dikw-workspace layout {snapshot_dir}
  │    prints path contract with ✅/⬜ markers
  │
  ├─ Stage 4 — Gate (one confirm, human)
  │    "Proceed? (yes / dry-run / revise question / cancel)"
  │
  └─ Stage 5 — Run session
       delegate: /dikw-session {snapshot_dir} [question]
       runs explore → plan → D → I → K → W → report
       writes into insights/ + sessions/{aim}/
```


Folder Layout (what Stage 2 creates)
-------------------------------------

```
{folder}/
└── _agent_dikw_space/                         ← agent-owned, do not hand-edit
    └── snapshot-2026-04-21/                   ← one per data state
        ├── manifest.yaml                      ← file list + hashes + sizes
        ├── source/                            ← symlinks to data (or copies if --freeze)
        │   ├── CGM.parquet  →  ../../../1-SourceStore/CGM.parquet
        │   └── ...
        ├── insights/                          ← DIKW outputs, per-task folders
        │   ├── data/                          ← D
        │   │   └── 01-col_overview/
        │   │       ├── report.md
        │   │       ├── analysis.py
        │   │       └── chart.png
        │   ├── information/                   ← I
        │   │   └── 01-cgm_trend/
        │   │       ├── report.md
        │   │       └── analysis.py
        │   ├── knowledge/                     ← K (reasoning, no code)
        │   │   └── 01-pattern_synthesis/
        │   │       └── report.md
        │   └── wisdom/                        ← W (reasoning, no code)
        │       └── 01-recommendations/
        │           └── report.md
        ├── sessions/                          ← per-question runs
        │   └── run1/
        │       ├── question.md
        │       ├── exploration/explore_notes.md
        │       ├── plan/plan-raw.yaml
        │       ├── gates/gate_{D,I,K,W}.md
        │       ├── output/final_output.md
        │       └── DIKW_STATE.json
        └── tmp/                               ← temp execution logs
```

Numbering rules:
  - Task folders are `NN-{task_name}` where NN is `01`, `02`, … in execution
    order. Gate-added tasks get the next number.
  - Task name (without NN-) stays the canonical key in `plan-raw.yaml`.


Stage 0 — Resolve & detect
---------------------------

Inspect `{folder}`:

```
if {folder}/manifest.yaml exists with subject_id + 1-SourceStore/:
    kind = "subject"
    source_roots = [{folder}/1-SourceStore/, {folder}/2-RecStore/]

elif {folder}/_agent_dikw_space/ exists:
    kind = "existing_dikw"
    source_roots = derived from existing manifest.yaml

else:
    kind = "plain"
    source_roots = [{folder}]   ← treat all files in folder as data
```

Record `kind` and `source_roots` in memory for later stages.


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

Print which one will be used.


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

  2. For each file in `source_roots` (walk recursively):
     - If `FREEZE=true`: copy the file into `{snapshot_dir}/source/` (flat)
     - Else: create a symlink `{snapshot_dir}/source/{basename}` → absolute path
       (if duplicate basename across source_roots, suffix with parent folder name)

  3. Write `{snapshot_dir}/manifest.yaml`:
     ```yaml
     created_at: "2026-04-21T14:30:00"
     created_by: "/dikw v0.1"
     folder: "{absolute path to {folder}}"
     kind: "subject"  # or "plain" / "existing_dikw"
     freeze: false
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
  ⬜ insights/data/NN-{task}/           — D-level reports + code
  ⬜ insights/information/NN-{task}/    — I-level reports + code
  ⬜ insights/knowledge/NN-{task}/      — K-level reasoning
  ⬜ insights/wisdom/NN-{task}/         — W-level reasoning

SESSION (new)
  ⬜ sessions/run1/exploration/, plan/, gates/, output/, DIKW_STATE.json

TEMP (auto-cleaned)
  ⬜ tmp/
```


Stage 4 — Gate (one confirm)
-----------------------------

Present:

```
📋 About to run DIKW on {folder}
   Kind: {kind}
   Snapshot: {snapshot_dir} ({is_new ? "new" : "reused"})
   Question: {question}

Proceed?  (yes / dry-run / revise "new question" / cancel)
```

If `DRY_RUN=true`: print the above and EXIT (do not run Stage 5).
If `AUTO_PROCEED=true`: pause 10 seconds, default to yes.
Else: wait for explicit user input.

User responses:
  - `yes` → Stage 5
  - `dry-run` → exit
  - `revise "..."` → update question, re-show, re-ask
  - `cancel` → abort (keep the scaffolded snapshot for later use)


Stage 5 — Run session
----------------------

Delegate to `/dikw-session`:

```
/dikw-session {snapshot_dir} {question}
```

`/dikw-session` already handles:
  - explore → plan → gate → D → gate → I → gate → K → gate → W → gate → report
  - writes into `{snapshot_dir}/insights/` + `{snapshot_dir}/sessions/{aim}/`
  - DIKW_STATE.json for resume-after-compaction

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
  - `source/` symlinks flatten both stores into one level:
    - `source/CGM.parquet` → `../../../1-SourceStore/CGM.parquet`
    - `source/Record-HmPtt.CGM5Min_RecAttr.parquet` → `../../../2-RecStore/Record-HmPtt.CGM5Min/RecAttr.parquet`
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
/dikw {folder} --freeze               → copy data into source/ (no symlinks)
/dikw {folder} --interactive          → pause at every DIKW gate (not just Stage 4)
```


Rules
-----

- NEVER write into `{folder}` outside of `_agent_dikw_space/`. User data is untouched.
- ALWAYS write manifest.yaml on snapshot creation — it's the provenance record.
- ALWAYS go through Stage 3 (layout preview) + Stage 4 (confirm gate) before Stage 5.
- If a snapshot exists but `source/` is empty or stale (files removed from user's
  folder), warn and suggest `--new-snapshot`.
- When creating symlinks, use paths relative to the snapshot dir so the snapshot
  is relocatable as a whole directory tree.


Estimated duration
-------------------

| Stage | Time | Interactive? |
|-------|------|--------------|
| 0-2   | 5-30s   | Auto (scaffolding) |
| 3     | 2s      | Auto (print) |
| 4     | —       | Gate (1 human confirm) |
| 5     | 30-60 min | Auto with AUTO_PROCEED=true; gates with =false |
| Total | ~30-60 min end-to-end | 1 confirm gate minimum |


Consumers
---------

The snapshot directory is self-contained and archivable:

```
tar -czf Subject-559-snapshot-2026-04-21.tgz \
    Subject-559/_agent_dikw_space/snapshot-2026-04-21/
```

Gives you a complete, reproducible analysis record: data (via manifest
hashes), insights, sessions, final report.

For per-task consumption:
  - `insights/data/NN-{task}/report.md` — read this task's D insight
  - `insights/data/NN-{task}/analysis.py` — re-run the analysis
  - `sessions/{aim}/output/final_output.md` — final synthesis for a run
