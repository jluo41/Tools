D_probe — Research Probe Pipeline (DESIGN)
=============================================

Status: v3.0.0 (2026-06-11) — hub-centric; 5-stage lifecycle + loop; fn/ procedures + 6 agents; two-mode Design
Owner:  jluo41
Scope:  probe lifecycle (Design → Materialize → Harvest → Judge → Close),
        with loop-back from Judge → Explore → Design.
        NO code execution — pure steering state on top of C_task.


Conceptual Layering
====================

A `project` is the umbrella for one cohesive research effort. Inside it live parallel worlds:

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/    <- project (umbrella)
|
|-- 📁 tasks/        <- 💼 C_task      build & run things (CODE lives here)
|-- 📁 probes/       <- 📊 D_probe     cross-run aggregation (CLAIMS live here) <- THIS SECTION
|-- 📁 insights/     <- 🧠 E_insight   DIKW cards from probes
|-- 📁 paper/        <- 📰 F_paper     what we publish
```

D_probe sits between execution (C_task) and synthesis (E_insight / F_paper):

```
A_discover → D_probe → C_task (via bridge, one-way)
                ↑ reads metrics.json / runtime.yaml
                ↓ writes claims
             E_insight ← consumes confirmed claims (K cards)
             F_paper   ← consumes confirmed claims (narrative spine)
```

See **MENTAL_MODEL.md** (sibling file) for the authoritative boundary rules between C_task and D_probe.


Current State (v3.0.0)
========================

Hub-centric structure: the hub owns the lifecycle engine, phase procedures,
agents, and all shared schemas. Only tools with genuine standalone value
(explore, inspect) keep their own skill directory.

```
D_probe/                                <- probe-scope layer (THIS SECTION)
|-- DESIGN.md                           (this file — internals)
|-- MENTAL_MODEL.md                     (boundary doc — C_task ↔ D_probe)
|-- CHANGELOG.md
|
|-- haipipe-probe/                      🧭 hub — THE skill (lifecycle + routing)
|   |-- SKILL.md                        entry point, routing, lifecycle dispatch
|   |
|   |-- ref/                            📚 ALL schemas + templates + workflow engine
|   |   |-- probe-lifecycle.workflow.js 5-stage lifecycle + loop-back logic
|   |   |-- probe-yaml-schema.md        probe.yaml field spec + validation rules
|   |   |-- probe-caveats-checklist.txt confound walk (consumed by judge + harvest)
|   |   |-- probe-entry-template.txt    per-probe rendering format
|   |   |-- probe-headline-template.txt scoreboard template
|   |   |-- probe-run-dashboard-template.txt  planned-vs-done runs per arm
|   |   |-- probe-cycle-audit-template.txt    per-probe closed-loop audit (CYCLE.md)
|   |   |-- probe-status-template.txt   campaign status tracker (4 sections)
|   |   |-- workflow-plan-sample.yaml   IPO template: 6 domain phases
|   |   |-- log-format.md              daily log format
|   |   |-- _legacy-scope-expmt.md     migration notes (read-only)
|   |
|   |-- fn/                             🔧 phase procedures (called by workflow.js)
|   |   |-- design.md                   Stage 1: hypothesis + arms (Mode A/B)
|   |   |-- bridge.md                   Stage 2: scaffold arms → C_task + deploy
|   |   |-- harvest.md                  Stage 3: link + aggregate + claim
|   |   |-- judge.md                    Stage 4: structural + integrity + claim verdict
|   |
|   |-- agents/                         🤖 D_probe's own agents (3 families)
|   |   |-- creators/
|   |   |   |-- probe-idea-creator-agent.md      (Design Mode B — auto)
|   |   |-- reviewers/
|   |   |   |-- probe-idea-reviewer-agent.md     (Design Mode B — auto)
|   |   |   |-- probe-structural-reviewer-agent.md
|   |   |   |-- probe-integrity-auditor-agent.md (Codex-backed)
|   |   |   |-- claim-verifier-agent.md          (Codex-backed)
|   |   |-- advancers/
|   |   |   |-- probe-explorer-agent.md
|   |   |-- README.md
|   |
|   |-- diagram/
|       |-- 01-probe-lifecycle.txt      architecture diagram (lifecycle + loop)
|
|-- haipipe-probe-explore/              🗺️  standalone: coverage map + propose next
|   |-- SKILL.md                        (independent value — useful outside lifecycle)
|
|-- haipipe-probe-inspect/              👁️  standalone: read-only query layer
    |-- SKILL.md                        (independent value — status, list, refs, audit)
