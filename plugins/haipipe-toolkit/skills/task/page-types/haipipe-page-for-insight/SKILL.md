---
name: haipipe-page-for-insight
description: >-
  The task-only Page Type for one CONSUMER-NEUTRAL Insight Page on the
  Task/Insights Board: a whole D→I→K→W chain plus reusable findings, carrying
  no downstream stake. This is where dataset-first exploration lives; Paper
  and Application consumers borrow a settled chain through PageX. Trigger:
  task insight, DIKW page, dataset exploration, insights board, page-type
  insight.
metadata:
  version: "0.6.4"
  last_updated: "2026-08-31"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Question/Scope → Sources → D → I → K → W → Reusable Findings"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-insight · turn evidence into a reusable D→I→K→W chain

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when inspecting Task/Discovery sources and `haipipe-plugin-pagex` when reusing accepted Page material.

## Where this type is used, and where it is not

```text
🧪 Task/Insights Board       THIS TYPE · one page, the whole D→I→K→W chain
                             consumer-neutral · no serves: · no application:

🔎 Application InsightBoard  NOT this type · four phase-owned Folders
                             I2 data · I3 information · I4 knowledge ·
                             I5 wisdom (`haipipe-insight-workflow`)
```

An Application decomposes the chain because its levels get reused across questions and refreshed on different clocks. This Board keeps them in one page because a consumer-neutral exploration has no roster to reassemble the chain for it, and one page is how it stays readable.

An Application borrows a settled chain from here through PageX rather than reopening the question locally.

What it borrows is an unsigned, consumer-neutral Reusable Finding. RF is not a
Design Handoff, has no `serves:` authority, and may not bind directly to an
Application DesignBoard. A consuming Application must register its own I1 QW
need and contextualize the exact RF version in a local, human-signed I5 Wisdom
Folder.

**Ownership, settled 260820.** This contract ships under `task/page-types/` because the task layer is now its only creator, which resolves the question QI0 raised while it governed both layers.

## Inherit and replace

```text
INHERIT from Task Page              REPLACE for Insight Page
source/run binding                  one-job grain → one neutral insight question
every shown number names a run      Why/Method/Result grammar → D→I→K→W
rerun reopens dependent reading     task verdict → Reusable Findings
human reads the result              one source → several Task/Discovery/Page sources allowed
```

Do not inherit a desired answer or downstream stake. A later Paper or
Application may borrow a settled finding; it does not commission this Page or
rewrite its question around a preferred consequence.

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
Task/Discovery Folder   executes or gathers source evidence
Task QA / source Page   says what data exists, at what grain, and how fresh
Task Insight Page       owns traceable D→I→K→W and reusable findings
Paper / Application    PageX-borrows a settled finding and decides its own use
```

This Page may name source population and analysis context, but never a
consumer's blocked decision, audience strategy, venue choice, or design
consequence. D/I/K remain evidence-led. W states general applicability,
boundary, and unsafe inference without writing final copy or strengthening K.

## Fixed Content outline

```text
### 1 · Origin
### 2 · Question and Scope
### 3 · Source Map
### 4 · Data
### 5 · Information
### 6 · Knowledge
### 7 · Wisdom
### 8 · Reusable Findings
```

- **Origin** says why the question is worth answering and what prompted it: a
  dataset landed, a run finished, or a pattern was noticed. It names no
  downstream consumer or blocked decision.
- **Question and Scope** states one answerable question with population/unit,
  time window, and exclusions.
- **Source Map** names Task Folders/Pages, Task QA, Discovery Pages, or accepted
  Pages. It never gives a downstream consumer a raw `results/` path.
- **Data** records dated observations with source/run anchors and no
  interpretation.
- **Information** derives patterns, nulls, and contradictions from named Data
  rows.
- **Knowledge** states propositions, strength, rivals, and boundary conditions
  from named Information rows.
- **Wisdom** states what K means in general: where it holds, where it breaks,
  and what would be unsafe to conclude. Every W row names a K parent.
- **Reusable Findings** exports finding, strength, boundary, source versions,
  and unresolved gaps in language a future consumer can use. It adds no design
  consequence because that belongs to the consumer's own workflow.

## Trace law

```text
source/run → D<n> → I<n> → K<n> → W<n> → RF<n> Reusable Finding
```

No level cites a later level as evidence. Preserve null, negative, and contradictory results. A contextual W may be useful and still fail when no K parent warrants it.

## Probe and PageX

```text
Task / Discovery Folder ─── Probe ──▶ Task Insight Page
accepted existing Page ──── PageX ──▶ Task Insight Page
settled Reusable Finding ─── PageX ──▶ any future consumer
```

On its board this Page Type inspects Task/Discovery sources through Probe. A consuming Paper or Application borrows a settled chain through PageX and never copies this Page's cards.

For an Application, that PageX edge terminates at its I5 bridge Folder, not at
Design. The Task Page supplies pre-climbed DIKW evidence; Application I1/I5 own
the commission, applicability judgment, design consequence, and signature.

## Runtime shape

```text
<task-board>/I<NN>-<slug>/                the Task/Insights Board, never an Application board
├── I<NN>-<slug>.md
└── evidence/
    ├── probe/   Task/Discovery cards and bindings
    ├── pagex/   accepted cross-Folder inputs
    └── display/ optional evidence views
```

The Page owns interpretation, not source code or raw results.
`evidence/display/` shows evidence and never becomes another authority.

## Workflow and staleness

Run the full shared workflow when needed:

```text
SHAPE ⇄ SURVEY ⇄ LAND ⇄ EMBED (the OUTLINE part) → WRITE → CHECK (the DRAFT part)
```

Changing a named run/source reopens dependent D/I/K/W/RF rows. A consumer's
context change does not rewrite this Page; that consumer must recheck the
PageX binding's applicability. A changed RF version stales every consuming
binding until it is rechecked.

## Closing checks

- `scope: task` is declared; `application:` and `serves:` are absent.
- The Page names no downstream consumer, blocked decision, or preferred use.
- The promised `insight-target` is reached or explicitly rejected with a reason.
- Every D row has a resolvable dated source/run.
- Every I/K/W/RF row traces to the immediately preceding authority.
- Nulls, contradictions, rivals, and scope limits remain visible.
- D/I/K contain no desired message or downstream persuasion language.
- W contextualizes without exceeding K; RF preserves unsafe inference and gaps.
- No RF claims a signature, `serves:` decision, Design Handoff, or direct
  Design authority.
- Source reruns have not left a settled but stale reading.
- A fresh consumer can use Division 8 through PageX without opening Task/Discovery sources.
- Division 8 reads correctly to a consumer that did not exist when it was written.

This variant owns no scripts.
