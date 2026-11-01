s03 · Agent role in subjective labeling
======================================

**Tags:** `concept` · `labeling`

**Stage:** explore

**For:** a deck, and what the agent does and what the person judges in subjective labeling, for the people who write the toolkit skills

**Delivery type:** skill

**Topic:** Judgment-centered annotation: one system helps users articulate and apply a standard, whether they begin with a rough idea and unlabeled corpus or existing labeled data. Human high-level judgments guide many items; the agent organizes cases, rules, conflicts, execution and audit. Proposed design; benefits remain to be tested.

**Feeds:** `reports/` q02_building_scanning_gates · q03_schema_and_handoff

Files
-----

- [Reviewed implementation plan](implementation-plan/PLAN.md): six core documents, 21 dependency-ordered work packages, agent assignments, contracts, evaluation design and six specialist audit/review records. The current specification uses separate Meaning and Expression agents, Workbench decision forms, asynchronous feedback and learning/validation/final-test custody. Implementation has not started in this planning turn. [Assignments](implementation-plan/WORK-PACKAGES.md) · [Review decisions](implementation-plan/REVIEW.md).
- [Interactive decision report](decision-report/build/index.html): a local six-card prototype for asynchronous preference collection, with source evidence, custom answers, defer, draft saving and feedback export. Synthetic examples; no automatic guideline update. [Source and method notes](decision-report/README.md).
- [Current presentation](delivery/deck/deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pptx): 23 slides in the established illustrated style. Version 12 returns the report to the whole Meaning Loop Agent (Annotation Alignment), which investigates, collects preferences again, reconciles decisions and updates rules and labels before rerunning Step 5. A new transition slide 12a sits before Step 6. [Full PDF](delivery/deck/deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pdf) · [Five-page discussion PDF](delivery/deck/deliverables/subjective-labeling-preference-return-v12-discussion.pdf) · [Before/after rationale](delivery/deck/source/meaning-loop-return-v12.md). These remain proposed concepts; the implementation-plan documents were reconciled to it on 2026-11-01 (version 2).
- [Deck sources](delivery/deck/README.md): v12 content, generation prompts, artwork and builder. Versions 1 to 11 are in `../_archive/20261031/slides-v1-v11/`.

- `s03-agent-role.md`: decisions, open questions and drawing words.
- `build_s03_agent_role.py`: drawing layout; reads this face.
- `s03-agent-role.excalidraw`: primary complete workflow, both entry points, meaning and expression loops, qualification, batch labeling, audit, outputs and evaluation.
- `s03-agent-role-workflow.yaml`: authored words for the complete workflow; the main builder reads it.
- `s03-agent-role.2-inspect-existing-labels.excalidraw`: use case 2, inspect existing labels.
- `s03-agent-role.3-execute-at-scale.excalidraw`: shared execution and evaluation.
- Each drawing has its own generated PNG preview; its nodes remain native Excalidraw elements.
- `s03-agent-role.png`: generated lightweight overview.
- `s03-agent-role.full.png`: generated full-resolution workflow, 6730 × 2760 pixels.
- `s03-agent-role.mindmap.md`: authored structured concept map.
- `s03-agent-role.mindmap.html`: generated standalone map.

Decided
-------

s03-D01 · The inputs are a human and a corpus; the intended outputs are an approved structured guideline and accepted labeled data, possibly a small subset of the corpus. (user 261026)

s03-D02 · Each iteration distinguishes updating the meaning of the guideline from improving how the same meaning is expressed. (user 261026)

s03-D03 · Compare multiple executor models without changing their weights; aim to improve the weakest model while preserving strong-model quality and reducing the gap. This is an objective to test. (user 261026)

s03-D04 · The two use cases are entry points into one process: rough idea without a guideline or labels, and existing labeled data with an optional old guideline. (user 261026)

s03-D05 · Make the whole process easier: the human makes high-level judgments affecting many items; the agent organizes evidence, applies decisions and checks consistency. (user 261026)

s03-D06 · Draw the two use cases separately, with a third shared execution flow; no outer frame, freer layout, emoji and independently movable nodes. (user 261026)

s03-D07 · Follow the supplied reference: pale role cards, restrained colored connectors, compact emoji, clean typography and clear local zones. Retain no whole-canvas frame and independently editable nodes. This user preference overrides the default monochrome style. (user 261027)

s03-D08 · Replace the primary summary drawing with one large, detailed architecture-style workflow, following the supplied food-event demo: numbered operations, concrete input/output records, explicit failure routes, shared records and evaluation. The main map supersedes the three-card summaries; earlier drawings remain supplemental. Its large size and pale zones are deliberate user overrides; preserve native editability and no whole-canvas outer frame. All steps remain proposed, not implementation or result claims. (user 261027)

s03-D09 · Both use-case slides use three rows: human-agent-corpus dialogue; two aligned outputs, a structured adaptive guideline and human-approved, guideline-consistent labeled data; then executor testing and large-scale labeling with audit. Existing labeled data is the left-side input in use case 2; the large unlabeled target corpus stays on the right in both. (user 261027)

s03-D10 · The presentation, source content, image generation prompts, artwork and prior versions live in this blueprint topic under `slides/`. The former Physician-SPACE output path is a compatibility symlink. (user 261027)

s03-D11 · The Subjective Labeling deck and its sources now live directly under the Tools blueprint Block at `../slides/`, rather than inside a Studio topic or the study paper folder. Earlier paths remain compatibility links. (user 261027)

s03-D12 · Redraw all five Subjective Labeling slides as version 4 in the shared IRB/team-workspace style: outline icons, muted role colors, spacious text and native editable arrows. Preserve both use cases, their paired accepted outputs and scaling row, and the evaluation plan. Keep earlier illustrated versions. (user 261027)

