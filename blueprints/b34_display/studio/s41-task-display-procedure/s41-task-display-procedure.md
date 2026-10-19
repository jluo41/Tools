s41 · Display procedure: from a sentence that needs a figure to a figure you accepted
=====================================================================================

**Tags:** `Levels`

**Stage:** shaping

**Topic:** every step of making one display (a figure or a table) for one page of a draft Task, drawn the way b32 s41
draws the draft Task: one workflow map of who does what, then acts, each a row of screens. A display is one unit
folder, `<task>/display/Display<n>-<slug>/`, built on evidence cards, accepted by a person, shown on the Section
canvas and copied into delivery only when built. The worked example is the Task 2.1 Overview Figure (SHIFT, b21),
cited by the sentence "The work will proceed in three steps (Overview Figure)." (C3.P6 · B7 · S7 of
`task21-draft-v1.11.md`; the figure itself is Section C8). It is NOT yet a display unit; the drawing says so in red.
Asked by JL 261016 ("for the b33 and b34, could we have the things like b32-s41? to show how things work step by
step?"). What a display is stays haipipe-display's; this topic draws its steps.

**Feeds:** none yet (b34 has no `reports/`)


Files
-----

```text
s41-task-display-procedure/
├── s41-task-display-procedure.md            this face; the drawing's words are the yaml block below
├── build_s41_task_display_procedure.py      the builder (b32 s41's map, screens and pictures, copied and cut)
├── s41-task-display-procedure.excalidraw    ① the workflow map; Ⓐ the homes today; Ⓑ one unit's folder, real and
│                                            proposed; ② ③ need and kind, ④ ⑤ the unit, ⑥ ⑦ render and check,
│                                            ⑧ accept, ⑨ ⑩ show, ⑪ deliver
└── s41-task-display-procedure.png           its preview
```

Read from disk on every build: the Overview Figure picture and b21 s05's canvas picture (both under the b21 Block).

```yaml
heading: ["① The display procedure: who does what", "a sentence that needs a figure → a figure you accepted, shown, then built into delivery"]
key: "Outcome: one unit folder per figure or table, built on evidence cards, with your accepted: tick; it shows on the canvas, and delivery holds only a built copy. Only you accept."
problem: "🎯 Problem: about 260 units live in three homes, none says what evidence it is built on, and no one checks that a figure's numbers match the sentence that cites it; the Overview Figure is a pptx and a png with no folder."
novelty: "🏆 What it gives: one home, the Task's display/ (✨1) · built_on: cards, and a check that the numbers agree (✨2) · your accepted: tick, never a score (✨3) · a missing display flagged as a proposal, as evidence does."
marks: [[2, 0, "✨1"], [4, 0, "✨2"], [5, 0, "✨3"]]
lanes: ["📄 display/ · the unit", "🧾 evidence/ · cards", "🤖 display agent", "🔍 the check", "👤 you"]
lane_w: [380, 330, 380, 360, 330]
symbols:
  title: "📐 Words: the parts of a display, and who writes them"
  rows:
  - ["Display<n>", "one unit folder: one figure or table"]
  - ["recipe/", "what draws it: script, spec, prompt or pptx"]
  - ["intake/", "the small approved data it reads"]
  - ["assets/", "the picture or table body it made"]
  - ["built_on:", "the evidence cards its numbers come from"]
  - ["accepted:", "your name and date; only you write it"]
  - ["🔍 dashed box", "does not exist yet"]
  - ["✍", "a step only you do"]
map:
- step: "📝 Need and kind"
  screens: "② ③"
  cells: [[4, "say it", "the sentence", "a need: S7 wants a figure"], [2, "pick(kind)", "the need · the route table", "one of five renderers"]]
  text: "display/: none yet"
- step: "🧾 Evidence"
  screens: "④"
  cells: [[2, "name(cards)", "evidence/cards.yaml", "built_on: the cards"]]
  plan: "cards it reads"
- step: "📂 The unit"
  screens: "⑤ ⑥"
  cells: [[2, "make(unit)", "the kind · built_on", "Display1-<slug>/: recipe · intake · README"]]
  text: "the unit's folder"
- step: "🖼 Render"
  screens: "⑦"
  cells: [[2, "render(recipe)", "recipe/ · intake/", "assets/ · preview.pdf"]]
  text: "assets/ · preview.pdf"
- step: "🔍 Check"
  screens: "⑧"
  cells: [[3, "🔍 match(numbers, cards)", "the figure's numbers · the cards", "same, or a list of differences"]]
  plan: "a check we lack"
- step: "✍️ Accept"
  screens: "⑨"
  cells: [[4, "✍ Accept", "preview.pdf", "accepted: <name> <date>"]]
  text: "README: accepted:"
- step: "🎞 Show"
  screens: "⑩ ⑪"
  cells: [[2, "draw(canvas)", "display/ · the cards", "the Displays card"], [4, "read", "the box in the text", "the figure it points to"]]
  text: "shown, not copied"
- step: "📤 Deliver"
  screens: "⑫"
  cells: [[2, "build(copy)", "the accepted unit", "<block>/delivery/<jNN>/<tNN>/"], [4, "✍ Send", "the built files", "sent, by you"]]
  text: "a built copy, never edited"
homes:
  frame: "Ⓐ Where displays live today, and where they go"
  sub: "about 260 units (WellDoc 16, DrFirst 102, Physician 144, REACH 1; b34 board.md, 261016), none yet with built_on: in its README"
  columns: ["Home", "path", "what it is"]
  rows:
  - ["Page Result payload", "<page>/results/<run>/payload/<unit>/", "the unit contract's home for an old Page; 66 found in DrFirst and Physician"]
  - ["older display/ lane", "…/evidence/display/<unit>/", "before Page Results; 98 found, 5 shown under legacy-outline-evidence"]
  - ["built copy", "<paper>/delivery/latex/displays/<unit>/", "a copy made for the paper; 5 found"]
  - ["🆕 the Task's display/", "<task>/display/Display<n>-<slug>/", "the one home to move to: beside draft/ and evidence/"]
  note: "❓ Open 2: what moves and what is only read. The counts are folder counts found 261016, not units checked one by one."
folders:
  frame: "Ⓑ One unit's folder: a real one, and the one Display1 would be"
  sub: "left: a real unit (Physician-SPACE, a Page Result payload) · right: the Overview Figure as a unit of Task 2.1, not made yet"
  tree: |
    Display3-cross-family-stability/        a real unit
    ├── README.md        claim · status: rendered
    ├── intake/
    │   ├── manifest.yaml
    │   └── inputs/01-cross_family_per_trait.tex
    ├── recipe/generate.py
    ├── float.tex        caption · label (the caller's)
    ├── preview.tex
    ├── preview.pdf
    └── assets/table-body.tex
  tree2: |
    <task>/display/Display1-overview-figure/     not made yet
    ├── README.md        claim · kind · built_on: · accepted:
    ├── intake/          manifest.yaml · inputs/
    ├── recipe/          the .pptx · export.md
    ├── assets/figure.pdf
    ├── float.tex        caption · label
    └── preview.pdf
  notes:
  - "The real unit's README holds a claim and a status; no README in the three homes has built_on: or accepted: yet."
  - "❓ The Overview Figure today: a pptx and pngs under b21/studio/s03-related-work-structure/ and a copy under b21/delivery/studio/s03-related-work-structure/render/ (v10 to v25). No recipe/, no README, no accepted:."
screen:
  task: "Task · 2.1"
  line: "Draft · Block b21 · Task 2.1 · the Overview Figure (C8), cited by C3.P6 · B7 · S7"
  tabs: ["Studio", "1 · Plan", "2 · Write", "3 · Evidence", "4 · Revise", "Delivery"]
tabs:
- act: "Act 2 · Need and kind"
  step_arrow: "a need"
  key: "A sentence points at a figure. First say what the figure is for and which of the five kinds it is; the door haipipe-display routes by kind. Nothing is drawn yet."
  states:
  - title: "② Display · 1 of 2: a sentence that needs a figure"
    tab: "3 · Evidence"
    step: "🖼 Display · need"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Sentence: "C3.P6 · B7 · S7 in task21-draft-v1.11.md", Words: "The work will proceed in three steps (Overview Figure).", Needs: "a picture of the three steps", Reads: "evidence/cards.yaml"}
    prompt: "/haipipe-display <task> need: S7 points to the Overview Figure; say which kind it is and what it must be built on."
    mark: "copy it, run it in Claude or Codex; the Display step has no tab of its own yet (Open 1)"
    arrow: "the agent picks a kind"
  - title: "③ Display · 2 of 2: the kind, by the route table"
    tab: "3 · Evidence"
    step: "🖼 Display · kind"
    chip: "→ next"
    boxes:
    - title: "haipipe-display routes by kind"
      rows: {Table: "📊 haipipe-display-table: numbers as a typeset table", Plot: "📈 haipipe-display-figure: numbers as a plot", Diagram: "📐 haipipe-display-diagram: a concept as an editable SVG", Picture: "🎨 haipipe-display-illustration: an AI concept figure", TeX: "✒️ haipipe-display-tex: TikZ, algorithm, equation; a person writes it"}
    - title: "The Overview Figure"
      dashed: true
      rows: {Kind: "📐 a concept figure; PowerPoint is an allowed way to author it", Values: "none: a concept figure shows no numbers", Made: "as a pptx, then a png (s03, v25)"}
    prompt: "/haipipe-display <task> route: S7's Overview Figure is a concept figure; start its unit."
    mark: "red: the Overview Figure is not a display unit yet; copy this to start it"
    arrow: "the agent starts the unit"
- act: "Act 3 · The unit on disk"
  step_arrow: "the unit"
  key: "One folder per display, in the Task's display/, beside draft/ and evidence/. Its README says what it is built on; its recipe and data make the render, so anyone can draw it again."
  states:
  - title: "④ Display · built on evidence"
    tab: "3 · Evidence"
    step: "🖼 Display · built_on"
    chip: "→ next"
    boxes:
    - title: "built_on: the cards the numbers come from"
      rows: {Plot or table: "built_on: WORK 1 (a card of evidence/cards.yaml), read by cards.py", Concept: "a concept figure shows no numbers, so built_on: is empty", Overview: "no card exists for it; built_on: stays empty"}
    prompt: "/haipipe-display <task> unit: make Display1-overview-figure; write built_on: from the cards it reads, or none."
    mark: "red: today no README holds built_on:; copy it to write the first one"
    arrow: "the agent makes the folder"
  - title: "⑤ the unit's folder, a real one and Display1"
    tree: true
- act: "Act 4 · Render and check"
  step_arrow: "render"
  key: "The renderer draws from recipe/ and intake/ and compiles preview.pdf. Then the numbers in the picture are matched against the cards. A number typed straight into float.tex is a defect."
  states:
  - title: "⑥ Display · 1 of 2: render"
    tab: "3 · Evidence"
    step: "🖼 Display · render"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Recipe: "recipe/: script, FigureSpec, prompt or pptx", Data: "intake/inputs/: small approved extracts only", Writes: "assets/ · float.tex · preview.pdf", Rule: "a number typed into float.tex is a defect"}
    prompt: "/haipipe-display <task> render Display1: draw it from recipe/, compile preview.pdf, then stop for my Accept."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent renders"
  - title: "⑦ Display · 2 of 2: check the numbers against the cards"
    tab: "3 · Evidence"
    step: "🔍 Display · check"
    chip: "→ next"
    boxes:
    - title: "Check · figure vs cards"
      dashed: true
      rows: {Figure: "<a number in preview.pdf>", Card: "<the item's value: its file and key>", Same: "yes, or the list of differences"}
    sections:
    - {t: "✅ evidence: cards.py check (every address, fact, anchor)"}
    - {t: "⬜ display: no check of a figure's numbers against the cards"}
    - {t: "🔶 the unit contract: numbers come only from intake/"}
    prompt: "/haipipe-display <task> check Display1: list each number in the figure and the card item it matches."
    mark: "red: this check does not exist yet; today a person compares by eye"
- act: "Act 5 · Accept"
  step_arrow: "accept"
  key: "Only you accept: you look at preview.pdf, then write accepted: in the README. A renderer's score is advice and never accepts."
  states:
  - title: "⑧ Display · accept"
    tab: "3 · Evidence"
    step: "🖼 Display · Display1"
    chip: "✍ accept"
    boxes:
    - title: "Display1 · Overview Figure · preview.pdf"
      dashed: true
      button: "Accept · Reject"
      mark: "you look at it, then accept"
      rows: {Preview: "preview.pdf", Built_on: "none (a concept figure)", Score: "advice only, never accepts", accepted: "blank until you tick"}
    prompt: "/haipipe-display <task> revise Display1: <my note on the picture>; show a new candidate."
    sections:
    - {t: "✅ accepted: your name and date, in README.md"}
    - {t: "🔶 a renderer score: advice, not a tick"}
    mark: "a changed picture goes to candidates/ first; you pick, then promote it"
- act: "Act 6 · Show and deliver"
  step_arrow: "show"
  key: "The accepted unit shows on the Section canvas in the Displays corner, and the box in the text marks the sentence that points to it. Delivery keeps only a built copy, never a second source."
  states:
  - title: "⑨ the canvas: the Displays corner"
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    fills: [0.695, 0.975, 0.625, 0.735]
    fills_label: "Displays: figures and tables, each built on Evidence cards"
    mark: "the C2 canvas, bottom right: a dashed empty card, 'No figure or table in C2 yet'; an accepted unit's picture goes here"
    open: "❓ The Overview Figure belongs to Section C8, whose canvas is not drawn yet; C2 holds no display"
    arrow: "the figure itself"
  - title: "⑩ the Overview Figure, as made today (v25)"
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/delivery/studio/s03-related-work-structure/render/Task-2.1-workflow-SHIFT-v25.png"
    mark: "cited by B7 S7 (Overview Figure); the example this drawing follows"
    open: "❓ Not a display unit yet: a pptx and a png under studio/s03, no recipe/, no README, no built_on:, no accepted:"
    arrow: "built into delivery"
  - title: "⑪ Delivery: a built copy"
    tab: "Delivery"
    step: "📤 Delivery"
    chip: "→ next"
    boxes:
    - title: "The built copy"
      rows: {Folder: "b21/delivery/j01_task21_section/<tNN>/", Copy: "Display1-overview-figure.pdf, from the unit's assets/", Rule: "built from the accepted unit, never edited by hand", Today: "render/ holds v10 to v25 as a Studio output"}
    prompt: "/haipipe-draft <task> deliver: build the text with Display1 placed, from the accepted unit only."
    mark: "copy it, run it; a wrong picture is fixed in the unit, then rebuilt"
```


Decided
-------

s41-D01 · A display gets one procedure topic, drawn the way b32 s41 draws the draft Task (JL 261016: "for the b33 and
    b34, could we have the things like b32-s41?").
s41-D02 · The worked example is the Task 2.1 Overview Figure, shown as not yet a unit, in red.
s41-D03 · A display step has no tab of its own: it sits in 3 · Evidence (today's Evidence-Display tab folds there,
    b32 s41 Ⓐ).


Open
----

1. Does the Display step get its own tab, or stay inside 3 · Evidence?
2. Which of the 260 units move to `<task>/display/`, which are only read.
3. A check of a figure's numbers against the cards: who writes it (haipipe-evidence's cards.py, or display).
4. The unit contract keeps `accepted:` in the Page; a Task unit needs it in its own README.
5. The sentence is C3.P6 · B7 · S7 but the figure is Section C8: which canvas shows its Display card.

(write here, or mark the drawing in red)
