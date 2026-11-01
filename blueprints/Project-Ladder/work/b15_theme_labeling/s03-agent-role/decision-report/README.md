# Meaning Loop decision report

A working local prototype of asynchronous human preference collection. The report turns learning evidence into rule-level choices, preserving source references and the scope of every answer.

## Open and rebuild

Open build/index.html after running: python build.py

Edit source/report-v1.json for content and source/template.html for behavior or appearance. The build/ directory is generated and ignored. Each new round must use a new report_id and the applicable guideline_version. No content hashes are used.

## What works

- Six decision cards with contrastive learning examples, candidate rules, explicit consequences, source references and affected scopes.
- No preselected answer. Choose a candidate, reject all candidates with an alternative, or defer for more evidence.
- Optional comments and additional human context.
- Browser-local draft persistence, a review step and downloadable structured JSON feedback.
- Partial submission: unresolved decisions remain open.
- Responsive layout, native form controls, keyboard focus and validation.

## Method boundary

The examples, initial brief and guideline are explicitly synthetic. This prototype has not searched a corpus, called a model, or collected real human evidence. It does not call a backend. Saving uses this browser's local storage; exporting creates a local feedback file. Browser storage may be unavailable, so a failed save is reported.

The proposed production flow is:

1. Collect the human's initial idea, source notes, and previous decisions.
2. Search learning items and cluster consequential uncertainties or rule conflicts.
3. Generate a versioned report with neutral options, contrastive evidence and affected scopes.
4. Collect choices, custom proposals, comments and deferred decisions asynchronously.
5. Check submitted feedback for conflicts; draft the guideline changes and recheck affected learning labels.
6. Return unresolved questions in the next report; pass approved, aligned artifacts to the Expression Loop.

The development report must contain only learning evidence. Both learning and evaluation items can be labeled in separate executor calls, but evaluation item content and errors do not enter this report. The builder rejects examples from other splits. This check is a prototype guard, not a complete production access-control system.

Human approval of a rule is not individual approval of all propagated labels. Feedback carries approval_scope: rule_preference_only and item_labels_approved: false. A custom answer is a proposal requiring interpretation, not an automatically executable rule. Selecting a future batch-audit policy does not establish that policy's sampling or acceptance thresholds.

Difficulty and uncertainty are separate diagnostic concepts, defined through decision cards as well as substantive labels. The agent should combine flagged cases with random and coverage sampling, rather than asking only about cases a model calls hard.

No submission automatically updates a guideline. The original version remains named in the feedback, so a future importer can reject stale submissions or merge them explicitly. New rounds must preserve prior decisions and show genuine conflicts without assuming that the newest answer silently overrides them.