```


Hub-Centric Architecture
==========================

The hub IS the skill. Phase procedures live in `fn/`, agents in `agents/`,
schemas in `ref/`. Only tools with genuine standalone value (explore, inspect)
keep their own skill directory.

**haipipe-probe (hub)** owns:

- Command routing and scope resolution
- Dashboard (list probes, status)
- Probe identity resolution (`P.0601 | 0601 | probes/0601_framing.../`)
- The 5-stage lifecycle engine (`ref/probe-lifecycle.workflow.js`)
- Loop-back logic (while loop in workflow.js)
- Phase procedures (`fn/design.md`, `fn/bridge.md`, `fn/harvest.md`, `fn/judge.md`)
- All 6 agents in 3 families (`agents/creators/`, `agents/reviewers/`, `agents/advancers/`)
- All shared schemas and templates (`ref/`)

**Lifecycle stages → fn/ procedures:**

```
Stage         Procedure       Mood            Writes to
───────────   ──────────────  ──────────────  ──────────────────────
1 DESIGN      fn/design.md    "what to ask"   probe.yaml (new / link)
              + idea agents   (Mode B: auto)
2 MATERIALIZE fn/bridge.md    "make it run"   C_task tasks/ (via Skill)
3 HARVEST     fn/harvest.md   "what answered" probe.yaml (result + claim)
4 JUDGE       fn/judge.md     "is it honest?" review.md, INTEGRITY_AUDIT.md,
                                               CLAIMS_FROM_RESULTS.md
5 INSIGHT     (E_insight)     "what did we    insights/ D + I + K + W cards
                               learn?"        (full DIKW cascade)
```

**Standalone skills (independent value outside lifecycle):**

```
haipipe-probe-explore    🗺️ coverage map + propose next (used between loop rounds)
haipipe-probe-inspect    👁️ read-only query layer (status, list, refs, audit)
```

```
                   +──────────────────────────────────────────+
                   |         haipipe-probe (hub)               |
                   |                                          |
                   |  SKILL.md    routing + lifecycle dispatch |
                   |  ref/        schemas + workflow.js        |
                   |  fn/         4 phase procedures           |
                   |  agents/     6 agents in 3 families       |
                   |  diagram/    architecture visuals          |
                   +──────────────────────────────────────────+
                          |                     |
                   standalone skills:    standalone skills:
                   +──────────────+      +──────────────+
                   |   explore    |      |   inspect    |
                   +──────────────+      +──────────────+
```


Two Ways to Enter
------------------

```
Path 1 — Via hub (recommended):  /haipipe-probe <verb> P.0601
  hub parses verb → reads fn/<stage>.md → dispatches via workflow.js

Path 2 — Standalone tool:        /haipipe-probe-explore
                                  /haipipe-probe-inspect P.0601
  independent tools with their own SKILL.md
```

The 4 lifecycle stages (design, materialize, harvest, judge) are accessed
ONLY through the hub. They no longer have their own slash commands.


Agent Families
===============

D_probe has three agent families: creators, reviewers, and advancers.

**The Design stage has TWO modes — this drives the creator family:**

```
C_task builders → always agents     code authoring is BATCHABLE and fans out per
                                    task TYPE (13 specialists). Always automated.

D_probe Design → MODE A or B        the FIRST probe needs human judgment (framing
                                    a research question). FOLLOW-UP probes (fill a
                                    coverage gap, confirm single-seed, test opposite
                                    direction) can be automated — the explore agent
                                    already does 80% of the design work.
