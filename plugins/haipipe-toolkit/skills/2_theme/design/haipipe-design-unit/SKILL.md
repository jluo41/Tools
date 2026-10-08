---
name: haipipe-design-unit
description: >-
  One step of a design method on one target, as one Run on the design ladder:
  reason ② (hard, t00: the ideas and their reasoning chains), generate ③ (hard:
  one design and its element record), revise (soft: a pass of the design's
  revise Run, generate with a frozen base and feedback), verify ④ (hard, another
  agent: T0 rules, T1 sources, T2 critique when the method lists it), and rank
  ⑤ (hard, another agent: rank, keep N, a predicted effect per design; T3 pretest
  on the kept when the method asks). Reads only the Job's inputs/ fence (and, to
  verify or rank, the target Results); writes only its Run's result/ (a revise:
  its pass). Use for run-reason-t00, run-generate-d<NN>, run-verify-d<NN>-v<k>,
  run-revise-d<NN>, run-rank-t99; not for opening Jobs or Tasks, projecting,
  releasing, sending, or measuring. Trigger: reason design ideas, generate a
  design, revise a design, verify a design, rank the designs, /haipipe-design-unit.
metadata:
  version: "0.4.1"
  last_updated: "2026-10-07"
---

# /haipipe-design-unit · one step of a method, one Run, one Result

## Version governance

This Design skill stays at `0.4.1`. Only explicit user approval may authorize a version change; the move onto the
ladder (261007) is recorded in the CHANGELOG and does not by itself authorize one.

This is a worker, like a display renderer, not a folder owner. The caller (`haipipe-design-workflow`, through
`haipipe-design`'s scaffold) allocates the Run, writes its `run.yaml`, sets up the Job's `inputs/`, opens the Tasks,
projects each closed Result into its Task (`project_draft.py draft | verdict`, `project_predictions.py`) and
releases. This worker does one step, writes `by:` on its card, and returns its Result.

Read [references/unit-contract.md](references/unit-contract.md) § Ladder on every invocation, then the reference for
the operation: [reason.md](references/reason.md) for ②, [rank.md](references/rank.md) for ⑤; generate, revise and
verify are below. The contract of the ladder is `../haipipe-design/ref/design-ladder.md`.

## The Ticket on the ladder

There is no separate Ticket file. A Run's ticket is three things the caller froze before dispatch:

```text
<Task>/runs/run-<type>-<target>/run.yaml   the Run: type · kind: hard · target · status · by
<Job>/<Job>.md                             the pins: goal · method (M04 m2) · method-sha · inputs (i2) · n
<Job>/inputs/                              the fence: goal.md · method.md · links · manifest.yaml
```

The worker reads `inputs/method.md` for the pinned version's choice at its step (② how to spread ideas, ③ how to
conduct, ④ which tests, ⑤ how to rank and how many to keep) and follows it; it never reads the method registry, the
Block's other files, another Job, or the web. Missing, stale or contradictory inputs (a manifest file changed since
its sha, a link that does not resolve, a step the method does not define) return a named hold: say what is wrong,
write no Result, and the caller puts the Run back.

**The fence.** Every reasoning step and every element names its `from`: a file in the manifest (by its path, its
name, or an id inside its name, with an optional locator: `handoff-W-03.md · row 2`, `W-03 row 2`, `rules.md`,
`rule r2.1`), or exactly the words `own knowledge`. Free prose that only shares a word with a file name (`my hunch
about the goal`) is not a source. A reasoning step may name its own `from`, which overrides its topic's. `own
knowledge` is allowed and visible; it is never dressed as a source.

## ② reason · `run-reason-t00` (designer agent)

In `t00_reason-ideas/`. Reads the fence; writes `result/chains.yaml` (the topics and their reasoning chains),
`result/ideas.yaml` (N + 5 ideas unless the method version's ② says otherwise, N the face's `n`; each with its
`name` and the design it will become) and `result/topics.md` (the readable report). It writes ideas only: the Job's `run-open-designs-jNN` opens the design Tasks after the
reviewer has checked the fence. Details and shapes: [references/reason.md](references/reason.md).

## ③ generate · `run-generate-d<NN>` (designer agent)

In the design's Task `tNN_d<NN>_<slug>/`. Reads the fence and its idea (t00's `ideas.yaml` row, whose `design` is
this Task's `d<NN>`). Writes:

```text
result/design.md        the design as the reader sees it, word for word (an SMS's text, a UI's screen.html)
result/elements.yaml    one entry per element: element · words · from · because · step: ③ · changed
```

and returns them; once the Run has closed, `haipipe-design-workflow`'s `project_draft.py draft` carries the words
into the face's `## Design` and the element record into the Task's `elements.yaml` (a hard Run writes only its own
`result/`). Use the element names the goal or the method lists; name any
other by its role. A hunch is `from: own knowledge`, never a made-up source. Check the actual text against the
goal's rules (length, the venue's required words, `{LINK}` and `{NAME}` slots not counted) before returning; the
self-check is never the review. A UI design is one self-contained `screen.html` with no script, rendered with
`scripts/render_screen.py` into the Result before any visual claim.

