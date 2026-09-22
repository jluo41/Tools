---
name: haipipe-idea-pressure-test
description: >-
  Red-team a research Idea for falsifiability, identification, construct
  validity, data access, ethics, feasibility, and the minimum informative
  experiment. Use when deciding whether an apparently novel idea can actually
  be tested; it keeps scientific novelty separate from design credibility.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.5"
  last_updated: "2026-09-22"
  capability_family: "2_test"
---

# /haipipe-idea-pressure-test · can this Idea survive contact with evidence?

Load `haipipe-ideation` and the target Idea Card. Load `haipipe-task` and
`haipipe-run` before commissioning any new internal computation. This skill
owns the scientific red-team and minimum-experiment specification; Task owns
data inspection, code, pilots, and execution receipts.

For a durable commission, use the owner-bound Run Specs in
`../haipipe-ideation/references/workflow-runs.md`. This capability's checks
are internal Steps unless separately commissioned under that contract.

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

### Identification credibility anchors and abstention

`identification.credibility` assesses whether the specified design can identify
the named target contrast in its stated population and setting, conditional on
its assumptions. Judge it from the claim–mechanism–design–outcome chain, the
operational measures/constructs, population and timing, exposure/comparator,
estimator, data provenance, and direct diagnostics or owner-native Task Results
that test identification assumptions. Cite those evidence objects in
`identification.evidence_basis` with exact artifact locations. This label does
not mean the claim is true, novel, feasible, or publishable, and it is not the
pilot's positive/negative outcome. A pilot informs identification only when its
receipt contains diagnostics that bear on a named assumption.
These are qualitative owner-specific anchors; they do not claim empirical
calibration against independent reviewer labels or downstream causal outcomes.

| Label | Evidence anchor and example |
|---|---|
| `strong` | The target contrast and constructs are operationalized; direct design/data evidence addresses material confounding, selection, reverse-causality, and leakage threats for the stated scope, with no material threat left open. Assumptions remain explicit; this is not proof of causality. Example: the registered design, data provenance, and owner-run diagnostics jointly address its named rival explanations. Compared with `conditional`, no named identification check remains outstanding. |
| `conditional` | The design could identify the target contrast if named, assessable assumptions/checks hold. Record each condition, needed evidence, owner, and route; do not imply it is satisfied. Example: a stated parallel-trends assumption has a specified diagnostic and owner route, but its result is pending. Compared with `strong`, a verifiable condition remains open; compared with `weak`, there is a concrete test that could resolve it. |
| `weak` | Available evidence identifies a material threat or rival explanation that the current design cannot distinguish from the claimed mechanism, and no specific verifiable check or demonstrated repair currently resolves it. Example: treatment selection is directly tied to the outcome-generating process and the proposed design has no comparison or diagnostic that separates them. Compared with `conditional`, the gap is not currently bounded by an assessable condition. |
| `unknown` | Frozen inputs are insufficient, inaccessible, or materially conflicting, so credibility cannot be judged; examples include an unspecified contrast/measure, unknown data provenance, missing design evidence, or unresolved reviewer disagreement. This is abstention, not a weak-design finding. Compared with `weak`, the evidence does not establish a design failure; it is insufficient to classify. |

Use `unknown` and HOLD when the design's target contrast or constructs are not
specified enough to assess, when the evidence basis is absent or conflicting,
or when a required diagnostic has not been obtained. State the missing object
and route it to its owner; do not downgrade missing evidence to `weak` or
upgrade an untested assumption to `strong`. If reviewers remain divided after
review, preserve each raw judgment; an `undetermined` resolution remains
`unknown`/HOLD. Keep `feasibility.pilot` separate, and never translate
identification credibility into novelty confidence or another field's label.

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
assessment_binding:
  mode: owning_run | direct
  assessment_id: "unique id in the owning Task Result or direct call"
  owning_run: "bNN.jNN.tNN/rNN | null"
  evaluator: null  # direct mode: {actor: person/ID or agent/ID, model_or_build: ...}
  criterion: null  # direct mode: {id: haipipe-idea-pressure-test, version: "0.1.4", owner: haipipe-idea-pressure-test}
  input: null      # direct mode: {subject_hash: "sha256:...", manifest_sha256: "sha256:..."}
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
  target_contrast: "the estimand or comparison the design intends to identify"
  evidence_basis: ["owner-native Task Result/source ID plus exact table, section, or diagnostic"]
  conditions: []  # required when conditional: testable assumption/check, evidence, owner, route
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
  reason: "required when status is skipped"
ethics_privacy: []
residual_risks: []
next_test: "..."
created_at: "ISO-8601"
```

Each evaluator writes a new immutable raw receipt with its own
`assessment_binding`. For `owning_run`, the evaluator, rubric and input hashes
are inherited through `owning_run` + `assessment_id` from the Task Result. For
`direct`, fill the three direct-mode fields from the shared contract in
`references/receipts.md`. If multiple reviewers assess the same frozen inputs,
retain every raw file and write a same-shape resolution receipt with
`review_resolution`, including when they agree; never edit a
reviewer's original or decide by vote. An unresolved identification judgment
projects to `unknown`/HOLD; it does not rewrite an independently observed
pilot status. The Idea Card's `pressure_receipt` points to the resolution
receipt when one exists.

Update the Idea Card's `identification` and `feasibility` blocks with the
receipt path. The Card projects `pilot.status` to its scalar
`feasibility.pilot`; a positive/negative status also projects the Task-owned
path, and a waiver projects its reason. `pending` and `skipped` do not require
a Task result and never pass the completed-Test/selected-card gate.
A skipped pilot keeps pilot.reason in this pressure receipt and projects to
pending in the Test Matrix, with no invented feasibility.receipt. Do not copy raw outputs into the
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
Include the complete direct-mode `assessment_binding` inline. If more than
one reviewer is used, retain each raw judgment and return the shared
`review_resolution` block; unresolved conflict remains HOLD.
