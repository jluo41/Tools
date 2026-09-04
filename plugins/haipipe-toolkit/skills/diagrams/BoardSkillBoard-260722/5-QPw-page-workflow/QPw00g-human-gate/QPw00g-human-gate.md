# The human gate: the five ticks a machine may never write, and the surface that does not exist yet
state: 🟡 PARTIAL · 4 of 5 ticks move to a rule-bound agent; the RULING and the 🛑 stay a person's · open: 5
owner: CC
method: collect every tick the contracts already reserve for a person, prove each is reserved by naming the file that reserves it, then rule where the surface lives; a tick a machine can fake is a defect
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
Where does a person actually sign off on a page, and can they do it in one place?

Five ticks on this board are reserved for a person and no machine may write any of them: `approved:` on an outline, `verified` on each bibex entry, `read:` on each probe card, `accepted: ✅` on each display unit, and the ruling a Page Type requires at CHECK.
They are defined, they are enforced, and they live in three different phases and N different files, so there is no single surface a person opens to do all of them.
JL ruled this page LAST of the group on 260818 and ruled the gate ACCEPT-BIASED: a person is asked to sign only after the machine's computed findings are all zero, so the gate is a confirmation rather than an inspection.
The bias changes what is PRESENTED and never who writes the tick, because silence is not consent and a required gate with no durable evidence still routes to HOLD.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every tick names the file that reserves it**: a claim that something is a human gate is worthless without the contract line that forbids the machine.
Quote the reserving rule, not a summary of it.

**The machine half and the human half are always drawn as two columns**: this page's whole subject is the boundary between them, so any figure that mixes them has lost the point.
Eight findings are computed and five ticks are written, and those numbers belong side by side.

**Accept-bias is about PRESENTATION, and the page must say so every time**: a sentence that lets the bias touch who writes the tick is a defect, not a shortening.
The one line that may never move is that silence is never consent.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
Eight computed findings on one side, five human ticks on the other, and nothing joining them yet.

```text
✋ THE HUMAN GATE · phase-independent · LAST of the QPw group by JL's 260818 ruling

🤖 MACHINE, deterministic                    ✋ YOU, and only you
   src/page_evidence.py · cli/check.py
   ─────────────────────────────────────      ──────────────────────────────────
   display-declared-no-claim                  `approved:`
   display-declared-not-rendered                on outline/<stem>-outline-v<N>.md
   display-intake-unfrozen                      at 🧭 OUTLINE · QPw1
   display-cited-not-embedded
   display-rendered-not-cited                 `verified`
   display-accept-stale                         per bibex/<stem>.bib entry
   latex-untitled                               at 🃏 EVIDENCE · QPw4
   projection-stale
                                              `accepted: ✅`
   plus the three INDEPENDENT counts            per display/<unit>/README.md
     declared ≠ rendered ≠ accepted             at ✅ CHECK step ⑤ · QPw6
     and only the third is yours
                                              the Page Type's RULING
                                                at ✅ CHECK · QPw6

⛔ THE HOLE: 4 ticks · 3 phases · N files · 0 surfaces
   and the .pdf and .docx a reader opens have machine findings
   but NO human tick of their own at all

✅ ACCEPT-BIAS, ruled 260818          ⛔ WHAT IT MAY NEVER CHANGE
   the gate opens only when the          silence ≠ consent
   computed findings are ZERO            a required gate with no durable
   one surface, pre-filled                 evidence still routes to HOLD
   yes is the EXPECTED answer            otherwise the machine approves
   confirmation, not inspection            itself by timeout
```
📌 The receipt's `human_gate` field is a POINTER carrying `{required, status, evidence}`; it records that a gate was satisfied and where to look, and never holds the approval.

## Content

### 1 · Five ticks, and the contract line that reserves each one
**The reservation rule**: each tick is forbidden to a machine by a named rule, not by convention.

