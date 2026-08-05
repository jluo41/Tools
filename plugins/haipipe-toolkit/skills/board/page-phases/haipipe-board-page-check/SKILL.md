---
name: haipipe-board-page-check
description: >-
  The CHECK phase contract for any Board Page. CHECK judges one concrete rendered version against its purpose, Aims, evidence, Page Type, and local closing rule, records findings where they apply, and routes the work to close, REVISE, PROBE, or a new DRAFT round; it does not cure its own substantive findings. Load haipipe-board-page, the matching Page Type, this contract, and haipipe-board-sentence when findings use sentence lanes, then any family checker. Use when reviewing a Page version, running a declared gate, planting findings in context, choosing the next phase, or preventing a checker from silently revising what it judged. Trigger: page check, CHECK phase, quality gate, review version, close round, route finding, restart phase, human decision, /haipipe-board-page-check.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-04"
  summary: "CHECK independently judges one immutable Page version and emits the terminal or corrective route used by RUN."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-check · judge one version and name its next authority

Load the contracts in this order:

```text
haipipe-board-page
  → matching page-types/ variant, when one exists
  → haipipe-board-page-check
  → haipipe-board-sentence, when findings use sentence lanes
  → family checker, when the Page belongs to paper or application
```

The Page Type or local contract owns the closing rule and whether a person must rule.
This file owns only CHECK authority.

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

## 🔀 Route by the authority needed next

```text
✅ CLOSE       the version meets the closing rule
🧵 REVISE     purpose and Aims stand, but realization needs work
🔎 PROBE      a consequential answer is missing
✍️ DRAFT      purpose or Aims must reopen, beginning a new round
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

## 🔀 CHECK is not necessarily last

CHECK may appear whenever a concrete version needs judgment.
It may repeat after REVISE, open PROBE, or send the Page into a new DRAFT round.
The common `DRAFT → PROBE → REVISE → CHECK` path is a useful route, not a mandatory sequence.

## 🧾 RUN receipt and version gate

When called by RUN, read `../../haipipe-board-page/ref/page-run-contract.md` and
return its common phase receipt. CHECK's receipt must additionally state:

```text
checked_version    source SHA-256 joined to rendered HTML SHA-256
verdict            pass | revise | blocked
findings           exact defects or none
evidence           visible support for every pass claim
route              CLOSE | REVISE | PROBE | DRAFT | HOLD
human_gate         required, status, and durable evidence
```

`checked_version` must equal both version fields and CHECK must not edit either
artifact. A mismatch means concurrent or hidden mutation and routes to HOLD.
The actor that produced a version may not be its CHECK actor. A changed version
after REVISE or DRAFT receives another CHECK; an earlier pass never transfers.
Only `verdict: pass` may route to CLOSE, and a required human gate without
durable passed evidence routes to HOLD.

## 📂 Files

```text
page-phases/haipipe-board-page-check/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-board-page`; Page Type variants live under `page-types/`; the sentence-level lane contract is `haipipe-board-sentence`; family checkers own their deterministic tools and artifact-specific gates.
The Board engine owns execution and audit; this phase owns only its authority and receipt.
