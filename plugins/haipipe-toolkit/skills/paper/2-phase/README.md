# 2-section-edit -- per-section DRAFT-GATHER-POLISH-CHECK

The **section-edit stage** for a paper. The combined hub
(`haipipe-paper-section-edit`) owns the full per-section lifecycle.
Phase workers are organized by phase.

```
Per-section lifecycle:  DRAFT → GATHER → POLISH → CHECK → sync → compile

Status strip:
§1:  draft ✅  │  display --  values --  citation 🚀  │  polish ⬜  │  check ⬜
```

## Structure

```
2-section-edit/
├── README.md                    ← you are here
├── USAGE.md                     ← recipes, the reply grammar, the effort dial
├── WIRING.md                    ← routing and dispatch
├── haipipe-paper-section-edit/  ← HUB: per-section lifecycle orchestrator
│
├── gather/                      ← GATHER: one skill per working doc
│   ├── haipipe-paper-section-edit-display    display  0-displays/ units
│   ├── haipipe-paper-section-edit-values     values   _VALUES_.md
│   └── haipipe-paper-section-edit-citation   citation _CITATION_.md
│
├── polish/                      ← POLISH: venue-quality prose
│   ├── haipipe-paper-section-edit-write                fresh draft from outline
│   ├── haipipe-paper-section-edit-write-conference     conference style
│   ├── haipipe-paper-section-edit-write-scientific     scientific style
│   ├── haipipe-paper-section-edit-write-systems        systems style
│   ├── haipipe-paper-section-edit-content              content review (WHAT)
│   ├── haipipe-paper-section-edit-humanizer            de-AI audit (HOW)
│   ├── haipipe-paper-section-edit-weaving              paragraph flow
│   └── haipipe-paper-section-edit-results-revision     results-specific
│
├── check/                       ← CHECK: section-level verification
│   └── haipipe-paper-section-edit-proof-checker        proof verification
│
├── tools/                       ← cross-cutting utilities
│   └── haipipe-paper-section-edit-diagram              paragraph-level ASCII diagrams
│
├── sections/                    ← per-section playbooks (intro, methods, etc.)
├── scripts/                     ← utility scripts
├── _shared/                     ← contracts (comment-protocol, sentence-format)
├── _test/                       ← tests
└── _archive/                    ← retired skills (merged into current ones)
```

Whole-paper skills (consistency, format, typeset, claim-audit, submission-audit,
diffpdf, optimizer, improve-loop, to-overleaf, reviewer) live in `3-build-submit/`
as `haipipe-paper-edit-*`.

## Naming convention

```
haipipe-paper-section-edit-*     section-level (this directory)
haipipe-paper-edit-*             whole-paper (3-build-submit/)
```

## The gather phase (AUDIT → SEARCH → CANDIDATE → [HUMAN] → PLACE → REVIEW)

Each gather skill owns one working doc and follows the same 6-phase lifecycle:

```
GATHER:
  display   → audit what's needed → plan units → route to task → [human approves] → link
  values    → audit numbers → trace to source → [human verifies] → place in tex
  citation  → audit gaps → search candidates → write to _CITATION_ → [human verifies on Scholar] → place \citep{}
```

Hard boundary: the agent searches and proposes; the human verifies and places.
The agent NEVER adds to .bib, NEVER fabricates numbers, NEVER creates ad-hoc plots.

## Progression order

```
DRAFT first, GATHER second, POLISH third, CHECK last:

  draft (structure + narrative sentences)
           ↓
  display + values + citation   (can run in parallel)
           ↓
  polish (rewrite draft sentences to venue quality)
           ↓
  check (section-level verification)
           ↓
  sync to tex → compile
```

## Comment-first discipline (POLISH phase)

Round 1 inserts findings as `%% {CC-<topic>-vMMDD}: ...` comments.
The human replies: `========> {JL vMMDD}: accept|reject|modify|discuss`.
A later apply round acts on accepted comments only.
