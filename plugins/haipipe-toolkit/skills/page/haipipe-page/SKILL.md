---
name: haipipe-page
description: >-
  Create, edit, build and serve a self-contained Page Folder from a supplied
  Markdown, text, HTML or other file, without requiring a Board. Also owns
  the Page Face contract and router of a Folder: what the readable .md is on
  disk, how its Run Workflow/Run Spec owner or legacy Page Type is resolved,
  which Run Spec holds authority, and PREVIEW, CREATE, WORK ON, RUNS, RUN. Trigger:
  file to page, HTML page, standalone page, host a page, open page code,
  create a page, update page, propose Page Runs, human-interaction runs,
  run page lifecycle, Page Face, Folder kind, legacy Page Type, Run Spec,
  /haipipe-page.
metadata:
  version: "0.112.0"
  last_updated: "2026-09-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page · one shape every page keeps

This is the executable door for ONE PAGE, with or without a Board. Say
`haipipe-page <file>`, `make this HTML file a Page Folder`,
`create a new page on <topic>`, `working on <page>`, or `run <page>`.
The canonical skill and runtime live in `skills/page/haipipe-page`.
An ordinary file is imported into a new Folder; an existing Page Face or
Page Folder is opened in place. Never silently wrap an existing Page again.

```text
haipipe-page                     haipipe-board
──────────────────────────       ──────────────────────────────
Page Folder and source authority Board membership and page groups
individual rendering and assets  navigation, index and aggregate build
standalone server and editing    Board hosting adapter to the same Page code
Page template and base contract  aggregate checker and cross-Page rules
```

The Page owns its parser, renderer, workspace server and template. Board calls
that same implementation through compatibility imports; it does not own a
second Page renderer. The authoritative template is `ref/page-template.md`.
Legacy Board paths remain compatibility links, not parallel authorities.

## ⚡ Fast feedback Step

When the person gives wording feedback on an already open Page Run, use the
fast foreground path by default. Read only the Run resume view, the latest
Version tail, the named paragraph slice, its dependent Bullet, and the frozen
Mermaid description. Make one bounded patch, update the required small Run
projections, perform one narrow check, and return the review packet. Target
under two minutes. Do not reread the whole Page, update the plan for a
wording-only change, rebuild anything, run broad tests, verify the browser, or
start or wait for a sub-agent. If a required record is missing, report the one
blocker instead of scanning the repository.

## 🤝 Two top-level doors, one Folder

`haipipe-page` and `haipipe-task` are peer entry doors. For a Page whose
`folder-kind: task`, both operate on the same physical `tNN_<task>/` Folder:

```text
Task door  executable work, P-B-E-R, native rNN, Result readiness
Page door  human interaction, typed RP/RE, evidence binding, Content, CHECK, release
```

Enter through Task when the primary product is independently testable output;
enter through Page when it is reader meaning or human acceptance. Page may
propose Task work but never allocates its native Run. Task may return a Result
but never accepts Page wording, closes a Page Run, or releases the Page.

For Task Folders, load `../../task/haipipe-task/ref/task-page.md` as the
detailed bridge. It owns the cross-face handshake, staleness propagation, and
the rule that the Folder closes only when both Task readiness and Page
readiness are current.

## 🏃 Page Run families inside Outline

Load `ref/page-run-families.md` before naming or allocating a Page Run. Plugin
Outline's Run Space presents three semantic areas plus the owner-native
Supporting group, in both standalone and Board-hosted mode:

```text
Page Writing  RP · rp-struct-NN · rp-scratch-NN_<target> · rp-sec-NN · rp-para-NN_Pxx[-Pyy]
              Structure · Scratch · Section · Paragraph (Review & Modify)
Page Evidence RE · re-value-NN_<slug> · re-display-NN_<slug> · re-cite-NN_<slug>
              Value · Display · Citation
RD         rdNN_<target> · one web/LaTeX/Word/slide/render delivery target
Supporting native rNN/riNN/rlNN/global identity · Task/Discovery grouping
```

This is a projection, not a second Run registry. `RP`, `RE`, and `RD` counters
are independent, and all are distinct from native `rNN`/`riNN`/`rlNN`
counters. Execution, Discovery, Insight (`riNN`), Design, and other native
families retain their identities under Supporting Runs; Page never renames
them. Supporting members are grouped by parent Task for readability, but the
external Results remain references and are never copied. `rp-struct-01`,
`rp-sec-01`, `re-value-01`, `rd01`, and `r01` may coexist; no sequence
renumbers or consumes another. RP uses explicit kind tokens:

```text
rp-struct-NN          Page Structure Run: SHAPE + SURVEY
rp-scratch-NN_<target> Human Scratch capture at C1 or C1.P1 (Section/paragraph group)
rp-sec-NN             Section-level writing
rp-para-NN_Pxx[-Pyy]  Paragraph-level writing
```

`rp-struct-01` is the initial Structure Run and contains both the SHAPE and
SURVEY cycles. It is one shared Ticket/Result even when several people
participate: record `participants` on the Run and `contributors` on each Step.
`rp-struct-02` is a later independent structure/Bullet refinement, not a new
participant or Survey pass. These Runs settle Page direction, coverage and
non-coverage, high-level section flow, ordered Bullets, Point roles, paragraph
jobs, typed evidence decisions, and the Mermaid map. After structure closes, Section Runs use
`rp-sec-NN`; paragraph Runs use `rp-para-NN_Pxx[-Pyy]` and expose their exact
Page-global paragraph target. `RE` uses the focal-result kinds `value`,
`display`, and `cite`; `DISPLAY` covers table, figure, and algorithm block
through `display_kind`. One RE Result/Card may expose many `$V_xxx$`,
`\figure{D_xxx}`, `\table{D_xxx}`, `\algorithm{D_xxx}`, and `\cite{C_xxx}` labels; a
label is not another Run. The Result root `labels:` manifest is the shared
binding source; Draft Space and Evidence Card renderers must preserve the
authored token in expandable provenance even when a resolved value is shown.
While a structure Run is open, its review artifact is
`outline/<stem>-logic.mmd`; the shared Draft Space renders it as a collapsed,
user-openable disclosure above the plan. A missing map is a visible blocker,
never an empty surface.

