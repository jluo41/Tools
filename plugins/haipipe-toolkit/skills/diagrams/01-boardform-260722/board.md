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
Seven groups; the letter in each page's id is the group it was OPENED under, so after the 260729
restructure a page may be listed under a newer group than its letter (QA6, QC2, QC3 and QC4
kept their ids when they moved, because the skill and other boards cite them; QA2 moved with its
id and then merged into the QAa faces the same day, so it is archived). QA defines the
thing; QAa owns the page, one face per section; QAb owns the sentence. Those three are the main
line. QB ships it; QD and QE own the live and shared layers and can be thought about in parallel.
The former QC group (Index and structure) dissolved on 260729: QC1 merged into QA1, QC2 into QA10,
QC3 joined QA and was renamed to page folder management, and QC4 joined QAa. The former
"QF · A board on top of other formats" group merged into QA on 260725 and its last page was
retired on 260726, so no QF id remains.

## Pages
### QA · Defining a board
The board itself: its map, its vocabulary, its index, and its checks.
QA0 is this board's own structure (and the convention that every board opens with one, JL
260729). QA1 maps the family's two folders and, since 260729, absorbs QC1: where a board folder
lives and what it is named. QA1a owns the words the family uses. QC3 owns page folder management,
a page living inside its subject folder. QA9 owns what is checked after any change. QA10 owns the
index page and the board's visual design, absorbing QC2 on 260729. The page sections and the
sentence left this group the same day for QAa and QAb.
QA0-board-map.md
QA1-form.md
QA1a-concepts.md
QC3-folderq.md
QA9-acceptance.md
QA10-ui-taste.md
### QAa · The page, section by section
One face per section of the shared Q/S page (JL 260729). QAa0 keeps the fixed on-stage order,
the two-workflow rule, and the Board mark; it is the former QA4 and keeps that page's history.
The source template `ref/q-template.md` is QAa0's since QA2 merged into these faces on 260729: each face owns its section in both projections, the source you write and the render you read.
QAa0 also records the base/variant model (JL 260729): the page is a base, a page kind (Question, Stage, the Skill roster; Display and Task as candidates) redefines only its Content structure, and variants ship under their consumer families such as `haipipe-paper-stage`. QAa1 owns Opening, QAa2 Diagram plus the
one-canvas-per-board scene (absorbing the former QA4a), QAa3 Content with the group-title
marker, QAa4 Items to Finish, QAa5 Where we are with the new 🧩 Skills subsection, QAa6 the
folds. QC4 owns how a topic becomes pages and groups in the first place.
QAa0-overall.md
QAa1-opening.md
QAa2-diagram.md
QAa3-content.md
QAa4-items.md
QAa5-where-we-are.md
QAa6-folds.md
QC4-question-group-design.md
### QAb · The sentence
The board's atomic unit and everything that attaches to it. QAb0 is the front door; QAb1 the
evidence card (the former QA8); QA6 the comment pinned to a selection; QAb2 editing the
sentence itself, still open; QAb3 what an agent acting on the sentence is handed (the former
QA8a); QAb4 the Sentence details panel and its filter, status, cleanup, archive, and restore lifecycle.
QAb0-overview.md
QAb1-evidence-card.md
QA6-comments.md
QAb2-editing.md
QAb3-agent-visibility.md
QAb4-sentence-details-lifecycle.md
### QB · Shipping the skill
Hand the skill over so a fresh agent can open a decent board without us.
Write SKILL.md, have a fresh agent cold-read it as acceptance, migrate the older
boards to the new format, and keep the code manageable (QB4: CSS/JS out to
skill-local assets; QB5: the Python split into src/; the grammar stays in the
skill). QB7 holds the sub-skill roster: which units this family ships besides
haipipe-board, now five (page, sentence, routing, digest) after JL added the two
verbs on 260729.
QB1-skillmd.md
QB2-newcomer.md
QB3-migrate.md
QB4-buildsplit.md
QB5-srcsplit.md
QB6-skill-to-page.md
QB7-subskills.md
### QD · Working on the board
The live layer: can you do real work on the board page itself?
One session per question (QD1), the restricted in-page drawer (QD2), the
unrestricted real terminal (QD3), how the page updates live without losing your
chat (QD6), attaching an excalidraw to a page from the page itself
(QD7, opened 260726; how that excalidraw renders is QAa2), counting updates by day
and by Board → Group → Page (QA10, which absorbed that dashboard with QC2), and making the current Board,
queue, focus, and work mode visible at the end of every agent reply (QD9). The index page's chatbot
is the QD2 drawer / QD3 terminal opened on board.md. Two pages left this group:
a board-agent question (QD5) archived 260725 as redundant with QD2 and QD3, and
LLM-assigned group icons (QD4) merged into the page-layout page on 260726, because the icon is a
layout marker and what blocks it is the page grammar's own rule about what a group title is
(that grammar lives on QAa3 since 260729).
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD6-liveupdate.md
QD7-diagramattach.md
QD9-session-status-strip.md
### QE · Sharing the board
Putting the board out there and making it a real thing others can open.
QE1 is the parent question: local or server, and which half other people get. Its
forks: how a mounted SPACE shows all its boards (QE2, v1 shipped 260724 as
`boards_api.py` plus a Boards view in `haichat-inlab`); where the code runs (QE3,
settled 260724: static half stays an invariant, hybrid layer split, branch
`feat/haichat-board`); whether the body text is editable in the page and what two
people editing at once does (QE4); where Boards sits in the console (QE5, JL's
call); which address serve.py binds to and where that setting lives once the code
is shared (QE6, opened 260726, the local half of QE1). The console also RELAYS the
live layer: chat and terminal work through it, piped to the workstation serve.py,
verified 260724.
QE1-hosting.md
QE2-mountspace.md
QE3-whereitruns.md
QE4-editlock.md
QE5-consolescope.md
QE6-bindaddress.md
### Q-Skill · What this family ships
One page per shipped unit of `skills/board/`, and nothing outside it: the skill
`haipipe-board`, and the agent `haipipe-board-reviewer-agent`. Scope is the
family this board designs, not every skill in the plugin (JL 260727).
These are ROSTER rows, not decisions. Each is generated by `skillpage.py` and kept
in sync by a managed span: the unit's own definition file becomes Content, its
CHANGELOG becomes dated Log lines, and the version rides the title so the index
row prints it. That makes the ACTIVITY dashboard able to rank which of this
family's units is actually changing. The mechanism is `QB6`.
Q-Skill-haipipe-board.md
Q-Skill-haipipe-board-reviewer-agent.md

