# The Job contract · its face, its Tasks in order, its names

Read before creating a Job, adding a Task to one, or naming a theme's own Jobs. The Job's
shape (which folders it may hold) is `haipipe-project`'s `ref/ladder.md`; what a Task is
and how it is built is `haipipe-task`'s; this skill owns the level between them.

## Where a Job sits

```text
bNN_<block>/
└── jNN_<job>/                     or a theme's own name (below)
    ├── jNN_<job>.md               the face (this contract)
    ├── studio/ reports/           its own topics and Questions, when it has them
    ├── runs/run-<type>-<target>/  soft Runs only at a Job (haipipe-run)
    ├── src/ sbatch/               shared code and a supervisor, when its Tasks share them
    ├── delivery/                  what the Job hands on
    └── tNN_<task>/                its Tasks, in order (haipipe-task builds each)
```

A Job groups Tasks that share inputs, code or one question. A Job holds no `scripts/`,
`results/` or `notebooks/` (the audit calls them debt): code and evidence live in a Task.

## The face: jNN_<job>.md

```markdown
# jNN · <title>

goal: <what this Job delivers>
close: <what must be true for this Job to close>
emoji: 🧭                       # its own emoji on the Goal tree line (a work Block, 261021)
answers: Q01                    # optional: the Block Question it answers (haipipe-report's link rule)

## Background                   # optional: what the work is for, a few bullets a newcomer reads first
- **Why**: <the need behind it> · **What we build**: <...> · **Where it stands**: <real numbers, their Run>

## Topic
<why these Tasks belong to one Job>

## Tasks
1. t01_<task> · <title>
2. t02_<task> · <title>

## Questions                    # optional: the Job's own register, when its Questions are its own

## Deliverables                 # a work Block: what the Job hands on, the Goal's to-do list (below)
```

1. **Title line**: `# jNN · <title>`, or the theme's folder name for a theme's own Job.
2. **goal · close**: one line each; the frame's Description shows them.
3. **answers:**: the Job answers a Block Question (`Q01`) or one need of it (`Q01.E2`); the
   Block's Audience Report then lists this Job in that Question's Work cell.
4. **## Tasks**: the Tasks in order, one line each, `N. <folder> · <title>`. Order is the
   reading and dependency order; a Task's number is its place when it was added and never
   moves. `new_job.py check` says when the list and the folders disagree.
5. **Questions at a Job**: a Job may keep its own register; its Audience Report then draws
   its rows at Job level, the same row as a Block's (`haipipe-report`).
6. **emoji**: one lively emoji per Job, different from every other Job's in its Block (JL 261020:
   "这个 job 的 emoji 应该更活泼一些"); the Goal tree shows it before the Job's name.