```text
tick             where it lives                    what reserves it
──────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<N>.md    "No machine may write that
                                                   tick, for the same reason no
                                                   machine accepts a display
                                                   render" · haipipe-page-outline
`verified`       per entry in bibex/<stem>.bib     the bibex law: a machine may
                                                   SUBSET or TRANSCRIBE bibtex,
                                                   never COMPOSE it · ruled 260815
`read:`          per probe/PP<NN>-<slug>/card.md   "Only a person may tick it, and
                                                   a changed `target` or a
                                                   re-pulled `proof/` drops the
                                                   tick back" · haipipe-plugin-probe
`accepted: ✅`   per display/<unit>/README.md      "CHECK never ticks it and never
                                                   reports a unit as accepted
                                                   because it looks finished"
                                                   · haipipe-page-check
the RULING       the Page Type's declared gate     a machine "may never claim that
                                                   a person approved a Page when
                                                   no person did" · same file
```
📌 All five share one property: a machine may compute everything around them and may not write them.

#### 1.1 · `approved:` is the only exit its phase has
(OUTLINE cannot be completed any other way)
The phase's whole output fits on one screen and a person can reject it in ten seconds, which is the argument for the gate being there at all.
What the tick judges is whether this is the RIGHT plan, and no mechanical check reaches that question.

