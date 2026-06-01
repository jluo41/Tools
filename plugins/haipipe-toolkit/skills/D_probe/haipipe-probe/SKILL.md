---
name: haipipe-probe
description: "Research probe pipeline — drives how tasks/runs in a project roll out. Each probe is a claim-directed research thread: design (hypothesis + planned arms), bridge (scaffold tasks/runs in C_task), result (harvest arms → claim), review (structural QA + Codex semantic verdict), explore (coverage + propose next), loop (review→propose→materialize→re-review). Contains no code — pure steering layer on top of C_task execution. Feeds F_paper. Trigger: probe, claim, hypothesis, drive probe, plan next runs, aggregate runs, statistical test, paired-t, coverage, propose next probe, review-loop, iterate until claim holds, implement the plan, deploy probes, /haipipe-probe."
argument-hint: [function] [probe_ref_or_path] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-01"
  summary: "Research probe pipeline — drives how tasks/runs in a project roll out."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): document lightweight probe folder naming (`MM-NN_slug`) plus year archive folders."
    - "1.2.0 (2026-06-01): probe folder naming switches to date-based `MMDD_slug` + `P.MMDD` refs (same-day collisions get a letter suffix)."
---

Skill: haipipe-probe (orchestrator)
=========================================

User-facing entry for the **research probe pipeline**.

Naming note: the command and folder remain `/haipipe-probe` and
`probes/` for compatibility. Conceptually this layer is
**D_probe**: each probe folder is a focused probe that asks reality
whether a candidate claim or story direction survives contact with
evidence.

Two pipelines live side-by-side in a project; this skill owns the
research side and never crosses into execution:

```
EXECUTION PIPELINE          (C_task)
  task / run = 做什么、怎么做
  artifacts:  code, notebooks, configs, runtime.yaml, metrics.json
  question:   "this run, did it work?"

RESEARCH PROBE PIPELINE     (D_probe ← this skill; project folder probes/)
  probe      = 朝哪个方向探索、为什么做、接下来做什么
  artifacts:  probe.yaml, daily logs, review.md, claim
  question:   "across these runs, does the hypothesis hold?"
```

A **probe is a research thread**, not a claim repository. It
steers how tasks and runs roll out: defines hypothesis → bridges plan
into C_task tasks → harvests arms → judges → proposes next move →
iterates. It contains NO code, NO notebooks, NO metrics computation;
all that lives in `tasks/`. It only holds **steering state** (plan +
links + verdict + narrative).

The two pipelines have a strict one-way dependency: probes read
task artifacts and link to them; tasks never reference probes.

```
/haipipe-probe                                -> dashboard (list probes)
/haipipe-probe design new <slug>              -> define new probe folder
/haipipe-probe design link <probe> <run-path> -> link a run to an arm
/haipipe-probe result <probe>                 -> aggregate + claim
/haipipe-probe review <probe>                 -> structural QA gate
/haipipe-probe review integrity <probe>       -> Codex fraud-pattern audit
/haipipe-probe review claim <probe>           -> Codex semantic verdict
/haipipe-probe bridge <probe>                 -> scaffold arms in C_task + deploy
/haipipe-probe explore [project-path]         -> coverage map + propose
/haipipe-probe loop <probe>                   -> iterate review→propose→materialize
/haipipe-probe inspect [<probe> | <project>]  -> list / status / audit
/haipipe-probe "<natural language>"           -> infer, dispatch
```

---

Specialists
-----------

```
haipipe-probe-design       PRE-RUN:  new / link arms (defines what to test)
haipipe-probe-bridge       BRIDGE:   scaffold arms as tasks in C_task + deploy
haipipe-probe-result       POST-RUN: aggregate stats + write claim
haipipe-probe-review       QA:       structural checks + Codex claim verdict
haipipe-probe-explore      META:     coverage map + propose next
haipipe-probe-loop         ITERATE:  chain review→propose→materialize→re-review
haipipe-probe-inspect      READ:     list / status / audit (no writes)
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
inspect, list, status, show probes           -> inspect
```

---

Files Owned by This Umbrella
-----------------------------

```
SKILL.md                       (this file)
ref/                           shared across specialists:
  probe-yaml-schema.md    probe.yaml field spec
  probe-entry-template.txt  per-probe entry template (project log)
  probe-headline-template.txt headline scoreboard skeleton
  probe-caveats-checklist.txt 8+ confound categories
  _legacy-scope-expmt.md       migrated content reference (read-only)
```


Where probes live (project-level)
---------------------------------------

```
examples/Proj-X/
├── probes/                            ← project-level folder
│   ├── INDEX.md                            (auto: list all probes)
│   ├── coverage.md                         (auto: /explore coverage output)
│   ├── propose.md                          (auto: /explore propose output)
│   ├── comparison.md                       (auto: /result render output)
│   │
│   ├── 0601_framing_loss-aversion/        ← active folder-per-probe
│   │   ├── probe.yaml                      source of truth (claim + arms + result)
│   │   ├── review.md                       latest QA + Codex verdict (overwritten)
│   │   ├── CLAIMS_FROM_RESULTS.md          Codex verdict snapshot
│   │   └── logs/                           daily narrative
│   │       ├── 2026-06-01.md
│   │       └── 2026-06-02.md
│   │
│   ├── 0602_simplification_plain-language/
│   │   └── ...
│   │
│   └── 2026-archive/                       inactive/completed/deprecated probes
│       ├── 0501_social-norm/
│       └── 0502_long-message/
│
├── tasks/...                               (execution, C_task owns)
└── paper/...                               (claims feed F_paper)
```

Naming: active probe folders live directly under `probes/` as
`<MMDD>_<short-name>/`, where `MMDD` is the creation date (`MM` = month,
`DD` = day). A second probe created the same day gets the next free
lowercase letter suffix (`0601` → `0601b`). The canonical source ref is
`P.<MMDD>` (e.g. `P.0601`). Inactive, completed, or deprecated probes
move to `probes/<YYYY>-archive/` with the original folder name preserved.
`probe.yaml` is **source of truth**; `comparison.md` and `INDEX.md`
are derived; `logs/<DATE>.md` is append-only daily narrative.
NO code in probe folders — figures/tables/notebooks live in tasks/
and are referenced via `evidence:` field in probe.yaml.

Probe identity contract:

```
folder:             probes/0601_framing_loss-aversion/
source of truth:    probes/0601_framing_loss-aversion/probe.yaml
yaml id:            P.0601
mixed source refs:  P.0601
resolver accepts:   P.0601 | 0601 | probes/0601_framing_loss-aversion/
```

Legacy grouped layouts such as
`probes/A_baseline_controls/01_lhm_vs_baseline/` may be read during
migration, but new probe folders should use the lightweight active/archive
layout.


Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve verb -> specialist via verb map.
Step 3: Validate target (probe ref/folder/path or project path).
Step 4: Dispatch: Skill("haipipe-probe-<specialist>", args="<verb> <rest>").
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
A_discover    feeds ideas  → suggested probes
C_task     provides runs → linked into probe arms
E_insight        consumes claims → analysis methodology
F_paper       consumes claims → paper writing

D_probe is the central hub: reads from B, writes claims that
feed both E_insight (analysis) and F_paper (writing).
```
