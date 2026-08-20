# Insight to Design: PageX consumes handoffs, Design never Probes
state: ✅ SETTLED · PageX, missing-insight, and no-Probe route verified
owner: JL

## Opening

How does a Design Page use insight without copying the evidence pipeline or inventing a premise?

It binds exact Design Handoffs through PageX. Each binding records what design move it permits, the boundary that travels with it, and the Aim it releases. If the handoff is absent, stale, or too weak, Design opens a missing-insight request and stops that move; only the local Insight Page may Probe.

### Writing Style

Use explicit verbs: **bind**, **adopt**, **decline**, **block**, **refresh**. Avoid
“based on the data” unless the exact handoff row is named.

## Diagram

```text
🎨 Design Aim
    │
    ├─ PageX match accepted ──▶ bind handoff ──▶ design move + inherited rail
    │
    └─ missing / stale / weak ─▶ missing-insight release
                                      │
                                      ▼
                               🔎 local Insight Page
                               PageX and/or Probe
                                      │
                                      └──── refreshed handoff ────▶ 🎨
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Every Design Page keeps a small ledger:

```text
Design Aim | Insight Page | handoff row | adopted/declined | use | boundary
```

This is a consumption map, not a duplicate DIKW narrative.

#### 2 · Missing-insight release

The release shows the blocked Aim, proposed question, DIKW target, current PageX matches, destination local Insight Page, and why those matches are insufficient.
It is user-visible because commissioning new evidence work is a scope decision.

#### 3 · No-Probe boundary

Brief, Design, and Artifact Pages never dispatch Task/Discovery Probe cards.
They may search PageX for already accepted Pages. A local Insight Page may combine
PageX inputs with a Task-backed Probe when the accepted Page evidence is not enough.

#### 4 · Reopen behavior

When a bound handoff becomes stale or changes materially, only the dependent
Design divisions reopen. Unaffected messages stay accepted.

## Aims

### A1 · Contract
- A1.1 · Every design move reaches one exact accepted handoff.
  **Done when:** the Insight Use Map has no unsupported adopted row.

#### A2 · Boundary
- A2.1 · Missing knowledge never triggers inline Design research.
  **Done when:** a fresh run routes it to a local Insight Page and stops the
  unsupported design move.

## States

### A1 · Contract
- ✅ A1.1 · Required by Design Page Type 0.2.0.

#### A2 · Boundary
- ✅ A2.1 · Two fresh agents stopped unsupported design moves and released local Insight Pages.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-intervention/SKILL.md`
  The Design Page's Insight Use Map and no-Probe rule.
- `../../../../application/haipipe-application/fn/missing-insight.md`
  The visible release procedure.
- `../../../../board/page-plugins/haipipe-plugin-pagex/SKILL.md`
  Accepted-Page acquisition and binding.

## Law

PageX reads accepted Pages. Probe reads Task/Discovery evidence. A Design Page uses the first and delegates the second to its local Insight Page.

## Log

260820 · Split PageX consumption from Probe acquisition at the Application layer.
260820 · Fresh-context SMS and email scenarios verified exact PageX consumption and local Insight release.