```

Mode A (interactive, default for round 1): human writes probe.yaml via design skill.
Mode B (auto, default for round >= 2 or --auto): probe-idea-creator-agent generates,
probe-idea-reviewer-agent checks, creator-reviewer loop (max 2 rounds).

**Three families, one axis each:**

```
creator   agents CREATE probe ideas          idea-creator (Design Mode B only)
reviewer  agents JUDGE                       idea-reviewer · structural · integrity · claim
advancer  agents PROPOSE direction           explore
```

**Creator agent (1 — Design Mode B only):**

```
Agent                       Fires in     Input                           Output
─────────────────────────   ──────────   ─────────────────────────────   ──────────────
probe-idea-creator-agent    Mode B only  explore proposals,              probe.yaml with
                                         existing probes,                hypothesis + arms
                                         insights K/W,                   + aggregation spec
                                         project research question
```

**Reviewer agents (4):**

```
Agent                              Gate         Backed by   Deliverable
──────────────────────────────────  ──────────  ─────────   ──────────────────────
probe-idea-reviewer-agent           idea QA     self        pass / revise / fail
  checks: falsifiable? not dup?     (Mode B)                (within Design stage)
  arms ok? worth compute?
probe-structural-reviewer-agent     structural  self        review.md
probe-integrity-auditor-agent       integrity   Codex       INTEGRITY_AUDIT.md
claim-verifier-agent                claim       Codex       CLAIMS_FROM_RESULTS.md
```

Idea-reviewer fires in Design Mode B. The other 3 fire in Judge stage,
order: structural → integrity → claim. `integrity = fail` blocks `claim`.

**Advancer agent (1 — D_probe's unique third family):**

```
Agent                    Deliverable                      Does NOT
─────────────────────    ─────────────────────────────    ──────────────────────
probe-explorer-agent     ranked next-probe list +         write probe.yaml (→ creator)
                         coverage map                     judge claims (→ reviewers)
```

**Knowledge home:** agents are THIN pointers — judgment logic stays in the specialist SKILL.md and ref/ (no duplicated checklists). Plugin top-level `agents/` holds flat symlinks for `subagent_type` dispatch.


Probe Lifecycle (5 stages + loop)
===================================

Orchestrated by `haipipe-probe/ref/probe-lifecycle.workflow.js`.
See `haipipe-probe/diagram/01-probe-lifecycle.txt` for the full architecture diagram.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  Stage 1: DESIGN — "what question to ask reality?"                       ║
║                                                                          ║
║  Mode A (interactive, round 1 default):                                  ║
║    🧑 human writes hypothesis + arms via haipipe-probe-design skill      ║
║                                                                          ║
║  Mode B (auto, round ≥2 default or --auto):                              ║
║    💡 probe-idea-creator-agent generates probe.yaml                       ║
║    🔍 probe-idea-reviewer-agent checks (falsifiable? dup? worth it?)     ║
║    ↺ creator-reviewer loop (max 2 rounds)                                ║
║                                                                          ║
║  Produces: probe.yaml (hypothesis + arms + aggregation spec)             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Stage 2: MATERIALIZE — "scaffold arms and make them run"                ║
║                                                                          ║
║    🌉 haipipe-probe-bridge scaffolds arms as C_task tasks                ║
║    📝 Run Script Reviewer agent checks code (creator-reviewer loop)      ║
║    🚀 sanity arm first → deploy rest → link runs to arms                 ║
║                                                                          ║
║  ═══════ C_task handoff: D_probe is asleep while C_task runs ═══════    ║
║                                                                          ║
║  Produces: tasks/<arm>/ with configs/, runs/, results/                   ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Stage 3: HARVEST — "what did reality answer?"                           ║
║                                                                          ║
║    📊 haipipe-probe-result links runs + aggregates stats + writes claim  ║
║    🛡️ probe-structural-reviewer checks (N≥3, arms paired, caveats)       ║
║                                                                          ║
║  Produces: probe.yaml result: block + claim: sentence                    ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Stage 4: JUDGE — "is the answer honest?"                                ║
║                                                                          ║
║    3 sequential gates (each independent reviewer):                       ║
║      🛡️ structural reviewer → review.md                                  ║
║      🔬 integrity auditor  → INTEGRITY_AUDIT.md (Codex)                  ║
║      ⚖️  claim verifier    → CLAIMS_FROM_RESULTS.md (Codex)              ║
║    Fail at any gate → stop.                                              ║
║                                                                          ║
║  Verdict: yes → Stage 5 (Insight)                                          ║
║           partial/no → Explore → loop back to Stage 1 (Design)           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Stage 5: INSIGHT — "what did we learn?" (full DIKW cascade)             ║
║                                                                          ║
║    Step 1: 🟦 D_data — per-arm observations                              ║
║      reads C_task I cards (or metrics.json directly)                     ║
║      card-creator-data-agent → card-reviewer-data-agent                  ║
║                                                                          ║
║    Step 2: 🟩 I_information — cross-arm patterns (needs ≥2 D cards)      ║
║      card-creator-information-agent → card-reviewer-information-agent    ║
║                                                                          ║
║    Step 3: 🟨 K_knowledge — validated belief from confirmed claim        ║
║      card-creator-knowledge-agent → card-reviewer-knowledge-agent        ║
║                                                                          ║
║    Step 4: 🟧 W_wisdom — actionable recommendation (optional)            ║
║      card-creator-wisdom-agent → card-reviewer-wisdom-agent              ║
║                                                                          ║
║    Final: 📋 index-integrity-auditor checks cross-ref graph              ║
║                                                                          ║
║  Produces: insights/D_data/ + I_information/ + K_knowledge/ + W_wisdom/  ║
║                                                                          ║
║  Parallel with C_task Stage 5 (Insight):                                 ║
║    C_task files D + I (per-task level, within one task's runs)            ║
║    D_probe files D + I + K + W (per-probe level, across arms)            ║
║    D_probe D reads C_task I as input (task patterns → probe observations)║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**The loop:**

```
Judge verdict = partial/no
  → 🗺️ Explore (coverage map + propose next probes)
  → Mode A: 🧑 human gate (approve/reject proposals)
    Mode B: 💡 idea-creator + 🔍 idea-reviewer (auto-generate + auto-review)
  → Back to Stage 1 (Design) with the new probe
  → Repeat until converged or budget exhausted
