# Sentence by sentence logic review

A text reads well only when every sentence follows from the one before it and leads to the one after (JL 261021: "主要是
review 逻辑关系：每句话都要看一下上下文，review 它的逻辑关系是否通顺，并且给每句话打分或评估"; "我觉得这个东西一定要读起来顺才行，
而且要有逻辑"). This method reviews a paragraph or a Section one sentence at a time, each in its context, and gives
each sentence three scores: how well its logic holds (logic), how smoothly it reads (read) and how free it is of AI-writing patterns (ai). The Coherence row of the
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
   things, is a problem. A repeated noun is not a pointer: "an agent" in s6 may name the agent of s4 across s5 and
   still carry, because the noun says what it means; only the pointer words must land in the sentence before.
   A word the author's rulings fix (an opening the author chose) is noted in the problem, not scored down.
3. **Setup and payoff.** A colon, `but`, `because`, `although`, `while`, `if` or `so` promises a relation. Check that
   what follows delivers exactly that relation: "X may make this worse:" must be followed by evidence that it is worse
   in the way "this" names, not by evidence of something else.
4. **Claim fit.** The claim is no stronger than what supports it (a hedge where the source is indirect); the facts
   agree with the sentences before; a word keeps one meaning (term drift: "agent", then "chatbot", then "model" for one
   thing).
5. **Introduced before used (JL 261111: "glucose here is appeared all of a sudden. Do we want to introduce a bit or
   not?").** A domain word, a data type or a model kind is introduced (what it is, where it comes from) before a
   sentence argues with it. "Glucose data are limited" right after a sentence on scaling laws in general is a weak
   link: first "Foundation models are trained on continuous glucose monitoring data, which come only from people
   wearing a sensor", then the limit.
6. **Job.** The sentence does a step of its paragraph's job, and the argument would break without it; it does not
   repeat a sentence before.
7. **Grammar (JL 261118: "can you check this problem? the writing grammar error.", a Word page of Methods with its
   underlines).** The sentence is standard written English, as a careful copy editor reads it: a comma after an opening
   phrase ("For all three traits, we report"), articles and agreement right, numbers in prose as decimals (0.001,
   never the code form 1e-3), and no script label used as an English noun ("the selection patients" is "the 24
   patients held out for selection"; "each share MLP" is "the MLP for each share"). A grammar error caps read at 6,
   so W4 must fix it, and the problem names it as `grammar: <what>`. Run `cli/grammar.py <draft>` first: what it
   names is certain; the rest is the reader's job.

Logic has three levels, and this method reads all three (JL 261021: "当我们说 logic 的时候，是不是指既有它所谓的
logic，比如 transition、逻辑衔接，或者是不是达到了总分总这种结构？"): the sentence (checks 1 to 6), the paragraph's shape,
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

Each sentence gets a logic score, a read score (easy to read) and an ai score (free of AI-writing patterns), out of
10 (JL 261113: every sentence carries an AI-writing and an easy-to-read score). A sentence passes at 8 or more on all
three, with no broken link.

| Score | Logic | Read | AI |
|---|---|---|---|
| 9-10 | link carried, every pointer clear, the payoff matches its setup | reads in one pass, natural | no AI-writing pattern |
| 8 | one tiny gap a reader would not notice | one tiny stumble | one faint pattern |
| 7 | the link is weak, or one pointer is unclear | one clear stumble | one clear pattern (a stock word, a definition stack, self-narration) |
| 5-6 | the payoff does not match its setup, or the claim outruns its support | hard to read in one pass | two or more patterns |
| 0-4 | broken: no link, or the sentence contradicts the one before | broken | reads as machine text |

The ai score uses the anti-AI evaluator's patterns (`hai-draft-review`, Mode 1); the problem names the pattern.

**Topic check (JL 261111).** Name each sentence's topic in two or three words before scoring. A sentence with two
topics scores at most 7 on read ("too packed": cut it to one topic; a split adds a sentence and its Bullet, so it is proposed to the writer as a plan change); a sentence that carries only half of the topic its neighbour
started scores at most 7 on read ("fragmented": merge it with that neighbour). One topic with one or two points is
the target (`plain-rules.md` §3).

**Natural phrasing (JL 261115: "one rule is to identify the weird non-human expression").** Read each sentence aloud
and quote any phrase a working scientist would not say to a colleague or write in a paper: stiff, bookish or
translated-sounding wording, a verb doing an odd job, a noun where a plain verb fits. Name the phrase and give the plain
one in the problem field (`"need not mean" → "does not always mean"`). One such phrase scores ai at most 7, even when
no AI-writing pattern is present. Worked examples (ScalingGlucose t01 v1.7, all missed by three readers):

| Written | Plain |
| --- | --- |
| A lower loss need not mean a better forecast | does not always mean |
| cannot say by itself which uses scale will improve | cannot tell us which uses will improve with scale |
| the readings already held | the readings they already have |
| Patients never seen in pretraining keep more error | have higher error |
| each reading sits in several overlapping training windows | appears in |

**Point count (JL 261115: "one sentence one topic, usually one or two points, at most three points").** A point is
one separate claim, result, definition or reason; a clause that only qualifies another (a time, a place, a condition)
is not a point of its own. One or two points is the target; three is the most a sentence carries. Four or more scores
at most 7 on read, like two topics ("too many points": split it). Count before scoring, and write the count on the line
(the problem field opens with it, below), so the person sees why a sentence passed or failed. Example: "A lower loss
need not mean a better forecast, patient description or clinical answer, and foundation models in health care need new
ways to judge whether they are reliable" is `topics 2, points 2`: loss against use, and how to judge health models,
joined by "and"; read at most 7.

## The line, one per sentence

The id is the Draft's own, written `s<n>`; an older report's `S<n>` is read as the same sentence.

```
Sentences:
- <address> · logic <0-10>/10 · read <0-10>/10 · ai <0-10>/10 · link: <relation>, <carried | weak | broken> · topics <n>, points <m>: <topic in 2-3 words>; <the specific problem> · Fix: <none | the rewritten sentence>
```

- **A problem always comes with a cure (JL 261115: "for the sentences with problem, please show the editing card with
  reasoning and suggestion options").** A sentence under 8 on any score, with a weak or broken link, or over the point
  rule never ends `Fix: none`: give the rewritten sentence, or, when the cure is a choice (a split, a cut, which claim
  to keep), `Fix: A <option> | B <option>`. The writer turns each into an Edit card (hai-draft-writing
  `ref/revise.md`); must-check M-D22.
- **`Fix:` holds the sentence itself, never a pointer (JL 261115: "the editing card is very bad").** Draft Lab
  shows the Fix text as the suggested replacement, strikes the old sentence through and offers ✓ Use this, so
  `Fix: see the card` put the words "see the card" up as the new sentence. When the sentence has an Edit card, copy
  the card's Expected (its Chosen option) into `Fix:`; when the Chosen option is keep, write `Fix: none`.
- **The count** opens the problem field: `topics 1, points 2: loss against use;` then the problem. Draft Lab shows it
  on the sentence's review card, and marks it when there are two topics or more than three points.

- **The specific problem** names the words and the check that fails, in at most 25 words: "'this' points to coverage
  in s8, but the second half is about wrong names" (setup and payoff), not "flows poorly". It answers the question a
  reader would ask at that spot ("why is this here?", "what does 'this' mean?"): the words, what they promised, what
  the reader got. When the logic holds, say what holds it in the link field ("'This list' picks up s6's short list"),
  so the author can trust it and move on; the problem is then "none", or a tiny gap named as tiny.
- **Fix** is the full rewritten sentence, one sentence, the same facts, numbers and citation keys, no fact added,
  changing the fewest words that cure the problem; a Fix that keeps less than 60% of the sentence (difflib ratio)
  needs a problem a small edit cannot cure, never style alone (JL 261113; hai-draft-writing `ref/revise.md`);
  given for every sentence below 8 and every weak or broken link; a sentence at 8 or more may carry one marked
  `Fix (optional):`. A rewrite that breaks one of the author's rulings is
  no fix. When the sentence is right but in the wrong place, the Fix is `move after s<n>` with its reason in the
  problem; the move is the writer's to weigh, since it changes the paragraph's order (its plan). When a word cap binds
  (an abstract at its venue's limit), a Fix that adds words names what it cuts, or the Venue row says how many words
  the Fixes add in all; a sentence too long for one pass is shortened, never split, since one sentence per S holds.
- After the lines, one line per paragraph: `Flow P<k>: s<a> <step> → s<b> <step> → … · shape: topic s<a>, support
  s<b> to S<c>, hand-off S<d> (or "none", with what is missing) · weakest join S<x> to S<y>`.
  The paragraph's opening seam belongs to it and may be its weakest join; when every join carries, name the least
  strong one.

The host shows these lines as a table beside the text (hai-draft-writing `ref/revise.md`, the workbench's 📋
Revise Review Report, and each score on the sentence's own row); a Revise loop ends only when every sentence passes.
