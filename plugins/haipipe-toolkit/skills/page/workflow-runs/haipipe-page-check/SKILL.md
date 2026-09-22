---
name: haipipe-page-check
description: >-
  The check gate of a Board Page (`Page.check`, the last row of the Run table): judge one rendered version
  against its purpose, Aims, evidence, and Page Face owner, then route to CLOSE,
  CONTEXT, OUTLINE, EVIDENCE, CONTENT, or HOLD. In pre-check mode it gates the
  WRITE cycle's inner loop and may only say another pass or ready. It judges the BUILT
  deliverable, not only the Markdown, and never cures its own findings.
  Trigger: page check, check gate, quality gate, review version, check the
  pdf, /haipipe-page-check.
metadata:
  version: "0.12.0"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-check · judge one version and name its next authority

Load the contracts in this order:

```text
haipipe-page
  → haipipe-page-workflow
  → haipipe-page-check
  → Folder-owning workflow or canonical family skill
  → exact Page Face owner
  → haipipe-sentence, when findings use sentence lanes
  → the current Folder owner checker (Paper, Insight, Design, or another resolved owner)
```

What is CHECK's alone: it is the Page Workflow Runtime's independent whole-Page
completion gate, and the only authority forbidden to change what it judges.
The `CHECK` label is a compatibility dispatch; its risk is becoming a hidden
revision, so any fix runs under another Run Spec and returns for a fresh look.
The Page Face owner supplies the closing rule and whether a person must rule.

At adoption, build, or release, apply `../../haipipe-page/ref/release-decisions.md`
for profile precedence and reuse of existing human decisions.

## 🧭 Run Workflow placement

CHECK evaluates the exit gate of the Page Run Workflow against one immutable
source/render version. It is not a Page Run and does not create a Run for a
finding, review turn, or route decision. The Runtime records the verdict and
selected legal route; a finding is repaired by the owning Run Spec and the
changed version returns to this gate.

## ⚡ Brief

```text
Q          judge ONE concrete rendered version cold and name its next
           authority by Run Spec/route; the only completion gate that may CLOSE
WRITES     findings · comments · the check record · a proposed or human
           ruling; NEVER the artifact it judges

WALLS
  read-only on the judged version: never edits, never rebuilds, never cures
    a finding in the same pass; the fix runs under another Run and the
    changed version returns for a fresh CHECK
  judges the BUILT deliverable (PDF · docx), not only the Markdown;
    declared, rendered, and accepted are three independent counts
  the actor that produced a version may not be its CHECK actor
  never writes any person-reserved tick, and never claims a person
    approved when no person did; silence is not consent
  only `verdict: pass` may route to CLOSE; a required human gate without
    durable passed evidence routes to HOLD
  checked_version must equal both version fields; a mismatch routes to HOLD
  never invents a gate and never skips a declared one

READ ECONOMY
  read fully ONLY the target page, frozen Context, the plan, applicable Requirement and
    Writing records, and this brief
  trust the plan's Answered:/Drawn: values as written; re-read only cards
    whose line ends `· recount`, plus one spot-check (haipipe-page-writing)
  batch shell calls; scope cli/check.py output to your page with grep
  never paste board-wide output or compile logs into your context; the
    board doors return compact JSON, use them

ROUTES (§🔀 · the six, each finding names one)
  ✅ CLOSE      the version meets the closing rule
  🧭 CONTEXT    policy, requirement, ownership, or related context is stale
  🧭 OUTLINE    the plan itself is wrong (SHAPE), or an Evidence Item has no
                complete Run graph (SURVEY): the next `v<G>.<S>[.<E>]` reopens planning
  🔎 EVIDENCE   a complete graph lacks a valid local Result (LAND), or a
                landed Result is stale or must be re-embedded
  ✍️ CONTENT    Page realization, purpose/Aims, or delivery needs work
  ⏸ HOLD        accept a named defect or park the work with an explicit record

RECEIPT  the common Run receipt plus this file's rows (checked_version ·
         verdict · findings · route · human_gate), shape in §🧾 below;
         field law: ../haipipe-page-workflow/ref/page-run-contract.md
         §Receipt step, field by field
```

Open the full contract below only where this brief does not settle your case; the full text wins every conflict.

## 🪪 The official-document lane

`## Content` states rules, never attributions. The mechanical checker flags
each offending line as `content-attribution` (WARN): a bare date code
("260819") or a person named as authority in Content or Diagram prose. On a
page under active work this lane routes CONTENT; on a legacy page it is
reported, not cured. Fenced blocks are exempt in the checker because a fence
may carry a frozen transcription another pen owns; this judge reads those by
eye and lists what it finds for the owning pen.

## 👁 The authority test

