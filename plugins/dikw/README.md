DIKW Analysis Agent Plugin
===========================

Skills for the DIKW (Data → Information → Knowledge → Wisdom) analysis pipeline.

Point `/dikw` at any folder (a dataset, a Subject-*/ patient slice, or an
existing DIKW workspace). It creates a dated snapshot under
`_agent_dikw_space/snapshot-<date>/` and runs the full pipeline — phases
`plan → D → I → K → W → report → done` with a gate after each phase.


Runtime model (5 concepts)
---------------------------

| Term | Values |
|------|--------|
| **Stage** | `S0`..`S5` — `/dikw` outer workspace setup (one-time) |
| **Phase** | `plan` / `D` / `I` / `K` / `W` / `report` / `done` — session state |
| **Step** | `task` / `gate` — every phase runs these two, in order |
| **Task** | a specific item run during `step=task` (one for `plan`/`report`; 2–3 for D/I/K/W) |
| **Gate** | a checkpoint run during `step=gate`; identifier `G-<phase>`; outcome is one of `approve` / `revise <phase> [feedback]` / `done` |

The gate outcome is the ONLY routing vocabulary. Three values, no others.


3-Tier Skill Design
-------------------

Most of the time you only need two commands: `/dikw` and `/dikw-workspace`.
Everything else is reachable but rarely typed by hand.

**Tier 1 — User-facing (type these)**

| Skill | What it does |
|---|---|
| /dikw | One-shot entry: detect folder, create snapshot, preview layout, confirm, run session |
| /dikw-workspace | Inspect layout / status, locate files, clean temps |

**Tier 2 — Task-execution skills (run during `step=task` of their phase)**

| Skill | Phase | What it does | Produces code? |
|---|---|---|---|
| /dikw-explore | (snapshot-level, pre-session) | Profile raw data, assess quality | no |
| /dikw-plan | `plan` | Design (or revise) the analysis plan | no |
| /dikw-data | `D` | Analyze raw data (WHAT is in the data?) | yes |
| /dikw-information | `I` | Extract patterns (WHAT PATTERNS exist?) | yes |
| /dikw-knowledge | `K` | Synthesize insights (WHY do patterns exist?) | no |
| /dikw-wisdom | `W` | Strategic recommendations (WHAT SHOULD WE DO?) | no |
| /dikw-report | `report` | Final report synthesizing all findings | no |

**Tier 3 — Internal (called by the orchestrator)**

| Skill | What it does |
|---|---|
| /dikw-session | Full lifecycle: phases `plan → D → I → K → W → report → done` with gates |
| /dikw-gate | Runs during `step=gate`: proposes gate outcome (approve / revise / done) |
| /dikw-context | Builds per-task context inside `step=task`; evaluates readiness (READY / BLOCKED / SKIP) |


Folder Layout
-------------

Every `/dikw` run creates artifacts under a user-owned folder:

```
<AnyFolder>/
├── ...user's data (untouched)...
│
└── _agent_dikw_space/                          agent-owned, do not hand-edit
    └── snapshot-<date>/                        one per data state
        ├── manifest.yaml                       file list + hashes + sizes
        ├── exploration/                        SNAPSHOT-LEVEL (shared across sessions)
        │   └── explore_notes.md                produced by /dikw Stage 4.5
        ├── source/                             copies of data (or --symlink)
        ├── insights/                           DIKW outputs, one folder per task
        │   ├── data/                           D-level
        │   │   └── D01-col_overview/
        │   │       ├── report.md
        │   │       ├── analysis.py
        │   │       └── chart.png
        │   ├── information/                    I-level
        │   │   └── I01-correlation_analysis/
        │   │       ├── report.md
        │   │       └── analysis.py
        │   ├── knowledge/                      K-level (reasoning only)
        │   │   └── K01-rule_extraction/report.md
        │   └── wisdom/                         W-level (reasoning only)
        │       └── W01-recommendations/report.md
        ├── sessions/                           per-question runs
        │   └── run1/
        │       ├── question.md
        │       ├── plan/
        │       │   ├── plan-raw.yaml           symlink → latest version
        │       │   ├── plan-raw-v1.yaml        initial
        │       │   └── plan-raw-v2.yaml        after a `revise plan` gate
        │       ├── gates/
        │       │   ├── G-plan-v1.md            gate after plan v1
        │       │   ├── G-D.md
        │       │   └── G-I.md
        │       ├── output/final_output.md
        │       └── DIKW_STATE.json
        └── tmp/                                temp logs, safe to clean
```

