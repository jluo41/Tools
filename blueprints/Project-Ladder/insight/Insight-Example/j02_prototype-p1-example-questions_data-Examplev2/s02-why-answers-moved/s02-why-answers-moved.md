s02 · Why the answers moved from j01
====================================

**Stage:** explore

**For:** whoever reads j02's comparison: why four answers changed when only the data moved

**Delivery type:** display

**Covers:** the one clock that moved (data freeze 1 → 2), the answers it changed, and the proposal it led to

**Excluded:** the questions' map (s01); the next plan's own review (the Prototype)

**Topic:** j02 runs the same analysis plan on data freeze 2. Only the data moved, so each changed answer has that one cause: more rows narrowed the pooling interval (K01: UNDETERMINED → POOL), and the daily drift's interval now crosses zero (I02). The change led to one proposal for the next plan.

```yaml
frames:
- title: 🔀 One clock moved, four answers changed
  intro: j01 and j02 run plan 1; only the data freeze differs
  boxes:
  - {id: v, at: [0, 0], title: 🗄 data freeze 1 → 2, why: 600 → 960 rows, tree: [six more days, the first ten unchanged]}
  - {id: k, at: [1, 0], title: 🧪 K01 pooling, why: the interval narrowed, tree: [UNDETERMINED in j01, POOL in j02]}
  - {id: i, at: [1, 1], title: 📈 I02 drift, why: its interval now crosses zero, tree: [downward in j01, no clear drift in j02]}
  - {id: p, at: [2, 0], title: 📝 a proposal, why: for plan 2, tree: [gap-over-the-window, taken into p2]}
  arrows:
  - {from: v, to: k, label: narrows}
  - {from: v, to: i, label: widens}
  - {from: k, to: p, label: leads to}
```

**Feeds:** `reports/q01_gap-across-freezes`


Files
-----

```text
s02-why-answers-moved/
├── s02-why-answers-moved.md        this face
└── <drawings, builder>
```


Decided
-------

s02-D01 · a changed answer is explained by the one clock that moved, never by a second cause (261106)


Open
----

1. whether the drift should be its own question in plan 2, or only K02's rival

(write here, or mark the drawing in red)