CHECK observes and decides what one visible version needs next.

```text
reads      rendered Page · purpose · Aims · evidence · inherited constraints
writes     findings · comments · check record · proposed or human ruling
does not   repair a substantive finding inside the same CHECK pass
```

Mechanical checks may run during any Run Spec.
The CHECK compatibility dispatch begins when their results and semantic
judgment are used to route or close a version.

If the same person or agent also fixes a finding, the work moves to the owning
Run Spec explicitly.
The changed version must be checked again.

## 🧩 Put each finding where it applies

```text
① MECHANICAL   run deterministic checks and preserve their exact result
② SEMANTIC     judge function, evidence, readability, and local requirements
③ SEED         place each actionable finding at its Page, section, sentence, or artifact
④ DECIDE       route the version using the finding's required authority
```

A chat report is a map, not the review surface.
When the Page Face owner supports comment lanes, put one concrete finding at the exact location it concerns and preserve the reply with it.
When the deliverable must remain clean, use the Page Face owner's declared ledger or review surface instead.

## 📦 Judge the BUILT artifact, not only the Markdown

A Page that ships a PDF or a docx is judged on what a person opens. Reading the `.md` and calling it checked is how five declared display units reached LaTeX as two without anyone being told (JL 260816).

`haipipe-board/src/page_evidence.py` reads the current typed DISPLAY Result and its `payload.unit`, computes these deterministically at step ①, and `cli/check.py` reports them. It reads the retired folder lane only for Pages with no current DISPLAY Result.
**Rendered and unrendered are different defects with different fixes**: a unit can print correctly and still trace to nothing, and telling its author to re-run a renderer that already worked is how a checker loses its reader.


```text
finding                          fires when                              route
──────────────────────────────────────────────────────────────────────────────────
display-result-unit-unresolved   a current DISPLAY Result has an invalid  EVIDENCE
                                 pointer or is ready without payload.unit
display-label-unbound            prose uses a D_ label absent from the       EVIDENCE
                                 selected current DISPLAY Result labels
display-declared-no-claim        a Result payload unit has no `claim:`    CONTENT
                                 row in its README: litter, not a proposal
display-declared-not-rendered    a Result payload unit exists with no     CONTENT
                                 asset and no preview.pdf; the finding
                                 NAMES the first missing step
                                 (① intake · ② recipe · ② asset · ④ preview)
display-intake-unfrozen          the unit RENDERED but intake/inputs/     EVIDENCE
                                 holds no frozen snapshot, so a printed
                                 number traces back to nothing
display-cited-not-embedded       the prose cites its bound D_ label or  CONTENT
                                 manuscript \ref, but Delivery omits it
display-rendered-not-cited       the unit rendered and no sentence cites  CONTENT
                                 a Result label or manuscript \ref
display-accept-stale             intake/ changed after `accepted: ✅`,    EVIDENCE
                                 so the tick binds a render that is gone
latex-untitled                   delivery/latex/<stem>.tex carries no     CONTENT
                                 title block built from the Page's H1
projection-stale                 delivery/latex/ or delivery/word/ is     CONTENT
                                 older than the Page source it projects
```

display-label-unbound is a warning while the Page is being drafted. Board
Delivery requires every cited D_ token to bind to a selected current Result.

**Folder count is never completed work.** The three counts are independent and CHECK reads all three: **declared** means the unit folder exists, **rendered** means a winning asset and `preview.pdf` both exist, **accepted** means a person ticked the README. A version whose declared count exceeds its rendered count does not pass.

**Step ⑤ ACCEPT is the human gate CHECK administers.** A machine may render, cite, build, and report; only a person writes `accepted: ✅` in a unit's README, and a changed `intake/` drops that tick back to ⬜. CHECK never ticks it and never reports a unit as accepted because it looks finished.

## 🔀 Route by the authority needed next

```text
✅ CLOSE       the version meets the closing rule
🧭 CONTEXT     policy, requirement, ownership, or related context is stale
🧭 OUTLINE    the plan itself is wrong (SHAPE), or an Evidence Item has no
              complete Run graph (SURVEY): the next `v<G>.<S>[.<E>]` reopens OUTLINE
🔎 EVIDENCE   a complete graph lacks a valid local Result (LAND), or a landed
              Result is stale or must be re-embedded
✍️ CONTENT    purpose, Aims, prose, or delivery realization needs work
⏸ HOLD        accept a named defect or park the work with an explicit record
```

A CHECK finding should name one of these routes.
“Fail” without an owner leaves the next worker guessing.

Returning to CONTENT does not create another Page. It starts another WRITE
pass on the same persistent Page; if the promise or structure changed, CONTENT
routes through OUTLINE before writing.

