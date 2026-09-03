---
name: haipipe-plugin-outline
description: >-
  The outline/ plugin of a Board page: the page's single planning authority,
  its eight process-record kinds, its nested evidence workspace, and the 🧭
  tab that reads Shape, evidence, and feedback together; first and default on
  every page. The main Page keeps only the compact Outline Table.
  Read-only surface; the deliverable of the OUTLINE phase. Trigger: outline
  plugin, outline tab, page outline, outline folder, plan file, record shape,
  evidence bundle, numbered discussion thread, /haipipe-plugin-outline.
metadata:
  version: "0.29.0"
  last_updated: "2026-09-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-outline · the page's process folder, and the tab that reads it

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface,
writer, boundary. This file owns outline's delta: what the folder holds, what
the tab shows, and who writes each file. The phase that produces the folder is
`page-workflows/haipipe-page-outline`; it loads `ref/plan-grammar.md`, not
this file.

```text
  this file      the FOLDER (eight records + evidence workspace) and ONE TAB
  ref/           plan-grammar.md · item-table.md · record-shape.md ·
                 specimen-section-plan.md · evidence-bundle.md: the exact
                 grammars a writer or parser needs
  the phase      page-workflows/haipipe-page-outline: one pass, its checks, its tick
```

## 🗂 The folder · product beside process

`<page>.md` is the PRODUCT: what the page asserts. `<page>/outline/` is the
PROCESS: how it came to assert it. Since 260831 the folder is legal on any
UNIT, task folders included (the unit symmetry, `haipipe-page` §📁): same
kinds, same grammar; a task folder simply never owes the venue-only
requirement file. Eight kinds, one flat file each with the
stem; only the plan is many-per-page, by version.

```text
<page>/outline/
├── <stem>-outline-v<N>.md    what we AGREED      authored · a person ticks · versioned
├── <stem>-requirement.md     what we MUST obey   V<n> generated venue · W<n> authored writing
│                             cli/requirement.py refreshes V and preserves W
├── <stem>-discussion.md      what is still ASKED authored · open D<nn> threads · never versioned
├── <stem>-feedback.md        what OTHERS said    generated · cli/feedback.py collect · page writes Landed
├── <stem>-evidence-items.md  what each item MUST BECOME
│                             authored · SHAPE specifies; SURVEY classifies Supporting routes + PageX Bindings + one Local Input plan + one Local Run declaration
│                             LAND validates sources and binds the ready Result (ref/item-table.md)
├── <stem>-evidence.md        what has LANDED     generated · cli/evidence-status.py · the table joined to the disk
├── <stem>-files.md           what it READS/WRITES authored · F<n> records · Path + Role
├── <stem>-log.md             what CHANGED        authored · dated records · append-only · newest first
└── evidence/                 what the plan MAY USE; never a second plan
    ├── bibex/                citation authority and derived workbench
    ├── display/              display evidence units
    ├── pagex/                exact cross-Folder source bindings
    ├── supporting-runs/      generated Evidence Item lineage; pointers only
    └── materials/            immutable captured source material
```

