# The classic draft page · three Spaces and their routes

The classic page still answers on `/_board/draft`, `?view=draft` and `layout=frame`; nothing new is added to it.
The focus page (SKILL.md) is the current page. Kept so a reader of an old link knows what it opens.

**LOAD `workbench` FIRST.** It owns what any workbench is: storage,
surface, writer, boundary. This file owns the Page workbench's delta: what the
three Spaces show, what the Runs panel does, what `draft/` holds, and who
writes each file. `Space` is the name for a user-facing surface; `Workspace`
survives only in old routes and internal ids.

```text
📃 <page title>
↑ Board level
[ band: page kind · state · draft version ]
[Guide] [Draft] [Evidence] [Delivery]
┌ one box per Space: tabs, Views, content ──────────────┐ ┌ Runs, right ──────────────┐
│ Draft     Table Reading Scratch RoadMap-Draw Revise · ▸ Structure │ │ the run types of THIS view │
│ Evidence  Citations Displays Values Supporting Runs         │ │ + New Run                  │
│           View: All items · Card · Source                   │ │ one run: name · state ·    │
│ Delivery  Web LaTeX Word Slides (each with its state)       │ │ Rerun · ▸ Prompt (Copy) ·  │
│           View: Preview · Artifacts · Checks                │ │ process · results          │
└──────────────────────────────────────────────────────┘ └──── ▸ folds to a strip ──┘
```

**Shared shell.** The page wears the shell every workbench shares
(`servers/README.md` "Adding a workbench"; `_host/tests/test_workbench_conformance.py`):
the title, the `↑ Board level` link when the Board has a Board-level workbench
(no `all boards · board index` line), a band read from the page (`page-type`, `state`, the
latest draft version), then the Space row with the shared Guide first and plain Space
names. Each Space's Views and content sit in one box (`.space-split>.space-main`), and
its Runs panel starts folded to the strip until the person opens it (`panel_html(...,
folded=True)`; a person's own fold or open is remembered). The shell's colors and tab
sizes are the Insight workbench's, kept once in `space_views.SPACE_CSS`, which Page and
Paper share. Guide reads the `page` entry of `workbench/guide/guide_families.py`:
`description`, the Workbench Table `workbench-table.md`, the papers
`servers/workbench/workbench-task-draft/related/papers.md` (`table-papers`),
Method's page `servers/workbench/workbench-task-draft/guide/method.md` with its cards in `guide/methods/` and its editable
methods canvas `guide/methods.excalidraw` (the canvas is the source), and RoadMap Draw's **Workbench design**,
`servers/workbench/workbench-task-draft/studio/page-workbench-design.excalidraw`, the design authority
below (hand-made; Part 0 is the shared shell).

Design authority: `servers/workbench/workbench-task-draft/studio/page-workbench-design.excalidraw`.
Change the drawing and the code together, and check every view in real Chrome at
about 2000px wide (a narrow window is not the test).
## 🔗 Link and routes

Return the short address by default: `<DOMAIN>/w/<board-slug>/<page-id>` for a
Board-hosted Page, `<DOMAIN>/w` for a standalone one. `<DOMAIN>` is the origin
the reader uses (AGENTS.md § Board serving). The Board host (`serve.py`) reads it
from `.server_config/settings.env`; a standalone `page.py serve <page> --port N`
binds `127.0.0.1` unless started with `--host` and `--public-url`, so only a
loopback or port-forwarded link reaches it. The server redirects it to
`/_board/draft?path=…&file=…` and composes `path` and `file` itself; the old
`/_board/outline` address still answers. Label it `Workbench Link`. Follow the
redirect and read one real value off the response before returning any link.

The Page views are the frame's Task Spaces. A
Task's Page opens in the base frame, `/_board/workbench?path=<task>`, and each view is a subspace
drawn in place: Description › Folder, Audience Report › Draft, Work Details › Evidence · Value,
Runs › Page Runs, Delivery › Lanes. A tab link of a Task's Page (`/w/<block>/<page>/<tab>`) opens
that Space; a Page outside a Task folder keeps its own view. One route serves every view,
`/_board/workbench?view=<draft|evidence|value|runs|delivery|folder|pageruns>&path=<page .md>`;
the old addresses (`/_board/draft`, `/_board/runs`, `/_board/folderstat`, ...) answer as it on a
GET, and each POST twin keeps its address.

```text
lens=div | evidence | delivery | run      which Space opens (run = the All-runs view)
view=table | reading | scratch | revise   the Draft view
focus=C<n>.P<m>.B<k>                      Bullet permalink: opens, scrolls to, marks that Bullet
run=<exact run id>                        opens the All-runs view at that Run
/w/runs · /w/delivery · /w/folder · /w/evidence   tab words ride on the short address
```

A writing Step handoff follows `../../../../draft/hai-draft/ref/user-check-packet.md`.

The Page shell's tab strip is 📃 Page (this workbench, first and default),
📤 Delivery (the full lane surface, `delivery.md`) and 📂 Folder
(`folder.md`); a Page with `labeling/` adds 🏷 Labeling.
## 📝 Draft Space

The View row comes first, as Guide's (a rule under it, no "View" label; the file
and section each view reads is its tooltip); the Structure card shows in Table only.

