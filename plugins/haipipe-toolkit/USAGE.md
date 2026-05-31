haipipe-toolkit — Usage Guide
==============================

Practical guide to USING the toolkit. For an inventory of what skills
exist see `README.md`. For task ↔ probe boundary thinking see
`skills/D_probe/MENTAL_MODEL.md`. This file is the workflow recipe
book — concrete commands, common flows, gotchas.


The 3 worlds — one project, three folders
==========================================

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/
│
├── 💼 tasks/         ← the WORK         (C_task)   code + runs + metrics
├── 📊 probes/   ← the CLAIMS       (D_probe)  steering + verdicts
└── 📰 paper/         ← the DELIVERABLE  (F_paper)  manuscripts
```

Each world has its own specialist family. You can stay in one or
cross between them; the cross-world dependency is **strict one-way**:

```
probes  ──reads──▶  tasks   (via probe.yaml arms[])
tasks        ──reads──▶  (nothing about probes)
paper        ──reads──▶  probes (claims) + tasks (figures)
```


Quick start — your first end-to-end run
========================================

You are at the repo root. You want to train a CGM baseline model
and aggregate 3 seeds into one claim.

```bash
# 0. Activate env (always, per CLAUDE.md)
source .venv/bin/activate && source env.sh

# 1. Scaffold a project (if not exists)
/haipipe-project task project ProjA-Bench-1-FairGlucose

# 2. Scaffold a model-training task (cascade auto-creates group)
/haipipe-task training --auto \
    --project-id ProjA-Bench-1-FairGlucose \
    --group A01_pretraining_clm \
    --task 01_train_clm_baseline

# 3. Edit the scaffolded files
cd examples/ProjA-Bench-1-FairGlucose/tasks/A01_pretraining_clm/01_train_clm_baseline/
$EDITOR 01_train_clm_baseline.py            # fill in actual training code
$EDITOR configs/5_model_clm_baseline.yaml   # fill in real ModelArgs

# 4. Pre-flight: run the code reviewer (or skip with env var first time)
# Option A: real review
# (see Tools/plugins/haipipe-toolkit/skills/C_task/agents/reviewers/run-script-reviewer-agent.md)
# Option B: skip for first smoke run
HAIPIPE_SKIP_REVIEW=1 bash runs/5_model_clm_baseline_seed42.sh

# 5. After the run, task-log.md is auto-regenerated; inspect:
cat task-log.md

# 6. Run 2 more seeds (variants via new run.sh per seed)
bash runs/5_model_clm_baseline_seed7.sh
bash runs/5_model_clm_baseline_seed13.sh

# 7. Design an probe to compare the 3 seeds against an LHM arm
/haipipe-probe design new E01 \
    --title "CLM baseline reproducibility" \
    --hypothesis "MAE val < 25.0 across 3 seeds, paired-t p<0.05"

# 8. Link the 3 runs into the probe as the baseline arm
/haipipe-probe design link E01 \
    tasks/A01_pretraining_clm/01_train_clm_baseline/results/run_seed42 \
    tasks/A01_pretraining_clm/01_train_clm_baseline/results/run_seed7 \
    tasks/A01_pretraining_clm/01_train_clm_baseline/results/run_seed13

# 9. Aggregate stats and write the claim
/haipipe-probe result E01
/haipipe-probe review E01     # structural QA + Codex semantic verdict
```


5 common workflows
===================

Workflow A — Build a new dataset (data-pipeline task)
------------------------------------------------------

```bash
# orchestrator cascade builds project + group + task in one shot
/haipipe-task data --auto \
    --project-id ProjB-Bench-2-CGMBaseline \
    --group D01_data \
    --task 01_build_record_cgm5min_wellreadi

# specialist scaffolds {task}.py + configs/1_record_*.yaml + runs/*.sh
# then suggests next step:
#   next: /haipipe-data-record (to author the actual builder)
/haipipe-data-record

# author builder logic in code-dev/1-PIPELINE/2-Record-WorkSpace/
# then back to the task folder and run:
cd examples/ProjB-Bench-2-CGMBaseline/tasks/D01_data/01_build_record_cgm5min_wellreadi/
HAIPIPE_SKIP_REVIEW=1 bash runs/1_record_cgm5min_wellreadi.sh
# heavy data lands in _WorkSpace/2-RecStore/; task-log.md auto-updates
```

Workflow B — Smoke-test a new algorithm class
----------------------------------------------

```bash
# Track A: develop the algo class in code/hainn/<algo>/
/haipipe-nn-algo            # author or refine

# Track B: scaffold paired X_algo demo
/haipipe-task algo --auto \
    --project-id ProjC-Model-1-ScalingLaw \
    --task 01_test_te_clm_lhm

