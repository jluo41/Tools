DIKW Input/Output — How Data Flows Through Skills
====================================================

How each skill reads from prior skills and writes for subsequent skills.
This is the data lifecycle of a DIKW session.


The Big Picture
----------------

  INPUT                    PROCESSING                     OUTPUT
  (what goes in)           (what happens)                 (what comes out)

  source/raw/*.parquet  ──→ /dikw-explore ──────────────→ explore_notes.md
                        │
  explore_notes.md  ────→ /dikw-plan ──────────────────→ plan-raw.yaml
                        │
  source/raw/*  ────────→ /dikw-data ──────────────────→ reports/data/*.md
                        │                                 code/data/*/
                        │
  source/raw/* ─────────→ /dikw-information ───────────→ reports/information/*.md
  + reports/data/*      │                                 code/information/*/
                        │
  reports/data/*  ──────→ /dikw-knowledge ─────────────→ reports/knowledge/*.md
  + reports/information/*│
                        │
  reports/data/*  ──────→ /dikw-wisdom ────────────────→ reports/wisdom/*.md
  + reports/information/*│
  + reports/knowledge/* │
                        │
  ALL reports  ─────────→ /dikw-report ────────────────→ final_output.md
  + explore_notes.md


The Context Chain
------------------

  Each skill reads specific inputs. This is NOT optional — the chain is strict.

  ┌─────────────┐
  │  Raw Data   │  source/raw/*.parquet, *.csv
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐
  │  Explore    │  → explore_notes.md
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐
  │  Plan       │  → plan-raw.yaml
  └──────┬──────┘
         │ defines tasks for
         ↓
  ┌─────────────┐     reads: raw data ONLY
  │  D tasks    │  → reports/data/*.md + code/data/*/
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐     reads: raw data + D reports
  │  I tasks    │  → reports/information/*.md + code/information/*/
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐     reads: D + I reports (NOT raw data)
  │  K tasks    │  → reports/knowledge/*.md
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐     reads: D + I + K reports (NOT raw data)
  │  W tasks    │  → reports/wisdom/*.md
  └──────┬──────┘
         │ read by
         ↓
  ┌─────────────┐     reads: ALL reports + explore_notes
  │  Report     │  → final_output.md
  └─────────────┘


Per-Skill I/O Specification
-----------------------------

  /dikw-explore
  READS:  source/raw/*                       (all data files)
          reports/                            (check for prior work)
  WRITES: sessions/{aim}/exploration/explore_notes.md

  /dikw-plan
  READS:  sessions/{aim}/exploration/explore_notes.md
  WRITES: sessions/{aim}/plan/plan-raw.yaml
          sessions/{aim}/plan/plan-raw-v{N}.yaml  (if revised)

  /dikw-data {task_name}
  READS:  source/raw/*                       (raw data files)
  WRITES: reports/data/{task_name}.md         (analysis report)
          code/data/{task_name}/*.py          (Python scripts)
          code/data/{task_name}/*.png         (charts)

  /dikw-information {task_name}
  READS:  source/raw/*                       (raw data files)
          reports/data/*.md                   (D reports for context)
  WRITES: reports/information/{task_name}.md
          code/information/{task_name}/*.py
          code/information/{task_name}/*.png

  /dikw-knowledge {task_name}
  READS:  reports/data/*.md                  (ALL D reports)
          reports/information/*.md            (ALL I reports)
  WRITES: reports/knowledge/{task_name}.md

  /dikw-wisdom {task_name}
  READS:  reports/data/*.md                  (ALL D reports)
          reports/information/*.md            (ALL I reports)
          reports/knowledge/*.md              (ALL K reports)
  WRITES: reports/wisdom/{task_name}.md

  /dikw-report
  READS:  sessions/{aim}/exploration/explore_notes.md
          reports/data/*.md                  (ALL D)
          reports/information/*.md            (ALL I)
          reports/knowledge/*.md              (ALL K)
          reports/wisdom/*.md                 (ALL W)
  WRITES: sessions/{aim}/output/final_output.md

  /dikw-gate
  READS:  sessions/{aim}/plan/plan-raw.yaml
          reports/ (all levels)
          sessions/{aim}/DIKW_STATE.json
  WRITES: sessions/{aim}/gates/gate_{level}.md
          sessions/{aim}/DIKW_STATE.json (updated)


Key I/O Rules
--------------

  1. D and I READ raw data. K and W DO NOT.
     K and W only read reports — they never touch source/raw/.
     This enforces the DIKW boundary: K/W reason, they don't analyze.

  2. Each level reads ALL reports from prior levels.
     I reads ALL D reports (not just "relevant" ones).
     K reads ALL D + ALL I reports.
     This ensures nothing is missed in synthesis.

  3. Reports are the INTERFACE between levels.
     D produces reports → I reads those reports.
     The report IS the output. No hidden state.
     If it's not in the report, the next level doesn't know about it.

  4. Code is a SIDE EFFECT, not the interface.
     D writes code to code/data/{task}/ — but I doesn't read D's code.
     I reads D's REPORT. The code is for audit/reproducibility.

  5. Task names are GLOBAL, not session-scoped.
     reports/data/col_overview.md is the same file across all sessions.
     If session 1 wrote it and session 2 needs it, it's already there.
     This enables incremental analysis (don't redo work).

  6. Session files ARE session-scoped.
     sessions/run1/exploration/ is separate from sessions/run2/.
     Each session has its own explore, plan, gates, state, output.


Workspace Evolution During a Session
--------------------------------------

  After /dikw-explore:

    project/
    ├── source/raw/df_etl_sample.parquet
    └── sessions/run1/
        └── exploration/explore_notes.md          ← NEW

  After /dikw-plan:

    project/
    ├── source/raw/df_etl_sample.parquet
    └── sessions/run1/
        ├── exploration/explore_notes.md
        ├── plan/plan-raw.yaml                    ← NEW
        └── DIKW_STATE.json                       ← NEW

  After D tasks:

    project/
    ├── source/raw/df_etl_sample.parquet
    ├── reports/data/                             ← NEW
    │   ├── col_overview.md
    │   └── quality_check.md
    ├── code/data/                                ← NEW
    │   ├── col_overview/analysis.py
    │   └── quality_check/check.py
    └── sessions/run1/
        ├── exploration/explore_notes.md
        ├── plan/plan-raw.yaml
        ├── gates/gate_D.md                       ← NEW
        └── DIKW_STATE.json

  After I tasks:

    project/
    ├── source/raw/df_etl_sample.parquet
    ├── reports/
    │   ├── data/col_overview.md, quality_check.md
    │   └── information/                          ← NEW
    │       ├── correlation_analysis.md
    │       └── segment_analysis.md
    ├── code/
    │   ├── data/col_overview/, quality_check/
    │   └── information/                          ← NEW
    │       └── correlation_analysis/
    └── sessions/run1/
        ├── gates/gate_D.md, gate_I.md            ← NEW
        └── DIKW_STATE.json

  After K + W + report:

    project/
    ├── source/raw/df_etl_sample.parquet
    ├── reports/
    │   ├── data/...
    │   ├── information/...
    │   ├── knowledge/rule_extraction.md          ← NEW
    │   └── wisdom/recommendations.md             ← NEW
    ├── code/
    │   ├── data/...
    │   └── information/...
    └── sessions/run1/
        ├── exploration/explore_notes.md
        ├── plan/plan-raw.yaml
        ├── output/final_output.md                ← NEW
        ├── gates/gate_D.md, gate_I.md, gate_K.md, gate_W.md
        └── DIKW_STATE.json (status: completed)


What Happens During Iteration (go back / add tasks)
----------------------------------------------------

  Scenario: After I, gate says "go back to D, add time_profile"

  BEFORE go-back:
    reports/data/col_overview.md       (exists, valid)
    reports/data/quality_check.md      (exists, valid)

  AFTER go-back:
    reports/data/col_overview.md       (unchanged — not re-run)
    reports/data/quality_check.md      (unchanged)
    reports/data/time_profile.md       ← NEW (from added D task)
    code/data/time_profile/            ← NEW

  Then I tasks re-run (they now read 3 D reports instead of 2):
    reports/information/correlation_analysis.md    (re-generated, may differ)
    reports/information/segment_analysis.md        (re-generated)


  Scenario: Plan revision after D

  BEFORE revision:
    sessions/run1/plan/plan-raw.yaml     (version 1)

  AFTER revision:
    sessions/run1/plan/plan-raw.yaml     (version 2, overwritten)
    sessions/run1/plan/plan-raw-v1.yaml  (backup of version 1)
    DIKW_STATE.json: plan_version=2

  Valid D reports from v1 are KEPT. Only new/changed tasks run.


File Naming Convention
-----------------------

  Reports:  reports/{level}/{task_name}.md
            level: data | information | knowledge | wisdom
            task_name: lowercase_with_underscores

  Code:     code/{level}/{task_name}/{script_name}.py
            Only for D and I (code-producing levels)

  Charts:   code/{level}/{task_name}/{chart_name}.png
            Referenced in reports via relative path

  Session:  sessions/{aim}/exploration/explore_notes.md
            sessions/{aim}/plan/plan-raw.yaml
            sessions/{aim}/output/final_output.md
            sessions/{aim}/gates/gate_{level}.md
            sessions/{aim}/DIKW_STATE.json

  No session prefix in task names:
    col_overview ✓
    run1_col_overview ✗

  Reports are project-wide, reusable across sessions.
  Session files are session-specific.
