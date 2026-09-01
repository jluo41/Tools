---
name: haipipe-page-check
description: >-
  The CHECK phase contract for any Board Page: judge one rendered version
  against its purpose, Aims, evidence, and Page Type, then route to CLOSE,
  OUTLINE, EVIDENCE, DRAFT, REVISE, or HOLD. In pre-check mode it gates the
  WRITE cycle's inner loop and may only say another pass or ready. It judges the BUILT
  deliverable, not only the Markdown, and never cures its own findings.
  Trigger: page check, CHECK phase, quality gate, review version, check the
  pdf, /haipipe-page-check.
metadata:
  version: "0.6.3"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-check · judge one version and name its next authority

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-check
  → haipipe-sentence, when findings use sentence lanes
  → family checker, when the Page belongs to paper or application
```

What is CHECK's alone: it is the only phase that may CLOSE, and the only one forbidden to change what it judges.
Its risk is becoming a hidden revision: curing its own finding and calling the same version checked, which is why the fix always runs under another phase and returns for a fresh look.
The Page Type or local contract supplies the closing rule and whether a person must rule.

## ⚡ Brief

```text
Q          judge ONE concrete rendered version cold and name its next
           authority by phase name; the only phase that may CLOSE
WRITES     findings · comments · the check record · a proposed or human
           ruling; NEVER the artifact it judges

WALLS
  read-only on the judged version: never edits, never rebuilds, never cures
    a finding in the same pass; the fix runs under another phase and the
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
  read fully ONLY the target page, the plan, and this brief
  trust the plan's Answered:/Drawn: values as written; re-read only cards
    whose line ends `· recount`, plus one spot-check (haipipe-page-draft §📖)
  batch shell calls; scope cli/check.py output to your page with grep
  never paste board-wide output or compile logs into your context; the
    board doors return compact JSON, use them

ROUTES (§🔀 · the six, each finding names one)
  ✅ CLOSE      the version meets the closing rule
  🧭 OUTLINE    the plan itself is wrong (SHAPE) or a number, citation or
                figure has no landed run (SURVEY): a v<N+1> reopens the
                OUTLINE part
  🔎 EVIDENCE   a landed row is stale or its run must be re-embedded
  ✍️ DRAFT      purpose or Aims must reopen, beginning a new round
  🧵 REVISE     purpose and Aims stand, but realization needs work
  ⏸ HOLD        accept a named defect or park the work with an explicit record

RECEIPT  the common phase receipt plus this file's rows (checked_version ·
         verdict · findings · route · human_gate), shape in §🧾 below;
         field law: ../haipipe-page-workflow/ref/page-run-contract.md
         §Receipt step, field by field
```

Open the full contract below only where this brief does not settle your case; the full text wins every conflict.

## 🪪 The official-document lane

`## Content` states rules, never attributions. The mechanical checker flags
each offending line as `content-attribution` (WARN): a bare date code
("260819") or a person named as authority in Content or Diagram prose. On a
page under active work this lane routes REVISE; on a legacy page it is
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

Mechanical checks may run during every phase.
The CHECK phase begins when their results and semantic judgment are used to route or close a version.

If the same person or agent also fixes a finding, the work changes phase explicitly.
The changed version must be checked again.

## 🧩 Put each finding where it applies

```text
① MECHANICAL   run deterministic checks and preserve their exact result
② SEMANTIC     judge function, evidence, readability, and local requirements
③ SEED         place each actionable finding at its Page, section, sentence, or artifact
④ DECIDE       route the version using the finding's required authority
```

A chat report is a map, not the review surface.
When the Page Type supports comment lanes, put one concrete finding at the exact location it concerns and preserve the reply with it.
When the deliverable must remain clean, use the Page Type's declared ledger or review surface instead.

## 📦 Judge the BUILT artifact, not only the Markdown

A Page that ships a PDF or a docx is judged on what a person opens. Reading the `.md` and calling it checked is how five declared display units reached LaTeX as two without anyone being told (JL 260816).

`haipipe-board/src/page_evidence.py` computes these deterministically at step ① and `cli/check.py` reports them.
**Rendered and unrendered are different defects with different fixes**: a unit can print correctly and still trace to nothing, and telling its author to re-run a renderer that already worked is how a checker loses its reader.


