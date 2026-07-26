# REVISE: turning a landed answer into a sentence
state: 🟡 PARTIAL
owner: JL
method: substitute only what has landed, change the prose directly, and leave a why-comment for every change

## Question
Once an answer comes back, who puts it into the sentence, and how does a human later tell what changed and why? REVISE is the only phase that rewrites prose a person has already read, which makes it the phase most likely to be distrusted. If a reader cannot see what an agent altered, the safe response is to re-read everything, and the phase has cost more than it saved.

It is also the phase that discharges placeholders, and that is where it can do real damage: substituting a number whose answer has not actually landed turns a visible hole into an invisible fabrication. The order of operations matters more here than anywhere else in the lifecycle.

The approach is a chain with substitution first and a comment for every edit: `place` puts landed answers where the brackets were and refuses to touch the rest, then the prose workers rewrite, and each leaves a `%%` why-comment. What we want is a phase that can run unattended and still be auditable in one pass, because a human at CHECK reads the comments rather than the diff.

## Boundary
- ✅ Covered here
  The four revise workers, why `place` runs first, what may be discharged, and why the phase is unattended.
- ↪ Covered elsewhere
  The placeholder grammar it discharges is `QB6`; where the answer came from is `QB4`; the human who reads the why-comments is `QB8`; the sentence-level attachments it must not break are the `QC` series.

## Diagram
```
   REVISE                                        runs UNATTENDED

    1  place        ◀── RUNS FIRST, and this order is not a preference
       │               for every placeholder whose answer HAS LANDED:
       │                 \cite{TOADD} [Q-X-n]  →  \citep{realkey}
       │                 {VAL:? …}    [Q-X-n]  →  the number
       │                 a done DR row         →  \input + \ref
       │               and for every one that has NOT landed:
       │                 LEAVE IT, and FLAG it.
       │               never verifies · never searches · never invents
       ▼
    2  content      section → paragraph → weave → sentence
       │            the ¶-to-¶ arc, hinges, rhythm
       ▼
    3  humanizer    removes AI tells; keeps evidence-tied claims
       ▼
    4  results      results prose specifically

    every worker leaves     %% {CC-place}:   why this changed
                            %% {CC-content}: …
                            %% {CC-humanizer}: …

                                  │
                                  ▼
                            CHECK reads the COMMENTS, not the diff
                            → QB8, the one human gate in the stage

   ── why place must be first ──────────────────────────────────────
      if the prose workers run first, they rewrite the sentence AROUND
      a placeholder, and the substitution then lands in a sentence
      nobody wrote deliberately. Worse, a rewritten sentence may no
      longer contain the bracket at all, and the answer has nowhere
      to go.

   ── the failure this phase must never have ───────────────────────
      discharging a bracket whose answer has NOT landed. That turns a
      visible hole into an invisible claim, which is the one defect
      the whole placeholder grammar exists to prevent.
```

## Content
### Unattended, and why that is safe
REVISE changes prose without asking, which sounds like the least safe thing in the lifecycle and is not. It cannot spend, it cannot fetch, and it cannot assert: everything it writes either came from a landed answer or is a rephrasing of what was already there. The one gate in the stage sits after it, at CHECK, where a human reads the accumulated why-comments in one pass.

That is the trade the design makes. Gating REVISE would double the human's cost per stage and catch nothing that CHECK does not catch, because nothing REVISE does is irreversible or unlogged.

### The why-comment is the interface
```
 %% {CC-place}:      substituted \citep{kim2019} for TOADD; answer
                     landed in PP03/QX2, verified 260726
 %% {CC-content}:    split the ¶; the second claim had no hinge
 %% {CC-humanizer}:  "it is important to note that" removed
```
Without these, a human at CHECK has to diff prose against prose and reconstruct intent. With them, the phase's whole output is readable as a list of decisions. This is why a REVISE worker that edits without commenting is a defect and not a tidy one.

### What it may never discharge
A bracket whose answer has not landed stays exactly as it is, and gets flagged. `place` is explicitly forbidden from verifying, searching or inventing: it is a substitution worker, and everything it substitutes must already exist somewhere it can read.

## Items to Finish
- [x] 📐 `place` runs first, and the reason is stated
      Prose rewritten around a placeholder loses the bracket the answer needs.
- [x] 🗣 Every worker leaves a why-comment
      `%% {CC-*}:` per change, so CHECK reads decisions rather than a diff.
- [x] 🚫 A bracket without a landed answer is never discharged
      `place` never verifies, never searches, never invents.
- [ ] 🧠 Rule what REVISE does when a landed answer CONTRADICTS the prose
      Today it substitutes. If the number came back different in kind, not just in value, the sentence around it may now be false, and nothing says whether that is REVISE's problem or a reopened DRAFT.
- [ ] 🔍 Detect an edit with no why-comment
      The rule is stated in three worker contracts and enforced nowhere.
- [ ] 🧪 One section, revised, read at CHECK from the comments alone
      The acceptance test for the whole phase: can a human accept or reject each change without reading the previous version?

## Where we are
The four workers exist and the chain order is implemented, with `place` first. The why-comment convention is stated in each worker's contract and used on the MISQ paper.

Two gaps, both about trust rather than mechanism. Nothing checks that an edit carried a comment, and nothing says what happens when a landed answer makes its own sentence wrong.

## Files
- `2-phase/2-revise/haipipe-paper-revise/`
  The chain that dispatches the four.
- `2-phase/2-revise/haipipe-paper-revise-place/`
  The substitution worker that runs first and refuses to do anything else.
- `2-phase/2-revise/haipipe-paper-revise-content/`
  Section, paragraph, weave, sentence; its siblings are `-humanizer` and `-results`.

## Law
REVISE runs unattended because it cannot spend, cannot fetch and cannot assert. Everything it writes is either a landed answer or a rephrasing of what was already there.

`place` runs FIRST. It substitutes only placeholders whose answers have landed, leaves and flags every other, and never verifies, searches or invents. Discharging a bracket whose answer has not landed turns a visible hole into an invisible claim and is the one defect this phase must never have.

Every worker leaves a `%%` why-comment for every change. The human at CHECK reads the comments, not the diff; an edit without a comment is a defect.

## Log
260726 · Created, for the same reason as `QB3`. Its central ruling, that `place` runs first, was implemented and written down nowhere.
