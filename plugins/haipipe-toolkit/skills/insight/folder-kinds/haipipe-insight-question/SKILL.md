---
name: haipipe-insight-question
description: >-
  InsightBoard Folder contract for one rung-facing
  Question register. Owns question birth, target rung, queue state, and the
  Page and Task faces without concluding the answer. Use to raise, retarget,
  queue, or audit an Insight question. Trigger: insight question, question
  register, QD QI QK QW, folder-kind question, /haipipe-insight-question.
metadata:
  version: "1.9.0"
  last_updated: "2026-10-02"
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
`../../haipipe-insight/ref/question-groups.md`. For what would answer a
question, read `../../haipipe-insight/ref/evidence-needs.md`: the evidence
needs on each row are the one join of Logic, Work and Report. For Page authoring and closure,
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
eligible partition column is a derived Question Group: MT02 column `<partition>` is
`QG-<partition>-I`, and MT04 column `full` is `QG-full-W`. A Question Group is never a fifth
register or a Folder. One row may contribute cells to several groups while
retaining one id and one origin.

## Input

Questions have two legal births: need-first from BR00's `Insight Needs Raised`,
or insight-first from a reader observing a gap on this board. Record raiser,
target rung, why now, what would answer it (in words, then as evidence needs),
affected partition(s), and blocked Aim. No preferred answer is admissible: "do nothing" and a null must remain
admissible answers.

**Expected (optional, JL 261001).** The register may record what the asker
expects BEFORE any run exists: the board's hypothesis. It is a recorded
prior, not a preferred answer. It is written once, never edited after the
first run of the question lands, never cited as evidence, and never handed to
the next rung. Its use is afterwards: an answering page that departs from it is a
surprise worth reading, and one that matches it confirms a belief. A missing
Expected line is legal and is shown as "none recorded".

A pre-climbed external-parent bridge is still an ordinary Wisdom question. Its
QW row additionally records the Task Insight instance, item, execution version,
RF id, and Result path
being evaluated plus the one local Wisdom W Folder that will contextualize it. The
borrowed RF is evidence for the question, not its Application answer.

## Page Face

On a Prototype board (`../../haipipe-insight/ref/prototype-contract.md`) each
question is one question file v2 in its own folder, holding the same fields
the register division below holds: the Queue's short wording (`question:`),
the short name (`name:`), the ask, Why now, What would answer it, the needs and
the agreed mark. On a register board:

Division 1 is the Queue; later divisions are one question each in id order,
each headed `#### N · <QID> · <Short Name>` (five words or fewer; the Insight
workbench prints it beside "Question N") with these fields, one paragraph each:

```markdown
#### 5 · QI4 · Temporal Dynamics

**The ask**: <the full question>
**Why now**: <why the board needs it>
**What would answer it**: <the evidence that would settle it, in words>
- E1 · compute · <what a run must produce> · pass: <what a result must show>
    cut: <partition> | the cell's partition | cross
    unit: <what one row is>
    measure: <the quantity>
    by: <the grouping or the contrast>
    uncertainty: <the interval or test>
    rivals: <the rivals adjusted for, or none>
    output: <file>.csv [<column>, …]
- E2 · cite · <what is borrowed> · from: QI3.E1
**Needs agreed**: ⬜ | ✅ <YYMMDD>
**Expected**: <optional · what the asker expects, written before any run>
**Where it stands**: <state, pointing at the Queue>
```

**Evidence needs (JL 261001).** The lines under **What would answer it** are
the question's evidence needs, `<QID>.E<n>`, each `compute`, `cite` or
`judge` (`../../haipipe-insight/ref/evidence-needs.md` § 1); every compute
need carries its work spec on the indented lines below it. They are planned
before any run or task is looked at (`haipipe-insight-evidence-plan`), agreed on the
**Needs agreed** line by an independent reviewer agent that did not draft them, bound by the answering page (`answers.yaml`), and cited
by its text. Once a bound result exists a need is never edited: append
`· retired: <reason>` and add a new id. A row with no need lines is
unplanned: legal on a board made before this contract, and reported by
`haipipe-insight-check`.

