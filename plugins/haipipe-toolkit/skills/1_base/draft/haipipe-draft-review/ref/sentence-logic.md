# Sentence by sentence logic review

A text reads well only when every sentence follows from the one before it and leads to the one after (JL 261021: "主要是
review 逻辑关系：每句话都要看一下上下文，review 它的逻辑关系是否通顺，并且给每句话打分或评估"; "我觉得这个东西一定要读起来顺才行，
而且要有逻辑"). This method reviews a paragraph or a Section one sentence at a time, each in its context, and gives
each sentence two scores: how well its logic holds (logic) and how smoothly it reads (read). The Coherence row of the
Revise review overlay (`evaluation-rubric.md`) is the Section's summary of these lines.

It is a review, so its reviewer never wrote the text (SKILL.md, independence) and never edits it.

## How to read

Read the whole paragraph once for its argument: what each paragraph is for, and the order of its steps. Then read
each sentence with the sentence before it and the sentence after it in view, and check five things.

1. **Link.** How does it join the sentence before? Name the relation: continues (the same subject goes on), example,
   cause, consequence, contrast, turn (However), concession (although), condition (if), or a new step. Then judge it:
   **carried** when the first words connect to what the sentence before said; **weak** when the reader must supply
   the link; **broken** when a new topic arrives with no link, or a turn word turns from nothing. A paragraph's first
   sentence links to the last sentence of the paragraph before, read with its own heading: a text of n sentences has
   n - 1 joins, paragraph seams included, and the Coherence row counts all of them.
   The text's very first sentence has no join: write `link: opening, carried` when it opens the argument, `weak`
   or `broken` when it does not.
2. **Reference.** Every `this`, `that`, `it`, `these`, `such`, `also`, `still`, `the same` and `instead` points to one thing,
   in the sentence before, that the reader can name. A pointer that reaches back two sentences, or that could mean two
   things, is a problem. A repeated noun is not a pointer: "an agent" in S6 may name the agent of S4 across S5 and
   still carry, because the noun says what it means; only the pointer words must land in the sentence before.
   A word the author's rulings fix (an opening the author chose) is noted in the problem, not scored down.
3. **Setup and payoff.** A colon, `but`, `because`, `although`, `while`, `if` or `so` promises a relation. Check that
   what follows delivers exactly that relation: "X may make this worse:" must be followed by evidence that it is worse
   in the way "this" names, not by evidence of something else.
4. **Claim fit.** The claim is no stronger than what supports it (a hedge where the source is indirect); the facts
   agree with the sentences before; a word keeps one meaning (term drift: "agent", then "chatbot", then "model" for one
   thing).
5. **Job.** The sentence does a step of its paragraph's job, and the argument would break without it; it does not
   repeat a sentence before.

Logic has three levels, and this method reads all three (JL 261021: "当我们说 logic 的时候，是不是指既有它所谓的
logic，比如 transition、逻辑衔接，或者是不是达到了总分总这种结构？"): the sentence (checks 1 to 5), the paragraph's shape,
and the Section's arc.

- **Paragraph shape: topic, support, hand-off (总分接).** The first sentence says what the paragraph is for (topic,
  总); each middle sentence backs it (support, 分); the last leads into the next paragraph (hand-off, 接). A closing
  summary (the second 总 of 总分总) belongs only at the end of a Section or a paper; inside an Introduction it repeats
  what the reader has just read. Name a missing part: no topic sentence (the claim arrives in the middle), a support
  sentence that backs another paragraph, or no hand-off (the next paragraph's first words must turn alone).
- **Section arc.** The paragraphs come in the order a reader's questions arise (for an Introduction: what is
  happening, why it matters, what is not known, what we did); a paragraph out of order is a paragraph-level problem,
  reported on its Flow line.

- **A text under headings** (a structured abstract, Key Points, a cover letter's labeled parts). Each heading stands
  alone: its first sentence is an opening (`link: opening of <heading>, carried` when it does its heading's job), and
  joins are counted only inside a heading. A heading of one sentence gets no Flow line; Key Points (Question, Findings,
  Meaning) get one Flow line together. Its shape is the heading's job (Objective is one aim, Results answer the
  questions in order), so `hand-off` is "none needed" except where the next heading leans on it (Conclusions leads
  into Relevance). A pointer that crosses a heading ("These findings" in Meaning) is allowed when the heading before
  holds what it names.

Then read it once more for **read**: natural words for the venue's reader (a reader whose first language is not
English included), subject and verb early, nothing between subject and verb that the reader must hold, one pass.

## Scores

Each sentence gets a logic score and a read score, out of 10. A sentence passes at 8 or more on both, with no broken
link.

| Score | Logic | Read |
|---|---|---|
| 9-10 | link carried, every pointer clear, the payoff matches its setup | reads in one pass, natural |
| 8 | one tiny gap a reader would not notice | one tiny stumble |
| 7 | the link is weak, or one pointer is unclear | one clear stumble |
| 5-6 | the payoff does not match its setup, or the claim outruns its support | hard to read in one pass |
| 0-4 | broken: no link, or the sentence contradicts the one before | broken |

## The line, one per sentence

```
Sentences:
- S<n> · logic <0-10>/10 · read <0-10>/10 · link: <relation>, <carried | weak | broken> · <the specific problem> · Fix: <none | the rewritten sentence>
```

- **The specific problem** names the words and the check that fails, in at most 25 words: "'this' points to coverage
  in S8, but the second half is about wrong names" (setup and payoff), not "flows poorly". It answers the question a
  reader would ask at that spot ("why is this here?", "what does 'this' mean?"): the words, what they promised, what
  the reader got. When the logic holds, say what holds it in the link field ("'This list' picks up S6's short list"),
  so the author can trust it and move on; the problem is then "none", or a tiny gap named as tiny.
- **Fix** is the full rewritten sentence, one sentence, the same facts, numbers and citation keys, no fact added;
  given for every sentence below 8 and every weak or broken link; a sentence at 8 or more may carry one marked
  `Fix (optional):`. A rewrite that breaks one of the author's rulings is
  no fix. When the sentence is right but in the wrong place, the Fix is `move after S<n>` with its reason in the
  problem; the move is the writer's to weigh, since it changes the paragraph's order (its plan). When a word cap binds
  (an abstract at its venue's limit), a Fix that adds words names what it cuts, or the Venue row says how many words
  the Fixes add in all; a sentence too long for one pass is shortened, never split, since one sentence per S holds.
- After the lines, one line per paragraph: `Flow P<k>: S<a> <step> → S<b> <step> → … · shape: topic S<a>, support
  S<b> to S<c>, hand-off S<d> (or "none", with what is missing) · weakest join S<x> to S<y>`.
  The paragraph's opening seam belongs to it and may be its weakest join; when every join carries, name the least
  strong one.

The host shows these lines as a table beside the text (haipipe-draft-writing `ref/revise.md`, the workbench's 📋
Revise Review Report); a Revise loop ends only when every sentence passes.
