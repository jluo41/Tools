# Drawing with a builder

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


A builder draws the topic from what is on disk, so a rebuild follows the code and the files
while keeping everything a person drew.

```python
sys.path.insert(0, str((HERE / "<relative path to haipipe-studio/scripts>").resolve()))
import canvas
canvas.write(out, els, "build_sNN_<topic>.py", redraw_frames=())
```

1. **canvas.write** gives each element a stable id from its content and merges with the canvas
   on disk against the last build's snapshot (`.sNN-<topic>.seed.json`, beside the drawing):
   anything the person added stays; a seed element the person edited stays; one they deleted
   stays deleted; every other seed element is redrawn. Frames are layout: the builder owns them.
2. **Check before regenerating**: a person's edits are detected by the snapshot, never by
   Excalidraw's `version` field (a save re-stamps them all).
3. **Never hand-edit the output**: change the builder or what it reads, then rerun it.
4. **Preview**: `render_png.py <drawing> <png> [scale]` draws a PNG with Pillow; Excalidraw
   shows the real drawing.
5. **A Block's make.sh**: `studio/_build/make.sh` reruns every builder of the level and every
   preview, so one command rebuilds the whole studio.
6. **Marks**: an open point drawn in red. Every change to a drawing, asked for or found on a
   redraw, gets a short green note right where it changed (`✎ <YYMMDD> <what changed>`, made by
   `canvas.change_note`), never a list of changes in the title frame or a corner (JL 261010; JL 261007: "leave the short green
   comments to where we changed"). Old notes stay; a note goes only with the thing it marks. A slide
   draft keeps a note about one slide only under that slide (`excalidraw-slide`, JL 261008).

`new_topic.py topic … --builder` writes a builder of this shape and runs it once: by default the five-part drawing
(`build_sNN_<topic>.py` on `five_parts.py`, its `design()` from `sketch_<topic>.py`'s A · B · C, written by
`five_parts.marks_writer`, which is `canvas.write` with `palette=False`); `--builder draw` one on excalidraw-studio's
`draw.py`, for a special shape (a screen, a report, a slide draft).
