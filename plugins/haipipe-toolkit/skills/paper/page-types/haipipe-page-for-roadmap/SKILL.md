---
name: haipipe-page-for-roadmap
description: >-
  The Paper Page Type for one paper's campaign plan: which directions to
  explore (data, model training, results analysis, …), each direction one
  ledger row serving a named Seed E-row, with an executor board, a done-when,
  a budget, and a person's release before anything runs. It is the ROUTE
  authority of the establish loop — the Seed states the gaps, this page plans
  the laps, the Collection Page collects what comes back. One page per paper,
  evergreen, third page of the story group. Use when a fresh Seed leaves
  everyone directionless, when planning which boards to dispatch to, when
  releasing or dropping a direction, or when reading what the campaign still
  owes. Trigger: roadmap page, roadmap, direction board, where to explore,
  campaign plan, release a direction, serves E-row, page-type roadmap,
  /haipipe-page-for-roadmap.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-27"
  summary: "0.1.1 (JL 260827): gate-receipt duty sunk from the workflow's receipts law into this contract — G2's receipt Log row lives on this page (the gate the live SD02-roadmap passed on 260824 without leaving a receipt, because only the collection contract carried the duty locally). 0.1.0 (JL 260824): the campaign plan page, born with journey 0.5.0 — P2 Roadmap (route) of the establish loop. One page per paper at A1-SD-story/SD02-roadmap/; a Direction Board of eight-column rows, each serving a Seed E-row; ⬜ proposed → ▶️ released (a person's act) → 🔵 running → ✅ landed / 🚫 dropped, rows never deleted; the page plans and never executes — dispatch and intake belong to the Collection Page, the E-row flip to the Seed."
  group-token: "SD"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Mission, division 2 is Direction Board; every later division's first word is a direction id R<n>, in id order"
---

# /haipipe-page-for-roadmap · route the campaign, one released row at a time

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: roadmap`.

## 🧭 Grain and home

Exactly one Roadmap per paper, minted right after the Seed and EVERGREEN (♻️):
it never closes while any E-row is ⬜/🔨. It is the story group's third page:

```text
Paper-<Slug>/0-paperboard/A1-SD-story/
├── SD00-ideation/               where the idea came from
├── SD01-seed/                   what the paper IS · the scoreboard
├── SD02-roadmap/                where to go next · THIS PAGE · the plan
└── SD03-collection/             what came back · the intake desk
```

The story group is wholly venue-free; the desk layer starts at the
`A2-NA-narrative/` group. In the journey (haipipe-paper-workflow 0.5.0) this
page is P2 Roadmap (route), the planning beat of the P1↔P2↔P3 establish loop.

## 📐 Content outline

```text
### 1 · Mission             🔒 what the paper still owes: the Seed's ⬜/🔨
                               E-rows and §8 open tensions, transcribed as a
                               readable debt list
### 2 · Direction Board     🔥 the whole campaign in one screen · one row per
                               direction
#### 3 · R1 · <slug>        one division per direction, in id order
#### 4 · R2 · <slug>
```

## 📊 The Direction Board · division 2

One row per exploration direction, eight columns, every cell a state and
never a blank:

```text
id  direction          serves   executor                done-when              budget  status       receipt
────────────────────────────────────────────────────────────────────────────────────────────────────────────
R1  data extract       E2       Project-…-Raw2AIData    cohort parquet +       2d      ✅ landed    QA/3-….md
                                                        coverage table
R2  model training     E1·E6    Project-ExpModel-…      ΔAUC CI excludes 0     1wk     🔵 running   —
R3  results analysis   E5       tasks/A1_TestToLearn    heterogeneity table    3d      ⬜ proposed  —
                                                        survives robustness
```

Status vocabulary: `⬜ proposed` → `▶️ released` → `🔵 running` →
`✅ landed` / `🚫 dropped` (reason in the division). Dropped rows are never
deleted — the graveyard stops the same dead end being re-planned in new words.
A `—` cell is legal only where the status makes it moot; on a live row every
cell is a state, a path, or a testable sentence.

Column laws:

- **serves** names at least one Seed §6 E-row (or an Ideation pilot
  obligation). A direction serving nothing may not be released — the same law
  the design family holds for direction cards: no exploring for exploring's
  sake.
- **executor** is a board or task-group path outside this repo; this page
  never runs anything.
- **done-when** is a testable sentence, not a vibe — it is what G3 reads.
- **receipt** is the QA file path the direction landed; the same string
  appears on the Collection lap that registered it and in the E-row cite that
  flipped on it.

## ✋ Release is a person's act

A machine proposes rows, estimates budgets, and recommends order; only a
person flips ⬜ proposed to ▶️ released, row by row, with initials and date in
the row's division. Gate G2 (Roadmap → Collection) reads exactly this: every
🔨/⬜ E-row has a ▶️ row serving it or an explicit waiver on the Seed's Log.
Its receipt Log row lives here: when the gate passes, this page's Log records
the gate, the rows released, and who released them.
Dropping a row is as human an act as releasing it.

## 🃏 The plan records; it never executes

Dispatch machinery does not live here. A released row is picked up by the
Collection Page, whose `probe/` lane raises one card per row and hands it to
the task/discovery orchestrators; receipts land there and are settled onto
the Seed. This page's own lanes stay thin:

```text
pagex/     binds SD01-seed (the §6 gap list and §8 tensions this plan serves)
probe/     optional: planning questions only (e.g. "does an executor for X
           exist?"), never the campaign dispatch itself
```

The three-pen law of the establish loop: Roadmap writes plans, Collection
registers receipts, the Seed alone flips E-rows.

## ✅ Closing checks

- Division 1 transcribes every current ⬜/🔨 E-row; none is silently missing.
- Every ledger row has no blank cell; every status is from the fixed
  vocabulary; every ▶️/🔵/✅ row carries a person's release with date.
- Every row's serves column resolves to a real E-row id on SD01-seed §6.
- Every ✅ landed row's receipt path exists on disk and matches the
  Collection lap that registered it.
- Dropped rows are all present with reasons; nothing planned has vanished.
- The page names no venue and contains no manuscript prose.
- The current outline is approved and CHECK closes the built version.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
