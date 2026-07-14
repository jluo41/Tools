haipipe-toolkit — Usage Guide
==============================

Practical guide to USING the toolkit. For an inventory of what skills exist see `README.md`. For the probe contract see `skills/probe/haipipe-probe/SKILL.md` (the constitution) and `ARCHITECTURE.md` (the whole model). This file is the workflow recipe book — concrete commands, common flows, gotchas.


The 4 worlds — one project, four folders
=========================================

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/
│
├── ⚙️ tasks/         ← the WORK      (task)        code + runs + metrics + QA/ digests
├── 🔎 discoveries/   ← the EVIDENCE  (discovery)   sources + verdicts + QA/ digests
├── 📄 papers/        ← the STORY     (paper)       manuscripts + 1-probes/ + 1-claims.md
└── 📬 applications/  ← the DELIVERY  (application) reports / messages / UI
```

`tasks/` + `discoveries/` are the two EXECUTORS — same shape, same rules. Together they are the
project's evidence BANK. `papers/` + `applications/` are the CONSUMERS.

The cross-world dependency is **strict one-way**, and the arrow is a PATH:

```
paper / application  ──reads──▶  tasks/ + discoveries/    via a probe section's `target:`
                                                          (a PATH to a <leaf>/QA/<n>-<slug>.md)
tasks / discoveries  ──reads──▶  NOTHING about papers.    The bank is PROBE-UNAWARE:
                                                          no _ASK/, no _ANS/, no answers:,
                                                          no PP id, ever.
```

**Two session modes.** The LEFT (executor) session just runs Plan→Build→Execute→Report for its
own sake — no questions, no asks. The bank grows autonomously. The RIGHT (consumer) session is
the one that asks. So in a healthy project most answers ALREADY EXIST before a paper asks for
them: a commission is the exception, not the norm.


Quick start — your first end-to-end run
========================================

You are at the repo root. You want to train a CGM baseline model across 3 seeds and leave the bank able to answer "is the baseline reproducible?".

```bash
# 0. Activate env (always, per CLAUDE.md)
source .venv/bin/activate && source env.sh

# 1. Scaffold a project (if not exists)
#    ProjX-* = plain dir under examples/    ·    /haipipe-project repo Project-* = repo-backed
/haipipe-project new ProjA-Bench-1-FairGlucose

# 2. Scaffold a model-fit task (cascade auto-creates group). Type is `fit` — "training" is an alias.
/haipipe-task fit --auto \
    --project-id ProjA-Bench-1-FairGlucose \
    --group A01_pretraining_clm \
    --task 01_train_clm_baseline

# 3. Edit the scaffolded files
cd examples/ProjA-Bench-1-FairGlucose/tasks/A01_pretraining_clm/01_train_clm_baseline/
$EDITOR 01_train_clm_baseline.py            # fill in actual training code
$EDITOR configs/5_model_clm_baseline.yaml   # fill in real ModelArgs

# 4. Pre-flight: run the task reviewer (or skip with env var first time)
# Option A: real review
# (see Tools/plugins/haipipe-toolkit/skills/task/agents/haipipe-task-reviewer-agent.md)
# Option B: skip for first smoke run
HAIPIPE_SKIP_REVIEW=1 bash runs/5_model_clm_baseline_seed42.sh

# 5. After the run, task-log.md is auto-regenerated; inspect:
cat task-log.md

# 6. Run 2 more seeds (variants via new run.sh per seed)
bash runs/5_model_clm_baseline_seed7.sh
bash runs/5_model_clm_baseline_seed13.sh

# 7. Ask the leaf a question. It answers from results/ if it can (depth 0),
#    and writes a READABLE digest either way.
/haipipe-task qa "Across the 3 baseline seeds, what is the val MAE mean/std, and is the
                  seed-to-seed spread smaller than the gap to the LHM arm?" \
              A01_pretraining_clm/01_train_clm_baseline

