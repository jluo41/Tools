# Delegation, integration and coordinator review

Version: 2  
Reconciled on 2026-11-01 to slide deck version 12 (Train and Test, Execution & Audit Agent, round report); version 1 was written against version 8.

This document is an execution contract for engineering agents. The coordinating agent remains accountable for design decisions, integration and final acceptance. Specialist approval is evidence, not a substitute for that review.

## 1. Team structure

Use at most three workers alongside one coordinator. All work occurs in the current shared workspace; do not create worktrees unless the user asks. Before each wave, the coordinator inventories changes, assigns exact files and sends the bounded task. Workers read applicable instructions and report any conflicting ownership before editing.

| Role | Responsibility | Must not do |
|---|---|---|
| Coordinator R | Freeze interfaces, assign scope, integrate, review real behavior, resolve disagreements | Declare completion from summaries alone |
| Engine/Meaning A | Contracts, durable feedback, sources, reports, integration, references, Meaning harness | Edit Workbench routes, or relax Test or confirmation custody |
| Workbench B | Renderer, interaction, response route, user states and browser evidence | Invent engine states or make browser data authoritative |
| Evaluation/Execution C | Train/Test custody, executors, scoring, the Step 5 staging loop and round reports, release readiness and scale | Change approved meaning, or use Test or confirmation cases to rewrite expression |

These engineering agents are separate from the runtime agents implemented by the system (the Meaning Loop Agent and the Execution & Audit Agent). Internal runtime helpers initially remain tools/services. Add autonomous subagents only when task isolation, latency or measured capability justifies them; do not multiply agents merely because a diagram has many boxes.

## 2. Ownership rules

One owner edits a file in a wave. B owns W/labeling.py; A owns new meaning_* modules; C owns new executor, evaluation and staging modules. Shared files such as E/job.py, E/cli.py, run_catalog.py and skill entrypoints are coordinator-controlled integration files unless explicitly reassigned for a wave. R also owns the narrowly scoped H/serve.py pre-parse size guard for the labeling response endpoint; this is a T04 dependency, not a general host rewrite.

If A needs a route change, A proposes the contract and B makes the edit. If C needs a Meaning schema extension, C supplies an example and rationale; A updates the schema after R approves the interface. Do not race to patch another worker's file. Do not delete or revert changes not made by the worker.

Keep a short handoff note at each package boundary: interface version, sample payload, error vocabulary, accepted/rejected states and test command. Interface changes after dependent work begins require a compatibility decision and updates to all consumers in the same integration wave.

## 3. Execution waves

### Wave 0: contracts and baseline

R verifies current checkout and baseline. A implements T01 with synthetic records. B studies current routing and prototypes the view against the agreed fixture only. C inventories custody and executor behavior and proposes T06 boundaries. R reviews the schemas before persistence and APIs are implemented.

Exit gate: no ambiguous actor authority, approval scope, Train/Test or confirmation visibility, record identity or version invalidation. Proposed filenames and paths are settled. No real model calls.

### Wave 1: first real form

A implements T02. B implements T03 and then T04 against A's store. C builds synthetic split/access fixtures for T06 without changing shared contracts unilaterally. R runs T05 in the actual Workbench.

Exit gate M1: a human can save/reload/partially submit; the server retains one immutable receipt; a fake integration worker receives it; errors and pending states are honest; legacy item actions still work.

### Wave 2: Meaning behavior

A completes T07–T11 in small reviewed increments. C completes custody and starts the executor adapter. B improves source display, issue states and integration feedback using the stable contracts. R checks exact-rule approval, custom-answer confirmation, contradictions, reference-label authority and the Step 2 investigation of synthetic round reports.

Exit gate M2: both entry cases lead through source-backed decision reports to versioned accepted meaning and appropriately approved references. The process waits only on dependent human choices. Test cases enter Meaning Loop work only by audit-issue reference, and no confirmation content reaches any agent.

### Wave 3: Step 5 staging behavior

C implements T12/T13/T15. A implements T14 and connects the T11 round report intake. B completes T16. R runs fake-executor scenarios where wording improves, semantics are missing, a model fails, quality plateaus, a Test issue reopens the Meaning Loop without reaching the rewriting context, and a round meets its criteria and routes to Step 6.

Exit gate M3: the staging loop can keep, reject, stop, reopen the Meaning Loop or proceed to Step 6 for the right reason, and every round writes a round report. It cannot silently change meaning, references or quality floors. Test aggregate disclosure and model-call budgets are observable.

### Wave 4: release and scale

C implements T17/T18, A implements T19, B exposes the relevant status using the same response/view conventions. R reviews recovery, audit math, version lineage and acceptance claims. Actual workloads remain separate authorized Runs.

Exit gate M4: a synthetic end-to-end release can pass its release readiness check, batch, resume, audit and deliver without lost items or false approvals. This engineering success does not establish real-world accuracy or throughput.

### Wave 5: experiments and communication

R prepares T20 Run tickets and coordinates source/skill/slide updates. After the user starts the actual study, record measured outcomes using its protocol. R separates completed implementation, demonstrated engineering behavior and research findings in the final report.

## 4. Ready-to-send worker prompts

Use the following as templates. Replace the allowed packages and exact owned files before dispatch. Do not send the entire roadmap as an unbounded mandate.

### Agent A: durable form slice

Read PLAN.md, CONTRACTS.md, WORK-PACKAGES.md and applicable repository/labeling instructions. Implement T01 and T02 only, in the exact new engine files assigned by the coordinator. Inspect existing job lane resolution and locking before choosing an adapter. Create synthetic source/report/draft/submission and round report fixtures; implement validation, immutable publication, compare-and-swap drafts, idempotent atomic submission and a durable integration outbox. Preserve legacy rounds. Do not edit Workbench routes, run real models, promote rule feedback into item gold, introduce hashes or touch unrelated files. Give B a stable Python API and fixture after T01 review. Return changed paths, tests actually run, recovery evidence and unresolved contract issues. Stop at a tested engine slice rather than implementing later Meaning behavior prematurely.

