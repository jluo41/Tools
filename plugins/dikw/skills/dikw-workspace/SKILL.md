---
name: dikw-workspace
description: "DIKW workspace manager. Preview layout, inspect status, locate files, clean temps, create skeletons under _agent_dikw_space/snapshot-<date>/. Use when the user asks about DIKW file locations, project setup, where to save, where to find reports, workspace status, or says /dikw-workspace. Trigger: workspace, files, project setup, where is, layout, preview paths, file tree, show reports, show insights, show code, create project, cleanup."
argument-hint: [command] [path]
---

Skill: dikw-workspace
=====================

Manage DIKW workspace files: preview the path layout, inspect status, locate
files, clean temps. Operates on the `_agent_dikw_space/snapshot-<date>/`
layout produced by `/dikw`.


Commands
--------

```
/dikw-workspace                             → status of cwd (default)
/dikw-workspace layout [path]               → preview path contract with ✅/⬜ markers
/dikw-workspace status [path]               → what currently exists
/dikw-workspace create [path]               → create an empty snapshot skeleton
/dikw-workspace locate [what] [path]        → find specific files
/dikw-workspace clean [path]                → remove tmp/, keep insights + sessions
```

Parse the first word of `$ARGUMENTS` as the command. Second arg is path
(default: cwd). If path is a plain folder, detect the kind; if it's already a
snapshot directory, operate on that snapshot.


Folder Layout
-------------

Every DIKW workspace follows this layout, nested under a user-owned folder:

```
{folder}/                                      USER DATA (untouched)
└── _agent_dikw_space/                         AGENT-OWNED workspace root
    └── snapshot-<date>/                       one analysis context per snapshot
        ├── manifest.yaml                      INPUT: file list + hashes + sizes
        ├── source/                            INPUT: symlinks (or copies) to data
        │   ├── CGM.parquet
        │   └── ...
        ├── insights/                          OUTPUT: DIKW reports + code
        │   ├── data/                          ├── D-level
        │   │   └── NN-{task}/
        │   │       ├── report.md              the insight
        │   │       ├── analysis.py            the code
        │   │       └── chart.png              any artifacts
        │   ├── information/                   ├── I-level
        │   │   └── NN-{task}/
        │   │       ├── report.md
        │   │       └── analysis.py
        │   ├── knowledge/                     ├── K-level (reasoning only)
        │   │   └── NN-{task}/
        │   │       └── report.md
        │   └── wisdom/                        └── W-level (reasoning only)
        │       └── NN-{task}/
        │           └── report.md
        ├── sessions/                          OUTPUT: per-question runs
        │   └── {aim}/
        │       ├── question.md
        │       ├── exploration/explore_notes.md
        │       ├── plan/plan-raw.yaml
        │       ├── gates/gate_{D,I,K,W}.md
        │       ├── output/final_output.md
        │       └── DIKW_STATE.json
        └── tmp/                               TEMP: execution logs, safe to clean
            └── {task}/{timestamp}/
                ├── prompt.txt
                ├── logs/stdout.log
                └── result.json
```

Key naming rules:
  - Task folders are `NN-{task_name}` where NN = `01`, `02`, … in execution order.
  - Task name (no NN-) is the canonical key in `plan-raw.yaml`.
  - Snapshots are named `snapshot-YYYY-MM-DD` (with `-b`, `-c` … suffix for
    same-day re-snapshots).


Path Resolution Rules
---------------------

All DIKW skills use these conventions (relative to the snapshot directory):

```
Source data:    source/{file}
Insight report: insights/{level_dir}/NN-{task}/report.md
Insight code:   insights/{level_dir}/NN-{task}/analysis.py  (D, I only)
Insight chart:  insights/{level_dir}/NN-{task}/{name}.{png,svg,...}

level_dir:      data | information | knowledge | wisdom

Explore notes:  sessions/{aim}/exploration/explore_notes.md
Plan:           sessions/{aim}/plan/plan-raw.yaml
Plan revision:  sessions/{aim}/plan/plan-raw-v{N}.yaml
Question:       sessions/{aim}/question.md
Final report:   sessions/{aim}/output/final_output.md
Gate reviews:   sessions/{aim}/gates/gate_{D,I,K,W}.md
Session state:  sessions/{aim}/DIKW_STATE.json

Temp workspace: tmp/{task}/{timestamp}/
```

