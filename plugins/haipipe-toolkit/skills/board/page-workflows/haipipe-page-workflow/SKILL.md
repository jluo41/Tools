---
name: haipipe-page-workflow
description: >-
  The RUN router of the page family: the head skill of page-workflows/, combining the four phase contracts DRAFT, PROBE, REVISE, and CHECK into one bounded, auditable, non-linear loop over ONE Board Page. It owns the raw-material packet, the phase receipt written under <board>/_runs/page/, the producer/judge role separation, and the stop rules; the four sibling contracts own their phases, haipipe-page owns what a page IS, and haipipe-board owns the executable machinery. RUN is deliberately not ADVANCE: a Page may repeat a phase, branch, HOLD, or return to DRAFT in a new round, and only CHECK may CLOSE. Use when one Page must be driven through the automatic loop, when a run receipt must be audited, or when a workflow surface needs the page lifecycle's one authoritative state source. Trigger: run a page, run page lifecycle, automatic page loop, audit page workflow, page run receipt, RUN router, DPRC, page workflow head, /haipipe-page-workflow.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-15"
  summary: "Born 260815 by MOVING haipipe-page's RUN verb here, so the workflow has one nameable head beside its four members."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-workflow · the four phases, combined into one auditable RUN

`haipipe-page` is the door for ONE PAGE and says what a page IS.
This skill is the head of the page WORKFLOW: it drives one existing Page through the phases as a bounded loop and leaves a receipt.
It moved here from `haipipe-page`'s RUN verb on 260815, so the workflow pattern reads the same in every family: one folder, one head skill, its member skills beside it.

**Who owns what**:

```
haipipe-page               what a page IS · CREATE · WORK ON
haipipe-page-workflow      RUN · the packet · the receipt · the stop rules
page-workflows/ members    each phase's own authority
haipipe-board              the machinery this skill calls, never contains
```

## 🔁 The shape of the loop

**The routing grammar**: authority-selected, never a conveyor belt.

```
✏️ DRAFT ──▶ 🔍 PROBE ──▶ 🖊 REVISE ──▶ ✅ CHECK ──▶ CLOSE
   ▲            (skippable)                 │
   └───────────── CHECK routes backward ────┘
```

Each phase may repeat, PROBE is skipped when no consequential unknown exists, and CHECK may route to REVISE, PROBE, or a new DRAFT round.
Which phase runs next is decided by AUTHORITY (`haipipe-page`'s authority test), not by position, which is why the verb is RUN and not ADVANCE.

**The four members**, each its own contract beside this file:

```
phase       authority                                          load
────────────────────────────────────────────────────────────────────────────────
DRAFT       define or reopen purpose, Aims, promised shape     ../haipipe-page-draft
PROBE       resolve a consequential unknown across the wall    ../haipipe-page-probe
REVISE      improve the realization while Aims stay fixed      ../haipipe-page-revise
CHECK       judge one version and route its next authority     ../haipipe-page-check
```

## 🔁 run one Page lifecycle

RUN is the automatic, bounded loop. Use it when the process itself must be
exercised and audited, rather than when one known edit is enough.

1. Read `ref/page-run-contract.md` and assemble its raw-material packet. Resolve
   the Page Type from the filename. For a new Page, CREATE and register it first
   (that verb stays with `haipipe-page`), then start at DRAFT. For an existing
   Page with no known next authority, start at CHECK. Before each phase dispatch,
   materialize that phase's Related Board Pages packet with
   `haipipe-board/cli/pagecontext.py`; an invalid row or missing scope is a
   named HOLD, never omitted context.
2. Invoke `haipipe-board/ref/page-lifecycle.workflow.js` with the packet. The
   workflow dispatches a phase-scoped producer for DRAFT, PROBE, or REVISE, a
   mechanical builder/version snapshot, and a fresh read-only reviewer for
   CHECK.
3. Follow returned routes rather than a prescribed order. Only CHECK may CLOSE.
   A route to DRAFT from another phase begins a new round only when purpose or an
   Aim reopened.
4. Stop at CLOSE, explicit HOLD, a missing input, a version mismatch, a required
   human gate, `max_steps`, or `max_rounds`. A limit stop means the run did not
   converge; it never means quality passed.
5. Write the exact Workflow result to
   `<board>/_runs/page/<page-id>/<run-id>.json`. Do not append the terminal CHECK
   result to the Page, because that would mutate the approved version.
6. Run `haipipe-board/cli/pageflow.py audit <receipt.json>`. Report the terminal
   route, checked version, traversed edges, deterministic finding count,
   semantic finding count, human-gate state, and residual risk.

RUN never lets one hidden pass write, judge, fix, and approve. The producer and
judge have different actor identities, and every changed version returns
through CHECK before CLOSE.

## 🧾 The receipt is the workflow's one state source

`<board>/_runs/page/<page-id>/<run-id>.json` is where a run's history lives, in the exact shape `ref/page-run-contract.md` fixes.
A surface that shows where a page stands in its lifecycle reads these receipts and nothing else, the same way the labeling stepper reads `## States`.
A page with no receipts is not an error: its next authority is the contract's own default, CHECK for an existing page, DRAFT for a new one.

## 📂 Files

**This skill's own files**: what ships in the folder, and what each part is for.

```
haipipe-page-workflow/
├── SKILL.md            this contract
├── CHANGELOG.md        version history
└── ref/
    └── page-run-contract.md   the packet + receipt spec RUN and its members share
```

The executable machinery stays under `haipipe-board`: `ref/page-lifecycle.workflow.js` (the controller), `src/page_lifecycle.py` (the deterministic auditor), and `cli/pageflow.py` (the audit CLI).
The non-interactive dispatch target is `agents/haipipe-page-orchestrator-agent.md`, which invokes this contract in a fresh context.