The canonical Page Run namespace has no new aliases. The kind token must match
the scope, and a paragraph target must be exact; a mismatched identity is held
as a contract error and cannot unlock later work. Retired compact identities in
existing records remain readable history but are not allocated for new Runs. A
phase-controller invocation is a **Page workflow pass**,
not a Page Run object. Owner-native phase receipts remain machine workflow
records: Page-heavy standalone Folders commonly use `workflow/receipts/`, while
the current Board controller's compatibility bundle uses
`<board>/_runs/page/<page-id>/`. An unallocated `new-*` route is still only an
Evidence plan.

## 🧑 fn/Runs proposes human interaction

`fn/runs.md` is the read-only proposal function for Page-owned interaction.
It identifies bounded places where the human must shape, compare, revise, or
accept the Page, and proposes those as Page Run candidates. A proposal is not
an allocated Run and receives no typed RP identity, Ticket, Result, or
Runs-inventory row
until the person selects it. An existing matching open Page Run is resumed
instead of duplicated.

Code, search, Discovery, data, rendering, build, and other output-producing
work remains a normal Task Run, even when a later human gate reviews that
output. The Page may point to the needed Task work but never mints or rewrites
its owner-native identity. Use `/haipipe-page runs <page> [focus]` to propose;
a direct bounded editing request counts as selecting the matching interaction.

The first structure Run is always `rp-struct-01`, even when imported content
already suggests a Shape. It iterates until the person explicitly
closes the Mermaid Structure, Outline Bullets, and Page-global paragraph index
`P01..PN`. Later structure/Bullet revisions may use `rp-struct-02`, etc. Only
after the structure contract is closed may `fn/Runs` propose Section-level
Runs in `rp-sec-NN` or paragraph groups in `rp-para-NN_Pxx[-Pyy]`. Every
paragraph Run name
must expose its exact paragraph number or contiguous range; semantic titles
stay in Goal instead of lengthening the identity.

### Three update boundaries

Interactive Page work has three different commit boundaries. Do not collapse
them into one expensive operation:

```text
Writing Step      complete one scoped draft/review/diagnose/revise cycle
                  → save candidate, rating/diagnosis, and dependent Bullets
Page Run close    settle its fixed structure, Section, or paragraph scope
                  plus its Evidence contract
Page release      after every Page Run and required evidence Task Result is ready,
                  adopt Content once and generate web/LaTeX/Word once
```

A routine Step never writes adopted Page Content, rebuilds delivery, runs the
whole test suite, or waits for browser/export verification. Its durable minimum
is the verbatim feedback, complete saved candidate, review/rating and diagnosis
when the scope requires them, affected Bullets, narrow source/protected-scope
check, and current Version/Step projection. Update an Evidence requirement
during a Step only when the cycle changes what the paragraph must cite, measure,
or show.
Between Steps or Runs, use
`page-workflows/haipipe-page-workflow/ref/interactive-execution-policy.md`:
heavy builds, exports, broad checks, delegated Task Runs, and sub-agent
analysis require an explicit scoped approval before dispatch.

A paragraph Page Run closes only after its text and Bullets are accepted and
its Evidence contract is explicit: each Bullet names `none` or a ready bound
CITE, VALUE, or DISPLAY Result. Discovery, figure production, citation lookup,
and other independently executable support remain Task Runs. Do not mark the
Page Run complete while required evidence is unresolved.

Closing one paragraph Run does not adopt it into `<page>.md` and does not
refresh `delivery/`. CONTENT waits behind the Page release barrier: all planned
Page Runs are complete and every required Task Result is ready and bound. Then
one Page-level CONTENT pass applies the accepted candidates, integrates the
evidence, builds the declared web/LaTeX/Word outputs, and routes one exact
version to CHECK. While the barrier is open, the Draft Space is current
and delivery is explicitly stale by design. For an interactive Page, the
person's explicit next-step instruction is the authority for this pass; the
Outline's `approved:` marker is optional supporting metadata and must not create
a second approval loop.

## ✅ Page configuration and completion checklist

For CREATE, a Page configuration/completion audit, or a whole-Page completion
claim, read `ref/page-checklist.md`. Assess the reader-facing Opening and
Content explicitly, then assess any backstage Outline, target, contract, and
Evidence records separately. Report configuration, content, review and hosting
separately: a created Folder, successful build, or default wrapper is not a
completed Page. Apply only checks relevant to the requested operation; a narrow
edit is not a whole-Page audit.

## File → Page Folder → work

For file intake, standalone building, or source editing, read
`ref/standalone.md` and use `cli/page.py`. For a hosting request, read
`fn/serve.md` first; it decides whether this Page server or the Board server
owns the URL. Choose the intake depth explicitly:

- `init` is a technical import only. It preserves the file and produces a
  visibly incomplete scaffold. Never stop here when the user asked for a Page
  they can immediately inspect or work on.
- `setup` is the normal Markdown file-to-working-Page route. It preserves the
  imported source, reads its H1/H2/prose structure, creates a Page-specific
  Opening and backstage requirement/target records, and writes an unapproved semantic Shape plus reader-move
  embedded `Draft:` fields in the Outline Markdown, Context/Files records, and
  a completed setup Task Run. A
  non-Section Bullet may map to several sentences; punctuation does not decide
  outline grain. Paragraph identity is one Page-global `P1..PN` sequence and
  does not reset at a new `C`. Inspect the generated roles and heads, then read the Bullet
  column alone. Correct any move whose place in the argument is unclear before
  handoff; generated does not mean human-approved.

This is not a request to obtain human Shape/Content acceptance. Do not require
a Board, group, Paper, evidence Run, PDF, or scholarly prose rewrite just to
import or host a file. Preserve the input verbatim in an editable copy and
report any unsupported dependencies.

```bash
python3 <toolkit>/skills/page/haipipe-page/cli/page.py init --file <input> --dest <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py setup <input.md> [--dest <page-folder>]
python3 <toolkit>/skills/page/haipipe-page/cli/page.py setup <existing-page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py migrate-addresses <existing-page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py migrate-drafts <existing-page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py inspect <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py build <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py serve <page-folder>
```