```

Stop conditions:
  ✅ converged — verdict = yes AND structural errors = 0 → Insight
  🟡 budget_exhausted — hit --rounds N without converging
  🔴 blocked — all proposals rejected (human or agent)
  ⏸️  paused — user interrupt


The ref/ Shared Schemas
========================

All specialists read from `ref/` for shared schemas and templates:

```
Resource                          Consumed by                Purpose
────────────────────────────────  ─────────────────────────  ─────────────────────────────
probe-yaml-schema.md              design, result, review     field spec + validation rules
probe-caveats-checklist.txt       result (claim), review     confound walk before saving
probe-entry-template.txt          result (render)            per-probe rendering format
probe-headline-template.txt       result (render)            scoreboard template
probe-run-dashboard-template.txt  inspect (runs)             planned-vs-done runs per arm
probe-cycle-audit-template.txt    inspect (cycle)            per-probe closed-loop audit
probe-status-template.txt         inspect (status)           campaign tracker (4 sections)
log-format.md                     (daily logs convention)    captain's-log style
```


Filesystem Layout (at the project level)
==========================================

```
examples/Proj-X/
├── probes/                                📊 D_probe — research steering
│   ├── INDEX.md                                (auto: list all probes)
│   ├── coverage.md                             (auto: /explore output)
│   ├── propose.md                              (auto: /explore proposals)
│   ├── comparison.md                           (auto: /result render output)
│   ├── STATUS.md                               (optional persist of /inspect status)
│   ├── RUNS.md                                 (optional persist of /inspect runs project)
│   │
│   ├── 0601_framing_loss-aversion/            active probe folder
│   │   ├── probe.yaml                          source of truth (claim + arms + result)
│   │   ├── review.md                           structural QA
│   │   ├── INTEGRITY_AUDIT.md                  Codex fraud-pattern check
│   │   ├── CLAIMS_FROM_RESULTS.md              Codex semantic verdict
│   │   ├── CYCLE.md                            closed-loop audit (derived)
│   │   ├── LOOP_LOG.md                         iteration history (if loop ran)
│   │   └── logs/                               daily captain's-log
│   │       ├── 2026-06-01.md
│   │       └── 2026-06-02.md
│   │
│   └── 2026-archive/                           inactive probes
│       └── 0501_social-norm/
│
├── tasks/...                                   💼 C_task — execution (code + results)
├── insights/...                                🧠 E_insight — DIKW cards
└── paper/...                                   📰 F_paper — writing
```


Cross-Skill References
=======================

```
Component                Calls / reads from              Direction
───────────────────────  ──────────────────────────────  ──────────
probe-idea-creator       explore proposals + insights/   D reads D + E
  (agents/creators/)     existing probes                 (Design Mode B)
