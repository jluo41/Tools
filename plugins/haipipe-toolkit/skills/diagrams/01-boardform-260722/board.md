# /haipipe-board: pinning down what "a board" is, so it can be reused

spine: A board = one folder. One markdown file per question inside it, plus one HTML page anyone can open. Pin that shape down, write it into SKILL.md, so someone else (and a future me with no memory) can open a board by following it.
close: Every Q on this board reaches ✅ or ⏸️. SKILL.md is written, and a fresh agent with no background can read only that and open a decent board, and then this skill is done.
excalidraw: http://127.0.0.1:5599/_excalidraw
session: 3e951d68-1c6d-4f22-af82-76dd70bb356d
## Topic
What a board is for: a topic has several undecided questions; lay them out on one page anyone can open and comment on; settle them one by one, then close the board.
Cast: JL = the one who decides. CC = Claude Code, who does the work. Colleagues = the people who review, discuss, or take responsibility for work on the board; each uses their own initials.
What makes this board unusual: its subject IS the board itself, a board used to define boards.

## Pipeline
Five groups; the letter in each Q's id is the group it was opened under. The first two (QA defines the thing, QB ships it) are the main line; QC, QD and QE each own one area and can be thought about in parallel. Each group's own intro lives with it in the ## Pages below and shows on the index page under the group header (QC2). The former "QF · A board on top of other formats" group merged into QA on 260725 and its last page was retired on 260726, so no QF id remains.

## Pages
### QA · Defining a board
Pin down the thing itself; nothing downstream is safe until this group lands.
Folder shape, then the shared Q/S source template, how one opened page's page is
laid out and how its group titles are marked, whether the whole board can share one
excalidraw with a frame per page, inline comments and what becomes of
one, the sentence apparatus, whether any agent sees what gets attached, what is
checked after any change, and which visual-taste rules improve the work surface
without turning it into a marketing page. Three rulings shipped and
were retired as pages because their law lives in `ref/board-form.md`: projection,
one file with two modes (former QA3, §8, its JS-only extras parked with it);
embedding another file by reference, `![[path#Section]]` (former QF1, §5); and the
`doc:` row that rendered source files as a slide with no Q wrapper (former QF2,
retired 260726, superseded by that embed, which does the same job inside a real
page). Two merges on 260726, both for the same reason, that a page which builds a thing
and a page which rules what becomes of it are one subject: QA5 into QA9 (writing
prose a stranger can read and checking the page still renders what the template
promises are two checks on one trigger), and QA7 into QA6 (building a comment and
ruling its remaining life; the split had let QA6 sit ✅ while the thing it built
had no ending). QD4 joined QA4 the same day for the same reason, and cost QA4 its
flattering 17/18: the icon question had been parked in another group while the
grammar it depends on lived here.
```
  folder  →  Q template  →  page layout  →  comments + lifecycle  →  sentence ⚑
   QA1         QA2            QA4                 QA6                  QA8
                               |
                one excalidraw per board, a frame per page  ──►  QA4a
                                                                        |
                                              does the chat see the     |
                                              sentence's attachments?  QA8a
                  |
                  |    after a change, does it still hold up?  ──►  QA9
                  |    scoped visual taste, audit before editing ──►  QA10
                  |
                  └─ structure renders · prose reads · the work surface stays a
                     work surface · what the page collects reaches the worker
```
QA1-form.md
QA2-qtemplate.md
QA4-pagelayout.md
QA4a-board-excalidraw.md
QA6-comments.md
QA8-sentence.md
QA8a-sentence-chat.md
QA9-acceptance.md
QA10-ui-taste.md
### QB · Shipping the skill
Hand the skill over so a fresh agent can open a decent board without us.
Write SKILL.md, have a fresh agent cold-read it as acceptance, migrate the older
boards to the new format, and keep the code manageable (QB4: CSS/JS out to
skill-local assets; QB5: the Python split into src/; the grammar stays in the
skill).
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
unrestricted real terminal (QD3), how the page updates live without losing your
chat (QD6), and attaching an excalidraw to a page from the page itself
(QD7, opened 260726; how that excalidraw renders is QA4 §2). The index page's chatbot
is the QD2 drawer / QD3 terminal opened on board.md. Two pages left this group:
a board-agent question (QD5) archived 260725 as redundant with QD2 and QD3, and
LLM-assigned group icons (QD4) merged into QA4 on 260726, because the icon is a
layout marker and what blocks it is QA4's own rule about what a group title is.
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD6-liveupdate.md
QD7-diagramattach.md
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

## Links
SKILL.md            ../../0_utils/haipipe-board/SKILL.md
build.py            ../../0_utils/haipipe-board/build.py
check.py            ../../0_utils/haipipe-board/check.py
watch.py            ../../0_utils/haipipe-board/watch.py
serve.py            ../../0_utils/haipipe-board/serve.py
CHANGELOG.md        ../../0_utils/haipipe-board/CHANGELOG.md
ref/                ../../0_utils/haipipe-board/ref/
ref/q-template.md   ../../0_utils/haipipe-board/ref/q-template.md
ref/board-form.md   ../../0_utils/haipipe-board/ref/board-form.md
ref/writing-rules.md ../../0_utils/haipipe-board/ref/writing-rules.md
ref/board-example.md ../../0_utils/haipipe-board/ref/board-example.md
haipipe-board/      ../../0_utils/haipipe-board/
env.sh              ../../../../../../env.sh
paper-board/        ../01-haipipe-paper-260725/
QC0@paper           ../01-haipipe-paper-260725/QC0-sentence-unit.md
QC1@paper           ../01-haipipe-paper-260725/QC1-sentence-citation.md
QC2@paper           ../01-haipipe-paper-260725/QC2-sentence-value.md
QC3@paper           ../01-haipipe-paper-260725/QC3-sentence-display-table.md
QC4@paper           ../01-haipipe-paper-260725/QC4-sentence-display-figure.md
QA4@paper           ../01-haipipe-paper-260725/QA4-the-board-tool.md
src/dialect_paper.py ../../0_utils/haipipe-board/src/dialect_paper.py
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