Markdown `setup` already performs `build`; do not run a redundant second build.
Use `migrate-addresses` explicitly for a pre-0.81 Shape whose paragraph number
resets inside each division; it preserves prose and rewrites active Page-owned
references before `setup` revalidates and rebuilds the Page.
After it returns, inspect the generated Page Face, Shape/Draft coverage, setup
Result checklist (`checks.json` and `report.md`), and `delivery/web/index.html`.
Setup fails when a blocking mechanical check is missing; semantic judgment and
human acceptance stay visibly deferred/untested. If role or Draft inspection
changes a checked artifact, rerun `setup <existing-page-folder>` so a new Task
Run fingerprints and validates the current records; `build` alone does not
refresh the audit. Start `serve` only when the user
explicitly asks for a hosted/live URL; a request for a built website is
satisfied by the static delivery and does not authorize an indefinite foreground
server. When hosting is requested, use the workspace's supported background
process manager, verify the configured public URL, and return instead of
blocking on the listener. One skill invocation performs all requested mechanical
substeps; do not make the user request them separately.

The built `delivery/web/` is a portable static reading site. The server always
renders Page source read-only and adds the same category-plugin pane used by
Board Pages. Standalone advertises only real top-level presenters: Outline,
Delivery, Folder, plus an optional domain-owned Labeling presenter when a
direct `labeling/` lane and the subjective-label plugin are present. The
standalone Labeling surface uses the current Codex task as its Chat transport;
Studio remains Board-hosted until its chat/draw backend is extracted. Evidence
and Run stay internal Outline workspaces, never duplicate top-level Plugins.
Choose the configured
reader-facing origin for links; exposing plugin writes beyond loopback requires
a token. The standalone Page Face has no Chat launcher, comment composer, or
Page-source save control. Edit Markdown and imported material on disk. Bounded
plugin read views remain available in either server mode. `--read-only`
disables plugin writes; without it, Scratch notes autosave and Finish is a
separate manual action. Do not publish private inputs without the user's
authority. Static files do not provide save-back.
Report build, server reachability, and plugin interaction mode separately; do
not claim hosting from a successful build alone.

Board registration is optional and separate: register the same Page Face,
then let Board supply navigation. Moving/removing Board membership must not
move or replace the Page's source. Board Page group descriptions remain
Board-owned and are outside this file-intake operation.

Scratch is available as a small human-thinking capture once the selected
Outline exists. Notes autosave to `rp-scratch-NN_<target>`; the person manually
clicks Finish Scratch, which asks the AI to generate a concise Summary from
the raw notes and closes the Run only after a non-empty Summary is returned.
Scratch writes only the selected Outline's `## Scratch` registry plus its
paired `runs/` and `results/` receipt; it never edits `Draft:` prose. In
Scratch Mode, saved raw Scratch remains visible by default even when the
underlying body is hidden; `+` reopens its editor. The Board-hosted Page Chat
and terminal read the current Scratch registry at connect time, and a saved
Scratch refreshes a held Page Chat's context. When the person asks to use
Scratch, treat the notes as user-authored planning context and route any
resulting wording through the normal Page workflow.

The reader-facing completion packet is defined in
`ref/user-check-packet.md`. The Draft Space includes a read-only Draft
projection beside each Bullet during SHAPE. The selected
`outline/<stem>-outline-v<G>.<S>[.<E>].md` is the sole Draft authority: each
Bullet stores its planning fields and `Draft:` candidate in that same file.
The candidate may exist before Shape approval and becomes exact adoption input
for CONTENT when explicitly accepted. The Page/Run Workflow is the writer of
the plan, the Page, and every Result; the reader-facing Table and Reading
views write none of them through the browser. Human feedback and acceptance
enter through the owning Page Writing Run's interaction and its recorded
Steps/Versions; Scratch is the explicitly bounded exception for rough human
notes. Draft Space has no legacy note thread or feedback composer. Delivery Workspace
is the read-only source-to-artifact consistency projection; it does not replace
the human Page CHECK gate.
See `haipipe-plugin-outline/ref/content-preview.md` for the write boundary.

Use `ref/user-check-packet.md` for the two response modes: a routine Writing
Step returns its exact Run/Version/Step heading, complete selected paragraphs,
a frozen Mermaid Structure description beside each paragraph address, a numbered
blockquote review passage, a brief change explanation, and the three
final Draft Space, Evidence Space, and Run Space links;
a formal delivery also returns the Delivery Workspace consistency receipt and
the evidence/PDF surfaces that are current.
The Current Run derives granular Track Changes from clean Step-level Before and
After text and shows each material wording change's local type, rationale, and
analysis status. Legacy records may retain historical preference fields, but
interactive Page Steps defer new preference inference to post-run analysis.
Diff markup never becomes Page prose, and analysis never becomes shared policy
without confirmation.
Classification lives in the change-card heading, not a second table. Status,
navigation, acceptance-only, and presenter-only Steps create no Track Changes;
the Runs surface expands only the current Step and keeps older Steps collapsed.

## 📁 What a page is on disk

For a canonical Task Page, **Task Folder = Page Folder =
`tNN_<task>/`**. The same-stem Markdown, `outline/`, `workflow/`, `scripts/`,
and `runs/` belong to that one Folder. Do not create a Page Folder beneath the
Task Folder; the parent `jNN_<job>/` remains only the Job container.

A page is one markdown file (the PRODUCT: what the page asserts) beside one
process folder (how it came to assert it) and the plugin lanes it actually
uses. The roster of legal folder names is `haipipe-plugin/ref/roster.md`.

```text
<page>/
├── page.toml     optional standalone registration: source + imported content
├── <page>.md      Opening · Content                         THIS reader contract
├── outline/       HUMAN process: plan and durable process records
│   ├── <stem>-context.md  generated context projection for all Page Run Specs
│   ├── <stem>-logic.mmd    derived Mermaid Structure reviewed by rp-struct-NN
│   ├── <stem>-evidence-items.md  authored Evidence Item contracts
│   └── _archive/legacy-outline-evidence/  retired folder material only
├── workflow/      MACHINE process: Workflow Runtime/compatibility receipts
│              ─── the LOWER, TASK-side part ───
├── scripts/       optional owned implementation, any language; shared Task
│   └── config/    Job code stays one level up in `src/`
├── runs/          authored RP, RE, and RD tickets; THE ONE execution door
├── results/       canonical Page Evidence Results and Folder-local Results.
│                  A canonical Task Page resolves
│                  generated output at `$OUTPUT_ROOT/results/<task>/<run>/`
│              ─── the UPPER, PAGE part ───
├── delivery/      what leaves the page: web/ · latex/ · word/ · slide/ · render/
└── studio/        the HUMAN's room on the page (JL 260831): closest to
    ├── chat/      the person · you talk here, sessions kept
    └── draw/      you draw here, one scene per owner; the chat may
                   redraw the scene's named elements on your ask
```

