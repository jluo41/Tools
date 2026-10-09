s01 · The toolkit map
=====================

**Topic:** Every part of `plugins/haipipe-toolkit` (the three skill layers by family, each server, the agents, the MCP server) with its size, and the Job of b01 that owns its design questions. It is the Block's index: when a part has no owning Job, the map shows it in red. Counted from disk on every rebuild (261009).

**Feeds:** `reports/` q01_blueprints_organized


Files
-----

```text
s01-toolkit-map/
├── s01-toolkit-map.md            this face
├── build_s01_toolkit_map.py      the builder: reads the folders, draws a lines-only table (../../_build/mapdraw.py)
├── s01-toolkit-map.excalidraw    the drawing; a person's marks are kept on rebuild
└── s01-toolkit-map.png           its preview
```

Rebuild: `python build_s01_toolkit_map.py`, then haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s01-D01 · <what was decided> (<who> <date>))


Open
----

1. The agents (19) and the MCP server codex-image2 have no owning Job: give agents to their theme's Job, or a Job of their own?
2. 1_base/project sits under j03 (a Project from root to Run) and the other 1_base families under j02: keep that split?

(write here, or mark the drawing in red)
