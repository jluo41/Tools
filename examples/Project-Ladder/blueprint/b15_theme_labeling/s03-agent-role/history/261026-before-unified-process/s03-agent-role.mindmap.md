---
mindmap: 1
title: Agent role in subjective labeling
written: 2026-10-26
---

# Agent mediates human and corpus <!-- root -->

Proposed system, explore stage. The human owns meaning; experiments must establish execution quality.

- Inputs and outputs <!-- n01 -->
  - Human: intent, judgments, comments and preferences <!-- n02 -->
  - Corpus: the collection of items to label <!-- n03 -->
  - Approved structured guideline <!-- n04 -->
  - Accepted labeled subset with provenance <!-- n05 -->
    Separate human-reviewed labels from model-expanded labels accepted under an audit policy.
- Facilitator agent <!-- n06 -->
  - Explore typical cases, boundaries and counterexamples <!-- n07 -->
  - Ask targeted questions and record the human's decisions <!-- n08 -->
  - Diagnose whether errors concern meaning or execution <!-- n09 -->
- Meaning loop: what should the labels mean? <!-- n10 -->
  - Formalize information, definitions, preferences and rules <!-- n11 -->
    A rule records conditions, label/action, exceptions, priority, examples and source decision.
  - Human approves semantic changes <!-- n12 -->
  - Handle contradictions without forcing agreement <!-- n13 -->
    Check transcription, missing context, preference changes, unstable judgment and mixed dimensions.
    - Clarify, revise or defer; unresolved is not a negative label <!-- n14 -->
    - Preserve initial judgments and review affected prior labels <!-- n15 -->
- Expression loop: how can models execute the same meaning? <!-- n16 -->
  - Freeze approved meaning; rewrite wording, order and decision steps <!-- n17 -->
  - Test independent executors in fresh contexts <!-- n18 -->
    Give the same permitted inputs and guideline; do not depend on hidden facilitator conversation.
  - Compare against human-adjudicated development examples <!-- n19 -->
  - Return semantic changes to the human <!-- n20 -->
    Finite regression checks cannot prove full semantic equivalence.
- Harness: repeatable tests and records <!-- n21 -->
  - Store guideline versions, judgments, predictions and cost <!-- n22 -->
  - Keep model weights fixed <!-- n23 -->
  - Freeze guideline before held-out evaluation <!-- n24 -->
    Held-out cases were not used for development. Hold out executor models too when testing transfer.
- Quality objectives, not established results <!-- n25 -->
  - Improve weakest quality while preserving strongest quality <!-- n26 -->
  - Reduce cost per accepted item; report coverage and abstentions <!-- n27 -->
  - Small agreement gaps alone do not establish correctness <!-- n28 -->
- Open decisions and owners <!-- n29 -->
  - Human: task scope, quality thresholds and acceptance policy <!-- n30 -->
  - Experiment owner: executor set, budget, splits and stopping rule <!-- n31 -->
  - Experiment owner: test transfer and semantic preservation <!-- n32 -->

## Notes

One facilitator can call tools and independent executors. These responsibilities do not require a multi-agent deployment. Fine-tuning model weights is outside this proposal.

Related detail: [s42 building procedure](../s42-task-building-procedure/s42-task-building-procedure.md). This concept does not certify that procedure's implementation.
