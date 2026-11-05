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

**Prefer a common word when it preserves the exact meaning.** Keep defined
technical terms and explain them when needed; precision is not traded for brevity.

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

**One reader move per sentence.** About 30 words is a prompt to inspect reading
burden, not a ceiling. Keep causal/logical relations and all qualifiers. A
Section's sentence/Bullet mapping may require an owner-approved plan change
before splitting; a clear long sentence may stay as written.

**Split at the hinge**, which is where the sentence changes subject:

❌ `A good question is specific, and being specific usually means naming this board's own things, so the sharper the question the more it leans on words a newcomer does not have.`

✅ `A good question is specific, and being specific usually means naming this board's own things.`
✅ `So the sharper the question, the more it leans on words a newcomer does not have.`

**No semicolons in draft sentences** (JL 2026-10-16: "if possible, do not use ';'"; JL 2026-11-04: "don't use ';' make them as the normal sentences").
A semicolon asks the reader to hold two clauses at once. Split it into plain sentences.
Semicolons stay only where someone else fixes the form: citations inside parentheses, a journal's affiliation list. `cli/anti_slop.py` flags the rest (rule `semicolon`). Statistics inside one parenthesis keep theirs, `(SE = 1.07; 95 percent CI, 0.69 to 4.90; p = 0.009)` (JL 261104: "could we use ';' here? as long as it is not the sentence").

**No transition set off by commas** (JL 261104: "don't use things like ' , however ,', Try to make a sentence to be smooth"). `, however,`, `, therefore,` and their kin stop the sentence in the middle. Rewrite so the sentence carries the turn, and open with a plain `But` or `Yet` when it needs one. `cli/anti_slop.py` flags them (rule `parenthetical-transition`).

❌ `A request, however, names a concrete action.`
✅ `But a request names a concrete action.`

❌ `…from 2015 to 2021 (Wang and Chatterjee, 2025); a CGM records glucose every five minutes.`
✅ `…from 2015 to 2021 (Wang and Chatterjee, 2025). A CGM records glucose every five minutes.`

## 3a · Paragraphs

**A paragraph holds 4 to 6 sentences** (JL 2026-11-04, said more than 4 times: "一个 paragraph 至少是 4~6 句话", "你只有两句话 有点奇怪吧"). A 1- to 3-sentence paragraph is merged with its neighbour on the same topic. One past 6 is split where its topic turns. After any cut (an anti-AI pass, a trimmed limit), recount: cutting sentences is what makes short paragraphs. `cli/paragraphs.py <file>` counts them.

A venue's own form wins and is named as a departure: a journal's short Conclusions, a structured abstract, a numbered list of limitations.

## 3b · Say a limit once

**No over-defensive lines** (JL 2026-11-04: "会不会有点过度防御啊", "do not do overprotection"). "Associated" already says the design is not causal, so do not add "causation cannot be established" or "these are descriptive associations, not causal effects". State each limit once, where it carries content, usually the Limitations. A line that only repeats "associated" is cut outright; it does not move anywhere. Do not hedge a hedge ("may potentially"). A limit stays when it tells the reader something new: what the data cannot separate, or what a score must not be used for. Never swap in a causal verb to drop a hedge: associational claims stay associational.

❌ `The score may carry information about prescribing; causation cannot be established.`
✅ `The score may carry information about prescribing beyond star rating.`

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
