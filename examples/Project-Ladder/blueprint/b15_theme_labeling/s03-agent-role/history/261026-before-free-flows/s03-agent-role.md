s03 · Agent role in subjective labeling
======================================

**Tags:** `concept` · `labeling`

**Stage:** explore

**Topic:** Judgment-centered annotation: one system helps users articulate and apply a standard, whether they begin with a rough idea and unlabeled corpus or existing labeled data. Human high-level judgments guide many items; the agent organizes cases, rules, conflicts, execution and audit. Proposed design; benefits remain to be tested.

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

s03-D04 · The two use cases are entry points into one process: rough idea without a guideline or labels, and existing labeled data with an optional old guideline. (user 261026)

s03-D05 · Make the whole process easier: the human makes high-level judgments affecting many items; the agent organizes evidence, applies decisions and checks consistency. (user 261026)

The unified process
-------------------

**Purpose.** Make the whole annotation process easier, from a vague conception to an inspectable labeled corpus. Two burdens motivate the system: articulating a standard through diverse cases, and applying that standard consistently to many items. Reducing effort while preserving quality is a hypothesis, not an achieved result. The proposed shift is to make a consequential judgment, rather than an individual label, the main unit of human work.

**Two entries, not two separate systems.** At the beginning, a person brings a rough idea and an unlabeled corpus, with no guideline. At the other entry, someone brings previously labeled data, with or without an old guideline, to understand, inspect or improve its quality. This inspector need not be the original annotator. Existing labels are evidence of earlier decisions; a majority does not establish their correctness. Without an authorized human decision, inferred rules and alleged conflicts remain provisional.

**The central collaboration.** The agent selects informative cases, proposes candidate rules, retrieves earlier decisions, and organizes supporting cases and counterexamples into questions. The human approves or revises rules, judges groups and contrasts, settles conflicts, or defers. One answer may affect many items. The agent explains what changed and which labels require review. It does not merely ask the human to label every item in sequence. Small item-level checks remain useful for testing whether stated rules match concrete judgments.

**Rule-linked issue groups.** Each group contains a candidate rule, supporting items, conflicting items, contextual differences, alternative explanations and a resolution status. A conflict can expose a missing condition, multiple annotator standards, a recording error, a questionable label, or missing information. Failure to find a shared feature is not evidence of careless labeling. Internal consistency and fitness for the inspector's intended use are separate questions. Confirmed corrections, proposed corrections and unresolved cases stay distinct.

**One evolving state.** The system maintains the current information and rules, their expression as a guideline, the corpus and labels, a decision history, and unresolved issues. It is not a one-way pipeline that finishes the guideline before labels exist. Cases refine rules; applying rules produces labels; audits expose cases that reopen the discussion. In a dataset-only audit, the output can be useful issue groups and provisional rules even before anyone approves a final standard.

**The two revision loops remain.** The meaning loop changes information and rules through explicit human judgment. The expression loop holds that approved meaning fixed and tests alternative wording across executor models with fixed weights. The initial objective is one shared guideline that different models can execute; separate model-specific guidelines would be a distinct experiment. Execution errors are diagnosed: unclear wording stays in the expression loop, unresolved meaning returns to human judgment. The agent never rewrites the standard merely to improve agreement with existing labels.

**Delivery at scale.** Produce an inspectable guideline, an accepted labeled subset or a larger batch accepted under a stated audit policy, a quality report, and rule-linked issue groups. Preserve versions, evidence, decisions and unresolved cases. Distinguish labels directly checked by a human from model-produced labels. New evidence can reopen the collaboration. A repeatable harness records these steps; it does not require multiple autonomous agents.

**What experiments must establish.** Compare human effort and experience at comparable quality; test whether the guideline reflects intended judgments; evaluate the usefulness of issue groups through independent review; and measure quality, coverage and cost across executors on held-out cases. Public labels are noisy references, planted label changes test recovery of those changes, and neither substitutes for real human evaluation. Retest agreement is a reference rather than a hard performance ceiling. Freeze development decisions before independent evaluation. No experiments were run for this concept drawing.


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
title: Judgment-centered annotation
subtitle: Proposed paradigm · two entry points, one evolving process · s03
key: One human judgment guides many items. The agent turns that judgment into rules, labels and checks.
problem: 'Two burdens: articulate a standard; apply it consistently at scale.'
start:
  title: Start with an idea
  lines: [Rough concept + corpus, No guideline or labels]
existing:
  title: Start with labels
  lines: [Labeled corpus, Optional existing guideline]
agent:
  title: Agent organizes judgment
  lines: [Select informative cases, Propose rules + supporting cases, Group conflicts + counterexamples, Recall earlier decisions]
human:
  title: Human judges the standard
  lines: [Approve rules or exceptions, Judge groups and contrasts, Resolve conflicts or defer]
guideline:
  title: Evolving guideline
  lines: ['Meaning: information + rules', 'Expression: wording + steps', Approved / provisional status]
execute:
  title: Execute at scale
  lines: [Same guideline; different models, Rewrite expression; keep meaning, Fixed weights; check quality + cost, Raise weakest; preserve strongest]
delivery:
  title: Inspectable outputs
  lines: [Guideline + accepted labels, Rule-linked issue groups + quality report, Preserve unresolved cases and decision history]
ask: Focused questions
decision: High-level decisions
meaning: Revise meaning
wording: Wording feedback
audit: Label + audit
foot: 'Test: less human effort; faithful standards; useful issue groups; affordable execution.'
open: 'OPEN · Human sets acceptance criteria. Experiment owner tests effort, quality and transfer.'
change: Two entries; human decisions now central
```
