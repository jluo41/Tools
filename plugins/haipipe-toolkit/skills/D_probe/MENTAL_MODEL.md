D_probe ↔ C_task — Mental Model
=================================

Onboarding doc. Read this BEFORE writing your first probe / probe, or
when something feels like it could go in either tasks/ or probes/
and you're not sure which.

Naming note: the current folder and command names still say
`D_probe`, `probes/`, and `/haipipe-probe` for
compatibility. Conceptually, this layer is **D_probe**: a
claim-directed probe that asks reality a focused question.


TL;DR
=====

```
C_task    =  DO     layer   "did this run work?"
D_probe   =  MEAN   layer   "across these runs, does the hypothesis hold?"
                          "what did this probe teach us?"

bridge skill (D → C):  scaffold probe arms as tasks
arms[] pointer (D → C):  probe reads tasks' metrics.json
tasks NEVER reference probes.
```

If you can ask **"did this run work?"** about something, it's a task.
If you can ask **"does this hypothesis / story direction survive contact
with reality?"** about it, it's a probe.


The two pipelines, side by side
================================

```
╔═══════════════════════════════════════════╗  ╔══════════════════════════════════════════╗
║  C_task — EXECUTION                       ║  ║  D_probe — RESEARCH                      ║
║                                           ║  ║                                          ║
║  unit:        task / run                   ║  ║  unit:        probe (research thread)     ║
║  asks:        "did THIS run work?"        ║  ║  asks:        "does the HYPOTHESIS hold ║
║                                           ║  ║                across these runs?"       ║
║                                           ║  ║                                          ║
║  artifacts:   code (*.py)                  ║  ║  artifacts:   probe.yaml             ║
║               configs/<RUN>.yaml           ║  ║               review.md                  ║
║               runs/<RUN>.sh                ║  ║               CLAIMS_FROM_RESULTS.md     ║
║               results/<RUN>/runtime.yaml   ║  ║               logs/<DATE>.md (daily)      ║
║               results/<RUN>/metrics.json   ║  ║                                          ║
║               notebooks/<RUN>.ipynb        ║  ║                                          ║
║               task-log.md (derived)        ║  ║                                          ║
║                                           ║  ║                                          ║
║  location:    examples/Proj-X/tasks/...    ║  ║  location:    examples/Proj-X/probes║
║                                           ║  ║                                          ║
║  has code?    YES — *.py runs, helpers     ║  ║  has code?    NO — pure steering state    ║
║                                           ║  ║                                          ║
║  mood:        "how / what / when"          ║  ║  mood:        "why / what next"          ║
║                                           ║  ║                "what did reality answer?"║
╚═══════════════════════════════════════════╝  ╚══════════════════════════════════════════╝
```


The 4 boundary rules
=====================

```
Rule 1 — probes/ folder has NO code, NO notebook, NO metric calculation.
         All computation lives in tasks/. Probes only hold
         steering state (plan + verdict + narrative).

Rule 2 — probe.yaml is STEERING state, not a result archive.
         result: block holds *aggregated references* to per-run
         metrics that physically live in tasks/.../metrics.json.

Rule 3 — Strict one-way dependency: probes READ tasks; tasks
         do NOT reference probes.
         - Delete an probe → no impact on tasks.
         - Delete a task → linked probe becomes invalid (caught by review).

Rule 4 — Tasks are ATOMIC; probes COMPOSE.
         - A single task/run can be referenced by multiple probes
           (as a member of different arms in different threads).
         - An probe cites multiple runs across multiple tasks.
```


The bridge — only one direction crosses C ↔ D
================================================