**revise · `run-revise-d<NN>`** (soft, a pass per new draft). Generate with a frozen base (the last draft) and the
failed review's findings as feedback; change only what the feedback names, keep the short name, and write the new
draft into the pass: `passes/pNN-<MMDD>/design.md`, `elements.yaml` (changed entries `changed: draft <k>`) and
`feedback.md`. Draft k = 1 + the number of revise passes; the next verify reads it: `run-verify-d<NN>-v<k>`. A new
idea is a new Task, never a revise. A fix that needs an input the fence lacks is not a revise either: hold, and
name the input (a new inputs version and a new Job, or the design dropped).

## ④ verify · `run-verify-d<NN>-v<k>` (reviewer agent, another context)

Reads draft k (the generate Result for k = 1, else the revise Run's (k-1)th pass), with its `elements.yaml`, and the
fence. Runs T0 and T1 always, and T2 when the pinned method version's ④ lists it, each a separate verdict with its
observed evidence:

```text
T0  rules        every goal and venue rule, on the text itself              pass · fail (rule id)
T1  sources      every element's from is in the manifest or own knowledge   pass · fail (element)
T2  critique     the design read cold as its reader: one clear ask, no      pass · fail (finding)
                 contradiction with the goal (when the method's ④ lists it)
```

T3 pretest is not a verify test: it runs once per Job on the kept designs, inside t99's rank Run, when the method's
⑤ asks for it.

Writes `result/review.md` (each test, its verdict, the evidence, what to change) and sets on its card `status:
passed` (every test run passes) or `failed`, `tests: {T0: ✓, T1: ✗ <element>, …}` and its own `by:`. A failed verify
routes to a revise; a review that cannot decide (a rule that cannot be read on the text) names the gap and its next
owner and is not a pass. Independence is real: a verify by the agent or context that generated is refused.

## ⑤ rank · `run-rank-t99` (reviewer agent, another context)

In `t99_review-whole/`. Reads every passed design of the Job, the face's `n` and the fence. Ranks them by the
method's rule, keeps N (no two alike; together they cover the goal; every input used where it should be), gives
each design a predicted effect against the control, and runs T3 pretest on the kept when the method's ⑤ asks. Writes only `result/ranking.csv` (`rank,design,predicted,why,
kept`) and `result/coverage.md`. The workflow then projects each row into the design's Task (`prediction.yaml`,
`frozen: draft`; `state: kept | dropped`); a person's release freezes it. Details: [references/rank.md](references/rank.md).

## Checks

```bash
python3 scripts/check_unit.py --ladder-result <Task>/runs/run-<type>-<target>
```

validates the Result's shape for its type (reason · generate · revise · verify · rank), that a hard Run wrote its
`result/`, that every `from` is inside the fence (strictly: a fence path, name or stem, `<stem-word> <id>` such as
`rule r2.1`, an id inside a fence file's name such as `W-03 row 2`, or exactly `own knowledge`), that every idea has
a `name`, that a verify's `by` is set and differs from the generator's, and that a ranking keeps the face's N. Structural validation is not a semantic endorsement; quote it, then judge.

## Boundaries

- Writes only its Run's `result/` (a revise: its pass) and `by:` · `status:` · `tests:` on its own card. Never a
  face, `elements.yaml`, `prediction.yaml`, another Run, the fence, the Job, the Block or a delivery file:
  `haipipe-design-workflow` projects those.
- Never opens Tasks, releases, sends, allocates traffic or measures an effect. A predicted effect is a forecast,
  never an observed finding.
- Placeholders only in this skill; the design's own words come from the fence and the method.

## Older boards

An older Design Folder board (Design Items, a Commission-pinned v2 Ticket, `run-design-<generate|verify>-<MMDD>-
<slug>`) keeps its procedure in [references/legacy/older-boards.md](references/legacy/older-boards.md) and its
contract in `references/unit-contract.md` § Older boards; `python3 scripts/check_unit.py --ticket <ticket> [--result
<result.yaml>]` and `--folder <Design Folder>` still check it. `scripts/rename_runs.py` renames its retired `rdNN_*`
Run names once.
