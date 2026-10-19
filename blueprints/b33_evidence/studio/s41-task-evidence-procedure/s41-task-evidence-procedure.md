s41 · Evidence procedure: from a claim to a card you can trust
==============================================================

**Tags:** `Levels`

**Stage:** shaping

**Topic:** how evidence works for one page, step by step, drawn the way b32 s41 draws the draft Task: one workflow map
of who does what, then each step as the screen a person sees, with the prompt to copy and what is still open in red.
The worked example is SHIFT Task 2.1, Section C2 (Project-SHIFT-Study, b21_event_cgm): its six Evidence cards in
`studio/s04-task21-updated-draft/evidence/cards.yaml`, the Runs they read in `discovery/b01_shift_proposal_evidence/
j21_task21_citations/`, and the canvas that shows them, b21 s05. Asked by JL 261016 ("for the b33 and b34, could we
have the things like b32-s41? to show how things work step by step?"). The card format and the script stay
haipipe-evidence's; this topic draws its screens.

**Feeds:** none yet (b33 has no `reports/`)


Files
-----

```text
s41-task-evidence-procedure/
├── s41-task-evidence-procedure.md          this face; the drawing's words are the yaml block below
├── build_s41_task_evidence_procedure.py    the builder (b32 s41's map and screens, copied and adapted)
├── s41-task-evidence-procedure.excalidraw  ① the map; ② ③ Find, ④ ⑤ Cards, ⑥ ⑦ Check, ⑧ ⑨ ⑩ Propose,
│                                           ⑪ ⑫ Show; Ⓑ where the files sit; Ⓒ what is still open
└── s41-task-evidence-procedure.png         its preview
```

Read from disk on every build: C2's `cards.yaml` and `proposals.md`, the output of `cards.py check`, each card's Task
title, the draft version, and b21 s05's canvas picture.

```yaml
heading: ["① Evidence: from a claim to a card you can trust", "one Section, C2: read, find, write cards, check, propose, show"]
key: "Outcome: every claim that needs a paper, a value or a figure has a card item with its exact words; what is missing is red and becomes a proposal a person ticks. Only a person ticks."
problem: "🎯 Problem: a sentence says 'rose about fifteenfold' and no one can see which paper, which line, or which words it backs; a missing source hides until a reviewer asks."
novelty: "🏆 What it gives: one card per topic, each item tied to its sentence and its exact words (✨1) · a check that every address and quote resolves (✨2) · a missing source becomes a proposal, and nothing is made until you tick it (✨3)."
marks: [[3, 0, "✨2"], [4, 1, "✨3"], [2, 0, "✨1"]]
lanes: ["📄 draft/ · text", "🗂 evidence/ · cards", "🔎 evidence agent", "🔬 discovery · work Task", "🖼 canvas", "👤 you"]
lane_w: [330, 330, 380, 400, 330, 330]
symbols:
  title: "📐 Words: the parts of the evidence work"
  rows:
  - ["CITE n", "a card from a discovery Task: a paper, blue"]
  - ["WORK n", "a card from a work Task: our own Run, violet"]
  - ["item", "one line on a card: a Run, its sentences, its words"]
  - ["for", "the sentences an item backs, like S5"]
  - ["anchor", "the exact words it backs, boxed in the text"]
  - ["need", "a missing item: red, with what to make"]
  - ["proposal", "a line in proposals.md a person ticks"]
  - ["address", "bNN.jNN.tNN.rNN: block, job, task, run"]
map:
- step: "🔎 Act 2 · Find"
  screens: "② ③"
  cells: [[2, "read(§3 as a reader)", "draft/ §3 text", "the sentences S1 to S14"]]
  text: "§3 draft, 14 sentences"
- cells: [[2, "find(claims)", "the sentences", "claim · kind · anchor words"]]
- step: "🗂 Act 3 · Cards"
  screens: "④ ⑤"
  cells: [[2, "write(cards)", "claims · Runs", "evidence/cards.yaml"]]
  plan: "cards.yaml: 6 cards"
- step: "✅ Act 4 · Check"
  screens: "⑥ ⑦"
  cells: [[2, "check(cards)", "cards.yaml · the Runs", "every address resolves"]]
- step: "⚑ Act 5 · Propose"
  screens: "⑧ ⑨ ⑩"
  cells: [[2, "propose(needs)", "the red items", "proposals.md"], [5, "✍ Tick", "each proposal", "[x], kept"]]
  plan: "proposals.md: 5 open"
- cells: [[3, "make(Run)", "a ticked proposal", "tNN/runs/rNN/result/"]]
- cells: [[2, "fill(card)", "the new Run", "need becomes run: rNN"]]
  plan: "need → run"
- step: "🖼 Act 6 · Show"
  screens: "⑪ ⑫"
  cells: [[4, "draw(canvas)", "cards.yaml · §3", "cards below, anchors boxed"]]
folders:
  frame: "Ⓑ Where each file sits"
  sub: "the cards beside the words, the papers in the Project's discovery world; the canvas only reads"
  tree: |
    Project-SHIFT-Study/
    ├── cowork/b21_event_cgm/studio/
    │   ├── s04-task21-updated-draft/
    │   │   ├── draft/                 the words (haipipe-draft)
    │   │   └── evidence/
    │   │       ├── cards.yaml         the six cards
    │   │       └── proposals.md       the five lines to tick
    │   └── s05-paragraph-editing-master/   the canvas that shows them
    └── discovery/b01_shift_proposal_evidence/j21_task21_citations/
        └── t05_event_input_forecasters/
            └── runs/r02_calzavara2025_.../result/
                ├── r02_calzavara2025_....bib
                └── facts.md           F09: "Incorporating all factors ..."
  notes:
  - "🗂 evidence/ sits in the draft Task beside draft/ and display/, one writer each; a canvas or a report only reads it"
  - "🔬 an address bNN.jNN.tNN.rNN is read in the Project's discovery/ for CITE, in its work/ for WORK"
  - "❓ b21's cards sit under a Studio topic today (s04), not under a Task folder: the Task is not made yet"
open:
  frame: "Ⓒ What is still open"
  lines:
  - "❓ C2 has no WORK card yet: no sentence there states a number from our own Run (Act 3, ⑤ shows the format)"
  - "❓ All five proposals are unticked: five needs are still red (Act 5, ⑩)"
  - "❓ The Page workbench's Evidence Space still reads the old format, not evidence/cards.yaml"
  - "❓ haipipe-draft-evidence retires in steps: new pages first, EMBED into the draft, Proj21's four Page evidence Runs become cards, then the skill goes"
  - "❓ evidence for a report and for slides is not drawn yet"
screen:
  task: "Task · 2.1 · C2"
  line: "Draft · Block b21 · Task 2.1 · Section C2 · Challenge and Significance"
  tabs: ["Studio", "1 · Plan", "2 · Write", "3 · Evidence", "4 · Revise", "Delivery"]
tabs:
- act: "Act 2 · Find"
  step_arrow: "Find"
  key: "A reader goes through the written Section, sentence by sentence, and marks each claim that needs a paper, a value or a figure, with the exact words that need it. No card is written yet."
  states:
  - title: "② Evidence · Find · 1 of 2: read the text as a reader"
    skills: [{side: left, skill: "haipipe-evidence", note: "finds what each claim needs"}, {side: right, skill: "haipipe-draft", note: "the text it reads, in draft/"}]
    tab: "3 · Evidence"
    step: "🔎 Evidence · find"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Reads: "§3 Draft <version>, C2 · S1-S14", Marks: "each claim that needs a paper, a value or a figure", Takes: "its sentence number and its exact words", Writes: "nothing yet: a list of claims"}
    prompt: "/haipipe-evidence find: read C2 (draft <version>) as a reader; for each claim that needs a paper, a value or a figure, give its sentence number and its exact words."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the reader marks"
  - title: "③ Evidence · Find · 2 of 2: the claims, with their words"
    skills: [{side: left, skill: "haipipe-evidence", note: "keeps the claims, then the cards"}, {side: right, skill: "you", note: "say which claims need no card"}]
    tab: "3 · Evidence"
    step: "🔎 Evidence · the claims"
    chip: "✓ done"
    boxes:
    - title: "Claims in C2 · sentence, anchor words, kind"
      live: claims
      dashed: true
    prompt: "/haipipe-evidence find: now write one card per topic for these claims."
    mark: "the words in quotes are the anchor: the page boxes them; no anchor, no box"
    open: "❓ no claim in C2 needs our own Run, so no WORK item is found here"
- act: "Act 3 · Cards"
  step_arrow: "Cards"
  key: "One card is one topic: a discovery Task (CITE, blue, external) or a work Task (WORK, violet, internal). Each item names its Run, its sentences (for) and its exact words (anchor). The script reads the paper's title and quote from the Run, so the card holds no copy."
  states:
  - title: "④ Evidence · Cards · 1 of 2: CITE, from a discovery Task"
    skills: [{side: left, skill: "haipipe-evidence", note: "writes evidence/cards.yaml"}, {side: right, skill: "haipipe-discovery", note: "makes the papers a CITE card reads"}]
    tab: "3 · Evidence"
    step: "🗂 Evidence · CITE 3"
    chip: "→ next"
    boxes:
    - title: "evidence/cards.yaml · the real CITE 3 card"
      live: cite3
      dashed: true
    prompt: "/haipipe-evidence cards: write C2's cards from the claims, one card per discovery Task for CITE, one per work Task for WORK; a missing source is a need item."
    mark: "one topic, three papers, each item tied to S5 and its own words"
    arrow: "a work Task works the same"
  - title: "⑤ Evidence · Cards · 2 of 2: WORK, from a work Task"
    skills: [{side: left, skill: "haipipe-evidence", note: "writes evidence/cards.yaml"}, {side: right, skill: "haipipe-task", note: "makes the Runs a WORK card reads"}]
    tab: "3 · Evidence"
    step: "🗂 Evidence · WORK n"
    chip: "format only"
    boxes:
    - title: "WORK card format · the skill's tested example (Project-Samsung)"
      dashed: true
      rows: {kind: "work", source: "b51.j02.t01 (a work Task)", item: "run: r01 · for: [7]", anchor: "12 rows", file: "metrics.json", key: "rows_total", what: "rows checked"}
    prompt: "/haipipe-evidence cards: add a WORK card for the number S7 states: read it from the Run's own output file and key."
    mark: "the number is read from the Run's file, so a card never holds a copy that can go stale"
    open: "❓ C2 has no WORK card yet; this is the format from the skill's own test, not a C2 card"
- act: "Act 4 · Check"
  step_arrow: "Check"
  key: "Before anything is drawn, the script resolves every address, fact and value. A card that does not resolve stops the page builder, so a canvas never shows a card that does not."
  states:
  - title: "⑥ Evidence · Check · 1 of 2: run the check"
    skills: [{side: left, skill: "haipipe-evidence", note: "scripts/cards.py check"}, {side: right, skill: "haipipe-discovery", note: "owns the Runs it reads"}]
    tab: "3 · Evidence"
    step: "✅ Evidence · check"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Command: "cards.py check evidence/cards.yaml", Reads: "each card's Task and Run in discovery/ or work/", Looks: "address · fact id · value · anchor words", Exit: "0 when all resolve, 1 on any problem"}
    prompt: "/haipipe-evidence check evidence/cards.yaml: resolve every address, fact and value, and say what is missing."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the script reads"
  - title: "⑦ Evidence · Check · 2 of 2: the real output"
    skills: [{side: left, skill: "haipipe-evidence", note: "prints one line per card"}, {side: right, skill: "you", note: "fix any problem line"}]
    tab: "3 · Evidence"
    step: "✅ Evidence · result"
    chip: "✓ resolves"
    boxes:
    - title: "cards.py check · C2's output, as it ran on this build"
      live: check
      dashed: true
    prompt: "/haipipe-evidence check evidence/cards.yaml --sentences s.json: also check that each anchor's words are in its sentence."
    mark: "numbered by the first sentence each card backs; CITE 2 has no source: it is the list of needs"
- act: "Act 5 · Propose"
  step_arrow: "Propose"
  key: "Each need becomes one line a person ticks: what to make, where, and for what purpose, marked proposed by evidence. Nothing is made before the tick; then the owner of that level (haipipe-discovery for a paper) makes the Run, and the need becomes an item."
  states:
  - title: "⑧ Evidence · Propose · 1 of 3: turn needs into proposals"
    skills: [{side: left, skill: "haipipe-evidence", note: "scripts/cards.py propose"}, {side: right, skill: "you", note: "read the proposals"}]
    tab: "3 · Evidence"
    step: "⚑ Evidence · propose"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Command: "cards.py propose evidence/cards.yaml --write", Reads: "every need item and its propose", Levels: "run · task · job · topic", Writes: "evidence/proposals.md, ticks kept"}
    prompt: "/haipipe-evidence propose evidence/cards.yaml --write: one flagged line per need, for me to tick."
    mark: "copy it, run it in Claude or Codex"
    arrow: "a person reads"
  - title: "⑨ Evidence · Propose · 2 of 3: the lines to tick"
    skills: [{side: left, skill: "haipipe-evidence", note: "writes proposals.md, keeps ticks"}, {side: right, skill: "you", note: "tick what to make; no skill ticks"}]
    tab: "3 · Evidence"
    step: "⚑ Evidence · proposals.md"
    chip: "✍ tick"
    boxes:
    - title: "evidence/proposals.md · the real lines"
      live: propose
      dashed: true
      button: "Tick"
      mark: "you read each, then tick"
    prompt: "Tick [x] in evidence/proposals.md the ones to make; leave the rest."
    mark: "each line names the card, the sentence and the purpose; the tick is yours alone"
    arrow: "you tick"
  - title: "⑩ Evidence · Propose · 3 of 3: the Run, then the card"
    skills: [{side: left, skill: "haipipe-discovery", note: "makes the Run for a ticked line"}, {side: right, skill: "haipipe-task", note: "the same, for a work Run"}]
    tab: "3 · Evidence"
    step: "⚑ Evidence · after the tick"
    chip: "✍ made"
    boxes:
    - title: "What one tick does · the first line, CITE 2 · S1"
      dashed: true
      rows: {Ticked: "[x] new discovery run in b01.j21.t01", Made by: "haipipe-discovery, as a numbered Run", Makes: "t01_*/runs/rNN_<paper>/result/: .bib, facts.md", Then: "need: the count becomes run: rNN, fact: [F..]", Now: "all five lines are still [ ]: nothing made"}
    prompt: "/haipipe-discovery b01.j21.t01: add a Run for the ticked proposal 'the count: more than 38 million in the US live with diabetes'."
    mark: "after the Run, re-run check; the red need turns into a blue item"
    open: "❗ the five CITE 2 needs stay red until a person ticks and the Runs are made"
- act: "Act 6 · Show"
  step_arrow: "Show"
  key: "The Section canvas only reads evidence/cards.yaml: the cards sit along the bottom, and each item's words are boxed in the text with the card's name in the margin. It keeps no copy of the cards."
  states:
  - title: "⑪ Canvas · Show · 1 of 2: the Evidence cards along the bottom"
    skills: [{side: left, skill: "haipipe-evidence", note: "cards.yaml, read by the canvas"}, {side: right, skill: "excalidraw-draft", note: "draws the Section canvas"}]
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    boxes: [[0.0075, 0.633, 0.673, 0.933, "← the six cards, one topic each: blue is CITE", 0.70, 0.80], [0.1475, 0.649, 0.316, 0.774, "← CITE 2: still needed, red", 0.70, 0.87]]
    prompt: "/haipipe-studio b21 s05: rebuild the Section canvas from evidence/cards.yaml."
    mark: "five cards are CITE (blue); CITE 2 lists the five needs in red, each with what will be made"
    open: "❓ no WORK card (violet) yet; the Page workbench's Evidence Space still reads the old format, not cards.yaml"
    arrow: "the words are boxed"
  - title: "⑫ Canvas · Show · 2 of 2: the anchor words, boxed in the text"
    skills: [{side: left, skill: "haipipe-evidence", note: "checks every anchor is in its sentence"}, {side: right, skill: "haipipe-display", note: "figures built on the cards"}]
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    boxes: [[0.2715, 0.086, 0.675, 0.628, "the Section text, C2: each backed phrase is boxed"], [0.473, 0.220, 0.625, 0.240, "← S5's anchor words, boxed", 0.70, 0.56], [0.643, 0.221, 0.667, 0.236, "← CITE 3 in the margin: the card behind it", 0.70, 0.60]]
    prompt: "/haipipe-evidence check evidence/cards.yaml --sentences s.json: every anchor must be found in its sentence before the canvas is built."
    mark: "blue box = a CITE anchor, red box = a still-needed one; the card's name stands in the margin beside the line"

```


Decided
-------

s41-D01 · Evidence gets one procedure topic, drawn the way b32 s41 draws the draft Task: a workflow map, then each step
    as the screen a person sees, with the prompt to copy and what is still open in red (JL 261016: "for the b33 and
    b34, could we have the things like b32-s41? to show how things work step by step?").
s41-D02 · The worked example is SHIFT Task 2.1, Section C2: its real cards.yaml, proposals.md, `cards.py check` output
    and b21 s05's canvas, all read from disk on every build.
s41-D03 · The steps are Find, Cards, Check, Propose, Show; making the Run belongs to haipipe-discovery or haipipe-task
    and is drawn as the end of Propose, not as an evidence step.


Open
----

1. C2 has no WORK card; draw the WORK path on a Section that has one.
2. All five proposals are unticked; once ticked and made, redraw ⑩ with the new Runs.
3. The Page workbench's Evidence Space still reads the old format.

(write here, or mark the drawing in red)
