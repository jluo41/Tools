---
name: haipipe-page-content
description: >-
  The 03 CONTENT phase of a Board Page. WRITE turns an approved,
  evidence-aware outline into Page Content, improves it under the same
  promise, builds the declared delivery projections, and performs a cold
  pre-check before handing one concrete version to the independent CHECK
  phase. Owns Page Division Writing Runs; replaces the active DRAFT and REVISE
  phase split. Trigger: page content, CONTENT phase, WRITE cycle, division
  writing, draft page, revise page, build page, /haipipe-page-content.
metadata:
  version: "0.2.1"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-content · write and build one evidence-aware Page version

Load, in order: `haipipe-page`, `haipipe-page-workflow`, this skill, the
Folder-owning workflow or canonical family skill, the exact Page Face owner,
`haipipe-plugin-outline/ref/plan-grammar.md`, applicable narrative/style
policy, `haipipe-run`, and the writing/build workers selected by that owner.
Load the owner once when one skill fills both Folder and Page Face roles.

CONTENT is one phase with one cycle. Drafting, revising, building, and
pre-checking are movements inside that cycle, not four Page phases:

```text
03 CONTENT · haipipe-page-content
└── WRITE
    ├── Draft       plan/evidence → division candidates
    ├── Revise      improve realization under the same promise
    ├── Build       regenerate declared delivery artifacts
    └── Pre-check   cold, non-closing readiness judgment
```

## ⚡ Brief

```text
ASKS     does this Page version realize the approved plan using only ready,
         folded Evidence Item Results?
READS    frozen Context record · approved outline · folded Evidence Items ·
         Local Results · applicable requirements/style policy · current Page
WRITES   Page Content, Opening/Aims when authorized, delivery projections,
         Page Division Writing Tickets/Results, log, CONTENT receipt
EXITS    every commissioned division Result is accepted and promoted; declared
         artifacts are current; a fresh pre-check reports ready
ROUTES   CHECK · CONTENT again · CONTEXT · OUTLINE · EVIDENCE · HOLD
TICK     none. CONTENT never approves or closes its own version
```

## 🧱 One division is the normal writing target

The addressed plan Bullet remains the trace unit, but a Level-4 writing Run
normally targets one Content division:

```text
target       C<n> from the approved plan
input        frozen Context + approved plan slice + folded Evidence Results
execution    one Page · Division Writing Run
result       one reviewable division candidate + trace/readiness report
promotion    accepted candidate replaces or creates that Page division
```

Several divisions may run in parallel when their inputs and Page write ranges
do not overlap. The final promotion is serialized in reader order. A trivial
same-session wording fix may remain an internal WRITE movement when it does
not satisfy the four Run tests; do not mint Runs merely to count edits.

## ⚙️ Run Profile

```text
ALLOWED      family Page · Division Writing; operation division-writing
TARGET       exactly one C<n> per Run; cardinality 0..D for D commissioned divisions
TICKET       <page>/runs/rNN_page-division-writing_cNN.<dialect>
INPUTS       <stem>-context.md + approved outline version + every folded local
             Evidence Result used by C<n> + current Page version
WORKER       haipipe-page-content plus the selected Page Face owner/narrative/style skill
RESULT       <page>/results/<RUNNAME>/ with candidate.md, trace.md, runtime.yaml
ACCEPT       candidate covers its plan bullets; every factual claim maps to a
             folded item or declared source; no unsupported hole; style and
             Page Face owner checks pass
PROMOTION    CONTENT writes the accepted candidate into <page>.md and records RUNNAME
REOPEN       context, plan, evidence Result, Page Face owner, acceptance, or target changed
```

For Job-backed Task Folders, resolve the Result through the `haipipe-run`
dialect instead of copying it into the Page Folder.

## ① Draft

- Enter only when Context is resolved and the plan version is approved.
- For each commissioned division, freeze only the addressed plan slice and
  Evidence Results it uses.
- A Section Page keeps one sentence slot per planned Bullet; other Page Face owners
  may realize one Bullet as one or more sentences.
- End each realized unit with its stable plan address according to the Page
  Type's sentence contract.
- Never invent a number, source, interpretation, or display. A missing support
  routes to EVIDENCE or OUTLINE.

## ② Revise

Revise under a fixed purpose, Aims, approved plan, and evidence boundary.
Improve argument, sequence, clarity, voice, citations, and captions. If the
promise or structure must change, stop and route to OUTLINE; if a governing
policy changed, route to CONTEXT.

Direct writes are the default. Candidate-only mode is used only when the user
explicitly asks to compare alternatives.

## ③ Build

Regenerate only the delivery projections declared by the Page Face owner or owning
workflow, such as `delivery/latex/`, `delivery/word/`, or render outputs. The
source Page remains the authority. A stale or failed build keeps CONTENT open;
it is not a CHECK finding yet because no checkable version exists.

## ④ Pre-check

Use a fresh context to judge the built candidate against mechanics, function,
evidence trace, readability, and local requirements. Pre-check may return only:

```text
another pass   → CONTENT
ready          → CHECK
blocked input  → CONTEXT | OUTLINE | EVIDENCE | HOLD
```

It may not CLOSE and may not write a person-reserved tick. The independent
`haipipe-page-check` phase still cold-checks the exact final source/render
identity and is the only phase allowed to CLOSE.

## 🔀 Authority routing

| Finding | Route |
|---|---|
| policy, requirement, ownership, or related-context drift | CONTEXT |
| argument, division shape, bullet expectation, or Aim promise is wrong | OUTLINE |
| Supporting/Local Result missing, stale, or unsuitable | EVIDENCE |
| prose, citation placement, caption, or build realization needs work | CONTENT |
| built version is ready for independent judgment | CHECK |
| required input cannot be obtained safely | HOLD |

## 🧾 Receipt

```text
phase: CONTENT
cycle: WRITE
context: <context record version/hash>
plan: v<N> approved ✅
division_runs: [<RUNNAME → Result → promoted C<n>>]
page: <source version before → after>
delivery: [<artifact paths>]
pre_check: ready | another-pass | blocked
artifacts: [<every written path>]
evidence: [<plan, context, Result, and check paths>]
route: CONTENT | CONTEXT | OUTLINE | EVIDENCE | CHECK | HOLD
next_cycle: WRITE | PREPARE | SHAPE | SURVEY | LAND | CHECK  # omit on HOLD
reason: <authority exercised and why the route follows>
reopens_promise: <true only when routing to OUTLINE because the promise changed>
```

## 🚧 Boundaries

- Do not change the approved plan or Evidence Item contract in place.
- Do not execute an Evidence Item Run or treat prose as an Evidence Result.
- Do not write a CHECK verdict, `accepted:`, `approved:`, or `Decide`.
- Do not count Draft/Revise/Build/Pre-check movements as separate Level-4 Runs.
- Do not leave a promoted Page division without the writing Run or explicit
  no-Run rationale that produced it.

## 📂 Files

```text
haipipe-page-content/
├── SKILL.md
├── CHANGELOG.md
└── ref/division-result.md
```

Historical DRAFT/REVISE/COMPILE receipt tokens are interpreted by the
lifecycle auditor. No redirect skills remain; every current writing dispatch
uses this skill and records `phase: CONTENT · cycle: WRITE`.
