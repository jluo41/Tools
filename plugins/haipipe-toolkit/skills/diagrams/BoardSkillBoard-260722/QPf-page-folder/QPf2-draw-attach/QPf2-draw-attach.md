# Draw · every page keeps its own drawing
state: 🟡 PARTIAL · scenes in page draw/, split + group view live · open: draw.py layout, old link route
owner: CC
method: one Excalidraw scene per page in the page's own draw/ folder; the page body carries only the ascii figure
session: da5c5ec9-ee25-4017-bd12-49324c28ae43

## Opening
Where does a page's drawing live, and how do you work on it?
Every page can have a drawing.
It is an Excalidraw scene, one file anyone can open, edit, and talk over.
The file sits in the page's own `draw/` folder, so it travels with the page and lives in git like every other file.
The page body shows only the ascii figure in `## Diagram`, which reads anywhere, even with scripts off.
To see or edit the real drawing, open the page's Draw split.
A group page pulls every member's drawing into one large view.

**Where this page sits**: `QPf1` says a page owns its folder and every subfolder is a plugin; this page owns the `draw/` plugin.
`QO5` owns the split workspace a drawing opens in, and `QO11` owns two people editing at once.

## Diagram
**The drawing's three homes**: the page shows ascii, the draw folder holds the scene, the group builds one view from them all.
```text
  📋 the PAGE, on stage                 🖌 the PLUGIN, beside it
  ┌───────────────────────────┐        ┌──────────────────────────┐
  │ ## Diagram                │        │ PAGEDIR/draw/            │
  │   ascii only · scripts-   │        │   PAGEID.excalidraw      │
  │   off readable            │  tab   │   scene · page-owned     │
  │ ## Content …              │ ──────▶│   edit · in the split    │
  │   (no embeds anywhere)    │  🖌     │   save · to this file    │
  └───────────────────────────┘        └──────────────────────────┘
                                              │ composed, never copied
  🗂 GROUPDIR/draw/group.excalidraw    ◀──────┘
     relationships + layout · import manifest over the page sources
```
The arrow into the group file runs one way.
The group scene keeps only where each drawing goes and a list of which drawings to pull in.
So a page's scene is read into the group view, never copied into it.

## Content
### 1 · Every drawing has one file, and one owner
**The files**: one drawing per owner, each in its owner's folder.
```text
📄 page drawing     PAGEDIR/draw/PAGEID.excalidraw    the page's own scene
🗺 group drawing    GROUPDIR/draw/group.excalidraw    layout + relations over the pages
🧭 board map        board.excalidraw                  the Index page's overview scene
🖼 image bytes      draw/assets/OWNER/                pasted images, kept out of the scene
```
📌 This part says which file holds which drawing, so you always know what to open.

The two page names in that list are different on purpose.
The folder is named for the page id plus its slug.
The scene file is named for the page id alone.
This page sits in `QPf2-draw-attach/` and its scene is `draw/QPf2.excalidraw`.
Each page drawing is a plain Excalidraw file, and it is still useful opened on its own.
A pasted image is saved under the owner's `draw/assets/`, and the scene keeps a relative path to it.
A page with no drawing yet gets an empty scene the first time its Draw split opens.
So there is never a missing file to trip over.
The group drawing holds only the group's own layout and a list naming each page's scene.
It never copies what those scenes contain.
`board.excalidraw` stays at the board root as the Index page's overview map.
Everything below it follows the new layout: one scene per page, one per group.

### 2 · You draw beside the page, never inside it
**The Draw split**: the drawing opens next to the page, never inside it.
```text
🖌 open        Plugin ▾ → Draw, or the Draw tab in the right pane
✏️ edit        draw on the canvas; saves go to this page's own scene file
✨ generate    the Draw-it button: Claude draws the page's ## Diagram for you
🔄 follow      navigate to another page and the canvas follows it
```
📌 This part says how to open a drawing, how to edit it, and how to ask Claude to draw it for you.

The split names the file it will save to before you draw.
So a stroke can never land in another page's scene.
The Draw-it button takes an optional ask.
Leave it empty, and it turns the page's ascii figure into a real drawing.
A drawing Claude made can be drawn again as often as you like.
The button refuses to overwrite a drawing a person made by hand.

### 3 · The big group picture is built from the page files, not copied from them
**One large drawing from many small ones**: what is kept, and what is built for you.
```text
💾 kept       each page's scene · the group's own layer · where each one goes
⚙️ built      one group view, built again on every open
🔒 owner      every shape keeps its owner, so an edit goes back to the right file
```
📌 This part says the group picture is put together from the page files each time it opens.

Opening a group's drawing loads the group scene, pulls in every member page's scene, and places them where the layout says.
Inside the group view you work in one mode at a time.
You can arrange the pages, edit the group's own layer, or step into one page's scene.
Only that owner's file receives the save.
Save a page, and the group view shows the change the next time it opens.
Nothing is ever merged or pulled in by hand.

### 4 · Two people cannot wipe out each other's work
**The safe save**: what the server checks before it writes.
```text
📥 opened     the revision the editor loaded
📤 save       owner · that revision · the changed elements
✅ accepted   the file has not moved since
⚠️ conflict   someone else saved first · reload and compare
```
📌 This part says every save is checked first, so nobody quietly loses work.

Every save carries the version it started from.
So two people on the same drawing cannot quietly overwrite each other.
The chat pane gets the same owner address as the canvas.
So asking chat to change a drawing writes to that drawing's own file.

