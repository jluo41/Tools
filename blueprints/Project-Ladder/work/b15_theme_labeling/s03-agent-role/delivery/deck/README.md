Subjective Labeling deck
========================

The delivery deck of Studio s03 (agent role in subjective labeling), in the Tools blueprint Block
`b15_theme_labeling`. It moved here from the Block's `slides/` folder on 261031 (s03-D13).

Current version: 12, Returning to the Meaning Loop
--------------------------------------------------

[Open the five-page discussion PDF](deliverables/subjective-labeling-preference-return-v12-discussion.pdf)

[Open the complete 23-slide PDF](deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pdf)

[Open the complete 23-slide PowerPoint](deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pptx)

Version 12 sends the round report to the whole Meaning Loop Agent, the Alignment Agent of v11. It investigates related cases and earlier decisions, collects preferences again, reconciles feedback and updates compatible rules and reference labels before rerunning Step 5. A separate report route proceeds to Step 6 when release criteria are met. Expression-only changes stay in Step 5 using Train evidence.

Updated stable slide IDs: 6, 10, 12 and 21. New transition slide 12a sits between Step 5 and Step 6. The complete deck has 23 physical pages; the five-page excerpt shows IDs 6, 10, 12, 12a and 21. Illustrations are raster; speaker notes are editable.

What is here
------------

```text
deck/
├── README.md        this file
├── source/          build-v12.mjs, release-v12.py, deck-content-v12.json (prompts and notes),
│                    meaning-loop-return-v12.md (before/after rationale), visual-review-v12.json
├── assets/          the 23 illustrations deck-content-v12.json names
├── deliverables/    v12 .pptx, .pdf and five-page PDF; the v11 .pptx, which build-v12.mjs starts from
└── build/v12/       slide previews, candidate files and validation.json
```

Build with `node source/build-v12.mjs`, then validate and release with `python source/release-v12.py`. Generated
artwork and outputs stay local (`.gitignore`); the authored sources are trackable.

[Before/after rationale and report contract](source/meaning-loop-return-v12.md) · [Exact prompts and notes](source/deck-content-v12.json)

Earlier versions
----------------

Versions 1 to 11, with their sources, artwork, builds and the full version history this README used to carry, are in
`../../../_archive/20261031/slides-v1-v11/` (its `README.md`).
