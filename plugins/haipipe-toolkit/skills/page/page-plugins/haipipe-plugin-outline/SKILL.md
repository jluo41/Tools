---
name: haipipe-plugin-outline
description: >-
  The outline/ plugin of a Board page: the page's single planning authority,
  its process records, and one minimal 🧭 tab with Draft, Evidence, and
  Run workspaces; Draft keeps compact Evidence routes in its Bullet column;
  first and default on every page. Evidence is Result-first,
  Run is split into RP, RE, RD, and Supporting Runs, and Context records stay
  off-stage in the Folder. Trigger: outline
  plugin, outline tab, page outline, outline folder, plan file, record shape,
  evidence bundle, numbered discussion thread, /haipipe-plugin-outline.
metadata:
  version: "0.71.1"
  last_updated: "2026-09-14"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-outline · three minimal workspaces

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface,
writer, boundary. This file owns outline's delta: what the folder holds, what
the tab shows, and who writes each file. The visible surface has exactly three
workspaces:

```text
Draft Space          Mermaid Structure + paragraph/Bullet table + compact Evidence routes
Evidence Space       one Result-first Evidence table
Run Space            RP + RE + RD + Supporting Runs
```

Context, requirement, discussion, feedback, files, log, and Skill records
remain durable Markdown process records. They are not visible workspaces;
inspect them through 📂 Folder when needed. This is a presentation removal, not
a destructive data migration.

```text
  this file      the process records and ONE three-workspace tab
  ref/           plan-grammar.md · item-table.md · record-shape.md ·
                 skill-record.md · specimen-section-plan.md ·
                 evidence-bundle.md: the exact
                 grammars a writer or parser needs
  the phases     haipipe-page-context · haipipe-page-outline · haipipe-page-evidence
```

## 🗂 The folder · product beside process

`<page>.md` is the PRODUCT: what the page asserts. `<page>/outline/` is the
PROCESS: how it came to assert it. Since 260831 the folder is legal on any
UNIT, task folders included (the unit symmetry, `haipipe-page` §📁): same
kinds, same grammar; a task folder simply never owes the venue-only
requirement file. Process records remain one flat file each with the stem; only
the plan is many-per-page, by version. New Evidence does not create an
Outline-owned artifact lane: its commission lives in `runs/` and its truth
lives in the bound Page-local `results/<re-run>/result.yaml` or the
Folder-owner's resolved canonical Result path, plus payload files.

```text
<page>/outline/
├── <stem>-outline-v<G>.<S>[.<E>].md
│                              generation · Shape · optional evidence revision · authored · versioned
├── <stem>-context.md         what phases MAY USE generated · CONTEXT/PREPARE
├── <stem>-preview.md         actual candidate prose by C.P.B · authored during SHAPE
├── <stem>-logic.mmd          derived Page Mermaid Structure · rp00 review projection · not a plan
├── <stem>-requirement.md     what we MUST obey   V<n> generated venue · W<n> authored writing
│                             cli/requirement.py refreshes V and preserves W
├── <stem>-discussion.md      what is still ASKED authored · open D<nn> threads · never versioned
├── <stem>-feedback.md        what OTHERS said    generated · cli/feedback.py collect · page writes Landed
├── <stem>-evidence-items.md  legacy compatibility index · read-only migration input
├── <stem>-evidence.md        legacy generated status · read-only fallback
├── <stem>-files.md           what it READS/WRITES authored · F<n> records · Path + Role
├── <stem>-log.md             what CHANGED        authored · dated records · append-only · newest first
├── skill/                    ranked Page Skills; one primary store + derived editor
│   ├── <stem>.md             PRIMARY · one name per row · order is the person's rank
│   └── <stem>-skill.html     DERIVED · embedded editor
└── evidence/                 legacy compatibility material; no new writes
    ├── bibex/                citation authority and derived workbench
    ├── display/              display evidence units
    ├── supporting-runs/      generated Evidence Item lineage; pointers only
    └── materials/            immutable captured source material
```