**The Folder symmetry**: every Folder has a Page Face and Task Face; a
`primary_face` says which is the usual entry, not which face exists.
`outline/` is the human planning/decision record and `workflow/` is the
machine-readable Workflow/Run record. Page-heavy work commonly stores
compatibility receipts under `workflow/receipts/`; executable work commonly stores
`plan.yaml` and `report.yaml`. Run Space is an Outline projection over this
shared Task Face. It presents Page Writing, Page Evidence, and Supporting Runs.
A native Run pairs its ticket with either a Folder-local Result or the Task
dialect's resolved `$OUTPUT_ROOT/results/<task>/<run>/`, but the Page surface
shows the Result first when its card opens; scripts, config, and notebooks
stay in Folder/detail inspection. Run is never a top-level Page Plugin or a
lifecycle owner.

New Page Evidence is an `RE` Page ticket plus a bound Result. A Folder-local
Result is stored as `results/<re-run>/result.yaml`; a Task-backed Result stays
at the owner dialect's resolved output path, and the RE records that path and
hash. One Evidence Item has one current RE lineage and one current Result/Card
projection; that Result may expose many stable labels such as
`$V_xxx$`, `\figure{D_xxx}`, `\table{D_xxx}`, `\algorithm{D_xxx}`, and
`\cite{C_xxx}`. The hidden
binding retains the Evidence Item, RE, Result path, and provenance. A label
that needs an independent acceptance or execution lineage becomes another
Evidence Item/RE. `outline/*-evidence.md` and `outline/evidence/*` are retired
locations, not runtime inputs. Move them to
`_archive/legacy-outline-evidence/` before the Page is treated as v4-ready.
The authored `outline/*-evidence-items.md` file remains the Outline Item
contract.
New cross-Folder evidence enters through Supporting Run references in the `RE`
Result; the external Ticket and Result stay at their owner and are never copied.

A unit MAY carry a `README.md`, and it is DERIVED (JL 260831): a generated
projection of the two-part tree as it actually stands (which lanes exist,
their counts, where the product and the rendered page live), regenerated
whole and never hand-edited — the structure's law lives HERE and in the
roster, so a hand-written copy per folder would be a second authority that
drifts. GitHub renders it where the board cannot reach; the 📂 tab computes
the same walk live (`live/folderstat.py`, whose `--write` becomes the
generator).

A folder is created only when it is used. Values are typed Evidence Items;
their ready local Result and provenance are shown inside the Outline
Evidence Space. Every number shown on a Page Face that comes from a Run crosses
ONE page-serving collection job (`task-type: page`, contract
`haipipe-task-for-page`); the Supporting Run Result becomes the explicit
cross-Folder evidence edge. A display-input Run therefore feeds the
page-serving collection Job; it does not bypass that one numeric door to feed
a Page DISPLAY unit directly. A local Run
may validate or reshape non-authoritative intermediates, but it
cannot become a second value door. A reusable derivation, a source-data change, or any displayed
numeric result belongs in the linked executable Folder and its Run Result
binding. The
the `outline/` process files, their ids, labels and writers are
`haipipe-plugin-outline/ref/record-shape.md`; the plan's grammar is
`ref/plan-grammar.md` beside it. A Run Spec owner loads the exact
Outline-plugin refs it needs as schema/material contracts. The Page surface installs
`haipipe-plugin-outline` once as the presenter; the presenter skill is not
appended to each phase's execution dependency chain.

## 🧬 One owner claims the Page Face

A property every Page carries cannot tell one Folder kind from another. A Page
shows something, cites something, states a number; so display, literature and
value are plugins. A Run Workflow/Run Spec owner or declared family skill owns
the Folder kind and its Page Face. A fixed Page Type may own a Page directly. No
`folder-kind:` or `page-type:` key is the flexible base.

Resolve ① to ⑥ in order and stop at the first key that matches. Exactly one
semantic owner may claim the Page Face. An in-place Folder's
`workflow/folder.yaml current.folder-kind` is authoritative; fixed-kind Folders
use Page `folder-kind:`. `page-type:` is the declared Page Type when no current
Folder kind exists. If current
state and Markdown disagree, fix the Folder, never the resolver.

```text
step  machine-readable key                    Page Face owner    contract
──────────────────────────────────────────────────────────────────────────
①     workflow/folder.yaml current kind        Run Workflow       Run Spec owner
②     frontmatter `folder-kind: <key>`        Run Spec/family     Run Spec/family skill
③     frontmatter `page-type: <key>`          Page Type           Page Type owner
④     filename QBv<n>-                        venue              for-venue
⑤     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑥     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

A Discovery Folder resolves `folder-kind: discovery` to its Discovery workflow
Run Spec owner. Its Task Face does not select the Task Folder technical-report
grammar: the Discovery Run Spec owner owns that Page Face, while `haipipe-task` owns only
`folder-kind: task`.

### Page Types are self-owned

Each current Page Type declares its own shape and owner in its Page-Face or
workflow skill. `check.py` validates the `page-type:` value against the
engine's current set and the resolver loads the owning contract directly.
There is no central inventory, compatibility layer, alias table, or Page Type
without an owning contract. A retired key must be migrated or removed from the
Page; it is not kept alive by a second document.

### Paper Pages

For a Paper Page, follow the [Paper routing contract](../../paper/haipipe-paper/SKILL.md#-routing)
and load the exact self-owned Ideation, Story, Section, Round or Venue skill.
For `page-type: ideation`, that is `haipipe-paper-ideation`; it delegates idea
semantics to `haipipe-ideation` and keeps Page projection/release here. General
Page work does not load Ideation or every Paper skill. Read the
[Paper–Page adapter](../../paper/haipipe-paper/ref/page-integration.md) when a
Paper Run or release is planned. At a Paper G4 Section CHECK, the Page CHECK
owner also applies the section-scoped `SUB-*` rows from the Paper
submission-readiness reference; cover-letter and whole-manuscript rows stay at
Paper level. The same owner is loaded only once.

### A variant extends the base and never redefines it

A Page Face specialization defines Content and fixed extension points without
reordering the base frame. In a migrated family it lives with the Run owner
or canonical family skill that owns the Folder kind; an unmigrated Page Type
remains a base variant under `page-types/`. Load the semantic owner before
writing. After moving a skill, re-run `install.sh --global` so the installed
symlink follows it.
For `folder-kind: task`, the canonical Folder owner remains `haipipe-task`;
the reader-facing companion `haipipe-page-task` adds the Task Page's
display-rich table, figure, and diagram contract. The companion refines the
Task Page surface and never creates a second Page frame or execution owner.

## 🎭 Page Run Workflow, independent of Folder kind

A Page Face persists while its Page Run Workflow authority changes. The page
workflow (`page-workflows/haipipe-page-workflow`) has a directed Run Spec graph;
the five labels below are only the compatibility dispatch projection, independent
of the domain workflow that owns the Folder kind:

```text
index     phase/cycle     skill                                  gate
──────────────────────────────────────────────────────────────────────────────────
00        CONTEXT/PREPARE  page-workflows/haipipe-page-context     ⚙ resolved context
01        OUTLINE/SHAPE    page-workflows/haipipe-page-outline     👤 approved:
          OUTLINE/SURVEY   page-workflows/haipipe-page-outline     👤 Decide per item
