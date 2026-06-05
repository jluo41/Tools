HANDOFF — haipipe-toolkit redesign (resume here)
==================================================

Last updated: 2026-06-05  (movement: F_paper 5-stage restructure + haipipe-paper-* name unification)
Purpose: pick up the design work from a fresh session without re-deriving it.

Read these, in order, to reload full context:
  1. ARCHITECTURE.md               — the 7-layer world view (the big picture)
  2. MENTAL_MODEL.md               — the C/D/E/G mechanics
  3. diagram/v260531/00-index.txt  — the CURRENT model as a visual set (start here for the gestalt)
  4. diagram/v260531/06-probe-cycle.txt — how to RUN one probe cycle (the 6-stage process)
  5. diagram/v260531/07-end-to-end-claim-gap.txt — the ask→claim-gap→probe→K/W→cash-out hinge
  6. skills/E_insight/DESIGN.md    — E (BUILT): agents + dual-mode + per-type reviewers
  7. skills/N_narrative/DESIGN.md  — the Narrative layer + Claim Gap Contract


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
READS insight content (🟨K/🟧W) + probe COVERAGE (probes/INDEX), finds a
claim slot that is GAP/weak, turns that slot into a **Claim Gap Contract**,
then whips a probe; the machine runs it and E files the result back as
insights (🟨 K + 🟧 W, both now wired); narrative reads the update. `ignite`
decides: cash out (paper) or whip again.

Cardinality: per ignite, n insights → 1 paper (n:1); over a thread's life,
1 narrative → N papers (1:N). The narrative is a persistent, iterating line;
papers are its discrete snapshots. A full visual breakdown is in
`diagram/v260531/` (hourglass · probe-cycle anatomy · nested cycles · roles · probe-cycle process).


LATEST MOVEMENT (2026-06-05): F_paper 5-stage restructure + name unification
============================================================================

F_paper (the paper-lifecycle skill family) was collapsed and renamed in one pass. This is a separate track from the C/D/E/G/N research-engine work below; nothing in that model changed.

**New stage layout** (was ~10 stage folders, now 5 + workflow):

```
0-workflow/   haipipe-paper (router) + 6 venue/task specialists (names unchanged)
1-structure/  decide WHAT the paper says (was 1-plan, then 1-narrate)
2-build/      NEW STAGE: build the physical paper folder the prose lives in
3-edit/       absorbed 3-write, 4-revise, 5-revise, 5-review, 6-review (one edit/audit family)
6-respond/    paper-rebuttal, rebuttal-response          (legacy names)
7-present/    paper-slides, paper-poster                 (legacy names)
components/   citation-*, paper-compile, paper-diff-folder (legacy names)
```

**Name unification**: every skill in stages 1-3 is now `haipipe-paper-<stage>-<topic>`, and every skill DIRECTORY equals its `name:` frontmatter (e.g. `3-edit/haipipe-paper-edit-to-overleaf/`). 37 skills renamed; all references swept (slash triggers, `Skill()` dispatches, backticked mentions, path refs); each renamed SKILL.md got a `1.1.0 (2026-06-05)` changelog line. Verified: zero leftover legacy tokens, zero duplicate names, dir==name for all of stages 1-3.

**2-build is new** (grounded in the gold paper `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025`):
- `_shared/paper-folder-anatomy.md`: the whole-folder contract (0-/1- prefix semantics, NN-MM grammar + gap rule, two-document main+SI rule, 1-compile.sh contract)
- `haipipe-paper-build-scaffold` (+6 templates): plan → conforming empty skeleton
- `haipipe-paper-build-restructure`: migrate/repair, gated by prose parity + compile parity
- `haipipe-paper-build-check` (+`scripts/check_structure.sh`): report-only conformance audit; script verified green on the gold paper and all failure paths fixture-tested

Other moves this pass: `overleaf-sync` → `3-edit/haipipe-paper-edit-to-overleaf`; `paper-diff-pdf` → `haipipe-paper-edit-diffpdf`; `paper-architecture` registered (its skill.md had no frontmatter at all); the four write skills live on as `-edit-write{,-scientific,-conference,-systems}` (write = the cold-start of editing).

Known leftovers (deliberate):
- `6-respond` / `7-present` / `components` / `sections` keep legacy names. If unifying later: `6-respond/paper-rebuttal` COLLIDES with workflow `haipipe-paper-rebuttal`; needs e.g. `haipipe-paper-respond-rebuttal`.
- `skills/F_paper/MENTAL_MODEL.md` still describes the old 8-stage layout; needs a rewrite around structure → build → edit → respond → present (a mechanical sweep would mangle it, so it was excluded).
- Reload Claude Code for the renamed skills to register.


PREVIOUS MOVEMENT (2026-05-31) — probe-cycle: K/W output + dogfood
================================================================

