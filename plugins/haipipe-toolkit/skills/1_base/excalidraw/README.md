# excalidraw · the family map

Every skill that draws on an Excalidraw canvas, in one folder (JL 261016: "we also need a
1_base/excalidraw to put the excalidraw-xxx skills into here"); moved out of `../display/` on 2026-10-16.
A Studio topic's drawing is built by a script on `excalidraw-studio/scripts/draw.py` and written through
haipipe-studio's `canvas.write`, so a rebuild keeps a person's marks.

```
excalidraw-studio/     🧭 THE LOOK · nine principles, draw.py (the helpers every builder imports), check.py
excalidraw-report/     🗺 a scratch packed with real material, or a report's answer and its evidence
excalidraw-draft/    🗺 a draft drawn: Map (Sections → paragraphs → Bullets → evidence) or Revise (a file's changes, the tracked Word file)
excalidraw-read/       🗺 one paper on a canvas: its logic, key passages shot, links to our paper
excalidraw-workflow/   🗺 a paper's building map: data → sources → tests → analysis → claim → Section
excalidraw-job/        🪜 a Job as a staircase of Tasks and Runs, with each Task's results
excalidraw-task/       🪜 a Task as a staircase of Runs or videos, with each step's results
excalidraw-slide/      🎞 a deck proposed on one canvas before it is built (s61-s69)
excalidraw-ideation/   💡 a paper's ideas as steps down from its question
```

A Studio topic's structured side, its mind map `mNN-<topic>.mindmap.md`, is not a canvas: haipipe-studio's mind map
part (`../project/haipipe-studio/_parts/mindmap/`) draws it as the draft's §1 Structure map, in HTML; the workbench
card switches between the two sides (Free · Structured).

Start at `excalidraw-studio/SKILL.md` before drawing any topic. Figures and tables for a document are
haipipe-display's (`../display/`), not these.
