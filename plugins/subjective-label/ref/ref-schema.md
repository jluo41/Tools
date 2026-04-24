ref-schema: Label Schema Design Guide
======================================

How to design a good label schema for subjective annotation.

---

Schema Requirements
--------------------

  A valid label schema for subjective-label must specify:

  1. Exactly ONE primary dimension per annotation task.
     (Multi-dimension tasks: run gallery generation once per dimension.)

  2. 2-6 label values per dimension.
     Fewer than 2: not a classification task.
     More than 6: too complex for gallery-based few-shot. Split into sub-tasks.

  3. Mutually exclusive values.
     Each text should receive exactly one label.
     If overlap is possible, add a tiebreaker rule to guideline.

  4. Exhaustive values.
     Every text can receive SOME label.
     Add a "none" or "other" catch-all if needed.


Good vs. Bad Schema Design
---------------------------

  Bad: vague values
    values: [positive, negative, neutral, mixed]
    Problem: "mixed" and "neutral" will constantly be confused.
    Fix: define exactly what "mixed" requires (e.g., "contains both
    explicit praise and explicit criticism in same turn").

  Bad: too many values
    values: [authoritative, directive, advisory, responsive,
             informational, neutral, evasive, deferring, ... 10 more]
    Problem: gallery cannot cover all with 25 examples.
    Fix: collapse to 4-5 values. Add a "detail" field in gallery for subtypes.

  Good: action-grounded values
    values: [authoritative, advisory, informational, responsive, none]
    Each value corresponds to a distinct observable behavior in the text.
    A coder can point to specific words/phrases that signal each value.

  Good: ordered spectrum (when applicable)
    values: [strongly_toward_WLST, mildly_toward_WLST, neutral,
             mildly_against_WLST, strongly_against_WLST]
    Spectrum schemas are naturally ordered — useful for regression-style analysis.


Boundary Case Design
---------------------

  For each pair of adjacent/confusable values, predefine a tiebreaker:

  Boundary: authoritative vs advisory
    Both may mention patient values.
    Tiebreaker: Did the recommendation come BEFORE the value question?
      Yes -> authoritative.   No -> advisory.

  Boundary: informational vs advisory
    Both state prognosis.
    Tiebreaker: Did the clinician ask about patient values at all?
      No -> informational.   Yes -> advisory.

  Boundary: responsive vs advisory
    Both involve patient values.
    Tiebreaker: Did the clinician ask about values BEFORE stating prognosis?
      Yes -> responsive.   No -> advisory.

  Document all tiebreakers in guideline.md Section 4 (Boundary Cases).


Multi-Dimension Tasks
----------------------

  If you need multiple labels per text (e.g., nudge_type + direction + intensity):

  Option A: Separate gallery per dimension
    Run /subjective-label gallery once per dimension.
    Each gallery focuses on one annotation criterion.
    Cleanest design — recommended.

  Option B: Multi-column gallery
    Each gallery entry has multiple label fields.
    gallery.json entry:
      {"id": "001", "text": "...",
       "nudge_type": "authoritative", "direction": "toward_WLST",
       "intensity": "strong", "reasoning": "..."}
    More complex — only use if dimensions are tightly coupled.


Gallery Size Guidelines
------------------------

  Target: 15-30 examples total.

  Minimum per label value: 2 examples.
  Recommended per label value: 3-5 examples.
  Boundary cases: 4-8 total (regardless of N labels).

  Rule of thumb:
    N_values * 4 examples + 5 boundary cases = recommended gallery size.
    For 5 values: 5*4 + 5 = 25 examples.

  Larger gallery -> better accuracy, but:
    - Longer prompts -> higher cost per inference call
    - Diminishing returns after ~30 examples
    - Weak models may lose focus with very long few-shot context
