b02 s02 · Base map
==================
view: findings

**Stage:** explore

**For:** a deck, and a table of who calls each base skill family, for the people who write the toolkit skills

**Delivery type:** data

**Topic:** Q01, who calls each base family: base family x caller (each theme, each other base
family, 0_utils, servers, other plugins), theme x theme (should be empty), base skills named by
only one theme, and base skills nobody outside their family names.

**Source:** read from disk every build by `callmap.py`, an index of which files name which skill
(`name`, /name, "name", skill: name, or a whole hyphenated name; history left out). Drawn with
b04's helpers through b03's canvas writer, so marks survive a rebuild.

**Feeds:** `../Q01 (answer drafted), and Q03's candidates.


Q01 · Answer
------------

**Question:** What does each base family give the themes?

**Answer (open):** A first answer, drawn from disk in [s02 base map](../../s02-base-map/s02-base-map.excalidraw) (counts are files that name a skill, not proven calls). Two base families are called by every theme, two by most, and four by only one or two themes. One theme, discovery, is named by six of the other seven themes, so it behaves like base.

**Page:** [q01_base_map.md](q01_base_map/q01_base_map.md): the full answer, its evidence and limits (moved from reports/)


Q03 · Answer
------------

**Question:** What sits in base but is not base?

**Answer (open):** not written yet.


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


Open
----

1. Agree its **For:** line and **Delivery type:** (data), proposed by the agent 261030?
