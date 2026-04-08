DIKW Session Walkthrough — What Happens Step by Step
======================================================

A concrete example showing EXACTLY what you type, what the AI does,
what files are created, and how the workspace evolves.

Dataset: df_etl_sample.parquet (10K rows, 96 cols, DrFirst SMS experiment)
Question: "What patterns drive patient engagement in this SMS experiment?"


=========================================================================
PHASE 0: Setup
=========================================================================

  You type:
    /dikw-workspace create ./drfirst

  What happens:
    Claude Code creates the project skeleton.

  Files BEFORE:
    (nothing)

  Files AFTER:
    drfirst/
    ├── source/raw/                    (empty, waiting for data)
    ├── reports/
    │   ├── data/
    │   ├── information/
    │   ├── knowledge/
    │   └── wisdom/
    ├── code/
    │   ├── data/
    │   └── information/
    └── sessions/

  Then you copy your data:
    cp df_etl_sample.parquet drfirst/source/raw/

  Files AFTER:
    drfirst/
    └── source/raw/
        └── df_etl_sample.parquet      ← YOUR DATA


=========================================================================
PHASE 1: Explore
=========================================================================

  You type:
    /dikw-session ./drfirst "What patterns drive patient engagement?"
    (or just: /dikw-explore ./drfirst)

  What Claude Code does:
    1. Lists files in source/raw/
    2. Reads df_etl_sample.parquet with python3 + pandas
    3. Prints: shape, columns, dtypes, nulls, distributions
    4. Checks reports/ for prior work (empty)
    5. Writes exploration notes

  You see in terminal:
    Loading df_etl_sample.parquet... 10,000 rows × 96 columns
    Key columns: patient_id, invitation_id, message, clicked, ...
    Null rate: 18.6% average across all columns
    Duplicates: 4,243 exact duplicate rows (42.4%)
    13 unique message arms (experiment variants)
    Writing explore notes...

  New files:
    drfirst/
    └── sessions/run1/
        └── exploration/
            └── explore_notes.md       ← NEW (9KB)

  explore_notes.md contains:
    Data Overview: 10K rows, 96 cols, 1 parquet file
    Column Profiles: patient_id (3,608 unique), clicked (bool, 57.8% true)...
    Quality Issues: 42.4% exact duplicate rows, 55 columns with nulls
    Observations: 13 experiment arms, timeliness arm underperforms
    Opportunities: dedup analysis, arm comparison, engagement funnel


=========================================================================
GATE 0: Review Explore
=========================================================================

  Claude Code says:
    Exploration complete.
    - 10K rows, 96 columns, single SMS experiment
    - 42% duplicates (critical — needs dedup before analysis)
    - 13 message arms, click rates vary 38-67%
    - Ready to plan?

  You can say:
    "yes, plan it"                    → goes to Phase 2
    "also check the time patterns"    → re-explores with focus
    "what's in the message column?"   → Claude Code checks and answers

  You say: "yes, plan it"


=========================================================================
PHASE 2: Plan
=========================================================================

  What Claude Code does:
    1. Reads sessions/run1/exploration/explore_notes.md
    2. Designs analysis plan based on actual findings
    3. Writes plan YAML

  New files:
    drfirst/
    └── sessions/run1/
        ├── exploration/explore_notes.md
        ├── plan/
        │   └── plan-raw.yaml          ← NEW
        └── DIKW_STATE.json            ← NEW

  plan-raw.yaml contains:
    goal: Identify which SMS message strategies drive patient engagement
    D:
      - name: dedup_analysis
        description: Profile and handle 42% duplicate rows
      - name: engagement_baseline
        description: Baseline click/auth/optout rates by arm
    I:
      - name: arm_effectiveness
        description: Statistical comparison of 13 arms (chi-square, effect size)
      - name: patient_segmentation
        description: Segment patients by engagement level, find predictors
    K:
      - name: behavioral_drivers
        description: Why some arms outperform — causal mechanisms
    W:
      - name: messaging_strategy
        description: Which arms to use, when, for whom


=========================================================================
GATE 1: Review Plan
=========================================================================

  Claude Code presents:
    DIKW Plan:
    Goal: Identify SMS engagement drivers
    D: dedup_analysis, engagement_baseline (2 tasks)
    I: arm_effectiveness, patient_segmentation (2 tasks)
    K: behavioral_drivers (1 task)
    W: messaging_strategy (1 task)
    Total: 6 tasks. Proceed?

  You can say:
    "yes"                             → starts D tasks
    "add a D task for time patterns"  → modifies plan, re-presents
    "skip K, not needed"              → marks K as skipped
    "too many I tasks, just do arm_effectiveness" → trims

  You say: "yes"