```
D_probe side                             C_task side
─────────────────                       ──────────────
 probe.yaml                         tasks/A01_*/
   arms:                                   ├── 01_pretrain_baseline/
     baseline: []   ← placeholder          │   ├── configs/run_seed42.yaml
     lhm:      []                          │   ├── runs/run_seed42.sh
                                           │   └── results/run_seed42/
                                           │       ├── runtime.yaml ─────┐
                                           │       └── metrics.json ────┐│
                                           └── 02_pretrain_lhm/         ││
                                               └── ...                  ││
                                                                        ││
   ① bridge skill (D → C, only direction):                              ││
        Skill("haipipe-task", "task-folder training ...")               ││
      scaffolds the arms as C_task tasks                                ││
                                                                        ││
   ② design link (D side only, after runs complete):                    ││
        arms.baseline.append("tasks/A01/01_pretrain_baseline/...")      ││
        arms.lhm     .append("tasks/A01/02_pretrain_lhm/...")           ││
                                                                        ││
   ③ result aggregate (D reads C via arms[] pointers):                  ││
        for arm in arms:                                                ││
            for run in arm:                                             ││
                metric = read(run/results/.../metrics.json) ◀───────────┘│
        write result: block in probe.yaml                           │
                                                                         │
   ④ review reads everything (D side only):                              │
        validates result: matches metrics ◀─────────────────────────────┘
        writes review.md + CLAIMS_FROM_RESULTS.md
```

Tasks never know an probe is reading them. They produce their
own metrics; the probe is just a downstream consumer.


One probe, full lifecycle
=========================

```
[t=0]  💡 Researcher has a question: "does architecture X beat baseline?"
         This is a probe: a focused kick at reality.
         │
[t=1]  📐 /haipipe-probe design new E02
         │   writes probes/02_x_vs_baseline/probe.yaml
         │     - hypothesis, claim_target
         │     - arms.baseline = []  (placeholder)
         │     - arms.x        = []  (placeholder)
         │     - aggregation spec (metric, statistic, noise_floor)
         │
[t=2]  🌉 /haipipe-probe bridge E02
         │   for each arm:
         │     Skill("haipipe-task", "task-folder training arm-baseline-seed42")
         │     Skill("haipipe-task", "task-folder training arm-x-seed42")
         │     ... (one task-folder per arm × seed)
         │   sanity arm runs first, then deploy rest
         │   ── C_task side now has 6 task-folders with run.sh ready ──
         │
[t=3]  ⚙️  C_task runs the training
         │   each run writes results/<RUN>/runtime.yaml + metrics.json
         │   ── pure C_task territory; D_probe is asleep ──
         │
[t=4]  🔗 /haipipe-probe design link E02 <run-path>
         │   (called by bridge automatically, or manually for stragglers)
         │   appends the run-path to the correct arm in probe.yaml
         │
[t=5]  📊 /haipipe-probe result aggregate E02
         │   scans arms[*].metrics.json
         │   computes mean / std / paired-t / sign-test
         │   writes result: block in probe.yaml
         │     status: pending → confirmed | inconclusive | refuted
         │
[t=6]  🔍 /haipipe-probe review E02
         │   structural QA: arms ≥1, metric set, caveats present, ...
         │   Codex semantic verdict (out-of-family review)
         │   writes review.md + CLAIMS_FROM_RESULTS.md
         │
[t=7]  📝 /haipipe-probe result claim E02
         │   final 1-2 sentence statement with stats + caveats
         │   "Treatment X beats baseline by Δ ± std (p=Y, N=3). +caveat."
         │
[t=8]  🗺️  /haipipe-probe explore (optional)
         │   coverage map across all probes
         │   proposes next probe to ask
         │
[t=9]  🔄 /haipipe-probe loop E02 (optional)
         │   review → fix → re-aggregate → re-review, until verdict is clean

[done] probe.yaml is the canonical probe record. C_task artifacts are the
       evidence. F_paper / E_dikw consume the claim downstream.
```


Filesystem layout — both worlds at the same project
=====================================================

```
examples/Proj-X/
│
├── tasks/                                  💼 C_task — execution
│   ├── A01_pretraining_clm/
│   │   ├── 01_pretrain_baseline/
│   │   │   ├── 01_pretrain_baseline.py
│   │   │   ├── configs/
│   │   │   ├── runs/
│   │   │   ├── results/
│   │   │   │   ├── run_seed42/
│   │   │   │   │   ├── runtime.yaml    ← per-run source of truth
│   │   │   │   │   └── metrics.json     ← per-run measurements
│   │   │   │   └── run_seed7/
│   │   │   ├── notebooks/
│   │   │   └── task-log.md              ← derived, per-task summary
│   │   └── 02_pretrain_lhm/...
│   ├── B01_evaluation_clm/...
│   └── ...
│
├── probes/                            📊 D_probe — research
│   ├── INDEX.md                            ← auto: list all probes
│   ├── coverage.md                         ← auto: gaps + proposals
│   ├── comparison.md                       ← auto: cross-probe view
│   │
│   ├── 01_baseline_noise_floor/
│   │   ├── probe.yaml                 ← steering state (this thread)
│   │   ├── review.md                       ← latest QA
│   │   ├── CLAIMS_FROM_RESULTS.md          ← Codex verdict snapshot
│   │   └── logs/<DATE>.md                  ← daily captain's-log
│   └── 02_x_vs_baseline/...
│
└── paper/                                  📰 F_paper — writing
    └── Paper-X-icml/...                    (consumes probes' claims)
```

