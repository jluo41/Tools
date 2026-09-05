---
name: task-table
description: >-
  Render a block/job/task/run tree as a two-lens table: the display lens says
  what exists and has run, while the plan lens says what every task DEVELOPS,
  reads, and writes. Generated from the tree by ref/render_task_table.py, never
  typed: the three words a person owns (develops:, input:, output:) live on the
  task page and the table projects them, falling back to the code's own
  docstring headline and config out_* keys. Shape: a block is a section, a job
  is one table, a task folder is one row; Config Catalog, Runs Overview, and
  Store Slots are appendices. A config never multiplies a Task row.
  Use when a tasks/ tree needs a one-page plan of what each task builds,
  when checking a table on disk still matches the tree, or when handing a
  restructured tree to a colleague. Not for a Phase/Cycle design contract
  (that is /workflow-table) and not for the naming audit (that is
  haipipe-task/ref/check_task_tree.py). Trigger: task table, what does each
  task develop, render the tasks, TASK-TABLE.md, /task-table.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-09-05"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /task-table · task plan plus display, read off the tree

`/workflow-table` is typed by a designer and says what MAY happen: one row per
Phase/Cycle contract. `/task-table` is its mirror image: generated from disk,
it says what each task IS GOING TO DEVELOP and what it has done. The minimum
unit is the **Task Folder**: one Task Table row remains one task even when that
folder owns several configs and Runs. Use it when a tree needs one answer to:

```text
What does this task build?   → Develops (one line)
What does it read?           → Input
What does it write?          → Output (a store slot, a results folder)
Has it run?                  → tickets ↔ receipts, by status
Which job serves a store?    → mode ① self-serving / ② consumer-serving
```

The same row carries two lenses:

| Lens | Question | Task Table fields | Authority |
|---|---|---|---|
| **Plan** | what is this task intended to build and consume? | Develops · Input · Output · Config Catalog purpose | task-page head and config declarations, with named fallbacks |
| **Display** | what is present and what has happened? | Addr · Task · Configs · Code · Runs · State | task tree, config files, tickets, receipts, and declared stores |

The plan lens and display lens are shown together for comprehension, but they
remain distinguishable. A typed page line is plain; a code-derived plan is
italic; a ticket or receipt reports runtime evidence. The table itself remains
a read projection and never becomes the authority for either lens.

`Configs` is a compact index inside the Task row. The **Config Catalog** appendix
has one row per config and carries its purpose, mode, input, and output. This
keeps the Task row readable while making every configuration explainable. A
missing `purpose:`, `description:`, or `headline:` is rendered as
`? (not declared)`; the generator never invents a purpose from a filename.

## 🧭 Core model

- **The table is a projection, never a source.** Nobody types a row in it. It
  is rendered by [`ref/render_task_table.py`](ref/render_task_table.py) and
  re-rendered whenever the tree moves. A copy on disk that no longer matches
  the tree is the drift `haipipe-task` code S8 hunts; `--check` catches it.
- **The three words a person owns live on the TASK PAGE**, which is the task's
  L3 content (`haipipe-task` ref/task-structure.md), in its head:

  ```text
  # t05_ratemds_photo_probe
  state: ⬜ MIGRATED · not yet run in the new tree
  owner:
  develops: what a third platform would add to NPI2Photo, before adding it
  input: @review/RateMDs/v2026-08/_campaign_chunks + @platforms/RateMDs/v2026-08/urls_npi_matched.parquet
  output: results/t05_ratemds_photo_probe/<run>/probe.json
  ```

  The table reads these lines. When `develops:` is missing it falls back to
  the code and renders the cell in _italics_, so a reader can tell a stated
  plan from an inferred one at a glance; the file header counts both. The TSV
  surface carries no mark, so a TSV reader treats the page as the source.
  A migrated page also carries `source:` (the legacy path it came from); the
  table leaves that line alone.
- **Address is the spine.** Every row keys on `bNNjNNtNN` (a Run on
  `bNNjNNtNNrNN`): the prefixes read off the path, exactly as
  `haipipe-task` ref/block-job-task-run.md defines them. A folder off that
  grammar is still rendered, with a `N1` finding; names are checked, never used
  as a filter.
- **A ticket is a planned Run; a receipt is an actual one.** `runs/<stem>.sh`
  pairs with `<job>/results/<task>/<stem>/runtime.yaml` by stem. Ticket
  without receipt = `Ready`. Receipt without ticket = orphan finding. The
  receipt's `status` is normalised the way `haipipe-run` does
  (`ok`/`complete` → Done, `running` → Running, `failed` → Failed, absent →
  `? (no status)`); a process exit code alone is never promoted to Done.

## 🧭 Table family boundary

`Task Tables` is the task-folder member of the Tables family. It is not a
Phase/Cycle design table and it is not the future Board Page/Page Folder table:

| Sibling | Owns | Does not replace |
|---|---|---|
| `/workflow-table` | Phase/Cycle plan, Run demand, Human Actions, Skill Coverage | concrete task inventory |
| `/task-table` | one row per task folder, with plan and observed runtime lenses | workflow phase contract |
| future `/board-table` | Board Page/Page Folder-level join of Page Face, Task Face, plugin lanes, and Runs | current `folderstat` inventory or Outline authority |

