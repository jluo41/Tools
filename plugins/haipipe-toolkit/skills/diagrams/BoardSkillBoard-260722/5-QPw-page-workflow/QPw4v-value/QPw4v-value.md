# Value: the lane the bank answers, bound by path, and read by a person before it may be quoted
state: 🟡 IN PROGRESS · the lane ships; 3 cards exist board-wide and none is read · open: 5
owner: CC
method: follow one number from the card that asks for it to the sentence that prints it, and name the state it must reach before a page may quote it
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
Where does a number on a page come from, and how does a reader trace it back?
The 🔢 value lane is the only one of EVIDENCE's three that crosses to a bank.
`QPw3` raised the card and sent the stripped question; this lane lands what came back.
Binding is BY PATH: `target:` names a real QA file rather than copying its content.
Two states matter and only the second means done.

**The two states**: `answered` is the machine's finish, and `read:` is the page's, ticked by a person who wrote the answer into the prose.
**What `proof/` holds**: the files pulled out of the task folder, with their source, run and sha256, so staleness is computable.
**Where it came from**: this face was split from `QPw4` on 260818, by JL's ruling that each evidence kind gets its own page.

## Writing Style
How this page must be written. Read it before editing, and edit to it.
- **Follow ONE number end to end.** The lane exists so a printed number traces back, so a rule stated without a path a reader can walk has not been stated.
- **Name the state, never say "landed" loosely.** The ladder is `planned`, `commissioned`, `answered`, `read`, and only the last is a person's.
- **Language and sentences.** English only, one sentence per line, no em-dashes.

## Diagram
**The value lane**: one card, one bank, one path, one human tick.

```text
🔢 VALUE · lane 2 of 3 in 🃏 EVIDENCE
┌──────────────────────────────────────────────────────────────────────┐
│ 📁 lands in   <page>/probe/PP<NN>-<slug>/card.md      plugin QPf9     │
│ ✋ hand       the BANK answers · a PERSON reads                       │
│ 🚦 exit test  state `answered` + target: names a REAL QA file         │
│               + proof/ is non-empty  ·  then `read:` 🧑              │
└──────────────────────────────────────────────────────────────────────┘

  the card, and which half may cross the wall:
  probe/PP<NN>-<slug>/
  ├── card.md      🧑 the head: question · serves: · state: · target: · read:
  ├── consumer/    🧱 the STAKE · what the page loses  🚫 NEVER crosses
  ├── executor/    🧱 the stripped question + the answer  ✅ may cross
  └── proof/       🧾 the pulled csv/json + source · run · sha256

  the state ladder, and only the last is a person's:
  planned ──▶ commissioned ──▶ answered ──▶ read 🧑
   raised     dispatched to     the bank     a person wrote it
   at PROBE   the bank          returned     into the prose
                                             ⚠️ REVERTS when target
                                                or proof/ changes

  💾 on this board today: 3 cards (QPf9's PP01·PP02·PP03) · 0 read
```
📌 A page quoting a number from a card that is not `read` is quoting an unread answer.

## Content

### 1 · The bank answers, and the binding is a PATH
**The binding rule**: `target:` names a file, and the page never copies the answer's content into itself.

```text
✅ target: <task-folder>/QA/3-visit-lbp-coefficients.md
   the answer stays where the bank wrote it · one owner · one copy

🚫 pasting the answer text into card.md
   two copies drift, and the page becomes the second owner of a fact
   it did not compute
```
📌 The bank is probe-unaware: it answered a neutral question and never saw the stake, which is what makes its answer reusable by another page.

#### 1.1 · `answered` with an empty `proof/` is not answered
(the exit test checks the binding AND the pulled files)
A card whose state says answered while its `proof/` holds nothing is the exact shape that read as done and was not.
So the test is two conditions, and the second is a directory listing rather than a claim.

### 2 · `read:` is the page's finish, and it reverts
**The tick rule**: `answered` is the machine's finish and `read:` is the page's.

```text
`answered`   the bank returned something
`read:` 🧑   a person read executor/a-executor.md, wrote the A-consumer
             into the page's prose, and ticked card.md
             ⚠️ a changed `target` or a re-pulled `proof/` DROPS the tick
```
📌 It is one of the five person-reserved ticks on this board and one of the two that go backward, the other being a display unit's `accepted: ✅`.

#### 2.1 · The revert rule is the same rule a display unit has, for the same reason
(acceptance binds to the inputs it was accepted with)
A tick that survived its own inputs changing would say a person approved something they never saw.
`QPw00g-human-gate` collects all five ticks and argues where the surface for them should live.

### 3 · One card may serve many bullets, and the link runs backward
**The serves rule**: the card names the plan addresses it answers, and the plan is never rewritten.

