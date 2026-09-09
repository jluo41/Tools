---
name: haipipe-page-content
description: >-
  The 03 CONTENT phase of a Board Page. WRITE turns an approved,
  evidence-aware outline into Page Content, improves it under the same
  promise, builds the declared delivery projections, and performs a cold
  pre-check before handing one concrete version to the independent CHECK
  phase. Owns Page Paragraph Writing Runs; replaces the active DRAFT and REVISE
  phase split. Trigger: page content, CONTENT phase, WRITE cycle, division
  writing, paragraph writing, draft page, revise page, build page, /haipipe-page-content.
metadata:
  version: "0.9.2"
  last_updated: "2026-09-08"
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
    ├── Entry check  approved plan/evidence + owner-declared form budget
    ├── Draft       plan/evidence → paragraph candidates
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
         Page Paragraph Writing Tickets/Results, log, CONTENT receipt
EXITS    the entry checklist passes; every commissioned paragraph Result is accepted and promoted; declared
         artifacts are current; a fresh pre-check reports ready
ROUTES   CHECK · CONTENT again · CONTEXT · OUTLINE · EVIDENCE · HOLD
TICK     none. CONTENT never approves or closes its own version
```

## 🧱 One paragraph is the normal writing target

The addressed plan Bullet remains the trace unit. A new Level-4 writing Run
targets exactly one paragraph; divisions still organize Content and Aims:

```text
target       C<n>.P<m> from the approved plan
input        Context/style + paragraph plan + folded Evidence + adjacent context
execution    one Page · Paragraph Writing Run
result       one reviewable paragraph + trace/readiness report
promotion    accepted paragraph replaces or creates that addressed Page paragraph
```

Plan the whole Section/Page, write paragraph by paragraph, then read the whole
division and Page for continuity. A one-division Section with six paragraphs
normally commissions six writing Runs, not one Section Run plus six children.
Do not turn every sentence, model call, or revision movement into another Run.

Default to reader-order drafting so each Run can consume the preceding accepted
paragraph. Independent paragraphs may be commissioned together only with frozen
seam expectations; promotion remains serialized and rechecks current neighbors.
An upstream paragraph change invalidates a dependent binding when its consumed
context changed materially. A trivial
same-session wording fix may remain an internal WRITE movement when it does
not satisfy the four Run tests; do not mint Runs merely to count edits.

Before commissioning, read `ref/paragraph-run.md`: it defines the Markdown
Ticket with its embedded prompt, exact Result files, style inputs, and promotion
checks. A prompt drafted in Outline is still planning; allocate the Ticket and
runtime receipt only when commissioning actual work. No new plugin or paragraph
folder level is needed. The bundled `cli/promote_paragraph.py` is the narrow
CONTENT write path for an accepted Result. Evidence and writing share `runs/`.

## ⚙️ Run Profile

```text
ALLOWED      family Page · Paragraph Writing; operation paragraph-writing
TARGET       exactly one C<n>.P<m> per Run; P Runs for P commissioned paragraphs
TICKET       <page>/runs/rNN_page-writing_cNN-pNN.md (prompt inside)
INPUTS       <stem>-context.md + approved outline version + every folded local
             Evidence Result used by C<n>.P<m> + Page version + paragraph
             requirements + any declared Narrative Decision + named style
             exemplars + optional Writing DNA packet + optional HAI anti-slop
             audit profile + adjacent context
WORKER       haipipe-page-content plus the selected Page Face owner/narrative/style skill
RESULT       <page>/results/<RUNNAME>/ with paragraph.md, trace.md, runtime.yaml;
             optional anti-slop.json when selected by the Ticket
