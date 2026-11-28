---
mindmap: 1
title: Judgment-centered annotation
written: 2026-10-26
---

# One process, two entry points <!-- root -->

Help people articulate a standard and apply it consistently at scale. Proposed design, not demonstrated performance.

- Why the process is hard <!-- n01 -->
  - Turn a rough conception into explicit definitions, rules and exceptions <!-- n02 -->
  - Apply the guideline consistently across diverse items <!-- n03 -->
- Two entry points <!-- n04 -->
  - Rough idea and corpus; no guideline or labels <!-- n05 -->
  - Existing labels, with or without an old guideline <!-- n06 -->
    The inspector may differ from the original annotator. Candidate rules remain provisional without confirmation.
- Agent prepares consequential judgments <!-- n07 -->
  - Select informative cases and propose rules <!-- n08 -->
  - Assemble supporting cases, contrasts and counterexamples <!-- n09 -->
  - Retrieve previous decisions and identify conflicts <!-- n10 -->
- Human judges the standard <!-- n11 -->
  - Approve or revise rules and exceptions <!-- n12 -->
  - Judge groups and contrasts <!-- n13 -->
  - Resolve conflicts, preserve differences or defer <!-- n14 -->
  - One decision may affect many labels <!-- n15 -->
- One evolving state <!-- n16 -->
  - Guideline: information and rules, rendered through expression <!-- n17 -->
  - Labels, evidence, decision history and unresolved issues <!-- n18 -->
  - Meaning revisions return to human judgment <!-- n19 -->
  - Wording revisions keep approved meaning fixed <!-- n20 -->
- Execute and audit at scale <!-- n21 -->
  - Test the same guideline across independent models with fixed weights <!-- n22 -->
  - Improve weakest quality while preserving stronger-model quality <!-- n23 -->
  - New cases and conflicts reopen the discussion <!-- n24 -->
- Inspectable outputs <!-- n25 -->
  - Guideline and labels with approval status and provenance <!-- n26 -->
  - Rule-linked issue groups with evidence and alternative explanations <!-- n27 -->
    A group holds a rule, supporting items, conflicting items and a resolution status. No common feature does not mean careless labeling.
  - Quality report and unresolved cases <!-- n28 -->
    Report internal consistency separately from fitness for the intended use.
- Open evaluation questions <!-- n29 -->
  - Human owner: acceptance criteria and intended standard <!-- n30 -->
  - Experiment owner: less effort at comparable quality? <!-- n31 -->
  - Experiment owner: useful audit groups and reliable low-cost execution? <!-- n32 -->
    Freeze the guideline before held-out evaluation; report coverage and cost with quality. Performance parity is unproven.

## Notes

Hidden-label access can test query efficiency, but it does not reproduce a human's high-level judgment or experience. Existing datasets support audits without requiring the original annotator to return. Unresolved findings are not confirmed errors.
