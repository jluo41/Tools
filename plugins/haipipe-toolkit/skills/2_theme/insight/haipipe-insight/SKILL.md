---
name: haipipe-insight
description: >-
  The one door for insight on the ladder: two special boards that work together.
  The Prototype (tasks/Prototype-bNN-<Topic>/) holds the questions and their
  scripts, one Job per release, signed and frozen; the insight Board
  (insights/Insight-<name>/) holds one dataset and its dated versions, one Job
  per release × data version, a Task per question, a hard Run per cut. Owns the
  ladder contract and its scaffold (insight_ladder.py), routes each level's Runs
  to the question, evidence-plan, meta, level, check, wisdom and workflow
  owners, and ends at a person-signed Design handoff, never a design. Also routes
  a dataset-first topic to the Task-side Insight Page, and reads the older
  Insight Block and register boards until they are carried over. Trigger:
  insight, Prototype, release, insight Board, data version, DIKW, question,
  partition, cut, compare Jobs, coverage, pooling verdict, Design handoff,
  /haipipe-insight.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-10-08"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight · the Prototype and the insight Board

Insight asks what a dataset can and cannot say, level by level (D what it holds · I rates and contrasts inside a
cut · K what survives tests across cuts · W the counsel a person signs for Design), and keeps the questions apart
from the data they run on. Read [`ref/insight-ladder.md`](ref/insight-ladder.md) before creating, naming, growing
or auditing any insight folder: it is the contract, and `scripts/insight_ladder.py` keeps its gates. A release, from
its proposals to its signature, is [`ref/release.md`](ref/release.md).

```text
Prototype   tasks/Prototype-bNN-<Topic>/      the questions + their scripts; a Job per release jNN_pN_<slug>/,
                                              frozen once a person signs it; proposals/ is its backlog
Board       insights/Insight-<name>/          one dataset, its dated versions (board.md versions:); a Job per
                                              release × data version jNN_pN_<D>vM/, a Task per question,
                                              a hard Run per cut runs/rNN_<partition>/
```

**How they work together.** A Board Job runs one signed release on one frozen data version and moves one clock from
the Job before it (`moved: start | data | code`). What a Job finds feeds back only as proposals in the Prototype's
`proposals/`; a triaged batch becomes the next release; the Board then adds a Job for it. New data needs no
release, a new release needs no new data, and a change in an answer has one cause.


Route
-----

Resolve the folder first, by its `board.md` (never its folder name), then load one owner:

| What the request names | Level | First owner |
|---|---|---|
| a Prototype (`board-kind: prototype`) | proposals · a version · a question | this door → the version's Run owner (§ Runs) |
| an insight Board (`board-kind: insight-board`, or `prototype:` in board.md) | data versions · Jobs · readings | this door → the Board's Run owner |
| a Board Job `jNN_pN_<D>vM/` or its Task `tNN_<L><NN>_<slug>/` | hard Runs · pages · compare | this door → `haipipe-insight-workflow` |
| a new topic | — | `insight_ladder.py prototype`, then `board` (ref/insight-ladder.md § Scripts) |
| a dataset-first topic for one Task Board | Task-side | `haipipe-task` → `fn/insight.md` → `haipipe-page-insight` |
| an Insight Block with `j01_data` … `j04_wisdom` | older layout | [`ref/block-contract.md`](ref/block-contract.md); carry it with `ref/prototype_from_block.py` |
| a register board `*-InsightBoard` | older layout | [`ref/board-contract.md`](ref/board-contract.md) + `haipipe-insight-workflow` |
| unclear | — | stop and ask; never create a duplicate board |

The router never runs a whole Job because a topic was named, and never creates a Board because a dataset was named.


Who owns what
-------------

```text
haipipe-insight                the door; the ladder contract and scaffold; open a version, set the cuts, add a Job,
                               the hard Runs' runner (ref/run_job.py, ref/run_question.py), the question map, carry-over
haipipe-insight-question       proposals and their triage; asking a question into a version; Q1-Q7 with
                               haipipe-question-review
haipipe-insight-evidence-plan  one question's needs and work specs, planned before any run, agreed by another agent
haipipe-insight-meta           a dataset and its data versions (board.md versions:, meta/meta.md)
haipipe-insight-data · -information · -knowledge   what an answering page may say at its level; -knowledge also
                               compares Jobs, checks consistency, pools or splits on Cross
haipipe-insight-wisdom         the counsel and the Design handoff a person signs
haipipe-insight-check          readings across Jobs (coverage, tracks), each answer against its question, the status grid
haipipe-insight-workflow       run cards by level and Space, signing a release, launching and closing a Job, dispatch
workbench-insight              the insight theme on the shared workbench frame
haipipe-report · haipipe-page-check   a Board question's report; another agent's CHECK of any page
haipipe-insight-bind           answers.yaml, for register boards only (no ladder Run binds)
haipipe-page-insight           the Task-side Insight Page and its RI Runs (its own route)
```


Runs
----

Every Run is `run-<type>-<target>/` (soft: `run.yaml`, its ticket, `passes/`) or `rNN_<partition>/` (hard: `run.sh`,
`run.yaml`, `result/`). The full list by level, with each owner, is ref/insight-ladder.md § Runs; in short:

```text
Prototype   triage-proposals · open-version · map · carry
a version   ask · review-questions · set-cuts · sign-release (a person)
a question  plan-evidence · review-plan · write-script · review-script
Board       add-version · add (a Job) · propose-cut · propose · coverage · track · consistency ·
            ask · report · check (the Board's questions) · write-counsel · draft-handoff (a person) · close
a Job       launch · power · compare · propose · close (a person)
a Task      rNN_<partition> (hard) · write · check (another agent) · pool · check-alignment
```

`insight_ladder.py run <folder> <type> [<target>]` makes a Run's folder and card with its owner skill, agent and
sign; `insight_ladder.py run <Task> partition <name|all>` makes a hard Run's ticket.


Laws
----

- **The question owns its code**, and the code exists once: in the release that holds the question. A Board Job
  reads it from there (`run_job.py`), never a copy. A question's id is never reused; it keeps its `tNN` everywhere.
- **Nothing generated is edited by hand**: a Run's `result/` (tables, figures, `runtime.yaml`, `report.md`), the
  question map and `meta/status.md` are their generators'. Change the source, rerun the ticket.
- **Another agent judges what an agent made**: questions, evidence plans, scripts and pages are reviewed or CHECKed
  in a fresh context, never by their maker.
- **A person signs** a release, the cuts, a Job's close and a Wisdom handoff: `signed: ✅ <YYMMDD>`, never a name
  and never a machine. The door records a signature the person states; it never decides one.
- **Power before any contrast**: a cut whose rows cannot answer is refused with its minimum detectable effect, and
  a partition is never judged by whether its result is still significant; whether cuts differ is a Cross question.
- **Counts and aggregates only**: no page, report or drawing reproduces a row.


Ends at a signed handoff
------------------------

A signed Design handoff is an insight decision, not a design: it names its finding, its strength and the Knowledge
results it rests on, its boundary, its pair (`pN × vM`), the design consequence and what it must not be read to
say, and never message copy. Design reads only a signed handoff, by its exact path. When a newer Job changes a
finding the handoff rests on, the handoff is stale and a new one is drafted; the old one stays. Shipping and
measuring belong downstream; what they return comes back as a new data version.

The register board's verbs, Run Specs, GI controls and standing authorization stay in `haipipe-insight-workflow`
(`ref/run-workflow.md`, `ref/authorization.md`) for the older boards until they are carried over.
