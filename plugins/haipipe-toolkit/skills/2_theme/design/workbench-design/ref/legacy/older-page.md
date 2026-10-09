The older Design Folder page and board (design.py, designboard.py)
==================================================================

(Moved here from workbench-design/SKILL.md on 261007, word for word, when the design theme moved onto the ladder.)
An older board (`B00_DesignBoard-<name>/`, `2-Design[-M<NN>]/Design-NN-<slug>/`) keeps this workbench until it is
carried over: `/_board/design` (the page) and `/_board/design-board` (the board). Its board grain is
`../design-board.md`; its Space ↔ file maps are `../space-mapping.md` (page) and `design-board-space-mapping.md`
(board). New work never reads this layout.

## The older page: one Design Folder in three Spaces

**LOAD `workbench` FIRST.** It owns the shared Page Workbench contract. This
skill owns the Design category's delta: the Design Item as the row of the
page, the three page Spaces that show it (Design Goal, Design, Delivery) and
the two board Spaces, the contract files each Space reads, and where a user
action is routed.

## Two grains, one workbench

This skill is the **Page level**: one Design Folder. The **Board level**,
`workbench-design/ref/design-board.md` (`/_board/design-board`), stacks every folder's
snapshot one grain up in one working Space, Design Tasks (every design task with its
designs, folder and state), beside the shared Guide. Each task row links down to its
page here; this page's header links back up. Nothing is stored twice.

A board that compares design methods holds one group per method, `2-Design-M<NN>-<slug>/`,
each with a frozen `method.md` (See input · Conduct process · Check output) and the Brief's
tasks as Design Folders, `Design-01` the same task under every method
(`haipipe-design/ref/legacy/method-folders.md`). A page under a method shows the method's title in its
header band; a board with only `2-Design/` reads as before.

Folder names say the goal, `Design-NN-<audience>-<job>-<venue>`: each part is
the first three content words of that Brief cell, filler words (with, within,
a, the, of, for, or, under, …) dropped:
`Design-01-all-patients-prescription-review-sms`. A renamed folder keeps
its `Design-NN` number, and an old link finds it by that number.

The Page title is one plain phrase from the same line, `<job> <venue> for <who>`
(`Prescription review SMS for all patients`; venue words: sms → SMS, ui-card →
app card), and the Brief's `audience` cell is written in plain words (`all
patients`, never `full SMSR2 population, unconditioned`).

Short links, for typing or pasting: `/_board/design-board` opens the server's
only DesignBoard (with several it lists them), `?board=B00` names one by the
unique start of its folder name, and `/_board/design?folder=<Design-NN>[&space=…]`
redirects to this folder's full `path=` and `file=` link (`Design-1` reads as
`Design-01`). The folder finds its board when only one board holds it; add
`&board=B00` when several do. When several boards hold it and no board is
named, the link answers 404 with a page that lists each board holding the
folder, one link each; it never guesses, because two boards' `Design-01` are
unrelated designs. A folder no board holds gets the list of boards. Under method folders,
`?folder=M02/Design-01` names one method's folder (a bare `Design-01` held by several methods
answers with a page listing them), and `/w/<board>/m02-design-01` opens that method's page.

## Plain words on the surface (JL 260916)

Every word a reader sees must be understood at first glance. `Space` is the
only word for a workbench surface. The Runs list shows **Commission, Generate, Verify** under their real ids.
Delivery is the ready projection. A line that waits on a person says **you**,
never the reader's name (JL 260921: a name there reads as the person who signed
the last record, a different fact). Explain the
work in plain language. Run guidance also names the canonical Run Type and
owner/worker Skills so the reader can identify the exact operation. Other
contract words use these reader-facing translations:

| in the files | on the screen |
|---|---|
| `roster` | the Brief, a line of the Brief |
| `handoff` (a signed Wisdom page) | signed insight |
| Ticket | run record |
| candidate | draft |
| `check_unit` | records check |
| `intent` / `move` | goal |
| `stance follow · basis evidence-informed` | follows the evidence · built on evidence; `mode` stays in the files |
| `FW01` (an insight page's file id) | `full-W01 · Send salience`: its label and its title |
| `R1` (a Brief line id) | the task's full name, `<job> <venue> for <who>` |

So none of these reach the screen: roster, handoff, Ticket, candidate, DU,
or a Brief line id such as `R1`. An insight page is always shown by its
on-screen label and its title (`full-W01 · Send salience`,
`young-male-I02 · …`), never by its file id `FW01`; the file keeps `FW01`
(JL 260918).

Ids are `ITEM01`, `ITEM02` (never `DI`, which reads as the Insight workbench's
Data → Information). Runs are named `run-design-<step>-<MMDD>-<slug>`: `run-design-generate-0918-design-1`. The
`sequence:` number counts across the whole folder, not per item, so ITEM02's first
Run may be `rd05`.

## The Spaces and the Runs panel (0.14.0)

JL 261001: one Design Folder is one design task, so its designs share one aim.
JL 261002: one Design page is one design task done by one design method, returning N
designs; comparing methods takes one page per method on the same task.

```text
🎨 Design · page level (one design task)
├── Design Task         the design task, once, in four views: Aim · Requirements · Resources · Leave out
├── Design Item        the task block, the element matrix, then one card per design:
│                       Design · Rationale · Evaluation;
│                       "Insight pages · N" and "Runs · N" fold inside each card
└── Delivery           every design that passed Verify, word for word · this task's csv

