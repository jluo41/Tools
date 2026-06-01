HANDOFF — haipipe-toolkit redesign (resume here)
==================================================

Last updated: 2026-05-31  (movement: probe-cycle — K/W output + dogfood; v2.3.2)
Purpose: pick up the design work from a fresh session without re-deriving it.

Read these, in order, to reload full context:
  1. ARCHITECTURE.md               — the 7-layer world view (the big picture)
  2. MENTAL_MODEL.md               — the C/D/E/G mechanics
  3. diagram/v260531/00-index.txt  — the CURRENT model as a visual set (start here for the gestalt)
  4. diagram/v260531/06-probe-cycle.txt — how to RUN one probe cycle (the 6-stage process)
  5. skills/E_insight/DESIGN.md    — E (BUILT): agents + dual-mode + per-type reviewers
  6. skills/N_narrative/DESIGN.md  — the Narrative layer (prior movement)


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


LATEST MOVEMENT (2026-05-31) — probe-cycle: K/W output + dogfood
================================================================

The probe-cycle (1 🔧 probe → N ✋ task-cycles → 1 🧠 insight) is now named,
documented (`diagram/v260531/06-probe-cycle.txt` = the 6-stage process), and its
insight-filing joint is fixed + dogfood-verified.

Done (committed; v2.3.0 → 2.3.2):
1. **E_insight agentified & BUILT** — `agents/creators/` (4, per DIKW) +
   `agents/reviewers/` (per-type `card-reviewer-{D,I,K,W}` + cross-layer
   `index-integrity-auditor`). Dual-mode skills (`ref/invocation-modes.md`).
   Per-type reviewers are a DELIBERATE departure from C/D's type-agnostic ones
   (each DIKW boundary differs — see `ref/dikw-boundaries.md`). Registry 13→22.
2. **Cycle vocabulary** — `narrative-cycle ⊃ probe-cycle ⊃ task-cycle`
   (grammar: cycle → stage → step; steps ◆ required / ◇ optional).
3. **K-from-probe fix (v2.3.2)** — a converged probe files its **claim → 🟨 K**
   (was wrongly a D card). `haipipe-insight-knowledge` + `card-creator-knowledge`
   + `invocation-modes` now source a CONFIRMED `probe_ref`; `probe-loop`
   convergence dispatches `card-creator-knowledge-agent`. **Dogfood-verified**
   on a stub (`/tmp/haipipe-dogfood/`, confirmed probe → K01; all gates green).

A probe-cycle's deliverable = **🟨 K (claim) + 🟧 W (next-step)**, both from the
probe; 🟦 D from its task-cycles; 🟩 I = cross-D pattern. **K is wired; W is NOT
yet** — that is the next step (below).


NEXT STEP (where to resume)
===========================

**Wire 🟧 W into the probe-cycle** (the K's twin — the probe's next-step rec).
The wisdom machinery is ALREADY correct (`haipipe-insight-wisdom` +
`card-creator-wisdom-agent` already do `K → W`); only the WIRING is missing:

1. `probe-loop` convergence: after filing K, chain
   `card-creator-wisdom-agent --scope <new-K>` → file the per-probe 🟧 W (the
   next-step). OPTIONAL ◇ — skip if the probe implies no concrete next-step.
   (per-probe W = single K; strategic W across many K stays cross-cycle.)
2. Docs: `06` stage Ⓕ (K → W), probe-loop text, the "probe-cycle → K+W" framing.
3. Dogfood: K01 → W01 ("run a param-matched re-test"); run card-reviewer-wisdom
   + index-integrity.
4. Bump `haipipe-probe-loop` metadata (→ 1.2.0 + changelog); commit.

Then (lower priority):
- **D-from-task reconciliation** — the `data` skill still reads a *probe*; it
  should read a *task*'s results. (Flagged in E_insight CHANGELOG.)
- **Metadata backfill** — some skills edited earlier this session are still at
  baseline `1.0.0` with no per-edit changelog (`haipipe-insight-{data,
  information,wisdom}`, probe-loop's pre-K changes). Bump + log if desired.
- **Full dogfood** — only stage Ⓕ was dogfooded; ①–⑤ have skills, not yet run e2e.

Discipline: when editing a skill/agent, bump `metadata.version` + add a
`metadata.changelog` line IN THE SAME COMMIT (per the metadata convention).


DONE (movement history, newest first)
=====================================

- **2026-05-31  probe-cycle K-fix (v2.3.2)** — converged probe files its claim
  → 🟨 K (was D); dogfood-verified. (commit `3ed80ac`)
- **2026-05-31  cycle vocabulary + probe-cycle process doc (v2.3.1)** —
  narrative/probe/task-cycle; `diagram/v260531/06-probe-cycle.txt`.
- **2026-05-31  E_insight agent skeleton (v2.3.0)** — per-type creators +
  reviewers + `dikw-boundaries.md`; agent registry 13→22.
- **2026-05-31  E_insight design + research-engine model (v2.2.0)** —
  DESIGN.md + diagram/v260531/ (hourglass, loops).
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
(pre-whip relevance) and the ignite steelman. E's reviewers are BUILT: per-type
`card-reviewer-{D,I,K,W}` (Codex accuracy + boundary/style) + `index-integrity`
(graph). `validity` gates guard "is it true";
`relevance` gates (narrative ends) guard "does it matter"; `fidelity` lint
guards "card faithful to evidence".
