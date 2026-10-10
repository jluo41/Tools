b02 s01 · Base overview
=======================

**Topic:** the base layer at a glance: each family in `skills/1_base` with its door, its
sub-folders and skills, where its agents are, its tests and the skills with no CHANGELOG; the
concerns the inventory raises (red) and the four Questions, each with the drawing that answers it.

**Source:** read from disk every build (the skills tree, `../../board.md`); drawn with b04's
helpers (`../../../b04_skill_folder/studio/_build/sketch.py`) through b03's canvas writer, so
marks survive a rebuild.

**Feeds:** all four reports; it is the map the other topics start from.


Files
-----

```text
s01-base-overview/
├── s01-base-overview.md             this notes file
├── build_s01_base_overview.py       the builder
├── s01-base-overview.excalidraw     the drawing; marks are kept on rebuild
└── s01-base-overview.png            preview
```

Rebuild: `python build_s01_base_overview.py`, or every b02 drawing with `../_build/make.sh`.


The studio topics
-----------------

- s01-base-overview: this drawing, the map.
- s02-base-map (Q01): each base family x who calls it (themes, other base families, servers).
- s03-base-shape (Q02): one row per family: door, ref/, cli/ or scripts/, agents, tests, CHANGELOG.
- s04-not-base (Q03): each candidate that may not be base, with its proposed home.
- s05-workbench-skills (Q04): page's three workbench skills beside servers/workbench.
