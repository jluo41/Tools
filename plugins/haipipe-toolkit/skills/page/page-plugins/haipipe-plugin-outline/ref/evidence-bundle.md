---
name: evidence-bundle
description: >-
  The derived, point-addressed view that joins a frozen Outline Point to its
  sentence scaffold and typed VALUE/CITE/DISPLAY Results. It is a
  view, not another evidence folder: source material remains owned by its
  plugin and the bundle is recomputed from the current page state.
metadata:
  version: "0.3.1"
  last_updated: "2026-09-04"
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
  ├─ Local Input           one frozen envelope assembled from valid supports
  ├─ Local RE(s)           one Page Evidence Run lineage per made item
  ├─ Local Result(s)       VALUE/CITE/DISPLAY, one current Result per item
  ├─ Evidence Card(s)      read-only projection of those current Results
  └─ Evidence Label(s)     zero-to-many inline VALUE/DISPLAY/CITE anchors
```

## 🧭 Ownership

```text
CONTEXT    freezes the governing Page context
OUTLINE    declares the Point, typed item expectation, and SURVEY Run graph
EVIDENCE   validates supports, freezes input, lands one local Result, and EMBEDs
CONTENT    realizes the folded plan in prose and delivery artifacts
CHECK      judges the whole built Page and human acceptance
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
  evidence_runs: [re-value-01_adjusted-effect]
  local_runs: [b03j01t02r01]
  cards: [evidence-card:E01-VALUE-adjusted-effect]
  labels: ["$V_adjusted_fx$", "\\figure{D_effect_forest}", "\\table{D_regression_main}", "\\cite{C_prior_work}"]
feedback:
  - E03-CITE-prior-work: Verified ✅ on the authored item row
  - E04-DISPLAY-effect-forest: accepted
item_states:
  E01-VALUE-adjusted-effect: ready
summary: complete | incomplete
```

The `sentences` list is optional while CONTENT is still making the scaffold.
The resource lists are computed from the page's folders and sentence links;
they are never hand-maintained in a second manifest.

## ✅ Readiness rule

The bundle has no independent status vocabulary. Every Evidence Item keeps the
derived ladder from `item-table.md` (`specified · planned · ready · folded ·
accepted`, plus its exception states). `summary` is only a live roll-up:
`complete` when every obligation is satisfied and every required human gate is
accepted; otherwise `incomplete`. It is never persisted as another authority.

`feedback` is a derived review signal, not a fourth storage plugin. It points
to the owner-held decision (`accepted: ✅`, CITE-item `Verified`, or an explicit
rejection/defer) so CONTENT and CHECK can see what a person said
without copying that decision into the bundle.

An item's evidence obligation is ready only when it has a ready local Result:

- every declared Supporting Result passes its owning Run gate;
- one frozen Local Input records those sources and hashes;
- exactly one current typed Page `RE` lineage emits an accepted VALUE, CITE, or
  DISPLAY Result; its read-only Card and zero-to-many Labels are derived from
  that Result. DISPLAY uses `D_` for tables, figures, and algorithm blocks;
  conceptual diagrams and AI illustrations use the ordinary figure label.
- a CITE item's authored `Verified` gate is signed before that Result is ready.

Sentence or Display work that remains belongs to CONTENT or CHECK, not to a new
bundle status. Final acceptance additionally requires the human gates owned by
the Evidence worker, DISPLAY Result, and Page contracts. A folder count alone is never
a pass.

## 🚫 Boundary

Do not create `<page>/evidence/` merely to hold this view. A copied bundle
would become stale as soon as a Result, citation verification, or DISPLAY
acceptance changed. If a human makes a selection, persist only that selection
at the owning unit (`selected:` / `rejected:`); derive the rest again.
