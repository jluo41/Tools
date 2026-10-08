Design Board: the same workbench, one grain up
==============================================

> **Older board page only.** This describes the older Design Folder board's workbench (Brief, Design Items,
> Commission → Generate → Verify). It stays at this path because other skills link it. A design Block on the
> ladder is described in `../SKILL.md` and `haipipe-design/ref/design-ladder.md`; new work never follows this file.

**LOAD `workbench` and `../SKILL.md` (`workbench-design`) FIRST.**
This reference is the Board level of the Design workbench, as served in
0.14.0. One 🎨 Design Board surface covers a whole DesignBoard in two
Spaces: Design Tasks and Theory of Design. It is served by
`servers/workbench-design/designboard.py` at `/_board/design-board`.
The Page level owns the Design Item, the register grammar, the state fold,
the plain words, and every action on one folder. The Board level owns only
the list of design tasks and the theory every design draws on. Every
design, run and delivery lives at the Page level.

```text
🎨 Design, two grains of one workbench
├── Board level   /_board/design-board?path=<board.md>      this reference
│                 Design Tasks · Theory of Design
└── Page level    /_board/design?path=<board.md>&file=2-Design/<Design-NN-…>/<Design-NN-…>.md
                  Design Goal · Design · Delivery, for one folder, with the buttons
```

Every task row links down to its Page level; the Page header links back
up. Nothing is stored twice: the Board level calls `design_snapshot` once
per folder and reads the result.


Plain words and full names
--------------------------

`Space` is the only reader-facing word (JL 260916). Every word on the
surface must be clear at first glance: "the Brief" and "a line of the
Brief", never roster; "signed insight", never handoff; "draft", never
candidate; "run record", never Ticket; "records check", never check_unit.
There is no DU and no Brief line id such as `R1` on screen. An insight page
shows as its label and title (`full-W01 · Send salience`), never its file id
`FW01`; the file keeps `FW01` (JL 260918). A design shows as "Design N";
the files say `ITEMNN`.

The Workflow is a list of Runs: Commission, Generate and Verify, recorded as
`run-design-(commission|generate|verify)-*`. Delivery is their ready projection:
Verify pass means ready for Delivery. Internal Steps add no Runs.

Folders carry their full name. The group is `2-Design/`, or one group per design method,
`2-Design-M<NN>-<slug>/` with its `method.md` (`haipipe-design/ref/legacy/method-folders.md`); the
Design Tasks Views are then the methods. Each Design Folder
is `Design-NN-<audience>-<job>-<venue>/`, never `DS`. Each part is the first
three content words of that Brief cell, with filler words dropped (with,
within, a, the, of, for, or, under, and so on). So the name says the goal:
`Design-01-<audience>-<job>-sms`. A renamed folder keeps
its `Design-NN` number, and an old link finds it by that number.


Design Tasks Space
------------------

Key `tasks`. It answers "what has this board promised to design, and is
each promise started?" It reads the Brief's list of design tasks and each
folder's register.

```text
Design tasks
design task                                               designs   folder                                               state
<Job> SMS for <audience a>                                10        Design-01-<audience-a>-<job>-sms                     1 ready · 9 generated
<Job> app card for <audience b> …                         1         Design-02-<audience-b>-<job>-ui-card                 1 generated
<Job> SMS for <audience c>                                1         —                                                    no folder yet  [New Design Folder]

every design task keeps   <rule> · <rule>
↓ Download all designs · 1 · csv
```

Each task shows by its full name, `<job> <venue> for <who>`, linked to its
Page level Design Space. The folder cell links to its Design Goal Space.
The Brief's row id (`R1`) is a key in the file and never a name on screen.

The list is the first Markdown table in the Brief under `0-BR-brief/`
(`0-BR-brief/BR00-brief/BR00-brief.md`) whose header names `audience`,
`job` and `venue` together. An audience table elsewhere in the Brief is
never read as the list. The `designs`, `insight` and `folder` columns are
matched by header word. `designs` is how many designs the line asks for.
A folder cell of `—` is a promise not yet kept. A Brief with no line-id
column still works: its rows are numbered R1, R2 and so on, as keys only.

The state cell says `no folder yet`, `folder missing on disk`, the Page
level's refusal reason for a legacy folder, or a count of item states.
A row with no folder still offers the **New Design Folder** button. A
folder on disk that no line names is listed under "folders no design task
lists". Below the table come the rules every design task keeps (the
acceptance lines every live design shares), then **↓ Download all designs
· N · csv**. The static twin has neither button nor download.

**The csv.** `GET /_board/design-bundle?path=<board.md>` returns one row per
design whose independent Verify passed. Columns: `line, who, their_job,
venue, folder, item, title, state, text, draft_run, render, because`.
`&folder=<folder>` keeps one task's rows; the Page Delivery Space links it.
Every row has `state=ready` and names the exact verified draft. A design
whose candidate or review records no longer validate shows `records
invalid` and leaves the csv. Failed, unverified and declined designs are
never listed. This is a design handoff, not leave to send; downstream
owners decide distribution.


Theory of Design: Guide › Method
--------------------------------

It was a board Space (key `theory`); since 261002 it is the shared Guide's Methods view,
which frames `/_board/design-board?embed=theory`, and an old `space=theory` link forwards
there. It renders `servers/workbench-design/guide/method.md`
first: how to design, the same for every board. Then it renders the
board's own `design-theory.md` beside `board.md`, when present: domain
knowledge, for example message theories. Both are ASCII docs.