No `board-table` skill or unified Board Table is installed yet. Do not invent
one from a Folder tab, and do not place Board-level planning fields in a Task
Table row.

## 📋 The shape: block = section, job = table, task folder = row

JL 260904: "each job will be a large table, the tasks are the rows, and a
block is the multiple job tables." That is the rendered shape, and the job's
own facts sit on its heading line so there is no separate job table:

```markdown
## b04 · b04_npi_dimension_tables

10 jobs · 17 tasks · stores: _WorkSpace/0-PHY-Store

### b04j08 · j08_npi2photo

① self-serving · 6 tasks · pages 6/6 (develops typed 0) · src 0 · tickets 0 · runs —

| Addr | Task | Develops | Input | Output | Configs | Code | Runs | State |
|---|---|---|---|---|---|---|---|
| b04j08t01 | t01_photo_url_table | _one photo URL per NPI, and a verdict on whether it is a face._ | — | — | r01_v2026-08 · r02_v2026-09 | npi2photo.py | 0 tk | ⬜ MIGRATED · … |
| b04j08t05 | t05_ratemds_photo_probe | _what a third platform would actually add, before adding it._ | — | — | — | probe_ratemds_photo.py | 0 tk | ⬜ MIGRATED · … |
```

The nine columns, and the question each one answers:

| Column | Answers | Read from |
|---|---|---|
| **Addr** | where is it, for grep and citations | `bNNjNNtNN` off the path |
| **Task** | what is the folder called | folder name, verbatim |
| **Develops** | what will this task build | page `develops:`; else the ticketed script's docstring headline, in _italics_ |
| **Input** | what does it read | page `input:`; else the newest config's `worklist`/`payload`/`inputs`/`source`/`base` |
| **Output** | what does it write, and where | page `output:`; else the config's `entry` + `out_*` keys, or `output`, or `store` |
| **Configs** | which configurations belong to this Task | config filenames and modes; full meaning is in Config Catalog |
| **Code** | which script does it | the script a ticket names |
| **Runs** | how many tickets, and what the receipts say | `runs/` count · receipt statuses |
| **State** | where the page says it stands | page `state:` |

Italics are the one mark: an italic Develops cell is the code's own words, not
yet confirmed by a person. Plain text means someone typed it on the page. The
file header counts both.

Two appendix surfaces come from the same scan:

| Surface | One row = | Columns |
|---|---|---|
| **Config Catalog** | one configuration file | Task · Config · Purpose · Mode · Input · Output · Purpose source |
| **Runs Overview** | one Run with a receipt (`--surface run` adds planned tickets) | Run (`bNNjNNtNNrNN`) · Task · Config · Ticket · Status · Started · Ended · Exit · Result · Source |
| **Store Slots** | one consumer-serving job | Store · Job · Provenance · Outputs declared by its tasks · Runs Done |

A `⚠ Findings` block closes the report with what the scan tripped over, one
line per task (no page, tickets off-grammar with a count, results without a
receipt, `config/` at the task root, two `store:` values in one job). Findings
are read off the tree, not judged; the full audit stays with
`haipipe-task/ref/check_task_tree.py`.

## 🗣 Showing the table (JL 260904)

"Show me the table", "preview it", "so we can understand it" means: **paste the
rendered markdown into the reply**, block by block, job by job. Nothing else.

- Never publish an Artifact, build an HTML page, or open a viewer for it. JL
  reads the chat; a link is a detour and the build is his tokens.
- Drop the columns that carry no information yet (a Runs column that is all
  `0 tk`, a State column that is all one value) and say so in one line.
- Point at `<tasks-dir>/TASK-TABLE.md` for the full Task Table and its Config
  Catalog appendix.

## 🧱 What it reads, and only this

| Source on disk | Fills |
|---|---|
| folder structure `bNN_/jNN_/tNN_` | Address, Task, Job, the row grain |
| `tNN_<task>.md` head: `state:` `owner:` `develops:` `input:` `output:` | State, Owner, the three plan words (rendered plain) |
| the script a ticket names (`TASK_NAME=` or a literal `*.py`), else the script named like the task | Develops fallback = its docstring headline, minus a `NN_name —` prefix |
| every `scripts/config/*` file | Config Catalog: `purpose:`/`description:`/`headline:` from the config or `_meta` block, `mode:`, and per-config Input/Output; missing purpose is `? (not declared)` |
| newest `scripts/config/*.yaml`, top-level or simple `_meta` fields | Input fallback = `worklist`/`payload`/`inputs`/`source`/`base`; Output fallback = `entry` + `out_tier/out_platform/out_vintage`, or `entry` + `out_dimension/vintage/out_name`, or `output`, or `store` |
| `runs/*.sh` `*.ps1` | tickets, the Runs column |
| `<job>/results/<task>/<run>/runtime.yaml` | receipts: status, started, ended, exit_code |
| `<job>/src/config-defaults.yaml` `store:` (declared) or a task config `store:` (derived) | Mode and the Store Slots surface |

