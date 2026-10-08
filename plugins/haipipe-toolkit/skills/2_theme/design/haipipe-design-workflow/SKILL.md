---
name: haipipe-design-workflow
description: >-
  The design ladder's Runs layer: which run-<type>-<target> Run comes next at the
  Block, the Job and each Task, who does it, who checks it and who signs, a
  design's state walk (draft → verify → revise → passed → kept | dropped →
  released), the run cards each Space's Runs panel shows, and the projections
  that carry a hard Run's Result into its level's files (a draft and a verdict
  into the design Task, t99's ranking into each prediction). Use to ask where a
  design Job stands or which Run may run next, check a gate, project a draft,
  verdict or ranking, close a Job, or read the run cards; setting up a Block or
  launching a Job is haipipe-design's. Trigger: where does the Job stand, next
  design Run, design gate, design state, project a draft, project predictions,
  close a design Job, run cards, /haipipe-design-workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-10-07"
---

# /haipipe-design-workflow · the design ladder's Runs

## Version governance

Only explicit user approval may authorize a version change. This skill keeps its current version, `0.4.0`; the move
onto the ladder (261007) is recorded in its CHANGELOG under it.

## What it owns

The ladder itself (folders, faces, names) is `haipipe-design/ref/design-ladder.md`. This skill owns how the Runs on
it follow each other:

- the Run Profile: the 22 Run types, their `run.yaml` card, hard and soft, naming ([references/run-profile.md](references/run-profile.md));
- the run cards: one per Run, the button, skill, agent, sign and prompt each Space's Runs panel shows
  ([references/run-cards.md](references/run-cards.md));
- the routes below, the gates on them, and a design's state;
- `run-close-j<NN>`, and the three projections that carry a closed hard Run's Result into its level's files
  (`scripts/project_draft.py draft | verdict`, `scripts/project_predictions.py`).

The work of each Run belongs to the skill its card names. A hard Run writes only its own `result/`; this skill
never writes a Result, and it is the only writer of a design Task's `state:`, `## Design` and `elements.yaml` after
the Task opens.

## Runs by level

```text
Block  set up      run-add-goal-<goal> (a person signs) · run-setup-rules (a person signs) · run-add-inputs-i<N>
       launch      run-add-job-j<NN>  (needs a signed goal, a registered method version, a frozen inputs version)
       report      run-add-observed-e<NN> · run-score-e<NN> · run-propose-questions · run-report-q<NN>
       also        run-propose-method-<slug> · run-draw-s<NN>
Job    set up      run-setup-goal-j<NN> · run-setup-method-j<NN> · run-setup-inputs-j<NN>   (set up = all three closed)
       open        run-open-designs-j<NN>
       release     run-freeze-predictions-j<NN> · run-release-j<NN> · run-close-j<NN>   (a person signs each)
Task   t00         run-reason-t00                                   hard · ②
       a design    run-generate-d<NN> · run-verify-d<NN>-v<k> · run-revise-d<NN>   hard · hard (another agent) · soft
       t99         run-rank-t99                                     hard (another agent) · ⑤
```

Every Block Run is soft (s11); the hard Runs sit in a Job's Tasks. A person signs a goal, the shared rules, the
frozen predictions with the release, and the close.

## Routes

```text
run-add-goal (signed) ─┐
run-setup-rules (signed)┤
run-add-inputs-i<N> ───┼─▶ run-add-job-j<NN>
registered method ─────┘        │
                                ▼
          run-setup-goal · run-setup-method · run-setup-inputs     all three closed = set up
                                │
                                ▼
          t00 run-reason-t00
                                │
                                ▼
          run-open-designs-j<NN>  pass 1: the reviewer's fence check (fence-check.md); on pass,
                                  one design Task per idea, then t99
                                │
                                ▼   per design, in parallel
          run-generate-d<NN> ─▶ project_draft.py draft ─▶ run-verify-d<NN>-v1 ─▶ project_draft.py verdict
                                                                │ pass ─▶ passed
                                                                │ fail
                                                                ▼
          run-revise-d<NN> (a new pass = draft k+1) ─▶ project_draft.py draft ─▶ run-verify-d<NN>-v<k+1> ─▶ verdict
                                │ every design passed, or dropped by a person
                                ▼
          t99 run-rank-t99 (another agent) ─▶ project_predictions.py: prediction.yaml (frozen: draft), kept | dropped
                                │
                                ▼
          run-freeze-predictions-j<NN> ─▶ run-release-j<NN> (a person signs) ─▶ run-close-j<NN>
                                │
                                ▼ later, once per Exp, at the Block
          run-add-observed-e<NN> ─▶ run-score-e<NN> ─▶ the method scorecard ─▶ run-propose-method-<slug>
```

A Route names the next permitted Run; it does not execute it. Several design Tasks run in parallel. ④ always runs T0
rules and T1 sources, and T2 critique when the pinned method version's ④ lists it. T3 pretest, when the method's ⑤
asks for it, runs once per Job on the kept designs, inside t99's rank Run.

**A fix that needs a new input is not a revise.** A revise may use only the Job's `inputs/`. When the review says the
design needs something the fence does not hold (a sender, a fact, a newer handoff), the design is dropped by a
person (`state: dropped`, its reason on the face), or the goal owner adds a new inputs version and a new Job reruns
it (`run-add-inputs-i<N+1>`, `run-add-job`, `moved: inputs`). The Job's fence never changes after `run-reason-t00`.

## Gates and who signs

| Gate | Before | Checked by | Signed by |
|---|---|---|---|
| goal signed | `run-add-job`, `run-setup-goal` | the goal line in `board.md ## Goals` carries `signed:`; aim, who, venue and n filled (only `leave-out` may stay `?`) | a person |
| rules signed | `run-add-job` | `design-goal.md` carries `rules: r<k>` and `signed:` | a person |
| set up | `run-reason-t00` | the three setup Runs closed; `inputs/method.md` there; `inputs/manifest.yaml` lists every file with its sha256 (first 12 hex) | none |
| fence | opening the design Tasks | `run-open-designs-j<NN>`'s first pass, `passes/pNN-<MMDD>/fence-check.md`, written by the reviewer agent, says pass: every reasoning step's `from` is a manifest file or `own knowledge` | none |
| independent review | `passed` | the verify's `by:` is set and differs from every generate and revise `by:` of the Task | none |
| ranked | `run-freeze-predictions` | `run-rank-t99` closed and projected (`project_predictions.py`) | none |
| release | `run-freeze-predictions` · `run-release` | every kept design `passed` before ranking, its prediction projected; frozen and released together | a person |
| close | `run-close` | every design Task terminal (released or dropped) | a person |

A gate that fails names what it waits on and who repairs it. Nothing is back-filled after the fact.

## A design's state

The face of each design Task carries `state:`. A hard Run never writes it: once that Run has closed, this skill's
projection reads its Result and moves the state.

```text
draft     the Task is open, no draft projected yet               run-open-designs (the scaffold)
verify    a draft waits for its review                           project_draft.py draft   (after generate or a revise pass)
revise    the last review failed                                 project_draft.py verdict (after a failed verify)
passed    the last review passed                                 project_draft.py verdict (after a passed verify)
kept      t99 kept it (top N)                                    project_predictions.py
dropped   t99 dropped it, or a person did; its Task stays, folded project_predictions.py · a person
released  a person released it                                   run-release (release.py)
```

`scripts/project_draft.py draft <task>` takes the newest draft (the closed `run-generate-d<NN>`'s
`result/design.md`, or the newest pass of `run-revise-d<NN>`, `passes/pNN-<MMDD>/design.md`, with its
`elements.yaml`) and writes it into the face's `## Design` and the Task's `elements.yaml`, then `state: verify`.
`scripts/project_draft.py verdict <task>` reads the newest closed verify's `status:` (`passed` or `failed`) and
writes `state: passed` or `revise`.

`scripts/project_predictions.py <job>` reads `t99_review-whole/runs/run-rank-t99/result/ranking.csv`
(`rank · design · predicted · why · kept`) and writes each design Task's `prediction.yaml` (`predicted · against ·
by · frozen: draft`) and its `state` (kept or dropped, only from `passed`). It never touches a prediction already
frozen, and prints what it changed.

## Where a Job stands

No script prints the next Run yet; read it level by level from the faces and the `run.yaml` cards:

1. **Block**: the goal's line in `board.md ## Goals` (`signed:`), `design-goal.md` (`rules:`, `signed:`), the inputs
   version's `manifest.yaml` (`frozen:`). Missing one: its Block Run is next (`run-add-goal`, `run-setup-rules`,
   `run-add-inputs`).