This is exhaustive for Page evidence storage. Never create a root
`<page>/evidence/`, an `outline/evidence/value/` copy lane, or an
`outline/evidence/probe/` lane. VALUE is an Evidence Item type, not a storage
folder: its contract and binding stay in the Outline records, while an actual
page-local VALUE payload is the Result of its local Run in sibling
`<page>/results/`; an external VALUE stays at its Supporting Run's real Result
path. Probe is retired compatibility material and has no active Page surface.

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
  `🧭 Outline` opens by default and renders only the read-only current-plan
  table. The grid is `Address · Planned move · Evidence · Supporting Runs ·
  Local Run`: C/P headers keep the plan's reader order and B rows join
  typed Evidence Items to their surveyed Supporting Runs and local route in
  separate columns. A real Run is a short, linked readable address such as
  `b01.j02.t03.r04` plus its lifecycle label (for example `Ready` or
  `Rerun`). A never-attempted real Ticket is `registered`; a failed,
  smoke-only, invalid, or explicitly stale attempt is `Rerun`, never `Done`;
  a missing Ticket is rendered as `needs … Run`, not a
  made-up id. Every displayed Run or planned-route token is an actual anchor:
  it opens the Outline plugin's `Evidence Workspace` at that Evidence Item, where
  its grouped Run items and exact Run/Result paths can be followed. The old
  `By bullet` and `Run links` segments are compatibility aliases only. An
  bounded `new-*` route stays visibly planned and may close SURVEY; only an
  ambiguous or unplaced route keeps SURVEY open. Item
  status has no column: chip colour carries
  the quick signal and the popover names the exact derived state. The compact Evidence label is
  `E<n><V/C/D>.<Label>`, where the authored `Label` is 1–12 ASCII
  alphanumeric characters; clicking it reveals the immutable id,
  full readable name, full type, PageX sources,
  acceptance contract, routes, and Result. There is no separate Page-authored
  narrative map. Content, Aims, and every other fold start shut. This folder
  remains the only authority for all eight records. A manuscript Section keeps
  no `### Writing Style` block in its product source; its page-owned writing
  rules are `W<n>` records inside `outline/<stem>-requirement.md`.
  Opening and Outline use distinct icons because the former orients the reader
  and the latter exposes the plan. `check.py` reports a surviving
  `## States`, `## Files`, `## Log` or `## Discussion` as `retired-section`.

The dotted address is presentation typography only. It resolves to the same
canonical stored identity `b01j02t03r04`; dots never mint a second Run id and
planned parent routes omit `.rNN` until a real Run is allocated.

The grammar of every record file, its labels, its writer and its teeth:
`ref/record-shape.md`.

## 📐 The plan · one grammar

The full grammar is `ref/plan-grammar.md`; the approved example is
`ref/specimen-section-plan.md`. What a reader must know without opening them:

```text
## C<n> · <name>                     division · ≤ 8 words · names its subject
### C<n>.P<m> · <move> · S<a> to S<b> paragraph · a Section page names the sentence span
- B<k> · <head>                      4 to 11 plain words: what the point DOES
  Note: <≤ 30 words> [🎯 Aim]        the constraint or definition
  Evidence: E<NN>-<TYPE>-<slug> · …  named expectation, written at SHAPE
  Accept: …                           observable ready-evidence contract
  Answered: · Drawn: · Routed:       appended by the fold, one per line
```

- **The grain is the Page Type's**: on a Section page one bullet is one
  sentence slot (`S<n> · …`); on every other page one bullet is one point that
  DRAFT turns into one or more sentences.
- **The plan never quotes the sentence it plans.** The sentence lives on the
  page; the plan says what the sentence must do and what constrains it. A Note
  is at most 30 words (a wrapped source line is still one Note); a Note that
  carries prose is DRAFT leaking upward.
- **Typed Evidence Items are the exception**: `E<NN>-VALUE-<slug>`,
  `E<NN>-CITE-<slug>`, or `E<NN>-DISPLAY-<slug>`, each with an expectation and
  an `Accept:` line. No Evidence line means nothing is owed.
- **The plan carries no Aim rows.** Aims live on the page; a 🎯 annotation names one.
  An ask with no Aim is a `D<nn>` thread, never a minted Aim.
- **The address is `C<n>.P<m>.B<k>`** and it is the join key for every other
  file in the folder and every card, key and unit in the sibling lanes.

## 🔒 The plan freezes at approval, not at creation

```text
  ✍️ v1 · approved: ⬜   a working document: edit, delete, rewrite freely
        │  🧑 a person ticks approved:
        ▼
  🔒 v1 · approved: ✅   frozen, correct as of that date
        │  the work moves on
        ▼
  ✍️ v2 · approved: ⬜   supersedes: v1 · v1 is kept, because it was right then
```

The fold's appends (`Answered:` `Drawn:` `Routed:` and a `PP<NN>` id once a
card serves a bullet) are the one write an approved version accepts, and they
add, never edit: a plan that rewrote its own heads as work landed would always
look finished. `approved:` is a person's; a machine may transcribe a person's
chat approval with the quote and the time, and writes `checked:` for itself.

## 🎛 The tab · Bullet + Evidence, one Outline plugin

