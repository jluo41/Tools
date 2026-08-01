# /haipipe-board: pinning down what "a board" is, so it can be reused

spine: A board = one folder. One markdown file per question inside it, plus one HTML page anyone can open. Pin that shape down, write it into SKILL.md, so someone else (and a future me with no memory) can open a board by following it.
close: Every Q on this board reaches ✅ or ⏸️. SKILL.md is written, and a fresh agent with no background can read only that and open a decent board, and then this skill is done.
excalidraw: /_excalidraw
session: 3e951d68-1c6d-4f22-af82-76dd70bb356d
## Topic
What a board is for: a topic has several undecided questions; lay them out on one page anyone can open and comment on; settle them one by one, then close the board.
Cast: JL = the one who decides. CC = Claude Code, who does the work. Colleagues = the people who review, discuss, or take responsibility for work on the board; each uses their own initials.
What makes this board unusual: its subject IS the board itself, a board used to define boards.

## Pipeline
Since 260731 every page id matches its group letter, and a parent page carries its faces as sub-letters: QB4 is the page, QB4a-QB4g its sections; QB5 the sentence, QB5a-QB5e what attaches to it.
Every earlier id stays resolvable as a declared Link, so a citation written under any older naming still lands on the right page.
260731: ids aligned to groups (36 renames), and the Skill roster became its own page kind, `Skill-0` `Skill-1` `Skill-2`.
260731: QD split back into QD · Working and QE · Sharing (briefly QDa/QDb the same day), the archived board-agent page returned as QD7, and Execute moved to QF: a lowercase letter now always means a page's face, never a group.
260730: seven groups folded into five, and `## Board Map` above draws how the groups connect.
260729: the old QC group dissolved (its folder-management and proposal pages survive as today's QB3 and QA2), and the page/sentence faces split out into what are now QB4* and QB5*.
260725: the former QF group merged into QA, and its last page retired on 260726.

## Board Map
Which folders this board works with, how its five groups connect, and the cross-group page edges that really exist.
Every id here is a link: a group token opens the index at that group, a page id opens the page.
`QA0` argues the folder map in full.

```text
─────────  ① the folders this board works with  ────────────────────────────────────

  ⚙️ ① skills/board/                          ONE folder, the family that SHIPS
       ├── haipipe-board/           the DOOR · SKILL.md src/ assets/ ref/ + 9 scripts
       ├── haipipe-board-index/     board + group altitude · lanes.py
       ├── haipipe-board-page/      SPEC · what a page is
       ├── haipipe-board-sentence/  SPEC · the atomic unit and its records
       ├── haipipe-board-routing/   VERB · one input -> one anchored write
       └── agents/                  haipipe-board-reviewer-agent.md

  🗂 ② skills/diagrams/01-boardform-260722/    THIS board, what is ARGUED
       board.md · 6 group folders · 44 pages · board.excalidraw · fig/ · _archive/
       board.html   📤 OUTPUT, never hand-edited

  📤 ③ every other board ① renders             what is RENDERED
       ⓐ skills/diagrams/01-*/            4 sibling design boards
       ⓑ <paper>/0-lifecycle/             a board that IS a tree
       ⓒ <unit>/diagram/<NN>-*/           a task or project board

  A subskill is a unit INSIDE ①, never a folder beside ②: it is a peer of the
  engine, not of the board. Every unit in ① is deletable from every other, and
  ② is deletable from all of them. `QA0` argues this in full.

─────────  ② how the five groups connect  ──────────────────────────────────────────

   what the system IS         what a reader GETS               how it is MADE
  ┌──────────────┐           ┌──────────────────────┐         ┌───────────────┐
  │ QA · Design  │──shapes──▶│ QB · Delivery        │◀─built──│ QC · Engine   │
  │ folders ·    │           │ Board → Group →      │   by    │ build · serve │
  │ concepts   3 │           │ Page → Section →     │         │ check · the   │
  └──────────────┘           │ Sentence          17 │         │ skill set   9 │
                             └──────────┬───────────┘         └───────┬───────┘
                                        │ operated live               │ every change
                                        ▼                             ▼ proves itself
  ┌──────────────────────┐ ┌──────────────────────┐  ┌───────────────┐
  │ QD · Working         │ │ QE · Sharing         │  │ QF · Execute  │
  │ session · chat ·     │ │ hosting · mounts ·   │  │ checker runs  │
  │ live updates · the   │ │ locks · console ·    │  │ fresh agent 2 │
  │ board agent        7 │ │ bind address       6 │  └───────────────┘
  └──────────────────────┘ └──────────────────────┘

─────────  ③ cross-group page edges  ───────────────────────────────────────────────

  QA0   ──places───▶  every folder above, and what may move between them
  QB2   ──renders──▶  the Index you are reading right now
  QB4   ──defines──▶  the base every page kind varies from
  QB4b   ──owns─────▶  board.excalidraw, one scene per board
  QB3   ──places───▶  every page, inside its own home folder
  QC5   ──feeds────▶  Skill-0 · haipipe-board
  QF1 + QF2 ─prove─▶  every change, before it ships

  every id above is a LINK · a plain token means no such page on this board
  a page's id now MATCHES its group; the old ids stay resolvable in `## Links`
```

[↗ the same map as a shared Excalidraw canvas](https://app.excalidraw.com/s/1JWkKv8oMIX/8OmxTBT2e1m?element=_Q20Q1taxY2jiainH_Y57)

## Related Folders
The folders this board touches: the engine that renders it, and what a board folder itself looks like. Click a folder, then a file, to read it right here. QB2 owns the fold, QA0 owns this list.
@ ../../board/haipipe-board | ⚙️ haipipe-board · the engine that ships
- SKILL.md
- ref/board-form.md
@ . | 🗂 01-boardform-260722 · what a board folder looks like
- board.md
- QA-design/QA0-three-folders.md

## Board Structure
This Board has one source `Board-Folder` and one generated `Board-Webpage`.
The map is part of the Board-Webpage-Index, not a third peer object, not another Q page, and not part of the settled-question count.

```text
📂 Board-Folder ──build.py──▶ 🌐 board.html : 🗂 Index #top ─▶ 📋 Page #<id> ─▶ ✍️ sentence
```

**Board-Folder — what exists and can be changed**
The folder `01-boardform-260722/` contains `board.md` as the Board-level manifest, one group folder for each page group, one Markdown file per Q/S page, `board.excalidraw` as the local whole-Board scene, `fig/` for image assets, `_archive/` for retired pages, and generated `board.html`.
Markdown decides which pages exist and what they say.
The canvas only records their visual placement and deliberately drawn relationship arrows.
`board.html` is derived and is never hand-edited.

**Board-Webpage-Index — understand the Board before entering a page**
The top view begins with title, Spine, Close condition, and progress.
Its Board Map then makes page relationships visible: each box is one Q/S page and an arrow is an explicitly authored, labelled relation, never an inference from page order.
This static Board loads its shared `board-map:` canvas; a live Board server defaults to the local `board.excalidraw` scene.
The textual index remains below the map because it is the searchable, accessible way to choose work.
Topic, Pipeline, this Board-Structure block, and Activity complete the Index.
`QB2` owns it.

**Board-Webpage-Page — work on one page**
Opening a Q or S row changes the same `board.html` document to `#<page-id>`, one focused page.
`QB4a`-`QB4g` own that page's sections; `QB5`-`QB5e` own the sentence and its attached records.

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
Page: QB4 the shared Q/S base, with one face per section: QB4a Opening, QB4b Diagram, QB4c Content, QB4d Items to Finish, QB4e Where we are, QB4f Files, QB4g the folds.
Sentence: QB5 the atomic unit, with QB5a the evidence card, QB5b comments, QB5c editing, QB5d chat, QB5e the details lifecycle.

```text
⚙️ ENGINE                      📋 PAGES · the working record         📂 FOLDER
─────────────────────────      ─────────────────────────────────    ────────────────────────
src/parse.py               ◀── QB1   the folder structure          ──▶  board.md · group folders/
src/page_board.py          ◀── QB2   Board-Webpage Design          ──▶  board.html  #top
page_board.py sidebar      ◀── QB2a  the pages sidebar             ──▶  the fixed left rail
assets/board.css
src/parse.py page_files    ◀── QB3   page folder management        ──▶  <page>/ home folder
src/page_question.py       ◀── QB4   the shared Q/S layout         ──▶  every Q*.md and S*.md
ref/q-template.md
render_structure()         ◀── QB4a  Opening · head and door       ──▶  the drawer above the read
xcal.py  split_diagram()   ◀── QB4b  Diagram · figure + canvas     ──▶  board.excalidraw · fig/
parse_content_sections()   ◀── QB4c  Content · divisions           ──▶  ### divisions in a page
render_question()          ◀── QB4d  Items · the testable gap      ──▶  - [ ] boxes
render_question()          ◀── QB4e  Where we are · state mirror   ──▶  dated state lines
sect('Files')              ◀── QB4f  Files · action map            ──▶  ## Files rows
det()                      ◀── QB4g  folds · the drawer            ──▶  Discussion Law Lesson Log
src/body.py                ◀── QB5   the atomic unit               ──▶  one sentence, one anchor
src/body.py CARDS          ◀── QB5a  the evidence card             ──▶  popover panels
assets/board.js  serve.py  ◀── QB5b  sentence-local comments       ──▶  the comment records
serve.py write path        ◀── QB5c  editing a sentence            ──▶  the page .md itself
assets/board.js #chat      ◀── QB5d  chat about one location       ──▶  a session per location
serve.py                   ◀── QB5e  details lifecycle             ──▶  archive / restore records
```
QB1-form.md
QB2-board-webpage-design.md
QB2a-sidebar.md
QB3-folderq.md
QB4-overall.md
QB4a-opening.md
QB4b-diagram.md
QB4c-content.md
QB4d-items.md
QB4e-where-we-are.md
QB4f-files.md
QB4g-folds.md
QB5-overview.md
QB5a-evidence-card.md
QB5b-comments.md
QB5c-editing.md
QB5d-agent-visibility.md
QB5e-sentence-details-lifecycle.md
### QC · Engine
How the delivery is produced and shipped.
QC1 what SKILL.md must say; QC2 and QC3 the code's shape (assets out of build.py, then the src/ split); QC4 migrating the older boards; QC5 how a skill folder becomes a synced page; QC6 the sub-skill roster; QC7 the write path's addressing contract; QC9 the whole round trip, md to html and back; QC8 splitting the live layer the way QC3 split the render layer; QC10 how a meeting note enters a board, as an artifact and as routed consequences.
One synced Skill page per shipped unit.
The family took QC6 §8's shape on 260731: one door (Skill-0 haipipe-board), the board+group altitude (Skill-1 index), two loadable SPECS (Skill-3 page, Skill-4 sentence), and the write-back VERB (Skill-5 routing); digest is named on the roster and unshipped.
An AGENT is its own page kind below the skills (JL 260731: a skill is LOADED, an agent is DISPATCHED): Agent-1 is the fresh-context reviewer and Agent-2 the page creator, one page each so N run at once.

```text
⚙️ ENGINE                      📋 PAGES · the working record            📂 FOLDER
─────────────────────────      ────────────────────────────────────    ────────────────────────
SKILL.md                   ◀── QC1      what SKILL.md must say        ──▶  SKILL.md
build.py                   ◀── QC2      build.py's size               ──▶  assets/*.css  *.js
src/*.py                   ◀── QC3      the src/ split                ──▶  src/ modules
build.py                   ◀── QC4      migrate the old boards        ──▶  the two older boards
skillpage.py               ◀── QC5      skill folder -> skill page    ──▶  Skill-*.md
?                          ◀── QC6      sub-skills roster             ──▶  the family's units
serve.py _sentence_line    ◀── QC7      the write path's anchor       ──▶  one line in one .md
serve.py  src/common.py    ◀── QC8      splitting the live layer      ──▶  live/ modules + thin CLI
build.py + live/write.py   ◀── QC9      the whole round trip          ──▶  _site/ tree + the .md
skillpage.py sync          ◀── Skill-0  haipipe-board · the engine    ──▶  SKILL.md snapshot
skillpage.py sync          ◀── Skill-1  haipipe-board-index           ──▶  its SKILL.md snapshot
skillpage.py sync          ◀── Skill-3  the page SPEC                 ──▶  its SKILL.md snapshot
skillpage.py sync          ◀── Skill-4  the sentence SPEC             ──▶  its SKILL.md snapshot
skillpage.py sync          ◀── Skill-5  the routing VERB              ──▶  its SKILL.md snapshot
skillpage.py sync          ◀── Agent-1  the fresh-context reviewer    ──▶  its definition .md
skillpage.py sync          ◀── Agent-2  the page creator, N at once   ──▶  one Q*.md per agent
```
QC1-skillmd.md
QC2-buildsplit.md
QC3-srcsplit.md
QC4-migrate.md
QC5-skill-to-page.md
QC6-subskills.md
QC7-writepath.md
QC8-livesplit.md
QC9-roundtrip.md
QC10-meetingnote.md
Skill-0-haipipe-board.md
Skill-1-haipipe-board-index.md
Skill-3-haipipe-board-page.md
Skill-4-haipipe-board-sentence.md
Skill-5-haipipe-board-routing.md
Agent-1-haipipe-board-reviewer-agent.md
Agent-2-haipipe-board-creator-agent.md
Meeting-1-260723-boardform-demo.md
### QD · Working
How people and agents work on a live board.
QD1 a session per question, QD2 the chat box, QD3 the real CLI (raw pane + the smooth pane, QD3m merged in 260801), QD4 live updates, QD5 attaching a drawing, QD6 the status strip, and QD7 the board-level agent (restored from the archive 260731: board-wide work such as adding pages and regrouping is working-layer work).

```text
⚙️ ENGINE                      📋 PAGES · the working record         📂 FOLDER
─────────────────────────      ─────────────────────────────────    ────────────────────────
serve.py                   ◀── QD1   a session per question        ──▶  session: in board.md
assets/board.js #chat      ◀── QD2   SDK · the chat box            ──▶  live replies
serve.py                   ◀── QD3   terminal · raw + smooth panes ──▶  a real CLI session
watch.py                   ◀── QD4   live page updates             ──▶  rebuilt board.html
xcal.py  serve.py          ◀── QD5   attach a drawing              ──▶  fig/ · board.excalidraw
serve.py                   ◀── QD6   board attachment in replies   ──▶  every reply's footer
serve.py sessions          ◀── QD7   the board-level agent         ──▶  a whole-board session
```
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD4-liveupdate.md
QD5-diagramattach.md
QD6-session-status-strip.md
QD7-boardagent.md
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
QF1 is the checker that runs after every change; QF2 is the fresh-agent acceptance run; QF3 drives the built page in a real browser; QF4 drives the chat inside it.
An execute record names its route, its result, and what it refused to touch.

```text
⚙️ ENGINE                      📋 PAGES · the working record        📂 FOLDER
─────────────────────────      ────────────────────────────────    ────────────────────────
check.py                   ◀── QF1  checking after every change   ──▶  the 0-error report
?                          ◀── QF2  fresh-agent acceptance        ──▶  the acceptance verdict
```
QF1-acceptance.md
QF2-newcomer.md
QF3-browser-run.md
QF4-talk-run.md
## Links
QD3m                QD-working/_archive/QD3m-smooth-terminal.md
QDa1                QD-working/QD1-chat-per-question.md
QDa2                QD-working/QD2-chat-sdk.md
QDa3                QD-working/QD3-chat-terminal.md
QDa4                QD-working/QD4-liveupdate.md
QDa5                QD-working/QD5-diagramattach.md
QDa6                QD-working/QD6-session-status-strip.md
QDa7                QD-working/QD7-boardagent.md
QDb1                QE-sharing/QE1-hosting.md
QDb2                QE-sharing/QE2-mountspace.md
QDb3                QE-sharing/QE3-whereitruns.md
QDb4                QE-sharing/QE4-editlock.md
QDb5                QE-sharing/QE5-consolescope.md
QDb6                QE-sharing/QE6-bindaddress.md
QD7                 QE-sharing/QE1-hosting.md
QD8                 QE-sharing/QE2-mountspace.md
QD9                 QE-sharing/QE3-whereitruns.md
QD10                QE-sharing/QE4-editlock.md
QD11                QE-sharing/QE5-consolescope.md
QD12                QE-sharing/QE6-bindaddress.md
QB6                 QC-engine/QC5-skill-to-page.md
QB7                 QC-engine/QC6-subskills.md
Q-Skill-haipipe-board                QC-engine/Skill-0-haipipe-board.md
Q-Skill-haipipe-board-index          QC-engine/Skill-1-haipipe-board-index.md
Q-Skill-haipipe-board-reviewer-agent QC-engine/Agent-1-haipipe-board-reviewer-agent.md
Skill-2              QC-engine/Agent-1-haipipe-board-reviewer-agent.md
QA1a                QA-design/QA1-concepts.md
QA2b                QB-delivery/QB2-board-webpage-design.md
QAa0                QB-delivery/QB4-overall.md
QAa1                QB-delivery/QB4a-opening.md
QAa2                QB-delivery/QB4b-diagram.md
QAa3                QB-delivery/QB4c-content.md
QAa4                QB-delivery/QB4d-items.md
QAa5                QB-delivery/QB4e-where-we-are.md
QAa7                QB-delivery/QB4f-files.md
QAa6                QB-delivery/QB4g-folds.md
QAb0                QB-delivery/QB5-overview.md
QAb1                QB-delivery/QB5a-evidence-card.md
QA6                 QB-delivery/QB5b-comments.md
QAb2                QB-delivery/QB5c-editing.md
QAb3                QB-delivery/QB5d-agent-visibility.md
QAb4                QB-delivery/QB5e-sentence-details-lifecycle.md
QA9                 QF-execute/QF1-acceptance.md
QA10                QB-delivery/QB2-board-webpage-design.md
QA4                 QB-delivery/QB4-overall.md
QA4a                QB-delivery/QB4b-diagram.md
QA8                 QB-delivery/QB5a-evidence-card.md
QA8a                QB-delivery/QB5d-agent-visibility.md
SKILL.md            ../../board/haipipe-board/SKILL.md
build.py            ../../board/haipipe-board/build.py
check.py            ../../board/haipipe-board/check.py
status.py           ../../board/haipipe-board/status.py
watch.py            ../../board/haipipe-board/watch.py
serve.py            ../../board/haipipe-board/serve.py
stage.py            ../../board/haipipe-board/stage.py
CHANGELOG.md        ../../board/haipipe-board/CHANGELOG.md
ref/                ../../board/haipipe-board/ref/
ref/q-template.md   ../../board/haipipe-board/ref/q-template.md
ref/board-form.md   ../../board/haipipe-board/ref/board-form.md
ref/writing-rules.md ../../board/haipipe-board/ref/writing-rules.md
ref/board-example.md ../../board/haipipe-board/ref/board-example.md
haipipe-board/      ../../board/haipipe-board/
board-family/       ../../board/
board-agents/       ../../board/agents/
haipipe-board-reviewer-agent.md ../../board/agents/haipipe-board-reviewer-agent.md
env.sh              ../../../../../../env.sh
paper-board/        ../01-haipipe-paper-260725/
QC0@paper           ../01-haipipe-paper-260725/QC-engine-page-and-sentence-contract/QC0-sentence-unit.md
QC1@paper           ../01-haipipe-paper-260725/QI-delivery-literature/QC1-sentence-citation.md
QC2@paper           ../01-haipipe-paper-260725/QJ-delivery-value/QC2-sentence-value.md
QC3@paper           ../01-haipipe-paper-260725/QK-delivery-display/QC3-sentence-display-table.md
QC4@paper           ../01-haipipe-paper-260725/QK-delivery-display/QC4-sentence-display-figure.md
QA1@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA1-eight-folders.md
QA4@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA4-the-board-tool.md
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
