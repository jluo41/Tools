# REVISE · When may it change a sentence a human has already read?
state: 🟡 PARTIAL
owner: JL
method: substitute only what has landed, run place first, and leave a why-comment for every change

## Question
REVISE is the only phase that rewrites prose a person has already read, and it does it without asking. That makes it the phase most likely to be distrusted, and distrust here is expensive in a specific way: if a reader cannot see what an agent altered, the only safe response is to re-read everything, and at that point the phase has cost more than it saved.

It is also the phase that discharges placeholders, which is where it can do real damage. Substituting a value whose answer has not actually landed turns a visible hole into an invisible claim, and that single failure would defeat the entire placeholder grammar. It is the reason the chain has a fixed order: `place` runs first, before any prose worker touches the sentence, because a rewritten sentence may no longer contain the bracket the answer needs.

What is unresolved is the case where the answer arrives and disagrees with its own sentence. Today `place` substitutes the number and stops. If the answer came back different in kind rather than merely different in value, the sentence around it may now be false, and nothing says whether repairing that is REVISE's job or a reopened DRAFT.

## Boundary
- ✅ Covered here
  The four revise workers, why `place` runs first, what may be discharged, and why the phase is unattended.
- ↪ Covered elsewhere
  The placeholder grammar it discharges is `QB8`; where the answer came from is `QB9`; the human who reads its comments is `QB11`; whether a stage may omit this phase is `QB7`.

## Diagram
```
   ♻️ REVISE                                      runs UNATTENDED

    1  place        ◀── RUNS FIRST, and this is not a preference
       │
       │   for every placeholder whose answer HAS LANDED:
       │     \cite{TOADD} [Q-X-n]  ──▶  \citep{realkey}
       │     {VAL:? …}    [Q-X-n]  ──▶  the number
       │     a done DR row         ──▶  \input + \ref
       │
       │   for every one that has NOT:
       │     LEAVE IT, and FLAG it.
       │
       │   never verifies · never searches · never invents
       ▼
    2  content      section → paragraph → weave → sentence
       │            the ¶-to-¶ arc, hinges, rhythm
       ▼
    3  humanizer    removes AI tells; keeps evidence-tied claims
       ▼
    4  results      results prose specifically

    every worker leaves      %% {CC-place}:      why this changed
                             %% {CC-content}:    …
                             %% {CC-humanizer}:  …
                                  │
                                  ▼
                       CHECK reads the COMMENTS, not the diff   → QB11

   ── WHY `place` MUST BE FIRST ─────────────────────────────────────
      if a prose worker runs first it rewrites the sentence AROUND
      the placeholder, and the substitution then lands in a sentence
      nobody wrote deliberately. Worse, a rewritten sentence may no
      longer contain the bracket at all, and the answer has nowhere
      to go.

   ── THE ONE FAILURE THIS PHASE MUST NEVER HAVE ────────────────────
      discharging a bracket whose answer has NOT landed.
      that turns a visible hole into an invisible claim, which is the
      exact defect the whole placeholder grammar exists to prevent.

   ── THE WHY-COMMENT IS THE INTERFACE ──────────────────────────────
      %% {CC-place}:      substituted \citep{kim2019} for TOADD;
                          answer landed in PP03/QX2, verified 260726
      %% {CC-content}:    split the ¶; the second claim had no hinge
      %% {CC-humanizer}:  "it is important to note that" removed

      without these a human at CHECK must diff prose against prose
      and reconstruct intent. With them the phase's whole output
      reads as a LIST OF DECISIONS. A worker that edits without
      commenting is a defect, and not a tidy one.

   ── THE OPEN CASE ─────────────────────────────────────────────────
      the landed answer CONTRADICTS its own sentence.
        the value came back different in KIND, not just in value
        `place` substitutes it and stops
        the sentence around it may now be FALSE
      ❓ REVISE's problem, or a reopened DRAFT? Nothing says.

   ── one stage skips this phase entirely ───────────────────────────
      2a-venue declares [draft, probe, check].               → QB7
      it produces a recommendation, not prose. Probably right,
      and stated nowhere.
```

## Content
### Unattended, and why that is the cheaper trade
REVISE changes prose without asking, which sounds like the least safe thing in the lifecycle and is not. It cannot spend, it cannot fetch and it cannot assert: everything it writes either came from a landed answer or is a rephrasing of what was already there. The one gate in the stage sits after it, where a human reads the accumulated why-comments in a single pass.

Gating REVISE would double the human's cost per stage and catch nothing CHECK does not catch, because nothing REVISE does is irreversible or unlogged. That is the whole argument, and it depends entirely on the comments actually being written.

### What it may never discharge
A bracket whose answer has not landed stays exactly as it is and gets flagged. `place` is explicitly forbidden from verifying, searching or inventing: it is a substitution worker, and everything it substitutes must already exist somewhere it can read. The forbidding matters more than it sounds, because a worker that is allowed to check would eventually be allowed to conclude.

### The rule everything rests on, enforced nowhere
The why-comment convention is stated in three worker contracts and checked by nothing. If a worker stops commenting, the failure is silent and the symptom appears at the gate as a human who cannot tell what changed, which reads like the human's problem rather than the worker's.

## Items to Finish
- [x] 📐 `place` runs first, and the reason is stated
      Prose rewritten around a placeholder loses the bracket the answer needs.
- [x] 🗣 Every worker leaves a why-comment
      `%% {CC-*}:` per change, so CHECK reads decisions rather than a diff.
- [x] 🚫 A bracket without a landed answer is never discharged
      `place` never verifies, never searches, never invents.
- [ ] 🧠 Rule what REVISE does when a landed answer CONTRADICTS its sentence
      Today it substitutes. If the answer differs in kind rather than in value, the sentence may now be false, and nothing says whether that is REVISE's problem or a reopened DRAFT.
- [ ] 🔍 Detect an edit with no why-comment
      Stated in three worker contracts, enforced nowhere.
- [ ] 🧪 Read one revised section at CHECK from the comments alone
      The acceptance test for the whole phase: can a human accept or reject each change without reading the previous version?

## Where we are
The four workers exist, the chain order is implemented with `place` first, and the why-comment convention is used on the MISQ paper. The phase does what it says.

Two gaps, both about trust rather than mechanism. Nothing checks that an edit carried a comment, and nothing says what happens when a landed answer makes its own sentence wrong.

## Files
- `2-phase/2-revise/haipipe-paper-revise/`
  The chain that dispatches the four, in order.
- `2-phase/2-revise/haipipe-paper-revise-place/`
  The substitution worker that runs first and refuses to do anything else.
- `2-phase/2-revise/haipipe-paper-revise-content/`
  Section, paragraph, weave, sentence; its siblings are `-humanizer` and `-results`.

## Law
REVISE runs unattended because it cannot spend, cannot fetch and cannot assert. Everything it writes is either a landed answer or a rephrasing of what was already there.

`place` runs FIRST. It substitutes only placeholders whose answers have landed, leaves and flags every other, and never verifies, searches or invents. Discharging a bracket whose answer has not landed turns a visible hole into an invisible claim, and is the one defect this phase must never have.

Every worker leaves a `%%` why-comment for every change. The human at CHECK reads the comments, not the diff; an edit without a comment is a defect.

## Log
260726 · Carried from `_archive/QB7-revise.md` and retitled to the fork rather than the phase name. The live question is the permission, not the procedure: this is the only phase that rewrites prose a person has already read.
