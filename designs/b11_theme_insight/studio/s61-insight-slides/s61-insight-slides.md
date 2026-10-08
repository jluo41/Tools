s61 · Insight slides
====================

**Topic:** a deck that argues for the insight theme on the ladder, the insight side of b12's
s61-design-slides and in its shape (261007: "make it like the s61 first and in the draw, you show the logic
flow, and then make it as the ppt slide"; b12's "is much better"). The deck's logic is drawn first; the
slides follow it. One idea runs through it: an insight Job changes one thing at a time, so when an answer
changes we can say why; and a claim leaves the Board only once it has earned it.

**Source:** the content of every slide is `slides.py` (title, bullets, picture, the drawings it comes from,
the reason the next slide follows, speaker notes), drawn from this Block's s00, s03, s11, s12, s13, s31 and
the Insight Guide's `method.md` (the published evidence). The slide layout is b12's `slide_kit.py`, loaded
by path, so the two theme decks lay out the same way and the storyboard and the deck cannot drift apart.

**Feeds:** `../../reports/` q01_insight_ladder · q02_partitions_pooling · q04_level_delivery.


Files
-----

```text
s61-insight-slides/
├── s61-insight-slides.md            this notes file
├── slides.py                        the deck's content: 19 slides, in order
├── build_s61_insight_slides.py      draws s61-insight-slides.excalidraw; marks are kept on rebuild
├── build_deck.py                    writes ../../delivery/insight-slides/ (generated; never edit it)
├── s61-insight-slides.excalidraw    the drawing: logic flow · storyboard · open
└── s61-insight-slides.png           its preview
```

The deck, written by `build_deck.py` in the html-to-svg skill's style (white, Times New Roman, no emoji):

```text
../../delivery/insight-slides/
├── insight-slides.pptx              native PowerPoint shapes and text boxes, speaker notes on each slide
├── insight-slides.pdf               the same slides, vector
└── svg/NN-<slug>.svg                one 1280 × 720 SVG per slide
```

Rebuild: `python build_s61_insight_slides.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s61-insight-slides.excalidraw s61-insight-slides.png 0.4`;
and `python build_deck.py` (needs python-pptx, cairosvg and pypdf; on macOS, Homebrew's cairo).


The deck, slide by slide
------------------------

```text
why    01 cover          The insight theme on the ladder
       02 evidence       Analysis is cheap now; a reason to trust it is not          measured failures
       03 why            Today we cannot say why an answer changed                    today → on the ladder
what   04 two-clocks     Two things change, on two clocks: the questions and the data
       05 one-clock      One change per Job, so every changed answer has one cause    the Map
       06 ladder         Four levels: Board, Job, Task, Run
       07 dikw           Each DIKW level may say more, and has one thing it may not say
how    08 question       A question is planned, agreed and signed before any data is read
       09 one-job        Inside one Job: power first, then run, check, compare and propose
       10 guardrails     Four guardrails keep the answers honest
learn  11 compare        Every answer gets a status against the previous Job
       12 example        One question, four Jobs: what a naive pipeline would have shipped
       13 learning-loop  Comparing Jobs is how the questions grow
       14 across-jobs    The Board reads across Jobs: a second D · I · K · W
now    15 handoff        Only signed Wisdom leaves, and it steers design             the crossing b12 draws
       16 workbench      One workbench: the same six Spaces at every level
       17 limits         What it guarantees, and what it does not
       18 bet            The design is itself a bet, and we can measure it
       19 status         Where it stands
```


Open
----

1. Who is it for: the people who run insight Boards, or a wider room? It decides the depth.
2. Slide 12's example is illustrative; swap in a real Board's four Jobs once one exists.
3. Slide 19 dates itself (2026-10-07): rebuild the deck before each showing.
4. One slide kit for both decks: `slide_kit.py` lives in b12's s61; move it to a shared place?

(write here, or mark the drawing in red)