Note: same project, three worlds, three folders. No code in
probes/. No claims in tasks/. No mixing. The folder is still named
probes/; conceptually each folder is one probe thread.


Common confusions — FAQ
========================

**Q: I have a Jupyter notebook that aggregates 5 runs into a plot.
     Where does it go?**
A: tasks/ — specifically a `display`-type task-folder (C-series).
   The aggregation logic is CODE; it belongs in C_task.
   The probe then references the plot via `evidence:` in
   probe.yaml. The CLAIM (in plain English) lives in the
   probe; the PLOT lives in a task.

**Q: Can one task be referenced by two probes?**
A: Yes. Tasks are atomic. Probes compose. E.g., one
   `01_pretrain_baseline/run_seed42` can serve as a baseline arm in
   E02 AND as a control arm in E07. They share the same run-path.

**Q: Can one probe span multiple projects?**
A: Not in this design. `examples/Proj-X/probes/` is project-
   scoped. Cross-project comparison happens in a higher-level
   skill (F_paper, or a meta-probe), not in probe.yaml.

**Q: What about exploratory runs that aren't part of any probe?**
A: Fine — they live in tasks/ alone, unlinked. No requirement to
   create an probe for every run. Probes exist for runs
   that test a specific claim.

**Q: When does a task-folder become a task-algo (X_algo demo)?**
A: When the run's purpose is "verify the algorithm class doesn't
   crash" — not "produce a result for a claim." A task-algo demo
   typically isn't linked to any probe.

**Q: probe.yaml has a `result:` block with numbers. Isn't that
     a result file then?**
A: No — those numbers are AGGREGATED REFERENCES to per-run metrics.
   The numbers are computed; the source of truth is each run's
   `metrics.json`. If you regenerate the probe.yaml result
   block, you'd read the same per-run metrics and recompute.

**Q: Where do daily notes about an probe go?**
A: `probes/<NN>_<slug>/logs/<YYYY-MM-DD>.md`. Append-only,
   one per day. Captain's-log style: what was tried, what surprised,
   what's next. Reviewed by `-loop` when iterating.


Cross-references
=================

```
C_task overall                  C_task/DESIGN.md
C_task → task-log               C_task/haipipe-task-logging/SKILL.md
C_task task-folder shape        C_task/haipipe-task/ref/hierarchy.md
C_task per-run runtime.yaml     C_task/haipipe-task/ref/runtime-yaml-schema.md

D_probe overall            D_probe/haipipe-probe/SKILL.md
D_probe bridge skill       D_probe/haipipe-probe-bridge/SKILL.md
D_probe.yaml schema        D_probe/ref/probe-yaml-schema.md
D_probe caveats checklist  D_probe/ref/probe-caveats-checklist.txt
D_probe legacy migration   D_probe/ref/_legacy-scope-expmt.md

Project umbrella (3 worlds)     B_project/haipipe-project/SKILL.md
```


One-line rules of thumb
========================

- New code? → tasks/  (never probes/)
- New claim? → probes/  (never tasks/)
- New plot? → tasks/display/  (referenced by probes/<X>/probe.yaml evidence:)
- New hypothesis? → probes/<NN>_<slug>/probe.yaml hypothesis: field
- New metric measurement? → tasks/<X>/results/<RUN>/metrics.json
- New per-run record? → tasks/<X>/results/<RUN>/runtime.yaml (atomic by run.sh)
- New cross-run statistic? → probes/<X>/probe.yaml result: (via /result aggregate)
- New "this didn't work, here's why" narrative? → probes/<X>/logs/<DATE>.md
- New CGM trace for one patient? → tasks/individual/  (never probes/)
