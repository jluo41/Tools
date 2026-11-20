---
name: haipipe-insight
description: "The door for insight: a Question Book (the questions, a Job per release), a DataPrep Block (the tools that make the data versions, a Job per prep version) and an insight Board (one dataset, a Task per question, a Run per segment); scaffolds the ladder. Use to set up or update a Board or a DataPrep Block. Trigger: insight, Question Book, insight Board, DataPrep, data prep, DIKW, /haipipe-insight, /haipipe-insight update."
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "3.11.0"
  last_updated: "2026-11-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight · the Question Book and the insight Board

> **Hidden helpers** (JL 261026: not in the skill listing, `disable-model-invocation: true`): when this door names one below, read its SKILL.md by path; the Skill tool cannot load it. A person can still type its `/name`.
>
> - `haipipe-insight-workflow` → `../haipipe-insight-workflow/SKILL.md`
> - `haipipe-insight-bind` → `../haipipe-insight-bind/SKILL.md`

Insight asks what a dataset can and cannot say, level by level (D what it holds · I rates and contrasts inside a
segment · K what survives tests across segments · W the counsel a person signs for Design), and keeps the questions apart
from the data they run on. Read [`ref/insight-ladder.md`](ref/insight-ladder.md) before creating, naming, growing
or auditing any insight folder: it is the contract, and `scripts/insight_ladder.py` keeps its gates. A release, from
its proposals to its signature, is [`ref/release.md`](ref/release.md).

```text
Question Book   insight/InsightQuestionBook-<Topic>/      the questions + their scripts; a Job per release jNN_question-vN_<slug>/,
                                              frozen once a person signs it; proposals/ is its backlog
Board       insight/Insight-<name>/          one dataset, its dated versions (board.md versions:); a Job per
                                              release × data version jNN_question-vN-<slug>_data-vM/,
                                              a Task per question, a hard Run per segment runs/rNN_<segment>/
```

A release is a **question version**, `question-vN`, and a data version is `data-vM` (its `label:` in words): the same id on screen, in folders, faces and Run names (ref/insight-ladder.md, JL 261109). Both Blocks sit in `insight/`, side by side.

**How they work together.** A Board Job runs one signed release on one frozen data version and moves one clock from
the Job before it (`moved: start | data | code`). What a Job finds feeds back only as proposals in the Question Book's
`proposals/`; a triaged batch becomes the next release; the Board then adds a Job for it. New data needs no
release, a new release needs no new data, and a change in an answer has one cause.


Route
-----

Resolve the folder first, by its `board.md` (never its folder name), then load one owner:

| What the request names | Level | First owner |
|---|---|---|
| a Question Book (`board-kind: prototype`) | proposals · a version · a question | this door → the version's Run owner (§ Runs) |
| an insight Board (`board-kind: insight-board`, or `prototype:` in board.md) | data versions · Jobs · readings | this door → the Board's Run owner |
| a Board Job `jNN_question-vN-<slug>_data-vM/` or its Task `tNN_<L><NN>_<slug>/` | hard Runs · pages · compare | this door → `haipipe-insight-workflow` |
| a DataPrep Block (`board-kind: insight-dataprep`), a prep version `jNN_prep-vK_<slug>/` or a step `tNN_<step>/`; a Board data Job `jNN_prep-vK-<slug>_data-vM/` | the data's code (no Runs) · a Board runs it and makes its data version | [`ref/dataprep.md`](ref/dataprep.md); the runner `ref/run_prep.py`; a step's script → `haipipe-task-for-data` |
| a new topic | — | `insight_ladder.py prototype`, then `board` (ref/insight-ladder.md § Scripts) |
| update, audit, bring an older Board up to date | Board · Question Book · Project | § Update below |
| a dataset-first topic for one Task Board | Task-side | `haipipe-task` → `fn/insight.md` → `haipipe-page-insight` |
| an Insight Block with `j01_data` … `j04_wisdom` | older layout | [`ref/block-contract.md`](ref/block-contract.md); carry it with `ref/prototype_from_block.py` |
| a register board `*-InsightBoard` | older layout | [`ref/board-contract.md`](ref/board-contract.md) + `haipipe-insight-workflow` |
| unclear | — | stop and ask; never create a duplicate board |

The router never runs a whole Job because a topic was named, and never creates a Board because a dataset was named.


Update
------

```text
/haipipe-insight update <Board path>            audit, dry run, apply, rerun, verify
/haipipe-insight update <Board path> --check    audit and dry run only; nothing is written (an instruction to
                                                stop after ref/update.md step 2, not a script flag)
/haipipe-insight update <Project path>          every insight Board in it, each with its Question Book
```

Read [ref/update.md](ref/update.md) first and follow it. It brings an older insight folder onto this contract through
`scripts/insight_ladder.py audit <folder>` (read-only: one row per check, the step that fixes it), `update <folder>`
(a dry run), `update <folder> --apply`, and `--rerun` for the receipts:

```text
names     pN, vM, AP<N>, F<M>, work/Prototype-bNN-<T>/  ->  question-vN, data-vM, insight/InsightQuestionBook-<T>/  (rename_code_data.py)
words     cut, partition in a sentence a person reads   ->  segment; run-set-cuts -> run-set-segments              (rename_segment.py)
goals     each face's missing goal: line                                                                           (goals)
hash      each Job's hash: re-pinned to its release, whose files the rename changed
receipts  each hard Run made from an older question.md or scripts: rerun by its ticket with --rerun (needs env.sh),
          and said when its tables did not come out the same
```

It never rewrites the Board's own folder name, a data version's `folder:` or `extract:` (data outside the Board), a
register board's `*-InsightBoard` name, a `renamed-from:` line, a script's variables (a code file gets whole names
and its sentences only), a table (.csv), or a machine name a receipt hashes (`partitions.md`, the `partition:` /
`partitions:` / `cut:` keys, `partition_power.csv`). A register board or an Insight Block (one Job per level) is not
renamed: `audit` names its carry script (ref/carry_over.py, ref/prototype_from_block.py). Read the dry run before
`--apply`; apply in place only where git can undo it, else on a copy first; check the pages after.


Who owns what
-------------

```text
haipipe-insight                the door; the ladder contract and scaffold; open a version, set the segments, add a Job,
                               the hard Runs' runner (ref/run_job.py, ref/run_question.py), what a question delivers and how it is reviewed (ref/deliverables.py, ref/deliverables.md; scripts/insight_ladder.py review), the question map, carry-over;
                               the Executive level X, read as the Overall Report (ref/overall_report.py, figures ref/overall_figures.py)
haipipe-insight-question       proposals and their triage; asking a question into a version; Q1-Q7 with
                               haipipe-report
haipipe-insight-evidence-plan  one question's needs and work specs, planned before any run, agreed by another agent
haipipe-insight-meta           a dataset and its data versions (board.md versions:, meta/meta.md)
haipipe-insight-data · -information · -knowledge   what an answering page may say at its level; -knowledge also
                               compares Jobs, checks consistency, pools or splits on Cross
haipipe-insight-wisdom         the counsel and the Design handoff a person signs
haipipe-insight-check          readings across Jobs (coverage, tracks), each answer against its question, the status grid
haipipe-insight-workflow       run cards by level and Space, the gates, the next Run, dispatch (it is no card's skill)
workbench-insight              the insight theme on the shared workbench frame
haipipe-report · haipipe-draft-review   a Board question's report; another agent's CHECK of any page
haipipe-insight-bind           answers.yaml, for register boards only (no ladder Run binds)
haipipe-page-insight           the Task-side Insight Page and its RI Runs (its own route)
```


Runs
----

Every Run is `run-<type>-<target>/` (soft: `run.yaml`, its ticket, `passes/`) or `rNN_<segment>/` (hard: `run.sh`,
`run.yaml`, `result/`). The full list by level, with each owner, is ref/insight-ladder.md § Runs; in short:

```text
Question Book   triage-proposals · open-version · map · carry
a version   ask · review-questions · set-segments · sign-release (a person)
a question  plan-evidence · review-plan · write-script · review-script
Board       add-version · add (a Job) · propose-cut · propose · coverage · track · consistency ·
            ask · report · check (the Board's questions) · write-counsel · draft-handoff (a person) · close
a Job       launch · power · compare · propose · close (a person)
a Task      rNN_<segment> (hard) · write · check (another agent) · pool · check-alignment
```

`insight_ladder.py run <folder> <type> [<target>]` makes a Run's folder and card with its owner skill, agent and
sign; `insight_ladder.py run <Task> partition <name|all>` makes a hard Run's ticket (`partition` is the machine key; a person reads segment).


Laws
----

- **The question owns its code**, and the code exists once: in the release that holds the question. A Board Job
  reads it from there (`run_job.py`), never a copy. A question's id is never reused; it keeps its `tNN` everywhere.
- **Nothing generated is edited by hand**: a Run's `result/` (tables, figures, `runtime.yaml`, `report.md`), the
  question map and `meta/status.md` are their generators'. Change the source, rerun the ticket.
- **Another agent judges what an agent made**: questions, evidence plans, scripts and pages are reviewed or CHECKed
  in a fresh context, never by their maker.
- **A person signs** a release, the segments, a Job's close and a Wisdom handoff: `signed: ✅ <YYMMDD>`, never a name
  and never a machine. The door records a signature the person states; it never decides one.
- **Power before any contrast**: a segment whose rows cannot answer is refused with its minimum detectable effect, and
  a segment is never judged by whether its result is still significant; whether segments differ is a Cross question.
- **Counts and aggregates only**: no page, report or drawing reproduces a row.


Ends at a signed handoff
------------------------

A signed Design handoff is an insight decision, not a design: it names its finding, its strength and the Knowledge
results it rests on, its boundary, its pair (`question-vN × data-vM`), the design consequence and what it must not be read to
say, and never message copy. Design reads only a signed handoff, by its exact path. When a newer Job changes a
finding the handoff rests on, the handoff is stale and a new one is drafted; the old one stays. Shipping and
measuring belong downstream; what they return comes back as a new data version.

The register board's verbs, Run Specs, GI controls and standing authorization stay in `haipipe-insight-workflow`
(`ref/run-workflow.md`, `ref/authorization.md`) for the older boards until they are carried over.
