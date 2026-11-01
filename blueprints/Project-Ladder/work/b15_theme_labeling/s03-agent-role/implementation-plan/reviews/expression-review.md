# Expression, evaluation and scale review of the assembled plan

Review scope: the six authored Markdown files in `/private/tmp/labeling-implementation-plan/`, especially `CONTRACTS.md`, `EVALUATION.md`, and T06/T10/T12–T19. Read-only design review. No model experiment, production scan, source-code edit or benchmark was run.

## Disposition

Approve the overall design and the bounded synthetic M0/M1 implementation slice. Resolve findings R1 and R2 before freezing evaluation/storage interfaces for M2/M3; resolve R3 before research tickets claim comparable workflow outcomes. R4 is a small dependency correction. These do not require stopping the synthetic form implementation or asking the user for another design decision.

The plan correctly separates training-free guideline optimization from weight training; Meaning authority from Expression wording; approval of a rule from reference-label approval; validation selection from final qualification; and engineering demonstrations from scientific evidence. It explicitly permits failure to find a suitable cheap model. The single RTX 4090 / 24 GB / approximately 8B configuration is a proposed benchmark, not an unsupported fit, speed or quality claim.

## R1. Important: the storage example contradicts protected-result custody

Locations: `CONTRACTS.md` section 1 storage tree, especially `evaluation/validation/`, `evaluation/final/` and the following custody paragraph; T06 and T13.

The tree places “protected results and safe aggregates” under J, while J is the developer-visible lane. The custody paragraph expressly moves protected items and reference labels outside that root, but not protected prediction records, model explanations, per-item errors or evaluator logs. Those outputs can reconstruct held-out content or labels even when original item files are inaccessible. T13's negative-test requirement is correct, but the concrete storage example leaves an implementer two conflicting instructions.

Smallest fix: make J/evaluation/validation and J/evaluation/final contain approved aggregate projections, opaque custody references and release/qualification status only. Explicitly place full protected execution attempts, predictions, explanations, scorer diagnostics and logs in custodian-owned storage. Specify J/gold as learning reference subsets only. Document any deliberately disclosed final results as a release event after qualification; that does not restore independence for later optimization.

Acceptance addition: seed a unique sentinel in held-out model output and scorer diagnostics, then prove that development filesystem views, report routes, search, cache, logs and tool-response projections cannot return it. Test both validation and final-test roles. This can use synthetic records and needs no real model call.

## R2. Important: reference and audit independence need a blind-first contract

Locations: `EVALUATION.md` sections 3 and 9; `WORK-PACKAGES.md` T10, T17 and T19; `CONTRACTS.md` reference-adjudicator role.

The plan calls for independent reference judgments and probability-sampled audits, but does not expressly prevent a reviewer from seeing executor predictions, model identity or prior labels before making the initial judgment. “Human reviewed” alone does not establish an independent target. In the existing-labeled-corpus case, displaying old labels immediately also encourages confirmation rather than an independent reference. Probability sampling fixes selection bias, not prediction-anchored human judgments.

This is a regression from the current skill contracts: `plugins/haipipe-toolkit/skills/2_theme/labeling/3_quality/haipipe-labeling-test/SKILL.md` lines 43 and 53 require human gold first, with executor outputs hidden; `3_quality/haipipe-labeling-audit/SKILL.md` lines 37–41 specifies a blind protocol and blind human sample.

Smallest fix: independent qualification/reference and population-audit judgments must be collected under frozen meaning with predictions/model identity hidden initially. Record and lock the blind first judgment before any prediction reveal or reconciliation. For final qualification, preserve the current gold-before-execution ordering unless a separately justified protocol explicitly changes it. For production audits, predictions already exist but remain hidden from the initial reviewer. Targeted debugging may reveal predictions; label it separately and do not automatically promote its post-reveal correction to independent gold.

Acceptance addition: a synthetic audit/reference UI payload contains item/context and rules but no prediction, model identity or hidden legacy label; unblinding is rejected before a stored first judgment; post-reveal adjudication preserves that first judgment and records its exposure state. Score the prespecified independent reference release rather than silently replacing it after seeing a model error.

## R3. Important for M5: comparisons need a common outcome standard

Location: `EVALUATION.md` section 7, especially Conventional baseline, Meaning forms only and Full two-loop system; T20.

The plan correctly fixes meaning when isolating Expression effects. For whole-workflow comparisons, different interfaces may create different meanings and reference labels. Evaluating each method only against the labels it helped create can reward internal self-consistency and makes accuracy differences uninterpretable as improved recovery of the person's intended construct.

