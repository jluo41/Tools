# The introduction: why this board exists and how to read it
state: 🟡 PARTIAL · reopened 260816 as the introduction chapter (QA0 and QA1 folded in); closes on the fresh-agent routing test and the carried rulings
owner: JL
method: one chapter a cold reader can finish: the reason in plain words, the glossary and the folder map carried whole, and pointers for every deeper contract; a coined word is a defect
session: d8c19e4a-9ff3-4052-91b3-ba262e24515b

## Opening
Why keep a board, and how do you read this one?

Design talk with an agent is smart and forgetful: the next session starts from nothing, and a decision that lives only in a chat will be lost, re-argued, or quietly reversed.
A board gives every decision an address instead: one topic is one folder, one decision is one page with a state anyone can read.
This chapter is the front door: the reason a board exists, the words it speaks, where its files live, and a tour of its chapters.

**Where this page sits**: This is the first page of the QA group and of the whole board.
`QA2` takes the next question, how a topic becomes pages and groups, and the ladder groups (`QB` down to `QS`) carry the contracts themselves.

**What was folded in**: On 260816 two pages became divisions of this one: the glossary (`QA1`, now `§4`) and the folder map (`QA0`, now `§5`).
Their full records sit in `_archive/QA1-concepts/` and `_archive/QA0-three-folders/`, and their open rulings live on in this page's Decision Now.

**What this page never restates**: A pointer is machine-checked on every build and a paraphrase is not.
So `§3` names each law and the page that rules it, and `§6` tours each chapter without repeating its contract.

**Covered elsewhere**: The board folder's shape is `QB1`; the page grammar is `QPs1`; a single page's internal glossary stays that page's `## Glossary`; the group graph is `board.md ## Board Map`.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Plain story, no metaphor**: The reason a board exists is told in plain words (JL 260816).
The chapter must pass the weak-English test everywhere: a shorter common word always beats a precise rare one.

**A coined word is a defect**: Every term in `§4` is the source documents' own word, and every entry names the page or file that defines it, so the glossary never becomes a second source.

**Point, never restate**: Outside `§4` and `§5`, which this page owns, a rule appears here only as a pointer to the page that rules it.

**Absorbed content stays whole**: `§4` and `§5` carry the absorbed pages' substance, not summaries of it; what they trim is history, which the archives keep.

## Diagram
**The ground and the ladder**: the three folders everything lives in, and the nine groups in reading order.

```text
  ── the ground: three folders, three kinds of truth ──────────
  ⚙️ ① skills/board/            SHIPS    read by a runtime
  🗂 ② this board folder        ARGUED   read by people
  📤 ③ every board/ site        RENDERED read by anyone     → §5

  ── the ladder: the groups in reading order ──────────────────
  🧭 QA · Design        the system's meta: this chapter + birth,
        │               round, identity, roster
  🏛 QB · Board  ──▶  📐 QPs · Page-Structure   what a page SAYS
        │             📂 QPf · Page-Folder      where its files LIVE
        │             🔁 QPw · Page-Workflow    how a page MOVES
        └─────────────────────┴──▶  ✏️ QS · Sentence  the atomic unit

  support lanes, entered when needed:
  ⚙️ QC · Engine        🖥 QO · Operating        ✅ QF · Execute
  the code's shape      the live, served board   what actually RAN
```

## Content
### 1 · Why a board
**The problem and the fix**: what is lost when a decision lives only in a chat, and what an address buys.

```text
  🗣 a design conversation ────▶ 💨 the next session starts from nothing
      smart · fast · forgetful      re-argued · reversed · lost

  📋 the board ────────────────▶ 🏠 every decision has an address
      one topic = one folder        one page · one state line
      one decision = one page       talk lands as sentences
            │
            ▼
  🎓 what settles GRADUATES into the skill that ships
  📤 what is generated is disposable · 🗃 what is argued is kept
```
📋 Establishes the reason the board exists, before any of its machinery.

#### 1.1 · A decision that lives only in a chat is already lost
You design a system by talking to an agent, and the conversation is good: options are weighed, a choice is made, work proceeds.
Then the session ends, and the next one starts from nothing.
The choice survives only in scrollback nobody will read, so it gets re-argued, quietly reversed, or simply forgotten.
"What did we decide about X?" has no answer, and the loudest most recent chat wins.
This board's own history shows the failure: "the work is finished" and "the board is ready to hand back" came apart three times in one day before `QA3` gave the round a gate.

