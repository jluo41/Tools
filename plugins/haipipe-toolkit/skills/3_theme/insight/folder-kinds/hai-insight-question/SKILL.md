---
name: hai-insight-question
description: 'Define and revise neutral questions in a Question Book release: proposals, batch triage, question
  definitions and independent review. Never answers data questions or signs a release. Trigger: insight question,
  proposals, question review, /hai-insight-question.'
metadata:
  version: 2.0.1
  last_updated: '2026-11-27'
  workflow: hai-insight-workflow
  folder_kind: question
  primary_face: page
  page_ruling: none
  legacy_page_type: question
  group-token: MT
  outline:
    mode: grammar
    source: ref/register-question.md
    shape: 'question register: division 1 is Queue; each later division begins with a Q[DIKW]<n> question id, in
      id order'
---

# /hai-insight-question

Load `hai-insight` and `hai-insight/ref/insight-ladder.md`. A Question Book Job is a question-set version. A Task defines a question; Board answer Tasks execute and interpret it on fixed data.

## Question source

A new or changed question lives at `InsightQuestionBook-〈topic〉/jNN_question-vN_〈slug〉/tNN_〈L〉NN_〈slug〉/question.md`. Its id is stable and never reused. The release's `questions` map is the complete membership; a kept member points to its source Task rather than copying it. Do not assume the list of local Task directories is the version.

`question.md` holds the id, level, short question, ask, method, segments, needs, agreement and the rationale: why ask now and what would answer it. The page asks without asserting the outcome. A declared Expected value is a prior, fixed before execution and never evidence.

## Propose

Write one proposal in the Book's `proposals/〈slug〉.md`:

```yaml
kind: new question   # new question | fix | retire | cut
level: information  # DIKWX level; omit for a segment
from: j03           # exact source Job, report or finding
state: open         # open | taken | declined
taken-in: ''        # question-vN when accepted
```

Explain the gap and its evidence. `cut` is the machine word for a segment. Keep a null result and no change admissible. A proposal is not a new Job or an answer.

## Triage a batch

Use `scripts/proposals.py` for list, take and decline operations; inspect its help for exact arguments. One triaged batch belongs to one version, using the open version or opening the next. Accepted proposals name `taken-in`; declined proposals retain the reason; unresolved ones stay open.

Apply through `hai-insight/scripts/insight_ladder.py`:

```text
question <release> <L><NN> <slug>       define a new neutral question
change   <release> <L><NN> --why …      revise it in the target version
retire   <release> <L><NN> --why …      remove it from this release, keeping its reason
```

A segment change belongs in that release's partitions.md and requires the person's segment signature. Do not make one version Job for every proposal.

## Define and review

Choose the minimum level supporting the ask: Data observes; Information derives within a segment without causal wording; Knowledge tests claims and rivals across results; Wisdom counsels within supported limits; Executive synthesizes cited answers for decisions.

Plan the required evidence with `hai-insight-evidence-plan`. A different agent agrees the needs. Compute needs require scripts and independent script review. Question review uses `hai-report` Q1–Q7, with particular checks that the level is justified and the actual extract can supply the evidence or a computed refusal.

A signed question version cannot be edited. A changed question retains its id and Book tNN in the target version and resets agreement. A level change receives a new id and links the source id; retire the original with a reason. Release retirement records remain in `release.yaml` and ids are never recycled.

Before the person signs the release, each new or changed question has its independent agreement, required script review and question-review verdict; segments are signed. This skill never supplies the signature or invents a preferred answer.

## Workbench and handoff

Version Main carries the motivation, evidence, goals, Plan + Results, Findings and review. Each question Task exposes its definition, needs, method, script and review. Show retained members with their source. The Board receives question ids, exact asks, levels, segments and agreed needs by release reference; it does not receive an assumed outcome or Design permission.

The run-cards source is `hai-insight-workflow/ref/run-cards.md`. Triage, ask, propose and review are operations with their owners, not extra Job/Task types. Use the shared Block UI and current Studio bindings through `workbench-insight`.
