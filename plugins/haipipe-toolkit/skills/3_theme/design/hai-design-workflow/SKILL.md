---
name: hai-design-workflow
description: "The design ladder's Runs layer: which Run comes next at the Block, Job and Task, who does, checks and signs it, a design's state walk, and the run cards. Use to ask where a design Job stands or to close it. Trigger: next design Run, design gate, design state, run cards, /hai-design-workflow."
metadata:
  version: "0.4.1"
  last_updated: "2026-11-27"
---

# /hai-design-workflow · the design ladder's Runs

## Version governance

Keep the version declared in metadata. Change it only with explicit user approval.

## What it owns

The ladder itself (folders, faces, names) is `hai-design/ref/design-ladder.md`. This skill owns how the Runs on
it follow each other:

- the Run Profile: the 22 Run types, their `run.yaml` card, hard and soft, naming ([references/run-profile.md](references/run-profile.md));
- the run cards: one per Run, the button, skill, agent, sign and prompt the Runs controls show
  ([references/run-cards.md](references/run-cards.md));
- the routes below, the gates on them, and a design's state;
- `run-close-j〈NN〉`, and the three projections that carry a closed hard Run's Result into its level's files
  (`scripts/project_draft.py draft | verdict`, `scripts/project_predictions.py`).

The work of each Run belongs to the skill its card names. A hard Run writes only its own `result/`; this skill
never writes a Result. It projects draft, review and ranking outcomes into a Task's `state:`, `## Design` and
`elements.yaml`. Delivery writes `released`; a person may mark a design `dropped` with a reason.

## Runs by level

```text
Block  set up      run-add-goal-〈goal〉 (a person signs) · run-setup-rules (a person signs) · run-add-inputs-v〈N〉
       launch      run-add-job-j〈NN〉  (needs a signed goal, a registered method version, a frozen inputs version)
       report      run-add-observed-e〈NN〉 · run-score-e〈NN〉 · run-propose-questions · run-report-q〈NN〉
       also        run-propose-method-〈slug〉 · run-draw-s〈NN〉
Job    set up      run-setup-goal-j〈NN〉 · run-setup-method-j〈NN〉 · run-setup-inputs-j〈NN〉   (set up = all three closed)
       open        run-open-designs-j〈NN〉
       release     run-freeze-predictions-j〈NN〉 · run-release-j〈NN〉 · run-close-j〈NN〉   (a person signs the first two once, then the close)
Task   t00         run-reason-t00                                   hard · ②
       a design    run-generate-d〈NN〉 · run-verify-d〈NN〉-v〈k〉 · run-revise-d〈NN〉   hard · hard (another agent) · soft
       t99         run-rank-t99                                     hard (another agent) · ⑤
```

Every Block Run is soft; the hard Runs sit in a Job's Tasks. A person signs a goal, the shared rules, the
frozen predictions with the release, and the close.

## Routes

```text
run-add-goal (signed) ─┐
run-setup-rules (signed)┤
run-add-inputs-v〈N〉 ───┼─▶ run-add-job-j〈NN〉
registered method ─────┘        │
                                ▼
          run-setup-goal · run-setup-method · run-setup-inputs     all three closed = set up
                                │
                                ▼
          t00 run-reason-t00
                                │
                                ▼
          run-open-designs-j〈NN〉  pass 1: the reviewer's fence check (fence-check.md); on pass,
                                  one design Task per idea, then t99
                                │
                                ▼   per design, in parallel
          run-generate-d〈NN〉 ─▶ project_draft.py draft ─▶ run-verify-d〈NN〉-v1 ─▶ project_draft.py verdict
                                                                │ pass ─▶ passed
                                                                │ fail
                                                                ▼
          run-revise-d〈NN〉 (a new pass = draft k+1) ─▶ project_draft.py draft ─▶ run-verify-d〈NN〉-v〈k+1〉 ─▶ verdict
                                │ every design passed, or dropped by a person
                                ▼
          t99 run-rank-t99 (another agent) ─▶ project_predictions.py: prediction.yaml (frozen: draft), kept | dropped
                                │
                                ▼
          run-freeze-predictions-j〈NN〉 ─▶ run-release-j〈NN〉 (a person signs) ─▶ run-close-j〈NN〉
                                │
                                ▼ later, once per Exp, at the Block
          run-add-observed-e〈NN〉 ─▶ run-score-e〈NN〉 ─▶ the method scorecard ─▶ run-propose-method-〈slug〉
```

A Route names the next permitted Run; it does not execute it. Several design Tasks run in parallel. ④ always runs T0
rules and T1 sources, and T2 critique when the pinned method version's ④ lists it. T3 pretest, when the method's ⑤
asks for it, runs once per Job on the kept designs, inside t99's rank Run.

