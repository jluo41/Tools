This file holds the full Page Folder tree and the Draft Markdown with the Runs beside the content, moved from `SKILL.md` § 📁 What a page is on disk.

A page is one markdown file (the PRODUCT: what the page asserts) beside one
process folder (how it came to assert it) and the workbench lanes it actually
uses. The roster of legal folder names is `workbench/ref/roster.md`.

```text
<page>/
├── page.toml     optional standalone registration: source + imported content
├── <page>.md      Opening · Content                         THIS reader contract
├── draft/         HUMAN process (`outline/` on Pages not yet moved; see below)
│   ├── <stem>-draft-v<G>.<S>[.<E>].md  the ONE current plan: Draft Markdown,
│   │                                   three sections on one skeleton
│   ├── <stem>-evidence-items.md  Evidence Markdown: ## Citations · Displays · Values
│   ├── records/   context, requirement, discussion, feedback, files, log, inputs
│   ├── previous/  superseded plan versions, moved here when a new one is written
│   └── _archive/  retired folder material only
├── workflow/      MACHINE process: Workflow Runtime/compatibility receipts
│              ─── the LOWER, TASK-side part ───
├── scripts/       optional owned implementation, any language; shared Task
│   └── config/    Job code stays one level up in `src/`
├── runs/          one folder per Page Run: runs/<name>/{<name>.md, run.yaml, passes/pNN-<MMDD>/}
│                  (run-<kind>-<slug>, run-delivery-<lane>); THE ONE execution door
├── results/       older Pages only: Results before one folder per Run (0.125).
│                  A canonical Task Page resolves
│                  generated output at `$OUTPUT_ROOT/<task>/results/<run>/`
│              ─── the UPPER, PAGE part ───
├── delivery/      what leaves the page: web/ · latex/ · word/ · slide/ · render/ (a Task in a Block builds
│                  to <block>/delivery/jNN_<job>/tNN_<task>/<lane>/ instead, never into the Task)
└── studio/        the HUMAN's room on the page (JL 260831): closest to
    ├── chat/      the person · you talk here, sessions kept
    └── draw/      you draw here, one scene per owner; the chat may
                   redraw the scene's named elements on your ask
```

**The Folder symmetry**: every Folder has a Page Face and Task Face; a
`primary_face` says which is the usual entry, not which face exists.
`draft/` is the human planning/decision record and `workflow/` is the
machine-readable Workflow/Run record. Page-heavy work commonly stores
compatibility receipts under `workflow/receipts/`; executable work commonly stores
`plan.yaml` and `report.yaml`. Run Space is an Outline projection over this
shared Task Face. It presents Page Writing, Page Evidence, and Supporting Runs.
A native Run pairs its ticket with either a Folder-local Result or the Task
dialect's resolved `$OUTPUT_ROOT/<task>/results/<run>/`, but the Page surface
shows the Result first when its card opens; scripts, config, and notebooks
stay in Folder/detail inspection. Run is never a top-level Page Workbench or a
lifecycle owner.

New Page Evidence is an `RE` Page ticket plus a bound Result. A Folder-local
Result is stored as `results/<re-run>/result.yaml`; a Task-backed Result stays
at the owner dialect's resolved output path, and the RE records that path and
Run id. One Evidence Item has one current RE lineage and one current Result/Card
projection; that Result may expose many stable labels such as
`$V_xxx$`, `\figure{D_xxx}`, `\table{D_xxx}`, `\algorithm{D_xxx}`, and
`\cite{C_xxx}`. The hidden
binding retains the Evidence Item, RE, Result path, and provenance. A label
that needs an independent acceptance or execution lineage becomes another
Evidence Item/RE. `outline/*-evidence.md` and `outline/evidence/*` are retired
locations, not runtime inputs. Move them to
`_archive/legacy-outline-evidence/` before the Page is treated as v4-ready.
The authored `draft/*-evidence-items.md` file remains the Outline Item
contract.
New cross-Folder evidence enters through Supporting Run references in the `RE`
Result; the external Ticket and Result stay at their owner and are never copied.

A unit MAY carry a `README.md`, and it is DERIVED (JL 260831): a generated
projection of the two-part tree as it actually stands (which lanes exist,
their counts, where the product and the rendered page live), regenerated
whole and never hand-edited — the structure's law lives HERE and in the
roster, so a hand-written copy per folder would be a second authority that
drifts. GitHub renders it where the board cannot reach; the 📂 tab computes
the same walk live (`servers/workbench/workbench-task-draft/folderstat.py`, whose `--write` becomes the
generator).

A folder is created only when it is used. Values are typed Evidence Items;
their ready local Result and provenance are shown inside the Outline
Evidence Space. Every number shown on a Page Face that comes from a Run crosses
ONE page-serving collection job (`task-type: evidence`, contract
`haipipe-task-for-evidence`); the Supporting Run Result becomes the explicit
cross-Folder evidence edge. A display-input Run therefore feeds the
page-serving collection Job; it does not bypass that one numeric door to feed
a Page DISPLAY unit directly. A local Run
may validate or reshape non-authoritative intermediates, but it
cannot become a second value door. A reusable derivation, a source-data change, or any displayed
numeric result belongs in the linked executable Folder and its Run Result
binding. The
the `draft/` process files, their ids, labels and writers are
`workbench-task-draft/ref/record-shape.md`; the plan's grammar is
`ref/plan-grammar.md` beside it. A Run Spec owner loads the exact
Outline-workbench refs it needs as schema/material contracts. The Page surface installs
`workbench-task-draft` once as the presenter; the presenter skill is not
appended to each Run's execution dependency chain.

