# Paragraph logic review

A paragraph can pass sentence by sentence and still fail as an argument (JL 261115: "I think we should also have a AI
reviewer to review the paragraph level logics, to check whether the logic is correct or not"). On the ScalingGlucose
Abstract every join read "carried" in `sentence-logic.md`, yet JL found two breaks: the findings went data, model,
data, and the closing sentence used an idea ("where past readings carry the answer") that nothing before set up.
This method reads the paragraph as one argument, before the sentence review, by a reviewer who never wrote it
(SKILL.md, independence). It never edits the text.

## When it runs

First, before `sentence-logic.md`. Polishing sentences that sit in the wrong order wastes a round: a move or a
missing step changes which sentences exist. A paper review round runs it as its own Task (`t03_paragraph_logic` in a
`jNN_review_<who>_v<MMDD>` Job, hai-paper-draft); a Revise pass runs it inside its report, on the Flow lines.

## Step 1 · the skeleton

One line per sentence: `s<n> · <role> · <topic in 2 or 3 words> · <its claim in 10 words or fewer>`. Roles: premise,
gap, pivot (Here we), design, finding, implication, advice, hand-off. Name the topic by its axis, not its wording:
"new data" and "repeated data" are both the topic **data**; "model size" is another topic.

## Step 2 · six checks, each scored 0-10

9-10 good, 8 passes, 7 weak, 6 or less broken. Each check names the sentences it rests on.

1. **Question answered.** The question or gap the paragraph opens is the one its end answers. Name the question and
   the sentence that answers it. A gap that asks one thing ("does scale help each task?") and an end that answers
   another ("scale helps where readings carry the answer") fails.
2. **Order.** Sentences on one topic sit together, in the order the reader's questions arise. A topic that leaves and
   comes back (A, B, A) fails, judged by the axis names of Step 1: new data, model size, repeated data is data,
   model, data. Name the order you would use.
3. **Inference.** Every conclusion, implication or advice names, or plainly rests on, the earlier sentences that
   support it, and uses only ideas those sentences set up. Name the sentences each conclusion rests on and any idea it
   brings in fresh (a mechanism, a category such as "tasks whose answer is in the past readings").
4. **Scope.** No conclusion is wider or stronger than its findings: a claim about "scale" when only data was shown to
   help, a negative ("rarely", "barely", "fades") with no task or range, a cause that was not tested. A host's own
   scope rule (a paper's Narrative, a venue rule) is checked here and named.
5. **Complete and needed.** No step the argument needs is missing (name what one sentence must say), and no sentence
   could be cut without loss.
6. **Shape.** A topic at the start, support in the middle, a hand-off or a close at the end (`sentence-logic.md`,
   总分接). A closing summary belongs only at the end of a Section or an Abstract.

## Step 3 · the verdict and the smallest fix

One verdict line, then the smallest paragraph-level fix: a move (`move s<n> after s<m>`), a missing step (what the one
sentence must say), a sentence to cut, or none. Keep every number and citation. When a word cap binds, say how many
words the fix adds and what it cuts. A fix that changes the order or the set of sentences is a plan change: it goes
to the writer as a `### Section question` card, and the person signs the new Structure before the sentences change
(hai-draft-logic).

## The lines

In a Revise pass the result sits on each paragraph's Flow line, after the sentence lines:

```
Flow P<k>: s<a> <step> → s<b> <step> → … · shape: topic s<a>, support s<b> to s<c>, hand-off s<d> · argument: question <n>/10 · order <n>/10 · inference <n>/10 · scope <n>/10 · complete <n>/10 · <grouped | A-B-A at s<x>> · close rests on s<a> to s<b> · missing: <none | the step>
```

As its own Result (a review round's `t03_paragraph_logic`), one file per Section, `logic-<section>.md`: a header with
the Draft version and a verdict, then per paragraph `### C<n>.P<m> · <title> · <lowest check>/10` with Claim, Support,
the skeleton, the six scores with their sentences, and Fix.

## What it does not do

It does not score sentences (`sentence-logic.md` does), rewrite them, or judge plain words (`plain-rules.md`). It does
not decide the order: it proposes one, and the person signs the Structure.
