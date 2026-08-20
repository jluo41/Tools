# Application Artifact Page: an optional governance promotion
state: 🟡 PARTIAL · contract 0.2.0 shipped · stale-version test pending
page-type: artifact
owner: JL

## Opening

Does every message, card, or report section need its own Page?

No. Concrete output normally remains a projection of its Design Page. Promote a unit to an Artifact Page only when it can be accepted, rejected, versioned, or deployed independently from its neighbors.

### Writing Style

Lead with the independent-governance reason for promotion. Show exact content and version separately from rationale.

## Diagram

```text
Design projection
      │
      ├─ reviewed/deployed with neighbors ──▶ stay on Design Page
      │
      └─ independently governed ────────────▶ 📦 Artifact Page
                                                   │
                                  version + render + acceptance + deploy
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

The Page states which independent accept/reject/version/deploy decision makes promotion necessary.

#### 2 · Source binding

Pins the Design Page, unit division, accepted handoffs, venue constraints, and rails that the Artifact may not broaden.

#### 3 · Content and render

Owns one exact content version and its visible render or executable package.

#### 4 · Acceptance

Approval binds reviewer, date, source Design version, content version, and render/ package version. Any material input change invalidates acceptance.

#### 5 · Deployment

Deployment records target, version, timestamp, receipt, rollback path, and the feedback route into the smallest affected Page.

## Aims

### A1 · Contract
- A1.1 · No Artifact Page exists merely because output exists.
  **Done when:** every Page names an independent governance decision.

#### A2 · Staleness
- A2.1 · Changed Design or render invalidates prior acceptance.
  **Done when:** a negative fixture fails before a refreshed version passes.

## States

### A1 · Contract
- ✅ A1.1 · Required by Artifact Page Type 0.2.0.

#### A2 · Staleness
- ⬜ A2.1 · Negative runtime fixture remains open.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-artifact/SKILL.md`
- `../../../../application/haipipe-application/fn/artifact.md`

## Law

Artifact is a governance promotion, not the default container for every rendered unit.

## Log

260820 · Made Artifact optional and projection-first.
