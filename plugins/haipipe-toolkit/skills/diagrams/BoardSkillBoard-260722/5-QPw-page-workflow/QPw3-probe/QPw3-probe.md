# Probe: turn each mark into a card, look for the answer that already exists, then ask
state: 🟡 IN PROGRESS · the phase ships at 0.3.0; the MATCH order has no checker · open: 6
owner: CC
method: settle who creates the card and when, then state the lookup that must run before any question is dispatched; every rule names the count that catches its failure
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
Before a page pays for a new answer, has somebody already answered this, and if not, who gets asked?

PROBE is phase ③ and the ONLY phase that creates an evidence card: it turns each bare mark left by the approved plan into a real folder at `<page>/probe/PP<NN>-<slug>/`, writes the stake-bearing Q-consumer and the stripped Q-executor, points the card back at the bullets it serves, and dispatches.
It ends the moment the question leaves, which is exactly where `QPw4` begins, and that split is what stopped four cards from sitting bound to a QA bank that did not exist while the page read as done.
Its first act is not asking but LOOKING: a four-step MATCH order runs before any dispatch, because reuse is cheap and a new question is not.
The card cannot be created earlier than this phase for one practical reason: its `consumer/` side carries the stake, the stake is an Aim, and Aims are written at DRAFT.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every rule names the COUNT that catches its failure**: declaring a card is free, so a rule with no count behind it cannot be enforced.
The receipt's `coverage` line is the model: it reports how many marked bullets actually got a card, and a gap stops the phase rather than reporting it.

**The link direction is stated every time it is mentioned**: the card knows the bullet and the bullet knows nothing about the card.
Any sentence implying the plan is edited to point at a card is wrong, because the plan is frozen before a card exists.

**The plugin owns the folder, this page owns the timing**: when this page and `QPf9` disagree about the folder, its four counts, or its state ladder, the plugin wins and this page is wrong.
Say the state words only as a set and never redefine one.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The mark becoming a card, the lookup that runs first, and the wall the question crosses.

```text
📮 PROBE · phase ③ of 7 · the ONLY phase that creates a card
                approved plan, frozen, never edited here
                     - B4 · the four coordinates      🔢
                                  │
        ┌─────────── MATCH, in this order ────────────┐
        │ 1. this page's own cards and bibex           │
        │ 2. PageX borrowed files + the source page's  │ reuse is cheap
        │    live material                             │ a new question
        │ 3. the task/discovery QA bank, by reading    │ is not
        │    one specific answer                       │
        │ 4. only then: a new card, and dispatch       │
        └──────────────────────┬───────────────────────┘
                               ▼
              <page>/probe/PP<NN>-<slug>/
              ├── consumer/   Q-consumer + THE STAKE     🚫 never crosses
              ├── executor/   the stripped Q-executor    ✅ only this is sent
              ├── proof/      manifest.yaml · files: []  EVIDENCE pulls into it
              └── card.md     serves: C4.P1.B4 · C3.P1.B3
                              state: planned → commissioned
                                  │
                    the clean context IS the wall
                                  ▼
              haipipe-task-orchestrator-agent      work the task layer owns
              haipipe-discovery-orchestrator-agent work the literature owns
                                  │
                    what comes back is a PATH to a QA file,
                    and binding that path is ④ EVIDENCE's
```
📌 The link runs BACKWARD: `card.md` names the bullets, and the plan is never rewritten to name the card.

## Content

### 1 · PROBE is the only phase that creates a card
**The ownership rule**: three phases hold something about a hole and only the third may open a file for it.

```text
phase       holds about the hole              why it may not create the card
────────────────────────────────────────────────────────────────────────────
① OUTLINE   the MARK, bare, no id             a plan is rejectable in ten
                                              seconds and a rejected plan must
                                              leave NOTHING on disk: a card for
                                              an unapproved plan is litter
                                              with an id
② DRAFT     the AIM the hole belongs to       the mark IS the proposal, so a
                                              second file saying the same thing
                                              is the duplication rule
③ PROBE     the CARD                          ← here
```
📌 The deciding reason is practical rather than tidy: the card's `consumer/` side carries the stake, the stake is an Aim, and Aims do not exist until DRAFT ends.

