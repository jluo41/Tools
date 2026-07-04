# 2-phase -- DRAFT-PROBE-REVISE-CHECK (shared across lifecycle stages)

The **phase dimension** of the paper skill architecture. Phase workers are shared across all lifecycle stages (seed, claims, pitch, narrative, display, section-edit). The hub for section-edit lives in `1-lifecycle/5-section-edit/haipipe-paper-section-edit/`.

```
Per-stage lifecycle:  DRAFT 🤖 → PROBE 🤖 → REVISE 🤖 → CHECK 🧑

Status strip:
phase:   draft ✅  │  probe: cite 🔥🚀  val --  disp --  │  revise ⬜  │  check ⬜
```

## Structure

```
2-phase/
├── README.md                           ← you are here
├── USAGE.md                            ← recipes, reply grammar, effort dial
├── WIRING.md                           ← routing and dispatch
├── REF/                                ← shared references
│   └── prose-quality.md                ← universal writing rules
│
├── 0-draft/                            ← DRAFT: settle structure + sentences
│   └── haipipe-paper-draft                 hub: structure + draft sentences
│
├── 1-probe/                            ← PROBE: agent-only, flag for CHECK
│   ├── haipipe-paper-probe-citation        citation → _CITATION_.md
│   ├── haipipe-paper-probe-values          values → _VALUES_.md
│   └── haipipe-paper-probe-display         display → 0-displays/ units
│
├── 2-revise/                           ← REVISE: venue-quality prose (auto)
│   ├── haipipe-paper-revise-content        content review (WHAT sentences say)
│   ├── haipipe-paper-revise-humanizer      de-AI audit (HOW sentences sound)
│   ├── haipipe-paper-revise-weaving        paragraph flow (HOW paragraphs connect)
│   └── haipipe-paper-revise-results        results-specific revision
│
├── 3-check/                            ← CHECK: human + agent gate
│   ├── haipipe-paper-check               6-axis verification gate
│   └── haipipe-paper-proof-checker         math proof verification
│
└── _archive/                           ← retired skills, incl. venue-style write-* skills
                                          and old draft LaTeX templates (venue knowledge
                                          now lives in _venue/ packs)
```

Whole-paper skills (consistency, format, typeset, claim-audit, submission-audit, diffpdf, optimizer, improve-loop, to-overleaf, reviewer) live in `3-build-submit/` as `haipipe-paper-edit-*`.

## Naming convention

```
haipipe-paper-{phase}-{what}    phase workers (this directory)
haipipe-paper-edit-*            whole-paper (3-build-submit/)
```

## Phase automation

- **DRAFT** 🤖: agent + user settle content decisions together
- **PROBE** 🤖: agent-only (dispatch evidence needs aggressively, flag for CHECK, no human gate)
- **REVISE** 🤖: agent-only (change the prose directly per prose-quality.md, leave why-comments, no comment-first)
- **CHECK** 🧑: human + agent (auto-checkers report, human decides: proceed/restart/accept/park)

## The probe phase (AUDIT → SEARCH → CANDIDATE → FLAG → PLACE → REVIEW)

Each probe-phase document worker owns one working doc and follows the same lifecycle:

```
PROBE:
  display   → audit what's needed → plan units → route to task → link
  values    → audit numbers → trace to source → place in tex
  citation  → audit gaps → search candidates → write to _CITATION_ → flag 🔍 for CHECK
```

Evidence needs beyond the document workers dispatch through `/haipipe-probe` (the project-side evidence gateway, mode light|full); probe calls `/haipipe-discovery` and `/haipipe-task` during its own Gather and files `/haipipe-insight` cards at Deposit.

Hard boundary: the agent searches and proposes; the human verifies in CHECK. The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots.

## Progression order

```
DRAFT first, PROBE second, REVISE third, CHECK last:

  draft (structure + narrative sentences)
           ↓
  probe: cite + val + disp   (can run in parallel)
           ↓
  revise (change the prose directly, leave why-comments)
           ↓
  check (verification gate → human decision)
           ↓
  sync to tex → compile
```
