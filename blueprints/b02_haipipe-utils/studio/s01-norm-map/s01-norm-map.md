s01 · The normalizer map
========================

**Topic:** How `plugins/haipipe-utils` fits together, left to right: the contract (haipipe-norm), each member with its version and the banks it resolves against, the API lane that serves it, and the Job of b02 that owns it; describe-medication's DrugKey feeds describe-insulin. A bank this SPACE's ExternalStore does not hold is red, which today is every bank (261009).

**Feeds:** `reports/` q01_package_description


Files
-----

```text
s01-norm-map/
├── s01-norm-map.md            this face
├── build_s01_norm_map.py      the builder: reads the folders, draws a lines-only table (../../_build/mapdraw.py)
├── s01-norm-map.excalidraw    the drawing; a person's marks are kept on rebuild
└── s01-norm-map.png           its preview
```

Rebuild: `python build_s01_norm_map.py`, then haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s01-D01 · <what was decided> (<who> <date>))


Open
----

1. Every bank is absent from DrFirst-SPACE: where does each live (j07_banks)?
2. Each member still has 'its own resolver' for banks; does it move onto haipipe-norm's paths.py (j01_norm_contract)?

(write here, or mark the drawing in red)
