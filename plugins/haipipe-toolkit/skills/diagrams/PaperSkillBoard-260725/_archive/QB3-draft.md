# DRAFT: raise every question, invent nothing
state: 🟡 PARTIAL
owner: JL
method: write everything the stage can source, mark everything it cannot, and answer nothing

## Question
What is a DRAFT allowed to write, and what must it refuse to write? This is the phase where a paper is most likely to acquire a lie, because a drafter that stops at every gap produces nothing and a drafter that fills them produces something worse than nothing: prose that reads finished and rests on a number or a source that was never checked.

The rule is a division of labour rather than a limit on effort. DRAFT owns structure, prose and QUESTIONS. It does not own facts. Every assertion it cannot source becomes a marked hole with a named question attached, and the hole is a first-class product of the phase rather than an admission of failure.

The approach is to make the honest path the easy one: a placeholder grammar that is quicker to write than a fabrication, a self-review in a fresh context before anything reaches a human, and a rule that a question raised is progress. What we want is a draft whose every unresolved claim is mechanically findable, so no gap can reach CHECK by being quiet.

## Boundary
- ✅ Covered here
  What DRAFT may write, what it must refuse, what it hands to PROBE, and the self-review that precedes the gate.
- ↪ Covered elsewhere
  The phase order and why evidence enters at only one of them is `QB2`; what a placeholder looks like is `QB6`; how the question actually travels is `QB4`; what the finished artifact is, is `QB9`.

## Diagram
```
   DRAFT
     │
     ├── MAY WRITE ─────────────────────────────────────────────
     │     the section's structure, from the venue blueprint
     │     real prose, one sentence per source line
     │     \citep{key}      ONLY if the key already greps in the .bib
     │     a QUESTION, as a `## Q-<Stage>-<n>` block
     │
     ├── MUST REFUSE ───────────────────────────────────────────
     │     a bibtex entry            the .bib is HUMAN-ONLY
     │     a number it did not read from a landed answer
     │     a citation key it has not verified
     │     an answer to its own question
     │     → each becomes a MARKED HOLE instead:
     │         \cite{TOADD} [Q-Section-4]
     │         {VAL:? what the number is} [Q-Section-4]
     │       marker and bracket SIDE BY SIDE, never fused
     │
     ├── SELF-REVIEW, before any human sees it ─────────────────
     │     a reviewer sub-agent in a FRESH context, because the
     │     drafter does not grade its own work. Checks the draft
     │     against the stage's artifact spec. Returns PASS or a
     │     list; the drafter fixes and re-reviews, bounded.
     │     This PRECEDES the human gate and never replaces it.
     │
     └── HANDS TO PROBE ────────────────────────────────────────
           the Q-consumer block: every question it raised, with
           the stake still attached. PROBE strips the stake.

   ⚠️ ORGANIZE and MATCH used to run HERE. They moved to PROBE on
      2026-07-20, when the DRAFT│PROBE human gate was removed and
      the reason for merging them evaporated. A DRAFT that writes
      a `### q-executor` is doing PROBE's job.
```

## Content
### A question is a product, not a failure
The phase is judged on whether every hole is marked and owned, not on how few holes there are. A section that raises nine questions and states nothing it cannot source has done its job; a section that raises none and quietly asserts a coefficient has not.

That is why the placeholder grammar puts the marker and the bracket side by side rather than fusing them. A `\cite{TOADD}` with no `[Q-Section-n]` beside it is worse than an empty sentence: it is a hole no question will ever fill, and nothing downstream will ever surface it.

### The three sub-workers
```
 draft-citation   walks for assertions owing a source, decides which
                  already have a real key in the .bib, REPORTS the rest.
                  READ-ONLY. It never writes, never searches, never
                  writes bibtex.
 draft-values     the same, for numbers owing a run
 draft-display    the same, for claims owing a figure or a table
```
All three report to the drafter, which holds the pen. That split exists so that finding a hole and filling a hole are done by different things.

### What it means that DRAFT is unattended
DRAFT runs without a human because it cannot spend and cannot assert. Those two limits are what make it safe, and they are the same two limits that make its output incomplete by design. Anything else would need a gate, and the design deliberately spends the human's attention once per stage, at CHECK.

## Items to Finish
- [x] 📐 The one-way rule is stated
      DRAFT writes structure, prose and questions; it refuses facts it cannot source.
- [x] 🔍 The three read-only finders exist
      `draft-citation`, `draft-values`, `draft-display`, none of which hold the pen.
- [x] 🧹 ORGANIZE and MATCH moved out
      Done 2026-07-20 when the DRAFT│PROBE gate was removed; a DRAFT writing a `### q-executor` is doing PROBE's job.
- [ ] 🧠 Rule what DRAFT does with a question it cannot phrase
      A gap it cannot even turn into an answerable question is the one case the grammar has no shape for, and it is the case most likely to become a silent assertion.
- [ ] 🧪 Verify no draft ever writes an unbracketed placeholder
      A checker for `\cite{TOADD}` and `{VAL:?}` with no `[Q-…]` beside them. The grammar states the rule and nothing enforces it.
- [ ] 📐 State the self-review's stopping condition
      "Bounded" is not a number. Say how many rounds, and what happens when it does not converge.

## Where we are
Implemented and in daily use across the MISQ paper, with the placeholder grammar live and the three finders read-only. The phase's discipline holds because it is easier to mark a hole than to fill one, which was the design intent.

Two things are stated and unenforced: the unbracketed-placeholder rule, and the self-review's bound.

## Files
- `2-phase/0-draft/haipipe-paper-draft/`
  The phase worker that holds the pen.
- `2-phase/0-draft/haipipe-paper-draft-citation/`
  The read-only citation finder; its siblings are `-values` and `-display`.
- `stages/5-section-edit/stage.md`
  The `prose_rule` block, which states the placeholder grammar for a section.

## Law
DRAFT writes structure, prose and QUESTIONS. It never writes a fact it cannot source: not a bibtex entry, not a number, not a citation key it has not verified, and never an answer to its own question.

Every unsourceable assertion becomes a marked hole with a named question beside it. The marker and the bracket sit side by side and are never fused, because a placeholder with no question is a hole nothing will ever fill.

A question raised is a product of this phase, not a failure of it. The finders report; the drafter holds the pen; the self-review runs in a fresh context and never replaces the human gate.

## Log
260726 · Created. DRAFT had no face at all: the group claimed to explain the lifecycle and skipped two of its four phases.
