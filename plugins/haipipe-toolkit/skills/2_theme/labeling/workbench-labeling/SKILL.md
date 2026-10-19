---
name: workbench-labeling
description: >-
  The 🏷 labeling theme of the shared workbench: its host (its own, or one tab on a Board), the Board level
  (every labeling job on the Board, zoom out), the Block and Job levels on the frame, and the family's Guide.
  A labeling Task's own screen (the four Spaces Data, Labeling, Quality, Delivery, the write door, the five
  Task types) is workbench-task-labeling. Use when opening or diagnosing the labeling workbench, its host, its
  Board view or its Guide, or /workbench-labeling.
metadata:
  version: "0.33.0"
  last_updated: "2026-10-16"
---

# /workbench-labeling · one job, one folder, one operated surface

**LOAD `workbench` and `haipipe-labeling` FIRST.** This is a Workbench lane:
it owns the `labeling/` roster row and its own surface. The family workflows
own semantic order and writes; this skill owns how that job lives beside and
appears beside one Page: the host, the Board level and the Guide. The Task's own screen is
`workbench-task-labeling` (its code `servers/workbench-labeling/workbench-task-labeling/`, b32 s41-D15).

```text
one page folder
├── <stem>.md                    what the Page says
├── labeling/                    the job itself · canonical
│   ├── config.yaml · corpus/ · policy/ · rounds/ · gold/ · handoff/
│   ├── test/ · evaluation/ · production/ · audit/
│   ├── gates/                      P0 contract + G0 receipts
│   ├── preparation-owner.yaml       source attachment, even before a job
│   ├── preparation-ref.yaml         accepted source package, before Contract
│   ├── cache/                      embeddings/ · reveal/ · derived, never authority
│   └── REPORT.md · .state.json  rendered/cache only; receipts win
├── runs/                        full `run-labeling-...` Tickets, beside labeling/
└── results/                     one folder per Ticket, same name

🏷 Board level · <DOMAIN>/w/<board-slug>   (→ /_board/labeling-board?path=<board.md>)
shell      title · band (jobs, waiting, next) · Guide · Jobs
all jobs   one card per Page that owns labeling/ · jobs that wait for you first
           click a card → the Page level below · "all labeling jobs" comes back
empty      S-Label-* Pages without a job appear under "Pages before Contract"
           and link to their Page-level Preparation View, without allocating a Run;
           flat Board sources first ask for a canonical Page folder

🏷 Task level · the labeling Task's screen, its four Spaces: skill workbench-task-labeling
```

## 🖥 Hosting · its own host, or one tab on a Board

