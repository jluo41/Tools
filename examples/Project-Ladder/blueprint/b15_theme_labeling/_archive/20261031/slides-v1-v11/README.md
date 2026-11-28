Subjective Labeling slides
==========================

The canonical presentation folder for the Tools blueprint Block `b15_theme_labeling`.

Current version: 12, Returning to the Meaning Loop
------------------------------------------------

[Open the five-page discussion PDF](deliverables/subjective-labeling-preference-return-v12-discussion.pdf)

[Open the complete 23-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pdf)

[Open the complete 23-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pptx)

Version 12 sends the round report to the whole Meaning Loop Agent, the Alignment Agent of v11. It investigates related cases and earlier decisions, collects preferences again, reconciles feedback and updates compatible rules and reference labels before rerunning Step 5. A separate report route proceeds to Step 6 when release criteria are met. Expression-only changes stay in Step 5 using Train evidence.

Updated stable slide IDs: 6, 10, 12 and 21. New transition slide 12a sits between Step 5 and Step 6. Existing slide identifiers are retained to keep earlier discussions traceable; the complete deck has 23 physical pages. The five-page excerpt shows IDs 6, 10, 12, 12a and 21. All other illustrations remain exactly as in v11. Revised images were generated and edited with built-in imagegen, visually reviewed, then embedded in the PowerPoint. Illustrations are raster; speaker notes are editable.

[Before/after rationale and report contract](source/meaning-loop-return-v12.md) · [Exact prompts and notes](source/deck-content-v12.json). Build with source/build-v12.mjs; validate and release with source/release-v12.py. Static workflow and interface concepts only; prior versions remain below.

Version 11, Alignment, execution and audit
-----------------------------------------

[Open the five-page discussion PDF](deliverables/subjective-labeling-alignment-audit-v11-discussion.pdf)

[Open the complete 22-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v11-alignment-audit.pdf)

[Open the complete 22-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v11-alignment-audit.pptx)

Version 11 uses v9 as its visual base. Annotation Alignment (Steps 2–4) reconciles human preferences, rules and reference labels. Execution & Audit (Step 5) runs both Train and staging Test, evaluates labeling performance, analyzes errors, and rewrites expression using Train evidence only. Suspected reference-label errors and rule issues return as decision reports for human review.

Both staging partitions are audited. Once Test findings guide revisions, Test is development evidence for subsequent versions; fresh independent cases are needed for claims about unseen data. Model weights remain fixed. Rules, expression, reference labels and execution settings are versioned together.

Pages 6–13, 16, 19 and 20 are revised; pages 21–22 explain the data roles and an audit decision card. Nine v9 illustrations remain exactly unchanged. The deck has 22 slides and the discussion excerpt has five. All revised illustrations were visually reviewed, and the PowerPoint passed round-trip import, package and image-preservation checks. These remain static concepts with synthetic examples and unrun metrics. Illustrations are raster; speaker notes are editable.

[Design rationale](source/alignment-audit-v11.md) · [Exact prompts and notes](source/deck-content-v11.json). Build with source/build-v11.mjs and release with source/release-v11.py. Versions 9 and 10 are preserved below.

Version 10, Train and Test
-------------------------

[Open the seven changed pages](deliverables/subjective-labeling-data-splits-v10.pdf)

[Open the complete 21-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v10-data-splits.pdf)

[Open the complete 21-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v10-data-splits.pptx)

Version 10 uses two partitions: Train develops meaning and expression; Test assesses the frozen result. Both receive labels during the Meaning Loop. Test reference labels remain separate from guideline development and hidden from executor prompts. No model weights change. A separate validation split is not part of this version.

Pages 6, 7, 12, 13, 17 and 19 are revised; page 21 explicitly shows both sets being labeled during Meaning Loop, with only Train feeding guideline development. The other fourteen illustrations and their notes remain unchanged. Static UI concepts still contain synthetic examples and unrun placeholders. Illustrations are raster; speaker notes are editable.

[Data-role rationale](source/data-splits-v10.md) · [Exact prompts and notes](source/deck-content-v10.json). Build with source/build-v10.mjs and release with source/release-v10.py. Earlier versions below retain their historical design.

Version 9, Workbench UI concepts
-------------------------------

[Open the five UI concept pages](deliverables/subjective-labeling-ui-concepts-v9.pdf)

[Open the complete 20-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v9-ui-concepts.pdf)

[Open the complete 20-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v9-ui-concepts.pptx)

Version 9 preserves the first fifteen illustrations and their speaker notes, then adds five Workbench UI concepts on pages 16–20: a decision inbox, an evidence-backed form, visible rule/label changes, an Expression experiment view and large-scale delivery with review. The interface follows the existing Data, Labeling, Quality and Delivery areas. Forms are primary, chat is supplementary, and semantic questions return through the Meaning Agent.

These are static imagegen mockups with synthetic examples, not deployed features. Model metrics are unrun placeholders. Rule approval stays distinct from affected-item approval. The batch-start illustration is disabled until qualification. The PPTX illustrations are raster; speaker notes and authored content remain editable.

[UI design rationale](source/ui-concept-v9.md) · [Exact prompts and notes](source/deck-content-v9.json). Build with source/build-v9.mjs and release with source/release-v9.py. The custom release checks use exact bytes, not content hashes, to honor repository instructions. Earlier releases remain available.

Version 8, Workbench decision reports
------------------------------------

[Open the 15-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v8-illustrated.pdf)

[Open the 15-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v8-illustrated.pptx)

Version 8 makes Workbench forms the default interface for collecting human preferences, with chat as supplementary context. Page 6 updates the overview. Pages 9–11 show report preparation, asynchronous form review, and feedback integration. Page 15 adds an enlarged decision card with alternatives, custom answers, defer, comments, save and submit. The other ten illustrations remain unchanged.

