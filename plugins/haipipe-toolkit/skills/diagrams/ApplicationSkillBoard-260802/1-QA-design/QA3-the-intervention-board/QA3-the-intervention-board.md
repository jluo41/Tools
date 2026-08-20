# The Application Board: one Brief, many Insights, many Designs
state: ✅ SETTLED · cardinality and ownership shipped
owner: JL

## Opening

Is an Application one Intervention Page?

No. The Application is the containing Board/folder. It owns one Brief, many
Insight Pages, many user-facing Design Pages, and only the Artifact Pages that earn an independent lifecycle.

### Writing Style

Use **Application** for the whole system and **Design Page** for one audience/job/ venue design. Use `intervention` only when referring to the machine Page key.

## Diagram

```text
Application
├── Brief × 1
├── Insight × N
├── Design × N
│   ├── patient × refill action × SMS
│   ├── clinician × review action × dashboard
│   └── manager × escalation action × report
└── Artifact × 0..N
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

One Design Page serves one audience × behavior job × primary venue. If either the decision maker, behavior job, or delivery logic changes materially, split Pages.

#### 2 · Message divisions

A Design Page may contain many repeated message or component divisions. Each division carries job, content move, handoff refs, constraints, variants, rails, and acceptance state.

#### 3 · Projection first

SMS copy, email sequence, dashboard cards, checklist rows, and report sections normally remain visible projections of the owning Design Page.

#### 4 · Artifact promotion

Promote only when one unit can be accepted, rejected, versioned, or deployed independently. Promotion is governance, not a synonym for “output.”

## Aims

### A1 · Contract
- A1.1 · The public skill never assumes exactly one Intervention.
  **Done when:** it routes many Design Pages and an optional Artifact layer.

## States

### A1 · Contract
- ✅ A1.1 · Shipped in Application 0.8.0 and Design Page Type 0.2.0.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-intervention/SKILL.md`
- `../../../../application/page-types/haipipe-page-for-artifact/SKILL.md`

## Law

The Application is the container; Design Pages are its compositional units.

## Log

260820 · Replaced “exactly one Intervention” with many audience/job/venue Designs.
