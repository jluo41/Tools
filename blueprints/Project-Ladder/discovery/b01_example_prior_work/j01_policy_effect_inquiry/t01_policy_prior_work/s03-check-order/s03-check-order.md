s03 · Which paper to check first
================================

**Stage:** explore

**For:** a deck on the order a person checks the Task's citations, for whoever reads the discovery theme's Task page

**Delivery type:** skill

**Covers:** the three placeholder papers, which one waits for a check, and the order of the checks

**Excluded:** how a paper is read (s01); the subgroup papers (`j02_subgroup_effect_inquiry`)

**Topic:** A placeholder topic: one paper's citation waits for a person; which comes first. Every paper here is made up.

**Feeds:** `reports/q02-setting.md`

```yaml
frames:
- title: 🙋 one citation waits for you
  intro: two papers read from their abstracts, one from its metadata only
  boxes:
  - {id: a, at: [0, 0], title: 📄 r01 and r02, why: read from their abstracts, tree: [cite key agrees, entry copied]}
  - {id: b, at: [1, 0], title: "❓ r03", why: metadata only, tree: [its venue unread, NEEDS a person]}
  - {id: c, at: [2, 0], title: ✅ then close, why: every citation checked, tree: [the Task closes, the Bib is final]}
  arrows:
  - {from: a, to: b, label: next}
  - {from: b, to: c, label: "? after the check", dashed: true}
```


Files
-----

```text
s03-check-order/
├── s03-check-order.md          this face
├── s03-check-order.excalidraw  its drawing (topic_map.py), with its .png preview
└── s03-check-order.mindmap.md  its mind map
```


Decided
-------

(none yet)


Open
----

1. Which paper does a person check first? (asked on runs/r04_collect_example_check_order)

(write here, or mark the drawing in red)
