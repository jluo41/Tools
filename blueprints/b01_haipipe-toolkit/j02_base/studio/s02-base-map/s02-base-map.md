b02 s02 · Base map
==================

**Topic:** Q01, who calls each base family: base family x caller (each theme, each other base
family, 0_utils, servers, other plugins), theme x theme (should be empty), base skills named by
only one theme, and base skills nobody outside their family names.

**Source:** read from disk every build by `callmap.py`, an index of which files name which skill
(`name`, /name, "name", skill: name, or a whole hyphenated name; history left out). Drawn with
b04's helpers through b03's canvas writer, so marks survive a rebuild.

**Feeds:** `../../reports/q01_base_map/` (answer drafted), and Q03's candidates.


Files
-----

```text
s02-base-map/
├── s02-base-map.md            this notes file
├── callmap.py                 the index: who names which skill
├── build_s02_base_map.py      the builder
├── s02-base-map.excalidraw    the drawing; marks are kept on rebuild
└── s02-base-map.png           preview
```

Rebuild: `python build_s02_base_map.py`, or every b02 drawing with `../_build/make.sh`.
