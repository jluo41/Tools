# Application Brief: one identity, one intent boundary
state: 🟡 PARTIAL · contract 0.2.0 shipped · runtime specimen pending
page-type: brief
owner: JL

## Opening

What must be fixed before an Application commissions insight work or designs delivery?

One Brief names the audience set, behavior/outcome intent, venue scope, constraints,
Insight Need Map, and initial Design roster. It owns no evidence analysis.

### Writing Style

State decisions and unknowns separately. Cite accepted Pages with PageX paths; turn missing premises into Insight Needs.

## Diagram

```text
accepted Pages ─ PageX ─┐
                        ├─▶ 📌 Brief ─┬─▶ Insight Need Map
user intent ────────────┘             └─▶ Design roster
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Names the application, owner, decision context, and delivery boundary.

#### 2 · Audience and outcomes

Defines who acts, current and desired behavior, success measures, guardrails, and kill conditions without pretending evidence is already settled.

#### 3 · Venue scope

Pins one or more candidate venue packs and states what would make the selection change.

#### 4 · Insight Need Map

For each unresolved design premise: need id, blocked Aim, proposed question, DIKW target, existing PageX matches, strength needed, and owner.

#### 5 · Design roster

Lists candidate Design Pages by audience × behavior job × primary venue. The roster may change as Insights settle.

## Aims

### A1 · Contract
- ✅ A1.1 · Insight and Design work can start without inventing audience or outcome.
  **Done when:** both receive exact Brief refs and unresolved needs.
  **Now:** Required by Brief Page Type 0.2.0.


### P · Specimen
- ⬜ P1 · One runtime Brief passes Page CHECK.
  **Done when:** a materialized application uses the 0.2.0 contract.
  **Now:** Runtime specimen remains open.


## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-brief/SKILL.md`
- `../../../../application/haipipe-application/fn/brief.md`

## Law

The Brief decides what the Application is trying to do and what it still needs to understand; it does not perform the understanding.

## Log

260820 · Added Insight Need Map and many-Design roster to Brief 0.2.0.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0