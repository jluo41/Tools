s13 · Block UI: Studio
======================

**Stage:** explore

**Tags:** Block UI

**For:** a deck, and the rules for how the Studio part shows in a Block's Studio (think), for every Theme that builds that page

**Delivery type:** ui

**Covers:** where an sNN appears in a Block page's Studio, and what it shows there.

**Excluded:** the other eight cells (s11 to s19); the page's own content, which each Theme designs (b16, b17).

**Topic:** how the Studio part shows in a Block page's Studio. It is read from the real page (b35_studio), so every Theme builds it the same way (JL 261031: "please add more subgroup of the UI ... to direct others how to make the UI for the report and work").

**Feeds:** none: b35 keeps no Questions


Rules
-----

1. Group buttons sit above the Purpose, one per Tag, in `_studio_groups.txt` order; topics with no Tag go last, as Other.
2. One card per sNN: its address, title, stage and delivery type; its one-line Topic; its drawing on the right.
3. Under the card, its tags: Slide · Draw · Mind map · Work · Delivery · Interaction, each only when it exists.
4. A Block's Studio shows its own sNN (at most 9) and those of its Jobs and Tasks.


Files
-----

```text
s13-block-ui-studio/
├── s13-block-ui-studio.md            this face
├── s13-block-ui-studio.excalidraw    the five parts; its Design is the real screen and these rules
├── screen.png                        the real page, shot by ../../shoot_screens.py
└── delivery/ui/                      the agreed rules, once agreed
```


Decided
-------

(none yet)


Open
----

1. A Task's sNN shows a long address (b35.j02.t02-s11:studio.studio_pages.block_page @ …): show only j02.t02-s11?

(write here, or mark the drawing in red)
