# QPf2-draw-attach · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · Every drawing has one file, and one owner

### C1.P1 · one drawing per owner, each in its owner's folder
- B1 · The two page names in that list are different on purpose.
- B2 · The folder is named for the page id plus its slug.
- B3 · The scene file is named for the page id alone.
- B4 · This page sits in `QPf2-draw-attach/` and its scene is `draw/QPf2.excalidraw`.
- B5 · Each page drawing is a plain Excalidraw file, and it is still useful opened on its own.
- B6 · A pasted image is saved under the owner's `draw/assets/`, and the scene keeps a relative path to it.
- B7 · A page with no drawing yet gets an empty scene the first time its Draw split opens.
- B8 · ⚠️ 5 more sentences in this division are not planned here yet

## C2 · You draw beside the page, never inside it

### C2.P1 · the drawing opens next to the page, never inside it
- B1 · The split names the file it will save to before you draw.
- B2 · So a stroke can never land in another page's scene.
- B3 · The Draw-it button takes an optional ask.
- B4 · Leave it empty, and it turns the page's ascii figure into a real drawing.
- B5 · A drawing Claude made can be drawn again as often as you like.
- B6 · The button refuses to overwrite a drawing a person made by hand.

## C3 · The big group picture is built from the page files, not copied from them

### C3.P1 · what is kept, and what is built for you
- B1 · Opening a group's drawing loads the group scene, pulls in every member page's scene, and places them where the layout says.
- B2 · Inside the group view you work in one mode at a time.
- B3 · You can arrange the pages, edit the group's own layer, or step into one page's scene.
- B4 · Only that owner's file receives the save.
- B5 · Save a page, and the group view shows the change the next time it opens.
- B6 · Nothing is ever merged or pulled in by hand.

## C4 · Two people cannot wipe out each other's work

### C4.P1 · what the server checks before it writes
- B1 · Every save carries the version it started from.
- B2 · So two people on the same drawing cannot quietly overwrite each other.
- B3 · The chat pane gets the same owner address as the canvas.
- B4 · So asking chat to change a drawing writes to that drawing's own file.

