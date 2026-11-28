# Workbench UI concepts, version 9

Status: static product mockups for discussion. These screens are not deployed features. All cases and workflow states are synthetic. The five new slides are pages 16–20 of the existing deck.

## Design direction

The main human surface is a decision inbox inside Labeling > Rounds. A person opens a small report, studies learning evidence and answers consequential questions. Sources, current rules and comments stay close to the question. Model/runtime settings live in Quality, where an experiment operator can inspect them without burdening ordinary preference collection.

Keep the existing Workbench shell and its Data, Labeling, Quality and Delivery areas. New report content uses a stable renderer. The Meaning Agent prepares questions and integrates human feedback; the Expression Agent works on fixed meaning and routes unresolved semantic issues back through Meaning. Optional chat supplies additional context to the same history.

Teal marks human decisions and approved standards. Purple marks corpus evidence and labels. Blue marks execution and evaluation. Orange identifies agent work and pending interpretation. Use text as well as color for every status. The small orange robot preserves continuity with the illustrated deck without taking over the screen.

## Screen 16: decision inbox

Primary action: open the next report. The center lists concrete questions, not generic performance metrics. Separate Meaning and Expression activity explains what is happening while a person is away. A waiting dependency is not a claim that all work has stopped.

Pending questions, saved drafts and submitted feedback need distinct views. Useful sorting criteria are consequence, dependency and unresolved age. Do not prioritize only uncertainty scores or the largest cluster. A small status panel links to the current guideline and reviewed labels.

## Screen 17: evidence beside a question

A wide decision form sits beside source-backed learning cases. The form offers alternatives, rejects all options, accepts custom wording, allows defer and preserves comments. No option starts selected. A compact source panel can expand context while keeping the question visible.

Save draft and Submit answers have different effects. The real implementation should allow partial reports, show durable receipt status and preserve drafts across return visits. Rejection and deferral remain distinct. Conditional comments are preserved and interpreted explicitly. Approval applies only to the exact shown scope; generic preferences may need a proposed rule patch before release.

On a narrow screen, stack evidence above the card, keep the question/choice hierarchy intact and place actions after the answer. A slide cannot validate responsive behavior; the implementation must test keyboard, focus, contrast, scrolling and actual persistence.

## Screen 18: changes and affected labels

After submission, show what the person said, the agent's proposed interpretation, what can be applied and what remains unresolved. A proposed guideline is visibly different from a released one. Provide rule-level before/after comparisons and the source decision.

The paired item panel exposes review scope and diagnostics. It must never turn rule approval into blanket item approval. Individually reviewed labels, inferred candidates and batch-accepted labels need different statuses. Exact rule patches already approved on a card should not require another redundant click.

## Screen 19: expression experiments

Quality shows the frozen meaning version, candidate expression and executor comparison. Empty metric cells are intentional unrun states. A production version would report quality, coverage and throughput, with definitions and uncertainty available on demand.

Only learning errors support wording development. Validation returns allowed summaries; independent final qualification remains separate. The Expression Agent reports missing meaning to the Meaning Agent rather than contacting humans directly or changing the standard. Fixed model weights, quality floors and stronger-model regression constraints remain visible in run settings.

## Screen 20: scale and acceptance

Both use cases arrive at the same Delivery view. Qualification and an audit/review policy precede batch execution. A disabled action communicates the missing prerequisite without suggesting an experiment has run.

Review queues distinguish uncertain items, probability-sampled audit cases and open semantic questions. Delivery includes the structured guideline, labels with acceptance provenance, unresolved cases and audit evidence. Resume/failure states and scope changes must remain inspectable. Do not use a single green completion badge to hide unresolved items.

## Source and validation

Exact built-in imagegen prompts, per-slide notes and source image references are in deck-content-v9.json. build-v9.mjs imports the v8 PPTX and appends the new pages. release-v9.py validates package structure, slide/notes counts, exact preservation of the original fifteen illustrations and notes, image embedding, dimensions and PDF pages. It uses exact bytes rather than hashes to follow repository instructions. The hash-based bundled finalizer is therefore not used.

The PDF and PPTX illustrations are raster assets. Speaker notes and the authored content manifest remain editable. Controls pictured in the slides are not interactive. The existing browser prototype is a separate artifact, and these mockups do not imply backend implementation.
