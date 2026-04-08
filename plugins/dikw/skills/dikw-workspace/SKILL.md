---
name: dikw-workspace
description: "DIKW workspace and file management skill. Create project structure, show file tree, locate reports/code/data, check what exists, clean up. Use when the user asks about DIKW file locations, project setup, where to save, where to find reports, workspace status, or says /dikw-workspace. Trigger: workspace, files, project setup, where is, file tree, show reports, show code, create project, cleanup."
argument-hint: [command] [project_dir]
---

# DIKW Workspace Manager

Manage DIKW project files: create, navigate, inspect, clean.

## Commands

```
/dikw-workspace                              → show workspace status (default)
/dikw-workspace status [project_dir]         → file tree + what exists at each level
/dikw-workspace create [project_dir]         → create a new project skeleton
/dikw-workspace locate [what] [project_dir]  → find specific files (reports, code, data, plan)
/dikw-workspace clean [project_dir]          → remove run_workspace/ artifacts, keep production files
```

## Context: $ARGUMENTS

Parse the first word as the command. If no command, default to `status`.

---

## Project Structure

Every DIKW project follows this layout:

```
{project_dir}/
│
├── source/                          INPUT (read-only during analysis)
│   └── raw/                         Raw data files (parquet, csv, etc.)
│       ├── df_etl_sample.parquet
│       └── ...
│
├── reports/                         OUTPUT: analysis reports (production)
│   ├── data/                        D-level reports
│   │   ├── col_overview.md
│   │   └── quality_check.md
│   ├── information/                 I-level reports
│   │   ├── correlation_analysis.md
│   │   └── segment_analysis.md
│   ├── knowledge/                   K-level reports
│   │   └── rule_extraction.md
│   └── wisdom/                      W-level reports
│       └── recommendations.md
│
├── code/                            OUTPUT: Python scripts (production)
│   ├── data/                        D-level code
│   │   ├── col_overview/
│   │   │   ├── analysis.py
│   │   │   └── chart.png
│   │   └── quality_check/
│   └── information/                 I-level code
│       └── correlation_analysis/
│           ├── correlations.py
│           └── heatmap.png
│
├── sessions/                        SESSION-SPECIFIC files
│   └── {aim}/                       One folder per session aim
│       ├── exploration/
│       │   └── explore_notes.md     Phase 1 output
│       ├── plan/
│       │   ├── plan-raw.yaml        Current plan
│       │   └── plan-raw-v2.yaml     Revised plans (if any)
│       ├── output/
│       │   └── final_output.md      Final report
│       ├── gates/
│       │   ├── gate_D.md            Gate review after D
│       │   ├── gate_I.md            Gate review after I
│       │   └── ...
│       └── DIKW_STATE.json          Session state (for resume)
│
├── run_workspace/                   WORKING area (temporary, auditable)
│   └── {task_name}/{timestamp}/
│       ├── prompt.txt               What Claude Code was told
│       ├── logs/
│       │   └── stdout.log           Claude Code output
│       ├── code/                    Working scripts (before copy to production)
│       └── result.json              Execution result
│
└── .mm_session                      Mattermost session state (Router only)
```

---

## Command: status

Show what exists in a project. Run `ls` and summarize:

```
📊 DIKW Workspace Status: /workspace/projects/drfirst
═══════════════════════════════════════════════════════

Source data:
  📁 source/raw/
     df_etl_sample.parquet (1.7MB, 10K rows × 96 cols)

Sessions:
  📁 sessions/run1/
     ✅ exploration/explore_notes.md (9.4K)
     ✅ plan/plan-raw.yaml (v1)
     ⬜ output/final_output.md (not yet)
     State: phase=I, 4/8 tasks done

Reports:
  📊 D (2/2 done):
     ✅ reports/data/col_overview.md (4.2K)
     ✅ reports/data/quality_check.md (3.8K)
  📈 I (1/2 done):
     ✅ reports/information/correlation_analysis.md (5.1K)
     ⬜ reports/information/segment_analysis.md
  🧠 K (0/1):
     ⬜ reports/knowledge/rule_extraction.md
  💡 W (0/1):
     ⬜ reports/wisdom/recommendations.md

Code:
  📁 code/data/col_overview/ (2 files: analysis.py, chart.png)
  📁 code/data/quality_check/ (1 file: check.py)
  📁 code/information/correlation_analysis/ (2 files)

Run workspace:
  📁 run_workspace/ (6 runs, 12MB total)
```

---

## Command: create

Create a new project skeleton:

```python
import os
project_dir = "{project_dir}"
for d in [
    "source/raw",
    "reports/data", "reports/information", "reports/knowledge", "reports/wisdom",
    "code/data", "code/information",
    "sessions",
    "run_workspace",
]:
    os.makedirs(os.path.join(project_dir, d), exist_ok=True)
```

Print: "Created project at {project_dir}. Drop data files in source/raw/."

---

## Command: locate

Find specific files. Parse what the user is looking for:

```
/dikw-workspace locate reports         → list all .md files in reports/
/dikw-workspace locate code            → list all code folders
/dikw-workspace locate data            → list files in source/raw/
/dikw-workspace locate plan            → find plan-raw.yaml
/dikw-workspace locate explore         → find explore_notes.md
/dikw-workspace locate D               → list D-level reports and code
/dikw-workspace locate col_overview    → find report + code for specific task
/dikw-workspace locate state           → show DIKW_STATE.json
/dikw-workspace locate gates           → list gate review files
```

For each found file, show: path, size, last modified.

---

## Command: clean

Remove temporary files, keep production outputs:

```
KEEP (never delete):
  source/raw/          — input data
  reports/             — production reports
  code/                — production scripts
  sessions/            — session files (explore, plan, output, gates, state)

DELETE (temporary):
  run_workspace/       — execution logs and working files
  .mm_session          — Mattermost state (only relevant for bot)

ASK before deleting:
  sessions/{aim}/DIKW_STATE.json — only if session is completed
```

Print what will be deleted, how much space freed, then ask for confirmation.

---

## Path Resolution Rules

All DIKW skills use these conventions:

```
Reports:    reports/{level_dir}/{task_name}.md
            level_dir: data | information | knowledge | wisdom

Code:       code/{level_dir}/{task_name}/
            Only for D and I levels (code-producing)

Explore:    sessions/{aim}/exploration/explore_notes.md
Plan:       sessions/{aim}/plan/plan-raw.yaml
Final:      sessions/{aim}/output/final_output.md
Gates:      sessions/{aim}/gates/gate_{level}.md
State:      sessions/{aim}/DIKW_STATE.json

Task names: lowercase_with_underscores, no session prefix
            col_overview ✓    run1_col_overview ✗
```

---

## Cross-references

- For D/I/K/W task execution: see /dikw-data, /dikw-information, etc.
- For the full pipeline: see /dikw-session
- For gate reviews: see /dikw-review
- For workspace alignment with HAI-Chat drive: see design/00-DESIGN.md

---

## Future: HAI-Chat Drive Alignment

Currently workspace is a Docker volume at /workspace/projects/.
Future: mount from HAI-Chat user drive at:

```
/uc-data/users/{user}/agent-workspaces/dikw-executor-bot/projects/
```

This makes DIKW reports browsable in the HAI-Chat drive sidebar.
See HAI-Chat/design/02-drive-and-storage/drive-structure.md for details.