🎨 Design · board level (every design task)
├── Guide (shared)          Description · Method (six steps, then one page: the theory, the
│                           method cards, the methods drawing) · RoadMap Draw (skills, method, workbench, folders in one
│                           drawing) · Related Paper (the papers, PDF and all)
└── Design Tasks Space      one row per design task · the rules every task keeps · the board csv
```

- Page level: **Design Goal · Design · Delivery** (input, process, output). The URL keys
  are `goal`, `design`, `delivery`. Old `space=insight` and `space=run` links open Design.
- Board level: **Design Tasks** (`tasks`), beside the shared **Guide** (JL 261002: "follow
  the design here, workbench"). The theory of design explains the family, so it is
  Guide › Method; an old `space=theory|methods|studio` link forwards to `guide=method`,
  and `space=papers` to `guide=related-paper`. Old `space=goal|design|delivery|run` board links open Design Tasks.
- Guide is mounted at both levels by `workbench`; the Design family's entry in
  `servers/workbench/guide_families.py` gives its skills, method steps, Spaces,
  folders, a `description`, and three framed pages (`explain`): Guide › Method gives six steps,
  then frames one page (`/_board/design-board?embed=theory&view=method&views=method`):
  the methods drawing first, then `servers/workbench-design/guide/method.md`, built on the six steps (the steps,
  steps 2, 3, 4 and 6 in depth, why it works, the Reference folded), Guide › Related Paper frames its Papers view
  alone (`views=papers`), and Guide › RoadMap Draw frames the one drawing of skills,
  method, workbench and folders `Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s02-workbench-ui/design-workbench-ui.excalidraw` (generated
  by `design-workbench-ui.py` beside it).
- Every Space at both levels has the **Runs panel** on the right (see below).
- The UI design drawing is `Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s02-workbench-ui/design-workbench-ui.excalidraw`: the design
  theme's drawings, their builders and their predecessors live in its Block's studio, one topic each
  (261007: the servers hold code only).
- The Workbench Table (Space · View · Run type · Agent · Skill · Person signs) is
  `ref/workbench-table.md`, in the `table-workbench` shape. It is the target the views,
  the run-cards file and the small design skills follow.

The header is one line, `Page level · <folder> · ↑ Board level`. A red line is added
only when something blocks the work: the folder is legacy, its insight inputs are
blocked, or the server cannot read run records. Nothing else lives in the header.

**Design Goal Space**

The Space is the **design input** (Theory of Design §2). Its heading is "The design
task": the ask in one sentence, then five blocks. Its owner skill is
`haipipe-design-goal`.

1. **Aim**: Objective, Patient task, Context, Target audience, Success metrics, Baseline,
   Deliverables.
2. **Channel requirements**: this task's lines beside the channel's standard. The
   standard comes from `skills/2_theme/design/venue/venue-<venue>/README.md` § Constraints.
3. **Requirements**: what every design must contain, and the register's acceptance
   lines as "Acceptance checks".
4. **Inputs and resources**: what the designs may draw on.
5. **Exclusions**: what must never appear in the message.

Each block is a two-column table (Item · Specification; the channel table adds the
channel's standard), in plain professional wording. It reads `design-goal.md` beside
`board.md`; the file's section titles stay `Aim`, `Venue`, `Rules`, `Resources`,
`Leave out`. A `Task · <folder>` section overrides a line for one task. A line is
`Item: specification <- source`; the source stays in the file and is never shown, so
file ids such as BR00 do not reach the screen (JL 261001). A `?` value shows as "Not
specified".

The task's name and counts come from the line of the Brief that names this folder
(`0-BR-brief/*/BR00-brief.md`, the first table whose header names `audience`, `job`
and `venue` together; columns matched by header word: `audience`, `job`, `venue`,
`designs`, `folder`). The Deliverables line reads `N designs requested · N registered · N ready`.
`designs` is the number the Brief asks for. `registered` and `ready` are counted from
the register and passed Verify records. `· N declined` is added only when an item was
declined. When the register is short of the Brief's count, the line offers **Ask the
agent to draft the missing N** (a draft request; see Actions). With no Brief line the
Space says so and names the file that would fill it.

The Space has no Insight board line. The board.md `reads:` line still exists as data:
it names the Insight boards whose pages fill a card's Insight pages fold.

`{LINK}` is the link slot, like `{NAME}` (JL 261001). Delivery and the csv show it
right after the ask's colon, before the opt-out (`with_link`). The stored text is
unchanged, and a text that already carries `{LINK}` shows as it is. `max_chars` does
not count it.

**Design Space**

The Space opens with the Design Goal in brief: the task's name, its Objective, Audience,
how success is measured, the Baseline every design is read against, and the rules every
design keeps. Then the **element matrix** (JL 261002: "make the design element be the
first citizen"): one row per design with a draft, one column per element the Design Goal
names (`Elements:` under Resources), and an `added` column. A cell is `·` when the design
kept the starting text's element, `★ <words>` when it changed it, `removed` when it
dropped it; the last row counts how many designs changed each element. A design's own
element record (`elements.yaml`) is read first, with where each element came from and how
it was chosen; a design without one is read by a word comparison with the starting text.
No `Elements:` line, no matrix. With the line, the add-item action makes the record
required: every new Design Item gets one more rule, "every element recorded", which
commissions `elements.yaml` and lists the Design Goal's element names (an item whose own
rule already reads `elements.yaml` keeps it). Then comes one card per Design Item.

A Design Item is one design target with its own rules: one SMS, one UI card, one
message pool. The screen says `Design 3`; the files keep `ITEM03`. It plays the role
on a Design Folder that an Evidence Item plays on an Outline page:

| Outline | Design |
|---|---|
| Evidence Item `E01` | Design Item `ITEM01` |
| expectation + acceptance | goal, expected outcome + rules |
| one Page Evidence Run | distinct rd Commission, Generate and Verify Runs |
| Result | draft + `checks.yaml` |
| accepted | ready for Delivery (Verify verdict `pass`) |

Each card's closed row is one short line per column, under one column header (JL 261001:
the closed row was too wordy; the sentences belong to the open card):

1. **Design**: `Design N ✅ · title`: the state's emoji right after the number, so the
   rows scan at a glance; a word follows only when the emoji alone does not say it
   ("ready" needs none; "generate queued · waiting on you" does).
2. **Rationale**: "Rests on" its top insight page by name in words, plus how many more
   (`Rests on Send salience · +3`).
3. **Evaluation**: `✓ 6/6 acceptance · effect not tested yet`.

`open all · close all` sits above the list. A row opens into a fixed-height card
(560px) that scrolls inside, so every card is the same size. The card body:

1. A line with the item's type, audience and job, and its `ITEMNN` file id.
2. The item's next eligible Run, when it has one (see "Next Run and copy" below).
3. The same three columns as the closed row (JL 261001), each growing downward:
   - **Design**: the SMS bubble (or the screen), "Ready for Delivery · 113 characters ·
     passed independent review", a light fold **Design Runs** (a small grey line, no summary words: the
     emoji and the acceptance count already say how far it got; this design's own runs: step, outcome, who and when, the person's words,
     the run id small), and the native buttons. The runs sit with the design because they
     are how this exact text was made and checked (JL 261001).
   - **Rationale**: Design move (open), then two folds, the design's own parts first
     (JL 261001). **Design elements · 1 new of 6**: the shown draft split into its
     elements against the Design Goal's `Starting text`, each with its support: kept
     (the chain's rows when the stance is follow, else "as sent"), ★ new, ★ removed or
     ★ changed (licensed by the named rows when the design explores; "none" plus its
     Limits when it follows), or Design Goal (a `{LINK}` slot, the opt-out). A sentence
     is cut into kept and new parts only when every part has three words or more;
     otherwise it stays whole, marked changed. Kept parts are backed as part of the
     message as tested, never one by one. When the draft's Generate wrote the element
     record (`elements.yaml`, named in its `result.yaml` as `elements`), the fold shows
     it first, as the designer recorded it: each element's words, where it came from
     (requirements, internal or external insight, intuition), the rule, row or theory
     it rests on, and whether it was reasoned (System 2) or intuitive (System 1), with
     its because and the options weighed (JL 261002). **Evidence chain · W1 → K1 → I1 → D8**: where
     those supports come from, from each row the design acts on (`because:`) down the
     links the insight pages record, one quoted row per level ("▲ because", "▲ shown
     by", "▲ counted from"), each page by its name in words and linked, the other
     parents of a row as "also rests on", then the Limits (named DO NOT rows) and the
     pages cited but not on the chain ("Also cited"). Neither fold is written by a
     Design Run: the workbench reads them from the register, the insight pages, the
     Design Goal and the shown draft.
   - **Evaluation**, three folds of one shape, each summary naming it and its verdict:
     **Acceptance · 6 of 6 pass · independent review** (each rule ✓/✗), **Review notes**
     (the reviewer's `review.md` lines), and **Expected effect · not tested yet, judged
     at the send** (Expected · Wrong if · Against the Design Goal's Baseline · Measured
     by its Success metrics).
   On a narrow screen the three columns stack.
4. The insight and the work are different things and both stay: the insight is why the
   design should work (the Insight board's finished work); Design Runs are how this design was
   made and checked (its own Commission, Generate and Verify runs).

Rules are marked ✓/✗ by the Verify of the draft shown, else by that draft's own
self-check, else "not checked yet". Rule N is criterion `rNN`, plus `rNNb`, `rNNc` when
the rule quoted several phrases. When the register changed after release, the line says
"the register changed after release; drafts still follow the released goal and rules".
A page whose Insight board moved is found by its last three path parts under the
Project's `insights/` world; both page-id schemes (`FW01-send-salience`,
`W01-full-send-salience`) read as words.

A screen shows as its rendered picture. An SMS shows as one message bubble on a
phone, with a `link` mark where the sending system inserts the link (just before
`Reply STOP to opt-out`). The design shown is the item's ready candidate, else its
latest draft while still in progress. A draft that failed the check is never shown,
on the card, in Delivery Space, or in the csv.

`?item=ITEM02` opens that item's card, marks it with an accent bar, and scrolls to it.
A declined item's card is folded after the live ones under `Declined, kept for the
record · N`. Runs that name no registered item appear below the cards as "Runs without
an item". The Space ends with the records check line (`records check: PASS` or its
findings, with folder-relative paths), read live and never cured.

There is no form for a new design on the page. Adding a design is the **Add a design**
run card in the Design Space's Runs panel.

**Next Run and copy**

Every open Design Item states its next eligible Run and actor, purpose, canonical
Type, Skills, prerequisites, released Commission, latest complete draft and latest
matching record when available. Eligibility follows the native action-state rules,
including held Commission decisions and stale queued-Run replacement. A queued or
running Run shows its current actor role. Blocked, unresolved, invalid-record and
ready items gain no start operation. Queueing does not claim the agent already ran.
Static views hide every write control.

Eligible Generate and Verify items also offer **Copy request → paste and send**, with a
**Copy prompt to chat** button and a reviewable prompt. It names the exact Board,
Folder, Page, item, target, Run Type, owner and worker Skills, prerequisites, released
Commission, matching Run and receipt, and next permitted action. The button only
copies text; the person must paste and send it in chat. Reading, expanding or copying
never allocates, queues, executes or sends work.

Copy is offered for an eligible new Generate or Verify, or one compatible planned Run.
It is not offered for Commission, running, stale, blocked, unresolved, invalid, ready
or retired states, a folder with audit findings, missing or blocked Insight bindings,
or a static view. A revision first uses the native feedback and queue form; its queued
Run can then be copied with its frozen base and feedback.

The prompt requires a fresh state read, reuses a compatible queued Run instead of
allocating a duplicate, and stops on changed or ambiguous state. It cannot create or
change the human Commission decision. Verify requires a fresh independent reviewer
context. Work stops after one Run and reports its id and receipt.

The Run types behind the card's buttons:

| Run name / canonical Type | Bounded work | Actor | Owner Skill | Worker Skill |
|---|---|---|---|---|
| Commission / `Design.commission` | release or hold one item's exact goal, rules and inputs | named person | `haipipe-design-workflow` | none; human decision |
| Generate / `Design.generate` | create or revise the released design and self-check every rule | agent | `haipipe-design-workflow` | `haipipe-design-unit` via `haipipe-designer-agent` |
| Verify / `Design.verify` | independently review exact completed drafts against released criteria | independent agent | `haipipe-design-workflow` | `haipipe-design-unit` via a fresh designer-agent context |

**Delivery Space**

Delivery is the read-only handoff of what is ready: every item whose independent
Verify passed, word for word. A text design is one table row, `design` (its number,
linked to its card, and title) · the text as the recipient sees it (an SMS as its
bubble, with its `link` mark). A design that has not passed Verify is not listed. A
declined item is folded under `Declined, kept for the record · N`. The Space ends with
the task's csv link (`↓ This design task's designs · N · csv`).

A **screen** (a UI design) is read as its picture. When the Generate Result names
`render_manifest` for a picture of the exact draft an item shows (`candidate` = that
Generate run), the card puts the picture on the left, with the HTML one click away,
and Delivery shows the folder's ready screens as a picture gallery instead of the
table. The presenter checks that the manifest, source and image exist and are not
newer than the Result. Existing `delivery/render/manifest.json` is a legacy fallback
only when that candidate has no Result-local manifest. A picture of an older draft is
never shown for a newer one. An acceptance rule with the word render, rendered or
rendering and no quoted phrase compiles to a `visual` check.

**Board level: Design Tasks, and the theory in Guide › Method**

**Design Tasks Space** is one table, design task · designs · folder · state, each task
linking to its page level. On a board with method folders its Views are the methods, one per
`2-Design-M<NN>-<slug>/` and no All View (the first method opens). Under each method a second
row of Views is the design unit's three steps, each with its part of `method.md` on top:
**① See input** (the packet the card names, from `1-IN-inputs/`, and `design-goal.md`),
**② Designs** (opens; task by task, each design's message and its reason from the Generate
result's `rationale.yaml`) and **③ Check output** (each design's Verify state and its predicted
click-through). So a method board needs no page level to read its designs; a task the method has
not made says "not designed this way yet" with a New Design Folder button for that method.
Without method folders the Views are the method families, read from the Brief's `method` column. Below it are the "every design task keeps" rules and
**↓ Download all designs** (one csv). New lines and new folders are started from the
Runs panel; the page has no form for them.

**The Method page** (`/_board/design-board?embed=theory&view=method&views=method`, which Guide ›
Method frames) is one document, `servers/workbench-design/guide/method.md`, under the methods drawing
(`Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s03-design-methods/parts/design-methods.excalidraw`, generated by `methods_drawing.py` beside it,
editable on the canvas). Its parts follow the six steps: **1 · The six steps** (one table:
what happens, where in the workbench, who); **2 · Step 2 in depth** (three families by where
the rule comes from, which method when, the index table drawn as thirteen **design method
cards**, one file each in `guide/methods/` beside it); **3 · Step 3 in depth** (what each design records);
**4 · Steps 4 and 6 in depth** (T0 to T4, the evidence); **5 · Why it works** (Simon's
definition, the four kinds of reasoning as sums, messages and soup diagrams); **Reference**,
folded (terms and people with links, the compact reasoning table, the theory behind each step,
the loop in full, O'Cathain's taxonomy). Guide's own step list is off (`explain` "only"). Headings underlined with `~~~` are sub-sections. The
older view keys (`design-theory`, `methods`, `studio`, `papers`) still answer for old links.
Closed, a card is the method's
name, whether any study tests it (counted from its `evidence` papers), its move, its
reasoning (abduction, induction, deduction), what it reads, each input coloured by kind,
what it returns, and where it comes from, each source linked. Open, **What the literature says** (rationale, context,
the steps its authors specify, strengths, limitations, as O'Cathain et al. 2019 describe
approaches) stands beside **Applied to AI** (the agent, its steps, what it returns, how a
second agent verifies it, the AI risk, the evidence on AI, the skill that would run it),
then its tests and its papers. A card whose head says `status: future` (By co-design) is a
method to add later: dashed, tagged "future · not run yet". A bracketed source (`[Prestwich 2013]`) opens that paper's
card in the Papers view; `(ours)` marks the workbench's own judgment. **Methods studio** opens `Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s03-design-methods/parts/design-methods.excalidraw` (three inputs → Design → Exp, the
Revise and Learning loops, design elements, the six families, the thirteen cards closed, an open card's two sides, O'Cathain's categories, the tests and the
open bet) in the
self-hosted Excalidraw canvas, loaded only when shown; edits save back to that file, which
the canvas may write through the root-level `Tools` link. **Papers** reads the
workbench's own `servers/workbench-design/related/papers.md` table (`group · role · key · paper · venue · doi ·
why here · pdf`), the same for every board, and shows it as the Paper workbench shows a
Story's Related Papers: one band per `group` (a design method, `all methods` or `tests`)
with its count, one card per paper. A band shows its key papers (★ in `key`, at least one
per group) and folds the rest under "N more papers"; a band with no key paper shows all
of them. Closed, a card is the title, then who · year · journal, a **PDF** badge when its
full text is inside, a **UTD24** mark when the journal is on the UT Dallas list of 24
business journals, and its role (`classic`, `review`, `evidence`); the head counts the
papers by role, in UTD24 journals and with a PDF, and **Show only the N papers with a
PDF** hides the rest and opens the folds. Open, a card is why it is here, its links (the
PDF in a new tab, the publisher page, the Paper Run), the abstract (folded) and the PDF
itself, loaded only when the card opens. The PDF is the row's `pdf` file in `related/papers/`,
kept there only under an open license (CC BY; `related/papers/README.md` lists each), else the
free copy of a Discovery Paper Run in the board's Project that holds the same DOI, which
also lends its abstract and Paper Run link. Without either the card says to read it on
the publisher page; a book with no DOI says so. The Runs panel's **Add a paper** run
(Discovery orchestrator, `haipipe-discovery`) makes a Paper Run and adds the row. All four views are general
(JL 261001): one channel's knowledge, such as an SMS board's message theories in its
`design-theory.md`, is a resource of the Design Goal and is not shown here; its **Add a
theory** run sits in the page's Design Goal Space.

**The Runs panel**

Every Space at both levels has the shared Runs panel on the right (`live.runs_panel`,
the same one the Paper and Page workbenches use). Its run types come from
`skills/2_theme/design/haipipe-design-workflow/references/run-cards.md` (`design_run_types` in
`design.py`), which is the Workbench Table written as cards. Each card names its
button, agent, skill, what the person signs, and a prompt to copy. Below the types,
each run shows its prompt, process and result.

The panel starts nothing. **Copy** hands the prompt to a Claude or Codex session,
which does the work. Examples of cards: Add design tasks and Add a theory (board);
Frame the aim and Pin the venue (Design Goal); Add a design, Commission, Generate and
Verify (Design); Passed review (Delivery). The card list in `run-cards.md` is the truth.

**Retired**

These are gone and are not described as current: the Insight Space and the Run Space
(their content now folds inside each card), the five-Space layout
(Goal/Design/Insight/Run/Delivery), the Goal's "Insight board" line, the "Insight
pages the designs use" fold, the "Run types in this Space" guide fold, the "New Design
Item" and "New design tasks" forms, the board-level Design and Delivery Spaces, the
old run-guide wording ("Start here", "Shown here · read-only"), Adopt (old Adopt
records stay readable; no writer creates them), and content hashes (sha256).

## The register

The register holds the goal, its evidence, and its rules, never its state. It
lives under `draft/` at `draft/<stem>-design-items.md`, one block per item:

```text
## ITEM01 · Send the salience wording unchanged
type: sms
audience: all patients
job: prescription review
goal: Send the salience wording unchanged, so the reader sees whose office wrote and what to review
stance: follow                     # follow · challenge · explore · generate
basis: evidence-informed           # brief-only · evidence-informed
mode: compose                      # compose · revise · brainstorm · theory-driven · challenge
expected: a first-time reader can say who sent it and what to do after one read
falsified: a cold reader cannot name the next step from the text alone
because: W01-full · W1, W3          # the insight rows it acts on · none
evidence:
- handoff · ../../../A00_SMSR2Full-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
```

`evidence` paths are relative to the Design Folder (the folder holding
`<stem>.md`), not to the register file. A line is `role · path` (or `role  path`
with two spaces); the roles are `evidence`, `handoff`, `inspiration`,
`reference`, and `avoid` (`base` and `feedback` are written by revise runs).

`because` names the insight rows the item acts on, as `<page id> · <row>[, <row>]`,
several pages split by `;` (`because: W01-full · W1, W3`; the older `FW02 · W1` still
reads). The card's Rationale starts its **Evidence chain** at each named DO row and
walks down the links the insight pages record on their `←` lines (Wisdom, Knowledge,
Information, Data, each row quoted by its id); a named DO NOT row is a **Limit**. The
rows are found among the item's `evidence` first, then on the same Insight board.
`because: none`, or a `brief-only` item with no line, reads "AI idea, not from an
insight". An `evidence-informed` item with no line starts at the DO rows of its cited
Wisdom pages and says so; a row not on its page reads "no such row on the cited page".
A `challenge` item adds "if it loses, the rule holds". The design bundle csv carries the
first row in its last column, `because`. The line is display only: a Commission does
not pin it.

`expected` and `falsified` judge design quality: what a reader can do or
understand with the draft. They may name what a later experiment will check,
but Design Runs judge design quality only, so no experiment words (arm,
allocation, power, winner, field) belong in them.

The bindings are checked when the item is added: a `challenge` stance goes
with `challenge` mode and only with it; `challenge` or `theory-driven` mode
needs both `expected` and `falsified`; `brainstorm` goes with stance `explore`
or `generate` and carries no `expected` or `falsified`. `add_item` refuses the
rest with one sentence.

`goal`, `stance`, `basis`, `expected`, and `falsified` feed the v2
`design_intent` (move, stance, basis, expected_effect, failure_condition; the
register says `goal` where the config says `move`, and the config's own `goal`
is the same goal sentence). The Commission pins its config (goal sentence,
stance, basis, mode, expected, falsified, the compiled criteria, and the raw
rule text) and the item's evidence files by path. It does not pin the
Brief version or venue packs. Generate and Verify inherit the released design fields and
evidence list, deriving only review_mode and the permitted operation mode, so an edit to the register after release reaches only a new
Commission, which means a new item (at most one release per item). The card then
says "the register changed after release; drafts still follow the released
goal and rules".

`acceptance` is prose; the Commission compiles each line into v2 criteria:

1. `≤ N`, `at most N` or `no more than N characters` → `max_chars` N;
   `under`, `fewer than` or `less than N characters` → `max_chars` N − 1.
2. A quoted phrase or a `{PLACEHOLDER}` → `contains`; with a negative word
   before it (no, not, does not, doesn't, don't, never, without, avoid,
   excludes) → `excludes`.
3. `ends with 'X'` → `ends_with` (compared with trailing whitespace stripped);
   `starts with`, `begins with` or `opens with 'X'` → `starts_with`.
4. Otherwise, a rule with the word render, rendered or rendering → `visual`.
5. Anything else → `semantic`, judged by the reviewer.

The first rule that applies wins, in this order: a length limit, then quoted
phrases, then the render word.

A rule quoting several phrases makes `rNN`, `rNNb`, `rNNc`. A phrase with only
"or", "and" or commas before it shares the previous phrase's kind, so
`no 'urgent', 'act now' or 'hurry'` excludes all three. An apostrophe inside a
word (`it's`, `doesn't`) is never a quote mark. No state is typed in the
register. Every `run-design-*` run record names the item it serves with
`item: ITEM01`, and the tab derives the item's state by walking its Runs in
order:

```text
not commissioned → commission open → commissioned | commission held
  → generate queued → generating → generated | generate failed
  → verify queued → verifying → ready | verify failed | verify invalid
queued run out of date: a queued run whose pinned file changed since it was queued
```

The full fold, with every queued, running and open state and who each one
waits on, is in `ref/space-mapping.md`.

Beside the state the tab always says **who is waited on**. `agent` is waited
on only while a run is queued or running (`agent · generate`,
`agent · verify`, `agent · running`). Otherwise it says **you** with the
step, never a person's name: `you · commission`, `you · release or hold`,
`you · queue the draft`, `you · queue the review`, `you · queue a revise`,
`you · queue the review again`, or `you · queue again`; a ready item waits on
no one.
A person releases the Commission and clicks the queue buttons; an agent runs
only what is queued. The only budget is
`max_iterations: 2` inside each Generate run; nothing counts revise runs
across an item.

## What the tab reads (it owns no storage)

```text
0-BR-brief/*/BR00-brief.md              the line that names this folder (task name, counts)
design-goal.md (beside board.md)        the five blocks of Design Goal Space
board.md  reads:                        the Insight boards whose pages fill a card's Insight pages fold
draft/<stem>-design-items.md          the register (goal, evidence, rules)
draft/feedback/<run>.md               the feedback a revise Generate was queued with
draft/<stem>-draft-request.md         an open request for the agent to draft items
runs/run-design-<op>-<MMDD>-<slug>.yaml run record: item, target, actor, config ref, pinned inputs
scripts/config/<run>.yaml               goal, design_intent, criteria, the rule text, unit
results/<run>/runtime.yaml              status, actor/worker, times, route, failure
results/<run>/result.yaml + checks.yaml verdict, artifacts, per-criterion checks
results/<run>/content/*                 the draft bytes
results/<run>/decision.yaml             Commission release/hold, when present
results/<run>/render/                   pictures and manifest pinned by result.yaml
delivery/render/                        legacy display manifests, when present
```

It never infers a state from a file name, never counts files as progress,
never shows a draft that no `result.yaml` lists or that failed the records
check; a passed Verify is the Delivery gate.

## Minimal by rule

The surface is text, tables, and folds. Deliberately absent: counters that
count the surface itself, static flow diagrams that read the same on every
folder, raw file listings, and any Space whose content is another Space's
(the card's insight flow names each page by its label and title and links to
it; what each page says, and what is still missing, lives in the card's
Insight pages fold).
The card's flow is drawn per item from its own evidence pages, so it differs
from folder to folder and is not a static diagram. An empty state is one sentence that names the file or Run that would
fill it.

## Actions · Commission decisions and the agent queue

The tab writes through one endpoint, `POST /_board/design-act`, implemented
in `servers/workbench-design/design_actions.py`. Each action writes exactly the contract's files
and nothing else. Every state that waits on a click shows its button, and the
page refuses an action the state does not show, naming the state and who is
waited on:

| Item state | Button | Writes |
| --- | --- | --- |
| not commissioned · commission open · commission held | Release commission · Hold (name + words) | `run-design-commission-*` run record, `decision.yaml`, complete receipt; the config compiled from the register and the item's evidence files, named by path. At most one release per item: a second Release is refused; releasing after hold creates a new Commission Run and preserves the old decision |
| commissioned · revise requested | Queue Generate · agent | planned `run-design-generate-*` run record, a copy of the released config, and a receipt for `haipipe-designer-agent` |
| generated · verify invalid | Queue Verify · independent agent | planned `run-design-verify-*` run record targeting the complete Generate Result; refused when that draft already has a completed valid independent review |
| generate failed · verify failed | Queue revise · agent (feedback) | planned Generate run record with `base` + `feedback` inputs, the feedback saved at `draft/feedback/<run>.md` (a challenge bet stays in challenge mode); refused for a draft that passed its review |
| queued run out of date | Queue again with today's insight files | the old queued run marked `superseded` (reason: the files that changed) and a fresh run that pins today's bytes; a revise keeps its base and feedback |
| blocked | named Run, reason and repair owner; no Commission button | the caller resolves the input/record problem through the Design workflow before work resumes |
| records invalid | recorded candidate/review mismatch and repair owner; no queue button | inspect the records check; preserve recorded versions, and use a new Run for changed content |
| ready | ready for Delivery | no decision Run; the passed Verify pins the exact candidate for handoff |
| generate queued · verify queued · generating · verifying | none ("queued for the agent") | — |
| any | no on-page form; the `add-item` action is started from the **Add a design** run card | one block appended to the register, after the binding check above |
| register short of the Brief's count | Ask the agent to draft the missing N (Design Goal Space) | `draft/<stem>-draft-request.md`: the goal, the insights with FINDING / CONSEQUENCE / DO / DO NOT lines, and how many items to draft. The queue runner only lists open requests; a Claude session appends the items with `add_item` and removes the file |

The independent Verify is the Delivery gate. A passed candidate is ready
without another human decision; a failed draft or failed review can still be
revised through the normal Generate queue. The writer refuses a second open
run for one item and a second review of a draft that already has a completed valid review.

Workers render only inside their own Result and pin the optional render manifest
before completion. The presenter reads this evidence directly; Delivery shows it
only for the exact Verify-passed candidate. Existing `delivery/render/` files are
legacy display material and never authorize new worker writes outside a Result.
Before handoff, the presenter revalidates the exact Generate and independent
Verify Results. Broken artifact, checks, config or render pins show `records
invalid`; Page/Board ready counts, Delivery and CSV all exclude that candidate.

Any form that asks for a name, words, or feedback is folded by default under
one line that names the choice (`Release or hold the commission`, `Queue a
revise, with feedback`); it opens on click, and is already open for the item selected with
`?item=`. A single agent-queue button needs no typing and stays in view. On a
card every form and button sits in the design column, which stays in view.
No control acts on every item at once (JL 260921): one decision, one item, one
sentence on the record. After a click,
every item button lands back on Design Space at that item; a draft request
lands on Design Goal Space.

A person's name is required on Commission and is recorded as the actor; the
name field starts filled with the person already seen on this folder's
decisions, so whoever releases types their own name if it differs. The words
typed are recorded verbatim in Commission's `decision.yaml`. Agent steps are only
*queued*: the tab never generates content, never judges a draft, and never
marks an agent Run complete. `design_actions.name_worker(folder, run, actor)`
names the real worker on the run record before dispatch; the caller then
closes the worker Run with `design_actions.complete_run(folder, run)`, which
runs the records check on the returned Result and writes the receipt
truthfully:

1. **Draft fails the check**: failed, route generate; the person queues a revise with feedback.
2. **Review fails the check**: failed, route verify, even when checks are only unresolved.
3. **Review verdict fail**: complete, route generate; the person queues a revise.
4. **Review verdict pass**: complete, route delivery; the exact candidate is ready.

A review that failed the check shows as `verify invalid · you · queue the
review again`, distinct from a draft that failed review, `verify failed · you ·
queue a revise`. There is no HOLD route from the agent side: HOLD is a
person's decision at Commission. Delivery is not a second decision gate; it
is the read-only handoff of a passed Verify.
Every action re-runs the records check and returns its findings with the
receipt. Refusals come back as one plain sentence under the button.

The records check (`check_unit.py --folder`) calls an open run stale when one
of its inputs or targets is newer than the run record (file time; no content
hashes, JL 260928). A closed run (complete, failed, blocked) reads its inputs
as history, so a later edit to an Insight page does not void it; a closed
Verify is still stale when its target Result is newer than its own
`result.yaml`, and Result files must not be newer than their `result.yaml`.
The frozen config and approval are checked for existence only. A superseded
run needs a reason and no result.

## Running the queue without a session

`cli/design_queue.py <board dir> --list` prints every planned Generate and
Verify run record on the board and every open draft request (it lists draft
requests and never fulfils them; a Claude session drafts the items with
`add_item`). `--run [--limit N] [--dry-run]` names a worker on each record
(`designer-cli-NN` / `reviewer-cli-NN`), dispatches `claude -p` with the
designer-agent brief, and closes the run with the records check. Proven on the
demo board 260917: one Generate run drafted, checked, and closed with no
session in the loop. A queued run whose pinned files changed since it was
queued is skipped with the names of those files; the runner never re-pins in
place, and the person clicks "Queue again" on the page. A worker that dies
and leaves no result is put back in the queue
(`design_actions.release_worker`: the record returns to planned, the lost
worker is named on the receipt) and the runner stops instead of burning the
rest of the queue. Release and Queue again are never taken by the
runner.

## Writer routing

Beyond those actions the tab has no writer. Every other intent routes to its
owner:

| User intent | Owning skill / route |
| --- | --- |
| Add or edit a Design Item | `haipipe-design` (the register); the **Add a design** run card starts it |
| Add a line to the Brief, or open its folder | `workbench-design/ref/design-board.md` (`add-tasks`, `new-folder`) |
| Change the Brief's prose, needs, or signed inputs | `haipipe-design-brief` |
| Release or hold a Commission | `haipipe-design-workflow` → `Design.commission` (a person) |
| Generate or revise a draft | `haipipe-design-workflow` → `Design.generate` (`haipipe-design-unit`) |
| Verify a draft | `haipipe-design-workflow` → `Design.verify` (fresh reviewer) |
| Hand off a passed design | Delivery Space (read only; no second decision) |
| Sign an insight | the Insight workbench, never this tab |
| Render a Design screen preview | `haipipe-design-unit` within the current Result; no extra Run |
| Inspect Page acceptance | Page CHECK, not this workbench |

Selecting an item or a Space is local presentation state and writes nothing.

## Boundary

Apply only to a current Design Page-Folder with `folder-kind: design`. Legacy
`2-DS-design/DS*` folders, `design/DU*` storage, `rNN_design_*` runs, PageX,
and v1 shapes are named as unsupported in the header and served with HTTP
410; nothing in them is read or reinterpreted. An old `DS` link is rewritten
to the `Design-NN` folder only when the file it names no longer exists, so a
DS folder still on disk answers 410 for itself, and a folder parked under the
board's `_archive/` (the way a closed record is retired) leaves its old links
healing to the folder that replaced it.
Fixture material for this tab is built by
`haipipe-page/tests/fixture_design_v2.py`, which writes only contract-valid
records. `--demo` rebuilds the demo DesignBoard under `skills/diagrams/`, and
refuses when the demo already holds runs (people make runs by clicking on it),
unless `--force`, which deletes those runs.

## Reader contract

From one tab, without opening a file, the reader can answer:

1. What does this design task want: its aim, for whom, on which venue, how
   many designs, the rules every design keeps, and what to leave out? (Design
   Goal Space)
2. What is being designed, item by item, and what does each design say?
3. Why this design: its goal, whether it follows or challenges the evidence,
   what it expects a reader to do, and what would show that wrong.
4. Which insights support each item, what they say, whether they are signed
   and pinned, and what is still missing? (the card's Insight pages fold)
5. For each item: which Run is it at, who acted, when, with what outcome, and
   who is it waiting on now? (the card's Runs fold)
6. Which exact draft (run and path) is ready for Delivery, verified by whom, and does
   the records check pass on the folder as it stands? (Design Space)
7. At a glance, what designs do we have? (Delivery Space)

See `ref/space-mapping.md` for the Space ↔ file map and the state fold table.
