fn-revise: Generate Revision Checklist → Hand Off to /paper-revise
====================================================================

Collect all revision commitments from the 4 rebuttal responses and the
annotated reviews, generate a structured checklist, then hand off to
the /paper-revise skill for actual LaTeX editing.

This function does NOT edit LaTeX. It produces the checklist that
/paper-revise will execute.

---

Input
======

  Prerequisites:
    - C-rebuttal-writing/ has all rebuttal responses
    - A-review-content/ has annotated reviews with paper source locations

---

Output
=======

  D-paper-revision/
  +-- revision-checklist.md     <- Structured list of all changes needed

---

Steps
======

Step 1: Collect revision commitments from rebuttals
------------------------------------------------------

  Read every rebuttal in C-rebuttal-writing/. Extract all revision
  commitments (text that says "we will...", "we add...", "we correct...",
  "in the revised paper..."):

    From {Rw1} rebuttal:
      - "Add Section X.Y with {new results}"
      - "Correct {error} in Section Z"
      - "Report both {metric A} and {metric B} in main text tables"

    From {Rw4} rebuttal:
      - "Replace {old method} with {new method}"
      - ...

Step 2: Collect paper source locations from annotations
---------------------------------------------------------

  Read every annotated review in A-review-content/. Extract all
  CC paper source references:

    `0-sections/05_baseline_results.tex:229` → rewrite event conclusion
    `0-sections/03_dataset_design.tex:23` → correct 66.2% error
    `0-sections/06_discussion.tex:39` → add data limitation

Step 3: Merge into a structured checklist
--------------------------------------------

  Group by section, with file:line references:

    ## revision-checklist.md

    ### Section N: {Section Title}
    | ID | File:Line       | What to change           | Why      | Reviewer          |
    |----|-----------------|--------------------------|----------|-------------------|
    | R1 | `{file}:{line}` | {old text} → {new text}  | {reason} | {Rw4} W1          |
    | R2 | `{file}:{line}` | Correct {error}          | {reason} | All 4             |

    ### Section M: {Section Title}
    | ID | File:Line       | What to change           | Why      | Reviewer          |
    |----|-----------------|--------------------------|----------|-------------------|
    | R3 | `{file}:{line}` | Add {method description} | {reason} | {Rw4} W2          |

    ### Section X.Y: {New Section Title} (NEW)
    | ID | Location      | What to add   | Why                | Reviewer           |
    |----|---------------|---------------|--------------------|--------------------|
    | R4 | After Sec X.Z | {new content} | {reviewer concern} | {Rw1} W7, {Rw2} W1|
    | R5 | After R4      | {new content} | {reviewer concern} | {Rw1} W10          |

    ### Discussion
    | ID | File:Line       | What to change   | Why      | Reviewer  |
    |----|-----------------|------------------|----------|-----------|
    | R6 | `{file}:{line}` | Add {limitation} | {reason} | {Rw1} W3  |

    ### Appendix
    | ID | Location           | What to add | Why      | Reviewer  |
    |----|--------------------|-------------|----------|-----------|
    | R7 | Appendix {X} (new) | {content}   | {reason} | {Rw4} W1  |
    | R8 | Appendix {Y} (new) | {content}   | {reason} | {Rw1} W6  |

Step 4: Cross-check completeness
-----------------------------------

  Verify every revision commitment in every rebuttal has a matching
  checklist item. Flag any orphaned commitments.

  Verify every [text-change] tag from Phase A annotations has a
  matching checklist item.

Step 5: Hand off to /paper-revise
------------------------------------

  Tell the user:

    "The revision checklist is at D-paper-revision/revision-checklist.md.
     To start editing the paper, use:
       /paper-revise [section-file]
     with the checklist items for that section."

  The /paper-revise skill handles the actual LaTeX editing — this
  function only produces the structured plan.
