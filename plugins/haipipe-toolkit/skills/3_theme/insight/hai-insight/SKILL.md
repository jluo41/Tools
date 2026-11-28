---
name: hai-insight
description: 'Create and maintain the Insight ladder: Question Book question releases, DataPrep code versions and
  Insight Board analyses over fixed versions. Route questions, preparation, evidence, Runs, reviews and signed Design
  handoffs. Trigger: insight, Question Book, DataPrep, DIKW, /hai-insight.'
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: 3.13.1
  last_updated: '2026-11-27'
---

# /hai-insight

Insight asks what data can and cannot support and keeps question definitions, preparation code and data versions independently identifiable. Read [ref/insight-ladder.md](ref/insight-ladder.md) before creating, naming or auditing its folders. Read [ref/dataprep.md](ref/dataprep.md) for preparation code and execution.

## Resolve the request

Read `board.md` first. Use the existing Block and its linked owners; do not create another Block merely because a dataset or topic was mentioned.

| Request | Owner and next reference |
|---|---|
| Question Book (`board-kind: prototype`), proposals or version | this skill; `hai-insight-question`; release membership in `ref/insight-ladder.md` |
| Insight Board (`board-kind: insight-board`), data versions or Jobs | this skill; `hai-insight-meta` for data metadata |
| DataPrep (`board-kind: insight-dataprep`), prep version or code step | `ref/dataprep.md`; `hai-task-for-data` for a step script |
| Board Job, answer Task or next Run | read `../hai-insight-workflow/SKILL.md` by path |
| One question's evidence requirements | `hai-insight-evidence-plan` |
| One Run's reading | `ref/run-report.md` and `ref/run_report.py` |
| A Task-side Insight Page | `hai-task` → `fn/insight.md` → `hai-page-insight` |
| UI or Studio design | `workbench-insight`, inside the owning Work Block |
| An unrecognized folder contract | inspect its declared owner and current files before proposing a mutation |

The workflow helper is loaded by path because it disables model invocation. Naming a topic does not authorize running every Job.

## The work

- Question Book: one Job per question-set version. Each member is a question definition; `release.yaml` is the authority, including retained Task references.
- DataPrep: one Job per preparation-code version. Ordered Tasks define steps; no step owns an execution Run.
- Insight Board: one Job fixes a question release and data version, plus a prep version when used. It holds answer Tasks and, for prep, a first Task running the entire chain. Computed question × segment work belongs in a Run.

A Board finding feeds proposals back to the Question Book. Triage a batch into a version; define or revise its questions, needs and methods; review them and obtain the person's signature. New data or prep code evolves independently. Do not invent a Job Type for each version or a Task Type for each step name.

## Responsibilities

| Skill | Responsibility |
|---|---|
| hai-insight | ladder, scaffold, question scripts, hard Run runners and Executive report |
| hai-insight-question | proposals, triage, neutral asks, changes and question review |
| hai-insight-evidence-plan | needs and work specs, with an independent review |
| hai-insight-meta | dataset and frozen data versions |
| hai-insight-data / information / knowledge | level-appropriate answers; Knowledge also compares and tests across results |
| hai-insight-wisdom | counsel and the signed Design handoff |
| hai-insight-check | coverage, tracks, answer alignment and close checks |
| hai-insight-workflow | Run routing and gates; each card names the worker |
| workbench-insight | reading and designing the shared Block UI |

## Execute through the contract

Use `scripts/insight_ladder.py` to scaffold the named operation, and `ref/run_job.py` / `ref/run_prep.py` for its tickets. Inspect the target and script help before a mutation; do not treat an inferred command as a supported flag. `audit <folder>` and `review <Board>` read current files; retain their concrete findings and any required rerun.

Question code exists once in its source release. Board tickets read that source. Generated result tables, figures, receipts and maps are changed through their generator. A Run's `report.md` is an agent's reading of its result and is checked independently.

The question id is stable and never reused. Retained questions are references, not copies. Board tNN positions may shift when prep occupies t01; the question id and release member source preserve identity.

An independent agent reviews questions, evidence plans, scripts and pages. A person signs the release, segments, prep version, Job close and Wisdom handoff when their gate requires it. Record only a signature actually stated by the person. Do not manufacture approval from task authorization.

Check power before contrasts; a supported refusal remains a result with its reason. Do not judge segments by whether their result is significant. Pages contain aggregates and evidence references, never patient rows.

## Deliver understanding

Brief states the motivation, evidence and desired result. Plan + Results stays together at each scope. Findings expresses what was learned and links its basis. Display one source across levels by reference.

A signed handoff names the finding, strength, evidence, version pins, boundaries and design consequence. Design reads the exact signed path and develops the design. A changed supporting result requires a new handoff; retain the signed record and its sources. Outcome feedback can form another data version.
