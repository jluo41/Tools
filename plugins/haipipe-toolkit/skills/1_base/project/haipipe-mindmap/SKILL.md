---
name: haipipe-mindmap
description: >-
  The structure map, one renderer shared by a draft Task's §1 Structure map and every Studio topic's mind map
  (scripts/mapview.py): the root card on the left, a card per paragraph or branch with the question it hands to the
  next, a plain line per point (its number, its role pill, its words), thin grey curves, edited where it is read. A
  topic's mind map, `mNN-<topic>.mindmap.md` beside its free drawing (s01 ↔ m01), is one Markdown file drawn with it:
  built from the topic's face (`from-topic`) when the topic is made, refreshed from it after, a person's nodes and
  words kept; a Block's or a world's work too (`from-work`: Block → Job → Task → Run with run counts). On top of §1
  a mind map adds ▸ details, lines under a point, and a chip per file a point names. Use to make, show, edit or
  refresh a mind map, or to change how §1 and the mind maps draw. Trigger: mind map, mindmap, mNN, structured side,
  Free | Structured, structure map, §1 map, map the work, /haipipe-mindmap.
metadata:
  version: "0.6.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /haipipe-mindmap · one structure map, shared

A draft Task's §1 Structure map and a Studio topic's mind map are drawn by the same code (`scripts/mapview.py`), so
they look and edit alike (JL 261026: "你把他们那个 map 也放到我们这个新的 skill 里面去 … 这样的话他们就共享了").

```text
draft/<stem>-draft-vN.md  ## 1 · Structure ──▶ draft_steps.py _plan_map ─┐
                                                                         ├─▶ mapview.render ─▶ the map (§1's look)
studio/sNN-<topic>/mNN-<topic>.mindmap.md ──▶ mmmap.draw ────────────────┘        │ each edit, one payload
       ▲ from-topic (the face)                                                   ▼
       └──────────── /_board/mindmap (mmmap.act) ◀── a mind map · a draft ──▶ /_board/draft-plan (plan_act)
```

A Studio topic has two sides, linked by number: its free drawing (`sNN-<topic>.excalidraw`) and its mind map
(`mNN-<topic>.mindmap.md`); the workbench card switches them (Free · Structured), and `new_topic.py` (haipipe-studio)
makes both.


The map
-------

1. **§1's look**: the root card (its name, its note in muted type as §1's arc); a card per first-level node (a small
   grey number over its bold name), and between two of them the question one hands to the next (`→ <question>`, a
   note line of the first); a plain line per point under it: its number (`1.2`), its role pill (`[role] words`), its
   words; thin grey curves. Its CSS and script are §1's own (`mapview.CSS`, `mapview.JS`).
2. **Edit in place, as §1**: click words and type; Enter adds the next point; ＋ point, ＋ paragraph (shown on hover);
   a point emptied is taken out (what hung under it moves up); a point dragged by its number onto another goes before
   it, onto a card last in it; a role typed into its pill; the question typed between two cards. Each change is one
   POST of §1's payload to the map's endpoint: a mind map's `/_board/mindmap` (`mmmap.act`) writes the `.mindmap.md`
   and its static page; a draft's `/_board/draft-plan` writes §1. Words changed on disk since the page showed them
   are refused.
3. **A mind map's extras**: ▸ opens a point's detail below it (its other note lines, Markdown: a link opens in the
   pop-out, a picture shows as itself), ✎ edits it; the lines under a point, and theirs, indented to any depth; a chip
   per file a point names (🖼 a picture, ↗ else), as §1's evidence chips. A draft's map draws without them.
4. **Written, not only built**: `from-topic` gives a skeleton; a map reads as §1 when
   it is written: each branch a step of the topic's argument with its kind (`[question] What Q01 asks`, the grey line
   over its name), the question it hands to the next (`→ …`), each point one short complete sentence with its role,
   the long text and links in its detail. A written map says `written:` in its header; a refresh then keeps its
   branches and its root as written and lets only the Files branch follow the disk. b17's five maps are written so.
5. **Where it shows**: a draft Task's 1 · Plan (§1 Structure); a topic card's Structured side, read from the file on
   every open; the static page `<stem>.mindmap.html` (read only, git-ignored).


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
haipipe-mindmap/
├── SKILL.md             this file
├── CHANGELOG.md         its versions
├── ref/grammar.md       the .mindmap.md grammar; the map's edits; refresh
├── scripts/mindmap.py   the commands
├── scripts/mmtree.py    the grammar: read, ids, write
├── scripts/mapview.py   the structure map: §1's markup, CSS and script, shared with draft_steps.py
├── scripts/mmmap.py     a mind map through mapview, and `act`, the one writer of its edits
├── scripts/mmbuild.py   from-topic, from-work, refresh
├── scripts/mmhtml.py    the static page and its Markdown
└── tests/test_mindmap.py
```