Nothing from git, from a board page, or from another table. If a value is not
on disk the cell says `—` or `?`; the generator never guesses a plausible one.
The task page supplies plan declarations; the tree and receipts supply display
facts. A future Board Table is outside this scan.

## 🛠️ Commands

```bash
G="$(git rev-parse --show-toplevel)/Tools/plugins/haipipe-toolkit/skills/0_utils/task-table/ref/render_task_table.py"

python3 $G <tasks-dir>                       # print Task + Config + Run + Store surfaces
python3 $G <tasks-dir> --surface task        # one surface: task | config | run | store
python3 $G <tasks-dir> --surface config      # one row per configuration
python3 $G <tasks-dir> --out auto            # write <tasks-dir>/TASK-TABLE.md
python3 $G <tasks-dir> --format tsv          # machine-readable
python3 $G <tasks-dir> --check <tasks-dir>/TASK-TABLE.md            # exit 1 on drift
python3 $G <tasks-dir> --check <mutated copy> --expect-fail         # GATE-1 proof
```

`--check` prints `✅ matches` and exits 0, or the diff plus `❌ DRIFT` and
exits 1. `--expect-fail` only inverts the exit code: the proof PASSES when
you see `❌ DRIFT` **and** exit 0. `<tasks-dir>` may also be one block
folder; the path works from any directory inside the repo, and the script
resolves nothing by `parents[N]`.

## 🔁 Render, then keep it true

1. **Render** `--out auto` once the tree exists. The first honest table of a
   restructured tree says `Ready` on every Task row and shows
   `? (not declared)` for configs without a purpose: that is missing plan
   content, shown as such.
2. **Fill the page heads**, not the table. A `develops:` line on `tNN_<task>.md`
   replaces the docstring fallback on the next render; the cell turns from
   _italic_ to plain. The header line counts how many are typed.
3. **Re-render after any move**: rename, new task/config, or a run that
   finished. The command is the repair; there is nothing to edit by hand.
4. **`--check` in a gate** before a commit or a hand-off. Prove it can fail
   first (`--expect-fail` on a mutated copy, GATE-1 in `haipipe-task`), then
   trust the pass.

## ✅ Validation gates

The rendered table is ready only when all of these hold:

- every task folder in the tree has exactly one Task Table row, and every row
  points at a folder that exists (structure, not name, decided the grain);
- every config file appears exactly once in Config Catalog and never creates a
  second Task row; its purpose is declared or explicitly shown as missing;
- every Develops cell is either plain (typed on the page), _italic_ (the
  ticketed script's docstring), or `?`; the header's typed/from-code counts add
  up to the task count;
- every Input/Output cell is a page line, a config-derived value, or `—`;
  nothing is guessed;
- plan cells remain distinguishable from observed display/runtime cells, and a
  Folder inventory is never relabelled as a Board Table;
- every Run row pairs a ticket with a receipt, or says which side is missing;
- no Run is `Done` on an exit code alone; a receipt with no `status` renders
  `? (no status)`;
- a job shows one mode and, when ②, one store with its provenance
  (`declared` or `derived`);
- `--check` against the file on disk exits 0, and has been shown to exit 1 on
  a mutated copy at least once for this tree.

If a cell cannot be filled from the files listed above, it stays `—`/`?`.
Do not repair the tree from this utility: a missing page, an off-grammar
ticket, or a `config/` at the task root belongs to `haipipe-task`, and the
person who owns the task writes its `develops:` line.

## 📚 Related contracts

- `/workflow-table` is the typed sibling: one row per Phase/Cycle contract,
  with Skill Coverage. Its Runs Overview row shape (`bNNjNNtNNrNN`) is reused
  here verbatim rather than redesigned.
- `haipipe-folder` is why a task row can carry a plan: a task folder has a
  Page Face (`tNN_<task>.md`, where `develops:` lives) and a Task Face (the
  code and runs the other columns read). Config files remain inside that Task
  Face; they are summarized in the row and expanded in Config Catalog.
- The current Folder already has separate projections: the
  `haipipe-plugin-folder` tab is live material inventory, Outline is the
  Page/plan projection, and Runs presents runtime. They are not yet one
  unified Board Table; that is a future sibling contract.
- `haipipe-task` owns the tree grammar (`ref/block-job-task-run.md`,
  `ref/hierarchy.md`, `ref/task-structure.md`), the task page, the `store:`
  declaration, and the naming/wiring audit `ref/check_task_tree.py`.
- `haipipe-run` owns Run identity, the runtime receipt, and the status
  normalisation this table renders.
- [`ref/task-table-schema.md`](ref/task-table-schema.md) carries the field
  definitions, the fallback order, the finding codes, and the `--check`
  protocol.

## 📂 Files

```text
task-table/
├── SKILL.md                      this contract and operating method
├── CHANGELOG.md                  skill-scoped version history
├── agents/openai.yaml            UI metadata and invocation prompt
├── ref/task-table-schema.md      fields, Config Catalog, fallbacks, --check protocol
└── ref/render_task_table.py      the generator; the only writer of a task table
```
