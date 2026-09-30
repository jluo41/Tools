---
name: haipipe-workbench-paper
description: >-
  The Paper-level workbench for one paper Board: a source-backed work console
  with Ideation, Story, Sections, and Delivery Spaces, each with its content on
  the left and its own Runs panel on the right. It follows the live Workbench
  contract used by haipipe-workbench-page but owns the paper journey rather
  than one Page's outline. Trigger: Paper Workbench, paper workbench, paper console,
  paper work console, paper spaces, /haipipe-workbench-paper.
metadata:
  version: "0.14.0"
  last_updated: "2026-09-29"
---

# /haipipe-workbench-paper · the Paper-level work console

**LOAD `haipipe-workbench` FIRST.** It defines the common Workbench law: STORAGE,
SURFACE, WRITER, and BOUNDARY. This skill defines the Paper-level delta. It is
the Paper counterpart to `haipipe-workbench-page`:

That skill is written for Page-level workbenches. For this Board-level workbench read
it for the four obligations only, then return here: the route, the Spaces, the
claim rules and the writer rule are all in this file.

```text
haipipe-workbench-page     Page-level planning surface
                           Draft + Evidence + Delivery, Runs beside each

haipipe-workbench-paper    Paper-level coordination surface
                           Ideation + Story + Sections + Delivery, Runs beside each
```

Paper Workbench is not a replacement for a Page's workbench and is not another
Paper Page. It is one optional surface on a Paper Board, used to oversee the
paper's records and route a person to the authority that owns each one.

The design is drawn in `servers/workbench-paper/studio/paper-workbench-design.excalidraw`
(JL 260927); the served page follows the drawing.

## 🔗 Default Workbench Link

When returning a link for a Paper Board, return the complete Paper Workbench
route by default:

```text
/_board/paper?path=<URL-encoded Paper>/board.md&file=board.md
```

Both query parameters are required. `path` identifies the owning Board source;
`file=board.md` states that this is a Board-level surface rather than a
Page-level Draft route. Use the configured reader-facing origin (the `--public-url` the board
server was started with; find the listening port before quoting a link, and
never hand a remote reader `127.0.0.1`) and keep the complete query in one
Markdown link. Add a hash only when the reader asks for a particular place.
The route is `#<space>[/<tab>][/<view>]`:

```text
ideation
story      spine · logic-work
sections   main · appendix          ×  table · narrative · evidence
delivery   latex · word · rounds    ×  preview · artifacts · checks   (rounds has no views)
```

The pre-260927 routes (`#setup/…`, `#run/…`, `#story/claims`, `#story/tasks`,
`#delivery/manuscript`, …) still land on the view that now holds their content.

There is no per-paper file behind the route: `servers/workbench-paper/paper.py` renders the four
Spaces from the Board's Markdown on every open, exactly as the Page workbench
does. The 0.1.0 `console/` prototype (a static `data.js` rebuilt by hand, one
paper only) is retired and is never read.

## 🧩 The four Workbench obligations

### 📦 Storage

Paper Workbench reads the Paper Board and its owned projections; it does not mint
a second authority store:

```text
Paper-<Slug>/
├── board.md                         Board identity and Paper links
├── A1-Story/
│   ├── Story00-ideation/            candidate Idea records         → Ideation Space
│   └── StoryA-<desk>-<idea>/        one prospective Story blueprint → Story Space, Sections order
├── Ba-<desk>-Main/                  manuscript Section Pages        → Sections › Main
├── Bb-<desk>-Appendix/              supporting Section Pages        → Sections › Appendix
├── Bc-<desk>-Round/                 feedback and response Pages     → Delivery › Rounds
└── delivery/                        generated whole-paper projection → Delivery › LaTeX, Word
```

**Markdown is the only truth source (JL 260918).** The route is Markdown →
HTML on every GET: every word a Space shows is read from a `.md` file of the
paper, the task home, or the discovery home at that moment, so a Markdown edit
is live on reload and the HTML is never an input to anything. The route also reads authored configuration (`paper-build.toml`,
`discovery.yaml`) and generated receipts (`delivery/build-manifest.json`,
Run `runtime.yaml`, and pair manifests). Config stays with its owner; receipts
are shown, never edited through this presentation layer.

