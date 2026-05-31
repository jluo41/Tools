HANDOFF — haipipe-toolkit redesign (resume here)
==================================================

Last updated: 2026-05-31  (movement: E_insight agentification + research-engine model)
Purpose: pick up the design work from a fresh session without re-deriving it.

Read these, in order, to reload full context:
  1. ARCHITECTURE.md               — the 7-layer world view (the big picture)
  2. MENTAL_MODEL.md               — the C/D/E/G mechanics
  3. diagram/v260531/00-index.txt  — the CURRENT model as a visual set (start here for the gestalt)
  4. skills/E_insight/DESIGN.md    — the live movement: E agentification + loop closure
  5. skills/N_narrative/DESIGN.md  — the Narrative layer (prior movement)


The mental model — an hourglass (read this first)
==================================================

The system is a research engine shaped like an HOURGLASS. A direction
decomposes DOWN into work (fan-out, 1:n), executes at the bottom, then
aggregates UP into a deliverable (fan-in, n:1):

  ⬇️ decompose 1:n                                              ⬆️ aggregate n:1
  🥢 application → 📖 narrative → 🔧 probe → ✋ task → 🧠 insight → 📖 narrative → 🥢 application → ↺🌱

ONE layer thinks; the rest are its stimulus / tool / hands / memory:

  🥢 application·ask  = 领导 (leader)    gives a COARSE direction (nudge); does no work
  📖 narrative        = 办事的人 (doer)   the BRAIN: sets the goal, makes the plan,
                                          reads what it knows, then whips probes.
                                          Never runs compute — delegates execution.
  🔧 probe            = 鞭子 (the whip)   one whip-crack at reality
  ✋ task             = 体力 (labor)      runs compute (eats 🌱 Source)
  🧠 insight          = 记忆 (memory)     the knowledge state a whip-crack updates

Vocabulary nailed this session: it is **whip** (挥鞭, crack a whip), NOT
"wipe". The probe is the whip; the narrative is the whip-hand.

`narrative ⇄ insights` is the engine (the refined "double arrow"): narrative
READS insight content (🟨K/🟧W) + probe COVERAGE (probes/INDEX), finds a gap,
whips a probe; the machine runs it and E files the result back as insights;
narrative reads the update. `ignite` decides: cash out (paper) or whip again.

Cardinality: per ignite, n insights → 1 paper (n:1); over a thread's life,
1 narrative → N papers (1:N). The narrative is a persistent, iterating line;
papers are its discrete snapshots. A full visual breakdown is in
`diagram/v260531/` (hourglass · probe-cycle anatomy · nested cycles · roles · probe-cycle process).


LATEST MOVEMENT (2026-05-31) — E_insight agentification + loop closure
======================================================================

Full write-up: `skills/E_insight/DESIGN.md` + the `diagram/v260531/` set.

1. **E had skins but no skeleton.** C_task and D_probe each ship a design
   doc + `agents/{...}`; E_insight had neither. This session designs E's
   skeleton, applying the C/D pattern THOUGHTFULLY (as D departed from C).

2. **Dual-mode invocation for E** (= C_task's `ref/invocation-modes.md`):
   mode chosen by INPUT COMPLETENESS, not by who calls. agent = full spec →
   SILENT; human = partial → ASK only the missing fields; agent + missing →
   `status: blocked` (never hang). One body, callable by human AND agent.

3. **Agent families for E** (thoughtful, not copied):
   - `creators/` per DIKW (D/I/K/W) = the headless, agent-callable filing
     path. The reason is "headless agent path", NOT C's "code is batchable".
   - `reviewers/` = E's UNIQUE gate: `card-fidelity` (Codex; card ≤ the
     evidence cited, no overclaim) + `index-integrity` (sources↔ref_by,
     INDEX↔files). This is the "fidelity lint" listed under Quality below.