Do not create new files under `outline/evidence/` or `<page>/evidence/`.
VALUE, DISPLAY (including table/figure), and CITE are Result payload types, not
  storage lanes. DISPLAY includes tables, figures, diagrams, illustrations,
  and algorithm blocks; `TABLE` is a legacy compatibility alias for DISPLAY.
A Page-owned Evidence attempt is an `RE`; its Result is canonical under
`results/<re-run>/`. One Evidence Item maps to one current RE lineage and one
current Result/Card projection. That Result may expose many stable inline
Evidence Labels (`$V_xxx$`, `\figure{D_xxx}`, `\table{D_xxx}`,
`\algorithm{D_xxx}`, or `\cite{C_xxx}`), whose hidden binding retains the Item,
RE, Result path, and
provenance. External evidence remains at the Supporting Run's real Result path
and is referenced from the RE Result manifest, never copied.
Old `*-evidence-items.md`, `*-evidence.md`, and `outline/evidence/*` remain
readable migration input so old Pages continue to render.

- **One question per file, and the questions do not overlap.** A fact that
  answers another file's question is misplaced: a settled thread is a log
  record, a deviation from the venue is a thread, a plan's status is on the
  page's Aims.
- **Authored versus generated is marked explicitly.** Most generated files are
  regenerated whole; Requirement is the bounded exception: its V block is
  generated and its W block is authored, so `cli/requirement.py` refreshes V
  while preserving the authored W records verbatim.
- **No file name contains `outline` except the plan**, because the plan globs
  are `*-outline-*.md`.
- **The page keeps four on-stage sections**, 🚪 Opening · 🧭 Outline · Content ·
  Aims, and nothing this folder holds. Opening stays visible and the Page's
  `🧭 Outline` opens by default and renders the current-plan table. The grid is
  `Address · Bullet · Feedback · Evidence · Supporting
  Runs · Local Run`: C/P headers keep the plan's reader order and B rows join
  routed Feedback, typed Evidence Items, their surveyed Supporting Runs, and
  local route in separate columns. A Feedback token opens the exact durable
  record through Folder inspection; it is never inert summary text. A real
  Run is a short, linked readable address such as
  `b01.j02.t03.r04` plus a compact next-action label (`run`, `rerun`, or
  `reuse`). A never-attempted real Ticket is `registered`; a failed,
  smoke-only, invalid, or explicitly stale attempt is `Rerun`, never `Done`;
  a missing Ticket is rendered as `needs … Run`, not a
  made-up id. A Page-local Run uses its Folder owner's current namespace and
  display label; its `plan` label means the address is proposed
  but no Run exists. Every displayed Run or planned-route token is an actual anchor:
  hovering it shows the Run filename, repository-relative Run path, available
  Result/Runtime paths, availability status, and next action; an unallocated
  route says so explicitly rather than inventing a path. On click, it opens
  the Outline plugin's Run Space at the exact real Run row, where its
  Purpose/Plan, Availability, Next action, and exact Run/Result
  paths are shown as selectable text. Raw Run, Result, and Runtime paths are
  never direct browser anchors:
  script and receipt responses may otherwise download instead of opening.
  The Page-to-Outline hand-off is one URL carrying `lens=run` for a Run token
  or `lens=evidence` for an Evidence item, the owning Evidence Item `focus`,
  and, for a Run, the exact `run`; do
  not split this state across one-shot browser storage keys. That explicit
  route remains authoritative while the Page frame finishes loading: no pending
  default refresh may replace it. Normal Run navigation does not open a
  modal/popover. A bounded inspector fallback may appear only when the named
  Run has no matching Runs-lens card, and it must remain closable and
  viewport-bounded on mobile Safari.
  The old `By bullet` and `Run links` segments are compatibility aliases only. A
  bounded `new-*` route stays visibly planned and may close SURVEY; only an
  ambiguous or unplaced route keeps SURVEY open. Item
  status has no column: chip colour carries the quick signal. A Run card—or
  its bounded fallback inspector—never compresses unlike facts into one status;
  it shows `Purpose` (or `Plan` before allocation), `Availability`, and `Next
  action` separately.
  Availability says `Planned`, `Run exists · Result missing`, `Run + Result`,
  or `Paths unresolved`; next action says `Allocate and run`, `Run`, `Rerun`,
  `Reuse Result`, or `Resolve path`. The compact Evidence label is
  `E<n><V/T/C/D>.<Label>`, where the authored `Label` is 1–12 ASCII
  alphanumeric characters; its accessible label carries `id · type · readable
  name` and its title carries `id · type · status`. Clicking it takes the same precise
  route an Evidence token takes: it opens the Outline plugin's Evidence
  Workspace at the exact Result row (`lens=evidence`, `focus=run-<id>`),
  scrolled into view and highlighted, where the immutable id, readable name,
  type, Bullet address, status, and Result path are shown once. The compact
  Page opens no Evidence popover and
  renders no card of those fields. There is no separate Page-authored
  narrative map. A derived `<stem>-logic.mmd` is the Page's read-only Mermaid
  Structure projection. The live Draft Space renders it at the top of
  the `By part` lens, above the plan and reading table, with its source path
  available under a collapsed `Sources` disclosure. Raw Mermaid source stays in Markdown and is not copied into
  the reader surface. While `rp00_mermaid-structure` has an active
  `ready`, `running`, `waiting-for-feedback`, or `blocked` status, the card
  must contain every Page-global `P01..PN` paragraph node; if the file is
  missing, the same location shows a named blocker instead of disappearing.
  The map may show branched argument moves; outside the
  mandatory `rp00` lifecycle, legacy Section maps may retain their own
  orientation-only grain. Content,
  Aims, and every other fold start shut. This folder
  remains the only authority for all nine records. A manuscript Section keeps
  no `### Writing Style` block in its product source; its page-owned writing
  rules are `W<n>` records inside `outline/<stem>-requirement.md`.
  Opening and Outline use distinct icons because the former orients the reader
  and the latter exposes the plan. `check.py` reports a surviving
  `## States`, `## Files`, `## Log` or `## Discussion` as `retired-section`.

