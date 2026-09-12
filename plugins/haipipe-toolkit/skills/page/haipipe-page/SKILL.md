---
name: haipipe-page
description: >-
  Create, edit, build and serve a self-contained Page Folder from a supplied
  Markdown, text, HTML or other file, without requiring a Board. Also owns
  the Page Face contract and router of a Folder: what the readable .md is on
  disk, how its phase-owned Folder kind or legacy Page Type is resolved, which
  Page Phase holds authority, and PREVIEW, CREATE, WORK ON, RUN. Trigger:
  file to page, HTML page, standalone page, host a page, open page code,
  create a page, update page, run page lifecycle, Page Face, Folder kind,
  legacy Page Type, Page Phase, /haipipe-page.
metadata:
  version: "0.67.0"
  last_updated: "2026-09-12"
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

## ✅ Page configuration and completion checklist

For CREATE, a Page configuration/completion audit, or a whole-Page completion
claim, read `ref/page-checklist.md`. Assess Opening, Outline, Content and Aims
explicitly, alongside the source configuration and requested delivery surface.
Report configuration, content, review and hosting separately: a created Folder,
successful build, or default wrapper is not a completed Page. Outline remains a
generated projection, not an extra authored section. Apply only checks relevant
to the requested operation; a narrow edit is not a whole-Page audit.

## File → Page Folder → work

For file intake, standalone building, serving, or source editing, read
`ref/standalone.md` and use `cli/page.py`. This is a technical workspace
operation, not a request to run the research/writing lifecycle or obtain human
Shape/Content acceptance. Do not require a Board, group, Paper, evidence Run,
PDF, or scholarly prose rewrite just to import or host a file. Preserve the
input verbatim in an editable copy and report any unsupported dependencies.

```bash
python3 <toolkit>/skills/page/haipipe-page/cli/page.py init --file <input> --dest <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py inspect <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py build <page-folder>
python3 <toolkit>/skills/page/haipipe-page/cli/page.py serve <page-folder>
```

The built `delivery/web/` is a portable static reading site. The server adds
the Source editor on writable hosts and the same category-plugin pane used by
Board Pages. Standalone currently advertises only real local presenters:
Outline, Runs, Delivery, and Folder; Studio remains Board-hosted until its
chat/draw backend is extracted. Evidence stays an internal Outline workspace,
never a duplicate top-level Plugin. Choose the configured
reader-facing origin for links; exposing writable editing beyond loopback
requires a token. Do not publish private inputs without the user's authority.
Static files do not provide save-back. Report build, server reachability, and
editing checks separately; do not claim hosting from a successful build alone.

Board registration is optional and separate: register the same Page Face,
then let Board supply navigation. Moving/removing Board membership must not
move or replace the Page's source. Board Page group descriptions remain
Board-owned and are outside this file-intake operation.

The reader-facing completion packet is defined in
`ref/user-check-packet.md`. The Bullet Workspace includes editable Content
preview beside each Bullet and its Evidence during SHAPE. These candidate
sentences live in `outline/<stem>-preview.md`, may exist before Shape approval,
and become exact adoption input for CONTENT when explicitly accepted. See
`haipipe-plugin-outline/ref/content-preview.md` for the write boundary.

Use `ref/user-check-packet.md` for the two response modes: a routine Writing
Step returns complete selected paragraphs and the two final Workspace links;
a formal delivery also returns the evidence/PDF surfaces that are current.

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
├── <page>.md      Opening · Outline · Content · Aims           THIS contract
├── outline/       HUMAN process: the plan (versioned, ticked), process records,
│                  and the nested Evidence Workspace (JL 260903)
│   ├── <stem>-context.md  generated PREPARE projection for all Page phases
│   └── evidence/  typed CITE/VALUE/DISPLAY material and Run lineage:
│       ├── bibex/       citation files and source metadata
│       ├── display/     units and recipes · accepted:
│       ├── supporting-runs/ generated lineage pointers only
│       └── materials/   dated captures and editable, byte-preserved file imports
├── workflow/      MACHINE process: one receipt per phase pass
│              ─── the LOWER, TASK-side part ───
├── scripts/       optional owned implementation, any language; shared Task
│   └── config/    Job code stays one level up in `src/`
├── runs/          optional authored Run tickets; THE ONE execution door
├── results/       Folder-local Results only. A canonical Task Page resolves
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
machine-readable phase/run record. Page-heavy work commonly stores phase
receipts under `workflow/receipts/`; executable work commonly stores
`plan.yaml` and `report.yaml`. Runs is an optional presenter beneath this shared
Task Face. It pairs the local ticket with either a Folder-local Result or the
Task dialect's resolved `$OUTPUT_ROOT/results/<task>/<run>/`; scripts, config, and notebooks
appear only when the dialect owns them. Runs is never a third universal face or
a lifecycle owner.

