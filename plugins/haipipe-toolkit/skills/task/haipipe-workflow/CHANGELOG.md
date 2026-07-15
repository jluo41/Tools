haipipe-workflow — Changelog
============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [2.4.0] — 2026-07-14

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14).

- **ref/plan-schema.md: the `answers:` report field is DELETED.** It was a top-level flow list of external ids naming what a run answered — the return half of a mailbox mechanism that no longer exists. A report describes what a run DID; it never names anyone downstream, because the executor layers do not know that anyone IS downstream. Replaced by a "Deleted fields" note pointing at the real mechanism: when a run answers a question, the answer is a FILE (`<leaf>/QA/<n>-<slug>.md`), and the asker reads it. Nothing is written back, no id is recorded, no field points outward.
- SKILL.md: the skill-family tree drops the retired evidence-gateway hop — a consumer holds its own evidence questions and dispatches them straight to an executor orchestrator as a sub-workflow (a question out, a path back). The family list is task / discovery / paper / application.

## [2.3.0] — 2026-07-04

- description lifecycle restored to 4 acts (Plan/Build/Execute/Report) and retired 'narrative' family replaced with paper/application; template.workflow.js doc pointers skills/flow/ -> skills/task/.

## [2.2.0] — 2026-07-04

- ref/plan-schema.md example agentType haipipe-task-reviewer-agent (was retired run-script-reviewer-agent).

## [2.1.0] — 2026-06-08

- restore 4-step lifecycle (Plan/Build/Execute/Report); build generates .workflow.js from plan.

## [2.0.0] — 2026-06-08

- add lifecycle (Plan/Execute/Report), file tracking, template vs specific, sub-workflow boundary rule.

## [1.0.0] — 2026-06-08

- initial skill — plan/build/run/inspect/template.
