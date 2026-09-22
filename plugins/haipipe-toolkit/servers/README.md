# servers/ · the browser-facing layer of haipipe-toolkit

Everything a browser is served by lives here, and nothing here is a skill. The
folder is a sibling of `skills/`, `agents/` and `mcp-servers/`: plugin-level
infrastructure that hosts the skills' Boards and Pages, for any SPACE that
carries a `.server_config/settings.env`. Nothing in it names one person, one
lab, or one deployment.

```
servers/
├── _host/               the transport: serve.py, auth, config, the `live` namespace, shell JS
├── haipipe-board/       Board-level presenters (home, structure, write, activity, shell)
├── haipipe-page/        the standalone Page server and the reader appearance (page.css, css/)
├── workbench-page/      🧭 everything one Page's tabs render: outline, evidence, value,
│                        runs, delivery (latex/word/bibex exports), folder status, plugview;
│                        exporters/ holds the md2tex, md2docx and docx2pdf writers
├── workbench-paper/     📄 the Paper workbench
├── workbench-studio/    🎨 chat, terminal, draw (Excalidraw), slides, vendored xterm
├── workbench-insight/   🔎 InsightBoard and its Run Specs
└── workbench-design/    🎨 Design Folder and Design Board
plugins/subjective-label/servers/
├── _host/serve.py                 🏷 subjective-label's own host: this host with --only labeling
└── workbench-labeling/            🏷 the Labeling workbench, discovered by both hosts
```

## Two words, two things

A **skill** named `haipipe-workbench-<x>` is the contract: what the lane holds
on disk and who writes it (`skills/page/haipipe-workbench-page` says what
`outline/`, `runs/`, `results/` and `delivery/` hold). A **workbench** folder
named `workbench-<x>` is that contract's served face, where a person works on
it in the browser. Same name on both sides:

| skill (`skills/`) | workbench (`servers/`) |
|---|---|
| `page/haipipe-workbench-page` (Outline · Run Space · Delivery · Folder) | `workbench-page/` |
| `page/haipipe-workbench-studio` | `workbench-studio/` |
| `design/haipipe-workbench-design` (+ `ref/design-board.md`, the Board grain) | `workbench-design/` |
| `paper/haipipe-workbench-paper` | `workbench-paper/` |
| `insight/haipipe-workbench-insight` (+ `ref/insight-board.md`, the Board grain) | `workbench-insight/` |
| `subjective-label/skills/label-building-workflow/haipipe-workbench-labeling` | `subjective-label/servers/workbench-labeling/` |

## Two URLs, one DOMAIN

A served Board or Page answers at a reader's address and a worker's address,
and they take the same two words:

```
<DOMAIN>/b/<board>                 the Board index                  (302 → the generated site)
<DOMAIN>/b/<board>/<page>          one Page, as the reader sees it
<DOMAIN>/w/<board>                 the Board's workbench            (302 → /_board/<route>?path=…&file=…)
<DOMAIN>/w/<board>/<page>          one Page's workbench, 📃 Page
<DOMAIN>/w/<board>/<page>/<tab>    runs · delivery · folder · evidence · value · design · insight · labeling
```

`<board>` is the folder's slug (`01-topic-260722` → `topic`), `<page>` the
Board's page id (`QA1`, `S-Label-1`). `home.py` resolves both against the Boards
Home already discovers, picks the Board-level route from what `board.md`
declares, and fills in `path=`, `file=` (and `page=` for labeling) itself. The
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
| The labeling host, for annotators | `python plugins/subjective-label/servers/_host/serve.py --root <root>` (this host with `--only labeling`) |
| One standalone Page Folder | `python skills/page/haipipe-page/cli/page.py serve <page>` (imports `servers/haipipe-page/standalone_server.py`; its workbench is `<DOMAIN>/w`) |
| Static Board projection | `python skills/board/haipipe-board/cli/build.py <board>` (reads the asset bundle through `src/assets.py`) |
| Prove a refactor changed no response | `python servers/_host/tests/gate_live.py --fixture <board> --file <page-rel> --save … --diff …` |

## Rules

1. **Arrow one way.** Servers import the skills' grammar (`src/`) and CLIs
   (`cli/build.py`). Skills import nothing from here, with two declared
   bridges for the static builders: `skills/board/haipipe-board/src/assets.py`
   and `skills/page/haipipe-page/src/page_assets.py`, plus the `src/__init__.py`
   of both engines putting `_host` on `sys.path` for the few grammar modules
   that read live projections.
2. **Routes are the contract.** `/_board/<name>` URLs did not change in the
   move; `/b/` and `/w/` are short forms that redirect to them, and
   `fn/serve.md` in the Board and Page skills returns `board-url` and
   `workbench-url` in that short form. (The retired 🛠 skill map routes are
   the one removal: `/_board/skill*`, `/_board/skillview`, `/_board/mdview`.)
3. **A workbench owns its files.** Python, JS, CSS and vendor files for one
   tab sit in one folder. Adding a tab is adding a folder plus its
   `WORKBENCH_ROUTES` row; the host discovers the rest.
4. **Another plugin's workbench is optional here.** The host starts without
   `subjective-label`; its labeling routes then answer 404. The dependency
   runs the other way and is declared in `subjective-label/servers/README.md`.
5. **Nothing personal.** Settings keys, defaults and printed examples are
   generic; a deployment's names live in its own `settings.env`.
