---
name: mindmap
part-of: haipipe-studio
description: >-
  A Studio topic's other side: its mind map, `mNN-<topic>.mindmap.md`, kept as one Markdown file and drawn the way a
  draft Task's §1 Structure map is (HTML, the root at the left, each node's children to its right), edited where it
  is read: click a node and type, Enter for the next node, ＋ for a child, empty it to take it out, drag it to move
  it; each change is written into the file. Every sNN has one, linked by number (s01 ↔ m01), built from the topic's
  face (`from-topic`) when the topic is made and refreshed from it after; a Block's or a world's work can be mapped
  too (`from-work`: Block → Job → Task → Run with run counts). A refresh keeps any node or wording a person added.
  Use to make, show, edit or refresh a topic's mind map, or to map a work Block. Trigger: mind map, mindmap, mNN,
  structured side, Free | Structured, map the work, map this Block.
metadata:
  version: "0.5.2"
  last_updated: "2026-10-26"
---

# /haipipe-studio mindmap · a topic's other side

A Studio topic has two sides, linked by number: the free drawing a person sketches on (`sNN-<topic>.excalidraw`)
and its mind map (`mNN-<topic>.mindmap.md`). The mind map is not a canvas. It is drawn the way the draft's §1
Structure map is (`servers/workbench/workbench-task-draft/draft_steps.py` `_plan_map`), so the structure of a topic
and the structure of a draft read and edit alike.

```text
sNN-<topic>.md (the face) ── from-topic ──▶ mNN-<topic>.mindmap.md ── drawn as §1's map ──▶ the card's Structured side
                                                  ▲                                              │
                                                  └──────── each edit: POST /_board/mindmap ◀───┘
```


The map
-------

1. **Look**: the root on the left in the key colour; each node a card; its children a column to its right; curved
   wires as the draft's §1 map draws them, each end at its card's first line (an opened card is met at its words); Markdown in a node shows as Markdown.
2. **A colour per branch, three styles**: each first-level branch takes a hue of the dataviz reference palette in its
   fixed order (validated light and dark; a ninth branch on is grey), its wires and cards follow it. The switch above
   the map picks the look, remembered in the browser: **Branches** (branch cards edged, leaves in a thin line of the colour),
   **Filled** (branch cards filled, leaves tinted), **Ink** (black and grey, as §1). An opened detail is its own panel,
   a soft box washed in its branch's colour.
3. **Short card, its detail behind ▸**: a card holds a few words; ▸ opens its detail below them, the lines under its
   bullet, as Markdown: a link opens in the pop-out, a picture (`![name](file)`) shows as itself. ✎ edits the detail
   as its Markdown; leaving the box saves it. A card with no detail shows ▸ on hover, to add one.
4. **Edit in place**: click a node and type (it shows its raw words while typed); Enter adds the next node below it;
   ＋ (shown on hover) adds a child last; a node emptied is taken out and what hung under it moves up; a node dragged
   onto another goes before it, onto a ＋ goes last under that node. Esc puts back what it held.
5. **Written once, where it lives**: each change is one POST to `/_board/mindmap` (`scripts/mmmap.py` `act`), which
   rewrites the `.mindmap.md` and its static page. A change to words that changed on disk since the page showed them
   is refused and the map reloads, so nothing typed elsewhere is lost.
6. **Any depth**: a node may hold nodes, and those nodes more, to any depth; a node with nothing under it is a leaf.
7. **A card opens its file**: a node whose words link a file (`[s01-work-ladder.png](s01-work-ladder.png)`) shows the
   words and a button beside them (🖼 for a picture, ↗ else) that opens it in the workbench's pop-out: a picture as
   itself, a drawing in its editor, a page in its reader. The Files branch writes each file as such a link.
8. **Where it shows**: the workbench topic card's Structured side (`servers/workbench/frame.py`), read from the file
   on every open; the static page `<stem>.mindmap.html` (read only, git-ignored), for opening outside the workbench.


Commands
--------

```text
python scripts/mindmap.py new        <x.mindmap.md> [--title T]     a root and nothing under it yet
python scripts/mindmap.py from-topic <studio/sNN-topic> [--out F]   the topic's mind map, mNN-<topic>
python scripts/mindmap.py from-work  <work/ | Block | Job> [--out F] Block → Job → Task → Run, run counts
python scripts/mindmap.py refresh    <x.mindmap.md>                  rebuild from disk; a person's words kept
python scripts/mindmap.py render     <x.mindmap.md>                  the static page
python scripts/mindmap.py check      <x.mindmap.md | folder> ...     grammar and ids
```

`new_topic.py topic` (haipipe-studio) runs `from-topic` itself, so a new topic is made with both sides.


Builders and refresh
--------------------

1. **from-topic**: the face's labelled lines (`**Topic:**`, `**Source:**`, `**Feeds:**` …) and its sections
   (Files, Decided, Open …) become branches; each sentence or item a leaf of at most seven words, the whole sentence
   its detail; the Files branch lists the folder's real files, each a link (its bubble opens it) and a picture shown
   in its detail; `**Stage:**`, `**Tags:**` and `**Label:**` go in the root's detail.
2. **from-work**: the root is the folder (a world, a Block, a Job); a Job reads `jNN_<job> · N tasks · M runs`, a
   Task `tNN_<task> · M runs, K done`, a Run its folder name and its state (✅ done, ❌ failed, 🔶 running, ⛔
   blocked, ⬜ open) from `run.yaml`; every Run shown; a Task's detail is its face's `goal:` and `close:`. A world stops at Tasks. Written to `<folder>/studio/
   mind-map.mindmap.md`, which a Block's or a world's `studio/` keeps loose (haipipe-project `ref/ladder.md`).
3. **Refresh**: a built node whose words a person did not change takes the new words; a node or words a person added
   stay; a built node gone from disk goes, unless a person changed it or hung something under it. A built node's
   `<!-- @key #hash -->` mark is how it knows.

The file's grammar: [ref/grammar.md](ref/grammar.md).


Files
-----

```text
_parts/mindmap/
├── PART.md              this file
├── CHANGELOG.md         its versions
├── ref/grammar.md       the .mindmap.md grammar; the map's edits; refresh
├── scripts/mindmap.py   the commands
├── scripts/mmtree.py    the grammar: read, ids, write
├── scripts/mmmap.py     the map (the §1 look) and `act`, the one writer of its edits
├── scripts/mmbuild.py   from-topic, from-work, refresh
├── scripts/mmhtml.py    the static page and its Markdown
└── tests/test_mindmap.py
```
