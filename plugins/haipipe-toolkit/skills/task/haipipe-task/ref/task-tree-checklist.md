# Task-tree checklist · the definition of done for a bNN/jNN/tNN/rNN tree

JL 260904, after a restructure shipped with no `runs/` in 19 tasks, tickets off
the `rNN_` grammar, results written inside tasks and `configs/` at task roots:
"you didn't follow the /haipipe-task; we need to give it a checklist". This is
that checklist. Every line is one thing a stranger can verify from disk, its
finding code, and the command that checks it. A tree is DONE only when every
row passes on the real folders, and the gate has been shown to FAIL on a
known-broken tree first (GATE-1).

## The six commands

```bash
C=Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/check_task_tree.py
T=Tools/plugins/haipipe-toolkit/skills/0_utils/task-table/ref/render_task_table.py

cp -R <one block> <scratch>/mut && rm -rf <scratch>/mut/<a task>/runs && mkdir <scratch>/mut/<a task>/results
python3 $C <scratch>/mut --expect-fail        # 1 GATE-1: plant breaks in a COPY; R02 and S12 must fire
python3 $C <tasks-dir>                        # 2 on the tree you built: 0 findings
bash <one ticket per task TYPE> <its own dry flag>   # 3 a receipt lands at <job>/results/<task>/<run>/runtime.yaml
                                              #   (scrapers take --dry_run, builders --dry-run, checks --check; read the script)
python3 $T <tasks-dir> --check <tasks-dir>/TASK-TABLE.md   # 4 the table on disk is CURRENT (a new receipt makes it stale)
python3 $T <tasks-dir> --out auto             # 5 re-render after 4 fails; every task a row, every ticket a Run, Findings empty
find . -name _WorkSpace -not -path './_WorkSpace*'   # 6 must print nothing (a wrong root creates one)
```

## The rows

NAME · every folder passes the stranger test
- [ ] N1  block `bNN_`, job `jNN_`, task `tNN_`; a job name is `<noun>_<qualifier>`, two words at least
- [ ] N5  no name made of shape words only (data, table, pipeline, pool, rank, …)
- [ ] —   Task names are unique within one Job; cross-Job repeats use full b/j/t addresses and relative paths
- [ ] N9  every ticket in `runs/` is `rNN_<stem>.sh|.ps1`; the stem does not repeat `run_`

SHAPE · one grammar at every level
- [ ] S18 every canonical b/j/t Block has `board.md` with exact `board-kind: task-block`
- [ ] S5  every task has `tNN_<task>.md` (the page a reader opens)
- [ ] S10 a task's own code is `scripts/`; a job's shared code is `src/`; never the other way
- [ ] S14 config sits INSIDE `scripts/config/`; no `configs/` or `config/` at the task root, no `"configs"` in code
- [ ] S11 a `.sh` that calls other tickets is a batcher: it lives in `sbatch/`, never in `runs/`
- [ ] R02 every task has `runs/` with at least one `rNN_` ticket, config-less scripts included
- [ ] S17 every job has `src/`, kept visible by a `.gitkeep` that names the slot; `results/` is never pre-created

WIRING · the ticket, the config, the script
- [ ] N7  every `rNN_` run-config has a ticket of the same stem, and the reverse when the task uses configs
- [ ] —   the ticket derives RUN_NAME from its own file name and names `scripts/config/${RUN_NAME}.yaml`
- [ ] —   the ticket calls a script that exists in `scripts/` (`python "$TASK_DIR/scripts/<stem>.py" "$@"`)
- [ ] S15 no store path is derived from the ticket's file name; a chunk folder is pinned in the config (`chunk_dir:`)
- [ ] S16 no script, config or ticket names a `tasks/…` path that does not exist (a hardcoded config path, an old `producer:` string)

RESULTS · generated output lands where the law says
- [ ] S12 no `results/` inside a task, and no task script writes `TASK_DIR / "results"`
- [ ] R01 every `results/<task>/<run>/` carries `runtime.yaml`; R05 no `results/<x>/` for a task that does not exist
- [ ] —   a script that writes its own output folder names it after `RUN_NAME`, so output sits beside its receipt

ROOT · the 260811 hazard
- [ ] S13 no `WS_ROOT = ….parents[N]`; the root is found by the marker walk (`pyproject.toml` + `code/`)
- [ ] —   `find . -name _WorkSpace -not -path './_WorkSpace*'` prints nothing

PROOF · nothing above is believed until it ran
- [ ] the checker fired on a mutated COPY with planted breaks (`--expect-fail` exit 0, naming the codes) and is clean on the real tree; the pre-BJTR tree fires only N0, which proves nothing about the new rows
- [ ] one ticket per task TYPE ran (dry run is fine) and its receipt reads `status: ok` at the job level
- [ ] the table's Findings block is empty and `--check` is green
- [ ] both numbers are written into the report a person reads

## What this list is not

- Not the naming law itself: `ref/block-job-task-run.md` and `ref/hierarchy.md` own that.
- Not the Stata dialect's extra rules (N2, N8, S1–S3, S7, S9): the same checker runs them when it sees `.do` and `.ps1`.
- Not a substitute for `fn/audit.md`, which pairs the four sisters of a RUN; this list is about the TREE.
