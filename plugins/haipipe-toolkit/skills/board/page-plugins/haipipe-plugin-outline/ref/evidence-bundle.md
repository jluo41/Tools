---
name: evidence-bundle
description: >-
  The derived, point-addressed view that joins a frozen Outline Point to its
  sentence scaffold, Probe cards, citations, proof, and Display units. It is a
  view, not another evidence folder: source material remains owned by its
  plugin and the bundle is recomputed from the current page state.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
---

# Evidence Bundle · one Point, all of its support

An Evidence Bundle answers one question:

> What does this Outline Point have, and what does it still need, before its
> sentence can be accepted?

The stable join key is the frozen Outline address:

```text
C<n>.P<n>.B<n>
```

The bundle never copies the material it displays. It joins live references:

```text
Point C3.P1.B4
  ├─ Sentence scaffold(s)  realizes: C3.P1.B4
  ├─ Probe card(s)         serves: C3.P1.B4
  ├─ Citation key(s)       named by the Point or its sentence
  ├─ Proof                 held by a Probe card's proof/
  └─ Display unit(s)       serves: C3.P1.B4
```

## 🧭 Ownership

```text
OUTLINE    declares the Point and its obligations
DRAFT      writes the sentence scaffold and visible holes
PROBE      creates value cards and writes their `serves:` backlink
EVIDENCE   lands answers, proof, citations, and Display intake
REVISE     writes final sentences and chooses/builds the Display
CHECK      judges the built result and human acceptance
```

`serves:` always points backward from material to the frozen Point. The
Outline is never edited merely because a card or unit was created.

## 📦 Derived shape

A renderer may expose a bundle as a compact card or side panel. Its fields are
logical, not a new storage schema:

```yaml
point: C3.P1.B4
sentences: [C3.P1.S1, C3.P1.S2]
obligations:
  value: 1
  citation: 1
  display: 1
resources:
  probes: [PP03]
  citations: [Deyo2015]
  displays: [Display2]
feedback:
  - PP03: read
  - Display2: accepted
status: evidence-ready | needs-probe | needs-intake | needs-citation | needs-revision | accepted
```

The `sentences` list is optional while DRAFT is still making the scaffold.
The resource lists are computed from the page's folders and sentence links;
they are never hand-maintained in a second manifest.

## ✅ Status rule

`feedback` is a derived review signal, not a fourth storage plugin. It points
to the owner-held decision (`state: read`, `accepted: ✅`, `verified`, or an
explicit rejection/defer) so REVISE and CHECK can see what a person said
without copying that decision into the bundle.

The bundle is `evidence-ready` only when every required obligation has a
landed source:

- a value has an answered, non-stale Probe card with `proof/` (or an explicit
  `why_empty`);
- a citation resolves to the page's Bibex entry;
- a Display obligation has frozen `intake/` and a named renderer.

`needs-revision` means the evidence exists but the sentence or Display still
has work. `accepted` additionally requires the human gates owned by the Probe,
Bibex, Display, and Page contracts. A folder count alone is never a pass.

## 🚫 Boundary

Do not create `<page>/evidence/` merely to hold this view. A copied bundle
would become stale as soon as a Probe answer, Bibex verification, or Display
acceptance changed. If a human makes a selection, persist only that selection
at the owning unit (`selected:` / `rejected:`); derive the rest again.