```text
card.md   serves: C4.P1.B4 · C3.P1.B3 · C7.P2.B1   ← written by PROBE
the plan  knows nothing about the card              ← frozen by `approved:`

a bullet reads as done only when EVERY card in its backlink has landed,
never when any one has: "one number landed, one question still open"
is not an answered bullet
```
📌 `PP04` on `QC1-visitlbp` serves three addresses because one script answers all three, and that is reuse rather than duplication.

### 4 · The lane does not wait, and nothing waits on it
**The parallel rule**: it runs beside 📚 citation and 🖼 display.

```text
🖼 display DOES depend on this lane's OUTPUT, not on its schedule:
   an intake freezes FROM a proof/, so it needs one answer, not all of them
📚 citation depends on nothing here at all
```
📌 No lane waits for another to FINISH, which is the qualification that makes the parallel claim true.

## Aims
### A1 · 🔢 The bank answers, and the binding is a PATH
- ⬜ A1.1 · No card on this board copies its answer's content instead of pointing at it.
  Done when every card's `target:` resolves to a real QA file and no `card.md` holds the answer text.
  **Now:** Not measured. Three cards exist board-wide, in `QPf9`, and none has been checked for a copied answer.
- ⬜ A1.2 · No card is `answered` with an empty `proof/`.
  Done when a sweep of every `answered` card finds a non-empty `proof/`.
  **Now:** Not measured. No sweep of `answered` cards against their `proof/` has run.
### A2 · ✋ `read:` is the page's finish, and it reverts
- ⬜ A2.1 · No page quotes a number from a card that is not `read`.
  Done when every printed value on this board traces to a card whose `read:` is ticked.
  **Now:** Not met, and knowably so: zero cards on this board are `read`, while the QPw pages print numbers throughout.
### A3 · ↩ One card may serve many bullets, and the link runs backward
- ⬜ A3.1 · Every card carries a `serves:` line that resolves.
  Done when the three cards on this board each name at least one real plan address.
  **Now:** Not met. The three cards on this board carry no `serves:` line at all.
### A4 · ⚖️ The lane does not wait, and nothing waits on it
- 🔨 A4.1 · No figure on this board orders the three lanes.
  Done when no prose or figure serializes citation, value and display.
  **Now:** Being worked on now. This page and `QPw4` draw them parallel; the rest of the board is unswept.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-plugins/haipipe-plugin-probe/SKILL.md`
  The card folder, its four counts, and the state ladder including the `read:` tick. It wins over this page on all three.
- `../probe/haipipe-probe/SKILL.md`
  The crossing protocol: stake stripping, bank independence, and the four slot words.
### 📥 Input files · what the work READS
- `<page>/probe/PP<NN>-<slug>/executor/`
  The stripped question that crossed, and the answer that came back.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw4v-value.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw4 §1](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The contract page these three lane faces belong to, and the Evidence Bundle that joins them.
- `continues · ALL` · [QPw3 §1](5-QPw-page-workflow/QPw3-probe/QPw3-probe.md)
  The phase that raised the card this lane fills, and the MATCH order that ran before it.
- `reads · ALL` · [QPf9 §1](4-QPf-page-folder/QPf9-probe/QPf9-probe.md)
  The probe plugin's folder contract and its four counts.

## Law
- 🔢 **Binding is by PATH, never by copy**: `target:` names the QA file and the page stays a reader
  Two copies of one fact drift, and the page would become the second owner of something it did not compute.
- 🧾 **`answered` with an empty `proof/` is not answered**: the exit test checks both
  A card whose state said answered while its proof folder was empty is the shape that read as done and was not.
- ✋ **`read:` is a person's, and it reverts**: a changed `target` or a re-pulled `proof/` drops the tick
  Acceptance binds to the inputs it was accepted with, which is the same rule a display unit's `accepted:` follows.
- ↩ **The link runs backward**: the card names the bullets and the frozen plan is never rewritten
  A bullet is done only when every card in its backlink has landed, never when any one has.

## Glossary
- 🔢 **card**: the folder at `<page>/probe/PP<NN>-<slug>/` holding one question, its answer, and its proof.
- 🎯 **target:**: the card field naming the QA file in the bank that answers it, by path.
- 🧾 **proof/**: the files pulled verbatim out of the task folder, with source, run and sha256.
- ✋ **read:**: the human tick meaning a person read the answer and wrote it into the page. It reverts.
- 🧱 **the wall**: the path boundary between `consumer/` and `executor/`; only the executor side may cross.

## Log
- 260818 · [DRAFT-CC] created as a lane face of `QPw4` on JL's ruling, given three times before it was executed. The page follows one number from the card that asks for it to the tick that permits quoting it, which is the thing `QPw4`'s single lane row could only summarize. Two facts written from disk rather than asserted: three cards exist board-wide, all in `QPf9`, and none carries a `serves:` line or a `read:` tick, so `A2.1` and `A3.1` are knowably unmet rather than merely unmeasured.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0