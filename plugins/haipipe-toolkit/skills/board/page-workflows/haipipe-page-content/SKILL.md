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
  version: "0.8.4"
  last_updated: "2026-09-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-content · write and build one evidence-aware Page version

Load, in order: `haipipe-page`, `haipipe-page-workflow`, this skill, the
Folder-owning workflow or canonical family skill, the exact Page Face owner,
`haipipe-plugin-outline/ref/plan-grammar.md`, applicable narrative/style
policy, `haipipe-run`, and the writing/build workers selected by that owner.
Load the owner once when one skill fills both Folder and Page Face roles.
For `folder-kind: task`, also load the reader-facing `haipipe-page-task`
companion; it supplies the Task Page's display-density and display-unit
contract without taking ownership of P-B-E-R.

CONTENT is one phase with one cycle. Drafting, revising, building, and
pre-checking are movements inside that cycle, not four Page phases:

```text
03 CONTENT · haipipe-page-content
└── WRITE
    ├── Entry check  approved plan/evidence + manuscript form budget
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
EXITS    the entry checklist passes; every commissioned division Result is accepted and promoted; declared
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
             folded item or declared source; draft mode may carry only named
             [E## pending] gates and final mode permits no unsupported hole;
             style and Page Face owner checks pass
PROMOTION    CONTENT writes the accepted candidate into <page>.md and records RUNNAME
REOPEN       context, plan, evidence Result, Page Face owner, acceptance, or target changed
```

For Job-backed Task Folders, resolve the Result through the `haipipe-run`
dialect instead of copying it into the Page Folder.

## ⓪ Entry check · the OUTLINE → CONTENT gate

Before allocating a Division Writing Run, write one compact entry-check record
from the current files. This is a handoff audit, not another plan and not a
draft. It must distinguish hard authority gates from form-range warnings.

```text
AUTHORITY  Context record is fresh · selected outline has G>=1 and either an
           explicit Shape approval or an evidence revision that declares and
           inherits its approved shape-base · every locally attainable typed
           item is folded from a complete accepted Local Result · every
           unresolved server/person gate is named on the approved plan · every
           Bullet has typed evidence or explicit none
NAMES      Page/Section name · ordered Content-division or subsection names ·
           paragraph jobs · any venue deviation and its ruling
STRUCTURE  divisions/subsections · paragraphs by division · total paragraphs ·
           sentence slots by paragraph · total sentence slots
LENGTH     declared word target · expected words per slot = target / slots ·
           applicable sentence-length center or limit and its named authority
REFERENCES CITE Items · verified source entries · planned citation-bearing
           slots · planned density = citation-bearing slots / all slots ·
           unique source keys and key density reported separately
EVIDENCE   typed/folded/stale counts · Result paths resolve · coverage is 100%
VERDICT    ready for WRITE | return to CONTEXT | OUTLINE | EVIDENCE | HOLD
```

For a Section Page, load the Section owner's form rules and use
`haipipe-paper-section/cli/section-stats.py` to measure any existing prose as a
baseline and every drafted candidate after promotion. Before prose exists,
sentence length is an expected value from the declared word budget, not an
actual measurement. If no authoritative word, paragraph, sentence-length, or
citation-density target exists, report `not specified`; never invent a venue
rule or silently borrow one from another Section.

Read the current plan and generated Evidence inventory once. Follow only the
Local Result pointers selected by the current Evidence Items; do not enumerate
historical Result trees unless a selected pointer, status, or hash disagrees.
Stop the entry audit as soon as every row has a supported verdict.

Keep four citation units separate: CITE Evidence Items, verified source
entries, citation-bearing sentence slots, and future citation-key mentions.
Only `citation-bearing slots / all slots` is the planned citation density.
After drafting, measure actual citation-bearing sentences, citation commands,
and key mentions from the prose and compare them with the plan.

A failed authority row blocks WRITE. A missing locally attainable Result also
blocks WRITE. A named secure-server or person gate may enter explicit draft
mode under the placeholder rule below; final mode still rejects it. A form metric outside a named
venue or paper requirement blocks only when that authority makes it binding;
otherwise mark it `⚠ review`, explain the tradeoff, and let the human decide.
For MISQ Section prose, treat a median near 21 words (normally within an
18–24-word center) as a comfortable house style unless a direct contract
overrides it. Sentence length is a
distribution, not a target for every sentence: vary short and long sentences
with their jobs. A sentence above 30 words triggers `⚠ review`, never an
automatic split or blocker; split it only when it stacks separable reader moves
or its syntax obscures the main claim.

## ① Draft

For a `folder-kind: task` Page, apply `haipipe-page-task` before drafting:
the display inventory is part of SHAPE, and numeric/empirical Content may
not be finalized as prose-only. Each Data or Result division needs its
substantive table or figure, and the method/provenance argument needs its
diagram when that visual carries reader meaning.

- Enter only when Context is resolved and the plan has `G>=1`. Use either an
  explicitly approved Shape version or an evidence revision that declares and
  inherits that Shape approval. Never write or refresh Content from `v0.*`.