The dotted address is presentation typography only. A global Supporting Run
resolves to `b01j02t03r04`; other Runs preserve their owner-native address and
display label. Never collapse distinct owner namespaces. Planned external
parents omit `.rNN`; a local full-address reservation is valid only under its
Folder owner's current naming contract and stays visibly `plan` until LAND
creates the Ticket. Page owns presentation, not family Run naming.

The grammar of every record file, its labels, its writer and its teeth:
`ref/record-shape.md`.

## 📐 The plan · one grammar

The full grammar is `ref/plan-grammar.md`; the approved example is
`ref/specimen-section-plan.md`. What a reader must know without opening them:

```text
## C<n> · <name>                     division · ≤ 8 words · names its subject
### C<n>.P<m> · <move> · S<a> to S<b> paragraph · a Section page names the sentence span
- B<k> · <head>                      legacy 4 to 11-word job head, or
                                     `[Role]` + concise substantive statement
  Note: <≤ 30 words> [🎯 Aim]        a short definition, scope, or constraint
  Annotation: <phrase>               optional reader-facing dash annotation
  Transition: <relation>             optional arrow to the next Point
  Evidence: E<NN>-<TYPE>-<slug> · …  named expectation, written at SHAPE
  Accept: …                           observable ready-evidence contract
  Evidence: none · …                  explicit source-free realization contract
  Answered: · Drawn: · Routed:       appended by the fold, one per line
```

- **The grain is the Page Type's**: on a Section page one bullet is one
  sentence slot (`S<n> · …`); on every other page one bullet is one point that
  CONTENT turns into one or more sentences.
