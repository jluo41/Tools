s05 · Studio gallery: one real sNN per kind
===========================================

**Stage:** explore

**Tags:** Studio

**For:** a deck, and a gallery page in the haipipe-studio skill (`ref/gallery.md`, counted by `scripts/gallery_scan.py`): one real sNN per kind, by level and Theme, for anyone starting a new sNN.

**Delivery type:** skill

**Covers:** where the sNN sit today (level, Theme, SPACE); the kinds of sNN at each level and what each hands over; one real example each.

**Excluded:** what an sNN is and its rules ([b35-s01:studio @ studio_skill](../s01-studio-skill/s01-studio-skill.md)); its page and card ([b35-s02:studio @ studio_pages](../s02-studio-pages/s02-studio-pages.md)); the deliveries ([b35-s04:studio @ delivery_gallery](../s04-delivery-gallery/s04-delivery-gallery.md)).

**Topic:** one real sNN of each kind, to copy from. JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery of the studios, as the new sNN". 638 sNN sit in 6 SPACEs (scan of 261030), and a new one starts from nothing. Earlier JL called s01's scenarios "more like the galleries, ... like different types of the sNN in different settings"; that catalogue, sketch F1 in b35-s01, moved here.

**Feeds:** haipipe-studio `ref/gallery.md`.


Files
-----

```text
s05-studio-gallery/
├── s05-studio-gallery.md                 this face
├── build_s05_studio_gallery.py           its drawing: the five parts, the Design read from the scan
├── s05-studio-gallery.excalidraw, .png
└── delivery/                             deck/ (its slides), skill/gallery.md (written by gallery_scan.py), render.yaml
```


Decided
-------

s05-D01 · The studio gallery is its own sNN, beside the delivery gallery (s04); b35-s01's sketch F1, each kind of sNN by level and Theme, moved here (JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery of the studios, as the new sNN").
s05-D02 · The counts are read from disk by `gallery_scan.py` on every rebuild, never typed.
s05-D03 · The gallery's examples are the newest of each kind from the scan, never one of the two galleries, and one that names its delivery comes first; `gallery_scan.py --write` writes `delivery/skill/gallery.md` on every rebuild of the drawing, and `render_delivery.py` renders it into haipipe-studio `ref/gallery.md`. Tools is a public repository, so an sNN from another SPACE shows only its path, never its face's words (JL 261030: "go ahead and do it", agreeing to take the newest real one of each kind).
s05-D04 · No sNN sits in a `studio/` folder any more, so the gallery shows each where it sits, beside its Jobs or Tasks (JL 261031, b35 r02: "We will not have the studio anymore").


Open
----

1. Are these the kinds, and is each kind on its right level?
2. Should a gallery card show the example's drawing, or only its name and delivery?

(write here, or mark the drawing in red)

Delivery preview
----------------

**Target delivery:** A searchable Studio gallery with main Draws, scope, and delivery links.

**Reader:** People and agents starting a similar design.

**State:** review prototype; not accepted or released.

- [Open delivery](delivery/web/index.html)
- [Main delivery Draw](delivery-design.excalidraw)
- [Draw preview](delivery-design.png)
- [Explanation slides](delivery/deck/index.html)
- [Delivery contract](delivery/web/contract.html)

The source is `../scripts/delivery-specs.json`; `../scripts/build_delivery_previews.py` generates the review package. Earlier drawings remain unchanged.