#### 1.2 · An address is what makes a decision citable
The fix is to give every decision a place instead of a moment.
One topic gets one folder; every decision gets one page; the page carries a state line (🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD) that anyone can read without reading the page.
Talk lands on the page as sentences, and a sentence is archived, never deleted (`QS2`), so the record survives every restructure.
A settled decision GRADUATES: its Law is copied into the skill that ships, and only then binds (`QA6`).
That is the whole loop: argue on a page, settle, graduate, and the chat can be forgotten because the page cannot.

#### 1.3 · The stranger test
The board is working when a stranger, human or agent, opens the generated site and knows three things without asking: what is decided, what is still open, and where to argue.
That is why this page's own close condition is a routing test: a fresh agent, given only this chapter, must find the owning page for any question.
It is also why the site is generated rather than authored: counts and states are computed from the pages on every build, so the front door cannot lie.

#### 1.4 · Why this board argues the board itself
This board's subject IS the board: a board used to define boards.
Every rule in `§3` was earned on these pages before it shipped, which is the strongest evidence the model works.
It is also the reason a reader meets the same ideas twice, once as this board's practice and once as the shipped family's contract, and `§5` is what keeps those two from being confused.

### 2 · How to read this board
**Three passes**: this chapter, the ladder, the lanes.

```text
  ① 🧭 read this chapter    the reason (§1) · the words (§4) ·
                            the folders (§5)
  ② 🪜 walk the ladder      QB ──▶ QPs ──▶ QPf ──▶ QPw ──▶ QS
                            the altitudes, in order
  ③ 🔦 enter a lane         QC · QO · QF, only when your question
                            is code, the live board, or evidence
```
🧭 Establishes the reading order: this chapter first, then the ladder, then the lanes.

Read this chapter first so the words mean what the pages mean.
Then walk the ladder from the board altitude down to the sentence, one tour rung below per group (`§6`).
Enter a support lane only when your question is about code, the served board, or evidence.

### 3 · The laws that hold everywhere
**The invariants**: rules that survived every round, each with the page that rules it.

```text
  ⚖️ one board = one folder · one page = one decision        QB1
  📂 a page owns its folder; every subfolder is a plugin     QPf1
  📝 markdown is the only source; board/ is derived          QC3
  ✏️ a sentence is archived, never deleted                   QS2
  🎓 settled Law graduates into SKILL.md, no more, no less   QA6
  🗣 a decision lives on a page, never only in a chat        QA3
```
⚖️ Establishes nothing new: each row is a pointer to the page that rules it.

The plugin boundary's own page is still owed in `QPf`, which this board records as visible debt rather than a stub.

### 4 · The words this family uses
**The glossary**: one entry per concept, each the source documents' own word, each naming where it is defined.

```text
  📦 4.1 the Board family     family ▸ skill ▸ folder ▸ source ▸ site
  📄 4.2 the page family      group ▸ page ▸ kind × phase ▸ state ▸ section
  ✏️ 4.3 the sentence family  sentence ▸ lane ▸ comment ▸ edit ▸ card
  ⚖️ 4.4 the working words    decision · standing · spine · sync · span
```
📖 Establishes the shared vocabulary; nothing here is defined for the first time.

#### 4.1 · The Board family

One topic's stack, from the shipped family down to the generated webpage a reader opens:

```text
📦 skills/board/                       the FAMILY that ships
 └─ 🎛 /haipipe-board                  the SKILL you invoke
     └─ 📁 BoardSkillBoard-260722/     one topic's Board-Folder
         ├─ 📝 board.md                the Board-level SOURCE
         └─ 🌐 board/                  the generated Board-Webpage
             ├─ 🏠 index.html          the Board-Webpage-Index
             └─ 📄 <group>/<id>.html   a Board-Webpage-Page
```

The FAMILY that ships: `skills/board/` (four skills + ten Page Types + four Page Phases + three agents as of 260806; the roster face is `QC1b` §2).
The SKILL you invoke: `/haipipe-board`; a subskill is a unit nested inside the family folder, never a peer of it (`§5.3`).
One topic's `Board-Folder`: `BoardSkillBoard-260722/`.
The Board-level SOURCE: `board.md` (Spine · Close · Topic · Pipeline · Board Map · Pages; optional Board Structure · Related Folders · Links).
The generated `Board-Webpage`: the `board/` site (`index.html`, one page per group, one file per Q/S page, shared `_assets/`), never hand-edited.
The `Board-Webpage-Index` is `board/index.html`; a `Board-Webpage-Page` is the focused per-page file (`board/<group>/<id>.html`) a page row opens.

