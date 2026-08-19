# Citation: the lane a person lands verbatim, and the tick no machine may write
state: 🟡 IN PROGRESS · the lane ships; one verified entry exists board-wide · open: 4
owner: CC
method: state what a person does, what a machine may never do, and the one field that says a human read the source; every rule names the file it lives in
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
Where does a reference come from, and who is allowed to write it down?
The 📚 citation lane is the one of EVIDENCE's three with no machine path.
A person supplies the entry, it lands verbatim in `<page>/bibex/<stem>.bib`, and a person ticks `verified`.
That tick means they read the entry against its source.
A machine may subset an existing bib or transcribe what a person gave it, and may never compose bibtex.

**Why the prohibition is the lane**: a composed entry looks correct on the page and is wrong in the bibliography, and no reader of the page can tell the difference.
**Where it came from**: this face was split from `QPw4` on 260818, by JL's ruling that each evidence kind gets its own page.

## Writing Style
How this page must be written. Read it before editing, and edit to it.
- **Every rule names the file it lives in.** A rule about the bib that does not say which file holds it cannot be checked.
- **Say what a machine may NOT do, not only what a person does.** The lane's identity is its prohibition, so a description that omits it has described nothing.
- **Language and sentences.** English only, one sentence per line, no em-dashes.

## Diagram
**The citation lane**: one hand, one file, one tick.

```text
📚 CITATION · lane 1 of 3 in 🃏 EVIDENCE
┌────────────────────────────────────────────────────────────────┐
│ 📁 lands in   <page>/bibex/<stem>.bib          plugin QPf8      │
│ ✋ hand       a PERSON, verbatim only                           │
│ 🚦 exit test  the key is landed AND `verified` is ticked         │
└────────────────────────────────────────────────────────────────┘
     🤖 a machine MAY        SUBSET an existing bib
                            TRANSCRIBE what a person supplied
     🚫 a machine MAY NEVER  COMPOSE bibtex
                            tick `verified`

  📮 does PROBE raise a card for this lane?
     🔴 no, when the key is KNOWN: a person lands it, no question asked
     🟢 yes, when the key is UNKNOWN and the bank must find the work

  💾 on this board today: 2 bib entries · 1 verified
     4-QPf-page-folder/QPf4-chat/bibex/QPf4-chat.bib:12
     `verified = {JL 260815}`  ← the only human tick that exists anywhere
```
📌 A page quoting a source whose entry is unverified is quoting something nobody checked.

## Content

### 1 · A person lands it, and a machine may never compose it
**The bibex law**: the machine's two permitted verbs are subset and transcribe.

```text
verb          allowed?   why
─────────────────────────────────────────────────────────────────
SUBSET        🟢 yes     the entry already exists and is being narrowed
TRANSCRIBE    🟢 yes     a person supplied the bytes and they are copied
COMPOSE       🔴 never   a fabricated entry is indistinguishable from a
                         correct one on the page, and wrong in the .bib
```
📌 The prohibition is what makes the lane a person's; drop it and the lane becomes a generator.

#### 1.1 · The tick means a person read the entry against its source
(`verified` on the entry, and no machine may write it)
It is one of the five ticks reserved for a person on this board, and it does not revert, because a bib entry has no upstream input to change under it.
`QPw00g-human-gate` collects all five and argues where they should live.

### 2 · PROBE raises a card only when the key is unknown
**The card rule**: a known paper needs no question, and an unknown one is bank work.

```text
situation                                   card?
──────────────────────────────────────────────────────────────
the key is known and the entry is in hand    🔴 no · land it
the key is known, the bibtex is not          🟡 UNRULED · QPw3's
                                                Decision Now row
the paper itself must be found               🟢 yes · dispatch it
```
📌 The middle row is the commonest case on this board and it has no ruling, which is why it is a card question rather than a settled one.

### 3 · The lane does not wait, and nothing waits on it
**The parallel rule**: it runs beside 🔢 value and 🖼 display, and no lane blocks another.

```text
🚫 SERIALIZED                     ✅ PARALLEL
① hunt every bib key first        📚 a person lands keys as they come
② then answer the values          🔢 the bank answers on its own clock
③ then freeze the intakes         🖼 intake freezes per landed answer
   ⛔ one missing key stalls          🟢 the slow lane delays only itself
      the bank and the intake
```
📌 A person hunting one reference must never be the reason a number cannot land.

## Aims
### A1 · 📚 A person lands it, and a machine may never compose it
- A1.1 · No entry on this board was composed by a machine.
  Done when every `.bib` entry traces to a person-supplied source or a subset of an existing entry.
### A2 · 📮 PROBE raises a card only when the key is unknown
- A2.1 · The known-paper-unknown-bibtex case is ruled.
  Done when `QPw3`'s Decision Now row is answered and this page carries the answer.
### A3 · ⚖️ The lane does not wait, and nothing waits on it
- A3.1 · No page on this board serialized the three lanes.
  Done when no figure or prose on this board orders citation before value or display.

## States
### A1 · 📚 A person lands it, and a machine may never compose it
- ⬜ A1.1 · Not measured. Two bib entries exist board-wide and neither has been traced to its supplier.
### A2 · 📮 PROBE raises a card only when the key is unknown
- 🧠 A2.1 · Waiting on JL, in `QPw3-probe`'s Decision Now row.
### A3 · ⚖️ The lane does not wait, and nothing waits on it
- 🔨 A3.1 · Being worked on now. This page and `QPw4` draw them parallel; the other 64 pages have not been swept.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-plugins/haipipe-plugin-bibex/SKILL.md`
  The bib file, its keys, and the law that a machine never composes bibtex. It wins over this page on all three.
- `page-workflows/haipipe-page-evidence/SKILL.md`
  The phase this lane belongs to, and the exit test that ends it.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw4c-citation.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw4 §1](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The contract page these three lane faces belong to, and the exit test all three share.
- `reads · ALL` · [QPf8 §1](4-QPf-page-folder/QPf8-bibex/QPf8-bibex.md)
  The bibex plugin's own page: the file, its keys, and the ✓ tick.
- `contrasts · ALL` · [QPw3 §4](5-QPw-page-workflow/QPw3-probe/QPw3-probe.md)
  Which marks earn a card, including the unruled known-paper-unknown-key case.

## Law
- 260815 JL · 📚 **A machine may SUBSET or TRANSCRIBE bibtex, never COMPOSE it**: the lane has no machine path
  A composed entry looks correct on the page and is wrong in the bibliography, and no reader of the page can tell.
- ✋ **Only a person ticks `verified`**: it means they read the entry against its source
  It is one of five person-reserved ticks on this board, and unlike `read:` and `accepted:` it does not revert.
- ⚖️ **The lane never blocks another lane**: a person hunting one key must not stall the bank
  The three kinds of EVIDENCE run at once, and the phase ends when all three pass.

## Glossary
- 📚 **bibex**: the page-owned bib file at `<page>/bibex/<stem>.bib`, one entry per reference.
- ✋ **verified**: the field a person ticks to say they read the entry against its source.
- 📮 **card**: a probe folder, raised for this lane only when the key is unknown.

## Log
- 260818 · [DRAFT-CC] created as a lane face of `QPw4` on JL's ruling, which he gave three times before it was executed: each evidence kind gets its own page, `QPw4c` citation, `QPw4d` display, `QPw4v` value. The earlier argument against the split (that `QPf8`, `QPf9` and `QPf5` already carry these subjects) was overruled: those pages own the FOLDER on disk, and these faces own the LANE inside the EVIDENCE phase, which is a different question. `QPw4` keeps the shared exit test and the Evidence Bundle join.
