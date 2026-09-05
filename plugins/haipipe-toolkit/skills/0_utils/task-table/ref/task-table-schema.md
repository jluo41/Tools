# Task Table schema and check protocol

Loaded by `/task-table` when a reader needs the exact field rules behind the
rendered surfaces. The generator `render_task_table.py` is the only writer of
a task table; this file says what each of its cells means and where it came
from. The generated row has two lenses: the plan lens (`Develops`, `Input`,
`Output`, and config declarations) and the observed display/runtime lens
(`Addr`, `Task`, `Configs`, `Code`, `Runs`, `State`). They are shown together
but remain separate sources of truth. The main Task Table has exactly one row
per Task Folder; Configs and Runs are separate appendix grains.

## 1. Row grain and address

| Level | Rendered as | Key |
|---|---|---|
| block | `## bNN · <block>` section, one line of counts and stores | `bNN` |
| job | `### bNNjNN · <job>` heading + its rollup line + ONE table | `bNNjNN` |
| task | one row in the job's table; the Task Folder is the minimum unit | `bNNjNNtNN` |
| config (appendix) | one row in Config Catalog per config file owned by a task | task address + config path |
| Run (appendix) | one row in Runs Overview: a ticket, a receipt, or a pair | `bNNjNNtNNrNN` |
| store (appendix) | one row in Store Slots per ② consumer-serving job | `bNNjNN` + store |

Grain is decided by STRUCTURE: a block is a folder under the root that holds
folders; a job is a folder under a block; a task is a folder under a job that
is not one of `src sbatch results notebooks QA workflow outline diagram
_tools dist chat`. The `<b|j|t|r>NN_` prefix is then read for the address; a
folder that has none renders `b??`/`j??`/`t??`/`r??` and a `N1` finding. A
name never filters a folder out.

## 2. Task Table fields

| Field | Source, in order | When absent |
|---|---|---|
| Address | folder prefixes joined | `t??` + N1 |
| Task | folder name | — |
| **Develops** | 1 page head `develops:` · 2 docstring headline of the main script | `?` |
| Input | 1 page head `input:` · 2 newest config top-level or `_meta` `worklist`/`payload`/`inputs`/`input`/`source`/`base` | `—` |
| Output | 1 page head `output:` · 2 newest config top-level or `_meta`: `entry`+`out_tier`/`out_platform`/`out_vintage`, else `entry`+`out_dimension`/`vintage`/`out_name`, else `output`, else `store` | `—` |
| State | page head `state:` | `? (no state: line)`; no page → `⬜ no page` + S5 |
| **Configs** | every config filename and its top-level `mode:` when present; full meaning is in Config Catalog | `—` |
| Code | main script name | `—` |
| Runs | `n tk` (tickets) · receipts by status | `0 tk` |
| Provenance | Develops in _italics_ = docstring fallback; Config Catalog reports the purpose source. The TSV surface carries no italics; a `--surface task --format tsv` reader treats the page/configs as the source of truth | — |

**Main script** = the script a ticket names (`TASK_NAME="…"` or any literal
`*.py`/`*.do`/`*.R`), matched with and without a legacy `NN_` prefix; else the
script whose stem overlaps the task's noun; else the first code file in
`scripts/`. **Docstring headline** = the first non-empty line of the module
docstring (`.py`) or the first comment line (`.do`, `.R`, `.sh`), with a
leading `NN_name —`, `NN_name:` or `name --` stripped.

The page head is the first 40 lines of `tNN_<task>.md`; a plan word is one
line `key: value`. An empty value counts as absent. A `source:` line (the
legacy path a migrated page came from) is not read and not a plan word.

## 3. Config Catalog fields

The Config Catalog is a detail projection, not a second Task Table. It has one
row per file under the task's `scripts/config/` (legacy root `config/` and
`configs/` are still read so the audit can report them). A config is not a new
Task: the owning Task Folder remains the only main-table row.