Header and Runs panel
---------------------

The header shows only the board title and "Board level". A records-check
warning is added only when the check has findings across folders. Counts
are left off on purpose (JL 261001).

Each Space has a Runs panel on the right, the shared panel the Paper and
Page workbenches use. Its run types come from
`skills/2_theme/design/haipipe-design-workflow/references/run-cards.md`; each card
names a button, an agent, a skill, what the person signs, and a prompt.
The older page's Workbench Table is `ref/legacy/workbench-table-older.md`. Board cards: Add design
tasks and Set shared rules (Design Tasks), Add a theory (Theory of Design).
The panel starts nothing. **Copy** hands the prompt to a Claude or Codex
session, which does the work through the named skill.


The Board-level writes
----------------------

Both go through `POST /_board/design-board-act {path, action, …}`. Neither
exists on the static `board/design.html`.

**`new-folder`** `{row}` opens a Design Folder for one line whose folder
cell is empty. It is the New Design Folder button. `row` is the parsed
Brief row key from the snapshot, such as `R3`; never the display title or
an integer position. Submit `{"row":"R3"}` for the row whose `id` is `R3`:

```text
2-Design/Design-NN-<audience>-<job>-<venue>/
├── Design-NN-….md                        the page (below)
└── draft/Design-NN-…-design-items.md     empty register with its header
```

The page passes the board checker from the start: `folder-kind: design`,
`state: 🔴 OPEN · no design registered yet`, `owner:` (the board's owner,
else the Brief's), and an Opening question, "Which N `<job> <venue>`
designs should we make for `<audience>`?". The workbench writes the
folder's name into that line's `folder` cell and lists the page in
board.md's `## Pages`, under its Design heading when there is one. A
second click on the same line is refused, because the line already names
its folder. A refusal names the task by its full name, never by `R3`.

**`add-tasks`** `{subgroups, job, venue, designs, insight, open}` still
answers on the route, with its old refusals. No form calls it now: new
design tasks come from the Add design tasks card, through
`haipipe-design-brief`.

The folder cell and the new lines are the only Brief edits this workbench
makes. The Brief's prose stays with `haipipe-design-brief`. Every other
action (register a design, release a Commission, queue Generate or Verify)
lives on the Page level.


Reads (and owns nothing)
------------------------

```text
board.md                                title · reads: · owner:
0-BR-brief/BR00-brief/BR00-brief.md     the list of design tasks
design-goal.md                          the design input (read by the Page level)
design-theory.md                        the board's domain theory, when present
2-Design/*/<Design-NN-…>.md             each Design Folder, through design_snapshot
```

`board.md` `reads:` still names the Insight boards. It now feeds only a
card's **Insight pages** fold at the Page level. It names each board by its
sibling folder name, or by a `../` path that stays inside the checkout,
for example `../../insights/<Name>-InsightBoard` from
`<Project>/designs/B<NN>_DesignBoard-<Name>-<YYMMDD>`.
The board checker (`cli/check.py`) accepts both forms.

A legacy folder under `2-Design/` (`design/DU*`, `rNN_design_*`, PageX, v1)
appears on its Brief line with its refusal reason and no items, as the Page
level says it. A `2-DS-design/DS*` folder lies outside `2-Design/` and is
not read. Park such a folder under the board's `_archive/` and take its row
out of `board.md` `## Pages`. The checker judges no `_` folder, so the
record keeps its bytes, and only live design tasks stay on the board.


Boundary
--------

Apply to a Board whose `board.md` says `board-kind: design-board` (or
`design`), whose folder name carries `DesignBoard` as a `-` or `_`
separated token (`B<NN>_DesignBoard-<Name>-<YYMMDD>`), or which holds
`2-Design/`. Boards are found under `examples*/*/designs/*/board.md`. The
legacy `applications/` globs are still searched for historical boards
only. The board checker audits every folder that holds Design Runs,
including one with only Commission Runs. Historical `run-design-adopt-*`
records stay readable under their real ids; current writers never create
them.

A bare `/_board/design-board` opens the server's only DesignBoard. With
several, it answers 200 with a list of them. A link that names no
DesignBoard answers 404 with the same list. A Page-level short link
`/_board/design?folder=Design-01` that fits several boards answers 404
with a page listing each board, never a guess. `Design-1` reads as
`Design-01`.


Reader contract
---------------

From the Board level alone, the reader can answer:

1. What has the board promised to design: for whom, on which venue, how
   many, and is each promise started?
2. Which rules does every design task keep?
3. Which exact drafts are ready for Delivery, board-wide? (the csv)
4. What theory, general and domain, should every design draw on?

Item states, insight pages, runs, and who is waited on are read at the
Page level, one click down.


Retired
-------

Retired in 0.14.0, kept here in one line each so old notes read right:

- Five Spaces at board level, and the board Goal, Design, Insight, Run
  and Delivery Spaces: old `goal|design|delivery|run|insight` links open
  Design Tasks.
- The Waiting on queue and the Every Run table: read per folder now.
- The "Run types in this Space" guide: replaced by the Runs panel.
- The "New design tasks" form and its Insight board picker.
- The Insight board line and the "Insight pages the designs use" fold.
- Adopt: historical records stay readable only.
- Content hashes: the csv has no hash column.

See `legacy/design-board-space-mapping.md` for the Space to file map at board
grain; `space-mapping.md` is the Page grain.