The agent generates structured decision reports from human sources and learning evidence; Workbench renders, saves and submits them. Both forms and chat feed the same versioned decision record. Conflicts and deferred questions return in later reports. Human approval of a rule does not approve every propagated item label. The deck describes the proposed integration; the local interactive prototype currently saves browser drafts and exports feedback files.

Exact prompts and notes: source/deck-content-v8.json. Build with source/build-v8.mjs; validate and release using source/release-v8.py. Illustrations are raster images; speaker notes are editable. Earlier versions remain available.

Version 7, items before task framing
-----------------------------------

[Open the 14-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v7-illustrated.pdf)

[Open the 14-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v7-illustrated.pptx)

Version 7 changes the preparation order: **Step 0 transforms the corpus into items; Step 1 frames the labeling task.** The overview, detailed slide order, page numbers and speaker notes follow this order. Steps 2–4 remain the Meaning Loop and Step 5 the Expression Loop. Page 7 is itemization; page 8 is task framing.

Exact built-in imagegen edit prompts and notes: `source/deck-content-v7.json`. Build with `source/build-v7.mjs`; inspect `build/v7/`; validate and export both formats with `source/release-v7.py`. Earlier releases remain available.

Version 6, illustrated method walkthrough
----------------------------------------

[Open the 14-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v6-illustrated.pdf)

[Open the 14-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v6-illustrated.pptx)

Version 6 retains the original five illustrated slides, replaces the overview with an end-to-end Agent system, and gives each Step 0–7 its own slide. Step 0 frames the task and inspects raw sources. Step 1 explicitly transforms the corpus into annotation items. Steps 2–4 form the Meaning Loop. Step 5 is the Expression Loop, where the agent calls fixed-weight executors and scores predictions against approved development labels, which stay hidden from executors. Meaning defects return to the human; executor limitations remain distinct. Steps 6–7 qualify, scale and audit.

The system is training-free in the sense of fixed model weights; guideline expression is still optimized on development evidence. The slides propose a method and do not claim achieved weak-model performance. PDF bookmarks name all slides. Illustrations are raster; PowerPoint speaker notes are editable.

Sources: `source/deck-content-v6.json` contains exact built-in imagegen prompts, correction prompts and detailed notes. `source/build-v6.mjs` builds the presentation and previews. `source/release-v6.py` validates the package, preserves the original five illustrations, and exports the PowerPoint and PDF. Generated previews and validation records live in `build/v6/`.

Version 5, illustrated workflow discussion
-----------------------------------------

[Open the six-slide presentation](deliverables/agent-mediated-labeling-workflows-and-evaluation-v5-illustrated.pptx)

Version 5 retains the original five illustrated slides from version 3 and appends slide 6, **Proposed workflow: steps to discuss**. It shows preparation, the human-agent meaning loop, wording refinement across executors, qualification, and large-scale labeling with audit. The workflow is a discussion draft. The illustrations are raster images; speaker notes remain editable.

The new artwork was generated with built-in imagegen. Its exact generation and correction prompts, detailed notes and source image references are in `source/deck-content-v5.json`. Rebuild with `source/build-v5.mjs`, review `build/v5/slide-6.png`, then validate and release with `source/release-v5.py`. Earlier releases remain intact.

Version 4, editable outline style
--------------------------------

[Open the five-slide presentation](deliverables/agent-mediated-labeling-workflows-and-evaluation-v4.pptx)

Version 4 redraws the Subjective Labeling deck in the style of the IRB/team-workspace presentation shared by the user: Helvetica Neue, thin outline icons, muted role colors, clear arrows, and generous whitespace. Text, boxes and connectors are native editable PowerPoint objects; icons are embedded Lucide artwork. This is the labeling deck, not an IRB deck.

Both use-case slides retain three rows: human-agent-corpus dialogue; the structured adaptive guideline and human-approved, guideline-consistent labeled data; executor testing and large-scale labeling with audit. Two further slides explain the proposed evaluations. No experimental results are claimed.

Sources
-------

- `source/build-v4.mjs`: authored layout, slide text, icon rendering and deck builder.
- `source/deck-content-v4.json`: authored content context and editable speaker notes.
- `source/node_modules`: local runtime dependency link; not tracked.
- `build/v4/`: generated slide previews, candidate deck and private validation records; not tracked.
- `deliverables/`: generated decks; not tracked.

Run the builder with Node.js after making the artifact-tool, lucide and sharp packages available. It writes `build/v4/`; review those previews before creating a new numbered release. Change the source, never hand-edit a generated artifact. Keep earlier releases.

Earlier versions
----------------

Versions 1–3 use imagegen slide illustrations, with editable speaker notes. Their artwork is under `assets/`; their original builder and content live under `.build/`. `generation-prompts*.md` are generated exports from those sources. They remain available for comparison.

The Studio s03/slides and Physician-SPACE output paths remain compatibility links to this folder.

Meaning Loop discussion figure, version 1
-----------------------------------------

[Open the illustrated diagram](assets/meaning-loop-development-and-labeling-v1.png).

The development route uses learning evidence, while the labeling route applies the guideline to both learning and evaluation items. Each prediction carries a task label plus separate difficulty and uncertainty diagnostics. The guideline defines these diagnostics and review actions. Learning-only case feedback returns to meaning development; approved meaning and reference labels pass to the Expression Loop.

This standalone discussion figure uses built-in imagegen and does not replace the current v7 deck. Exact generation and correction prompts, data-access boundaries, diagnostic-field proposals, and evaluation caveats are in [the figure source](source/meaning-loop-development-and-labeling-v1.json). Model-reported difficulty is not evidence of correctness. Repeated selection uses validation; final test remains separate.
