# /haipipe-board: pinning down what "a board" is, so it can be reused

spine: A board = one source folder. One Markdown file per page inside it, plus one generated board/ site with an Index, group pages, focused page files, and shared assets. Pin that shape down in SKILL.md so a fresh reader can open and run it without memory.
close: Every Q on this board reaches ✅ or ⏸️. SKILL.md is written, and a fresh agent with no background can read only that and open a decent board, and then this skill is done.
excalidraw: /_excalidraw
dialect: paper
session: 2a45769d-85f8-4704-a30f-17adb2c82776
## Topic
What a board is for: a topic has several undecided questions; lay them out on one page anyone can open and comment on; settle them one by one, then close the board.
Cast: JL = the one who decides. CC = Claude Code, who does the work. Colleagues = the people who review, discuss, or take responsibility for work on the board; each uses their own initials.
What makes this board unusual: its subject IS the board itself, a board used to define boards.

## Pipeline
- 260816 · [RESTRUCTURE-CC, JL ruled] the Design kind folded into the Q series across QB, QPw and QS: a unit rides the Q page that argues its contract, and where no Q page argued it, the Design page became one.
  `Design-6` became `QPw2-the-hands`, keeping its three agent snapshots, its deck and its scene; `Design-4` became `QS5-writing`, keeping `haipipe-writing`; `Design-5` folded into `QS1`, whose contract it ships, and is archived whole.
  Both converted pages were brought to the Q page contract in the same round: a question lead, `## Writing Style`, `## Files`, face figures and numbered paragraphs per division, `A<n>` Aim groups with `Done when`, one State row per Aim, and each page's unruled question as a `### Decision Now` with its options.
  `QPw1` gained a `skill/` list naming the five `page-workflows` units, which closes the debt line that said the phase contracts had no page arguing them.
- 260816 · [RENUMBER-CC, JL ruled] every group folder now carries its place in `## Pages`: `QC-engine/` became `7-QC-engine/`, and the folder listing finally reads in the board's own order.
  A letter says WHICH group and cannot say which comes FIRST, so the three support lanes floated to the top of every listing and `QPs`/`QPf` sat inverted against each other, telling a reader one story while the Index told another.
  Renaming the letters was weighed and refused: it moves 1594 id mentions across 43 pages, needs a `## Links` row each to keep the old ids alive, and cannot order the page rung without spending the s, f and w that say structure, folder and workflow. Numbering moved 197 path strings and no id at all, because nobody cites a folder.
  The rule graduated into the skill the same day (`haipipe-board` 0.138.0): `group_stem()` strips the number before any reader sees the letter, `regroup.py` numbers a whole board, `＋Q` follows what a board already does, and `check.py` fails when a folder and `## Pages` disagree. `QA00 §5.4` carries the law, `QPf1` the ＋Q behaviour.
- 260816 · [RESTRUCTURE-CC, JL ruled] the QB group went to four pages, on JL's call for few pages.
  `QB1`'s standing rule split out as `QB1a`: the page read as settled while the group's one open decision, what may be written into a board we render but do not own, was buried inside it and invisible on the roster. The vacated `### 4` became the board folder's own plugins, `board.excalidraw`, `fig/`, `_archive/`, `_runs/` and the generated `board/`.
  Both Design pages dissolved the way `QPs00` dissolved into `QPs1`: `haipipe-board` and the 260723 meeting note now ride `QB1`, `haipipe-board-routing` rides `QB1a`, and the prose is archived whole with its `draw/`.
  `QB2` lost `### 14`, which only said what the page did not own, and gained the group page, `board/<GROUP>.html`, which Board Structure has declared since it was written and no page argued.
  Numbers are sub-letters rather than new ones: `QB3` to `QB10` are burned ids from the old QB group's split into the page rung, and `QB4` alone is still cited in 161 files.
- 260816 · [RULE-CC, JL delegated] the close's second half was ruled on QA2 §7, after JL answered "make the decision yourself": a closed board folder STAYS with a `closed:` line in its head, `close` REPORTS every settled Law that names no landing site instead of refusing, and a graduated Law row now carries `→ landed in <file>`.
  The third ruling was wrong once and JL caught it in one line ("who said so???"): CC had banned reopening a closed board while `QPw1`, both shipped agents and `QA00`'s own state line all reopen things, so the ban was struck and only the record survives, `closed:` kept and `reopened: YYMMDD · why` added.
- 260816 · [RESTRUCTURE-CC, JL ruled] the QA group became the CONSTITUTION, one page per rung of the loop it describes: why (QA00), the life of a board (QA2), the round (QA3), what ships (QA6).
  Seven pages became four. The identity page left for `QC4`, because what it rules is engine code and QA holds no deliverable; QA6a and QA6b folded into QA6 whole; QA2 absorbed the close, the hole nobody owned, and became `QA2-board-life`.
  The group was renamed because "Design" already means a page kind here (`Design-<n>`), and its folder is `1-QA-constitution/`.
  Numbers were left alone rather than renumbered contiguous: `QA3` is cited as a law row on the front page, so the gaps at 1, 4 and 5 stay and resolve through `## Links`; `QC4` is a reuse under the 260801 precedent and the round trip stays `QC3`.
- 260816 · [FOLD-CC, JL ruled] QA00 became the introduction chapter: QA0 (the folders) and QA1 (the words) folded in as its §5 and §4, and the chapter now opens on why a board exists, told as a plain story (JL chose no metaphor).
  Both pages archived whole with their plugins; their open rulings carried into QA00's Decision Now; QA0, QA1, and QA1a resolve through `## Links`.
