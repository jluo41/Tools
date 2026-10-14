s09 · Block folder: what the Block's folder holds
==================================================

**Stage:** closed

**Tags:** `UI` · `Structure`

**Topic:** the Studio's fifth folding part, Folder, under the topic cards, Related, Delivery and Timeline: the Block's own
folder as a tree, so a person sees what each folder of the Block holds without leaving the workbench. Asked by JL
261012: "我想创建一个 s09。这个 s09 我们是要创建 folder，也就是在 related 和 timeline 下面再搞一个 folder，这样我就可以
看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容。" Then: "I want to make it to be the s09-block-folder"
(s09-D10). Its decisions start at D10: s09-D01 to D09 are the old s09's, kept in s01 since it merged there.

**Feeds:** `reports/` q09_studio_report_on_screen


What it shows
-------------

```text
▾ Folder
  blueprints/b10_project_workbench/
  📁 related/   2    what came in from outside, kept as it came
  📁 reports/  12    the Questions: a folder each, with its report
  📂 runs/     16    the Runs: a folder each
     📁 run-draw-s08/  3   soft · draw · done · 10 passes
  📁 studio/   16    the Studio: a folder per topic
  📝 board.md        18 KB   12 Oct
```

1. **One tree**: the Block's folder, its folders first and then its files, by name.
2. **A folder** folds; it says how many things it holds and what it is for: the shared names (studio/, reports/,
   runs/, related/, delivery/, passes/, result/, history/) by a fixed line, a Run by its card (kind · type · status
   · passes), any other folder by its face's title.
3. **Loads when opened**: the first level comes with the page; a folder's rows load the first time it opens
   (`?view=dir&path=`), so a Block of thousands of files stays light (b00_rawdata holds 5,317). Past 300 rows a
   button loads the rest.
4. **A file** opens in the pop-out: a .md in the reader, a drawing as the drawing, anything else as itself; it
   says its size and the day it last changed.
5. **Left out**: dotfiles (a drawing's `.seed.json`), `__pycache__`, `node_modules`; a link that leaves the root
   is named, not followed.

It writes nothing. Code: `servers/workbench/frame.py` `studio_folder`, `folder_rows`, `_run_word`, the page
script's Folder loader; `frame_view.py` answers `view=dir`. Shared viewers reach only their grant: the share doors
check `path=` (s52).

```yaml
frames:
- title: "② How a row is read"
  intro: "One folder at a time, from disk, every time it is opened; nothing is written."
  boxes:
  - {id: disk, at: [0, 0], title: 📁 the Block's folder, why: on disk, as it is, cols: 1,
     tree: ["{block}/", "{files} files in {dirs} folders", "b00_rawdata: 5,317 files"]}
  - {id: read, at: [1, 0], title: 🔎 folder_rows, why: one folder's rows, cols: 1,
     tree: [dotfiles and caches left out, "folders first, then files, by name", "300 rows, then: Show the other N"]}
  - {id: screen, at: [2, 0], title: 🖥️ Studio › Folder, why: the fifth folding part, cols: 1, key: true,
     tree: [under Related, Delivery and Timeline, the first level comes with the page, "a folder's rows: when it opens"]}
  - {id: share, at: [0, 1], title: 🔒 a shared viewer, why: "the share doors check path=", cols: 1,
     tree: [sees only the folders of their grant, "a path outside the root: 404"]}
  - {id: folder, at: [1, 1], title: 📂 a folder row, why: it folds, cols: 1,
     tree: ["how many it holds", "studio/ runs/ reports/ …: a fixed line", "a Run: kind · type · status · passes", "else: its face's title"]}
  - {id: file, at: [2, 1], title: 📄 a file row, why: "a click: the pop-out", cols: 1,
     tree: [".md: the reader", ".excalidraw: the drawing", "else: the file itself", "its size, the day it changed"]}
  arrows:
  - {from: disk, to: read, label: is read by}
  - {from: read, to: screen, label: fills its first level}
  - {from: screen, to: folder, label: a folder opens}
  - {from: folder, to: read, label: "asks view=dir"}
  - {from: screen, to: file, label: a file is clicked}
  - {from: share, to: folder, label: is checked at}
```


Files
-----

```text
s09-block-folder/
├── s09-block-folder.md            this face; the frames: yaml holds the map's words
├── build_s09_block_folder.py      the builder: ① the screen, read from disk; ② the map, from the yaml
├── s09-block-folder.excalidraw    two frames in a row: the Folder on screen --> how a row is read
└── s09-block-folder.png           its preview
```

Rebuild: `python build_s09_block_folder.py` (it renders the preview too).


Decided
-------

s09-D10 · A topic of its own for the Studio's Folder part, s09-block-folder (JL 261012: "我想创建一个 s09 ... 在
    related 和 timeline 下面再搞一个 folder"; then "where is our s09 for this ... I want to make it to be the
    s09-block-folder"). First made as s33-studio-folder the same day, since s09 had merged into s01 that morning
    (s01-D37); renamed at JL's ask. The old s09's decisions keep s09-D01 to D09 in s01, so this topic's start at
    D10, and its one session, `runs/run-draw-s09/`, moved to s01's `history/run-draw-s09/`.
s09-D11 · Folder is the Studio's fifth folding part (fourth until s03-D09 put Delivery under Related), under Timeline: the Block's own folder as one tree, folders
    first, then files, by name; a folder says its count and what it is for, a file its size and its day; a file
    opens in the pop-out (JL 261012: "这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容").
s09-D12 · A folder's rows load when it is opened (`?view=dir&path=`), 300 at a time with a button for the rest:
    a Block can hold thousands of files (b00_rawdata, 5,317), so the page carries only the first level (built
    261012). `path=` is the key the share doors already check (s52).
s09-D13 · What a folder is for: the names every Block shares by a fixed line, a Run by its card (kind · type ·
    status · passes), any other folder by its face's title; a title that only repeats the folder's name is left
    out (built 261012, after the first look showed "run-draw-s00/ 3 run-draw-s00").
s09-D14 · Stage → closed: the Folder part is done (JL 261012: "we can close s09 now"). Its two open points move to
    Later, not needed now. The Report it feeds, q09_studio_report_on_screen, is still open.


Open
----

(none: closed 261012, s09-D14)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. Remember which folders were open, in this browser, as the Timeline keeps its level?
2. Find a file by name inside the tree, for a Block as large as b00_rawdata?

(write here, or mark the drawing in red)
