s01 · The two modes
===================

**Topic:** How `plugins/inlab-human` fits together: the reader study (bundle, blind then assisted review, report), the clinician console (its routers and the agent drawer), the endpoint-predict tool both use, and the de-identification boundary in front of them, each with the Job of b03 that owns it. Read from code and docs only; no case data (261009).

**Feeds:** `reports/` q01_ownership


Files
-----

```text
s01-two-modes-map/
├── s01-two-modes-map.md            this face
├── build_s01_two_modes_map.py      the builder: reads the folders, draws a lines-only table (../../_build/mapdraw.py)
├── s01-two-modes-map.excalidraw    the drawing; a person's marks are kept on rebuild
└── s01-two-modes-map.png           its preview
```

Rebuild: `python build_s01_two_modes_map.py`, then haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s01-D01 · <what was decided> (<who> <date>))


Open
----

1. The plugin has no tests (Q02): which part gets the first suite?
2. The boundary is stated, not checked: where does the check run (j05_data_boundary)?

(write here, or mark the drawing in red)
