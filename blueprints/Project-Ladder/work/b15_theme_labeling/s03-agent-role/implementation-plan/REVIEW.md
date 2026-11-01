# Plan review and baseline evidence

Version 1, 2026-10-27. Status: reviewed implementation specification. Three specialist reviews, coordinator corrections and specialist re-reviews are complete. Production implementation has not started in this planning turn.

## 1. Independent source audits

Three planning agents inspected different boundaries in parallel. Their audit memos are retained under reviews/ with machine-specific paths normalized to portable repository placeholders:

- workbench-audit.md: actual routes, persistence, authentication, UI integration and migration.
- meaning-audit.md: semantic authority, source provenance, rule reports, references and asynchronous behavior.
- expression-audit.md: executor code, data separation, quality/speed evaluation, qualification and scale.

These audits are design evidence. They did not execute a real labeling experiment or implement production features.

## 2. Coordinator dispositions

| Finding or disagreement | Coordinator decision | Where reflected |
|---|---|---|
| Workbench has item actions, not decision-report submit/save | Build a real new-mode view and engine store, then verify actual browser persistence | T01–T05 |
| Audit suggested new meaning/ storage; early draft reused rounds/ | Adopt J/meaning/ for rule-level records; keep rounds/ unchanged for legacy item events | CONTRACTS section 1 |
| One audit treated all choices as preferences; another allowed exact rule approval | Exact displayed patch plus clear selection can approve that exact scope; custom/qualified comments need interpretation confirmation | T09 and submission contract |
| Prototype exports explicitly say rule_preference_only | Preserve that narrow scope on import; never retroactively upgrade it | T09 |
| Early draft listed publish as browser action | Publication/integration initially remain engine/command-line tools; browser only reads/responds | CONTRACTS section 12, T04 |
| Existing human_id and attest do not verify identity | Label evidence accurately; external respondents need authenticated assigned-job permission | T04 |
| Existing shared non-owners cannot POST | Do not grant broad owner access to bypass this; retain disabled shared response until narrow capability exists | T04 and PLAN |
| Current test workflow selects a model on sealed test | Separate aggregate validation selection from independent final qualification | EVALUATION sections 2–4 |
| Both partitions can be labeled without both developing meaning | Separate developer, executor and scorer contexts and storage | T06, T10, T13 |
| Existing policy components do not include canonical rules.json | Add an explicit new-mode manifest/validator adapter; do not pretend legacy support exists | CONTRACTS section 1 and T01 |
| Existing hash-based code conflicts with repository no-hash rule | New components introduce no hashes; any touched legacy preparation migration must be scoped, explicit and tested | T06 |
| Many Run names and skill gates describe unbuilt capabilities | Treat inventory declarations as plans; show unavailable states until implementations and checks exist | PLAN section 4 and T16 |
| Small cross-model gap alone can reward poor quality | Absolute floors, coverage and stronger-model regression constraints precede gap preference | EVALUATION section 5 |
| Provider completion can precede local durable write | Represent uncertain attempts and reconcile; do not promise exactly-once provider execution | T18 |
| Risk-selected audits cannot estimate population quality alone | Add probability sampling and appropriate estimators | T19 |

## 3. Baseline actually executed

From the Tools checkout, using the owning workspace's .venv/bin/python, the coordinator ran the following existing targeted tests with bytecode/cache output disabled:

    PYTHONDONTWRITEBYTECODE=1 <repository-python> -m pytest -q -p no:cacheprovider \
      plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_definition_discussion.py \
      plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_calibration.py \
      plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_corpus_tools.py

Observed result: 36 passed in 2.73 seconds.

This establishes a narrow existing-engine baseline only. It does not validate proposed form persistence, new loops, production labeling, data isolation or model quality. No paid executor, local GPU campaign, production scan or human study was run.

## 4. Assembled-package review and corrections

Each specialist reviewed the six authored documents after the source audit. The coordinator checked the findings, revised the contracts and assignments, then returned the changed sections for a second review. All three specialists reported no remaining blocker in their reviewed amendments. Their full review/re-review memos are retained alongside the original audits.

| Reviewer finding | Coordinator correction | Re-review outcome |
|---|---|---|
| Workbench F1: replay could fail after draft/report changed | Authenticated committed-request lookup precedes mutable revision checks; exact request envelope retained | Resolved |
| Workbench F2: lifecycle status conflicted with immutable payloads | Separate immutable events/receipts and rebuildable current_status projection | Resolved |
| Workbench F3: schema omitted none/reject-options | Explicit reject_options/rejected_options with no-patch semantics | Resolved |
| Workbench F4: host parses before action-level payload bound | R owns narrow pre-parse guard in H/serve.py; B owns action validation | Resolved |
| Meaning M1: an authority enum could self-confirm a source | Require committed scoped approval provenance; collector cannot self-promote | Resolved |
| Meaning M2: integration could publish half a release | Commit manifest published last binds policy, compatible/pending/excluded references, issues and invalidations | Resolved |
| Meaning M3: fresh request IDs could reapply partial-card answers | Stable answer IDs/revisions, decision-effect history and explicit supersession | Resolved |
| Meaning M4: policy mapping and partial reference coverage unclear | Explicit G_NN-to-mNN manifest binding; approved rules may have pending references but cannot support unsupported scores | Addressed |
| Expression R1: protected results appeared under developer J | Keep held-out predictions, logs, attempts and reference rows in custody; only safe projections in J | Resolved |
| Expression R2: independent judgments could be prediction-anchored | Blind-first reference and population-audit judgments, with separate assisted workflows | Resolved |
| Expression R3: workflows could score against their own generated answers | Common independent outcome standard for Meaning comparisons; fixed meaning/references for Expression comparisons | Resolved |
| Expression R4: T14 lacked its reference dependency | Add T10 to T14 dependencies | Resolved |

The coordinator also corrected source paths and the renderer filename, separated freeze_candidate from issue_handoff, replaced an exactly-once consumption claim with idempotent durable effects, and distinguished draft selection from explicit submission approval. Final clarifications retain the approved source payload revision during authority promotion and require final-reference lock before candidate execution.

Coordinator verdict: the package is ready for bounded implementation, beginning with T00/T01 and M1. This is approval of the specification and task decomposition, not approval of a deployed system or evidence of research benefit. All proposed engineering and research tests remain to be executed in their assigned packages.

## 5. Decisions intentionally left to implementation/study configuration

- Actual label schema, data groups and task-specific diagnostics.
- Exact evaluator model roster, unused transfer families and runtime configurations.
- Study-specific quality floors, noninferiority/equivalence margins and precision requirements.
- Corpus partition sizes, validation query budget and production audit sample plan.
- Whether deployment after the trusted-local M1 slice adds authenticated external participants.

These are configuration decisions, not permission blockers for the synthetic M1 slice. Use synthetic fixtures to implement the contracts. Do not invent real study values or launch experiments to resolve them without the user's instruction.
