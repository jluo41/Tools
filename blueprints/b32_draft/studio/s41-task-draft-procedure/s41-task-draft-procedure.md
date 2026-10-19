s41 · Task draft procedure: from a plan to a Section you accept, line by line
============================================================================

**Tags:** `Levels`

**Stage:** shaping

**Topic:** every step of a ✎ draft Task (`task-type: draft`, s03), drawn the way b15 s42 drew the labeling building
Task: one workflow map of who does what, one revise pass as a loop, the Task as a tree, and each step's tab as it
develops (Operation over Result). A draft Task writes one Section (a paper Section, a proposal's part, a report): it
plans, finds its evidence, writes, then revises pass by pass on the Section canvas until the person says done, and its
text is built into tex, docx and pdf. The worked example is SHIFT Task 2.1, Section C2 (b21_event_cgm, Codex thread
"SHIFT · Event CGM", 261014), whose Section canvas is b21 s05. Asked by JL 261015 ("How do you think you can add sNN
in b32 to showing the design as well?"; then "Tools/blueprints/b15_theme_labeling/studio/s42-task-building-procedure
<---- you can try to follow this"). The draft's grammar and its Runs stay haipipe-draft's; this topic draws its screens.

**Feeds:** none yet (b32 has no `reports/`)


Files
-----

```text
s41-task-draft-procedure/
├── s41-task-draft-procedure.md            this face; the drawing's words are the yaml block below
├── build_s41_task_draft_procedure.py      the builder (b15 s42's map, loop, tree and screens)
├── s41-task-draft-procedure.excalidraw    ① the workflow map; Ⓐ today's tabs → the four steps;
│                                          ② ③ Studio, ④ ⑤ Plan, ⑥ ⑦ Write, ⑧ ⑨ Evidence,
│                                          ⑩ ⑪ ⑫ Revise, ⑬-⑯ Delivery (render, read back); Ⓑ where Studio and Delivery live;
│                                          Ⓓ the skills and the code behind the screens, one large frame; beside each screen, its skills
├── s41-task-draft-procedure.png           its preview
└── history/s21-draft-skill-map-261016/    the skill-map topic s21, folded in here on 2026-10-16
```

Read from disk on every build: today's draft tabs (`DRAFT_TASK_SUBS` in `servers/workbench/frame.py`), B21's draft
version and sentence count (`b21_event_cgm/studio/s04-task21-updated-draft/draft/`), and b21 s05's canvas picture.

```yaml
heading: ["① The draft Task: who does what", "a plan → your Section, every change accepted by you"]
key: "Outcome: the Section's text in draft/, every change shown old → new and accepted by you, then built into tex, docx and pdf. Only you accept a change."
problem: "🎯 Problem: a Section is written in Word, in chat and on a canvas at once; reviews, evidence and text sit in three places, and no one can see what changed, why, or which sentence a comment means."
novelty: "🏆 What it gives: one text (draft/), every view built from it · C1 one Section canvas every step fills, column by column: logic left, text middle, evidence and edits right (✨1) · C2 every change old → new, and only you accept it (✨2) · C3 a quick loop: notes in, canvas out in seconds; the full rubric only on ask (✨3)."
marks: [[7, 0, "✨1"], [8, 1, "✨2"], [9, 1, "✨3"]]
lanes: ["📄 tNN/draft/ · text", "📐 tNN/draft/ · plan, E", "🤖 writing agent", "🔎 evidence agent", "🧪 reviewer", "👤 you"]
lane_w: [330, 330, 380, 330, 300, 330]
symbols:
  title: "📐 Words: the parts of a draft, and who reads them"
  rows:
  - ["§1 Structure", "the plan: paragraphs and Bullets"]
  - ["§2 Scratch", "what each paragraph will say"]
  - ["§3 Draft", "the text, one Bullet a sentence"]
  - ["C2.P3.B1", "a sentence's address"]
  - ["E<nn>", "one Evidence Item: VALUE · CITE · DISPLAY"]
  - ["R<n>", "one edit card: old → new, why, state"]
  - ["pass k", "one small loop: notes, edits, accept"]
  - ["round n", "one big loop: plan to Send, and the file back"]
  - ["previous/", "the older versions, kept"]
map:
- step: "🎨 Studio"
  screens: "② ③"
  cells: [[5, "talk, sketch", "the Task · related", "your ideas"], [2, "draw(ideas)", "your words · the chat", "<block>/studio/sNN-<topic>/", "haipipe-studio ref/draw.md"]]
  text: "draft/: none yet"
  plan: "ideas, a logic sketch"
- step: "📐 Stage 1 · Plan"
  screens: "④ ⑤"
  cells: [[2, "gather(task)", "face · studio · related", "records/<stem>-context.md", "haipipe-draft-logic ref/context.md"]]
  plan: "context, requirement"
- cells: [[2, "structure(context)", "context · the Studio sketch", "§1: P · B", "haipipe-draft-logic ref/structure.md"], [5, "✍ Sign plan", "§1 Structure", "plan v1"]]
  plan: "§1 signed"
  loop: "Studio ⇄ plan, one loop"
  loop_to: 0
  loop_to_cell: 1
- step: "🔎 Evidence asks"
  screens: "⑨ · a side loop"
  cells: [[3, "cards(claims in §1)", "§1 Bullets · the Project's Runs", "a card a claim: have · ask a Job · ask a person · soften", "haipipe-evidence cards.py check · propose"], [5, "✍ Tick asks", "evidence/proposals.md", "a Run in its Job", "haipipe-task · -discovery"]]
  plan: "cards: ✅ have · 🔶 asked · ❓ person"
- step: "✍️ Stage 2 · Write"
  screens: "⑥ ⑦"
  cells: [[2, "scratch(§1)", "§1 · the Studio sketch", "§2 Scratch", "haipipe-draft-logic ref/scratch.md"]]
  text: "§2 Scratch"
- cells: [[2, "write(§2)", "§2 · the cards", "§3 v1.0 · red box where a card waits", "haipipe-draft-writing ref/writing.md"]]
  text: "§3 Draft v1.0"
- step: "🔎 Stage 3 · reader pass"
  screens: "⑧ ⑨"
  cells: [[3, "find(claims in §3)", "§3, read as a reader", "cards for claims the plan missed", "haipipe-evidence cards.py propose"], [5, "✍ Agree", "each new card", "bound, or asked as above"]]
  plan: "every card bound or asked"
- step: "🔁 Stage 4 · Revise"
  screens: "⑩ ⑪ ⑫"
  cells: [[2, "draw(Section)", "§3 · cards back from their Runs · R", "the Section canvas", "excalidraw-draft section_canvas.py"], [5, "notes, marks", "the canvas · chat", "your feedback"]]
  text: "canvas: ▓ changed words"
- cells: [[2, "propose(feedback)", "the named sentences", "Revise cards: why · original · expected", "haipipe-draft-writing ref/revise.md"], [5, "✍ Accept · reject", "each Revise card", "accepted cards"]]
- cells: [[2, "apply(cards)", "accepted cards · addresses", "§3 v<next>", "haipipe-draft-writing ref/revise.md"], [4, "check(Section)", "on ask: the rubric", "findings → Revise cards", "haipipe-draft-review ref/evaluation.md"], [5, "✍ Done?", "the Section", "another pass · done"]]
  text: "§3 v<next> · old in previous/"
  loop: "small loop · another pass: k ← k+1"
  span: "pass k"
- step: "📤 Delivery"
  screens: "⑬ ⑭ ⑮"
  cells: [[2, "export(§3)", "§3 Draft", "<block>/delivery/<jNN>/<tNN>/", "haipipe-delivery ref/page-delivery.md"], [3, "render(files)", ".docx · .pdf", "one picture a page", "haipipe-delivery word_round.py render"], [5, "✍ Send", "files · pictures", "sent, by you"]]
  text: "built, never edited"
- step: "📥 Read back"
  screens: "⑯"
  cells: [[2, "read(file back)", "their OneDrive copy", "-vN · its pictures · comments", "haipipe-delivery word_round.py pull"], [5, "✍ Another round?", "their changes", "round n+1 · stop"]]
  text: "their -vN beside ours"
  loop: "big loop · another round, when the file comes back changed: n ← n+1"
  loop_to: 1
  loop_side: right
today:
  frame: "Ⓐ Today's draft tabs, and the step each becomes"
  sub: "the 13 tabs a draft Task opens on today (read from frame.py), folded into the step tabs Studio · 1-4 · Delivery, named the same in Work and Report"
  columns: ["Space", "tab today", "becomes"]
  map:
    Scope: "1 · Plan"
    Plan: "1 · Plan"
    Requirement: "1 · Plan"
    Records: "1 · Plan (a card)"
    Table: "Report (stays)"
    Reading: "2 · Write (its Result)"
    Questions: "Report (stays)"
    Draft-Scratch: "2 · Write"
    Draft-Revise: "4 · Revise"
    Evidence-Citation: "3 · Evidence"
    Evidence-Display: "3 · Evidence"
    Evidence-Value: "3 · Evidence"
    Evidence-Supporting: "3 · Evidence"
  note: "Studio becomes the first step tab and Delivery the last (JL 261015); Runs keeps its own Space. Report keeps Table and Questions; each step tab is named the same in Work and Report, as b15 s41 does."
skills_tree:   # the skills as their folders, one column per level, read from disk on every build (JL 261016)
  frames:   # one large frame for all (JL 261016: "merge Ⓓ and Ⓔ together ... A large frame for all")
    - frame: "Ⓓ The skills and the code behind the screens, as their folders: one column per level"
      columns: [[draft], ["project:haipipe-delivery,haipipe-report,haipipe-studio", evidence], [display], [excalidraw], [workbench, "2_theme/labeling:workbench-labeling,workbench-task-labeling"], ["code:servers/workbench", "code:servers/workbench-labeling"]]
  links:   # a manual and the code it explains: [skill (either name), code folder, words on the line]
    - [[workbench-task-draft, workbench-page], "workbench-task-draft/", "explains"]
    - [[workbench-task-labeling], "workbench-task-labeling/", "explains"]
  key: [haipipe-draft, haipipe-draft-logic, haipipe-draft-writing, haipipe-draft-review, haipipe-evidence, haipipe-display]
  roles:   # what each skill does, in a few plain words (JL 261016: "simply explain each skill's utilities")
    haipipe-draft: "the door: makes the folder, face, build"
    haipipe-draft-logic: "plans what to say, before writing"
    haipipe-draft-writing: "writes the text, then revises it"
    haipipe-draft-review: "judges the text; never writes it"
    haipipe-draft-workflow: "runs the steps in order"
    haipipe-evidence: "the door: card format, order, proposals"
    haipipe-evidence-cite: "CITE cards: others' papers"
    haipipe-evidence-work: "WORK cards: our own results"
    haipipe-display: "picks the renderer for a figure"
    haipipe-display-diagram: "draws a workflow diagram as SVG"
    haipipe-display-figure: "plots data: line, bar, scatter"
    haipipe-display-illustration: "AI picture of a concept"
    haipipe-display-table: "builds a LaTeX table from data"
    haipipe-display-tex: "hand-written TikZ or equation"
    html-ppt: "a slide deck as one HTML file"
    html-to-svg: "turns HTML slides into SVG"
    figure-to-svg: "turns a figure picture into SVG"
    icon-to-svg: "redraws one icon as SVG"
    haipipe-delivery: "builds the Block's delivery/ files"
    haipipe-report: "asks questions, writes their reports"
    haipipe-studio: "the Studio topics and screen"
    excalidraw-studio: "how every drawing looks"
    excalidraw-ideation: "draws ideas from one question"
    excalidraw-job: "draws a Job as stairs"
    excalidraw-task: "draws a Task as stairs"
    excalidraw-read: "puts one paper on a canvas"
    excalidraw-report: "a scratch or a report drawing"
    excalidraw-draft: "a draft drawn: Section map or changes"
    excalidraw-slide: "plans a deck on a canvas"
    excalidraw-workflow: "maps a study's workflow"
    workbench: "/wb: opens a workbench"
    workbench-task-draft: "explains the draft Task screen"
    workbench-labeling: "the labeling theme: host, Board, Guide"
    workbench-task-labeling: "explains the labeling Task screen"
  extra:   # what a skill took into its own SKILL.md, not a page of its own
    haipipe-report: [["## Questions", "was haipipe-question"]]
    haipipe-draft-review: [["SKILL.md mode 1", "was haipipe-writing (evaluate)"]]
  out: "Inside each skill: a page that was a skill of its own (\"was …\"), or a skill kept inside it. haipipe-draft calls writing, review, evidence and display; display reads evidence."
folders:
  frame: "Ⓑ Studio and Delivery are the Block's folders"
  sub: "a Task keeps no studio/ or delivery/ of its own: its first and last tabs open the Block's, filtered to this Task"
  tree: |
    b21_event_cgm/
    ├── studio/
    │   ├── s04-task21-updated-draft/
    │   ├── s05-paragraph-editing-master/
    │   └── s06-section-canvas-c5…/ ◀ 🎨 the Task's Studio tab: a Block topic
    ├── j01_task21_section/
    │   └── <tNN>/                  the Task: face, draft/, runs/
    │       └── draft/              ◀ 1-4 · Plan … Revise
    └── delivery/
        └── j01_task21_section/
            └── <tNN>/              ◀ 📤 the Task's Delivery tab
  notes:
  - "🎨 Studio: one studio/ for Block, Job and Task; a Task's Studio tab shows the Block's sNN topics in its Job's group (s06 for C5), the same cards the Block's Studio shows"
  - "📤 Delivery: built into the Block's delivery/, under the Task's own path (delivery_dir: b/j/t → b/delivery/j/t); the Block's Delivery lists the same files"
  - "❓ B21's j01 has no Task folder yet: <tNN> is the Section C2 Task to make (Open 4)"
screen:
  task: "Task · 2.1 · C2"
  line: "Draft · Block b21 · Task 2.1 · Section C2 · Challenge and Significance"
  tabs: ["Studio", "1 · Plan", "2 · Write", "3 · Evidence", "4 · Revise", "Delivery"]
tabs:
- act: "Act 2 · Work › Studio"
  step_arrow: "Studio"
  key: "Before the plan: you talk with the agent about the Section's argument and it sketches it on the canvas (the drawing above, the chat below). No sentence is written here; what you settle goes into the plan."
  states:
  - title: "② Work › Studio · 1 of 2: talk and sketch"
    skills: [{side: left, skill: "haipipe-studio", note: "the Studio tab; was workbench-studio"}, {side: right, skill: "excalidraw-studio", note: "how the sketch looks; moved to 1_base/excalidraw"}]
    tab: "Studio"
    step: "🎨 Studio · talk k"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Task: "Task 2.1 · Section C2", Topic: "b21/studio/sNN-<topic>/: a Block topic", Related: "b21/related/: s02, the meetings", Chat: "Claude or Codex, this Task"}
    notes: ["user feedback: P4 should come before P5", "🖼 a photo of my sketch → <task>/notes/<stamp>.png"]
    prompt: "/haipipe-studio <block> <sNN>: talk with me about C2's argument and sketch it on the canvas; write no text yet."
    mark: "copy it, talk in Claude or Codex"
    arrow: "the agent sketches"
  - title: "③ Work › Studio · 2 of 2: the argument, ready to plan"
    skills: [{side: left, skill: "haipipe-studio", note: "keeps the sketch and the chat"}, {side: right, skill: "haipipe-draft-logic", note: "reads the argument into the plan"}]
    tab: "Studio"
    step: "🎨 Studio · the sketch"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "🎨 The logic sketch: P3 → P4 → P5"}
    - {t: "💬 The talk, pass by pass"}
    - {t: "📌 What goes into the plan"}
    mark: "the Block's own Studio topic: the Block's Studio shows the same folder; it writes no text"
- act: "Act 3 · Work › Stage 1 · Plan"
  step_arrow: "Stage 1"
  key: "Before any sentence: §1 Structure, each paragraph's job and each Bullet. It is often shaped in the Studio: what you settle there is written into the Task's §1 at once (D25), so this tab already shows it; the agent fills what the Studio left open, and you sign."
  states:
  - title: "④ Work › 1 · Plan · 1 of 2: gather, then plan"
    skills: [{side: left, skill: "haipipe-draft-logic", note: "gathers (context), then plans (structure); was haipipe-draft-context + -structure"}, {side: right, skill: "haipipe-draft-workflow", note: "runs the steps in order"}]
    tab: "1 · Plan"
    step: "📐 Stage 1 · Plan"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Task: "Task 2.1 · Gordon Gao", Section: "C2 · Challenge and Significance", Requirement: "the template: about 2 pages, 5 parts", Context: "records/<stem>-context.md"}
    prompt: "/haipipe-draft <task> structure: gather the context, write §1 Structure for C2, then stop for my Sign."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent plans"
  - title: "⑤ Work › 1 · Plan · 2 of 2: Sign the plan"
    skills: [{side: left, skill: "haipipe-draft-logic", note: "writes the plan you sign: §1 Structure"}, {side: right, skill: "you", note: "sign it; no skill signs"}]
    tab: "1 · Plan"
    step: "📐 Stage 1 · §1 Structure"
    chip: "✍ sign"
    boxes:
    - title: "§1 Structure · the draft plan"
      dashed: true
      button: "Sign · Revise plan"
      mark: "you read it, then sign"
      rows: {P3: "event information is still under-used", P4: "observed links can mislead a forecast", P5: "our base, and the gap", Bullets: "S1-S14, one job each"}
    prompt: "/haipipe-draft <task> structure: revise §1 from my notes, then stop for my Sign."
    sections:
    - {t: "📐 §1 Structure: P3 · P4 · P5"}
    - {t: "🧩 Bullets, one job each"}
    - {t: "🧭 How they join: P3 → P4 → P5"}
    mark: "after Sign: the step folds ✓, these cards stay"
- act: "Act 4 · Work › Stage 2 · Write"
  step_arrow: "Stage 2"
  key: "Write like a first draft (D26): from the signed plan, §2 Scratch says what each paragraph will say, then §3 Draft is the first full text, written where the thought goes, with no rules yet. The evidence agent proposes cards beside you as you write; the rules come in Revise. The same text is the Studio canvas's middle."
  states:
  - title: "⑥ Work › 2 · Write · 1 of 2: scratch, then write"
    skills: [{side: left, skill: "haipipe-draft-writing", note: "drafts; was haipipe-writing (drafting) + haipipe-sentence"}, {side: right, skill: "haipipe-draft-review", note: "judges; was haipipe-writing (evaluate) + haipipe-draft-check"}]
    tab: "2 · Write"
    step: "✍️ Stage 2 · Write"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Plan: "§1, signed", Studio: "the logic sketch: P3 → P4 → P5", Rubric: "structure · purpose · evidence · readability", Writes: "§2 Scratch, then §3 Draft"}
    prompt: "/haipipe-draft <task> write: scratch §2 from the plan, then write §3 for C2; mark claims you cannot support yet."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent writes"
  - title: "⑦ Work › 2 · Write · 2 of 2: the logic and the text, on the canvas"
    skills: [{side: left, skill: "haipipe-draft-writing", note: "the text, a sentence a line"}, {side: right, skill: "excalidraw-draft", note: "draws this canvas; moved to 1_base/excalidraw"}]
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    fills: [0.005, 0.675]
    fills_label: "2 · Write fills these: the logic, then the text"
    mark: "the text is the one in draft/; the canvas reads it, so a person reads the whole Section at once"
- act: "Act 5 · Work › Stage 3 · Evidence"
  step_arrow: "Stage 3"
  key: "Claim first (D22): once you sign the plan, each claim that needs a value, a citation or a figure gets a card: have it, ask a Job, ask a person, or soften the claim; you tick the asks and their Runs go on while you write. After Write, a reader pass adds cards for claims the plan missed. CITE comes from a discovery Task or Job, WORK from a work Task or Job; each names its Run, bNN.jNN.tNN.rNN."
  states:
  - title: "⑧ Work › 3 · Evidence · 1 of 2: a card per claim, asks, then a reader pass"
    skills: [{side: left, skill: "haipipe-evidence-cite", note: "CITE: papers and what they report, from discovery Runs"}, {side: right, skill: "haipipe-evidence-work", note: "WORK: values from our own Runs, read from their output"}]
    tab: "3 · Evidence"
    step: "🔎 Stage 3 · Evidence"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Reads: "§1 at the plan · §3 <version> as a reader", Finds: "each claim with no card yet", Card: "have · ask a Job · ask a person · soften", Asks: "evidence/proposals.md, you tick"}
    prompt: "/haipipe-evidence <task>: a card for each claim in C2's plan (have, ask, soften), the asks in proposals.md; after Write, read C2 as a reader for claims the plan missed; stop for my tick."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent finds"
  - title: "⑨ Work › 3 · Evidence · 2 of 2: Evidence cards along the bottom"
    skills: [{side: left, skill: "haipipe-evidence", note: "the door: cards.yaml in narrative order, the checks, proposals.md"}, {side: right, skill: "haipipe-display", note: "figures and tables, built on the cards"}]
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    fills: [0.005, 0.68]
    fills_label: "3 · Evidence: the cards along the bottom"
    mark: "each card is one topic: CITE = a discovery Task (papers, and the values they report), WORK = a work Task (our Runs' values and figures); each item tagged S5; red = still needed; Agree binds each Result"
- act: "Act 6 · Work › Stage 4 · Revise"
  step_arrow: "Stage 4"
  key: "Pass by pass on the Section canvas: your notes go in with the prompt, the agent writes Revise cards (why, original, expected), the canvas is rebuilt, you accept each card. Quick by default; the full rubric only on ask."
  states:
  - title: "⑩ Work › 4 · Revise · 1 of 3: your notes on the Section"
    skills: [{side: left, skill: "haipipe-draft-writing", note: "reads your notes, proposes Revise cards"}, {side: right, skill: "you", note: "your notes and sketches"}]
    tab: "4 · Revise"
    step: "🔁 Stage 4 · pass k"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Section: "C2 · P3-P5 · S1-S14", Draft: "<version>", Cards: "6 Evidence · 7 Revise", Mode: "quick: no full review"}
    notes: ["user feedback: split S1, keep the numbers", "🖼 a pasted image → <task>/notes/<stamp>.png"]
    prompt: "/haipipe-draft <task> revise: read my notes on C2, write Revise cards (why, original, expected), rebuild the canvas."
    mark: "copy it with your notes, run it"
    arrow: "the agent proposes"
  - title: "⑪ Work › 4 · Revise · 2 of 3: Revise cards on the canvas"
    skills: [{side: left, skill: "haipipe-draft-writing", note: "Revise cards: why, original, expected; or auto revise: rounds until good, big decisions held for you"}, {side: right, skill: "haipipe-draft-review", note: "judges each change; never the writer"}]
    shot: "examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm/studio/s05-paragraph-editing-master/s05-paragraph-editing-master.png"
    fills: [0.70, 0.995]
    fills_label: "4 · Revise: the upper boxes"
    mark: "one editing unit, P3-P5: left, the old PDF over the logic · middle, one wide text card · right, the Revise box (Edit, Review, Section question), small cards as stairs, a line from each sentence · bottom, every Evidence card once, its words boxed in the text with the card name beside them"
    open: "❓ Open 1: the Revise cards live in s05's face today, not in draft/"
    arrow: "you accept"
  - title: "⑫ Work › 4 · Revise · 3 of 3: accept each card"
    skills: [{side: left, skill: "haipipe-draft-writing", note: "writes the accepted sentence into draft/"}, {side: right, skill: "you", note: "accept or reject each card"}]
    tab: "4 · Revise"
    step: "🔁 Stage 4 · Revise cards"
    chip: "✍ accept"
    boxes:
    - title: "Edit · S1 · split into three sentences"
      dashed: true
      button: "Accept · Reject"
      mark: "you read old and new, then accept"
      rows: {Why: "one sentence, one job", Original: "More than 38 million … (2025); a CGM records …", Expected: "… with diabetes. Among adults … (2025). A CGM …", State: "proposed"}
    sections:
    - {t: "✅ Edit · S3 · often self-reported: written"}
    - {t: "✅ Edit · S6 · leads into EventGlucose: written"}
    - {t: "🔶 Edit · S1 · split into three: proposed"}
    - {t: "🔶 Review · S4 · S9 · S14: suggested"}
    - {t: "❓ Section question · aims and hypotheses: open"}
    mark: "Accept writes the sentence into §3 by its address; a newer sentence stops it"
- act: "Act 7 · Work › Delivery"
  step_arrow: "Delivery"
  key: "The accepted text is built, never edited by hand: tex, docx (tracked against the file it replaces) and pdf; its pages are rendered so you see it as Word lays it out; only you send it. When the file comes back changed, it is read back and a new round starts."
  states:
  - title: "⑬ Work › Delivery · 1 of 4: build"
    skills: [{side: left, skill: "haipipe-delivery", note: "builds the .docx, .tex, .pdf into the Block's delivery/; took in haipipe-draft-delivery"}, {side: right, skill: "haipipe-draft-review", note: "checks the built file, not only the Markdown"}]
    tab: "Delivery"
    step: "📤 Delivery"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Text: "§3 Draft <version>", Builds: "tex · docx · pdf", By: "page.py export · read_revise.py deliver", Rule: "built, never edited by hand"}
    prompt: "/haipipe-draft <task> deliver: build C2 into docx and pdf, and check it both ways."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the agent builds"
  - title: "⑭ Work › Delivery · 2 of 4: render the pages"
    skills: [{side: left, skill: "haipipe-delivery", note: "word_round.py render: each page a picture"}, {side: right, skill: "excalidraw-draft", note: "puts the pages on the Section canvas"}]
    tab: "Delivery"
    step: "📤 Delivery · render"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {File: "<name>-v<N>.docx · .pdf", Makes: "render/<name>-v<N>/p-<N>.png", By: "word_round.py render <N>", Why: "you see it as Word lays it out"}
    prompt: "/haipipe-delivery render v<N> of the Task 2.1 file, then show me the pages."
    mark: "copy it, run it in Claude or Codex"
    arrow: "you look at the pages"
  - title: "⑮ Work › Delivery · 3 of 4: check, then Send"
    skills: [{side: left, skill: "haipipe-draft-review", note: "the Page check gate; was haipipe-draft-check"}, {side: right, skill: "you", note: "Send; only a person sends"}]
    tab: "Delivery"
    step: "📤 Delivery · the built files"
    chip: "✍ send"
    boxes:
    - title: "The built files"
      dashed: true
      button: "Send"
      mark: "you open them, then mark sent"
      rows: {Folder: "b21/delivery/j01_task21_section/<tNN>/", docx: "<stem>.docx", pdf: "<stem>.pdf", To: "OneDrive: Core 2/Task 2.1 - Gordon Gao-draft-JL.docx", Check: "reject all = old file · accept all = draft", State: "not sent"}
    sections:
    - {t: "📄 Word, each change tracked"}
    - {t: "📕 PDF"}
    - {t: "✉️ Sent: only you mark it"}
    mark: "the Block's own delivery/: the Block's Delivery shows the same files; only you mark them sent"
    arrow: "they edit it in OneDrive"
  - title: "⑯ Work › Delivery · 4 of 4: read back, then another round?"
    skills: [{side: left, skill: "haipipe-delivery", note: "word_round.py pull: their copy as -v<N+1>, rendered"}, {side: right, skill: "you", note: "another round, or stop"}]
    tab: "Delivery"
    step: "📥 Read back"
    chip: "✍ round?"
    boxes:
    - title: "What came back"
      dashed: true
      button: "Another round"
      mark: "you read their comments, then say round n+1 or stop"
      rows: {From: "OneDrive: Core 2/Task 2.1 - Gordon Gao-draft-JL.docx", Changed: "since v<N>, by Gordon Gao", Saved: "<name>-v<N+1>.docx · .pdf", Pages: "render/<name>-v<N+1>/", Comments: "the new ones by others", "Next to": "the same OneDrive file, after round n+1"}
    sections:
    - {t: "🖼 Their pages: the next canvas's left"}
    - {t: "💬 Their new comments"}
    - {t: "🔁 Round n+1 → 1 · Plan, in this sNN"}
    mark: "round n+1 stays in this Section's sNN; round n's drawing moves to history/round-<n>-<date>/ (D23)"
```


Decided
-------

s41-D01 · A draft Task gets one procedure topic, drawn the way b15 s42 draws the labeling building Task: the workflow
    map of who does what, one pass as a loop, the Task as a tree, and each step's tab as it develops (JL 261015: "you
    can try to follow this").
s41-D02 · The worked example is SHIFT Task 2.1, Section C2, and its canvas is b21 s05 as it stands; the drawing reads
    both from disk (JL 261015, asked after reading the Codex thread "SHIFT · Event CGM").
s41-D03 · The step tabs are Studio, 1 · Plan, 2 · Evidence, 3 · Write, 4 · Revise, then Delivery: the Studio (talk and
    sketch the argument) comes before the plan, and Delivery is the last tab (JL 261015: "we should also add Studio
    before the plan, So it is the Studio, 1, Plan, ..... and Delivery as the last one").
s41-D04 · The Task's Studio tab is the Block's own Studio topic for this Task, `<block>/studio/sNN-<topic>/`, and its
    Delivery tab is the Block's own `delivery/`, under the Task's path (`<block>/delivery/<jNN>/<tNN>/`): the same
    folders the Block's Studio and Delivery show, never a copy inside the Task (JL 261015: "the Studio will the the sNN
    tNN for it, they are the same folder, and the Delivery will also be the same Delivery in the block level delivery").
s41-D05 · Write comes before Evidence: the evidence agent reads the written Section as a reader and puts an Evidence card on
    each claim that needs support, as Codex did on B21 C2 (CITE 1 for S1). The step tabs are Studio, 1 · Plan, 2 · Write,
    3 · Evidence, 4 · Revise, Delivery. Each step's Result is the same Section canvas from that session, filled one
    column at a time: logic (Studio, Plan), text (Write), evidence (Evidence), edits (Revise) (JL 261015: "we might
    first need the Write, and then need the Evidence, and then need the revise?"; "I think we might want the good UI
    to follow what we discussed in the codex session of SHIFT · Event CGM").
s41-D06 · The text lives in the Task's own `draft/` subfolder, `<block>/<jNN>/<tNN>/draft/`: the plan (§1), the scratch
    (§2) and the text (§3), with `evidence/` and `display/` beside it (s41-D08); the map's two state lanes are that folder (JL 261015: "I think we will
    have the "draft" subfolder in the taskfolder").
s41-D07 · The Section canvas is in English and one editing unit holds several paragraphs (b21 s05-D07; JL 261015: "one
    editing unit can have several paragraphs"): left, the Section cut from the old PDF above its logic; middle, one wide
    text card, the main piece, heavy and large, a sentence after a sentence with no gap; right, the Revise cards with
    no box, as stairs with a line from each card's sentence; along the bottom, every Evidence card once, in loose rows
    kept near the text, not a grid; bottom right, under Revise and right of the Evidence, the Displays (figures and tables built on the Evidence) (JL 261016: "freestyle ... the content card is the main"). A Revise card is named by
    kind (Edit, Review, Section question) and its sentence, not R1-R7, with three rows: Why, Original, Expected (JL 261015:
    "do not call it Rxx"). Each Evidence card is one topic holding many items: CITE, a discovery Task or Job (papers,
    and any value or figure a paper reports); WORK, a work Task or Job (our Runs' values, figures and tables); a figure
    or table is an item of either. Each item is tagged with its sentence, and each paper
    is read from its Run's result/ by address bNN.jNN.tNN.rNN, title first. The words each item backs are boxed in the
    text, with the card's name beside them in the margin (JL 261015: "the E should be Exxx"; "one Ecite to have
    multiple paper"; JL 261016: "Ecite, and Ework", then "just CITE ... WORK", blue external and violet internal; "highlight it as well, and link it to the Evidence card").
s41-D08 · A draft Task keeps three sibling folders, one writer each: `draft/` (the words, haipipe-draft), `evidence/`
    (`cards.yaml` and `proposals.md`, haipipe-evidence) and `display/` (one unit per figure or table, haipipe-display).
    Display reads `evidence/`; the draft reads both; the Section canvas only reads all three. Missing evidence becomes a
    flagged proposal in `evidence/proposals.md` (a new Run, Task, Job or Studio topic, proposed by evidence, for a stated
    purpose) that a person ticks. haipipe-draft-evidence retires in steps: new pages first, then EMBED moves into
    haipipe-draft, then Proj21's four Page evidence Runs become cards, then the skill goes (JL 261016: "in the folder of
    the draft-task, we should have the subfolder of draft, evidence, and display"; "it can just call the evidence and
    display"). First moved: b21's C2 cards, to `studio/s04-task21-updated-draft/evidence/`.
s41-D09 · The skills behind the draft are now five, and every screen names its own (was b32 s21, folded in here; JL
    261016: "maybe no more s21, merge it to the s41"; "Current s21 is very hard to follow"): haipipe-draft (the door: plan,
    folder, steps; `ref/folder.md` replaced haipipe-folder), haipipe-draft-writing (writes; took in haipipe-writing's
    drafting, haipipe-sentence and the WRITE Run), haipipe-draft-review (judges, never the writer; took in haipipe-writing's
    evaluate side and haipipe-draft-check), haipipe-evidence (the door; its two kinds are haipipe-evidence-cite for
    papers from discovery Runs and haipipe-evidence-work for values from our own Runs) and haipipe-display. Out of `draft/`:
    the excalidraw skills (`1_base/excalidraw/`), workbench and workbench-page (`1_base/workbench/`), the Studio screen
    (haipipe-studio), Questions (haipipe-report); no links inside Tools. The full record of those seven moves is
    `history/s21-draft-skill-map-261016/` (s21-D01 to D07).
s41-D10 · Each screen frame shows the skills behind it outside its edges: on the left `[skill] ──▶`, the skill that makes
    what you see; on the right `◀── [skill]`, the one that reads or checks it; dashed when it is a person; each box says
    what was merged into it. Ⓓ draws the skills as their folders, read from disk on every build: `1_base/<family>/` in
    the first column, its skills stacked in the next (one level holds many skills, not one per step), a sub-folder such as
    `workflow-runs/` one column further; the five the draft runs on in the key colour, "+ what it took in" beside each
    (JL 261016: "for each UI, we should also use <---- [box] and [box] -----> to explain how the skills are merged"; "a
    new frame to use the stair tree"; then "每个 style 算作一列 … 这一列里是不是可能有几个相同 level 的 skill … 按照这个
    folder 的 structure 把这个画出来"). One level further, inside each skill, are the pages that were skills of their own
    (a page whose first lines say "was the skill X") and the skills kept inside it, such as the humanizers in
    haipipe-draft-review; Ⓓ holds the draft's skills, Ⓔ the drawing and screen families, each one screen (JL 261016:
    "where are the old things? … you can unfolder more"). Since then Ⓓ is ONE large frame, read by zooming (`canvas.large`): every family side by
    side and, last, the code behind the screens, `servers/workbench/` with `workbench-task-draft/` opened file by file (each file's
    first docstring line), a dashed red "explains" line from its manual `workbench-task-draft` (JL 261016: "merge Ⓓ and
    Ⓔ together, and also have a tree to show the workbench-task-draft"; "A large frame for all").
s41-D11 · `workflow-runs/` is removed; its six Run skills fold into their owners: context, structure and scratch become
    `haipipe-draft/ref/` pages (the plan's steps: gather, shape, rough notes); revise becomes
    `haipipe-draft-writing/ref/revise.md` (the writer's before-and-after ledger); evidence (LAND, EMBED) becomes
    `haipipe-evidence/ref/page-evidence.md`; delivery joins haipipe-delivery. Four `haipipe-draft-*` skills remain:
    haipipe-draft (the door, the plan), haipipe-draft-writing (writes), haipipe-draft-review (judges, never the writer)
    and haipipe-draft-workflow (runs the steps, giving the writing and the judging to different agents). Old triggers
    still land on the right page (JL 261016: "could we remove the workflow-runs, and put the haipipe-draft-xxx to the
    root?"; "go ahead and update").
s41-D12 · The plan gets its own skill again, `haipipe-draft-logic`: deciding what to say, beside writing (how to say
    it) and review (is it good). It holds `ref/structure.md` (SHAPE and SURVEY, the Draft's `## 1 · Structure`),
    `ref/context.md` (what the plan must satisfy) and `ref/scratch.md` (rough thinking, `## 2 · Scratch`), moved out of
    haipipe-draft, which keeps the door: the folder, the face, building and serving the Page. Run names stay
    (`run-structure-<slug>`, `run-scratch-<target>`, Page.context), and `/haipipe-draft-structure`, `-context`,
    `-scratch` land on it. Five remain: haipipe-draft, haipipe-draft-logic, haipipe-draft-writing, haipipe-draft-review,
    haipipe-draft-workflow (JL 261016: "we should still have haipipe-draft-structure, or we can call it
    haipipe-draft-logic ... it will work as the plan"; "yes, go ahead and do it").
s41-D13 · Auto revise: rounds of haipipe-draft-writing (revise) and haipipe-draft-review (a fresh agent each round)
    until the text is good enough, then one stop. A round applies small fixes to a candidate copy (wording, a broken rule
    such as a semicolon, a long sentence split with the same meaning) and holds every big one as a decision card for
    JL: anything that changes a claim, a number, a citation, or the plan (`## 1 · Structure`). It stops when the
    reviewer's rubric verdict is ready and the anti_slop score is under its threshold, when a round does not improve, or
    after 3 rounds. Nothing reaches the Draft before JL picks: the Revise area shows the decisions first and the small
    fixes folded under them (JL 261016: "auto revise ... several rounds of revising until the things are self-evaluated
    good enough, and give some big decisions in the revise area"; "go ahead and do both").

s41-D14 · `workbench-page` is renamed `workbench-task-draft` (0.102.0), named after the server folder it explains,
    `servers/workbench/workbench-task-draft/`; the folder has a README whose first line points to the manual.

s41-D15 · One Task type, one folder: `workbench-task-<type>/` holds everything a Task of that type shows, its layout
    `task_<type>.py` (`TASK_TYPE`, `spaces()`), its views, their assets and tests, and its manual is the skill
    `workbench-task-<type>`. A type every theme uses sits in `servers/workbench/`, a theme's own type in
    `servers/workbench-<theme>/`. The draft layout moved out of `frame.py` into `workbench-task-draft/task_draft.py`, and
    `frame.task_layouts()` finds every such folder (`host_registry.task_folders()`), so a new type is only a new folder
    (JL 261016: "I want to put the UI assets related to this workbench-task-xxx to this folder ... we can have many
    other types of the task types later").


s41-D16 · `excalidraw-section` and `excalidraw-revise` merge into one skill, `excalidraw-draft` (2.0.0), with two modes:
    Map (`ref/map.md`: a paper's Sections, paragraphs, Bullets and evidence cards, from the plans) and Revise
    (`ref/revise.md`: a file we change, each section's page beside the updated sentences, the tracked Word file). Both
    draw a haipipe-draft draft; the old names stay as triggers (JL 261016: "should we make excalidraw-revise and
    exxcalidraw-section to be merged as the excalidraw-draft?").

s41-D17 · No `haipipe-draft-revise`: revising is the writer's second pass, so it stays in haipipe-draft-writing
    (`ref/revise.md`, `ref/auto-revise.md`). The order is logic → writing → review → writing (revise); one writer for
    `draft/`, and the judge is never the writer (JL 261016: "Or it is good to keep, as the revise is a type of
    writing?").

s41-D18 · The labeling Task type is its own folder too: `servers/workbench-labeling/workbench-task-labeling/` holds
    `task_labeling.py` (the frame's Spaces for a labeling Task by its type, out of `labeling_theme.py`), `labeling.py`
    (the engine's Labeling workbench and its write door) and its tab's js; its manual is the new skill
    `workbench-task-labeling`, split out of `workbench-labeling`, which keeps the host, the Board level and the Guide.
    A theme's own Task type lays out only that theme's Tasks (`frame.task_layouts(theme)`), so a labeling
    `task-type: eval` never touches a work Task (JL 261016: "go ahead with workbench-task-labeling").

s41-D19 · haipipe-draft-writing's `ref/drafting.md` is `ref/writing.md` and opens with the rules every sentence is
    written by: the five sections of `haipipe-draft-review/ref/plain-rules.md`, one line each. The rules stay in that
    one page, so the writer and the reviewer read the same list (JL 261016: "COULD WE CHANGE THIS TO THE
    ref/writing.md, and do we have any writing rules here?").
s41-D20 · Frame Ⓒ (one revise pass as seven boxes, and the Task as a tree) is dropped: ⑩ ⑪ ⑫ already show the pass
    as screens, and the loop that matters now is the whole round, Delivery → Render → read the returned file back →
    Plan again, which is to be drawn after ⑭ (JL 261019, on a screenshot of Ⓒ: "我们是不是不再需要这个了？").

s41-D21 · Two loops (JL 261019: "我感觉这里我们应该有所谓的小循环和大循环，对吧？"). The small loop is a Revise pass,
    draw → notes → cards → accept → apply, k ← k+1, until ✍ Done?. The big loop is a round: Plan to Send, then the
    co-authors change the file, we read it back (`-vN`, rendered, their comments) and plan again, n ← n+1. Render
    comes before Send (you look at the pictures of what goes out) and again on the file that comes back; the real
    stop is ✍ Another round? answered stop, not Send.

s41-D22 · Claim first; evidence is a side loop, not a stage (replaces the order in D05; JL 261019: "OK，那你改改吧", on
    Open 5). Once you sign the plan, each Bullet that needs backing gets a card from `cards.py`: have it, ask a Job,
    ask a person, or soften the claim; you tick the asks in `evidence/proposals.md` and that level's skill makes the
    Run in its own Job. Writing does not wait: a sentence whose card waits keeps a red box. After Write, the reader
    pass (D05's place) adds cards for claims the plan missed. A card that comes back enters the small loop at
    draw(Section), because a number can change the claim.

s41-D23 · A new round stays in the same Section topic, `studio/sNN-<topic>/`; it never opens a new sNN (JL 261019: "应该还是
    当下这个 SNN of section 对吧？ … 我们可以把这几个版本留着"). Before round n+1 is drawn, round n's drawing, its
    preview and its page pictures move to `history/round-<n>-<yymmdd>/` in that topic, and the drawing is rebuilt
    from the file that came back. Nothing is written over: the text keeps its versions in `draft/previous/`, the
    file we sent and the one that came back are `-vN` in `delivery/` and `related/materials/`.

s41-D24 · Studio is one thing at every level: the Block's `studio/sNN-<topic>/`. A Job's or a Task's Studio tab opens
    the same Block Studio, showing the topics in its Job's group; a topic is named by what it is about (s06
    section-canvas-c5-timeline), never by a tNN, and no Job or Task keeps a studio/ (JL 261019: "我们这个 studio 其实就是
    sNN jNN tNN … 它跟我们这个 block level 的这个 SNN 是一个东西").

s41-D25 · The plan and the Studio are one loop (JL 261019: "这个 plan 有的时候我们可能是在 Studio 里面做，但它也会相应地
    去更新 … 这个 plan 其实跟 Studio 是紧密连接的"). What a Studio talk settles is written into the Task's
    `draft/` §1 by haipipe-draft-logic in the same session, so the 1 · Plan tab already shows it and asks only for what
    is still open and for your Sign. Studio and Delivery live at the Block and show in the Task too, one place for two
    uses (D04, D24); the plan stays the Task's own file, fed from the Studio.

s41-D26 · Write is a first draft, not a finished text (JL 261019: "这个 Write 感觉跟 scratch 一样，就跟写小说、写草稿
    一样，没有那么多负担。Evidence 也可以先放着，你一边写，就有人一边帮你去找 evidence"). One text, two views: the
    Studio shows `draft/` §3 drawn on the Section canvas, to read and mark; the 2 · Write tab shows the same §2 and §3 as
    a page to type in, one paragraph under its plan line, no rule checks while writing. The evidence agent watches
    the text and proposes cards in the margin next to the sentence (proposed, not bound); you may ignore them. The
    writing rules (haipipe-draft-review plain-rules) apply in 4 · Revise.
s41-D27 · Every delivery item names the one OneDrive file it goes to (JL 261019: "每个 delivery 我们都要 point to 它
    具体要到 OneDrive 的哪个地方"). Today the Block names only its OneDrive folders (`onedrive:` in board.md) and each
    file's place sits inside a Block script (b21 word_versions.py) or a delivery.md row's words. Proposed: one row per
    item in `delivery/delivery.md`, "Where each item goes" (item, OneDrive file under an `onedrive:` folder, reader);
    `word_round.py` reads it, so push and pull need no path, and the Delivery view shows "→ OneDrive: <file>" and which
    version that file holds.

s41-D28 · The canvas and the step tabs are two views of the same files, kept in step through the files, never with
    each other (JL 261019: "我虽然有 stage 1、2、3、4，但比如我都在这个画布上工作，那我这个 stage 1、2、3、4 的内容
    也会对应更新"). The truth is the Task's `draft/` (§1, §2, §3, records/) and `evidence/cards.yaml`. The tabs are
    rendered from them on every open. The canvas is read back: a sentence typed over on it goes into §3 by its address
    (code, as Revise mode's `read_revise.py edits --apply`), a ✓ on a card sets its state (code), a red note or sketch
    becomes a feedback record that haipipe-draft-writing or -logic turns into Revise cards or a §1 change (an agent);
    then the canvas is rebuilt from the files. Opening a canvas older than its files rebuilds it first.


Open
----

1. Where the Revise cards live: `draft/records/<stem>-revise.md` (proposed: then Chat, the workbench and the canvas read
   one file) or a Studio face, as b21 s05 keeps them today.
2. What Accept writes: only the sentence into §3, or also a new draft version with the old one in `previous/`.
3. Today's 13 tabs fold into the step tabs (Ⓐ): Table and Questions stay in Report; is Records a card under Plan?
4. B21's draft sits under `studio/s04-task21-updated-draft/draft/`, not under a Task; a draft Task owns its `draft/`.

(write here, or mark the drawing in red)