Smallest fix: distinguish two analyses. For Expression-only comparisons, hold the approved meaning, reference release, items and budgets fixed. For end-to-end Meaning comparisons, prespecify an independent common outcome assessment under the same person's intended task, with assessor exposure recorded and condition identity hidden where feasible. Separately report within-guideline consistency and fidelity to the person's preferences. If the workflows intentionally yield different valid constructs, report them as different endpoints, not a single accuracy ranking. The final-test outcome assessment must not feed the development guideline.

Acceptance addition for study tickets: every primary comparison names its reference standard, who authored/adjudicated it, whether the workflow influenced it, and how differences in meaning are handled. This is a protocol/schema check, not a new experiment.

## R4. Small dependency fix: T14 uses T10's reviewed references

Location: `WORK-PACKAGES.md` section 1 dependency table and T14.

T14 requires a regression set of approved learning cases, but depends only on T09/T12. T10 produces reference releases and diagnostic policy. A scheduler could start candidate acceptance against provisional/inferred labels before the required approved reference contract exists.

Smallest fix: add T10 to T14's dependencies. Draft expression-generation code can proceed against synthetic fixtures earlier, but actual learning-regression acceptance requires the reviewed reference release. T15 already depends transitively on T10 through T13, so this is an earlier package-boundary correction rather than a controller redesign.

## Confirmed strengths and non-findings

- T06 groups correlated records and checks exact/near duplicates before exposure, preserves known exposure history and distinguishes procedural from enforceable isolation. No new content hashes are required.
- T10 distinguishes inferred, directly reviewed and batch-accepted labels. Meaning approval does not certify all propagated items.
- T12/T13 account for malformed output, omitted/duplicate IDs, failures, retries and abstention; scoring cannot silently discard difficult requests.
- T15 optimizes weakest-model quality subject to quality/coverage floors and stronger-model noninferiority, with gap reduction secondary. Executor inability is not permission to weaken meaning.
- Protected-result escalation carries safe aggregates and triggers fresh learning-side investigation. Final-test failure requires a new independent qualification set for a new confirmatory claim.
- EVALUATION sections 5–7 require group-aware paired uncertainty, a prespecified equivalence/noninferiority margin, transfer to an unused model family and meaningful human-effort measurement. No general claim that cheap and expensive executors are already equivalent is made.
- The current `freeze_candidate` / `issue_handoff` split in CONTRACTS section 11 resolves the earlier candidate-versus-qualified-release lifecycle ambiguity. T17's ordering is consistent with it.
- T18 correctly declines exactly-once remote-call guarantees and requires uncertain-attempt reconciliation; T19 separates probability-sample estimation from targeted issue discovery.
- Real hardware/model Runs remain separately authorized. Synthetic fixture tests validate implementation behavior only.

## Review limits

This review assesses the written design and checked source-contract references. It does not establish that new custody isolation, model adapters, scoring, forms or production recovery are implemented. The coordinator's recorded baseline tests were not rerun during this review. After the small revisions, the scoped approval is for implementation against these contracts, not production deployment or research success.

## Amendment verification and resolution verdict

Re-read the amended sections after the coordinator's changes. R1–R4 are resolved at the written-design level:

- R1: CONTRACTS section 1 now limits J/evaluation to safe projections and custody references, makes J/gold learning-only, and explicitly keeps protected predictions, attempts, diagnostics, reasons, logs and complete reference rows outside developer-visible J. T13 carries the same acceptance boundary, including safe held-out manifests. Backups and exports are covered.
- R2: CONTRACTS section 8 records blind_first, model_assisted and legacy_unknown presentation modes. EVALUATION sections 3 and 9 require independent initial judgments before prediction/model-identity disclosure and preserve later reconciliation separately. T10 and T19 reflect this distinction in acceptance. Implementation should preserve the existing final-test skill's gold-before-execution ordering and test the blind-first transition, rather than treating the presence of a metadata field as proof of independence.
- R3: EVALUATION section 7 now requires a common independent outcome standard for Meaning workflow comparisons, distinguishes within-guideline consistency, addresses an evolving human conception, and declines unsupported cross-method accuracy comparisons when no common target exists. T20 requires this protocol in study tickets. Expression-only comparisons keep meaning and reference releases fixed.
- R4: The dependency table now makes T14 depend on T09, T10 and T12.

Verdict: approve the revised evaluation, Expression Loop and production/audit plan as an implementation specification. No remaining blocking contradiction was found in the amended sections. This approval remains scoped to the design; access isolation, blind-review behavior, execution recovery and scientific quality/speed claims still require the stated implementation and evaluation evidence. No production files were edited and no experiment was run during this verification.
