fn-rebuttal: Plan Strategy + Write One Rebuttal Response
=========================================================

Plan the per-reviewer strategy (first time only), then write the actual
rebuttal response for one reviewer. Strategy planning happens ONCE before
the first reviewer; subsequent reviewers reuse the same plan.

---

Input
======

  Prerequisites:
    - A-review-content/review-{id}.md has annotations
    - B-rebuttal-task/README.md has task status
  User provides: reviewer ID
  User provides (first time only): venue format (ICML, NeurIPS, etc.)

---

Output
=======

  C-rebuttal-writing/
  +-- README.md                    <- Strategy: reviewer goals, char budgets, table allocation
  +-- rebuttal-{reviewer_id}.md   <- Ready to paste into venue system

---

Part 1: Strategy Planning (first reviewer only)
==================================================

If C-rebuttal-writing/0-rebuttal-strategy.md does not exist, create it now.
If it already exists, skip to Part 2.

Step 1: Read venue format
---------------------------

  Read ref/formats.md to determine:
    - Per-reviewer or shared + per-reviewer?
    - Character/word limit per response
    - Discussion rounds
    - Anonymity requirements

Step 2: Classify each reviewer
--------------------------------

  | Reviewer | Score | Confidence | Goal       | Effort |
  |----------|-------|------------|------------|--------|
  | {Rw1}   | 3     | 3          | Flip to 4+ | HIGH   |
  | {Rw2}   | 4     | 3          | Maintain   | LOW    |
  | {Rw3}   | 3     | 3          | Flip to 4+ | MEDIUM |
  | {Rw4}   | 3     | 4          | Neutralize | MEDIUM |

  Rules:
    - Weak reject + confidence <= 3 → flip target (primary effort)
    - Weak accept → maintain (brief, grateful)
    - Any score + confidence >= 4 → neutralize (precise, don't overreach)

Step 3: Plan table allocation across responses
-------------------------------------------------

  Since per-reviewer venues have NO shared response, tables that serve
  multiple reviewers must appear in the reviewer who needs them most.
  Other reviewers get a text summary with supplementary reference.

  | Table         | Primary location | Others              |
  |---------------|------------------|---------------------|
  | {key table A} | {Rw1} (W7)       | {Rw2}: text summary |
  | {key table B} | {Rw4} (W1)       | —                   |
  | {key table C} | {Rw4} (W2)       | —                   |
  | {key table D} | {Rw3} (L1)       | {Rw1}: text mention |

Step 4: Plan character budget per reviewer
--------------------------------------------

  For each reviewer, list the points they raised and allocate chars:

  | Point           | Their concern           | Format          | ~Chars    | Priority |
  |-----------------|-------------------------|-----------------|-----------|----------|
  | W1/Q1           | {score-driving concern} | TABLE (5 rows)  | ~700      | must     |
  | W2/Q2           | {second concern}        | TABLE (3 rows)  | ~500      | must     |
  | W3              | {third concern}         | TEXT (3 sent)   | ~300      | must     |
  | W4/Q3           | {fourth concern}        | TEXT (4 sent)   | ~400      | should   |
  | W5-W7           | Minor points            | TEXT (compress)  | ~400      | should   |
  | Intro + closing |                         | TEXT            | ~300      | must     |
  | **Total**       |                         |                 | **~2600** |          |
  | **Spare**       |                         |                 | **~2400** |          |

  Budget tips:
    - A markdown table row ≈ 80-100 chars
    - A paragraph (3-4 sentences) ≈ 300-500 chars
    - Opening + closing ≈ 200-400 chars
    - Anonymous supplementary URL ≈ 80 chars
    - Leave 200+ chars spare for polish

Step 5: Write C-rebuttal-writing/0-rebuttal-strategy.md
--------------------------------------------

  Combine Steps 2-4 into the README:
    1. Reviewer classification table
    2. Table allocation plan
    3. Per-reviewer char budget summaries
    4. Anonymous supplementary URL (if created)

---

Part 2: Write One Reviewer's Response
========================================

Step 6: Load context
----------------------

  Read in order:
    1. ref/principles.md (writing principles)
    2. C-rebuttal-writing/0-rebuttal-strategy.md (strategy + char budget)
    3. A-review-content/review-{id}.md (annotated review)
    4. B-rebuttal-task/README.md (task status)

Step 7: Order the points
---------------------------

  From the strategy, determine point order for THIS reviewer:
    1. The concern that most influenced their score (lead with this)
    2. Other major concerns with experimental evidence
    3. Minor concerns (1-sentence answers)
    4. Implicit concerns (originality, contribution level)

  Order by the REVIEWER's priorities, not yours.

Step 8: Draft each point using quote-then-respond
-----------------------------------------------------

  For each point, follow this structure (see Principle 10):

    **{Tags}: {Short title}.**
    > "{Reviewer's key sentence — the core of their concern.}"

    {1-2 sentences: acknowledge + WHY you investigated.}

    {Evidence: table or key numbers.}

    {1-2 sentences: what this means + revision commitment.}

  Example:

    **W1/Q1: Device confounding.**
    > "Observed subgroup disparities may be partially driven by CGM
    > device differences if device usage correlates with demographics."

    Your concern led us to stratify by three device types using real
    device records. The T1D-T2D gap persists within every device type:

    | Device    | N   | T1D   | T2D   | Gap   |
    |-----------|-----|-------|-------|-------|
    | Dexcom G6 | 136 | 28.07 | 22.57 | +5.50 |
    | Dexcom G7 | 123 | 29.63 | 23.37 | +6.26 |

    The gap reflects T1D glycemic volatility, not device artifacts.
    We add this as Appendix X in the revised paper.

  Key rules:
    - Quote the reviewer's CORE sentence, not the whole paragraph
    - Use the reviewer's own terminology in your response
    - Every W/Q/L tag must be ctrl+F searchable
    - One block per concern (group only if tightly related)
    - Tables are evidence WITHIN narrative, not standalone dumps
    - Every table has text before (WHY) and after (WHAT IT MEANS)

Step 9: Write opening and closing
------------------------------------

  Opening (1-2 sentences):
    - Thank the reviewer (use their words from Strengths if possible)
    - Reference the anonymous supplementary URL
    - Do NOT over-praise

  Closing (1 sentence):
    - Brief gratitude: "materially improved" or "helped sharpen"
    - NOT effusive

Step 10: Include revision commitments
----------------------------------------

  Each response should list specific changes to the revised paper.
  Group them at the end or inline after each point:

    *Revision commitments:*
    (1) Add Section X.Y with {new results}.
    (2) Correct "{old claim}" to "{corrected claim}."
    (3) Report both {metric A} and {metric B} in main text tables.

  Be specific: section numbers, what changes, why.

Step 11: Address ALL points
------------------------------

  CRITICAL: Every W, Q, L the reviewer raised must appear in the response.
  Even minor points need at least 1 sentence.

  For minor points, compress into one paragraph:
    **W4:** {1-sentence answer}.
    **W5:** {1-sentence answer}.
    **W6:** {1-sentence answer}.

  The reviewer should be able to ctrl+F for every tag they wrote and find it.

Step 12: Iterative Revision with Author Comments
----------------------------------------------------

  The rebuttal file is a LIVING DOCUMENT. After CC generates the initial
  draft, coauthors add inline comments using the annotation convention:

    **W1/Q1: Device confounding.**
    > "Observed subgroup disparities may be partially driven by..."

    Your concern led us to stratify by three device types...

    > JL: 这里要不要加上 LightGBM 的结果？
    > CC: Added. LightGBM: G6 +5.33, G7 +7.34.

    | Device    | N   | T1D   | T2D   | Gap   |
    |-----------|-----|-------|-------|-------|
    | Dexcom G6 | 136 | 28.07 | 22.57 | +5.50 |

    > XZ: Table is good but too many columns. Can we drop N(T1D)/N(T2D)?
    > CC: Simplified.

  Workflow:
    1. CC generates initial draft → rebuttal-{id}.md
    2. Author reads, adds `> {INITIALS}:` comments inline
    3. CC revises the rebuttal text based on comments
       (CC's responses go as `> CC:` below the author's comment)
    4. Repeat until author approves
    5. Export clean version (Step 14)

  Rules:
    - Author comments stay in the file — they are the revision history
    - CC modifies the rebuttal text AND responds to the comment
    - Never delete author comments; they document WHY changes were made

Step 13: Self-check
----------------------

  Before presenting to the author (initial draft) or exporting (final):
    [ ] Every response block quotes the reviewer's key sentence
    [ ] First sentence after each quote directly addresses that concern
    [ ] Every W/Q/L tag appears in the response (ctrl+F check)
    [ ] Numbers match other reviewer responses (consistency)
    [ ] Tone: grateful, not defensive
    [ ] No "we disagree" or "reviewer misunderstood"
    [ ] Uses reviewer's own terminology (no rephrasing)
    [ ] Anonymous URL included
    [ ] Revision commitments listed
    [ ] Within character limit (measure clean version, not annotated)

Step 14: Export clean version
-------------------------------

  Each rebuttal-{id}.md is the ANNOTATED version (with > comments).
  To submit, export a clean version that strips all annotations:

    grep -v '^> ' rebuttal-{id}.md > rebuttal-{id}-clean.md

  Or CC can generate it: copy the rebuttal text, remove all `> {INITIALS}:`
  and `> CC:` lines, then measure character count on the clean version.

  Final output per reviewer:
    rebuttal-{id}.md         <- annotated (internal, with revision history)
    rebuttal-{id}-clean.md   <- clean (ready to paste into venue system)

  Character count is measured on the CLEAN version only.
  The annotated version can be any length.
