---
name: haipipe-page-context
description: >-
  The 00 CONTEXT phase of a Board Page. PREPARE collects, resolves, and
  freezes the policy, requirements, Page ownership, related information,
  feedback, and process records needed by later Page phases into one generated
  Context record inside the shared Outline plugin. Use before SHAPE, whenever
  the governing inputs changed, or when another phase reports missing or
  conflicting context. Trigger: page context, CONTEXT phase, PREPARE context,
  Context Workspace, outline context, collect page requirements,
  /haipipe-page-context.
metadata:
  version: "0.1.3"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-context · prepare the Page's decision context

Enter through `haipipe-page` and `haipipe-page-workflow`, then load this phase,
the Folder-owning workflow or canonical family skill, the exact Page Face
owner, and
`haipipe-plugin-outline/ref/record-shape.md`, in that canonical order. The
Outline plugin presents the generated record after authority is resolved.

CONTEXT is a Page phase, not a new Plugin. Its output is presented in
`haipipe-plugin-outline` beside the Page's other process records:

```text
haipipe-page-context      owns PREPARE and the generated context projection
haipipe-plugin-outline   owns the Context Workspace that presents it
source records           remain authoritative and physically separate
```

## ⚡ Brief

```text
PHASE    00 CONTEXT
CYCLE    PREPARE · Collect → Resolve → Freeze
ASKS     what exact context may the next Page phase rely on?
READS    Page + Folder identity · Folder owner · Page Face owner · policy ·
         requirement · feedback · discussion · files · log · ranked skills ·
         related Page fragments · current plan/evidence/run state
WRITES   outline/<stem>-context.md, generated; one CONTEXT phase receipt
EXITS    every required authority is named, conflicts and missing inputs are
         explicit, and every frozen source has an address plus freshness fact
ROUTES   OUTLINE · CONTEXT again · HOLD
RUNS     none. PREPARE is planning/context resolution, not a Level-4 Run
```

## 🧭 One Context Workspace, not two record groups

The Outline plugin exposes three workspaces:

```text
🧭 Outline
├── Bullet Workspace
├── Evidence Workspace
└── Context Workspace
    ├── Overview                 generated <stem>-context.md
    ├── Policy & Requirements   Folder owner + Page Face owner + Requirement
    ├── Related Information     Files rows and bounded related Page fragments
    ├── Feedback & Decisions    Feedback + open Discussion
    └── Records                 Files + Log + ranked Skills
```

This is one surface over several authorities. Do not concatenate the source
files, move them into a new folder, or make the generated Context record a
second source of truth. The record points to the sources and states how they
resolved for this Page version.

## ① Collect

Collect only sources that can change what the Page should become:

1. Resolve Folder identity from `workflow/phase.yaml`, then `folder-kind:`,
   then the compatibility `page-type:` route.
2. Read the Folder owner and Page Face owner contracts, if applicable. The
   Page Face owner is the exact workflow-phase, canonical family, or legacy
   Page-Type skill that owns the readable contract; load it once when it is
   also the Folder owner.
3. Read the full Page and its current Outline records: Requirement,
   Discussion, Feedback, Files, Log, and ranked Skills.
4. Materialize one-hop Related Board Page fragments declared by the Files
   record. Use `haipipe-board/cli/pagecontext.py`; do not infer dependencies
   from topic similarity.
5. Read the current plan, Evidence Item table, relevant Run receipts, and the
   latest Page workflow receipt only far enough to identify freshness and the
   next authority.

A source that cannot be read is recorded as missing. PREPARE never fills the
gap with a plausible rule.

If the named authority itself is stale or incomplete, CONTEXT does not repair
that upstream artifact. Return `HOLD` with its exact path, Folder or Page Face
owner skill, the required change, and `resume: CONTEXT/PREPARE`. A stale
Paper Narrative rule returns to `haipipe-paper-narrative`, the paper-journey
owner. A stale Venue rule returns to `haipipe-paper-venue`, the owning QBv bank
Page Face owner; Venue is a library, not a paper-journey phase. After the exact owner
repairs and versions the source, the consumer Page resumes at CONTEXT/PREPARE
and freezes the new source. CONTEXT owns resolution and handoff, not upstream
authorship.

## ② Resolve

Resolve authority from broad to specific:

```text
base Page + template
  → Folder-owning workflow or canonical family skill
  → Page Face owner
  → Page workflow phase
  → authored W<n> Requirement records
  → division and bullet contracts
```

A specific source may refine a broad source. It may not silently contradict
it. Record each conflict with both source paths and route to HOLD or CONTEXT;
do not choose the more convenient rule.

Resolve the five facts later phases need:

| Fact | Required answer |
|---|---|
| Identity | exact Page, Folder kind, owning workflow, current Page phase |
| Purpose | Page question, audience, scope, and non-goals |
| Structure | required Page shape, division expectations, and outline policy |
| Style | applicable narrative/writing rules with their authority paths |
| Evidence | current Evidence Items, accepted Result boundaries, and known gaps |

## ③ Freeze

Write `outline/<stem>-context.md` using `ref/context-record.md`. Every source
row carries a repository-relative path, role, and freshness fact. Use a
SHA-256 when stable bytes matter; use a durable version/receipt identifier
when the source owns its own version grammar.

The record may summarize a rule for orientation, but the path remains the
authority. It must clearly separate:

```text
resolved      safe for the next phase to use
missing       required source absent or unreadable
conflicting   two authorities disagree
stale         source changed after this context record
not-applicable deliberately absent under the resolved Page contract
```

If any required row is missing, conflicting, or stale, PREPARE does not exit
to OUTLINE.

## 🔄 Reopen law

CONTEXT is numbered `00` because it precedes Page construction, not because it
runs only once. Reopen PREPARE when any of these change:

- Folder kind, Folder owner, or Page Face owner;
- venue, policy, requirement, writing/narrative rule, or user instruction;
- a related Page fragment named by the context;
- accepted feedback or a settled Discussion ruling;
- the current plan/evidence binding in a way that changes what later phases
  are allowed to assume.

A content-only edit under the same frozen authority does not reopen CONTEXT.

## 🧾 Receipt

```text
phase: CONTEXT
cycle: PREPARE
context: outline/<stem>-context.md
sources: n resolved · n missing · n conflicting · n stale
identity: <Folder kind> · <Folder owner> · <Page Face owner or none>
artifacts: ["outline/<stem>-context.md"]
evidence: [<authority paths and version/hash facts>]
route: OUTLINE | CONTEXT | HOLD
next_cycle: SHAPE | PREPARE       # omit when route is HOLD
reason: <why the context is usable or what prevents it>
reopens_promise: false
```

The common field law is
`../haipipe-page-workflow/ref/page-run-contract.md`. A CONTEXT receipt is a
workflow receipt, not a Level-4 Run Result.

## 🚧 Boundaries

- Do not write the plan, Evidence Item contracts, Runs, Results, Page Content,
  delivery artifacts, or a CHECK verdict.
- Do not invent a policy, requirement, citation, number, or human decision.
- Do not turn Related Board Page navigation into evidence. Cross-Folder
  evidence enters through a named Supporting Run Result; a page-owned static
  source may be named in a future Local Input.
- Do not create `haipipe-plugin-context`. Context is an internal workspace of
  `haipipe-plugin-outline`.

## 📂 Files

```text
haipipe-page-context/
├── SKILL.md
├── CHANGELOG.md
└── ref/context-record.md
```
