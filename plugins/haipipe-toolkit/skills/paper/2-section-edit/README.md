# 2-section-edit — per-section DRAFT-GATHER-POLISH-CHECK

The **section-edit stage** for a paper. The combined hub
(`haipipe-paper-section-edit`) owns the full per-section lifecycle.
Layer workers are organized by phase.

```
Per-section lifecycle:  DRAFT → GATHER → POLISH → CHECK → sync → compile
                        (L1-L3)  (L4-L6)  (L7)     (L8)

DRAFT lives in the hub (haipipe-paper-section-edit).
GATHER, POLISH, CHECK live here as layer workers.
```

## Structure

```
3-write-edit/
├── README.md                  ← you are here
├── USAGE.md                   ← recipes, the reply grammar, the effort dial
├── WIRING.md                  ← routing and dispatch
├── haipipe-paper-edit/        ← ORCHESTRATOR: catalog + agents + the edit cycle
│
├── gather/                    ← L4-L6: display, values, citation
│   ├── haipipe-paper-edit-values               L5  every number matches its source
│   ├── haipipe-paper-edit-citation              L6  every \cite resolves and supports its claim
│   ├── haipipe-paper-edit-check-reference       L6  reference verification (script-backed)
│   ├── haipipe-paper-edit-manual-review-citations  L6  manual citation review
│   └── haipipe-paper-edit-manual-review-values     L5  manual values review
│
├── polish/                     ← L7: prose (actual sentence-level writing)
│   ├── haipipe-paper-edit-write                L7  fresh draft from outline
│   ├── haipipe-paper-edit-write-conference     L7  conference-style draft
│   ├── haipipe-paper-edit-write-scientific     L7  scientific-style draft
│   ├── haipipe-paper-edit-write-systems        L7  systems-style draft
│   ├── haipipe-paper-edit-weaving              L7  rebuttal-driven revision (paragraph polish)
│   ├── haipipe-paper-edit-content              L7  content review (what sentences say, de-AI)
│   └── haipipe-paper-edit-results-revision     L7  results-specific revision
│
├── check/                     ← L8: checklist (final verification)
│   ├── haipipe-paper-edit-claim-audit          L8  every claim traceable to evidence
│   ├── haipipe-paper-edit-consistency          L8  terminology, \label/\ref, notation
│   ├── haipipe-paper-edit-format               L8  venue style, headings, units
│   ├── haipipe-paper-edit-typeset              L8  widows, orphans, overfull boxes
│   ├── haipipe-paper-edit-proof-checker        L8  proof verification
│   ├── haipipe-paper-edit-reviewer             L8  self-review
│   └── haipipe-paper-edit-submission-audit     L8  final submission check
│
├── tools/                     ← cross-cutting utilities
│   ├── haipipe-paper-edit-diffpdf              tracked-changes PDF
│   ├── haipipe-paper-edit-to-overleaf          export to Overleaf
│   ├── haipipe-paper-edit-optimizer            optimization pass
│   ├── haipipe-paper-edit-improve-loop         iterative improvement
│   └── haipipe-paper-edit-diagram              section logic diagrams
│
├── agents/                    ← stage agents (fan out annotators)
├── sections/                  ← per-section playbooks
├── scripts/                   ← utility scripts
├── _shared/                   ← contracts every sub-skill obeys
└── _test/                     ← tests
```

## The edit cycle within each phase

Each phase follows the comment-first discipline:

```
GATHER:  L5 values     → annotate numbers needing verification → human confirms → trace to source
         L6 citation   → annotate missing/wrong cites → human confirms → Scholar verify + place

WRITE:   L7 prose      → draft from outline → comment-first review → human ========> reply → apply

CHECK:   L8 checklist  → annotate issues (format, consistency, claims) → human confirms → fix
```

Comment-first means: Round 1 inserts findings as `%% {CC-<topic>-vMMDD}: ...` comments.
The human replies on the same line: `========> {JL vMMDD}: accept|reject|modify|discuss`.
A later apply round acts on accepted comments only.

## Progression order

```
GATHER first, WRITE second, CHECK last:

  gather/values + gather/citation   (can run in parallel)
           ↓
  polish/edit-write or polish/content  (prose uses gathered materials)
           ↓
  check/format → check/consistency → check/claim-audit → check/submission-audit
```

Review wide in parallel within a phase; advance phases in dependency order.

## Relationship to the editing scaffold

```
1-lifecycle/haipipe-paper-editing/    PLAN (L1-L3) + per-section hub
  ├── L1 paper structure              z-structure scaffold
  ├── L2 section structure            outline structure block
  ├── L3 narrative                    ¶ headlines + previews + draft sentences
  │
  └── dispatches to 3-write-edit/:
      ├── gather/   L4-L6             values, citation verification
      ├── polish/    L7                prose drafting and polishing
      └── check/    L8                final verification
```

The editing scaffold tracks progress across all layers. The 3-write-edit/ skills
are the layer workers that do the actual work. The scaffold owns the _CITATION_
and _VALUES_ tracking files; the gather/ skills update them.
