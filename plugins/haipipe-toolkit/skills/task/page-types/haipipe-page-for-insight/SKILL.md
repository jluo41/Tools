---
name: haipipe-page-for-insight
description: >-
  The Page Type for one CONSUMER-NEUTRAL Insight Page on the Task/Insights
  Board: a whole D→I→K→W chain in one page, carrying no downstream stake. This
  is where dataset-first exploration lives, before any Application raises a
  need; an Application borrows a settled chain from here through PageX.
  Trigger: task insight, DIKW page, dataset exploration, insights board,
  page-type insight.
metadata:
  version: "0.6.0"
  last_updated: "2026-08-20"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Question/Scope → Sources → D → I → K → W → Reusable Findings"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-insight · turn evidence into D→I→K→W, in one of two scopes

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when inspecting Task/Discovery sources and `haipipe-plugin-pagex` when reusing accepted Page material.

## Where this type is used, and where it is not

```text
🧪 Task/Insights Board       THIS TYPE · one page, the whole D→I→K→W chain
                             consumer-neutral · no serves: · no application:

🔎 Application InsightBoard  NOT this type · four separate pages
                             haipipe-page-for-data · -information
                             -knowledge · -wisdom
```

An Application decomposes the chain because its levels get reused across questions and refreshed on different clocks. This Board keeps them in one page because a consumer-neutral exploration has no roster to reassemble the chain for it, and one page is how it stays readable.

An Application borrows a settled chain from here through PageX rather than reopening the question locally.

**Ownership, settled 260820.** This contract ships under `task/page-types/` because the task layer is now its only creator, which resolves the question QI0 raised while it governed both layers.

## Inherit and replace

```text
INHERIT from Task Page              REPLACE for Insight Page
source/run binding                  one-job grain → one application insight question
every shown number names a run      Why/Method/Result grammar → D→I→K→W
rerun reopens dependent reading     task verdict → Design Handoff
human reads the result              one source → several Task/Discovery/Page sources allowed
```

Do not inherit a desired answer. The Application may name the design decision this Page serves; it may not prescribe the finding the Page must reach.

## Required identity

Declare:

```yaml
page-type: insight
scope: task                                      # the only live scope
insight-target: data | information | knowledge | wisdom
```

A Page carrying `application:` or `serves:` is defective: those two fields are a commission, and this Board's pages are consumer-neutral so they can be reused by a consumer that did not exist when they were written.

One Page covers one answerable insight question. Split when two questions can settle, stale, or be reused independently.

## Boundary

```text
Task/Discovery       executes or gathers source evidence
Meta Page            says what data exists, at what grain, how fresh   (application scope)
Insight Page         owns traceable D→I→K and contextual W
Brief/Design Page    chooses what to do with settled handoffs through PageX
```

A `scope: application` Page may say which Application decision is blocked. A `scope: task` Page may not: naming a downstream stake is what makes a page unreusable by the next consumer.

In both scopes D/I/K rows stay evidence-led. W rows may use audience, behavior, context, and venue, but may not write final copy or silently strengthen K.

## Fixed Content outline

```text
                          scope: task              scope: application
### 1 ·                   Origin                   Application Need
### 2 · Question and Scope
### 3 · Source Map
### 4 · Data
### 5 · Information
### 6 · Knowledge
### 7 ·                   Wisdom                   Application Wisdom
### 8 ·                   Reusable Findings        Design Handoff
```

Divisions 2 to 6 are identical in both scopes. Only the two ends differ, because only the two ends touch a consumer.

- **Origin** (`scope: task`) says why the question is worth answering and what prompted it: a dataset landed, a run finished, a pattern was noticed. It names no downstream consumer and no blocked decision.
- **Application Need** (`scope: application`) names the Application, audience/behavior context, owning Aim, and decision this Page informs. It states no preferred result.
- **Question and Scope** rewrites that need as one answerable question with population/unit, time window, and exclusions.
- **Source Map** names Task Pages/folders, Task QA, Discovery Pages, or accepted Pages. It never gives a Design Page a raw `results/` path.
- **Data** records dated observations with source/run anchors and no interpretation.
- **Information** derives patterns, nulls, and contradictions from named Data rows.
- **Knowledge** states propositions, strength, rivals, and boundary conditions from named Information rows.
- **Wisdom** (`scope: task`) states what K means in general: where it holds, where it breaks, what it would be unsafe to conclude. Every W row names a K parent.
- **Application Wisdom** (`scope: application`) states what K means for this Application's audience, context, behavior, and risk. Every W row names a K parent.
- **Reusable Findings** (`scope: task`) exports finding, strength, boundary, source versions, and unresolved gaps, in language a consumer this Page has never heard of can still use. No design consequence, because there is no design yet.
- **Design Handoff** (`scope: application`) exports the same, plus design consequence, forbidden overreach, and the `serves:` id it releases. It contains no final message copy.

## Trace law

```text
source/run → D<n> → I<n> → K<n> → W<n> → H<n> Design Handoff
```

No level cites a later level as evidence. Preserve null, negative, and contradictory results. A contextual W may be useful and still fail when no K parent warrants it.

## Probe and PageX

```text
Task / Discovery folder ── Probe ──▶ Insight Page          (both scopes)
accepted existing Page ─── PageX ──▶ Insight Page          (both scopes)
settled Reusable Finding ─ PageX ──▶ any consumer          (scope: task)
settled Design Handoff ─── PageX ──▶ Brief / Design Page   (scope: application)

a scope: task Page may ALSO be borrowed straight into a scope: application
Page, which is the normal route when exploration preceded the Brief
```

On its board this Page Type inspects Task/Discovery sources through Probe. A consuming Paper or Application borrows a settled chain through PageX and never copies this Page's cards.

## Runtime shape

```text
<task-board>/I<NN>-<slug>/                the Task/Insights Board, never an Application board
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

- `scope:` is declared, and the fields it requires are present and no others.
- A `scope: application` Page serves one named Brief raised need or Design Aim; a `scope: task` Page names no consumer at all.
- The promised `insight-target` is reached or explicitly rejected with a reason.
- Every D row has a resolvable dated source/run.
- Every I/K/W/H row traces to the immediately preceding authority.
- Nulls, contradictions, rivals, and scope limits remain visible.
- D/I/K contain no desired message or downstream persuasion language.
- W contextualizes without exceeding K; Handoff names forbidden overreach.
- Source reruns have not left a settled but stale reading.
- A fresh consumer can use Division 8 through PageX without opening Task/Discovery sources.
- A `scope: task` Division 8 reads correctly to a consumer that did not exist when it was written.

This variant owns no scripts.
