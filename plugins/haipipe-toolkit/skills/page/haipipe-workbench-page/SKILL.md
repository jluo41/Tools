---
name: haipipe-workbench-page
description: >-
  The Page workbench of one Page, paired with servers/workbench-page: three
  Spaces (Draft, Evidence, Delivery), each with its content on the left and
  its own Runs panel on the right, over the Page's draft/ folder. Draft reads
  the three-section Draft Markdown (Table, Reading, Scratch, Revise); Evidence
  reads the Evidence Markdown and its Results (Citations, Displays, Values,
  Supporting Runs); Delivery shows the built web, LaTeX, Word and slides
  files. The Runs panel lists each view's run types from run-cards.md and
  copies prompts; it starts nothing. Also owns the 📂 Folder tab. Trigger:
  page workbench, workbench link, Draft Space, Evidence Space, Delivery
  Space, Runs panel, run type, run card, add a run button, draft folder, plan
  file, record shape, evidence bundle, delivery tab, folder tab, stale
  workbench, /haipipe-workbench-page.
metadata:
  version: "0.94.0"
  last_updated: "2026-09-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-workbench-page · three Spaces, Runs on the right

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means the workbench views and the `delivery/` artifacts its export doors write (`*-view.html`, `.tex`, `.pdf`, `.docx`, `index.html`): fix `servers/workbench-page/` or the Page source, then rebuild.

> ⛔ **No content hashes** (hard rule, JL 260928; AGENTS.md rule 9). A version is its number and date; staleness is file time. Never write, check or compare a sha256 in a Page, Result, record or workbench view.

**LOAD `haipipe-workbench` FIRST.** It owns what any workbench is: storage,
surface, writer, boundary. This file owns the Page workbench's delta: what the
three Spaces show, what the Runs panel does, what `draft/` holds, and who
writes each file. `Space` is the name for a user-facing surface; `Workspace`
survives only in old routes and internal ids.

```text
📃 <page title>
[Draft Space] [Evidence Space] [Delivery Space]
┌ content, left ───────────────────────────────────────┐ ┌ Runs, right ──────────────┐
│ Draft     ▸ Structure · View: Table Reading Scratch Revise │ │ the run types of THIS view │
│ Evidence  Citations Displays Values Supporting Runs         │ │ + New Run                  │
│           View: All items · Card · Source                   │ │ one run: name · state ·    │
│ Delivery  Web LaTeX Word Slides (each with its state)       │ │ Rerun · ▸ Prompt (Copy) ·  │
│           View: Preview · Artifacts · Checks                │ │ process · results          │
└──────────────────────────────────────────────────────┘ └──── ▸ folds to a strip ──┘
```

Design authority: `servers/workbench-page/studio/page-workbench-design.excalidraw`.
Change the drawing and the code together, and check every view in real Chrome at
about 2000px wide (a narrow window is not the test).

## 🧼 UI rule · as concise as possible (JL 260927)

Show content and the controls that act on it. Before adding a hint, count, id,
status line or breadcrumb, ask whether JL would click or read it; if not, leave
it out and put the explanation in docs. Removed on JL's request, never to
return: the Page bar, `⧉ run-*` copy chips, evidence chips under paragraphs
(`E01 ✓`), run sub-lines (`targets · v001 · s001`), the Structure jump line
(`C1 › P1 · P2`), sentence counts, the Runs header crumbs and totals, and short
`rp-` ids on screen (since 260928 the names on disk are readable too).

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

```text
lens=div | evidence | delivery | run      which Space opens (run = the All-runs view)
view=table | reading | scratch | revise   the Draft view
focus=C<n>.P<m>.B<k>                      Bullet permalink: opens, scrolls to, marks that Bullet
run=<exact run id>                        opens the All-runs view at that Run
/w/runs · /w/delivery · /w/folder · /w/evidence   tab words ride on the short address
```

A writing Step handoff follows `../haipipe-page/ref/user-check-packet.md`.

The Page shell's tab strip is 📃 Page (this workbench, first and default),
📤 Delivery (the full lane surface, `ref/delivery.md`) and 📂 Folder
(`ref/folder.md`); a Page with `labeling/` adds 🏷 Labeling.

## 🗂 The folder · product beside process

`<page>.md` is the PRODUCT: what the Page asserts. `draft/` is the PROCESS:
how it came to assert it (Page skill 0.118). The same layout is legal on any
unit, Task folders included.