=========================================================================
PHASE 3: D-Level Tasks (sequential)
=========================================================================

  --- Task D-1: dedup_analysis ---

  What Claude Code does:
    1. Reads source/raw/df_etl_sample.parquet
    2. Writes Python script: identifies exact duplicates
    3. Produces dedup statistics
    4. Writes report

  New files:
    drfirst/
    ├── reports/data/
    │   └── dedup_analysis.md          ← NEW (4.2KB)
    └── code/data/
        └── dedup_analysis/
            ├── dedup.py               ← NEW (Python script)
            └── dedup_chart.png        ← NEW (visualization)

  dedup_analysis.md key finding:
    "4,243 of 10,000 rows are exact duplicates (42.4%).
     Caused by retry mechanism: same invitation_id appears 2-3 times.
     5,757 unique invitations. Deduped dataset recommended for analysis."


  --- Task D-2: engagement_baseline ---

  What Claude Code does:
    1. Reads source/raw/df_etl_sample.parquet
    2. Computes per-arm engagement metrics
    3. Writes report

  New files:
    drfirst/
    ├── reports/data/
    │   ├── dedup_analysis.md
    │   └── engagement_baseline.md     ← NEW (5.1KB)
    └── code/data/
        ├── dedup_analysis/
        └── engagement_baseline/
            ├── baseline.py            ← NEW
            └── arm_comparison.png     ← NEW

  engagement_baseline.md key finding:
    "13 arms, click rates range 38-67%.
     Top: authority (67%), emotionalCue (62%), socialProof (58%).
     Bottom: timeliness (38%), default (42%).
     Overall: 57.8% clicked, 23.1% authenticated, 4.2% opted out."


=========================================================================
GATE 2: Review D-Level
=========================================================================

  Claude Code (running /dikw-review logic):
    D complete. 2 reports.
    - dedup_analysis: 42% dupes from retry mechanism
    - engagement_baseline: 13 arms, 38-67% click rates

    Assessment: SUFFICIENT for I-level.
    Both reports contain specific numbers and tables.
    No critical gaps.

    Recommendation: PROCEED to I

  You say: "yes"

  Workspace now:
    drfirst/
    ├── source/raw/df_etl_sample.parquet
    ├── reports/data/
    │   ├── dedup_analysis.md                  ✅
    │   └── engagement_baseline.md             ✅
    ├── code/data/
    │   ├── dedup_analysis/dedup.py, chart.png
    │   └── engagement_baseline/baseline.py, arm_comparison.png
    └── sessions/run1/
        ├── exploration/explore_notes.md
        ├── plan/plan-raw.yaml
        ├── gates/
        │   └── gate_D.md                      ← NEW
        └── DIKW_STATE.json (phase=I)


=========================================================================
PHASE 4: I-Level Tasks
=========================================================================

  --- Task I-1: arm_effectiveness ---

  Claude Code:
    1. Reads D reports (context: 42% dupes, 13 arms)
    2. Reads raw data, runs chi-square test per arm
    3. Computes effect sizes

  New files:
    ├── reports/information/
    │   └── arm_effectiveness.md               ← NEW (6.3KB)
    └── code/information/
        └── arm_effectiveness/
            ├── chi_square.py                  ← NEW
            └── effect_sizes.png               ← NEW

  Key finding:
    "authority arm vs default: χ²=45.2, p<0.001, Cramér's V=0.19.
     3 arms statistically outperform default (p<0.01).
     timeliness arm UNDERPERFORMS default (p=0.03)."


  --- Task I-2: patient_segmentation ---

  New files:
    ├── reports/information/
    │   ├── arm_effectiveness.md
    │   └── patient_segmentation.md            ← NEW (5.8KB)
    └── code/information/
        └── patient_segmentation/
            ├── segmentation.py                ← NEW
            └── segments.png                   ← NEW

  Key finding:
    "3 patient segments by engagement level:
     High (23%): click+auth, mostly age>50, authority arm most effective.
     Medium (35%): click only, mixed ages, emotionalCue works best.
     Low (42%): no click, younger, no arm significantly helps."


