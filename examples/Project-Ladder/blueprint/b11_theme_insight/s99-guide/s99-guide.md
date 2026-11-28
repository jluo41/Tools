s99 · Theme Guide: Insight
=======================
view: overview

**Stage:** explore

**For:** a 📖 Guide section on the Block focus page, right after 🎨 Studio in the section menu, for anyone opening an insight Block

**Delivery type:** ui

**Covers:** where Guide sits in the menu; what it shows at Block, Job and Task level; where its content comes from on disk

**Excluded:** the Jobs section's rows and Main (s11-insight-job-preview)

**Why:** what should a person read on an insight Block's page to understand how its work is done?

**Topic:** The Insight theme guide explains how its three Block kinds cooperate and how to read their work. It references [Theme Guide](../../b17_theme_work/s78-studio-type-theme-guide/s78-studio-type-theme-guide.md). The s99 directory, sources, proposals and editable drawings stay in place. Band classification and Studio Type are separate; automatic explicit type binding depends on the shared reader.

**Feeds:** none


Files
-----

```text
s99-guide/
├── s99-guide.md                       this face
└── delivery/ui/
    ├── insight-guide-view.html        the preview: 📖 Guide after 🎨 Studio, four Views on top, left tabs, content right
    ├── insight-guide-view-data.py     reads guide.yaml, method.md, the method cards, papers.md, the two drawings
    ├── insight-guide-view-data.js     its output (regenerate, never edit)
    └── img/                           each RoadMap frame and the methods drawing, rendered by render_png.py
```

Regenerate (from the SPACE root): `uv run --with pyyaml --with pillow python examples/Project-Ladder/blueprint/b11_theme_insight/s99-guide/delivery/ui/insight-guide-view-data.py > examples/Project-Ladder/blueprint/b11_theme_insight/s99-guide/delivery/ui/insight-guide-view-data.js`.

Sources: `servers/workbench-insight/guide/guide.yaml` (description, skills, `levels:`), `guide/method.md` (the six steps),
`guide/methods/{answer,read}/` and `hai-report/ref/asking-methods/` (the cards), `related/papers.md`,
`studio/insight-workbench-design.excalidraw` (RoadMap, one left tab per frame) and `guide/methods.excalidraw`.
The old s31 Insight Guide (Block · Job · Task folds per View) is in git at `HEAD:…/s31-insight-guide/`.


Decided
-------

(none yet: a decision is one line, s99-D01 · <what was decided> (<who> <date>))


Open
----

1. Description's Block · Job · Task tables come from `guide.yaml` `levels:`, which still names the six old Spaces (Idea Studio, Audience Report, Work Details); rewrite them as the focus page's sections (Report, 💼 Jobs, 🎨 Studio …)?
2. `method.md` still says Scope, Question Book and Insight Spaces in its "where" column; same rewrite?
3. Method shows the six steps as left tabs; or Block · Job · Task tabs, as the old s31 cut it?
4. On a Job or Task page, does 📖 Guide open on that level's tab, or is the Guide only on the Block page?
5. RoadMap shows one frame per tab; is the Studio drawing enough, or does Guide need its own drawing per level?

(write here, or mark the drawing in red)