- **Point presentation is source-compatible**: a head may begin `[Role]` (or
  `[n · Role]`) followed by a concise declarative planning statement. The live
  Outline and compact Page table print `[n · Role] statement`, strip source
  labels such as `Note:`, and render short `Note:`/`Annotation:`/indented `-`
  lines as dash annotations. `Transition:` is one arrow between adjacent
  Points, not an extra Bullet or manuscript sentence. New or edited Points
  must use plain subject–verb language; a role tag is optional and should not
  be added merely to make a line look structured; planner imperatives (`Open with`,
  `Explain`, `Introduce`, `Name`, `Connect`, `Ask`, `Keep`, `Return`, `Hand`,
  `State`) are compatibility-only legacy input. Legacy heads remain readable
  with the neutral `Point` role until an author migrates them through a new
  unapproved Shape.
- **The Bullet head stays concise.** Actual candidate sentences may be written
  during SHAPE in `<stem>-preview.md`, beside the plan. Promoted sentences live
  on the Page. A Note
  is at most 30 words (a wrapped source line is still one Note); a Note that
  carries prose is CONTENT leaking upward.
- **Every Bullet declares its evidence boundary.** Use one or more typed
  `E<NN>-VALUE-<slug>`,
  `E<NN>-CITE-<slug>`, or `E<NN>-DISPLAY-<slug>`, each with an expectation and
  an `Accept:` line; otherwise use exactly `Evidence: none · <reason>`. A
  missing Evidence line is a SHAPE defect, not shorthand for nothing owed.
  `none` forbids citation placements, concrete empirical values, figures, and
  tables in that Bullet's CONTENT realization.
- **Evidence does not inherit through a paragraph.** Paragraph and division
  cards only group the display. Each evidence-dependent Bullet owns its own
  typed Item; Bullets supporting different propositions may reuse the same
  source and Supporting Run, but never the same claim-level Item.
- **The plan carries no Aim rows.** Aims live on the page; a 🎯 annotation names one.
  An ask with no Aim is a `D<nn>` thread, never a minted Aim.
- **The address is `C<n>.P<m>.B<k>`** and it is the join key for every other
  file in the folder and every card, key and unit in the sibling lanes.

## 🔒 Generation · Shape · Evidence

```text
v0.16       pre-Content Shape 16
v0.16.1     same Shape, Evidence/Run fold 1
v1.0        first approved Content-eligible generation
v1.0.1      same approved Shape, Evidence/Run fold 1
v1.1        bounded Shape revision inside generation 1
v2.0        unapproved major redesign opened when substantial review calls for it
```

The version is `v<G>.<S>[.<E>]`; omitting `E` means zero. `G=0` never touches
Content. A bounded Shape change increments `S` and resets `E`; an evidence or
Run fold increments `E` without changing Shape. From `G>=1`, a released version
requires Content reconciliation through the CONTENT gates; creating or editing
an unapproved working Shape only updates the rehearsal and does not refresh
published Content or PDFs. A pure evidence revision declares its `shape-base`
and inherits that Shape's approval. Increment `G` only for a large change to
the central argument, hypotheses, major divisions, or overall narrative after
a substantial review round. Mechanical repairs stay within the current
version. First approval promotes to `v1.0` only after every machine-finishable
Evidence Item has been taken as far as possible; remaining secure-server or
person gates are named in the approval line. `approved:` remains a person's
act; a machine may only transcribe a direct approval or an existing Shape
approval inherited by an evidence fold.

## 🎛 The tab · Draft + Evidence + Run, one Outline plugin

The Draft Space uses two columns per paragraph: **Bullet** on the left and
**Draft** on the right. It is a static, read-only projection: no tap-to-edit,
editor, add button, form, comment composer, or browser write-back script is
rendered. The plan and candidate wording remain Markdown authorities under
`outline/`: the UI keeps the plan filename and
`outline/<stem>-preview.md` under a collapsed `Sources` disclosure, while the Mermaid card identifies
`outline/<stem>-logic.mmd`. Keep the two columns side by side on phones; omit
process metadata and controls that do not help reading. The left column shows
the authored role beside each statement, with neutral `[Point]` only as a
compatibility fallback. When a Bullet has typed or legacy evidence, the same
left column shows a compact, read-only Evidence route/card tag; the full item
card remains in Evidence Space. New candidate-sentence feedback belongs to the active
Page Run in chat, where wording, rationale, and acceptance share one Step
history. Historical signed preview lanes remain preserved in Markdown but are
not rendered. The Draft Space has no separate Comments disclosure or comment
composer. Read `ref/content-preview.md` when a workflow writes or consumes
candidate prose; it owns storage and the CONTENT handoff.