#    → returns tasks/A01_pretraining_clm/01_train_clm_baseline/QA/1-baseline-seed-spread.md
#      # Q — <the question>  ##Answer [→ results/…]  ##Caveats  ##Not-done
#      That file is now the bank's answer, general and reusable — no paper owns it.

# 8. (later, in a PAPER session) a claim needs that number.
#    The paper's PROBE phase opens a section in papers/<P>/1-probes/PP02_baseline.md:
#       - serves: 1-claims (C3)
#       - target: tasks/A01_pretraining_clm/01_train_clm_baseline/QA/1-baseline-seed-spread.md
#       - state:  answered           ← DERIVED: the QA file exists
#       - reading: "spread 0.3 ≪ 1.1 gap ⇒ C3 supported"
#    T2 REUSE: one grep + one read. Nothing re-runs. This is the NORMAL case.
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
# now graduate to a real training run (type = fit):
/haipipe-task fit --auto ...
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

Workflow E — A paper needs evidence it does not have (the probe loop)
---------------------------------------------------------------------

The five steps run INSIDE a paper stage's PROBE phase. You normally invoke the stage skill, not
these steps by hand — this is what it does under the hood.

```text
📝 DRAFT   the claims stage leaves a GAP: "does LHM-A beat baseline on test-id?"
              │
① ORGANIZE  the Q-paper lands as a SECTION in papers/<P>/1-probes/PP05_lhm-arch.md
              │   ## Why  🔒  "H2 dies if the gain is inside the seed noise."   ← NEVER LEAVES
              │   ## Q1   serves: 1-claims (C4)
              │           commission: |            ← T1: the stake is STRIPPED OUT
              │             Compare LHM-A vs the CLM baseline on the test-id split,
              │             N=3 paired seeds, same schedule. Report per-seed MAE, the
              │             paired difference, and its spread.
              │             Accepted: any direction — magnitude is NOT yours to judge.
              ▼
② MATCH     grep {tasks,discoveries}/**/QA/*.md   ← MATCH ON THE ANSWER, never the topic.
            READ the candidate QA file. A similar-sounding leaf that does not literally
            answer this question is a MISS, not a hit.
              ├─ ✅ a QA file answers it   → T2 REUSE. Point at it. STOP. (the normal case)
              └─ 🔴 nothing                → ③
              ▼
③ DISPATCH  hand the `commission` block, VERBATIM, and NOTHING ELSE:
              Agent(haipipe-task-orchestrator-agent)      ← runs / code
              Agent(haipipe-discovery-orchestrator-agent) ← literature
            Their CLEAN CONTEXT is the wall. Never send ## Why. Never send the probe file.
            Inside, the orchestrator runs the qa gate (① scan ② digest ③ P-B-E-R) and picks
            the shallowest depth that answers it (read | new run | new script | new leaf).
            You never learn which. It returns ONE thing: a PATH.
              ▼
④ POINT     target: tasks/B01_evaluation_clm/03_lhm_vs_baseline/QA/2-lhm-paired-delta.md
              ▼
⑤ INTERPRET reading: |    ← T2: the stake goes back IN
              paired Δ = −0.7 ± 0.2 over 3 seeds ⇒ outside seed noise ⇒ C4 supported.
            → 1-claims.md flips C4 (status + confidence + claim_type live THERE, not here)
```

🚫 What you must NOT do in a paper session: open `results/`, run the analysis inline, and write
the digest yourself. That is LAW 1 broken. The probe CAUSES a QA file; the EXECUTOR AUTHORS it.
If the results already exist but there is no readable digest, DISPATCH a digest-only run — a
clean-context agent reads `results/` and writes the QA file. No code runs. It is cheap.


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
  - auto-creates missing parents (project / task-group) if `--project-id` and `--group` are provided (Step 3b cascade)
  - returns `status: blocked` when a required input can't be inferred (instead of asking)

Without AUTO, the same orchestrator asks at every ambiguous step. Use AUTO for batch / nightly / scripted; interactive for first-time.


Gotchas
========