All Page Evidence storage is nested under `outline/evidence/`; a root
`<page>/evidence/` directory is a legacy migration shape, not a new write
target. The Outline plugin owns the nested workspace and its CITE/VALUE/DISPLAY
contracts. An existing `outline/evidence/pagex/` lane is also read-only
migration input; new cross-Folder evidence enters through Supporting Run Results.

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
Evidence Workspace. Every number shown on a Page Face that comes from a Run crosses
ONE page-serving collection job (`task-type: page`, contract
`haipipe-task-for-page`); the Supporting Run Result becomes the explicit
cross-Folder evidence edge. A display-input Run therefore feeds the
page-serving collection Job; it does not bypass that one numeric door to feed
a Page DISPLAY unit directly. A local Run
may validate or reshape non-authoritative intermediates, but it
cannot become a second value door. A reusable derivation, a source-data change, or any displayed
numeric result belongs in the linked executable Folder and its Run Result
binding. The
nine `outline/` process files and its nested evidence workspace, their ids, labels and writers are
`haipipe-plugin-outline/ref/record-shape.md`; the plan's grammar is
`ref/plan-grammar.md` beside it. A phase loads the exact Outline-plugin refs it
needs as schema/material contracts. The Page surface installs
`haipipe-plugin-outline` once as the presenter; the presenter skill is not
appended to each phase's execution dependency chain.

## 🧬 One owner claims the Page Face

A property every Page carries cannot tell one Folder kind from another. A Page
shows something, cites something, states a number; so display, literature and
value are plugins. A workflow phase or declared family skill owns the Folder
kind and its Page Face. A fixed Page Type may own a Page directly. No
`folder-kind:` or `page-type:` key is the flexible base.

Resolve ① to ⑥ in order and stop at the first key that matches. Exactly one
semantic owner may claim the Page Face. An in-place Folder's
`workflow/phase.yaml current.folder-kind` is authoritative; fixed-kind Folders
use Page `folder-kind:`. `page-type:` is the declared Page Type when no current
Folder kind exists. If current
state and Markdown disagree, fix the Folder, never the resolver.