#### 4.2 · The page family

Where a page sits: a group holds pages, and each page carries a kind, a type with a phase, a state line, and its sections:

```text
🗂 group          a ### heading in ## Pages, one folder per group
 └─ 📄 page       Q decision 🔒 closes by its checkboxes
                  S stage    🚪 closes at its human gate
                  Design    🎨 closes on a SELECTION record (260815)
     ├─ 🧬 Page KIND (Q · stage · design)  ×  🌀 Phase (DRAFT·PROBE·REVISE·CHECK)
     ├─ 🚦 state: line      🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD
     └─ 📑 section          a ## heading, fixed order, 🧭 Opening leads
```

page / face: one `Q*.md` or `S*.md`; Q is a decision (closes when its checkboxes close), S is a lifecycle stage (closes at its human gate); one layout serves both.
Design-<n>: the unit design page (260815); the mirror kinds Skill-<unit> and Agent-<unit> retired when for-design absorbed them, and a unit page now settles on its SELECTION record like any Q.
Page kind / Page Phase: one page combines a stable kind with a current phase; the kinds are thinning toward stage and design (`QPs2`, JL 260815), the four phases DRAFT · PROBE · REVISE · CHECK ship under `board/page-phases/`, and the verbs CREATE / WORK ON / RUN are `haipipe-page`'s door (`QPw1`).
section: a `##` heading inside a page; the on-stage order is fixed (`QPs1`), and the renderer knows sections only through `ALIAS` (`src/common.py`).
Opening: the lead section's one name on every page kind (260731); `Question` survives only as a legacy alias, so older pages parse forever.
group: a `###` heading in `## Pages`, one folder per group (`QB1`); since 260731 every page id matches its group letter, and every earlier id stays resolvable as a declared Link.
state: the first emoji of the `state:` line (🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD); the suffix is human-readable and never a fifth state.

#### 4.3 · The sentence family

One sentence and its lanes: the atomic row, and the typed `>` lines that adjacency binds to it:

```text
📝 sentence              one source line, the atomic row (QS1)
 ├─ 🛤 apparatus / lane  any typed > line bound by adjacency
 ├─ 💬 > Comment WHO     a remark on the sentence just above
 ├─ ✎  > edit record     one saved whole-sentence change
 └─ 🃏 > Card the words  a panel on marked words inside it
```

sentence: the atomic row, one per source line (`QS1`).
apparatus / lane: a typed `>` line bound to the sentence above it by adjacency (`QS1`).
comment: a sentence-local `> Comment WHO` row written directly below the sentence it discusses; the former page-bottom queue and its open/solved lifecycle are retired.
edit record: a sentence-local `> ✎` row recording one saved whole-sentence change (`QS2`).
card: a panel opened by clicking a few marked words INSIDE a sentence, written `> Card the words: what to show`.

#### 4.4 · The working vocabulary

The six terms of trade and the object or rule each one names:

```text
⚖️ decision       what a Q face settles  →  🎓 graduates into SKILL.md or ref/
🪪 standing       may this family write into a board it does not own?
🦴 spine / close  board.md's one-line purpose + its acceptance condition
🔁 sync           done means written back to the owning face, same round
🤖 managed span   a <!-- haipipe:...start/end --> block a script owns
🧩 Skills row     what a page governs and whether it landed
```

decision: what a Q face settles; the word replaced "ruling" on 260729 (JL). A settled decision GRADUATES: its `## Law` is copied into `SKILL.md` (operating rules) or `ref/` (specs), and only then binds.
standing: whether this family may make a given write into a board it renders but does not own; mechanical writes have it, editorial writes do not (`QB1` §4).
spine / close: board.md's one-line purpose and its acceptance condition.
sync / write-back: work done in a round is written back to its owning face the same round; "done" means written back.
managed span: a block between `<!-- haipipe:...start -->` and `end` markers that a script owns (`stage.py`, `skillpage.py`); authors never edit inside.
🧩 Skills: the States row listing what a page governs and whether it landed; the convention is owned by `QPs1`.

### 5 · The three folders
**The geography**: everything lives in one of three places, and the board is the deletable one.