🧭 Outline is the FIRST and DEFAULT tab on a page (`live/shell.py` asks the
plugin registry's default and ranks it first; on a group page, which has no
live page, 💬 Chat is the fallback). Every other tab shows one material; only
🧭 shows the plan and, against each part of it, what that part still owes.

```text
🧭 Draft Space            default · Mermaid + paragraph/Bullet table
   Evidence Space         one Result-first Evidence table
   Run Space              RP + RE + RD + Supporting Runs
```

These are the only visible workspaces. Durable Context, Requirement,
Discussion, Feedback, Files, Log, and Skill records remain in Markdown and are
available through Folder inspection; they do not reappear as cards, lenses, or
summary panes. The visible surface is deliberately smaller than the process
authority on disk.

The plan card mirrors the Page's numbered four-step workflow strip exactly:
`1 SHAPE  2 SURVEY  3 LAND  4 EMBED`; completed steps, the current step, and
future steps remain visually distinct. The arrow notation
`SHAPE → SURVEY → LAND → EMBED` describes flow, not literal UI separators. It
does not compare an undrafted Page Content
section with the approved Shape or emit a `Shape/content mismatch` warning:
zero Content is ordinary before EMBED/CONTENT. Structural conformance remains a
checker concern at the phase boundary, not an alarm in the planning workspace.

- **Two Bullet lenses over one parse**: By part is one card per Content division
  with its Aims, ticks and `Now:` facts; 🚦 What is left is the same rows with
  ⬜ before ✅, because opening it is asking what the page still owes.
- **Evidence Space is one table, not another plugin or lens collection.**
  Its only columns are `Evidence · Bullet · Result`. Each unique Evidence id
  appears once. VALUE, DISPLAY, and CITE are compact type labels on the same
  table, not sub-tabs. `DISPLAY` (including the legacy `TABLE` alias) is
  shown as one type, not a fourth lane;
  the standalone Evidence tab is retired;
  `/_board/evidence` exists only as the embedded compatibility renderer for
  this Workspace.
- **Each Run chip opens the exact Runs-lens card, not a file download or the
  owning Evidence card.** The detail begins
  with a readable Purpose derived from an allocated Run's Ticket name and the
  owning Evidence Item. Before allocation it shows a Plan derived from that
  item's Expected/Acceptance contract and SURVEY's Local Input note. It then
  separates Availability from Next action and prints Run and Result paths as
  selectable text. New commission data belongs to the RE ticket and its
  generated `results/<re-run>/result.yaml`; the old
  `outline/<stem>-evidence-items.md` is compatibility input only.
- **Probe is not a lens or lane.** Do not create or restore a Probe tab or
  `outline/evidence/probe/`; legacy Probe artifacts may be read only for
  migration and must be routed into typed Evidence Items.
- **Process records remain off-stage.** Context, Requirement, Discussion,
  Feedback, Files, Log, and Skills are inspected through Folder when needed;
  Outline must not recreate them as chips, cards, or hidden workspace lenses.
- **Feedback is a review queue, not a source-file dump.** Show one compact
  `open · landed · rounds` tally, then the Round's main Ask. Keep its Order,
  Gate, and source collapsed. Each feedback row exposes only its headline,
  Feedback, and next Work; From, Landed provenance, and routed parent rows sit
  under `Source & routing`. The Round's instructional boilerplate is not shown.
- **The plan card sits above the division cards** and joins each bullet to
  the disk: each `E<NN>-TYPE-<slug>` joins its Supporting Runs, Local Input,
  local Page · Evidence Item Run, ready Result, and fold. Header counts `specified · planned
  · ready · folded · accepted` are computed
  separately and never collapsed.
