# Pitch Readability

The pitch is the one-minute, skim-in-one-screen artifact. If a reader slows down
to parse a sentence, the pitch failed. Read each section aloud; if you stumble,
rewrite it.

## Global language rules

1. One idea per sentence. Do not bundle method + claim or claim + interpretation.
2. Lead with the point. The result or the question comes first, context second.
3. Keep sentences short. Most under ~25 words; the hook question <=20.
4. Use plain words. Prefer "more / fewer / raises" over "elevated / diminished / is associated with an increase in". Avoid discipline jargon the target venue's readers will not parse (e.g. "extensive / intensive margin" for a clinical audience: say "whether an opioid is prescribed" vs "the dose once prescribed").
5. Use concrete numbers, not qualifiers. "raises MME by 12.9 (N=766k)" beats "higher".
6. No AI voice. No buzzword stacks, no italics-on-nouns, no parenthetical name-explosions.
7. Use active verbs. "Agreeable physicians prescribe more" beats "more is prescribed by".
8. Compress, do not split. Drop adjectives and hedging rather than chopping into fragments; <=6 sentences per paragraph.
9. Frame as a trade-off or mechanism, not as blame. Do not villainize a group; explain the behavior and what it trades off. Not "nice doctors over-prescribe", but "being agreeable can mean yielding to patient pressure, while clinical firmness can protect".

## Section cues (lead each section the right way)

| Section | Lead with | Ceiling / rule |
|---|---|---|
| One-Minute Pitch | a short plain-language paragraph a newcomer understands and finds interesting | ~4-6 short sentences; assume no background |
| Hook | one curiosity move: scene / surprise / paradox+stakes / one question | 2-4 short sentences (grab -> deepen -> bridge); commit to ONE move; never stack questions; any question <=20 words |
| Finding - Surprise | the unexpected result (sentence 1) | then the tension it creates |
| Implication - So What | what changes + who can act | in the first two sentences |
| Audience and Venue Fit | the reader and their need | before naming the venue format |
| Evidence - Why Believe | each claim tied to a table/display/model/check/source | mark planned evidence as planned |
| Limitation - Still Fragile | the top three highest-risk weaknesses | nothing else |
| Next Evidence Move | a verb + the artifact it updates | e.g. "Test... and backfill the ledger" |

## The One-Minute Pitch is for a newcomer

Write the One-Minute Pitch for a reader who knows little about the topic. Give
just enough plain-language context that they understand the question, then the
surprising finding, then why it matters, so they finish able to repeat the gist
and curious to read on. It is a short paragraph (~4-6 short sentences), not a
single compressed thesis sentence; a lone kernel reads as too terse for a
newcomer. Keep every sentence short and one-idea, but do not strip the context
that makes a newcomer care.

Open with a plain framing sentence that names what you study: "We study whether
X relates to Y" or "We study how X shapes Y". Then give the puzzle, the method in
plain words, the surprising finding, and why it matters.

## A good hook: narrative methods

A hook creates a curiosity gap and commits to ONE narrative method (the best
hooks often combine two, like paradox + stakes). Pick deliberately from this
menu; never default to a stack of questions.

Length: a hook is short but not bare, about 2-4 short sentences. Open with the
move, add a sentence that deepens the tension or stakes, and bridge toward the
question. One lone sentence reads as abrupt; more than four loses punch and starts
to overlap the One-Minute Pitch.

