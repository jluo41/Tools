---
name: haipipe-plugin-paper
description: >-
  The Paper-level plugin for one paper Board: a source-backed work console
  with Setup, Ideation, Story, Run, and Delivery Spaces. It follows the live Plugin
  contract used by haipipe-plugin-outline but owns the paper journey rather
  than one Page's outline. Trigger: Paper Plugin, paper plugin, paper console,
  paper work console, paper spaces, /haipipe-plugin-paper.
metadata:
  version: "0.4.1"
  last_updated: "2026-09-21"
---

# /haipipe-plugin-paper · the Paper-level work console

**LOAD `haipipe-plugin` FIRST.** It defines the common Plugin law: STORAGE,
SURFACE, WRITER, and BOUNDARY. This skill defines the Paper-level delta. It is
the Paper counterpart to `haipipe-plugin-outline`:

That skill is written for Page-level plugins. For this Board-level plugin read
it for the four obligations only, then return here: the route, the Spaces, the
claim rules and the writer rule are all in this file.

```text
haipipe-plugin-outline    Page-level planning surface
                           Draft + Evidence + Run

haipipe-plugin-paper      Paper-level coordination surface
                           Setup + Ideation + Story + Run + Delivery
```

Paper Plugin is not a replacement for Outline and is not another Paper Page.
It is one optional surface on a Paper Board, used to oversee the paper's
records and route a person to the authority that owns each one.

## 🔗 Default Plugin Link

When returning a link for a Paper Board, return the complete Paper Plugin
route by default:

```text
/_board/paper?path=<URL-encoded Paper>/board.md&file=board.md
```

Both query parameters are required. `path` identifies the owning Board source;
`file=board.md` states that this is a Board-level surface rather than a
Page-level Outline route. Use the configured reader-facing origin (the `--public-url` the board
server was started with; find the listening port before quoting a link, and
never hand a remote reader `127.0.0.1`) and keep the complete query in one
Markdown link. Add a hash only when the reader asks for a particular subspace.
The route is `#<space>/<view>`:

```text
setup      folders · sessions
ideation   pool · evidence · admission
story      spine · claims · tasks · sections · evidence
run        page · evidence · supporting · gates · workflow
delivery   manuscript · sections · displays · checks · rounds
```

There is no per-paper file behind the route: `live/paper.py` renders the five
Spaces from the Board's Markdown on every open, exactly as Outline does. The
0.1.0 `console/` prototype (a static `data.js` rebuilt by hand, one paper
only) is retired and is never read.

## 🧩 The four Plugin obligations

### 📦 Storage

Paper Plugin reads the Paper Board and its owned projections; it does not mint
a second authority store:

```text
Paper-<Slug>/
├── board.md                         Board identity and Paper links
├── A1-Story/
│   ├── Story00-ideation/            candidate Idea records
│   └── StoryA-<desk>-<idea>/        one prospective Story blueprint
├── Ba-<desk>-Main/                  manuscript Section Pages
├── Bb-<desk>-Appendix/              supporting Section Pages
├── Bc-<desk>-Round/                 feedback and response Pages
└── delivery/                        generated whole-paper projection
```

**Markdown is the only truth source (JL 260918).** The route is Markdown →
HTML on every GET: every word a Space shows is read from a `.md` file of the
paper, the task home, or the discovery home at that moment, so a Markdown edit
is live on reload and the HTML is never an input to anything. The route also reads authored configuration (`paper-build.toml`,
`discovery.yaml`) and generated receipts (`delivery/build-manifest.json`,
Run `runtime.yaml`, and pair manifests). Config stays with its owner; receipts
are shown, never edited through this presentation layer.

Every Space ends with a `backend Markdown` card that names the exact files
it was read from (✓ present · ⬜ absent), so a reader can always trace a word
to its file. The only words that are not read from a file are the plugin's own
labels, briefs and empty-state hints. Page rendering copy lives in
`live/paper.py`; drawer registration and its hint live in
`assets/js/10-drawer/09-plugin-paper.js`. Both are versioned with the Board skill.

`board.md`, Story00, StoryA, Section Pages, Round Pages, delivery receipts,
and owner-native Run records remain authoritative. The Plugin stores nothing:
no `console/`, no `data.js`, no Links key. A Board opts in with one line in
board.md, `dialect: paper`, which `page_board.py` exposes as
`data-board-dialect="paper"` for the drawer registration
(`assets/js/10-drawer/09-plugin-paper.js`).

### 🖼 Surface