# tiny config (batch_size=1, max_steps=5) verifies the algo runs end-to-end
cd examples/ProjC-Model-1-ScalingLaw/tasks/X_algo/01_test_te_clm_lhm/
HAIPIPE_SKIP_REVIEW=1 bash runs/algo_te_clm_lhm_tiny.sh

# loss.json present + "didn't crash" → algo class is plumbed correctly
# now graduate to real training:
/haipipe-task training --auto ...
```

Workflow C — Evaluate a trained model
--------------------------------------

```bash
/haipipe-task eval --auto \
    --project-id ProjC-Model-1-ScalingLaw \
    --group B01_evaluation_clm \
    --task 01_eval_clm_h24 \
    --target-model clm_d128_l12/@v0007

# specialist seeds configs/eval_clm_h24.yaml with the target model pinned
# run it:
cd examples/ProjC-Model-1-ScalingLaw/tasks/B01_evaluation_clm/01_eval_clm_h24/
HAIPIPE_SKIP_REVIEW=1 bash runs/eval_clm_h24.sh
# metrics.json lands in results/run_*/; task-log.md shows headline
```

Workflow D — Make a paper figure
---------------------------------

```bash
/haipipe-task display --auto \
    --project-id ProjC-Model-1-ScalingLaw \
    --group C01_paper_figures \
    --task 01_main_figure_mae_vs_modelsize \
    --kind figure

# edit configs/figure_main.yaml to list source_runs (upstream eval results)
# run; .pdf + .png + source_data.csv land in results/<run>/
bash runs/figure_main.sh
```

Workflow E — Run a full probe (research thread)
-----------------------------------------------------

```bash
# 1. Design — declare hypothesis, planned arms, aggregation spec
/haipipe-probe design new E02 \
    --title "LHM-A architecture beats baseline on test-id" \
    --hypothesis "LHM-A MAE < baseline by ≥0.5, paired-t p<0.05, N=3"

# 2. Bridge — scaffold the arms as tasks in C_task and deploy
/haipipe-probe bridge E02
# (this auto-calls Skill("haipipe-task", "task-folder training ..."))

# 3. Wait for training; runs complete; results/<RUN>/metrics.json written

# 4. Link the runs back into the probe (bridge does this auto)
# (manual fallback: /haipipe-probe design link E02 <run-path>)

# 5. Aggregate
/haipipe-probe result E02         # mean/std/paired-t/sign

# 6. Review (structural QA + Codex semantic verdict)
/haipipe-probe review E02

# 7. Iterate if needed
/haipipe-probe loop E02           # review → propose → re-materialize
```


Auto mode (`--auto`)
=====================

Most orchestrators accept `--auto` to skip interactive ASK prompts:

```
--auto              one-off flag in args
CLAUDE_AUTO_HANDOFF=1   env var
AUTO_MODE=1             alternate env var
```

When AUTO is on, the orchestrator:
  - infers from cwd + keywords + args (Step 3a cascade)
  - auto-creates missing parents (project / task-group) if `--project-id`
    and `--group` are provided (Step 3b cascade)
  - returns `status: blocked` when a required input can't be inferred
    (instead of asking)

Without AUTO, the same orchestrator asks at every ambiguous step.
Use AUTO for batch / nightly / scripted; interactive for first-time.


Gotchas
========

1. **CODE_REVIEW.md gate blocks first runs.**
   Every `run.sh` checks for `<task>/CODE_REVIEW.md` (produced by the
   Run Script Reviewer agent). Without it, run.sh exits 2 immediately.
   Three ways to satisfy:

   - Run the reviewer agent (recommended for non-throwaway runs).
   - `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh` (env var, one run).
   - `_meta.skip_review: true` in `configs/<RUN>.yaml` (permanent for
     that config — only for throwaway / smoke tasks).

2. **Group letter must match task-type.**
   `/haipipe-task data` only scaffolds under a **D**-series group.
   Mismatch (e.g., trying to put data into A-series) → blocked in
   AUTO; warn + ASK in interactive.

   ```
   A=training  B=eval  C=display  D=data  E=individual  F=agent  X=algo
   ```

3. **Single-direction dependency: probes read tasks, never vice versa.**
   Don't write `probe.yaml` paths into task configs. Don't import
   task code from probe scripts (probes have no code at all).

4. **`results/` is for LIGHT artifacts only.**
   Heavy outputs (`.pt`, `.ckpt`, `.npy`, `.parquet > 1 MB`) belong in
   `_WorkSpace/{N}-*Store/`. `-inspect review` flags violations.

5. **Run-name pairing is mandatory.**
   `configs/<RUN>.yaml`, `runs/<RUN>.sh`, `results/<RUN>/`,
   `notebooks/<RUN>.ipynb` must all share the same `<RUN>` token.
   Renaming one = renaming all four.

6. **`.venv` + `env.sh` always.**
   `source .venv/bin/activate && source env.sh` before any Python
   command. `env.sh` sets `PYTHONPATH` to the current worktree (not
   main's editable install).

7. **`code/haifn/` is generated.**
   Never edit `code/haifn/` directly. Edit builders in
   `code-dev/1-PIPELINE/`, then run the builder.


Cheatsheet — scope × command
=============================

```
SCOPE          COMMAND                                              EFFECT
─────────────  ───────────────────────────────────────────────────  ──────────────────────
project        /haipipe-project task project new <ID>               scaffold project shell
project        /haipipe-project review <ID>                         structural audit
project        /haipipe-project organize <ID>                       reorganize files
project        /haipipe-project overview [<ID>]                     dashboard

