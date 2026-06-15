E_insight — The Archive Layer (DESIGN)
========================================

Status: v2.0.0 (2026-06-11) — DIKW producer partition established.
        C_task Stage 5 files D cards; D_probe convergence files K cards;
        E_insight owns I + W synthesis. Prior: agentification + dual-mode +
        per-type reviewers (2026-05-31).
Owner:  jluo41

Read ARCHITECTURE.md + MENTAL_MODEL.md first. This doc designs the AGENT
and INVOCATION structure for E_insight, bringing it to parity with C_task
and D_probe — which both have `agents/` + a top-level design doc; E had
neither. The pattern is applied THOUGHTFULLY (the way D_probe departed
from C_task), not copy-pasted.


Why this doc exists (the gap)
=============================

E_insight had the SKINS but no SKELETON:

```
C_task    DESIGN.md       + agents/{creators, reviewers}
D_probe   MENTAL_MODEL.md + agents/{reviewers, advancers}
E_insight  — none —        + — none —          ← only 6 SKILL.md + ref/
```

E is the only one of C/D/E with neither a design doc nor an agents/ layer.
This doc adds the skeleton.


E's nature (recap — the librarian)
==================================

E_insight does NOT think, compute, or claim. It FILES. It is CALLED BY
C_task and D_probe to file cards, and it synthesizes cross-cutting
patterns (I) and recommendations (W) from the accumulated cards.

```
called by:  C_task Stage 5 → files D cards (per-task observations)
            D_probe convergence → files K cards (per-probe beliefs)
            G_application Phase 4 → files any DIKW level
owns:       I synthesis (cross-D patterns) + W synthesis (cross-K actions)
writes:     insights/ only (D/I/K/W cards + INDEX)
NEVER:      writes tasks/ or probes/ ; triggers a probe (that is G-ask's job)
```


Who produces what (the DIKW producer partition)
================================================

Each DIKW level has one natural producer, determined by scope:

```
DIKW level     Producer           Trigger                          Scope
─────────────  ─────────────────  ───────────────────────────────  ──────────────
🟦 D data      C_task Stage 5     task lifecycle completes         one task/run
🟩 I info      E_insight          enough D cards accumulate        cross-task pattern
🟨 K knowledge D_probe loop       probe converges (confirmed)      one probe claim
🟧 W wisdom    E_insight / G_app  enough K cards accumulate        cross-probe action
```

The principle: **DIKW levels are partitioned by scope. Each scope has one natural owner. No layer files cards above its scope.**

- A task doesn't produce K (it doesn't test hypotheses — that's a probe's job).
- A probe doesn't produce I (it doesn't see cross-probe patterns — that's synthesis).
- The atomic layers (D, K) are filed automatically by their producers.
- The synthesis layers (I, W) require either enough accumulation or human judgment.

G_application-ask can also file any DIKW level during its Phase 4, but even then it calls the same E_insight skills — just with broader orchestration context.


The asymmetry note (E vs C vs D) — apply, don't copy
====================================================

D_probe's README warns: apply the agent pattern *thoughtfully*. Each layer
answers "is the BUILD batchable/headless, or interactive?" differently:

```
          builder family          reviewer family            advancer
─────────────────────────────────────────────────────────────────────────
C_task    creators/ (per TYPE)    reviewers/ (fixed 2)       — none —
          ∵ code authoring is     type-agnostic, gate all
          batchable, fans out

D_probe   SKILLS (no creators)    reviewers/ (3)             advancers/ (1)
          ∵ probe design is       structural/integrity/      explore =
          interactive, low-vol    claim                      propose next

E_insight creators/ (per DIKW)    reviewers/ (4 per-type     deferred
          ∵ "the HEADLESS path    + 1 cross-layer): one      (explore skill
          an AGENT calls", not    card-reviewer per D/I/K/W   already covers
          C's "batchable code"    + index-integrity (graph)  the read side)
```

Two reframes settled this session:
1. **E's creators exist for a different reason than C's** — not because filing
   is mechanical, but because we need a headless, full-args path an agent can
   call with zero human-in-the-loop. The creator IS that path.
2. **E's reviewers go PER-TYPE** — a deliberate departure from C/D's
   type-agnostic reviewers. Each DIKW card has a genuinely different boundary
   (D traces · I needs ≥2 D · K needs the probe + full counter-evidence · W
   must be actionable), so each gets its own card-reviewer enforcing accuracy +
   style against `ref/dikw-boundaries.md`. Only `index-integrity` stays shared
   (the cross-layer graph cannot be per-type).


