s02 · The Studio on every page
==============================

**Stage:** explore

**Tags:** Studio

**For:** a deck, and the Studio's UI in the workbench (`servers/workbench/focus_page.py`, `focus.css`): the Studio inside a Block, Job or Task page, and, since s02-D05, an sNN's card as the place every link to it lands (JL 261030: "what I want to achieve is how to get the UI for the studio page"; "like the studio embed in other page, and studio itself as a page").

**Delivery type:** ui

**Covers:** what an sNN's page shows; the Studio rows on a Block, Job or Task page; the Block map; groups and Links

**Excluded:** what a Studio is and delivers (s01); mind map and leaf drawings (s03); slide rules (b34-s02)

**Links:** [b35-s01:studio @ studio_skill](../s01-studio-skill/s01-studio-skill.md)

**Topic:** what a topic is for on the Block, a Job or a Task, and how the page it sits on shows it. Its sNN sit beside the Jobs and Tasks of the level they serve (b35-s01-D12). JL 261029: "我觉得我们可能会有几种 level 的 studio ... Block level studio, Job level studio, Task level studio, 它们各自都干什么？" This topic says what a topic is for on each level, and how its level's page and the pages above it show it.

From b35 s07 (topic-links), merged 261030: how topics in different Blocks connect: groups and Links lines. They often talk about the same thing; JL 261029: "I still want them to be connected". Groups (`studio/_groups.txt`, a face's `**Tags:**`) gather them, and a `**Links:**` line points from one topic to another, shown on the face (the topic page that listed them both ways is retired, s02-D05).

**Feeds:** `servers/workbench/focus_page.py`; haipipe-ui (the page rules); haipipe-studio (Tags, Links).


Files
-----

```text
s02-studio-pages/
├── s02-studio-pages.md            this face
├── s02-studio-pages.excalidraw    its drawing
├── s02-studio-pages.mindmap.md    its mind map, a drawing per leaf in map/
├── s02-studio-pages.ideas.md      the open ideas
├── s02-studio-pages.slides.json   each slide's content and leaf
├── slides/                        the slide pictures
└── result/                 working output; merged sNN kept whole under result/merged-*/
```


Decided
-------

s02-D01 · A topic has its own page on the same template as a Block, Job or Task page; the Studio rows on other pages preview it, and their name, line and picture open it (JL 261029: "make this clickable ... just like the same template to the block job"; "we will treat the studio just as a page as well, but we can also preview them in other page level as well"). (Was b35 s04-D01, merged 261030.)

s02-D02 · The mind map is a section of the topic page, not a pop-out, and the page has no Slides button, since Ideas already shows the slides (JL 261029: "the mindmap should be embebed in the page as well, not a new pop out page"; "why we still need this"). (Was b35 s04-D02, merged 261030.)

s02-D03 · Topics connect across Blocks by one shared list of groups per Project and by a `**Links:**` line on a face, naming other topics by address; the page shows links both ways (JL 261029: "I still want them to be connected"; "这个挺好的"). It was b35-s01's D08. (Was b35 s07-D01, merged 261030.)

s02-D04 · s02 delivers the Studio's UI, two screens: the Studio inside a Block, Job or Task page, and the Studio as a page of its own, one sNN's page; its Design draws both screens, its Job builds them (JL 261030: "what I want to achieve is how to get the UI for the studio page"; "like the studio embed in other page, and studio itself as a page").

s02-D05 · An sNN has no page of its own any more; this replaces D01, D02 and D04's second screen. A link to an sNN (the left rail's, an old `?path=…/sNN-…` link) opens its card in its level's Studio section, under its group, the card outlined; the card's name and line open the face, its picture the slide, each in the pop-out; Links show on the face (JL 261031: "first we will remove the single page for the studio ... when we click this, we will be point to" the card in `section=studio`; "ok, go ahead"). Code: `focus_page.py` `topic_home`, `rail_url`; `frame_view.py` sends an old link on (302).


Open
----

1. What is a topic for on each level: Block, a design question; Job, how its Tasks fit; Task, one figure or table to agree?
2. Which part of a topic does a reader see first, and does the face's Decided list still belong? (from b35-s01)
3. Does a Job page show its Tasks' topics too, or only its own?
4. Where does the Project's one group list live, while each Block still has `studio/_groups.txt`? (from b35 s07, topic-links)
5. Does a `**Links:**` line name a topic by its full label or by its address only? Today the page finds a back link by the folder name, so the line links the face. (from b35 s07, topic-links)

(write here, or mark the drawing in red)

Delivery preview
----------------

**Target delivery:** A Studio browser with a dedicated detail page and large Draw viewer.

**Reader:** People working within a Block, Job or Task.

**State:** review prototype; not accepted or released.

- [Open delivery](delivery/web/index.html)
- [Main delivery Draw](delivery-design.excalidraw)
- [Draw preview](delivery-design.png)
- [Explanation slides](delivery/deck/index.html)
- [Delivery contract](delivery/web/contract.html)

The source is `../scripts/delivery-specs.json`; `../scripts/build_delivery_previews.py` generates the review package. Earlier drawings remain unchanged.
