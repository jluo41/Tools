s51 · Server runtime
====================

**Topic:** how the workbench server runs today: how it starts, which folders make it up, how one
request finds its page, how the base frame draws a folder, which routes each workbench answers,
and where SPACE Home's links land. It is the first server topic: s01-s13 design the ladder and the
screens; s51 on are the served side of that design (JL 261007: "you can do it like s51_xxxx, for
the front end part").

**Feeds:** `reports/` q08_workbench_base · q09_studio_report_on_screen · q12_space_hosting ·
q07_workbench_mapping.

**Source:** every fact in the drawing is read off the server code at build time
(`Tools/plugins/haipipe-toolkit/servers/`): the folders from `host_registry.server_folders()`, the
mixins from `serve.py`'s `class Handler(...)`, the GET routes in `do_GET`'s order, the routes per
workbench from `WORKBENCH_ROUTES`, the themes on the frame from each `*_theme.py`. A rebuild
redraws it from the code as it stands.


**Routes, by who answers them (JL 261007: "how these linked to the themes and workbench base
URL?"):** frame 3 is a table of the 26 GET routes, one row per server folder: its theme, whether
that theme is on the frame, its routes, and how a person gets there. Every Block opens at
/w/<block>, which redirects to the base URL /_board/workbench; the frame picks the theme from the
Theme folder the Block sits in, or the theme that claims the Block by what it holds. Every theme
has its <theme>_theme.py now (261007) and is drawn inside the frame; the frame has no band and no
link to a theme's older <theme>-board page, which answers only at its own address. A Page's tabs (/w/<block>/<page>/<tab>)
redirect to the base's Task-level routes (blue). None is dead; /_board/health is a status check
nobody links. /_board/run-result is opened from every Runs panel, though its code sits in
workbench-paper.

**The Task level's routes, merged into the frame (JL 261007: "why not merge them into the base?";
"go ahead and do it"):** they were the old Page workbench, one route and one page per tab. Now they
are the frame's Task Spaces, each view a subspace drawn in place (`workbench/frame.py` PAGE_VIEWS);
a theme keeps them beside its own subspaces. One route serves them all,
`/_board/workbench?view=<view>&path=<page .md>` (`frame_view.py`). The old addresses answer as it on
a GET or HEAD (`serve.py` PAGE_VIEW_ROUTES), their POST twins keep theirs, and a Task Page's
`/w/<block>/<page>/<tab>` opens its Space in the frame. GET routes: 26 before, 18 now.

```text
old route               the frame's Task Space › subspace
draft (· outline)       Audience Report › Draft
evidence · value        Work Details › Evidence · Value
runs                    Runs › Page Runs
delivery                Delivery › Lanes
folderstat              Description › Folder
pageruns                no Space: the Draft view's stepper reads it (json)
```

**Board pages named as their themes (261007, JL: "make them the same to the theme name"):** every
theme's board page is `/_board/<theme>-board`; `task-board` is now `work-board` and `paper` is
`paper-board`. The old names still answer (serve.py `OLD_ROUTES`).

**Status and next (261007):** frame 7, read at build time. Done: 18 GET routes (26 this morning);
four themes on the frame (cowork, design, paper, work); board pages named as their themes; 10 old
addresses still answering. Next, in order: restart the live servers (all started before today's
serve.py change); one route table for do_GET and do_HEAD; discovery, insight and labeling onto the
frame; retire the old board pages; the item views (run-result into the base, the rest as pop-outs);
hosting for colleagues (Q12).

Files
-----

```text
s51-server-runtime/
├── s51-server-runtime.md            this face: how it works, what was checked, what is open
├── build_s51_server_runtime.py      the builder; reads the server code; marks are kept on rebuild
├── s51-server-runtime.excalidraw    the drawing: seven frames and Questions
└── s51-server-runtime.png           its preview
```

Rebuild: `python build_s51_server_runtime.py` (or `../_build/make.sh`).


How the server works
--------------------

```text
serve.py --root <SPACE> --port <N>
  │  settings.env (PORT, BIND_HOST, AUTH_FILE, DOMAIN ...), a flag wins over the file
  │  no claude_agent_sdk? re-exec under <root>/.venv/bin/python
  ▼
ThreadingHTTPServer ── Handler (one class of ~30 mixins, each from live.<module>)
  │
  ▼  one request
  auth → terminal off? → --only? → Home → /b/ · /w/ short address (302) → private file?
       → /_board/<name> → that mixin's view → HTML (built per request, read from disk)
       → else a static file under --root
```

1. **One process, one root.** `servers/_host/serve.py` serves one SPACE root. Nothing is built
   ahead: every page is made from the files on disk when it is asked for, so an edit on disk
   shows on the next reload. Code is different: the server never reloads, so a code change
   needs a restart.
2. **Many folders, one namespace.** Every folder under `servers/` (the host, `space-home`,
   `haipipe-page`, the base `workbench` and its `task-page`, each `workbench-<theme>`) puts its
   `*.py` on one package, `live`, so `from live.frame import ...` works wherever the file sits. Their
   `assets/js` and `assets/css` are joined into one `board.js` and one `board.css`.
3. **One request.** `do_GET` checks sign-in, the terminal switch and `--only` first, then tries
   Home, the short `/b/` and `/w/` addresses (a 302 to the long `/_board/<name>?path=…`), then each
   `/_board/<name>` in turn; anything else is a static file, except private ones.
4. **The frame.** `/_board/workbench?path=<folder>` draws any Block, Job or Task folder: the
   folder's name gives its level (`bNN_` · `jNN_` · `tNN_`, a `board.md`, or the theme's own
   names, `Theme.level_patterns`: paper's `Ba-`/`Bb-`/`Bc-` groups are Jobs, its `S-` Sections
   Tasks), the Theme folder it sits in gives its theme, the vanilla
   defaults fill all six Spaces from the standard folders, and the theme's `<theme>_theme.py`
   replaces only the Spaces it fills. A theme that fails to import falls back to vanilla.