probe-idea-reviewer      just-created probe.yaml         D reads D
  (agents/reviewers/)    existing probes (dup check)     (Design Mode B)
fn/bridge.md             Skill("haipipe-task")           D → C (scaffold)
                         C_task/agents/task-reviewer     D reads C agent (GATE 1)
fn/harvest.md            tasks/.../metrics.json          D reads C results
                         tasks/.../runtime.yaml          D reads C status
fn/judge.md              C_task/task-reviewer-agent      D delegates per-run QA to C (GATE 2)
probe-lifecycle.wf.js    card-creator-{D,I,K,W}-agent   D → E (DIKW cascade on convergence)
haipipe-probe-explore    (reads all probe yamls)         D reads D (coverage map)
```

**Strict one-way:** C_task never references D_probe. Tasks never know a probe is reading them.


Relationship to C_task — Boundary Summary
==========================================

Full boundary rules live in **MENTAL_MODEL.md** (sibling file). The short version:

```
Rule 1 — probes/ has NO code.          All computation in tasks/.
Rule 2 — probe.yaml is steering state. Source metrics live in tasks/.../metrics.json.
Rule 3 — One-way dependency.           Probes READ tasks; tasks do NOT reference probes.
Rule 4 — Tasks are ATOMIC.             One task can serve multiple probes.
```

The bridge is the only crossing point (D → C). The contract:

```
What D reads from C:
  - results/<RUN>/metrics.json     per-run measurements (scalar or {point, ci_*})
  - results/<RUN>/runtime.yaml     per-run status (ok / failed / running)
  - configs/<RUN>.yaml             git_sha, AIData version (for consistency checks)

What D writes to C (via bridge only):
  - new task-folders under tasks/   (scaffolded via Skill("haipipe-task"))
  - configs/<RUN>.yaml              (wired from probe arm run_specs)
  - runs/<RUN>.sh                   (generated run wrapper)

What C never sees:
  - probe.yaml, review.md, CLAIMS_FROM_RESULTS.md, LOOP_LOG.md
  - any file under probes/
```


Decision Log
=============

2026-06-11  Created: DESIGN.md v1.0.0 (internals doc, parallel to C_task/DESIGN.md).
            MENTAL_MODEL.md remains the boundary doc.
2026-06-11  Upgraded: DESIGN.md v2.0.0 — 5-stage lifecycle (Design/Materialize/Harvest/Judge/Insight).
            Stage 5 renamed Close → Insight for parallel naming with C_task Stage 5.
            Insight stage files full DIKW cascade: D (per-arm) → I (cross-arm) → K (claim) → W (next step).
            C_task Insight files D+I (per-task level); D_probe Insight files D+I+K+W (per-probe level).
            D_probe D reads C_task I as input (task patterns become probe observations).
            Loop-back from Judge → Explore → Design absorbed into probe-lifecycle.workflow.js.
            Two-mode Design stage: Mode A (human) / Mode B (probe-idea-creator + reviewer agents).
            Agent count: 4 → 6 own (+1 creator, +1 reviewer) + 9 borrowed from E_insight in Stage 5.
2026-06-11  Restructured: DESIGN.md v3.0.0 — hub-centric consolidation.
            4 lifecycle specialists (design/bridge/result/review) → fn/ procedures under hub.
            Shared ref/ merged into hub ref/. agents/ moved under hub.
            Only explore + inspect keep standalone skill directories.
            Top-level agent symlinks updated to new paths.
            D_probe root: 9 items → 5 (hub + explore + inspect + 3 docs).
