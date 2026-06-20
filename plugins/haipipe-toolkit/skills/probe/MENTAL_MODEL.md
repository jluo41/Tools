probe ↔ task — Mental Model
=================================

Onboarding doc. Read this BEFORE writing your first probe / probe, or
when something feels like it could go in either tasks/ or probes/
and you're not sure which.

Naming note: the current folder and command names still say
`probe`, `probes/`, and `/haipipe-probe` for
compatibility. Conceptually, this layer is **probe**: a
claim-directed probe that asks reality a focused question.


TL;DR
=====

```
task    =  DO     layer   "did this run work?"
probe   =  MEAN   layer   "across these runs, does the hypothesis hold?"
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
║  task — EXECUTION                       ║  ║  probe — RESEARCH                      ║
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
         - Delete a probe → no impact on tasks.
         - Delete a task → linked probe becomes invalid (caught by review).

Rule 4 — Tasks are ATOMIC; probes COMPOSE.
         - A single task/run can be referenced by multiple probes
           (as a member of different arms in different threads).
         - A probe cites multiple runs across multiple tasks.
```


The bridge — only one direction crosses C ↔ D
================================================

```
probe side                             task side
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
      scaffolds the arms as task tasks                                ││
                                                                        ││
   ② design link (D side only, after runs complete):                    ││
        arms.baseline.append("tasks/A01/01_pretrain_baseline/...")      ││
        arms.lhm     .append("tasks/A01/02_pretrain_lhm/...")           ││
                                                                        ││
   ③ result aggregate (D reads C via arms[] pointers):                  ││
        for arm in arms:                                                ││
            for run in arm.runs:                                        ││
                metric = read(run/results/.../metrics.json) ◀───────────┘│
        write result: block in probe.yaml                           │
                                                                         │
   ④ review reads everything (D side only):                              │
        validates result: matches metrics ◀─────────────────────────────┘
        writes review.md + CLAIMS_FROM_RESULTS.md
```

Tasks never know a probe is reading them. They produce their
own metrics; the probe is just a downstream consumer.


One probe, full lifecycle
=========================

```
[t=0]  💡 Researcher has a question: "does architecture X beat baseline?"
         This is a probe: a focused kick at reality.
         │
[t=1]  📐 /haipipe-probe design new x_vs_baseline --date 0602
         │   writes probes/0602_x_vs_baseline/probe.yaml
         │     - hypothesis, claim_target
         │     - arms.baseline = []  (placeholder)
         │     - arms.x        = []  (placeholder)
         │     - aggregation spec (metric, statistic, noise_floor)
         │
[t=2]  🌉 /haipipe-probe bridge P.0602
         │   for each arm:
         │     Skill("haipipe-task", "task-folder training arm-baseline-seed42")
         │     Skill("haipipe-task", "task-folder training arm-x-seed42")
         │     ... (one task-folder per arm × seed)
         │   sanity arm runs first, then deploy rest
         │   ── task side now has 6 task-folders with run.sh ready ──
         │
[t=3]  ⚙️  task runs the training
         │   each run writes results/<RUN>/runtime.yaml + metrics.json
         │   ── pure task territory; probe is asleep ──
         │
[t=4]  🔗 /haipipe-probe design link P.0602 <run-path>
         │   (called by bridge automatically, or manually for stragglers)
         │   appends the run-path to the correct arm in probe.yaml
         │
[t=5]  📊 /haipipe-probe result aggregate P.0602
         │   scans arms[*].runs[*]/results/<RUN>/metrics.json
         │   computes mean / std / paired-t / sign-test
         │   writes result: block in probe.yaml
         │     status: pending → confirmed | inconclusive | refuted
         │
[t=6]  🔍 /haipipe-probe review P.0602
         │   structural QA: arms ≥1, metric set, caveats present, ...
         │   Codex semantic verdict (out-of-family review)
         │   writes review.md + CLAIMS_FROM_RESULTS.md
         │
[t=7]  📝 /haipipe-probe result claim P.0602
         │   final 1-2 sentence statement with stats + caveats
         │   "Treatment X beats baseline by Δ ± std (p=Y, N=3). +caveat."
         │
[t=8]  🗺️  /haipipe-probe explore (optional)
         │   coverage map across all probes
         │   proposes next probe to ask
         │
[t=9]  🔄 /haipipe-probe loop P.0602 (optional)
         │   review → fix → re-aggregate → re-review, until verdict is clean

[done] probe.yaml is the canonical probe record. task artifacts are the
       evidence. insight files D + K cards; paper consumes K + W downstream.
```


Filesystem layout — both worlds at the same project
=====================================================

```
examples/Proj-X/
│
├── tasks/                                  💼 task — execution
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
├── probes/                            📊 probe — research
│   ├── INDEX.md                            ← auto: list all probes
│   ├── coverage.md                         ← auto: gaps + proposals
│   ├── comparison.md                       ← auto: cross-probe view
│   │
│   ├── 0601_baseline_noise_floor/
│   │   ├── probe.yaml                 ← steering state (this thread)
│   │   ├── review.md                       ← latest QA
│   │   ├── CLAIMS_FROM_RESULTS.md          ← Codex verdict snapshot
│   │   └── logs/<DATE>.md                  ← daily captain's-log
│   └── 0602_x_vs_baseline/...
│
└── paper/                                  📰 paper — writing
    └── Paper-X-icml/...                    (consumes probes' claims)
```

Note: same project, four worlds, four folders. No code in
probes/ or insights/. No claims in tasks/. No mixing. The folder is still
named probes/; conceptually each folder is one probe thread.

