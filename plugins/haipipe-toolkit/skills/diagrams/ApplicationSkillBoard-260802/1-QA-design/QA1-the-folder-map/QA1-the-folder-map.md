# The folder map: one Application, four Page families, one delivery tail
state: ✅ SETTLED · canonical runtime tree shipped
owner: JL

## Opening

Where does each kind of Application work live?

The runtime tree follows dependency order. Each Insight and Design Page owns its own folder; concrete outputs stay inside Design unless independently governed.

### Writing Style

Use runtime paths, not skill-source paths, when explaining where application work lands.

## Diagram

```text
<application-root>/
├── 0-brief/
│   └── brief.md
├── 1-insights/
│   └── <insight-id>/<insight-id>.md
├── 2-design/
│   └── <design-id>/<design-id>.md
│       ├── pagex/
│       ├── outline/
│       └── display|word|slide|.../
├── 3-artifacts/
│   └── <artifact-id>/<artifact-id>.md
├── 4-deploy/
└── 5-rounds/
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Exactly one Page fixes the Application identity, audience set, outcomes, venue scope, Insight Need Map, and initial Design roster.

#### 2 · Insights

One folder answers one Application insight question. It may read accepted Pages with PageX or acquire Task/Discovery evidence through Task-backed Probe.

#### 3 · Design

One folder serves one audience × behavior job × primary venue. Repeated message or unit divisions live on that Page with their projections.

#### 4 · Artifacts

This folder is optional. A unit enters only when it can be accepted, rejected, versioned, or deployed independently from neighboring units.

#### 5 · Tail

Deployment receipts and feedback rounds are not Page Types. They reopen the smallest affected Insight, Design, or Artifact Page.

## Aims

### A1 · Contract
- A1.1 · Every current Application procedure writes into this tree.
  **Done when:** no public procedure requires legacy `0-lifecycle/` or
  application-local `1-probes/`.

## States

### A1 · Contract
- ✅ A1.1 · Application 0.8.0 and its procedures declare this tree.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
- `../../../../application/README.md`

## Law

Folders follow authority and dependency; they do not mirror every internal skill.

## Log

260820 · Added `1-insights/` and `2-design/`; made `3-artifacts/` optional.
