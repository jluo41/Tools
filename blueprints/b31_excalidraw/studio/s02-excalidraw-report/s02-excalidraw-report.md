s02 · excalidraw-report: a report drawing and a scratch
=======================================================

**Stage:** agreed

**Topic:** what the skill `excalidraw-report` draws and how: its two modes (a scratch, a whiteboard packed with the real
material of a question that a person and an agent mark up together; and a report drawing, a report's answer and its
evidence in named frames), the rules each mode follows, the steps and scripts from material to a finished drawing, where
its files live, and the drawings it has made in this workspace, checked against the drawing principles of b31 s01. It sits
beside s01 (excalidraw-studio, how every Studio drawing reads) and s03 to s05 (the other three drawing skills).

**Feeds:** none yet


Files
-----

```text
s02-excalidraw-report/
├── s02-excalidraw-report.md        this face; the drawing's words are its yaml blocks
├── build_s02_excalidraw_report.py  the builder; reads this face and the skill folder on disk
├── s02-excalidraw-report.excalidraw  four frames in two acts, joined by named arrows
├── s02-excalidraw-report.png       its preview
└── .s02-excalidraw-report.seed.json  generated snapshot for keeping a person's marks
```


What the drawing holds
----------------------

Four frames in two acts, each act a row named at the left (as b10 s52 does); a named arrow for each step; each frame
as large as one screen, its key point in the one slight colour, its density measured in its corner.

```yaml
acts:
- name: Act 1 · What it draws and how
  frames: [①, ②]
  arrow: made with
- name: Act 2 · Where it lives and what it made
  frames: [③, ④]
  arrow: checked on
between: {from: ①, to: ③, label: lives in}
```

```text
Act 1 · What it draws and how       ① the skill, one mind map ─made with─▶ ② two workflows, loops drawn
         │ lives in
Act 2 · Where it lives, what it made ③ its folder, read from disk ─checked on─▶ ④ two real drawings, six checks
```

① 🧠 the skill as one mind map: the centre says what it draws; branches for its two modes, its rules, its steps, its
   scripts, the shared canvas, the comment loop and its boundary; each with a one-line summary drawn large.
② 🔁 how a drawing is made: one workflow per mode, step by step with the script named; the scratch's comment loop and the
   report drawing's rebuild loop are drawn closed.
③ 🧰 the skill folder as a folder tree read from disk, with what each part does, and the facts read from it (version,
   changelog entries, rules, plot helpers).