- Refresh Content after every accepted plan-version change. A Shape revision
  may alter structure and prose. An evidence revision updates only affected
  realizations, citations, values, displays, and their traces; unchanged prose
  is still revalidated against the exact new plan version.
- For each commissioned division, freeze only the addressed plan slice and
  Evidence Results it uses.
- A Section Page keeps one sentence slot per planned Bullet; other Page Face owners
  may realize one Bullet as one or more sentences.
- A normal manuscript paragraph contains 4–6 sentences. Grow an underdeveloped
  paragraph by adding warranted one-point sentences, not by lengthening its
  existing sentences.
- A Section sentence realizes one point. Do not fuse a definition, mechanism,
  boundary, result, and transition merely to save space. For MISQ, keep the
  median around 18–24 words while varying individual sentence lengths. Review
  a 30+ word sentence for stacked moves or difficult syntax; keep it when one
  coherent relation is clearer in the longer form.
- Let paragraph logic carry the flow. Avoid formulaic connective ladders,
  repeated three-part templates, inflated framing, and clause-stacked prose;
  preserve calibrated hedging and exact theoretical terms.
- Keep workflow bookkeeping out of reader prose. Words such as `historical`,
  `provisional`, `pending`, and `will be replaced` belong in the Evidence Item,
  Result, or Discussion record, not in the manuscript.
- When an older accepted value exists, write that value plainly and keep its
  provisional caveat in the evidence record. When no value exists and the
  approved plan names a server/person gate, draft mode may place exactly one
  visible marker `[E## pending]` at the owed realization. It is a drafting aid,
  not evidence; final mode rejects every such marker.
- End each realized unit with its stable plan address according to the Page
  Type's sentence contract.
- Enforce the addressed Bullet's evidence boundary. A citation placement
  requires a CITE Item on that same Bullet; a concrete empirical value requires
  a VALUE Item there; a placed figure or table requires its DISPLAY Item.
  `Evidence: none` forbids all four. If the prose needs material the Bullet did
  not declare, return it to OUTLINE/SHAPE before writing.
- Do not inherit evidence from another sentence slot in the same paragraph.
  Even when two Bullets cite the same source, CONTENT traces each placement to
  that Bullet's own CITE Item; source and Supporting Run reuse happen beneath
  the two distinct Items.
- Never invent a number, source, interpretation, or display. A missing support
  routes to EVIDENCE or OUTLINE.

## ② Revise

Revise under a fixed purpose, Aims, approved plan, and evidence boundary.
Improve argument, sequence, clarity, voice, citations, and captions. If the
promise or structure must change, stop and route to OUTLINE; if a governing
policy changed, route to CONTEXT.

For manuscript headings, apply `haipipe-paper-section`'s “Reader-facing
subsection titles” contract: validate title-to-body fit and synchronize an
authorized naming repair across the current Outline, Content, Aims, and built
delivery. A title repair alone is not permission to rewrite the argument.

Before Build, run `haipipe-paper-revise-humanizer`, then have a fresh-context
reviewer compare the revised prose with measured passages from named MISQ
exemplars and return a style verdict. Record both receipts. A requested
`writing-only` review may judge argument and prose while unresolved values stay
in explicit `[E## pending]` markers; exclude those markers from the style
verdict and do not mistake that review for final readiness.

Direct writes are the default. Candidate-only mode is used only when the user
explicitly asks to compare alternatives.

## ③ Build

Regenerate only the delivery projections declared by the Page Face owner or owning
workflow, such as `delivery/latex/`, `delivery/word/`, or render outputs. The
source Page remains the authority. A stale or failed build keeps CONTENT open;
it is not a CHECK finding yet because no checkable version exists.

After Build, assemble the user-check packet from
`../../haipipe-page/ref/user-check-packet.md`: rebuild affected DISPLAY
previews, rebuild the one-Page LaTeX PDF when Page prose or an embedded display
changed, and give the verified Board Page URL where the generated Outline table
can be read. Surface 2 lists the evidence a person can open now (Display
PDFs, the citation register, VALUE item cards); surface 3 states whether
Revise ran, so a first draft is never shown as final; surface 4, the
Page/Section PDF, is the delivery shown after Revise, never the paper master.
For a Task Page, this build is incomplete if the declared table, figure, or
diagram units lack current `preview.pdf` files or the Page-level PDF contains
only their references instead of the winning floats.

When the person asks for a complete version, deliver the requested LaTeX/PDF
and Word projections, report the PDF page count, and return the reader-facing
viewer link. Trim figure PDFs to their content margins before assembly. If a
named server/person gate prevents a final build, return the best available
draft PDF first with its visible evidence markers; final build mode must fail
while any `[E## pending]` marker remains.

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
plan: v<G>.<S>[.<E>] · Shape approved directly or inherited ✅
entry_check: authority/evidence pass · form ready or named warnings
division_runs: [<RUNNAME → Result → promoted C<n>>]
page: <source version before → after>
delivery: [<artifact paths>]
build_manifest: <owning delivery/build-manifest.json, when this build emits one>
user_check_packet: Board Outline URL · evidence to open now (Display PDFs · citations · value cards) · Content state after Revise · current Page-level PDF
revise: humanizer receipt · fresh-context MISQ style verdict
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
