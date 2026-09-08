---
name: haipipe-idea-pressure-test
description: >-
  Red-team a research Idea for falsifiability, identification, construct
  validity, data access, ethics, feasibility, and the minimum informative
  experiment. Use when deciding whether an apparently novel idea can actually
  be tested; it keeps scientific novelty separate from design credibility.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.1"
  last_updated: "2026-09-08"
  capability_family: "2_test"
---

# /haipipe-idea-pressure-test · can this Idea survive contact with evidence?

Load `haipipe-ideation` and the target Idea Card. Load `haipipe-task` and
`haipipe-run` before commissioning any new internal computation. This skill
owns the scientific red-team and minimum-experiment specification; Task owns
data inspection, code, pilots, and execution receipts.

## Pressure surface

Test each axis independently:

| Axis | Required question |
|---|---|
| falsifiability | What observation would contradict the central claim? |
| mechanism | What alternative mechanism produces the same result? |
| construct validity | Do measures represent the claimed concepts? |
| identification | What confounding, selection, reverse causality, or leakage remains? |
| data | Are population, variables, timing, linkage, and access real rather than assumed? |
| feasibility | Can the minimum experiment run with available compute, people, time, and permissions? |
| ethics/privacy | Does execution require consent, PHI handling, sensitive inference, or restricted transfer? |
| robustness | What negative control, placebo, sensitivity, or replication would change belief? |
| failure value | Would a null or contradictory result still teach something? |

Do not use novelty as a proxy for any of these axes.

## Procedure

1. Rewrite the Idea as a claim–mechanism–design–outcome chain.
2. Name the strongest fatal assumption and the strongest repairable weakness.
3. Specify the minimum informative experiment: exact input population,
   treatment/exposure, comparator, outcome, estimator or decision rule,
   expected artifact, and pass/fail interpretation.
4. Inventory existing Task Results before proposing new work. An existing
   analysis counts as a pilot only when its receipt answers this exact bounded
   question and identifies the output and provenance.
5. If new computation is required, commission one owner-native Task Run with a
   target, Ticket, Result, and acceptance gate. Do not create an ideation Run.
6. Read the returned evidence as `positive`, `negative`, `pending`, `skipped`,
   or `waived`. `skipped` preserves history but does not pass the gate; a
   waiver must explain why no pilot is informative or permitted.
7. Record fatal blockers, repair paths, residual risks, and the next cheapest
   discriminating test. A negative pilot may justify redesign or abandonment;
   it is not a failed pressure-test process.

## Output receipt

Write `workflow/pressure/<idea>_<timestamp>.yaml`:

```yaml
version: 1
kind: idea-pressure-test
idea_id: i01
chain:
  claim: "central falsifiable claim"
  mechanism: "proposed mechanism"
  design: "identification/design strategy"
  outcome: "primary outcome"
falsifiable: true
fatal_assumptions: []
repairable_weaknesses: []
identification:
  credibility: strong | conditional | weak | unknown
  confounds: []
  repair_path: "..."
minimum_experiment:
  question: "..."
  population: "exact eligible units and time window"
  exposure: "treatment, exposure, intervention, or predictor"
  comparator: "counterfactual/control/reference condition"
  outcome: "primary observable outcome"
  estimator_or_rule: "estimator, model comparison, or decision rule"
  expected_artifact: "owner-native table, model, diagnostic, or report"
  task_result: "path or null"
  acceptance_rule: "..."
  failure_interpretation: "..."
pilot:
  status: positive | negative | pending | skipped | waived
  task_result: "Task-owned result/runtime path or null"
  waiver: "reasoned waiver text or null"
ethics_privacy: []
residual_risks: []
next_test: "..."
created_at: "ISO-8601"
```

Update the Idea Card's `identification` and `feasibility` blocks with the
receipt path. The Card projects `pilot.status` to its scalar
`feasibility.pilot`; a positive/negative status also projects the Task-owned
path, and a waiver projects its reason. `pending` and `skipped` do not require
a Task result and never pass the Test gate. Do not copy raw outputs into the
card.

## Exit gate

Pressure testing is ready when the central claim is falsifiable, the minimum
experiment and failure reading are explicit, identification credibility is
honestly classified, data/ethics constraints are known, and the pilot has a
Task-owned positive/negative receipt or a reasoned waiver. A fatal unresolved
assumption yields HOLD or abandon, not a confident recommendation.

## One-off mode

Return the pressure table, minimum experiment, fatal assumption, repair path,
and evidence needed next. Do not execute new analysis unless the user's task
authorizes it.
