# The board, in one chapter
state: 🔴 OPEN · drafted 260815; closes on the fresh-agent routing test
owner: CC
method: pointers and invariants only; the build checks every id and link on this page, so nothing here restates what another page rules
session: d8c19e4a-9ff3-4052-91b3-ba262e24515b

## Opening
Can a reader with no background learn what this system is, how to read this board, and where every rule lives, from this one page?

This board designs the Board system itself: one topic becomes one folder, one page per decision, and one generated site anyone can open and comment on.
Since 260815 its groups are the system's own ladder, so reading the board in order is the tour of the system.
This page is the front door: it states the problem, names the laws that hold everywhere, and points at the page that rules each part.
It never restates a contract, because a pointer is machine-checked on every build and a paraphrase is not.
The deck in this page's `slide/` plugin presents the same introduction to a live audience.

## Diagram
**The ladder**: the nine groups in reading order, each mirroring the unit it argues.

```text
  🧭 QA · Design        the system's meta: words · folders · round · roster
        │
  🏛 QB · Board  ──▶  📐 QPs · Page-Structure   what a page SAYS
        │             📂 QPf · Page-Folder      where its files LIVE
        │             🔁 QPw · Page-Workflow    how a page MOVES
        │                        │
        └────────────────────────┴──▶  ✏️ QS · Sentence   the atomic unit

  support lanes, entered when needed:
  ⚙️ QC · Engine        🖥 QO · Operating        ✅ QF · Execute
  the code's shape      the live, served board   what actually RAN
```

## Content
### 1 · How to read this board
**Three passes**: the words, the ladder, the lanes.

```text
  ① 🧭 QA    the words (QA1) · the folders (QA0) · the round (QA3)
  ② 🪜 QB ──▶ QPs ──▶ QPf ──▶ QPw ──▶ QS    the altitudes, in order
  ③ 🔦 QC · QO · QF    enter for the code, the live surface, the proof
```

Read `QA1` first so the words mean what the pages mean.
Then walk the ladder from the board altitude down to the sentence, one chapter division below per group.
Enter a support lane only when your question is about code, the served board, or evidence.

### 2 · The laws that hold everywhere
**The invariants**: rules that survived every round, each with the page that rules it.

```text
  ⚖️ one board = one folder · one page = one decision        QB1
  📂 a page owns its folder; every subfolder is a plugin     QPf1
  📝 markdown is the only source; board/ is derived          QC3
  ✏️ a sentence is archived, never deleted                   QS2
  🎓 settled Law graduates into SKILL.md, no more, no less   QA6
  🗣 a decision lives on a page, never only in a chat        QA3
```

The plugin boundary's own page is still owed in `QPf`, which this board records as visible debt rather than a stub.

### 3 · Chapter QA · the constitution
**Six premises**: what must hold before any artifact exists, and the page that holds each.

```text
  🗺 QA0  geography    ships · argued · rendered, mutually deletable
  📖 QA1  language     every term, one authoritative definition
  🏗 QA2  birth        a topic becomes pages BEFORE files exist
  🔁 QA3  the round    when an agent may hand the board back
  🪪 QA5  identity     why "it points at nothing" kept returning
  📇 QA6  the roster   what ships (QA6a the manual · QA6b the units)
```

No page here owns a deliverable, and that is the group's definition.
Delete any one of them and nothing breaks today; a zero-background reader gets lost tomorrow.
The group's cautionary tale is `QA5`: one defect class, reported four times in different clothes, because identity lived in names and empty lookups stayed silent.
`QA3` exists because "the work is finished" and "the board is ready to hand back" came apart three times in one day, and a person caught it each time.

### 4 · Chapter QB · the board altitude
**One folder, one board**: the source a person edits and the site anyone opens.

```text
  📂 QB1   the folder: board.md · groups · pages · plugins
  🏠 QB2   the Index: spine · Board Map · Section Matrix
  📑 QB2a  the sidebar rail on every page
  ⚙️ Design-1  the engine's design page, its bytes in skill/
  🔀 Design-2  routing: every write onto a board, both altitudes
```

