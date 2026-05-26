How Questions Drive the Pipeline
==================================

Human asks ONE general question. The pipeline figures out everything else.


The Seed
---------

  The question is the seed. Everything grows from it.

  Question
    | shapes
  Explore (what data do we have to answer this?)
    | shapes
  Plan (what specific tasks will answer this?)
    | shapes
  D tasks (what facts do we need?)
    | shapes
  I tasks (what patterns to look for?)
    | shapes
  K tasks (what to explain?)
    | shapes
  W tasks (what to recommend?)
    | answers
  Report (here's the answer to your question)

  Human only provides the question.
  Every other decision flows from it automatically.


How It Works
-------------

  Human asks:
    "How should we design SMS messages to improve engagement
     for patients with low engagement?"

  /dikw-explore discovers:
    10K rows, 13 message arms, 42% duplicates, 3,608 patients
    Click rates vary 38-67%. Some patients never click.

  /dikw-plan reads the question + explore findings and THINKS:
    "To answer 'how to design messages for low engagement patients'
     I need to:
     1. First understand who the low-engagement patients ARE (D)
     2. Then find what patterns differentiate them (I)
     3. Then understand WHY they don't engage (K)
     4. Then recommend message design changes (W)"

  /dikw-plan writes:
    goal: Design SMS strategies for low-engagement patients
    D:
      - name: engagement_profiling
        description: Define engagement levels, profile low-engagement group
      - name: data_quality
        description: Handle duplicates and nulls before analysis
    I:
      - name: low_engagement_predictors
        description: What predicts low engagement? (demographics, timing, arm)
      - name: arm_response_by_segment
        description: Which arms work for low vs high engagement patients?
    K:
      - name: disengagement_drivers
        description: Why don't low-engagement patients respond?
    W:
      - name: message_redesign
        description: Specific message design recommendations for low-engagement

  The plan is SHAPED BY the question.
  Different question → different plan → different tasks.


Question Types
---------------

  Different questions produce different plans from the SAME data:

  BROAD: "What patterns exist in this data?"
    D: col_overview, quality_check
    I: statistical_summary, correlation_analysis
    K: rule_extraction
    W: strategic_recommendations
    → Full survey. Classic DIKW.

  FOCUSED: "Which SMS arm has the highest engagement?"
    D: engagement_baseline (per arm)
    I: arm_effectiveness (chi-square, effect sizes)
    K: arm_performance_drivers
    W: arm_selection_strategy
    → Narrow. Fewer tasks. Targeted.

  HYPOTHESIS: "Authority messaging works better for older patients"
    D: age_arm_crosstab (profile age × arm interaction)
    I: age_arm_interaction_test (test the hypothesis statistically)
    K: age_authority_mechanism (if confirmed, explain why)
    W: age_targeted_messaging (practical rollout plan)
    → Designed to test one specific claim.

  COMPARATIVE: "How does this quarter compare to last?"
    D: current_profile, historical_profile
    I: quarter_comparison, trend_detection
    K: change_drivers
    W: adjustment_recommendations
    → Two data sources. Comparison focus.

  FOLLOW-UP: "Last session found 3 segments. Dig into the low group."
    D: low_segment_detailed_profile
    I: low_segment_behavior_patterns
    K: low_segment_barriers
    W: low_segment_interventions
    → Builds on prior session. May skip explore.


How the Question Shapes Each Level
------------------------------------

  Question: "How to improve engagement for low-engagement patients?"

  D answers: WHO are the low-engagement patients?
    engagement_profiling →
      "42% of patients (1,515) never clicked any message.
       They are younger (median 34 vs 52), more urban,
       prescribed maintenance medications."

  I answers: WHAT predicts their low engagement?
    low_engagement_predictors →
      "Age <40 is the strongest predictor (OR=3.2, p<0.001).
       No message arm significantly improves their click rate.
       Morning messages slightly better than afternoon (p=0.08)."

  K answers: WHY don't they engage?
    disengagement_drivers →
      "Young patients likely manage health via apps, not SMS.
       Current arms use medical authority framing — resonates
       with older patients but not younger digital natives."

  W answers: WHAT SHOULD WE DO?
    message_redesign →
      "1. Create a new arm: app-redirect (link to patient portal)
       2. Test casual/peer framing instead of authority for <40
       3. Send at 8am not 2pm for working-age patients
       4. Reduce message frequency for non-responders (weekly → monthly)"


The Plan Is Not Fixed
----------------------

  The initial plan comes from the question + explore notes.
  But gate outcomes can FEED BACK into the plan during execution.
  IMPORTANT: gates do NOT directly modify task lists. Every
  non-forward gate outcome is `revise [feedback]`, which routes
  back to plan. The PLANNER (in plan-v{N+1}) is the only thing
  that adds, removes, or re-specs tasks — informed by the feedback.

  D discovers something unexpected:
    "Low-engagement patients aren't just non-clickers —
     they're actively opting out. 12% opted out."
    → G-D outcome: `revise "12% opt-out rate found in D; the
       opt-out cohort needs its own characterization before we
       can correlate engagement with anything else."`
    → routes to plan; plan-v2 adds an I-task: optout_analysis

  I finds the hypothesis is wrong:
    "Age doesn't predict engagement after controlling for
     message frequency. Frequency is the real driver."
    → G-I outcome: `revise "Age signal disappears after
       controlling for message frequency. Frequency is the
       real driver and K should explain its mechanism, not age."`
    → routes to plan; plan-v3 re-specs the K-task from
       age_mechanism to frequency_mechanism

  K reveals the question itself should change:
    "The problem isn't message design — it's message volume.
     Low-engagement patients receive 3x more messages."
    → G-K outcome: `revise "Low-engagement patients receive 3x
       more messages — the actionable lever is volume, not
       design. W should optimize volume, not redesign content."`
    → routes to plan; plan-v4 swaps the W-task from
       message_redesign to volume_optimization

  The question stays the same. The plan evolves through plan-v{N}
  files; gates only emit outcomes (approve / revise / done) and
  let the planner do the work. This is the DIKW pipeline working
  correctly — learning and adapting through a single router.
