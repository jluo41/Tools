---
name: haipipe-experiment
description: "Research probe pipeline — drives how tasks/runs in a project roll out. Each probe/experiment is a claim-directed research thread: design (hypothesis + planned arms), bridge (scaffold tasks/runs in C_task), result (harvest arms → claim), review (structural QA + Codex semantic verdict), explore (coverage + propose next), loop (review→propose→materialize→re-review). Contains no code — pure steering layer on top of C_task execution. Feeds F_paper. Trigger: probe, experiment, claim, hypothesis, drive experiment, plan next runs, aggregate runs, statistical test, paired-t, coverage, propose next experiment, review-loop, iterate until claim holds, implement the plan, deploy experiments, /haipipe-experiment."
argument-hint: [function] [experiment_id_or_path] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-experiment (orchestrator)
=========================================

User-facing entry for the **research probe pipeline**.

Naming note: the command and folder remain `/haipipe-experiment` and
`experiments/` for compatibility. Conceptually this layer is
**D_probe**: each experiment folder is a focused probe that asks reality
whether a candidate claim or story direction survives contact with
evidence.

Two pipelines live side-by-side in a project; this skill owns the
research side and never crosses into execution:

```
EXECUTION PIPELINE          (C_task)
  task / run = 做什么、怎么做
  artifacts:  code, notebooks, configs, runtime.yaml, metrics.json
  question:   "this run, did it work?"

RESEARCH PROBE PIPELINE     (D_probe ← this skill; folder name D_experiment)
  probe      = 朝哪个方向探索、为什么做、接下来做什么
  artifacts:  experiment.yaml, daily logs, review.md, claim
  question:   "across these runs, does the hypothesis hold?"
```

An **experiment is a probe thread**, not a claim repository. It
steers how tasks and runs roll out: defines hypothesis → bridges plan
into C_task tasks → harvests arms → judges → proposes next move →
iterates. It contains NO code, NO notebooks, NO metrics computation;
all that lives in `tasks/`. It only holds **steering state** (plan +
links + verdict + narrative).

The two pipelines have a strict one-way dependency: experiments read
task artifacts and link to them; tasks never reference experiments.

```
/haipipe-experiment                                -> dashboard (list expmts)
/haipipe-experiment design <ID>                    -> define new experiment
/haipipe-experiment link <ID> <run-path>           -> link a run to an arm
/haipipe-experiment result <ID>                    -> aggregate + claim
/haipipe-experiment review <ID>                    -> structural QA gate
/haipipe-experiment review integrity <ID>          -> Codex fraud-pattern audit
/haipipe-experiment review claim <ID>              -> Codex semantic verdict
/haipipe-experiment bridge <ID>                    -> scaffold arms in C_task + deploy
/haipipe-experiment explore [project-path]         -> coverage map + propose
/haipipe-experiment loop <ID>                      -> iterate review→propose→materialize
/haipipe-experiment inspect [<ID> | <project>]     -> list / status / audit
/haipipe-experiment "<natural language>"           -> infer, dispatch
```

---

Specialists
-----------

```
haipipe-experiment-design       PRE-RUN:  new / link arms (defines what to test)
haipipe-experiment-bridge       BRIDGE:   scaffold arms as tasks in C_task + deploy
haipipe-experiment-result       POST-RUN: aggregate stats + write claim
haipipe-experiment-review       QA:       structural checks + Codex claim verdict
haipipe-experiment-explore      META:     coverage map + propose next
haipipe-experiment-loop         ITERATE:  chain review→propose→materialize→re-review
haipipe-experiment-inspect      READ:     list / status / audit (no writes)
```

---

Function Verb Map
------------------

```
new, define, create, design, hypothesis           -> design (new)
link, attach, add run, assign run                 -> design (link)
bridge, deploy, scaffold, materialize, implement,
make-runnable, run the plan, 实现实验, 部署        -> bridge
aggregate, compute, mean+std, paired-t            -> result (aggregate)
claim, conclude, write statement                  -> result (claim)
review, qa, quality check                         -> review (structural)
audit, integrity, fraud, fake-GT, phantom results,
honesty check, scope check, leakage check         -> review (integrity)
verdict, judge, supports?, semantic check         -> review (claim)
explore, coverage, gap, propose, suggest          -> explore
loop, iterate, until passes, auto-review-loop,
review-loop, keep improving                       -> loop
inspect, list, status, show experiments           -> inspect
```

---

Files Owned by This Umbrella
-----------------------------

```
SKILL.md                       (this file)
ref/                           shared across specialists:
  experiment-yaml-schema.md    experiment.yaml field spec
  experiment-entry-template.txt  per-experiment entry template (project log)
  experiment-headline-template.txt headline scoreboard skeleton
  experiment-caveats-checklist.txt 8+ confound categories
  _legacy-scope-expmt.md       migrated content reference
```


Where experiments live (project-level)
---------------------------------------

```
examples/Proj-X/
├── experiments/                            ← project-level folder
│   ├── INDEX.md                            (auto: list all experiments)
│   ├── coverage.md                         (auto: /explore coverage output)
│   ├── propose.md                          (auto: /explore propose output)
│   ├── comparison.md                       (auto: /result render output)
│   │
│   ├── 01_baseline_noise_floor/            ← folder-per-experiment
│   │   ├── experiment.yaml                 source of truth (claim + arms + result)
│   │   ├── review.md                       latest QA + Codex verdict (overwritten)
│   │   ├── CLAIMS_FROM_RESULTS.md          Codex verdict snapshot
│   │   └── logs/                           daily narrative
│   │       ├── 2026-05-24.md
│   │       └── 2026-05-25.md
│   │
│   └── 02_lhm_vs_baseline/
│       └── ...
│
├── tasks/...                               (execution, C_task owns)
└── paper/...                               (claims feed F_paper)
```

Naming: `<NN>_<slug>/` (2-digit, no gap on creation, snake_case slug).
`experiment.yaml` is **source of truth**; `comparison.md` and `INDEX.md`
are derived; `logs/<DATE>.md` is append-only daily narrative.
NO code in experiment folders — figures/tables/notebooks live in tasks/
and are referenced via `evidence:` field in experiment.yaml.


Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve verb -> specialist via verb map.
Step 3: Validate target (experiment ID or project path).
Step 4: Dispatch: Skill("haipipe-experiment-<specialist>", args="<verb> <rest>").
Step 5: Surface specialist tail.
```


Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences
artifacts: [paths created / read]
next:      suggested next command (often inspect or explore)
```


Relation to other top-level skills
-----------------------------------

```
A_discover    feeds ideas  → suggested experiments
C_task     provides runs → linked into experiment arms
E_insight        consumes claims → analysis methodology
F_paper       consumes claims → paper writing

D_probe is the central hub: reads from B, writes claims that
feed both E_insight (analysis) and F_paper (writing).
```