4. **THE BIG FINDING — loop closure.** `haipipe-probe-loop` never calls
   E_insight; the probe cycle (`probe → task → INSIGHT`, L0) has an empty last cell
   (probe-loop materializes via design+bridge, then jumps to
   narrative-report, skipping the DIKW filing). E's headless creators close
   it — and the loop (L1 inner × L2 narrative fan-out) is WHY filing must be
   headless (cannot HITL every card). E never DRIVES a loop; always the callee.

   ```
   L0 cycle   probe → bridge → N tasks → result → [E files D/I/K/W]  ← THE GAP (probe cycle)
   L1 inner   haipipe-probe-loop (review→verdict→propose→materialize→re-review)  BUILT
   L2 outer   N_narrative ⇄ insights (one turn = one narrative-cycle; ignite-log)  scope A BUILT
   L3 trigger ignite=ready → narrative-report → application (cash-out)        path exists
   ```


NEXT STEP (where to resume)
===========================

Build E's skeleton — the design is recorded in `skills/E_insight/DESIGN.md`:

1. `skills/E_insight/ref/invocation-modes.md` — formalize the per-DIKW
   "spec-complete" table (what makes each card headless-fileable).
2. `skills/E_insight/agents/README.md` + `{creators,reviewers}/_TEMPLATE.md`.
3. Author 4 creators (`card-creator-{data,information,knowledge,wisdom}`) +
   2 reviewers (`card-fidelity` Codex, `index-integrity`). Thin pointers —
   judgment logic stays in the SKILLs + ref/, not duplicated in the agents.
4. Add the dual-mode body + structured return to the 6 insight SKILLs.

Open decisions (see DESIGN.md Q1–Q4):
- Q2: should `haipipe-probe-loop` auto-call E on convergence (close L0 inside
  the loop), or stay E-agnostic with G-ask doing the filing?
- creator = thin agent (for fan-out) vs just the skill's headless mode.
- probe : insight = 1:1 (one bundle) — settled this session.


DONE (movement history, newest first)
=====================================

- **2026-05-31  E_insight agentification + research-engine model** — this
  movement (above): DESIGN.md + diagram/v260531/ + this HANDOFF + CHANGELOG 2.2.0.
- **N_narrative scope A** — `skills/N_narrative/` built: story / claims /
  ignite-log / decision-tree schema + `/haipipe-narrative` (new / status /
  claims / ignite). Reads insights/K+W; writes only narratives/; never fires
  a probe (that is scope B).
- **probe rename landed** (`fd80941`) — `D_experiment` → `D_probe`;
  `experiment.yaml` → `probe.yaml`; `experiments/` → `probes/`; 8/8 skill
  names match dirs; generic academic "experiment" prose preserved.
- **ARCHITECTURE.md** — the 7-layer world, KB⇄Narrative, ignite, cash-out
  layer, the flywheel, multiplicity (1 narrative : N papers).


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
narrative READS insights (content) + probes/INDEX (coverage); never writes/triggers directly
```


DEFERRED — N_narrative scope B + gates (NOT in current work)
============================================================

- Auto gap-diff: claims.md `needs[]` minus insights/K → auto-emit
  `/haipipe-probe design new ...` (through G_application ask, never directly).
- Wire narrative gaps into G_application ask-kind (load→gap→chain stub
  already exists in `skills/G_application/haipipe-application-ask/`).
- ignite as an ENFORCED gate with an adversarial steelman reviewer
  ("argue this is NOT worth selling") — scope A only records the judgment.
- The pre-whip gate (G1): review "should this probe run at all" before
  `/haipipe-probe design`. Currently design just asks the user; no gate.


Quality / gates model
=====================

Every arrow (transformation) gets a guardian agent that only refutes;
producer ≠ reviewer. Existing strong gates: G3 Run Script Reviewer (Codex
cross-family, `skills/C_task/agents/reviewers/run-script-reviewer-agent.md`)
and G5 Claim Verdict (Codex, `haipipe-probe-review`). Missing/planned: G1
(pre-whip relevance), the ignite steelman, and E's `card-fidelity` reviewer
(designed this movement; not built). `validity` gates guard "is it true";
`relevance` gates (narrative ends) guard "does it matter"; `fidelity` lint
guards "card faithful to evidence".
