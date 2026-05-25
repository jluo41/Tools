C_task — Task-Type Specialist Series (DESIGN)
==============================================

Status: Phase 3 complete (2026-05-24) — content seeded, Phase 4 cleanup remaining
Owner:  jluo41
Scope:  task-folder scaffolding split into per-type specialists,
        mirroring the /haipipe-data and /haipipe-nn pattern.


Conceptual Layering
====================

A `project` is the umbrella for one cohesive research effort. Inside
it live THREE parallel worlds:

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/    ← project (umbrella)
│
├── 📁 tasks/        ← 💼 the WORK         build & run things
├── 📁 paper/        ← 📰 the DELIVERABLE  what we publish
└── 📁 experiment/   ← 📊 the CLAIMS       cross-run aggregation
```

Each world has its own specialist family — different sections, no overlap:

```
project umbrella     /haipipe-project              B_project/ (this folder's sibling)
tasks/               /haipipe-task-*               C_task/    ← THIS SECTION
paper/               /paper-*                      (existing paper-workflow / paper-figure / ...)
experiment/          /haipipe-experiment           D_experiment/
```

`B_project/` owns project-scope ops (the umbrella + inspect + organize).
`C_task/` owns task-scope ops — the 7 task-type specialists below.


Current State (Phase 2 complete)
=================================

```
B_project/                              ← project-scope skills
├── haipipe-project/                    🧭 umbrella
├── haipipe-project-inspect/            🔍 read project structure
└── haipipe-project-organize/           🛠️  reorganize project files

C_task/                                 ← task-scope skills (THIS SECTION)
├── DESIGN.md                           (this file)
├── haipipe-task/                       🧭 task orchestrator
│   ├── SKILL.md                        (asks scope; dispatches by task-type)
│   ├── ref/                            SHARED: hierarchy, run-sh-template, ...
│   └── fn/{project, task-group, task-folder, run}.md
│
├── haipipe-task-data/                  🔧 data-pipeline (Stage 1-4)
├── haipipe-task-algo/                  🧪 algo-dev demo
├── haipipe-task-training/              🧠 model training (Stage 5)
├── haipipe-task-eval/                  📊 model evaluation
├── haipipe-task-display/               🖼️  paper figure / table
├── haipipe-task-individual/            👤 subject-centric query
└── haipipe-task-agent/                 🤖 LLM agent call
```

Scope=project and scope=task-group stay in the orchestrator (they only
open a directory and seed a first task-folder, then delegate to a type
specialist). Scope=task-folder dispatches to one of 7 specialists.


Critical Distinction: algo-dev vs training
===========================================

```
┌──────────────────┬───────────────────────────────┬──────────────────────────────────┐
│                  │ task-algo (开发)              │ task-training (产出)             │
├──────────────────┼───────────────────────────────┼──────────────────────────────────┤
│ Purpose          │ verify the algorithm runs     │ train a real model + sweep       │
│                  │ end-to-end (smoke test)       │                                  │
│ Group letter     │ X_algo (Track A paired)       │ A-series (model-run)             │
│ Config scale     │ minimal (1-batch / tiny)      │ full hyperparam grid             │
│ Runtime          │ minutes                       │ hours-to-days                    │
│ Outputs          │ "didn't crash" + 1 loss val   │ checkpoint → _WorkSpace/5        │
│ Audience         │ algo developer themselves     │ cross-run comparison, paper      │
│ Pipeline skill   │ /haipipe-nn-algo              │ /haipipe-nn-tuner + -instance    │
└──────────────────┴───────────────────────────────┴──────────────────────────────────┘
```


Group Letter Assignment
========================

```
A = model-run (training)         /haipipe-task-training
B = evaluation                   /haipipe-task-eval
C = display (figure/table)       /haipipe-task-display
D = data-pipeline                /haipipe-task-data          (reassigned from D_demo)
E = individual query             /haipipe-task-individual    (new)
F = agent                        /haipipe-task-agent         (new)
X = algo-dev demo (paired)       /haipipe-task-algo          (renamed from D_demo)
```

Migration cost for existing projects: `tasks/D_demo/` → `tasks/X_algo/`
(one rename per project, deferred until Phase 4).


Per-Specialist Responsibilities
================================

Every type specialist owns:

```
SKILL.md              entry + this type's invariants + group-letter default
ref/config-seed.yaml  the YAML template seeded into configs/
ref/run-sh.template   (optional) overrides for parameter injection
fn/scaffold.md        scaffold flow + cross-skill links
fn/pitfalls.md        (optional) common mistakes for this type
```

Shared content stays in `haipipe-task/ref/` and is read by all type
specialists.


Cross-Skill References
=======================

Each task-* specialist links to its corresponding pipeline skill —
the pipeline skill owns the CODE, the task-* skill owns the EXAMPLE
SCAFFOLD under `examples/`. No duplication.

```
task-data         ↔  /haipipe-data
                       (-source / -record / -case / -aidata)
task-algo         ↔  /haipipe-nn-algo
                       (Layer 1 — algorithm class, forward, loss)
task-training     ↔  /haipipe-nn-tuner + /haipipe-nn-instance
                       (Layer 2 + 3 — hyperparam sweep, materialization)
task-eval         ↔  /haipipe-end (or future eval skill)
task-display      ↔  (none — independent; pulls from results/<run>/)
task-individual   ↔  /haipipe-subject
task-agent        ↔  /claude-api (adjacent; no pipeline skill yet)
```


Orchestrator Routing
=====================

```
/haipipe-task                           ❓ ask scope: project | task-group | task-folder
/haipipe-task project ...               ──▶ fn/project.md       (scaffold project + first group)
/haipipe-task task-group ...            ──▶ fn/task-group.md    (scaffold group)
/haipipe-task task-folder               ❓ ask task-type:
       data        ──▶  /haipipe-task-data
       algo        ──▶  /haipipe-task-algo
       training    ──▶  /haipipe-task-training
       eval        ──▶  /haipipe-task-eval
       display     ──▶  /haipipe-task-display
       individual  ──▶  /haipipe-task-individual
       agent       ──▶  /haipipe-task-agent
```

Shortcuts allowed (skip the questions):

```
/haipipe-task-training {project_id} {group} {name}
/haipipe-task-data     {project_id} {group} {name}
...
```

Equivalent entries via umbrella:

```
/haipipe-project task task-folder training {project_id} {group} {name}
```


Migration Plan
==============

Phase 1 — DESIGN review                                      ✅ DONE
  ✓ group-letter assignment confirmed (A/B/C/D/E/F/X)
  ✓ scope split confirmed (project + task-group in orchestrator;
    task-folder dispatches)
  ✓ Option B confirmed (split B_project/ and C_task/ directories)

Phase 2 — Skeleton                                            ✅ DONE (2026-05-24)
  ✓ created 7 task-* specialist directories with SKILL.md stubs
  ✓ each stub: frontmatter + position-in-series + scaffold layout +
    cross-skill link + TODO marker for scaffold flow
  ✓ updated haipipe-task SKILL.md to dispatch (legacy fn/task-folder.md
    marked DEPRECATED)
  ✓ updated haipipe-project umbrella to advertise new commands and
    document the layered conceptual model
  ✓ split into B_project/ (umbrella + inspect + organize) and
    C_task/ (orchestrator + 7 type specialists)

Phase 3 — Per-type content                                  ✅ DONE (2026-05-24)
  ✓ data:        fn/scaffold.md + ref/config-seed.yaml ({stage}_{layer}_{ds}.yaml)
  ✓ algo:        fn/scaffold.md + ref/config-seed.yaml (algo_<name>_tiny.yaml)
  ✓ training:    fn/scaffold.md + ref/config-seed.yaml (5_model_<name>.yaml)
  ✓ eval:        fn/scaffold.md + ref/config-seed.yaml (eval_<target>.yaml)
  ✓ display:     fn/scaffold.md + ref/config-seed.yaml (figure_<name>.yaml | table_<name>.yaml)
  ✓ individual:  fn/scaffold.md + ref/config-seed.yaml (subject_<view>.yaml)
  ✓ agent:       fn/scaffold.md + ref/config-seed.yaml (agent_<name>.yaml + prompts/)
  ✓ all 7 SKILL.md TODO sections replaced with pointer to fn/scaffold.md

Phase 4 — Cleanup
  ▢ remove monolithic branching from haipipe-task SKILL.md
    (delete legacy fn/task-folder.md once all type specialists ship)
  ▢ update B_project/haipipe-project/diagram.txt to show the
    B_project / C_task split
  ▢ rename D_demo → X_algo across existing projects (one PR per project)


Open Questions
==============

Q1. `task-eval` — should there be a /haipipe-eval pipeline skill, or
    keep eval logic project-local?
    Current default: project-local. Revisit if eval logic stabilizes
    across projects.

Q2. `task-agent` — no corresponding pipeline skill yet. Is /claude-api
    enough as a building block, or do we need a /haipipe-agent skill?
    Current default: /claude-api is sufficient for now; ship agent
    scaffold with placeholder config seed.

Q3. Should existing 5 task-types in `haipipe-task/fn/*.md` be deleted,
    or kept as DEPRECATED fallbacks during transition?
    Current default: keep one cycle as fallback; delete after all
    type specialists ship (Phase 4).


Decision Log
============

2026-05-24
  - Approved: split haipipe-project-task into 7 type specialists.
  - Approved: drop "project-" prefix; rename to haipipe-task-*.
  - Approved: move task series to sibling directory C_task/.
  - Approved: group letters A=training, B=eval, C=display, D=data,
    E=individual, F=agent, X=algo-demo. D_demo → X_algo.