- **One Evidence identity has one HTML target.** If a stale snapshot repeats
  an item id, show one focusable card with an explicit duplicate-identity
  warning and the conflicting source records. Never mark that contract ready
  or silently discard the conflict; SHAPE resolves it. Run groups and item
  counts use unique identities so duplicate records do not break deep links.
- **Both failure modes render as a named row, never a blank**: 🕳 owed and
  nothing there (a bullet cites `Display2` and no unit folder exists) · 🎈
  there and uncited (a card no bullet names).
- **The tab calls no model.** It reads the plan, the page, the record files and
  the sibling lanes on every open. It performs no writes. Page/Run workflows
  write the authored rehearsal records, and the next GET re-reads them.
  The Aims are read from the page first; a plan row fills only an id the page
  lacks.
- **The answer comes first**: the page's own question, then one line of counts
  (done · left · waiting), then the cards; unfinished rows stay in sight and
  finished ones fold.

The built Board page also carries a smaller, always-visible **Page Outline
table** (`haipipe-board/src/page_question.py::_outline_grid`). It is a compact
projection, not a second full tab: `Address · Bullet · Feedback ·
Evidence · Supporting Runs · Local Run`. It deliberately omits aggregate state
counts and the broader sibling-material bundle. Those remain in the richer
live 🧭 tab; item state on the compact table is conveyed only by chip colour
and the chip's title, and every chip (Feedback, Evidence, Supporting Run,
Local Run) is a deep link into the one live 🧭 tab rather than a card of its own.

In that compact Evidence column, a valid source-free Bullet renders `none` and
exposes its reason on hover. An omitted evidence decision renders `missing` as
  a defect; it is never visually conflated with an intentional source-free move.

### 🔒 Read-only boundary

The Draft Space is a reader-only projection of the current plan and candidate
wording. It renders the Mermaid map as a collapsed, native open/close
disclosure and the Bullet/Draft table, plus navigation
and an on-demand `Sources` disclosure for the source paths. It emits no Bullet editor, append control, preview
form, comment composer, or write-back script. The outer Outline POST remains a
shell-registration compatibility route; `edit-preview`, `edit-bullet`, and
`append-bullet` are rejected server-side as read-only requests.

The owning Page/Run workflow writes the Markdown sources—usually the selected
`outline/<stem>-outline-v*.md` plan or `outline/<stem>-preview.md` candidate—then
the next GET refreshes the projection. Generated HTML is never an edit target,
and a stale browser form cannot bypass this boundary. The underlying Markdown
writer contracts and approved-Shape immutability still apply outside the
reader-facing Space.

An approved Shape is immutable. The first successful Bullet write copies the
selected approved plan to the next bounded Shape version (for example `v1.1`
→ `v1.2`), marks the copy `approved: ⬜`, records `working-copy-of`, and leaves
the approved file byte-for-byte unchanged. Later writes reuse that unapproved
working file. The server returns the working version and rebuilds the Board;
the live tab re-reads it on reload. This is a narrow SHAPE edit surface, not a
CONTENT writer and not a replacement for human approval.

When returning a Page-changing response, provide direct reader links to both
views of this plugin: the Draft Space route (`<Board URL>&lens=div`) and
the Evidence Space route (`<Board URL>&lens=evidence`). The
compact Page URL and the embedded `/_board/evidence?...&embed=1` iframe are not
substitutes for these direct workspace links; the latter is an implementation
detail and should not be presented as the primary Evidence link.

### 🤝 Human review packet · the chat counterpart of the tab

When a person asks to review, check, read, or approve a page outline, the
OUTLINE phase reads these existing records as one compact, linked packet:

```text
① Current Shape    version/content licence/next version · prior-version diff + reasons · approval · arc · C/P path · measured Section counts
② Evidence owed    typed/status counts · distinct item/source/placement/key metrics · display count/purpose · material paths
③ What shaped it   routed Feedback · applicable Requirement · open Discussion only
④ Human decision   AI verdict + reason · exact approval/Decide choice · blockers · no inferred tick
```

