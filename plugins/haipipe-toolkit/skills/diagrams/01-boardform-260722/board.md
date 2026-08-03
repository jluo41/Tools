# /haipipe-board: pinning down what "a board" is, so it can be reused

spine: A board = one source folder. One Markdown file per page inside it, plus one generated board/ site with an Index, group pages, focused page files, and shared assets. Pin that shape down in SKILL.md so a fresh reader can open and run it without memory.
close: Every Q on this board reaches ✅ or ⏸️. SKILL.md is written, and a fresh agent with no background can read only that and open a decent board, and then this skill is done.
excalidraw: /_excalidraw
session: 2a45769d-85f8-4704-a30f-17adb2c82776
## Topic
What a board is for: a topic has several undecided questions; lay them out on one page anyone can open and comment on; settle them one by one, then close the board.
Cast: JL = the one who decides. CC = Claude Code, who does the work. Colleagues = the people who review, discuss, or take responsibility for work on the board; each uses their own initials.
What makes this board unusual: its subject IS the board itself, a board used to define boards.

## Pipeline
260802: QB5's five faces folded. QB5a, QB5b and QB5c became QB5's own `### 3` to `### 6` and were archived; QB5d moved to QD8, because a generated address is how a machine POINTS AT a location rather than a thing attached to a sentence; QB5e stayed its own page, since nothing in it is built and its identity question is open. Same shape and same answer as QB4's seven section faces on 260801.
Since 260731 every page id matches its group letter, and a parent page may carry faces as sub-letters. Neither QB4 nor QB5 does any more: QB4's seven section faces folded into its Content on 260801 and QB5's five followed on 260802, which is now the answer whenever a face stops carrying a subject of its own.
Every earlier id stays resolvable as a declared Link, so a citation written under any older naming still lands on the right page.
260731: ids aligned to groups (36 renames), and the Skill roster became its own page kind, `Skill-0` `Skill-1` `Skill-2`.
260731: QD split back into QD · Working and QE · Sharing (briefly QDa/QDb the same day), the archived board-agent page returned as QD7, and Execute moved to QF: a lowercase letter now always means a page's face, never a group.
260730: seven groups folded into five, and `## Board Map` above draws how the groups connect.
260729: the old QC group dissolved (its folder-management and proposal pages survive as today's QB3 and QA2), and the page/sentence faces split out into what are now QB4* and QB5*.
260725: the former QF group merged into QA, and its last page retired on 260726.

## Board Map
Which folders this board works with, how its seven groups connect, and the cross-group page edges that really exist.
Every id here is a link: a group token opens the index at that group, a page id opens the page.
`QA0` argues the folder map in full.

```text
─────────  ① the folders this board works with  ────────────────────────────────────

  ⚙️ ① skills/board/                          ONE folder, the family that SHIPS
       ├── haipipe-board/           the DOOR · SKILL.md src/ assets/ ref/ + 9 scripts
       ├── haipipe-board-page/      SPEC · what a page is
       ├── haipipe-board-page-for-skill/
       │                            SPEC · the VARIANT for skill and agent pages
       ├── haipipe-board-sentence/  SPEC + DOOR · one line · 3 verbs (260802)
       ├── haipipe-board-routing/   VERB · BOTH altitudes · src/lanes.py
       │                            board.md structure + one anchored write
       └── agents/                  haipipe-board-reviewer-agent.md
       🗑 haipipe-board-index/ merged into routing 260802 (JL ruled B)

  🗂 ② skills/diagrams/01-boardform-260722/    THIS board, what is ARGUED
       board.md · 7 group folders · 52 pages · board.excalidraw · fig/ · _archive/
       board/   📤 OUTPUT: Index · group pages · focused pages · shared assets

  📤 ③ every other board ① renders             what is RENDERED
       ⓐ skills/diagrams/01-*/            4 sibling design boards
       ⓑ <paper>/0-lifecycle/             a board that IS a tree
       ⓒ <unit>/diagram/<NN>-*/           a task or project board

  A subskill is a unit INSIDE ①, never a folder beside ②: it is a peer of the
  engine, not of the board. Every unit in ① is deletable from every other, and
  ② is deletable from all of them. `QA0` argues this in full.

─────────  ② how the groups connect  ───────────────────────────────────────────────

   what the system IS         what a reader GETS               how it is MADE
  ┌──────────────┐           ┌──────────────────────┐         ┌───────────────┐
  │ QA · Design  │──shapes──▶│ QB · Delivery        │◀─built──│ QC · Engine   │
  │ folders ·    │           │ Board → Group →      │   by    │ build · serve │
  │ concepts   4 │           │ Page → Section →     │         │ check · the   │
  └──────────────┘           │ Sentence           8 │         │ skill set  20 │
                             └──────────┬───────────┘         └───────┬───────┘
                                        │ operated live               │ every change
                                        ▼                             ▼ proves itself
  ┌──────────────────────┐ ┌──────────────────────┐  ┌───────────────┐
  │QD · Working with Chat│ │ QE · Sharing         │  │ QF · Execute  │
  │ session · chat ·     │ │ hosting · mounts ·   │  │ checker runs  │
  │ split panes ·        │ │ locks · console ·    │  │ fresh agent 5 │
  │ status strip       8 │ │ bind address       6 │  └───────────────┘
  └──────────────────────┘ └──────────────────────┘

─────────  ③ cross-group page edges  ───────────────────────────────────────────────

  QA0   ──places───▶  every folder above, and what may move between them
  QB2   ──renders──▶  the Index you are reading right now
  QB4   ──defines──▶  the base every page kind varies from
  QB4    ──owns─────▶  board.excalidraw, one scene per board
  QB3   ──places───▶  every page, inside its own home folder
  QC5   ──feeds────▶  Skill-0 · haipipe-board
  QF1 ──proves───▶  every page change · QF2 ──proves───▶ every skill revision

  every id above is a LINK · a plain token means no such page on this board
  a page's id now MATCHES its group; the old ids stay resolvable in `## Links`
```

[↗ the same map as a shared Excalidraw canvas](https://app.excalidraw.com/s/1JWkKv8oMIX/8OmxTBT2e1m?element=_Q20Q1taxY2jiainH_Y57)

## Related Folders
The folders this board touches: the engine that renders it, and what a board folder itself looks like. Open a folder and navigate it, the way you would browse a directory. QB2 owns the fold, QA0 owns which roots are listed; everything below a root is what is actually on disk.
@ ../../board/haipipe-board | ⚙️ haipipe-board · the engine that ships
@ . | 🗂 01-boardform-260722 · what a board folder looks like

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
The folder `01-boardform-260722/` contains `board.md` as the Board-level manifest, one descriptive group folder for each page group, one Markdown file per Q/S page, `board.excalidraw` as the local whole-Board scene, `fig/` for image assets, `_archive/` for retired pages, and generated `board/`.
Markdown decides which pages exist and what they say.
The canvas only records their visual placement and deliberately drawn relationship arrows.
Everything under `board/` is derived and is never hand-edited.

**Board-Webpage-Index — understand the Board before entering a page**
`board/index.html` begins with title, Spine, and Close condition.
Its Board Map makes relationships visible; Related Folders opens declared source files; the Section Matrix derives every page's section state; the textual roster remains the searchable way to choose work; Activity closes the Index.
Topic, Pipeline, and this Board Structure remain source-only documentation in `board.md`.
`QB2` owns it.

**Board-Webpage-Group — understand one group before entering a page**
`board/<GROUP>.html` shows the group's purpose, expandable explanation or lane diagram, progress, and page rows.

**Board-Webpage-Page — work on one page**
Opening a Q or S row goes to `board/<GROUP>/<page>.html`, one focused page with the shared sidebar.
With scripts on the router swaps that page into the current document so chat and terminal attachment survive; with scripts off the same link navigates normally.
`QB4`'s Content specifies each page section; `QB5` owns the sentence and everything written onto it, and `QB5e` owns the record lifecycle.

## Pages
### QA · Design
What the Board system IS, before any piece of it is built.
QA1 owns the words the family uses; QA2 owns how a topic becomes pages and groups in the first place; QA3 owns when an agent may hand a round back.
Still unwritten: the board types page (Skill-Board · Paper-Board · Task-Board), born when its content exists, not before.

```text
⚙️ ENGINE                      📋 PAGES · the working record        📂 FOLDER
─────────────────────────      ────────────────────────────────    ────────────────────────
ref/board-form.md §1       ◀── QA0  the folders and their kinds   ──▶  every folder above
ref/board-form.md          ◀── QA1  the words this family uses    ──▶  the shared vocabulary
?                          ◀── QA2  page and group proposals      ──▶  a new page + group folder
build.py check.py          ◀── QA3  the round's closing gate      ──▶  every reply to JL
```
QA0-three-folders.md
QA1-concepts.md
QA2-question-group-design.md
QA3-the-round.md
### QB · Delivery
What a reader gets, altitude by altitude: Board → Group → Page → Section → Sentence.
Board: QB1 the folder, QB2 the webpage and its Index (QB2a its pages sidebar), QB3 a page's home folder.
Page: QB4 the page template, whose Content specifies each section in turn, one division per section (the seven per-section faces were folded into it on 260801 and archived).
Sentence: QB5 the atomic unit, holding the card, the lanes, the remark and the edit in its own Content since the five faces folded on 260802; QB5e still owns the details lifecycle, and the generated address left for QD8.
Write affordance: QB8 attaches a drawing to the `## Diagram` section from the page, the write-half of QB4's Diagram section (moved from QD5, 260801).

```text
one page = one reading protocol · each section answers ONE reader question
──────────────────────────────────────────────────────────────────────
🧭 Opening · what is this page, and why should I care?
🖼 Diagram · can I see the whole subject at once, before reading?
📚 Content · what does this page actually establish?
🎯 Aims · which durable target states should this page establish?
📍 States · what is true now for each Aim, and which decision waits on JL?
📎 Files · which few files do I open to continue this work?
🗃 the folds · what was ruled, learned, and changed, if I need it?
──────────────────────────────────────────────────────────────────────
the order IS the protocol: intent, then substance, then status
all seven are specified in QB4's Content, one division each, and every
division uses the same five rows · conveys · holds · source · rules · omit
──────────────────────────────────────────────────────────────────────
around the page, the other altitudes this group owns
🏛 QB1 the board folder · QB2 the webpage index · QB2a the sidebar rail
📂 QB3 a page inside its own home folder · 📋 QB4 the shared Q/S frame
✏️ QB5 the sentence: two surfaces, one page · §3 card · §4 lanes ·
§5 remark · §6 edit · 📄 QB5e the details lifecycle, still its own
🖌 QB8 attach a drawing to the ## Diagram section, from the page (was QD5)
──────────────────────────────────────────────────────────────────────
the engine behind each row lives on that page's Files · code shape: QC2
```
QB1-form.md
QB2-board-webpage-design.md
QB2a-sidebar.md
QB3-folderq.md
QB4-overall.md
QB5-overview.md
QB5e-sentence-details-lifecycle.md
QB8-diagramattach.md
### QC · Engine
How the delivery is produced and shipped.
QC1 what the family ships (QC1a what SKILL.md must say, QC1b the sub-skill roster); QC2 the code's shape under one Law (QC2a assets out of build.py, QC2b the src/ split, QC2c the live-layer split); QC3 generating a page from something that exists outside the board (QC3a a skill folder, QC3b a meeting note); QC4 the whole round trip md to html and back (QC4a the write path's addressing contract).
One synced Skill page per shipped unit.
The family took QC1b §2's shape on 260731, lost a unit on 260802 and gained one the same day: one door (Skill-0 haipipe-board), two loadable SPECS (Skill-3 page, Skill-6 the skill-page variant), the sentence which became a DOOR + SPEC on 260802 (Skill-4), and the write VERB (Skill-5 routing), which absorbed the board and group altitude when JL ruled the index merged into it; the retired Skill-1 is in `_archive/` and its id still resolves, and digest is named on the roster and unshipped.
Skill-6 is `haipipe-board-page-for-skill`, opened because five roster Openings came out of one template: a Skill or Agent page mirrors a unit that ships elsewhere and DECIDES NOTHING, so the base Opening shape, which ends in what the page decides, left it with no question to ask.
Skill-7 is `haipipe-writing`, the roster's first row for a unit OUTSIDE `skills/board/` (JL 260802), which widens QC3a's 260727 scope ruling; it belongs because it owns `ref/writing-rules.md`, the prose standard every page here is judged against, and where the new line falls is a Decision Now row on QC3a.
Skill-8 is `haipipe-board-page-for-venue`, the SECOND variant of Skill-3 and the roster's second unit born by lifting a rule off the page that carried it (JL 260803, one day after Skill-6 was born the same way); it governs the QBv pages on the paper board, so it is the first roster row whose consumer is another board, and whether a variant of the base may ship beside the base when its consumer is elsewhere is the same open QC3a scope row that Skill-7 widened.
An AGENT is its own page kind below the skills (JL 260731: a skill is LOADED, an agent is DISPATCHED): Agent-1 is the fresh-context reviewer and Agent-2 the page creator, one page each so N run at once.
260801: renumbered contiguous QC1-QC4 (JL forced); the former QC5/QC7 generators and round-trip topics are now QC3/QC4, and every retired id resolves through the Links table.

