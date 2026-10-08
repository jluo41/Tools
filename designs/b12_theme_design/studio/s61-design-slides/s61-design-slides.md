s61 · Design slides
===================

**Topic:** a high-level deck that explains the design theme on the ladder (JL 261007: "make it like the
s61 first and in the draw, you show the logic flow, and then make it as the ppt slide"), the design side
of b11's s61. The deck's logic is drawn first; the slides follow it. One idea runs through it: a design
Job changes one thing at a time, so when the designs change we can say why, and the Exp can teach the
method, not only the designs.

**Source:** the content of every slide is `slides.py` (title, bullets, picture, the drawings it comes
from, the reason the next slide follows, speaker notes), drawn from this Block's s00, s01, s03, s11, s12,
s13, s21 and `../../goal-design-workbench.md`. `slide_kit.py` lays a slide out once; the drawing and the
deck both draw with it, so the storyboard and the deck cannot drift apart.

**Feeds:** `../../reports/` q01_design_ladder · q02_design_workbench · q03_insight_steers_design.


Files
-----

```text
s61-design-slides/
├── s61-design-slides.md            this notes file
├── slides.py                       the deck's content: 11 slides, in order
├── slide_kit.py                    one slide's layout (title · bullets · flow, ladder, grid or cards)
├── build_s61_design_slides.py      draws s61-design-slides.excalidraw; marks are kept on rebuild
├── build_deck.py                   writes ../../delivery/design-slides/ (generated; never edit it)
├── s61-design-slides.excalidraw    the drawing: logic flow · storyboard · open
└── s61-design-slides.png           its preview
```

The deck, written by `build_deck.py` in the html-to-svg skill's style (white, Times New Roman, no emoji):

```text
../../delivery/design-slides/
├── design-slides.pptx              native PowerPoint shapes and text boxes, speaker notes on each slide
├── design-slides.pdf               the same slides, vector
└── svg/NN-<slug>.svg               one 1280 × 720 SVG per slide
```

Rebuild: `python build_s61_design_slides.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s61-design-slides.excalidraw s61-design-slides.png 0.4`;
and `python build_deck.py` (needs python-pptx, cairosvg and pypdf; on macOS, Homebrew's cairo).


What the drawing holds
----------------------

1. **logic flow**: one box per slide, top to bottom, its claim and the drawings it comes from; the words
   on each arrow say why the next slide follows; the five groups bracket them: why (the pain) · what (the
   idea and the ladder) · how (one Job, kept honest) · learn (the loops that improve it) · now (where you
   see it, where it stands).
2. **storyboard**: every slide at half size, drawn by the deck's own layout.
3. **open**: what is still to decide, in red.

The deck, slide by slide:

```text
01 cover           The design theme on the ladder
02 why             Today we cannot say why a design changed               today → on the ladder
03 method          A design method is a frozen recipe                     the five steps
04 ladder          Four levels: Block, Job, Task, Run                     the staircase
05 one-clock       One change per Job, so every difference has one cause  the Map: goals × methods
06 one-job         Inside one Job                                         set up → reason → make → rank → release
07 guardrails      Four guardrails keep the designs honest                fence · another agent · a person · frozen
08 learning-loop   The Exp teaches the method, not only the designs       release → Exp → score → new version
09 insight-steers  Insight steers design through one handoff              W-NN → inputs → Job → element
10 workbench       One workbench: the same six Spaces at every level      Space × level
11 status          Where it stands                                        done · in progress · open
```


Open
----

1. Who is it for: the people who run design Boards, or a wider room? It decides the depth.
2. One form for both decks: b11's s61 plans an HTML deck and a PDF; this one is a .pptx and a PDF.
3. Slide 11 dates itself (2026-10-07): rebuild the deck before each showing.
4. A slide showing one design as the reader sees it, once a real Job exists.

(write here, or mark the drawing in red)
