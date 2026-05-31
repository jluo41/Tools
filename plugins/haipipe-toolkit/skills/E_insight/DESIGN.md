E_insight — The Archive Layer (DESIGN)
========================================

Status: DESIGN draft (2026-05-31) — agentification + dual-mode pass.
        Captures the design conversation; the templates/agents are NOT
        built yet (that is the next, separate step).
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

E_insight creators/ (per DIKW)    reviewers/ (2)             deferred
          ∵ NOT "batchable code"  card-fidelity +            (explore skill
          but "the HEADLESS path   index-integrity            already covers
          an AGENT calls"          = E's UNIQUE gate          the read side)
```

Key reframe settled this session: **E's creators exist for a different
reason than C's.** Not because filing is mechanical — because the user
needs a headless, full-args path an agent can call with zero
human-in-the-loop. The creator IS that path.


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

The system runs as nested loops. They map onto EXISTING machinery — except
one empty cell, which is E's job:

```
L0 atom    🔧 Probe ─bridge─▶ ✋ N×Task ─run─▶ result→probe.yaml ─▶ 🧠 E files D/I/K/W
           [bridge + result BUILT]                                  ▲ ★ EMPTY TODAY
L1 inner   haipipe-probe-loop  (review→verdict→propose→materialize→re-review)  [BUILT]
L2 outer   N_narrative ⇄ KB    (ignite-log; claims.md GAP rows)  [scope A BUILT, auto=scope B ⏳]
L3 trigger ignite=ready → narrative-report → Application (cash-out)            [path exists]
```

THE FINDING: `haipipe-probe-loop` never calls E_insight. Its Step 6
materializes (design + bridge → C_task), then on convergence jumps to
`narrative-report` — skipping the DIKW filing entirely. So the L0 atom's
last cell ("→ insight") is unwired.

Two consequences:
1. **E's headless creators are exactly what closes the L0 atom inside the
   L1 loop.** Their full-spec source in loop mode = the confirmed
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
│   └── reviewers/                  🆕 E's unique fidelity gate
│       ├── _TEMPLATE.md
│       ├── card-fidelity-reviewer-agent.md     (Codex: card <= evidence)
│       └── index-integrity-auditor-agent.md    (sources<->ref_by, INDEX<->files)
└── haipipe-insight*/SKILL.md       ♻️ each gains a dual-mode body + structured return
```

Growth axes (C's iron rule): creators grow per DIKW layer; reviewers are
fixed + type-agnostic (gate all four layers; adding a card type = +1
creator, +0 reviewer).


Decisions settled this session
==============================

- E gets a DESIGN.md + agents/ (parity with C/D).            ✅
- Dual-mode by input completeness; agent-missing → blocked.  ✅
- creators/ per DIKW (4) = the headless agent path.          ✅ (user override of
                                                                an earlier "no creators" lean)
- reviewers/ = card-fidelity (Codex) + index-integrity.      ✅
- E never triggers probes / drives loops; always callee.     ✅
- E closes the L0 atom that probe-loop currently skips.       ✅


Open questions (decide before building)
=======================================

Q1. Is the creator a SEPARATE agent, or just the skill's headless mode?
    C's creator authors extra body the skill doesn't; E's card is mostly
    schema, so E's creator is thinner. Lean: keep it a thin agent for
    fan-out parallelism (G-report files many cards at once), but it may
    just wrap the skill.

Q2. Should probe-loop be amended to call E on convergence (auto-close L0),
    or stay E-agnostic with G-ask doing the filing? Touches L1 ownership.

Q3. Does E need an advancer (synthesis proposer: "what is filable/
    synthesizable now")? The haipipe-insight-explore skill already covers
    the read/coverage side; advancer deferred unless explore proves too thin.

Q4. fidelity + integrity as two reviewers, or one? Kept separate (distinct
    deliverables; integrity is graph-only, fidelity re-reads evidence).


Next steps
==========

1. Write ref/invocation-modes.md (formalize the per-DIKW completeness table).
2. Write agents/README.md + agents/{creators,reviewers}/_TEMPLATE.md.
3. Author the 4 creators + 2 reviewers from the templates (thin pointers;
   judgment logic stays in the SKILLs + ref/, not duplicated in agents).
4. Add the dual-mode body + structured return to the 6 insight SKILLs.
5. (Decide Q2) optionally wire probe-loop → E on convergence to auto-close L0.