The Index is DERIVED, which is why it can be trusted: counts and states are computed from the pages on every build, so the front door cannot lie.
What is authored at this altitude is only `board.md`.
The two units that ship this altitude live here as Design pages, their contract surfaces plugged beside them.

### 5 · Chapter QPs · what a page says
**Structure and closing**: the sections in their fixed order, and the two kinds that change what closing means.

```text
  📐 QPs1  the base: Opening · Diagram · Content · Aims · States
  🏷 QPs2  the kinds and their admission
  🧪 QPs3  the stage specimen     closing = a human gate
  🧪 QPs4  the design specimen    closing = a SELECTION record
  🧩 Design-3  the page spec's own design page · Design-4  the prose standard
```

A kind survives only if it changes what closing MEANS, which is why five kinds became two on 260815.
The mirror kind died of a measured disease: a page that decides nothing has no question to ask, so five Openings came out of one template.
The group's method is specimen-first: build one real page, then write the contract it taught you (`QPs3`, `QPs4`).

### 6 · Chapter QPf · where the files live
**The plugin law**: a page owns its folder, and every subfolder of it is a plugin.

```text
  📂 QPf1   <name>/<name>.md · the page owns its folder · the 📂 tab
  🖌 QPf2   draw: attaching a scene (QPf2a the linked sources)
  🎬 QPf3   slide: the AI-authored deck plugin
  💬 QPf4   chat: ONE Chat, kept conversations (its faces folded in)
  🖼 QPf5   display: the rendered-unit plugin
  🚪 QPf9   probe: a page is a small paper · probe/ mirrors 1-probes/
  📜 QPf6   latex · 📝 QPf7  word · 📚 QPf8  bibex   the projections
  🛠 QPf10  skill: bibex's twin into the skill tree · uses/designs
  ⬜ owed   the boundary page · meeting · fixture
```

Discovery never enters a plugin, a boundary earned twice before its own page exists.
The hazards and their defusal are that boundary page's story to tell, and writing it is the group's named debt.
The plugin contracts ship as one unit whose roster every plugin page cites, and each page above rules exactly one row of it.
Material that once wore page costumes lands here instead: decks, scenes, unit snapshots, meeting notes, kept conversations, and since 260815 a page's own bib, skill map, evidence questions, and compiled projections.

### 7 · Chapter QPw · how a page moves
**The loop and its hands**: four phases, and the dispatched agents that run them.

```text
  🔁 QPw1  the page's time axis: draft · probe · revise · check
  🧩 Design-6  the workflow unit's page; the three dispatched
     agents' pages folded into it (🗂), reviewer · creator · orchestrator
```

This chapter was born owing its debt, on purpose: the four phase contracts ship as skills with no page arguing them, and the receipt contract has no page either.
The one-writer-one-page rule is why large batches fan out as N agents and never as one agent with N pages.
A round ends at `QA3`'s gate, and CHECK belongs to a fresh context that knows nothing you forgot to write down.

### 8 · Chapter QS · the atomic unit
**One sentence**: the smallest thing that carries an address, a record, and a card.

```text
  ✏️ QS1  the sentence: card · lanes · remark · edit
  🗃 QS2  the record lifecycle: archived, never deleted
  📍 QS3  the generated address a machine points at
  🧪 QS4  the run: every shape crossed with every write
  🧩 Design-5  the sentence unit's design page
```

The board's memory is sentence-grained, and `QS2` owns the law that keeps it.
That is how the 260815 restructure could move and rename most of the board while every old citation still resolves.
The write path lands exactly one line in one file, and `QS4` exists to prove every shape of that claim.

### 9 · Chapter QC · how it is coded
**The round trip**: markdown in, site out, and a reader's action landing back in markdown.

```text
  📝 md ──build──▶ 🌐 board/ ──reader──▶ live write ──▶ 📝 md
  ⚙️ QC1  one Law, three files (QC1a build · QC1b src · QC1c live)
  🏭 QC2  a page from outside: a skill (QC2a) · a meeting (QC2b)
  🔁 QC3  the whole trip, and the anchor a write lands on (QC3a)
```