The response links the direct Draft Space and Evidence Space routes,
then links the current plan and every record it names.  A feedback row
is shown with the bullet it shapes (`Routed:` address), not merely as a count;
an Evidence Item is shown with its expected payload, acceptance, and surveyed
path, not merely its identifier.  Routine rows may collapse into counts, but
the response never hides a material open row behind a count.  This packet is
read-only and belongs to the human-chat contract in
`page-workflows/haipipe-page-outline`; the tab remains the authoritative live
surface; the review packet itself performs no write.

For a Section, the form audit reports paragraph jobs/transitions, word and
sentence-slot budgets, implied sentence length, venue citation-density
expectation when available, and any paragraph whose sole job is defensive
meta-commentary. Citation reporting never substitutes CITE Item count for
source entries, realized placements, key mentions, or cited-sentence density.

### Evidence stays with the Bullet

```text
① COMPACT, never a second workspace   the Bullet keeps a small Evidence route; full detail lives in Evidence Space
② a TAG, not a pill        10.5px monospace · nowrap · 4px radius · 0 4px padding
③ the note is a WORD       `in bibex/` → nothing (the colour says it) · `no unit declared yet` → `owed`
④ never say it twice       a chip is `E<n><V/C/D>.<Label>` (Label ≤ 12 chars); the ↩ tag is suppressed for a card the row already names
```

No emoji inside a tag; colour is only a quick signal. A Run chip's small word
is its next action (`plan`, `run`, `rerun`, or `reuse`), never a combined
status. On the compact Page, and on the Draft Space plan card inside
the live tab, an Evidence chip is a route to its Evidence Space item
card, never a popover; inside the live tab the THING itself
(the reference as printed, the card's own question, the unit's own claim) is
shown on that card, and a 📚 panel prints `Author et al.`, never the author list.
`CITE` is one Evidence Item type, not a separate table column: one bullet may
show several compact `E<n>C.<Label>` chips beside its VALUE and DISPLAY items.
A Results bullet may legitimately show no CITE chip when it reports only this
study's analysis and points to its own displays.

## 🧷 Evidence Item → RE → Result → Card → Labels

The Outline vocabulary has five distinct layers:

```text
Evidence Item   authored obligation: what this Bullet needs
      ↓
RE              Page-local execution lineage: how this item is made ready
      ↓
Result          canonical fact/payload: what the RE produced
      ↓
Evidence Card   read-only UI projection of the current Result
      ↓
Evidence Labels zero-to-many inline anchors into that Result
```

The Card is not a second item or a second Result store. The Label is not a
new item merely because it is used more than once. A label that needs its own
acceptance, provenance, or execution lineage must be promoted to another
Evidence Item and another RE. The authoritative syntax and binding contract
is `haipipe-page/ref/page-run-families.md`.

## 🔗 The Evidence Space · one Result-first table

The table projects each Evidence id to its Bullet address and canonical Result.
New authority lives in `runs/` and `results/<re-run>/result.yaml`; payload files
remain beside that Result. An external source stays at the Supporting Run's
real Result path and is referenced from the RE manifest without copying.
Legacy `outline/*-evidence*.md` and `outline/evidence/*` may fill missing labels
or not-yet-run rows during migration, but the renderer must prefer Result data
and must not write back into those legacy locations.

## ✍️ Who writes what

```text
file            written by                                    regenerate with
────────────────────────────────────────────────────────────────────────────────────────────────
plan            SHAPE (in session or haipipe-page-outline-agent); Page/Run workflow writes or revises an unapproved working Shape; EMBED's fold appends   never
context         CONTEXT/PREPARE; generated source-bound projection         haipipe-page-context
requirement V   the generator; V1 always, V2–V4 only when     cli/requirement.py <page>.md
                the bound venue source supplies their material
requirement W   the page author; generator preserves verbatim never (authored)
discussion      any phase or the page chat, as D<nn> records  never (authored)
feedback        the generator; the page writes Landed only   cli/feedback.py collect <page>.md
evidence-items  legacy compatibility index                    no new writes
evidence        legacy generated status fallback              no new writes
files           any phase or the page chat                    never (authored)
log             every phase and the page chat, append only    never (authored)
skills          scan seed + person's rank/add/remove gestures  /_board/skill (embedded sibling store)
```