**A fix that needs a new input is not a revise.** A revise may use only the Job's `inputs/`. When the review says the
design needs something the fence does not hold (a sender, a fact, a newer handoff), the design is dropped by a
person (`state: dropped`, its reason on the face), or the goal owner adds a new inputs version and a new Job reruns
it (`run-add-inputs-v〈N+1〉`, `run-add-job`, `moved: inputs`). The Job's fence never changes after `run-reason-t00`.

## Gates and who signs

| Gate | Before | Checked by | Signed by |
|---|---|---|---|
| goal signed | `run-add-job`, `run-setup-goal` | the goal line in `board.md ## Goals` carries `signed:`; aim, who, venue and n filled (only `leave-out` may stay `?`) | a person |
| rules signed | `run-add-job` | `design-goal.md` carries `rules: r〈k〉` and `signed:` | a person |
| set up | `run-reason-t00` | the three setup Runs closed; `inputs/method.md` there; `inputs/manifest.yaml` lists every file with its sha256 (first 12 hex) | none |
| fence | opening the design Tasks | `run-open-designs-j〈NN〉`'s first pass, `passes/pNN-〈MMDD〉/fence-check.md`, written by the reviewer agent, says pass: every reasoning step's `from` is a manifest file or `own knowledge` | none |
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

`scripts/project_draft.py draft 〈task〉` takes the newest draft (the closed `run-generate-d〈NN〉`'s
`result/design.md`, or the newest pass of `run-revise-d〈NN〉`, `passes/pNN-〈MMDD〉/design.md`, with its
`elements.yaml`) and writes it into the face's `## Design` and the Task's `elements.yaml`, then `state: verify`.
`scripts/project_draft.py verdict 〈task〉` reads the newest closed verify's `status:` (`passed` or `failed`) and
writes `state: passed` or `revise`.

`scripts/project_predictions.py 〈job〉` reads `t99_review-whole/runs/run-rank-t99/result/ranking.csv`
(`rank · design · predicted · why · kept`) and writes each design Task's `prediction.yaml` (`predicted · against ·
by · why · frozen: draft`; show the `why` beside the predicted number) and its `state` (kept or dropped, only from `passed`). It never touches a prediction already
frozen, and prints what it changed.

## Where a Job stands

No script prints the next Run yet; read it level by level from the faces and the `run.yaml` cards:

1. **Block**: the goal's line in `board.md ## Goals` (`name:`, `signed:`), `design-goal.md` (`rules:`, `signed:`), the inputs
   version's `manifest.yaml` (`frozen:`). Missing one: its Block Run is next (`run-add-goal`, `run-setup-rules`,
   `run-add-inputs`).
2. **Job setup**: `runs/run-setup-goal|method|inputs-j〈NN〉/run.yaml` `status:`; the first not `closed` is next.
3. **t00**: `t00_reason-ideas/runs/run-reason-t00/run.yaml`; then `run-open-designs-j〈NN〉` and its
   `fence-check.md` pass.
4. **Each design**: the face's `state:` names the next Run: `draft` → `run-generate-d〈NN〉`; `verify` →
   `run-verify-d〈NN〉-v〈k〉` for the newest draft k; `revise` → a new pass of `run-revise-d〈NN〉`; `passed` → wait
   for t99.
5. **t99**: every design `passed` or `dropped` → `run-rank-t99`; closed → `project_predictions.py`.
6. **Release**: every kept design with a projected prediction → `run-freeze-predictions` and `run-release`, then
   `run-close` once every Task is released or dropped.

A Run whose card says `open` or `running` is the one in flight; finish it before starting the next on that target.

## Stop rules

- One open Run per target: check the target's Run cards and do not allocate a competing Run while one is open.
  The allocator checks Run type and owner level; this concurrency check is the caller's duty. A verify is named by the
  draft it reads (`-v〈k〉`, k = 1 + the revise passes), so asking again for the same draft finds the same Run.
- A verify never reruns on an unchanged draft; a new draft is a new pass of `run-revise` and a new verify `-v〈k+1〉`.
- A hard Run's `result/` is closed once its card says `closed`, `passed` or `failed`; new inputs are a new Run.
- A Job is never edited after `run-release`: a changed method or inputs version is a new Job (`run-add-job`).
- Stop at `run-close-j〈NN〉`. Sending, the experiment and its measurement belong downstream; what comes back lands
  once at the Block (`run-add-observed`).

Report each actual Run with its type, target, kind, who did it, status, the gate it passed and the route taken.
Planned Runs are not inventory.

Before Job allocation, check that the inputs manifest is frozen and its recorded hashes match; the scaffold's
directory-existence check alone does not establish that gate. Before projecting a hard Result, read its Run card
and require a closed outcome (`closed`, `passed` or `failed`, as appropriate). The draft projection locates draft
files and protects settled Tasks, but does not itself check the generator's closure. Do not project an in-flight
Result merely because its file exists.