task-group     /haipipe-task task-group <ID> --project-id <PROJ>    scaffold a group

task-folder    /haipipe-task <type> --auto                          orchestrator scaffold
               /haipipe-task-for-data    --auto                         direct, data-pipeline
               /haipipe-task-for-algo    --auto                         direct, X_algo smoke
               /haipipe-task-for-training --auto                        direct, A-series train
               /haipipe-task-for-eval     --auto                        direct, B-series eval
               /haipipe-task-for-display  --auto                        direct, C-series fig
               /haipipe-task-for-individual --auto                      direct, E individual
               /haipipe-task-for-agent   --auto                         direct, F LLM agent

run            bash runs/<NAME>.sh                                  execute a run
               HAIPIPE_SKIP_REVIEW=1 bash runs/<NAME>.sh            same, skip review

task observe   /haipipe-task-logging <task-path>                    regen task-log.md
               /haipipe-task-logging <task-path> --print            regen + cat

probe     /haipipe-probe design new <ID>                  declare new thread
               /haipipe-probe design link <ID> <run-path>      attach a run to an arm
               /haipipe-probe bridge <ID>                      scaffold arms + deploy
               /haipipe-probe result <ID>                      aggregate stats + claim
               /haipipe-probe review <ID>                      QA + Codex verdict
               /haipipe-probe explore                          coverage + propose next
               /haipipe-probe loop <ID>                        iterate until clean
               /haipipe-probe inspect [<ID>]                   list / status

paper          /paper-workflow / /paper-figure / ...                see F_paper section
```


Where to go deeper
===================

```
What is this toolkit                         README.md (this folder)
Project layout, 3 worlds                     skills/B_project/haipipe-project/SKILL.md
Task ↔ probe boundary                   skills/D_probe/MENTAL_MODEL.md  ⭐
Task hierarchy + naming                      skills/C_task/haipipe-task/ref/hierarchy.md
Task-type series design                      skills/C_task/DESIGN.md
runtime.yaml schema                          skills/C_task/haipipe-task/ref/runtime-yaml-schema.md
task-log.md (per-task observability)         skills/C_task/haipipe-task-logging/SKILL.md
Run.sh wrapper internals                     skills/C_task/haipipe-task/ref/run-sh-template.sh
probe.yaml schema                       skills/D_probe/ref/probe-yaml-schema.md
Bridge skill (D ↔ C connector)               skills/D_probe/haipipe-probe-bridge/SKILL.md
Pipeline (Stages 1-4)                        skills/1_data/haipipe-data/SKILL.md
Pipeline (Stage 5 NN)                        skills/2_nn/haipipe-nn/SKILL.md
Pipeline (Stage 6 endpoints)                 skills/3_end/haipipe-end/SKILL.md
Per-individual contract (Stages 0-2)            skills/4_individual/haipipe-individual/SKILL.md
Run Script Reviewer (pre-flight agent)       skills/C_task/agents/reviewers/run-script-reviewer-agent.md
```


One-line rules of thumb
========================

```
New code?              → tasks/
New claim?             → probes/
New plot?              → tasks/display/  (referenced from probe.yaml evidence:)
New hypothesis?        → probes/<NN>/probe.yaml
New metric value?      → tasks/.../metrics.json
New per-run record?    → tasks/.../runtime.yaml (atomic, by run.sh)
New cross-run stat?    → probes/<NN>/probe.yaml result: (via result aggregate)
New "why it failed"?   → probes/<NN>/logs/<DATE>.md
New individual view?      → tasks/individual/  (E-series)
New LLM agent task?    → tasks/agent/  (F-series)
First run after scaffold? → HAIPIPE_SKIP_REVIEW=1, or run reviewer agent first
```
