5 Key Concepts for Understanding Reviews
==========================================

Before writing any rebuttal, you must deeply understand the reviews.
These 5 concepts guide that understanding.

---

Concept 1: Reviewer Intent vs Reviewer Words
==============================================

What the reviewer wrote is not always what they mean.

  A reviewer with Originality=2 who writes 11 weaknesses is really saying:
  "I need to see something novel to change my score." Address 9 of the 11
  weaknesses but miss the originality concern, and they won't budge.

  A reviewer who writes "events don't help" might really mean:
  "Your analysis of events is too shallow." The fix isn't proving events
  help — it's showing you analyzed the problem rigorously.

How to identify intent:
  - Look at their sub-scores (Soundness, Originality, Significance)
  - Which weaknesses did they spend the most words on?
  - What did they put in their summary vs their weaknesses?
  - What is their confidence level? (High confidence = domain expert,
    low confidence = may have misunderstood)

---

Concept 2: Paper's Own Framing
===============================

Sometimes the reviewer's concern is valid because YOUR paper framed
something incorrectly, not because your work is flawed.

  Example: Paper says "events provide only minimal improvement,
  suggesting neural models implicitly capture event dynamics."
  Reviewer reads this and naturally pushes back: "Your event
  analysis is superficial."

  The fix: change YOUR framing, not argue with the reviewer.
  "Feature X doesn't help" → "Feature-X integration is an open
  challenge that our benchmark uniquely enables."

When annotating reviews, always ask:
  - Did we say something that caused this concern?
  - Where in OUR paper did we make this claim?
  - Is the reviewer responding to our framing or our actual results?

---

Concept 3: Cross-Review Resonance
===================================

When multiple reviewers independently raise the same concern, it's a
strong signal that must be addressed centrally.

  4/4 reviewers mention event analysis → this is THE issue
  3/4 mention no fairness mitigation → second priority
  1/4 mentions device confounding → targeted response only

Cross-review resonance tells you:
  - What the AC will focus on (shared concerns get most AC attention)
  - What your revised paper must address in the main text (not appendix)
  - Where a weak response will hurt you across multiple reviewers

When annotating, mark shared concerns explicitly:
  > {AU}: Same concern as {Rw3} L1. See annotation there.

---

Concept 4: Author's Honest Reaction
=====================================

The annotation is where domain expertise meets reviewer feedback.
Be honest, not diplomatic:

  Agree:    > {AU}: This is very true. Our current framing is wrong.
  Disagree: > {AU}: The reviewer misunderstood — we DO use patient-level
              bootstrap, it's just not clearly stated. Need to clarify.
  Unsure:   > {AU}: This is a hard question. How should we answer this?
  Defer:    > {AU}: Same as {Rw3}. Check the other comments.
  Partial:  > {AU}: Half right. We admit the limitation but the design
              choice is intentional — 8.6x oversampling for T1D.

The annotation serves two purposes:
  1. Load the context into YOUR brain (the "笨功夫" part)
  2. Give CC enough information to map to experiments/tasks

A terse "agree" or "disagree" is not enough. Explain WHY — what's
your reasoning as the domain expert?

---

Concept 5: Actionability Spectrum
==================================

Each reviewer concern falls somewhere on this spectrum:

  Need experiment    Need analysis    Need text change    Need to concede
  ─────────────────────────────────────────────────────────────────────
  "No mitigation"    "Device confound" "I/O confusion"    "No race/SES"
  → train new models → stratify data  → clarify Section 4 → admit limitation
  → P2: B5-B7, C11   → P4: C10        → P9: text revision → P9: text revision

Identifying where each concern falls EARLY saves effort:
  - Experiments: need time, GPU, planning → start first
  - Analysis: can run on existing data → do quickly
  - Text changes: just writing → do during revision
  - Concessions: just honesty → write in rebuttal directly

Don't waste time designing experiments for a concern that just needs
a clear concession. Don't try to concede away a concern that needs
experimental evidence.