```text
<page>/
├── <page>.md                          the Page Face; Delivery reads it
├── draft/
│   ├── <stem>-draft-v<G>.<S>[.<E>].md the ONE current plan: three sections (below)
│   ├── <stem>-evidence-items.md       Evidence Item contracts: ## Citations · ## Displays · ## Values
│   ├── records/                       context · requirement · discussion · feedback · files · log
│   ├── previous/                      every superseded plan version
│   ├── skill/                         ranked Page Skills (ref/skill-record.md)
│   └── _archive/                      old Outline evidence; migration only, never read
├── runs/<name>.md                     one ticket per run, flat (written when it opens)
├── results/<name>/                    one folder per run, the same name (written when it closes)
├── delivery/                          web/ latex/ word/ slide/ (generated)
├── workflow/                          machine receipts
└── studio/                            the person's own drawings and notes
```

The Draft Markdown has three sections that repeat one skeleton
(`### C<n>.P<m>` headings, `- B<k>` numbers); `haipipe-page` SKILL.md
§ "The Draft Markdown and Runs beside the content" owns it:

```text
## 1 · Structure · Bullet Point Table   ### Structure Overview, then each Bullet's Point and plan lines
## 2 · Scratch · What to write here     rough notes under each paragraph heading
## 3 · Draft · Reading and Revise       the sentences, one line per Bullet
```

Readers never parse the sections themselves: `src/plan_layout.py::to_canonical`
folds them into the one grammar in `ref/plan-grammar.md`, and every writer hands
its edited plan to `from_canonical`. `src/outline_version.py::plan_dir` finds
`draft/` first and still reads an unmigrated Page's `outline/`;
`page.py draft-layout <page>` migrates one Page or a whole tree. Every record is
found through `record_path`. No run list, date or history belongs in either
Markdown.

**Evidence names.** The stored id keeps its form (`E13-DISPLAY-cohort-overview`,
sealed Results carry it). People read the type-first short name
`Edisplay13`, `Ecite25`, `Evalue01` (`src/item_table.py::short_name`, JL 260928).

## 📝 Draft Space

1. **Structure card**: one folded line, `▸ Structure`. Open, it shows the
   Structure Overview (a division by its title, a paragraph by its title, its
   sentences and job, and the question leading on). Click the text to edit it
   as a box; Save (`action: structure`) renames or reorders headings in all
   three sections and saves the `→` lines. A paragraph that holds points cannot
   be dropped or re-addressed here; that is `run-structure` work.
2. **Reads line**: which file and section each view reads.
3. **Table**: each Bullet's Point (section 1) beside its sentence (section 3). Read-only.
4. **Reading**: the sentences as prose (section 3). Read-only.
5. **Scratch**: the person's rough notes (section 2). Clicking a heading opens
   its note form; the first note opens `run-scratch-<MMDD>-<c1-p2>` (its ticket
   only); later autosaves change only the notes; `Finish Scratch` asks for a
   short Summary and is the close (`results/`, one log line). It never edits
   Draft prose.
6. **Revise**: one box per paragraph, pre-filled with its Draft (or the Page's
   own sentences where no Draft exists), one sentence per line, a blank line
   between points. `Save` or Cmd+Enter (`action: revise`) writes the changed
   Draft fields only. The first Save on a paragraph opens its Revise run,
   `run-revise-<MMDD>-<c1-p2>` (`haipipe-page-revise`), whose ticket keeps the
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

**Supporting Runs** (JL 260928) shows the work the items stand on. It reads
each current item's `Supporting Runs` line (`Execution · reuse · b03j02t01r04;
…`), resolves every address through `live.runs.supporting_task_runs`, and draws
one tree: Execution or Discovery > Block > Job > Task > Run, each Run by its
ticket name with its state and one chip per Evidence Item it feeds. A chip
opens that item on its own tab; a Run selected in the tree narrows the Runs
panel, whose `Task runs` (haipipe-task) and `Discovery runs` (haipipe-discovery)
types list the same Runs with their Result files. An unknown address shows under `Not found`. A Supporting Run's owner
stays its Task or Discovery folder, never this Page.

Five layers stay distinct (full binding contract:
`../haipipe-page/ref/page-run-families.md`):

```text
Evidence Item   authored obligation: what this Bullet needs        draft/<stem>-evidence-items.md
RE              Page-local run that makes the item ready           runs/run-<value|citation|display>-<MMDD>-<slug>.md
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
`ref/delivery.md`.

## ▶️ Runs panel · one per Space

1. **Place**: a column on the right at every page width; `▸` folds it to a
   strip, `◂` opens it; the choice is remembered per Space in this browser.
   The folded strip turns green when a run awaits the person.
2. **Run types**: the `🔘 BUTTON` lines of
   `../haipipe-page-workflow/ref/run-cards.md`, as `label · Space · ticket
   pattern · views <names>`. A view or tab shows only the buttons that name it,
   each with its run count for the current target, then `+ New Run`.
3. **Target**: the selected paragraph or item narrows every list; nothing
   selected means the whole Page.