The dual-mode invocation contract (the core)
============================================

Both a HUMAN and an AGENT call the same skill. The mode is chosen by
INPUT COMPLETENESS, not by who calls — verbatim the contract C_task
already ships in `C_task/haipipe-task/ref/invocation-modes.md`.

```
              ┌─────────────────────────────────────────────┐
 human  ─────▶│  haipipe-insight-<layer>  (one body)         │
 (often        │  input gate: card requisites complete?       │
  partial)     │    ✅ yes → SILENT  (produce card, no ASK)    │◀── card-creator-<layer>-agent
               │    ❌ no + user → ASK only the missing fields │    (always full spec → SILENT)
 agent  ─────▶│    ❌ no + no user → status: blocked, missing │
 (full spec)   │            (caller re-dispatches; never hang) │
               └─────────────────────────────────────────────┘
                  every call ends with a structured return block
```

Branch 3 (missing input + no user = agent path) is the load-bearing one:
the skill must NEVER hang on an ASK in a headless run — it returns
`status: blocked` + `missing: [field]`, and the calling agent fills it and
re-dispatches. Never invent a required field.

What "complete" means per layer (the meat of E's ref/invocation-modes.md,
derived from ref/insight-md-schema.md):

```
D (Data)        source_id (task/probe) + headline + Numbers table + tags
I (Information)  sources:[D..] (>=1) + pattern + direction + pattern stmt
K (Knowledge)    sources:[probe] MUST be confirmed + claim + confidence
W (Wisdom)       sources:[K..] + rec + type + cost + how-to-act
```


E's role in the loop architecture
===================================

The system runs as nested loops. The smallest unit is the **probe cycle** (L0:
probe → N tasks → insight). The insight filing cell is now wired via two paths:

```
L0 cycle   🔧 Probe ─bridge─▶ ✋ N×Task ─run─▶ result→probe.yaml ─▶ 🧠 E files D + K
  (probe cycle)                  │ Stage 5                            ▲ ✅ WIRED
                                 └──▶ 🟦 D card (per-task)            │
                                                    probe convergence └──▶ 🟨 K card (per-probe)
L1 inner   haipipe-probe-loop  (review→verdict→propose→materialize→re-review)  [BUILT]
L2 outer   N_narrative ⇄ KB    (ignite-log; claims.md GAP rows)  [scope A BUILT, auto=scope B ⏳]
L3 trigger ignite=ready → narrative-report → Application (cash-out)            [path exists]
```

The two concrete paths into E_insight:

```
Path A (task → D):   C_task Stage 5 (Insight) → Skill("haipipe-insight-data") → 🟦 D card
  trigger:   task lifecycle completes with results (eval, fit, stata-reg, stata-data)
  source:    results/<run>/metrics.json + workflow/report*.yaml
  review:    card-reviewer-data-agent validates accuracy + boundary

Path B (probe → K):  D_probe convergence → card-creator-knowledge-agent → 🟨 K card
  trigger:   probe result.status = confirmed (or refuted)
  source:    probe.yaml claim + result block
  review:    card-reviewer-knowledge-agent validates scope + counter-evidence
  optional:  chains card-creator-wisdom-agent → 🟧 W card (per-probe next-step)
```

Synthesis (I, W) is NOT triggered by a single producer — it accumulates:

```
Path C (D cards → I): when ≥2 D cards show the same pattern → /haipipe-insight information
  trigger:   C_task Stage 5 suggests when D card count ≥ 3 in a task-group
             G_application-ask Phase 4 schedules explicitly
             human calls /haipipe-insight information directly

Path D (K cards → W): when K cards imply an actionable recommendation → /haipipe-insight wisdom
  trigger:   G_application-ask Phase 4 schedules explicitly
             human calls /haipipe-insight wisdom directly
```

E never DRIVES a loop. It is always the callee. L1 (probe-loop) and L2
(narrative / G-ask) decide "go round again"; E only files when called.

The headless filing requirement still holds: L1 runs round after round;
L2 can fan out several probes at once. You cannot human-in-the-loop every
card. Headless E filing is a structural requirement, not a nicety.


Proposed structure (the skeleton to build)
===========================================

