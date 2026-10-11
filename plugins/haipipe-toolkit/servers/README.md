# servers/ · the browser-facing layer of haipipe-toolkit

Everything a browser is served by lives here, and nothing here is a skill. The
folder is a sibling of `skills/`, `agents/` and `mcp-servers/`: plugin-level
infrastructure that hosts the skills' Boards and Pages, for any SPACE that
carries a `.server_config/settings.env`. Nothing in it names one person, one
lab, or one deployment.

```
servers/
├── _host/               the transport: serve.py, auth, config, the `live` namespace, shell JS
├── space-home/          SPACE Home and Board-level writes (home, structure, write, activity)
├── haipipe-page/        the standalone Page server and the reader appearance (page.css, css/)
├── workbench/           🧭 the base, under every theme: 🎨 Studio (draw/Excalidraw, chat,
│                        terminal, slides, vendored xterm) and the read-only Guide Space;
│                        with no theme on top it is the vanilla workbench
│   └── task/            the base's Task level, once workbench-page: everything one Page's
│                        tabs render: outline, evidence, value, runs, delivery (latex/word/
│                        bibex exports), folder status, plugview; exporters/ holds the md2tex,
│                        md2docx and docx2pdf writers
├── workbench-paper/     📄 the Paper workbench
├── workbench-work/      📋 the work theme (once task): Questions as Logic / Work / Report, Studio
├── workbench-cowork/    📨 CoWork Blocks: Jobs, who we wait on, Questions, emails, meetings
├── workbench-discovery/ 🔭 Discovery Blocks: papers, Result cards, citations to verify, BibTeX
├── workbench-insight/   🔎 InsightBoard and its Run Specs
├── workbench-design/    🎨 Design Folder and Design Board
└── workbench-labeling/  🏷 the Labeling workbench; `_host/serve.py --only labeling` serves it alone
```

## Two words, two things

A **skill** named `workbench-<x>` is the contract: what the lane holds
on disk and who writes it (`skills/1_base/page/workbench-page` says what
`outline/`, `runs/`, `results/` and `delivery/` hold). A **workbench** folder
named `workbench-<x>` is that contract's served face, where a person works on
it in the browser. Same name on both sides, except the Studio contract, which
every workbench reuses and so is served from `workbench/`:

