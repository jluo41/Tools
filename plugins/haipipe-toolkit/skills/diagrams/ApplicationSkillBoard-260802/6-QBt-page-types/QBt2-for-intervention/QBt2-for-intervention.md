# Intervention: map settled insights into components and variants
state: 🟡 PARTIAL · contract shipped · fresh-context design passed · open: materialized runtime map
page-type: intervention
owner: JL

## Opening
How does Application turn settled Insight Pages into a message, dashboard, checklist, or report without rerunning DIKW?

Intervention selects and translates K/W rows into mechanisms, principles, strategy, components, variants, and safety rails. It is Application's composition Page and uses a distinct name because Board already owns generic Design.

**Covered here**: the global delivery architecture and Artifact handoffs.

**Covered elsewhere**: Brief owns audience and promise; Artifact owns concrete content and acceptance.

## Writing Style
Write every design move as an action tied to an Insight Page. Distinguish invariant, experimental variable, and safety rail explicitly.

## Diagram
**The transformation chain**: no design move floats free of knowledge or delivery.

```text
Insight K/W ─▶ principle ─▶ component ─▶ Artifact Page
```

## Content

### 1 · Insight selection
**Selection state**: adopted and declined inputs are both inspectable.
```text
Insight Page | adopted/declined | reason | boundary
```
Adopted and declined Insight Pages remain visible with one-line reasons.

### 2 · Theory of change
**Mechanism chain**: each action link names its knowledge warrant.
```text
K/W row → mechanism → audience action → outcome
```
Every audience-action link names the K/W row that warrants it.

### 3 · Intervention principles
**Principle form**: knowledge becomes an executable design move.
```text
because <insight>, do <move>, within <rail>
```
Principles are executable design moves, not claims paraphrased as advice.

### 4 · Strategy and arc
**Composition choice**: venue and behavior determine the organizing form.
```text
framing | sequence | interaction architecture | narrative
```
The venue decides whether this is framing, sequence, interaction architecture, or narrative.

### 5 · Component map
**Unit map**: one row becomes one independently approvable Artifact.
```text
unit | audience job | content move | constraint | rail
```
One row exists per independently approvable Artifact unit, with audience job, content move, constraint, and rail.

### 6 · Variants and arms
**Experiment boundary**: invariant content is separated from the tested variable.
```text
invariant core + one variable → arm A / arm B
```
The Page separates what stays invariant from what deployment is allowed to test.

### 7 · Safety and compliance
**Safety rail**: prohibited and unsupported moves are visible before authoring.
```text
risk | trigger | prohibited move | required safeguard
```
Unsupported, unsafe, or prohibited moves are explicit before copy is authored.

### 8 · Artifact handoff
**Component packet**: each unit receives only its own bounded design inputs.
```text
component row + principle refs + venue constraints + rails
```
Every unit receives one current, versioned handoff row.

## Aims

### A5 · Component map
- A5.1 · The independent accept/reject test determines Artifact grain.
  **Done when:** a runtime map has no row combining separately reviewable units.

### A8 · Artifact handoff
- A8.1 · A fresh Artifact agent executes one row without inventing strategy.
  **Done when:** forward validation preserves trace, invariant, variant, and rail.

## States

### A5 · Component map
- ⬜ A5.1 · No runtime component map has been inspected yet.

### A8 · Artifact handoff
- ✅ A8.1 · Fresh-context validation on 260817 mapped Insight A/B into timing and non-blaming principles, one core SMS component, one conditional renal component, and explicit safety rails without inventing strategy.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-intervention/SKILL.md`
  The Page Type contract this specimen exercises.
- `../../../../application/haipipe-application/fn/intervention.md`
  The Application door procedure.

## Log
260817 · Fresh Application agent used the independent accept/reject test, kept the core SMS as one Artifact, and withheld the renal-specific component until a new Wisdom handoff exists.
260817 · Named Intervention rather than Design to avoid collision with Board's candidate-selection Page Type.