```text
  ⚙️ ① SHIPS       skills/board/           a reusable procedure,
                                           read by a runtime
  🗂 ② IS ARGUED   this board folder       the rulings that produced
                                           it, read by people
  📤 ③ IS RENDERED every board/ site       generated output, read by
                                           anyone, owned by no one

  🧪 delete ② ▸ every skill in ① still runs
  🧪 hand-edit ③ ▸ the next build erases you
```
🗺 Establishes where every new file belongs, and which movements between the three are allowed.

#### 5.1 · The three kinds, and why the distinction pays

All three are casually called the Board, and each carries a different kind of truth:

```text
kind          lifetime                    breaks how
────────────────────────────────────────────────────────────────────
⚙️ ① ships    as long as anyone uses it   a design argument leaks in,
                                          and the skill cannot ship
                                          without its own history
🗂 ② argued   until the board closes      a runtime starts reading it,
                                          and an open question becomes
                                          a dependency
📤 ③ rendered until the next build        someone hand-edits it, and the
                                          edit vanishes silently
```

The full map of `①`, one unit per line:

```text
  ⚙️ ① skills/board/                          ONE folder, the family
       ├── haipipe-board/                     the DOOR · build and serve
       │     SKILL.md          what an agent is told
       │     src/              parse · body · page_board · page_question
       │     assets/           css/ · js/  (inlined at build)
       │     ref/              board-form.md · page-template.md
       │     cli/              build.py check.py serve.py watch.py
       │                       xcal.py regroup.py skillpage.py stage.py
       │     status.py
       ├── haipipe-page/                the ENGINE · Page = TYPE x PHASE
       │                                      verbs CREATE / WORK ON / RUN
       ├── page-types/                        ten TYPE variants, one unit each
       ├── page-phases/                       four PHASE contracts
       ├── haipipe-sentence/            SPEC · the atomic unit
       ├── haipipe-board-routing/             VERB · BOTH altitudes
       │     SKILL.md · src/lanes.py          structure + anchored write-back
       ├── agents/                            reviewer · creator · orchestrator
       │     haipipe-board-reviewer-agent.md  + creator + page-orchestrator
       ├── README.md  CHANGELOG.md
       └── every unit versions on its own clock
```

`②` is this folder, `BoardSkillBoard-260722/`: `board.md` as the manifest, one folder per page group, `board.excalidraw`, `fig/`, `_archive/`, `_runs/`, and generated `board/`.
`③` is every other board folder `①` is pointed at: the sibling design boards under `skills/diagrams/01-*/`, a paper's `0-lifecycle/`, and any `<unit>/diagram/<NN>-<topic>-<YYMMDD>/`.
`②` is one of these too; it is numbered apart because it is the only one whose CONTENT this family owns.

#### 5.2 · The movements that are allowed, and the two that are forbidden

```text
   ⒜  ② ──graduates──▶ ①
        a page reaches ✅ and its Law is COPIED into whichever unit of
        ① owns it. The page stays; the skill gains the rule.    → QC1
   ⒝  ① ──renders──▶ ② ③
        cli/build.py reads a board folder and writes its board/ site.
        The renderer never reads a board's MEANING, only its form.
   ⒞  ① ──writes back──▶ ② ③
        serve.py turns a click into a line of markdown in a page.
        A comment, an item, an archive move: always the .md, never the .html.
   ⒟  inside ①, the units stay separable
        haipipe-board-routing reads board.md and each page's `# ` line and
        never imports haipipe-board/src/, so the two ship on their own clocks.

   ✗  ① ──▶ ②          the family depending on the board that designs it
   ✗  anything ──▶ board/   it is output; the next build erases you

   delete ② and every skill in ① still runs. That is the test.
```

#### 5.3 · A subskill is a unit inside ①, never a folder beside it

`skills/board/` is one folder on disk and one family in the roster, so it is one number.
Inside it, a unit earns its own directory when it has its own trigger, its own contract, and its own version.
That test admitted `haipipe-board-index` on 260730 and was reversed on 260802: JL merged the index into `haipipe-board-routing`, because three of its five verbs turned out to be other units' work written a second time, which the trigger-contract-version test does not detect.
The separability rule is what keeps this honest: `haipipe-board-routing` never imports `haipipe-board/src/`; it reads `board.md` and each page's `# ` line, which is a surface both units can hold still.
If that import ever appears, the two are one skill wearing two folders.

#### 5.4 · One folder per group, inside the board folder

