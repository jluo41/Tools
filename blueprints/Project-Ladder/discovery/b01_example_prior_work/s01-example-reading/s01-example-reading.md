s01 · How the example papers are read
=====================================

**Stage:** shaping

**For:** a deck on how one placeholder paper becomes a cited Result, for whoever reads the discovery theme's example pages

**Delivery type:** skill

**Covers:** a paper admitted as one Run, its Card, facts and one Bib entry, the Task's Evidence Bib, and its hand-over to the Paper-Example

**Excluded:** how the paper prints the citation (Paper-Example's `j03_evidence_cite`); finding real papers (haipipe-discovery-search)

**Topic:** A placeholder topic: the path from a paper to the Bib a paper cites, and where a person checks a citation. Every paper here is made up.

**Feeds:** `reports/q01-earlier-effect.md`

```yaml
frames:
- title: 📚 one paper, one Run, one Bib entry
  intro: a placeholder paper read into a Result, then handed over
  boxes:
  - {id: p, at: [0, 0], title: 📄 a paper, why: admitted as one Run, tree: [rNN_<author><year>_<slug>, its ticket]}
  - {id: r, at: [1, 0], title: 🧾 its Result, why: what the Run returns, tree: [Card with its readout, facts, one-entry Bib]}
  - {id: b, at: [2, 0], title: 📖 the Evidence Bib, why: the Task's Results joined, tree: [draft/evidence/bibex/, handed over in delivery/]}
  - {id: c, at: [1, 1], title: "❓ a person checks", why: a NEEDS line waits for you, tree: [title and year, against its source]}
  arrows:
  - {from: p, to: r, label: read}
  - {from: r, to: b, label: built}
  - {from: r, to: c, label: "? check", dashed: true}
```


Files
-----

```text
s01-example-reading/
├── s01-example-reading.md          this face
├── s01-example-reading.excalidraw  its drawing (topic_map.py), with its .png preview
└── s01-example-reading.mindmap.md  its mind map
```


Decided
-------

s01-D01 · A paper's Card says in its verification line when a person must check it (placeholder decision, 261108; record j01_policy_effect_inquiry/t01_policy_prior_work/runs/r05_collect_example_check_rules)


Open
----

(none here: which paper a person checks first is s03's, at j01_policy_effect_inquiry/t01_policy_prior_work)
