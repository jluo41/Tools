# 🔎 Review and scoring

- **Fresh reviewers only** · the must-check gate
  - Paragraph logic, then sentence logic (logic, read, ai), by a reviewer that never wrote the text; 8 passes.
- **Blind A/B keeps only "easier and the same meaning"** · `1e8be4f06`
  - Adopt refuses a pair that says `meaning: no`, and a later pair carrying its words.
- **Paragraph logic** · haipipe-draft-review `ref/paragraph-logic.md`
  - Claim and support, hidden steps, alternatives, agreement with the evidence.
  - ScalingGlucose r01: 45 of 53 paragraphs under 8.
- **The lab starts the review by default** · haipipe-paper 1.40.0
  - Each Section session's first turn runs the review, skipped when the Draft was already reviewed at its version.
