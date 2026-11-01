s03 · Agent role in subjective labeling
======================================

**Tags:** `concept` · `labeling`

**Stage:** explore

**Topic:** An agent helps a person discover, express and apply their labeling criteria through examples from a corpus (the collection of items to label). This proposed system separates changes in meaning from changes in expression, then tests whether independent executor models can apply the same guideline reliably. This is a design, not an implementation or a measured result.

**Feeds:** `reports/` q02_building_scanning_gates · q03_schema_and_handoff

Files
-----

- `s03-agent-role.md`: decisions, open questions and drawing words.
- `build_s03_agent_role.py`: drawing layout; reads this face.
- `s03-agent-role.excalidraw`: generated editable concept drawing.
- `s03-agent-role.png`: generated preview.
- `s03-agent-role.mindmap.md`: authored structured concept map.
- `s03-agent-role.mindmap.html`: generated standalone map.

Decided
-------

s03-D01 · The inputs are a human and a corpus; the intended outputs are an approved structured guideline and accepted labeled data, possibly a small subset of the corpus. (user 261026)

s03-D02 · Each iteration distinguishes updating the meaning of the guideline from improving how the same meaning is expressed. (user 261026)

s03-D03 · Compare multiple executor models without changing their weights; aim to improve the weakest model while preserving strong-model quality and reducing the gap. This is an objective to test. (user 261026)

Proposed system
---------------

The facilitator agent selects informative corpus examples, asks focused questions, records decisions, proposes guideline edits and diagnoses executor errors. It mediates both directions: the human explains intent; the corpus exposes cases the human may not have considered. The corpus supplies evidence, not an independent preference.

**Meaning loop:** inspect representative examples, boundaries and counterexamples; elicit definitions, rules, exceptions and preferences; resolve conflicts with the human; record approved semantic changes. A structured rule records its condition, action/label, exceptions, priority, examples and source decision. Information includes label definitions, task scope and contextual facts. Preferences become rules only when the human accepts their operational meaning.

**Expression loop:** hold the approved meaning fixed and rewrite wording, order, decision steps or examples. Run independent executor models in fresh contexts that receive the guideline and permitted task inputs, not the facilitator's conversation. Compare errors against human-adjudicated development examples. A change that alters meaning returns to the meaning loop. Passing a finite regression set is evidence of preservation, not a proof of equivalence.

**Conflict handling:** first check whether the agent misrecorded a judgment. Then distinguish missing context, a revised preference, unstable judgment and mixed dimensions. Show paired examples and the affected rule without accusing the human. The human can clarify, revise or defer. Preserve initial and revised judgments; unresolved is distinct from a negative/none label. A semantic revision identifies old labels requiring review.

**Harness:** the repeatable software surrounding model calls stores guideline versions, human decisions, examples, predictions, costs and evaluation splits. It enforces frozen evaluation inputs and traceability. Multiple responsibilities do not require multiple autonomous agents; one facilitator can call tools and independent executors.

**Evaluation and delivery:** freeze a candidate guideline before using held-out cases, which were excluded from development. Evaluate quality against human judgments, coverage (how much receives a usable label), abstentions and cost per accepted item. Test held-out executor models to assess transfer when feasible. Favor a quality floor for the weakest executor and a non-regression tolerance for stronger executors; reducing the performance gap alone could make every executor worse. Keep human-reviewed labels separate from model-expanded labels accepted through an explicit audit policy. Deliver the guideline, accepted subset and provenance, plus remaining unresolved cases and evidence of executor quality.

The proposed nested loops make the semantic boundary visible. Revising meaning and wording together obscures whether an apparent gain came from better execution or a changed labeling standard. Fine-tuning model weights is outside this design.

Open
----

1. Human owner: choose the task, label definitions and acceptable unresolved cases.
2. Human owner: set quality, non-regression and coverage thresholds, and an acceptance/audit policy.
3. Experiment owner: select executor models, budget, development/held-out splits and stopping rule; run no experiments until requested.
4. Experiment owner: test whether weaker models improve without semantic drift or stronger-model degradation. No performance parity is established.

Related: `../s42-task-building-procedure/s42-task-building-procedure.md` describes the detailed building procedure. This topic proposes the conceptual boundary; it does not modify that procedure or certify the current implementation.

Drawing words
-------------

```yaml
title: Agent role in subjective labeling
subtitle: Proposed system · s03 · explore
key: Help a human turn corpus examples into explicit rules that different models can reliably execute.
human:
  title: Human
  body: Intent, judgments, comments\nApproves meaning
corpus:
  title: Corpus
  body: Items to label\nTypical, boundary and conflicting cases
meaning:
  title: 1 · Clarify meaning
  body: Agent selects cases, asks, records\nHuman resolves conflicts or defers\nApprove definitions, rules, exceptions
  loop: Revise with new evidence
expression:
  title: 2 · Improve expression
  body: Agent rewrites; meaning stays fixed\nIndependent models label examples\nCompare errors with human judgments
  loop: Rewrite and retest
handoff: Approved meaning
return: Meaning changed? Return to human
outputs:
  title: Deliver
  body: Approved structured guideline\nAccepted labeled subset\nDecision and version provenance
harness:
  title: Harness · repeatable tests and records
  body: Fixed model weights · human reference judgments · frozen held-out evaluation
objective: 'Aim: raise weakest quality; preserve strongest quality; reduce cost.'
rationale: 'Choice: separate meaning and wording; joint edits can hide changed rules.'
open: 'OPEN · Human: quality and acceptance thresholds. Experiment owner: models and transfer test.'
unproven: Performance parity is unproven; agreement alone is insufficient.
```