7. **## Background**: optional; what the Job is for, in plain words and real numbers, a few `- **Label**: ...`
   bullets (why it is needed, what we build, how we know, where it stands). The Goal view shows it under the goal,
   above the tree, its words folded under one "BACKGROUND · N points" line and its pictures in view (JL 261021: "可以再加一个 section，比如叫 background 啥的，介绍一下我们要实现什么"); the goal line
   itself says the end state a reader wants, not the steps. A fenced `yaml` block there holding `timeline:` (items, times,
   bites: [{name, at, items}], caption) is drawn as a picture: a lane per item, a row per moment, a band per bite
   across the items it holds (j01_ext_food, JL 261021: "how do you think you can make the html to show this in the
   goal"); `spans: [{name, item, from, to, aside}]` draws the other shape, one lane over a stretch of time (an
   exercise activity from its start to its end; `aside` dashed, a device's day total; j02_ext_exercise, 261021);
   `clock: {from: "07:00", to: "09:00", hour_px: 150}` in place of `times` draws a real clock, every hour the same
   height and each HH:MM where its minutes put it, labelled every `mark` minutes (60 by default; 180 for a whole day,
   which ends at 24:00); a clock whose `to` comes before its `from` (23:00 to 07:00) runs past midnight (exercise,
   step and sleep, 261021);
   any other fenced block shows as written. A span with `zoom: true`, and the block's `zoom: {items, times, bites}`,
   draw one picture: the day's events, and that span opened beside them into its own lanes and bites, joined by two
   dashed lines (j01, JL 261021: "你可以把这两个图融成一个图吗"). `rule: {question, width?, branches: [{answer, title,
   then, example, today}]}` draws the handling rule in the same picture, top right: the question, then a box per answer,
   the one that holds today filled (j01: what happens to a meal with no logged end). Separate timeline blocks one after another share one
   line, side by side.
8. **## Deliverables**: a work Job's to-do list, below. `haipipe-project audit --today` reports a
   work Job without it, or without `emoji:`, as debt; `/wb update` lists them to write.

## The Deliverables: what a Job hands on (LLMRec b01 and b02, 261021)

JL 261020: "I want it like the TODO list ... for each job, what are the delivery and outcome to
provide ... make the Goal to be the first one". The face's `## Deliverables` holds one fenced
`yaml` block; the workflow layout's Goal view (workbench-work `work_progress.py`) draws it as one
folded tree, Goal → Job → Task → item, and ticks each item from disk, never from a person's word.

```yaml
deliverables:
- what: C2B rerank answers, fold00       # its short name; quote it when it holds ": "
  kind: data                             # data · table · figure · card · check · site · view · code · doc
  task: t03_c2b_llm_rerank               # the Task it sits under (else its run's Task, else the Job)
  means:                                 # what it is: 2 to 5 short bullets, plain words
  - C2B is the second step, rerank.
  - For each search, a model gets only the doctors it kept in C2A.
  files: _WorkSpace/A-Store/fold00/c2b-rerank/*/*reconciled*/run_manifest.json   # a glob or a list
  count: 6                               # the files that make it whole
  run: t03_c2b_llm_rerank/r24_fold00     # the Run whose finish ticks it; several: runs: [{run, part}], each must finish
  checked_by: t01_pool/r01_pool_build    # a Run that rebuilt or compared it, never its maker
  from: [{what: Retry, means: [...], files: ..., run: ...}]   # the batches it was gathered in
  open: [Terra is still answering]       # what keeps it 🔶
  used_by: [b03 j01 t06]                 # who reads it
  example: {file: ..., columns: [...]}   # one row or record a reader sees first
  browse: {root: ..., index: ...}        # a finished set, opened level by level
  opens: <another item's what>           # a view: it ticks only when that item's browse index is on disk
```

1. **One thing handed on**: an item is what a reader of the Job uses, not a step. Keep only the
   latest (JL 261021): `files` names the final view (a reconciled set, the published build),
   never the passes and retries that made it; those are its `from:` batches when they matter.
2. **means**: bullets a newcomer reads first (JL 261021: "make this part a little big";
   "可以用 bullet points 吗"). Each bullet one point; the first says what the step is, a term is
   defined where it first appears (`NPI: the national ID every US doctor has`), real model and
   folder names, no shorthand a stranger cannot read.
3. **The tick**: ✅ its files are on disk (`count` of them) and its Run finished; 🔶 some files, a
   Run short of its gate, or an `open:` line; 🚧 its Run is running; ❌ a failed Run with nothing on
   disk; ☐ nothing yet. A Task, a Job and the Goal are ✅ or 🔶, never ❌ for one open item. The tick
   reads only the disk: a close that needs a person (read, signed) stays an `open:` line until then.
4. **Paths**: `files` is read from the face's folder, unless it starts with `_WorkSpace/` or
   `code/` (then from the SPACE root); `example.file` and `browse.root` are always from the SPACE
   root. The view says a path from its Task (`runs/<run>/result/...`).
5. **The Block's own**: a Block's `board.md` may hold its own `## Deliverables` for what no Job
   owns (a drawing across Jobs); the tree shows them last, as "Across all Jobs". A table made by a
   Run is a Job's: a hard Run lives in a Task (LLMRec b01 j09 holds the five-source comparison).
6. **kind**: data (a stored set), table (one table), figure (charts), card (a Table Card), check
   (an audit or comparison verdict), site (a published build), view (a link that opens a set),
   code, doc.
7. **A Task with nothing yet**: list what it will hand on, with no file on disk; it shows ☐ todo.
   The Goal tree shows only a Task that has an item, so a Task with none is invisible there.
8. **A replaced Task still read**: list its output while another Run still reads it, with an
   `open:` line naming the readers and what replaces it; drop the item once they have moved.
9. **Write it from the records**: the Runs' receipts, the Tasks' faces and the files on disk, by
   the agent that knows the Job. `/wb update` names a Job that lacks it; it never writes one.
10. **Check it**: `new_job.py check <job>` also checks the list: it parses, each item has `what`
   (once), a `kind` of rule 6, `means`, and `files` or `opens`, and every Task and Run it names is
   there. A file not made yet is a to-do, not an error. Then open the Goal view and read the ticks.

## The six Spaces at Job level

| Space | shows (vanilla) | its buttons → skill |
|---|---|---|
| Description | the face: title, goal, close, answers | Update the description → **haipipe-job** |
| Idea Studio | the Job's studio topics | `run-draw-<sNN>` (add · redraw · save a session) → haipipe-studio |
| Audience Report | its Questions' rows, if it has a register | Ask · Write · Rebuild drawing · Check → haipipe-report |
| Work Details | its Tasks: name · title · Runs | Add a Task → **haipipe-job** |
| Runs | the Job's soft Runs | Run → haipipe-run |
| Delivery | `delivery/` items | Build the delivery → **haipipe-job** |

1. **Update the description** (`run-face-<jNN>`): edit the face's fields, Topic and Tasks list.
2. **Add a Task** (`run-add-<tNN>`): `new_job.py task <job> --slug … --title …` makes the next
   `tNN_<task>/` with a bare face and lists it; `haipipe-task` then builds the Task (Build the
   Task, at Task level).
3. **Build the delivery** (`run-delivery-<target>`): this skill's at a Job, as a Block's is haipipe-block's
   (decided, b03 s21, 261007).

## A theme's own Job names

A theme may name its Jobs and Tasks its own way instead of `jNN_` / `tNN_` (a paper's
version groups and its Sections). It declares the names once, on its Theme:

```python
THEME = Theme(name="<theme>", ..., level_patterns={"Job": r"^<job regex>", "Task": r"^<task regex>"})
```

1. **Where it counts**: a Job pattern only directly under its Block, a Task pattern only
   directly under one of its Jobs; `jNN_` and `tNN_` still count everywhere.
2. **Which theme's**: the theme that reads the Block (`haipipe-block`: its claim, else its
   Theme folder); the vanilla frame has no patterns.
3. **Scaffold**: `new_job.py job <block> --name <folder>` and `new_job.py task <job> --name
   <folder>` take the theme's name as given; the face's title line starts with that name.
4. **Faces**: the same face file, `<folder>/<folder>.md`, and the same fields.

## Scaffold and check

```bash
S=<haipipe-job>/scripts
python $S/new_job.py job  <block> --slug <job>  --title '<title>' [--answers Q01] [--goal '…'] [--close '…']
python $S/new_job.py task <job>   --slug <task> --title '<title>' [--kind page] [--answers Q01.E1]
python $S/new_job.py check <job>
```

`job` and `task` take the next free number (or `--nn`, or `--name`), refuse a taken one or an
existing folder, and make no empty folders. `check` exits 1 when `## Tasks` and the folders
disagree. Then `haipipe-project audit <job>` checks its shape.
