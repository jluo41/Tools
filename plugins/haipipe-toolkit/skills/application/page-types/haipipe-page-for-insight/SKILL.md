---
name: haipipe-page-for-insight
description: >-
  The Application-owned Page Type contract for one Application-local Insight Page. It serves one Brief or Design need, uses Task-backed Probe/source/run/staleness/human-reading rules to turn Task, Discovery, and accepted Page evidence into D→I→K, then adds application-contextual Wisdom and a PageX-ready Design Handoff. Use when an Application needs to understand its data before design, when a Brief or Design Page has a missing premise, when several Task outputs must be synthesized for one audience/behavior decision, or when deployment data refreshes an existing insight. Trigger: application insight, insights page, DIKW for application, design evidence need, data exploration for message design, page-type insight, /haipipe-page-for-insight.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-20"
  summary: "Application-owned placement with Task-backed evidence: neutral D/I/K, contextual W, and a PageX-ready Design Handoff."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Application Need → Question/Scope → Sources → D → I → K → Application W → Design Handoff"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-insight · understand what this Application needs before design

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when inspecting Task/Discovery sources and `haipipe-plugin-pagex` when reusing accepted Page material.

This Page Type lives under the Application skill set because its lifecycle serves one Application. It remains Task-backed because file placement cannot transfer evidence authority.

## Inherit and replace

```text
INHERIT from Task Page              REPLACE for Insight Page
source/run binding                  one-task-folder grain → one application insight question
every shown number names a run      Why/Method/Result grammar → D→I→K→W
rerun reopens dependent reading     task verdict → Design Handoff
human reads the result              one source → several Task/Discovery/Page sources allowed
```

Do not inherit a desired answer. The Application may name the design decision this Page serves; it may not prescribe the finding the Page must reach.

## Required identity

Declare:

```yaml
page-type: insight
scope: application
application: <application-root-or-id>
serves: <Brief Aim or Design Need id>
insight-target: data | information | knowledge | wisdom
```

One Page covers one answerable Application insight question. Split when two questions can settle, stale, or be reused independently.

## Boundary

```text
Task/Discovery       executes or gathers source evidence
Insight Page         owns traceable D→I→K and contextual W for one Application need
Brief/Design Page    chooses what to do with settled handoffs through PageX
Artifact             owns exact content/render/acceptance
```

The Page may say which Application decision is blocked. Its D/I/K rows stay evidence-led. Its W rows may use audience, behavior, context, and venue, but may not write final copy or silently strengthen K.

## Fixed Content outline

```text
### 1 · Application Need
### 2 · Question and Scope
### 3 · Source Map
### 4 · Data
### 5 · Information
### 6 · Knowledge
### 7 · Application Wisdom
### 8 · Design Handoff
```

- **Application Need** names the Application, audience/behavior context, owning Aim, and decision this Page informs. It states no preferred result.
- **Question and Scope** rewrites that need as one answerable question with population/unit, time window, and exclusions.
- **Source Map** names Task Pages/folders, Task QA, Discovery Pages, or accepted Pages. It never gives a Design Page a raw `results/` path.
- **Data** records dated observations with source/run anchors and no interpretation.
- **Information** derives patterns, nulls, and contradictions from named Data rows.
- **Knowledge** states propositions, strength, rivals, and boundary conditions from named Information rows.
- **Application Wisdom** states what K means for this Application's audience, context, behavior, and risk. Every W row names a K parent.
- **Design Handoff** exports finding, strength, boundary, source versions, design consequence, forbidden overreach, unresolved gaps, and `serves:` id. It contains no final message copy.

## Trace law

```text
source/run → D<n> → I<n> → K<n> → W<n> → H<n> Design Handoff
```

No level cites a later level as evidence. Preserve null, negative, and contradictory results. A contextual W may be useful and still fail when no K parent warrants it.

## Probe and PageX

```text
Task / Discovery folder ── Probe ──▶ local Insight Page
accepted existing Page ─── PageX ──▶ local Insight Page
settled Design Handoff ─── PageX ──▶ Brief / Design Page
```

This is the only Application Page Type allowed to inspect Task/Discovery sources through Probe. Brief, Design, and Artifact Pages own no `probe/` and cannot copy this Page's cards.

## Runtime shape

```text
<application-root>/1-insights/I<NN>-<slug>/
├── I<NN>-<slug>.md
├── probe/       Task/Discovery cards and bindings
├── pagex/       accepted cross-Page inputs
└── display/     optional evidence views
```

The Page owns interpretation, not source code or raw results. `display/` shows evidence and never becomes another authority.

## Workflow and staleness

Run the full shared workflow when needed:

```text
OUTLINE ⇄ PROBE ⇄ EVIDENCE → DRAFT → REVISE → CHECK
```

Changing a named run/source reopens dependent D/I/K/W/H rows. Changing Application context reopens W/H without rewriting still-valid D/I/K. A Design Page borrowing a changed Handoff becomes stale until it rechecks applicability and acceptance.

## Closing checks

- The Page serves one named Brief Aim or Design Need.
- The promised `insight-target` is reached or explicitly rejected with a reason.
- Every D row has a resolvable dated source/run.
- Every I/K/W/H row traces to the immediately preceding authority.
- Nulls, contradictions, rivals, and scope limits remain visible.
- D/I/K contain no desired message or downstream persuasion language.
- W contextualizes without exceeding K; Handoff names forbidden overreach.
- Source reruns have not left a settled but stale reading.
- A fresh Design agent can consume Division 8 through PageX without opening Task/Discovery sources.

This variant owns no scripts.
