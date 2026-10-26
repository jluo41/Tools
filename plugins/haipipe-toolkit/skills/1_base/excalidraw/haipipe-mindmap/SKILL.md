---
name: haipipe-mindmap
description: >-
  A mind map kept as one Markdown file, `<name>.mindmap.md`, and shown three ways: the file itself, an Excalidraw
  canvas drawn left to right (`.excalidraw` and its `.png`), and a web page with the Markdown rendered
  (`.mindmap.html`). Editable both ways: `sync` reads canvas edits back into the file (changed words, added boxes,
  rewiring, reordering, deletions) and keeps anything else drawn on the canvas; an edit made on both sides stops until
  the person picks a side. Builders read it from disk: `from-work` (Block → Job → Task → Run, with run counts) and
  `from-topic` (a Studio topic's structured side, `mNN-<topic>`); a refresh keeps any node or wording a person added.
  Use to make, draw, edit or refresh a mind map, to give a Studio topic its structured side, to map a work Block or a
  whole work/ world, or to bring canvas edits back into the file. Trigger: mind map, mindmap, mNN, structured side,
  map the work, map this Block, sync the mind map, /haipipe-mindmap.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.2.0"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md
---

# /haipipe-mindmap · one file, three views

A mind map is a tree, and a tree is easiest to keep as an indented list. So the list is the source, and the
pictures are views of it: a person can edit whichever is in front of them, and the other two follow.

```text
                    render ─▶ <name>.excalidraw ─▶ <name>.png      (left to right, one screen)
<name>.mindmap.md ──┤
   ▲  the source    └ html ───▶ <name>.mindmap.html                (Markdown rendered, folds; git ignores it)
   │
   └──── sync ◀── a person's edits on the canvas: words, new boxes, arrows, order, deletions
```

Before drawing, load `/excalidraw-studio`: the canvas is a map frame under its principles (① one screen, ② a mind
map, ⑤ the key colour on the root, ⑦ at most 200 words, ⑧ boxes as wide as their words), drawn with its
`scripts/draw.py` (`Drawing`, its measure, wrap, key and the ⑥ ⑦ badge) and checked with its `scripts/check.py`. The
preview is haipipe-studio's `render_png.py`.


Commands
--------

```text
python scripts/mindmap.py new        <x.mindmap.md> [--title T]       a root and nothing under it yet
python scripts/mindmap.py from-work  <work/ | Block | Job> [--out F]   Block → Job → Task → Run, run counts
python scripts/mindmap.py from-topic <studio/sNN-topic> [--out F]      the topic's structured side, mNN-<topic>
python scripts/mindmap.py refresh    <x.mindmap.md>                    rebuild from disk; a person's words kept
python scripts/mindmap.py render     <x.mindmap.md> [--force]          canvas + png + page from the file
python scripts/mindmap.py sync       <x.mindmap.md> [--take file|canvas|<id>=file|<id>=canvas]
python scripts/mindmap.py html       <x.mindmap.md>                    the page only
python scripts/mindmap.py check      <x.mindmap.md | folder> ...       grammar, ids, views, nothing unsynced
```

1. **Exit codes**: 0 done; 1 a check failed; 2 an edit waits for a person (a conflict, or `render` asked to draw
   over canvas edits the file does not have yet).
2. **`--all`** on a builder keeps every node; without it the builder folds its longest lists into `+N more` so the
   map keeps principle ⑦'s 200 words and one screen of leaves.
3. **Python**: 3.9 or newer with Pillow, e.g. `uv run --with pillow python scripts/mindmap.py …`.


Where the files go
------------------

| map | its file | why there |
|---|---|---|
| a Studio topic's structured side | `studio/sNN-<topic>/mNN-<topic>.mindmap.md` (+ `.excalidraw`, `.png`) | the topic folder holds both sides (haipipe-studio ref/topic-contract.md); the workbench card switches Free and Structured |
| a Block's work | `<Block>/studio/mind-map.mindmap.md` (+ `mind-map.excalidraw`, `.png`) | a Block's `studio/` keeps `mind-map.*` loose, like its question map (haipipe-project ref/ladder.md) |
| a whole world | `work/studio/mind-map.mindmap.md` | a world folder may hold one `studio/` for project-wide drawings |
| anything else | any `<name>.mindmap.md` | `new`, then edit |

The `mNN` keeps its topic's number (s01 → m01) and is never the topic's main drawing: the workbench shows it only
on the card's Structured side.


Editing both ways
-----------------

1. **In the file**: change words, add a bullet (no id needed; `render` gives it the next `nNN`), indent or outdent
   it, move it, delete it, write a note under it. Then `sync` (or `render`).
2. **On the canvas**: double-click a box and change its words; draw a box (or plain words) and an arrow from the
   node it belongs under; drag a line's start onto another box, or draw a new arrow from it, to move a node;
   drag a box above or below its sibling to reorder; delete a box to delete its node (its children move up).
   Then `sync`.
3. **Kept**: anything else drawn on the canvas (a note, a circle, a box no arrow joins to the map) stays the
   person's, through every render. A box `sync` took into the file is drawn again as the map's own.
4. **Both sides**: an edit to the same node on both sides (words both ways, edited here and deleted there, moved
   both ways, the same children reordered both ways) stops `sync` with exit 2 and writes nothing. It lists each
   conflict with both sides; the person picks: `--take canvas`, `--take file`, or per node `--take n03=canvas`.
5. **Markdown on the canvas**: a node's `**bold**`, `` `code` `` and links show as plain words on the canvas and as
   Markdown on the page. Words changed on the canvas come back plain.
6. **Notes** (lines under a bullet) are edited in the file only; the canvas shows them small and grey.

How `sync` tells the sides apart, and the grammar of the file: [ref/grammar.md](ref/grammar.md).


Builders and refresh
--------------------

1. **from-work**: the root is the folder (a world, a Block, a Job); a Job reads `jNN_<job> · N tasks · M runs`, a
   Task `tNN_<task> · M runs, K done`, a Run its folder name and its state (✅ done, ❌ failed, 🔶 running, ⛔
   blocked, ⬜ open) from `run.yaml`. A world stops at Tasks. Folder names, never new ones (excalidraw-job's rule).
2. **from-topic**: the topic face's labelled lines (`**Topic:**`, `**Source:**`, `**Feeds:**` …) and its sections
   (Files, Decided, Open …) become branches; each sentence or item a leaf of at most nine words; the Files branch
   lists the folder's real files; `**Stage:**`, `**Tags:**` and `**Label:**` sit under the root as its note.
3. **Refresh** (`refresh`, or a builder run again on an existing file): first `sync`, so no canvas edit is lost;
   then a built node whose words a person did not change takes the new words; a node or words a person added stay;
   a built node gone from disk goes, unless a person changed it or hung something under it. A built node's
   `<!-- @key #hash -->` mark is how it knows.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-mindmap` | the `.mindmap.md` grammar, its three views, `sync`, the builders and their refresh |
| `excalidraw-studio` | how the canvas reads: the principles, `draw.py`, `check.py` |
| `haipipe-studio` | the topic folder and its face (the mNN files listed in its contract), `render_png.py` |
| `haipipe-project` | where `studio/` may sit (`ref/ladder.md`: a world's `studio/`, a Block's `mind-map.*`) |
| the workbench (`servers/workbench/frame.py`) | the topic card's Free · Structured switch |


Files
-----

```text
haipipe-mindmap/
├── SKILL.md             this file
├── CHANGELOG.md         its versions
├── agents/openai.yaml   Codex's card
├── ref/grammar.md       the .mindmap.md grammar; how sync reads the canvas; conflicts
├── scripts/mindmap.py   the commands
├── scripts/mmtree.py    the grammar: read, ids, write
├── scripts/mmcanvas.py  the canvas: draw left to right, read edits back, merge
├── scripts/mmbuild.py   from-work, from-topic, the 200-word fit, refresh
├── scripts/mmhtml.py    the web page
└── tests/test_mindmap.py
```