`POST /_board/outline` keeps the shell's `tab: {url, write}` registration
contract but performs no Draft write. Legacy `edit-bullet`, `append-bullet`,
and `edit-preview` actions are rejected explicitly. Candidate feedback is
recorded through the active Page Run, not a second POST queue.

### Bullet permalink

Every rendered Bullet owns one stable direct route:

```text
/_board/outline?path=<board-or-page-root>&file=<page.md>&lens=div&focus=C<n>.P<m>.B<k>
```

`lens=div` selects Draft Space and the human-readable `focus` address
opens its containing paragraph, scrolls the exact Bullet into view, and marks
that row as focused. The DOM may use a prefixed safe id such as
`bullet-C1-P1-B1`; the URL keeps the authored `C.P.B` identity. The compact
Page table and the Draft Space address both expose this same route.
Board and standalone Page shells consume the route; neither owns a second
Bullet renderer or rewrites the Page's source.

At a formal SHAPE/SURVEY/EMBED checkpoint, run affected Outline generators,
rebuild the Board and inspect the required projection. For a routine interactive
Writing Step, save and inspect the live Markdown-backed target instead of
rebuilding the whole Board. The shared `haipipe-page/ref/user-check-packet.md`
owns the exact fast-path return; never claim a deferred generated surface is
current.

Interactive Run history lives in the paired `results/<run>/vNNN.md` journals,
not a second editable Outline. The current preview remains the working source;
a historical Step is a snapshot. Preserve any historical signed preview lanes
verbatim when updating preview prose, but record new feedback in the Writing
Run. The generated Paper Round Feedback record is not a chat-feedback inbox.
Human acceptance of a paragraph does not tick the whole Shape or Page.

## 📂 Files

- `ref/plan-grammar.md` · the plan file's grammar, type switch, marks, versions, teeth
- `ref/item-table.md` · the Evidence Item table: typed identities, Run graph, derived status
- `ref/record-shape.md` · the nine record kinds: ids, labels, writers, per-kind rules
- `ref/specimen-section-plan.md` · the approved Section plan, frozen (MISQ Abstract v3)
- `ref/evidence-bundle.md` · the broader derived per-bullet join; item states come from the item ladder
- `../../haipipe-page/ref/page-run-families.md` · RP/RE/RD plus Item/Result/Card/Label bindings
- `ref/evidence/citations.md` · CITE authority and verification
- `ref/evidence/values.md` · VALUE provenance
- `ref/evidence/displays.md` · DISPLAY unit and acceptance
- `ref/evidence/pagex.md` · legacy PageX migration note; no active binding field
- `ref/space-mapping.md` · UI Space → renderer → Markdown/Result mapping
- `../../../board/haipipe-board/live/outline.py` · the parse, the lenses, `plan_card`, `_records`, the chips
- `../../../board/haipipe-board/live/shell.py` · the tab strip; 🧭 ranked first and opened by default
- `../../../board/haipipe-board/src/page_question.py` · the compact six-column Page Outline projection
- `../../../board/haipipe-board/checks/outline.py` · the standing check over every board's plans
- `../../../board/haipipe-board/src/plan_shape.py` · `plan-shape-off-type`, `bullet-missing-note`, the head and Note teeth
- `../../../board/haipipe-board/cli/requirement.py` · `cli/feedback.py` · `cli/evidence-status.py` · the three generators
- `../../page-workflows/haipipe-page-outline/SKILL.md` · the phase whose deliverable this folder is
- `ref/skill-record.md` · the nested ranked store inspected through Folder
- `../../../diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf12-outline/QPf12-outline.md` · the design page and its rulings