```text
finding                          fires when                              route
──────────────────────────────────────────────────────────────────────────────────
display-declared-no-claim        a unit folder with no `claim:` row in    DRAFT
                                 its README: litter, not a proposal
display-declared-not-rendered    a unit folder exists with no winning     REVISE
                                 asset and no preview.pdf; the finding
                                 NAMES the first missing step
                                 (① intake · ② recipe · ② asset · ④ preview)
display-intake-unfrozen          the unit RENDERED but intake/inputs/     EVIDENCE
                                 holds no frozen snapshot, so a printed
                                 number traces back to nothing
display-cited-not-embedded       the prose cites the unit but latex/      REVISE
                                 <stem>.tex never inputs it
display-rendered-not-cited       the unit rendered and no sentence names   REVISE
                                 it, so neither projection places it
display-accept-stale             intake/ changed after `accepted: ✅`,    EVIDENCE
                                 so the tick binds a render that is gone
latex-untitled                   latex/<stem>.tex carries no title block  REVISE
                                 built from the Page's own H1
projection-stale                 latex/ or word/ is older than the        REVISE
                                 Page source it projects
```

**Folder count is never completed work.** The three counts are independent and CHECK reads all three: **declared** means the unit folder exists, **rendered** means a winning asset and `preview.pdf` both exist, **accepted** means a person ticked the README. A version whose declared count exceeds its rendered count does not pass.

**Step ⑤ ACCEPT is the human gate CHECK administers.** A machine may render, cite, build, and report; only a person writes `accepted: ✅` in a unit's README, and a changed `intake/` drops that tick back to ⬜. CHECK never ticks it and never reports a unit as accepted because it looks finished.

## 🔀 Route by the authority needed next

```text
✅ CLOSE       the version meets the closing rule
🧭 OUTLINE    the plan itself is wrong (SHAPE), or a number, citation or
              figure has no landed run (SURVEY): a v<N+1> reopens the OUTLINE part
🔎 EVIDENCE   a landed row is stale, or its run must be re-embedded
✍️ DRAFT      purpose or Aims must reopen, beginning a new round
🧵 REVISE     purpose and Aims stand, but realization needs work
⏸ HOLD        accept a named defect or park the work with an explicit record
```

A CHECK finding should name one of these routes.
“Fail” without an owner leaves the next worker guessing.

Returning to DRAFT does not create another Page or necessarily another unit.
It starts a new round on the same persistent Page because the promise reopened.

## 🚪 Human gates belong to the Page Type or local contract

CHECK does not assume every Page has the same gate.
A Q decision Page may close when its Aims are met, a Stage Page may require an explicit human ruling, and a Skill mirror may close when its unit ships.

Never invent a gate and never skip a declared one.
A machine may gather evidence, plant comments, and propose a ruling.
It may close an answered decision row according to the base contract, but it may never claim that a person approved a Page when no person did.

The gate exchange is durable input to whichever phase restarts.
The restarted phase reads each finding together with its reply rather than receiving a summary stripped of the decision context.

## ✋ The gate is ACCEPT-BIASED, and that changes only what is SHOWN

JL 260818, in his own words: "human should be more likely to accept it." A gate's
real cost is not the tick, it is the SEARCH a person performs before deciding
whether to write it. Moving that search onto the machine is the only lever that
makes yes the likely answer without touching the tick itself.

```text
✅ WHAT THE BIAS CHANGES · the presentation
   present a gate only when `mechanical_errors` for that page is ZERO, so
   nobody is asked to accept a display that never rendered or a PDF with
   no title block
   the gate is a CONFIRMATION, not an inspection

⛔ WHAT IT MAY NEVER CHANGE · the writer
   silence is not consent
   a required gate with no durable passed evidence still routes to HOLD
   otherwise the machine approves itself by timeout
```

**Person ticks are selected by artifacts plus the Folder's owning phase.**
CHECK administers display acceptance and any owner RULING that exists:

```text
tick             lives on                          reserved by            phase
──────────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<N>.md    haipipe-page-outline     SHAPE
`Decide`         outline/<stem>-items.md, per row  haipipe-page-outline     SURVEY
`verified`       each evidence/bibex entry         haipipe-plugin-bibex     LAND
`read:`          each outbound evidence/probe card haipipe-plugin-probe     LAND
`accepted: ✅`   the page · each display README    this contract            CHECK
the RULING       phase Gate/Closure, when declared  owning workflow phase    CHECK
```

