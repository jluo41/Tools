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
│   ├── haipipe-paper-probe                 hub: ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET
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

- **DRAFT** 🤖→🧑: agent writes the REAL draft (sections: complete prose with real `\citep{}` keys from .bib + `{VAL:?}`/`\cite{TOADD}` placeholders) → ⛔ HARD STOP: user reviews structure; the user's verb/"go" is the gate (logged `[GATE]` in _LOG)
- **PROBE** 🤖: agent-only (dispatch evidence needs aggressively, flag for CHECK, no human gate)
- **REVISE** 🤖: agent-only and PROOF-CARRYING — reached only via `Skill(haipipe-paper-revise)` (never inline); changes the prose directly per prose-quality.md on the .md FIRST then syncs to tex; leaves why-comments; `[REVISE]` _LOG entry carries `workers: content ✓ humanizer ✓ …`
- **CHECK** 🧑: human + agent (auto-checkers report, human decides: proceed/restart/accept/park). Never commit before CHECK opens.

The user drives phases with VERBS on the stage skill (`/haipipe-paper-section-edit <section> [draft|probe|revise|check]`); a bare invocation shows status and proposes — never runs — the next phase. The agent never self-advances past a human gate.

## The probe phase (ONE pipeline: MATCH first, dispatch what is left, harvest paper-side)

ALL acquisition goes: probe SECTION → ② MATCH against the bank's QA corpus → and only what MATCH
cannot close → ③ DISPATCH the section's `q-executor:` block, VERBATIM, to
`Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)`.
(The reuse decision IS the paper-side MATCH.) The three
lane workers are HARVESTERS that transcribe what landed — they never search, grep-discover, or
dispatch tasks themselves (JL 2026-07-07 ruling):

```
PROBE:
  citation  → audit gaps → unmet gap becomes a question SECTION → harvest the answering QA
              file's source anchors → _CITATION_ → 🔍 for CHECK
  values    → audit numbers → unsourced number becomes a question SECTION → harvest the QA
              file's value anchors → _VALUES_
  display   → audit needs → missing unit → DR row in the 4-display inbox → link existing/done
              units → _DISPLAY_ + tex
```

Every lane obligation is written into the probe SECTION (`harvest: OWED → accepted`);
`check-probe-cards.sh` FAILs an OWED lane or a `planned` section at VERIFY and at the CHECK gate.

Hard boundary: the DISPATCHED executor finds, the harvesters follow pointers, the human verifies in CHECK. The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots, NEVER searches inline during PROBE.

## Progression order

```
DRAFT first, PROBE second, REVISE third, CHECK last:

  draft (structure + REAL prose, placeholders for unverified)
           ↓
  ⛔ user structure review — [GATE] logged, user's verb advances
           ↓
  probe: cite + val + disp   (can run in parallel)
           ↓
  revise (dispatched workers change the .md directly, leave
          why-comments, sync .md → tex; workers line in _LOG)
           ↓
  check (verification gate → human decision; commits only after)
           ↓
  compile
```
