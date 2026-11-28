# Drawing with a builder

Part of hai-studio's topic contract (`ref/topic-contract.md`).

A builder draws the topic from what is on disk, so a rebuild follows the code and the files while keeping
everything a person drew.

```python
sys.path.insert(0, str((HERE / "<relative path to hai-studio/scripts>").resolve()))
import canvas
canvas.write(out, els, "build_sNN_<topic>.py", redraw_frames=())
```

## Which builder

1. **`new_topic.py topic … --builder`**: the five-part drawing. Writes `build_sNN_<topic>.py` on `five_parts.py` and
   `sketch_<topic>.py` with the Design's A · B · C stubs, and runs it once. The five parts: 1 Idea, 2 Now, 3 Design
   (A the pieces step by step, B how it grew, C the open choices as stickies), 4 Process, 5 Delivery.
2. **`--builder draw`**: a builder on hai-draw's `draw.py`, only for a special shape (a screen, a report, a
   slide draft). Load `/hai-draw` and follow its "Redraw a topic".
3. **No `--builder`**: `quick_draw.py`'s light quick drawing, to mark up by hand.

An existing topic keeps its drawing until someone redraws it.

## Fill it, then redraw

1. Fill the builder's SPEC from the face and the sketches from the topic; rerun the builder.
2. `check.py` (hai-draw's) says which parts or placeholders are missing.
3. A data topic (`**Delivery type:** data`): its sketch A is the data built step by step, a small table per step
   with its real columns and made-up rows (`five_parts.data_table`, `data_step`).
4. Render the preview: `render_png.py <drawing>.excalidraw <drawing>.png`.

## What canvas.write keeps

1. **Stable ids, merged on write**: each element gets an id from its content and is merged with the canvas on disk
   against the last build's snapshot (`.sNN-<topic>.seed.json`, beside the drawing). What the person added stays; a
   seed element the person edited stays; one they deleted stays deleted; every other seed element is redrawn. Frames
   are layout: the builder owns them.
2. **Edits found by the snapshot**, never by Excalidraw's `version` field (a save re-stamps them all).
3. **Never hand-edit the output**: change the builder or what it reads, then rerun it.
4. **Marks**: an open point is drawn in red; every change gets a short green note where it changed
   (`canvas.change_note`, `ref/topic-look.md` § Change notes).

## Read it as a reader, then call the reviewer

A passing `check.py` is not done. Answer the reader's questions for the topic's kind (Job, Task, video or Run frame)
from the rendered frames alone. Then call `hai-studio-reviewer-agent` in a fresh context, fix its gaps in the
face or the builder, and repeat until it returns `answers`. The questions and the loop: `ref/reader-review.md`.