Resolve `TOOLS_ROOT` to the checkout containing `plugins/` (`.` from that
checkout, or a consuming workspace's `Tools` link) and `PYTHON_BIN` to that
workspace's Python 3.10+ interpreter before using these host commands. The
system `python3` may be too old; check `"$PYTHON_BIN" --version` first.

```text
own host    "$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/servers/_host/serve.py" --only labeling --root <folder>
            the shared haipipe host with --only labeling: own port, DOMAIN and auth
            file; terminal, chat and every Board write route answer 404
Board tab   "$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/servers/_host/serve.py" --root <folder>
            🏷 is one tab among the others; same routes, same write door
addresses   <DOMAIN>/w/<board-slug>                    every labeling job on the Board
            <DOMAIN>/w/<board-slug>/<page-id>/labeling one job, four Spaces
            <DOMAIN>/workbench/labeling?file=<Page>/<Page>.md
                                                        a canonical Page folder without a Board
```

The separate host isolates the service and its settings. Its direct Page route
resolves an existing `<Page>/<Page>.md` relative to `--root`, without `board.md`
or a generated Page URL. It rejects flat sources, symlinks, traversal, and
requests on the mixed Board host. The direct Page has the same Spaces, Views,
Runs panel, and Labeling action door; it has no Board back link. Create a Page folder before attaching Corpus Preparation or creating a
new Contract.

`<DOMAIN>` is whichever origin the server printed at startup (loopback, the
Tailscale IP, or the configured `--public-url`); the link body is the same for
all of them. The short address redirects to the long route and the server
fills in `path=<board>/board.md`, `file=<page-rel>` and `page=<generated
html>` itself. The workbench code is `servers/workbench-labeling/workbench-task-labeling/labeling.py`,
a mixin of the shared host; it reads the Board's page list through one
adapter (`_board_pages`) and nothing else of the Board grammar, and the
`engine/` it calls imports nothing from haipipe-toolkit. See
`plugins/haipipe-toolkit/servers/workbench-labeling/README.md`.

## 🔭 Two levels: Board and Page

| level | where it opens | what it shows | writes |
|---|---|---|---|
| Board | the Board index, and the `S-Label-Dash` control Page | one card per Page with a linked preparation package or a `labeling/config.yaml` job (in `labeling/`, one card per Job, carrying the Job address `bNNjNN`): target, question, data, step badge, progress, next step; Pages with neither listed below | none |
| Page | any real job Page; in `labeling/`, the Job's labeling Task Page, standing for the whole Job | the four Spaces and their Runs panels; a `labeling/` Job's other Tasks with their latest Run in `Data → Preparation` (Job data) and `Quality → External gold`; label definitions and Confirm meaning in `Labeling → Definition`, round tables in `Labeling → Rounds` | only `POST /_board/labeling/act` |

A card links to `/_board/labeling?path=…&file=…&page=…`, so zooming in opens
the Page level in the same pane. The `all labeling jobs` link under the Page's
title goes back to `/_board/labeling-board?path=<board.md>`. Cards sort by what waits
for the human: labeling in progress, then meaning confirmation, then a round to
start, then judged, repair, and read-only (HOLD) jobs. The Board level reads
each job through the same view model as the Page level (`_view_model`,
`_next_step`), so the two can never disagree, and it never stores a label.
Labels stay per Page because each target has its own human gate.

The registry offers the Board-level entry (`id: labeling-board`) only on the
Board index or on `S-Label-Dash`, and the Page-level entry (`id: labeling`)
only on job Pages, so one 🏷 entry is offered at a time. A Board whose job
Pages are not named `S-Label-*` is recognised after `POST
/_board/labeling-board` counts its `labeling/` lanes.

The specialized `page-type: labeling` Job Page owns one corpus snapshot × one
target construct × one identified human semantic authority and uses the
labeling Page grammar. That Page type is not a
capability switch: a paper section, algorithm Page, or other Folder may open
the same plugin before a job exists and route P0 creation through Chat. The
control Page `S-Label-Dash` owns no job, so it gets no Page-level lane; it
opens the Board-level view instead.

## 🧭 Guide · how the family works

Guide is the first tab of both levels, mounted by the shared `mount_guide()` from
the server's own `servers/workbench-labeling/guide/guide.yaml` (moved there from
`servers/workbench/guide_families.py`, 261007), with its method in `guide/` and its papers
in `related/` beside it. Its four Views read only family files, never a job:

```text
Description    one paragraph: what the workbench does
Method         the shared Method page (`/_board/guide?family=labeling&mode=method`,
               `"only"`: it replaces Guide's own step list) from guide/method.md,
               in Design's folding cards: Method design (the drawing
               guide/methods.excalidraw), 1 · the six steps, the
               steps in depth (1, 3, 4, 5 and 6) each with its method cards (guide/methods/,
               13), why it works, Reference. The drawing's first version came from the
               shared method-canvas.py; after that the canvas is the source
               Every card starts closed, here and on RoadMap Draw
RoadMap Draw   "Workbench design": Tools/blueprints/b15_theme_labeling/studio/s02-labeling-workbench/labeling-workbench-ui.excalidraw,
               generated by labeling-workbench-ui.py beside it (never edited by hand)
               + the Workbench Table, ref/workbench-table.md
Related Paper  related/papers.md, checked by table-papers
```

The Workbench Table (Level · Space · View · Run type · Agent · Skill · Person
signs) is generated by `ref/make_workbench_table.py` from
`haipipe-labeling-building/ref/ref-space-mapping.md`: the Space roster, the Run types and
their words and View, the declared Skills, and `## Run Type agents` (who does each
Run type and what the person signs). Change a row there, rerun the script, then run
table-workbench's `render_workbench_table.py --check`. Adding a paper is a
Discovery run; the table and its check belong to table-papers.

## 📂 Files

- `servers/workbench-labeling/labeling_theme.py` · the theme on the frame: Block and Job levels, the Task ▾ options
- `servers/workbench-labeling/guide/` (`guide.yaml`, `method.md`, `methods/`, `methods.excalidraw`) and
  `related/papers.md` · Guide, in the server folder (261007)
- `ref/workbench-table.md` · the Workbench Table, generated by `ref/make_workbench_table.py`
- `Tools/blueprints/b15_theme_labeling/studio/s02-labeling-workbench/labeling-workbench-ui.py` · the Workbench design drawing
- `../workbench-task-labeling/SKILL.md` · a labeling Task's screen (its code: `servers/workbench-labeling/workbench-task-labeling/`)
