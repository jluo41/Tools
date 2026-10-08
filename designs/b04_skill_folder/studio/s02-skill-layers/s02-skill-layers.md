b04 s02 · Skill layers
====================

**Topic:** what each layer (0_utils, 1_base, 2_theme) holds, each workbench skill beside its server, and q01's three open choices.

**Source:** read from disk every build: each layer's families and skills, the workbench-* skills and their server folders, folder names that occur twice. Concerns and open questions are red text; JL's choices are pink notes.
Drawn with `../_build/sketch.py` through b03's canvas writer, so marks survive a rebuild.

**Feeds:** `../../reports/q01_skill_layers/`.


Files
-----

```text
s02-skill-layers/
├── s02-skill-layers.md            this notes file
├── build_s02_skill_layers.py   the builder
├── s02-skill-layers.excalidraw    the drawing; marks are kept on rebuild
└── s02-skill-layers.png           preview
```

Rebuild: `python build_s02_skill_layers.py`, or every drawing with `../_build/make.sh`.