2. **Job setup**: `runs/run-setup-goal|method|inputs-j<NN>/run.yaml` `status:`; the first not `closed` is next.
3. **t00**: `t00_reason-ideas/runs/run-reason-t00/run.yaml`; then `run-open-designs-j<NN>` and its
   `fence-check.md` pass.
4. **Each design**: the face's `state:` names the next Run: `draft` → `run-generate-d<NN>`; `verify` →
   `run-verify-d<NN>-v<k>` for the newest draft k; `revise` → a new pass of `run-revise-d<NN>`; `passed` → wait
   for t99.
5. **t99**: every design `passed` or `dropped` → `run-rank-t99`; closed → `project_predictions.py`.
6. **Release**: every kept design with a projected prediction → `run-freeze-predictions` and `run-release`, then
   `run-close` once every Task is released or dropped.

A Run whose card says `open` or `running` is the one in flight; finish it before starting the next on that target.

## Stop rules

- One open Run per target: a second Run on a target whose Run is still open is refused. A verify is named by the
  draft it reads (`-v<k>`, k = 1 + the revise passes), so asking again for the same draft finds the same Run.
- A verify never reruns on an unchanged draft; a new draft is a new pass of `run-revise` and a new verify `-v<k+1>`.
- A hard Run's `result/` is closed once its card says `closed`, `passed` or `failed`; new inputs are a new Run.
- A Job is never edited after `run-release`: a changed method or inputs version is a new Job (`run-add-job`).
- Stop at `run-close-j<NN>`. Sending, the experiment and its measurement belong downstream; what comes back lands
  once at the Block (`run-add-observed`).

Report each actual Run with its type, target, kind, who did it, status, the gate it passed and the route taken.
Planned Runs are not inventory.

## Older board

An older board (`2-Design[-M<NN>]/Design-NN-<slug>/`, Design Items, Commission → Generate → Verify,
`run-design-<step>-<MMDD>-<slug>`) keeps its workflow in
[references/legacy/older-board.md](references/legacy/older-board.md) and its Run Profile in
[references/legacy/run-profile-older.md](references/legacy/run-profile-older.md); its cards stay at the end of
`references/run-cards.md`, where the older page's workbench reads them. New work never writes it.
