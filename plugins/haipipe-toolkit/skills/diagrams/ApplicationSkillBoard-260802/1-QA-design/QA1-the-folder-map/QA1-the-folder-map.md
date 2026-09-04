# The folder map: two named boards, four Page families
state: ✅ SETTLED · two-board runtime tree shipped
owner: JL

## Opening

Where does each kind of Application work live?

An Application is two boards, each named for its subject. The InsightBoard holds what the data says; the DesignBoard holds what gets sent and who signed it. Every Page owns its own folder, group folders carry their group token, and concrete output stays a projection rather than becoming a Page.

### Writing Style

Use runtime paths, not skill-source paths, when explaining where application work lands.

## Diagram

**The runtime tree**: two boards, named for their subjects.

```text
<application-root>/
├── <DataSubject>-InsightBoard/          e.g. SmsClickR4-InsightBoard
│   ├── board.md
│   ├── 0-M-meta/M00-meta/               page-type: meta
│   │   ├── pagex/
│   │   └── display/
│   └── 1-I-insights/I<NN>-<slug>/       page-type: insight · scope: application
│       ├── probe/                       the ONLY probe/ in an Application
│       ├── pagex/
│       └── display/
└── <DesignTopic>-DesignBoard/           e.g. YoungMaleRefill-DesignBoard
    ├── board.md
    ├── 0-A-brief/A00-brief/             page-type: brief
    │   └── pagex/
    ├── 1-D-design/D<NN>-<audience>-<job>/   page-type: design
    │   ├── pagex/
    │   ├── outline/
    │   └── display/
    └── 2-artifacts/                     projections only · no Pages
```

Gone from this tree: `4-deploy/` and `5-rounds/`. The Application ends at ACCEPTED, and shipping and measurement are task-layer work.

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
- ✅ A1.1 · Every current Application procedure writes into this tree.
  **Done when:** no public procedure requires legacy `0-lifecycle/` or
  application-local `1-probes/`.
  **Now:** Application 0.8.0 and its procedures declare this tree.


## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
- `../../../../application/README.md`

## Law

Folders follow authority and dependency; they do not mirror every internal skill.

## Log

260820 · Added `1-insights/` and `2-design/`; made `3-artifacts/` optional.
260820 · Replaced the single-board tree with two named boards, renamed the group folders to carry their token, and dropped `4-deploy/` and `5-rounds/`.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0