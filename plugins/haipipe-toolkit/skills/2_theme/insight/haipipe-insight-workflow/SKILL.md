---
name: haipipe-insight-workflow
description: >-
  Where an insight folder stands and which Run is next, on the insight ladder:
  the Prototype (its releases and questions) and the insight Board (its data
  versions, Jobs and Tasks). Owns the run cards (one card per workbench button:
  its Run, skill, agent, sign and prompt), the gates between levels (agreed
  questions, set cuts, a signed release, a frozen data version, one clock per
  Job, power before contrast, a checked page, a signed close and handoff), and
  routing each Run to the skill that does it. Use to ask what is next for a
  Prototype, release, Board, Job or Task, to find who owns a button, to check the
  cards, or to run the older register boards' workflow until they are carried
  over. Trigger: what next, next Run, run card, gate, insight workflow, where
  does this Job stand, who owns this button, /haipipe-insight-workflow.
metadata:
  version: "3.0.0"
  last_updated: "2026-10-08"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight-workflow · the run cards, the gates, and what is next

Load `haipipe-insight` (the ladder contract, `ref/insight-ladder.md`) and `haipipe-run` (the Run contract). This
skill routes; it never does a Run's work. Each Run is done by the one skill its card names, by the agent its card
names, and signed where its card says a person signs.

```text
ref/run-cards.md          one card per workbench button: label · <Level> › <Space> · ^pattern · views, then
                          🧩 SKILL · 🤖 AGENT · ✍️ SIGNS · 💬 PROMPT; the gates at the end
scripts/run_cards.py      the cards' one reader; --check: every card whole, its skill and agent real, its pattern
                          naming its own Run, and every run type of insight_ladder.py carded with the same skill
scripts/next_run.py       <folder>: where it stands and which Run is next, read from its files, never written
ref/register-board-workflow.md   the older register boards' workflow (GI0-GI6, Question Groups), word for word
```

The workbench reads the cards (`servers/workbench-insight`), and the Insight Workbench Table is generated from them
(`workbench-insight/scripts/cards_table.py`). Change a card, then rerun the table and `run_cards.py --check`.


What is next
------------

`python scripts/next_run.py <folder>` walks the gates in order and names the first Run that is owed:

```text
release   a question with no plan → run-plan-evidence · not agreed → run-review-plan · a compute need with no
          script → run-write-script · cuts not set → run-set-cuts · all set → run-sign-release (a person)
Prototype no release → run-open-version-p1 · the newest signed and proposals open → triage, then the next release
Board     no data version → run-add-version-v1 · no Job → run-add-j01 · the newest Job closed and a new data
          version or a new signed release waiting → run-add-j<NN> (one clock) · else the readings
Job       not launched → run-launch · a cut not run → its run.sh · a page not written → run-write · not checked →
          run-check · all checked and a Job before it → run-compare · then run-close (a person)
Task      the same, for one question
```

It never runs or writes anything. A person or an agent presses the button the card names; a refusal (a cut too
thin to answer) counts as done.


The gates
---------

The full table is `ref/run-cards.md § Gates`; the scaffold (`haipipe-insight/scripts/insight_ladder.py`) refuses to
pass them. In short: a question's needs are agreed by another agent and its script reviewed by another agent; the
cuts are set before any outcome and signed; a release is signed by a person and then frozen; a data version is
frozen when added; a Job pairs a signed release with a frozen data version, a new pair, one clock moved; power is
checked before any contrast; a page is CHECKed by another agent; a Job is closed by a person once every page is
checked and it is compared with the Job before it; a handoff is signed by a person before Design reads it.

A gate is declared passed only by the review, CHECK or signature it names, never by a timer or a loop, and never by
the agent that made the thing. `signed: ✅ <YYMMDD>` is a person's, recorded when the person states it.


Who does a Run
--------------

```text
makes       haipipe-insight-agent              asks, plans, writes pages and counsel, adds versions and Jobs
judges      haipipe-insight-reviewer-agent      reviews questions and plans, checks alignment and consistency
            haipipe-page-check-agent            CHECKs a page or a Board report
            haipipe-task-reviewer-agent         reviews a script
runs        haipipe-task-orchestrator-agent     launches a Job, runs a hard Run's ticket
writes code haipipe-task-creator-agent          writes a question's script
signs       a person                            the cuts, a release, a Job's close, a handoff
```

A judging Run is never done by the agent that made what it judges, on that level.


Older boards
------------

A register board (`*-InsightBoard`, MT00-MT04) keeps its own workflow until it is carried into a release:
[`ref/register-board-workflow.md`](ref/register-board-workflow.md), with `ref/run-workflow.md`,
`ref/partition-policy.md`, `ref/authorization.md`, `ref/handoff-record.md`, `ref/task-rf-bridge.md` and
`ref/migration.md` as before. An Insight Block with one Job per DIKW level is carried with
`haipipe-insight/ref/prototype_from_block.py`.


Return
------

For a status ask: the folder, its state line and the next Run with its card (skill, agent, sign). For a Run: the
Run's folder, its card, what it wrote, and the next Run. Name every person's decision still owed.
