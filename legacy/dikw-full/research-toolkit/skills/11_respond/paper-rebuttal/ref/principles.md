Rebuttal Writing Principles (Venue-Agnostic)
==============================================

These principles apply to all ML conference and journal rebuttals.
Venue-specific format rules are in formats.md.
Concepts for understanding reviews are in concepts.md.

---

Principle 1: Cover All Points
==============================

Every weakness (W), question (Q), limitation (L), and concern the reviewer
raised MUST be addressed in your response. Missing one signals avoidance.

  - Even a 1-sentence acknowledgment is better than silence.
  - Group related points (e.g., "W7/W11/Q4: Fairness mitigation") but make
    sure the reviewer can see their tag referenced.
  - After drafting, run a coverage check: grep for every W/Q/L tag.

---

Principle 2: Self-Contained Responses
======================================

Each per-reviewer response stands alone. You cannot say "see our response
to Reviewer X." The reviewer may not read other responses.

  - Repeat key findings when relevant to multiple reviewers.
  - The AC reads ALL responses — keep numbers and framing consistent.
  - Same experiment, same numbers, same conclusion across all responses.

---

Principle 3: Narrative, Not Table Dump
=======================================

For each concern, follow this 4-step structure inside the
quote-then-respond block (see Principle 10 for the quote format):

  1. > "{reviewer's key sentence}"  <- their concern, verbatim
  2. "This led us to investigate"   <- explain WHY you ran the experiment
  3. "We found [Z]"                 <- the result (table or number)
  4. "This means [W]"               <- what changes in the paper

Tables are EVIDENCE within the narrative, not the narrative itself.
A table without surrounding text explaining WHY and WHAT IT MEANS
reads as defensive padding.

---

Principle 4: Prioritize by Reviewer
=====================================

Lead with what matters most to THAT reviewer, not your favorite result.

  - Read their review carefully — what gave them the most pause?
  - Their score is driven by 1-2 key concerns, not all of them.
  - Address the score-driving concerns first, then quick answers for the rest.
  - If a reviewer gave Originality=2, they need to see new contributions early.
  - If a reviewer gave Soundness=2, they need methodological fixes first.

---

Principle 5: Commit to Specific Revisions
==========================================

Every response should include concrete revision commitments:

  Good: "We add Section 5.4 presenting these results in the revised paper."
  Good: "We correct Section 3: '{old claim}' -> '{corrected claim}.'"
  Bad:  "We will consider revising the paper."
  Bad:  (no mention of what changes)

Reviewers need to know what the revised paper will look like.

---

Principle 6: Concede Honestly, Fight With Data
================================================

  Legitimate limitations -> concede clearly, don't hedge
    "Missing race/SES is a data source limitation, not a design choice."

  Addressable concerns -> fight with new experiments + exact numbers
    "We implemented 7 strategies; {best method} achieves -12.4%."

  Paper errors -> correct proactively, show transparency
    "We correct an error in Section 3: {old claim} should be {corrected claim}."

  Never be defensive. Never say "the reviewer misunderstood." Frame as:
    "Your feedback led us to discover..."
    "This concern motivated us to investigate..."

---

Principle 7: Character Budget
==============================

Plan allocation per point BEFORE writing. Estimate:

  - A markdown table row ≈ 80-100 chars
  - A 5-row table with header ≈ 500-600 chars
  - A paragraph (3-4 sentences) ≈ 300-500 chars
  - Opening + closing ≈ 200-400 chars

Workflow:
  1. List all points for this reviewer
  2. Assign priority (must / should / if-room)
  3. Allocate chars per point
  4. Draft, then measure with `wc -c`
  5. Trim or expand to fit

---

Principle 8: Anonymous Supplementary
=====================================

When you have more evidence than fits in the char limit:

  Inline (in the response):
    - Compact tables for KEY evidence the reviewer MUST see
    - The finding that answers their specific concern

  Supplementary (anonymous URL):
    - Full tables with all rows/columns
    - Additional analyses, per-subgroup breakdowns
    - Extended method descriptions

  Every response should reference the supplementary:
    "Detailed results are available in the anonymous supplementary: [URL]"

  Setup: GitHub repo (private) + anonymous.4open.science wrapper.

