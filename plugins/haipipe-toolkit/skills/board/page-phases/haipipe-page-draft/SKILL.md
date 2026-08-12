---
name: haipipe-page-draft
description: >-
  The DRAFT phase contract for any Board Page. DRAFT is the authority to define or reopen the Page's purpose, Aims, and promised shape for one round; it is not identified by an empty file, first typing, or adding text. Load haipipe-page first, then the matching Page Type under page-types/, then this contract, and finally the stage's declared family craft files. Use when creating a Page promise, changing what an existing Page is for, adding or removing an Aim, starting a new round after REVISE or CHECK, or raising a stake-bearing Q-consumer without performing PROBE. Trigger: page draft, DRAFT phase, define purpose, reopen Aims, new round, raise Q-consumer, owned hole, draft boundary, /haipipe-page-draft.
metadata:
  version: "0.3.2"
  last_updated: "2026-08-05"
  summary: "DRAFT owns the Page promise and emits an auditable receipt into the bounded RUN router."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-draft · give one Page a promise

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-draft
  → family craft: the stage's declared craft files, when the Page belongs to paper or application
```

What is DRAFT's alone: the promise may move here, and nowhere else without a new round.
Its risk runs in one direction: presenting an unavailable answer as settled fact, because a hole hidden at DRAFT reaches print wearing the same face as a real number.
So DRAFT's exit is not polish; it is a stable purpose, its Aims, and every unknown named with an owner.

## 🎯 The authority test

DRAFT decides what the Page is trying to become in the current round:

```text
owns       purpose · Aims · promised shape
may do     add · delete · move · rewrite
exits      when the promise is stable enough to test, investigate, or realize
```

An operation does not identify DRAFT.
Adding a paragraph for an existing Aim is REVISE.
Adding a new Aim, removing a promised result, or changing the Page's purpose is DRAFT.

DRAFT may run on an empty Page, repeat before handoff, or reopen a mature Page after REVISE or CHECK.
Returning to DRAFT because purpose or Aims changed starts a new round on the same persistent Page.

## ✍️ What DRAFT may write

DRAFT may write any Page section needed to expose the promise, subject to the base and matching Page Type.

```text
🧭 Opening      states the purpose now being promised
🖼 Diagram      exposes the promised shape when a figure helps
📚 Content      makes the proposed substance concrete enough to test
🎯 Aims         creates, removes, or changes the durable targets
📍 States       creates the factual initial row for each Aim
📎 Files        records the few continuations the round depends on
🗃 Log          records that the promise opened or changed
```

DRAFT is not the only phase allowed to create text or sections.
REVISE may add, delete, move, and rewrite under a fixed promise.
The difference is authority, not the visible diff.

## 🕳 Raise the question, then stop

When the Page needs a fact it cannot support, DRAFT leaves a visible hole and raises a Q-consumer carrying the stake.
A Q-consumer is the Page-side record of the question: what must be known, and the STAKE, meaning what the Page loses if the answer never comes.

```text
target prose     "The effect is <HOLE>." [Q-<local-id>]
Q-consumer       what must be known · why this Page depends on it
```

The Page Type or family names the physical hole and id shape.
The id must join the prose site to the Q-consumer.
Never invent a value or source to avoid a hole.

DRAFT stops before all executor-side work:

```text
DRAFT owns       Q-consumer · stake · visible hole
PROBE owns       Q-executor · route · match · dispatch · A-executor · A-consumer
```

Writing the neutral Q-executor, choosing a bank route, or collecting an answer is PROBE even when it happens immediately after drafting.

## 🔀 Exit and routing

DRAFT has no mandatory next phase.
Route by what the Page now needs:

```text
consequential unknown remains     → PROBE
promise is stable but realization needs work → REVISE
version is ready for judgment     → CHECK
promise still unsettled           → DRAFT again
```

A Page Type or local contract may declare a gate.
DRAFT never invents one.

## 🧾 RUN receipt

When called by RUN, read `../../haipipe-page/ref/page-run-contract.md` and
return its common phase receipt. DRAFT's receipt must additionally make these
facts explicit:

```text
reason             which purpose, Aim, or promised shape DRAFT defined
artifacts          the target Page and any declared source it changed
evidence           the exact Page locations that expose the promise
route              DRAFT | PROBE | REVISE | CHECK | HOLD
reopens_promise    false for repeated DRAFT in the same unsettled round
```

DRAFT never routes directly to CLOSE and never calls its own output checked.
If this DRAFT was entered from another phase, the controller already opened the
new round; DRAFT records that round rather than incrementing it again.

## 📂 Files

```text
page-phases/haipipe-page-draft/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-page`; Page Type variants live under `page-types/`; the shared question crossing is `probe/haipipe-probe` and begins only when the work enters PROBE.
The Board engine owns execution and audit; this phase owns only its authority and receipt.
