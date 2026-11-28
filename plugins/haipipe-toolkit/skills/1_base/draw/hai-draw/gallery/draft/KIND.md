---
name: draft
part-of: hai-draw
description: "Draws a draft in Excalidraw in three modes: Map (a paper's Sections), Revise (a changed file with its tracked Word file) and Section (one Section on a canvas, synced back). Use to map or edit a draft. Trigger: section canvas, paper map, /hai-draw draft."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "2.5.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw draft · a draft drawn: its map, or its changes

One kind for drawing a draft, in three modes. Each reads a hai-draft draft and draws it on a Studio canvas;
none writes the draft's words.

```text
Map     the Draft plans ─▶ paper · Sections · paragraphs · Bullets · evidence cards    ref/map.md
Revise  their file ─▶ the plan (face yaml) ─▶ draft/ sentences ─▶ side by side ─▶ tracked .docx    ref/revise.md
Section one Section: pages · text · evidence, comments, changes, one frame                      ref/section.md
```

| Mode | When | Read | Script |
|---|---|---|---|
| Map | where each part of a paper sits, what evidence each point waits for | `ref/map.md` | `ref/excalidraw_section.py` |
| Revise | a file we must change, shown before anyone opens Word | `ref/revise.md`, `ref/revise-spec.md` | `ref/read_revise.py`, `ref/track_changes.py` |
| Section | editing one Section: the canvas a draft Task's Studio opens on | `ref/section.md` | `ref/section_canvas.py` |

Read the mode's page before drawing; each page keeps its own rules, commands and boundary.


Boundary
--------

| Owner | Owns |
|---|---|
| `hai-draw draft` | the Map, Revise and Section drawings, the revise plan's grammar, the tracked Word file and its checks |
| `hai-draw` | how every drawing looks |
| `hai-draw read` | reading one paper; its `read_paper.py` cuts and draws the pages Revise shows |
| `hai-draft` | the draft folder's grammar the sentences live in |
| `hai-draft-logic` | the plan and its Bullets the Map draws |
| `hai-draft-writing` | writing and revising the sentences a change touches |
| `hai-studio` | the topic folder, its face, its builder's writer (`canvas.write`) |
