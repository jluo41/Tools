# Icon libraries

Part of hai-studio's drawing rules (CONSTITUTION.md A04: a Design is pictures). Two sources of pictures:

```text
scripts/icons.py           our own icons, a function each, lit by a state (ok, wait, bad, off)
scripts/icon_library.py    any item of a downloaded Excalidraw library, by its name
```

Every icon, with its name: `ref/icons/icons.png` (our own) and `ref/icons/libraries.png` (the libraries).

## Use an item

```python
from icon_library import item
els += item("clipboard", "a_clip", x, y, w=120)
els += item("Ideation", "a_team", x, y, h=200, lib="stick-figures-collaboration", color="#047857")
```

1. **By name**: matched without case. A name two libraries share needs `lib=`; an unknown name fails and lists the
   nearest names.
2. **Place and size**: `(x, y)` is its top-left; `w` or `h` scales it, both fit it inside; neither keeps its size.
3. **Colour**: `color=` recolours lines and outlines; fills stay as drawn.
4. **Find one**: `python scripts/icon_library.py --list search` prints the names that hold the word.

## The libraries kept here

From the Excalidraw public libraries, <https://libraries.excalidraw.com> (the `excalidraw-libraries` repository, MIT),
each file as downloaded, in `ref/icons/libraries/`:

| File | Holds | Author |
|---|---|---|
| `icons.excalidrawlib` | files and documents by kind: paper, clipboard, table, search, upload | xxxDeveloper |
| `system-icons.excalidrawlib` | filter, set up, tree, bar graph, file, warn, relationship | xxxDeveloper |
| `basic-ux-wireframing-elements.excalidrawlib` | the parts of a screen: buttons, toggles, fields, a modal, a menu | gabi.macakova |
| `stick-figures-collaboration.excalidrawlib` | people working together: Ideation, Presentation, Conversation | freepik |

`ref/icons/stick-figures.excalidrawlib` (single people, Youri Tjang) was kept earlier and reads the same way.
`ref/icons/own-icons.excalidrawlib` holds our own icons (`icons.py --gallery` writes it), to drag in by hand.

## Add a library

1. Pick one at <https://libraries.excalidraw.com>; prefer general pictures over product logos.
2. Save its `.excalidrawlib` file into `ref/icons/libraries/`, unchanged. Keep a file under 1 MB.
3. Add its row above and its origin to `references/sources.yaml`.
4. Run `python scripts/icon_library.py --gallery` and look at `ref/icons/libraries.png`.
5. Run the tests: every item of every kept library must draw.
