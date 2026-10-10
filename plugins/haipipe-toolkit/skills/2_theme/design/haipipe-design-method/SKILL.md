---
name: haipipe-design-method
description: >-
  The design method registry: what a design method is (a recipe, frozen per
  version, that turns a goal and its inputs into N designs in five steps: ① See
  input · ② Reason ideas · ③ Conduct process · ④ Review item · ⑤ Review whole),
  the registered methods MNN and their versions m<k> (methods/), each typed by one
  of the Guide's 13 cards, and how a method evolves: proposals, the next
  version, and the scorecard summed from what each Exp returned. Owns
  run-setup-method-j<NN> (pin a version into a Job), run-propose-method-<slug>,
  run-add-observed-e<NN> and run-score-e<NN>. Use to list or pin a method, cut
  or propose a version, add an Exp's per-arm totals, score the predictions, or
  read the method scorecard. Trigger: design method, method version, registered
  method, pin a method, propose a method, method scorecard, add observed, score
  the Exp, /haipipe-design-method.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
metadata:
  version: "0.4.1"
  last_updated: "2026-10-09"
  # version history: ./CHANGELOG.md
---

# /haipipe-design-method · the method registry

Version governance: this skill starts at `0.4.0` and keeps it; only explicit user approval may authorize a version
change.

"For the design, the key thing is what is the design method" (JL 261007, b12 s00). A **design method** is a recipe,
frozen per version, that turns a goal and its inputs into N designs. On the ladder
(`haipipe-design/ref/design-ladder.md`) a Job pins one method version and never writes its own; this skill keeps the
methods, cuts their versions, and learns which version works from what each Exp returns.


Three layers
------------

```text
a card       the Guide's 13 types (servers/workbench-design/guide/methods/): By goal, By insight, By precedent …
             the move, the literature, the tests; generic, never pinned
a method     MNN-<slug>/method.md here: one way of designing, typed by one card (M04 Actionable insights: By insight)
a version    MNN-<slug>/m<k>.md: the method made concrete, its choice at each of the five steps; frozen; what a Job pins
```

The five steps, each version's choice at each (the design unit, b12 s03):

```text
① See input          what the design work may see: the parts of step ① it reads (sees:), the rest is fenced out
② Reason ideas       how ideas are made: how many, how spread, from which sources          t00 · run-reason-t00
③ Conduct process    how one idea becomes one design                                       tNN · run-generate-d<NN>
④ Review item        which checks each design passes: T0 rules · T1 sources (always),       tNN · run-verify-d<NN>-v<k>
                     T2 critique when the version lists it
⑤ Review whole       how the ideas are ranked, how many kept, the predicted effect,        t99 · run-rank-t99
                     and whether T3 pretest runs on the kept
```

T3 (a pretest with readers) runs once per Job on the kept designs, inside t99's rank Run, when the version's ⑤ says
so; T4, the Exp, is not part of the method: it is the learning loop below. ② makes N + 5 ideas unless the version's
② names another count (`haipipe-design-unit/references/reason.md`).


The registry
------------

```text
methods/
├── README.md
├── M01-goal-only/            method.md (name · type · family · card · versions · current) · m1.md
├── M02-overall-performance/  m1.md
├── M03-detailed-evidence/    m1.md
├── M04-actionable-insights/  m1.md · m2.md
└── M05-raw-data-agent/       m1.md
```

A version file is what `run-setup-method-j<NN>` copies into the Job's `inputs/method.md`, word for word:

```yaml
---
method: M04
version: m2
steps: {① See input: …, ② Reason ideas: …, ③ Conduct process: …, ④ Review item: …, ⑤ Review whole: …}
sees: [Goal · how much is set, Information · whose]      # the parts of step ① it reads (haipipe-design-goal ref/inputs.md)
runs-it: designer agent ①②③ · a reviewer agent ④⑤
loops: one pass                                          # or: rounds, each a Run on t00 and t99
---
```

