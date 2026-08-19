# Evidence: land the citation, the value, and the display intake, each by its own hand
state: 🟡 IN PROGRESS · three lanes ship; one verified citation exists board-wide, on QPf4 · open: 6
owner: CC
method: give each of the three kinds its own lane with its own hand and its own exit test, then show why they are one phase and not three
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
For every claim the plan promised, is the thing that backs it actually on disk, and whose hand put it there?

EVIDENCE is phase ④ and its plain job is that question, answered three ways: a CITATION is a bibex entry a person landed, a VALUE is a probe card bound to its answering QA file, and a DISPLAY INTAKE is a frozen snapshot plus the renderer that will draw it.
The three run as LANES rather than steps: they start together, no lane waits for another to FINISH, and the phase ends when all three pass.
It changes what the page KNOWS without authoring the page's argument, which is why it never edits target prose and never touches purpose or Aims.
It was called PROBE until 260816, and the rename was not cosmetic: PROBE owned one of the three things a claim needs, so a page could finish it with every question answered and still print a paragraph where a table was promised.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every rule names its LANE**: the three kinds have different hands, different folders, and different exit tests, so a rule that does not say which lane it governs cannot be applied.
Writing "the evidence must be verified" says nothing, because only one of the three lanes has a `verified` field at all.

**Lanes are parallel and must never be drawn as a sequence**: an arrow between two lanes is a factual error about this phase, not a stylistic choice.
The one real chain in this phase runs from an answer to its display intake, and it is drawn once, as a chain, and labelled as such.

**The plugin pages own their folders**: when this page and `QPf5`, `QPf8`, or `QPf9` disagree about a folder, the plugin page wins and this page is wrong.
This page owns the TIMING and the exit test; it never restates the shape on disk.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
Three lanes at once, three hands, three exit tests, and the one chain that makes them one phase.

```text
🃏 EVIDENCE · phase ④ of 7 · THREE LANES, NOT THREE STEPS
┌──────────────────────────────────────────────────────────────────────────┐
│ lane          lands in                    hand         exit test         │
│ ───────────────────────────────────────────────────────────────────────── │
│ 📚 citation   <page>/bibex/<stem>.bib      a PERSON     `verified` on     │
│               one entry                    verbatim      the entry        │
│                                            only                           │
│ 🔢 value      <page>/probe/PP<NN>-<slug>/  the BANK     `state:` answered │
│               card.md                      task or       + target: names  │
│                                            discovery      a real QA file  │
│                                                          + answer/ holds  │
│                                                            its extract    │
│ 🖼 display    <page>/display/<stem>-       this phase    intake/ frozen   │
│    intake     Display<N>-<slug>/intake/    freezes it    from that answer │
│               + README.md rows             and NAMES     + a renderer     │
│                                            the renderer    named          │
└──────────────────────────────────────────────────────────────────────────┘
   ⛔ no lane waits on another. the phase ends when ALL THREE pass.

   THE ONE CHAIN, and the reason this is one phase:
   Q-executor ─▶ bank QA file ─▶ probe card ─▶ display intake/ ─▶ float.tex ─▶ latex · word
                 "ask once, cite twice": the intake cites the bank by id
                 and a render never invents a value

   THE DERIVED JOIN, keyed by Point, not a fourth folder:
   C3.P1.B4 ├─ answer/proof   probe card · target path · proof manifest
            ├─ citation       bibex key + verification state
            ├─ display input  frozen intake/ + named renderer
            └─ sentence       STILL A HOLE until REVISE realizes it
   → `evidence-ready` when every required source has landed
```
📌 The 🖼 lane freezes inputs here and realizes them in REVISE; only step ① of the display walk belongs to this phase.

## Content

### 1 · Three kinds, three hands, three exit tests
**The lane rule**: each kind has a card that holds it, a maker, and a human gate, and none of the three gates moves into this phase.