- 260815 · [FOLD-CC, JL ruled] "just have one Chat in the plugin": QPf4's four faces folded into its Content the evening they were born, GUI and TUI became a form choice inside the one surface, 13 open aims carried with source tags, full face records archived, then restored as 🗂 FOLDED pages the same night when the FOLDED state shipped (a fold stays linkable, it only stops competing for room).
- 260815 · [MIGRATE-CC, JL ruled] the chat pages joined the plugin that keeps their record: the morning's QO1-QO4 became QPf4a-QPf4d, faces of the new QPf4-chat contract page, and the QO lane renumbered contiguous (260801 rule).
  QPf2a was archived in a parallel session with its scene kept under QPf2; its Links row points at the archive.
- 260815 · [REVISE-CC, JL ruled] the draw plugin became ONE page: QPf2a folded into QPf2, Excalidraw left every `## Diagram` (ascii only on stage), and all 61 page scenes moved into their pages' `draw/` folders. The engine's linked-drawing machinery still reads the old layout; QPf2's Aims carry that debt.
- 260815 · [RESTRUCTURE-CC, JL ruled] the ladder regroup: groups now follow Board -> Page(structure - folder - workflow) -> Sentence, each mirroring the unit it argues.
  Pages became folders (every subfolder is a plugin); the mirror kind retired and its ten pages converted to for-design pages, each holding its unit's contract surface in a `skill/` plugin; Meeting-1 dissolved into `Skill-0`'s `meeting/` plugin and QG with it; QA4's deck moved into its `slide/` plugin; Skill-6 and Skill-8 archived with their units' retirement.
  QU was never born: unit pages live IN their altitude group (the 260805 argue/mirror split re-merged because D12 removed its premise).
  QD and QE merged as QO - Operating; QC renumbered contiguous; the roster pages joined QA.
  Reused numbers follow the 260801 precedent; every other retired id resolves through `## Links`.
  Debt made visible instead of stubbed (QA rule: a page is born when its content exists): the four phase contracts and run receipts (QPw), the plugin boundary + skill/meeting/chat/fixture plugin pages (QPf), and the three reform units' pages (Skill-9/10/11).
