# The Block contract · its face, its Spaces, its theme

Read before creating, editing or checking a Block's face, or deciding which theme reads a
Block. The Block's shape (its name, which folders it may hold) is `hai-project`'s
`ref/ladder.md`; its content is this skill's; each theme adds its own words over it.

## Where a Block sits

```text
<Project>/<theme folder>/bNN_<topic>/      work/ · discovery/ · cowork/ · paper/ · insight/ · design/ · labeling/
├── board.md                               the face (this contract)
├── sNN-<topic>/                    Idea Studio: topics shared by the whole Block (hai-studio)
├── trace/<YYMMDD>/<HHMM>_<slug>.md       one piece of work: its prompts, plan, files and check (hai-trace)
├── reports/qNN_<topic>/                   an older Block only: a Question's answer now sits in its topic (hai-report)
├── runs/run-<type>-<target>/              soft Runs only at a Block (hai-run)
├── delivery/                              what the Block hands on
├── resources/                             pinned reading the Block cites
└── jNN_<job>/                             its Jobs, in order (hai-job)
```

A Block holds at most 9 sNN Studio topics (`new_topic.py` refuses a tenth unless `--over-limit`). Before
adding more, reuse a related topic or make an independent area its own Block. Existing topics keep
their ids and files.

No empty folder is made ahead of its content (`hai-project`): a topic, `runs/`
and the Jobs come with their first item. A design Block in the Tools repo
(`Tools/examples/bNN_<topic>/`) has the same face and folders, read by the vanilla frame.

## The face: board.md

```markdown
# bNN · <title>

board-kind: <kind>
spine: <one sentence naming the Block's topic and boundary>
close: <what must be true for this Block to close>
bands: j0N 🗄️ data · j1N 🏋️ pretraining   (optional: names each group of Jobs by its first digit; Status draws one section per group)
workbench: <theme>              # optional: the theme that reads it, when its Theme folder names another

## Topic
<why these Jobs belong to one Block, and what this Block excludes>

## Pipeline                     # optional: how the Jobs depend on each other (a Result binding)
## Pages                        # optional: a reading order, when the tree's order is not enough
## Questions                    # optional: the register (hai-report), a fenced yaml questions: list
## Related resources            # optional: the resources register (hai-report)
## Data                         # optional, a work Block: a fenced yaml data: list, where its data is
```