④ 🖼️ two drawings it made (a report's roadmap, found on disk; the Studio and Report logic tree of b10 s02), each checked
   against the drawing principles, one line each.

Rebuild: `python build_s02_excalidraw_report.py`, then `render_png.py` for the preview.


The skill (the mind map, ①)
---------------------------

```yaml
mindmap:
  centre: excalidraw-report draws a question's material, as a scratch or a report drawing
  branches:
  - title: 🧽 Mode 1 · a scratch
    summary: "a loose whiteboard of real material to think on together"
    by: standing
    leaves:
    - "loose clusters, sticky notes, trees, excerpts, red marks; no template"
    - "a design scratch shows concepts and placeholders, never workspace content"
    - "a results report scratch shows the real counts, names and receipts"
    - "one frame named Questions: each question, our ideas blue, each choice pink"
  - title: 📈 Mode 2 · a report drawing
    summary: "a report's answer and its evidence, in named frames"
    by: standing
    leaves:
    - "first frame: the answer headline plus the strongest evidence"
    - "values, tables, native plots, embedded source figures, the logic"
    - "one Question, one drawing, linked once from its Evidence"
    - "every plot and table carries a clickable source label"
  - title: 📏 The rules
    summary: "dense with the real thing, loose, readable, never patched"
    by: standing
    leaves:
    - "facts read from disk, never typed; aggregates only, no row-level records"
    - "Nunito for words, Cascadia for paths; never a handwritten font (261009)"
    - "a red rectangle around the one wrong line, never an ellipse"
    - "no fenced room to sketch: the whole canvas is the person's"
    - "a generated drawing is rebuilt from its builder, never edited by hand"
  - title: 🪜 The steps
    summary: "read the material, seed the canvas, look at the preview, fix"
    by: standing
    leaves:
    - "read the report, its Results and figures before drawing"
    - "make a short content plan: each finding to a frame and a source"
    - "build, render the PNG, crop each cluster, fix overlaps, rerun"
    - "⏳ later: a scratch has no preview kept in any Block"
  - title: 🛠️ The scripts
    summary: "a plot kit, a picture helper, a renderer, two builders"
    by: standing
    leaves:
    - "ref/plot_kit.py: native plots drawn as Excalidraw shapes"
    - "ref/add_pictures.py: source figures as image elements"
    - "ref/render_excalidraw.py: real Excalidraw in headless Chrome, one frame"
    - "haipipe-studio canvas.py (write) and render_png.py (preview)"
    - "haipipe-report build_report_drawing.py: stack studio frames under a heading"
  - title: 🤝 The shared canvas
    summary: "the script seeds it, the person owns what they draw"
    by: standing
    leaves:
    - "each seed element has an s- id from its content"
    - "a snapshot .<name>.seed.json sits beside the drawing"
    - "a rebuild keeps a person's edits, drops what they deleted"
    - "an open Edit tab can save over a rebuild: reload after one"
  - title: 💬 The comment loop
    summary: "a person marks in red, the agent answers in blue"
    by: standing
    leaves:
    - "a person's elements are the ones without an s- id"
    - "a reply is a seed element from a REPLIES list, beside the mark"
    - "a decision folds into the builder; the marks are never touched"
  - title: 🚧 The boundary
    summary: "one question's working material, not a paper figure"
    by: standing
    leaves:
    - "excalidraw-draft draws a paper's structure from its Draft"
    - "a manuscript figure is a display unit (haipipe-display)"
    - "the report's words belong to haipipe-draft and haipipe-report"
    - "⏳ later: does a report drawing follow the drawing principles?"
```


How a drawing is made (the workflows, ②)
----------------------------------------

```yaml
flows:
- name: A scratch
  labels: [seed, look, mark, read, answer, rebuild, keep]
  loop: "the person reloads the tab and marks again; a rebuild keeps every mark"
  steps:
  - title: 📚 Real material
    lines: ["disk, skills, receipts, runs", "the Questions from board.md"]
  - title: 🧱 Seed script
    lines: ["studio/_build/build_<name>.py", "loose clusters, stickies, trees"]
  - title: 🖼️ Preview
    lines: ["render_png.py", "crop each cluster; fix overlaps"]
    key: true
  - title: 🖍️ Person marks
    lines: ["red notes, rings, arrows", "a mock-up, a crossed-out box"]
  - title: 🔍 Agent reads
    lines: ["elements without an s- id", "what each one points at"]
  - title: 🔵 Blue reply
    lines: ["from a REPLIES list", "beside the mark, never over it"]
  - title: ♻️ Rebuild
    lines: ["canvas.write keeps the marks", "ask for a tab reload"]
- name: A report drawing
  labels: [plan, draw, add, render, link, change, rebuild]
  loop: "a changed report or Result is rebuilt from its builder, never patched"
  steps:
  - title: 📖 Read it all
    lines: ["the report, cited Results", "figures and limits"]
  - title: 🗂️ Content plan
    lines: ["each finding to a frame", "and to its source file"]
  - title: 📐 Builder draws
    lines: ["plot_kit: hbar, compare, share_bar", "values read from the Result"]
  - title: 🖼️ Add figures
    lines: ["add_pictures.py", "source figures as images"]
  - title: 🔎 Render frame 1
    lines: ["render_excalidraw.py --frame first", "the answer must read"]
    key: true
  - title: 🔗 Link once
    lines: ["from the report's Evidence", "one Question, one drawing"]
  - title: ♻️ Rebuild
    lines: ["or build_report_drawing.py", "from studio frames"]
```


Where it lives (the folder, ③)
------------------------------

Real folders, read from disk on every build; the changelog lines are its newest headings, read live. `notes` says what a part does.

```yaml
skill:
  path: plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-report
  open: [ref]
  notes:
    SKILL.md: "both modes, rules, steps"
    CHANGELOG.md: "what changed and why"
    plot_kit.py: "native plots as shapes"
    add_pictures.py: "source figures as images"
    render_excalidraw.py: "one frame to a PNG"
    report-drawing.md: "the report mode's rules"
    elements.md: "sticky, mark, mono helpers"
```


What it made (the pictures, ④)
------------------------------

```yaml
pictures:
- title: "📈 A report drawing: a Question's roadmap"
  find: "reports/*/*-roadmap.png under a Project's work Block"
  caption: "found on disk: {n} report roadmaps in one Block; this is one"
  verdicts:
  - "❌ ① larger than 2800 x 1600; the words are about 14 px"
  - "✅ ② boxes joined by arrows, a JSON panel; not a list"
  - "✅ ④ no folder tree"
  - "❌ ⑤ no key-point colour; small grey words"
  - "➖ ⑥ a picture: not measured"
- title: "🔗 Report mode: Studio and Report, a logic tree"
  find: "b10 studio s02-studio-workbench-skill/studio-and-report.png"
  caption: "screens, what is on disk, and a logic tree"
  verdicts:
  - "❌ ① much larger than one screen (6000 wide)"
  - "✅ ② screens and a logic tree with named arrows"
  - "✅ ③ frames in a row, each Space a frame"
  - "✅ ④ trees only for real folders"
  - "➖ ⑥ screens: not measured"
```


Decided
-------

- s02-D01 · Created (asked 261012: "for the excalidraw report, slide, read, and section, we should have the s02, 03, 04, 05 for them as well"): the topic on excalidraw-report, beside b31 s01 (excalidraw-studio) (JL 261012)
- s02-D02 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the topic shows what excalidraw-report draws and how; its three open points moved to Later


Open
----

(none open: agreed 261012, s02-D02; 3 points moved to Later)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. The report drawings made so far predate the drawing principles: are they one screen with words of 20 px or more, or do they keep the report mode's own larger canvas?
2. No scratch drawing has a preview kept in any Block (only its builder and `.excalidraw`): keep one `.png` per scratch, so this topic can show it?
3. Should the skill name the one slight key-point colour, or keep the report mode black, red and series colours only?

