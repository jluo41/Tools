Human-AI Interaction Logic in DIKW Sessions
=============================================

How control flows between Human and AI during a DIKW analysis session.

This document describes the LOGIC of interaction — not the UI (terminal vs
Mattermost), but WHO decides WHAT and WHEN.


The Two Roles
--------------

  Human = the PRINCIPAL (委托人)
    Owns the question. Owns the data. Owns the decision.
    Delegates analysis work to AI. Reviews AI's output.
    Can intervene at any time. Can override any AI decision.

  AI = the AGENT (代理人)
    Does the analytical work. Follows the DIKW protocol.
    Reports findings. Recommends next steps.
    Never acts without authority (explicit or delegated via AUTO_PROCEED).


Three Interaction Regimes
--------------------------

  The balance of control shifts during a session:

  Regime 1: HUMAN LEADS (session design)
  ────────────────────────────────────────
    When: Start of session, plan review, major redirections
    Human: asks the question, approves the plan, sets scope
    AI: proposes, presents options, waits for decision

    Examples:
      Human: "Analyze this DrFirst dataset for engagement patterns"
      Human: "Add a task for time-of-day analysis"
      Human: "Skip K-level, go straight to recommendations"
      Human: "Go back to D, the dedup wasn't done right"

  Regime 2: AI LEADS (task execution)
  ────────────────────────────────────
    When: Running D/I/K/W tasks, exploring data, writing reports
    AI: reads data, writes code, produces reports, signals completion
    Human: monitors (or is absent), can interrupt if needed

    Examples:
      AI: runs /dikw-data col_overview → writes report
      AI: runs /dikw-review → recommends "ADD_TASKS"
      AI: runs /dikw-knowledge → synthesizes D+I findings

  Regime 3: NEGOTIATION (gate reviews)
  ─────────────────────────────────────
    When: After each level completes, at gates
    AI: presents findings + recommendation
    Human: agrees, disagrees, or redirects
    Together: decide what happens next

    Examples:
      AI: "D done. Gap: time not analyzed. Recommend ADD_TASKS."
      Human: "Agree, add the task."
      --- or ---
      Human: "No, skip it. Proceed to I."
      --- or ---
      Human: "Actually, the whole plan is wrong. Revise."


The Session Timeline (who leads when)
--------------------------------------

  Time →

  HUMAN LEADS          AI LEADS          NEGOTIATION
  ───────────          ────────          ───────────
  Ask question ──────→
                       Explore data ───→
                                         Review explore notes
  Approve/revise plan →
                       D task 1 ────────→
                       D task 2 ────────→
                                         Gate review D
                                         (proceed? add? back?)
                       I task 1 ────────→
                       I task 2 ────────→
                                         Gate review I
                       K task 1 ────────→
                                         Gate review K
                       W task 1 ────────→
                                         Gate review W
                       Final report ────→
                                         Final review
  Accept / redirect →


The Conversation Patterns
--------------------------

  Pattern 1: APPROVAL (most common, fast)

    AI:    "D done. 2 reports. Key finding: 42% duplicates."
    AI:    "Recommend: proceed to I"
    Human: "ok"
    AI:    [runs I tasks]

  Pattern 2: REDIRECT (Human overrides AI's recommendation)

    AI:    "D done. Recommend: proceed to I"
    Human: "wait, go back and add a dedup task first"
    AI:    "OK, adding D task: dedup_dataset"
    AI:    [runs dedup, re-reviews D]
    AI:    "D done (3 tasks now). Proceed to I?"
    Human: "yes"

  Pattern 3: INQUIRY (Human asks before deciding)

    AI:    "D done. Recommend: ADD_TASKS (time dimension)"
    Human: "show me the col_overview report first"
    AI:    [reads and summarizes the report]
    Human: "ok, the time column has too many nulls. skip it."
    AI:    "OK, proceeding to I without time analysis."

  Pattern 4: REVISION (fundamental plan change)

    AI:    "I done. Recommend: proceed to K"
    Human: "actually, the I results show the data is about
            something different than we planned. revise the plan."
    AI:    [re-reads all D+I reports]
    AI:    "New plan: focus on X instead of Y. D:2, I:2, K:1, W:1"
    Human: "yes, go with that"
    AI:    [re-runs from D with new tasks, skipping already-valid work]

  Pattern 5: AUTONOMOUS (AUTO_PROCEED=true)

    AI:    [explores data]
    AI:    [reviews → plans → auto-approves]
    AI:    [runs D → reviews → proceeds]
    AI:    [runs I → reviews → proceeds]
    AI:    [runs K → W → report]
    AI:    "Session complete. Final report at: ..."
    Human: [reads report when available]

  Pattern 6: ABORT (Human stops early)

    AI:    "D done. Recommend: proceed to I"
    Human: "stop here, I have enough from D"
    AI:    [writes final report from D only]
    AI:    "Partial session complete."


When AI Should Ask vs When AI Should Act
-----------------------------------------

  AI SHOULD ASK (never assume):
    - Changing the plan structure (adding/removing levels)
    - Going back to a prior level
    - Skipping planned tasks
    - Interpreting ambiguous Human instructions

  AI SHOULD ACT (don't waste Human's time):
    - Running tasks within an approved plan
    - Adding minor detail tasks (if AUTO_PROCEED=true)
    - Handling technical errors (retry, adjust approach)
    - Writing reports from completed analysis

  AI SHOULD PRESENT AND WAIT:
    - Gate reviews (show findings + recommendation, then wait)
    - Plan proposals (show plan, then wait for approval)
    - Final report (present summary, then wait for acceptance)


How This Maps to Execution Environments
-----------------------------------------

  Claude Code (local):
    Human types → Claude Code responds → same terminal
    Interruption: Human just types mid-task
    Wait: Claude Code pauses, presents, waits for input
    All 6 patterns work naturally in conversation

  HAI-Chat (cloud bots):
    Human types in aim channel → Advisor reviews → commands Router
    Interruption: Human types in aim channel, Router relays to Advisor
    Wait: Advisor posts judgment, waits for Human (or proxy-decides)
    Patterns 1-4: Advisor mediates between Human and system
    Pattern 5: Advisor auto-proceeds with proxy authority
    Pattern 6: Human sends "abort" or Advisor sends @dikw-router-bot abort

  LangGraph (executor):
    Human doesn't interact directly with executor
    Executor just runs the task — no Human gate inside execution
    Gates happen BETWEEN tasks, at the session orchestrator level


The Information Human Needs at Each Gate
-----------------------------------------

  Gate after Explore:
    - What data exists (files, rows, columns)
    - Data quality summary (nulls, dupes, types)
    - Is it what we expected?
    - What's surprising or concerning?

  Gate after Plan:
    - How many tasks per level
    - Are tasks specific to THIS data (not generic)?
    - Is the scope reasonable (not too ambitious)?
    - Are any levels unnecessary for our question?

  Gate after D:
    - What facts were discovered?
    - Any data quality blockers for I-level?
    - Any missing profiling that I-level needs?

  Gate after I:
    - What patterns were found? (with statistical significance)
    - Are patterns strong enough for K-level synthesis?
    - Any surprising findings that change the question?

  Gate after K:
    - What causal claims are validated?
    - Are claims specific enough for W-level recommendations?
    - Any knowledge gaps that need more I-level work?

  Gate after W:
    - Are recommendations actionable?
    - Are they grounded in evidence?
    - Do they answer the original question?
