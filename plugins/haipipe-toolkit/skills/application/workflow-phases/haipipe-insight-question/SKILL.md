---
name: haipipe-insight-question
description: >-
  InsightBoard workflow phase I1 and Folder contract for one rung-facing
  Question register. Owns question birth, target rung, queue state, and the
  Page and Task faces without concluding the answer. Use to raise, retarget,
  queue, or audit an Insight question. Trigger: insight question, question
  register, I1, QD QI QK QW, folder-kind question, /haipipe-insight-question.
metadata:
  version: "1.0.2"
  last_updated: "2026-08-31"
  workflow: haipipe-insight-workflow
  phase: I1
  folder_kind: question
  primary_face: page
  page_ruling: none
  legacy_page_type: question
  group-token: "MT"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Queue, always first; every later division's first word is a question id Q[DIKW]<n>, in id order"
---

# /haipipe-insight-question · make the board's ask explicit

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.
Existing registers may retain `page-type: question`; new ones use
`folder-kind: question` plus `question-rung:`.

## Position

I1 follows GI0 and precedes the first runnable D/I/K/W rung. Four Question
Folders live beside Meta:

```text
MT01-question-data          question-rung: data
MT02-question-information   question-rung: information
MT03-question-knowledge     question-rung: knowledge
MT04-question-wisdom        question-rung: wisdom
```

## Folder Kind

A Question Folder is a register, never an answer. Each question has one stable
`QD|QI|QK|QW<n>` id and one owning register. Retargeting moves the record; it
does not clone it.

## Input

Questions have two legal births: need-first from BR00's `Insight Needs Raised`,
or insight-first from a reader observing a gap on this board. Record raiser,
target rung, why now, what would answer it, affected partition(s), and blocked
Aim. No preferred answer is admissible.

A pre-climbed external-parent bridge is still an ordinary Wisdom question. Its
QW row additionally records the exact Task Insight Page and `RF<n>@<version>`
being evaluated plus the one local I5 W Folder that will contextualize it. The
borrowed RF is evidence for the question, not its Application answer.

## Page Face

Division 1 is the Queue; later divisions are one question each in id order.
The Queue shows the current Folder ids and canonical marks (`⬜`, `🟡`, `✅`,
`🚫`) per partition where applicable. It asks and tracks; it never contains a
D/I/K/W conclusion.

## Task Face

Classify the minimum rung that can answer the ask; mint or resume the target
Folder; update the Queue from phase receipts; preserve partial-final reasons;
and propagate reopening when a cited parent changes. The register pen writes
queue state; target Folders write receipts in their own
`outline/<stem>-log.md`.

For the pre-climbed external-parent bridge, verify the five assertions owned by
`haipipe-insight-workflow`, write the Task Page/RF version and local W Folder on
the QW row, and reopen that row whenever the RF or one of its source versions
changes. Never mark the row terminal merely because the Task RF is settled.

## Plugins

- `outline` required;
- `pagex` optional for the originating Brief need or lower-rung register;
- `probe` and `code` forbidden: the register dispatches work but does not do it.

## Gate and Closure

GI1 passes for one question when its id, rung, origin, answerability test, and
initial Queue cell are complete. A bridge QW additionally requires its exact
Task Page/RF version and local W Folder. GI6 closes the registered chain only
when its target rung is terminal and every partial final has a reason on its
target Folder; for a bridge, that terminal is the signed local I5 Folder, never
the external RF. An empty register is valid and closed as a register.

## Handoff

Hand the next rung a neutral question id, exact ask, target, scope/partition,
answerability test, and blocked Aim. A bridge handoff also carries the exact
Task Page/RF version to I5. Never hand it an anticipated result or Design
permission.

## Files

- Runtime: `0-MT-meta/MT01-question-data/` through `MT04-question-wisdom/`
- Queue grammar is owned here; register receipts live at
  `<register>/outline/<register-stem>-log.md`; no private scripts.
