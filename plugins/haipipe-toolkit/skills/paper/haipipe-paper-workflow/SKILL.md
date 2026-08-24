---
name: haipipe-paper-workflow
description: >-
  The paper-level phase machine: five phases (Ideate → Establish → Tell →
  Realize → Respond), one gate between each, every gate a checkable assertion
  over existing Pages. It owns transitions and phase receipts only — content
  authority stays with the six Page Type contracts, lifecycle authority with
  haipipe-page-workflow, and every verdict with an independent CHECK plus a
  human tick. "Journey phase" (P0-P4) and "Page phase" (OUTLINE…CHECK) are
  distinct words by law. Use when asking where a paper is in the journey,
  whether it may advance, what to mint next, or when running assemble.
  Trigger: paper journey, journey phase, what phase are we in, may we advance,
  phase gate, mint next page, assemble gate, /haipipe-paper-workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-24"
  summary: "0.4.0 (JL 260824): ideation-first story order per ideation 0.4.0 — P0's authority page is A1-SD-story/SD00-ideation (the separate A0 group is abolished), the seed sits at SD01, and G0's receipt reads: SD01-seed exists and its §5 first row binds SD00-ideation back. 0.3.0 (JL 260824): P0 renamed IDEATE — ideation page, token ID, home A0-ID-ideation, per the type rename in ideation 0.3.0. 0.2.0 (JL 260823): P0's home moves with explore 0.2.0 — the nursery lives at paperboard/A0, the repo is minted with the explore page before the seed, and G0's receipt becomes the same-board SD00 binding (the standing IdeaBoard is retired unshipped). 0.1.0: the thin five-phase machine over the six Page Types; owns gates and receipts only; explicitly NOT a revival of the deleted S01-S10 stage lane; gates are grep-able assertions; advancement is never scheduled."
---

# /haipipe-paper-workflow · know the phase, test the gate, mint the next page

Load `haipipe-paper` first; this file is its phase authority. It never edits a
Page, never runs a Page's lifecycle (that is `haipipe-page-workflow`), and
never judges content (that is CHECK plus the human ticks).

## 🔤 Terminology law

A **journey phase** is one of the five positions below (P0–P4). A **Page
phase** is one step of `haipipe-page-workflow`'s OUTLINE…CHECK loop. Every
`[phase]` argument in the door's verbs is a PAGE phase; a bare "phase" in any
Paper document must be readable as exactly one of the two, or it is a defect —
the same law the Round contract holds for "Paper Round" versus "workflow
round". Prefer "journey" when speaking of P0–P4.

## 🧭 Why this is not the retired stage lane

The deleted S01–S10 machinery owned ten content contracts, a resolver, and
per-stage tooling. This file owns none of that: content lives in the six Page
Type contracts, and this file only states WHICH page holds authority in each
phase and WHEN the next one may be minted. Deleting this file would lose no
content rule — that is the test it must keep passing.

## 🗺 The five phases

```text
phase          authority page                    what the phase produces
──────────────────────────────────────────────────────────────────────────────
P0 Ideate      ideation (A1-SD-story/SD00)       a graduated idea · the repo
                                                 is minted WITH this page,
                                                 before the seed
P1 Establish   seed     (A1-SD-story/SD01)       a defensible identity + E-board
P2 Tell        narrative (one per desk, A1)      a desk decision + section map
P3 Realize     section  (one per unit, B pairs)  signed-off units
   P3.9        assemble — a VERB, not a phase    the built deliverable ·
                                                 DRAFT until G3 holds
P4 Respond     round    (C1)                     routed concerns + response

library        venue    (QBv bank)               consulted at P2 §1 · never a phase
```

P0 and P4 are the cheap loop zones: ideas are disposable, rounds recur.
P1–P3 are the expensive one-way street the gates protect. A round may reopen
P1, P2, or P3; a retarget mints a new P2 from the unchanged seed.

## 🚪 The gates

Each gate is an assertion over pages that already exist. A gate that cannot be
tested by reading named files is misdesigned.

```text
G0  Ideate → Establish    precondition, tested on the ledger row alone:
                          per-claim novelty cells bound to QA files · a pilot
                          receipt or explicit waiver · a person's PROCEED tick
                          (or CAUTION with its risk accepted in the tick) ·
                          receipt, recorded after the act: SD01-seed exists in
                          this board's A1-SD-story and its §5 first row binds
                          SD00-ideation back (an idea graduating into a
                          DIFFERENT paper adds: that new repo exists as a
                          submodule)

G1  Establish → Tell      the Seed's outline is human-ticked · every ✅/🔨
                          E-row cites a §5 asset and carries its novelty
                          reading · the pitch sells nothing beyond ✅ rows
                          (placeholders visible otherwise)

G2  Tell → Realize        the Narrative's §1 binds one bank page · every claim
                          row names an E-row parent · every section-map row
                          names its unit page and budget

G3  Realize → assemble    every map row's unit page is CHECK-closed
                          (✅ SETTLED) · assemble itself RUNS ANYTIME — a
                          build made while G3 fails is watermarked DRAFT in
                          its receipt, one made while it holds is
                          SUBMISSION-READY · the gate informs, the person
                          decides, and the upload is a human act either way

G4  Respond (per round)   every received concern appears exactly once in the
                          ledger and routes exactly once — to the Seed when it
                          demands evidence the paper does not hold, to the
                          Narrative for a retelling, to a Section for a rework
                          — and a person approves the response receipt
```

## 🧾 Phase receipts

A phase transition leaves exactly one receipt: a dated Log row on the page
that granted it (the Ideation Page for G0, the Seed for G1, the Narrative for
G2 and G3, the Round for G4), stating the gate, the assertion results, and who
ticked. No separate receipt store exists; the pages are the record.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the
human tick or CHECK verdict it names. Nothing in this file may be wired to a
timer, a heartbeat, or a loop that advances phases on wall-clock time — a
recurring job may report "gate G3 still fails: SM04 not settled", never "gate
passed". (Adopted from the ARIS external-cadence rule: a heartbeat may say
keep going, never good enough.)

## 🔀 Resolving "what phase are we in"

Phase is read, not stored: it is the highest gate whose assertion currently
holds, per telling. Two tellings of one paper may sit in different phases —
the MS telling in P4 while a WISE telling is in P3 — because P2 onward is
per-narrative. P0 and P1 are per-paper and shared.