The Paper Plugin is a Board-level right-pane Plugin. The Board shell owns the
Plugin tab, close behavior, persistence, and iframe. The Paper surface follows
the Outline template: quiet white/gray typography, compact bordered tabs,
source-backed rows, and no second shell or decorative dashboard chrome.

Reading rules (JL 260918): base type 16px; label/value rows are a two-column
table with cell edges and a shaded label cell, never text nested in text; a
value that is itself a table or a tree spans the full width; every table has
cell edges; long prose is set one sentence per line, for display only. No
type under 12px; a closed card shows its whole headline (never an ellipsis on
a claim or an idea); a card says a thing once (a subline that repeats the
`where` label is dropped). Checked by driving all twenty Space views in real
Chrome at 1360px and 2000px: no page overflow, no view leaking, nothing past
the right edge.

The five visible top-level Spaces are:

```text
Setup Space       how the Paper Board is arranged and can be prepared
Ideation Space    candidate Ideas, comparison, testing, and admission
Story Space       the one prospective Story and its research-to-section map
Run Space         Page, Evidence and Supporting Runs, gates, the Run-Type map
Delivery Space    the manuscript delivery/ holds, its compile order and checks
```

`Space` is the reader-facing word for `Workspace`. They are the same surface
concept. A physical folder is not automatically a visible Space, and a Space
does not create a new folder.

### ✍️ Writer

The current Paper Plugin is a read-only projection. It reads Paper sources on
each open and routes actions to the owner that is allowed to write them.

**The Paper Plugin has two separate copy-only engagements.** Every card
summary, every Spine row, and any text selection inside a Space carries a
`⧉ chat` control. It puts a discussion/context snippet on the clipboard:

```text
[paper board · <Paper>] <Space> › <view> › <card> › <row>
source: <repo-relative .md path> · <row ref, e.g. C5 · E6>
quote: "<the selected words, when there is a selection>"
text: <the row or card text>
note:
```

