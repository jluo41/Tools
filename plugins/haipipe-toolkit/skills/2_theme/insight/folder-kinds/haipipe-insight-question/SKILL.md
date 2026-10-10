---
name: haipipe-insight-question
description: >-
  The insight questions on the ladder: how a question gets into a Prototype
  release and how it changes. Owns the proposals (proposals/<slug>.md: new
  question · fix · retire · cut, written by a Board's or a Job's Propose Run),
  their triage into one release per batch, asking a question into a release
  (its id, its tNN, its question.md), and the question review (Q1–Q7, with
  haipipe-question-review). Never answers a question and never signs. Use to
  propose, triage, ask, change, retire or review an insight question, or to
  read the older question registers until they are carried over. Trigger:
  insight question, propose a question, proposals, triage, ask a question,
  question review, folder-kind question, /haipipe-insight-question.
metadata:
  version: "2.0.1"
  last_updated: "2026-10-09"
  workflow: haipipe-insight-workflow
  folder_kind: question
  primary_face: page
  page_ruling: none
  legacy_page_type: question
  group-token: "MT"
  outline:
    mode: grammar
    source: "ref/register-question.md"
    shape: "an older register: division 1 is Queue, always first; every later division's first word is a question id Q[DIKW]<n>, in id order"
---

# /haipipe-insight-question · from a proposal to a question in a release

## Position

Load `haipipe-insight` (`ref/insight-ladder.md`, `ref/release.md`). A question lives in a Prototype release, one
Task per question: `work/Prototype-bNN-<Topic>/jNN_pN_<slug>/tNN_<L><NN>_<slug>/question.md`
(`haipipe-insight/ref/block-contract.md` § The question file: id, level, the short question, the ask, Why now, What
would answer it, the partitions it is asked on, its needs, agreed). This skill owns how a question gets there and
how it changes; whether it is answered is the Board's.

```text
the Board, a Job ──propose──▶ proposals/<slug>.md ──triage──▶ a release ──ask · change · retire──▶ question.md
                              (open)                         (taken-in: pN)                       (agreed by another agent)
```

## Folder Kind

A question is one Task of a release, `tNN_<L><NN>_<slug>/`, holding its `question.md` and its one script; it is never
an answer. Its id `<L><NN>` fixes its level; its `tNN` stays the same in every release and every Board Job.

## Input

**Proposals** are the only way a question, a fix, a retirement or a cut reaches a release. One file each, `proposals/<slug>.md`:

```yaml
---
kind: new question          # new question · fix · retire · cut
level: information          # the DIKW level it would sit at (blank for a cut)
from: j03                   # the Job, report or reading it came from (coverage, q02, a vs-previous row)
state: open                 # open · taken · declined
taken-in: ''                # the release that took it
---

# <a short title>

<why, in a line or two: the gap, the weak answer, the new field, the cut and why it is asked about>
```

Three Runs write them, and write nothing else: a Job's `run-propose-j<NN>` (new or changed questions from its
comparison, and what it could not answer), the Board's `run-propose-coverage` (a DIKW level with no question, a cut
with no answer) and `run-propose-cut-<slug>`. `insight_ladder.py propose` makes the file. A proposal records no
preferred answer: "nothing changes" and a null stay admissible.


**Triage.** `run-triage-proposals-pN` takes one batch into one release, never one proposal at a time (decided 261008): the
newest release while it is open, otherwise the next one. Each proposal is taken (`taken-in: pN`), declined with a
reason, or left open for a later batch. `python scripts/proposals.py list | take <slugs> --into pN | decline <slug>
--why "…"` records it and prints how to apply each taken one:

```text
new question   insight_ladder.py question <release> <L><NN> <slug>     run-ask-<l><nn>
fix            insight_ladder.py change <release> <L><NN> --why "…"     then plan, review, script, review again
retire         insight_ladder.py retire <release> <L><NN> --why "…"
cut            the release's partitions.md, then run-set-cuts-pN         a person signs the cuts
```