#### 1.1 · Three skills answered this three ways until 260817
(`haipipe-page-draft` §🃏 said DRAFT creates it OWED, `haipipe-page-evidence` §🧾 said it may arrive PROPOSED, `haipipe-plugin-outline` §📐 said PROBE creates it)
JL asked the question outright: who should do the proof, and is that DRAFT's work or OUTLINE's.
It was ruled PROBE on the stake argument, and PROBE got its own contract instead of borrowing EVIDENCE's.
The three contradicting sentences were then corrected in all three files rather than left to whichever one a reader happened to load.

#### 1.2 · Two smaller consequences fall out of the same order
(a frozen address, and an honest count)
The plan's address is frozen by the `approved:` tick before any card points at it, so `serves: C4.P1.B4` can never name a bullet that was renumbered afterwards.
The card count starts honest: `6 serve · 0 answered` on the 🧭 tab is a true reading of a page nobody has dispatched yet, rather than an artefact of cards created too early.

### 2 · One mark is not one card
**The matching rule**: the plan marks what a SENTENCE owes and a card is what a BANK can answer, and this phase is where those two units are matched.

```text
many bullets ─▶ one card    the usual case. PP04 on QC1-visitlbp serves
                            C3.P1.B3 · C3.P3.B3 · C7.P2.B1, because all
                            three are answered by reading one script.
one bullet  ─▶ many cards   legal. B4 may owe both a coefficient and the
                            N behind it, from two different runs.
a mark      ─▶ no card      only when a card already serving another
                            bullet answers it too. add the address to
                            that card's `serves:`, never open a second.
```
📌 A question is asked ONCE, and a duplicate card is the exact failure the id exists to prevent.

#### 2.1 · A bullet reads as done only when EVERY card in its backlink has landed
(`answered`, `answered-local`, or `read`, and never when any one of them has)
One number landed while one question stays open is not an answered bullet, and a reader who sees a filled sentence cannot tell the difference.
So the test is over the whole backlink, which is why the link is stored on the card rather than counted per bullet.

### 3 · MATCH runs before any dispatch, and PageX is reuse rather than a second bank
**The lookup rule**: four steps in order, and step 4 is reached only after the nearest existing answer has been read and rejected.

```text
1. this page's own cards and bibex
2. PageX borrowed files, plus the source page's live material
3. the task or discovery QA bank, by reading one specific answer
4. only then: create a new card and dispatch

record it: match: PP03 · PageX/QC0-results/probe/PP02/card.md · reuse
           match: B4   · no exact PageX/QA answer · new → dispatched
```
📌 This is the smoothness rule: reuse is cheap and visible, and a new probe is expensive and must be justified in the receipt.

#### 3.1 · A shortlist entry is never evidence by itself
(`POST /_board/pagex-match` produces a candidate list whose overlap score is navigation only)
PROBE must open the candidate and may record `reuse` only when the neutral Q-executor is LITERALLY answered by it.
A topic-similar file is a candidate and nothing more, and when it does not answer the question the honest verdict stays `bank: new|run|code`.

### 4 · Only some marks are questions
**The mark rule**: the plan carries six marks and this phase acts on one and a half of them.

```text
mark          PROBE creates                    why
──────────────────────────────────────────────────────────────────────────
🔢 value      a card, always                    this is the phase
📚 citation   a card ONLY when the key is       a known key is landed by a
              UNKNOWN and the bank must         PERSON into bibex/ and needs
              find the work                     no question asked
🖼 display    NOTHING                           its intake/ freezes from a
                                                proof/ that does not exist
                                                yet: EVIDENCE creates it
🧮 proof      NOTHING                           not a card kind: a proof is
                                                prose resting on a pulled
                                                file inside a card's proof/
🎯 aim        NOTHING                           DRAFT's, tracked in States
✅ have it    NOTHING                           already true
```
📌 A page whose plan carries only 🎯 and ✅ marks skips PROBE entirely, and that is the phase being unnecessary rather than being skipped.