```text
kind          who CREATES the card        who FILLS it
──────────────────────────────────────────────────────────────────
🔢 value      ③ PROBE, from the mark      ④ EVIDENCE
📚 citation   a PERSON lands the entry;   ④ EVIDENCE binds it,
              PROBE opens a card only     a person marks `verified`
              when the key is UNKNOWN
🖼 display    ④ EVIDENCE, and only here   ④ EVIDENCE
```
📌 Filling is the boundary for 🔢 and 📚; the display unit is this phase's from its first byte, because a unit that cannot yet be filled cannot honestly be declared either.

#### 1.1 · A value card arrives already RAISED, and a duplicate is the failure
(ruled 260817, replacing "DRAFT proposes")
`haipipe-page-probe` created the card from the approved plan's mark, wrote its `serves:` backlink, and dispatched its stripped question, so this phase usually opens onto a page whose value holes are already folders.
Finding a card already raised is the normal case and is never a reason to create a second one: a question is asked once, and the card id exists to prevent the duplicate.

#### 1.2 · A machine may subset or transcribe bibtex, and may never compose it
(the bibex law, ruled 260815, and the reason the 📚 lane's hand is a person)
The entry lands verbatim from a source a person supplied, and the `verified` tick says a person read it against that source.
A composed entry is indistinguishable from a correct one on the page and wrong in the bibliography, which is why the lane has no machine path at all.

#### 1.3 · Why the display unit cannot be declared earlier
(its `intake/` freezes FROM a `proof/` that does not exist until an answer does)
A page shipped "1 display declared, 0 unit folders on disk" on 260817 by declaring a unit nothing could fill.
So the plan carries only a bare 🖼 mark until this phase has a probe `proof/` to freeze from, and the unit folder is born here.

### 2 · Lanes, not steps, and the phase ends when all three pass
**The parallelism rule**: they run at once, each with its own hand and its own exit test, and no lane blocks another.

```text
🚫 SERIALIZED                        ✅ PARALLEL
① find every bib key                📚 a person lands keys as they come
② then answer every value           🔢 the bank answers on its own clock
③ then freeze every intake          🖼 intake freezes per answer that lands

   a person hunting one missing key      the slow lane delays only itself
   would stall the bank AND the intake
```
📌 This is also why the three are not three pages: pages in a listing imply a reading order, and these three have none.

#### 2.1 · The three kinds are one phase because they CHAIN, not because they resemble each other
(split the chain across phases and the handoff is what gets dropped)
`QV2-lbp-regression-results` carried 7 bound probe cards and 2 rendered displays out of 5 declared, and its LaTeX correctly embedded 2.
JL read that page on 260816 and asked "you have five displays in the display plugins, but only two in the latex, why? Is it the workflow issue?".
It was: nothing owned the intake, so the chain from answer to render had no phase responsible for its middle.

#### 2.2 · The rename from PROBE carried the scope with it
(260816, and PROBE became a live phase again on 260817 meaning something else)
The cosmetic half was that `haipipe-page-probe` and `haipipe-probe` read as the same skill while one is a phase and the other is the crossing protocol.
The substantive half was that PROBE owned one of the three things a claim needs, so the phase could pass with every question answered and the page still missing its table.
DESIGN was weighed as the new name and rejected, because a phase called DESIGN would carry DRAFT's authority over purpose and Aims.

### 3 · The six-step loop is one loop across two phases
**The ownership split**: steps ①②③ end when the question leaves and belong to PROBE, and steps ④⑤⑥ begin when something comes back and belong here.

```text
COLLECT      land the newly raised Q-consumer in the topic's E0 queue
① ORGANIZE   strip the stake, write or reuse the Q-executor          ③ PROBE
② MATCH      read existing evidence before requesting new work       ③ PROBE
③ DISPATCH   send only the neutral Q-executor                        ③ PROBE
④ POINT      bind the returned answer BY PATH                        ④ EVIDENCE
⑤ INTERPRET  copy the A-executor back, write one A-consumer per      ④ EVIDENCE
             Q-consumer
⑥ CARD       land the answer in its kind's card                      ④ EVIDENCE
```
📌 The steps did not change on 260817; only their owner is now written down, and step ⑥ is this phase's exit condition rather than an afterthought.

#### 3.1 · The stake never crosses the wall, and the wall applies to the value lane only
(Q-consumer carries the stake, Q-executor is the only question sent across)
The Q-consumer is authoritative on the target page and carries what the page needs, why it matters, and what breaks; the Q-executor is neutral and answerable by a stranger.
The stake may appear in the Q-consumer and its audit trace, and never in the Q-executor, the A-executor, the dispatch payload, or any bank artifact.
One Q-executor may serve several Q-consumers, and that is reuse rather than duplication.

#### 3.2 · Binding is by PATH, and an answered card with an empty proof folder is not answered
(`target:` names the QA file, and `proof/` must hold the pulled files behind it)
The binding names a real file in the probe-unaware bank rather than copying its content into the page.
A card whose `state:` says answered while its `proof/` is empty is the exact shape that read as done and was not, so the exit test checks both.

### 4 · The display walk is split, and this phase owns only step ①
**The split rule**: five steps, three phases, and the human tick at the end stays where it is.

```text
① INTAKE  🧑 freeze the answer into intake/     EVIDENCE  it is the ANSWER
② RENDER  ⚙️ the renderer writes recipe/        REVISE    the caption and
③ PICK    🧑 choose among candidates/           REVISE    which rows are
④ BUILD   ⚙️ assets/ · float.tex · preview.pdf  REVISE    the ARGUMENT
⑤ ACCEPT  🧑 README `accepted: ✅`              CHECK     the human gate,
                                                          unmoved
```
📌 So EVIDENCE never draws a table: it freezes what the table will be drawn FROM, writes the unit's README rows, and names the renderer that owes step ②.

#### 4.1 · Naming the renderer is part of freezing the intake
(`kind:` selects it, and the five kinds map one to one)
`table` goes to `haipipe-display-table`, `figure` to `haipipe-display-figure`, `diagram` to `haipipe-display-diagram`, `tex` to `haipipe-display-tex` for tikz, algorithm2e and display equations, and `illustration` to `haipipe-display-illustration`.
An intake frozen without a named renderer leaves step ② with no owner, which is how a declared unit reaches LaTeX as nothing.

#### 4.2 · Naming an unrendered unit in prose is legal and useful
(the chip binds a pending render and says what is owed)
Candidate rendering does not wait for release approval either: a PHI-safe aggregate intake may be rendered for review while a method or provenance probe stays open.
What is not legal is a declared unit with no claim row, because nothing then says what it would show.

### 5 · What this phase writes, and the two surfaces it must never touch
**The write surface rule**: it writes the answer records and never the argument.

```text
MAY WRITE     the QA-probe · the probe card's state and target ·
              a bibex entry landed verbatim · a display unit's README
              rows and intake/ ONLY · the target page's E0 queue and
              E<n> division · an evidence-based State update
🚫 NEVER      target prose
🚫 NEVER      purpose or Aims
🚫 NEVER      a display unit's recipe/ or assets/
```
📌 Landing an answer into the prose belongs to REVISE under a fixed promise, or to DRAFT if the answer changes what the page is for.

#### 5.1 · The Evidence Bundle is a join and not a fourth storage plugin
(keyed by the Outline Point, which is the stable handoff)
The bundle gathers the answer and proof, the citation and its verification state, the frozen display input, and the sentence that is still a hole.
It becomes `evidence-ready` only when every required source has landed, and `accepted` only after the human gates owned by the source plugins and CHECK have passed.
This phase never edits the outline to add new ids: `serves:` is written by the probe or display unit back to the frozen Point.

## Aims

### A1 · 🧾 Three kinds, three hands, three exit tests
- A1.1 · Each lane's hand and exit test are readable without opening a plugin page.
  Done when all three lanes name their folder, their hand, and their test in one figure.
- A1.2 · No card on this board is a duplicate of another card's question.
  Done when every `serves:` line on this board resolves and no two cards carry the same Q-executor.

### A2 · ⚖️ Lanes, not steps, and the phase ends when all three pass
- A2.1 · No page or figure on this board draws the three kinds as a sequence.
  Done when a sweep finds no arrow between two lanes.
- A2.2 · The declared and rendered display counts agree on every page of this board.
  Done when `cli/check.py` reports zero `display-declared-not-rendered` findings.

### A3 · 🔁 The six-step loop is one loop across two phases
- A3.1 · Every step names exactly one owning phase.
  Done when the six steps each carry one phase label and no step carries two.
- A3.2 · No bank artifact on this board carries a stake.
  Done when a sweep of dispatched Q-executors finds no consumer-side language.

### A4 · 🖼 The display walk is split, and this phase owns only step ①
- A4.1 · No display unit on this board is frozen without a named renderer.
  Done when every `intake/manifest.yaml` on this board has a `kind:` row resolving to one of the five renderers.

### A5 · ✍️ What this phase writes, and the two surfaces it must never touch
- A5.1 · No EVIDENCE run has written target prose, purpose, or Aims.
  Done when a receipt audit over `_runs/page/` shows no EVIDENCE receipt whose artifacts include prose.
- A5.2 · The Evidence Bundle is derived rather than stored.
  Done when no folder on this board holds a bundle as a file.

## States
### Decision Now
- [ ] 🗣 Rule whether the three lanes ever become three pages
      📍 `Part` §2, lanes not steps
      🔔 `Why now` JL proposed QPw4c, QPw4d and QPw4v on 260818 and the three subjects already have pages in the QPf group, so the board would carry each of them twice
      ⭐ `A ·` keep three LANE DIVISIONS on this page, each pointing at its QPf plugin page: this page owns the timing and the exit test, `QPf8` `QPf9` `QPf5` own the folders, and nothing is said twice
      `B ·` split into three lettered faces, which gives each lane its own Aims and States at the cost of a third copy of the same three subjects, and which is the shape JL folded on 260815 when `QPf4`'s four chat faces went back into its Content the evening they were born
      🛑 `Blocks` A2.1, and the board's page count
      🤖 `If nobody answers` A takes effect, which is what this page is written as

### A1 · 🧾 Three kinds, three hands, three exit tests
- ✅ A1.1 · Met. The Diagram carries all three lanes with folder, hand, and exit test.
- ⬜ A1.2 · Not measured. No sweep of `serves:` lines or Q-executor duplication has been run on this board.

### A2 · ⚖️ Lanes, not steps, and the phase ends when all three pass
- 🔨 A2.1 · Being worked on now. This page draws them parallel; the rest of the board has not been swept.
- ⬜ A2.2 · Not met. `cli/check.py` reports one `display-declared-not-rendered` on `QPf6-Display1-latex-proof` today.

### A3 · 🔁 The six-step loop is one loop across two phases
- ✅ A3.1 · Met. The six steps each carry one owner in `§3`, split ①②③ to PROBE and ④⑤⑥ here on 260817.
- ⬜ A3.2 · Not measured. No sweep of dispatched Q-executors for consumer-side language exists.

### A4 · 🖼 The display walk is split, and this phase owns only step ①
- ⬜ A4.1 · Not met. `cli/check.py` reports `display-intake-unfrozen` on FOUR units, not two: `QPf5-Display1`, `QPf5-Display2`, `QPw00-Display1`, `QPw00-Display2`.

### A5 · ✍️ What this phase writes, and the two surfaces it must never touch
- ⬜ A5.1 · Measurable now and measured: `_runs/page/` holds 5 receipts, all `CHECK` or `REVISE` and none `EVIDENCE`, so no EVIDENCE run has written prose because none has run.
- ✅ A5.2 · Met. The bundle is defined as a join keyed by Point and no folder holds one.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-evidence/SKILL.md`
  The phase contract itself, and the authority on its procedure.
- `../probe/haipipe-probe/SKILL.md`
  The shared crossing protocol: stake stripping, bank independence, and the evidence boundary.
### 📥 Input files · what the work READS
- `<page>/probe/PP<NN>-<slug>/`
  The cards PROBE raised, whose answers this phase lands.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw4-evidence.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw2 §2](5-QPw-page-workflow/QPw2-draft/QPw2-draft.md)
  Where the stake is written that a card's consumer side must carry, which is why a card cannot be raised before DRAFT ends.
- `reads · ALL` · [QPf9 §1](4-QPf-page-folder/QPf9-probe/QPf9-probe.md)
  The probe plugin's folder contract for the 🔢 lane. It wins over this page on the folder's shape.
- `reads · ALL` · [QPf8 §1](4-QPf-page-folder/QPf8-bibex/QPf8-bibex.md)
  The bibex plugin's contract for the 📚 lane, including the law that a machine never composes bibtex.
- `reads · ALL` · [QPf5 §1](4-QPf-page-folder/QPf5-display/QPf5-display.md)
  The display plugin's unit contract and its five-step walk, of which this phase owns only step ①.

## Law
- 260816 JL · 🪪 **The rename carried the scope**: PROBE owned one of the three things a claim needs, so the phase could pass while the page still lacked its table
  `QV2-lbp-regression-results` carried 7 bound cards and 2 rendered displays out of 5 declared, and JL read it and asked whether it was a workflow issue.
  DESIGN was weighed as the new name and rejected, because a phase called DESIGN would carry DRAFT's authority over purpose and Aims.
- 260817 JL · ⚖️ **Three LANES, not three steps**: they run at once, each with its own hand and its own exit test, and the phase ends when all three pass
  Serializing them would let a person hunting one missing bib key stall the bank and the intake behind it.
  The option rejected was an ordered citation-then-value-then-display sequence, which loses because the lanes have no real dependency on each other.
- 260815 JL · 📚 **A machine may SUBSET or TRANSCRIBE bibtex, never COMPOSE it**: the 📚 lane's hand is a person and has no machine path
  A composed entry looks correct on the page and is wrong in the bibliography.
- 🖼 **A display unit is born at EVIDENCE and no earlier**: its `intake/` freezes from a `proof/` that does not exist until an answer does
  Declaring a unit nothing can fill is how a page shipped "1 display declared, 0 unit folders on disk" on 260817.
- 🔢 **Answered with an empty `proof/` is not answered**: the exit test checks the binding AND the extract
  A card whose state said answered while its proof folder was empty is the exact shape that read as done and was not.

## Glossary
- 🃏 **lane**: one of the three kinds of evidence, each with its own folder, hand, and exit test, all three running at once.
- 🔢 **probe card**: the folder at `<page>/probe/PP<NN>-<slug>/` holding one question, its answer, and its proof.
- 📚 **bibex entry**: a bibtex record landed verbatim into `<page>/bibex/<stem>.bib`, carrying a `verified` field a person ticks.
- 🖼 **intake**: the frozen snapshot a display unit will be drawn from, plus the named renderer that owes the drawing.
- 🔗 **Evidence Bundle**: the derived join of all three kinds for one Outline Point, `evidence-ready` when every required source has landed.
- 🧱 **Q-executor**: the neutral, stake-free question, and the only question that crosses to the bank.
- ✋ **read:**: the 🔢 lane's human tick in `card.md`, meaning a person read the answer and wrote it into the page. `answered` is the machine's finish; `read:` is the page's, and it REVERTS when `target` or `proof/` changes.

## Log
- 260818 · [DRAFT-CC] page created on JL's ruling that each workflow step gets its own page. Written from `haipipe-page-evidence`, and it answers JL's own proposal in the same round: he asked for QPw4c citation, QPw4d display and QPw4v value as three sub-pages, and the answer is three LANE DIVISIONS instead, because `QPf8`, `QPf9` and `QPf5` already carry those three subjects as folder contracts and three sub-pages would be a third copy. Two further reasons went into the Decision Now row rather than being decided silently: JL folded this exact shape on 260815 when `QPf4`'s four lettered chat faces went back into its Content, and a lettered listing implies a reading order that three parallel lanes do not have. Five divisions: the three lanes, the parallelism rule and the QV2 incident, the six-step loop split across two phases, the display walk's step ①, and the write surfaces. Also corrected here against JL's summary "the probe to get the evidence": probe serves the 🔢 lane only, since a citation comes from a person and a display intake comes from an answer that already landed.