The Queue row keeps the question SHORT and plain (the workbench's question
line); the long form belongs in **The ask**.
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
`draft/records/<stem>-log.md`.

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

## Workbenches

- `outline` required, including Context links to an originating Brief need;
- no active PageX or Probe lane: a register records identity and state, not
  evidence;
- `code` and analysis Runs forbidden: the register records questions and state.
- `runs` only for explicitly commissioned Page Writing/Delivery Runs under the
  shared Page contract; routine registration and settlement create no Run.

## The question review (Q1-Q7)

Whether a question is a GOOD question is judged before its needs are run, by
a reviewer agent that did not write it, on seven tests. The check
(`haipipe-insight-check`) only flags suspects for Q1, Q2, Q4 and Q6 as notes;
the review reads the question.

```text
Q1 one thing     the ask asks one question; two joined by "and" are two questions
Q2 logic         the needs form one argument from the observed to the answer: each need
                 is read by the next (a judge reads every compute and cite it rests on)
Q3 consumer      Why now names who waits on the answer (a higher question, a design,
                 a replication target) and what they do with it
Q4 rung          the ask belongs at its rung: Data observes, Information derives with no
                 cause word, Knowledge claims with rivals, Wisdom counsels
Q5 answerable    the extract can carry it (a field exists, a partition is not
                 degenerate on it) or the refusal is itself computed
Q6 new           no other question already asks it or computes the same table
Q7 open          no preferred answer: a null and "do nothing" stay admissible
```

The review writes one verdict per question, `keep`, `split`, `merge` or
`move`, each with its reason, and for a split the small questions and the one
line of logic that joins them. **It proposes; a person signs.** Nothing is
split, merged, moved or reworded by a rule or by the reviewer. A signed change
retires the old question with its reason (`retired:` on its needs, a
successor id) and never edits it in place; a carried question
(`ref/carry_over.py`) keeps its words until a signed change replaces them.

## Gate and Closure

GI1 passes for one question when the question review has a verdict for it
(`keep`, or a signed change applied) and its id prefix agrees with `question-rung:`,
origin and answerability test are complete, its evidence needs are written
with kinds legal at its rung, and every eligible partition has an explicit
Queue cell. Those cells derive their Question Group memberships;
no separate group acceptance exists. A bridge QW additionally requires its exact
instance/item/version/RF packet and local W Folder. GI6 closes the registered chain only
when its target rung is terminal, `haipipe-insight-check` finds no overclaim on
the cell (every need bound, fit, cited and current), and every partial final
has a reason on its target Folder; for a bridge, that terminal is the signed local Wisdom Folder, never
the external RF. Under a current `UNDETERMINED` partition verdict, a non-template
W cell may settle `🟡 <page> final` only when the answering W Page records the
exact unresolved blocker and what could resolve it, and quotes the licensing
sentence in `ref/partition-policy.md`. The W Page receipt and this register's
GI6 receipt both quote that sentence; the partial exit creates no GI5 pass,
signature, or Design input. If the evidence remains obtainable within the
frozen Workflow, keep the cell open instead. An empty register is valid and
closed as a register.

## Handoff

Hand the next rung a neutral question id, exact ask, its evidence needs,
target, scope/partition, answerability test, and blocked Aim. A bridge handoff also carries the exact
item Result/RF packet to Wisdom. Never hand it an anticipated result or Design
permission.

## Files

- Runtime: `0-MT-meta/MT01-question-data/` through `MT04-question-wisdom/`
- A settled cell names its answering page: `✅ <page id>` (`✅ <L><NN>-<partition>`), `🟡 <page id>
  final`, or `🚫 <reason>`. The page's state line names the question back
  (`answers QI2`); one page may answer several questions, and the cell is the join.
- A ✅ cell that `haipipe-insight-check` reports GAP, STALE or UNBOUND is an
  overclaim: the register pen drops it to 🟡 until the page is fixed.
- Queue grammar is owned here; register receipts live at
  `<register>/draft/records/<register-stem>-log.md`; no private scripts.
- Question Groups are derived by
  `../../haipipe-insight/ref/question-groups.md`; no group path is created.
