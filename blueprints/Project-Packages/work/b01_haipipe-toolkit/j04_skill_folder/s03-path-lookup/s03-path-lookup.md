b04 s03 · Path lookup
===================

**Stage:** explore

**For:** a deck, and how code finds a skill by name, not by folder depth, for the people who write the toolkit skills

**Delivery type:** code

**Topic:** how code finds a skill since q02 (by name, not by depth), and what the next move would still have to fix.

**Source:** counted from disk every build: lookups in use, literal layer paths in code and Markdown, Pages with an old-form structure-source, exported delivery scripts, moved paths git does not know yet, the venue submodule's name and path. Concerns and open questions are red text; JL's choices are pink notes.
Drawn with `../_build/sketch.py` through b03's canvas writer, so marks survive a rebuild.

**Feeds:** `../reports/q02_path_fix/`.


Files
-----

```text
s03-path-lookup/
├── s03-path-lookup.md            this notes file
├── build_s03_path_lookup.py   the builder
├── s03-path-lookup.excalidraw    the drawing; marks are kept on rebuild
└── s03-path-lookup.png           preview
```

Rebuild: `python build_s03_path_lookup.py`, or every drawing with `../_build/make.sh`.


Open
----

1. Agree its **For:** line and **Delivery type:** (code), proposed by the agent 261030?