02        EVIDENCE/LAND    page-workflows/haipipe-page-evidence    ⚙ local work exhausted; external gates named
          EVIDENCE/EMBED   page-workflows/haipipe-page-evidence    ⚙ v0 → SHAPE · G>=1 → CONTENT
03        CONTENT/WRITE    page-workflows/haipipe-page-content     ⚙ cold pre-check ready
04        CHECK/CHECK      page-workflows/haipipe-page-check       👤 accepted:
```

The evidence loop law: SHAPE specifies typed Evidence Items; SURVEY
plans zero-to-many Execution/Discovery Supporting Runs plus exactly one Page
`RE` lineage per item; LAND produces one ready local Result/Card; EMBED
interprets it. The ledger is `outline/<stem>-evidence-items.md`
(`haipipe-plugin-outline/ref/item-table.md`).

Collaborative writing uses persistent `RP` Runs across one Page under
`../page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md`.
`rp-struct-NN` is the Page Structure Run: its SHAPE and SURVEY cycles settle
Mermaid Structure, Outline Bullets, Point roles, paragraph jobs, and typed
evidence decisions; it does not write full prose or execute evidence work.
Several people may contribute Steps to the same `rp-struct-01`; record
`participants` and per-Step `contributors` rather than creating one Run per
person. `rp-sec-NN` covers one named Section drafting/revision session.
`rp-para-NN_Pxx[-Pyy]` covers one fixed paragraph or contiguous paragraph
group. A complete Section draft → review/rating → diagnose → revise cycle is
one Step inside its Section Run, not a new Run. If the person later
commissions another independent Section drafting/revision session, allocate a
new `rp-sec-NN`. For the same paragraph target, reopen the existing Run in a
new Version unless the target or goal materially changes. Closing one Run
does not modify Page Content or delivery. After all planned RP Runs and
required evidence Results are complete, one Page-level CONTENT pass adopts the
agreed wording. It then commissions one or more `RD` Delivery Runs for the
declared targets without commissioning an additional delegated Task Run for
every accepted paragraph. `RD` is a delivery identity, not a second CONTENT or
CHECK phase.
The historical/explicitly delegated single-paragraph profile remains in
`haipipe-page-content/ref/paragraph-run.md`. Neither path adds a plugin.

### 🧬 Writing DNA handoff

The Page has one style authority: the resolved Context and its authored
requirements. When the external `writing-dna-skill` supplies a profile, the
Page carries a frozen, style-only packet into CONTENT; it does not copy the
corpus into the Page, create a second Outline, or treat DNA as Evidence.

```text
CONTEXT/PREPARE  resolve policy + profile id/status/hash
OUTLINE/SHAPE    freeze the reader job, Bullet order, claim contract, and any
                 declared paragraph-level Narrative Decision
EVIDENCE         land and fold factual Results; DNA has no evidence authority
WRITING RUN      freeze applicable Decision + style packet; reload only on drift
CONTENT/WRITE    adopt agreed wording; preserve its recorded style decisions
CHECK            judge the built Page and the Run's recorded style application
```

If a named style is required but its profile or required exemplars cannot be
resolved, CONTEXT/HOLD owns the block. If the style is optional, CONTENT may
write under the Page owner's policy without DNA. A profile can change wording,
rhythm, and compatible structure only after the content contract is stable;
claim strength, evidence order, topic, and reader promise remain Page-owned.
A declared `Narrative Decision` is the approved reason for a paragraph's
organization; it is consumed by CONTENT, is not an Evidence Item, and is never
minted or rewritten by Writing DNA. If it conflicts with the approved Outline,
route back to OUTLINE.
The HAI-side adapter and three-pass realization rules are
[`haipipe-writing/ref/writing-dna-adapter.md`](../../writing/haipipe-writing/ref/writing-dna-adapter.md).

Resolve one invocation as: Folder → base Page Face → Run Workflow/Run Spec-owned
Folder kind or declared Page Type → current Run Spec → Run Spec-selected and
page-local plugins.
The cycles form a routing grammar, not a conveyor belt: each may repeat,
SURVEY and LAND are skipped when the page promises nothing it cannot already
support, and CHECK may route to any earlier cycle. When the visible operation
is ambiguous, the authority test decides:

```text
governing policy/context is stale              → PREPARE
the section list itself is being agreed        → SHAPE
an item has no valid Run graph or Decide        → SURVEY
a decided item has no ready local Result        → LAND
a ready item is not yet in the plan             → EMBED
approved purpose, Aim promise, or structure changes → OUTLINE / SHAPE
prose realization changes under the same promise → CONTENT / WRITE
a concrete version is judged                   → CHECK
```

`RUN` is the router verb, deliberately not `ADVANCE`; it is owned by
`page-workflows/haipipe-page-workflow`, whose `ref/page-run-contract.md` holds
the packet, receipt, version, role-separation and stop rules, and whose
`ref/phase-cards.md` states every phase in the same six fields. A pass may run
inside a person's session (the page chat, which resolves Run owners and controller operations and reads the
strip: `haipipe-plugin-studio/ref/chat.md` §🔁) or as that phase's agent; both leave the same
trace (the artifact, one log record, the receipt).

## 📑 Two sections on stage, and nothing else

The reader-facing Page order is `Opening → Content`. Outline, Aims, Stage
Contract, Files, Discussion, Log, and other process records live in the Page
Folder and are shown only by their owning Draft, Evidence, Run, Delivery, or
Folder surfaces. `check.py` may still inspect those records, but their presence
must not add another main Page section.

```text
#   section    conveys · the reader question                 phase authority              omit
────────────────────────────────────────────────────────────────────────────────────────────────
1   🚪 Opening what is this page, why should I care?         CONTENT defines and clarifies      never
2   Content    what does this page actually establish?       CONTENT writes and builds          Q may · S never
```

Each section answers one reader question, and a sentence answering another
section's question is misplaced: substance in Opening moves to Content.
Inherited inputs and venue move to backstage contract records, page-owned prose
rules to authored W records in `outline/<stem>-requirement.md`, intended
outcomes to backstage target records, current facts to their Run/CHECK
receipts, and a question for a person to a `D<nn>` record.
There is no `## Boundary` section: what a page covers is the Opening's job,
stated as a `**Covered elsewhere**:` part in its drawer.