Addendum (v2.3.4): **W is now wired** — a converged probe-cycle files 🟨 K,
then optionally (◇) the per-probe 🟧 W (scoped to that K). Dogfood-verified
(K01 → W01; all wisdom + index-integrity gates green). The earlier
Claim Gap Contract hinge (v2.3.3) is unchanged: a narrative-cycle exposes a
C-slot GAP/weak row in `claims.md`; that row becomes the contract for one
probe-cycle; the probe contract expects K/W (**both wired now**); narrative
re-reads K/W and records ignite. See
`diagram/v260531/07-end-to-end-claim-gap.txt`, `ARCHITECTURE.md`, and
`skills/N_narrative/.../narrative-schema.md`.

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
probe; 🟦 D from its task-cycles; 🟩 I = cross-D pattern. **K and W are both
wired now** (W added v2.3.4, dogfood-verified) — the per-probe loop closes with
K+W; 🟩 I and STRATEGIC W (across many K) stay cross-cycle synthesis.


NEXT STEP (where to resume) — CLOSE THE NARRATIVE LOOP
=====================================================

Framing (from the 2026-05-31 narrative-loop review): the outer loop has TWO
arms. The **induction arm** (KB → 📖: `claims` reads K/W, `ignite` records) is
wired. The **deduction arm** (📖 → KB: a story's GAP says which whip to crack)
is still the HUMAN — `narratives/*/claims.md` holds the Claim Gap Contract, but
nothing turns it into a probe. Wiring W (v2.3.4) was step 1 — it filled the
narrative's INPUT (K+W). Steps 2–4 below close the loop itself.

1. **Deduction-arm handoff** (the missing return rail — scope B, first slice).
   Make `/haipipe-narrative claims <id>` emit a ready-to-run Claim Gap Contract
   — a `/haipipe-probe design new ... --hypothesis "..."` command line WITH the
   evidence standard — instead of prose, so a human approves ONE line instead of
   retyping. Goes THROUGH `G_application` ask (narrative NEVER writes `probes/`
   directly — hard rule). Turns "human re-reads + retypes" into "human approves".
2. **`ignite` as a GATE, not a log.** Add the steelman reviewer ("argue this is
   NOT worth selling") so `/haipipe-narrative ignite` ENFORCES the judgment
   (stops motivated reasoning), rather than only appending to `ignite-log.md`.
3. **GAP→have notification** (N_narrative open Q2) — when E files a K/W, refresh
   any `claims.md` that references it (today: manual `claims` re-scan).
4. **Full e2e dogfood of the loop** — run ask → narrative → contract → probe →
   K/W → re-read → ignite once on a real instantiated project. Only stage Ⓕ
   (K, now W) has been dogfooded; the loop has never turned end-to-end.

Probe-cycle internals (lower priority — refinements, not loop-blockers):
- **D-from-task reconciliation** — `haipipe-insight-data` still sources a D from
  a *confirmed probe*; per the model (D+I = C_task lens, K+W = D_probe lens) a
  🟦 D should source a *task*'s `results/` (`source_id` = task id). Fix the data
  skill + `card-creator-data-agent` + `invocation-modes` D row, then re-point
  probe-loop's per-arm D filing. Flagged in E_insight CHANGELOG.
- **Metadata backfill** — `haipipe-insight-{data,information,wisdom}` still at
  baseline `1.0.0`. The wisdom pair is now load-bearing; a `1.1.0` "W wired
  (consumer)" line would aid traceability.

Discipline: when editing a skill/agent, bump `metadata.version` + add a
`metadata.changelog` line IN THE SAME COMMIT (per the metadata convention).


DONE (movement history, newest first)
=====================================

- **2026-06-05  F_paper 5-stage restructure + haipipe-paper-* unification**:
  stages collapsed to 1-structure / 2-build (new) / 3-edit (absorbed write,
  revise, review); 37 skills renamed to `haipipe-paper-<stage>-<topic>` with
  dir == name; 2-build stage built from the npjDM2025 gold paper (anatomy
  contract, scaffold templates, parity-gated restructure, check_structure.sh).
- **2026-05-31  W wired into the probe-cycle (v2.3.4)** — a converged
  `haipipe-probe-loop` (→ 1.2.0) files 🟨 K, then optionally (◇) chains
  `card-creator-wisdom-agent --scope <new-K>` → the per-probe 🟧 W. The W
  machinery was already correct; only the wiring was missing. Per-probe W
  (single-K) vs strategic W (cross-K) made explicit. Dogfood: K01 → W01,
  13/13 wisdom + 5/5 index-integrity gates green (independent re-run). Flipped the v2.3.3
  "W is next" caveats; corrected `DESIGN.md` Q2 (was the stale data-agent
  dispatch).
- **2026-05-31  end-to-end claim-gap hinge (v2.3.3)** — named the
  **Claim Gap Contract** as the connector between narrative-cycle and
  probe-cycle; added diagram 07 and threaded schema/architecture docs.
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
  `/haipipe-probe design new ...` from Claim Gap Contracts (through
  G_application ask, never directly).
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
