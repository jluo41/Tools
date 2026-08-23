# Meta: the InsightBoard's head page, split out of the Brief

state: 🟡 PARTIAL · contract 0.1.0 shipped · runtime specimen pending
page-type: meta
owner: JL

## Opening

Where does an Application say what data it actually has, before anyone asks a question of it?

On one Meta Page heading each InsightBoard. Until 260820 that material sat in the Brief, whose eight divisions served two different readers: 1-5 said what we are building and for whom, 6-7 said what data we have and what we must understand. When JL split the Application into an InsightBoard and a DesignBoard, the Brief split on its own seam and this Page took the insight half.

### Writing Style

Say what a division records, then say what it may not record. This Page's whole discipline is describing without concluding, and prose that only lists divisions will not carry that.

## Diagram

```text
STAYS ON THE BRIEF · delivery      MOVED HERE · the data
─────────────────────────────      ──────────────────────────────────────
opportunity · audience             source inventory · unit and grain
outcome · venue scope · promise    population · window · freshness · limits
the needs it RAISES                the roster of which page ANSWERS each
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

One Meta Page per InsightBoard, declaring `page-type: meta`. Seven fixed divisions: Purpose and Scope, Source Inventory, Unit and Grain, Population and Time Window, Freshness and Staleness, Known Limits, Insight Roster.

#### 2 · Why `meta` and not `opening`

`## Opening` is already a required section on every Board Page, so a page named Opening gives a reader "the Opening of the Opening page." The paper family hit the same collision and named its head page Seed.

#### 3 · Describes, never concludes

The Page may say a table holds 41,000 invitations over eleven months. It may not say the click rate is low, that a cohort underperforms, or that anything should change. An interpreting sentence belongs in an Insight Page's Information or Knowledge division. It also raises no question of its own: the Brief raises a need, and this Page records which Insight Page took it.

#### 4 · The Insight Roster

One row per raised need, with the answering page and its state. A need with no page is visible on purpose, because that row is the board's open queue.

## Aims

### A1 · Contract
- A1.1 · Each board has its own head page and neither carries the other's material.
  **Done when:** no source inventory remains on the Brief and no delivery framing appears here.

#### A2 · Discipline
- A2.1 · The Page describes without concluding.
  **Done when:** no division interprets, compares, ranks, or recommends.

### P · Specimen
- P1 · One runtime Meta Page inventories a real dataset.
  **Done when:** a fresh agent writes one and stops at the correct gate.

## States

### A1 · Contract
- ✅ A1.1 · Shipped in Meta Page Type 0.1.0 and Brief Page Type 0.3.0.

#### A2 · Discipline
- ✅ A2.1 · The closing checks forbid interpretation and question-raising.

### P · Specimen
- ⬜ P1 · No runtime Meta Page exists yet.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-meta/SKILL.md`
  The canonical Page Type and division grammar.
- `../../../../application/haipipe-application/fn/meta.md`
  The public route for create and refresh.

## Law

Meta owns the description of the data; Insight owns every claim made from it. A sentence that interprets has crossed a board boundary, not just a section boundary.

## Log

260820 · Created by splitting `haipipe-page-for-brief` when the Application became an InsightBoard plus a DesignBoard (JL).
