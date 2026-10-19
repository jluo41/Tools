# Auto revise · rounds until it is good enough, the big decisions held for you

A mode of the Revise Run (`ref/revise.md`), decided as b32 s41-D13 (JL 261016: "auto revise, which means it do several
rounds of revising until the things are self-evaluated good enough, and give some big decisions in the revise area").
The loop is run by haipipe-draft-workflow; this page is what the writer does in each round, and the rule for what it
may change.

## One round

```text
writer (this skill)          revises candidate.md: applies the small fixes, holds the big ones
reviewer (haipipe-draft-review, a FRESH agent each round, never the writer)
                             judges candidate.md on the rubric's four axes (Mechanics · Function · Evidence ·
                             Readability) and runs anti_slop.py audit --format json for the guard score
record                       cli/auto_revise.py record <run> <round.yaml>
check                        cli/auto_revise.py check <run>  →  STOP or CONTINUE, and why
```

The writer only ever edits `candidate.md`, a copy. The Draft is not touched: what reaches it is what the person accepts.

## Small and big

1. **Small, applied in the round**: wording; a broken plain-English rule (a semicolon, a stock AI phrase, an undefined
   word); a long sentence split into two with the same meaning; a join between two sentences.
2. **Big, held for the person**: anything that changes what the text claims, any number, any citation, the order of the
   argument, a sentence added or cut, or the plan (`## 1 · Structure`, owned by haipipe-draft-logic).
3. **When unsure, it is big.** A held decision costs one click; a wrong silent change costs trust.

Each big item is written as a decision: `where` (S5, P4, Section), `what` is at stake, two or three `options`, the
reviewer's `lean` and `why`. NOT VERIFIABLE on an axis is never a pass either: it becomes a decision (add the source,
narrow the claim, or accept it as open).

## When it stops

The rubric says no detector score establishes acceptance, so the stop is the reviewer's verdict:

1. **Ready**: no axis says NEEDS WORK.
2. **No improvement**: the NEEDS WORK count did not fall from the round before, or anti_slop rose by more than 5.
3. **Limit**: 3 rounds (`--max-rounds`).

## What the person sees

`cli/auto_revise.py cards <run>` writes `decisions.yaml`: the decisions first, each once however many rounds held it,
then the small fixes, folded, each with its round, before and after, so any of them can be undone. On a Section canvas
(b21 s05) the Revise area shows the decisions as cards to pick, and one card "N small fixes in K rounds" folded under
them. The person picks; the next writing pass writes the picks and the accepted small fixes into the Draft, through
the sentence addresses (`ref/sentence.md`).

## Where it lives on disk

```text
<task>/runs/run-revise-<target>/auto-<YYMMDD>/
├── candidate.md       the text as it stands after the last round (a copy)
├── rounds/r01.yaml …  each round: rubric verdicts, anti_slop score, small (applied), big (held)
└── decisions.yaml     the cards for the person
```
