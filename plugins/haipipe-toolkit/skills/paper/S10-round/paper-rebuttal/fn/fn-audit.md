fn-audit: Audit Rebuttal Responses
====================================

Verify coverage, character limits, and consistency across all responses.

---

Input
======

  User provides: path to review directory
  Prerequisites: C-rebuttal-writing/rebuttal-{reviewer_id}.md exists for all reviewers

---

Steps
======

Step 1: Character count check
-------------------------------

  For each C-rebuttal-writing/rebuttal-{reviewer_id}.md:
    - Extract the rebuttal section (the text to paste into venue system)
    - Count characters: wc -c
    - Flag if over venue limit (check ref/formats.md)
    - Report spare chars

  Output table:
    | Reviewer | Chars | Limit | Status           |
    |----------|-------|-------|------------------|
    | {Rw1}   | 3327  | 5000  | OK (1673 spare)  |
    | {Rw2}   | 4812  | 5000  | OK (188 spare)   |
    | ...     | ...   | ...   | ...              |

Step 2: Coverage check
------------------------

  For each reviewer, extract all W/Q/L tags from A-review-content/review-{reviewer_id}.md.
  Then grep C-rebuttal-writing/rebuttal-{reviewer_id}.md for each tag.

  Flag any tag that appears 0 times in the rebuttal = MISSING.

  Output table:
    | Reviewer | Tag | In review | In rebuttal | Status  |
    |----------|-----|-----------|-------------|---------|
    | {Rw1}   | W1  | yes       | yes         | OK      |
    | {Rw1}   | W2  | yes       | yes         | OK      |
    | {Rw1}   | Q3  | yes       | no          | MISSING |

Step 3: Number consistency check
----------------------------------

  Extract all specific numbers from ALL rebuttals:
    - Metric values, gap sizes, percentages, p-values
    - Table values (subgroup A metric, subgroup B metric, etc.)

  Check: does the same metric appear with different values across responses?
  Flag inconsistencies.

  Example inconsistency:
    {Rw1} says "gap +6.28" but {Rw4} says "gap +5.76"
    -> Flag: which is correct? (Could be different analyses — verify.)

Step 4: Claim consistency check
---------------------------------

  Check that the same experiment is described consistently:
    - Same conclusion ("events don't help" vs "events can help with fusion")
    - Same framing ("the barrier is sparsity" in all responses)
    - No contradictions

  Common traps:
    - Different metric values from different model versions
    - "Only significant" in one response, "notable trend" in another
    - Different framing of the same limitation

Step 5: Anonymous URL check
------------------------------

  Verify:
    - All responses reference the anonymous supplementary URL
    - The URL is the same across all responses
    - The URL resolves (curl check)
    - No non-anonymized URLs (GitHub usernames, institution URLs)

Step 6: Tone check
---------------------

  Scan for red flags (see ref/principles.md Principle 10):
    - "We disagree" → replace with "We clarify"
    - "The reviewer misunderstood" → replace with "Your feedback led us to..."
    - Excessive praise (more than 1-2 sentences)
    - Defensive language
    - Missing gratitude (no thanks at all)

Step 7: Generate report
--------------------------

  Produce a summary report:
    - Character counts (all within limit?)
    - Coverage (all tags addressed?)
    - Number consistency (any conflicts?)
    - Claim consistency (any contradictions?)
    - Anonymous URL (working?)
    - Tone (any red flags?)
    - Action items (what to fix)

---

Output
=======

  Print the audit report to the user.
  List specific action items for each issue found.