The screen does not say where it read from (JL 260927: "as concise as
possible"); this file and the drawing's "What each Space reads" table do.
Page rendering copy lives in `servers/workbench-paper/paper.py`; drawer
registration and its hint live in
`servers/workbench-paper/assets/js/10-drawer/09-workbench-paper.js`.

`board.md`, Story00, StoryA, Section Pages, Round Pages, delivery receipts,
and owner-native Run records remain authoritative. The Workbench stores nothing:
no `console/`, no `data.js`, no Links key. A Board opts in with one line in
board.md, `dialect: paper`, which `page_board.py` exposes as
`data-board-dialect="paper"` for the drawer registration.

### 🖼 Surface

The Paper Workbench is a Board-level right-pane Workbench. The Board shell owns the
Workbench tab, close behavior, persistence, and iframe. The Paper surface uses the
Page workbench's grammar: Space buttons on top, then the Space's tabs, then its
views, the content on the left and its Runs panel on the right at every width
(the same `runs_panel.py` markup, a panel folds to a strip). Nothing on screen
explains itself: no source lines, counts, hints, crumbs or copy-to-chat chips
(JL 260927).

Reading rules (JL 260918): base type 16px; label/value rows are a two-column
table with cell edges and a shaded label cell, never text nested in text; every
table has cell edges; long prose is set one sentence per line, for display only.
No type under 12px, inside the Runs panel too; a closed card shows its whole
headline (never an ellipsis on a claim or an idea). Checked by
`skills/board/haipipe-board/tests/audit_paper_views.py`, which drives all
sixteen routes in real Chrome at 1360px and 2000px: no page overflow, no pane
leaking, nothing past the right edge, a Runs panel beside every view.

The four Spaces, in the order the paper moves:

```text
Ideation Space    candidate Ideas and their admission
Story Space       the one prospective Story: Spine, High-level logic + Low-level work
Sections Space    every Section in compile order, joined to its Section Page
Delivery Space    the manuscript delivery/ holds, its checks, and the review rounds
```

`Space` is the reader-facing word for `Workspace`. They are the same surface
concept. A physical folder is not automatically a visible Space, and a Space
does not create a new folder.

### ✍️ Writer

The Paper Workbench is a read-only projection. It reads Paper sources on each
open and routes actions to the owner that is allowed to write them.

**Its only engagement is the Runs panel.** Each Space lists the run types its
tab or view owns, from `haipipe-paper-workflow/ref/run-cards.md` (`🔘 BUTTON`
and `💬 PROMPT` lines). Selecting an idea, question, claim, C7/C6 row, Section
or round narrows the panel to that target. A run shows its prompt (Copy), its
process and its results; Rerun and `+ New Run` copy a prompt the person runs in
a Claude or Codex session, which records who started it. Clicking never sends,
starts, allocates, or writes; the page makes no request of its own.

| Surface | Authority / writer | Runs panel |
|---|---|---|
| Ideation | `haipipe-ideation` / `haipipe-paper-ideation` | Idea review (`ridea`) · Generate ideas · Test idea |
| Story | `haipipe-paper-story` and the Story Page | Story revise (the Story's `rp-`) · Claim review (`rclaim`) · Task review (`rtask`) · Supporting runs |
| Sections | each Section Page, through its own Page workbench | Narrative review (`rnarra`) · the Section's Draft, Evidence and Delivery runs |
| Delivery | `haipipe-paper-assemble` / `haipipe-paper-round` | Build (the last `build-manifest.json`) · Check · Response |

Run names are the full names the Page workbench uses: `rclaim-01_…` shows as
`run-claim-01`, `ridea` as `run-idea`, `rtask` as `run-task`, `rnarra` as
`run-narrative`; the last build shows as `run-compile-<yymmdd>`.

### 🚧 Boundary

The Paper Workbench coordinates the Paper Board; it does not become the owner of
Page prose, Evidence Results, Discovery records, Task configurations, or
delivery wording. Board discovery must continue to treat Workbench implementation
files as non-Page material. No Paper Workbench view may silently copy an
authority record just to make its table easier to render.

## 🗂 Spaces, tabs and views

Each Space answers one operational question. Its tabs and views are views over
the same records, not new lifecycle stages. Opening a card or clicking a row
selects it for the Space's Runs panel; a tab change clears the selection.

### Ideation Space · "Which Idea should continue?"

One collapsed Idea Card per idea (the shape of the Page's Evidence cards). The
card LEADS with the Idea's Research Question (the `**Research Question**` field
of its Idea division), so a reader meets the question first; the title is the
subline. Without one, the title leads. Opening it shows the Idea's fields in
page order, the bound Evidence Items with their Verified tick, the comparison
fields, and last a collapsed `Writing plan` holding the plan's Bullets: they
say what the Idea division will say, never what the idea is. Source: the page's
Ideas (ranked) table when Content carries one, else the plan's
`Idea <n>: <research question>` divisions.

Admission (G0) is on the card: its verdict, and where the idea went. Position in
the ranking is an attention aid; `idea_id` is the stable identity, and the
Workbench never creates a second admission decision.

### Story Space · "What is this Paper saying and doing?"

```text
Spine       the Story's C1 Identity, C2 Pitch and C4 Stakes as label/value rows;
            each division opens on the Story page (Open ↗)
High-level logic + Low-level work  (`#story/logic-work`)
            one tree, split down the middle (JL 260929): one block per research
            question, the question across the top; left, its Hypotheses,
            Potential claims and Potential contributions; right, its Potential
            work: Foundation (shared, folded), then This question. Last, "Not
            under a question"
```

```text
▾ Question 1  Do model size and data size contribute symmetrically …?
  HYPOTHESES                                      │ POTENTIAL WORK
   Hypothesis 1a  Capacity saturates: past a      │ Foundation
                  modest size, a bigger model …🔨 │  › Data        Which CGM readings train the models?
   Hypothesis 1b  Data keeps paying: more …    🔨 │  › Training    Can the full model grid be trained?
  POTENTIAL CLAIMS                                │  › Evaluation  How well does each trained model do?
   Claim 1a  More capacity stops helping: …       │ This question
             from Hypothesis 1a                   │  Results  Fitted as one law, what do all the models' scores say?
  POTENTIAL CONTRIBUTIONS                         │           for Hypotheses 1a and 1b · also for Questions 2, 3, 4 and 5
   Patients, not parameters: …                    │    tasks/  b04 scaling_law_analysis
             rests on Claims 1a and 1b            │              j01 collect_and_fit
                                                  │                t01 collect_scaling_data  ▸ 3 runs
```

Where each line comes from (haipipe-paper-story 0.13.0): the question block
(`#### 3.N · Question N · RQn`) and its four groups, items coded 1a, 1b …:
**Hypotheses** (`- **1a** · Name: sentence · tested by E1`), **Potential claims**
(`- **1a** · C1 · from 1a · Name: sentence`; the C1 alias is not shown), **Potential
contributions** (`- rests on 1a, 1b · Name: sentence`), **Potential work** (`- **T1** · for
1a, 1b`, optionally followed by addresses that narrow a row to this question's folders).
Each hypothesis, claim and contribution puts its pill (and a hypothesis's mark) on
one line and starts its text on the next, the short name before the colon in bold
(JL 260929: "make the text start from the next line after the label"). A work item's words are its §7/§6 row's
`question` cell and its pill the row's `stage` (Data, Training, Evaluation, Results,
Analysis, Figures, or Discovery for a §6 row); work runs top to bottom in that order
(JL 260929: "the work should follow the logics"). §7 rows marked `every question` sit
under Foundation in every block, folded, "shared by all 5 questions" (JL 260929: "the
question level foundation work … and it can be shared"). A row another question also
lists on the same folders says "also for Questions 2, 3, 4 and 5"; a row narrowed to
other folders there (each question's own figures) does not. A hypothesis's mark comes
from the §5 rows it names (✅ established, 🔨 provisional, ⬜ absent, ❌ contradicted). A
group with no item says "none yet", or the Story's own `- none: …` reason. A Story that
still writes the RQ table gets one hypothesis per §5 row and its work read from either
end of the §5↔§7 links. `question_blocks()` parses the blocks and `story_tree()` makes
every join.

Nothing sits behind a Details click (JL 260929: "replace it with the plain text"): the
answer state, tests and each claim's Role, Now and If it fails stay in the Story file.
Under each work item: its folders in the Task or Discovery home, one line per level
(`b04` block, `j01` job, `t01` task linked to its page, R as `▸ 3 runs · no receipts`
opening to each run ticket and its receipt state; a Discovery task also says what it
found). Work built in another project says "built outside tasks/" with its path; a row
with no folder says "no folder yet".

Look (JL 260929: "你觉得你还可以再怎么去美化一下它"): each group label is a colored band
(no left stripe, JL 260930): Hypotheses and This question's work blue, Potential claims green,
Potential contributions orange, Foundation work gray (its band says "shared by all 5
questions"). Each question's header row has a light background. Every work item folds,
closed by default (JL 260929: "右边那些 results 也是可以 click 的，也是可以 collapse 的"); its
closed line still shows its stage, its question, "for Hypotheses 1a and 1b", "also for
Questions …" and its size ("4 tasks · 20 runs", or "no folder yet").

Questions start closed (JL 260930): the questions alone read as the paper's outline, with nothing else on the closed line (JL 260930: no tally). The closed line is two lines: the "Question N" pill with the block's `**Name**` beside it, then the full question below. board.md `story-current: <Story stem>` limits the tree to that Story (a submitted paper and its redesign are two Stories; the tree shows the one being worked on, with no Story label); without it every Story's questions are drawn. Picking: a click on a closed question opens it and selects it for the Runs panel; on an open, unselected one it selects; on the selected one it closes. A click on a hypothesis selects it, lights the work that tests it and opens it.
Opening a work item selects it; closing it clears the pick. Under 1100px the right half
drops below the left. The only box is the tree's frame.

Task home rules: the Task home is `examples/<Project>/tasks/` (or `task/`, or
board.md `task-home:`), read Block → Job → Task in both folder shapes (a task folder
with its own runs/ results/, or the flat `<job>/{runs,results,scripts}/<task>/`);
runs are the tickets under runs/ and their state is the result's `runtime.yaml`.
Write every C7 address in full, one per job or task
(`Task: b01.j01, b01.j02.`, `b01.j05.t02–t03`): a bare `j02` after a comma is not
an address. The
claim = board.md `blocks: b03 b04 b02.j01` + every address on a C7 row. Address
grammar: lowercase two-digit `bNN[.jNN[.tNN[.rNN]]]` (a row id such as `B2` is
not an address); end the row's design cell with `Task: b03.j02.`, as C6 ends its
scope cell with `Discovery: b01.j04.`. CLAIMED = a block or job shows because
`blocks:` or a C7 address covers it; ADDRESSED = the C7 row names its own
address. Unclaimed jobs are named once, muted, never expanded. Discovery home
(`examples/<Project>/discoveries/`, or `discovery-home:`) is claimed the same way
through `discoveries:` and C6 addresses.

The High-level logic + Low-level work Runs panel lists Claim review (`rclaim`), Task review (`rtask`), Task
runs (haipipe-task) and Discovery runs (haipipe-discovery): the supporting runs this
paper's Evidence Items cite, each under its owner and keyed to the C7 and C6 rows
whose addresses cover them and to every hypothesis, E-row and question above those
rows, so picking a question or a hypothesis shows the runs behind it. Every run type and run names its skill
(`🧩 SKILL` in run-cards.md).
The drawing
`studio/paper-workbench-design.excalidraw` (generated by
`studio/paper-workbench-design.py`) also shows a Delivery › Cover
letter tab (live): it reads `build-manifest.json` `cover_letter`, which
haipipe-paper-assemble's run-delivery-coverletter writes from the submission Round
page's Cover letter division, and shows the letter, its files and its checks.

A board with no Story page says `No Story yet.` in each tab, never an empty pane.
Story Space presents StoryA's blueprint; C6 is the Discovery Roadmap, C7 the Task
Roadmap, C8 the Section Narrative and compile order (shown in Sections Space).
These are Story divisions, not extra Pages or extra Spaces.

### Sections Space · "Where is each Section?"

```text
Table       one row per Section in compile order: number · name · draft version ·
            state word (from the Page's state: line); Open ↗ goes to that Page's
            workbench (/_board/draft). A C8 row with no Section Page reads
            `not set up`
Narrative   one card per C8 row: the reader question leads; open = the row's
            moves, what it must establish and refuse, evidence, display, exit
            state, cut rule, and the Section's session: its Claude session from
            the page's `session:` line (`/haipipe-paper sessions`) and any Codex
            peer paired to that id (one per Section Page, JL 260916, 260928)
Evidence    the hero list: every DISPLAY item on a Main or Appendix page and
            every VALUE item on the Abstract page, each opening its Section's
            Evidence Space
```

Main and Appendix are tabs. Selecting a Section shows its runs: Narrative review
(`rnarra`, on the Story page) and the Section Page's own runs, grouped as Draft,
Evidence and Delivery runs by the Page Space folder that holds them. Evidence
runs are named by the item they serve (`run-value-E25`), as on the Page.

### Delivery Space · "What leaves the Paper?"

```text
LaTeX · Word   Preview   the main PDF in a frame; the main DOCX as a file row
               Artifacts the outputs paper-build.toml names (built · size · written,
                         or ⬜ not built); LaTeX adds the display register and
                         submission assets, Word the returned files under
                         delivery/word-feedback/ (read, never built from)
               Checks    build facts (words, citations, displays, pages ready,
                         submission status), pages changed since the build, G4,
                         the manifest's checks, latexmk and docx results, one row
                         per page (fragment · ready · notes), and every warning
Rounds         one card per Bc-<desk>-Round page (kind, received, due, base
               build, folders, state) and the venue page; the Round page owns
               the dispositions (G5)
```

Delivery reads only what haipipe-paper-assemble wrote and what the pages carry;
it builds nothing on open. The Build button copies the build prompt.

## Workflow, Run Specs and control records

`haipipe-paper-workflow/ref/run-workflow.md` is the canonical Spec list and
compatibility map; `ref/space-mapping.md` names each Run's reader-facing name,
canonical Type and Spec, owner/worker Skills, actor, prerequisites and the
Space that shows it. Both are definition views for readers of this skill; the
screen shows only the Runs panels, whose buttons come from
`haipipe-paper-workflow/ref/run-cards.md`.

Paper judgment Specs are `idea`, `claim`, `obligation`, and `narrative`; shared
native Specs are `support`, `structure`, `write`, `evidence`, and `deliver`;
Paper delivery/response Specs are `compile` and `response`. Selection (I3),
setup, G0–G5, sync and Story/Section routes remain control actions with no Run
Type. A visible row never creates a receipt.

## 🚦 Gates and ownership

The Paper Workbench may display gate state, but the named owner closes the gate:

```text
G0  Ideation → Story       I3 / Paper Ideation handoff      shown on the Idea card
G1  Story → work           Story release of Discovery/Task  shown on C7 / C6 cards
G2  work → Story           accepted Result and interpretation shown on the claim state
G3  Story → Section        human release of one C8 row      shown on the Section row
G4  Section → Compile      Section release and delivery     shown in Delivery › Checks
G5  Round → next route     every concern answered once      shown on the Round card
```

The Workbench must never infer a human approval from a percentage, a folder's
existence, a generated PDF, or a Run-Type row marked `recorded`.

## 🔒 Link and presentation rules

- Paper Workbench links use `/_board/paper` with URL-encoded `path` and `file`.
- Draft links use `/_board/draft` and a concrete Page `file`; the two
  routes are siblings, not aliases.
- A Paper link may start at `file=board.md` and use a hash for a place,
  for example `#story/logic-work` or `#sections/main/narrative`.
- The parent Board URL remains the shell's URL when the Workbench is in the right
  pane; the iframe URL carries the Paper Workbench route, just as the Page's does.
- `Run-Type` is not a synonym for `Space`, `Workspace`, or concrete `Run`.

## ✅ Completion checks

- The skill is discoverable as `haipipe-workbench-paper` and loads the common
  `haipipe-workbench` contract first.
- The Paper Board exposes one `Paper` Workbench entry, not a generic Console
  entry and not a second Draft entry.
- Its direct link has the form
  `/_board/paper?path=<board.md>&file=board.md`, and it answers on any Board
  whose board.md says `dialect: paper` with no other file present.
- Ideation, Story, Sections, and Delivery are the visible Spaces, each with a
  Runs panel on the right; their tabs and views remain views over authority records.
- Every run type comes from `haipipe-paper-workflow/ref/run-cards.md`; no button
  sends, starts or writes anything.
- StoryA remains the sole prospective Paper blueprint, and Section Pages keep
  their own Page lifecycle.
- The route reads no `console/`, `data.js`, or other per-paper projection;
  `tests/test_paper_workbench.py` keeps that tooth, and `audit_paper_views.py`
  flags no view at 1360px and 2000px.