```text
step  machine-readable key                    Page Face owner    contract
──────────────────────────────────────────────────────────────────────────
①     workflow/phase.yaml current kind        workflow phase     phase skill
②     frontmatter `folder-kind: <key>`        phase or family    phase/family skill
③     frontmatter `page-type: <key>`          Page Type          phase/family/for-<key>
④     filename QBv<n>-                        venue              for-venue
⑤     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑥     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

A Discovery Folder resolves `folder-kind: discovery` to its Discovery workflow
phase. Its Task Face does not select the Task Folder technical-report grammar:
the Discovery phase owns that Page Face, while `haipipe-task` owns only
`folder-kind: task`.

### Page Types are self-owned

Each current Page Type declares its own shape and owner in its Page-Face or
workflow skill. `check.py` validates the `page-type:` value against the
engine's current set and the resolver loads the owning contract directly.
There is no central inventory, compatibility layer, alias table, or Page Type
without an owning contract. A retired key must be migrated or removed from the
Page; it is not kept alive by a second document.

### A variant extends the base and never redefines it

A Page Face specialization defines Content and fixed extension points without
reordering the base frame. In a migrated family it lives in the workflow phase
or canonical family skill that owns the Folder kind; an unmigrated Page Type
remains a base variant under `page-types/`. Load the semantic owner before
writing. After moving a skill, re-run `install.sh --global` so the installed
symlink follows it.
For `folder-kind: task`, the canonical Folder owner remains `haipipe-task`;
the reader-facing companion `haipipe-page-task` adds the Task Page's
display-rich table, figure, and diagram contract. The companion refines the
Task Page surface and never creates a second Page frame or execution owner.

## 🎭 Page phases, independent of Folder kind

A Page Face persists while its Page-workflow authority changes. The page
workflow (`page-workflows/haipipe-page-workflow`) has five numbered phases,
independent of the domain workflow phase that owns the Folder kind:

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
plans zero-to-many Execution/Discovery Supporting Runs plus exactly one local
Page Evidence Item Run; LAND produces one ready local Result; EMBED interprets
it. The ledger is `outline/<stem>-evidence-items.md`
(`haipipe-plugin-outline/ref/item-table.md`).

Collaborative writing uses one persistent Run for a bounded goal, possibly
several paragraphs, under
`../page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md`.
SHAPE and `haipipe-writing` co-develop Bullets and candidate prose. Human
feedback advances Steps; explicit closure seals a Version. CONTENT adopts
agreed wording and delivery without commissioning another Run per paragraph.
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

Resolve one invocation as: Folder → base Page Face → phase-owned Folder kind
or declared Page Type → current cycle →
phase-selected and page-local plugins.
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
inside a person's session (the page chat, which knows the phases and reads the
strip: `haipipe-plugin-studio/ref/chat.md` §🔁) or as that phase's agent; both leave the same
trace (the artifact, one log record, the receipt).

## 📑 Four sections on stage, and nothing else

The authority is `haipipe-board/ref/board-form.md` §4: the on-stage order is
`Opening → Outline → Content → Aims`, the optional folds (`Law` · `Lesson` ·
`Glossary`) follow, and everything else a page used to carry lives in
`outline/` (log, discussion, files) or was merged (States into Aims).
`check.py` reports a surviving `## States`, `## Files`, `## Log`,
`## Discussion` or an older name as `retired-section`.

```text
#   section    conveys · the reader question                 phase authority              omit
────────────────────────────────────────────────────────────────────────────────────────────────
1   🚪 Opening what is this page, why should I care?         CONTENT defines and clarifies      never
2   Outline    how is this page structured and supported?    generated authoritative projection       when no plan exists
3   Content    what does this page actually establish?       CONTENT writes and builds          Q may · S never
4   Aims       what should become true, for which Content    CONTENT sets target and test;      never
               division, and what is true now for each?      any phase updates Now:
```

Each section answers one reader question, and a sentence answering another
section's question is misplaced: substance in Opening moves to Content,
inherited inputs and venue move to the Stage Contract, page-owned prose rules
to authored W records in `outline/<stem>-requirement.md`, intended outcomes to an Aim's target, current
facts to that Aim's `Now:`, and a question for a person to a `D<nn>` record.
There is no `## Boundary` section: what a page covers is the Opening's job,
stated as a `**Covered elsewhere**:` part in its drawer.

`## Outline` is the only on-page projection of the planning process. It opens
by default immediately after the always-visible Opening. Normally it renders
the current plan's `▤ Outline table`: `Address · Bullet · Feedback ·
Evidence · Supporting Run · Local Run`; C/P rows are planning group headers and B rows
are the checkable claim/evidence rows. Evidence chip colour carries the quick
signal and its deep-linked Evidence Workspace card carries the detail, so no
separate Status column or Page popover is shown. A Page
Type may define one generated
executive projection from its own authoritative Content records. When it does,
that projection appears first and the generic plan table remains available in
a closed evidence drawer. The paper family's Story owns its Section Narrative
and any supported compact section-map projection; resolve its current semantic
contract through `haipipe-paper-story`. The base Page does not prescribe the
Story's research Content divisions. No projection is copied into a Page-authored
`## Outline`, and a Page-authored section map does not exist. Content, Aims,
References, and every other optional fold start shut. The `outline/` folder
remains the authority for every plan, writing rule, evidence, feedback,
requirement, discussion, file, and log record.