The person pastes it into the chat and types the note; the agent then edits
the Markdown the `source:` line names. Two sizes of edit: a TRACEABILITY edit
(an address suffix such as `Task: b03.j02.` or `Discovery: b01.j04.`, a typo)
is made directly in that file, with no version bump and no rebuild, because
the page re-reads the Markdown on every open; an edit that changes what the
paper says (a claim, a research question, a design, a Section's narrative)
belongs to the owning skill in the table below, and the agent routes there. Cards carry `data-src` (the Markdown
they were read from) and `data-ref` (the row). The page makes no request of
its own, so feedback can never fork the truth into a second store. A browser
`(+)` writer, if added later, must append to the card's judgment Run journal
(`results/<run>/v<NNN>.md`, run-naming.md §8) exactly as Outline's Draft Space
composer does, never to a Plugin file.

Selecting text in the Workflow map cites `ref/space-mapping.md`, its source of
Run definitions. This remains a discussion/context snippet, not a Run request.
The Run map is a read-only catalogue; actual Tickets, Results, and status stay
in the separate native Run inventory. A distinct `⧉ Copy Run request` control
appears in `Start here` cells only for exact Paper judgment targets currently
bound to an admitted Idea, C5 claim, C7 obligation, or C8 narrative row. Its
copied prompt names the Board, source Page and item, instantiated Spec and Run
Type, owner, prerequisites, exact typed matching Run/status, expected receipt,
and next owner-permitted action. It may ask the owner to inspect or commission
that bounded judgment, but clicking it only copies the text: it does not send,
start, allocate, or write. Page Structure/Writing, Evidence, Delivery, Support,
Compile, and Response targets stay prompt-free until this view can bind their
required owner/worker, scope, input, and gate state. Setup Apply remains not
built. Never show a Run prompt where the target or owner workflow is unresolved;
the receiving owner must verify prerequisites and HOLD when a gate or required
input fails.

| Surface | Authority / writer | Plugin behavior |
|---|---|---|
| Setup | Board builder and explicit setup workflow | show folders, Pages, and one session row per Section Page; Preview before Apply |
| Ideation | `haipipe-ideation` / `haipipe-paper-ideation` | show the Idea pool and its admitted handoff; do not create a second selection receipt |
| Story | `haipipe-paper-story` and the Story Page | show C1–C8, claims, roadmaps, and Section routes; do not replace StoryA |
| Run | the owner-native Run/Task/Discovery workflow | show Run-Type and receipt links; do not invent a Run instance |
| Delivery | `haipipe-paper-assemble` | show generated readiness; do not edit delivery artifacts |

Setup Apply may become a bounded writer, but it must preview the exact folder,
Page, section, and Codex-session changes first and apply them as one explicit
setup action. The Plugin must never silently create folders, sessions, or
receipts merely because a row is visible.

### 🚧 Boundary

The Paper Plugin coordinates the Paper Board; it does not become the owner of
Page prose, Evidence Results, Discovery records, Task configurations, or
delivery wording. Board discovery must continue to treat Plugin implementation
files as non-Page material. No Paper Plugin subspace may silently copy an
authority record just to make its table easier to render.

## 🗂 Spaces and Subspaces

Each top-level Space answers one operational question. Its subspaces are
views over the same records, not new lifecycle stages.

### Setup Space · “What is configured?”

```text
Board             board.md identity · the scaffold folders haipipe-paper §📂
                  names, each present or missing on disk
Folder & Page     every ## Pages group with its pages, linked to their Outline
Codex sessions    one row per Section Page; no rows for Ideation, Story, or Supporting
```

A Preview / Apply writer is not built; until it is, nothing on this surface
claims to create a folder, Page, or session.

Codex sessions are per Section Page (JL 260916): setting up a Section means
creating its folder, its Page, and its one Codex session, named for that
Section (for example `paper-misq-introduction`). Ideation, Story, and
Supporting work run in the current session and never get a session row.

The Setup Space is the place where a person can eventually say “create this
setup”. Until the setup writer is connected, it must say `preview only` and
name the missing writer rather than displaying a fake Apply success.

### Ideation Space · “Which Idea should continue?”

```text
Idea pool         one collapsed Idea Card per idea (Discussion = ridea Run), the shape of Outline's
                  Evidence cards: the summary line is id · title · bullet
                  count · Evidence chips · division · verdict; opening it shows
                  the Bullets with their Notes and Evidence lines, the bound
                  Evidence Items with their Verified tick, the table fields,
                  and the division link. Source: the page's Ideas (ranked)
                  table when Content carries one, else the plan's
                  `Idea <n>: <title>` divisions (an Ideation Page before Content)
Evidence items    outline/<stem>-evidence-items.md with each Verified tick;
                  novelty and prior-art checks are its CITE items
Admission         workflow/selection.yaml · handoff/paper-ideation.yaml ·
                  projection/paper-ideation-sync.yaml, present or absent, and
                  every `went to` cell
```

Position in the ranking is an attention aid. `idea_id` is the stable identity;
the Plugin must not treat list position as an Idea identifier or create a
second admission decision.

### Story Space · “What is this Paper saying and doing?”

```text
Spine               each Story<Letter> page: its state line, then the Story's
                    own C1 Identity, C2 Pitch and C4 Stakes content as
                    label/value rows; compile order collapsed at the end
Claims & Hypothesis one card per C5 E-row, joined to its C3 research question;
                    the card's Discussion row is its rclaim Run when one exists
Task Roadmap        first the Task home: examples/<Project>/tasks/ (or task/,
                    or board.md `task-home:`), one collapsed card per bNN block
                    THIS PAPER CLAIMS, open = its claimed jobs, each a table
                    addr · task · develops · runs · state read off the folder
                    in both shapes (task folder under the job, or flat
                    runs/<task>/ scripts/<task>/ results/<task>/); a Run's
                    receipt is results/<run>/runtime.yaml. The claim = board.md
                    `blocks: b03 b04 b02.j01` + every address on a C7 row.
                    Address grammar: lowercase two-digit `bNN[.jNN[.tNN[.rNN]]]`
                    (a row id such as `B2` is not an address). Convention: end
                    the row's design cell with `Task: b03.j02.`, as C6 ends
                    its scope cell with `Discovery: b01.j04.`; a row may carry
                    several addresses and its card resolves each. Two words,
                    never mixed: CLAIMED = a block or job shows in the Task
                    home because `blocks:` or any C7 address covers it;
                    ADDRESSED = the C7 row names its own address, and its card
                    reads `allocated · N/M levels exist`, `address named ·
                    nothing on disk`, or else `no address yet`;
                    unclaimed blocks and jobs are named once, muted, never
                    expanded; no claim = whole home, said so. Then one card per
                    C7 row; its bNN[.jNN[.tNN]] address says which levels
                    exist, else `no address yet`. Then Discovery needs: the C6
                    D-rows with a discovery column = the inquiry each row names
                    by address (b01.j04), and the Discovery home
                    (examples/<Project>/discoveries/, or `discovery-home:`):
                    one card per jNN inquiry, open = its Discovery Task Pages
                    (question · runs · status · outcome from discovery.yaml),
                    claimed by `discoveries:` + C6 addresses the same way.
                    Discussion = rtask Run
Sections            one card per C8 row: what the section must express, its
                    minted page and state; Discussion = rnarra Run
Evidence Items      the hero list only: every DISPLAY item on a Main page and
                    every VALUE item on the Abstract page, each linking to its
                    Section's Evidence Space; no Run, it points at the re- Run
```

Every list uses one card shape, the Evidence card of Outline: chevron · kind
pill · label with a muted subline · where · status; open shows label/value
rows. A card is a projection of a Story row; the Story page stays the
authority and the judgment Run (`haipipe-paper/ref/run-naming.md` §8) keeps
the discussion.

A board with no Story page shows one named row, `no Story yet · G0 open`,
never an empty pane.

Story Space presents StoryA's C1–C8 blueprint. C1–C5 are the seed and evidence
basis; C6 is the Discovery Roadmap; C7 is the Task Roadmap; C8 is the Section
Narrative and compile order. These are Story divisions, not extra Pages or
extra Spaces.

### Run Space · “What bounded work moves the Paper?”

The three run types are the Page Run families of
`haipipe-page/ref/page-run-families.md`, read at paper level.

```text
Page Runs         RP Page Writing (rp-struct · rp-sec · rp-para · rp-scratch),
                  RD Page Delivery (rdNN) and the judgment Runs (ridea · rclaim
                  · rtask · rnarra): one card per page, open = run · kind ·
                  runtime status · Outline Run Space link
Evidence Runs     RE Page Evidence: one card per page, one row per Evidence
                  Item joined to the Local Run the item names (re-value ·
                  re-display · re-cite, or the legacy paper-local pj…), with
                  its mode, its Result, and the Supporting Runs that feed it;
                  an item with no Local Run reads `not allocated`, a ticket no
                  item names is listed as unnamed
Supporting Runs   owner-native Runs cited on an item's `Supporting Runs:` line,
                  as a Block › Job › Task › Run tree per owner: Execution (the
                  Task home) and Discovery (the Discovery home). One card per
                  block; each Run row resolves its ticket and receipt on disk
                  (or says ✗) and lists who uses it, grouped by page. A Run is
                  never renamed or copied; a line with no address is listed
                  apart
Gates             G0–G5 read from the files haipipe-paper-workflow names
                  (I3 receipt · C8 rows vs minted pages · build-manifest.json
                  · Round pages); a gate no file answers says so
                  Workflow map      Run Type / Spec / control entries by Space,
                                    including purpose, owner/worker Skill,
                                    actor, prerequisites and entry path
                  ref/space-mapping.md, plus a `folder on this board` column;
                  under it Folder tree × Run-Type, two boxes of two aligned
                  columns: box 1 the paper folder, box 2 the project homes
                  (claimed Task-home blocks · Discovery inquiries). Left the
                  bare, COMPLETE tree of the REAL folders as a collapsible
                  explorer (board/ and _archive/ skipped; page groups open,
                  everything else closed; a folder opens three levels below a
                  page folder, two below a Task or Discovery task; files
                  listed up to 40 per folder, the rest a count; a folder the
                  map has no slot for reads `not in the map`); right, one
                  edged cell per row: the folder's counts, and on the first
                  folder of each slot its Run-Type chips. Nothing else on the
                  tree (JL: less is more). A slot with no folder yet is named
                  under the boxes. The card states its backend Markdown; a
                  definition view, never a creator
```

The Workflow map is a definition view, not another Run inventory. It shows
`mode · schema · path` for each Run Spec. Concrete Run instances and their
receipts remain with their native owners.

### Delivery Space · “What leaves the Paper?”

```text
Manuscript        the paper as delivery/ holds it: title, venue, status and
                  build time from build-manifest.json; one row per output
                  named in paper-build.toml [outputs] (built · size · written,
                  or ⬜ not built); returned files under delivery/word-feedback/
                  are read, never built from; build facts (words, citations,
                  displays, pages ready, submission status) and the build
                  command; no delivery/ = `G4 open`, said so
Sections          the compile order (manifest, else the Story's C8 block): one
                  row per page with its state, outline version + approval,
                  fragment (delivery/latex/<page>.tex), its own 📜 📝 🌐 lanes,
                  the last build's ready verdict and notes; a page edited after
                  the build is flagged
Displays          delivery/display-register.md: printed vs declared numbering,
                  label, unit, page; submission-assets listed
Checks            the manifest's checks (✓/✗), latexmk and docx return codes,
                  evidence mode, every build warning and unresolved \ref
Rounds & Venue    one card per Bc-<desk>-Round page (kind, received, due, base
                  build, folders, state) and the venue page from the board's
                  Links; the Round page owns the dispositions
```

Delivery reads only what haipipe-paper-assemble wrote and what the pages
carry; it builds nothing on open. The build is one command, shown in place.

## Workflow, Run Specs and control records

`haipipe-paper-workflow/ref/run-workflow.md` is the canonical Spec list and
compatibility map. A Workflow Definition lists bounded Run Specs and routes;
its Runtime lists actual native Runs and receipts. Run Types are reusable
contracts. Spaces/Workspaces present these records. A Step stays inside a Run.

The map at `ref/space-mapping.md` names each Run's reader-facing name,
canonical Type and Spec, bounded purpose, owner/worker Skills, actor,
prerequisites, and Space role/entry. Its four control rows have no Run Type.
The map is read-only and does not allocate work or prove execution. Resolve
actual target, owner, type, dependency, matching native Run and status from the
Runtime/native owner; keep planned, managed and reused records distinct.

Paper judgment Specs are `idea`, `claim`, `obligation`, and `narrative`; shared
native Specs are `support`, `structure`, `write`, `evidence`, and `deliver`;
Paper delivery/response Specs are `compile` and `response`. Selection (I3),
setup, G0–G5, sync and Story/Section routes remain control actions. In particular,
`paper.section.route` records G3 and links the selected Section Specs; it is
not a missing extra Run or a replacement for Section writing.

Keep the definition view separate from allocated native Runs. A visible row
never creates a receipt. The board's existing `⧉ chat` cites its source and
copies discussion context only. The separate Run-request control is available
only on exact, supported Paper judgment targets; all other cells remain
prompt-free until their target and prerequisites can be resolved.
The old `paper.*` Run-Type labels remain explained by
the canonical compatibility table; do not use Phase records as workflow units.

## 🚦 Gates and ownership

The Paper Plugin may display gate state, but the named owner closes the gate:

```text
G0  Ideation → Story       I3 / Paper Ideation handoff
G1  Story → work           Story release of relevant Discovery/Task work
G2  work → Story           accepted owner-native Result and interpretation
G3  Story → Section        human release of one C8 Section row
G4  Section → Compile      current Section Page release/CHECK and delivery
G5  Round → next route     every concern routed once and answered once
```

The Plugin is a read-only overview of these gates. It must never infer a
human approval from a percentage, a folder's existence, a generated PDF, or a
Run-Type row marked `recorded`.

## 🔒 Link and presentation rules

- Paper Plugin links use `/_board/paper` with URL-encoded `path` and `file`.
- Outline links use `/_board/outline` and a concrete Page `file`; the two
  routes are siblings, not aliases.
- A Paper link may start at `file=board.md` and use a hash for a Paper
  subspace, for example `#story/claims` or `#run/workflow`.
- The parent Board URL remains the shell's URL when the Plugin is in the right
  pane; the iframe URL carries the Paper Plugin route, just as Outline does.
- The surface is calm and dense: source path, owner, state, and next action
  are visible; decorative cards, duplicate dashboards, and hidden state are
  not.
- `Run-Type` is not a synonym for `Space`, `Workspace`, or concrete `Run`.

## ✅ Completion checks

- The skill is discoverable as `haipipe-plugin-paper` and loads the common
  `haipipe-plugin` contract first.
- The Paper Board exposes one `Paper` Plugin entry, not a generic Console
  entry and not a second Outline entry.
- Its direct link has the form
  `/_board/paper?path=<board.md>&file=board.md`, and it answers on any Board
  whose board.md says `dialect: paper` with no other file present.
- Setup, Ideation, Story, Run, and Delivery are visible Spaces; their subspaces remain
  views over authority records.
- Every Spec row names its canonical Run Type and owner; controls are visibly
  separate and have no Run Type. No row implies that a Run exists merely
  because it is planned.
- The map is source-grounded in `ref/space-mapping.md`; actual matching Run
  identities and status remain with native inventories.
- StoryA remains the sole prospective Paper blueprint, and Section Pages keep
  their own Page/Outline lifecycle.
- The route reads no `console/`, `data.js`, or other per-paper projection;
  `tests/test_paper_plugin.py` keeps that tooth.