Task names: lowercase_with_underscores, no NN- prefix, no session prefix.
  col_overview ✓    01-col_overview ✗    run1_col_overview ✗


Command: layout
----------------

Preview the path contract for a folder. Detect the kind, show what exists
(✅) and what would be created (⬜).

Usage:
  `/dikw-workspace layout [path]`

Behavior:

1. Resolve the path:
   - If `path` is a plain folder → target snapshot = `path/_agent_dikw_space/snapshot-<latest>/`
   - If `path` ends in `snapshot-<date>` → target = `path` itself
   - If `path/_agent_dikw_space/` doesn't exist → show what WOULD be created

2. Detect the folder kind:
   - `subject` — has `manifest.yaml` with `subject_id` + `1-SourceStore/`
   - `existing_dikw` — has `_agent_dikw_space/`
   - `plain` — otherwise

3. Print the path contract with markers:

```
DIKW Workspace Layout
═══════════════════════════════════════════════════════════════════════════
folder: /abs/path/to/folder
kind:   subject
target: /abs/path/to/folder/_agent_dikw_space/snapshot-2026-04-21/

MANIFEST
  ⬜ manifest.yaml                               will be created at snapshot time

SOURCE (read-only input)
  ⬜ source/CGM.parquet        →  ../../../1-SourceStore/CGM.parquet
  ⬜ source/Diet.parquet       →  ../../../1-SourceStore/Diet.parquet
  ⬜ source/Exercise.parquet   →  ../../../1-SourceStore/Exercise.parquet
  ⬜ source/Medication.parquet →  ../../../1-SourceStore/Medication.parquet
  ⬜ source/Ptt.parquet        →  ../../../1-SourceStore/Ptt.parquet
  ⬜ source/Record-HmPtt.CGM5Min_RecAttr.parquet  →  ../../../2-RecStore/...

INSIGHTS (DIKW outputs — one folder per task)
  ⬜ insights/data/NN-{task}/           D-level: report.md + analysis.py + charts
  ⬜ insights/information/NN-{task}/    I-level: report.md + analysis.py + charts
  ⬜ insights/knowledge/NN-{task}/      K-level: report.md (reasoning, no code)
  ⬜ insights/wisdom/NN-{task}/         W-level: report.md (reasoning, no code)

SESSIONS (per-question runs)
  ⬜ sessions/{aim}/question.md
  ⬜ sessions/{aim}/exploration/explore_notes.md
  ⬜ sessions/{aim}/plan/plan-raw.yaml
  ⬜ sessions/{aim}/gates/gate_{D,I,K,W}.md
  ⬜ sessions/{aim}/output/final_output.md
  ⬜ sessions/{aim}/DIKW_STATE.json

TEMP (safe to clean)
  ⬜ tmp/{task}/{timestamp}/
```

For an already-initialized snapshot, flip ⬜ → ✅ for files that exist, and
list counts (e.g. "3 D tasks, 2 I tasks, 1 K, 1 W, 2 sessions").


Command: status
----------------

Show what currently exists in a snapshot. Run `ls` + summarize:

Usage:
  `/dikw-workspace status [path]`

Output:

```
📊 DIKW Workspace Status
═══════════════════════════════════════════════════════════════════════════
folder: /abs/path/to/folder
snapshot: snapshot-2026-04-21/ (reused 3 times since creation)

Source (frozen at 2026-04-21T14:30:00):
  ✅ 6 files symlinked, 24MB total
     source/CGM.parquet, Diet.parquet, Exercise.parquet, ...

Insights:
  📊 D (3/3 done):
     ✅ insights/data/01-col_overview/        (report 4.2K + analysis.py + chart.png)
     ✅ insights/data/02-quality_check/       (report 3.8K + analysis.py)
     ✅ insights/data/03-time_coverage/       (report 2.1K + analysis.py)
  📈 I (2/2 done):
     ✅ insights/information/01-cgm_trend/    (report 5.1K + analysis.py + heatmap.png)
     ✅ insights/information/02-meal_glucose/ (report 4.7K + analysis.py)
  🧠 K (1/1 done):
     ✅ insights/knowledge/01-pattern_synthesis/report.md
  💡 W (0/1):
     ⬜ insights/wisdom/01-recommendations/

Sessions:
  📁 sessions/run1/
     ✅ exploration/explore_notes.md (9.4K)
     ✅ plan/plan-raw.yaml (v1)
     ⬜ output/final_output.md
     State: phase=W, 6/7 tasks done

Temp:
  📁 tmp/ (4 runs, 8MB total)
```


