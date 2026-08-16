# Draw · every page keeps its own drawing
state: 🟡 PARTIAL · scenes in page draw/, split + compose live · open: draw.py layout, embed-write retire
owner: CC
page-type: design
method: one Excalidraw scene per page in the page's own draw/ folder; the page body carries only the ascii figure
session: da5c5ec9-ee25-4017-bd12-49324c28ae43

## Opening
Where does a page's drawing live, and how do you work on it?
Every page can have a drawing: an Excalidraw scene anyone can open, edit, and talk over.
The scene is a file in the page's own `draw/` folder, so it travels with the page and lives in git like everything else.
The page body itself shows only the ascii figure in `## Diagram`, which reads anywhere, even with scripts off.
To see or edit the real drawing, open the page's Draw split; the group page composes every member's drawing into one large view.

**Where this page sits**: `QPf1` says a page owns its folder and every subfolder is a plugin; this page owns the `draw/` plugin.
`QO5` owns the split workspace a drawing opens in, and `QO11` owns two people editing at once.

## Diagram
**The drawing's three homes**: the page shows ascii, the plugin holds the scene, the group composes.
```text
  📋 the PAGE, on stage                 🖌 the PLUGIN, beside it
  ┌───────────────────────────┐        ┌──────────────────────────┐
  │ ## Diagram                │        │ PAGE/draw/               │
  │   ascii only · scripts-   │        │   PAGE.excalidraw        │
  │   off readable            │  tab   │   scene · page-owned     │
  │ ## Content …              │ ──────▶│   edit · in the split    │
  │   (no embeds anywhere)    │  🖌     │   save · to this file    │
  └───────────────────────────┘        └──────────────────────────┘
                                              │ composed, never copied
  🗂 GROUP/draw/group.excalidraw    ◀─────────┘
     relationships + layout · import manifest over the page sources
```
The scene is the page's own, it opens in a split beside the page, and every edit saves back to that one file.

## Content
### 1 · Where a drawing lives
**The files**: one scene per owner, each in its owner's folder.
```text
📄 page drawing     PAGE/draw/PAGE.excalidraw      the page's own scene
🗺 group drawing    GROUP/draw/group.excalidraw    layout + relations over the pages
🧭 board map        board.excalidraw               the Index page's overview scene
🖼 image bytes      draw/assets/OWNER/             pasted images, kept out of the scene
```
Each page drawing is an ordinary Excalidraw file that is useful opened by itself.
Pasted image bytes land under the owner's `draw/assets/` and the scene keeps a relative pointer to them.
A page that has no drawing yet gets an empty scene created the first time its Draw split opens, so there is never a missing file to trip over.
The group drawing holds only group-level layout and an import list naming each page's scene; it never copies their content.

### 2 · Opening, editing, and generating
**The Draw split**: the drawing opens beside the page, never inside it.
```text
🖌 open        Plugin ▾ → Draw, or the Draw tab in the right pane
✏️ edit        draw on the canvas; saves go to this page's own scene file
✨ generate    the Draw-it button: Claude draws the page's ## Diagram for you
🔄 follow      navigate to another page and the canvas follows it
```
The split shows which file it saves to before you draw, so a gesture can never land in another page's scene.
The Draw-it button takes an optional ask; left empty, it draws the page's ascii figure as a real scene.
A generated scene may be regenerated freely, but the button refuses to overwrite a drawing a person made by hand.

### 3 · The group view is composed, never copied
**One large drawing from many small ones**: what is stored and what is derived.
```text
💾 stored     each page's scene · the group's own layer · placements
⚙️ derived    one composed view, rebuilt on every open
🔒 identity   every element keeps its owner, so edits route home
```
Opening a group's drawing loads the group scene, pulls in every member page's scene, and places them by the stored layout.
Editing inside the composed view happens in one visible mode at a time: arrange the pages, edit the group's own layer, or enter one page's scene; only that owner's file receives the save.
A page save updates the composed view on its next open; nothing is ever merged or imported by hand.