| skill (`skills/`) | workbench (`servers/`) |
|---|---|
| `1_base/page/workbench-page` (Outline · Run Space · Delivery · Folder) | `workbench/task-page/` (the base's Task level) |
| `1_base/page/workbench-studio` (Draw · Chat · Terminal · ✨ pens; shared by every workbench) | `workbench/` |
| `2_theme/design/workbench-design` (+ `ref/design-board.md`, the Board grain) | `workbench-design/` |
| `2_theme/paper/workbench-paper` | `workbench-paper/` |
| `2_theme/work/workbench-work` | `workbench-work/` (the work theme) |
| `2_theme/cowork/workbench-cowork` | `workbench-cowork/` |
| `2_theme/discovery/workbench-discovery` | `workbench-discovery/` |
| `2_theme/insight/workbench-insight` (+ `ref/insight-board.md`, the Board grain) | `workbench-insight/` |
| `2_theme/labeling/workbench-labeling` | `workbench-labeling/` |

## Two URLs, one DOMAIN

A served Board or Page answers at a reader's address and a worker's address,
and they take the same two words:

```
<DOMAIN>/b/<board>                 the Board                        (302 → the base frame, as /w/)
<DOMAIN>/b/<board>/<page>          one Page, as the reader sees it  (302 → /_board/page?path=…)
<DOMAIN>/w/<board>                 the Board's workbench            (302 → /_board/workbench?path=…, the frame)
<DOMAIN>/w/<board>/<page>          one Page's workbench, 📃 Page
<DOMAIN>/w/<board>/<page>/<tab>    runs · delivery · folder · evidence · value · design · insight · labeling
```

`<board>` is the folder's slug (`01-topic-260722` → `topic`), `<page>` the
Board's page id (`QA1`, `S-Label-1`). `home.py` resolves both against the Boards
Home already discovers and fills in `path=`, `file=` (and `page=` for labeling) itself.
A Board opens in the base frame (`workbench/frame.py`, JL 261007), in its theme; every theme is
on the frame. The page carries no band line and no link to a theme's older page (JL 261007). An
`--only <workbench>` host serves no frame, so there `/w/<board>` and `/b/<board>` still open
the theme's own page. The
long `/_board/...` routes stay the contract; on them `file=` may now be
omitted, and `base.py:derive_file()` reads it off the disk.

`<DOMAIN>` is a variable. Every link body and every redirect is
origin-relative, so one body works at each origin the server answers at. The
server prints them at startup, labelled `configured` (`--public-url`, env
`HAIPIPE_DOMAIN`, or the `DOMAIN` line of `<root>/.server_config/settings.env`),
`tailscale` (when the bind reaches this machine's Tailscale IP) and `loopback`.
`server_config.py` reads the generic keys `SPACE_NAME`, `DOMAIN`, `BIND_HOST`,
`TAILSCALE_ADDRESS`, `PORT`, `AUTH_FILE`, `ACCESS_MODE`, `NO_AUTH`; a
deployment may prefix them (`<PREFIX>_DOMAIN`).

SPACE Home (`<DOMAIN>/`, also `/boards`) is the read-only Space view: every Project,
inside it every Theme (`tasks`, `discoveries`, `cowork`, `papers`, `insights`, `designs`,
in that order; then any other root folder), inside that the Block cards. Cards open
`/w/<block>` when its slug is unique, else the frame's long address; both open the base
frame. `?kind=task` (or `?kind=task,paper`) filters by block type and is written back
to the address bar, so a link reproduces the view. `?project=<Project>` (its SPACE-relative
folder, its folder name, or its project.yaml id) shows that one Project alone, with a link back
to every Project; the two combine (`?project=…&kind=cowork`). `/wb` (the `workbench` skill's
`cli/wb.py`) opens these addresses, and the frame's, from a path or from plain words. Projects start open when the view
holds at most five, closed otherwise; a person's own folds and Project order stay in
the browser.

Task Blocks (`board-kind: task-block`) open at `/w/<block-folder>` or
`/_board/work-board?path=<block>/board.md`. SPACE Home links directly to their
live Workbench without a static build. See [Task Workbench](workbench-work/README.md)
for Question reports, the four working Views and the synthetic demo.

CoWork Blocks (`board-kind: cowork-block`, `cowork/bNN_<topic>/`) open the same way at
`/w/<block-folder>` or `/_board/cowork-board?path=<block>/board.md`; every Block of a
Project at `/_board/cowork-board?path=<Project>/cowork`. The page reuses the Task
Workbench's stylesheet and script (`skills/2_theme/cowork/workbench-cowork`).

Discovery Blocks (`board-kind: discovery-block`, `discoveries/bNN_<block>/`) open the same
way at `/w/<block-folder>` or `/_board/discovery-board?path=<block>/board.md`; every Block of
a Project at `?path=<Project>/discoveries`. Task, CoWork and Discovery stay separate
workbenches with one look (JL 261004).

Every family has one **Guide Space**. Its `Skill set`, `Methods`, `Workbench`,
`Folder map` and `RoadMap Draw` Views appear directly below the Space row.
Diagrams are independently folding rows in one column. Guide reads declared
family definitions and resolves folder conventions inside the current
instance; working questions, progress and drawing writers stay with their
native family. See [Guide runtime and design studio](workbench/README.md).
The shared host, standalone Page host and dedicated Labeling host reuse the
read-only Excalidraw proxy; Labeling remains an optional package.

## What a server folder is

Every folder here (and every `plugins/*/servers/workbench-*`) may hold:

- `*.py` mixins, importable as `live.<module>` through `_host/live/__init__.py`,
  which grafts every folder onto one `live` namespace (`host_registry.py` lists
  them). Module names are unique across folders.
- `assets/js/**` and `assets/css/**` parts. `_host/host_assets.py` concatenates
  them in sorted relative-path order into the one `board.js` / `board.css` a
  rendered Board page loads; the numeric prefix still says where a part goes.
- `assets/vendor/…` for third-party files a route serves (xterm).
- `tests/` and `checks/` for that folder's own behaviour.
- a row in `host_registry.WORKBENCH_ROUTES`, the `/_board/<name>` names it answers.

## Entry points

| Want | Run |
|---|---|
| Boards, a project, or a SPACE root | `python servers/_host/serve.py --root <root>` |
| One workbench only, own port and DOMAIN, no terminal, chat or Board writes | `python servers/_host/serve.py --root <root> --only <workbench>` |
| The labeling host, for annotators | `python plugins/haipipe-toolkit/servers/_host/serve.py --only labeling --root <root>` |
| One standalone Page Folder | `python skills/1_base/page/haipipe-page/cli/page.py serve <page>` (imports `servers/haipipe-page/standalone_server.py`; its workbench is `<DOMAIN>/w`) |
| One Page in the reader | `<DOMAIN>/_board/page?path=/<page .md or folder>`: the Page engine's `render_page`, the same document `page.py export --lane web` writes (`workbench/page_reader.py`) |
| Prove a refactor changed no response | `python servers/_host/tests/gate_live.py --fixture <board> --file <page-rel> --save … --diff …` |

## Adding a workbench · what every workbench does the same way

A new workbench follows the shared rules below, and `_host/tests/test_workbench_conformance.py`
fails until it does (JL 261003: "make sure other new workbench UI will do the same thing").
Families older than a rule are listed in that test's `GAPS` with what they still miss.

1. **Same shell.** Header, band, then the Space row with Guide mounted first by
   `mount_guide()`; each Space's View tabs and content sit in one box. Use the colors and
   tab sizes the Insight workbench and Guide use; do not restyle them per workbench.
   Spaces run Guide → setup → work → Delivery (`workbench/README.md` § Space order).
2. **One Guide, four Views.** Description · Method · RoadMap Draw · Related Paper, filled
   from the family's entry in `workbench/guide_families.py`:
   - `description`: what the workbench does, in a short paragraph;
   - `method`: its steps as text;
   - `method_doc` and `method_drawing`, with a `method` explain to `/_board/guide?mode=method`
     marked `"only"` (2026-10-03; Guide's own step list is then hidden, and stays in
     `method` for the RoadMap drawing): "The method in one picture" (the editable canvas
     `ref/<name>-methods.excalidraw`), then one document `ref/<name>-method.md` with the steps
     as its spine (JL 261003, as Design's): 1 · the steps, one table (`step | what happens |
     methods | where in the workbench | who signs`); then "Step N in depth" sections, each
     with its `family | method | card` table (cards in `ref/methods/<family>/`) and the
     `test | asks | when | source` rows of its own steps; then Why it works; then Reference,
     folded (terms and people with checked links, coined Chinese marked as ours). Every part
     is a fold, open at first except Reference. One made-up
     example throughout; no file notes on screen. `blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/method-canvas.py`
     draws the canvas's first version from the document; after that the canvas is the source;
   - `table`: the Workbench Table, `ref/workbench-table.md` beside its skill
     (Space · View · Run type · Agent · Skill · Person signs; `skills/0_utils/table-workbench`);
   - a `roadmap-draw` explain titled **Workbench design**: one generated drawing of the
     workbench (`studio/<name>.py` writes `studio/<name>.excalidraw`, Studio style, never
     edited by hand);
   - `papers_table` (or the family's own papers page as a `related-paper` explain): its
     papers in `ref/<name>-papers.md`, checked by `skills/0_utils/table-papers`.
3. **Inside Guide, no window-sized heights.** A page shown in Guide (one that posts
   `haipipe-explain-height`) gives every canvas and PDF frame a fixed pixel height; a
   `vh` height grows the frame without end and the canvas keeps zooming.
4. **Short address.** A Board's workbench answers at `<DOMAIN>/w/<board>`; a route row
   in `host_registry.WORKBENCH_ROUTES` and the folder name `workbench-<name>` are enough.
5. **No icon of its own.** The host answers `/favicon*` only for the Excalidraw app, so
   every workbench tab shows the browser's default icon. Do not add one.
6. **Runs on the right.** Every working Space, Guide included, puts its runs in the shared
   Runs panel to the right of its content: `workbench/runs_panel.py` (`panel_markup`,
   `PANEL_CSS`, `PANEL_JS`, and `SPLIT_CSS` for the layout), fed by the family's run cards or
   Workbench Table. It stays on the right at every width and folds to a vertical "◂ Runs"
   tab. Guide's panel lists the Workbench Table rows whose Space is Guide.

## Rules

1. **Arrow one way.** Servers import the Page engine's grammar
   (`skills/1_base/page/haipipe-page/src/`) and its `cli/` helpers (`check.py`, the Board
   checker; `draw.py`; `refs.py`). The Board skill is retired (JL 261005): its live
   parts moved into the Page skill, the rest was deleted. Skills import nothing from here, with one
   declared bridge: `skills/1_base/page/haipipe-page/src/page_assets.py` reads the Page
   look from `haipipe-page/assets`, so the reader and the web delivery agree.

   **One reader (JL 261004).** A Page is shown in exactly one way, the Page engine's
   `render_page`: in every workbench pop-out, at `/_board/page`, behind `/b/<board>/<page>`,
   and in its web delivery. Its default is reader mode (sentences run on as
   paragraphs, a folded Sources list per subsection; 🔍 Evidence brings back the
   per-sentence lanes). The Board's static site (`cli/build.py`, `board/**.html`)
   is retired and deleted: nothing links to it and no write rebuilds it. The
   Labeling workbench binds to the Page in the live reader too.
2. **Routes are the contract.** `/_board/<name>` URLs did not change in the
   move; `/b/` and `/w/` are short forms that redirect to them, and
   `haipipe-page/fn/serve-host.md` returns `board-url` and
   `workbench-url` in that short form. (The retired 🛠 skill map routes are
   the one removal: `/_board/skill*`, `/_board/skillview`, `/_board/mdview`.)
3. **A workbench owns its files.** Python, JS, CSS and vendor files for one
   tab sit in one folder. Adding a tab is adding a folder plus its
   `WORKBENCH_ROUTES` row; the host discovers the rest.
4. **A theme's server is a sibling folder.** The labeling theme, once its own
   plugin, is `workbench-labeling/` here; its engine and skills are
   `skills/2_theme/labeling/` (see `workbench-labeling/README.md`).
5. **Nothing personal.** Settings keys, defaults and printed examples are
   generic; a deployment's names live in its own `settings.env`.