Command: create
----------------

Create a snapshot skeleton without invoking `/dikw` (for manual workflows).

Usage:
  `/dikw-workspace create [path]`

```python
import os, datetime

folder = "{path}"
today = datetime.date.today().isoformat()
snapshot_dir = f"{folder}/_agent_dikw_space/snapshot-{today}"

for d in [
    "source",
    "insights/data", "insights/information", "insights/knowledge", "insights/wisdom",
    "sessions",
    "tmp",
]:
    os.makedirs(f"{snapshot_dir}/{d}", exist_ok=True)
```

Print: "Created snapshot at `{snapshot_dir}`. Use `/dikw {folder}` to start a session."

This does NOT create the manifest.yaml or populate source/ — that's `/dikw`'s
job at snapshot time. Use this command only when you want an empty skeleton.


Command: locate
----------------

Find specific files in the latest snapshot.

Usage:
  `/dikw-workspace locate [what] [path]`

Examples:

```
/dikw-workspace locate insights            → list all insight reports
/dikw-workspace locate D                   → list D-level tasks
/dikw-workspace locate information        → list I-level tasks
/dikw-workspace locate K                   → list K-level tasks
/dikw-workspace locate W                   → list W-level tasks
/dikw-workspace locate code                → list all analysis.py files
/dikw-workspace locate source              → list source/ symlinks
/dikw-workspace locate plan                → find plan-raw.yaml files
/dikw-workspace locate explore             → find explore_notes.md
/dikw-workspace locate col_overview        → find a specific task's folder
/dikw-workspace locate state               → show DIKW_STATE.json files
/dikw-workspace locate gates               → list gate review files
/dikw-workspace locate snapshot            → list all snapshot-*/ dirs
/dikw-workspace locate manifest            → show manifest.yaml
```

For each found file: path, size, last modified.


Command: clean
---------------

Remove temporary files, keep production outputs.

Usage:
  `/dikw-workspace clean [path]`

```
KEEP (never delete):
  source/              — symlinks / frozen data
  insights/            — DIKW outputs
  sessions/            — session records
  manifest.yaml        — provenance

DELETE (temporary):
  tmp/                 — execution logs, working files

ASK before deleting:
  sessions/{aim}/DIKW_STATE.json — only if session is completed
```

Print what will be deleted and how much space will be freed, then ask for
confirmation.


Subject-folder detection
-------------------------

If `{folder}/manifest.yaml` exists and contains `subject_id`, the folder is a
per-subject data contract (haipipe-subject). In that case:

  - `source_roots = [{folder}/1-SourceStore/, {folder}/2-RecStore/]`
  - `source/` inside the snapshot flattens both stores:
    - `source/CGM.parquet` → `../../../1-SourceStore/CGM.parquet`
    - `source/Record-HmPtt.CGM5Min_RecAttr.parquet`
        → `../../../2-RecStore/Record-HmPtt.CGM5Min/RecAttr.parquet`
  - Duplicate basenames across the two stores get a parent-folder prefix.

Record `kind: "subject"` + the subject_id in the snapshot's `manifest.yaml`.


Future: HAI-Chat Drive Alignment
---------------------------------

Currently workspace is a local folder. Future: mount from HAI-Chat user drive at

```
/uc-data/users/{user}/agent-workspaces/dikw-executor-bot/projects/
```

making DIKW artifacts browsable in the HAI-Chat drive sidebar.


Cross-references
-----------------

- For the top-level orchestrator: `/dikw`
- For individual phase execution: `/dikw-explore`, `/dikw-plan`,
  `/dikw-data`, `/dikw-information`, `/dikw-knowledge`, `/dikw-wisdom`,
  `/dikw-report`
- For full-session execution: `/dikw-session`
- For gate reviews: `/dikw-review`
- For per-task context + readiness evaluation: `/dikw-context`


Rules
-----

- NEVER write outside `{folder}/_agent_dikw_space/`. User data is untouched.
- ALWAYS resolve to a specific `snapshot-<date>/` before reading or writing.
- Task folders are `NN-{task_name}/` — use the canonical task name from
  `plan-raw.yaml`, prefixed with the next available `NN-` for this level.
- When listing insights, sort task folders by NN- prefix (execution order).
- `create` skeleton only — let `/dikw` own manifest.yaml + source/ population.
