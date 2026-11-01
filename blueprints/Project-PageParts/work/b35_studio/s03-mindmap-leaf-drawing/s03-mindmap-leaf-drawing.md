s03 · One leaf, one drawing
===========================

**Stage:** explore

**Tags:** Mind map

**For:** a deck, and haipipe-mindmap (SKILL.md, `mmsketch.py`, `mmmap.py`): one drawing per leaf.

**Delivery type:** skill

**Links:** [b35-s01:studio @ studio_skill](../s01-studio-skill/s01-studio-skill.md)

**Topic:** how a topic's mind map, slides and drawings hang together. JL 261029, after three tries: "一个 leaf 就一个 draw 然后里面可以有几个 slides". Built in haipipe-mindmap 0.8.0 (`scripts/mmsketch.py`); this topic keeps what is settled and what is still loose.

**Feeds:** haipipe-mindmap SKILL.md, `scripts/mmsketch.py`, `scripts/mmmap.py`.


Files
-----

```text
s03-mindmap-leaf-drawing/
├── s03-mindmap-leaf-drawing.md            this face
├── s03-mindmap-leaf-drawing.ideas.md      the open ideas, one per slide
├── s03-mindmap-leaf-drawing.slides.json   style sketch-notes, each slide's content and leaf
├── slides/idea-NN-<slug>.png          the pictures
├── map/<leaf id>-<words>.excalidraw   one drawing per leaf, holding its slides
└── s03-mindmap-leaf-drawing.mindmap.md    the mind map
```


Decided
-------

s03-D01 · A topic's mind map starts with "The total workflow"; each first-level branch is a section, and each leaf under it has one drawing, `map/<leaf id>-<words>.excalidraw`, holding that leaf's slides (a slide names its leaf in `.slides.json`, `"leaf": "n29"`); a ✎ link on the leaf opens it in the page's pop-out (JL 261029: "the first node should be a section"; "we should have a section named the total workflow"; "一个 leaf 就一个 draw 然后里面可以有几个 slides"). It replaces b35-s01's D09, which said a section holds the slides.
s03-D02 · The map wraps to the page's width (JL 261029: "the mind map is too wide").


Open
----

1. Does every leaf get a drawing when the map is sketched, or only a leaf with a slide?
2. Can one slide sit on two leaves?
3. Does a red mark on a leaf's drawing start a new pass?

(write here, or mark the drawing in red)

Delivery preview
----------------

**Target delivery:** A mind map authoring guide with node rules, safe update rules, and a worked map.

**Reader:** Agents authoring and maintaining shared structure maps.

**State:** review prototype; not accepted or released.

- [Open delivery](delivery/web/index.html)
- [Main delivery Draw](delivery-design.excalidraw)
- [Draw preview](delivery-design.png)
- [Explanation slides](delivery/deck/index.html)
- [Delivery contract](delivery/web/contract.html)

The source is `../scripts/delivery-specs.json`; `../scripts/build_delivery_previews.py` generates the review package. Earlier drawings remain unchanged.
