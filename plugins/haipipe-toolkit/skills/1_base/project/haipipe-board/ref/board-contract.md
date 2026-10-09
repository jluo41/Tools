# The Block contract · its face, its Spaces, its theme

Read before creating, editing or checking a Block's face, or deciding which theme reads a
Block. The Block's shape (its name, which folders it may hold) is `haipipe-project`'s
`ref/ladder.md`; its content is this skill's; each theme adds its own words over it.

## Where a Block sits

```text
<Project>/<theme folder>/bNN_<topic>/      tasks/ · discoveries/ · cowork/ · papers/ · insights/ · designs/ · labelings/
├── board.md                               the face (this contract)
├── studio/sNN-<topic>/                    Idea Studio: topics shared by the whole Block (haipipe-studio)
├── reports/qNN_<topic>/                   Audience Report: one folder per Question (haipipe-question · haipipe-report)
├── runs/run-<type>-<target>/              soft Runs only at a Block (haipipe-run)
├── delivery/                              what the Block hands on
├── resources/                             pinned reading the Block cites
└── jNN_<job>/                             its Jobs, in order (haipipe-job)
```

No empty folder is made ahead of its content (`haipipe-project`): `studio/`, `reports/`,
`runs/` and the Jobs come with their first item. A design Block in the Tools repo
(`Tools/blueprints/bNN_<topic>/`) has the same face and folders, read by the vanilla frame.

## The face: board.md

```markdown
# bNN · <title>

board-kind: <kind>
spine: <one sentence naming the Block's topic and boundary>
close: <what must be true for this Block to close>
workbench: <theme>              # optional: the theme that reads it, when its Theme folder names another

## Topic
<why these Jobs belong to one Block, and what this Block excludes>

## Pipeline                     # optional: how the Jobs depend on each other (a Result binding)
## Pages                        # optional: a reading order, when the tree's order is not enough
## Questions                    # optional: the register (haipipe-question), a fenced yaml questions: list
## Related resources            # optional: the resources register (haipipe-question)
```

1. **Title line**: `# bNN · <title>`, the Block's number and a short title.
2. **board-kind**: what kind of Block it is (`task-block`, `discovery-block`, `cowork-block`,
   `design-board`, `insight-board`, `labeling-board`, or a theme's own); the Theme folder
   gives the default.
3. **spine**: one sentence, the topic and its boundary; the frame shows it under Description.
4. **close**: the condition that closes the Block; usually every Question answered.
5. **Header fields only**: `key: value` lines between the title and the first `##`; the frame's
   Description reads `board-kind`, `spine`, `goal`, `state`, `close`, `answer-status`, `status`.

A theme's own Block template sits over this one and keeps these fields: the work theme's is
`haipipe-task`'s `ref/block-board-template.md`; the others are each theme skill's.

## The six Spaces at Block level

| Space | shows (vanilla) | reads | its buttons → skill |
|---|---|---|---|
| Description | the face: title, header fields | `board.md` | Update the description → **haipipe-board** |
| Idea Studio | one row per studio topic | `studio/sNN-<topic>/` | `run-draw-<sNN>` (add · redraw · save a session) → haipipe-studio |
| Audience Report | Question │ Work │ Report rows | `## Questions`, `reports/`, Jobs' and Tasks' `answers:` | Ask a Question → haipipe-question; Write · Rebuild drawing · Check → haipipe-report |
| Work Details | its Jobs: name · title · Tasks | `jNN_<job>/` (or the theme's Job names) | Add a Job → **haipipe-board** (scaffold by haipipe-job) |
| Runs | the Block's soft Runs | `runs/*/run.yaml` | Run → haipipe-run |
| Delivery | `delivery/` items | `delivery/` | Build the delivery → **haipipe-board** |

A theme fills any Space with its own view (`servers/workbench-<theme>/<theme>_theme.py`);
what it leaves out is the vanilla default above (`servers/workbench/frame.py` `vanilla`).
The Guide is each theme's.

1. **Update the description** (`run-face-<bNN>`): edit the face's header fields and Topic;
   keep the field names; a theme's own fields stay.
2. **Add a Job** (`run-add-<jNN>`): `haipipe-job`'s `scripts/new_job.py <block> --slug …`
   makes the next `jNN_<job>/` and its face; add it to `## Pages` only when the Block keeps
   an explicit order.
3. **Build the delivery** (`run-delivery-<target>`): this skill's at a Block (decided, b03 s21,
   261007): Block and Job delivery stay in their level skills, following the theme's delivery
   rule; a Page Task's is `haipipe-page-delivery`'s. No separate `haipipe-delivery` until a
   theme's Block delivery needs more than the level skill holds.

## Which theme reads a Block

The frame asks, in this order:

```text
1. a theme that claims it        Theme.claims(block) -> True   (asked before the Theme folder)
2. its Theme folder              tasks/ → work · discoveries/ → discovery · cowork/ · papers/ →
                                 paper · insights/ → insight · designs/ → design · labelings/ → labeling
3. otherwise                     vanilla (also every Block outside a Project, e.g. Tools/blueprints/)
```

1. **Claims**: a theme declares `claims=<function>` on its `Theme(...)`; the function gets the
   Block folder and returns True for a Block it reads by what the Block holds. An Insight
   Block kept in `tasks/` is claimed by its `workbench: insight` field; a labeling Block by a
   `schema.yaml` beside its `board.md`.
2. **To make a theme read a Block** in another Theme folder: give the face the field that
   theme's `claims` reads (`workbench: <theme>`, `--workbench` on `new_board.py`), never move
   the Block only for its screen.
3. **A claim is cached** per Block and `board.md` version; editing the face re-asks.
4. **A claim that fails** (raises) claims nothing; the Theme folder decides.

## Scaffold

```bash
python <haipipe-board>/scripts/new_board.py <Project>/<theme folder> --slug <topic> --title '<title>' \
  [--nn NN] [--kind <board-kind>] [--spine '…'] [--close '…'] [--workbench <theme>] [--questions] [--dry-run]
```

It takes the next free `NN` in the Theme folder (or `--nn`), the Theme folder's default
`board-kind` (or `--kind`; an unknown folder needs one), writes `bNN_<topic>/board.md`, and
refuses an existing folder or a taken number. `--questions` adds an empty register for
`haipipe-question`. Then `haipipe-project audit <block>` checks its shape.