## 📄 The Draft Markdown and Runs beside the content (0.118)

The plan is one Markdown a person can read and edit by hand: three sections
that repeat one skeleton (`### C<n>.P<m>` headings, `- B<k>` numbers).

```text
## 1 · Structure · Bullet Point Table   ### Structure Overview, then per paragraph each
                                        Bullet's Point and its plan/evidence lines
## 2 · Scratch · What to write here     rough notes under each paragraph heading
## 3 · Draft · Reading and Revise       the sentences, one line per Bullet
```

The Structure Overview declares each division, then gives each paragraph a
title line, its sentences and job, and the question that leads to the next:

```text
- C1 · Introduction
- C1.P1 · Physician prescribing behavior
  → s1 to s6 · quality and spending · comparable decisions · opioid example
  → C1.P2: Could interpersonal dispositions help explain variation?
```

A part line names its part: `- C1 · Introduction`. A bare `- C1`, `- C1 ·` or
`- **C1**` still reads as part C1, with no title (261122). A Bullet that sits
under no part line the reader understands is never addressed as C0: `page.py
health` fails it with "part line needs a label". When a Page line with no
`realizes:` tag follows a tagged one, health counts it as part of that Bullet.
So the sync check names that text and asks you to tag it or add it to the Draft.

In the workbench the Structure card opens from its folded `Structure` line and
shows these entries (a division shows its title only); clicking them edits them
as text: renaming or reordering a `C1.P1`
line moves its headings in all three sections, and the `→` lines are saved
into the overview.

`src/plan_layout.py` folds the Draft section back into the Draft-first plan
for every reader (`canonical_plan` calls `to_canonical`), and every workbench
writer hands its edited plan to `from_canonical`, which rewrites sections 1
and 3 and keeps the Structure Overview, Scratch notes and any trailing
section; a renamed paragraph is renamed in all three sections. A Scratch save
writes the notes under their heading with one hidden marker line
(`<!-- run-scratch-0928-c1-p2 · paragraph · open -->`); notes typed by hand are
read too. No run list, date or history belongs in either Markdown.

`src/outline_version.py::plan_dir` finds `draft/` first and `outline/` on
older Pages; `latest_outline` and `retire_superseded` read both `-draft-v` and
`-outline-v` names. A new Run is one folder, `runs/<name>/`
(`src/run_folders.py`): its ticket, `run.yaml` and one `passes/pNN-<MMDD>/` per close. An older Page's flat
`runs/<name>.md` with `results/<name>/` still reads; `page.py run-names` moves it into folders.

The workbench has three Spaces, each tab one part of a file, each Space with a
`Reads` line naming that file (`servers/workbench/workbench-task-draft/space_views.py`):

```text
Draft      Table ## 1 · Scratch ## 2 · Reading, Revise ## 3 of the Draft Markdown
Evidence   Citations · Displays · Values = evidence/cards.yaml (a Page made before 2026-10-16: the ##
           sections of <stem>-evidence-items.md);
           views All items (ID · item · used by · state) · Card · Source
           Supporting Runs = every item's `Supporting Runs` line as a tree
           (Execution/Discovery > Block > Job > Task > Run, each Run with the
           items it feeds); views All items (the tree) · Source (those lines)
Delivery   Web · LaTeX · Word · Slides = delivery/<format>/;
           views Preview · Artifacts · Checks (read only)
```

Each Space's Runs panel is a column on the right of its content that stays in
view while the page scrolls (JL 260927): run types on top (the `🔘 BUTTON`
lines of `haipipe-draft-workflow/ref/run-cards.md`; each view or tab lists only
its own types through their `· views`: Table · Structure revise, Evidence
embed; Reading · Auto write; Scratch · Scratch; Revise · Section and
Paragraph revise; each Evidence tab its own kind, older `pj..t..r..` runs
joining the item they serve; Delivery Preview and Artifacts · Build, Checks ·
Check, with the format tab picking that format's builds), the selected run
below them with Rerun, a
prompt to copy, its process and its results, and the `runs/` folders it saves
in. Selecting a paragraph or an item row (`E40`) narrows the panel; a panel
folds to one line. There is no Page bar above the Spaces (JL 260927: "I don't
need this"); the Check prompt lives in the Delivery panel, and an old
`?lens=run` link still opens the page-wide run list. Buttons copy prompts;
they never start a run by themselves.

`page.py check-page-folder <page | board>` says whether each Page is on this
layout and names the fix for every rule it misses (`fn/check-page-folder.md`;
the rules live in `src/layout_check.py`).

`page.py draft-layout <page | board | tasks-dir> [--sort-runs]` moves a Page, or
every Page under a Board or Task tree, to this layout (a Task Page with no plan
yet only gets `draft/`): it
renames `outline/` to `draft/`, writes the three-section plan as the next
version (refusing if any Bullet would change), groups the Evidence Markdown
into `## Citations`, `## Displays` and `## Values` (refusing if any item block
would change), and with `--sort-runs` moves
each ticket into its Space folder, fixes moved scripts' paths, and repoints
`runs/<name>` citations. It then rewrites `outline/` paths that name a migrated
Page's plan folder, inside each Page and in the files around them
(`sweep_outline_paths`; `_archive/` outside a Page keeps its layout). With
`--archive-evidence` it moves retired Evidence lanes to
`draft/_archive/legacy-outline-evidence/`, except a `display/` lane whose units
have no DISPLAY Result yet. A Page it refuses in a tree run is reported and the
other Pages still move. Sealed `results/` are never edited, and a Run ticket keeps an `outline/` path that its own Result recorded.
