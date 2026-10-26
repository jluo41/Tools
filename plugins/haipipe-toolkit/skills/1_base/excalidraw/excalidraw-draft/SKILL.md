---
name: excalidraw-draft
description: >-
  Draw a draft in Excalidraw, in one of three modes. Map: a paper's Sections, or one Section, read
  left to right (Sections, paragraphs, each Bullet a row, a Text column, an evidence card per
  Evidence Item), generated from the Draft plans. Revise: a file we change (a co-author's Word
  file, an IRB protocol for a Change in Research), each section's page beside the updated
  sentences, a note per change, and last the tracked Word file, checked both ways. Section: one
  Section on one canvas for editing it, the file's pages left, the text middle, evidence, comments
  and changes right (ref/section_canvas.py; sync reads the canvas back into the draft). Use for a section canvas, edit this section,
  sync the canvas, a
  paper map, a Section map, "draw the sections", "what do we change in this file", "show the
  changes to the draft", a tracked-changes file built from a plan, a CIR or amendment,
  /excalidraw-draft, /excalidraw-section, /excalidraw-revise.
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