🧭 Outline is the FIRST and DEFAULT tab on a page (`live/shell.py` asks the
plugin registry's default and ranks it first; on a group page, which has no
live page, 💬 Chat is the fallback). Every other tab shows one material; only
🧭 shows the plan and, against each part of it, what that part still owes.

```text
🧭 Bullet Workspace       default · By part | What is left
   Evidence Workspace     Evidence Items and their material/Run lineage
   Plan Context           Requirement | Discussion | Feedback
   Page Records           Files | Log
```

Bullet and Evidence are the two primary workspaces and justify the plugin's
name: **Outline = Bullet + Evidence**. Plan Context explains why the outline
has its current shape; Page Records report what it touched and what changed.
They remain separate authored files on disk, but they do not compete as five
top-level buttons.

- **Two Bullet lenses over one parse**: By part is one card per Content division
  with its Aims, ticks and `Now:` facts; 🚦 What is left is the same rows with
  ⬜ before ✅, because opening it is asking what the page still owes.
- **Evidence Workspace is an internal lens, not another plugin.** It joins each
  Evidence Item to Supporting Runs, its optional local Run/Result, citation,
  value, display, and PageX material. The standalone Evidence tab is retired;
  the compatibility `/_board/evidence` renderer may be embedded here only.
- **Probe is not a lens or lane.** Do not create or restore a Probe tab or
  `outline/evidence/probe/`; legacy Probe artifacts may be read only for
  migration and must be routed into typed Evidence Items.
- **One subordinate chip per process record file that exists**, with its record
  count, grouped under Plan Context or Page Records; a file that does not exist
  draws no chip. Every lens draws records the same way: id
  badge, headline, label grid, status pill, detail behind "more".
- **The plan card sits above the division cards** and joins each bullet to
  the disk: each `E<NN>-TYPE-<slug>` joins its Supporting Runs, PageX bindings,
  local Page · Evidence Item Run, ready Result, and fold. Header counts `specified · planned
  · ready · folded · accepted` are computed
  separately and never collapsed.
- **Both failure modes render as a named row, never a blank**: 🕳 owed and
  nothing there (a bullet cites `Display2` and no unit folder exists) · 🎈
  there and uncited (a card no bullet names).
- **The tab writes nothing and calls no model.** It reads the plan, the page,
  the record files and the sibling lanes on every open, so it cannot be stale.
  The Aims are read from the page first; a plan row fills only an id the page
  lacks.
- **The answer comes first**: the page's own question, then one line of counts
  (done · left · waiting), then the cards; unfinished rows stay in sight and
  finished ones fold.

The built Board page also carries a smaller, always-visible **Page Outline
table** (`haipipe-board/src/page_question.py::_outline_grid`). It is a compact
projection, not a second full tab: `Address · Planned move · Evidence ·
Supporting Runs · Local Run`. It deliberately omits aggregate state counts and
the broader sibling-material bundle. Those remain in the richer live 🧭 tab;
item state on the compact table is conveyed only by chip colour and popover.

### 🤝 Human review packet · the chat counterpart of the tab

When a person asks to review, check, read, or approve a page outline, the
OUTLINE phase reads these existing records as one compact, linked packet:

```text
① Current Shape    plan v<N> · approval state · arc · C/P reader path
② Evidence owed    Evidence Item table · typed/status counts · material source/Run paths
③ What shaped it   routed Feedback · applicable Requirement · open Discussion only
④ Human decision   exact approval/Decide choice · blockers · no inferred tick
```

The response links the current plan and every record it names.  A feedback row
is shown with the bullet it shapes (`Routed:` address), not merely as a count;
an Evidence Item is shown with its expected payload, acceptance, and surveyed
path, not merely its identifier.  Routine rows may collapse into counts, but
the response never hides a material open row behind a count.  This packet is
read-only and belongs to the human-chat contract in
`page-workflows/haipipe-page-outline`; the tab remains the authoritative live
surface and writes nothing.

### Chips stay inside the sentence