```
examples/Proj-X/
├── tasks/      💼 task      code + results + D cards (via Stage 5)
├── probes/     📊 probe     steering state + K cards (via convergence)
├── insights/   🧠 insight   DIKW knowledge base (D/I/K/W cards + INDEX)
└── paper/      📰 paper     consumes K + W for publication
```


Common confusions — FAQ
========================

**Q: I have a Jupyter notebook that aggregates 5 runs into a plot.
     Where does it go?**
A: tasks/ — specifically a `display`-type task-folder (C-series).
   The aggregation logic is CODE; it belongs in task.
   The probe then references the plot via `evidence:` in
   probe.yaml. The CLAIM (in plain English) lives in the
   probe; the PLOT lives in a task.

**Q: Can one task be referenced by two probes?**
A: Yes. Tasks are atomic. Probes compose. E.g., one
   `01_pretrain_baseline/run_seed42` can serve as a baseline arm in
   P.0602 AND as a control arm in P.0603. They share the same run-path.

**Q: Can one probe span multiple projects?**
A: Not in this design. `examples/Proj-X/probes/` is project-
   scoped. Cross-project comparison happens in a higher-level
   skill (paper, or a meta-probe), not in probe.yaml.

**Q: What about exploratory runs that aren't part of any probe?**
A: Fine — they live in tasks/ alone, unlinked. No requirement to
   create a probe for every run. Probes exist for runs
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

**Q: Where do daily notes about a probe go?**
A: `probes/<MMDD>_<slug>/logs/<YYYY-MM-DD>.md`. Append-only,
   one per day. Captain's-log style: what was tried, what surprised,
   what's next. Reviewed by `-loop` when iterating.


Where probes meet insights (task ↔ probe ↔ insight)
============================================================

The three layers form a knowledge pipeline. Each layer produces DIKW cards at its natural scope:

```
task (execution)     produces → 🟦 D observation    "this task's data showed X"
probe (research)     produces → 🟨 K belief          "this probe confirms/refutes X"
insight (knowledge)  synthesizes → 🟩 I pattern      "across tasks, the pattern is X"
                       synthesizes → 🟧 W action       "based on what we know, do X"
```

Concrete wiring:

```
task Stage 5 (Insight)  →  Skill("haipipe-insight-data")  →  🟦 D card
  trigger:  task lifecycle completes with results (eval, fit, stata-reg, stata-data)
  source:   results/<run>/metrics.json + workflow/report*.yaml
  scope:    one task/run

probe convergence       →  card-creator-knowledge-agent   →  🟨 K card
  trigger:  probe result.status = confirmed or refuted
  source:   probe.yaml claim + result block
  scope:    one probe claim
  optional: chains card-creator-wisdom-agent → 🟧 W per-probe next-step
```

The DIKW partition principle: atomic layers (D, K) are filed automatically by their producers. Synthesis layers (I, W) require cross-source context and are owned by insight.

**Q: Can a task produce a K card directly?**
A: No. K requires a controlled comparison (a probe with arms × seeds × test). One task run is an observation (D), not a belief (K). Even if a single eval shows AUC=0.95, that's a D card until a probe formally compares it against a baseline.

**Q: Can a probe produce an I card?**
A: No. I is a cross-D pattern ("5 tasks all show the same trend"). A single probe sees only its own arms, not other probes' findings. I-level synthesis is insight's job.

**Q: What about the per-probe D + K in CYCLE.md?**
A: CYCLE.md is a DERIVED audit view that lists which D and K cards a probe produced. It does not file them — task Stage 5 files D, probe convergence files K. CYCLE.md just links to the filed cards via grep on `sources:`.


Cross-references
=================

```
task overall                  task/DESIGN.md
task task-folder shape        task/haipipe-task/ref/hierarchy.md
task per-run runtime.yaml     task/haipipe-task/ref/runtime-yaml-schema.md

probe overall            probe/haipipe-probe/SKILL.md
probe bridge skill       probe/haipipe-probe-bridge/SKILL.md
probe.yaml schema          probe/haipipe-probe/ref/probe-yaml-schema.md
probe caveats checklist  probe/haipipe-probe/ref/probe-caveats-checklist.txt
probe legacy migration   probe/haipipe-probe/ref/_legacy-scope-expmt.md

insight overall               insight/DESIGN.md
insight DIKW boundaries       insight/ref/dikw-boundaries.md
insight card schema           insight/ref/insight-md-schema.md

Project umbrella (3 worlds)     project/haipipe-project/SKILL.md
```


One-line rules of thumb
========================

- New code? → tasks/  (never probes/)
- New claim? → probes/  (never tasks/)
- New plot? → tasks/display/  (referenced by probes/<X>/probe.yaml evidence:)
- New hypothesis? → probes/<MMDD>_<slug>/probe.yaml hypothesis: field
- New metric measurement? → tasks/<X>/results/<RUN>/metrics.json
- New per-run record? → tasks/<X>/results/<RUN>/runtime.yaml (atomic by run.sh)
- New cross-run statistic? → probes/<X>/probe.yaml result: (via /result aggregate)
- New "this didn't work, here's why" narrative? → probes/<X>/logs/<DATE>.md
- New CGM trace for one patient? → tasks/individual/  (never probes/)
- New observation from a task run? → insights/D_data/  (filed by task Stage 5)
- New belief from a confirmed probe? → insights/K_knowledge/  (filed by probe convergence)
- New cross-task pattern? → insights/I_information/  (synthesized by insight)
- New actionable recommendation? → insights/W_wisdom/  (synthesized by insight)