The live Outline/Bullet Workspace makes each paragraph address (`C<n>.P<m>`)
an expand/collapse control and keeps its Bullets inside that group. Bullet heads
may be edited and a new Bullet appended through the server-backed Outline
editor. Markdown remains authoritative: the first write against an approved
Shape creates the next unapproved working Shape and preserves the approved
file; subsequent writes reuse that working version. Generated Page HTML is
never an edit target.

The visible labels are `🚪 Opening` and `🧭 Outline`; they must not reuse one
icon because they answer different reader questions. Opening is reader prose,
not an internal ledger: a bare claim, Evidence, or Run address is forbidden
there. Name the subject in plain English first and keep any address only as a
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

## 🎯 One Aim is one row: target, test, and Now

`## Aims` is the Aims' only home. One Aim is one row: its tick, its target,
its `Done when:` test and its `Now:` fact. The plan carries 🎯 marks that name
these rows and no rows of its own.

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
🔁 RUN        /haipipe-page run <page> [from <phase>]
```

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

For substantive writing or research delivery, after any Page, plan, Page-local evidence, DISPLAY, Content, or derived
projection change, return the compact packet in
`ref/user-check-packet.md`. For a routine interactive turn, return the full
selected paragraphs and concise feedback dispositions, followed by direct
Bullet Workspace and Evidence Workspace links at the very end. Do not build
or append a PDF on every wording edit. The following surfaces are the formal
delivery packet, not mandatory work for each feedback Step:

1. the verified Board route in two direct views: **Bullet Workspace**
   (`lens=div`) and **Outline table** (the compact Page projection);
2. **Evidence you can open now**: the direct Evidence Workspace link
   (`lens=workspace&seg=items`) plus, per ready
   typed Evidence Item, the DISPLAY unit's `preview.pdf`, the Page's citation
   register, or the VALUE item card deep link;
3. **Content state**: the Page version and whether Revise ran (owner-selected workers and
   the fresh-context style verdict against the resolved owner's policy); a first draft is labelled as such;
4. the current one-Page compiled PDF, labelled **Latest Page-level PDF**, the
   delivery surface shown after Revise.

“Page-level” means this Page or Section Page only. It is not the paper master,
the desk-room build, a Display preview, or a configuration file. Keep raw
receipts, logs, TeX sources, manifests, and unrelated outputs out of the
primary completion block. If any requested surface is missing or stale, say so
explicitly and name the blocker instead of presenting an older file as current.
The user-check packet is new-layout-only: it accepts only
`outline/evidence/display/<unit>/preview.pdf`,
`outline/evidence/bibex/<stem>-bib.html`, the Evidence Workspace one-URL
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

**Interactive work on**: a sentence/paragraph feedback request selects the
persistent Writing Run path above. Resume current decisions and affected
sources; make the narrow patch, save feedback and result, and return the saved
passage. Do not use the broad repair/build loop below for that request.

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
  instead saves/reads the live preview; an explicitly requested adoption-only
  operation saves/checks Content and reports delivery as not refreshed. Neither
  is whole-Page completion. Human approval and write scope remain binding.
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
→ the phase-owned Page Face or declared Page Type → the current Page
Phase contract → the page's own
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
bullet      C3.P1.B4       the plan's address; a sentence names it with realizes:
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
├── ref/page-checklist.md  configuration, four-section and delivery acceptance
├── ref/glossary.md     every word this family uses, with the path it names
├── ref/user-check-packet.md  the four-surface reader-facing completion packet
└── CHANGELOG.md        version history, and the only home for retired rules
```

Owns `ref/page-template.md`, `cli/page.py`, `src/` and the shared `live/`
Page presenters. Board `ref/board-form.md` §4 remains the shared frame
reference during extraction. Board `cli/preview.py` and
`cli/pagecontext.py` live with the machinery. The lifecycle packet and receipt
spec belong to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`.
