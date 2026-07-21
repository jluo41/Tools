# 2-phase -- DRAFT-PROBE-REVISE-CHECK (shared across lifecycle stages)

The **phase dimension** of the paper skill architecture. Phase workers are shared across all lifecycle stages (seed, claims, pitch, narrative, display, section-edit). The hub for section-edit lives in `1-lifecycle/haipipe-paper-stage/stages/5-section-edit//`.

```
Per-stage lifecycle:  DRAFT 🤖→🧑 → PROBE 🤖 → REVISE 🤖 → CHECK 🧑
                      ⛔ two gates: the DRAFT structure review and CHECK.
                      Unattended? a fresh-context reviewer subagent stands in
                      at each gate — the gate is delegated, never skipped.

Status strip:
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

## Structure

```
2-phase/
├── README.md                           ← you are here
├── USAGE.md                            ← recipes, reply grammar, effort dial
├── WIRING.md                           ← routing and dispatch
├── REF/                                ← shared references (prose-quality, comment-protocol,
│                                         paragraph-indexing, sentence-format, tex-file-anatomy,
│                                         paper-folder-anatomy)
│
├── 0-draft/                            ← DRAFT: settle structure + sentences, ORGANIZE + MATCH
│   ├── haipipe-paper-draft                 hub: structure + draft sentences + the probe plan
│   ├── haipipe-paper-draft-citation        source holes → \cite{TOADD} [Q-<Stage>-<n>]
│   ├── haipipe-paper-draft-values          number holes → {VAL:? <what>} [Q-<Stage>-<n>]
│   └── haipipe-paper-draft-display         display holes → DR row in _DISPLAY_REQUEST.md
│
├── 1-probe/                            ← PROBE: agent-only, flag for CHECK
│   └── haipipe-paper-probe                 DISPATCH → POINT → INTERPRET (harvest inline)
│
├── 2-revise/                           ← REVISE: venue-quality prose (auto)
│   ├── haipipe-paper-revise                hub: routes the pass
│   ├── haipipe-paper-revise-place          runs FIRST: lands answers into their placeholders
│   ├── haipipe-paper-revise-content        content + ¶-flow (WHAT sentences say, HOW ¶s weave)
│   ├── haipipe-paper-revise-humanizer      de-AI audit (HOW sentences sound)
│   └── haipipe-paper-revise-results        results-specific revision
│
└── 3-check/                            ← CHECK: human + agent gate
    ├── haipipe-paper-check                 6-axis verification gate
    └── haipipe-paper-proof-checker         math proof verification
```

Whole-paper skills (scaffold, conform, restructure, claim-audit, optimizer, reviewer, polish, compile, diffpdf, to-overleaf) live in `3-deliver/`, grouped `1-build/ 2-audit/ 3-polish/ 4-ship/`.

## Naming convention

```
haipipe-paper-{phase}-{what}    phase workers (this directory)
```

## Phase automation

- **DRAFT** 🤖→🧑: agent writes the REAL draft (complete prose with real `\citep{}` keys from .bib) AND authors the probe plan (① ORGANIZE + ② MATCH). Every hole ends FILLED or OWNED → ⛔ HARD STOP: user reviews structure + the probe plan together; the user's verb/"go" is the gate (logged `[GATE]` in _LOG)
- **PROBE** 🤖: agent-only — runs the plan forward (③ DISPATCH → ④ POINT → ⑤ INTERPRET), flags for CHECK, no human gate
- **REVISE** 🤖: agent-only and PROOF-CARRYING — reached only via `Skill(haipipe-paper-revise)` (never inline); changes the prose directly per prose-quality.md on the .md FIRST then syncs to tex; leaves why-comments; `[REVISE]` _LOG entry carries `workers: content ✓ humanizer ✓ …`
- **CHECK** 🧑: human + agent (auto-checkers report, human decides: proceed/restart/accept/park). Never commit before CHECK opens.

The user drives phases with VERBS on the stage skill (`/haipipe-paper-stage section-edit <section> [draft|probe|revise|check]`); a bare invocation shows status and proposes — never runs — the next phase. The agent never self-advances past a human gate.

## Holes: FILLED or OWNED

DRAFT's done-state. Every hole in the prose is either FILLED, or OWNED — carrying the id of the question that will settle it:

```
a source it cannot verify   →  \cite{TOADD} [Q-<Stage>-<n>]
a number it does not have   →  {VAL:? <what>} [Q-<Stage>-<n>]
a display that does not exist →  a DR row in 0-lifecycle/4-display/_DISPLAY_REQUEST.md
```

Each `Q-<Stage>-<n>` is a Q-consumer in the stage doc (it holds the STAKE) bound to a `## QX<n>` ENTRY in `1-probes/PPNN_<topic>/` (it holds the question). PROBE dispatches the entry, harvests the answer into its `### a-executor`; REVISE's `-place` worker substitutes the landed answer into the placeholder.

## The probe phase

ALL acquisition goes through `haipipe-paper-probe`, executing the plan DRAFT authored. `1-probes/` is the only consumer-side source of truth; `_LOG_<stage>.md` is the only sidecar. Full contract: `1-probe/README.md` and `../../probe/haipipe-probe/SKILL.md`.

`check-probe-cards.sh` FAILs a `planned` entry, an unresolvable `target`, and an `answered` target whose `### a-executor` is still empty — at the worker's VERIFY step and again at the CHECK gate.

Hard boundary: the DISPATCHED executor finds, the paper follows pointers, the human verifies in CHECK. The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots, NEVER searches inline during PROBE.

## Progression order

```
DRAFT first, PROBE second, REVISE third, CHECK last:

  draft (structure + REAL prose; every hole FILLED or OWNED; the probe plan authored)
           ↓
  ⛔ user structure review — [GATE] logged, user's verb advances
           ↓
  probe (dispatch the OWNED questions, point each target, harvest into a-executor)
           ↓
  revise (place runs FIRST and lands the answers; then the workers change the .md
          directly, leave why-comments, sync .md → tex; workers line in _LOG)
           ↓
  check (verification gate → human decision; commits only after)
           ↓
  compile
```
