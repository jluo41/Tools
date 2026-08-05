---
name: haipipe-board-page-revise
description: >-
  The REVISE phase contract for any Board Page. REVISE improves the realization of the current round while the Page's purpose and Aims stay fixed; it may add, delete, move, or rewrite, so edit shape never distinguishes it from DRAFT. Load haipipe-board-page first, then the matching Page Type, then this contract, and finally the stage's declared family craft files. Use when incorporating landed evidence or feedback, improving structure or prose under fixed Aims, deciding whether a change instead requires a new DRAFT round, or preserving an unanswered hole rather than inventing its answer. Trigger: page revise, REVISE phase, fixed Aims, rewrite, add paragraph, delete section, move argument, land answer, candidate diff, /haipipe-board-page-revise.
metadata:
  version: "0.3.2"
  last_updated: "2026-08-05"
  summary: "REVISE improves a fixed Page promise and emits an auditable receipt before the changed version is checked again."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-revise · make the current promise work

Load the contracts in this order:

```text
haipipe-board-page
  → matching page-types/ variant, when one exists
  → haipipe-board-page-revise
  → family craft: the stage's declared craft files, when the Page belongs to paper or application
```

What is REVISE's alone: the Page may change a great deal here while its promise may not move at all.
Its risk is the quiet swap: a revision that redefines what the Page is for while calling itself an improvement, which is why the fixed purpose and Aims are the phase's one test.
The moment the promise stops fitting, the work is a new DRAFT round and says so.

## 🔒 The authority test

REVISE changes the Page while holding its purpose and Aims fixed.

```text
same promise after the change       → REVISE
purpose or Aim must change          → DRAFT, new round
an unanswered fact blocks the edit  → PROBE, then route again
```

The size, age, and operation of the edit do not decide the phase.
Adding a paragraph, deleting a section, moving an argument, and rewriting the Opening may all be REVISE when the current promise still describes the result.

REVISE may occur directly after DRAFT, after PROBE, after CHECK feedback, or repeatedly.
It is not defined as the third step of a rigid sequence.

## ✍️ What REVISE may write

Subject to the base and matching Page Type:

```text
🧭 Opening      revise when the same purpose needs clearer expression
🖼 Diagram      revise when the same subject needs a better whole-page view
📚 Content      add · delete · move · rewrite under fixed Aims
🎯 Aims         do not change their intent inside REVISE
📍 States       update from visible evidence produced by the work
📎 Files        update continuations made stale by the revision
🗃 Log          record the pass, evidence used, and remaining gaps
```

An administrative correction to an Aim record may preserve its meaning.
Changing what the Aim promises is DRAFT even when the textual diff is small.

## 🧵 Land evidence before polishing affected prose

When PROBE returned an answer, revise in this order:

```text
① LAND       read A-consumer and its A-executor source, then discharge the owned hole
② ARGUE      test accuracy, warrant, sequence, and claim strength
③ SOUND      improve voice and readability after the final facts are present
```

The order is conditional, not a claim that every REVISE follows PROBE.
If no answer landed, begin with the first applicable step.

An unanswered hole remains visible and keeps its id.
Never estimate, infer from nearby prose, quietly drop the sentence, or remove the marker merely to make the Page look finished.

## 🪞 Direct and candidate modes

```text
DIRECT      default · change the Page and record why a non-trivial change was made
CANDIDATE   explicit author request only · leave the Page unchanged and place a
            reviewable proposal in the Page Type's sentence or comment surface
```

Candidate mode is review material, not a completed revision.
The Page returns to direct REVISE after the author chooses.

The family craft files own prose, markup, or artifact-specific quality rules.
This contract owns only the phase boundary and routing.

## 🔀 Exit and routing

```text
fixed promise now works and is ready to judge → CHECK
another consequential unknown appears         → PROBE
purpose or Aims must change                    → DRAFT, new round
more work under the same promise               → REVISE again
```

REVISE never closes a human gate on its own.

## 🧾 RUN receipt

When called by RUN, read `../../haipipe-board-page/ref/page-run-contract.md` and
return its common phase receipt. REVISE's receipt must additionally state:

```text
reason             which fixed Aim the revision now serves
artifacts          every target or continuation changed in this pass
evidence           landed answer, feedback, or close-reading evidence used
route              REVISE | PROBE | DRAFT | CHECK | HOLD
reopens_promise    true only when revision discovered that purpose/Aims changed
```

A successful content change produces a new source/render version. REVISE may
suggest CHECK, but it never labels that version approved and never routes to
CLOSE. If it routes to DRAFT, the controller increments the round exactly once.

## 📂 Files

```text
page-phases/haipipe-board-page-revise/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-board-page`; Page Type variants live under `page-types/`; prose and artifact craft files remain in their owning families.
The Board engine owns execution and audit; this phase owns only its authority and receipt.
