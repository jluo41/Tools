E_insight — The Archive Layer (DESIGN)
========================================

Status: BUILT (2026-05-31) — agentification + dual-mode + per-type reviewers landed.
        Built this session: ref/invocation-modes.md + ref/dikw-boundaries.md
        (boundaries + worked examples); agents/ (README + creators×4 +
        reviewers×5 [4 per-type card-reviewers + 1 cross-layer index-integrity]
        + 2 _TEMPLATEs); the 4 DIKW skills declare dual-mode; 9 top-level agent
        symlinks (registry 22); haipipe-probe-loop wired to file a D card on
        convergence (Q2). Remaining: higher-layer I/K/W auto-synthesis as cards
        accumulate; an E_insight CHANGELOG; dogfood.
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

E_insight does NOT think, compute, or claim. It FILES. It reads evidence
that C_task and D_probe already produced and writes DIKW markdown cards +
the cross-reference graph. Hard invariants (unchanged):

```
reads:    probes/ + tasks/   (the evidence anchors)
writes:   insights/ only     (D/I/K/W cards + INDEX)
NEVER:    writes tasks/ or probes/ ; triggers a probe (that is G-ask's job)
```


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


E's role in the loop architecture (the big finding)
===================================================

The system runs as nested loops. The smallest unit is the **probe cycle** (L0:
probe → N tasks → insight). They map onto EXISTING machinery — except one empty
cell, which is E's job:

```
L0 cycle   🔧 Probe ─bridge─▶ ✋ N×Task ─run─▶ result→probe.yaml ─▶ 🧠 E files D/I/K/W
  (probe cycle)  [bridge + result BUILT]                            ▲ ★ EMPTY TODAY
L1 inner   haipipe-probe-loop  (review→verdict→propose→materialize→re-review)  [BUILT]
L2 outer   N_narrative ⇄ KB    (ignite-log; claims.md GAP rows)  [scope A BUILT, auto=scope B ⏳]
L3 trigger ignite=ready → narrative-report → Application (cash-out)            [path exists]
```

THE FINDING: `haipipe-probe-loop` never calls E_insight. Its Step 6
materializes (design + bridge → C_task), then on convergence jumps to
`haipipe-paper-structure-narrative` — skipping the DIKW filing entirely. So the probe cycle's
last cell ("→ insight") is unwired.

Two consequences:
1. **E's headless creators are exactly what closes the probe cycle (L0) inside
   the L1 loop.** Their full-spec source in loop mode = the confirmed
   `probe.yaml` + the tasks' `results/`.
2. **The loop is WHY E filing must be headless.** L1 runs round after round;
   L2 can fan out several probes at once. You cannot human-in-the-loop every
   card. Headless E filing is a structural requirement, not a nicety.

E never DRIVES a loop. It is always the callee. L1 (probe-loop) and L2
(narrative / G-ask) decide "go round again"; E only files when called.


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


Decisions settled this session
==============================

- E gets a DESIGN.md + agents/ (parity with C/D).            ✅
- Dual-mode by input completeness; agent-missing → blocked.  ✅
- creators/ per DIKW (4) = the headless agent path.          ✅ (user override of
                                                                an earlier "no creators" lean)
- reviewers/ = one per DIKW (card-reviewer-{D,I,K,W}: Codex
  accuracy + style) + cross-layer index-integrity.           ✅ (per-type, user's call)
- E never triggers probes / drives loops; always callee.     ✅
- E closes the probe cycle (L0) that probe-loop skips.        ✅


Open questions (decide before building)
=======================================

Q1. [RESOLVED — build both] Creator is a SEPARATE thin agent AND the
    underlying skill stays (exactly C_task's split): each
    card-creator-<layer>-agent calls the dual-mode haipipe-insight-<layer>
    skill headless. The agent is the fan-out-able subagent_type; the skill
    holds the filing logic.

Q2. [RESOLVED — wired now] haipipe-probe-loop Step 3 (convergence) dispatches
    card-creator-knowledge-agent for the confirmed probe → files the 🟨 K from
    its claim, then optionally chains card-creator-wisdom-agent --scope <new-K>
    → files the per-probe 🟧 W (the next-step), closing L0 inside the loop. The
    🟦 D observations come from the probe's task-cycles; 🟩 I (cross-D pattern)
    and STRATEGIC W (across many K) stay OUT of the per-probe loop (accumulate
    via the report phase / explore).

Q3. Does E need an advancer (synthesis proposer: "what is filable/
    synthesizable now")? The haipipe-insight-explore skill already covers
    the read/coverage side; advancer deferred unless explore proves too thin.

Q4. [RESOLVED — per-type] Each DIKW card has a distinct boundary, so E uses a
    SPECIFIC card-reviewer per type (a deliberate departure from C/D's
    type-agnostic reviewers), each enforcing accuracy + style/boundary against
    ref/dikw-boundaries.md. index-integrity stays single (the cross-layer graph
    cannot be per-type).


Next steps
==========

DONE this session:
  ✅ 1. ref/invocation-modes.md (per-DIKW completeness table + 3 branches)
  ✅ 2. agents/README.md + creators/_TEMPLATE.md + reviewers/_TEMPLATE.md
  ✅ 3. 4 creators + 5 reviewers (4 per-type card-reviewers + 1 index-integrity)
        + ref/dikw-boundaries.md (boundaries + examples) + 9 top-level symlinks
  ✅ 4. dual-mode "Invocation modes" block added to the 4 DIKW skills
  ✅ 5. (Q2) probe-loop wired → card-creator-data-agent on convergence

Remaining:
  - Higher-layer I/K/W auto-synthesis as D cards accumulate (report phase /
    haipipe-insight-explore) — NOT per single probe.
  - An E_insight CHANGELOG.md (parity with C_task / D_probe).
  - Dogfood: run a converged probe through the loop; confirm the D card files
    and the two reviewers pass on a real card.