Since 260726 every board keeps one folder per page group, named `Q<letter>-<slug of the group title>`.
The bare `Q<letter>/` form is rejected because it writes the id a second time; the group's SUBJECT is the half a reader cannot recover from the filenames.
Membership is by PATH, never by registration: `## Pages` lists bare filenames and sets order and grouping only, so moving a page between folders is a pure `git mv`.

#### 5.5 · The live layer's scope is the SPACE, one server for every board under it

A board folder is the unit of CONTENT, and it is not the unit of SERVING.
One `serve.py` runs per repo root and serves every board beneath it, so `--root` is the served tree rather than a board, and `target()` refuses any path that escapes it.
Both pieces of local state live at the root: the activity database and the session sidecar are both `<root>/.haipipe-board/`.
A terminal is keyed by the sha1 of its page's absolute path, so two boards' pages can never collide, and `/_board/terms` lists what is running across all of them at once.
The consequence that bites is in the other direction, and `QF1` owns it: anything shared, meaning the inlined assets and the engine itself, changes every board under the root at once, so a change checked against one board has not been checked.

#### 5.6 · What is deletable from what

Every unit inside `①` is deletable from every other unit inside `①`.
`②` is deletable from all of them: it argues the family and ships nothing.
That is the test this division exists to protect, and it is the reason a runtime may never read a Q page.
This division also owns the data of board.md's `## Related Folders`: which roots the Index fold lists, and which files each may open (`related_folders()` embeds only those named `.md`/`.txt` files at build).

### 6 · The tour: one rung per chapter
**The chapters**: the nine groups in reading order, each mirroring the unit it argues.

```text
  6.1 🧭 QA constitution  6.2 🏛 QB board      6.3 📐 QPs structure
  6.4 📂 QPf folder       6.5 🔁 QPw workflow  6.6 ✏️ QS sentence
  6.7 ⚙️ QC engine        6.8 🖥 QO operating  6.9 ✅ QF execute
```
🪜 Establishes what each chapter holds and where its rules live; nothing here restates a contract.

#### 6.1 · Chapter QA · the constitution

What must hold before any artifact exists, and the page or division that holds each:

```text
  🗺 §5   geography     ships · argued · rendered  (was QA0, folded 260816)
  📖 §4   language      every term, one definition (was QA1, folded 260816)
  🏗 QA2  birth         a topic becomes pages BEFORE files exist
  🔁 QA3  the round     when an agent may hand the board back
  🪪 QA5  identity      why "it points at nothing" kept returning
  📇 QA6  the roster    what ships (QA6a the manual · QA6b the units)
```

No page here owns a deliverable, and that is the group's definition.
The group's cautionary tale is `QA5`: one defect class, reported four times in different clothes, because identity lived in names and empty lookups stayed silent.
`QA3` exists because "the work is finished" and "the board is ready to hand back" came apart three times in one day, and a person caught it each time.

#### 6.2 · Chapter QB · the board altitude

One folder, one board: the source a person edits and the site anyone opens:

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

#### 6.3 · Chapter QPs · what a page says

Structure and closing: the sections in their fixed order, and the two kinds that change what closing means:

```text
  📐 QPs1   the base: Opening · Diagram · Content · Aims · States
            + the haipipe-page unit, plugged in its skill/ (QPs00 folded in 260816)
  🏷 QPs2   the kinds and their admission
  🧪 QPs3   the stage specimen     closing = a human gate
  🧪 QPs4   the design specimen    closing = a SELECTION record
```

The group fronts on its base: `QPs1` states the grammar and, since JL folded `QPs00` into it on 260816, also carries `haipipe-page`'s snapshot and health record, because the grammar and the unit that ships it are one subject.
A kind survives only if it changes what closing MEANS, which is why five kinds became two on 260815.
The mirror kind died of a measured disease: a page that decides nothing has no question to ask, so five Openings came out of one template.
The group's method is specimen-first: build one real page, then write the contract it taught you (`QPs3`, `QPs4`).

#### 6.4 · Chapter QPf · where the files live

The plugin law: a page owns its folder, and every subfolder of it is a plugin:

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
Material that once wore page costumes lands here instead: decks, scenes, unit snapshots, meeting notes, kept conversations, and since 260815 a page's own bib, skill map, evidence questions, and compiled projections.

#### 6.5 · Chapter QPw · how a page moves

The loop and its hands: four phases, and the dispatched agents that run them:

```text
  🔁 QPw1  the page's time axis: draft · probe · revise · check
  🧩 Design-6  the workflow unit's page; the three dispatched
     agents' pages folded into it (🗂), reviewer · creator · orchestrator
```

This chapter was born owing its debt, on purpose: the four phase contracts ship as skills with no page arguing them, and the receipt contract has no page either.
The one-writer-one-page rule is why large batches fan out as N agents and never as one agent with N pages.
A round ends at `QA3`'s gate, and CHECK belongs to a fresh context that knows nothing you forgot to write down.

#### 6.6 · Chapter QS · the atomic unit

One sentence: the smallest thing that carries an address, a record, and a card:

```text
  ✏️ QS1  the sentence: card · lanes · remark · edit
  🗃 QS2  the record lifecycle: archived, never deleted
  📍 QS3  the generated address a machine points at
  🧪 QS4  the run: every shape crossed with every write
  🧩 Design-5  the sentence unit's design page
  ✍️ Design-4  the prose standard's design page: two producers of one
     ✎ grammar, side by side (moved from QPs, JL 260816)
```

The board's memory is sentence-grained, and `QS2` owns the law that keeps it.
`Design-4` sits here because `haipipe-writing`'s product is a `✎` sentence lane, the grammar `Design-5`'s unit owns, and the two producers of that one record are watched in one chapter (JL 260816).
That is how the 260815 restructure could move and rename most of the board while every old citation still resolves.
The write path lands exactly one line in one file, and `QS4` exists to prove every shape of that claim.

#### 6.7 · Chapter QC · how it is coded

The round trip: markdown in, site out, and a reader's action landing back in markdown:

```text
  📝 md ──build──▶ 🌐 board/ ──reader──▶ live write ──▶ 📝 md
  ⚙️ QC1  one Law, three files (QC1a build · QC1b src · QC1c live)
  🏭 QC2  a page from outside: a skill (QC2a) · a meeting (QC2b)
  🔁 QC3  the whole trip, and the anchor a write lands on (QC3a)
```

HTML never travels back into markdown, and every generated byte is disposable.
The group's founding ruling was JL's, on seeing 25 loose scripts: "这个结构很差" (this structure is bad), and the top level emptied into `cli/` and `tests/` the same day.
What the one Law demands of each file is `QC1`'s to state, and this chapter only points at where it lands.

#### 6.8 · Chapter QO · the served board

Two audiences, one server: you working on the board, and others arriving at it:

```text
  🖥 you      QO1 the split workspace · QO2 the status strip · QO3 the cost
  🔗 them     QO4 hosting · QO5 mounts · QO6 where it runs
  🔒 access   QO7 locks · QO8 the console · QO9 the bind address
```

Working and Sharing were one group until 260731, two until 260815, and one again now; the split's reason died with the restructure.
The line that matters most is `QO9`'s: the bind address is the only access control there is, so the listener stays on loopback by default.
The chat and terminal questions that once lived here moved to `QPf4`, the chat plugin's page, because a kept conversation is material.

#### 6.9 · Chapter QF · what actually ran

Evidence, not claims: the lane that keeps "contract written" from passing as done:

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
### P · The page itself
- P1 · A fresh agent routes five questions from this page alone
  Done when: five questions naming no page ids each land on the owning page, using only this chapter.
- P2 · Every pointer on this page resolves on every build
  Done when: the build's dead-link and unresolved-id checks report zero findings on this page.
- P3 · The deck presents this chapter, division by division
  Done when: the `slide/` deck follows `§1` to `§6`, one slide per rung, re-authored after the 260816 fold.

### A4 · The words this family uses
- A4.1 · JL reads the glossary once and strikes or adds entries
  Done when: every entry in `§4` is confirmed, struck, or replaced by JL's own word.
- A4.2 · Every entry names its defining page or file
  Done when: no entry in `§4` defines anything; each points at the page or file that does.

### A5 · The three folders
- A5.1 · The three-folder model is ratified as drawn
  Done when: JL confirms `①` `②` `③` and the nesting of subskills inside `①`.
- A5.2 · The two forbidden movements are ratified
  Done when: JL confirms no runtime may read a Q page and nothing is hand-written into `board/`.
- A5.3 · `skills/diagrams/_feedback/` has a ruled home
  Done when: JL places it inside the map or explicitly outside it.
