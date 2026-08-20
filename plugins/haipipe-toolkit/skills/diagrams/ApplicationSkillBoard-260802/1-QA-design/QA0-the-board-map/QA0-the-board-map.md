# The Board map: five decisions from understanding to delivery
state: ✅ SETTLED · architecture shipped in Application 0.8.0
owner: JL

## Opening

How should this Board be read?

Read Architecture first, then the local Insights layer, then Page Types, routing, and execution proof. Legacy Delivery pages and venue packs are supporting branches, not alternative spines.

### Writing Style

Name ownership and direction. Do not describe the Board as a flat catalog.

## Diagram

```text
QA architecture
      ↓
QI local Insights ── PageX ──▶ QBt Brief · Design · Artifact
      │                                │
      │                                ├── QBv venue constraints
      │                                ▼
      └──────────────────────────────▶ QC routes ──▶ QF proof

QB legacy pages ── migration evidence only
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

QA decides the runtime tree, authorities, cardinality, and the distinction between
Design projection and promoted Artifact.

#### 2 · Insights

QI decides how an Application-local Insight Page uses Task-backed evidence rules and publishes a Design Handoff.

#### 3 · Page Types

QBt plus QI1 form the four-type roster: one Brief, many Insights, many Design
Pages, and zero or more promoted Artifact Pages.

#### 4 · Engine

QC checks that public verbs route to Page contracts rather than reviving the old stage ladder.

#### 5 · Execute

QF records validation. “Skill written” is not “system works.”

## Aims

### A1 · Contract
- A1.1 · A reader can identify the authority for any Application question.
  **Done when:** the map distinguishes architecture, insight, type, route, and proof.

## States

### A1 · Contract
- ✅ A1.1 · The Board index and this Page show the same dependency order.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
  The public system summarized here.

## Law

No historical page or venue pack may override the four current Page Type contracts.

## Log

260820 · Replaced the external Insight Board → single Intervention map with the
Application-local Brief → Insights → many Design Pages architecture.
