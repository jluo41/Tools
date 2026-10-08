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
answers: Q01                    # optional: the Block Question it answers (haipipe-report's link rule)

## Topic
<why these Tasks belong to one Job>

## Tasks
1. t01_<task> · <title>
2. t02_<task> · <title>

## Questions                    # optional: the Job's own register, when its Questions are its own
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

## The six Spaces at Job level

| Space | shows (vanilla) | its buttons → skill |
|---|---|---|
| Description | the face: title, goal, close, answers | Update the description → **haipipe-job** |
| Idea Studio | the Job's studio topics | `run-draw-<sNN>` (add · redraw · save a session) → haipipe-studio |
| Audience Report | its Questions' rows, if it has a register | Ask → haipipe-question; Write · Rebuild drawing · Check → haipipe-report |
| Work Details | its Tasks: name · title · Runs | Add a Task → **haipipe-job** |
| Runs | the Job's soft Runs | Run → haipipe-run |
| Delivery | `delivery/` items | Build the delivery → **haipipe-job** |

1. **Update the description** (`run-face-<jNN>`): edit the face's fields, Topic and Tasks list.
2. **Add a Task** (`run-add-<tNN>`): `new_job.py task <job> --slug … --title …` makes the next
   `tNN_<task>/` with a bare face and lists it; `haipipe-task` then builds the Task (Build the
   Task, at Task level).
3. **Build the delivery** (`run-delivery-<target>`): this skill's at a Job, as a Block's is haipipe-board's
   (decided, b03 s21, 261007).

## A theme's own Job names

A theme may name its Jobs and Tasks its own way instead of `jNN_` / `tNN_` (a paper's
version groups and its Sections). It declares the names once, on its Theme:

```python
THEME = Theme(name="<theme>", ..., level_patterns={"Job": r"^<job regex>", "Task": r"^<task regex>"})
```

1. **Where it counts**: a Job pattern only directly under its Block, a Task pattern only
   directly under one of its Jobs; `jNN_` and `tNN_` still count everywhere.
2. **Which theme's**: the theme that reads the Block (`haipipe-board`: its claim, else its
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
