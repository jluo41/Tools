How Questions Drive the Pipeline
==================================

Human asks ONE question. The pipeline figures out everything else.

The plan output is **two related batches** (task_batch +
probe_batch) plus an `insight_yield` map that says which DIKW
cards each work item closes. **DIKW is a lens, not a phase order** —
sessions never run "D-tasks first, then I-tasks, then K-tasks".


The Seed
---------

The question is the seed. Everything grows from it.

```
Question
  | shapes
Explore (what KB do we already have?  what task/probe results?)
  | shapes
Plan (what tasks + probes do we need, and what DIKW yield each)
  | dispatches
Workers (task + probe, mostly in parallel within batch)
  | yields
DIKW cards (filed into insights/D_data, I_information, K_knowledge, W_wisdom)
  | answers
Report (here's the answer to your question)

Human only provides the question.
Every other decision flows from it automatically.
```


How It Works
-------------

Human asks:

```
"How should we design SMS messages to improve engagement for
 patients with low engagement?"
```

`/haipipe-insight-explore` discovers:

```
10K rows, 13 message arms, 42% duplicates, 3,608 patients.
Click rates vary 38-67%. Some patients never click.
KB has: K01 (timing-of-day effect), I02 (3-arm comparison),
        D05 (engagement distribution), no W on SMS design yet.
```

`/haipipe-application-plan` reads question + explore findings and
THINKS in terms of **yields**:

```
The question is asking about DESIGN (W-level recommendation).
That implies:
  - need a fresh K claim about what causes low engagement
    → so I need a probe comparing arms × engagement segments
  - need fresh D + I on who counts as "low engagement"
    → so I need a regression task to define the segment
  - the existing K01 (timing) is reusable as a refs in the new K
```

`/haipipe-application-plan` writes:

```yaml
plan_version: 1
question: "How should we design SMS messages to improve engagement
           for patients with low engagement?"

existing_relevant:
  knowledge:    [K01]
  information:  [I02]
  data:         [D05]
  probes:  [03_sms_arm_comparison (confirmed)]

# Batch A — task work (D + I yield)
task_batch:
  - id:    T1
    skill: /haipipe-task eval
    type:  regression
    yields: [D06, I04]
    notes: "define low-engagement segment + predictors profile"
  - id:    T2
    skill: /haipipe-task display
    type:  display
    yields: [I05]
    refs:  [D06]
    notes: "engagement × arm overlay plot for low segment"

# Batch B — probe work (K + W yield)
probe_batch:
  - id:    P.B01
    skill: /haipipe-probe design
    new:   true
    arms:  [arm_warm, arm_directive, arm_baseline]
    population: "low engagement segment from D06"
    yields: [K05, W02]
    needs:  [D06]
    rationale: "Test message tone × low-engagement interaction"

insight_yield:
  D06: {layer: D, sources: [T1]}
  I04: {layer: I, sources: [T1]}
  I05: {layer: I, sources: [T2], refs: [D06]}
  K05: {layer: K, sources: [P.B01], refs: [K01, I04, I05]}
  W02: {layer: W, sources: [P.B01], refs: [K05]}

dag:
  - T1 → D06 + I04 (define segment)
  - T2 needs D06 → I05 (visualize)
  - P.B01 needs D06 → K05 + W02 (test arms in segment)
  - All yields filed → G-report
```


Why DIKW is NOT a phase order
-------------------------------

The old model was: phase=D → phase=I → phase=K → phase=W (sequence).

The new model says:

```
A "DIKW phase" was a fiction. In reality:
  - A single regression task (one shell of code) can produce evidence
    for D, I, AND K candidates at once. The CARDS get separate ids
    only because their content has different epistemic commitment levels.
  - Multiple tasks can collectively close ONE D card (cross-task
    evidence). E.g., D06 might have sources: [T1, T3, T7].
  - K and W cannot exist without a probe. No probe, no K.
    Multiple D / I are NOT a path to K.
  - "K from many K" (strategic W) is fine and lives in W_wisdom/
    with sources: [K01, K03, K05].

Plan therefore enumerates work items (tasks + probes) and their
yields, NOT phases. Workers execute in parallel within batch (subject
to dag). Cards are filed at the end (Phase 4 in ask kind).
```


Why batches not 1:1
---------------------

```
N tasks  ↔  M D/I cards     (many-to-many)
P probes ↔ Q K/W cards (many-to-many)

  - 1 task → multiple cards: a regression task can yield D + I
    simultaneously (lens multiplicity).
  - N tasks → 1 card: a D card can cite [T1, T2, T5] as sources
    (cross-task evidence).
  - 1 probe → multiple K + multiple W (main claim + side claims
    + corresponding next-step recommendations).
  - K → W: a per-probe W cites the K it derives from.
  - K01 + K03 + K05 → strategic W: cross-probe synthesis is
    legal, just mark sources: [K01, K03, K05] and `type: strategic`.
```


Plan output goes where
-----------------------

```
applications/ask/<NN_slug>/plans/plan-v{N}.yaml      written by THIS skill
applications/ask/<NN_slug>/plans/plan.yaml           symlink → plan-v{N}.yaml (latest)

After plan approval:
  Phase 2 dispatcher reads plan and invokes /haipipe-task * + /haipipe-probe *
  Phase 3 result aggregator triggers /haipipe-probe result for confirmed claims
  Phase 4 archivist invokes /haipipe-insight-{data,information,knowledge,wisdom}
          each one files cards from materialized evidence
```


On --revise
------------

When a gate returns `revise [feedback]`:

```
/haipipe-application-plan --revise <N-1> --feedback "<text>"
  ↑ takes the prior plan + feedback verbatim
  ↑ writes plan-v{N}.yaml with revision.changes.{added,removed,modified}
  ↑ revise_history entry appended
  ↑ plan symlink updated

Plan is the SOLE router. A gate at G-claim does NOT route directly
to G-observe — it routes K→plan, and plan re-decides whether to
add an observation task, modify a probe, or rescope the
question.
```