## Links
QA2                 _archive/QA2-qtemplate.md
QC1                 _archive/QC1-where.md
QC2                 _archive/QC2-indexdesign.md
QD5                 _archive/QD5-boardagent.md
QA4                 QAa-the-page/QAa0-overall.md
QA4a                QAa-the-page/QAa2-diagram.md
QA8                 QAb-the-sentence/QAb1-evidence-card.md
QA8a                QAb-the-sentence/QAb3-agent-visibility.md
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
QC0@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC0-sentence-unit.md
QC1@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC1-sentence-citation.md
QC2@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC2-sentence-value.md
QC3@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC3-sentence-display-table.md
QC4@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC4-sentence-display-figure.md
QA1@paper           ../01-haipipe-paper-260725/QA-where-things-live/QA1-eight-folders.md
QA4@paper           ../01-haipipe-paper-260725/QA-where-things-live/QA4-the-board-tool.md
src/dialect_paper.py ../../board/haipipe-board/src/dialect_paper.py
src/common.py       ../../board/haipipe-board/src/common.py
src/body.py         ../../board/haipipe-board/src/body.py
src/page_board.py   ../../board/haipipe-board/src/page_board.py
src/page_question.py ../../board/haipipe-board/src/page_question.py
assets/board-mark.svg ../../board/haipipe-board/assets/board-mark.svg
assets/board.css    ../../board/haipipe-board/assets/board.css
assets/board.js     ../../board/haipipe-board/assets/board.js
fig/board-mark-palettes.svg fig/board-mark-palettes.svg
haipipe-board/assets/board.js ../../board/haipipe-board/assets/board.js
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
