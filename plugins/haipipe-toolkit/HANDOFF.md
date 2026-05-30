HANDOFF — haipipe-toolkit redesign (resume here)
==================================================

Last updated: 2026-05-30
Purpose: pick up the design work from a fresh session without re-deriving it.

Read these three, in order, to reload full context:
  1. ARCHITECTURE.md            — the 7-layer world view (the big picture)
  2. MENTAL_MODEL.md            — the 4-layer (C/D/E/G) mechanics
  3. skills/N_narrative/DESIGN.md — the layer we are currently building


The one-paragraph mental model
==============================

The system is a research engine. Facts flow up:
`Source → Task → Probe → Insight (= KB)`. A living story (`Narrative`)
sits in a **double-arrow loop with the KB** — facts ignite stories, stories
demand new probes. When a story is "ignited enough to sell", an
`Application` cashes it out into a deliverable (paper / report / message /
UI). Paper is just the (communication, read-only) kind; message/ui are the
(intervention) kind whose real-world reaction flows back to Source — making
the whole thing a flywheel, not a pipeline.

```
Source → Task → Probe → Insight ═══ Narrative → Application → (回流 to Source)
  🌱      ✋      🔧       🧠     ⇅      📖           🥢            ↺
                      └──── KB ────┘  ⇅ = the only double arrow (ignite lives here)
```

Key vocabulary settled this session:
- **Probe** = a claim-directed research thread (was "experiment"). One
  probe = one `probe.yaml` = one whip-crack at reality. References tasks as
  arms; never owns them. Produces K+W. Lives in `probes/`.
- **Narrative** = the living story (NOUN). KB ⇄ Narrative is the engine.
- **Application** = the act of cashing KB out (VERB). paper/report/message/ui.
- **ignite** = the gate on the KB⇄Narrative arrow: "am I ignited (eager to
  sell this)?" — advance if yes, re-scope/shelve if no.


DONE this session
=================

1. **ARCHITECTURE.md written** (committed) — the 7-layer world, KB⇄Narrative
   as the only double arrow, ignite gate, application = cash-out layer,
   two-axis classification of applications, the flywheel, multiplicity rules
   (1 narrative : N papers; KB shared once).

2. **probe rename fully landed in code** (committed in `fd80941`):
   - `skills/D_experiment/` → `skills/D_probe/`
   - all 8 skills `haipipe-experiment-*` → `haipipe-probe-*` (names match dirs)
   - `experiment.yaml` → `probe.yaml`; `experiments/` → `probes/`
   - `ref/experiment-*.{md,txt}` → `ref/probe-*.{md,txt}`
   - identifiers `experiment_id` → `probe_id`, `next_experiments_needed`
     → `next_probes_needed`
   - Generic academic "experiment" in F_paper / A_discover / 0_venue PROSE
     was deliberately PRESERVED (those describe paper-writing, not this
     layer). The `experimental` adjective was never touched.
   - `project-structure.md` already shows the new `probes/` layout.
   - Verified: 0 dangling `haipipe-experiment` / `D_experiment` /
     `experiment.yaml` tokens; 8/8 skill `name:` fields match their dirs.

3. **N_narrative/DESIGN.md written** (this commit) — full design for the new
   Narrative layer, scope A. NOT yet implemented as a runnable skill.


The expected project folder layout (reference)
==============================================

Authoritative source: `skills/B_project/haipipe-project/ref/project-structure.md`

```
examples/Proj{Series}-{Category}-{Num}-{Name}/   e.g. ProjB-Bench-1-FairGlucose
├── tasks/          ✋ WORK       C_task    (MANDATORY) code, configs, runs, metrics
├── probes/         🔧 CLAIMS     D_probe   (MANDATORY) research threads, NO code
├── insights/       🧠 KNOWLEDGE  E_insight (MANDATORY) D/I/K/W cards, NO code
├── diagram/        📖 STORY      —         (MANDATORY) project narrative, high-level
├── paper/          📰 PUBLISH    F_paper   (optional)  manuscripts
├── applications/   🥢 DELIVER    G_app     (optional)  messages / UI / reports
└── narratives/     📖 STORY-LINE N_narr    (PLANNED, not yet enforced — see DESIGN.md)
```

One-way dependency rule (who may read whom):
```
probes/  READS tasks/ ;  insights/ READS probes/+tasks/ ;
paper/ + applications/ READ insights/K+W ;
tasks/ READS no one (atomic foundation) ;  probes/ NEVER reads insights/
```


NEXT STEP (where to resume)
===========================

We are mid-way through building the **N_narrative layer, scope A**. The
DESIGN.md is written and AWAITING USER REVIEW.

Immediate decision pending:
  → User should read `skills/N_narrative/DESIGN.md` and approve/amend the
    schema BEFORE we build the skill (schema stability matters because
    scope B automates against it).

Then build (scope A):
  - `skills/N_narrative/haipipe-narrative/SKILL.md`
  - `skills/N_narrative/haipipe-narrative/ref/narrative-schema.md`
  Verbs: `new <slug>` / `status` / `claims <id>` / `ignite <id>`.

Scope A unit = one narrative folder with 4 files (decided):
  `story.md` (angle + why sell + core claim),
  `claims.md` (needed K cards by reference; GAP/weak rows = next whip),
  `ignite-log.md` (append-only "am I ignited?" judgments),
  `decision-tree.md` (section paths A/B/C/D).


DEFERRED — scope B (explicitly NOT in current work)
===================================================

- Auto gap-diff: claims.md `needs[]` minus insights/K → auto-emit
  `/haipipe-probe design new ...`.
- Wire narrative gaps into G_application ask-kind (load→gap→chain stub
  already exists in `skills/G_application/haipipe-application-ask/`).
- ignite as an ENFORCED gate with an adversarial steelman reviewer
  ("argue this is NOT worth selling") — scope A only records the judgment.
- The pre-whip gate (G1): review "should this probe run at all" before
  `/haipipe-probe design`. Currently design just asks the user; no gate.

See DESIGN.md "Scope boundary" + "Open questions" for the full deferred list.


Quality / gates model (discussed, not yet built)
================================================

For when we get to correctness: every arrow (transformation) gets a
guardian agent that only refutes; producer ≠ reviewer. Existing strong
gates: G3 Run Script Reviewer (Codex cross-family, in
`agents/run-script-reviewer.md`) and G5 Claim Verdict (Codex, in
`haipipe-probe-review`). Missing gates: G1 (pre-whip relevance) and the
ignite steelman. `validity` gates guard "is it true"; `relevance` gates
(narrative ends) guard "does it matter"; `fidelity` lint guards
"card faithful to evidence".
