Meaning Loop return and renewed preference collection
====================================================

Version 12 revises version 11 in the existing illustrated style. The Meaning Loop Agent is the agent called Alignment Agent in v11; annotation alignment remains the purpose of its loop.

Before and after
----------------

Before, the overview return arrow landed on Workbench review, and the diagnostic cards suggested a direct handoff to human review. This made the receiving agent's investigation and renewed preference collection unclear.

After, the Execution & Audit Agent produces a round report. Unresolved rule, preference or reference-label questions reopen the whole Meaning Loop Agent. The report enters the agent boundary, not the human-review node. Step 2 investigates and prepares a decision report, Step 3 collects preferences again, and Step 4 reconciles decisions and updates compatible versions. The resulting guideline and reference labels return to Step 5 for another execution. A distinct route advances to Step 6 when release criteria are met.

Round report contract
---------------------

Every execution round records the rule, expression, reference-label, item-set and executor versions; labeling performance by model and partition; changes attempted; unresolved cases and uncertainty; evidence supporting alternative explanations; candidate actions and affected scope; and the next action or stop reason. Flags are hypotheses. Executor consensus alone cannot establish that a reference label is wrong.

Expression-only problems can continue in Step 5 using Train evidence while preserving approved rules. Questions about meaning or accepted labels return to the Meaning Loop Agent. Resource limits, missing context and model limits may require deferral or executor changes rather than preference revision. A report may find that no change is warranted.

Renewed preference collection
----------------------------

The agent searches related cases and earlier decisions before preparing questions. Decision cards show the current rule, conflicting evidence, contrasting cases, alternatives and consequences. They ask about newly exposed boundaries and exceptions, not just whether a model prediction should replace a label. The human can confirm, clarify, revise, defer or supply another answer. Earlier decisions stay visible. Submitted answers are reconciled with prior preferences; apparent contradictions trigger clarification of scope or context. Unanswered cards remain open, and independent investigation may continue asynchronously.

Approval and versioning
----------------------

Human input determines new preferences and rule changes. The agent records their reason and scope, identifies affected items, and applies changes within the authorized approval policy. Approval of a rule is distinct from approval of every propagated label. Preserve original annotations, earlier decisions and prior run results. Updated rules and reference labels are evaluated again before release. Deferrals remain explicit in the delivery package.

Performance reporting
---------------------

Separate expression-only gains under unchanged reference labels from reference-label corrections and semantic changes. Rewriting is training-free: model weights stay fixed. Train supplies direct expression-refinement evidence. Both Train and staging Test can supply audit issues to the Meaning Loop. Once Test findings inform updates, later staging scores do not estimate independent end-to-end generalization; fresh independent cases are required for that claim.

Presentation changes
--------------------

Revised stable slide IDs: 6 (overview), 10 (renewed preference collection), 12 (Step 5 report routing), 21 (Train/Test return destination). Added stable slide ID 12a between original slides 12 and 13, explaining the handoff between Steps 5 and 6. Existing slide IDs are intentionally retained so earlier discussions remain traceable. The deck contains 23 physical pages. The five-page discussion excerpt follows IDs 6, 10, 12, 12a and 21. Speaker notes clarify affected neighboring steps. All unchanged illustrations remain exact copies of v11.

These illustrations and forms are proposed workflow concepts, not implemented features or measured model results.
