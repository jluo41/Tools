# Application Insight Page: one question, one DIKW chain, one Design Handoff
state: 🟡 PARTIAL · contract shipped · runtime specimen pending
page-type: insight
owner: JL

## Opening

What fixed shape lets an Application understand its data before it designs a message or interface?

One Insight Page answers one Application insight question. It does not mirror an entire dataset and it does not combine unrelated audience decisions. Its fixed divisions preserve the path from need to evidence to actionable handoff.

### Writing Style

Separate observation, organization, supported interpretation, contextual judgment, and design handoff. A sentence must not silently jump from D to W.

## Diagram

```text
1 Application Need
        ↓
2 Question + Scope ──▶ 3 Source Map
        ↓                    ↓
4 Data ──▶ 5 Information ──▶ 6 Knowledge
                                      ↓
                         7 Application Wisdom
                                      ↓
                              8 Design Handoff
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Names the Brief or Design Aim this Page serves and why the answer changes a real design decision.

#### 2 · Question and Scope

States one bounded, answerable question, the population/context, relevant time, and explicit exclusions.

#### 3 · Source Map

Pins Task folders, Discovery folders, accepted Pages, run identities, timestamps, and known limits. PageX consumes accepted Pages; Probe reaches Task/Discovery only when the current map cannot answer the question.

#### 4–7 · DIKW

- **D · Data:** anchored observations, rows, outputs, or source facts.
- **I · Information:** organized contrasts, rates, segments, or patterns.
- **K · Knowledge:** supported interpretation with strength and boundary.
- **W · Wisdom:** what this Application should do, avoid, or leave undecided.

#### 8 · Design Handoff

Publishes exact K/W rows, strength, boundary, allowed use, prohibited inference, staleness condition, and the blocked Design Aim it releases.

## Aims

### A1 · Contract
- A1.1 · One Page answers one Application insight question.
  **Done when:** every division supports the same downstream decision.

#### A2 · Handoff
- A2.1 · A Design Page can consume the answer without reopening raw evidence.
  **Done when:** the handoff names exact rows, limits, and staleness.

### P · Specimen
- P1 · One runtime Page exercises D→I→K→W and the handoff.
  **Done when:** a fresh agent creates or repairs one Page and stops at the correct
  human/validation gate.

## States

### A1 · Contract
- ✅ A1.1 · Fixed by Insight Page Type 0.3.0.

#### A2 · Handoff
- ✅ A2.1 · Division 8 is mandatory in the shipped contract.

### P · Specimen
- ⬜ P1 · Fresh-context validation has not yet been written back.

## Files

### 📋 Contracts
- `../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
  Canonical Page Type and division grammar.
- `../../../../application/haipipe-application/fn/chain.md`
  Public route for create, refresh, and missing-insight work.

## Law

D/I/K are evidence-led. W may be Application-contextual. The Design Handoff may be narrower than W, never broader than K/W support.

## Log

260820 · Added the fixed eight-division Application Insight contract.
