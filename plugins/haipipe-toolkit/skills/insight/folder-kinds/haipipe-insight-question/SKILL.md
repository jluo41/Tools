---
name: haipipe-insight-question
description: >-
  InsightBoard Folder contract for one rung-facing
  Question register. Owns question birth, target rung, queue state, and the
  Page and Task faces without concluding the answer. Use to raise, retarget,
  queue, or audit an Insight question. Trigger: insight question, question
  register, QD QI QK QW, folder-kind question, /haipipe-insight-question.
metadata:
  version: "1.3.2"
  last_updated: "2026-09-20"
  workflow: haipipe-insight-workflow
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

For registration, status, or dispatch, read
`../../haipipe-insight/ref/question-groups.md`. For Page authoring and closure,
read `../../haipipe-insight/ref/page-v2-adapter.md`.

## Position

Question owns registration and settlement. GI0 and GI1 constrain answering
Runs; registration itself is a control update without a Run identity. Four Question
Folders live beside Meta:

```text
MT01-question-data          question-rung: data
MT02-question-information   question-rung: information
MT03-question-knowledge     question-rung: knowledge
MT04-question-wisdom        question-rung: wisdom
```

## Folder Kind

A Question Folder is a register, never an answer. Each question has one stable
`QD|QI|QK|QW<n>` id and one owning register. The id prefix fixes its rung.
A changed target rung creates a successor ask in the destination register with
its next legal id and `supersedes: <old-id>`. Keep the old row, citations and
receipts; record `superseded-by: <new-id>`, and retire its open cells with an
explicit refusal reason. Previously settled cells retain their historical
marks. The successor starts with its own open cells and answerability test;
no completion or person signature transfers. Record both links in owner logs.

The register is one DIKW-axis slice of the board. Its intersection with each
eligible partition column is a derived Question Group: MT02 column B is
`QG-B-I`, and MT04 column F is `QG-F-W`. A Question Group is never a fifth
register or a Folder. One row may contribute cells to several groups while
retaining one id and one origin.

## Input

Questions have two legal births: need-first from BR00's `Insight Needs Raised`,
or insight-first from a reader observing a gap on this board. Record raiser,
target rung, why now, what would answer it, affected partition(s), and blocked
Aim. No preferred answer is admissible.

A pre-climbed external-parent bridge is still an ordinary Wisdom question. Its
QW row additionally records the Task Insight instance, item, execution version,
RF id, and Result path/hash
being evaluated plus the one local Wisdom W Folder that will contextualize it. The
borrowed RF is evidence for the question, not its Application answer.

## Page Face

Division 1 is the Queue; later divisions are one question each in id order.
The Queue shows the current Folder ids and canonical marks (`⬜`, `🟡`, `✅`,
`🚫`) per partition where applicable. Its partition columns plus this Folder's
`question-rung:` derive the `QG-<partition>-<rung>` handles; no group state is
written. It asks and tracks; it never contains a D/I/K/W conclusion.

## Task Face

Classify the minimum rung that can answer the ask; identify each eligible
`partition × target-rung` group; mint or resume the target Folder for one
selected cell; update the Queue from Page CLOSE plus Run and GI control receipts; preserve
partial-final reasons; and propagate reopening when a cited parent changes.
The register pen writes queue state; target Folders write receipts in their own
`outline/<stem>-log.md`.

For the pre-climbed external-parent bridge, verify the five assertions owned by
`haipipe-insight-workflow`, write the exact item Result/RF packet and local W Folder on
the QW row, and reopen that row whenever the RF or one of its source versions
changes. Never mark the row terminal merely because the Task RF is settled.

### Run Profile

Use the parameterized Run Specs in
`../../haipipe-insight-workflow/ref/run-workflow.md`. This Folder kind does
not itself allocate a Run. Declare a bounded Spec per selected Page writing,
evidence, delivery, or supporting computation target; use the worker's native
Ticket, Result, receipt, and close rule. Record each actual Run once in the
Insight Runtime, with its full owner address and exact input versions.
Routine resource updates and GI evaluations remain control records. An accepted
Run Result satisfies only its declared target; Page CHECK/CLOSE and the
Folder's GI conditions still govern citation and register settlement.

## Plugins

- `outline` required, including Context links to an originating Brief need;
- no active PageX or Probe lane: a register records identity and state, not
  evidence;
- `code` and analysis Runs forbidden: the register records questions and state.
- `runs` only for explicitly commissioned Page Writing/Delivery Runs under the
  shared Page contract; routine registration and settlement create no Run.

## Gate and Closure

GI1 passes for one question when its id prefix agrees with `question-rung:`,
origin and answerability test are complete, and every eligible partition has
an explicit Queue cell. Those cells derive their Question Group memberships;
no separate group acceptance exists. A bridge QW additionally requires its exact
instance/item/version/RF packet and local W Folder. GI6 closes the registered chain only
when its target rung is terminal and every partial final has a reason on its
target Folder; for a bridge, that terminal is the signed local Wisdom Folder, never
the external RF. Under a current `UNDETERMINED` partition verdict, a non-template
W cell may settle `🟡 <page> final` only when the answering W Page records the
exact unresolved blocker and what could resolve it, and quotes the licensing
sentence in `ref/partition-policy.md`. The W Page receipt and this register's
GI6 receipt both quote that sentence; the partial exit creates no GI5 pass,
signature, or Design input. If the evidence remains obtainable within the
frozen Workflow, keep the cell open instead. An empty register is valid and
closed as a register.

## Handoff

Hand the next rung a neutral question id, exact ask, target, scope/partition,
answerability test, and blocked Aim. A bridge handoff also carries the exact
item Result/RF packet to Wisdom. Never hand it an anticipated result or Design
permission.

## Files

- Runtime: `0-MT-meta/MT01-question-data/` through `MT04-question-wisdom/`
- Queue grammar is owned here; register receipts live at
  `<register>/outline/<register-stem>-log.md`; no private scripts.
- Question Groups are derived by
  `../../haipipe-insight/ref/question-groups.md`; no group path is created.