#### 1.2 · TWO of the five go BACKWARD, and that is what keeps them out of the receipt
(`accepted: ✅` when `intake/` changes, which is the `display-accept-stale` finding; `read:` when the card's `target` or `proof/` changes)
This is what makes the five ticks unstorable in a receipt: receipts are an append-only chain and a tick that can revert cannot live in one.
The other three stand until a person moves them, so the reverting pair is the reason the whole set lives in its artifacts instead.
`QPw00r §3` carries the invariant behind that, and the seam is written as `## Law` on both pages so neither can absorb the other by accident.

### 2 · The surface does not exist: five ticks, three phases, N files
**The dispersion rule**: nothing today collects them, so a page can ship with two ticks missing and no reader is told.

```text
today a person must open
  the outline file                            1 file
  the bib file, and find each entry           1 file · N entries
  every probe card                            N files
  every display unit's README                 N files
  whatever review surface the Page Type names 1 more

and no single count anywhere says "2 of 5 ticked"
```
📌 The machine half is already deterministic and complete: eight findings computed by `src/page_evidence.py` and reported by `cli/check.py`.

#### 2.1 · Declared, rendered, and accepted are three independent counts
(and only the third is a person's)
Declared means the unit folder exists, rendered means a winning asset and `preview.pdf` both exist, accepted means a person ticked the README.
A version whose declared count exceeds its rendered count does not pass, so the machine can and does gate the first two without touching the third.
Folder count is never completed work.

#### 2.2 · What this surface must NOT become
(a second store)
The ticks stay where they are, in the artifacts that own them, and the surface reads and writes through to those files.
A surface holding its own copy of the tick would immediately drift from the artifact, and the drift would be invisible in exactly the direction that matters.

### 3 · The built deliverable has no tick of its own
**The gap rule**: the PDF and the docx a reader opens carry machine findings and no human sign-off.

```text
what the machine says about them
  latex-untitled       the .tex carries no title block from the page's own H1
  projection-stale     the .tex or .docx is older than the source it projects

what a person says about them
  nothing. there is no field.
```
📌 This is the one part of the gate that is a genuine hole rather than a dispersion problem: all five ticks exist on some artifact and this sixth surface has never been named.

#### 3.1 · The three live projection-stale findings show why it matters
(`QPf5-display` for both its `.tex` and its `.docx`, and `QPw00-page-loop` for its `.tex`)
Each means the source moved and the deliverable did not, and a machine can say that much.
What a machine cannot say is whether the rebuilt file reads correctly, which is precisely the judgment a tick would carry.

### 4 · Accept-bias changes what is shown and never who writes
**The bias rule**: JL 260818, "human should be more likely to accept it".

```text
✅ WHAT THE BIAS CHANGES
   the gate opens only when mechanical_errors is ZERO, so nobody is asked to
   accept a display that never rendered or a PDF with no title block
   one surface, pre-filled, five ticks in one place instead of N files
   yes is the expected answer, so the gate is a CONFIRMATION not an inspection

⛔ WHAT IT MAY NEVER CHANGE
   silence is not consent
   a required gate with no durable evidence still routes to HOLD
   otherwise the machine approves itself by timeout, which is the same thing
   the receipts page forbids for the same reason
```
📌 So the bias is a scheduling rule about when a person is interrupted, and the writer of every tick is unchanged.

#### 4.1 · The gate is a confirmation because the machine did the hunting
(eight findings cleared before the interruption, not after it)
The cost of a gate is not the tick, it is the search a person performs to decide whether to write it.
Moving that search onto the machine is what makes yes the likely answer, and it is the only lever available that does not touch the tick itself.

### 5 · Where this gate lives, and why it is last
**The placement rule**: it spans three phases, so no single phase page can own it.

```text
QPw1 OUTLINE   owns `approved:`
QPw4 EVIDENCE  owns `verified`
QPw6 CHECK     owns `accepted: ✅` and the Page Type's ruling
QPw00r RECEIPTS  can only POINT at all five, never hold them

→ the gate is the LAST page of the group because it is what every earlier
  page's work finally reaches, and because the receipt that records it must
  already exist before there is anything to record
```
📌 JL ruled the order on 260818: receipts at `QPw00r` and the gate at `QPw00g`, reversing an earlier draft that had them the other way round.

### 6 · A person's job is to BREAK, not to approve
**The cut rule**: a rule that survives being WRITTEN DOWN belongs to an agent, and a judgment RE-MADE every time belongs to the person whose intent it depends on (JL 260818: "human not to approve, they to break").

```text
                🤖 AGENT rule                🧑 HUMAN break
──────────────────────────────────────────────────────────────────────
scope           LOCAL: this axis label,      WHOLE: only visible looking
                this DOI, this button        at all of it at once
right answer?   YES, independent of intent   NO, it depends on intent
write it down?  ✅ survives forever          ❌ dies; tomorrow may differ
                                             with nothing on disk changed
output          a VERDICT, pass or fail      a PROPOSAL, do it differently
```
📌 So four of the five ticks move to `haipipe-board-approver-agent`, which passes by DEFAULT against `agents/approve-rules/<kind>-rules.md`; the RULING stays a person's, and so does the 🛑 on any of the other four.

#### 6.1 · This session is the measurement, not an argument for it
(six interventions on 260818, and not one of them was a mechanical check)
JL asked what 7, 8 and 9 were and ruled they may not carry phase numbers; he asked what `fig` was and ruled a figure belongs to display; he ruled `QPw4` into three lane faces; he ruled the display is an evidence card; he ruled the human is a brake.
Every one is a whole-artifact judgment that depends on what he wants the board to be, and none of them could have been written as a rule the day before.
Meanwhile the four errors the checker found the same day were all local, all rule-shaped, and none of them needed him.

#### 6.2 · The default flips, and that is what makes it cheap
(pass unless a rule fails; a 🛑 arrives afterwards and REVERTS the tick)
A blocking gate cost every artifact a wait on one reader, and this board has five ticks across N files with no surface joining them, which is `§2`.
An accept-by-default gate costs one re-plan when a person breaks something, and nothing at all when they do not.
The line that does not move is the one `§4` already holds: silence is never consent for the RULING, which no agent may write at any confidence.

#### 6.3 · Every break becomes a rule, in the person's own words
(`promoted <YYMMDD> from <who>'s break on <what>`, appended at the bottom, never renumbered)
The approver transcribes a 🛑 into the matching rules file when the reason can be written so it never needs judging again, and reports it as a steer when it cannot.
`approve-rules/approve-rules.md` R8 already carries one, promoted from a break on this group's own outline: never delete the ONLY place a rule is written, even when the surrounding division is being shrunk.
A rule whose origin is lost is a rule nobody can argue with later, so the stamp is part of the rule.


## Aims

### Decision Now
- [ ] 🗣 Rule whether the built PDF and docx get a human tick of their own
      📍 `Part` §3, the built deliverable has no tick of its own
      🔔 `Why now` all five ticks exist and no surface joins them, while `projection-stale` fires on three artifacts on this board today and no person has ever signed one off
      ⭐ `A ·` no new tick: the display unit's `accepted: ✅` plus a zero `projection-stale` count already means every accepted unit reached the built file, so a separate signature would be a second copy of a decision already made
      `B ·` a `released:` tick per projection, which is the only thing that captures "I opened the PDF and it reads correctly", at the cost of a sixth tick on a page whose whole complaint is that five are already scattered
      🛑 `Blocks` A3.1, and the surface's field list in A2.1
      🤖 `If nobody answers` A takes effect, because it adds no tick and the counts it relies on already exist


### A1 · ✋ Five ticks, and the contract line that reserves each one
- ✅ A1.1 · Each of the five names the contract line that forbids the machine.
  Done when all five rows carry a quoted reserving rule rather than a paraphrase.
  **Now:** Met. All five rows in `§1` carry their reserving rule from `haipipe-page-outline`, the bibex law, `haipipe-plugin-probe`, and `haipipe-page-check`.


### A2 · 🗂 The surface does not exist: five ticks, three phases, N files
- ⬜ A2.1 · One surface presents all five ticks for one page.
  Done when a person can read and write all five from one place, with the tick still stored in its owning artifact.
  **Now:** Not started. This is the page's whole reason for existing and nothing is built.
- ⬜ A2.2 · A count exists saying how many of a page's required ticks are done.
  Done when `cli/check.py` or the 🚪 strip reports `<n> of <n> ticked` per page.
  **Now:** Not started. No per-page tick count exists anywhere.


### A3 · 📄 The built deliverable has no tick of its own
- 🧠 A3.1 · The PDF and the docx have a named human sign-off or a written ruling that they need none.
  Done when either a tick field exists for the projections, or this page records the decision that machine findings suffice for them.
  **Now:** Waiting on the Decision Now row above.


### A4 · ✅ Accept-bias changes what is shown and never who writes
- ⬜ A4.1 · No gate is presented while any computed finding for that page is non-zero.
  Done when the surface refuses to open on a page with a live error.
  **Now:** Not started. The rule was ruled on 260818 and nothing presents a gate yet.
- ✅ A4.2 · No tick has ever been written by anything other than a person.
  Done when every tick on this board traces to a named person and a date.
  **Now:** Met so far, trivially: no tick exists anywhere on this board, so none has been faked.


### A5 · 🚪 Where this gate lives, and why it is last
- ✅ A5.1 · The seam against the receipts page is written on both pages.
  Done when `QPw00r` and this page each carry the rule that a receipt points at a tick and never holds one.
  **Now:** Met. The seam is a `## Law` row on this page and on `QPw00r`.


### A6 · 🛑 A person's job is to BREAK, not to approve
- 🔨 A6.1 · Four of the five ticks are passed by rule rather than by a person.
  Done when `haipipe-board-approver-agent` has written an `auto` pass on at least one artifact of each kind: outline, display, cite, value.
  **Now:** Being worked on now. The four rules files and the approver agent shipped 260818; no `auto` pass exists on any artifact yet, so the count is 0 of 4 kinds.
- ⬜ A6.2 · No break is answered twice.
  Done when every 🛑 on this board either appears as a numbered rule in `agents/approve-rules/` with its origin stamp, or is recorded as a steer that could not be written down.
  **Now:** Not met. One rule is promoted (`approve-rules.md` R8) against six breaks JL made on 260818, so five of his six are recorded nowhere as either a rule or a steer.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-outline/SKILL.md`
  Reserves `approved:` and states why no machine may write it.
- `page-workflows/haipipe-page-check/SKILL.md`
  Reserves `accepted: ✅` and the Page Type's ruling, and forbids a machine claiming either.
- `page-plugins/haipipe-plugin-bibex/SKILL.md`
  The bibex law that puts the `verified` tick in a person's hands.
### 🧪 Checks · what CATCHES a page breaking a rule
- `haipipe-board/src/page_evidence.py`
  Computes the eight findings that must all be zero before this gate opens.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw00g-human-gate.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QPw1 §3](5-QPw-page-workflow/QPw1-outline/QPw1-outline.md)
  The `approved:` tick and the argument that its phase has no other exit.
- `reads · ALL` · [QPw6 §2](5-QPw-page-workflow/QPw6-check/QPw6-check.md)
  The three independent counts, step ⑤ ACCEPT, and the eight computed findings this gate waits on.
- `contrasts · ALL` · [QPw00r §3](5-QPw-page-workflow/QPw00r-receipts/QPw00r-receipts.md)
  The append-only chain that can point at a tick and never hold one, which is the seam between the two pages.

## Law
- 260818 JL · ✋ **The human gate is LAST**: after the receipts, because a receipt reads the tick and can never hold it
  The controller writes receipts, so a gate inside one is a machine writing its own approval; and a tick is mutable while receipts are an append-only sha256 chain.
  The option rejected was folding the gate into `QPw6 check`, which already administers two of the five ticks, and it loses because the other three live in OUTLINE and EVIDENCE and no single phase page can own all five.
- 260818 JL · ✅ **The gate is accept-biased**: a person is asked to sign only after the computed findings are zero
  The bias changes what is presented and never who writes the tick.
- ⛔ **Silence is never consent**: a required gate with no durable evidence routes to HOLD, not CLOSE
  Otherwise the machine approves itself by timeout.
- 🗂 **The surface is not a store**: every tick stays in the artifact that owns it and the surface writes through
  A surface holding its own copy would drift from the artifact, invisibly, in the one direction that matters.
- 📦 **Folder count is never completed work**: declared, rendered, and accepted are three independent counts and only the third is a person's
  A machine gates the first two without ever touching the third.

## Glossary
- ✋ **tick**: a field only a person may write, of which this board has five.
- ✅ **accept-bias**: the rule that a gate is presented only after the machine's findings are zero, so confirming is the expected outcome.
- 🚪 **the surface**: the one place a person would do all five ticks for a page, which does not exist yet.
- ⏸ **HOLD**: where a required gate with no durable evidence routes, instead of CLOSE.

## Log
- 260818 · [REVISE-CC] four ticks corrected to FIVE across the title, state line, Opening, `§1`, `§1.2`, `§2`, both Aim groups, the Law rows and the Glossary. The missed one is `read:` on a probe card, reserved by `haipipe-plugin-probe`: "Only a person may tick it, and a changed `target` or a re-pulled `proof/` drops the tick back." `§1.2` said `accepted: ✅` was the only tick that reverts; TWO revert, and the pair is now the argument for keeping all five in their artifacts instead of a receipt.

- 260818 1600 · [DRAFT-CC] `§6` added on JL's ruling that a person's job is to BREAK, not to approve: His example, said in Chinese and rendered here: a person is the one who feels this display is no good OVERALL, or that this outline's DIRECTION is wrong, and those are the places a person must break and propose. The cut is whether a rule survives being written down. Four of the five ticks moved to a new `haipipe-board-approver-agent` that passes by DEFAULT against four numbered rules files under `agents/approve-rules/`, seeded from the `display-*` findings `check.py` already emits plus the craft checks nothing was running. The RULING stays a person's and has no rules file, because deciding a page's own question is the point of the page. `§6.1` is the measurement rather than the argument: JL made six interventions on 260818 and every one was a whole-artifact judgment, while all four errors the checker found the same day were local and rule-shaped. `§6.3` closes the loop: a break is promoted into the matching rules file in the person's own words with a `promoted <date> from <who>'s break on <what>` stamp, and R8 of `approve-rules.md` is the first one.- 260818 · [DRAFT-CC] page created, and it is the only page of the QPw group born with nothing on disk behind it, which is the point: the five ticks it collects are defined and enforced in three separate phases and no surface joins them. JL ruled two things into it the same day. First, the page goes LAST, after `QPw00r` receipts, reversing an earlier draft that had them the other way round; the reason is written as `## Law` on both pages so neither can absorb the other later. Second, "human should be more likely to accept it", which is implemented as an accept-bias on PRESENTATION only: the gate opens when the computed findings are zero, and the one line that may not move is that silence is never consent. The genuine hole, as opposed to the dispersion problem, is `§3`: the PDF and the docx have machine findings and no human sign-off at all, which is the Decision Now row.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0