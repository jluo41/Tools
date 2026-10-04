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
  version: "0.26.0"
  last_updated: "2026-10-03"
---

# /haipipe-workbench-paper · the Paper-level work console

**LOAD `haipipe-workbench` FIRST.** It defines the common Workbench law: STORAGE,
SURFACE, WRITER, and BOUNDARY. This skill defines the Paper-level delta. It is
the Paper counterpart to `haipipe-workbench-page`:

That skill is written for Page-level workbenches. For this Board-level workbench read
it for the four duties only, then return here: the route, the Spaces, the
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

When returning a link for a Paper Board, return the short address by default,
as every workbench does (`servers/README.md` "Adding a workbench", rule 4; JL 261003):

```text
<DOMAIN>/w/<paper-board-folder>                 the Paper Workbench
<DOMAIN>/w/<paper-board-folder>/<Section stem>  one Section's Page workbench
```

The server redirects it to the full route
`/_board/paper?path=<URL-encoded Paper>/board.md&file=board.md` (or
`/_board/draft?path=…&file=…` for a Section) and composes `path` and `file`
itself; the full route still answers and stays the form for scripts and tests.
`<DOMAIN>` is the origin the reader uses (the `--public-url` the board server was
started with; find the listening port before quoting a link, and never hand a
remote reader `127.0.0.1`). Follow the redirect and read one real value off the
response before returning the link, and keep it in one Markdown link. Add a hash
only when the reader asks for a particular place; the hash rides on the
redirected page. The route is `#<space>[/<tab>][/<view>]`:

```text
ideation
story      spine · roadmap-draw · logic-work · related
sections   main · appendix          ×  table · narrative · evidence
delivery   latex · word · rounds    ×  preview · artifacts · checks   (rounds has no views)
```

The pre-260927 routes (`#setup/…`, `#run/…`, `#story/claims`, `#story/tasks`,
`#delivery/manuscript`, …) still land on the view that now holds their content.

There is no per-paper file behind the route: `servers/workbench-paper/paper.py` renders the four
Spaces from the Board's Markdown on every open, exactly as the Page workbench
does. The 0.1.0 `console/` prototype (a static `data.js` rebuilt by hand, one
paper only) is retired and is never read.

## 🧩 The four Workbench duties

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
├── studio/                          Story drawings and their scripts → Story › RoadMap Draw
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

**Shared shell (JL 261003).** Above the Spaces the page wears the shell every
workbench shares (`servers/README.md` "Adding a workbench";
`_host/tests/test_workbench_conformance.py`): the title,
one band (desk · Story version · N questions · N Sections · built or not built yet,
`paper._shell_band`), then the Space row with the shared Guide first and plain names
(Ideation · Story · Sections · Delivery). Each Space's tabs, Views and content sit in
one box; its Runs panel starts folded to the strip and opens on a click. The colors
and tab sizes are the Insight workbench's, kept once in `space_views.SPACE_CSS`; the
Spine shows each division by name, never its C-code. Guide reads the `paper` entry of
`workbench-shared/guide_families.py`: `description`, the Workbench Table
`ref/workbench-table.md` (each working row is one `run-cards.md` button; its 🤖 AGENT,
🧩 SKILL and ✍️ SIGNS lines agree, `table-workbench --check --cards`), the papers
`ref/paper-papers.md` (`table-papers`),
Method's page `ref/paper-method.md` with its cards in `ref/methods/` and its editable
methods canvas `ref/paper-methods.excalidraw` (the canvas is the source), and RoadMap Draw's **Workbench design**,
`servers/workbench-paper/studio/paper-workbench-design.excalidraw`, written by
`paper-workbench-design.py` (Part 0 the shared shell, then each Space's sub-spaces, runs
and skills, each Space as shown, and what each reads; rerun it, never edit the scene).

Reading rules (JL 260918): base type 16px; label/value rows are a two-column
table with cell edges and a shaded label cell, never text nested in text; every
table has cell edges; long prose is set one sentence per line, for display only.
No type under 12px, inside the Runs panel too; a closed card shows its whole
headline (never an ellipsis on a claim or an idea). Checked by
`skills/board/haipipe-board/tests/audit_paper_views.py`, which drives all
nineteen routes in real Chrome at 1360px and 2000px: no page overflow, no pane
leaking, nothing past the right edge, a Runs panel beside every view.

