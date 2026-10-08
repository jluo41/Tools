# Design Run Profile · the ladder (0.4.0, 261007)

The Run contract is `haipipe-run`'s: one folder per Run in its level's `runs/`, a `run.yaml` card, hard or soft. This
profile names the design theme's Run types on the ladder (`haipipe-design/ref/design-ladder.md`). The older board's
profile is [legacy/run-profile-older.md](legacy/run-profile-older.md).

## Naming

Every Run is a folder `run-<type>-<target>/` (JL 261007: "unify the name to be run-xxx-xxx"), no date: the date is
in its passes. `<type>` is lowercase words joined by `-`; `<target>` is the object it works on, lowercased (`g01`,
`i2`, `j03`, `e01`, `q01`, `s01`, `t00`, `t99`, `d04`). A Run whose type already names its object drops the target
(`run-setup-rules`, `run-propose-questions`).

A repeat on the same target names what it reads, never a counter: the verify of d04's second draft is
`run-verify-d04-v2`, where k is the draft number (1 for the generate, plus one per pass of `run-revise-d04`). A
revise is one soft Run per design, one pass per new draft. Older names stay readable, never
renamed in place: `rNN_<type>_<target>/` (drawn before 261007) and `run-design-<step>-<MMDD>-<slug>` (the older
board).

## The 22 Run types

| Level | Run | Kind | Does | Who does it | Who checks | Signs | Skill |
|---|---|---|---|---|---|---|---|
| Block | `run-add-goal-<goal>` | soft | a goal into `board.md ## Goals` | designer agent | — | a person | haipipe-design-goal |
| Block | `run-setup-rules` | soft | the shared rules, `design-goal.md` | designer agent | — | a person | haipipe-design-goal |
| Block | `run-add-inputs-i<N>` | soft | an inputs version `inputs/iN/` + manifest, frozen | designer agent | manifest sha256 | none | haipipe-design-goal |
| Block | `run-add-job-j<NN>` | soft | an empty Job, its pins on its face | designer agent | — | none | haipipe-design |
| Block | `run-propose-method-<slug>` | soft | a method change, sent to the registry | designer agent | — | a person | haipipe-design-method |
| Block | `run-add-observed-e<NN>` | soft | an Exp's per-arm totals, `observed/eNN_<exp>/` | designer agent | manifest sha256 | none | haipipe-design-method |
| Block | `run-score-e<NN>` | soft | every arm's design scored, `scores.csv` in its own folder | reviewer agent | — | none | haipipe-design-method |
| Block | `run-propose-questions` | soft | the Block's questions into `board.md ## Questions` | designer agent | another agent agrees | none | haipipe-question |
| Block | `run-report-q<NN>` | soft | a question's report in `reports/qNN_<topic>/` | designer agent | another agent | none | haipipe-report |
| Block | `run-draw-s<NN>` | soft | a studio topic and its builder | designer agent | — | none | excalidraw-report |
| Job | `run-setup-goal-j<NN>` | soft | confirm the face's `goal:` pin names a signed goal; record it in its pass | designer agent | signed at the Block | none | haipipe-design-goal |
| Job | `run-setup-method-j<NN>` | soft | pin a method version; `inputs/method.md`, `method-sha` | designer agent | — | none | haipipe-design-method |
| Job | `run-setup-inputs-j<NN>` | soft | build `inputs/goal.md`, the links and `manifest.yaml` (step ①), after `inputs/method.md` | designer agent | manifest sha256 | none | haipipe-design-goal |
| Job | `run-open-designs-j<NN>` | soft | pass 1: the reviewer's `fence-check.md`; on pass, one design Task per idea, then t99 | designer agent | reviewer agent (the fence check) | none | haipipe-design |
| Job | `run-freeze-predictions-j<NN>` | soft | freeze the kept designs' predictions | a person | — | a person | haipipe-design-delivery |
| Job | `run-release-j<NN>` | soft | the kept designs into `delivery/` | designer agent | — | a person | haipipe-design-delivery |
| Job | `run-close-j<NN>` | soft | close the Job; frozen | designer agent | every design terminal | a person | haipipe-design-workflow |
| Task | `run-reason-t00` | hard | ② `ideas.yaml` · `chains.yaml` · `topics.md` | designer agent | the fence check | none | haipipe-design-unit |
| Task | `run-generate-d<NN>` | hard | ③ one design, its `elements.yaml` | designer agent | its own self-check | none | haipipe-design-unit |
| Task | `run-verify-d<NN>-v<k>` | hard | ④ T0 · T1, and T2 when the method's ④ lists it, on draft k | reviewer agent | the result itself | none | haipipe-design-unit |
| Task | `run-revise-d<NN>` | soft | the next draft from frozen feedback, one pass each | designer agent | the next verify | none | haipipe-design-unit |
| Task | `run-rank-t99` | hard | ⑤ rank, keep N, predict (T3 on the kept when the method's ⑤ asks); `ranking.csv` | reviewer agent | — | none | haipipe-design-unit |

A closed hard Run's Result reaches its level's files only through `haipipe-design-workflow`'s projections:
`project_draft.py draft` (a draft into the Task's face and `elements.yaml`), `project_draft.py verdict` (the
verify's status into `state:`), `project_predictions.py` (t99's ranking into each `prediction.yaml` and `state:`).
These are Steps of the workflow, not Runs.

## Hard and soft

A **hard** Run (`kind: hard`: reason, generate, verify, rank) writes only its own `result/` and counts as evidence.
Its ticket is its `run.yaml` (no `.sh`: an agent runs it under its skill). While its card says `open` or `running`
the Run may be retried in place; once `closed`, `passed` or `failed`, its `result/` never changes, and new inputs are
a new Run (a verify of the next draft is the next `-v<k>`).

A **soft** Run (`kind: soft`) writes its level's own files (a face, `board.md`, `design-goal.md`, `inputs/`,
`delivery/`) and keeps each round in `passes/pNN-<MMDD>/`. Two soft Runs keep their output in their own folder:
`run-revise-d<NN>`, whose pass holds the new draft (`passes/pNN-<MMDD>/design.md`, `elements.yaml`,
`feedback.md`) until `project_draft.py draft` carries it into the Task; and `run-score-e<NN>`, whose `scores.csv`
is the Block's record of that Exp's scoring. A person's decision (a signature, a release) is soft.