- A5.4 · The ✗-direction checker is commissioned or deferred
  Done when: a checker proves no shipped file cites a Q page, or the deferral is recorded with its reason.

## States
- ⬜ P1 · The routing test has not run; it is this page's close condition.
- ✅ P2 · The 260816 post-fold build reports zero findings on this page; QA0, QA1, and QA1a resolve through `## Links`.
- ⬜ P3 · The deck predates the fold and presents the old nine-chapter layout; re-authoring is owed.
- 🧠 A4.1 · Waiting on JL's read; every entry was refreshed to the current architecture before the fold.
- 🧠 A4.2 · Proposed yes; an entry that defines instead of pointing would make the glossary a second source.
- 🧠 A5.1 · Proposed yes as drawn; two boards already run on it, and `QC1` and the ladder groups assume it.
- 🧠 A5.2 · Proposed yes; the whole test is one line: delete `②` and every skill in `①` still runs.
- 🧠 A5.3 · Proposed: it is `①`'s inbox, since every card's `lands_in:` names a shipped file, so a card graduates exactly as a page's Law does.
- 🧠 A5.4 · Proposed defer until A5.1 and A5.2 are ticked; a checker can only enforce a rule that has been ruled.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🗺 Ratify the three-folder model as drawn (A5.1) and the two forbidden movements (A5.2)
- [ ] 🧾 Rule where `skills/diagrams/_feedback/` belongs (A5.3)
      A · it joins `②` as the boards' lesson inbox. B · it is `①`'s inbox, a card graduates like a Law. C · it stays outside the map.
- [ ] 📖 Rule what `face` means, because two authorities disagree (A4.1)
      This page's `§4.2` says page and face are the SAME thing, while `haipipe-page/SKILL.md`'s glossary row says a face is a page whose id carries its parent's number.
      ⭐ A: synonyms, and a child page is a `child`. ⭐ B: `face` means only the child form.
      🤖 If nobody answers: CC follows A, because 45 pages were reworded from `face` to `page` on the weak-English axis and A is what that wording assumes.
- [ ] 🧠 Read `§4` once as the glossary (A4.1) and strike or add entries

## Files
- `board.md`
  The manifest this page's tour is derived from; its `## Pages` is the only registry, and its `## Related Folders` data is `§5.6`'s to govern.
- `slide/`
  The presented surface: the AI-authored deck, one slide per division; owed a re-authoring after the 260816 fold (P3).
- `skill/`
  The page's skill map (QPf10's plugin): one row, `haipipe-board · uses`.
- `_archive/QA0-three-folders/` · `_archive/QA1-concepts/`
  The absorbed pages, whole: their full States, Logs, and plugins, kept per `QS2`.
- `../../board/haipipe-board/SKILL.md`
  The distilled manual: the sum of the settled rules, kept elsewhere so this page can stay a chapter.
- `../../board/haipipe-board/ref/board-form.md` · `src/common.py`
  The grammar the words in `§4` come from, and `ALIAS`, the machine half of "section".

## Log
- 260816 · [FOLD-CC, JL ruled] QA0 and QA1 folded into this page: the words became `§4`, the folders became `§5`, and the chapter reopened on why a board exists (`§1`).
  JL chose the plain story over a metaphor for `§1`; the candidate metaphors (courthouse, ward round, manuscript) are recorded in this session's chat.
  Both pages' open rulings carried into Decision Now unsettled; both archived whole with their plugins; their ids resolve here through `## Links`.
- 260815 · [REVISE-CC] §5 followed the QPs00 rename (JL): the chapter fronts on the unit page the way this board fronts on this page.
- 260815 1720 · [JL via CC] the page grew its skill/ plugin: one declared row, `haipipe-board · uses`, so the front door carries the engine's live card.
- 260815 1710 · [REVISE-CC] the tour caught up with the QPf build round: the plugin roster grew from five to ten.
- 260815 1700 · [REVISE-CC] the deck aim closed under JL's ruling "We will just have the AI deck"; reopened 260816 by the fold (P3).
- 260815 1540 · [REVISE-CC] R1: the chapters grew from one table into nine divisions, each anchored in its group's own story.
- 260815 1420 · [DRAFT-CC] opened as the board's chapter 1 (JL ruled D21-D23): pointers and invariants only; QA4 archived and its deck absorbed into this page's slide/ plugin.
- (the absorbed pages' own Logs stay in `_archive/QA0-three-folders/` and `_archive/QA1-concepts/`, unrewritten)