## 🚪 Human gates belong to the Page Face owner

CHECK does not assume every Page has the same gate.
A Q decision Page may close when its Aims are met, a Stage Page may require an explicit human ruling, and a Skill mirror may close when its unit ships.

Never invent a gate and never skip a declared one.
A machine may gather evidence, plant comments, and propose a ruling.
It may close an answered decision row according to the base contract, but it may never claim that a person approved a Page when no person did.

The gate exchange is durable input to whichever Run restarts.
The restarted Run reads each finding together with its reply rather than receiving a summary stripped of the decision context.

## ✋ The gate is EVIDENCE-LED, and that changes only what is SHOWN

The packet gathers the evidence a person needs to decide, including failed
checks, unresolved disagreements, and limitations. It reduces the search needed
for review without steering acceptance. Accept, request changes, reject, and
pause remain valid recorded decisions.

```text
✅ WHAT THE PACKET PROVIDES · the presentation
   present a gate only when `mechanical_errors` for that page is ZERO, so
   nobody is asked to accept a display that never rendered or a PDF with
   no title block
   the gate presents evidence for an informed review and decision

⛔ WHAT IT MAY NEVER CHANGE · the writer
   silence is not consent
   a required gate with no durable passed evidence still routes to HOLD
   otherwise the machine approves itself by timeout
```

**Person ticks are selected by artifacts plus the Folder's owning Run Spec/Workflow.**
CHECK administers display acceptance and any owner RULING that exists:

```text
tick             lives on                          reserved by            Run
──────────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<G>.<S>[.<E>].md  haipipe-page-structure  SHAPE; evidence may inherit
`Decide`         outline/<stem>-evidence-items.md, per item  haipipe-page-structure  SURVEY
`Verified`       each authored CITE Evidence Item  haipipe-page-evidence     LAND
`read:`          legacy outbound source material   owning Run    LAND
`accepted: ✅`   the page · each display README    this contract            CHECK
the RULING       Run Gate/Closure, when declared  owning Run    CHECK
```

New Pages use typed Evidence Items. Each ordinary-Page CITE gate lives as
`Verified: ✅ <who> <timestamp>` on its authored Evidence Item row and is
administered by EVIDENCE/LAND; the CITE Result is not ready without it. They do
not create a new `evidence/probe/` lane. Discovery Result verification remains
in the owning Discovery runtime receipt. A legacy BibTeX `verified` field or
`read:` receipt may still be displayed while migrated material is retired.

`read:` and `accepted: ✅` REVERT when their inputs change. For a Run-owned
Folder, `page_ruling: none` adds no owner tick, `domain-gate` reuses the Run
gate receipt, and `local` requires a distinct Page-Face RULING. Legacy Page
Types retain their declared closing gate.

A further human-reserved write is an ORDER rather than a field: the row rank
in `outline/skill/`, whose law is "the scan seeds, the person ranks" and where
a refresh never edits, reorders, or removes a row.

Collect required gates across the selected version's plan, Evidence Results,
Run acceptance, delivery receipts, and owner policy. The response must show
`settled / required`, the owner, evidence, recorded decision, and next action
for every required gate, including any owner RULING. `cli/pageprogress.py --owed`
is a collecting input; a partial UI card is not the full acceptance packet.
Apply `../../haipipe-page/ref/release-decisions.md` to reuse prior applicable
acceptance. Mechanical checks never supply a person's decision.

## 🔀 CHECK is not necessarily last

CHECK may appear whenever a concrete version needs judgment. It may repeat
after CONTENT, open EVIDENCE, or return the Page to CONTEXT or OUTLINE. The
common `CONTEXT → OUTLINE ⇄ EVIDENCE → CONTENT → CHECK` route is useful, not a
mandatory fixed sequence.

**Two things this Run gained on 260901.** (1) PRE-CHECK MODE: inside the
WRITE cycle the same judge, in a fresh context, reads the built version after
the mechanical teeth pass and answers only "another pass" or "ready"; it never
CLOSEs, and the loop's budget (3 rounds, a finding surviving two consecutive
rounds is a HOLD) is `haipipe-page-workflow` §The WRITE loop's. (2) A PERSON'S
"NO" IS ROUTED, never a dead end: it lands as one feedback record in
`outline/`, `accepted:` stays unticked, and it routes like a finding (wording →
CONTENT/WRITE · an absent Run graph → OUTLINE/SURVEY · an incomplete or stale
Result → EVIDENCE/LAND · the argument → OUTLINE/SHAPE). A checkable "no" is
promoted into a tooth or a pre-check rule
(`agents/approve-rules/`), so the machine catches it every time after. The
machine's "ready" was always a floor, not a verdict.

