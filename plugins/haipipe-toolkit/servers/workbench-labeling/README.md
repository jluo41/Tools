# servers/workbench-labeling · the browser-facing layer of the labeling theme

The labeling theme's skills and engine live in `skills/2_theme/labeling/`; this folder is
their served face, one `workbench-<theme>` beside the others.

```
servers/
├── _host/serve.py             the shared haipipe host; `--only labeling` makes it the Labeling host
└── workbench-labeling/        🏷 the served face of workbench-labeling
    ├── labeling_theme.py      the theme on the frame: Block and Job levels
    ├── guide/ · related/      the family's Guide
    └── workbench-task-labeling/   a labeling Task's screen ⟷ skill workbench-task-labeling (b32 s41-D15)
        ├── task_labeling.py   the frame's Spaces for a labeling Task, by its type
        ├── labeling.py        LabelingMixin: labeling-board, labeling, and the one write door
        └── assets/js/10-drawer/60-workbench-labeling.js   the drawer row a Board page shows
    (its design studio, labeling-workbench-ui.py and its drawing, lives in Tools/blueprints/Project-Ladder/work/b15_theme_labeling/s02-labeling-workbench/)
```

## Two ways to serve it

Both host commands require Python 3.10 or newer. Use the workspace virtual
environment rather than assuming the system `python3` is new enough.

| Want | Run |
|---|---|
| Labeling on its own host: own port, DOMAIN, auth file; no terminal, chat or Board writes | `python plugins/haipipe-toolkit/servers/_host/serve.py --only labeling --root <folder>` |
| Labeling as one tab among the others on a Board | `python plugins/haipipe-toolkit/servers/_host/serve.py --root <folder>` (`workbench-labeling/` is one of its workbenches) |

Both print the DOMAIN lines they answer at (loopback, the Tailscale IP when the
bind reaches it, the configured origin) and the short routes:

```
<DOMAIN>/w/<board>                      every labeling job on that Board
<DOMAIN>/w/<board>/<page>/labeling      one Page: four Spaces, including Data → Preparation before Contract
<DOMAIN>/workbench/labeling?file=<Page>/<Page>.md
                                       a canonical Page folder on the dedicated Labeling host
```

The dedicated host can open a canonical Page folder without `board.md` or a
generated Board Page. `file=` is a path relative to `--root`. The Page file must
exist as `<Page>/<Page>.md`; flat Markdown sources and symlinked paths are
rejected. This route is unavailable on the mixed Board host. It has the same
Data, Labeling, Quality, Delivery, Runs, and engine-checked action surface;
the Board back link applies only to Board-backed Pages.

`<board>` is the Board folder's slug (`job-mini-board` for `job-mini-board-260830`)
and `<page>` a Page id (`S-Label-1`). The server fills in `path=`, `file=` and
`page=` itself and redirects to the long `/_board/labeling...` route.

## Dependency

`workbench-labeling/workbench-task-labeling/labeling.py` is a mixin for the shared host: it takes
`target()`, `reply()` and the HTTP plumbing from `haipipe-toolkit/servers/_host`,
and reads a Board's page list through one adapter, `_board_pages()`, which is
the only place it touches the Board grammar (`haipipe-toolkit/skills/1_base/draft/haipipe-draft/src`).
The dedicated Page-folder route uses its own checked resolver and does not
call the Board parser.
The shared Guide Space is mounted through
`haipipe-toolkit/servers/workbench` from this folder's `guide/guide.yaml`; the method page
and its cards are `guide/method.md`, `guide/methods/` and `guide/methods.excalidraw`, the papers
`related/papers.md` (moved here from the skill's `ref/`, 261007). Its methods and UI diagrams describe
the labeling family; folder links retain this host's private-source boundary.
Each Space's Runs panel is the shared one, `haipipe-toolkit/servers/workbench/runs_panel.py`
(`panel_markup`, `PANEL_CSS`, `PANEL_JS`, `SPLIT_CSS`), with Labeling's own gated Run
cards passed in. Both follow the rules every workbench shares
(`haipipe-toolkit/servers/README.md` "Adding a workbench"); how they were met is
recorded in `Tools/blueprints/Project-Ladder/work/b15_theme_labeling/s02-labeling-workbench/labeling-shared-rules.md`.
The engine under `../../skills/2_theme/labeling/engine/` imports nothing from the servers. So:

- **runtime**: independent. The labeling host (`serve.py --only labeling`) is its own process
  and origin: own port, DOMAIN and auth file; terminal, chat and Board writes answer 404.
- **install**: the labeling workbench is part of haipipe-toolkit; it is always present.

Settings come from `<root>/.server_config/settings.env` with the generic keys
`DOMAIN`, `BIND_HOST`, `PORT`, `AUTH_FILE`, `SPACE_NAME`, `NO_AUTH`; see
`haipipe-toolkit/servers/_host/server_config.py`.

The shared host refuses direct static requests for JSONL data, source-owned
`corpus-preparation/` files, and Page `labeling/` files. The Workbench reads
accepted receipts through checked server-side routes instead. Keep any other
private raw formats outside the served `<root>` until a specific route protects
them.

## Focus pages

`/_board/workbench?path=<Job-or-Task>&layout=focus` now presents labeling's
real content one section at a time. `labeling_focus.py` owns this adapter;
`focus-assets/` owns its styling and small interactions. The shared frame only
dispatches labeling focus requests here. Other themes retain their presenter.

- Job: Goal and a next-action link, Tasks, Reports, label schema, Outputs,
  Studio-All, Timeline and Folders.
- Items Task: Goal, Runs, Data, Items, Embedding, Reports and Outputs. Content
  comes from `task_labeling.py`; sampling, recipe signatures and notes use the
  existing endpoints. Prompts copy instructions; they do not start work.
- Labeling Task: the existing Contract, Definition, Rounds, Guideline,
  qualification and delivery views. A same-origin embedded view preserves the
  existing engine identity, attestation, hold checks and write door. Its
  `focus=1` parameter changes presentation only.
- Reports link to the owning Task's saved Run results. Missing results remain
  visibly absent. A next action is recomputed from the preparation engine with
  `settle_runs=False` or the labeling view model, never from browser progress.

Content disclosures become stable sections in this layout. Job/Task folders,
Run tickets, receipt authority and computational workers are unchanged. This
UI does not implement missing guideline-learning, executor-optimization or
large-scale labeling workers. A page load starts no Run and signs nothing.

## Shared Work alignment

Labeling Block and Job focus pages now use the shared Work components:
Overview (Goal, Requirements, MindMap), Status (topic-based View BJTR),
Findings (Labeling's existing result reader), and Delivery (Labeling's signed
release reader). Report includes the content and actions; old Work and MindMap
links resolve to the corresponding Report view. No engine writer changes.

`work_frame.SHARED` supplies the eight unnumbered supporting sections and their
rail labels. Both entrances use `work_frame.shared_bodies`: explicit View or
Topic associations limit in-view content; the rail includes all records in the
current Block or Job scope. Unassigned records remain in the rail. The shared
Files browser, Studio tabs, and mobile navigation are reused.

The design matrices and migration boundaries live in
`blueprints/Project-Ladder/work/b15_theme_labeling/ui/`. Items, Meaning,
Expression and legacy Task screens still retain their existing Report/Work
workflow; their table describes the alignment target, not a completed migration.
