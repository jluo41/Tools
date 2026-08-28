---
name: haipipe-page-for-collection
description: >-
  Paper Page Type for a paper's evidence intake desk: dispatches the Roadmap's
  released directions, registers every QA receipt that comes back, and groups
  the campaign into laps. Use when dispatching directions, registering
  receipts, closing a lap, or seeing what is still out. Trigger: collection
  page, intake, lap, register QA, page-type collection.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-27"
  group-token: "SD"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Intake, then one division per lap L<n> in id order; Open is last"
---

# /haipipe-page-for-collection · collect the receipts, close the lap

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: collection`.

## 🧭 Grain and home

Exactly one Collection per paper, minted with (or right after) the Roadmap
and EVERGREEN (♻️): it never closes while any direction row is running. It is
the story group's fourth page:

```text
Paper-<Slug>/0-paperboard/A1-SD-story/
├── SD00-ideation/               where the idea came from
├── SD01-seed/                   what the paper IS · the scoreboard
├── SD02-roadmap/                where to go next · the plan
└── SD03-collection/             what came back · THIS PAGE · the intake desk
```

In the journey (haipipe-paper-workflow 0.5.0) this page is P3 Collection
(collect), the intake beat of the P1↔P2↔P3 establish loop.

## 📥 The Intake law · division 1

QA files are the SUBSTANCE of what came back; this page REGISTERS them and
never restates them. A lap row carries paths, ids, and one-line readings —
never copied tables, values, or conclusions, which would make this page a
second evidence authority the family forbids. Anyone wanting the finding
opens the QA file; anyone wanting the paper-grade assertion reads the Seed's
E-row. Division 1 states this law and the campaign's intake scope (which QA
banks receipts may come from).

## 📐 Content outline

```text
### 1 · Intake              🔒 the law above + intake scope
#### 2 · L1 · <date-slug>   one division per LAP, in id order
#### 3 · L2 · <date-slug>
### N · Open                🔥 what is still out running · always last
```

## 🔁 A lap · the middle divisions

One lap = one batch of released rows dispatched and brought home together.
Each lap division carries four blocks, all register-shaped:

```text
ran        which ▶️ released Roadmap rows this lap dispatched (R ids)
cards      the probe/ card ids raised for them (PP<NN>, one per row)
landed     one line per receipt: R id → QA path → one-line reading
settle     the E-flips this lap PROPOSES: E-row id → QA path · the Seed
           writes the flip; this block is a proposal, never the account
```

The join is one string in three places: the QA path in a lap's `landed` block
= the Roadmap row's receipt cell = the E-row's cite after the Seed settles.
Gate G3 (Collection → Seed) reads a lap: done-when tests hold, every card
binds a landed QA path, and the settle is written on the Seed — its receipt
Log row lives here.

A settle proposal reads discovery verdicts through the shared adapter
(novel → HIGH · partial → MEDIUM · preempted → LOW · inconclusive → stays
⬜), and the intake re-check screens every closest-prior list for this
paper's own preprints and versions, which are never prior art against their
own manuscript unless the Seed rules otherwise.

## 🃏 Dispatch rides the existing probe machinery

This page's `probe/` lane IS the campaign's dispatch surface: one card per
released direction row, stripped to a neutral Q-executor and handed to the
task/discovery orchestrators exactly as any page's PROBE phase does. Nothing
new is invented — the orchestrators, QA banks, claim rules, and `working`
state discipline all apply unchanged.

A card whose executor died before Report is HELD, never answered: the lap
registers the halt AS a halt and re-dispatches under the executor layer's
reclaim rule. A null result is a COMPLETED search that found nothing; a halt
gathered nothing and rejected nothing, and conflating the two mis-decides
the claim the card serves.

```text
pagex/     binds SD02-roadmap (the released rows) and SD01-seed (the E-rows
           the settle proposals point at)
probe/     the dispatch cards · one per released row · receipts land here
           first, then are registered on the lap
```

Three pens, never crossed: the Roadmap writes plans, this page registers
receipts, the Seed alone flips E-rows.

## ✅ Closing checks

- Division 1 states the Intake law and scope; no lap block restates QA
  content beyond a one-line reading.
- Every lap's `ran` ids resolve to ▶️/🔵/✅ rows on SD02-roadmap; every
  `landed` path exists on disk.
- Every card in `probe/` belongs to a named lap or sits in Open; nothing
  dispatched is unregistered.
- Every settle proposal names a real E-row and the exact QA path; the Seed's
  matching flip (when made) cites the same path.
- Open lists every still-running card; an empty Open with 🔵 rows on the
  Roadmap is a defect on one side or the other.
- The page names no venue and contains no manuscript prose.
- The current outline is approved and CHECK closes the built version.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