=========================================================================
GATE 3: Review I-Level
=========================================================================

  Claude Code:
    I complete. 2 reports.
    - arm_effectiveness: 3 arms outperform, stats significant
    - patient_segmentation: 3 segments, age is key predictor

    Assessment: SUFFICIENT for K-level.
    Statistical evidence is strong. Segments are clear.

    Recommendation: PROCEED to K

  You say: "yes"

  Workspace now:
    drfirst/
    ├── reports/
    │   ├── data/dedup_analysis.md, engagement_baseline.md       ✅✅
    │   └── information/arm_effectiveness.md, patient_segmentation.md  ✅✅
    ├── code/
    │   ├── data/dedup_analysis/, engagement_baseline/
    │   └── information/arm_effectiveness/, patient_segmentation/
    └── sessions/run1/
        ├── gates/gate_D.md, gate_I.md                           ✅✅


=========================================================================
PHASE 5: K-Level (reasoning, no code)
=========================================================================

  --- Task K-1: behavioral_drivers ---

  Claude Code:
    1. Reads ALL D reports (2 files)
    2. Reads ALL I reports (2 files)
    3. Synthesizes: WHY do patterns exist?
    4. NO code execution — reasoning only

  New files:
    └── reports/knowledge/
        └── behavioral_drivers.md              ← NEW (4.5KB)

  No code/ folder (K-level doesn't write code).

  Key finding:
    "Authority messaging works because patients over 50 respond to
     credibility signals (doctor recommendation framing).
     Timeliness fails because urgency creates resistance in patients
     who already feel over-messaged.
     Age is the primary moderator: >50 respond to authority, <30
     respond to emotional framing, 30-50 are mixed."


=========================================================================
PHASE 6: W-Level (reasoning, no code)
=========================================================================

  --- Task W-1: messaging_strategy ---

  Claude Code:
    1. Reads ALL D + I + K reports (5 files)
    2. Produces actionable recommendations
    3. NO code execution

  New files:
    └── reports/wisdom/
        └── messaging_strategy.md              ← NEW (5.2KB)

  Key finding:
    "Recommendation 1: Use authority arm for patients >50 (expected +25% engagement).
     Recommendation 2: Use emotionalCue for patients <30 (expected +15%).
     Recommendation 3: Drop timeliness arm entirely (underperforms default).
     Recommendation 4: Deduplicate before any production deployment.
     Recommendation 5: Run A/B test on age-segmented arm assignment."


=========================================================================
PHASE 7: Final Report
=========================================================================

  Claude Code:
    1. Reads explore_notes.md + ALL D/I/K/W reports (7 files)
    2. Writes comprehensive final report

  New files:
    └── sessions/run1/
        └── output/
            └── final_output.md                ← NEW (8.5KB)


=========================================================================
FINAL WORKSPACE
=========================================================================

  drfirst/
  ├── source/
  │   └── raw/
  │       └── df_etl_sample.parquet            (input, untouched)
  │
  ├── reports/                                 (ALL analysis output)
  │   ├── data/
  │   │   ├── dedup_analysis.md                D-1: 42% dupes from retry
  │   │   └── engagement_baseline.md           D-2: 13 arms, 38-67% clicks
  │   ├── information/
  │   │   ├── arm_effectiveness.md             I-1: 3 arms outperform (p<0.01)
  │   │   └── patient_segmentation.md          I-2: 3 segments, age is key
  │   ├── knowledge/
  │   │   └── behavioral_drivers.md            K-1: authority works for >50
  │   └── wisdom/
  │       └── messaging_strategy.md            W-1: age-segmented arm strategy
  │
  ├── code/                                    (Python scripts + charts)
  │   ├── data/
  │   │   ├── dedup_analysis/dedup.py, chart.png
  │   │   └── engagement_baseline/baseline.py, arm_comparison.png
  │   └── information/
  │       ├── arm_effectiveness/chi_square.py, effect_sizes.png
  │       └── patient_segmentation/segmentation.py, segments.png
  │
  └── sessions/
      └── run1/                                (this session's files)
          ├── exploration/
          │   └── explore_notes.md             Phase 1 findings
          ├── plan/
          │   └── plan-raw.yaml                The analysis plan
          ├── gates/
          │   ├── gate_D.md                    D gate: PROCEED
          │   ├── gate_I.md                    I gate: PROCEED
          │   ├── gate_K.md                    K gate: PROCEED
          │   └── gate_W.md                    W gate: PROCEED
          ├── output/
          │   └── final_output.md              THE FINAL REPORT
          └── DIKW_STATE.json                  status: completed


  Total files produced:
    6 reports (.md)
    4 code folders (with .py + .png)
    1 explore notes
    1 plan (yaml)
    4 gate reviews
    1 final report
    1 state file
    = 18 files from 1 question + 1 parquet