```text
① INLINE, never a column   a chip lives in the row's own span; a sibling column steals the text's width
② a TAG, not a pill        10.5px monospace · nowrap · 4px radius · 0 4px padding
③ the note is a WORD       `in bibex/` → nothing (the colour says it) · `no unit declared yet` → `owed`
④ never say it twice       a chip is `E<n><V/C/D>.<Label>` (≤ 12 chars); the ↩ tag is suppressed for a card the row already names
```

No emoji inside a tag; status belongs to colour and the popover detail. A chip opens a native popover holding the THING itself
(the reference as printed, the card's own question, the unit's own claim); a
📚 panel prints `Author et al.`, never the author list.
`CITE` is one Evidence Item type, not a separate table column: one bullet may
show several compact `E<n>C.<Label>` chips beside its VALUE and DISPLAY items.
A Results bullet may legitimately show no CITE chip when it reports only this
study's analysis and points to its own displays.

## 🔗 The evidence workspace · nested material, one derived join

The tab shows, per bullet, the join of the frozen address to everything
that names it: the sentence scaffold (`realizes:`), Evidence citation keys,
display units and their `accepted:` tick.
The joined view is a projection. Material authority lives below
`outline/evidence/`, and a human
choice such as `selected: Display2` lives on the owning unit. Each typed item's
state comes only from the ladder in `ref/item-table.md`. The broader point-level
projection is described in `ref/evidence-bundle.md`; it has no competing status
vocabulary and is not `<stem>-evidence.md`. That generated file is specifically
the authored Evidence Item table joined to Supporting/Local Run receipts and
ready local Results.

## ✍️ Who writes what

```text
file            written by                                    regenerate with
────────────────────────────────────────────────────────────────────────────────────────────────
plan            SHAPE (in session or haipipe-page-outline-agent); EMBED's fold appends   never
requirement V   the generator; V1 always, V2–V4 only when     cli/requirement.py <page>.md
                the bound venue source supplies their material
requirement W   the page author; generator preserves verbatim never (authored)
discussion      any phase or the page chat, as D<nn> records  never (authored)
feedback        the generator; the page writes Landed only   cli/feedback.py collect <page>.md
evidence-items  SHAPE: Target · Label · Need · Expected · Acceptance; SURVEY: classified existing/planned Runs +  never
                PageX Bindings + one Local Input plan + one Local Run declaration; person: Decide;
                LAND executes/validates sources and binds input + Result
evidence        the generator                                 cli/evidence-status.py <page>.md
files           any phase or the page chat                    never (authored)
log             every phase and the page chat, append only    never (authored)
```

`POST /_board/outline` exists only so the shell's `tab: {url, write}` contract
holds; it writes nothing.

## 📂 Files

- `ref/plan-grammar.md` · the plan file's grammar, type switch, marks, versions, teeth
- `ref/item-table.md` · the Evidence Item table: typed identities, Run graph, derived status
- `ref/record-shape.md` · the eight record kinds: ids, labels, writers, per-kind rules
- `ref/specimen-section-plan.md` · the approved Section plan, frozen (MISQ Abstract v3)
- `ref/evidence-bundle.md` · the broader derived per-bullet join; item states come from the item ladder
- `ref/evidence/citations.md` · CITE authority and verification
- `ref/evidence/values.md` · VALUE provenance
- `ref/evidence/displays.md` · DISPLAY unit and acceptance
- `ref/evidence/pagex.md` · cross-Folder source binding and validation
- `../../haipipe-board/live/outline.py` · the parse, the lenses, `plan_card`, `_records`, the chips
- `../../haipipe-board/live/shell.py` · the tab strip; 🧭 ranked first and opened by default
- `../../haipipe-board/src/page_question.py` · the compact five-column Page Outline projection
- `../../haipipe-board/checks/outline.py` · the standing check over every board's plans
- `../../haipipe-board/src/plan_shape.py` · `plan-shape-off-type`, `bullet-missing-note`, the head and Note teeth
- `../../haipipe-board/cli/requirement.py` · `cli/feedback.py` · `cli/evidence-status.py` · the three generators
- `../../page-workflows/haipipe-page-outline/SKILL.md` · the phase whose deliverable this folder is
- `../../../diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf12-outline/QPf12-outline.md` · the design page and its rulings