1. **A version is frozen.** Once a Job pins it, its file never changes; a change is `m<k+1>`. `pin_method.py` writes
   the version's sha (first 12 hex of sha256) into the Job face's `method-sha:` and refuses a Job already pinned to
   another text.
2. **One clock per Job.** A Job on a new version is a new Job (`moved: method`), on the same goal and inputs as the
   one before it, so a change in the designs has one cause. Comparing two methods is two Jobs in one Map row.
3. **Generic only.** A method names parts of step ① and kinds of source, never an application, a project, a vendor
   or a person; the Block's own material is in its inputs versions.
4. **No 13 skills.** The unit (`haipipe-design-unit`) reads the pinned version; a new method is a new folder here,
   not a new skill.


How a method evolves
--------------------

```text
a trigger ─▶ run-propose-method-<slug> (a Block) ─▶ the next version m<k+1> written here ─▶ benched against m<k>
          ─▶ reviewed by another agent ─▶ signed by a person ─▶ a new Job pins it (moved: method)
```

The triggers (s00): the checks fail often (④ T0 or T1); the N designs are alike (⑤ coverage); the critique or a
pretest finds a pattern (T2, T3); the Exp says the version loses (the scorecard); a paper suggests a procedure; a new
kind of input appears. New inputs alone need no new version: they are a new inputs version. A proposal is written
into the Block's `runs/run-propose-method-<slug>/` and names the trigger, the step it changes and the evidence; the
registry cuts the version only when a person signs.


The learning loop: observed, scores, scorecard
----------------------------------------------

What an Exp returns lands once, at the Block, never per Job (s11):

1. **`run-add-observed-e<NN>`** writes `observed/eNN_<exp>/`: `arms.csv` (arm · job · design · n · observed; per-arm
   totals only, never rows), `source.md` (the insight Block's signed handoff or a vendor's per-arm report it came
   from) and a frozen `manifest.yaml`. Raw Exp rows stay in their store.
2. **`run-score-e<NN>`** scores every arm's design against the prediction frozen at its release (`prediction.yaml`):
   `scripts/score_exp.py <block> eNN` writes `runs/run-score-eNN/scores.csv` (job · design · predicted · observed ·
   direction · in_range · error) in its own Run folder and prints the scorecard. The reviewer agent runs it.
3. **The scorecard** sums the scores per method version: designs scored, right direction, in the predicted range.
   A Job's Predicted vs observed reads its own rows; the Block's Method scorecard reads the sums. The contract:
   [ref/scorecard.md](ref/scorecard.md).


The Runs
--------

| Run | Level | Writes | Who | Signs |
|---|---|---|---|---|
| `run-setup-method-j<NN>` | Job | `inputs/method.md`, the face's `method-sha:` | designer agent | none |
| `run-propose-method-<slug>` | Block | a proposal in its Run; the next version when signed | designer agent | a person |
| `run-add-observed-e<NN>` | Block | `observed/eNN_<exp>/` | designer agent | none |
| `run-score-e<NN>` | Block | `runs/run-score-eNN/scores.csv` | reviewer agent | none |

All four are soft (`haipipe-run`: `run-<type>-<target>/run.yaml`, `passes/`).

```bash
python scripts/pin_method.py --list
python scripts/pin_method.py design/Design-<name>/j03_g01_m04          # run-setup-method-j03
python scripts/score_exp.py design/Design-<name> e01                    # run-score-e01
```


Boundary
--------

This skill keeps the registry and scores the Exp's per-arm totals. It does not build a Job's fence
(`haipipe-design-goal`), run a method's steps (`haipipe-design-unit`), freeze predictions or release
(`haipipe-design-delivery`), or run, allocate or measure the Exp (outside the theme). The Guide's 13 cards stay in
`servers/workbench-design/guide/methods/`, where the workbench's Guide reads them.