```
E_insight/
├── DESIGN.md                       (this file)
├── CHANGELOG.md                    🆕 parity with C/D
├── ref/
│   ├── invocation-modes.md         🆕 the dual-mode contract + per-DIKW table
│   ├── dikw-boundaries.md          🆕 each layer's boundary + worked examples (reviewers enforce)
│   ├── insight-md-schema.md        ✅ exists (reviewers point here, no dup)
│   ├── insight-context-loading.md  ✅ exists
│   └── index-templates.md          ✅ exists
├── agents/
│   ├── README.md                   🆕 roster + this asymmetry note
│   ├── creators/                   🆕 the headless, agent-callable path
│   │   ├── _TEMPLATE.md
│   │   ├── card-creator-data-agent.md
│   │   ├── card-creator-information-agent.md
│   │   ├── card-creator-knowledge-agent.md
│   │   └── card-creator-wisdom-agent.md
│   └── reviewers/                  🆕 one card-reviewer per DIKW type + 1 cross-layer
│       ├── _TEMPLATE.md
│       ├── card-reviewer-data-agent.md          🟦 Codex accuracy + D boundary/style
│       ├── card-reviewer-information-agent.md    🟩
│       ├── card-reviewer-knowledge-agent.md      🟨 + the ★ probe gate
│       ├── card-reviewer-wisdom-agent.md         🟧
│       └── index-integrity-auditor-agent.md     🔗 cross-layer: sources<->ref_by, INDEX<->files
└── haipipe-insight*/SKILL.md       ♻️ each gains a dual-mode body + structured return
```

Growth axes: creators grow per DIKW layer (+1 creator per layer). E DEPARTS
from C's "reviewers fixed/type-agnostic" rule — reviewers ALSO grow per layer
(+1 card-reviewer per layer), because each layer's boundary genuinely differs;
only index-integrity is shared. Adding a card type = +1 creator AND +1 reviewer.


Decisions settled
==================

Session 1 (2026-05-31):
- E gets a DESIGN.md + agents/ (parity with C/D).            ✅
- Dual-mode by input completeness; agent-missing → blocked.  ✅
- creators/ per DIKW (4) = the headless agent path.          ✅
- reviewers/ per DIKW (4) + cross-layer index-integrity.     ✅
- E never triggers probes / drives loops; always callee.     ✅
- E closes the probe cycle (L0) that probe-loop skips.        ✅

Session 2 (2026-06-11):
- **DIKW producer partition established.** D cards produced by C_task Stage 5; K cards produced by D_probe convergence; I + W owned by E_insight as synthesis layers. Each DIKW level partitioned by scope — no layer files above its scope. ✅
- **C_task Stage 5 (Insight)** calls Skill("haipipe-insight-data") → files D card after task lifecycle completes. Optional, only for insight-worthy types (eval, fit, stata-reg, stata-data). ✅
- **D_probe convergence** calls card-creator-knowledge-agent → files K card when probe result.status = confirmed/refuted. ✅
- **L0 loop cell wired.** The formerly empty "→ insight" cell now has two concrete paths: task→D and probe→K. ✅


Open questions
===============

Q1. [RESOLVED — build both] Creator is a SEPARATE thin agent AND the
    underlying skill stays: each card-creator-<layer>-agent calls the
    dual-mode haipipe-insight-<layer> skill headless.

Q2. [RESOLVED — wired] probe-loop convergence → K card; C_task Stage 5 → D card.
    🟩 I and strategic 🟧 W stay OUT of the per-probe loop (accumulate via
    explore / G_application).

Q3. Does E need an advancer (synthesis proposer)? Deferred — explore skill
    covers the read/coverage side. C_task Stage 5 now suggests I-level
    synthesis when D card count >= 3 in a task-group, which partially fills
    this role.

Q4. [RESOLVED — per-type] Each DIKW card gets a specific card-reviewer
    enforcing accuracy + style against ref/dikw-boundaries.md.


Next steps
==========

DONE:
  ✅ 1. ref/invocation-modes.md + ref/dikw-boundaries.md
  ✅ 2. agents/ (4 creators + 5 reviewers + README + templates)
  ✅ 3. dual-mode blocks in all 4 DIKW skills
  ✅ 4. probe-loop wired → card-creator-knowledge-agent on convergence
  ✅ 5. C_task Stage 5 wired → Skill("haipipe-insight-data") for D cards
  ✅ 6. DIKW producer partition documented (this doc + dikw-boundaries.md)
  ✅ 7. D_probe MENTAL_MODEL.md updated with insight connection

Remaining:
  - I-level auto-synthesis trigger: when C_task Stage 5 suggests (D count >= 3),
    who acts? Currently suggestion only. Could wire to G_application or make
    haipipe-insight-explore auto-check.
  - E_insight CHANGELOG.md (parity with C_task / D_probe).
  - Dogfood: run a real task through Stage 5 → D card → reviewer pass.
  - Dogfood: run a converged probe through loop → K card → reviewer pass.