5. **The frame is the door (261007).** `/w/<block>`, `/b/<block>` and every SPACE Home card
   open the frame. It has no band line and no link to a theme's older page (JL 261007: "why I
   still have this? please remove that"); the level tabs say where you are, the folder's path is
   the title's tooltip. An old page answers only at its own address (`/_board/paper-board` now
   forwards to the frame). All seven themes are on it (cowork, design, discovery, insight, labeling, paper,
   work; the last three added 261007). A theme may claim a Block kept in another Theme folder by
   what it holds (`Theme.claims`): an Insight Block in `tasks/` (`workbench: insight`), a labeling
   Block in `tasks/` (its `schema.yaml`). An `--only <workbench>` host serves no frame, so it keeps the theme's own
   page. An older `?view=questions#question-QNN` link opens Audience Report on that row.
6. **Base styles only (JL 261007).** A frame page carries the frame's own CSS and the base's shared
   view styles (`SPACE_VIEW_CSS`, `WORK_ITEM_CSS`, `.st-ok` · `.st-warn` · `.topic.missing`), never a
   theme's stylesheet; a theme's Space html uses base classes, and a missing component goes into
   the base. A guard test keeps those styles off the frame's own parts.
7. **The Guide by level.** A family whose `guide.yaml` has `levels:` (paper, work) draws every Guide
   View as three folding sections, Block · Job · Task, of cards; the words come from
   `workbench/guide/levels.yaml` with the theme's overrides, a Space card's `sub` and `runs` live from
   the frame; the frame passes its level so that section opens (frame 8; b03 `s31-guide`).
8. **A Page Task.** A theme whose Tasks are Pages (paper's Sections) returns
   `frame.page_task_spaces`: Description Scope · Plan · Requirement · Records, Audience Report Table ·
   Reading · Questions, Work Details Draft-… · Evidence-…, Delivery LaTeX · Word, each view the Page
   itself embedded (`/_board/draft?…&embed=1`); run cards per view, none on Table and Reading. The
   paper theme adds its own lines over it. Other Tasks keep the Page views as extra tabs
   (`PAGE_VIEWS`, design-b03-project), which step aside where a theme lays the Page out.


Checked (261007)
----------------

- Host tests: `_host/tests` 47 passed; `workbench-work` 21, `workbench-cowork` 12,
  `workbench-design` 5, `workbench-discovery` 4 passed.
- A fresh server on the current code: Home and `/_board/health` 200; the frame on every Block
  under the root (68), their first Jobs and Tasks, all six Spaces: 1,620 requests, all 200, none
  over 3 s; the Guide, 9 families × 4 Views, all 200.
- `/w/<block>` for all 68 Blocks: all land, except one slug two labeling Projects share (a 404 by
  design; the long address works).
- Not fixed here: `haipipe-page/tests/test_standalone_server.py`, 5 of 26 fail, the same at the
  last commit; they test the standalone `page.py serve` host, not the SPACE server.
- About a dozen older `serve.py` processes from earlier sessions are still running on other
  ports with the code they started with.
- Later the same day: `_host/tests` 70 passed, work 21, paper 4, cowork 12, design 5, discovery 4;
  the frame sweep 1,626 of 1,626; the card Guide on every work Block, Job and Task, 908 of 908;
  paper's 9 Jobs and 50 Sections at their levels; the Sections' Page views, 50 × 17 screens,
  850 of 850, every embedded view loading.


Open
----

1. Decided (JL 261007): `/w/<block>` opens the frame now, before the theme files. Checked: all
   72 Home cards land in the frame, 70 with an old page link, all 70 of those load.
2. Every theme is on the frame (261007). Each old page retires once its theme's Spaces hold all
   it shows; still only on old pages: insight's Check gates, discovery's add-resource and
   add-drawing forms, labeling's annotation views (the frame links them; it never writes labels).
3. A theme that fails to import falls back to vanilla without a word: say so on the page?
4. No reload on a code change, and old processes keep serving old code: a restart command, or a
   watch?
5. Hosting for colleagues (Q12): an always-on host, sign-in, a viewer mode with no writes.
6. `do_GET` and `do_HEAD` each list every route: one route table instead of two if-chains?
7. One mechanism for a Task's Page views: `page_task_spaces` for every Page Task, then `PAGE_VIEWS` goes?
8. Evidence-Supporting has no Task runs / Discovery runs card in `run-cards.md` yet, and the cards'
   `views` lines still put Structure revise, Evidence embed and Auto write on Table and Reading.
9. A Section's Questions: the Work column should list the Runs that worked it and what they changed.
10. `question_rows`: one heading per group in All, for every theme?
11. Paper: `Ba-` (Main) and `Bb-` (Appendix) are two Jobs today; s12 draws one version Job (Q01).

(write here, or mark the drawing in red)
