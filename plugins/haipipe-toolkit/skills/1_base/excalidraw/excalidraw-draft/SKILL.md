---
name: excalidraw-draft
description: "Draws a draft in Excalidraw in three modes: Map (a paper's Sections), Revise (a changed file with its tracked Word file) and Section (one Section on a canvas, synced back). Use to map or edit a draft. Trigger: section canvas, paper map, /excalidraw-draft, /excalidraw-section, /excalidraw-revise."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
disable-model-invocation: true
metadata:
  version: "2.5.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /excalidraw-draft · a draft drawn: its map, or its changes

One skill for drawing a draft (b32 s41-D16, JL 261016: "should we make excalidraw-revise and
excalidraw-section to be merged as the excalidraw-draft?"). Both modes read the same thing, a
haipipe-draft draft, and draw it on a Studio canvas; neither writes the draft's words.

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
| `excalidraw-draft` | the Map, Revise and Section drawings, the revise plan's grammar, the tracked Word file and its checks |
| `excalidraw-studio` | how every drawing looks |
| `excalidraw-read` | reading one paper; its `read_paper.py` cuts and draws the pages Revise shows |
| `haipipe-draft` | the draft folder's grammar the sentences live in |
| `haipipe-draft-logic` | the plan and its Bullets the Map draws |
| `haipipe-draft-writing` | writing and revising the sentences a change touches |
| `haipipe-studio` | the topic folder, its face, its builder's writer (`canvas.write`) |