The four Spaces, in the order the paper moves:

```text
Ideation Space    candidate Ideas and their admission
Story Space       the one prospective Story: Spine, RoadMap Draw, High-level logic +
                  Low-level work, Related Papers
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
and `💬 PROMPT` lines). Selecting an idea, question, claim, Task or Discovery row, Section
or round narrows the panel to that target. A run shows its prompt (Copy), its
process and its results; Rerun and `+ New Run` copy a prompt the person runs in
a Claude or Codex session, which records who started it. Clicking never sends,
starts, allocates, or writes; the page makes no request of its own.

| Surface | Authority / writer | Runs panel |
|---|---|---|
| Ideation | `haipipe-ideation` / `haipipe-paper-ideation` | Idea review (`run-paper-idea-…`) · Generate ideas · Test idea |
| Story | `haipipe-paper-story` and the Story Page | Story revise (the Story's Page Runs) · Claim review (`run-paper-claim-…`) · Task review (`run-paper-task-…`) · Supporting runs |
| Sections | each Section Page, through its own Page workbench | Narrative review (`run-paper-narrative-…`) · the Section's Draft, Evidence and Delivery runs |
| Delivery | `haipipe-paper-assemble` / `haipipe-paper-round` | Build (the last `build-manifest.json`) · Check · Response |

Run names are full names: Paper judgment Runs are `run-paper-idea-…`,
`run-paper-claim-…`, `run-paper-task-…` and `run-paper-narrative-…`; Page Runs are
`run-<kind>-<MMDD>-<slug>`; the last build shows as `run-compile-<yymmdd>`.

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
Spine       the Story's §1 Identity, §2 Pitch and §4 Stakes as label/value rows;
            each division opens on the Story page (Open ↗)
RoadMap Draw  (`#story/roadmap-draw`)
            the paper's drawings in studio/, editable; a script-written drawing
            is redrawn by the Redraw card
High-level logic + Low-level work  (`#story/logic-work`)
            one tree, split down the middle (JL 260929): one block per research
            question, the question across the top; left, its hypotheses,
            potential claims and potential contributions, each item under its
            own pill, no group labels; middle, its work: the foundation every
            question shares, then this question's own; right, its Report
            (JL 261003): `reports/qNN_<topic>/` beside `studio/`, its state
            (Answered · Partial · Open), its answer in a line, Open ↗, or "No
            report yet". Three columns at every width. A hypothesis shows ✅ only
            when its question's Report says answered, else 📝 (stated, not yet
            shown). Last, "Not under a question"
Related Papers  (`#story/related`)
            one card per §5.3 related paper, the target venue first; open a
            card to read its PDF
```

```text
▾ Question 1  Model or data?
  We make the model bigger, or give it more training data, and see which one lowers the forecast error.
  Hypothesis 1a                              🔨 │ › Data        Which training data?
  Capacity saturates: past a modest size, …     │ › Training    Train the whole grid?
  Hypothesis 1b                              🔨 │ › Evaluation  How good is each model?
  Data keeps paying: more training data …       │
                                                │ › Results     One law for all?
  Claim 1a                                      │   We fit one scaling law to every model's score …
  More capacity stops helping: …                │   for Hypotheses 1a and 1b · also for Questions 2, 3, 4 and 5
  from Hypothesis 1a                            │     tasks/  b04 scaling_law_analysis
                                                │               j01 collect_and_fit
  Contribution 1a                               │                 t01 collect_scaling_data  ▸ 3 runs
  Patients, not parameters: …                   │
  rests on Claims 1a and 1b                     │