1. **Structure card**: one folded line, `▸ Structure`. Open, it shows the
   Structure Overview (a division by its title, a paragraph by its title, its
   sentences and job, and the question leading on). Click the text to edit it
   as a box; Save (`action: structure`) renames or reorders headings in all
   three sections and saves the `→` lines. A paragraph that holds points cannot
   be dropped or re-addressed here; that is `run-structure` work.
2. **Reads**: which file and section each view reads, as the View row's tooltip.
3. **Table**: each Bullet's Point (section 1) beside its sentence (section 3). Read-only.
4. **Reading**: the sentences as prose (section 3). Read-only.
5. **Scratch**: the person's rough notes (section 2). Clicking a heading opens
   its note form; the first note opens `run-scratch-<c1-p2>` (its ticket
   only); later autosaves change only the notes; `Finish Scratch` asks for a
   short Summary and is the close (`results/`, one log line). It never edits
   Draft prose.
6. **RoadMap Draw**: the Section's logic as a tree, on an editable canvas at a fixed 640px height, read left to right: the
   claim at the left, each box splitting into the reasons it rests on, the Bullets as
   leaves (role and gist; solid green when their Evidence Items are verified, dashed
   orange while one waits). Each Bullet is its own row in one column, a Bullet that
   supports another just under it, stepped in, and the space right of the column stays
   free for writing.
   The drawing `studio/<stem>-roadmap.excalidraw` is the source of the logic: an agent
   draws its first version (Runs › Draw the logic; skill `0_utils/draw-logic-tree`, which
   owns the tree's rules and its `--check-scene`), then the person edits it here and every
   stroke saves through Studio. It never replaces an existing RoadMap without `--force`.
   With no drawing the View says so; rendering writes nothing.
7. **Revise**: one box per paragraph, pre-filled with its Draft (or the Page's
   own sentences where no Draft exists), one sentence per line, a blank line
   between points. `Save` or Cmd+Enter (`action: revise`) writes the changed
   Draft fields only. The first Save on a paragraph opens its Revise run,
   `run-revise-<c1-p2>` (`hai-draft-writing (ref/revise.md)`), whose ticket keeps the
   text before; later Saves change only the Draft; `page.py close-run` writes the
   Before / After ledger when the person says close. The status line under the
   box says `Saved · run-revise-0929-c1-p2 · 1 sentence` at once; the Runs panel is
   built with the page, so the run appears under Revise edits after a reload. No
   timer save; leaving with unsaved text asks first.
   Adding or removing points is Structure work.

Clicking a paragraph (its header in any view but Scratch, or a line in
Reading) selects it: the paragraph is outlined and the Runs panel narrows to
it; a second click clears it. The header click selects and does not fold (the
Scratch opener in `outline_scratch.py` cancels the fold outside Scratch view; a
read-only host has no Scratch opener, so there it also folds).

## 🔎 Evidence Space

1. **Reads line**: `draft/<stem>-evidence-items.md`.
2. **Tabs**: Citations · Displays · Values, each with its item count, then Supporting Runs.
3. **All items**: a table (ID · Item · Used by · State · Card), one row per item.
4. **Card**: the Result-first evidence page (`/_board/evidence`) in a frame,
   showing only the current tab's kind; its duplicate header and count row are hidden.
5. **Source**: that tab's section of the Evidence Markdown.

Selecting a row, or opening a card in Card view, selects that item: its row is
outlined and the Runs panel shows its runs. Switching to Card with a row
selected opens and scrolls to that card; a `Card` button on a row does both.
Used by is the item's Bullet address, from the Result, else the ledger target.

**Supporting Runs** shows the work the items stand on. It reads
each current item's `Supporting Runs` line (`Execution · reuse · b03j02t01r04;
…`), resolves every address through `live.runs.supporting_task_runs`, and draws
one tree: Execution or Discovery > Block > Job > Task > Run, each Run by its
ticket name with its state and one chip per Evidence Item it feeds. A chip
opens that item on its own tab; a Run selected in the tree narrows the Runs
panel, whose `Task runs` (hai-task) and `Discovery runs` (hai-discovery)
types list the same Runs with their Result files. An unknown address shows under `Not found`. A Supporting Run's owner
stays its Task or Discovery folder, never this Page.

Five layers stay distinct (full binding contract:
`../../../../draft/hai-draft/ref/page-run-families.md`):

```text
Evidence Item   authored obligation: what this Bullet needs        draft/<stem>-evidence-items.md
RE              Page-local run that makes the item ready           runs/run-<value|citation|display>-<slug>.md
Result          canonical fact and payload                         results/<re-run>/result.yaml
Evidence Card   read-only view of the current Result               Card view
Evidence Labels inline anchors into that Result: $V_x$ · \cite{C_x} · \figure{D_x} · \table{D_x} · \algorithm{D_x}
```

One item has one current RE lineage and one Card; one Result may expose many
Labels, and a Label never creates an item. External evidence stays at the
Supporting Run's real Result path and is referenced, never copied. The old
`outline/evidence/` folder and `*-evidence.md` snapshots are retired: move them
to `draft/_archive/legacy-outline-evidence/`; nothing reads them.

## 📤 Delivery Space

Tabs Web · LaTeX · Word · Slides, each with its state word (`pass`, `stale` or
`not built`, by file time against the Page); views Preview · Artifacts · Checks.
Nothing is edited in Delivery: a wrong word in a built file is fixed in the
Page or its exporter, then rebuilt. Lanes, writers and doors:
`delivery.md`.