1. **Title line**: `# bNN · <title>`, the Block's number and a short title.
2. **board-kind**: what kind of Block it is (`task-block`, `discovery-block`, `cowork-block`,
   `design-board`, `insight-board`, `labeling-board`, or a theme's own); the Theme folder
   gives the default.
3. **spine**: one sentence, the topic and its boundary; the frame shows it under Description.
4. **close**: the condition that closes the Block; usually every Question answered.
5. **Header fields only**: `key: value` lines between the title and the first `##`; the frame's
   Description reads `board-kind`, `spine`, `goal`, `state`, `close`, `answer-status`, `status`.

6. **Data** (work Block, optional): a fenced ```yaml block whose top key is `data:`, one row per
   store the Block reads or writes; the work Findings shows it first as 🗄️ Data (JL 261111). A
   count is never typed: `count:` points at a Result under the Block (`file:` JSON or YAML, a dotted
   `key:`, a `label:`), one or a list, read each time the page opens. A store whose `where:` is a folder of
   the SPACE, written from its root (`_WorkSpace/2-RecStore/cohort_a`), also shows in the Files pane under
   Read-From; a catalog or a share has no folder to show.

```yaml
data:
  - name: deid.derived
    where: <catalog>.<schema>        # a Volume path, a share or a repo folder
    holds: one line on what it holds
    access: who can read it
    link: <url>                      # optional
    count: {file: jNN_x/tNN_x/runs/rNN_x/result/summary.json, key: tables.n, label: tables}
```

A theme's own Block template sits over this one and keeps these fields: the work theme's is
`hai-task`'s `ref/block-board-template.md`; the others are each theme skill's.

## The six Spaces at Block level (the older tabbed screen)

| Space | shows (vanilla) | reads | its buttons → skill |
|---|---|---|---|
| Description | the face: title, header fields | `board.md` | Update the description → **hai-block** |
| Idea Studio | one row per studio topic | `sNN-<topic>/` | add · redraw · save a session → hai-studio (no Run: a round is the topic's `passes/pNN-<MMDD>/`) |
| Audience Report | Question │ Work │ Report rows | `## Questions`, the answering topics (an older Block: `reports/`), Jobs' and Tasks' `answers:` | Ask a Question · Write · Rebuild drawing · Check → hai-report |
| Work Details | its Jobs: name · title · Tasks | `jNN_<job>/` (or the theme's Job names) | Add a Job → **hai-block** (scaffold by hai-job) |
| Runs | the Block's soft Runs | `runs/*/run.yaml` | Run → hai-run |
| Delivery | `delivery/` items | `delivery/` | Build the delivery → **hai-block** |

A theme fills any Space with its own view (`servers/workbench-<theme>/<theme>_theme.py`);
what it leaves out is the vanilla default above (`servers/workbench/page/block_index_page/frame.py` `vanilla`).
The Guide is each theme's.

1. **Update the description** (`run-face-<bNN>`): edit the face's header fields and Topic;
   keep the field names; a theme's own fields stay.
2. **Add a Job** (`run-add-<jNN>`): `hai-job`'s `scripts/new_job.py job <block> --slug … --title "…"`
   makes the next `jNN_<job>/` and its face; add it to `## Pages` only when the Block keeps
   an explicit order.
3. **Build the delivery** (`run-delivery-<target>`): this skill's at a Block (decided, b03 s21,
   261007): the Block's `delivery/` folder, its paths and helpers and the Delivery view are `hai-delivery`'s
   (a Page Task's: its `ref/page-delivery.md`); the theme's delivery rule says what is built.

## Which theme reads a Block

The frame asks, in this order:

```text
1. a theme that claims it        Theme.claims(block) -> True   (asked before the Theme folder)
2. its Theme folder              work/ · discovery/ · cowork/ · paper/ · insight/ · design/ · labeling/
                                 (an older plural folder, tasks/ or discoveries/ or papers/, still reads)
3. otherwise                     vanilla (also every Block outside a Project, e.g. Tools/examples/)
```

1. **Claims**: a theme declares `claims=<function>` on its `Theme(...)`; the function gets the
   Block folder and returns True for a Block it reads by what the Block holds. An Insight
   Block kept in `work/` is claimed by its `workbench: insight` field; a labeling Block by a
   `schema.yaml` beside its `board.md`.
2. **To make a theme read a Block** in another Theme folder: give the face the field that
   theme's `claims` reads (`workbench: <theme>`, `--workbench` on `new_board.py`), never move
   the Block only for its screen.
3. **A claim is cached** per Block and `board.md` version; editing the face re-asks.
4. **A claim that fails** (raises) claims nothing; the Theme folder decides.

## Example Blocks

Each theme keeps one example Block: the Block every page of that theme is drawn from, so a page change
shows on real files (hai-ui A08).

1. **Made by the scripts only**: `new_board.py` (this skill), `new_job.py` (`hai-job`) and
   `soft_run.py` (`hai-run`); nothing in it is typed by hand.
2. **Every state**: Jobs in more than one band and many Jobs in one band, a Job with no Task, Tasks done,
   running, waiting on you and planned, a check Run with an open round, traces, and Studio topics (a concept
   with its drawing, a UI preview, `s99` its own Guide) made by `new_topic.py`.
3. **No real work**: its Topic says it is the example; it holds no real code, data or findings.
4. **Where**: work `examples/Project-Ladder/work/b01_example_work`; paper
   `examples/Project-Ladder/paper/Paper-Example`.

A UI preview topic's live views render this Block (`hai-studio` ref/ui-preview-topic.md).
The Block whose pages are designed on an example names it on its face, `examples: work/b01_example_work`
(paths from the Project folder, comma-separated); its Files pane then shows a Block Examples part.

## Scaffold

```bash
python <hai-block>/scripts/new_board.py <Project>/<theme folder> --slug <topic> --title '<title>' \
  [--nn NN] [--kind <board-kind>] [--spine '…'] [--close '…'] [--workbench <theme>] [--questions] [--dry-run]
```

It takes the next free `NN` in the Theme folder (or `--nn`), the Theme folder's default
`board-kind` (or `--kind`; an unknown folder needs one), writes `bNN_<topic>/board.md`, and
refuses an existing folder or a taken number. An empty register for `hai-report` comes by default (`--no-questions` leaves it out). Then `hai-project audit <block>` checks its shape.