| Method | What it does | Fits | Risk | Template |
|---|---|---|---|---|
| Paradox / tension | sets expectation against reality | behavioral, provocative venues | a weak contrast feels contrived | "We reward X; yet X does the opposite." |
| Vivid scene | a concrete moment with specifics | newcomers, broad audiences | anecdote is not evidence; soft for clinical | "Two [subjects], same [condition], two [outcomes]." |
| Surprising fact | leads with the counterintuitive result | confident empirical work | spoils the Surprise section | "The most [praised X] is the worst [Y]." |
| Stakes / consequence | opens with what is at risk | policy, clinical impact | generic fear-mongering | "[Big harm] continues, yet we cannot explain [gap]." |
| Gap / unexplored | names an obvious-in-hindsight blind spot | justifying novelty | weak alone; reviewers dislike pure gap-filling | "[Abundant data] exists, yet no one has asked [question]." |
| One sharp question | a single curiosity-gap question (<=20 words) | inviting the reader in | defers the payoff; never stack questions | "Can [X], [vividly described], predict [Y]?" |
| Reframe / new lens | views the familiar from a surprising angle | fresh framing | can oversimplify | "[X] is usually [done one way]; what if it already exists [another way]?" |

Choosing:
- Commit to one method, or a deliberate combination of two; never stack rhetorical questions, which dilutes the punch and reads as undecided.
- For medical and empirical venues, strongest to weakest: paradox+stakes > surprising fact > vivid scene; gap and single-question are weaker alone; analogy or metaphor is risky in clinical writing.
- When unsure, draft the hook in two or three methods and compare before committing.
- During selection, lay the candidates out as `\subsection*` blocks under the Hook section (one per method, the chosen one marked "(selected)"), compile, and compare in the PDF; collapse to the selected hook once it is locked.

Worked example (commit to one move):
BEFORE (four stacked questions): "Why do two patients with the same back pain leave two physicians with very different opioid prescriptions? How much of that gap is the physician rather than the patient? And could the way patients describe a physician online reveal who prescribes more? Millions of patient reviews already describe these physicians, yet prescribing research has barely read them."
AFTER (paradox + stakes): "We train doctors to be agreeable, and patients reward it. Yet in the middle of an opioid crisis, the most agreeable-seeming doctors may be writing the riskiest prescriptions."
Rule applied: commit to one move; drop the question stack; tie to stakes the reader already cares about.

## Before and after rewrites

Quoted from a real `1-pitch.tex` (Paper-Personality-Opioid-MedJournal).

**Pair 1 — audience before venue format (section cue: Audience).**
- BEFORE: "The target venue is a general medical journal, read by clinicians and health-policy audiences in a JAMA-style IMRAD format."
- AFTER: "Clinicians and health-policy readers need scalable ways to detect unsafe opioid prescribing."
- Why: name the reader and their need first; the venue format is not what makes them care.

**Pair 2 — say what the artifact proves (section cue: Why Believe; rule 5).**
- BEFORE: "The main adjusted association is planned as Table 1 and Display 01."
- AFTER: "Table 1 and Display 01 will show the adjusted association between perceived agreeableness and opioid intensity."
- Why: tie the artifact to the claim it supports, not just its existence.

**Pair 3 — verb + artifact (section cue: Next Evidence Move; rule 2).**
- BEFORE: "Probe the threshold result and the severity confound for robustness."
- AFTER: "Test the threshold result and the severity confound, then backfill the result into the claim ledger."
- Why: start with a concrete verb and name the artifact the move will update.

## Reviewer checklist

- [ ] One-Minute Pitch is a short newcomer paragraph (~4-6 short sentences) opening with a "We study..." framing sentence.
- [ ] Hook commits to one narrative method (not a stack of questions) and leads the section; any question <=20 words.
- [ ] Surprise states the unexpected result in sentence 1.
- [ ] Implication names who can act within the first two sentences.
- [ ] Audience names the reader and their need before the venue format.
- [ ] Every Why-Believe sentence links to an artifact or source; planned evidence is marked planned.
- [ ] Still Fragile lists at most three weaknesses.
- [ ] Next Evidence Move starts with a verb and names the artifact it updates.
- [ ] Read aloud without stumbling; one idea per sentence; no AI voice.

## Done-gate use

Readability is part of the pitch exit criteria. The pitch gate fails before
marking the pitch `working`, `reliable`, or `paper-ready` if any section misses
its cue (wrong lead, over the word ceiling), any Why-Believe sentence is
unsupported with no source or planned artifact named, or Next Evidence Move
lacks a verb and a named artifact.