HTML never travels back into markdown, and every generated byte is disposable.
The group's founding ruling was JL's, on seeing 25 loose scripts: "这个结构很差" (this structure is bad), and the top level emptied into `cli/` and `tests/` the same day.
What the one Law demands of each file is `QC1`'s to state, and this chapter only points at where it lands.

### 10 · Chapter QO · the served board
**Two audiences, one server**: you working on the board, and others arriving at it.

```text
  🖥 you      QO1 the split workspace · QO2 the status strip · QO3 the cost
  🔗 them     QO4 hosting · QO5 mounts · QO6 where it runs
  🔒 access   QO7 locks · QO8 the console · QO9 the bind address
```

Working and Sharing were one group until 260731, two until 260815, and one again now; the split's reason died with the restructure.
The line that matters most is `QO9`'s: the bind address is the only access control there is, so the listener stays on loopback by default.
The chat and terminal questions that once lived here moved to `QPf4`, the chat plugin's page, because a kept conversation is material.

### 11 · Chapter QF · what actually ran
**Evidence, not claims**: the lane that keeps "contract written" from passing as done.

```text
  ✅ QF1  the gate after every change: check.py + a fresh reviewer
  🐣 QF2  a zero-context agent must open the skill unaided
  🌐 QF3  a real browser drives the built page
  💬 QF4  a real chat turn drives the drawer
```

The founding incident: a whole feature was built and running on 260726 while its page still said nothing is built, so the board and the machine told two different stories.
Mechanical checks catch state; only a fresh reader catches prose, which is why every gate here pairs the two.
An execute record names its route, its result, and what it refused to touch.

## Aims
- [ ] 🐣 A fresh agent routes five questions from this page alone
      Five questions naming no page ids; using only this page, the agent must land on the owning page each time.
- [ ] 🔗 Every pointer on this page resolves on every build
      The build's dead-link and unresolved-id checks cover each id above; the aim holds while this page has zero findings.
- [x] 🎬 The deck presents the same introduction
      The AI-authored deck in `slide/` follows the chapter divisions §3 to §11, one slide per rung; the absorbed QA4 deck it replaced predated the ladder and was a verbatim reflow, the tier JL retired.

## States
- ⬜ The routing test has not run; it is this page's close condition.
- 🔨 Pointer health is checked by the build from now on; the first clean run is the evidence to record here.
- ✅ The deck question is ruled and done: JL 260815 "We will just have the AI deck", so the reflow tier retired board-wide and this page's deck is authored against the chapter divisions.

## Files
- `board.md`
  The manifest this page's ladder is derived from; its `## Pages` is the only registry.
- `QA-design/QA00-overview/slide/`
  The presented surface: the AI-authored deck, one slide per chapter rung. The absorbed QA4 deck was removed when the reflow tier retired.
- `SKILL.md`
  The distilled manual: the sum of the settled rules, kept elsewhere so this page can stay a map.

## Log
- 260815 1710 · [REVISE-CC] §6 caught up with the QPf build round: the roster grew from five plugins to ten (probe QPf9, latex QPf6, word QPf7, bibex QPf8, skill QPf10), so the owed line drops `skill` and keeps the boundary page, meeting, and fixture as the group's remaining debt.
- 260815 1700 · [REVISE-CC] the deck aim closed under JL's ruling "We will just have the AI deck": an authored deck now follows §3 to §11 one slide per rung, and the stale absorbed QA4 deck (a pre-ladder verbatim reflow) was removed from slide/.
- 260815 1540 · [REVISE-CC] R1: the chapters grew from one table into nine divisions (§3 to §11), each anchored in its group's own story; the laws moved up to §2.
- 260815 1420 · [DRAFT-CC] opened as the board's chapter 1 (JL ruled D21-D23): pointers and invariants only; QA4 archived and its deck absorbed into this page's slide/ plugin.