There is no reader-facing `## Outline` projection. The current plan's `▤ Outline
table` remains available in Draft Space with `Address · Bullet · Feedback ·
Evidence · Supporting Run · Local Run`; C/P rows are planning group headers and
B rows are the checkable claim/evidence rows. The compact reading projection
shows the Point statement, not the plan's process-only `Note:` annotations.
The `outline/` folder remains the authority for every plan, writing rule,
evidence, feedback, requirement, discussion, file, and log record.

The live Outline/Draft Space makes each paragraph address (`C<n>.P<m>`;
`P` increases once across the whole Page and never resets at a new `C`)
an expand/collapse control and keeps its Bullets inside that group. It is a
read-only projection: each Bullet keeps its bracketed role label and any
compact Evidence route, while Bullet heads, candidate wording, comments, and
new Bullets are not editable from the rendered page. Page/Run workflow writers
update the selected Outline Markdown; the next GET re-reads that one file.
Markdown remains authoritative: a workflow write against an approved
Shape creates the next unapproved working Shape and preserves the approved
file; subsequent writes reuse that working version. Generated Page HTML is
never an edit target.

The visible reader labels are `🚪 Opening` and `📚 Content`; they must not reuse
one icon because they answer different reader questions. Draft/Outline is a
separate owning Space, not a third reader section. Opening is reader prose, not
an internal ledger: a bare claim, Evidence, or Run address is forbidden there.
Name the subject in plain English first and keep any address only as a
secondary compact handle, such as `primary total-MME association
(Claim1.TotalMME)`.

A manuscript `page-type: section` tightens the reader surface: `🚪 Opening`
renders exactly one paragraph and has no reader drawer. Its page-owned prose
rules live as authored `W<n>` records in `outline/<stem>-requirement.md`, after
its generated venue `V<n>` records. The Outline plugin exposes both through
one `📏 Requirement` lens to CONTEXT, OUTLINE, CONTENT, and CHECK. The Section
product source carries no `### Writing Style`; post-paragraph notes and Stage
Contract remain source-side and do not appear on the manuscript review
surface. Other Page Types retain the ordinary Opening drawer when they need it.

## 🎯 Backstage target records: one Aim is one row

The Page Face does not render targets as a third reader section. When a
workflow uses Aim records, the legacy `## Aims` syntax remains the record
shape: one Aim is one row with its tick, target, `Done when:` test, and `Now:`
fact. The plan carries 🎯 marks that name these backstage rows and no rows of
its own.

```markdown
## Aims
### A3 · 📚 Results
- ✅ A3.1 · The headline coefficient carries its four coordinates.
  **Done when:** a reader can quote SPEC, window, trait form and outcome.
  **Now:** met; §3.2 states all four beside the estimate.
```

- **The tick says its meaning by shape**: `✅` met · `🔨` being worked on ·
  `🧠` waiting on a ruling · `⬜` not met · `❄️` deliberately held. This is the
  Aim vocabulary, not the page `state:` line, which keeps ✅ 🟡 🔴 ⏸️.
- **A group `### A<n> · <emoji> <name>` maps to Content division n**, taking
  its number, name and emoji so the two sections line up by eye and by id
  (`check.py` `group-name-drift`, `group-no-division`); `### P · Page-level`
  holds a target that genuinely crosses divisions.
- **`Now:` is a snapshot**; the reason for a transition is a log record. A live
  ask for a person is that Aim's `Now:` marked `🧠`, pointing at its `D<nn>`.
- **A fact with no Aim id is a note**, not a status; an ask that owns no Aim
  becomes a `D<nn>` thread, never a minted Aim. An Aim is not a task: one
  division may own zero, one or many; changing an Aim's optional `Plan` does
  not change the Aim.
- **`### Decision Now` is reserved inside Aims** for a machine-proposed
  ruling: one `- [ ]` row with the ask, one option per line saying what
  choosing it commits you to, and a `→ CC recommends` line. A machine closes
  a row only after the person answered (in chat, in a lane, or by ticking)
  and records which option, who, when, and their words.

## 🚪 Preview · create · work on · run

```text
👁 PREVIEW    /haipipe-page preview <page>                 read verb, writes nothing
📄 CREATE     /haipipe-page create a new page on <topic>   [on <board>]
🔧 WORK ON    /haipipe-page working on <page>              or just the path
🧑 RUNS       /haipipe-page runs <page> [focus]            propose human interaction
🔁 RUN        /haipipe-page run <page> [from <operation>]
```

The RUN `from` selector accepts the existing Page controller operation names
(CONTEXT, OUTLINE, EVIDENCE, CONTENT, CHECK); its parser/API may retain the
field name `phase`. This help wording does not add a Run-id selector.

**Preview**: `cli/preview.py <page>` prints one screen (title, the Opening's
visible paragraph, the Aims with their `Now:` lines, the Content divisions,
the last log record); a group or board folder prints one roster line per
page. A gist, never a substitute for the whole-file read.

### 🔗 Open the rendered Page