1. **CODE_REVIEW.md gate blocks first runs.**
   Every `run.sh` checks for `<task>/CODE_REVIEW.md` (produced by the Run Script Reviewer agent). Without it, run.sh exits 2 immediately. Three ways to satisfy:

   - Run the reviewer agent (recommended for non-throwaway runs).
   - `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh` (env var, one run).
   - `_meta.skip_review: true` in `configs/<RUN>.yaml` (permanent for that config — only for throwaway / smoke tasks).

2. **Group letters are PROJECT-specific — never infer task-type from one.**
   `A01_`, `B01_`, `C01_` are organizational prefixes, NOT type indicators. Each project defines its own scheme, and **the project's existing scheme always wins**. Type is detected from script content or from the explicit type arg — never from the letter (`haipipe-task/SKILL.md:40`, `:294`).

   The letters below are only the **DEFAULT** a specialist picks for a project with no scheme yet:

   ```
   data D · fit A · eval B · display C · individual E · agent F · raw R · algo X_algo
   ```

3. **Single-direction dependency: a paper reads the bank, never vice versa.**
   Never write a paper path, a PP id, a claim id (`C4`), or a hypothesis id (`H2`) into anything
   under `tasks/` or `discoveries/`. The bank is PROBE-UNAWARE (no `_ASK/`, no `_ANS/`, no
   `answers:` field). A QA file that says "claims-stage" or "the paper" has been contaminated —
   the evidence comes back paper-shaped and the next paper inherits the first one's frame.

4. **`results/` is for LIGHT artifacts only.**
   Heavy outputs (`.pt`, `.ckpt`, `.npy`, `.parquet > 1 MB`) belong in `_WorkSpace/{N}-*Store/`. Nothing audits this automatically — the project-audit skills are retired; it is a review-time convention.

5. **Run-name pairing is mandatory.**
   `configs/<RUN>.yaml`, `runs/<RUN>.sh`, `results/<RUN>/`, `notebooks/<RUN>.ipynb` must all share the same `<RUN>` token. Renaming one = renaming all four.