### Agent B: Workbench form slice

Read the plan package and current labeling Workbench implementation. Own the exact view/assets and labeling.py changes assigned for T03/T04. Build a renderer from structured reports inside the building Task's Decide view on the focus page (labeling_focus.py; b15 s13 maps Steps 2 and 3 to it, s58 C2 draws it). Connect save/submit through the existing labeling action route and A's store. Enforce server-resolved job/actor authority, escape all source/comment text, support none/defer/custom/partial submission and display draft/submitted/pending states. Do not generate executable form HTML from model output or add publication/integration as browser powers. Preserve legacy item labeling. Use synthetic data for browser checks; prove reload persistence, duplicate-submit behavior and stale revisions. Do not claim verified identity from a typed human ID. Return screenshots plus persisted-record/API evidence and any unavailable shared-participant support.

### Agent C: data boundary and evaluator foundation

Read CONTRACTS.md and EVALUATION.md plus actual corpus/label executor code. Work only on assigned T06/T12 files and synthetic tests until the coordinator opens later packages. Design enforceable Train, Test and confirmation projections and executor, scorer and auditor contexts; audit search, embeddings, logs, caches and tool responses for leakage into the expression rewriting step. Adapt fixed-weight executor calls without exposing references to executors, or Test case-level content to the expression rewriting step. Record failures, abstentions, runtime settings and every requested item. Do not run paid/local GPU experiments, start production scans, rewrite expression from Test cases, touch the confirmation set, change human meaning or introduce content hashes. Return an access matrix tested against synthetic fixtures, fake-transport test evidence and a specific list of remaining enforcement limitations.

### Independent reviewer after each milestone

Inspect the actual diff and run the smallest relevant checks in the current shared workspace. Compare behavior with the package contracts, not only the author's summary. Focus on approval scope, durable state, Test and confirmation leakage, round report routing, semantic drift, failure recovery, legacy compatibility and misleading UI claims. Do not edit files owned by active workers. Return findings with severity, exact file/function, reproduction and smallest fix. Distinguish blocking defects from optional improvements. If no blocker is found, state the tested scope and what remains untested; do not issue blanket production approval.

## 5. Coordinator review gates

| Gate | Required evidence | Blocking examples |
|---|---|---|
| R0: scope and ownership | Actual changed files and assigned owner | Unrelated edits, competing stores, hidden feature expansion |
| R1: contracts | Valid/invalid fixtures and consumer compatibility | Ambiguous authority, stale option remapping, unclear label approval |
| R2: persistence | Atomicity, replay, conflict and restart checks | Lost submissions, duplicate integrations, mutable receipts |
| R3: user behavior | Real Workbench browser + persisted record | Screenshot-only demo, false saved/approved status, hidden defaults |
| R4: data separation | Negative access tests across tools/files/logs | Test case-level errors entering expression prompts or examples; confirmation content in any agent-visible root |
| R5: semantic authority | Exact patch and custom-comment scenarios | Rule meaning changed in Step 5, automatic gold from a rule or from executor consensus |
| R6: evaluation | Synthetic scoring, round report and frozen protocol tests | Gap-only selection, dropped failures, a round without a round report, optimization on the confirmation set |
| R7: operational release | Recovery/audit/handoff tests | Silent item loss, unsupported exactly-once claim, biased audit estimate |
| R8: communication | Sources, skills and slides match actual status | Planned capability presented as measured or deployed |

R reviews every milestone and resolves contradictory agent recommendations explicitly in REVIEW.md or the milestone review record. A failing gate returns to the owner with a reproduction and bounded fix. Recheck the failed path and directly affected paths; do not rerun unrelated expensive checks without a reason.

## 6. Verification levels and reporting

Use four separate labels:

- Specified: contract and task exist, no implementation claim.
- Implemented: source exists and targeted checks pass.
- Demonstrated: the real user/engine path has been exercised within stated conditions.
- Evaluated: an authorized real-data/model study produced interpretable evidence.

A package can be implemented without being demonstrated in the deployed Workbench, or demonstrated synthetically without evaluated research benefits. Report the narrowest true status. Planned metrics and imagined screenshots never count as results.

When a worker finishes, R reads source and evidence, checks shared-file diffs, reproduces the essential path and records accept/revise/defer. Accepted work unblocks dependent packages. Deferred optional improvements remain listed, not silently forgotten.

## 7. Permission, runtime and repository boundaries

Use the repository interpreter and existing generators. Changes under Tools must respect the current sandbox permission mechanism. Do not ask the user to reconfirm ordinary authorized edits merely because the work is split across agents. Never start compute/regression/model campaigns unless the user asks. Prepare their Run tickets instead.

Keep synthetic fixtures in public Tools; private corpus/human data belongs in the correct private job lane. Do not print credentials or load env.sh values into logs. Do not directly modify generated HTML, images, PDFs or slide decks; modify sources and regenerate. Preserve existing changed files. No worktree, commit or push is part of this plan unless explicitly requested.

For a server-code change, use the configured server/restart mechanism and verify the actual reader-facing configured origin. Do not launch an ad-hoc public server. If the required environment is unavailable, finish other tests and report the exact unverified surface.

## 8. First next assignment

Start with T00/T01 and the bounded M1 slice. The reviewable deliverable is one real Workbench decision report whose saved and submitted states persist on the server and whose feedback reaches a recoverable integration queue. It is deliberately small enough to inspect end to end, while preserving the contracts needed for the full two-loop system.