## Page Face

The question's page is its `question.md` (`haipipe-insight/ref/block-contract.md` § The question file): the YAML block
(id, level, the short question, name, the ask, method, partitions, needs, agreed, signed), then its prose (**Why now**,
**What would answer it**, any field it was carried with). The short question stays short and plain, the long form is
the ask; the page asks and never concludes.

## Task Face

`run-ask-<l><nn>` asks one question into an open release from plain words: the minimum level that can answer it
(D observes · I derives inside a cut, no cause word · K claims across results, with rivals · W counsels), its id
`<L><NN>` (the next number at that level, never reused, a retired one included), its Task `tNN_<L><NN>_<slug>/`
(`tNN` the next number in the Prototype, kept in every later release and every Board Job) and its `question.md`. It
never answers the question. Its needs come next, from `haipipe-insight-evidence-plan`, agreed by another agent.

A question may record **Expected** before any run: the asker's prior, written once, never edited after the first
run, never cited as evidence. A page that departs from it is a surprise worth reading.

**Change and retire.** A question in a signed release never changes. A fix is carried into the next release under
the same `tNN` (`insight_ladder.py change`): its `changes:` list says what changed in which release, and its
`agreed:` resets. A level change is a new id at the new level, its `source: {from: [<old id>]}` named, and the old
one retired. A retired question leaves `questions:` for `retired:` in release.yaml with its reason.

## Workbenches

```text
run-triage-proposals-p<N>   Prototype › Description   haipipe-insight-agent            signs none
run-ask-<l><nn>             Release › Work Details    haipipe-insight-agent            signs none
run-propose-j<NN>           Job › Audience Report     haipipe-insight-agent            signs none
run-propose-coverage        Block › Audience Report   haipipe-insight-agent            signs none
run-propose-cut-<slug>      Block › Description       haipipe-insight-agent            signs none
run-review-questions-p<N>   Release › Work Details    haipipe-insight-reviewer-agent   a person signs a change (skill haipipe-question-review)
```

Their cards are `haipipe-insight-workflow/ref/run-cards.md`; no code or analysis Run belongs to a question here.

## Gate and Closure

`run-review-questions-pN`: before a release is signed, a reviewer agent that wrote none of its new or changed
questions judges each through `haipipe-question-review` (the seven tests; keep, split, merge or move; a person signs a
change; never a reworded ask). What insight adds:

- **Q4 the level is the level**: Data observes, Information derives with no cause word, Knowledge claims with rivals,
  Wisdom counsels.
- **Q5 answerable is the extract**: a field exists, a cut is not degenerate on it, or the refusal is itself computed.
- `haipipe-insight-check` only flags suspects for Q1, Q2, Q4 and Q6 as notes; the review reads the question.

- A question passes into a signed release only when its needs are agreed by another agent
  (`agreed: ✅ <YYMMDD>`), its script is reviewed by another agent, and the review has a verdict for it; then a
  person signs the release (`haipipe-insight/ref/release.md` § Signing).

## Handoff

Hand the evidence plan (`haipipe-insight-evidence-plan`) and, through the release, the Board a neutral question id,
the exact ask, its level, the cuts it is asked on and its agreed needs. Never an anticipated answer or a Design
permission.

## Files

```text
proposals/<slug>.md · proposals/README.md                       the backlog (Prototype)
jNN_pN_<slug>/release.yaml                                      questions · retired
jNN_pN_<slug>/tNN_<L><NN>_<slug>/question.md · scripts/          a question new or changed in that release
scripts/proposals.py                                            list · take · decline
```

A register board's four question registers (MT01-MT04, the Queue, GI1 and GI6) and an Insight Block's questions keep
their contract in [`ref/register-question.md`](ref/register-question.md), word for word, until each is carried into
a release (`haipipe-insight/ref/prototype_from_block.py`, after `ref/carry_over.py` for a register board).
