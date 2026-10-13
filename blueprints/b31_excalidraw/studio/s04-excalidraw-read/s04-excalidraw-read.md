s04 · excalidraw-read: a paper read onto a canvas, and a file we revise
=======================================================================

**Stage:** agreed

**Topic:** what the skill `excalidraw-read` draws and how. It reads one paper's PDF onto a canvas: the paper's
logic as a chain, its key passages shot from the PDF with the quoted words highlighted, a comment on each, and
how each passage links to a claim of our paper. Its second mode, revise, reads a file we are asked to change (a
co-author's Word file) and shoots one picture per section with the planned changes in red. This topic draws both
modes in one place, beside b31 s01 (the principles of a Studio drawing) and s21 (the revise mode, measured on a
real drawing); it does not repeat s21. The version, the ref files, the commands and the three real canvases are
read from disk on every build.

**Source:** `plugins/haipipe-toolkit/skills/1_base/display/excalidraw-read/` (SKILL.md, CHANGELOG.md, ref/), and the
three canvases the revise mode made on 2026-10-11 in WellDoc-SPACE (`examples-0-cowork/Project-SHIFT-Study/cowork/`,
b02, b03, b04).

**Feeds:** no Question yet (b31 has no `reports/`).


Files
-----

```text
s04-excalidraw-read/
├── s04-excalidraw-read.md          this face; the yaml blocks below are the drawing's words
├── build_s04_excalidraw_read.py    the builder
├── s04-excalidraw-read.excalidraw  the drawing; a person's marks are kept on rebuild
└── s04-excalidraw-read.png         its preview
```

Rebuild: `python build_s04_excalidraw_read.py` (it writes the preview too).


What the drawing holds
----------------------

```text
act 1  What it draws:                 ① the skill as a mind map ── its read mode, step by step ──▶ ② the read mode as a workflow
act 2  Where it lives, what it made:  ③ its folder, as a folder tree ── its output, seen ──▶ ④ three canvases it made
```

```yaml
acts:
- name: Act 1 · What it draws
  frames: [①, ②]
  arrow: its read mode, step by step
- name: Act 2 · Where it lives and what it made
  frames: [③, ④]
  arrow: its output, seen
between: {from: ①, to: ③, label: lives in}
```


The words of frame ①: the skill as a mind map
---------------------------------------------

```yaml
mindmap:
  centre: "excalidraw-read: one file read onto a canvas, in two modes"
  branches:
  - title: "📄 Read mode"
    by: standing
    summary: "A paper's logic as a chain, its key passages shot from the PDF, each linked to our paper."
    leaves:
    - "four frames: Paper logic, Link to our paper, Questions, Excerpts"
    - "5 to 9 passages, each with Says, Comment and a link"
    - "a quote is found by its words and highlighted in place"
    - "reading.yaml is the one file an agent writes by hand"
  - title: "📝 Revise mode"
    by: standing
    summary: "A co-author's Word file, one shot per section, the planned changes in red."
    leaves:
    - "a plan in the face's yaml: find, new, why, evidence needed"
    - "sentence mode, then a tracked Word file built last"
    - "measured on a real drawing in b31 s21, not repeated here"
    - "one row per section, each note level with its words"
  - title: "🛠️ Its scripts"
    by: standing
    summary: "Three scripts in ref/, run from the command line."
    leaves:
    - "{read_paper_commands}"
    - "{read_revise_commands}"
    - "track_changes.py writes the tracked changes"
    - "run with the repo's .venv python"
  - title: "📏 Its rules"
    by: standing
    summary: "The paper's own words, highlighted in place; nothing retyped."
    leaves:
    - "every passage links or says why not"
    - "a corrected number is dated in its comment"
    - "words stay 20 px or more; frames fit one screen"
  - title: "🔗 Link to our paper"
    by: standing
    summary: "Each passage is tied to one of our claims by one of five relations."
    leaves:
    - "{relations}"
    - "targets carry our paper's real ids, never invented"
    - "a claim with no passage says so, in red"
  - title: "🤝 A shared canvas"
    by: standing
    summary: "The person's marks survive every rebuild."
    leaves:
    - "written through canvas.write, a seed snapshot beside the drawing"
    - "a red mark is read, folded into reading.yaml, then rebuilt"
    - "needs poppler, Pillow and PyYAML"
```


The words of frame ②: the read mode as a workflow
-------------------------------------------------

```yaml
flow:
  steps:
  - title: "1 · Get the text"
    lines:
    - "read_paper.py text"
    - "paper.txt, page-marked, with figure and table captions"
    - "the PDF stays in the ignored _WorkSpace/"
  - title: "2 · Read, then write the reading"
    key: true
    lines:
    - "an agent reads the paper and our paper's claims"
    - "reading.yaml: 5 to 8 logic steps, 5 to 9 passages, the links"
    - "the paper, not every corner"
  - title: "3 · Shoot the passages"
    lines:
    - "read_paper.py shoot"
    - "each quote found by its words, highlighted, cropped to 3 lines"
    - "a table or figure takes a box, not a quote"
  - title: "4 · Draw the canvas"
    lines:
    - "read_paper.py draw, or all for 3 and 4"
    - "four frames and a .png preview"
    - "the person's marks kept"
  - title: "👤 5 · Look and decide"
    lines:
    - "match 1.00 ok; below 0.8 the quote is recopied"
    - "the open questions are the person's to answer"
    - "an answer goes back into reading.yaml"
  labels: [text, yaml, shots, canvas]
pointer:
  title: "📝 The revise mode is the same reading turned on a file we change"
  lines:
  - "its steps, its scripts and the seconds each takes: b31 s21-revise-mode-workflow"
  - "this frame draws only the read mode"
canvas_frames:
- {name: Paper logic, what: "the argument, one box per step, each naming the passages it rests on"}
- {name: Link to our paper, what: "each of our claims with the passages that touch it"}
- {name: Questions, what: "what the person must decide, in red"}
- {name: Excerpts, what: "one card per passage: the shot, Says, Comment, the link"}
```


The words of frame ③: where it lives
------------------------------------

```yaml
folder:
  path: plugins/haipipe-toolkit/skills/1_base/display/excalidraw-read
  open: [ref]
  notes:
    read_paper.py: "read mode: text, boxes, shoot, draw, all"
    read_revise.py: "revise mode: draw, edits, seed, deliver"
    reading-spec.md: "the reading.yaml an agent writes"
    revise-spec.md: "the plan yaml of a revise"
    track_changes.py: "writes the tracked changes"
  why: "A skill folder: SKILL.md says how, ref/ holds the two modes' scripts and the specs of their yaml."
  also:
  - "Its drawing helpers are not here: canvas.write and render_png.py are haipipe-studio's."
  - "Its look is excalidraw-studio's: this topic follows its principles."
```


The words of frame ④: what it made
----------------------------------

All three are revise-mode canvases from 2026-10-11 (the SHIFT cowork Blocks, in WellDoc-SPACE). Only the top of each
preview is shown. No paper-mode canvas could be found in this workspace (see Open 1).

```yaml
canvases:
- {block: b04_prep_ai, path: examples-0-cowork/Project-SHIFT-Study/cowork/b04_prep_ai/studio/s04-task31-updated-draft/s04-task31-updated-draft}
- {block: b03_event_cgm, path: examples-0-cowork/Project-SHIFT-Study/cowork/b03_event_cgm/studio/s04-task21-updated-draft/s04-task21-updated-draft}
- {block: b02_aid_ai, path: examples-0-cowork/Project-SHIFT-Study/cowork/b02_aid_ai/studio/s04-task32-updated-draft/s04-task32-updated-draft}
picture_note: "Each canvas checked against the drawing principles, one line each, read from its own .excalidraw."
```


Decided
-------

s04-D01 · Created (asked 261012: "for the excalidraw report, slide, read, and section, we should have the s02, 03, 04, 05 for them as well"): the topic on excalidraw-read, beside b31 s01 (excalidraw-studio); its revise mode stays in b31 s21.
s04-D02 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the topic shows excalidraw-read's read mode, step by
    step; its three open points moved to Later, and step 5 is the person's step (👤), not an open point.


Open
----

(none open: agreed 261012, s04-D02; 3 points moved to Later)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. No paper-mode canvas (a `reading.yaml` with its shots) exists in this workspace; the worked example the skill names (`Knowledge-Base/.../salvi-2024-gpt4-persuasion/`) is not here. Read mode is drawn from its spec and code, not from a measured run.
2. The side-by-side frame of the revise canvases is wider than the 2,800 px rule (kept for the three note columns); is that still acceptable under the principles of b31 s01?
3. Read mode has no timing like s21's seconds per rebuild; should one paper read be measured?

