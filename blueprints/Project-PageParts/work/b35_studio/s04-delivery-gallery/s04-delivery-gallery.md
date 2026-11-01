s04 · Delivery gallery: one real delivery per kind
==================================================

**Stage:** explore

**Tags:** Delivery

**For:** a deck, and a gallery page in the haipipe-delivery skill (`ref/gallery.md`, counted by haipipe-studio `scripts/gallery_scan.py`): one real delivery per kind (Word + PDF, LaTeX + PDF, web page, deck, skill, ...) and whose it is, for anyone about to hand something over.

**Delivery type:** skill

**Covers:** the kinds of delivery found on disk; whose delivery it is (a Page's, a Task's, a Block's, a Job's, an sNN's); the kinds of Block and what each hands over.

**Excluded:** how an sNN's `delivery/` renders out, and the one-delivery rule ([b35-s01:studio @ studio_skill](../s01-studio-skill/s01-studio-skill.md)); building a paper's Word and PDF (haipipe-paper-assemble); the kinds of sNN ([b35-s05:studio @ studio_gallery](../s05-studio-gallery/s05-studio-gallery.md)).

**Topic:** one real delivery of each kind, to copy from. JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery of the studios, as the new sNN". Every sNN now ends in a delivery, yet nobody can see the deliveries that exist side by side: 165 `delivery/` folders in 6 SPACEs (scan of 261030), most of them a Page's LaTeX and PDF. A gallery shows one real delivery of each kind, so a new one copies a good one. The kinds of Block, once sketch F2 in b35-s01, moved here.

**Feeds:** haipipe-delivery `ref/gallery.md`.


Files
-----

```text
s04-delivery-gallery/
├── s04-delivery-gallery.md               this face
├── build_s04_delivery_gallery.py         its drawing: the five parts, the Design read from the scan
├── s04-delivery-gallery.excalidraw, .png
└── delivery/                             deck/ (its slides), skill/gallery.md (written by gallery_scan.py), render.yaml
```


Decided
-------

s04-D01 · The delivery gallery is its own sNN, beside the studio gallery (s05); b35-s01's sketch F2, the kinds of Block and what each hands over, moved here (JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery of the studios, as the new sNN").
s04-D02 · The gallery is counted from disk by `gallery_scan.py`, folder and file names only, never a file's content and never `_WorkSpace/`; a SPACE inside a SPACE is a copy and is skipped.
s04-D03 · The gallery's examples are the newest of each kind from the scan, never one of the two galleries, and one that names its delivery comes first; `gallery_scan.py --write` writes `delivery/skill/gallery.md` on every rebuild of the drawing, and `render_delivery.py` renders it into haipipe-delivery `ref/gallery.md`. Tools is a public repository, so an sNN from another SPACE shows only its path, never its face's words (JL 261030: "go ahead and do it", agreeing to take the newest real one of each kind).


Open
----

1. Word + PDF and LaTeX + PDF: one kind or two?
2. No ui, table or figure delivery exists yet: keep them as kinds in the gallery?
3. Should every Block list its ## Deliveries, as b35's board.md does?

(write here, or mark the drawing in red)

Delivery preview
----------------

**Target delivery:** A searchable gallery page generated from curated example configuration.

**Reader:** People and agents deciding what to hand over.

**State:** review prototype; not accepted or released.

- [Open delivery](delivery/web/index.html)
- [Main delivery Draw](delivery-design.excalidraw)
- [Draw preview](delivery-design.png)
- [Explanation slides](delivery/deck/index.html)
- [Delivery contract](delivery/web/contract.html)

The source is `../scripts/delivery-specs.json`; `../scripts/build_delivery_previews.py` generates the review package. Earlier drawings remain unchanged.
