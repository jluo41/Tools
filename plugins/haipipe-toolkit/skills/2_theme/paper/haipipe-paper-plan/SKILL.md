---
name: haipipe-paper-plan
description: "A paper Board's plan, the studio topics after its story: s03 data flow (how the data becomes each answer: Runs, evidence rows, claims), s04 paper flow (Sections in reader order with their questions, evidence, words, and the dated steps to the send) and s06 paper displays (each display: name, type, what it shows, main or supplement, the Run that makes it, checked against the venue's display rules). Checks that every question lands in a Section and every display has a Run and follows the venue. Trigger: paper plan, data flow, paper flow, display plan, plan the displays, venue display rules, s03, s04, s06, word budget, timeline to the send, /haipipe-paper-plan."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.2"
  last_updated: "2026-11-08"
  group-token: "s03-paper-dataflow"
  # version history: ./CHANGELOG.md
---

# /haipipe-paper-plan · how the data becomes each answer, and how the answers become the paper

Asked 261019 on Physician-SPACE's Project-Example-B: "你觉得我们需要一个 plan 吗？haipipe-paper-plan / plan for
the data flow and plan for the paper flow"; "should make the s03-paper-dataflow-plan and s04-paper-workflow-plan";
"please think about to make the s03 to be the paper-dataflow, and s04 to be the s04-paper-workflow".

A paper's Studio topics sit in the Board folder beside its Jobs; each answers one question, in this order:

```text
s01-ideation          which study is worth doing?          many ideas → one     haipipe-paper-ideation
s02-story-<desk>-…    what does this paper ask, and why?   its questions         haipipe-paper-story
s03-paper-dataflow    where does each answer come from?    data → Runs → RQ      this skill
s04-paper-workflow    how is the paper made from them?     RQ → Section → send   this skill
s05-paper-checklist   is the paper ready to send?          ticks from disk       haipipe-paper (checklist.md, paper_check.py --write)
s06-paper-displays    what does the reader see?            RQ → display → Run    this skill (checked against the venue)
s10-related-work-…    which papers are closest to ours?    20 to 25 papers       haipipe-paper-related
```

s03 and s04 both start from the story's research questions and go opposite ways: s03 back to the data, s04 forward
to the reader. Each changes for its own reason: s03 when a Run lands, s04 when a Section is written or a date moves.


## Shared Paper and Grant planning

Grant is a type within the Paper theme and shares Data + Paper Plan. Data flow
maps existing and proposed data to the aims; Paper flow maps the application’s
argument, sections, evidence and figures. Keep the application preparation
roadmap distinct from the proposed research milestones. Requirements and limits
come from the selected funding call, not manuscript defaults.

Story by Section appears in both Story and Displays but remains the Story
owner’s Section Narrative. The display plan links figures to that argument;
it never maintains a second narrative. The current Paper renderer shares that
source; Grant-specific rendering, scaffolding and assembly support must be
verified before treating the proposed matrix as executable behavior.

One owner per fact
------------------

The plan reads the story; it never copies it. A fact is written once:

| fact | written on | read by |
|---|---|---|
| the research questions, hypotheses, claims | s02 face §3 | s03 rows, s04 `answers` |
| the evidence rows and their support state | s02 face §5 E table | s03 claim cards, s04 Section marks |
| the Runs each question waits on | s02 face §7 T table: its `where` cell names the folders (`b03.j03.t02`), `state` says done or not | s03 analysis cards |
| the venue list | s02 face §9 | s04 `**Budget:**` names the target's desk |
| where the data comes from, how it is matched and tabled | s03 `<topic>-drawing.yaml` | s03 foundation cards |
| the Sections, their words, displays and evidence | s04 Sections table | s04 drawing, the first version's `## Narrative` |
| each display, its type, where it goes and the Run that makes it | s06 Displays table | s06 drawing, s04's displays, s03's "in the paper" column, the j01 pool |
| the venue's display rules | `venues/<venue>/call.md` `## Displays` (haipipe-paper-venue) | s06 check, the evidence ledger's limit |
| the dates to the send | s04 Timeline table | s04 drawing |