### 4 · Saves are checked, never blind
**The safe save**: what the server verifies before writing.
```text
📥 opened     the revision the editor loaded
📤 save       owner · that revision · the changed elements
✅ accepted   the file has not moved since
⚠️ conflict   someone else saved first · reload and compare
```
Every save carries the revision it started from, so two people editing the same drawing cannot silently overwrite each other.
The chat pane receives the same owner address as the canvas, so asking it to change a drawing routes to that drawing's own file.

## Aims
- [x] 🚚 Every page scene lives in its page's draw/ plugin
      61 scenes moved and renamed to current page ids; only group.excalidraw remains at group level.
- [x] 🧹 No ## Diagram embeds an Excalidraw canvas
      The frame links are stripped from all 19 pages that carried one; Diagram is ascii-only.
- [ ] ⚙️ draw.py learns the folded layout
      Group = the group folder, page scene = the page's draw/; manifests re-point; verify passes on this board.
- [x] 🖼 The group canvas renders again
      page_board.group_canvas anchors on the group folder instead of the members' shared parent.
- [ ] 🗑 The unused embed-write route retires
      The live layer still accepts a write that no page renders; removing it closes the loop.

## States
The drawings themselves are in place: every page scene sits in its page's folder, the split opens and follows the page, and the group view composes.
draw.py's verify still round-trips the legacy board.excalidraw at the board root instead of the folded page layout.
serve.py still accepts the embed-write save at `/_board/excalidraw`, which writes a scene link into `## Diagram` that no page renders.

## Log
- 260816 · [REVISE-CC] findings pass: fence placeholders de-bracketed to PAGE/GROUP/OWNER tokens so the renderer stops mangling them into dead anchors, state: line cut to a row with an open: part, the image-bytes row corrected to the shipped `draw/assets/` home, States now names the two engine facts instead of pointing at Aims, the split box rows turned into label · value with the clause moved below the figure, and the Log's coined terms said plainly.
- 260815 1800 · [JL via CC] this plugin's own skill shipped: `haipipe-plugin-draw` under `page-plugins/` (the round that shipped one small skill per plugin); `haipipe-plugin`'s 67-line excalidraw section became this unit, corrected to the page-folder layout on the way.
- 260815 1650 · [REVISE-CC, JL asked] title, Opening, and Content rewritten to the present contract in plain words; the history that lived there (the ruling, the retired attach button, the migration record) stays in this Log and the archive. The rule itself is now in `ref/writing-rules.md` and `ref/page-template.md`: the page says what IS, the Log keeps the story.
- 260815 1610 · [FIX-CC] the group canvas renders again: `page_board`'s three root probes looked for a `pyproject.toml` no tree here carries, so every GROUP DRAW section (and the Index map's canvas path) blanked silently; the shared `server_root()` now accepts the repo's `.git` as the marker (QO13: serve starts at the repo root). Verified live on QPw: composed canvas + 🖌 Draw tab, owner `this group`.
- 260815 1530 · [REVISE-CC, JL ruled] the renderer follows the ruling: `## Diagram` stages the ascii figure alone (no `✏️ Excalidraw` fold, no attach button: `render_diagram` flattened, `50-xcal.js` deleted); the drawing's one door in the viewer is the 🖌 Draw split, now also a row in the shell's Plugin menu. Excalidraw itself runs locally (docker, 127.0.0.1:5610) behind serve.py's `/_excalidraw` proxy.
- 260815 1420 · [MERGE-CC] QPf2a folded in as Content §3-§7 (JL: one page for the draw plugin); its file is archived as `_archive/QPf2a-linked-drawings.md` and every old id resolves through Links.
- 260815 1420 · [REVISE-CC] rewritten to the plugin contract after the 260815 ruling: Excalidraw leaves ## Diagram, scenes live in page draw/ folders, the attach mechanics retire to the archive.
