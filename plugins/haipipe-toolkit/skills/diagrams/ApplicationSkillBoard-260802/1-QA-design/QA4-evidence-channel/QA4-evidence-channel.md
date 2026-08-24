# The evidence channel: PageX for accepted Pages, Probe only inside Insight
state: ✅ SETTLED · acquisition and consumption boundary verified
owner: JL

## Opening

When does Application use PageX, and when may it Probe?

PageX is the normal consumption route for accepted Pages. Probe is an acquisition route available only to an Application-local Insight Page under Task-backed authority. Brief, Design, and Artifact Pages never Probe.

### Writing Style

Say whether the source is an accepted Page or a Task/Discovery evidence folder; the noun determines the route.

## Diagram

```text
accepted Page ───────── PageX ───────▶ Brief / Insight / Design / Artifact

Task or Discovery folder ── Probe ──▶ Insight Page only
                                           │
                                           └─ accepted Design Handoff ─ PageX ─▶ Design
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

PageX binds existing accepted Page content by path and exact handoff row. It does not rediscover or re-evaluate the source folder.

#### 2 · Probe

Probe reaches Task/Discovery evidence when the local Insight question cannot be answered by accepted Pages. The Insight Page owns the question and receives the result; Task rules own evidence discipline.

#### 3 · Missing-insight route

A blocked Design Page records its Aim, the missing premise, current PageX matches, and why they are insufficient. It releases that packet to one local Insight Page and stops the unsupported design move.

#### 4 · Refresh

When evidence or accepted Pages change, refresh the local Insight and reopen only dependent Design divisions.

## Aims

### A1 · Contract
- A1.1 · No Design procedure dispatches Probe.
  **Done when:** routing and fresh-agent behavior both send missing knowledge to
  the InsightBoard's `1-I-insights/`.

## States

### A1 · Contract
- ✅ A1.1 · Both fresh agents routed missing premises to local Insight Pages and kept Probe out of Design.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/fn/chain.md`
- `../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
- `../../../../board/page-plugins/haipipe-plugin-pagex/SKILL.md`

## Law

PageX consumes accepted Pages. Probe acquires Task/Discovery evidence. Only an
Insight Page may cross from the second route back into the first.

## Log

260820 · Narrowed the old “Application owns no Probe” rule to “Design owns no
Probe; Application-local Insight may Probe under Task-backed authority.”
260820 · Two fresh-context runs verified the boundary on SMS and multi-audience email scenarios.
