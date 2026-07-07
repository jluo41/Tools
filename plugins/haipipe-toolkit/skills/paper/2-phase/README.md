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
├── REF/                                ← shared references (prose-quality, comment-protocol,
│                                         paragraph-indexing, sentence-format, tex-file-anatomy)
│
├── 0-draft/                            ← DRAFT: settle structure + sentences
│   └── haipipe-paper-draft                 hub: structure + draft sentences
│
├── 1-probe/                            ← PROBE: agent-only, flag for CHECK
│   ├── haipipe-paper-probe                 hub: BOOKKEEP → DISPATCH → TRANSLATE → VERIFY
│   ├── haipipe-paper-probe-citation        citation harvester → _CITATION_.md
│   ├── haipipe-paper-probe-values          values harvester → _VALUES_.md
│   └── haipipe-paper-probe-display         display harvester → _DISPLAY_ + 0-displays/ links
│
├── 2-revise/                           ← REVISE: venue-quality prose (auto)
│   ├── haipipe-paper-revise                hub: routes the pass
│   ├── haipipe-paper-revise-content        content + ¶-flow (WHAT sentences say, HOW ¶s weave)
│   ├── haipipe-paper-revise-humanizer      de-AI audit (HOW sentences sound)
│   └── haipipe-paper-revise-results        results-specific revision
│
└── 3-check/                            ← CHECK: human + agent gate
    ├── haipipe-paper-check               6-axis verification gate
    └── haipipe-paper-proof-checker         math proof verification

(retired skills — venue-style write-*, old edit-cycle agents, old draft LaTeX
templates — live in the paper-root `_archive/`, not under 2-phase/)
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

## The probe phase (ONE pipeline: acquire via gateway → harvest paper-side)

ALL acquisition goes PP card → gateway (`Agent(haipipe-probe-orchestrator-agent)`)
→ discovery/task orchestrators; the workers are HARVESTERS that transcribe what
landed (JL 2026-07-07 ruling — they never search, grep-discover, or dispatch tasks):

```
PROBE:
  citation  → audit gaps → route to probe plans → harvest pick_list → _CITATION_ → 🔍 for CHECK
  values    → audit numbers → route unsourced to probe plans → harvest value_refs → _VALUES_
  display   → audit needs → plan (generation via probe) → link landed units → _DISPLAY_ + tex
```

Every lane obligation is written into the PP card (`harvest: OWED → accepted`);
`check-probe-cards.sh` FAILs an OWED lane or a planned card at VERIFY and at the CHECK gate.

Hard boundary: the gateway finds, the harvesters follow pointers, the human verifies in CHECK. The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots, NEVER searches inline during PROBE.

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
