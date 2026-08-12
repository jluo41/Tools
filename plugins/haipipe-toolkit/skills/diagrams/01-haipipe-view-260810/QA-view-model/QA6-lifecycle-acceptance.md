# Independent gates and bounded reopening
state: ✅ SETTLED · machines establish freshness; people accept Views and Displays
owner: JL
method: track evidence, body, artifact, and handoff state separately and reopen only dependents

## Opening
When is a View ready, and which parts must reopen when its evidence, Display, or consumer changes?
A successful build proves freshness and routing, not human acceptance.
Evidence, the readable body, each Display, and each consumer handoff therefore keep separate states.
Changes propagate only through declared dependencies so an unrelated View or Display does not reopen.
This Page decides closure authority and the smallest safe reopening rule.

**Machine authority**: validate bindings, build artifacts, compare hashes, and report stale dependencies.

**Human authority**: accept the current View meaning, each promised Display render, and any downstream placement gate that requires judgment.

## Diagram

**Separate gates**: readiness is a conjunction, not one status copied across the chain.

```text
evidence current
      │
      ▼
View body valid ── human View acceptance
      │
      ├──▶ Display1 rendered ── human acceptance 1
      └──▶ Display2 rendered ── human acceptance 2
                    │
                    ▼
             consumer handoff
```

## Content

### 1 · State dimensions

**The state ledger**: each dimension changes independently.

```text
freshness ≠ body validity ≠ rendering ≠ acceptance ≠ handoff
```

Track input and evidence freshness, body/Card validity, artifact status, Display human acceptance, fixture freshness, View human acceptance, and consumer placement/handoff separately.
No build, browser check, or rendered preview may write `accepted` on a person's behalf.

### 2 · Closure

**The close test**: mechanical readiness and human gates are both required.

```text
current bindings + inspectable outputs + current fixture + human gates ──▶ close
```

Mechanical readiness requires resolvable inputs and Cards, inspectable promised Displays, resolvable consumers, and a current fixture.
View closure additionally requires human acceptance of the current body.
Each Display keeps its own human gate, and a consumer may hand off only the accepted subset it names.

### 3 · Reopening

**The propagation rule**: a change follows declared bindings only.

```text
changed node ──▶ dependent body / Displays / handoffs
             └─╳ unrelated units remain closed
```

An evidence or source change reopens the affected body/Card judgment, every dependent Display, the View acceptance when meaning changed, and their handoffs.
A render-only Display change reopens that Display and its handoffs without automatically reopening unrelated Displays or unchanged View meaning.
A consumer prose or placement change reopens that consumer only.
The manifest's declared bindings define the propagation path.

## Aims

### A1 · State dimensions
- A1.1 · Prevent freshness, rendering, acceptance, and handoff from collapsing into one status.
  **Done when:** each can change without silently changing the others.

### A2 · Closure
- A2.1 · Separate mechanical completion from human closure.
  **Done when:** a current fixture can coexist with waiting View and Display gates.

### A3 · Reopening
- A3.1 · Reopen only declared dependents.
  **Done when:** evidence, render, and consumer changes follow three distinct propagation rules.

## States

### A1 · State dimensions
- ✅ A1.1 · QBt1 and QV1 report evidence, artifact, acceptance, fixture, and handoff state independently.

### A2 · Closure
- ✅ A2.1 · The specimen builds and checks current while View, Displays, and consumer handoff remain waiting on their own gates.

### A3 · Reopening
- ✅ A3.1 · Content 3 defines dependency-scoped reopening and excludes unrelated artifacts.

## Files

- `../QBt-page-types/QBt1-for-view.md`
  The specimen carrying all independent gates.
- `../../view/haipipe-view/scripts/view.py`
  The deterministic freshness, build, and status implementation.
- `../QBt-page-types/views/QBt1-for-view/manifest.json`
  The declared dependency graph used for bounded reopening.

## Log

- 260811 · [RULING-JL] A View may own many Displays, and each Display keeps an independent acceptance decision.
- 260810 · [RULING-JL] Machine validation and successful rendering never imply human acceptance or consumer handoff.