### 5 · Exit, routing, and the count that stops the phase
**The coverage rule**: the phase exits when every marked bullet is served by at least one card, and a gap is a HOLD rather than a pass.

```text
every marked bullet served, every card planned  ─▶ ④ EVIDENCE
the bank already answered this question         ─▶ point at it; still EVIDENCE
no route can answer it                          ─▶ HOLD, named, with a reason
the plan owes the wrong thing                   ─▶ ① OUTLINE, a v2, never a
                                                   quiet edit here

receipt line that catches the failure mode:
coverage: <n> of <n> marked bullets served    🚫 a gap is a HOLD, not a pass
```
📌 PROBE never routes to REVISE, because a card that was opened and never landed supports no sentence.

#### 5.1 · Declaring a card is free, which is why the receipt counts creations
(a phase whose declared and created counts disagree stops rather than reports)
This is the same rule that made "1 display declared, 0 unit folders on disk" a stopping condition rather than a note.
`QPw00 §🪞` carries it for every plugin in the loop, and `coverage` is this phase's instance of it.

## Aims

### Decision Now
- [ ] 🗣 Rule what PROBE does with a 📚 mark whose key is unknown but whose SOURCE is known
      📍 `Part` §4, only some marks are questions
      🔔 `Why now` the contract says a card is opened only when the bank must find the work, and it does not say which side of that line "I know the paper, I do not have the bibtex" falls on, which is the commonest case on this board
      ⭐ `A ·` no card: a person lands the entry into bibex/ verbatim, because the bibex law already forbids a machine composing bibtex and finding a known paper's entry is not bank work
      `B ·` a card, so the fetch is auditable and the receipt shows who supplied the entry, at the cost of a card that no bank actually answers
      🛑 `Blocks` A4.1, and the 📚 lane's exit test on QPw4
      🤖 `If nobody answers` A takes effect, because the bibex law already puts the entry in a person's hands


### A1 · 📮 PROBE is the only phase that creates a card
- ⬜ A1.1 · No card on this board exists for an unapproved plan.
  Done when every `probe/PP<NN>-<slug>/` on this board traces to an outline file carrying `approved: ✅`.
  **Now:** Not measurable yet, because no outline on this board carries `approved: ✅`.
- ✅ A1.2 · The three contradicting sentences from before 260817 are gone from all three contracts.
  Done when a grep of the draft, evidence, and outline-plugin contracts finds one answer to who creates the card.
  **Now:** Met. The 260817 round corrected all three contracts and `haipipe-page-probe` shipped as the single answer.


### A2 · 🔢 One mark is not one card
- ⬜ A2.1 · No two cards on this board carry the same Q-executor.
  Done when a sweep of `executor/` across this board finds no duplicate question.
  **Now:** Not measured. No sweep of `executor/` for duplicate questions has been run.
- ⬜ A2.2 · A bullet's done test reads its whole backlink rather than any one card.
  Done when a checker fails a bullet marked done while one card in its `serves:` set is unlanded.
  **Now:** Not started. No checker reads a bullet's backlink as a set.


### A3 · 🔗 MATCH runs before any dispatch, and PageX is reuse rather than a second bank
- ⬜ A3.1 · Every dispatched card's receipt carries its match trace.
  Done when every PROBE receipt under `_runs/page/` has one `match:` row per obligation.
  **Now:** Not started. The MATCH order shipped in 0.3.0 on 260817 and no receipt on this board carries a `match:` row.
- ⬜ A3.2 · No `reuse` verdict was recorded from a shortlist score alone.
  Done when every `reuse` row names an opened candidate file rather than a match endpoint response.
  **Now:** Not measurable until A3.1 produces a trace to read.


### A4 · 🧭 Only some marks are questions
- 🧠 A4.1 · No card on this board was opened for a 🖼, 🧮, 🎯, or ✅ mark.
  Done when every card on this board traces to a 🔢 mark or to a 📚 mark whose key was unknown.
  **Now:** Waiting on the Decision Now row above, which decides one of the two card-opening conditions.


