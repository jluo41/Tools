---
name: evidence-bundle
description: >-
  The derived, point-addressed view that joins a frozen Outline Point to its
  sentence scaffold, Probe cards, citations, proof, and Display units. It is a
  view, not another evidence folder: source material remains owned by its
  plugin and the bundle is recomputed from the current page state.
metadata:
  version: "0.2.1"
  last_updated: "2026-09-02"
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
  ├─ Evidence Item(s)      Target: C3.P1.B4
  ├─ Supporting Result(s) Execution/Discovery Run authorities
  ├─ PageX source(s)       exact file/Result + accepted authority
  ├─ Local Result(s)       VALUE/CITE/DISPLAY, one per made item
  └─ Probe card(s)         only when an external question crossing is needed
```

## 🧭 Ownership

```text
OUTLINE    declares the Point, typed item expectation, and SURVEY source graph
DRAFT      writes the sentence scaffold and visible holes
PROBE      governs any separate outbound question crossing
EVIDENCE   validates supports/PageX, freezes input, and lands one local Result
REVISE     improves realization without changing the evidence contract
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
  items: [E01-VALUE-adjusted-effect]
  supporting_runs: [b01j02t03r04]
  pagex_bindings: [other/page/results/r08/result.yaml]
  local_runs: [b03j01t02r01]
  probes: []
feedback:
  - PP03: read
  - Display2: accepted
item_states:
  E01-VALUE-adjusted-effect: ready
summary: complete | incomplete
```

The `sentences` list is optional while DRAFT is still making the scaffold.
The resource lists are computed from the page's folders and sentence links;
they are never hand-maintained in a second manifest.

## ✅ Readiness rule

The bundle has no independent status vocabulary. Every Evidence Item keeps the
derived ladder from `item-table.md` (`specified · planned · ready · folded ·
accepted`, plus its exception states). `summary` is only a live roll-up:
`complete` when every obligation is satisfied and every required human gate is
accepted; otherwise `incomplete`. It is never persisted as another authority.

`feedback` is a derived review signal, not a fourth storage plugin. It points
to the owner-held decision (`state: read`, `accepted: ✅`, `verified`, or an
explicit rejection/defer) so REVISE and CHECK can see what a person said
without copying that decision into the bundle.

An item's evidence obligation is ready only when it has a ready local Result:

- every declared Supporting Result passes its owning Run gate;
- every PageX binding resolves an exact source with accepted authority;
- one frozen Local Input records those sources and hashes;
- exactly one local Page Evidence Item Run emits an accepted VALUE, CITE, or
  DISPLAY Result.

Sentence or Display work that remains belongs to REVISE or CHECK, not to a new
bundle status. Final acceptance additionally requires the human gates owned by
the Evidence, Probe, Display, and Page contracts. A folder count alone is never
a pass.

## 🚫 Boundary

Do not create `<page>/evidence/` merely to hold this view. A copied bundle
would become stale as soon as a Probe answer, citation verification, or Display
acceptance changed. If a human makes a selection, persist only that selection
at the owning unit (`selected:` / `rejected:`); derive the rest again.
