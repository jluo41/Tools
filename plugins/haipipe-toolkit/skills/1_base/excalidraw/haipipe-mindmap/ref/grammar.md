# The `.mindmap.md` grammar

One file is the mind map. `scripts/mmtree.py` reads and writes it; nothing else is the source.

## The shape

```markdown
---
mindmap: 1
title: Trip
built: from-work ../..          # only a built map: the builder and its source, relative to this file
---

# Trip **plan** <!-- root -->

Why we go: rest.                 # the root's note: any lines before the list

- Where <!-- n01 -->
  - Lisbon <!-- n02 -->
  - Porto <!-- n03 -->
- When <!-- n04 -->
  the week after the deadline    # a node's note: a line under its bullet, not a bullet
  - May <!-- n05 -->
- j01_build · 2 tasks · 8 runs <!-- @j01_build #3fa2c1 -->

## Notes

Anything from the first `## ` heading after the list on is kept as written, and rendered on the page.
```

1. **Front matter**: `key: value` lines between `---`. `mindmap: 1` is the grammar's version; `title` names the
   canvas frame and the page; `built` is set by a builder.
2. **Root**: the first `# ` line. Its id is always `root`.
3. **Nodes**: one bullet each (`-`, `*`, `+` or `1.`; written back as `-`), nested by indent (two spaces a level;
   any deeper indent nests). The words are Markdown.
4. **Ids**: a trailing `<!-- id -->`. A person's node is `nNN`; a bullet typed without one gets the next free `nNN`
   on the next `render` or `sync`, never an id the canvas still remembers. A built node's id starts with `@` and
   names its source (`@j01_build/t02_fit`, `@topic/0`); its `#hash` is the hash of the words its builder wrote.
5. **Notes** under a bullet are drawn small under its box and edited in the file only.
6. **Encoding**: UTF-8 with LF line ends, on every platform.

## The canvas

`render` draws one frame, `mm:frame`, left to right: the root at the left in the key colour (#fff3bf), a column per
depth, each parent centred on its children, a line from each parent's right side to its child's left side, and the
⑥ ⑦ badge. Every element it draws has an id starting `mm:`:

```text
mm:frame            the frame; customData.mindmap.base = what was drawn: {id: {text, parent, order}}
mm:<id>:box         a node's box (customData.mindmap = its id)
mm:<id>:text        its words, bound to the box (Excalidraw's containerId), so a double-click edits them
mm:<id>:edge        the line to its parent, bound at both ends
mm:<id>:note        its note, small and grey
mm:title mm:sub mm:x<k>   the frame's title, its line, the badge
```

A tree too wide for one screen wraps its words narrower; one too tall stands its boxes closer or makes its leaves'
lines longer, so a map that fits principle ⑦ also fits ① (2800 x 1600).

## How `sync` reads the canvas

The base in `mm:frame` is the tree as last drawn. `sync` compares three trees: the base, the file now, the canvas now.

```text
words      a box's bound words (originalText) differ from the base
deleted    a node's box is gone or marked deleted, or its words are empty
added      a person's box with words, or plain words, that an arrow joins to a node (or to another added box)
moved      an arrow (or line) ends at a node's box and starts at another node: a person's arrow first, then the
           node's own edge where its start was dragged; bound ends first, else the box the end point lies in
reordered  siblings read top to bottom by their boxes' centres
kept       every other element of the person's: never read, never removed
```

A node whose line was deleted and nothing else changed stays where it was. A node whose parent's box was deleted
moves up to the nearest node still on the canvas. A loop (a node under its own child) is ignored.

## Both sides

```text
conflict                                         --take canvas         --take file
words changed on both sides, differently         the canvas's words    the file's words
words changed on the canvas, node deleted in the file   stays deleted    stays deleted
deleted on the canvas, changed in the file       deleted               kept, as the file has it
moved on both sides, to different parents        the canvas's parent   the file's parent
moved on the canvas, deleted in the file         stays deleted         stays deleted
children reordered on both sides, differently    the canvas's order    the file's order
added on the canvas under a node the file deleted  not added           not added
```

With any open conflict `sync` writes nothing and exits 2. `render` exits 2 too while the canvas holds edits the
file lacks; `render --force` draws over them.

## Refresh

A built node keeps `#hash`, the hash of its builder's words. On refresh:

```text
built, words unchanged (hash matches)   takes the builder's new words and hash
built, words a person changed           keeps the person's words (and the old hash, so it stays "changed")
built, gone from disk                   goes, unless a person changed it or a person's node hangs under it
a person's node (nNN)                   stays, under the same parent, in the same place among its siblings
new on disk                             inserted after its built sibling, in the builder's order
```
