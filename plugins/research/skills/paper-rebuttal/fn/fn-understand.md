fn-understand: Read + Annotate One Reviewer
=============================================

The foundation of the entire rebuttal process. Read one reviewer's full
review, go through each paragraph, and build understanding through
annotation dialogue between the author(s) and CC.

This is deliberate, thorough work — 笨功夫. No shortcuts.

---

Input
======

  User provides: path to one reviewer's review file (or raw review text)
  User identifies: their initials (e.g., AB, CD — any 2-3 letter abbreviation)

---

Output
=======

  An annotated review file in A-review-content/:

    A-review-content/
    +-- review-{reviewer_id}.md     <- full review + all annotations

  The file preserves the COMPLETE original review text with inline
  annotations below each paragraph.

---

Steps
======

Step 1: Create the annotated review file
------------------------------------------

  Read the reviewer's full text. Create A-review-content/review-{id}.md
  with this structure:

    # Review: {reviewer_id}
    # Score: {score} | Confidence: {confidence}
    # Sub-scores: Soundness={X} | Originality={X} | Significance={X} | Presentation={X}

    ## Summary
    {reviewer's summary text}

    ## Strengths
    {reviewer's strengths text}

    ## Weaknesses

    **W1:** {first weakness text}

    **W2:** {second weakness text}
    ...

    ## Questions

    **Q1:** {first question}
    ...

    ## Limitations
    {reviewer's limitations text}

Step 2: Identify the score-driving concerns
---------------------------------------------

  Before the author starts annotating, CC should analyze:

  1. Which sub-scores are lowest? (Originality=2 means they want novelty)
  2. Which weaknesses got the most words? (length ≈ importance to reviewer)
  3. What's in the summary vs weaknesses? (summary = what they think the
     paper IS; weaknesses = what's MISSING)
  4. Confidence level: high = domain expert (precise answers needed),
     low = may have misunderstood (clarification may help)

  Present this analysis to the author BEFORE annotation:

    > CC: Score-driving analysis for {reviewer_id}:
    > - Lowest sub-score: Originality=2 → they need to see novel contributions
    > - Most words on: W7 (fairness mitigation) and W2 (event analysis)
    > - Confidence=3 → persuadable with strong evidence
    > - Summary focuses on benchmark design → they value this but want more

Step 3: Annotate paragraph by paragraph
-----------------------------------------

  Go through EACH section of the review. For each paragraph/weakness/question:

  1. CC reads the paragraph and identifies:
     - What the reviewer is saying (surface level)
     - What they might really mean (intent, per Concept 1)
     - Whether this echoes other reviewers (Concept 3: cross-review resonance)
     - Whether this is caused by the paper's own framing (Concept 2)

  2. CC prompts the author:
     "What's your reaction to this? Do you agree? What should we do?"

  3. Author annotates with their honest reaction:
     > {AU}: We should admit this. Our framing was wrong.

  4. CC responds with THREE things:

     a) Map to rebuttal point + task:
        > CC: Maps to P1 (event analysis). Task A2 has the temporal stats.

     b) Locate the paper source text that caused this concern.
        Search the LaTeX source files for the relevant passage.
        Provide a clickable file:line reference AND quote the text:

        > CC: Paper source:
        >   `0-sections/05_baseline_results.tex:229`
        >   > "{quoted text from your paper that triggered the concern}"
        >   → This framing caused the reviewer's concern. Needs rewrite.

        The file:line format is clickable in VS Code / Claude Code.
        Always quote the actual text so authors can see it without clicking.

        If the concern is about something MISSING from the paper (e.g.,
        "no fairness mitigation"), note where it SHOULD be added:
        > CC: Paper source: not present.
        >   Suggested location: after `0-sections/05_baseline_results.tex:275`
        >   (end of Section 5.2 Fairness Analysis)
        >   → Add new Section 5.4: Fairness-Aware Training

     c) Flag cross-review connections:
        > CC: {Rw2} Q1 raises the same concern. See review-{Rw2}.md W2.

Step 4: Tag each concern with actionability
----------------------------------------------

  After annotation, add a structured tag block for each W/Q/L:

    **W2:** Event coverage 16.8% makes conclusions fragile...
    > {AU}: Our framing is wrong. Need to reframe as open challenge.
    > CC: Maps to P1 ({topic}). Task {task_ids}.
    > CC: Paper source:
    >   `{section_file}:{line}`
    >   > "{quoted text from paper}"
    >   → Rewrite: "{new framing}"
    > CC-action: [text-change] rewrite {file}:{lines}
    > CC-action: [experiment] {task_id} {description} (done)
    > CC-action: [analysis] {task_id} {description} (done)
    > CC-cross: {Rw2} Q1, {Rw3} L1, {Rw4} W3

  Action types:
    [experiment]   — needs new model training or API calls
    [analysis]     — needs computation on existing data/predictions
    [text-change]  — needs rewriting in the LaTeX source
    [concede]      — needs honest acknowledgment in rebuttal + paper

  This feeds into Phase B (experiment planning).

