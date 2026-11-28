# draw · the family map

Every drawing on an Excalidraw canvas, in one skill: `/hai-draw`. A Studio topic's drawing is the five-part
drawing by default (hai-studio's `scripts/five_parts.py`); a special shape (a screen, a report, a slide draft) is
built on `hai-draw/scripts/draw.py`. Both are written through hai-studio's `canvas.write`, so a rebuild keeps a
person's marks.

Each kind of drawing is a gallery entry, `hai-draw/gallery/<kind>/KIND.md`, with its own scripts, ref and tests.
They are not skills: `/hai-draw <kind>` reads the entry.

```
hai-draw/                    🚪🧭 THE DOOR AND THE LOOK · nine principles, scripts/draw.py, scripts/check.py
hai-draw/gallery/report/     🗺 a scratch packed with real material, or a report's answer and its evidence
hai-draw/gallery/draft/      🗺 a draft drawn: Map (Sections → paragraphs → Bullets → evidence) or Revise (a file's changes, the tracked Word file)
hai-draw/gallery/read/       🗺 one paper on a canvas: its logic, key passages shot, links to our paper
hai-draw/gallery/workflow/   🗺 a paper's building map: data → sources → tests → analysis → claim → Section
hai-draw/gallery/job/        🪜 a Job as a staircase of Tasks and Runs, with each Task's results
hai-draw/gallery/task/       🪜 a Task as a staircase of Runs or videos, with each step's results
hai-draw/gallery/slide/      🎞 a deck proposed on one canvas before it is built (s61-s69)
hai-draw/gallery/ideation/   💡 a paper's ideas as steps down from its question
hai-draw/gallery/story/      💡 a paper's story: its research questions, each with what answers it
```

A Studio topic's structured side, its mind map `sNN-<topic>.mindmap.md`, is not a canvas: hai-mindmap
(`../project/hai-mindmap/`) draws it with the code that draws a draft's §1 Structure map; the workbench card
switches between the two sides (Free · Structured).

Start at `hai-draw/SKILL.md` before drawing any topic. Figures and tables for a document are
hai-display's (`../display/`), not these.