A number on a card is read from the Result that holds it on every build, never typed: `count:` on a foundation card,
`numbers:` (keyed by T row, one `{json, say}` or a list of them) on an analysis card.

**When the story and the disk disagree** (an E row "established" whose source holds no Result, or a number its Result
does not say), the plan still draws what the story says and lists the row in its Open for the story's owner; it
never edits the story. A figure or table is
made by a Run (a figure Run's `result/`, JL 261013); s04 names that Run and only shows the display's state.


s03-paper-dataflow
------------------

How the data becomes each answer: the building map, drawn by `excalidraw-workflow`'s `workflow_drawing.py`, read left
to right. Its words are `s03-paper-dataflow-drawing.yaml` beside the face; everything else is read on every build.

```text
THE DATA ─▶ THE MATCHING ─▶ THE TABLES ─▶ ANALYSIS ─▶ HYPOTHESIS → CLAIM ─▶ IN THE PAPER
roster       names → IDs     one row per    §7 T rows    §3 hypotheses,       s04's displays
engines      (cards from the yaml, numbers  per RQ       §5 E states          for that RQ
             read from metrics files)
```

1. **Foundation** (the yaml's `foundation:` columns D, S, T): the inputs, how they are linked, the tables every
   question stands on. Each card names its Block, Job or Task (`b03.j02.t04`), and its `count:` reads a Result's
   JSON file: a list counted (`list:`), or an object's own values (`say: "{rows:,} rows"`, nested keys joined by `_`).
2. **One row per research question**, read from the telling (board.md `story-current:`): its research question, its
   `Potential work` T rows as analysis cards (solid when the T row's `state` is done, dashed when not; a row with no
   `state` is done when a Run's `result/` in its folder holds a file), each with its answer when the yaml's
   `numbers:` names the Result that holds it (the card shows the T row's Run ids when its `where` names them); its hypotheses and claims with their E rows' states (a claim resting on
   several hypotheses, `from 1a, 1b`, is drawn once and named beside the others); and its displays from s04.
3. **The face** says which Blocks hold the pipeline and which Run rebuilds them in order (`**Pipeline:**`; "no
   pipeline Run yet" when none does), and keeps Decided and Open like every topic. Decided holds only what was
   decided while planning the flow (which fold feeds the figures, which table a question reads); a decision the
   story already records is not repeated here.

An older Board's `s03-paper-workflow` is this map under its old name: move the folder to `s03-paper-dataflow`, write
`renamed-from: s03-paper-workflow` under its title, move a hand-written builder to the topic's `history/`, and draw
through `workflow_drawing.py make`. `make` writes excalidraw-workflow's starting yaml; replace its foundation with
yours (`ref/faces.md`), and give it no `figures:` key unless one question must override s04's displays.


s04-paper-workflow
------------------

How the answers become the paper, drawn by `excalidraw-workflow`'s `paperflow_drawing.py`: the Sections as stairs in
reader order (the main frame), what each must do, the displays with the Run that makes each, and the dated steps to
the send. The face carries two lines and three tables:

```text
**Budget:** <the target desk's limits, from its haipipe-paper-venue desk record>, or "<limits> (own estimate: no desk record)"
**Send:** <date> (proposed | agreed by <person> <date>)

| S | section | answers | job | displays | evidence | words |
| Display | title | kind | answers | made by | state |
| W | step | when | who | state |
```

1. **Sections, in reader order**: one row each, `answers` names its research questions (`RQ1`), `job` is one plain
   sentence of what it must establish, `evidence` its E rows (`E4 to E7`) or Discovery rows (`D1`), `words` its
   budget. Every row counts toward the cap unless its words cell says `(outside the count)`: count what the desk
   counts (a page-based desk counts the abstract and captions, so give captions a row). The Results follow the
   story's question order; a venue's "leads with" decides what the abstract and title lead with, not that order.
2. **Every research question lands in a Section.** The drawing prints `❗ RQn has no section` in red when one does not.
   A Section whose evidence is all missing (E rows absent, D rows not read) is drawn red and dashed; its mark means
   "its evidence is in hand", not "it is written", and the drawing says so in its legend.
3. **Displays**: `Figure 1`, `Table 1`, `eFigure 1`; `made by` names the figure Run inside its Job that makes it
   (`b03.j03.t02.r05`, or `a new figure Run after T5`); `state` is done, partly or not started. The count stays within the desk's cap.
4. **Timeline**: from today to the send, one row per step: G0, the Runs the questions wait on, the version
   (`j11_writing_v<MMDD>_<desk>`), the drafted Sections, the displays, the check, the send. `when` is a date or a week
   (dates from the clock, never invented); a person's step names who and the verb (`JL marks`, `JL presses Run`, `a
   person reads 200 names`, `JL sends`: marks, presses, reads, signs, sends, agrees, approves, decides, starts),
   which the drawing marks 🙋 until the step is done; a step a person and an agent share names the person's verb.
   Today comes from the clock; a later date is a proposal counted from it. The version is named by its planned send
   date and the story topic's desk part (`jNN_writing_v<send MMDD>_<desk>`, the first one `j11`; the desk from `s02-story-<desk>-…`).
5. **When the first version is made**, its `## Narrative` is seeded from the Sections table, aligned with
   the Story topic's §8 argument. The version owns its concrete Section rows and compile order;
   the shared Section Narrative remains on the Story topic, and s04 keeps the Displays and the Timeline current.


s06-paper-displays
------------------

Found by its slug, `sNN-paper-displays`: s06 by default, the next free number on a Board whose s06 is taken.
A row's `made by` may name the version it uses (`j01.t03.r02`); the check then reads that Run's `result/`, else the
newest.
A row's Display cell is a pool letter (`Display A`, numbered for the paper by row order) or the printed label itself
(`Table B1`, for a venue that letters its appendix tables, MISQ), which is kept as it is. A pool face answers to its
`display-plan:` line, a `label:` that reads "Display X", or its `number:` (a paper whose `label:` is the LaTeX label,
`tab:results`, keeps it).

The display plan (JL 261101: "in the /haipipe-paper-plan, we should also have the plan for the displays"; "the display
like that should also follow the venue, the venue we are using"): every display the paper will show, planned once,
before it is drawn, and checked against the venue's display rules. The face carries one table and a sketch per display:

```text
**Venue:** <the venues/<venue>/ folder the plan follows>

| Display | name | type | shows | answers | section | where | made by | state |
|---|---|---|---|---|---|---|---|---|
| Display A | <what it shows, in a few words> | figure | <its layout: panels, axes, colour> | RQ1 | Results | main | <the Run> | ⬜ not started |

#### Display A        a ```text sketch of its layout, under its own heading
```

1. **A letter, never a number.** A row is `Display A`, `Display B` … in the pool; its paper number is counted on every
   build from the row order (main figures Figure 1, 2 …; main tables Table 1 …; supplement rows the venue's
   `supplement labels`, eFigure 1 at JAMA). Reorder the rows to renumber the paper.
2. **One row, one pool Task.** First relabel any pool Task the plan already means (`label: Display A` on its face,
   so a drawn figure keeps its Runs); then `display_plan.py seed <Board> --apply` writes each missing
   `j01_evidence_display/tNN_display-<letter>-<slug>/` face (`label:`, `name:`, `type:`, `answers:`, `made by:`), the
   next tNN in one letter sequence: the pool has no main or supplement split, the plan's `where` decides; each
   Run of that Task is a version of the display (haipipe-paper-evidence), its `preview.pdf` the display as the paper
   prints it.
3. **The venue check** (`display_plan.py check <Board>`, exit 1 on a ❗ only; ⚠️ and ⬜ are to look at): main and
   supplement counts within the limits; a Run for every row (an address, `j01.t01.r01` in the Board or
   `b03.j03.t02.r05` in the Project's work/, must be on disk; words such as "a new figure Run after T5" read as not
   made yet); a sketch for every row; each drawn display's caption words, its figure's format, and its width in pixels
   against the venue's width × resolution; a pool Task the plan does not name; the rules the venue has not recorded.
   The same lines are drawn in the s06 drawing and ticked in the checklist's P9. The workbench's Report › Displays
   › 1 · Plan shows the s06 drawing only, no check lines (JL 261102: "we might want to have this to be a excalidraw
   only. No need to put others"); 3 · Examples shows the `sNN-paper-display-examples` drawing the same way.
4. **s04 keeps only the names.** Its Sections table's `displays` cell names the rows (`Display A, Display C`); its old
   Displays table is read only on a Board with no s06.

Steps
-----

```bash
N=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/new_topic.py
W=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-workflow/scripts
python $N topic <Board> --nn 03 --slug paper-dataflow --title "Paper dataflow: how the data becomes each answer"
python $N topic <Board> --nn 04 --slug paper-workflow --title "Paper workflow: how the answers become the paper"
python $N topic <Board> --nn 06 --slug paper-displays --title "Paper displays: what the reader sees, by the venue's rules"
#   replace the faces new_topic.py writes with ref/faces.md's (and add `Plan` to _studio_groups.txt if the Board has one)
python $W/workflow_drawing.py make <Board>/s03-paper-dataflow     # builder + a drawing yaml to fill
python $W/paperflow_drawing.py make <Board>/s04-paper-workflow    # builder
python $W/displayplan_drawing.py make <Board>/s06-paper-displays  # builder (delete new_topic's starter drawing first)
#   fill s03's yaml and s04's tables (templates: ref/faces.md), then draw both
python <Board>/s03-paper-dataflow/build_s03_paper_dataflow.py    # each builder writes its .png too
python <Board>/s04-paper-workflow/build_s04_paper_workflow.py
python <Board>/s06-paper-displays/build_s06_paper_displays.py
P=Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-plan/scripts
python $P/display_plan.py check <Board>          # the venue check; then seed the pool: display_plan.py seed <Board> --apply
python Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts/check.py <x>.excalidraw
```

`check.py` judges s04 frame by frame; it only names s03, whose building map keeps excalidraw-workflow's own column
layout, and its preview is too small to read: read s03 in the Studio, zoomed in. Then read each picture as a reader,
from the picture alone (these four are the reviewer's questions for a plan topic, haipipe-studio
`ref/reader-review.md`):

1. s03: what goes in, how it is linked, and which Run gives each question its numbers? Which Run is still missing?
2. s04: in what order does the reader meet the questions, and where is each one answered?
3. s04: which displays carry the answers, and which Run makes each?
4. s04: what must happen, by whom and by when, before the paper is sent?
5. s06: what does each display show, where does it go, and does it follow the venue's rules?


Boundary
--------

The plan decides nothing about the questions: they are the story's (`haipipe-paper-story`). It starts no Run: it
names the Run, and a person presses Run. A desk's limits are its `haipipe-paper-venue` record's (the bank:
`Tools/plugins/haipipe-toolkit/skills/2_theme/paper/venue/bank/1-QBv-desks/`); with no record, the face says the
budget is an own estimate. A record for another journal (PNAS for PNAS Nexus) is no record; a record marked partial
is used and the budget says "(partial desk record)". The pipeline's Blocks,
Jobs, Tasks and Runs are the Task layer's (`haipipe-project`); their figures are a figure Run's. How each drawing looks
is `excalidraw-studio`'s; the drawers are `excalidraw-workflow`'s; the topic folders and faces are `haipipe-studio`'s.
Once a version exists, its Sections and `## Narrative` are the version's (`haipipe-paper-draft`).


Worked example
--------------

Physician-SPACE `examples-<world>/Project-Example-B/paper/Paper-Example-B/`, the JAMA Network Open Original
Investigation: s02 asks three questions, s03 reads its data flow from `work/b03_jama_agent_vs_search_engine/` (its
pipeline Run `runs/run-pipeline-fold00/`), s04 plans a 3,000-word article with five displays.