| Field | Source, in order | When absent |
|---|---|---|
| Task | owning task address and folder name | — |
| Config | path relative to the Task Folder | — |
| Purpose | top-level `purpose:` · top-level `description:` · `_meta.purpose:` · `_meta.description:` · top-level or `_meta` `headline:` | `? (not declared)` |
| Mode | top-level `mode:` · `_meta.mode:` | `—` |
| Input | config top-level or `_meta` `worklist`/`payload`/`inputs`/`input`/`source`/`base` | `—` |
| Output | config top-level or `_meta` `entry` + `out_*`, else `output`, else `store` | `—` |
| Purpose source | the exact declaration used (`top-level purpose`, `_meta.purpose`, etc.) | `not declared` |

The purpose parser reads only scalar fields and simple `|`/`>` block scalars;
it does not parse arbitrary YAML. A filename, `mode`, or other inferred label
is never promoted to Purpose. This makes missing configuration intent visible
without changing the config's authority.

## 4. Job heading line

The job has no table of its own; its facts are one line under `### bNNjNN · <job>`.

| Field | Source |
|---|---|
| Mode | ② when a `store:` resolves, else ① |
| Store | `src/config-defaults.yaml` or `.do` `store:` → `declared`; else the first `store:` found in a task config → `derived`. Two distinct values → `S-store` finding |
| src | file count in `src/` (shared code) |
| pages | tasks with `tNN_<task>.md` / tasks; `develops typed n` counts pages carrying a `develops:` line |
| tickets · runs | summed over the job's tasks |

## 5. Runs Overview fields

| Field | Source |
|---|---|
| Run | task address + ticket/receipt stem prefix |
| Ticket | `runs/<stem>.sh` or `.ps1`; `⬜ none` for an orphan receipt |
| Config | matching `scripts/config/<stem>.*` relative to the task |
| Status | receipt `status` normalised: `ok`/`complete`/`completed` → Done · `running` → Running · `failed`/`aborted` → Failed · `planned` → Ready · `blocked` → Held · `superseded` → Superseded · absent → `? (no status)`; ticket without receipt → Ready |
| Started / Ended | receipt `started`/`started_at`, `ended`/`finished_at`, first 16 chars |
| Exit | receipt `exit_code` |
| Result | receipt folder relative to the block |
| Source | `receipt` or `ticket only` |

Receipts are looked up at `<job>/results/<task>/<run>/runtime.yaml` (the
nested law) and, flagged `S-results`, at `<task>/results/<run>/runtime.yaml`.
A results folder without `runtime.yaml` is `R01`.

## 6. Findings

| Code | Meaning | Owner of the repair |
|---|---|---|
| N1 | folder off the `<b|j|t>NN_` grammar; for tickets, one line per task with the count and two examples | haipipe-task |
| S5 | task has no `tNN_<task>.md` | haipipe-task |
| S10 | `config/` or `configs/` at the task root | haipipe-task |
| S-legacy | code at the task root, not `scripts/` | haipipe-task |
| S-results | `results/` inside the task | haipipe-task |
| S-store | two `store:` values in one job | haipipe-task |
| R01 | results folder without a receipt | haipipe-run |
| R-orphan | receipt with no ticket, or a results folder for a task that does not exist | haipipe-run |

Findings are listed, never repaired, by this utility.

## 7. The `--check` protocol

```text
render(tree) == file on disk, ignoring the two generated-stamp lines
   yes → exit 0   "matches the tree"
   no  → exit 1   unified diff, first 40 lines
--expect-fail inverts the exit code
```

Prove the gate before trusting it (haipipe-task GATE-1): mutate one cell in a
copy, run `--check <copy> --expect-fail`, see `❌ DRIFT` printed AND exit 0
(the flag inverts only the exit code, never the message); then run `--check`
on the real file, see `✅ matches` and exit 0. Record both. A check that has
never failed is a tick, not a gate.

## 8. Minimal conformance checklist

```text
[ ] one Task Table row per task folder; grain by structure
[ ] one Config Catalog row per config file; config purpose is declared or marked missing
[ ] Develops from the page, or from the docstring with the script named
[ ] Input/Output from the page, or from the config with the file named, or —
[ ] every Run row pairs ticket ↔ receipt or says which is missing
[ ] no Done without a receipt status that says so
[ ] one mode per job; store provenance declared or derived
[ ] --check exits 0 on disk and has exited 1 on a mutated copy
[ ] the table is regenerated, never edited
```