### A5 · 🔀 Exit, routing, and the count that stops the phase
- ⬜ A5.1 · No PROBE run has reported a pass while its coverage was short.
  Done when every PROBE receipt with `coverage` below full carries `next: HOLD`.
  **Now:** Not measurable yet, because no PROBE run has been dispatched from this board.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-probe/SKILL.md`
  The phase contract itself, at 0.3.0, and the authority on its procedure.
- `page-plugins/haipipe-plugin-probe/SKILL.md`
  The folder's shape, its four counts, and its state ladder. It wins over this page on all three.
- `../probe/haipipe-probe/SKILL.md`
  The crossing protocol: stake stripping, bank independence, and the four slot words.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw3-probe.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw2 §2](5-QPw-page-workflow/QPw2-draft/QPw2-draft.md)
  Where the stake is written, which is the reason this phase and not an earlier one creates the card.
- `continues · EVIDENCE` · [QPw4 §3](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The phase that begins the moment this one ends, and the owner of steps ④⑤⑥ of the shared loop.
- `reads · ALL` · [QPf9 §1](4-QPf-page-folder/QPf9-probe/QPf9-probe.md)
  The probe plugin's folder contract, its four counts, and its state ladder.
- `reads · ALL` · [QPf11 §1](4-QPf-page-folder/QPf11-pagex/QPf11-pagex.md)
  PageX, which is step 2 of the MATCH order and a reuse list rather than a second bank.

## Law
- 260817 JL · 📮 **The card is created at PROBE**: never at OUTLINE, never at DRAFT
  Three skills answered this three ways until JL asked outright whether the proof belongs to DRAFT or OUTLINE.
  The deciding reason is the stake: a card's `consumer/` side carries what the page loses, that is an Aim, and Aims are written at DRAFT, so PROBE is the earliest phase at which a complete card can exist.
  The option rejected was DRAFT creating it in an OWED state, which loses because no rule can reorder a stake that does not exist yet.
- 🔢 **A question is asked ONCE**: many bullets may share one card and a duplicate card is the failure the id prevents
  `PP04` on `QC1-visitlbp` serves three addresses because one script answers all three.
- ↩ **The link runs backward**: the card names the bullets and the plan is never rewritten
  The plan is frozen by the `approved:` tick before any card exists, which is what makes a `serves:` address permanently resolvable.
- 🔗 **A shortlist entry is never evidence**: `reuse` may be recorded only after the candidate has been opened and literally answers the Q-executor
  The match endpoint's overlap score is navigation, and a topic-similar file leaves the honest verdict at new work.
- 🛑 **A coverage gap is a HOLD, not a pass**: declaring a card is free, so the receipt counts what was actually created
  A phase whose declared and created counts disagree stops rather than reports.

## Glossary
- 📮 **card**: the folder at `<page>/probe/PP<NN>-<slug>/` holding one question, allocated `PP<NN>` on its page and never reused.
- ↩ **serves:**: the card's backward link naming every plan address it answers.
- 🔗 **MATCH**: the four-step lookup that must run before any new question is dispatched.
- 🧱 **the wall**: the path boundary between `consumer/` and `executor/`, enforced by dispatching into a clean context that never sees the stake.
- 🛑 **coverage**: the receipt line reporting how many marked bullets actually got a card.

## Log
- 260818 · [DRAFT-CC] page created to complete the loop after `QPw1`, `QPw2` and `QPw4`, which had left this phase with no page while two of them linked to it. Written from `haipipe-page-probe` 0.3.0. Five divisions: who creates the card and why not earlier, the mark-to-card matching, the MATCH order with PageX as step 2, which of the six marks are questions, and the coverage count that stops the phase. The 260817 ruling that settled three contradicting contracts is carried as the first `## Law` row with its rejected option named. One real gap in the contract became the Decision Now row: it says a 📚 card opens when the bank must find the work, and never says which side of that line a known paper with an unknown bibtex key falls on, which is the commonest case here.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0