6. **`.venv` + `env.sh` always.**
   `source .venv/bin/activate && source env.sh` before any Python command. `env.sh` sets `PYTHONPATH` to the current worktree (not main's editable install).

7. **`code/haifn/` is generated.**
   Never edit `code/haifn/` directly. Edit builders in `code-dev/1-PIPELINE/`, then run the builder.


Cheatsheet — scope × command
=============================

```
SCOPE          COMMAND                                              EFFECT
─────────────  ───────────────────────────────────────────────────  ──────────────────────
project        /haipipe-project new <ProjX-ID>                      scaffold plain project shell
project        /haipipe-project repo <Project-ID> [--org <owner>]   scaffold repo-backed project
project        /haipipe-project                                     list projects + the 2 setup paths
                 (review / organize / overview are RETIRED — originals in skills/project/_archive/)

task-group     /haipipe-task task-group <ID> --project-id <PROJ>    scaffold a group

task-folder    /haipipe-task <type> --auto                          orchestrator scaffold
                 types: data · raw · algo · fit · eval · display · individual · agent · endpoint
               /haipipe-task-for-data       --auto                      direct, data pipeline
               /haipipe-task-for-raw        --auto                      direct, raw ingest
               /haipipe-task-for-algo       --auto                      direct, X_algo smoke
               /haipipe-task-for-fit        --auto                      direct, model fit / training / sweep
               /haipipe-task-for-eval       --auto                      direct, evaluation
               /haipipe-task-for-display    --auto                      direct, figure / table
               /haipipe-task-for-individual --auto                      direct, per-individual
               /haipipe-task-for-endpoint   --auto                      direct, endpoint package
               /haipipe-task-for-stata      --auto                      direct, Stata engine
               /haipipe-task-for-agent      --auto                      direct, LLM agent

run            bash runs/<NAME>.sh                                  execute a run
               HAIPIPE_SKIP_REVIEW=1 bash runs/<NAME>.sh            same, skip review

task report    /haipipe-task report <task-path>                     summarize runtime + metrics
               cat <task-path>/workflow/report.yaml                 inspect task report

qa (bank)      /haipipe-task qa "<question>" [<leaf>]               ask the task bank
               /haipipe-discovery qa "<question>" [<leaf>]          ask the discovery bank
                 ① QA scan  ② digest from existing artifacts  ③ P-B-E-R  🚫 refuse
                 → returns <leaf>/QA/<n>-<slug>.md   ·   `ls <leaf>/QA/` IS the index
                 general language only: no PP id, no claim id, no stake

probe (paper)  /haipipe-probe                                       the contract, one screen
               /haipipe-probe contract | anatomy                    probe-file + QA/ anatomy
               /haipipe-probe status                                derive states from disk
               /haipipe-probe "<question>"                          ROUTES to the qa verb;
                                                                    runs no bank work itself

paper          /haipipe-paper enter <paper-path>                    open-needs dashboard
               /haipipe-paper status                                lifecycle frontier
```

💀 DELETED — do not use, do not resurrect: `/haipipe-probe design|link|bridge|result|review|
explore|loop|inspect` (the probe.yaml era) · `/haipipe-task asks` (the probe-aware verb, reborn
as `qa`) · `Agent(haipipe-probe-orchestrator-agent)` (the gateway; dispatch is now a direct
`Agent()` call on the task/discovery orchestrators).


Where to go deeper
===================

```
What is this toolkit                         README.md (this folder)
The whole model (KB ⇄ delivery, the probe)   ARCHITECTURE.md               ⭐ read first
The probe CONSTITUTION                       skills/probe/haipipe-probe/SKILL.md  ⭐ the contract
The design of record (rulings R1-R18)        Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/
Claim judging (G1/G2/G3)                     skills/probe/haipipe-probe-review/SKILL.md
Project layout, the 4 worlds                 skills/project/haipipe-project/SKILL.md
Task hierarchy + naming                      skills/task/haipipe-task/ref/hierarchy.md
Task-type series design                      skills/task/DESIGN.md
runtime.yaml schema                          skills/task/haipipe-task/ref/runtime-yaml-schema.md
task report (per-task observability)         skills/task/haipipe-task/fn/workflow-report.md
Run.sh wrapper internals                     skills/task/haipipe-task/ref/run-sh-template.sh
the qa verb (task side)                      skills/task/haipipe-task/fn/qa.md
the qa verb (discovery side)                 skills/discovery/haipipe-discovery/ (the twin)
Pipeline (Stages 1-4)                        skills/task/1_data/haipipe-data/SKILL.md
Pipeline (Stage 5 NN)                        skills/task/2_nn/haipipe-nn/SKILL.md
Pipeline (Stage 6 endpoints)                 skills/task/3_end/haipipe-end/SKILL.md
Per-individual contract (Stages 0-2)         skills/task/4_individual/haipipe-individual/SKILL.md
Task Reviewer (pre-flight agent)             skills/task/agents/haipipe-task-reviewer-agent.md
```


One-line rules of thumb
========================

```
New code?                 → tasks/<leaf>/
New literature?           → discoveries/<leaf>/
New plot?                 → tasks/ (C-series display task)
New metric value?         → tasks/.../results/<run>/metrics.json
New per-run record?       → tasks/.../runtime.yaml (atomic, by run.sh)
New READABLE answer?      → tasks|discoveries/<leaf>/QA/<n>-<slug>.md   ← the executor writes it
New question (as a human)?→ /haipipe-task qa "…"  ·  /haipipe-discovery qa "…"
New question (from a paper)? → a SECTION in papers/<P>/1-probes/PPNN_<topic>.md, then DISPATCH
New hypothesis / claim?   → papers/<P>/0-lifecycle/1-claims/1-claims.md   (never the bank)
The stake / why it matters? → the probe file's ONE `## Why`. It never leaves that file.
New individual view?      → tasks/individual/  (E-series)
New LLM agent task?       → tasks/agent/  (F-series)
First run after scaffold? → HAIPIPE_SKIP_REVIEW=1, or run reviewer agent first
```