For standalone technical intake/edit/build, use `ref/standalone.md` and its
handoff; a source/Folder link is appropriate and a Board URL is not required.
For a hosted standalone Page, verify its configured Page-server origin. The
following server instructions apply only when this Page is hosted by a Board.

A source `.md` path is not the Board reader-facing link. Build the Board, then open
the generated Page through the repository's configured Board server:

```bash
ROOT="$(git rev-parse --show-toplevel)"
set -a
source "$ROOT/.server_config/settings.env"
set +a
python3 "$ROOT/$JJLUO_SERVER_SCRIPT" --root "$ROOT" \
  --host "$JJLUO_BIND_HOST" --port "$JJLUO_LOCAL_PORT" \
  --space-name "$JJLUO_SPACE_NAME" --public-url "$JJLUO_PUBLIC_URL" \
  --no-auth
```

Open `<JJLUO_PUBLIC_URL>/b/<board-slug>/<page-id>` in a browser. The short
route redirects to the canonical generated file; `<page-id>` is the resolved
Page id (for example, `b01j03t04` for a Task Page). The Board index is
`<JJLUO_PUBLIC_URL>/b/<board-slug>`. If the server is already running, reuse
it; do not start a second listener. Use the configured public URL for a
reader-facing reply and never substitute `localhost`, `127.0.0.1`, or
`file://`. The short-route and server details are owned by
`haipipe-board/ref/operations.md`; this section is the Page entry point.

Before returning a reader-facing Page link, make a lightweight request to the
exact configured public URL and require a successful response. Every Board-hosted
delivery reply ends with that verified Board URL when the request
succeeds. If verification fails, the user-check packet ends with an explicit
Board-unavailable blocker and no clickable substitute. It may not end with a
source-file path, `localhost`, `127.0.0.1`, or `file://`.

### 👀 User check packet · the only primary return surfaces

For substantive writing or research delivery, return the compact packet in
`ref/user-check-packet.md`. For a routine interactive turn, return the full
selected paragraphs and concise feedback dispositions, followed by direct
Draft Space, Evidence Space, and Current Run links at the very end.
Only the live
Draft Space must be refreshed for a routine Step; the Evidence Space
changes only when that Step changes an evidence requirement. Do not update
adopted Content or build web, LaTeX, Word, or PDF at Page Run close. The
following surfaces are the formal Page-release packet, produced once after all
Page Runs and required evidence Task Results are complete:

1. the verified Board route in two direct views: **Draft Space**
   (`lens=div`) and **Outline table** (the compact Page projection);
2. **Evidence you can open now**: the direct Evidence Space link
   (`lens=evidence`) plus, per ready
   typed Evidence Item, the DISPLAY unit's `preview.pdf`, the Page's citation
   register, or the VALUE item card deep link;