s03-D13 · The deck is this topic's delivery: version 12 and what it builds from live in `delivery/deck/`; versions 1 to 11 moved to `../_archive/20261031/slides-v1-v11/`. Replaces D10 and D11, which put the deck in `slides/` at the Block. (JL 261031)

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
5. Agree its **For:** line and **Delivery type:** (skill), proposed by the agent 261030?

Related: `../s42-task-building-procedure/s42-task-building-procedure.md` describes the detailed building procedure. This topic proposes the conceptual boundary; it does not modify that procedure or certify the current implementation.

Complete workflow
-----------------

The current main drawing reads `s03-agent-role-workflow.yaml`. Read steps 01–12 across the colored zones, then follow the two revision loops and the audit return. The lower band specifies the shared records and the evaluation plan. The example question packet is illustrative, not a real dataset result. Colored card borders indicate responsibility, not completed implementation.

The previous three overview drawings are preserved in history and as supplementary views where present. Their wording is retained below for reference; the current main builder does not regenerate them.

Earlier overview words
----------------------

The user requested three separate, frame-free drawings on 261026. This overrides the usual enclosing frame and density badge. Each node is a small independent group of editable shapes, text and emoji; arrows are separate native elements. The 261027 reference adds pale cards and a local collaboration zone, with no whole-canvas enclosing box. The shared narrative and structured map remain above and alongside these drawings.

```yaml
flows:
  - file: s03-agent-role
    title: '01  From a rough idea'
    subtitle: 'Use case 1 · I know roughly what I mean. Help me make it clear.'
    takeaway: One answer can guide many labels.
    zone: 'Human + agent: build the standard together'
    zone_note: 'A question about a rule can resolve many individual cases.'
    output_label: 'Accepted outputs'
    status: 'Proposed workflow · Human effort and label quality still need evaluation.'
    nodes:
      idea: {icon: '💭', title: A rough idea, body: 'No guideline yet.\nNo labeled data yet.'}
      source: {icon: '📚', title: A world of cases, body: 'Typical items, surprises\nand difficult boundaries.'}
      agent: {icon: '🤖', title: Agent brings a question, body: 'A proposed rule.\nExamples and counterexamples.'}
      human: {icon: '🧑', title: You make the judgment, body: 'Judge a group or contrast.\nClarify, revise or defer.'}
      guide: {icon: '📝', title: The standard takes shape, body: 'Definitions, rules, exceptions.\nYour decisions stay visible.'}
      result: {icon: '🏷️', title: Labels grow with it, body: 'Apply the rule to many items.\nReview samples and uncertain cases.'}
    arrows: {input: Start here, source: Explore, ask: Ask, approve: Record, apply: Apply, loop: 'New boundary?'}
    note: 'You judge what matters; the agent organizes and follows through.'
  - file: s03-agent-role.2-inspect-existing-labels
    title: '02  Make sense of existing labels'
    subtitle: 'Use case 2 · Someone labeled this dataset. How consistent is it?'
    takeaway: Inspect a rule and its conflicts together.
    zone: 'Human + agent: inspect the standard behind the labels'
    zone_note: 'Bring supporting cases, conflicts and alternative explanations together.'
    output_label: 'Audit outputs'
    status: 'Proposed workflow · Inferred rules remain provisional until accepted.'
    nodes:
      idea: {icon: '🗂️', title: An existing dataset, body: 'Items + labels.\nPerhaps an old guideline.'}
      source: {icon: '🔓', title: Anyone can inspect, body: 'No need to find\nthe original annotator.'}
      agent: {icon: '🤖', title: Agent proposes rules, body: 'What seems to explain\nthese labeling decisions?'}
      human: {icon: '🔎', title: Inspect an issue group, body: 'A rule + supporting items\n+ conflicting items.'}
      guide: {icon: '🧑', title: You inspect the evidence, body: 'An exception? Another standard?\nA wrong label? Still unresolved?'}
      result: {icon: '📋', title: An inspectable quality report, body: 'Rules, issue groups and findings.\nConfirmed changes stay traceable.'}
    arrows: {input: Inspect, source: Enter here, ask: Group, approve: Review, apply: Resolve / defer, loop: 'Revise the rule?'}
    note: 'A flagged item is a question to investigate, not a proven error.'
  - file: s03-agent-role.3-execute-at-scale
    title: '03  Let the guideline do more work'
    subtitle: 'Shared continuation · Use an accepted standard at larger scale.'
    takeaway: Keep the meaning. Make execution easier.
    zone: 'Agent + executors: improve how the rule is expressed'
    zone_note: 'One shared guideline; independent model calls; fixed model weights.'
    output_label: 'Scaled outputs'
    status: 'Proposed workflow · Human-approved meaning constrains every rewrite.'
    nodes:
      idea: {icon: '📝', title: An approved guideline, body: 'Information + rules\n+ their current expression.'}
      source: {icon: '🧭', title: Meaning belongs to people, body: 'A semantic change returns\nto human judgment.'}
      agent: {icon: '✍️', title: Agent improves the wording, body: 'Clearer steps and examples.\nSame approved meaning.'}
      human: {icon: '🤖', title: Different executor models, body: 'Same guideline, fresh contexts.\nModel weights stay fixed.'}
      guide: {icon: '🧪', title: Compare and inspect, body: 'Quality, coverage and cost.\nRaise weakest; preserve strongest.'}
      result: {icon: '🏷️', title: Scale with a qualified model, body: 'Freeze and test on held-out items.\nLabel in batches; audit and report.'}
    arrows: {input: Rewrite, source: Check meaning, ask: Try, approve: Measure, apply: Qualify, loop: Rewrite / retest}
    note: 'Lower effort and model cost are goals to test, not established results.'
```