- 260806 · [REVISE-CC] the `QBt` figure was frozen at one built specimen while eight sit in the roster twelve lines below it. Corrected against `ls 3-QPs-page-structure/`: eight pages on disk (QBt1 QBt2 QBt3 QBt4 QBt5 QBt6 QBt9 QBt10), each row now carrying the head key that page really declares, and only `for-skill` and `for-meeting` left unbuilt. The `QBt7`/`QBt8` gap is recorded too: a grep for either id across `skills/` returns nothing, so the numbers were never used, which contradicts the `QD` renumbering ruling below and is now an open row on `QB6`.
260802: QB8's five faces folded. QB8a, QB8b and QB8c became QB8's own `### 3` to `### 6` and were archived; QB8d moved to QD8, because a generated address is how a machine POINTS AT a location rather than a thing attached to a sentence; QB8e stayed its own page, since nothing in it is built and its identity question is open. Same shape and same answer as QB4's seven section faces on 260801.
Since 260731 every page id matches its group letter, and a parent page may carry faces as sub-letters. Neither QB4 nor QB8 does any more: QB4's seven section faces folded into its Content on 260801 and QB8's five followed on 260802, which is now the answer whenever a face stops carrying a subject of its own.
Every earlier id stays resolvable as a declared Link, so a citation written under any older naming still lands on the right page.
260731: ids aligned to groups (36 renames), and the Skill roster became its own page kind, `Skill-0` `Skill-1` `Skill-2`.
260731: QD split back into QD · Working and QE · Sharing (briefly QDa/QDb the same day), the archived board-agent page returned as QD7, and Execute moved to QF: a lowercase letter now always means a page's face, never a group.
260730: seven groups folded into five, and `## Board Map` above draws how the groups connect.
260729: the old QC group dissolved (its folder-management and proposal pages survive as today's QB3 and QA2), and the page/sentence faces split out into what are now QB4* and QB8*.
260725: the former QF group merged into QA, and its last page retired on 260726.

## Board Map
Which folders this board works with, how its groups connect, and the cross-group page edges that really exist.
Every id here is a link: a group token opens the index at that group, a page id opens the page.
`QA00` §5 argues the folder map in full.

```text
─────────  ① the folders this board works with  ────────────────────────────────────

  ⚙️ ① skills/board/                          ONE folder, the family that SHIPS
       ├── haipipe-board/           the DOOR · engine · cli/ src/ live/ ref/
       ├── haipipe-page/            SPEC · composes structure × folder × workflow
       ├── page-types/              the KIND variants · stage · design (5 → 2 underway)
       ├── page-phases/             draft · probe · revise · check (fold to workflow ruled)
       ├── haipipe-sentence/  haipipe-board-routing/  agents/
       └── ⬜ page-structure · page-workflow · page-folder units, ruled 260815, unbuilt

  🗂 ② skills/diagrams/BoardSkillBoard-260722/ THIS board, what is ARGUED
       board.md · 9 group folders · its folded pages · plugins in page folders
       board/   📤 OUTPUT: Index · group pages · focused pages · shared assets

  📤 ③ every other board ① renders             what is RENDERED

─────────  ② the groups ARE the ladder  ────────────────────────────────────────────

   what holds first             the altitudes, in reading order
  ┌────────────────┐ ┌──────────────────────────────────────────────────┐
  │ QA·Constitution│ │ 🏛 QB · Board ──▶ 📐 QPs · Page-Structure        │
  │ why · life ·   │ │                   📂 QPf · Page-Folder & plugins │
  │ round · ships  │ │                   🔁 QPw · Page-Workflow         │
  │              4 │ │                              ──▶ ✏️ QS · Sentence │
  │ one page per   │ │ each group holds its contract pages AND the      │
  │ rung of the    │ │ unit that ships it (skill/ plugin on the page)   │
  │ loop           │ └──────────────────────────────────────────────────┘
  └────────────────┘
   the support lanes
  ┌───────────────────┐ ┌────────────────────┐ ┌───────────────────┐
  │ ⚙️ QC · Engine    │ │ 🖥 QO · Operating  │ │ ✅ QF · Execute   │
  │ the code's shape  │ │ you working · them │ │ what actually RAN │
  │ + the defect   10 │ │ arriving        13 │ │ with evidence   4 │
  │ class that returns│ └────────────────────┘ └───────────────────┘
  └───────────────────┘

─────────  ③ cross-group page edges  ───────────────────────────────────────────────

  QA00 ──places───▶  every folder above     QPs1 ──defines──▶ the base page
  QB2  ──renders──▶  this Index             QPf1 ──rules───▶  <name>/<name>.md
  QPw00 ─times────▶  every page's loop      QS1  ──owns────▶  the atomic unit
  QF1  ──proves───▶  every page change      QA6  ──lists───▶  every shipped unit

  every id above is a LINK · retired ids keep resolving through ## Links
```

[↗ the same map as a shared Excalidraw canvas](https://app.excalidraw.com/s/1JWkKv8oMIX/8OmxTBT2e1m?element=_Q20Q1taxY2jiainH_Y57)

## Related Folders
The folders this board touches: the engine that renders it, and what a board folder itself looks like. Open a folder and navigate it, the way you would browse a directory. QB2 owns the fold, QA00 §5 owns which roots are listed; everything below a root is what is actually on disk.
@ ../../board/haipipe-board | ⚙️ haipipe-board · the engine that ships
@ . | 🗂 BoardSkillBoard-260722 · what a board folder looks like

## Board Structure
This Board has one source `Board-Folder` and one generated `Board-Webpage`.
The map is part of the Board-Webpage-Index, not a third peer object, not another Q page, and not part of the settled-question count.

```text
📂 Board-Folder ──build.py──▶ 🌐 board/
                                  ├── 🗂 index.html
                                  ├── 📚 <GROUP>.html
                                  └── 📋 <GROUP>/<page>.html ──▶ ✍️ sentence
```

**Board-Folder — what exists and can be changed**
The folder `BoardSkillBoard-260722/` contains `board.md` as the Board-level manifest, one numbered descriptive group folder for each page group (`7-QC-engine/`, the number being its place in `## Pages`), one Markdown file per Q/S page, `board.excalidraw` as the local whole-Board scene, `fig/` for image assets, and generated `board/`. Its `_archive/` of retired pages was deleted 260822 with every other archive in this tree.
Markdown decides which pages exist and what they say.
The canvas only records their visual placement and deliberately drawn relationship arrows.
Everything under `board/` is derived and is never hand-edited.

**Board-Webpage-Index — understand the Board before entering a page**
`board/index.html` begins with title, Spine, and Close condition.
Its Board Map makes relationships visible; Related Folders opens declared source files; the Section Matrix derives every page's section state; the textual roster remains the searchable way to choose work; Activity closes the Index.
Topic, Pipeline, and this Board Structure remain source-only documentation in `board.md`.
`QB2` owns it, and its `§14` owns the group page one rung below.

**Board-Webpage-Group — understand one group before entering a page**
`board/<GROUP>.html` shows the group's purpose, expandable explanation or lane diagram, progress, and page rows.

**Board-Webpage-Page — work on one page**
Opening a Q or S row goes to `board/<GROUP>/<page>.html`, one focused page with the shared sidebar.
With scripts on the router swaps that page into the current document so chat and terminal attachment survive; with scripts off the same link navigates normally.
`QPs1`'s Content specifies each page section; `QS1` owns the sentence and everything written onto it, and `QS2` owns the record lifecycle.

## Pages
### QA · Constitution
What must hold before any piece of the system is built: one page per rung of the loop the board runs on, argue ▸ settle ▸ graduate.
QA00 is the introduction chapter (260816): why a board exists, the words (absorbed QA1, its §4), the folder geography (absorbed QA0, its §5), and the tour of the chapters, with the deck as its `slide/` plugin.

```text
🧭 ① WHY        QA00  why a board exists · the words · the folders · the tour
🌱 ② LIFE       QA2   a topic becomes pages · and what must be true to END
                      (the close joined birth 260816; §7 holds its three holes)
🔁 ③ ROUND      QA3   when an agent may hand the board back            ✅
🎓 ④ SHIPS      QA6   the unit roster · the SKILL.md cut line
                      (QA6a and QA6b folded in 260816)
✕ the identity page left for QC4 (260816): it rules engine code
```
QA00-overview.md
QA2-board-life.md
QA3-the-round.md
QA6-skillfamily.md
### QB · Board
The Board altitude: what a board IS on disk, and what it SHOWS on screen.
The two Design pages dissolved on 260816, the way QPs00 dissolved into QPs1: each unit now rides the Q page that argues its contract, and both ids still resolve through `## Links`.

```text
📂 the folder      QB1   ① ships and binds · ② argues · where a board
                         lives · group folders · what sits beside board.md
                         carries haipipe-board + the 260723 meeting note
⚖️ the outside     QB1a  what may be written into a board we render but
                         do not own: mechanical · editorial · who broke it
                         carries haipipe-board-routing, the write verb
                         🔴 the group's one open decision
🌐 the webpage     QB2   the Index a reader lands on · rows · ordering ·
                         the group page · the map · activity · the dials
📑 the rail        QB2a  every page, and the open page's own parts
```
QB1-form.md
QB1a-standing.md
QB2-board-webpage-design.md
QB2a-sidebar.md
### QPs · Page-Structure
What a page SAYS: the sections in their fixed order, and the kinds that change what closing means.

```text
📐 the base            QPs1  the sections · five rows · the folds · carries the
                             haipipe-page skill/ plugin (QPs00 folded in, JL 260816)
🏷 the kinds           QPs2  what closes a page: Q · stage · design
🧪 the specimens       QPs3  for-stage · QPs4  for-design
⬜ debt                Skill-9 page-structure, when the unit ships
```
QPs1-overall.md
QPs2-page-types.md
QPs3-for-stage.md
QPs4-for-design.md
### QPf · Page-Folder
Where a page's files LIVE: the folder that carries the page, and the plugins inside it.
A page is `<name>/<name>.md` and every subfolder of it is a plugin (JL 260815); discovery never enters one.

```text
📂 the folder          QPf1  a page owns its folder
🖌 draw                QPf2  the draw plugin · one scene per owner
🎬 slide               QPf3  the deck plugin, reborn from the slide kind
💬 chat                QPf4  ONE Chat: record in chat/ · TUI or GUI
                       chosen after opening · its four faces folded
                       into Content §3-§6 on 260815 evening
🖼 display             QPf5  the display plugin · the family's unit
                       contract adopted at <page>/display/<unit>/
🚪 probe               QPf9  the probe plugin · a page is a small
                       paper, probe/ mirrors 1-probes/, cite by id
📜 latex               QPf6  the latex plugin · md2tex + xelatex,
                       shipped 0.128.0 · derived, regenerable
📝 word                QPf7  the word plugin · coauthor .docx + the
                       PDF twin the tab frames
📚 bibex               QPf8  the bibex plugin · the page-owned bib,
                       fetched whole by key, JL's ✓ (ruled 260815)
🛠 skill               QPf10 the skill plugin · the ranked skill list,
                       the drag is the one judgment (flattened 260816)
🔗 pagex               QPf11 the pagex plugin · the third citation twin:
                       borrow FILES from other pages as symlinks
🧭 outline             QPf12 the outline meta-surface · the page re-read
                       per division from §N anchors, live, storage-less
🗂 task                QPf13 the task plugin · the fourth citation twin:
                       borrow whole task FOLDERS as symlinks, status
                       read live from plan.yaml / report.yaml / QA/
🗣 meeting             QPf14 the meeting plugin · a page's own kept
                       record of a conversation, standalone (260818)
🧾 evidence            QPf15 ONE tab presents the four evidence lanes
                       as segments · storage and gates stay (260831)
⬜ debt                the fixture plugin page, born once its own
                       contract is written
```
QPf1-folder.md
QPf2-draw-attach.md
QPf3-slide.md
QPf4-chat.md
QPf4a-chat-per-question.md
QPf4b-chat-sdk.md
QPf4c-chat-terminal.md
QPf4d-chat-terminal-design.md
QPf5-display.md
QPf6-latex.md
QPf7-word.md
QPf8-bibex.md
QPf9-probe.md
QPf10-skill.md
QPf11-pagex.md
QPf12-outline.md
QPf13-task.md
QPf14-meeting.md
QPf15-evidence.md
### QPw · Page-Workflow
How a page MOVES, in two halves that must not be read as one sequence: `QPw1`-`QPw6` are the PHASES, one page per phase, in loop order, and each one RUNS; `QPw00a`-`QPw00g` are the MACHINE, which cuts across every phase and never runs at all. JL 260818: "Please explain what is 7, 8, 9??? I still don't get it?" - the numbering was the whole confusion, because read in sequence it says "CHECK, then agents, then receipts, then the gate", which is not a thing that happens.
Design-6 became QPw00a on 260816 (renamed off the coined word "hands" on 260818, JL: "why I don't understand 7 specifically"), when the Design kind folded into the Q series: the unit rides the Q page that argues it.
Renumbered 260818 (JL): the loop became `QPw00`, the group holder, on `QA00`'s precedent; the six phases took `QPw1`-`QPw6` in loop order; the hands moved to the tail. JL ruled the human gate LAST of all, and ruled it accept-biased: the machine must clear every mechanical finding before a person is asked to sign.

```text
🔁 the loop        QPw00 the TIME AXIS only: seven phases, non-linear routing,
                        rounds, RUN ≠ ADVANCE, the DRAFT⇄REVISE test, and
                        Page Type vs Page Phase as separate axes
── ⏱️ THE PHASES · QPw1-QPw6, in loop order, each one RUNS ────────────

🧭 outline         QPw1  the MARK · the plan down to the POINT, each bullet
                        marked · exits on NOTHING but a person's `approved:`
                        the cheapest gate on the board: one screen, rejectable
                        in ten seconds, and it costs the prose after
✏️ draft           QPw2  the AIM + the sentence scaffold with visible holes;
                        JL's words: convert the outline's bullets into
                        sentences · the stake a card will carry is written HERE,
                        which is why no card may exist before this phase ends
📮 probe           QPw3  the CARD · PageX/MATCH before new work, then
                        probe/PP<NN>-<slug>/ + `serves:` + dispatch
                        ⬜ born from haipipe-page-probe, 228 lines
🃏 evidence        QPw4  the CONTRACT page for three lane faces: the shared
                        exit test, the six-step loop split, and the Evidence
                        Bundle join keyed by Outline Point
📚 citation        QPw4c a PERSON lands the entry verbatim into bibex/ and
                        ticks `verified` · a machine may subset or transcribe
                        bibtex and may NEVER compose it · one verified entry
                        exists board-wide, on QPf4
🔢 value           QPw4v the BANK answers, bound BY PATH to a real QA file,
                        with proof/ pulled · then `read:` 🧑, the tick that
                        permits quoting · 3 cards board-wide, 0 read
🖼 display         QPw4d this lane FREEZES intake/ and names the renderer,
                        and never draws · the unit outlives 3 phases:
                        ① EVIDENCE ②③④ REVISE ⑤ CHECK · 4 units board-wide
                        and every intake is UNFROZEN
                        ⚖️ split from QPw4 on 260818: JL ruled it three times
🖊 revise          QPw5  the SENTENCE · cite landed cards by id, render, pick,
                        build, and COMPILE until compile earns its own split
                        ⬜ born from haipipe-page-revise, 158 lines
✅ check           QPw6  the ROUTE · CLOSE|REVISE|EVIDENCE|DRAFT|HOLD, judged on
                        the BUILT pdf and docx, never by its own producer
                        ⬜ born from haipipe-page-check, 158 lines

── 🔧 THE MACHINE · QPw00a-QPw00g cut ACROSS all six phases ──────────────
   They have no position in time and never "run". Three axes of one run:
   🎭 QPw00a WHO acts · 📜 QPw00r WHAT proves it ran · ⚖️ QPw00g WHO says yes.
   Three separate pages because each carries its own open ruling, and one
   merged page would hold three unrelated Decision Now blocks.

🤖 the agents      QPw00a  🎭 WHO ACTS · the ROSTER of the three agent units that run a
                        page when no person is in the loop, each at its own
                        maturity with its own debt: haipipe-board-creator-agent
                        (never judges) · haipipe-board-reviewer-agent (never
                        repairs) · haipipe-page-orchestrator-agent (never edits
                        prose) · all three snapshotted in skill/
                        ⚠️ the ROLE SEPARATION rule itself belongs to QPw00 §9.3;
                        this page owns the roster and the per-unit debt only
🧾 the receipts    QPw00r  📜 WHAT PROVES IT · _runs/page/ · one receipt per ATTEMPTED phase, chained
                        by sha256, the seven invariants, and an auditor that
                        REHASHES rather than trusting the receipt · carries the
                        one live run 260805-0216-QB8e and the 11 defects it
                        returned against its own contract · closes the ⬜ debt line
✋ the human gate  QPw00g  ⚖️ WHO SAYS YES · LAST, by JL's 260818 ruling: the FIVE
                        ticks a machine may never write (`approved:` on the
                        outline · `verified` on a bibex entry · `read:` on a
                        probe card · `accepted: ✅` on a display README · the
                        Page Type's ruling), today in 3 phases and N files with
                        0 surfaces joining them · accept-biased: the gate opens
                        only when the 8 routed mechanical findings are zero (10
                        are emitted), and silence is still never consent
                        🔴 the only page born empty, and being empty IS its question
⛔ COMPILE gets no page: zero lines of its own, folded into haipipe-page-revise.
   Whether that fold is permanent is QPw5's Decision Now row, since the loop's
   vocabulary names seven phases and only six have contracts.
```
QPw00-page-loop.md
QPw1-outline.md
QPw2-draft.md
QPw3-probe.md
QPw4-evidence.md
QPw4c-citation.md
QPw4d-display.md
QPw4v-value.md
QPw5-revise.md
QPw6-check.md
QPw00a-page-agents.md
QPw00r-receipts.md
QPw00g-human-gate.md
### QS · Sentence
The atomic unit: one line, its lanes, its card, and everything written onto it.
Both Design pages left on 260816: Design-5 folded into QS1, whose contract it ships, and Design-4 became QS5, since no page argued the prose standard.

```text
✏️ the unit        QS1   one source line · the card · the `>` lanes
                        carries the haipipe-sentence skill/ plugin
                        (Design-5 folded in 260816)
🗃 the records     QS2   how attached records age: typed views, states,
                        archive-first cleanup with restore
📍 the address     QS3   the generated C/H/P/S address an agent is handed
✅ the proof       QS4   every shape a sentence takes, crossed with
                        every operation that writes one
✎ the rewrite     QS5   the verb that rewrites prose and records every
                        word it changed · carries haipipe-writing
                        (Design-4, and it ships from outside the family)
```
QS1-overview.md
QS2-sentence-details-lifecycle.md
QS3-sentence-address.md
QS4-sentence-run.md
QS5-writing.md
### QC · Engine
How the delivery is produced and shipped, renumbered contiguous on 260815 (the roster pages left for QA6).
QC1 the code's shape under one Law (QC1a build, QC1b src, QC1c live); QC2 generating a page from outside the board (QC2a a skill folder, QC2b a meeting note); QC3 the round trip md to html and back (QC3a the write path's anchor); QC4 the defect class that keeps returning, identity read from a NAME and lookups that return EMPTY (arrived from QA on 260816; the number is reused per the 260801 rule and the round trip is QC3).
QC1-codeshape.md
QC1a-buildsplit.md
QC1b-srcsplit.md
QC1c-livesplit.md
QC2-generate.md
QC2a-skill-to-page.md
QC2b-meetingnote.md
QC3-roundtrip.md
QC3a-writepath.md
QC4-identity-and-scope.md
### QO · Operating
The live, served board: you working on it, and others arriving at it.
Working (260731's QD): QO1 the split workspace, QO2 the status strip, QO3 what a page costs.
Sharing (260731's QE): QO4 hosting, QO5 mounting a SPACE, QO6 where it runs, QO7 editing and locks, QO8 the console, QO9 the bind address.
The two lanes merged on 260815; the chat pages left for `QPf4` the same evening (JL: the chat pages belong to the plugin), and the lane renumbered to close its gaps per the 260801 rule.
QO1-split-workspace.md
QO2-session-status-strip.md
QO3-pagecost.md
QO4-hosting.md
QO5-mountspace.md
QO6-whereitruns.md
QO7-editlock.md
QO8-consolescope.md
QO9-bindaddress.md
### QF · Execute
What actually RAN, with evidence and a reopen path: the layer that keeps "contract written" from passing as done.
QF1 the per-change page gate; QF2 the fresh-agent usability acceptance; QF3 drives the built page in a real browser; QF4 drives the chat inside it.
The sentence run moved home to QS4.
QF1-acceptance.md
QF2-newcomer.md
QF3-browser-run.md
QF4-talk-run.md

## Links
# Design-6/7/8 folded into one Page-Workflow design (JL 260815:
# one Design relates to several skills or agents).
# Design-6 became QPw2 on 260816 (the Design kind folded into the Q series).
Design-6             5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
Design-6-page-workflow.md            5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
Design-7             5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
Design-8             5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
# Agent-* joined Design-* (JL 260815); old ids stay resolvable.
# Skill-* became Design-* (JL 260815); the old ids stay resolvable.
# Design-1 and Design-2 archived 260816; every id still resolves.
# QPs00 folded into QPs1 (JL 260816): the grammar page carries the unit's skill/ plugin; QPs00, Design-3 and Skill-3 all resolve there. The archived page sits at _archive/QPs00-haipipe-page/.
Skill-3              3-QPs-page-structure/QPs1-overall/QPs1-overall.md
Skill-3-haipipe-page.md              3-QPs-page-structure/QPs1-overall/QPs1-overall.md
Design-3             3-QPs-page-structure/QPs1-overall/QPs1-overall.md
Design-3-haipipe-page.md             3-QPs-page-structure/QPs1-overall/QPs1-overall.md
QPs00                3-QPs-page-structure/QPs1-overall/QPs1-overall.md
QPs00-haipipe-page.md                3-QPs-page-structure/QPs1-overall/QPs1-overall.md
# Design-4 moved QPs → QS (JL 260816), then became QS5 the same day when the Design kind folded into the Q series.
Design-4             6-QS-sentence/QS5-writing/QS5-writing.md
Design-4-haipipe-writing.md          6-QS-sentence/QS5-writing/QS5-writing.md
Skill-7              6-QS-sentence/QS5-writing/QS5-writing.md
Skill-7-haipipe-writing.md           6-QS-sentence/QS5-writing/QS5-writing.md
# Design-5 folded into QS1 (260816): the sentence contract page carries the unit's skill/ plugin. The archived page sits at _archive/Design-5-haipipe-sentence/.
Design-5             6-QS-sentence/QS1-overview/QS1-overview.md
Design-5-haipipe-sentence.md         6-QS-sentence/QS1-overview/QS1-overview.md
Skill-4              6-QS-sentence/QS1-overview/QS1-overview.md
Skill-4-haipipe-sentence.md          6-QS-sentence/QS1-overview/QS1-overview.md
# 260815 evening fold: the chat faces, one file each, whole.
QPf4a                    4-QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md
QPf4b                    4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md
QPf4c                    4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md
QPf4d                    4-QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md
QA4                  1-QA-constitution/QA00-overview/QA00-overview.md
# 260815 evening: the chat migration. QO ids were REUSED in-lane
# (260801 precedent); the chat pages' morning ids resolve here.
QO1-chat-per-question.md 4-QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md
QO2-chat-sdk.md          4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md
QO3-chat-terminal.md     4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md
QO4-terminal-design.md   4-QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md
QO10                     8-QO-operating/QO6-whereitruns/QO6-whereitruns.md
QO11                     8-QO-operating/QO7-editlock/QO7-editlock.md
QO12                     8-QO-operating/QO8-consolescope/QO8-consolescope.md
QO13                     8-QO-operating/QO9-bindaddress/QO9-bindaddress.md
# 260815 restructure (JL): the ladder regroup. Every retired id
# resolves here; a reused number follows the 260801 precedent.
QB3                  4-QPf-page-folder/QPf1-folder/QPf1-folder.md
QB4                  3-QPs-page-structure/QPs1-overall/QPs1-overall.md
QB5                  5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md
QB6                  3-QPs-page-structure/QPs2-page-types/QPs2-page-types.md
QB7                  4-QPf-page-folder/QPf2-draw-attach/QPf2-draw-attach.md
QB8                  6-QS-sentence/QS1-overview/QS1-overview.md
QB8e                 6-QS-sentence/QS2-sentence-details-lifecycle/QS2-sentence-details-lifecycle.md
QBt1                 3-QPs-page-structure/QPs3-for-stage/QPs3-for-stage.md
# The slide TYPE died 260815 (JL: the slide is the plugin version, optional on
# every page); its QBt9 specimen is archived whole and QPf3 is now the plugin's page.
# The same evening QPs2 swept to the two-kind hub; its ten-type record is archived whole.
QBt10                3-QPs-page-structure/QPs4-for-design/QPs4-for-design.md
QC2c                 7-QC-engine/QC1c-livesplit/QC1c-livesplit.md
QC3b                 7-QC-engine/QC2b-meetingnote/QC2b-meetingnote.md
# QC4 was the round trip's id in the 260815 renumber and is now a LIVE page
# (the identity class, arrived from QA5 on 260816); the round trip is QC3.
QC4a                 7-QC-engine/QC3a-writepath/QC3a-writepath.md
QD1                  4-QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md
QD2                  4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md
QD3                  4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md
QD4                  4-QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md
QD5                  8-QO-operating/QO1-split-workspace/QO1-split-workspace.md
QD6                 8-QO-operating/QO2-session-status-strip/QO2-session-status-strip.md
QD7                  8-QO-operating/QO3-pagecost/QO3-pagecost.md
QD8                  6-QS-sentence/QS3-sentence-address/QS3-sentence-address.md
QE1                  8-QO-operating/QO4-hosting/QO4-hosting.md
QE2                  8-QO-operating/QO5-mountspace/QO5-mountspace.md
QE3                  8-QO-operating/QO6-whereitruns/QO6-whereitruns.md
QE4                  8-QO-operating/QO7-editlock/QO7-editlock.md
QE5                  8-QO-operating/QO8-consolescope/QO8-consolescope.md
QE6                  8-QO-operating/QO9-bindaddress/QO9-bindaddress.md
QF5                  6-QS-sentence/QS4-sentence-run/QS4-sentence-run.md
# the five paper-owned specimens moved to the paper board on 260809 (QB6 ruling A).
# Declared here so every citation on this board still resolves and still clicks.
QBt2                     ../PaperSkillBoard-260725/board/QBt/QBt2-for-venue.html
QBt3                     ../PaperSkillBoard-260725/board/QBt/QBt3-for-display.html
QBt4                     ../PaperSkillBoard-260725/board/QBt/QBt4-for-literature.html
QBt5                     ../PaperSkillBoard-260725/board/QBt/QBt5-for-value.html
QBt6                     ../PaperSkillBoard-260725/board/QBt/QBt6-for-section.html
QBt2-for-venue.md        ../PaperSkillBoard-260725/4-QBt-page-types/QBt2-for-venue/QBt2-for-venue.md
QBt3-for-display.md      ../PaperSkillBoard-260725/4-QBt-page-types/QBt3-for-display/QBt3-for-display.md
QBt4-for-literature.md   ../PaperSkillBoard-260725/4-QBt-page-types/QBt4-for-literature/QBt4-for-literature.md
QBt5-for-value.md        ../PaperSkillBoard-260725/4-QBt-page-types/QBt5-for-value/QBt5-for-value.md
QBt6-for-section.md      ../PaperSkillBoard-260725/4-QBt-page-types/QBt6-for-section/QBt6-for-section.md
QBt11 ../../../../subjective-label/diagram/SubjectiveLabelBoard-260722/8-QG-page-type/QG1-for-labeling/QG1-for-labeling.md
draw.py              ../../board/haipipe-board/cli/draw.py
test_linked_drawings.py ../../board/haipipe-board/tests/test_linked_drawings.py
live/xcal.py          ../../board/haipipe-board/live/xcal.py
board.excalidraw      board.excalidraw
8-QO-operating/draw/group.excalidraw 8-QO-operating/draw/group.excalidraw
QPf2a.excalidraw    4-QPf-page-folder/QPf2-draw-attach/draw/QPf2.excalidraw
QC5                 7-QC-engine/QC2-generate/QC2-generate.md
QC5a                7-QC-engine/QC2a-skill-to-page/QC2a-skill-to-page.md
QC5b                7-QC-engine/QC2b-meetingnote/QC2b-meetingnote.md
QC7                 7-QC-engine/QC3-roundtrip/QC3-roundtrip.md
QC7a                7-QC-engine/QC3a-writepath/QC3a-writepath.md
QC6                 1-QA-constitution/QA6-skillfamily/QA6-skillfamily.md
QC8                 7-QC-engine/QC1c-livesplit/QC1c-livesplit.md
QC9                 7-QC-engine/QC3-roundtrip/QC3-roundtrip.md
QC10                7-QC-engine/QC2b-meetingnote/QC2b-meetingnote.md
QDa1                4-QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md
QDa2                4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md
QDa3                4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md
QDa5                4-QPf-page-folder/QPf2-draw-attach/QPf2-draw-attach.md
QB9                 5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md
QB10                3-QPs-page-structure/QPs2-page-types/QPs2-page-types.md
QD13                8-QO-operating/QO1-split-workspace/QO1-split-workspace.md
QC5-pagecost        8-QO-operating/QO3-pagecost/QO3-pagecost.md
QD8-pagecost        8-QO-operating/QO3-pagecost/QO3-pagecost.md
# 260818 renumber (JL): the loop became the group holder, the hands moved to the tail.
# The bare keys QPw1 and QPw2 are deliberately NOT redirected: they are live pages
# now (QPw1-outline, QPw2-draft), and a redirect would shadow the real page.
QPw1-page-loop      5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md
QPw2-the-hands      5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
QPw7-the-hands      5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
# 260818 second renumber (JL: "if they are not follow, then it is not with w etc."):
# 7, 8 and 9 were never phases, so they lost their phase-shaped numbers and became
# subordinates of QPw00, the run, on the QPw4c/4v/4d precedent.
QPw7                5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
QPw7-page-agents    5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md
QPw8                5-QPw-page-workflow/QPw00r-receipts/QPw00r-receipts.md
QPw8-receipts       5-QPw-page-workflow/QPw00r-receipts/QPw00r-receipts.md
QPw9                5-QPw-page-workflow/QPw00g-human-gate/QPw00g-human-gate.md
QPw9-human-gate     5-QPw-page-workflow/QPw00g-human-gate/QPw00g-human-gate.md
QD14                4-QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md
QDa6                8-QO-operating/QO2-session-status-strip/QO2-session-status-strip.md
QDb1                8-QO-operating/QO4-hosting/QO4-hosting.md
QDb2                8-QO-operating/QO5-mountspace/QO5-mountspace.md
QDb3                8-QO-operating/QO6-whereitruns/QO6-whereitruns.md
QDb4                8-QO-operating/QO7-editlock/QO7-editlock.md
QDb5                8-QO-operating/QO8-consolescope/QO8-consolescope.md
QDb6                8-QO-operating/QO9-bindaddress/QO9-bindaddress.md
QD9                 8-QO-operating/QO6-whereitruns/QO6-whereitruns.md
QD10                8-QO-operating/QO7-editlock/QO7-editlock.md
QD11                8-QO-operating/QO8-consolescope/QO8-consolescope.md
QD12                8-QO-operating/QO9-bindaddress/QO9-bindaddress.md
# QA0 and QA1 folded into QA00, the introduction chapter (JL 260816):
# the words are its §4, the folders its §5. The archived pages sit whole
# at _archive/QA0-three-folders/ and _archive/QA1-concepts/.
QA0                  1-QA-constitution/QA00-overview/QA00-overview.md
QA1                  1-QA-constitution/QA00-overview/QA00-overview.md
QA1a                 1-QA-constitution/QA00-overview/QA00-overview.md
# The QA restructure (JL 260816): QA became the CONSTITUTION, one page per
# rung. QA5 moved to QC4 (it rules engine code), QA6a and QA6b folded into
# QA6 whole, and QA2 absorbed the close as QA2-board-life.
QA5                  7-QC-engine/QC4-identity-and-scope/QC4-identity-and-scope.md
QA5-identity-and-scope.md 7-QC-engine/QC4-identity-and-scope/QC4-identity-and-scope.md
QA6a                 1-QA-constitution/QA6-skillfamily/QA6-skillfamily.md
QA6b                 1-QA-constitution/QA6-skillfamily/QA6-skillfamily.md
QA2-question-group-design.md 1-QA-constitution/QA2-board-life/QA2-board-life.md
QA2b                2-QB-board/QB2-board-webpage-design/QB2-board-webpage-design.md
QAa0                3-QPs-page-structure/QPs1-overall/QPs1-overall.md
QB5e                6-QS-sentence/QS2-sentence-details-lifecycle/QS2-sentence-details-lifecycle.md
QB8d                6-QS-sentence/QS3-sentence-address/QS3-sentence-address.md
QAb3                6-QS-sentence/QS3-sentence-address/QS3-sentence-address.md
QAb0                6-QS-sentence/QS1-overview/QS1-overview.md
# (the row mapping QA6 to QB5b-comments left 260816: QA6 is a live page, and
#  the comments face still resolves through QB5b and QB8b below.)
QAb4                6-QS-sentence/QS2-sentence-details-lifecycle/QS2-sentence-details-lifecycle.md
QA9                 9-QF-execute/QF1-acceptance/QF1-acceptance.md
QA10                2-QB-board/QB2-board-webpage-design/QB2-board-webpage-design.md
QA8a                6-QS-sentence/QS3-sentence-address/QS3-sentence-address.md
SKILL.md            ../../board/haipipe-board/SKILL.md
build.py            ../../board/haipipe-board/cli/build.py
check.py            ../../board/haipipe-board/cli/check.py
status.py           ../../board/haipipe-board/status.py
watch.py            ../../board/haipipe-board/cli/watch.py
serve.py            ../../board/haipipe-board/cli/serve.py
stage.py            ../../board/haipipe-board/cli/stage.py
CHANGELOG.md        ../../board/haipipe-board/CHANGELOG.md
ref/                ../../board/haipipe-board/ref/
ref/page-template.md   ../../board/haipipe-board/ref/page-template.md
ref/board-form.md   ../../board/haipipe-board/ref/board-form.md
ref/writing-rules.md ../../board/haipipe-board/ref/writing-rules.md
ref/board-example.md ../../board/haipipe-board/ref/board-example.md
haipipe-board/      ../../board/haipipe-board/
board-family/       ../../board/
board-agents/       ../../board/agents/
haipipe-board-reviewer-agent.md ../../board/agents/haipipe-board-reviewer-agent.md
env.sh              ../../../../../../env.sh
paper-board/        ../PaperSkillBoard-260725/
QC0@paper           ../PaperSkillBoard-260725/6-QC-engine/QC5-sentence-evidence-contract/QC5-sentence-evidence-contract.md
QC1@paper           ../PaperSkillBoard-260725/3-QBe-delivery-element/QBe1-sentence-cite-value-display/QBe1-sentence-cite-value-display.md
QC2@paper           ../PaperSkillBoard-260725/3-QBe-delivery-element/QBe1-sentence-cite-value-display/QBe1-sentence-cite-value-display.md
QC3@paper           ../PaperSkillBoard-260725/3-QBe-delivery-element/QBe1-sentence-cite-value-display/QBe1-sentence-cite-value-display.md
QC4@paper           ../PaperSkillBoard-260725/3-QBe-delivery-element/QBe1-sentence-cite-value-display/QBe1-sentence-cite-value-display.md
QA1@paper           ../PaperSkillBoard-260725/1-QA-design/QA1-the-folder-map/QA1-the-folder-map.md
QA4@paper           ../PaperSkillBoard-260725/1-QA-design/QA4-the-board-tool/QA4-the-board-tool.md
src/dialect_paper.py ../../board/haipipe-board/src/dialect_paper.py
src/common.py       ../../board/haipipe-board/src/common.py
src/body.py         ../../board/haipipe-board/src/body.py
src/page_board.py   ../../board/haipipe-board/src/page_board.py
src/page_question.py ../../board/haipipe-board/src/page_question.py
assets/board-mark.svg ../../board/haipipe-board/assets/board-mark.svg
assets/css/        ../../board/haipipe-board/assets/css/
assets/js/         ../../board/haipipe-board/assets/js/
fig/board-mark-palettes.svg fig/board-mark-palettes.svg
haipipe-board/assets/js/ ../../board/haipipe-board/assets/js/
haipipe-paper-stage/ ../../paper/_old/haipipe-paper-stage/
0-lifecycle/        ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
SubjectiveLabelBoard-260722/ ../../../../subjective-label/diagram/SubjectiveLabelBoard-260722/
haichat-inlab/      ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/
main.py             ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/main.py
console_api.py      ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py
tasks_api.py        ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/tasks_api.py
labeling_api.py     ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/labeling_api.py
web/                ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/web/
docker-compose.yml  ../../../../../../platforms/HAIChat-SPACE/docker-compose.yml