## The card: run.yaml

```yaml
run: run-verify-d04-v2
kind: hard                 # hard · soft; the name does not say it
type: verify
scope: t04_d04_<slug>      # the level folder whose runs/ holds it
target: d04-v2
skill: haipipe-design-unit
agent: haipipe-design-reviewer-agent
signs: none                # what a person signs on it, or none
status: open               # open · running · closed · passed · failed · blocked
by: reviewer agent         # who did it, written by the Run's writer; for a verify, never the agent that generated
started_at: 2026-10-07T10:00:00
finished_at: 2026-10-07T10:02:00
usage: {in: <tokens>, out: <tokens>}   # the Cost and Performance views read it; {} while unknown
```

These are haipipe-run's card fields (`run · kind · type · scope · target · skill · agent · signs · status`) plus
the design theme's `by · started_at · finished_at · usage`; `ticket`, `passes`, `writes` and `feeds` are left out
because the card is the ticket and the passes are its folder.

A verify adds `tests: {T0: ✓, T1: ✓}` (and `T2` when the method lists it) and `status: passed | failed`; a
generate adds `draft: 1`. The card is written by the
scaffold (`haipipe-design/scripts/design_ladder.py run`) and then by the Run's own writer; a reader lists, counts and
shows Runs from it without opening a Result.

## Counting

Count allocated Run folders, with their status, including failed, blocked and superseded ones. Passes, Steps, model
calls, drafts inside one pass, renders and projections are not Runs.
