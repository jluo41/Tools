# The `.mindmap.md` grammar

One file is the mind map. `scripts/mmtree.py` reads and writes it; the map on the card and the static page are drawn
from it, and every edit made on the card is written back into it.

## The shape

```markdown
---
mindmap: 1
title: Trip
built: from-topic .              # only a built map: the builder and its source, relative to this file
---

# Trip **plan** <!-- root -->

Why we go: rest.                 # the root's note: any lines before the list

- Where <!-- n01 -->
  - Lisbon <!-- n02 -->
  - Porto <!-- n03 -->
- When <!-- n04 -->
  the week after the deadline    # a node's note: a line under its bullet, not a bullet
  - May <!-- n05 -->
- Topic <!-- @topic #7e13bd -->

## Notes

Anything from the first `## ` heading after the list on is kept as written, and rendered on the static page.
```

1. **Front matter**: `key: value` lines between `---`. `mindmap: 1` is the grammar's version; `title` names the
   static page; `built` is set by a builder.
2. **Root**: the first `# ` line. Its id is always `root`.
3. **Nodes**: one bullet each (`-`, `*`, `+` or `1.`; written back as `-`), nested by indent (two spaces a level;
   any deeper indent nests). The words are Markdown and show as Markdown on the map.
4. **Ids**: a trailing `<!-- id -->`. A person's node is `nNN`; a bullet typed without one gets the next free `nNN`
   when the map is next drawn. A built node's id starts with `@` and names its source (`@j01_build/t02_fit`,
   `@topic/0`); its `#hash` is the hash of the words its builder wrote.
5. **Notes** under a bullet show on hover on the map and are edited in the file.
6. **Encoding**: UTF-8 with LF line ends, on every platform.

## The map's edits

Each is one POST to `/_board/mindmap` with the file's path from the host's root (`mmmap.act`):

```text
what   with                         writes
text   id, was, value               the node's words (refused when the words on disk are no longer `was`)
add    parent, after?, value        a new node nNN under parent, after `after` (else last)
drop   id, was                      the node out; its children take its place
move   id, before | parent          before a node (its sibling then), or last under a parent; never under itself
```

A read-only host refuses every change (403); a path outside the host's root or not a `.mindmap.md` is refused (400).
After each change the static page is rebuilt.

## Refresh

A built node keeps `#hash`, the hash of its builder's words. On refresh:

```text
built, words unchanged (hash matches)   takes the builder's new words and hash
built, words a person changed           keeps the person's words (and the old hash, so it stays "changed")
built, gone from disk                   goes, unless a person changed it or a person's node hangs under it
a person's node (nNN)                   stays, under the same parent, in the same place among its siblings
new on disk                             inserted after its built sibling, in the builder's order
```