4. **Run card**: an id strip when there are two or more runs, the name, a state
   badge (Closed · Held · Awaiting you · Running), Rerun, the skill it uses
   (`Skill haipipe-page-writing · haipipe-writing`: a `skills:` line in its ticket
   or runtime, else its card's `🧩 SKILL` line; JL 260928), a folded `▸ Prompt`
   with Copy, the running process, and the Results folder with its files.
5. **Starts nothing**: Rerun, `+ New Run` and Copy copy a prompt (the
   `💬 PROMPT` line with `{page} {plan} {target} {button} {run}` filled in).
   The person runs it in a Claude or Codex session, which records who started it.

The panel opens on a type with a run awaiting the person, else the view's
first type with runs. The Evidence Supporting Runs tab adds `Task runs` and
`Discovery runs`; a run no button claims shows under `Other`.

**Which runs, where, in what order, with which skill** is the studio drawing's
section "The runs of a Page": 1 Context, 2 Structure revise, 5 Evidence embed
(Draft › Table) · 3 Task and Discovery runs (Evidence › Supporting Runs) · 4 one
run per Evidence item (Citations · Displays · Values) · 6 Auto write (Draft ›
Reading) · 7 Section revise, 8 Paragraph revise (Draft › Revise) · adopt (code) ·
9 Build (Delivery) · 10 Check (Delivery › Checks); Scratch and Revise edits any
time. Every card in `run-cards.md` carries the same Space, view and skill.

**Run names** (`src/run_names.py`, JL 260928): `run-<kind>-<MMDD>-<slug>`, the
name on disk and on screen alike (`run-section-0927-readability-cleanup`,
`run-paragraph-0928-c1-p2`, `run-value-0928-score-validation`); a taken name gets
`-2`. The three Delivery runs have one fixed name each, `run-delivery-webpage`,
`-latex`, `-word`, rebuilt in place. An older name (`rp-sec-07`, `re-value-07_x`,
`pj06t11r01_x`) still reads and is shown by `display_name` / `_name_by_item` until
`page.py run-names <page>` renames the Page once (flat `runs/`, `results/`, every
mention inside the Page; then `page.py export`).

**Records at the two ends** (JL 260928, AGENTS.md rule 3): `page.py open-run <page>
--kind <kind> --slug <words> [--target C1.P2] [--goal …]` writes the one ticket
(`status: open`); while open only the Page's text changes and the panel shows the
run as Running with no result; `page.py close-run <page> <run>` writes
`results/<name>/`, marks the ticket closed and adds one log line. The workbench's
own writers follow it: the first Revise Save on a paragraph opens
`run-revise-<MMDD>-<c1-p2>` (its ticket keeps the text before), and Finish Scratch
is the close of a Scratch run.

**To add a run type** for runs that already exist (a known ticket prefix), edit
`run-cards.md` only; the page rereads it on every load:

1. **Own prompt, own card**: every button in a card shares that card's first
   `💬 PROMPT` (`runs_panel.py::run_types`); a button that needs its own prompt
   gets its own `## \`…\`` card.
2. **Patterns never overlap**: a run joins the FIRST button, in card order, whose
   pattern matches its ticket name, so `re-value-check-` would fall under `^re-value-`.
3. **No runs yet**: a button with no runs shows `No runs yet.`; its prompt is
   copied from `+ New Run`, where `{run}` is not filled, so a new-run prompt never uses it.
4. **Selection**: a selected paragraph or row finds a run through the run's
   `target:` (a Bullet `C1.P2.B3` also counts for `C1.P2`) and its Evidence item
   (an `item: E<NN>-…` line near the top of its `.md` ticket), never its name
   (`runs_panel.py::_targets`).

**A new ticket prefix is a new Run family.** Prefer a Step inside an existing
Run when the work belongs to it. A new family needs all of:

1. **Owner skill** under `../workflow-runs/` (run-cards.md leaves Run authority
   to it) and its card in `run-cards.md`.
2. **`../../../servers/workbench-page/runs.py`**: `_TICKET_NAME` (else the run
   never appears); for a Page writing run also `_valid_page_run_id` (else it shows
   Held) and the label helpers `_page_run_label`, `_page_writing_subspace`,
   `_run_name`, `_run_action`.
3. **`runs_panel.py::_DISPLAY`**: its full-word name (`run-…-NN`); a family
   already named in full words (`run-delivery-latex`) needs none.
4. **`../haipipe-page/src/run_folders.py::_KINDS`**: its `runs/<space>-run/` folder.
5. **Docs**: `../haipipe-page/ref/page-run-families.md`, `../haipipe-page-workflow/`
   (SKILL.md, `ref/interactive-writing-run.md`), `../../run/haipipe-run/ref/run-catalog.md`,
   and a case in `servers/haipipe-page/tests/test_runs_panel.py`.

Cross-check by mirroring the newest family: `grep -rnE "rp-revise|_REVISE_RUN|revise\)"`
over `servers/workbench-page`, `skills/page` and `skills/run` lists every place it is registered.

A new tab or view needs `space_views.py`.

The All-runs view (`lens=run`, reached by a `?run=` link, no button) is the
older full Run presenter: `ref/run-space.md`.

## ✍️ Who writes what

```text
file                         written by                                         regenerate with
───────────────────────────────────────────────────────────────────────────────────────────────────
plan (draft-v*.md)           run-structure (SHAPE/SURVEY); evidence embed appends; never
                             the Structure card, Scratch and Revise saves
evidence-items.md            SHAPE/SURVEY item contract                           never (authored)
records/context              CONTEXT (haipipe-page-context)                       haipipe-page-context
records/requirement V | W    V: cli/requirement.py · W: the author, kept verbatim cli/requirement.py <page>.md
records/discussion           any Run or the page chat, as D<nn> records           never (authored)
records/feedback             cli/feedback.py collect; the Page writes Landed      cli/feedback.py collect
records/files · log          any Run or the page chat; log is append-only         never (authored)
<page>.md ## Content         page.py adopt, from the Draft                        page.py adopt
delivery/*                   the exporters (export.py, exporters/)                rebuild the lane
```

The workbench calls no model and writes only through `POST /_board/draft`:
`action: scratch` (notes and a Scratch Run), `action: revise` (Draft fields and
a Revise Run Step), `action: structure` (headings, logged in `records/log`).
Without an action the POST only registers the tab. `edit-preview`,
`edit-bullet` and `append-bullet` are refused: sentences are edited in Revise,
Bullets and structure through `run-structure`. All three write the current plan
file in place and do not check `approved:`: Scratch and Revise change only
sections 2 and 3, the Structure card only headings and the Overview. A new
Shape version (`approved: ⬜`, `supersedes:`) is `run-structure`'s job.

## 🔒 Versions · generation · Shape · evidence

```text
v0.16       pre-Content Shape 16            v1.0.1   same approved Shape, evidence fold 1
v0.16.1     same Shape, evidence fold 1     v1.1     bounded Shape revision in generation 1
v1.0        first approved generation       v2.0     major redesign after a review round
```

The version is `v<G>.<S>[.<E>]`; no `E` means zero. `G=0` never touches
Content. A Shape change increments `S` and resets `E`; an evidence fold
increments `E` and inherits its Shape's approval (`shape-base:`). `approved:`
is a person's act; a machine only transcribes it. At release,
`../haipipe-page/ref/release-decisions.md` decides profile precedence.

## 🤝 Review packet

When a person asks to review or approve a plan, the structure Run answers with
one linked packet (current Shape, evidence owed, what shaped it, the decision
asked) and the Draft and Evidence links: `ref/review-packet.md`. It writes
nothing.

## 📂 Files

- `ref/plan-grammar.md` · the canonical plan grammar every reader parses
- `ref/item-table.md` · Evidence Item identities, Run graph, derived status
- `ref/record-shape.md` · the six records: ids, labels, writers, rules
- `ref/specimen-section-plan.md` · an approved Section plan, frozen
- `ref/evidence-bundle.md` · the derived per-Bullet evidence join
- `ref/evidence/citations.md` · `values.md` · `displays.md` · `pagex.md` · per-kind authority
- `ref/space-mapping.md` · UI Space → renderer → Markdown or Result
- `ref/run-space.md` · the All-runs view (`lens=run`)
- `ref/delivery.md` · the Delivery lanes, writers and doors
- `ref/folder.md` · the 📂 Folder tab: live inventory and rebuild pills
- `ref/content-preview.md` · candidate prose storage and the CONTENT handoff
- `ref/review-packet.md` · the review packet
- `ref/skill-record.md` · the ranked Page Skills store
- `../haipipe-page-workflow/ref/run-cards.md` · the run types and prompts the panel shows
- `../../../servers/workbench-page/outline.py` · the page shell, the Spaces, the Draft views
- `../../../servers/workbench-page/space_views.py` · Evidence and Delivery tabs, views, selection
- `../../../servers/workbench-page/runs_panel.py` · the Runs panel
- `../../../servers/workbench-page/outline_structure.py` · `outline_scratch.py` · `outline_revise.py` · the three writers
- `../../../servers/workbench-page/evidence.py` · `delivery.py` · `export.py` · `exporters/` · `runs.py` · `folderstat.py`
- `../../../servers/workbench-page/studio/page-workbench-design.excalidraw` · the design drawing
- `../haipipe-page/src/plan_layout.py` · `outline_version.py` · `item_table.py` · `page_question.py`
