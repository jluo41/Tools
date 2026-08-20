# Revise-results craft

Craft file for stage section-edit, loaded by the REVISE phase when the unit is a Results section.
Source: converted from `workers/haipipe-paper-revise-results/SKILL.md` on 2026-08-05 (thin-paper phase 2); it is DATA, not a registered skill.

## Overview

Use this craft for late-stage Results revision when the science is mostly stable but the writing architecture is not.
The job here is narrow: repair subsection titles, bridge paragraphs, paragraph openings, and local argumentative flow.
It runs fully automatically, applies fixes directly, and leaves `%% {CC-results}:` comments explaining WHY for CHECK review.

Before you start, read the shared prose rules: `../../haipipe-paper/ref/prose-quality.md` (one idea per sentence, no em-dash, compress not split, no AI voice, <=6 sentences/paragraph, Pn.Sn markers) — all revise passes enforce them; the checks below are results-specific ADDITIONS, not replacements.

Also read the venue's results conventions from
`0-lifecycle/2-venue/S-Venue-0-venue.md`: its Results blueprint and Writing
Principles. Fall back to the pinned venue pack only when that S page is absent.

Use the DRAFT phase when WHAT the section says is still unsettled; a CHECK restart can return there. Use this craft when the section is largely right but still reads like stitched figure captions rather than a controlled argument.

## Quick Checks

Before revising any Results subsection, check:

1. Is the title selling the conclusion rather than the method?
2. Does the first sentence of each paragraph state that paragraph's point?
3. Are openings like `we asked`, `we examined`, or `to test this` overused?
4. Are abstract words masking a more specific noun?
5. Is the relationship to the previous paragraph explicit?
6. Is the paragraph only reporting a result, or advancing the argument?
7. Does the paragraph close by stating what changes in interpretation?
8. Does the subsection end in a way that naturally leads into the next one?

## Subsection Pattern

Each Results subsection should answer two reader questions in order:

1. Why is this analysis needed now?
2. What does it establish?

If the second question appears before the first, the subsection will feel abrupt.

The first paragraph should bridge from the previous subsection and state why the next analysis is necessary.
Later paragraphs should each do one job: sharpen a finding, separate related findings, show a consequence for evaluation or prioritization, or explain what a comparison actually distinguishes.

## Paragraph Openings

Prefer openings that either orient the reader or state a concrete result:

- `The molecular branch first showed ...`
- `The same pattern was also evident in ...`
- `A further question was whether ...`
- `Cross-representation analyses showed ...`

Avoid repeated procedural scaffolds:

- `To test this ...`
- `We next asked ...`
- `We then examined ...`

At the start of a new paragraph, avoid vague pronouns unless the referent is unmistakable.
Replace `this structure` or `that mismatch` with the explicit noun phrase.

## Style Rules

- One paragraph, one job.
- Use explicit contrasts early.
- Surface key quantitative anchors before interpretation.
- Keep the register controlled, direct, and specific.
- End each subsection with a sentence that changes the reader's expectation for the next subsection.

## Common Failure Modes

- method-like subsection titles
- first paragraphs that announce a result without a rationale
- several paragraphs in a row with the same procedural opening
- abstract nouns that blur what is actually being compared
- summary sentences that restate the result but not its implication