```text
⚙️ ENGINE                       📋 PAGES · the working record            📂 FOLDER
──────────────────────────      ────────────────────────────────────    ────────────────────────
SKILL.md + the roster       ◀── QC1      the skill family ships        ──▶  skills/board/ units
SKILL.md                    ◀── QC1a     what SKILL.md must say        ──▶  SKILL.md
?                           ◀── QC1b     sub-skills roster             ──▶  the family's units
build.py src/ serve.py      ◀── QC2      the code's shape · one Law    ──▶  assets/ src/ live/
build.py                    ◀── QC2a     build.py's size               ──▶  assets/*.css  *.js
src/*.py                    ◀── QC2b     the src/ split                ──▶  src/ modules
serve.py  src/common.py     ◀── QC2c     splitting the live layer      ──▶  live/ modules + thin CLI
skillpage.py meetingpage.py ◀── QC3      a page from outside the board ──▶  Skill-*.md · a meeting page
skillpage.py                ◀── QC3a     skill folder -> skill page    ──▶  Skill-*.md
meetingpage.py              ◀── QC3b     a meeting note on the board   ──▶  the dated note file
build.py + live/write.py    ◀── QC4      the whole round trip          ──▶  board/ tree + the .md
serve.py _sentence_line     ◀── QC4a     the write path's anchor       ──▶  one line in one .md
skillpage.py sync           ◀── Skill-0  haipipe-board · the engine    ──▶  SKILL.md snapshot
skillpage.py new/sync       ◀── Skill-6  the SKILL-PAGE variant      ──▶  every Skill-* · Agent-*
skillpage.py sync           ◀── Skill-8  the VENUE-PAGE variant       ──▶  QBv-* on the PAPER board
skillpage.py sync           ◀── Skill-7  haipipe-writing · NEIGHBOUR  ──▶  skills/writing/, not board/
skillpage.py sync           ◀── Skill-3  the page SPEC                 ──▶  its SKILL.md snapshot
skillpage.py sync           ◀── Skill-4  the sentence SPEC             ──▶  its SKILL.md snapshot
skillpage.py sync           ◀── Skill-5  the write VERB, both altitudes──▶  its SKILL.md snapshot
skillpage.py sync           ◀── Agent-1  the fresh-context reviewer    ──▶  its definition .md
skillpage.py sync           ◀── Agent-2  the page creator, N at once   ──▶  one Q*.md per agent
```
QC1-skillfamily.md
QC1a-skillmd.md
QC1b-subskills.md
QC2-codeshape.md
QC2a-buildsplit.md
QC2b-srcsplit.md
QC2c-livesplit.md
QC3-generate.md
QC3a-skill-to-page.md
QC3b-meetingnote.md
QC4-roundtrip.md
QC4a-writepath.md
Skill-0-haipipe-board.md
Skill-3-haipipe-board-page.md
Skill-4-haipipe-board-sentence.md
Skill-5-haipipe-board-routing.md
Agent-1-haipipe-board-reviewer-agent.md
Agent-2-haipipe-board-creator-agent.md
Skill-6-haipipe-board-page-for-skill.md
Skill-7-haipipe-writing.md
Skill-8-haipipe-board-page-for-venue.md
### QD · Working with Chat
How people and agents work on a live board.
QD1 a session per question, QD2 the GUI chat version, QD3 the TUI chat version (raw pane + the smooth pane, QD3m merged in 260801), QD4 the terminal's form per device, QD5 operating the board as index, page and chat each refreshing on its own, QD6 the status strip, QD7 what a page costs to open and what we spend to make it less, and QD8 the generated address and what an agent acting on one is handed.
Numbers in this lane are POSITIONS, and the lane is renumbered to close its gaps (JL 260801: "为啥不按序号来排?").
The earlier rule was the opposite, that a number is a permanent address and a retired page leaves a hole, which is how six live pages came to be numbered up to QD14; the holes were doing more damage than the renumbering they were meant to prevent, because a reader cannot tell a gap from a missing page.
Renumbered 260801: QD14 (the terminal's form) became QD4 so it sits beside the engine it designs, and QD13 (the split workspace) became QD5; QD1, QD2, QD3 and QD6 did not move.
QD7 arrived from `QC` on 260802 (JL: "move it") and took the `QD7` position on 260802 when the empty `QD7-rejoin-bench` stub was archived, because this lane closes its gaps: what a page costs to open was opened in the engine lane because every lever is engine code, and moved here because WAITING is what stops the work and this lane is where the work happens. The rule it sets for the next page like it is that a lane is chosen by where a cost is FELT, not by which file holds its fix.
What the retired pages took with them is recorded here rather than in a gap: QD4 (live pages) was archived 260801 and its file keeps its own name, `_archive/QD4-liveupdate.md`; the drawing-attach page moved to QB as `QB8`; the board-level agent was archived once QD1 settled that a chat attaches at three levels; and the 260731 split into QE · Sharing carried off five more.
QD4 is QD3's design half, split out on 260801 when the terminal proved hard to use on a phone: QD3 owns the engine and QD4 owns the FORM, meaning where typing happens, what the pane shows when 80 columns will not fit, and what the page owes a reader who switches away and comes back.
QD5 asks whether the board should be operated as three side-by-side panes (index · page · chat) rather than as one html document that swaps its own middle; it measured the four causes of the unsmooth refresh, ruled the mechanism as three same-origin iframes in one shell page on 260801, and is the successor to the archived live-update page's in-place-swap approach.

```text
⚙️ ENGINE                      📋 PAGES · the working record         📂 FOLDER
─────────────────────────      ─────────────────────────────────    ────────────────────────
serve.py                   ◀── QD1   a session per question        ──▶  session: in board.md
assets/board.js #chat      ◀── QD2   GUI · the chat box            ──▶  live replies
serve.py                   ◀── QD3   terminal · raw + smooth panes ──▶  a real CLI session
30-terminal.js             ◀── QD4   the terminal's FORM per device──▶  phone · desktop
serve.py build.py          ◀── QD5   each pane refreshes on its own──▶  index · page · chat
serve.py                   ◀── QD6   the reply status strip        ──▶  every reply's footer
serve.py live/activity.py  ◀── QD7   what a page COSTS to open     ──▶  bytes · lanes · the browser
```
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD4-terminal-design.md
QD5-split-workspace.md
QD6-session-status-strip.md
QD7-pagecost.md
QD8-sentence-address.md
### QE · Sharing
How a board is hosted, mounted, and opened by someone who is not its author.

```text
⚙️ ENGINE                      📋 PAGES · the working record        📂 FOLDER
─────────────────────────      ────────────────────────────────    ────────────────────────
serve.py                   ◀── QE1  hosting · local vs server     ──▶  the served URL
serve.py mounts            ◀── QE2  mounting a SPACE              ──▶  /Tools/... paths
serve.py                   ◀── QE3  where the board runs          ──▶  host + port
serve.py                   ◀── QE4  in-page editing and locks     ──▶  the lock records
?                          ◀── QE5  place in the console          ──▶  console rows
serve.py                   ◀── QE6  which address it binds to     ──▶  tailnet :5599
```
QE1-hosting.md
QE2-mountspace.md
QE3-whereitruns.md
QE4-editlock.md
QE5-consolescope.md
QE6-bindaddress.md
### QF · Execute
What actually RAN, with evidence and a reopen path: the layer that keeps "skill written, delivery defined" from passing as done.
QF1 is the per-change page gate: deterministic `check.py` plus the fresh page reviewer. QF2 is the separate fresh-agent usability acceptance for a revised skill; QF3 drives the built page in a real browser; QF4 drives the chat inside it. QF5 is the sentence run: every shape a sentence can take, crossed with every operation that writes one.
An execute record names its route, its result, and what it refused to touch.

```text
⚙️ ENGINE                      📋 PAGES · the working record        📂 FOLDER
─────────────────────────      ────────────────────────────────    ────────────────────────
check.py + page reviewer   ◀── QF1  page gate after every change  ──▶  mechanics + prose verdict
fresh skill agent          ◀── QF2  revised-skill usability       ──▶  acceptance verdict
```
QF1-acceptance.md
QF2-newcomer.md
QF3-browser-run.md
QF4-talk-run.md
QF5-sentence-run.md
### QG · Meeting
What was said out loud, kept where it can be cited.
One page per meeting, imported from an `echo-meeting` vault note by `meetingpage.py`: the summary is the reading path, the raw transcript is reference, and the decisions inside it are routed onto the pages that own them.
This group ACCUMULATES, which is why it is a group rather than a few rows inside `QD`: a roster of shipped units has a natural size, a history of meetings does not.
`QC3b` rules how a note becomes one of these pages.

Meeting-1-260723-boardform-demo.md

## Links
QC5                 QC-engine/QC3-generate.md
QC5a                QC-engine/QC3a-skill-to-page.md
QC5b                QC-engine/QC3b-meetingnote.md
QC7                 QC-engine/QC4-roundtrip.md
QC7a                QC-engine/QC4a-writepath.md
QC6                 QC-engine/QC1b-subskills.md
QC8                 QC-engine/QC2c-livesplit.md
QC9                 QC-engine/QC4-roundtrip.md
QC10                QC-engine/QC3b-meetingnote.md
QD3m                QD-working/_archive/QD3m-smooth-terminal.md
QDa1                QD-working/QD1-chat-per-question.md
QDa2                QD-working/QD2-chat-sdk.md
QDa3                QD-working/QD3-chat-terminal.md
QDa4                QD-working/_archive/QD4-liveupdate.md
QD4-liveupdate      QD-working/_archive/QD4-liveupdate.md
QDa5                QB-delivery/QB8-diagramattach.md
QD13                QD-working/QD5-split-workspace.md
QC5-pagecost        QD-working/QD7-pagecost.md
QD8-pagecost        QD-working/QD7-pagecost.md
QD14                QD-working/QD4-terminal-design.md
QDa6                QD-working/QD6-session-status-strip.md
QDa7                QD-working/_archive/QD7-boardagent.md
QDb1                QE-sharing/QE1-hosting.md
QDb2                QE-sharing/QE2-mountspace.md
QDb3                QE-sharing/QE3-whereitruns.md
QDb4                QE-sharing/QE4-editlock.md
QDb5                QE-sharing/QE5-consolescope.md
QDb6                QE-sharing/QE6-bindaddress.md
QD9                 QE-sharing/QE3-whereitruns.md
QD10                QE-sharing/QE4-editlock.md
QD11                QE-sharing/QE5-consolescope.md
QD12                QE-sharing/QE6-bindaddress.md
QB6                 QC-engine/QC3a-skill-to-page.md
QB7                 QC-engine/QC1b-subskills.md
Q-Skill-haipipe-board                QC-engine/Skill-0-haipipe-board.md
Q-Skill-haipipe-board-index          _archive/Skill-1-haipipe-board-index.md
Skill-1              _archive/Skill-1-haipipe-board-index.md
Q-Skill-haipipe-board-reviewer-agent QC-engine/Agent-1-haipipe-board-reviewer-agent.md
Skill-2              QC-engine/Agent-1-haipipe-board-reviewer-agent.md
QA1a                QA-design/QA1-concepts.md
QA2b                QB-delivery/QB2-board-webpage-design.md
QAa0                QB-delivery/QB4-overall.md
QAa1                QB-delivery/_archive/QB4a-opening.md
QAa2                QB-delivery/_archive/QB4b-diagram.md
QAa3                QB-delivery/_archive/QB4c-content.md
QAa4                QB-delivery/_archive/QB4d-items.md
QAa5                QB-delivery/_archive/QB4e-where-we-are.md
QAa7                QB-delivery/_archive/QB4f-files.md
QAa6                QB-delivery/_archive/QB4g-folds.md
QB5a                QB-delivery/_archive/QB5a-evidence-card.md
QB5b                QB-delivery/_archive/QB5b-comments.md
QB5c                QB-delivery/_archive/QB5c-editing.md
QB5d                QD-working/QD8-sentence-address.md
QAb1                QB-delivery/_archive/QB5a-evidence-card.md
QAb2                QB-delivery/_archive/QB5c-editing.md
QAb3                QD-working/QD8-sentence-address.md
QB4a                QB-delivery/_archive/QB4a-opening.md
QB4b                QB-delivery/_archive/QB4b-diagram.md
QB4c                QB-delivery/_archive/QB4c-content.md
QB4d                QB-delivery/_archive/QB4d-items.md
QB4e                QB-delivery/_archive/QB4e-where-we-are.md
QB4f                QB-delivery/_archive/QB4f-files.md
QB4g                QB-delivery/_archive/QB4g-folds.md
QAb0                QB-delivery/QB5-overview.md
QA6                 QB-delivery/_archive/QB5b-comments.md
QAb4                QB-delivery/QB5e-sentence-details-lifecycle.md
QA9                 QF-execute/QF1-acceptance.md
QA10                QB-delivery/QB2-board-webpage-design.md
QA4                 QB-delivery/QB4-overall.md
QA4a                QB-delivery/_archive/QB4b-diagram.md
QA8                 QB-delivery/_archive/QB5a-evidence-card.md
QA8a                QD-working/QD8-sentence-address.md
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
paper-board/        ../01-haipipe-paper-260725/
QC0@paper           ../01-haipipe-paper-260725/QC-engine/QC5-sentence-evidence-contract.md
QC1@paper           ../01-haipipe-paper-260725/QBe-delivery-element/QBe1-sentence-cite-value-display.md
QC2@paper           ../01-haipipe-paper-260725/QBe-delivery-element/QBe1-sentence-cite-value-display.md
QC3@paper           ../01-haipipe-paper-260725/QBe-delivery-element/QBe1-sentence-cite-value-display.md
QC4@paper           ../01-haipipe-paper-260725/QBe-delivery-element/QBe1-sentence-cite-value-display.md
QA1@paper           ../01-haipipe-paper-260725/QA-design/QA1-the-folder-map.md
QA4@paper           ../01-haipipe-paper-260725/QA-design/QA4-the-board-tool.md
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
haipipe-paper-stage/ ../../paper/1-lifecycle/haipipe-paper-stage/
0-lifecycle/        ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
02-method-260722/   ../../../../subjective-label/diagram/02-method-260722/
haichat-inlab/      ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/
main.py             ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/main.py
console_api.py      ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py
tasks_api.py        ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/tasks_api.py
labeling_api.py     ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/labeling_api.py
web/                ../../../../../../platforms/HAIChat-SPACE/haichat-inlab/web/
docker-compose.yml  ../../../../../../platforms/HAIChat-SPACE/docker-compose.yml
