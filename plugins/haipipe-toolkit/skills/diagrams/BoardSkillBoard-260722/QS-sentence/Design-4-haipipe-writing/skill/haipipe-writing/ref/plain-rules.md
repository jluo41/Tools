# The plain-English rules, and the ruling behind each one

Every rule here was ruled by JL on 2026-08-01, while rewriting the design board's
`QB4` page sentence by sentence. Each carries the moment it came from, because a
rule with no story gets argued with; a rule with a story gets applied.

## 1 · The test

Can a reader who does **not read English well** follow this?

That is harder than "is it correct" and harder than "would a newcomer follow it",
and it is the one that catches what the others miss. Prose can be structurally
right, do its job, cite real evidence, and still be unreadable because it is
written in the house shorthand.

Run it on the **heading first**. A heading is what a reader meets before deciding
whether to read on, so a heading that fails has already cost you the reader.

## 2 · Words

**A shorter common word always beats a precise rare one.** You lose no precision:
a plainer word for the same thing is just better writing.

✅ `settles a decision`
❌ `argues one choice to a close`

✅ `give each kind its own layout`
❌ `let each kind lay itself out around whatever it happens to carry`

**Idiom is the specific hazard.** It sounds fluent to the person who wrote it and
like noise to everyone else.

**A word the repo invented is explained where it is used, or it is not used.**
`on stage` appeared seventeen times on `QB4` and was defined nowhere. The fix was
both halves at once: stop using it in headings AND put it in the Glossary, because
either one alone still leaves a reader stuck.

## 3 · Sentences

**One idea per sentence.** Past about 30 words a sentence is usually two, and the
join is usually a colon or a `because` doing work a full stop should do.

**Split at the hinge**, which is where the sentence changes subject:

❌ `A good question is specific, and being specific usually means naming this board's own things, so the sharper the question the more it leans on words a newcomer does not have.`

✅ `A good question is specific, and being specific usually means naming this board's own things.`
✅ `So the sharper the question, the more it leans on words a newcomer does not have.`

## 4 · Headings

**A heading names its CONSEQUENCE, not its mechanism.**

✅ `A blank line decides what people see`
❌ `The opening paragraph ends at the first blank line`

The second one is *true*. It passed every other check on the page, and it told a
reader nothing, because it describes the machine instead of the effect.

## 5 · Shapes

**A good/bad pair gets its own line, marked ✅ and ❌.** Never bury a contrast in a
sentence: `Prefer X to Y, and Z to W` makes the reader hold four quoted phrases at
once and work out which two are the good ones, which is the work the example
existed to save.

**A list that will grow is never written as a closed list.** Name examples and say
the set grows, so a fourth member does not force an edit. The full list belongs in
whatever part owns it.

## 6 · The AI tells this repo has actually produced

Not a general catalogue. These are the ones found in this codebase's own prose.
`cli/score.py` matches exactly these and no others:

- `X is not the thing being traded away: it is Y` — the reversal flourish
- `…, which is why …` bolted onto an already-finished sentence
- `not only … but also`
- the four-slot house skeleton: `This page defines X` / `The hard part is` /
  `Without that` / `It succeeds when`. On one 53-page board, 37 pages ended on
  "succeeds when" and 22 opened on "This page", so the pages differed by one noun.

**The paste test settles any argument.** Swap the subject noun. If it still reads
correctly on a neighbouring page, it said nothing.

## 7 · What no rule here can do

None of this judges whether a sentence is CLEAR. `score.py` counts house words,
long words, sentence length, and known tells; a low score is a worklist being
empty, not a verdict of clear. The judgment stays with a person, and the tools
exist to put the right sentences in front of them.
