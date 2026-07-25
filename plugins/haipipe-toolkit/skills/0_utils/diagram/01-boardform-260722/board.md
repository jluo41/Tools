# /haipipe-board: pinning down what "a board" is, so it can be reused

spine: A board = one folder. One markdown file per question inside it, plus one HTML page anyone can open. Pin that shape down, write it into SKILL.md, so someone else (and a future me with no memory) can open a board by following it.
close: Every Q on this board reaches ✅ or ⏸️. SKILL.md is written, and a fresh agent with no background can read only that and open a decent board, and then this skill is done.
session: 3e951d68-1c6d-4f22-af82-76dd70bb356d
## Topic
What a board is for: a topic has several undecided questions; lay them out on one page anyone can open and comment on; settle them one by one, then close the board.
Cast: JL = the one who decides. CC = Claude Code, who does the work. Colleagues = the people who review, discuss, or take responsibility for work on the board; each uses their own initials.
What makes this board unusual: its subject IS the board itself, a board used to define boards.

## Pipeline
Five groups; the letter in each Q's id is its group. The first two (QA defines the thing, QB ships it) are the main line; QC, QD and QE each own one area and can be thought about in parallel. Each group's own intro lives with it in the ## Roster below and shows on the index page under the group header (QC2).

## Roster
### QA · Defining a board
Pin down the thing itself; nothing downstream is safe until this group lands.
Folder shape, then the template for a single Q file, what to do about projection,
how one question's page is laid out, how to write body text that reads like human
language, how to add inline comments, and the lifecycle of one comment.
```
  folder  →  Q template  →  projection  →  page layout  →  writing  →  comments  →  lifecycle
   QA1         QA2            QA3            QA4            QA5         QA6          QA7
```
QA1-form.md
QA2-qtemplate.md
QA3-htmlppt.md
QA4-pagelayout.md
QA5-readable.md
QA6-comments.md
QA7-lifecycle.md
### QB · Shipping the skill
Hand the skill over so a fresh agent can open a decent board without us.
Write SKILL.md, have a fresh agent cold-read it as acceptance, migrate the older
boards to the new format, and keep the code manageable (QB4: build.py's CSS/JS
split into skill-local assets; the grammar stays in the skill).
QB1-skillmd.md
QB2-newcomer.md
QB3-migrate.md
QB4-buildsplit.md
QB5-srcsplit.md
### QC · Index and structure
The board's skeleton: where a board lives, and what the front page must show.
Where a board lives and what it is named (QC1); what the index page looks like
and how to see in three seconds which question to work on (QC2). Split from QA4:
QA4 owns the single-question page you land on after clicking, QC2 owns the index
you see before clicking.
QC1-where.md
QC2-indexdesign.md
QC3-folderq.md
### QD · Working on the board
The live layer: can you do real work on the board page itself?
One session per question (QD1), the restricted in-page drawer (QD2), the
unrestricted real terminal (QD3), LLM-assigned group icons (QD4), and how the
page updates live without losing your chat (QD6). The index page's chatbot is the
QD2 drawer / QD3 terminal opened on board.md; a separate board-agent question
(QD5) was archived 260725 as redundant with them.
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD4-topicicon.md
QD6-liveupdate.md
### QE · Sharing the board
Putting the board out there and making it a real thing others can open.
QE1 is the parent question: local or server, and which half other people get. Its
forks: how a mounted SPACE shows all its boards (QE2, v1 shipped 260724 as
`boards_api.py` plus a Boards view in `haichat-inlab`); where the code runs (QE3,
settled 260724: static half stays an invariant, hybrid layer split, branch
`feat/haichat-board`); whether the body text is editable in the page and what two
people editing at once does (QE4); where Boards sits in the console (QE5, JL's
call). The console also RELAYS the live layer: chat and terminal work through it,
piped to the workstation serve.py, verified 260724.
QE1-hosting.md
QE2-mountspace.md
QE3-whereitruns.md
QE4-editlock.md
QE5-consolescope.md
### QF · A board on top of other formats
Can a Q show content that lives in another file, and what must that file's side
guarantee? Raised by the first board laid over a paper's 0-lifecycle tree, where
the stage docs have their own formats and copying them into faces drifts (QF1).
QF1-embed.md
QF2-docslide.md

## Links
SKILL.md            ../../haipipe-board/SKILL.md
build.py            ../../haipipe-board/build.py
watch.py            ../../haipipe-board/watch.py
serve.py            ../../haipipe-board/serve.py
CHANGELOG.md        ../../haipipe-board/CHANGELOG.md
ref/                ../../haipipe-board/ref/
ref/q-template.md   ../../haipipe-board/ref/q-template.md
ref/board-form.md   ../../haipipe-board/ref/board-form.md
ref/writing-rules.md ../../haipipe-board/ref/writing-rules.md
ref/board-example.md ../../haipipe-board/ref/board-example.md
haipipe-board/      ../../haipipe-board/
haipipe-paper-stage/ ../../../paper/1-lifecycle/haipipe-paper-stage/
0-lifecycle/        ../../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
02-method-260722/   ../../../../../subjective-label/diagram/02-method-260722/
haichat-inlab/      ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/
main.py             ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/main.py
console_api.py      ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py
tasks_api.py        ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/tasks_api.py
labeling_api.py     ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/labeling_api.py
web/                ../../../../../../../platforms/HAIChat-SPACE/haichat-inlab/web/
docker-compose.yml  ../../../../../../../platforms/HAIChat-SPACE/docker-compose.yml
