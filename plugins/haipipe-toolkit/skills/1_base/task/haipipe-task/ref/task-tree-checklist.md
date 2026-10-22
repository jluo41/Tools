# Task-tree checklist · the definition of done for a bNN/jNN/tNN/rNN tree

JL 260904, after a restructure shipped with no `runs/` in 19 Tasks, Tickets off
the `rNN_` grammar, Results written inside Tasks and config outside `scripts/`:
"you didn't follow the /haipipe-task; we need to give it a checklist". This is
that checklist. Every line is one thing a stranger can verify from disk, its
finding code, and the command that checks it. A tree is DONE only when every
row passes on the real folders, and the gate has been shown to FAIL on a
known-broken tree first (GATE-1).

## The commands

```bash
C=Tools/plugins/haipipe-toolkit/skills/1_base/task/haipipe-task/scripts/check_task_tree.py
L=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/scripts/ladder.py

cp -R <one block> <scratch>/mut && rm -rf <scratch>/mut/<job>/<task>/runs
python3 $C <scratch>/mut --expect-fail        # 1 GATE-1: plant a break in a COPY; R02 must fire
python3 $C <block or work/>                   # 2 on the tree you built: 0 findings
python  $L audit <block> --today              # 3 the ladder's shape and today's rules: 0 failed, no debt
bash <one ticket per task TYPE> <its own dry flag>   # 4 a receipt lands at <task>/runs/<run>/result/runtime.yaml
                                              #   (scrapers take --dry_run, builders --dry-run, checks --check; read the script)
/wb update <block> --no-open                  # 5 every Job's Goal items tick from disk; the plan lists what is left
find . -name _WorkSpace -not -path './_WorkSpace*'   # 6 must print nothing (a wrong root creates one)
```

## The rows

NAME · every folder passes the stranger test
- [ ] N1  block `bNN_`, job `jNN_`, task `tNN_`; a job name is `<noun>_<qualifier>`, two words at least
- [ ] N5  no name made of shape words only (data, table, pipeline, pool, rank, …)
- [ ] —   Task names are unique within one Job; cross-Job repeats use full b/j/t addresses and relative paths
- [ ] N9  every ticket in `runs/` is `rNN_<stem>.sh|.ps1`; the stem does not repeat `run_`
- [ ] N10 each `rNN` index identifies exactly one Run stem inside its Task

SHAPE · one grammar at every level
- [ ] S18 every canonical b/j/t Block has `board.md` with exact `board-kind: task-block`
- [ ] S20 no Block, Job, or Task root contains `README.md`; use the Block face, the Job face, the Task face or a `studio/` topic
- [ ] S5  every task has `tNN_<task>.md` (the page a reader opens)
- [ ] S10 a task's own code is `scripts/`; a job's shared code is `src/`; never the other way
- [ ] S14 a Run's config is `runs/<run>/config.yaml` (or `scripts/config/<run>.yaml` in a Block not yet moved);
        no config lane exists at the Task root
- [ ] S11 a `.sh` that calls other tickets is a batcher: it lives in `sbatch/`, never in `runs/`
- [ ] S4  a kept chat session carries BOTH `digest.md` and `transcript.md`; `studio/` holds only `chat/` and `draw/`
- [ ] R02 every task has `runs/` with at least one `rNN_` Run, config-less scripts included
- [ ] —   a Job holds `src/` only when two of its Tasks share code (S17, a `src/` in every Job, was dropped 261021)

WIRING · the ticket, the config, the script
- [ ] N7  every `rNN_` run-config has a ticket of the same stem, and the reverse when the task uses configs
- [ ] —   the ticket derives RUN_NAME from its own file name and names `scripts/config/${RUN_NAME}.yaml`
- [ ] —   the ticket calls a script that exists in `scripts/` (`python "$TASK_DIR/scripts/<stem>.py" "$@"`)
- [ ] S15 no store path is derived from the ticket's file name; a chunk folder is pinned in the config (`chunk_dir:`)
- [ ] S16 no script, config or ticket names a `work/…` path that does not exist (a hardcoded config path, an old `producer:` string)

RESULTS · generated output lands where the law says
- [ ] R01 every Run that wrote `runs/<run>/result/` carries `runtime.yaml` there or in a `passes/pNN-<MMDD>/`;
        a Block not yet moved: every `<task>/results/<run>/` carries one
- [ ] S12 no `results/` at the Job level, and no task script writes `TASK_DIR / "results"`: a Result lives in
        the Task that owns the Run (JL 260909)
- [ ] S16 no path names the old `tasks/` world (it is `work/` since 261010) or a `work/…` path that does not exist
- [ ] —   a script that writes its own output folder names it after `RUN_NAME`, so output sits beside its receipt

ROOT · the 260811 hazard
- [ ] S13 no `WS_ROOT = ….parents[N]`; the root is found by the marker walk (`pyproject.toml` + `code/`)
- [ ] —   `find . -name _WorkSpace -not -path './_WorkSpace*'` prints nothing

PROOF · nothing above is believed until it ran
- [ ] the checker fired on a mutated COPY with planted breaks (`--expect-fail` exit 0, naming the codes) and is clean on the real tree; the pre-BJTR tree fires only N0, which proves nothing about the new rows
- [ ] one ticket per task TYPE ran (dry run is fine) and its receipt sits in its Run's `result/`
- [ ] `ladder.py audit --today` shows no failed and no debt, and the Goal view ticks what the disk holds
- [ ] both numbers are written into the report a person reads

## What this list is not

- Not the naming law itself: `ref/task-folder.md` § Names owns that.
- Not the Stata dialect's extra rules (N2, N8, S1–S3, S7, S9): the same checker runs them when it sees `.do` and `.ps1`.
- Not a substitute for `fn/audit.md`, which pairs the four sisters of a RUN; this list is about the TREE.