```

Where each line comes from (haipipe-paper-story 0.13.0): the question block
(`#### 3.N · Question N · RQn`) and its four groups, items coded 1a, 1b … (a Question 0
that sets the tasks opens with a **Tasks** group, `- Pretraining · Name: sentence`, drawn
first with its kind as the pill, and shows only the groups it fills; JL 260930):
**Hypotheses** (`- **1a** · Name: sentence · tested by E1`), **Potential claims**
(`- **1a** · C1 · from 1a · Name: sentence`; the C1 alias is not shown), **Potential
contributions** (`- rests on 1a, 1b · Name: sentence`), **Potential work** (`- **T1** · for
1a, 1b`, optionally followed by addresses that narrow a row to this question's folders).
Each hypothesis, claim and contribution puts its pill (and a hypothesis's mark) on
one line and starts its text on the next, the short name before the colon in bold
(JL 260929: "make the text start from the next line after the label"). A work item reads like a question: its pill the row's
`stage` (Data, Training, Evaluation, Results, Analysis, Figures, or Discovery for a §6
row) with the row's `name` cell beside it, and the row's `question` cell, one plain
sentence, on the line below (JL 260930: "the Label, + Short names, and a new line to
explain what it is"); a row with no `name` cell shows its `question` beside the pill; work runs top to bottom in that order
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
(`b04` block, `j01` job, `t01` task as plain text (JL 260930: its link only opened the raw
Task Markdown), R as `▸ 3 runs · no receipts`
on the task line, opening to each run ticket and its receipt state below it, one level in; a Discovery task also says what it
found). Work built in another project says "built outside tasks/" with its path; a row
with no folder says "no folder yet".

A run opens its results (JL 260930: "for a run, how could we have a popout window to
show the results of that run's results"). Each run line under R is a link; a click opens
a pop-out over the page (Esc or a click outside closes it; "Open in its own tab ↗", or a
Cmd-click, keeps it). A Task run's card in the Runs panel has the same "Open the results ↗".
The pop-out is `GET /_board/run-result?task=<Task folder>&run=<run stem>`
(`render_run_result` in `paper.py`): the run's receipt (`runtime.yaml`), then its
summaries (Markdown with its tables drawn; a `.md` with no Markdown mark, and `.txt`, as written), figures, tables (the first 50 rows of
each `.csv`/`.tsv`) and every other file, each opening raw, with links to the run script,
the executed notebook (`notebooks/<run>.ipynb`) and the Task page. The files are the run's
own `results/<run>/`; in a Task that keeps one shared `results/`, the files named after the
run (`run_6a2_f01.sh` → `figures/6a2_f01_…png`), else those whose path holds every word of
its name (`run_fit_forecast.sh` → `fits_forecast/…`), else all of `results/`, and the page
says which (`run_files`). It reads only inside the server root. The page runs nothing:
Rerun still copies a prompt for a Claude or Codex session.

Look (JL 260929: "你觉得你还可以再怎么去美化一下它"): no group labels (JL 260930:
"Hypotheses <--- could we just remove this … of no information", and the same for
Foundation work, "shared by all 7 questions" and This question's work). Every item's pill
names its kind, a contribution's too (JL 260930: "we can have the contribution label as
well, just as the claim and hypothesis"): Hypothesis 1a, Claim 1a, Contribution 1a, a
contribution coded by its order in the question. A gap separates the groups; an empty
group shows its kind's pill over "none yet" or the Story's own `- none: …` reason. Only a
Question 0's Tasks keeps its label, because its pills name the task alone. On the right,
the foundation every question shares comes first, this question's own work after a gap.
Each question's header row has a light background. A pick draws nothing
(JL 260930, of the blue left bar: "I don't want this as well"; a fill was turned down
before): an opened question or work item shows the pick by being open, and the Runs
panel names it. Every work item folds,
closed by default (JL 260929: "右边那些 results 也是可以 click 的，也是可以 collapse 的"); its
closed line still shows its stage and short name, the plain sentence, "for Hypotheses
1a and 1b", "also for Questions …" and its size ("4 tasks · 20 runs", or "no folder yet").

Questions start closed (JL 260930): the questions alone read as the paper's outline, with nothing else on the closed line (JL 260930: no tally). The closed line is two lines: the "Question N" pill with the block's `**Name**` beside it, then the plain question below. board.md `story-current: <Story stem>` limits the tree to that Story (a submitted paper and its redesign are two Stories; the tree shows the one being worked on, with no Story label); without it every Story's questions are drawn. Picking: a click on a closed question opens it and selects it for the Runs panel; on an open, unselected one it selects; on the selected one it closes. A click on a hypothesis selects it, lights the work that tests it and opens it.
Opening a work item selects it; closing it clears the pick. Under 1100px the right half
drops below the left. The only box is the tree's frame.

**RoadMap Draw** (`#story/roadmap-draw`, between Spine and the logic view; JL 260930 named it:
"a view … to show the excalidraw draw which will be saved here: studio"): the paper's own
Excalidraw canvas, full width and editable, on a drawing in `<paper>/studio/`: the
Story's own `<Story stem>.excalidraw` (the Story board.md `story-current:` names, else the
first `Story<X>`) when it exists, else the first drawing there, else the Story's own,
new. The canvas is the server's self-hosted Excalidraw
(`/_excalidraw/?board=<path>&edit=1`), loaded when the tab shows; every stroke saves
through `/_board/excalidraw-save`. The server writes the empty file the first time the
canvas opens (`mint_board_scene` in `servers/workbench-shared/xcal.py`: a plain scene,
only in a `studio/` folder beside a `board.md`); rendering the page writes nothing. With more
than one `.excalidraw` in `studio/`, each is a button above the canvas, the Story's own first;
"Open full screen ↗" opens the same canvas in its own tab. One tab holds the pen: a second
tab on the same drawing opens read-only. Opening a drawing never saves it; the first
stroke does, so a drawing a script wrote stays as its script wrote it until someone draws.

**Related Papers** (`#story/related`, JL 260930: "each paper to be a card that I can
read the original pdf"): the papers this study stands beside, one card each. The
paper's target venue comes first, under "At <venue>", and other venues follow under
"Other venues" (JL 260930: "this is not limited to NMI"); inside each, the cards sit in
bands: Closest to this paper, For one research question, Background, Cautions and
framing. The rows are the Story's §5.3 P-board (haipipe-paper-story 0.14.0); each names
the Discovery Paper Run that holds the paper, and the card reads that Run's Result
folder: `runtime.yaml` (title, authors, venue), `abstract.md`, `source-access.json`
(the publisher link) and `paper.pdf`. The venue is the H1 of board.md's `venue-page`, before its colon; a card
sits under it when its Run's venue string starts with that name.

An open card (JL 261002: "add a table like its High Logic and Low Work") shows, in order:
**Why we keep it**, from the P-board's `keep` cell (else its `why it matters` line), with
one chip per question from `bears on` (supports, limits, contradicts, method, frames);
then **Their logic | Their work**, the paper's question, findings and contribution
beside its data and method, read from the Run's `logic-work.yaml` and headed with what
the reading was made from; then the links (the PDF, the publisher, the Paper Run, and
every other PDF in the Result, such as a supplement or an earlier version); then the
abstract, folded; then the article PDF. A Run without `logic-work.yaml` shows no table.

```text
▾ <paper title>
  <First author> et al. · <year> · <venue>                         RQ1 📄
  ┌ WHY WE KEEP IT ───────────────────────────────────────────────────────┐
  │ <keep cell>                                                           │
  │ [RQ1 limits] [RQ2 supports]                                           │
  └───────────────────────────────────────────────────────────────────────┘
  THEIR LOGIC                          │ THEIR WORK · READ FROM THE PDF
  Question  <what it asks>             │ Data      <archive, sample, scale>
  Finding 1 <with its number>          │ Method 1  <first step>
  Finding 2 …                          │ Method 2  …
  Contribution <what it adds>          │
  Open the PDF ↗ · Publisher page ↗ · Paper Run ↗ · Supplementary information ↗
  ▸ Abstract
  [ the article PDF ]
```

```text
45 PAPERS · 38 WITH A PDF
At Nature Machine Intelligence  15
CLOSEST TO THIS PAPER  3
┌──────────────────────────────────────────────────────────────────────┐
│ ▸ Cardiac health assessment across scenarios and devices using a …   │
│   Gu et al. · 2026 · Nature Machine Intelligence              RQ1 📄 │
├──────────────────────────────────────────────────────────────────────┤
│ ▸ Neural scaling of deep chemical models                             │
│   Frey et al. · 2023 · Nature Machine Intelligence            All 📄 │
└──────────────────────────────────────────────────────────────────────┘
Other venues  30
```

Closed, a card is two plain lines (JL 260930: "too messy, not readable … no need to show
all the details in the card front face"): the title, then first author, year and short
venue, with the question and a 📄 when the PDF is inside. A band's cards sit as rows in
one box. Open, it shows why the paper matters (the P row's line), "Open the PDF in a new
tab ↗", "Publisher page ↗", "Paper Run ↗", the abstract folded under "Abstract", and the
PDF itself, or "No free full text" when the Run has none. There is no facts line (the P id,
reading depth, citing Sections, venue string; JL 260930: "not relevant and could be
removed"); those stay in the Story row and the Paper Run. The PDF frame carries `data-pdf`, not `data-src`, so the page's `lazy()` loader leaves it
alone and it loads only when its card opens. A row whose Run is missing says "no Paper Run
at <address>". `related_html()` draws the tab; `_paper_card()` one card;
`paper_card_data()` reads one Run.

Task home rules: the Task home is `examples/<Project>/tasks/` (or `task/`, or
board.md `task-home:`), read Block → Job → Task in both folder shapes (a task folder
with its own runs/ results/, or the flat `<job>/{runs,results,scripts}/<task>/`);
runs are the tickets under runs/ and their state is the result's `runtime.yaml`.
Write every Task Roadmap address in full, one per job or task
(`Task: b01.j01, b01.j02.`, `b01.j05.t02–t03`): a bare `j02` after a comma is not
an address. The
claim = board.md `blocks: b03 b04 b02.j01` + every address on a Task Roadmap row. Address
grammar: lowercase two-digit `bNN[.jNN[.tNN[.rNN]]]` (a row id such as `B2` is
not an address); end the row's design cell with `Task: b03.j02.`, as a Discovery Roadmap row ends its
scope cell with `Discovery: b01.j04.`. CLAIMED = a block or job shows because
`blocks:` or a Task Roadmap address covers it; ADDRESSED = the row names its own
address. Unclaimed jobs are named once, muted, never expanded. Discovery home
(`examples/<Project>/discoveries/`, or `discovery-home:`) is claimed the same way
through `discoveries:` and Discovery Roadmap addresses.

The High-level logic + Low-level work Runs panel lists Claim review (`run-paper-claim-…`), Task review (`run-paper-task-…`), Task
runs (haipipe-task) and Discovery runs (haipipe-discovery): the supporting runs this
paper's Evidence Items cite, each under its owner and keyed to the Task and Discovery Roadmap rows
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
Story Space presents StoryA's blueprint; §6 is the Discovery Roadmap, §7 the Task
Roadmap, §8 the Section Narrative and compile order (shown in Sections Space).
These are Story divisions, not extra Pages or extra Spaces.

### Sections Space · "Where is each Section?"

```text
Table       one row per Section in compile order: number · name · draft version ·
            state word (from the Page's state: line); Open ↗ goes to that Page's
            workbench (/_board/draft). A Section Narrative row with no Section
            Page reads `not set up`
Narrative   one card per Section Narrative row: the reader question leads;
            open = the row's
            moves, what it must establish and refuse, evidence, display, exit
            state, cut rule, and the Section's session: its Claude session from
            the page's `session:` line (`/haipipe-paper sessions`) and any Codex
            peer paired to that id (one per Section Page, JL 260916, 260928)
Evidence    the hero list: every DISPLAY item on a Main or Appendix page and
            every VALUE item on the Abstract page, each opening its Section's
            Evidence Space
```

Main and Appendix are tabs. Selecting a Section shows its runs: Narrative review
(`run-paper-narrative-…`, on the Story page) and the Section Page's own runs, grouped as Draft,
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

`haipipe-paper-workflow/ref/run-workflow.md` is the one Spec list and
compatibility map; `ref/space-mapping.md` names each Run's reader-facing name,
Run Type and Spec, owner/worker Skills, actor, prerequisites and the
Space that shows it. Both are definition views for readers of this skill; the
screen shows only the Runs panels, whose buttons come from
`haipipe-paper-workflow/ref/run-cards.md`.

Paper judgment Specs are `idea`, `claim`, `task`, and `narrative`; shared
native Specs are `support`, `structure`, `write`, `evidence`, and `deliver`;
Paper delivery/response Specs are `compile` and `response`. Selection (I3),
setup, G0–G5, sync and Story/Section routes remain control actions with no Run
Type. A visible row never creates a receipt.

## 🚦 Gates and ownership

The Paper Workbench may display gate state, but the named owner closes the gate:

```text
G0  Ideation → Story       I3 / Paper Ideation handoff      shown on the Idea card
G1  Story → work           Story release of Discovery/Task  shown on the work rows
G2  work → Story           accepted Result and interpretation shown on the claim state
G3  Story → Section        human release of one §8 row      shown on the Section row
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
- Its link is the short `/w/<paper-board-folder>`, which redirects to
  `/_board/paper?path=<board.md>&file=board.md`; that route answers on any Board
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