3. **Content state**: the Page version and whether Revise ran (owner-selected workers and
   the fresh-context style verdict against the resolved owner's policy); a first draft is labelled as such;
4. the current one-Page compiled PDF, labelled **Latest Page-level PDF**, the
   delivery surface shown after Revise;
5. the read-only **Delivery Workspace** (`lens=delivery`), whose lane receipt
   confirms that the current Page source and saved delivery artifacts agree.

“Page-level” means this Page or Section Page only. It is not the paper master,
the desk-room build, a Display preview, or a configuration file. Keep raw
receipts, logs, TeX sources, manifests, and unrelated outputs out of the
primary completion block. If any requested surface is missing or stale, say so
explicitly and name the blocker instead of presenting an older file as current.
The user-check packet is new-layout-only: it accepts only Result payload
previews and bibliography artifacts at their resolved producer paths, the Evidence Space one-URL
route, and `delivery/latex/<stem>.pdf`; legacy locations do not qualify.

**Create from file**: follow `ref/standalone.md`; no Board/group is required.

**Create authored Page**: resolve a Board/group only when membership was
requested · pick the id and copy `ref/page-template.md`, never
retype the shape · a three-to-five-word title stating the purpose · the
Opening as one visible paragraph above the first blank line · Content as
numbered parts, each with a caption, a figure and a short intro · Aims with
their `Now:` lines · `outline/<stem>-files.md` with any Related Board Page row
the current phase needs · register in `board.md` only if requested · build, check, read the
RENDER, report the finding count.

**Interactive work on**: when the person asks what interaction is needed, use
`fn/runs.md` and do not allocate before selection. A direct bounded
sentence/paragraph feedback request is already a selection: resume a matching
open Page Run or allocate the next typed Page-local RP for an independent goal.
When the person enters or resumes an open Run before giving feedback, return
the pre-Step review packet with the complete selected paragraphs separated by
visible `### PNN · Cn.Pm` blocks, `S1...Sn` labels, proposed next Step number,
review scope, and the three direct links;
do not create a journal Step yet. After feedback arrives, resume current
decisions and affected sources; make the narrow patch, save feedback and
result, refresh the live Draft Space, and return the saved passage. Do
not write Page Content, refresh delivery, wait for export/browser verification,
or use the broad repair/build loop below for that request.

**General Page work on**: ONE page is the deliverable. Read the whole file and its
`outline/` first; if the files record declares Related Board Pages, load the
one-hop packet from `cli/pagecontext.py <page> --phase <PHASE>` · run the
checker and fix the mechanical findings in bulk · then read for what no
checker reaches (the weak-English axis, one question per part, an Opening that
says more than the title) · a rule nobody wrote down goes in three places (the
owning page, `ref/page-template.md`, this file) · build, check, read the
render, report before and after counts · a write outside the target page only
when the page cannot be made correct without it, named file by file · never
rewrite a sibling page's content.

**Run**: human-feedback writing uses the persistent profile above. For automated
phase work, the bounded loop lives with `page-workflows/haipipe-page-workflow`.
The dispatch stays in the session you typed it in: a subagent is not handed
the `Workflow` tool. A new page is CREATEd first (Board registration is optional) and RUN starts
at CONTEXT; an existing page with no known next authority starts at CHECK.

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/preview.py <page>
python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
python3 <toolkit>/skills/board/haipipe-board/cli/check.py --rules
```

`--rules` prints every finding code with its message; read the laws before
writing, not from the error text after. `watch.py` rebuilds on any `.md`
save; a `.py`, `.css` or `.js` change needs one build run.

## ✍️ What a write may touch

For substantive Page prose, load this skill and
`haipipe-board/ref/writing-rules.md` directly before writing; a copied checklist
in a prompt is a second authority and drifts. Technical file intake and code
edits use `ref/standalone.md` instead; do not apply scholarly title, sentence,
language or figure rules to imported HTML/code or its generated wrapper.

- **Formal delivery finishes on the rendered Page.** Build/check and inspect
  the required projection before calling it current. A routine Writing Step
  saves/reads only the live Draft Space candidate. A Page Run close seals
  its text, Bullets, and Evidence contract but leaves Content and delivery
  unchanged. Only the Page-level release after all required Runs are complete
  adopts Content and refreshes web/LaTeX/Word. Human approval and write scope
  remain binding.
- **An accepted process ruling lands in its owning skill when a skill update
  is requested.** Apply it only to Pages within the authorized scope; a skill
  update does not regenerate every Paper. Local writing preferences stay in
  the Writing history until promotion to a wider rule is explicitly approved.
  The Page receipt names the exact skill version used.
- **The write anchor rule**: a machine write lands at a section boundary,
  never at a byte offset; appending under a named `##` heading is safe.
- **The human-decision rule**: a machine updates an Aim's tick only from
  evidence it can inspect; a person's ruling is transcribed with the quote
  (`approved: ✅ JL 260831 0146 · in chat: "…"`), never decided.
- **The form rules, each owned once**: the title is a functional label, not a
  headline. Use three to five visible words in sentence case, never six
  (`writing-rules.md`; `title-too-long`), and name the Page's subject plus the
  work or deliverable it owns. Keep it objective and concrete: do not put a
  joke, marketing phrase, surprise, accusation, or unqualified finding in the
  title. Prefer `[subject]: [operation or deliverable]`, such as
  `NPI2Photo: screening physician photo URLs`; put results, caveats, and
  interpretation in Opening or Content, where scope and denominators can be
  stated. Before writing, ask whether a new reader can tell what the Page does
  from the title alone and whether the wording claims more than the evidence
  supports ·
  the first blank line in Opening is the split between the visible paragraph
  (≈450 characters, 520 ceiling, `OPENING_MAX_STAGE_CHARS`) and the drawer ·
  every figure carries a caption line above its fence · Content is numbered
  all the way down (`### 3 ·`, `**3.2 ·**`, `#### 3.2.1 ·`) · `More details`
  is a list of labelled parts, never one block · a figure row is a label and
  its value, never a clause · the `state:` line is one row under 110
  characters · a heading is a lookup key (`writing-rules.md` §A heading is a
  lookup key).
- **The Opening's first job is to define the words its own question uses**,
  one line each with a real example; speak about the subject, never from a
  reusable scaffold (`This page defines …`): if the paragraph still fits
  another page after its nouns are swapped, rewrite it.
- **Before writing back, self-check**: no promise the page does not support,
  no sentence that only fills a category, one sentence per source line,
  English only, no em-dash. This improves the draft and approves nothing; a
  fresh reviewer judges formal Page completion, not each local feedback Step.

## 🔍 How a page is judged

Evaluation asks whether the authored page satisfies its declared
requirements, never whether the reviewer likes the format, and the
requirements resolve in this order: this contract and `ref/page-template.md`
→ the Folder-owned Page Face or declared Page Type → the selected Run profile
and Page controller operation → the page's own
authored W records in `outline/<stem>-requirement.md` (and `## Stage Contract` on S) → the local division
purpose and each paragraph's job line. A more specific source refines a
broader one and never silently contradicts it; a conflict is reported and
that criterion is not judged until the owner resolves it. The rubric (four
axes, four verdicts, the review units, the batch-voice test, the report row)
is `page-workflows/haipipe-page-check` §📏; `check.py --strict` supplies the
mechanical half, the page's `✅ Quality Check` runs the rubric in the page
chat, and `haipipe-page-check-agent` runs it in a fresh context.

## 🔤 The words

Every term this family uses is defined in `ref/glossary.md` beside the path it
names: Context record, plan, Bullet, Evidence Item, Supporting Run, Local
Input, local Run, Result, availability, next action, phase, and receipt. Load
it when a reader asks what a word means or when you are about to coin one;
`writing-rules.md` forbids a phrase that is neither the source's own wording
nor defined where a reader can find it.

## 🏷 How a location is written

```text
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB8's grammar  haipipe-sentence owns everything below the section
bullet      C3.P7.B4       division 3, Page paragraph 7, Bullet 4; a sentence names it with realizes:
thread      D07            board-wide, cited from any page
```

Every id inside a fenced figure renders as a link.

## ✅ Closing checks

- For Page creation or whole-Page completion, apply `ref/page-checklist.md`
  and name unmet, deferred or untested checks; never promote a scaffold,
  a static build or an inferred human approval into completion.
- Every `folder-kind:` and `page-type:` value resolves directly to its owning
  Page or workflow contract; no central registry is consulted.
- Every heading passes `writing-rules.md`'s five lookup-key tests;
  `grep -n '^#\+ .*, '` returns only clauses that state a second rule.
- No section states a rule a cited authority owns (`board-form.md` §4,
  `page-template.md`, `writing-rules.md`, `haipipe-plugin-outline`), except
  where this file adds what a machine may write.
- Every path this file names resolves on disk; each `##` section answers one
  reader question.

## 📂 Files

```text
haipipe-page/
├── SKILL.md            this contract
├── fn/serve.md         host one Page Folder and route Board hosting
├── fn/runs.md          propose Page Runs needing human interaction
├── ref/page-checklist.md  configuration, four-section and delivery acceptance
├── ref/page-run-families.md  RP/RE/RD and Evidence Item/Result/Card/Label contract
├── ref/glossary.md     every word this family uses, with the path it names
├── src/evidence_labels.py  shared token grammar and Result-label resolver
├── ref/user-check-packet.md  the four-surface reader-facing completion packet
└── CHANGELOG.md        version history, and the only home for retired rules
```

Owns `ref/page-template.md`, `cli/page.py`, `src/` and the shared `live/`
Page presenters. Board `ref/board-form.md` §4 remains the shared frame
reference during extraction. Board `cli/preview.py` and
`cli/pagecontext.py` live with the machinery. The lifecycle packet and receipt
spec belong to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`.
