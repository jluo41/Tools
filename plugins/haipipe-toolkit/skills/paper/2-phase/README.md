# 2-phase -- declared phase engine (shared across lifecycle stages)

The **phase dimension** of the paper skill architecture. Phase workers are shared across all lifecycle stages (seed, claims, pitch, narrative, display, section-edit). The hub for section-edit lives in `1-lifecycle/haipipe-paper-stage/stages/5-section-edit//`.

```
Typical stage:        DRAFT 🤖 → PROBE 🤖 → REVISE 🤖 → CHECK 🧑
Venue stage:          DRAFT 🤖 → PROBE 🤖 ───────────→ CHECK 🧑
                      stage.md declares the ordered phases and gates.
                      All current stages have one human gate: CHECK.

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
├── 0-draft/                            ← DRAFT: settle structure + sentences + raise Q-consumers
│   ├── haipipe-paper-draft                 hub: structure + draft sentences + questions
│   ├── haipipe-paper-draft-citation        source holes → \cite{TOADD} [Q-<Stage>-<n>]
│   ├── haipipe-paper-draft-values          number holes → {VAL:? <what>} [Q-<Stage>-<n>]
│   └── haipipe-paper-draft-display         display holes → DR row in _DISPLAY_REQUEST.md
│
├── 1-probe/                            ← PROBE: agent-only within the --depth ceiling
│   └── haipipe-paper-probe                 ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET
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

- **DRAFT** 🤖: writes the artifact and raises every unresolved Q-consumer question. It does not touch `1-probes/` and opens no gate unless `stage.md` explicitly declares one.
- **PROBE** 🤖: owns ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET; dispatch is limited by the human-supplied `--depth` ceiling.
- **REVISE** 🤖: when declared, is PROOF-CARRYING — reached only via `Skill(haipipe-paper-revise)`; changes the prose directly, leaves why-comments, and records `workers: content ✓ humanizer ✓ …` in the owning S page's `## Log`.
- **CHECK** 🧑: human + agent (auto-checkers report, human decides: proceed/restart/accept/park). Never commit before CHECK opens.

The stage router runs its declared phases in order. A phase verb can restart or
target one phase. The agent never self-advances past a declared human gate.

## Holes: FILLED or OWNED

DRAFT's done-state. Every hole in the prose is either FILLED, or OWNED — carrying the id of the question that will settle it:

```
a source it cannot verify   →  \cite{TOADD} [Q-<Stage>-<n>]
a number it does not have   →  {VAL:? <what>} [Q-<Stage>-<n>]
a display that does not exist →  a DR row in 0-lifecycle/3-display/_DISPLAY_REQUEST.md
```

Each `Q-<Stage>-<n>` is a Q-consumer in the stage doc (it holds the
STAKE). PROBE binds it to a `QXn_<slug>.md` ENTRY in
`1-probes/PPNN_<topic>/`, dispatches within the ceiling, and harvests the answer
into `### a-executor`; REVISE's `-place` worker substitutes landed answers.

## The probe phase

ALL acquisition goes through `haipipe-paper-probe`, which authors and executes
the plan from the S page's Q-consumer. `1-probes/` is the consumer-side source
of truth; phase history lives in the owning S page's `## Log`. Full contract:
`1-probe/README.md` and `../../probe/haipipe-probe/SKILL.md`.

`check-probe-cards.sh` FAILs a `planned` entry, an unresolvable `target`, and an `answered` target whose `### a-executor` is still empty — at the worker's VERIFY step and again at the CHECK gate.

Hard boundary: the DISPATCHED executor finds, the paper follows pointers, the human verifies in CHECK. The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots, NEVER searches inline during PROBE.

## Progression order

```
DRAFT first, PROBE second, each remaining declared phase next, CHECK last:

  draft (structure + REAL prose; every hole FILLED or OWNED; Q-consumers raised)
           ↓
  probe (author entries, MATCH, dispatch allowed work, point + harvest)
           ↓
  revise (when declared: place runs FIRST; workers update prose and log provenance)
           ↓
  check (verification gate → human decision; commits only after)
           ↓
  compile
```