---

Principle 9: Contribution Framing
===================================

New experiments in the rebuttal should serve the paper's THESIS, not
demonstrate effort. Frame correctly:

  Good: "Your insight led us to diagnose three barriers, showing that
         our benchmark enables this research direction."
  Bad:  "We ran 6 additional experiments."

  Good: "This analysis reveals that metric-A fairness can diverge from
         metric-B fairness — a finding that changes how the community
         should evaluate fairness."
  Bad:  "We developed three new metrics."

The paper is a benchmark — its value is enabling research, not solving
every problem. New experiments demonstrate the benchmark's PRESCRIPTIVE
VALUE, not that you threw everything at the wall.

---

Principle 10: Quote-Then-Respond
==================================

Each response block MUST begin with the reviewer's own words before
your answer. This does three things: (1) proves you read carefully,
(2) anchors the reviewer so they know exactly which concern you're
addressing, (3) prevents your response from drifting off-topic.

  Format (see also Principle 3 for narrative structure):

    **{Tags}: {Short title}.**
    > "{Reviewer's key sentence — the core of their concern.}"

    {Your response: acknowledge → evidence → what it means → revision.}

  Rules:

    Quote the CORE, not the whole paragraph.
      Good: > "observed subgroup disparities may be partially driven
            > by CGM device differences"
      Bad:  > (entire 8-line paragraph pasted)

    Your FIRST sentence after the quote must directly answer
    the reviewer's concern — not introduce background or context.
      Good: "We ruled out device confounding by stratifying..."
            (directly addresses "device confounding")
      Bad:  "We conducted several additional analyses..."
            (vague, doesn't connect to the quoted concern)

    Use the reviewer's own terminology in your response.
      Reviewer says "device confounding" → you say "device confounding"
      Do NOT rephrase to "hardware variation" or "sensor differences"

    Every W/Q/L tag must be ctrl+F searchable in the response.
      If reviewer wrote W1, W2, Q1 — all three must appear as tags.

    One block per concern (or per tightly related group).
      OK to group: **W7/W11/Q4: Fairness mitigation.** (same topic)
      NOT OK: answering W1 and W8 in the same paragraph (unrelated)

---

Principle 11: Tone
===================

  Grateful:    "Your suggestion led us to discover..."
               "This concern motivated a deeper analysis that revealed..."

  Not defensive: Never "we disagree" or "the reviewer misunderstood"
                 Instead: "We clarify..." or "We correct..."

  Measured:    Use exact numbers, not enthusiasm.
               "{Method} reduces the gap by 12.4%"
               NOT "our exciting new algorithm dramatically improves fairness"

  Respectful:  Acknowledge the reviewer's expertise.
               "The reviewer correctly identified that our CIs were sample-level."

  Brief:       Don't pad with pleasantries. One opening sentence of thanks,
               then straight to the substance.

  Mandatory opener pattern: EVERY response block must begin with one of:
    - "We thank the reviewer/editor for ..."
    - "We are grateful to the reviewer/editor for ..."
    - "We agree with the reviewer/editor that ..."
    - "We appreciate this comment ..."
    - "We accept this criticism ..."

  Never open with a bare "Agreed." or "Added X." or "Task X provides ...".
  Even for short responses, give one acknowledging clause naming the
  specific concern before the substantive answer. Terse no-subject
  openers read as dismissive even when the substance is strong.

---

Principle 12: Verbatim Reviewer Quoting with Source Tracking
=============================================================

When you quote the reviewer (Principle 10), the text inside the quote
block MUST be a verbatim copy of the sentence(s) from the raw review
file. Do not paraphrase, summarize, fix grammar, or smooth typos.
Reviewers routinely grep your rebuttal against their own letter to
verify they were quoted accurately; a paraphrase invites a strong
negative reaction even when your response is otherwise excellent.

  Rules:

    - Quote VERBATIM. Preserve reviewer typos ("logacion") and
      punctuation. The only allowed adjustment is LaTeX escaping
      (`%` -> `\%`, `&` -> `\&`, `<` -> `\textless{}`).
    - Use `[\ldots]` to indicate elision when skipping irrelevant
      mid-passage text. NEVER use `[\ldots]` to replace material that
      changes the reviewer's meaning.
    - Do NOT flatten reviewer questions into reviewer assertions.
      If the reviewer asked "Is it possible the LLM is largely echoing
      sentiment?" your quote must include the question mark; do not
      rephrase as "The LLM is largely echoing sentiment."
    - Do NOT attribute manuscript-derived phrasings to the editor or
      reviewer. The editor only said what the editor wrote.
    - Above each quote block, add a LaTeX comment with the source:
        % Source: A-review-content/review-R1.md:L42-L44
      This is for internal grep / co-author cross-reference; the
      comment is invisible in the rendered PDF.
    - Multi-paragraph concerns: quote the most pointed 1-3 sentences in
      full; supplement with `[\ldots]` only if you skip text that does
      not change the meaning.

  If you cannot find a verbatim source in the raw review files, do not
  invent text. Add a source comment noting where the concern came from
  (e.g., cover letter, AC summary) and quote that source directly.

---

Principle 13: No Internal Scaffolding in the Rendered PDF
==========================================================

The reviewer-facing PDF must contain zero internal-process artifacts.
Reviewers do not have access to your task-tracker, decision log, file
paths, or revision-checklist IDs, and seeing them feels like reading
someone else's project-management notes.

  Strip from rendered output (keep in LaTeX comments only):

    - File paths:    `04-methods.tex`, `examples/ProjA/...`
    - Revision IDs:  `[R23]`, `[R6]` from revision-checklist.md
    - Task IDs:      `task \texttt{B6}`, `task \texttt{C5}`
    - Decision IDs:  `[D-001]`, `[D-002]` from DECISIONS.md
    - Source paths:  `A-review-content/review-R1.md:L42` (use a `%`
                     LaTeX comment, never visible prose)
    - Label names:   `\texttt{sec:cross_family_judge}`,
                     `\texttt{tab:hard_case_human}`

  Replace task IDs with PLAIN-ENGLISH + manuscript anchor:

    Bad:   "Bootstrap CIs (task \texttt{B6}) confirm precision."
    Good:  "1,000-resample bootstrap confidence intervals
            confirm precision (SPS r = 0.814, 95% CI [0.812, 0.816])."

    Bad:   "Discriminant evidence from task \texttt{C5}."
    Good:  "Discriminant evidence from a partial-correlation analysis
            controlling for star rating (Supplementary Section S5.2,
            Partial Correlation Analysis)."

  Macro design pattern (if using a structured LaTeX rebuttal template):

    - Define macros (\paperedit, \taskref, \decref) that accept internal
      IDs as arguments but DO NOT render those IDs to the PDF.
    - The first arg can be a filename like "04-methods.tex"; resolve it
      to a human section name ("Section Methods") via a lookup table
      in the macro definition.
    - \decref should render NOTHING in the PDF (purely team-internal).
    - \paperedit and \taskref should render "Manuscript change. In
      Section X: ..." and "Supporting analysis. ..." with no bracket
      tag and no file path.

  Verification: after compiling, run
    pdftotext rebuttal.pdf - | grep -E 'task A|task B|task C|sec:|tab:|D-001|D-002|examples/|A-review-content|\\[R[0-9]+\\]'
  Expect zero hits before submission.

  Cross-references to the manuscript: when the rebuttal is compiled
  standalone (not as part of the paper build), `\ref{}` calls to paper
  labels will render as `??`. Either (a) wire up `xr` with
  `\externaldocument` to the paper's `.aux` file, or (b) hardcode the
  section/figure names in prose (e.g., "Supplementary Section S5.2
  (Partial Correlation Analysis)"). Option (b) is more robust for
  one-shot rebuttal compilations.
