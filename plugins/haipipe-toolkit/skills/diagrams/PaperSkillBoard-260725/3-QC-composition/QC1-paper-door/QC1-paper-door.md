# QC1 · Keep the Paper door thin while Pages carry the work

state: ✅ SETTLED · thin Paper router validated
owner: JL
method: trace every Paper verb to an existing Page Type, shared workflow, or accepted assembly input

## Opening
What should the Paper door still own after research design, evidence, displays, and prose have moved onto Pages?
It owns entry, Page selection, Paper graph integrity, assembly, and delivery.
It delegates lifecycle to the shared Page workflow and never recreates the retired S01 to S10 stage router.

**Where this page sits**: QC2 names the Page-local plugins the door may request but does not implement.

**Why it matters**: a thin door stays understandable because every durable decision remains visible on a Page.

## Writing Style
Describe routing in terms of user intent and owning Page.
Do not restate full Page Type or plugin contracts.

## Diagram
**Thin Paper router**: public verbs resolve to owners instead of stage implementations.

```text
user intent ─▶ Paper door ─┬─▶ typed Page
                           ├─▶ shared Page workflow
                           └─▶ assemble accepted outputs
```

## Content
### 1 · Paper door
**Composition law**: route, inspect, and assemble without becoming a second authoring tree.

```text
seed · venue · narrative · section · round
                    │
                    └─▶ accepted outputs ─▶ paper build

/haipipe-paper status [family] ─▶ regenerated rollup, not a Page Type
```

Retargeting preserves Seed, creates or updates Venue, and creates a distinct Narrative.
Assembly reads accepted Narrative, Section, and display outputs rather than mining raw Task or Discovery folders.

## Aims
### A1 · 🚪 Paper door
- A1.1 · Every public Paper verb resolves to one durable owner.
  **Done when:** no active verb depends on a retired stage contract or duplicate build engine.

## States
### A1 · 🚪 Paper door
- ✅ A1.1 · The current door routes five Page Types, one status command, and accepted-output assembly.

## Files
- `../../paper/haipipe-paper/SKILL.md` · current public door
- `../../paper/README.md` · family map and retired boundary

## Log
260820 · Reduced the Paper runtime to routing, graph integrity, assembly, and delivery.
260820 · Dropped Dash as a Page Type; `/haipipe-paper status [family]` now covers the same rollup as a command.
