Annotation Alignment and Execution & Audit
=========================================

Version 11 uses the version 9 presentation as its visual and structural base. It preserves its illustrated entities, restrained colors, spacious flow diagrams and Workbench interface concepts. It updates the process around whole-dataset diagnosis, Train-only expression refinement and human decisions about rules and labels.

The two loops
-------------

Annotation Alignment owns elicitation and reconciliation of the user's intended standard, current rules and reference labels. Human sources, corpus exploration and audit reports produce focused decision cards. The person can keep a rule or label, correct a reference label, change a rule, supply another decision or defer. Decisions have explicit scopes. Rule approval does not automatically approve all propagated item labels.

Execution & Audit is a staging environment. Executors apply the same guideline to both Train and Test. Scoring tools evaluate labeling performance against the compatible reference version. The auditor separately inspects item-level disagreements and plausible causes. A Train-only refiner adjusts wording, order, decision steps and examples while preserving approved rules. The auditor can inspect both partitions; the refiner receives only Train evidence in a separate context. Test item content, errors, report text and memory must not be passed into the refiner.

Performance evaluation and error analysis
-----------------------------------------

"Evaluate labeling performance" replaces the ambiguous "Score predictions" label. Evaluation reports task-appropriate quality metrics and coverage separately by model and dataset partition. Tool telemetry records speed and cost. Reference answers are hidden from target executor prompts. Unresolved and abstained items remain visible.

Error analysis examines cases, current rules, original annotation provenance, available context and model disagreements. A disagreement or model consensus does not establish a reference-label error. Hypotheses include expression problems, suspected reference-label errors, rule gaps or conflicts, executor limitations, missing context and genuine ambiguity.

Train expression errors feed the refiner. Rule and label issues from either staging partition become an Alignment report for human review. The system records rejected flags as well as confirmed corrections. Unflagged cases receive random audit checks so agreement is not assumed to prove correctness.

Versioned rounds and stopping
----------------------------

Each round binds rule, expression, reference-label, dataset partition and executor versions. Preserve original labels and previous run results. Human-approved rule changes identify affected items in both partitions for re-review; label-only corrections retain their reason and scope. New versions produce new executions rather than overwriting old results.

Report expression-only gains against a common unchanged reference standard separately from label corrections and semantic changes. Whole-system before/after comparisons need a common independent adjudicated outcome standard, not merely two sets of self-consistent labels. Stop at declared quality/coverage criteria, diminishing gains, unresolved issues requiring a person, or a budget limit. Always produce a report, including when no candidate qualifies.

Train and staging Test
----------------------

The operational split is Train for direct expression development and Test for checking the same candidate and finding issues. Both sets are audited. Human review may act on issues from either set. Once Test findings guide changes, subsequent system versions have development exposure to that set. These staging scores are not independent whole-system generalization estimates. The research evaluation on slide 5 uses fresh cases beyond this staging dataset. An operational release gate and a scientific generalization claim are distinct.

Release package
---------------

The release binds the guideline, compatible reference-label version, executor settings, resolved and unresolved issue records, quality report and audit policy. Production batches preserve provenance distinguishing individually reviewed, inferred and audit-accepted labels. New rule or label issues reopen Alignment. A narrow cross-model performance gap is insufficient without acceptable quality and coverage.

Deck scope
----------

The first twenty slide positions stay in their v9 order. Pages 6–13, 16, 19 and 20 are revised. Page 21 explains Train and Test in staging. Page 22 illustrates an audit issue decision card. Pages 1–5, 14–15 and 17–18 retain their v9 illustrations. Relevant speaker notes use the updated process. The five-page discussion excerpt contains pages 6, 12, 19, 21 and 22.

The interface illustrations use synthetic examples and unrun metric placeholders. They describe a proposed system, not deployed features or measured results. The slides remain raster illustrations with editable speaker notes, matching v9.
