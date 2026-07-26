# DRAFT · What must a draft refuse to write?
state: 🟡 PARTIAL
owner: JL
method: write everything the stage can source, mark everything it cannot, and answer nothing

## Question
DRAFT is the phase where a paper is most likely to acquire a lie. A drafter that stops at every gap produces nothing; a drafter that fills them produces something worse than nothing, which is prose that reads finished and rests on a number or a source nobody checked. So the useful question is not what DRAFT writes. It is what it must refuse to write, and whether the refusal has anywhere to go.

The refusal has a shape: a marked hole with a named question beside it. `\cite{TOADD} [Q-Section-4]` and `{VAL:? what the number is} [Q-Section-4]`, marker and bracket side by side and never fused. That design makes the honest path the cheap one, because writing a placeholder is faster than fabricating a citation, and it makes the dishonest path visible, because a hole is grep-able and a fabrication is not.

Two holes in the scheme are open, and both are about the cases the grammar does not cover. A `\cite{TOADD}` written with no bracket beside it is worse than an empty sentence: it is a hole no question will ever fill, and nothing on this system detects one. And a gap the drafter cannot even turn into an answerable question has no shape at all, which makes it the case most likely to become a quiet assertion instead.

## Boundary
- ✅ Covered here
  What DRAFT may write, what it must refuse, the placeholder grammar it writes instead, and the self-review before the gate.
- ↪ Covered elsewhere
  Where the question then goes is `QB9`; who discharges the placeholder is `QB10`; how a placeholder renders as a chip is `QC1` and `QC2`; what a surviving one means at the gate is `QB11`.

## Diagram
```
   ✍️ DRAFT                                       runs UNATTENDED

    ── MAY WRITE ─────────────────────────────────────────────────
       the section's structure, from the venue blueprint
       real prose, one sentence per source line
       \citep{key}     ONLY if the key already greps in the .bib
       a QUESTION, as a `## Q-<Stage>-<n>` block

    ── MUST REFUSE ───────────────────────────────────────────────
       a bibtex entry           the .bib is HUMAN-ONLY 🔒
       a number it did not read from a landed answer
       a citation key it has not verified
       an answer to its own question

       ▼ each becomes a MARKED HOLE instead

         \cite{TOADD}          [Q-Section-4]
         {VAL:? what is owed}  [Q-Section-4]
         ╰─ the marker ─╯      ╰─ who owes it ─╯
         side by side. NEVER fused.

    ── BORN FROM CONTENT, DIES INTO CONTENT ──────────────────────
       DRAFT  ──▶ the sentence that needs it drops it in
       PROBE  ──▶ the bracket is claimed by a probe entry   → QB9
       REVISE ──▶ the landed answer is substituted, and it is gone
                                                            → QB10
       it is NOT a TODO list beside the prose. It lives INSIDE the
       sentence that owes it, which is why it cannot be forgotten
       separately from the claim it supports.

    ── THE THREE FINDERS, all READ-ONLY ──────────────────────────
       draft-citation   walks for assertions owing a SOURCE
       draft-values     …owing a NUMBER
       draft-display    …owing a FIGURE or TABLE
       all three REPORT. The drafter holds the pen. Finding a hole
       and filling a hole are done by different things on purpose.
       None of them searches. None of them writes bibtex.

    ── SELF-REVIEW, before any human sees it ─────────────────────
       a reviewer sub-agent in a FRESH context, because the drafter
       does not grade its own work. Checks the draft against the
       stage's artifact spec, returns PASS or a list, the drafter
       fixes and re-reviews, "bounded".
       ⚠️ "bounded" is not a number.
       This PRECEDES the human gate and never replaces it. → QB11

   ── THE TWO STATES THE GRAMMAR CANNOT SEE ─────────────────────────
      ⚠️ \cite{TOADD} with NO bracket
         a hole no question will ever fill. Nothing detects it.
      ⚠️ a bare numeral typed straight into prose
         invisible by construction: there is nothing to hang a
         placeholder on.                                    (→ QC2)

   ── moved out, 2026-07-20 ─────────────────────────────────────────
      ORGANIZE and MATCH used to run HERE. They left for PROBE when
      the DRAFT│PROBE gate was removed and the reason for merging
      them evaporated. A DRAFT that writes a `### q-executor` is
      doing PROBE's job.
```

## Content
### A question is a product, not a failure
The phase is judged on whether every hole is marked and owned, not on how few holes there are. A section that raises nine questions and asserts nothing it cannot source has done its job. A section that raises none and quietly states a coefficient has not, and it looks better while being worse, which is exactly why the rule has to be structural rather than cultural.

### Why unattended is safe here
DRAFT runs without a human because it cannot spend and cannot assert. Those two limits are what make it safe to leave alone, and they are the same two limits that make its output incomplete by design. Anything else would need a gate, and the design deliberately spends the human's attention once per stage.

### The case with no shape
A gap the drafter cannot phrase as an answerable question fits none of the grammar. It is not a missing citation and not a missing number; it is a claim whose evidence nobody knows how to go and get. Today it has no marker, so it becomes prose, and prose is the one form in which it stops being visible. This is the most dangerous open item on the page and the least discussed.

## Items to Finish
- [x] 📐 The one-way rule is stated
      DRAFT writes structure, prose and questions; it refuses facts it cannot source.
- [x] 🏷 Typed placeholders exist, each naming its owing question
      Marker and bracket beside each other, never fused.
- [x] 🔍 The three finders are read-only
      `draft-citation`, `draft-values`, `draft-display`; none holds the pen.
- [x] 🧹 ORGANIZE and MATCH moved out
      2026-07-20, when the DRAFT│PROBE gate was removed.
- [ ] 🧠 Rule what DRAFT does with a gap it cannot phrase as a question
      The one case the grammar has no shape for, and the case most likely to become a silent assertion.
- [ ] 🔍 Detect an unbracketed placeholder
      A checker for `\cite{TOADD}` and `{VAL:?}` with no `[Q-…]` beside them. The grammar states the rule and nothing enforces it.
- [ ] 📐 State the self-review's stopping condition
      "Bounded" is not a number. Say how many rounds, and what happens when it does not converge.

## Where we are
Implemented and in daily use across the MISQ paper. The discipline holds because the design made marking a hole cheaper than filling one, which was the intent rather than a happy accident.

Two rules are stated and unenforced, the unbracketed placeholder and the self-review's bound, and one case is unruled and invisible: the gap with no phrasable question.

## Files
- `2-phase/0-draft/haipipe-paper-draft/`
  The phase worker that holds the pen.
- `2-phase/0-draft/haipipe-paper-draft-citation/`
  The read-only citation finder; its siblings are `-values` and `-display`.
- `stages/5-section-edit/template.md`
  The placeholder rules, inline as drafting guidance.

## Law
DRAFT writes structure, prose and QUESTIONS. It never writes a fact it cannot source: not a bibtex entry, not a number, not a citation key it has not verified, and never an answer to its own question. The `.bib` is human-only; an agent greps it and never writes it.

Every unsourceable assertion becomes a marked hole with a named question beside it. The marker and the bracket sit side by side and are never fused, because a placeholder with no question is a hole nothing will ever fill.

A question raised is a product of this phase, not a failure of it. The finders report; the drafter holds the pen; the self-review runs in a fresh context and never replaces the human gate.

## Log
260726 · Rewritten from `_archive/QB3-draft.md`, which described the phase rather than asking anything, and `_archive/QB6-placeholders.md`, which described the grammar. Both are DRAFT's problem and the fork is the same in each: the cases the grammar cannot see.
