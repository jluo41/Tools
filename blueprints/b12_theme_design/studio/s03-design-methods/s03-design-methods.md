s03 · Design methods
====================

**Topic:** the design method, drawn: the methods drawing at the top of Guide › Method (requirements,
internal and external insights → Design → Exp; thirteen method cards), and the design unit (one
unit in five steps: see input, propose ideas, conduct, check each, check overall; one row per method).

**Source:** the two drawings and their scripts live here; the design workbench's Guide opens them
here (moved from the skill's `ref/` and `servers/workbench-design/studio/`, 261007). The method text
and the papers table live with the design theme's server:
`Tools/plugins/haipipe-toolkit/servers/workbench-design/` `guide/method.md` (cards in `guide/methods/`) ·
`related/papers.md` (PDFs in `related/papers/`).

**Feeds:** `../../reports/` q01_design_ladder · q02_design_workbench.


Files
-----

```text
s03-design-methods/
├── s03-design-methods.md            this notes file
├── s03-design-methods.excalidraw    the one drawing (JL 261007: "put both of them in one excalidraw"):
│                                    1 how we design (redrawn 261007 on the design unit: the reasoning kinds by
│                                    step, the five-step unit in the Revise and Learning loops, the three families
│                                    as ①'s choice, each card naming its registered methods M01-M05) · 2 the design
│                                    unit catalog; the plain catalog stays in parts/;
│                                    marks you add here are kept on rebuild
├── s03-design-methods.png           its preview
├── build_s03_design_methods.py      copies the three parts into the one drawing, each in its frame
├── parts/                           each part, drawn by its own script (Guide › Method reads 1 and 2 here)
│   ├── design-methods.excalidraw    1 · the methods canvas        ← methods_drawing.py
│   ├── design-unit-methods.excalidraw  2 · the design unit catalog  ← design_unit_drawing.py
│   ├── s03-design-unit.excalidraw   3 · the catalog, plain        ← build_s03_design_unit.py (marks kept)
│   └── *.png                        their previews
├── methods_drawing.py · design_unit_drawing.py · build_s03_design_unit.py
├── chat/                            the methods session (260929-261002): its brief and transcript
└── _archive/                        the three-step unit (261005); the 3 Oct methods canvas and its script
                                     (design-methods-261003, methods_drawing-261003.py), before the redraw
```

Rebuild a part, then the one drawing:
`python3 methods_drawing.py parts/design-methods.excalidraw <server>/related/papers.md` ·
`python3 design_unit_drawing.py` · `python3 build_s03_design_unit.py`, then
`python3 build_s03_design_methods.py` and
`python3 ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s03-design-methods.excalidraw s03-design-methods.png 0.5`.
The first two are author scripts: fold any canvas edit on a part into them first; a mark on the one
drawing stays there.

(write here, or mark the drawing in red)