## 🧾 RUN receipt and version gate

When called by RUN, read `../../haipipe-page-workflow/ref/page-run-contract.md` and
return its common Run receipt. CHECK's receipt must additionally state:

```text
checked_version    source SHA-256 joined to rendered HTML SHA-256
verdict            pass | revise | blocked
findings           exact defects or none
evidence           visible support for every pass claim
route              CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
next_cycle         PREPARE | SHAPE | SURVEY | LAND | EMBED | WRITE
                   (required only for a nonterminal Page-Run route; omit on
                   CLOSE or HOLD)
human_gate         required, status, and durable evidence
```

`checked_version` must equal both version fields and CHECK must not edit either
artifact. A mismatch means concurrent or hidden mutation and routes to HOLD.
The actor that produced a version may not be its CHECK actor. A changed version
after CONTENT receives another CHECK; an earlier pass never transfers.
Only `verdict: pass` may route to CLOSE, and a required human gate without
durable passed evidence routes to HOLD.

## 📏 The rubric · four axes, four verdicts, one row per unit

Requirements resolve in the order `haipipe-page` §🔍 states (base and
template → Page Face owner → current Run Spec owner → the page's authored W records in
`outline/<stem>-requirement.md` and Stage Contract → the division purpose
and each paragraph's job line); a conflict between two sources is reported
and that criterion is not judged. A non-Section compatibility page may still
carry `## Writing Style` in its source.

Use the shared **Mechanics, Function, Evidence, Readability** criteria and four
verdicts from
`../../../writing/haipipe-writing/ref/evaluation-rubric.md`.
That is the base prose rubric used by both Writing self-review and this
independent CHECK. Its version/hash and the actual checked artifact/version
belong in the receipt. Add Page-specific mechanics from check.py, required
source/render consistency, Aims and visible artifact evidence under this
contract. Judge Readability for the intended reader using a fresh context.

Writing's self-review is input evidence, never this CHECK's verdict. Preserve
the different-actor and immutable-version requirements above; review all
required Page units even if a previous Writing Step checked only a local seam.

For a Paper Section Page at G4, also load
`../../../paper/haipipe-paper/ref/submission-readiness.md` and apply only the
section-scoped `SUB-INTRO-*`, `SUB-METHOD-*`, `SUB-RESULT-*`, or `SUB-DISC-*`
rows that belong to that Page. These rows use the shared four axes and verdicts;
they do not create a second Page checklist, score, manifest field, or lifecycle
Run. `SUB-COVER-*` and `SUB-WHOLE-*` remain Paper-level checks after assembly.
Keep the Results/Discussion seam explicit: report and quantify observations in
Results, then interpret, compare, and bound them in Discussion. A retelling
criterion without independent human evidence is `NOT VERIFIABLE`, never a pass.

The review units are every present `##` section, every direct `###` Content
division, and every `####` paragraph whose job must be tested. Four verdicts
only: `MEETS`, `NEEDS WORK`, `N/A` (the rule genuinely does not apply),
`NOT VERIFIABLE` (the evidence is unavailable; never a pass). When the same
section changed on several pages, the batch is one more readability unit: read
those sections consecutively in board order, and the batch NEEDS WORK when the
prose is interchangeable after noun substitution or a repeated scaffold makes
distinct pages sound like one form letter; the smallest fix restates each
page's own stake in its own order, never cosmetic synonyms.

```text
unit | applicable requirements + source | verdict | evidence | smallest fix
```

Then the requirement conflicts, the mechanical findings, and one page-level
verdict. The review is read-only: it never edits prose, ticks an Aim, closes a
Decision Now row, or closes a page.

## 📂 Files

```text
workflow-runs/haipipe-page-check/
├── SKILL.md            this CHECK judgment contract
└── CHANGELOG.md        version history
```

This is the CHECK judgment contract dispatched by `haipipe-page-workflow`; it
does not define a separate Run or Workflow. The owning Page Workflow's Run
Specs and Runtime determine whether a CHECK is a step inside an existing Run or
a standalone Page control receipt.

Owns no scripts.
The base is `haipipe-page`; a Page Face owner may be a Run Spec owner,
canonical family skill, or legacy variant under `page-types/`; the
sentence-level lane contract is `haipipe-sentence`; family checkers own their
deterministic tools and artifact-specific gates.
The Board engine owns execution and audit; this gate owns only its judgment and receipt.

**The Board page that argues this Run** is `QPw6-check` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open, currently whether WARNINGS may block CLOSE.

**This CHECK contract in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../../haipipe-page-workflow/ref/Run-cards.md` §CHECK. That file states every Run in the SAME fields, so one Run can be read next to another; this contract states the reasoning behind them.