`read:` and `accepted: ✅` REVERT when their inputs change. For a phase-owned
Folder, `page_ruling: none` adds no owner tick, `domain-gate` reuses the phase
gate receipt, and `local` requires a distinct Page-Face RULING. Legacy Page
Types retain their declared closing gate.

A sixth human-reserved write exists and is deliberately NOT on this list, because
it is an ORDER rather than a field: the row rank in `skill/` and
`evidence/pagex/`, whose
law is "the scan seeds, the person ranks" and where "a refresh never edits,
reorders, or removes a row".

They live in three phases and N files. A read-only collecting surface exists at
`haipipe-board/live/outline.py`, which shows `approved:`, `verified`, `read` and
`accepted:` in one card and omits the RULING; it reports no `<n> of <n>` count
and cannot write. The joined owed ledger is `cli/pagephase.py --owed`.

## 🔀 CHECK is not necessarily last

CHECK may appear whenever a concrete version needs judgment.
It may repeat after REVISE, open EVIDENCE, or send the Page into a new DRAFT round.
The common `OUTLINE part → WRITE → CHECK` path is a useful route, not a mandatory sequence.

**Two things this phase gained on 260901.** (1) PRE-CHECK MODE: inside the
WRITE cycle the same judge, in a fresh context, reads the built version after
the mechanical teeth pass and answers only "another pass" or "ready"; it never
CLOSEs, and the loop's budget (3 rounds, a finding surviving two consecutive
rounds is a HOLD) is `haipipe-page-workflow` §The WRITE loop's. (2) A PERSON'S
"NO" IS ROUTED, never a dead end: it lands as one feedback record in
`outline/`, `accepted:` stays unticked, and it routes like a finding (wording →
WRITE · a number, citation or figure → OUTLINE at SURVEY · the argument →
OUTLINE at SHAPE). A checkable "no" is promoted into a tooth or a pre-check rule
(`agents/approve-rules/`), so the machine catches it every time after. The
machine's "ready" was always a floor, not a verdict.

## 🧾 RUN receipt and version gate

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. CHECK's receipt must additionally state:

```text
checked_version    source SHA-256 joined to rendered HTML SHA-256
verdict            pass | revise | blocked
findings           exact defects or none
evidence           visible support for every pass claim
route              CLOSE | OUTLINE | EVIDENCE | DRAFT | REVISE | HOLD
human_gate         required, status, and durable evidence
```

`checked_version` must equal both version fields and CHECK must not edit either
artifact. A mismatch means concurrent or hidden mutation and routes to HOLD.
The actor that produced a version may not be its CHECK actor. A changed version
after REVISE or DRAFT receives another CHECK; an earlier pass never transfers.
Only `verdict: pass` may route to CLOSE, and a required human gate without
durable passed evidence routes to HOLD.

## 📏 The rubric · four axes, four verdicts, one row per unit

Requirements resolve in the order `haipipe-page` §🔍 states (base and
template → Page Type → Phase → the page's `### Writing Style` and Stage
Contract → the division purpose and each paragraph's job line); a conflict
between two sources is reported and that criterion is not judged.

```text
axis          question                                                            judge
─────────────────────────────────────────────────────────────────────────────────────────────
Mechanics     is the required structure present, ordered, addressable, consistent?  check.py
Function      does this section answer the reader question the contract assigns?    semantic reviewer
Evidence      can every factual compliance claim point to visible text, an Aim's
              Now:, or a linked artifact?                                            semantic reviewer
Readability   can a zero-background reader understand the section without
              supplying a missing premise?                                           fresh-context reviewer
```

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
page-workflows/haipipe-page-check/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-page`; Page Type variants live under `page-types/`; the sentence-level lane contract is `haipipe-sentence`; family checkers own their deterministic tools and artifact-specific gates.
The Board engine owns execution and audit; this phase owns only its authority and receipt.

**The Board page that argues this phase** is `QPw6-check` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open, currently whether WARNINGS may block CLOSE.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §CHECK. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.