## Aims
- [x] 🚚 Every page's drawing sits in that page's own draw/ folder
      61 scenes moved and renamed to current page ids, and only group.excalidraw is left at group level.
- [x] 🧹 No page puts an Excalidraw canvas inside ## Diagram
      The frame links are gone from all 19 pages that carried one, and Diagram holds ascii only.
- [ ] ⚙️ draw.py works with the new folder layout
      The group scene is the group folder's, each page scene is its own, the import lists point at the new paths, and verify passes on this board.
- [x] 🖼 The group picture shows up again
      page_board.group_canvas now starts from the group folder instead of the members' shared parent.
- [ ] 🗑 The unused Excalidraw+ route is switched off
      `/_board/excalidraw` writes a hosted scene link into `## Diagram` that no page draws, and it goes; `/_board/excalidraw-save` saves a page's own scene, and it stays.

## States
The drawings themselves are in place: every page scene sits in its page's folder, the split opens and follows the page, and the group view builds.
`## Diagram` holds ascii only on every live page, and the one Excalidraw link left sits in `_archive/QA0-board-map.md`.
draw.py's verify still checks the old `board.excalidraw` at the board root instead of the new page layout.
One blocker sits in front of that: `draw.py verify` stops on this board with "Group QA imports do not match board.md".
The cause is `QA-design/draw/group.excalidraw`, which still pulls in the QA0 and QA1 scenes after both pages left the list.
So §3's group view does not build for that group today.
serve.py still accepts `/_board/excalidraw`, the old Excalidraw+ route that writes a hosted scene link into `## Diagram` that no page draws.
The other route, `/_board/excalidraw-save`, saves a page's own scene, is in daily use, and is not the one to switch off.

## Log
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我他妈真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 12 sentences flagged before, 7 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260816 · [REVISE-CC] second findings pass
      Seven findings applied, each checked against the engine source before the sentence was written.
      JL ruled the `page-type: design` line off the head: this page is a settled contract that never weighed candidates, so it is a plain Q decision page and must not close under the design contract.
      The first pass had collapsed two different placeholders into one token, which made the page claim a scene is named after its page folder; the fences now carry `PAGEDIR/draw/PAGEID.excalidraw`, and §1 says the stem is the page id alone, with this page's own `QPf2-draw-attach/draw/QPf2.excalidraw` as the example.
      The retirement target is named correctly at last: `/_board/excalidraw` is the Excalidraw+ mint that writes a hosted link into `## Diagram` (serve.py 506, xcal.py `new_excalidraw`), while `/_board/excalidraw-save` is the live page-scene save (serve.py 321), so the old wording pointed the retirement at the working save path.
      States gained the current blocker under §3 and the missing fact for the ascii-only Aim: `draw.py verify` aborts on `QA-design/draw/group.excalidraw`, which still imports the QA0 and QA1 scenes after both pages folded into QA00, and no live page's `## Diagram` carries an Excalidraw link.
      §1 now says the root `board.excalidraw` stays the Index map while the folded layout owns the page and group scenes, and the Diagram's closing line was replaced with the one thing only that figure shows, the one-way composition arrow.
- 260816 · [REVISE-CC] first findings pass
      Five findings applied to the head, the fences, and States.
      The angle-bracket placeholders in the fences were replaced with plain tokens, the `state:` line was cut down to a row with an `open:` part, and the image-bytes row was corrected to the shipped `draw/assets/` home.
      States stopped pointing at the Aims and started naming the engine facts, and the split box's rows became label and value with the clause moved out of the fence and under the figure.
- 260815 1800 · [JL via CC] this plugin's own skill shipped: `haipipe-plugin-draw` under `page-plugins/` (the round that shipped one small skill per plugin); `haipipe-plugin`'s 67-line excalidraw section became this unit, corrected to the page-folder layout on the way.
- 260815 1650 · [REVISE-CC, JL asked] title, Opening, and Content rewritten to the present contract in plain words; the history that lived there (the ruling, the retired attach button, the migration record) stays in this Log and the archive. The rule itself is now in `ref/writing-rules.md` and `ref/page-template.md`: the page says what IS, the Log keeps the story.
- 260815 1610 · [FIX-CC] the group canvas renders again: `page_board`'s three root probes looked for a `pyproject.toml` no tree here carries, so every GROUP DRAW section (and the Index map's canvas path) blanked silently; the shared `server_root()` now accepts the repo's `.git` as the marker (QO13: serve starts at the repo root). Verified live on QPw: composed canvas + 🖌 Draw tab, owner `this group`.
- 260815 1530 · [REVISE-CC, JL ruled] the renderer follows the ruling: `## Diagram` stages the ascii figure alone (no `✏️ Excalidraw` fold, no attach button: `render_diagram` flattened, `50-xcal.js` deleted); the drawing's one door in the viewer is the 🖌 Draw split, now also a row in the shell's Plugin menu. Excalidraw itself runs locally (docker, 127.0.0.1:5610) behind serve.py's `/_excalidraw` proxy.
- 260815 1420 · [MERGE-CC] QPf2a folded in as Content §3-§7 (JL: one page for the draw plugin); its file is archived as `_archive/QPf2a-linked-drawings.md` and every old id resolves through Links.
- 260815 1420 · [REVISE-CC] rewritten to the plugin contract after the 260815 ruling: Excalidraw leaves ## Diagram, scenes live in page draw/ folders, the attach mechanics retire to the archive.