Step 5: Consolidate paper source references
----------------------------------------------

  Collect ALL paper source references from Steps 3-4 into a single table
  at the bottom of the file. This gives authors a quick view of every
  paragraph in the paper that this reviewer's concerns touch.

    ## Paper Sources Touched by This Review

    | Section | File:Line                      | Concern    | What to change                    |
    |---------|--------------------------------|------------|-----------------------------------|
    | Sec 3   | `{section_file}:{line}`        | W1, Q3     | {description}                     |
    | Sec 5   | `{section_file}:{line}`        | W2, W5     | {description}                     |
    | Sec 5.4 | New section (after Sec 5.3)    | W7, W11    | {description}                     |
    | Sec 6   | `{section_file}:{line}`        | W3         | {description}                     |
    | App     | New appendix                   | W6         | {description}                     |

  Rules:
    - One row per paper location (merge concerns that touch the same line)
    - Sort by section order (Sec 1 → Sec 2 → ... → Appendix)
    - "New section" or "New appendix" for content not yet in the paper
    - This table feeds into Phase D (revision checklist)

Step 6: Summarize the reviewer's core concerns
-------------------------------------------------

  After annotating everything, CC writes a bottom-line summary:

    ## Bottom Line

    Reviewer {id} cares most about:
    1. {concern A} — this would change their score
    2. {concern B} — this supports their score
    3. {concern C} — nice to have

    Strategy hint: {flip / maintain / neutralize}

    Cross-review connections:
    - W2/W5/Q1 → shared with {Rw2}, {Rw3}, {Rw4} ({topic})
    - W7/W11/Q4 → shared with {Rw2} W1 ({topic})

---

Collaboration Notes
====================

  Multiple coauthors can annotate the same review at different times.
  When a second coauthor reads the file:
    1. They see existing annotations ({AU1}'s, CC's)
    2. They add their own below:
       > {AU2}: I disagree with {AU1} here. I think we should push back.
    3. CC can respond to the new annotation:
       > CC: Noted. {AU2}'s point changes the strategy for this concern.

  The file is a living document until Phase C (rebuttal writing).

---

Step 6: Generate A-review-content/README.md (after ALL reviewers done)
========================================================================

  This step runs ONCE, after every reviewer has been annotated.
  It synthesizes all individual reviews into a single overview.

  The README contains four sections:

  **Section 1: Reviewer Scores**

    | Reviewer | Score           | Confidence | Soundness | Originality | Significance | Presentation |
    |----------|-----------------|------------|-----------|-------------|--------------|--------------|
    | {Rw1}   | 3 (Weak Reject) | 3          | 2         | 2           | 3            | 3            |
    | {Rw2}   | 4 (Weak Accept) | 3          | 2         | 3           | 3            | 2            |
    | ...      | ...             | ...        | ...       | ...         | ...          | ...          |

  **Section 2: Master Mapping — Reviewer Concerns → Rebuttal Points**

    Group all concerns that share CC-cross tags into rebuttal points (P1, P2, ...).
    This is the CORE TABLE of the entire rebuttal process.

    | Point | Topic                      | {Rw1}          | {Rw2}       | {Rw3}  | {Rw4}  |
    |-------|----------------------------|----------------|-------------|--------|--------|
    | P1    | {most shared concern}      | W2, W5, W9, Q1 | W2, Q1, Lim | L1, Q1 | W3, Q3 |
    | P2    | {second shared concern}    | W7, W11, Q4    | W1          | —      | Orig=2 |
    | P3    | {third concern}            | W10            | W1          | —      | Orig=2 |
    | P4    | {single-reviewer concern}  | —              | —           | —      | W1, Q1 |
    | ...   | ...                        | ...            | ...         | ...    | ...    |

    Rules for grouping:
      - Concerns with the same CC-cross tags → same point
      - Points shared by more reviewers → higher priority (lower P number)
      - Single-reviewer concerns → still get a point, but lower priority
      - Implicit concerns (e.g., Originality=2) → map to the point that addresses it

  **Section 3: Concern Inventory per Reviewer**

    For each reviewer, list every W/Q/L with:
      - The concern text (1-line summary)
      - Actionability tag ([experiment/analysis/text-change/concede])
      - Cross-review connection

    | Tag | Concern                     | Actionability      | Cross-review        |
    |-----|-----------------------------|--------------------|---------------------|
    | W1  | {concern summary}           | concede            | {Rw3} L3            |
    | W2  | {concern summary}           | text-change + exp  | {Rw2} W2, {Rw4} W3  |
    | Q1  | {question summary}          | analysis           | {Rw2} Q1            |
    | ...  | ...                         | ...                | ...                 |

  **Section 4: Cross-Review Resonance**

    | Concern                    | Reviewers        | Signal strength | Priority |
    |----------------------------|------------------|-----------------|----------|
    | {most shared}              | ALL 4            | strongest       | P1       |
    | {second shared}            | {Rw1, Rw2, Rw4} | strong          | P2       |
    | {third shared}             | {Rw1, Rw3}      | moderate        | P4       |
    | {single-reviewer concern}  | {Rw4} only       | single reviewer | P5       |

---

Quality Check
==============

  Before moving to Phase B, verify:
    [ ] Every W, Q, L has at least one author annotation
    [ ] Every concern has a CC response with mapping
    [ ] Every concern is tagged [experiment/analysis/text-change/concede]
    [ ] Cross-review connections are flagged
    [ ] Bottom-line summary exists for each reviewer
    [ ] README.md exists with master mapping + concern inventory
    [ ] The author can articulate: "What would change this reviewer's score?"
