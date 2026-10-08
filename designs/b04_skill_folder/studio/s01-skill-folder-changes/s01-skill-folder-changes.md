b04 s01 · Skill folder changes
==============================

**Topic:** what q02 (path fix) and q03 (labeling merge) changed in the toolkit, drawn as a
results scratch: the folders before and after, who moved what, the kinds of broken path and
their fix, the checks, and the open choices per question.

**Source:** every fact is read when the builder runs. "Before" is `git ls-tree` of Tools HEAD;
"now" is the disk (layers, families and their SKILL.md counts, server folders); the check lines
are the Checks sections of `../../reports/q02_path_fix/` and `../../reports/q03_merge_subjective_label/`;
the question rows come from `../../board.md`.

**Feeds:** `reports/` q02_path_fix · q03_merge_subjective_label (and q01_skill_layers' choices).


Files
-----

```text
s01-skill-folder-changes/
├── s01-skill-folder-changes.md          this notes file
├── build_s01_skill_folder_changes.py    the builder; a person's marks are kept on rebuild
├── s01-skill-folder-changes.excalidraw  the drawing
└── s01-skill-folder-changes.png         its preview
```

Rebuild: `python build_s01_skill_folder_changes.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s01-skill-folder-changes.excalidraw s01-skill-folder-changes.png`.
It writes through b03's `canvas.write` (snapshot in b03's `_build/`), as b02's s01 does.


Other topics
------------

- s02-skill-layers: q01's layers, how servers pair with them, and its three open choices.
- s03-path-lookup: how code finds a skill now, and what the next move must fix again.
- s04-theme-shape: whether every theme folder has the same shape.
- The work theme's skills are asked in b17 (`../../../b17_theme_work/studio/s02-work-skills/`).

Rebuild every drawing: `../_build/make.sh`.
