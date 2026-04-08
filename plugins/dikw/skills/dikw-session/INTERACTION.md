DIKW Session — Human ↔ AI Interaction Design
================================================

How Human and AI interact during a DIKW session in Claude Code.
This is the local prototype of the HAI-Chat bot system interaction.


Two Execution Environments, Same Protocol
-------------------------------------------

  HAI-Chat (Cloud Bots)                 Claude Code (Local Skills)
  ─────────────────────                 ──────────────────────────
  Human ↔ Advisor (MM channel)          Human ↔ Claude Code (terminal)
  Advisor → Router (@mention)           /dikw-session (orchestrator skill)
  Router → Executor (MM thread)         /dikw-data, /dikw-info (sub-skills)
  Executor → Claude Code (claude -p)    Claude Code runs directly
  .mm_session state                     DIKW_STATE.json
  Emoji signals                         File existence = done
  Channels + threads                    Folders + files

  Same DIKW protocol. Same file structure. Same gate logic.
  Skills are the local prototype. Bots are the cloud deployment.


The 5 Interaction Moments
---------------------------

Every DIKW session has exactly 5 types of Human ↔ AI interaction:


  Moment 1 — ASKING THE QUESTION (session start)
  ------------------------------------------------

    Human types:
      /dikw-session ./project "What drives patient engagement in SMS?"

    AI responds:
      Project: ./project
      Data found: df_etl_sample.parquet (1.7MB, 10K rows)
      Starting exploration...

    Mapping:
      Claude Code: Human types in terminal
      HAI-Chat:    Human types /dikw ask in landing channel


  Moment 2 — REVIEWING THE PLAN (after explore)
  ------------------------------------------------

    AI runs explore, presents the plan:

      DIKW Plan (version 1):
      Goal: Analyze SMS experiment for engagement drivers
      D: col_overview, dedup_analysis
      I: arm_effectiveness, engagement_funnel
      K: behavioral_drivers
      W: messaging_strategy

      Proceed? (yes / revise / skip levels)

    Human can:
      "yes"                           → proceed as planned
      "add a D task for time"         → AI adds task, re-presents
      "skip K"                        → mark K as skipped
      "change I to demographics"      → AI revises I tasks
      "make it 2 tasks max per level" → AI trims

    Mapping:
      Claude Code: Human types naturally, AI re-presents plan
      HAI-Chat:    Advisor presents in aim channel, Human discusses,
                   Advisor sends @dikw-router-bot command


  Moment 3 — GATE REVIEWS (between levels)
  ------------------------------------------

    After each level, AI reviews and presents:

      Gate Review: D-level complete
      col_overview: 96 columns profiled
      dedup_analysis: 42% dupes from retry mechanism
      Gap: time dimension not analyzed
      Recommendation: ADD_TASKS → time_dimension_profile
      Agree? (yes / skip / proceed anyway)

    Human can:
      "yes, add it"                   → AI runs new task, re-reviews
      "no, proceed to I"              → AI skips gap, moves on
      "revise the whole plan"         → AI re-plans from scratch
      "show me the D reports first"   → AI reads and summarizes
      "go back to explore"            → AI re-explores with focus

    With AUTO_PROCEED=true:
      AI decides automatically. Human can still interrupt anytime.

    Mapping:
      Claude Code: /dikw-review presents in terminal
      HAI-Chat:    Router notifies Advisor, Advisor reviews + discusses
                   with Human, Advisor sends command to Router


  Moment 4 — MID-TASK CONVERSATION (during execution)
  ----------------------------------------------------

    While AI works, Human can interrupt:

      Human: "wait, are you using deduped data?"
      AI: "I'm using raw. Should I deduplicate first?"
      Human: "yes"
      AI: "Adding D task: create_deduped_dataset. Will re-run."

    This is natural conversation. The skill system manages state,
    but Human always has control.

    Mapping:
      Claude Code: Human types in same terminal session
      HAI-Chat:    Human types in aim channel, Router relays to Advisor,
                   Advisor discusses with Human


  Moment 5 — FINAL REPORT (session end)
  ----------------------------------------

    AI presents the report:

      Final Report: sessions/run1/output/final_output.md

      Executive Summary:
      - 13 SMS arms tested, 3 outperform
      - "authority" arm: 67% click rate
      - Age is strongest engagement predictor
      - Recommended: authority for >50, timeliness for <30

      Satisfied? (yes / need more / go back)

    Human can:
      "looks good, done"              → session complete
      "need more on age segments"     → AI goes back to I-level
      "the recommendations are vague" → AI goes back to W-level

    Mapping:
      Claude Code: Human reads in terminal or opens file
      HAI-Chat:    Advisor reviews, discusses with Human,
                   signals @dikw-router-bot done


Interaction Modes
------------------

  AUTO_PROCEED=false (interactive, default for local):
    Human reviews at every gate. Natural conversation.
    Best for: learning the data, first-time analysis, important decisions.

  AUTO_PROCEED=true (autonomous, default for cloud):
    AI decides at every gate. Runs unattended.
    Human can still interrupt at any time.
    Best for: overnight runs, batch analysis, known-good datasets.

  Mixed (practical):
    AUTO_PROCEED=true but HUMAN_CHECKPOINT at plan stage.
    AI runs autonomously after Human approves the plan.
    Best for: "I'll approve the plan, then let it run."


Why Skill-First Matters for Interaction
-----------------------------------------

  When you run /dikw-session locally:
    - You SEE every step happening in real time
    - You can interrupt at ANY point (not just gates)
    - You can ask "why did you do that?" and get an answer
    - You can say "redo that differently" immediately
    - The conversation IS the interaction — no proxy layer

  When the same skills run on HAI-Chat:
    - Advisor is your proxy (it reviews for you)
    - You interact via Mattermost (async, not real-time)
    - Gates are formal checkpoints (not casual interrupts)
    - You might be absent (Advisor proxy-decides)

  The local experience teaches you how the system thinks.
  Then you trust it to run autonomously on the cloud.

  This is why we build skills first, cloud second.