Key rules:
  - Task folders are named `{L}{NN}-{task_name}/` where `L` is the phase
    letter (D/I/K/W) and `NN` = `01`, `02`, … in execution order within
    that phase. Gate-added tasks get the next `NN`.
  - Exploration is **snapshot-level**, not session-level — shared across
    all sessions on the same snapshot.
  - Plans are **versioned**. Each `revise plan` gate outcome bumps the
    version and writes `plan-raw-v{N}.yaml`.


Usage
-----

**Common case — full session on any folder:**
```
/dikw /path/to/folder "What patterns exist in this dataset?"
```

**Subject-*/ patient folder (auto-detected):**
```
/dikw _WorkSpace/A-User-Store/UserGroup-OhioT1DM/Subject-559 \
      "CGM patterns, meal/exercise/insulin interactions, red flags"
```

**Preview only — no execution:**
```
/dikw /path/to/folder --dry-run
```

**Force a fresh snapshot (don't reuse latest):**
```
/dikw /path/to/folder --new-snapshot
```

**Run unattended (auto-accept gate outcomes):**
```
/dikw /path/to/folder "question" --auto
```
Default is `AUTO_PROCEED=false`: session pauses at every gate for human
acceptance. With `--auto`, the gate's proposed outcome is auto-accepted.

**Inspect a workspace:**
```
/dikw-workspace layout /path/to/folder
/dikw-workspace status /path/to/folder
```

**Re-run one phase task:**
```
/dikw-data col_overview /path/to/folder/_agent_dikw_space/snapshot-2026-04-21
```

**Force re-exploration of a snapshot:**
```
/dikw /path/to/folder --re-explore
```


DIKW Boundaries
---------------

```
Phase   Question                  Method        Reads              Produces
─────   ────────                  ──────        ─────              ────────
D       WHAT is in the data?      CODE          source/            facts + code + charts
I       WHAT PATTERNS exist?      CODE          source/ + D        patterns + code + charts
K       WHY do patterns exist?    REASONING     D + I reports      explanations (md only)
W       WHAT SHOULD WE DO?        REASONING     D + I + K reports  recommendations (md only)
```


Gate outcomes — the only routing vocabulary
--------------------------------------------

At every `step=gate`, the gate outcome is exactly one of:

```
approve                     → current phase output is good; next forward phase
revise <phase> [feedback]   → re-enter <phase>
                                <phase>=current → redo current phase (add tasks)
                                <phase>=earlier → go back to that phase
                                <phase>=plan    → rewrite the plan (bumps plan_version)
done                        → findings sufficient; jump to report
```

`/dikw-session` handles all of this automatically. Back-edges (e.g., G-K
routing back to `plan` or `D`) are just `revise <phase>` outcomes.


Snapshot semantics
-------------------

  - First run on a folder creates `snapshot-YYYY-MM-DD/` and runs
    `/dikw-explore` once at Stage 4.5 (snapshot-level `exploration/`).
  - Re-runs REUSE the latest snapshot by default (insights accumulate).
  - `--new-snapshot` forces a new snapshot folder. Same-day duplicates get
    a letter suffix (`snapshot-2026-04-21-b/`).
  - `--re-explore` re-runs `/dikw-explore` on an existing snapshot when
    data has materially changed.
  - Snapshots are self-contained and archivable:
    `tar -czf Subject-559-snapshot-2026-04-21.tgz Subject-559/_agent_dikw_space/snapshot-2026-04-21/`


Principle
---------

**Skill-first development:** Always make skills work locally in Claude Code
first (`/dikw-data col_overview`), then deploy to cloud agents.
The skill prompt is the source of truth.