ACCEPT       candidate covers its plan bullets; every factual claim maps to a
             folded item or declared source; draft mode may carry only named
             [E## pending] gates and final mode permits no unsupported hole;
             style and Page Face owner checks pass; any anti-slop report is
             diagnostic only and does not supply acceptance
PROMOTION    CONTENT writes only the addressed paragraph into <page>.md and
             records RUNNAME, target, Result hash, and Page before/after identity
REOPEN       context, plan, evidence Result, Page Face owner, acceptance, or target changed
```

The concrete promotion call is:

```bash
python3 Tools/plugins/haipipe-toolkit/skills/board/page-workflows/haipipe-page-content/cli/promote_paragraph.py \
  --page <page>/page.md \
  --result <page>/results/<RUNNAME> \
  --dry-run

python3 Tools/plugins/haipipe-toolkit/skills/board/page-workflows/haipipe-page-content/cli/promote_paragraph.py \
  --page <page>/page.md \
  --result <page>/results/<RUNNAME>
```

The Result `runtime.yaml` must be `family: page`,
`operation: paragraph-writing`, `status: complete`, and must include a
`page-source` input with the frozen Page SHA-256. The promoter takes a per-Page
lock, rechecks that hash, resolves the exact `C<n>.P<m>` structural address,
and refuses stale Pages, headings/lists/tables/fences, or apparatus/comment
records that its prose-only writer would orphan. It writes the Page and the
Run's lifecycle receipt atomically, verifies the addressed paragraph and final
hash, and records `promotion.status: promoted`. A second call is
idempotent; an interrupted `applying` receipt is recovered only when the
planned Page hash and candidate still match. A refusal routes to CONTENT,
OUTLINE, EVIDENCE, CONTEXT, or HOLD according to the reason; it never becomes
a CHECK verdict.

For Job-backed Task Folders, resolve the Result through the `haipipe-run`
dialect instead of copying it into the Page Folder.
Retain historical `division-writing` Tickets/Results without renaming or
splitting them. New paragraph work uses this profile and may cite the old
Result as prior prose, never as newly produced evidence.

## ⓪ Entry check · the OUTLINE → CONTENT gate

Before allocating Paragraph Writing Runs, write one compact entry-check record
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
           paragraph jobs · declared Narrative Decisions and their rulings ·
           any venue deviation and its ruling
STRUCTURE  divisions/subsections · paragraphs by division · total paragraphs ·
           sentence slots by paragraph · total sentence slots
LENGTH     declared word target · expected words per slot = target / slots ·
           applicable sentence-length center or limit and its named authority
REFERENCES CITE Items · verified source entries · planned citation-bearing
           slots · planned density = citation-bearing slots / all slots ·
           unique source keys and key density reported separately
CLAIMS     each approved proposition and verb strength fits its bound Evidence
           Result · no silent downgrade or upgrade · mismatch routes to
           OUTLINE/EVIDENCE before allocating a Paragraph Writing Run
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
blocks WRITE. Stop before allocating writing Tickets or runtime receipts;
record the finding in the phase record, not as a diagnostic Run. A named secure-server or person gate may enter explicit draft
mode under the placeholder rule below; final mode still rejects it. A form metric outside a named
venue or paper requirement blocks only when that authority makes it binding;
otherwise mark it `⚠ review`, explain the tradeoff, and let the human decide.
Sentence-length and paragraph targets come from the resolved Page Face owner
and the frozen Context's named policy. Record `not specified` when neither
declares one. Vary sentence length with the reader job; review difficult syntax
or stacked moves against that policy rather than importing a journal's range.

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
- For each commissioned paragraph, freeze its addressed plan slice, Evidence
  Results, any declared Narrative Decision, specific requirements, and
  consumed neighboring context. The Decision fixes the approved paragraph
  organization; Writing DNA may only render compatible surface choices.
  Read the whole approved argument first; the Ticket references that authority
  without creating another outline. A paragraph with an unclear job returns
  to SHAPE instead of receiving generic filler.
- A Section Page keeps one sentence slot per planned Bullet; other Page Face owners
  may realize one Bullet as one or more sentences.
- Follow the Page Face owner's paragraph budget. Grow an underdeveloped
  paragraph with warranted reader moves rather than padding sentences.
- A Section sentence realizes one point. Do not fuse a definition, mechanism,
  boundary, result, and transition merely to save space. Review stacked moves
  and difficult syntax under the resolved style policy; one coherent relation
  may be clearer in a longer sentence.
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

Apply the resolved Page Face owner's heading contract: validate title-to-body
fit and synchronize an
authorized naming repair across the current Outline, Content, Aims, and built
delivery. A title repair alone is not permission to rewrite the argument.

Before Build, run the revision workers selected by that owner and frozen
Context, then have a fresh-context reviewer judge the revised prose against
those named requirements and any declared exemplars. Record the exact policy,
workers used, and style verdict. For a Paper Section, load
`haipipe-paper-section` and run `haipipe-paper-revise-humanizer` when that
owner requires it; journal exemplars apply only to their declared venue.
Other Page owners supply their own policy. An optional worker that is not
applicable is recorded as such, never as a missing Paper gate. A requested
`writing-only` review may judge argument and prose while unresolved values stay
in explicit `[E## pending]` markers; exclude those markers from the style
verdict and do not mistake that review for final readiness.

When a Paragraph Ticket selects the HAI anti-slop adapter, run its read-only
audit after the candidate has been rendered with the approved content and
Writing DNA. Record the report beside the Result and route any finding to a
bounded CONTENT revision. Do not chain all ten external references, use their
scores as a Page gate, or invoke their auto-fix commands. If a revision changes
existing prose, compare preservation-sensitive facts before `wdiff.py` writes
the change record.

Dispatch prose-changing revision workers against the commissioned paragraph
inside its writing Run. A full-Page reviewer may identify affected paragraphs
but may not silently replace the whole Section outside their Result/promotion
trail. A worker that cannot honor that write scope is not selected for a direct
Page write; use its findings to commission bounded paragraph revisions instead.

Write the paragraph Result first, validate it, then promote it directly when
authorized; do not add a human approval gate for every paragraph unless the
owner/user requires one. Candidate-only mode is for explicit comparison asks.
An accepted Result remains immutable. Later material revision gets a new Run
with `supersedes`; unchanged-contract retries append attempts. Small no-Run
edits retain the host's word-level trail and an explicit no-Run rationale.

Before Build, read the assembled division/Section and Page in order. Check
repeated definitions, duplicated claims, abrupt seams, terminology, and
formulaic paragraph rhythms. Record findings in the CONTENT receipt by
paragraph address. Fix only affected paragraphs through their writing work;
do not silently rewrite the whole division after accepting paragraph Results.
If order, paragraph jobs, or claims must change, return to SHAPE. This integrated
review is an internal WRITE movement, not an extra umbrella Run or a new QA lane.

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
paragraph_runs: [<RUNNAME → Result/hash → promoted C<n>.P<m>>]
integration: <ordered division/Page read · seam findings and affected targets>
anti_slop: [<RUNNAME → report/hash → diagnostic findings or not-selected>]
page: <source version before → after>
delivery: [<artifact paths>]
build_manifest: <owning delivery/build-manifest.json, when this build emits one>
user_check_packet: Board Outline URL · evidence to open now (Display PDFs · citations · value cards) · Content state after Revise · current Page-level PDF
revise: <owner-selected revision receipts or not-applicable> · fresh-context style verdict against <named policy>
pre_check: ready | another-pass | blocked
artifacts: [<every written path>]
evidence: [<plan, context, Result, and check paths>]
route: CONTENT | CONTEXT | OUTLINE | EVIDENCE | CHECK | HOLD
next_cycle: WRITE | PREPARE | SHAPE | SURVEY | LAND | CHECK  # omit on HOLD
reason: <authority exercised and why the route follows>
reopens_promise: false  # current receipt grammar; describe promise changes in reason and route to OUTLINE
```

## 🚧 Boundaries

- Do not change the approved plan or Evidence Item contract in place.
- Do not execute an Evidence Item Run or treat prose as an Evidence Result.
- Do not write a CHECK verdict, `accepted:`, `approved:`, or `Decide`.
- Do not count Draft/Revise/Build/Pre-check movements as separate Level-4 Runs.
- Do not leave a promoted Page paragraph without the writing Run or explicit
  no-Run rationale that produced it.

## 📂 Files

```text
haipipe-page-content/
├── SKILL.md
├── CHANGELOG.md
├── ref/paragraph-run.md
└── cli/promote_paragraph.py
```

Every current writing dispatch records `phase: CONTENT · cycle: WRITE`.
For an existing receipt using retired phase names, consult
`../haipipe-page-workflow/ref/page-run-contract.md#legacy-compatibility-only`;
those tokens are read-only historical input.
