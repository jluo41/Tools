---
mindmap: 1
title: s58 · Task UI: Work · structured
built: from-topic .
---

# s58 · Task UI: Work <!-- root #6d67d7 -->

**Tags:** `Task UI`
**Stage:** shaping

- For <!-- @for #f78806 -->
  - a deck, and the Work screen of … <!-- @for/0 #1ae629 -->
    a deck, and the Work screen of a labeling Task (one step, of six types) on the focus page (`delivery/ui/task-work`), for the people who build the workbench
- Delivery type <!-- @delivery-type #58a44f -->
  - ui <!-- @delivery-type/0 #636117 -->
- Covers <!-- @covers #a6c44a -->
  - each Task view drawn from its step … <!-- @covers/0 #2872f4 -->
    each Task view drawn from its step slide (the deck's pages 7 to 15: In → who works → Out, your part, next), its close-up screen (pages 16 to 23) drawing the Results, and a coverage table in task_views.py (COVER, check()) that fails when a slide box has no place on the screen (JL 261101: "you should read the steps here, in this slides, and then you think how do design it"); the type sets the view buttons (its steps).
  - Rows: A 📦 items (Data · Items … <!-- @covers/1 #aaba7b -->
    Rows: A 📦 items (Data · Items · Embedding · Split), B 📏 ground truth (Labels), C 🧭 meaning (Frame · Report · Preferences · Update;
  - Loop 1, 2 … making m01, m02 … <!-- @covers/2 #d39856 -->
    Loop 1, 2 … making m01, m02 …; the only Task with an interaction), D 🛠 expression (Rewrite · Run · Evaluate · Release; rounds e01, e02 … under one meaning), E 🔍 scanning (Batches · Audit · Final labels), F 📊 score (Agreement).
  - Work shows ⚙️ Process (the slide's flow … <!-- @covers/3 #ddd8de -->
    Work shows ⚙️ Process (the slide's flow and your part) and 📊 Results (its Out in detail), each numbered from 1.
- Excluded <!-- @excluded #980495 -->
  - the other eight cells of the 3 … <!-- @excluded/0 #915146 -->
    the other eight cells of the 3 × 3 (s51, s52, s53, s54, s55, s56, s57, s59); the engine's own Labeling workbench, where a person labels (s02); every Theme's shared frame (b10).
- Topic <!-- @topic #7e13bd -->
  - A Task's Work: each step's input, prompt … <!-- @topic/0 #0d0ade -->
    A Task's Work: each step's input, prompt and sign; one cell of the labeling 3 × 3, a labeling Task (one step, of six types) × Work (do), copied from the paper theme's (b16 j01;
  - JL 261031: "please go ahead and update … <!-- @topic/1 #20cd7c -->
    JL 261031: "please go ahead and update them").
  - Its drawing is haipipe-studio's five parts, drawn … <!-- @topic/2 #a7478d -->
    Its drawing is haipipe-studio's five parts, drawn by `build_s58_task_ui_work.py` through j01's `labeling_ui_cells.py`; its Design is every view as the same full screen, lettered, settled one round each.
  - Names are the public DICES-350 dataset's; no … <!-- @topic/3 #9f447d -->
    Names are the public DICES-350 dataset's; no item text is drawn.
- Feeds <!-- @feeds #ffe8e9 -->
  - `reports/` q01_labeling_ladder <!-- @feeds/0 #70ceeb -->
- Files <!-- @files #6ce6c5 -->
  - [py] [build_s58_task_ui_work.py](build_s58_task_ui_work.py) <!-- @files/0 #f2e71b -->
  - delivery/ <!-- @files/1 #404761 -->
  - review/ <!-- @files/2 #7928fb -->
  - [excalidraw] [s58-task-ui-work.earlier-old-layout-v2.excalidraw](s58-task-ui-work.earlier-old-layout-v2.excalidraw) <!-- @files/3 #814d00 -->
  - [png] [s58-task-ui-work.earlier-old-layout-v2.png](s58-task-ui-work.earlier-old-layout-v2.png) <!-- @files/4 #993dc8 -->
    ![s58-task-ui-work.earlier-old-layout-v2.png](s58-task-ui-work.earlier-old-layout-v2.png)
  - [excalidraw] [s58-task-ui-work.excalidraw](s58-task-ui-work.excalidraw) <!-- @files/5 #175436 -->
  - [md] [s58-task-ui-work.md](s58-task-ui-work.md) <!-- @files/6 #af33ec -->
  - [png] [s58-task-ui-work.png](s58-task-ui-work.png) <!-- @files/7 #27bdc4 -->
    ![s58-task-ui-work.png](s58-task-ui-work.png)
  - [html] [s58-task-ui-work.slides.html](s58-task-ui-work.slides.html) <!-- @files/8 #f0d31c -->
  - [json] [s58-task-ui-work.slides.json](s58-task-ui-work.slides.json) <!-- @files/9 #2f4c55 -->
  - [pptx] [s58-task-ui-work.slides.pptx](s58-task-ui-work.slides.pptx) <!-- @files/10 #ae5db0 -->
- Decided <!-- @decided #55615a -->
  - s58-D12 · C3 Preferences passes stage 1 … <!-- @decided/0 #cac9cf -->
    s58-D12 · C3 Preferences passes stage 1 of the design loop at round 3, mean 8.4 (review/C3-s1-r03.md; round 2 scored 7.6 once the prompt box came in, review/C3-s1-r02.md); JL looks once before it is built.
  - s58-D11 · C1 Frame passes stage 1 … <!-- @decided/1 #3dda6c -->
    s58-D11 · C1 Frame passes stage 1 of the design loop at round 2, mean 8.1 (review/C1-s1-r02.md; round 1 scored 7.9, review/C1-s1-r01.md); JL looks once before it is built.
  - s58-D10 · C2 Report passes stage 1 … <!-- @decided/2 #a3cb46 -->
    s58-D10 · C2 Report passes stage 1 of the design loop at round 1, mean 8.1 (review/C2-s1-r01.md); JL looks once before it is built.
  - s58-D09 · C3 Preferences has its prompt … <!-- @decided/3 #9e5124 -->
    s58-D09 · C3 Preferences has its prompt too: after you answer report-03, the box takes your notes (slide 10's "Optional chat · Add context") and Copy prompt sends your answers and notes to the chat session, which saves them to the same decision record and starts Update; the Results lines "Optional chat" and "Where your answers go" go into it. Every step now has a prompt (JL 261101: "we should also have a box where we can enter the template and then we copy it to the chat"). Replaces s58-D07's "your own step (C3) has none".
  - s58-D08 · C2 Report's Results are the … <!-- @decided/4 #5e56fc -->
    s58-D08 · C2 Report's Results are the loop's 🙋 Interaction report (one row per loop: Loop 3 waiting, Loop 1 and 2 answered), 📌 Typical cases, ⚠️ Hard cases, 🎲 Random cases, and 🧠 Guideline rules as a mind map with its versions (m01, m02 as buttons; each card's Q tag on the rule it asks about). The agent writes the report with /haipipe-labeling-interaction, a labeling /haipipe-interaction collect Run per loop (`rNN_collect_report_mNN`), which you answer in Preferences; the meaning loop's iterations are Loop 1, 2, 3 and expression's are rounds e01, e02; the example is response safety throughout (JL 261101: "we might have the Loop 1, Step 1 report, that the agent using the /haipipe-labeling-interaction to call /haipipe-interaction to generate the report"; "make the guideline as the mindmap, to make the rules to be very very clean"; "the Interaction Report and then the Typical Cases, Hard Cases, Random Cases, and also the Guideline Rule Mindmap with different versions").
  - s58-D07 · Every agent step's Process carries … <!-- @decided/5 #bf3fcc -->
    s58-D07 · Every agent step's Process carries its prompt, the draft Task's Prompt box redrawn: the words filled from the step's inputs, fields only you fill (Frame: Goal, Use cases, Constraints; elsewhere your notes), the line naming the Task's chat session, and Copy prompt; your own step (C3) has none. A prompt is you → the agent, an interaction the agent → you (JL 261101: "prepare the prompt template that the user can enter and copy to the chat session").
  - s58-D06 · D3 Evaluate passes stage 1 … <!-- @decided/6 #bf6b7a -->
    s58-D06 · D3 Evaluate passes stage 1 of the design loop at round 2, mean 8.0 (review/D3-s1-r02.md; round 1 scored 7.6, review/D3-s1-r01.md); JL looks once before it is built.
  - s58-D05 · Reference-label versions are written lNN, … <!-- @decided/7 #4ff392 -->
    s58-D05 · Reference-label versions are written lNN, the deck's own letter (slides 19 and 22: "Expression e03 / Labels l02"), so rNN means a Run only. Found by D3's round-1 review ("r02 reads as a Run"); swept through task_views.py, s13's map, PLAN.md, CONTRACTS.md, the engine's fixture and tests and the server test (proposed by Claude 261101).
  - s58-D04 · C3 Preferences passes stage 1 … <!-- @decided/8 #e8ceb6 -->
    s58-D04 · C3 Preferences passes stage 1 of the design loop at round 1, mean 8.0 (review/C3-s1-r01.md); JL looks once before it is built, with the review's three fixes and which of them the slide allows.
  - s58-D03 · Building becomes two Tasks, one … <!-- @decided/9 #714edb -->
    s58-D03 · Building becomes two Tasks, one per loop: 🧭 meaning (Frame · Report · Preferences · Update) and 🛠 expression (Rewrite · Run · Evaluate · Release); a turns strip shows each loop (m01, m02 … ; e01, e02 … under one meaning), the round report sends expression back to meaning's next Report, and only meaning's Preferences carries an interaction, one collect Run per turn, whose answers Update records as the meaning history (JL 261101: "we have the meaning-loop and expression-loop"; "we hope that the interaction is only available in the meaning loop task").
  - s58-D02 · No Runs view: the view-button-list … <!-- @decided/10 #c19f16 -->
    s58-D02 · No Runs view: the view-button-list holds a Task's steps only; each step shows the Runs that made it in its own Process, and every Run in time order is the right-rail Timeline (JL 261101: "for things here, we don't put Runs as a seperate things view").
  - s58-D01 · s05 (old layout refinement v2) … <!-- @decided/11 #7a3b49 -->
    s58-D01 · s05 (old layout refinement v2) folds into this topic as its earlier sketch, kept beside the drawing (JL 261031).
- Open <!-- @open #cf9b77 -->
  - Replaced (JL 261031: "It is stupid that … <!-- @open/0 #f4adb3 -->
    Replaced (JL 261031: "It is stupid that every view has the same three boxes"): every view now shows its own step's sections from the previous version; the old one-template design and its reviews are in review/old-template-261031/.
  - A2 (items · Items) passed stage 1 … <!-- @open/1 #626b7b -->
    A2 (items · Items) passed stage 1 at round 3 (8.9, review/A2-s1-r03.md) and waits for JL to look once.
  - Redrawn 261101 from the step slides as … <!-- @open/2 #64aac1 -->
    Redrawn 261101 from the step slides as two loops (s58-D03); the views wait for the design loop and JL's look. Earlier designs and their reviews stay in review/old-*/.
  - ? a Sign here, or only in … <!-- @open/3 #9a6f78 -->
    ? a Sign here, or only in the Labeling workbench
  - Which letter to settle next <!-- @open/4 #fe10a7 -->
