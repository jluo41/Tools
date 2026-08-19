# display-rules · what an agent checks before 🖼 `accepted:`

Seeded 260818 from the `display-*` findings `cli/check.py` already emits, plus
the craft checks nothing was running. A rule here is LOCAL and has a right
answer independent of intent.

## Already mechanical · `cli/check.py` emits these today

```text
R1  display-declared-no-claim      the README states a claim under one of the
                                   contract's row names. A folder without a
                                   claim is not a proposal.
R2  display-declared-not-rendered  a unit folder is not a display; the
                                   projections embed only rendered units
R3  display-intake-unfrozen        intake/inputs/ holds a frozen snapshot, so
                                   a printed number can be traced back
R4  display-accept-stale           no `accepted: ✅` binds a render whose
                                   inputs have since changed
R5  display-cited-not-embedded     a unit the prose cites appears in the
                                   built .tex
R6  display-rendered-not-cited     a rendered unit is cited by some sentence,
                                   or no reader ever reaches it
```

⚠️ **R7 was listed here and does NOT exist in the checker** (found 260818 by the
first display approver). `display-preview-stale` appears only as an HTML badge
at `src/page_question.py:695`; the six codes `cli/check.py` really emits are
R1-R6, at `src/page_evidence.py:234-292`. It moved to the craft list below and
must be run BY HAND until someone adds it, because a rule filed under
"mechanical" that no machine runs lets a stale preview pass silently.

Run them, do not re-implement them:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board> | grep '^<page>.md'
```

## Craft · write these, they are not yet checked anywhere

```text
R7   PREVIEW NEWER THAN ITS RECIPE. `stat` the mtimes: `preview.pdf` and
     `assets/figure.pdf` are not older than anything under `recipe/`. When
     they are, say whether the diff was cosmetic, and fail anyway: nobody
     recompiled, so nobody knows whether it was.
R8   LEGIBLE AT PRINT SIZE. Open preview.pdf, render one page to png, and
     READ it. Body text under about 6pt at the size it is embedded fails.
     ⬅ this is a look, not a grep, which is why an agent must open the pdf
R9   NOTHING CLIPPED. No row, axis label, legend entry or table column runs
     off the crop. Compare the asset's page box against its content box.
R10  AXES AND UNITS LABELLED. Every numeric axis carries a name and a unit.
     A bare number axis is a defect even when the caption explains it.
R11  THE CAPTION MATCHES THE FIGURE. Every noun the caption promises appears
     in the drawing, and the drawing states no number the caption denies.
R12  THE CLAIM IS VISIBLE. The README's `claim:` is something a reader could
     conclude FROM the picture, not something only the author knows.
R13  ONE PAGE. A unit whose preview.pdf runs to two pages is a unit whose
     geometry was never set; it prints wrong in every host.
R14  NO INVENTED VALUE. Every number drawn appears in intake/inputs/. A
     renderer that computes a new number is out of its authority.
```

## 🚫 NOT rules, and never write them here

```text
"is this display good overall?"
"is this the right chart type for this argument?"
"does this figure carry its weight on the page?"
```

These are whole-artifact judgments that depend on what the page is FOR, so
they change with intent and cannot be written once. They are a person's 🛑,
and an agent asked them would answer confidently and be wrong.
