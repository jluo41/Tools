Design Board workbench: Space to file map (Board level)
=======================================================

This is the Board level of the Design workbench, as served in 0.14.0. It
has two Spaces: Design Tasks and Theory of Design. Every design, run and
delivery lives at the Page level (`../space-mapping.md`). `../design-board.md`
describes the Board level in prose.


The two Spaces
--------------

| Space (tab, `space=`) | Reads | Shows | Links down to |
| --- | --- | --- | --- |
| Design Tasks Space (`tasks`) | the Brief's design task list (`0-BR-brief/BR00-brief/BR00-brief.md`, the table with `audience`, `job`, `venue`, `designs`, `folder`, `insight` columns); each `2-Design/*/` folder's register, and its independent Verify results for the counts and the csv | one row per task: design task (full name `<job> <venue> for <who>`, never its line id) · designs · folder · state; a **New Design Folder** button on a row with no folder; folders no design task lists; "every design task keeps" (the shared rules); **↓ Download all designs · N · csv** | the task name opens the folder's Page Design Space; the folder cell opens its Design Goal Space |
| Guide › Method and Guide › Related Paper (was the Theory of Design Space, `theory`; old links forward) | `servers/workbench-design/guide/method.md`, then the board's own `design-theory.md` beside `board.md` | the general theory of design, then the board's domain knowledge, both rendered from ASCII docs | none |

Header: the board title and "Board level" only. A records-check warning
is added only when the check has findings across folders.


The Runs panel
--------------

Each Space has the shared Runs panel on the right. Its run types come from
`skills/2_theme/design/haipipe-design-workflow/references/run-cards.md`. Each card
names a button, an agent, a skill, what the person signs, and a prompt.
The older page's Workbench Table is `legacy/workbench-table-older.md`. Board cards: Add design
tasks and Set shared rules (Tasks), Add a theory (Theory). The panel
starts nothing. **Copy** hands the prompt to a session.


The list of design tasks
------------------------

The first Markdown table in the Brief whose header names `audience`, `job`
and `venue` together:

```text
| line | audience | job | venue | designs | insight | folder |
|---|---|---|---|---|---|---|
| R1 | all patients | prescription review | sms | 10 |  | `Design-01-all-patients-prescription-review-sms` |
| R4 | young male, age 35 or under | prescription review | sms | 10 |  | — |
```

Columns match by header word: `audience`, `job`, `venue`, `designs` (or
`wanted` or `how many`), `insight`, `folder`. The line id is the column
headed `line`, `row`, `id`, `#`, or `page`. A Brief with no line-id column
still works: its rows are numbered R1, R2 and so on, in order. The id is a
key in the file, never a name on screen. `—`, `-`, or an empty folder cell
means "no folder yet". The `insight` column is still parsed, but the Board
level no longer shows it.

Line state is derived: `no folder yet`, `folder missing on disk`, the Page
level's refusal reason for a legacy folder, or a count of item states
(`1 ready · 9 generated`). Item states follow the Page-level state fold:
Commission, Generate and Verify Runs (`run-design-(commission|generate|verify)-*`)
with receipts in `results/<stem>/runtime.yaml`. Verify pass means ready
for Delivery. Declined items stay out of the counts and the csv.


The writes
----------

`new-folder` `{row}`: `row` is the parsed Brief row's `id`, for example
`{"row":"R3"}`; never a display title or integer position. It creates
`2-Design/Design-NN-<audience-slug>-<job-slug>-<venue>/` with a page that
passes the board checker (`folder-kind: design`, `state: 🔴 OPEN · no
design registered yet`, `owner:` from board.md else the Brief, an Opening
question "Which N <job> <venue> designs should we make for <audience>?")
and an empty register. It writes the folder name into the line's `folder`
cell and lists the page in board.md `## Pages` under its Design heading.
It is refused when the line already names a folder (so a second click
opens no duplicate) or is not in the Brief. A refusal names the task by
its full name, never `R3`.

`add-tasks` still answers on the route, but no form calls it. New design
tasks come from the Add design tasks card, through `haipipe-design-brief`.

Neither write exists on the static `board/design.html`.


Routes
------

```text
GET  /_board/design-board?path=/…/board.md[&space=tasks|theory]
GET  /_board/design-board?board=<folder name>          short link; a unique name start is enough
GET  /_board/design-board                              bare link: the server's only DesignBoard; with several, a list of them (200)
GET  /_board/design?folder=<Design-NN-…>[&space=…]     short Page-level link; 302 to the full path= & file= link; several boards hold it: 404 page listing each, never a guess
GET  /_board/design-bundle?path=/…/board.md[&folder=]  csv, one row per independently verified ready design; downstream owners decide sending
POST /_board/design-board       {path}                 -> the live URL (workbench menu)
POST /_board/design-board-act   {path, action, …}      -> new-folder (add-tasks kept, no form)
board/design.html                                       static twin, built with the Board site
```

Boards are found under `examples*/*/designs/*/board.md`, for example
`examples-<N>-<world>/<Project>/designs/B<NN>_DesignBoard-<Name>-<YYMMDD>`.
The legacy `applications/` globs are still searched for historical boards
only.

`?space=` aliases: `goal, brief, frame, plan, design, items, run, runs,
delivery, ready` open Design Tasks (the retired board Spaces);
`theories, knowledge` open Theory of Design. Default `tasks`.


Retired
-------

Retired in 0.14.0, kept here in one line each so old notes read right:

- Five Spaces at board level, and the board Goal, Design, Insight, Run
  and Delivery Spaces.
- The Waiting on queue and the Every Run table.
- The "Run types in this Space" guide.
- The "New design tasks" form and its Insight board picker.
- The Insight board line and the "Insight pages the designs use" fold.
  `board.md` `reads:` now feeds only a card's Insight pages fold.
- Adopt: historical records stay readable only.
- Content hashes.
