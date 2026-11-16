---
name: haipipe-design
description: >-
  The one door for the design theme on the ladder: a design Block (one application, one channel), a Job (one
  goal × one method version × one inputs version → N designs), a Task per method step, and their Runs. Owns
  the ladder contract and scaffold (design_ladder.py); routes the rest to the goal, method, unit, workflow and
  delivery owners. `/haipipe-design update <Block>` brings an older design Block onto the current names and
  makes its Design Method Book. Use to set up a design Block, launch a Job, open its design Tasks, audit or
  update a design folder, find who owns a design Run, or read an older Design Folder board; where a Job stands
  is haipipe-design-workflow's. Trigger: design Block, set up a design Block, launch a design Job, open the
  design Tasks, design ladder, update design block, update the old design Block, Design Method Book,
  /haipipe-design, /haipipe-design update.
metadata:
  version: "0.4.2"
  last_updated: "2026-10-26"
  folder_owner: canonical
  folder_kind: design
  primary_face: board
  page_ruling: domain-gate
  outline:
    mode: grammar
    source: "ref/design-ladder.md"
    shape: "goal signed → Job pinned → ② ideas → ③ ④ each design → ⑤ rank → release"
---

# /haipipe-design · the design ladder's door

> Scripts here need Python 3.10+: where a command says `python3`, run it as `uv run --python 3.13 --with pyyaml python ...` (or a SPACE `.venv/bin/python`); see `plugins/haipipe-toolkit/skills/README.md` § Running a skill's scripts.

> **Hidden helpers** (JL 261026: not in the skill listing, `disable-model-invocation: true`): when this door names one below, read its SKILL.md by path; the Skill tool cannot load it. A person can still type its `/name`.
>
> - `haipipe-design-brief` → `../haipipe-design-brief/SKILL.md`
> - `haipipe-design-goal` → `../haipipe-design-goal/SKILL.md`
> - `haipipe-design-delivery` → `../haipipe-design-delivery/SKILL.md`

## Version governance

Each design skill keeps its own current version (this one `0.4.2`; `haipipe-design-unit` `0.4.1`, `workbench-design`
its own); none changes without a person's explicit approval. The move onto the ladder (261007) is recorded in each
CHANGELOG under the current version and does not by itself authorize a new one.

## The ladder

Read [ref/design-ladder.md](ref/design-ladder.md) on every invocation that creates, names or audits a design
folder. In one picture (designed in `Tools/blueprints/Project-Ladder/work/b12_theme_design`, s11 · s12 · s13 · s21):

```text
design/DesignMethodBook-<Topic>/  Block: the designer of one kind of thing; one Job per method type jNN_M0x-<slug>/
design/Design-<name>/             Block: one application, one channel; goals signed, inputs versions, Exp results
└── jNN_<goal>_M0x-<slug>-mK_inputs-vM/   Job: goal G01 × method M02 m1 × inputs-v2 → N designs; inputs/ is its fence
    ├── t00_reason-ideas/          ② reason ideas           run-reason-t00            (hard)
    ├── tNN_d<NN>_<slug>/          ③ ④ one design           run-generate-d<NN> · run-verify-d<NN>-v<k> (hard)
    │                                                       run-revise-d<NN>          (soft)
    └── t99_review-whole/          ⑤ review whole           run-rank-t99              (hard)
```

A **Design Method Book** beside the Board, `design/DesignMethodBook-<Topic>/`, is the designer of one channel:
sms, a checklist (JL 261109: named as insight's `insight/InsightQuestionBook-<Topic>/`; on screen "Design Method
Book", views Method · Versions · Ideas · Scorecard · MindMap). `<Topic>` names the channel, and its face says
it (`channel: sms`, the line its Boards carry too). The channel's own rules are the venue pack (`venue/venue-<channel>/`); an application's shared rules stay on its Board (`design-goal.md`), signed there. It holds one Job per method type `jNN_M0x-<slug>/`; types sit side by side and are compared (M01 goal
only, M02 overall performance), and only `mK` is a version of one type, signed by a person (`versions:` on the type's
face, `mK.md` frozen beside it). A method does not change when the materials do: new materials are a new inputs
version. One Board designs in one channel: it names its Book (`method-book:`), and each Job pins a type and a
version (`method: M01 m2`). Example: `blueprints/Project-Ladder/design/DesignMethodBook-Example/` beside `Design-Example/`.

```bash
python scripts/design_ladder.py block  design/Design-<name> --title "<application>" --channel sms
python scripts/design_ladder.py book   design/DesignMethodBook-<Topic> --serves design/Design-<name>
python scripts/design_ladder.py method design/DesignMethodBook-<Topic>/j01_M01-goal-only --version m2   # m2.md frozen beside the type; m2 must be registered in haipipe-design-method first
```

There is no `release` level in `design_ladder.py`: freezing a method version is `method --version mK` above;
releasing a design Job's designs is `haipipe-design-delivery`'s `scripts/release.py <job folder>`.

A design method is the recipe that turns a goal and its inputs into N designs in five steps (① See input · ② Reason
ideas · ③ Conduct process · ④ Review item · ⑤ Review whole). It is registered and versioned in
`haipipe-design-method`; a Job pins one version and never writes its own. One clock moves per Job (the method or the
inputs), so a change in the designs has one cause.

## Routing

| The request is about | Owner |
|---|---|
| the ladder's folders, names and faces; a new Block, Job or Task folder; `run-add-job`, `run-open-designs` | `haipipe-design` (this skill, `scripts/design_ladder.py`) |
| an older Block onto the current names, with its Design Method Book: `/haipipe-design update <Block>` | `haipipe-design` (this skill, [ref/update.md](ref/update.md)) |
| the goal list, the shared rules, an inputs version, a Job's `inputs/` fence: `run-add-goal`, `run-setup-rules`, `run-add-inputs`, `run-setup-goal`, `run-setup-inputs` | `haipipe-design-goal` |
| what a method is, its versions, the scorecard, a proposal, an Exp's results: `run-setup-method`, `run-propose-method`, `run-add-observed`, `run-score` | `haipipe-design-method` |
| one step of a method on one target: `run-reason-t00`, `run-generate`, `run-verify`, `run-revise`, `run-rank-t99` | `haipipe-design-unit` |
| where a Job stands and which Run is next, the gates, the run cards, a design's state and its projections (draft, verdict, predictions), `run-close` | `haipipe-design-workflow` |
| the release, the frozen predictions, `designs.json`: `run-freeze-predictions`, `run-release` | `haipipe-design-delivery` |
| what the workbench shows at each level | `workbench-design` |
| a Block question and its report: `run-propose-questions`, `run-report` | `haipipe-report` |
| the Run folder, its `run.yaml`, passes and receipts | `haipipe-run` |
| a channel's style rules (SMS, email, push, UI card …) | `venue/venue-<channel>/` |

The agents: `haipipe-designer-agent` does the Block's and the Job's soft Runs the cards give it (add a goal, set up,
launch, open designs, prepare a release) and reasons, generates and revises; `haipipe-design-reviewer-agent`
verifies, ranks, checks t00's fence and scores an Exp, always in a context that did not generate. A person signs a
goal, the shared rules, the frozen predictions with the release, and the close.

## The Runs this skill owns

**`run-add-job-j<NN>`** (Block, soft). Needs a signed goal in `board.md ## Goals`, signed shared rules
(`design-goal.md` `rules:` and `signed:`), a registered method version and a frozen inputs version; the scaffold
refuses any of them missing, an unsigned release, and a folder whose words differ from its pins. Makes the empty Job with its
pins; `n` comes from the goal's line (`--n` only to say the same):

```bash
python scripts/design_ladder.py job design/Design-<name>/j03_<goal-name>_M02-overall-performance-m1_inputs-v2 --goal G01 --moved method
python scripts/design_ladder.py job design/Design-<name>/j03_<goal-name>_<method-name> --goal G01 --method "M04 m2" --inputs i2 --moved method   # no Book: older names
python scripts/design_ladder.py run design/Design-<name> add-job j03
```

The Job is then set up by its own three Runs (`run-setup-goal`, `run-setup-method`, `run-setup-inputs`); set up =
all three closed.

**`run-open-designs-j<NN>`** (Job, soft). Its first pass is the reviewer agent's fence check: every reasoning
step's `from` in t00's `chains.yaml` names a file of the Job's `inputs/manifest.yaml` or says `own knowledge`, written
as `runs/run-open-designs-j<NN>/passes/pNN-<MMDD>/fence-check.md` ending in `pass` or `fail`. Only after a pass does
the next pass open one design Task per idea of `runs/run-reason-t00/result/ideas.yaml`, named by the idea's `name`,
then t99:

```bash
python scripts/design_ladder.py task <job> d04 <name>      # one per idea: I04 (name: <name>) → t04_d04_<name>/
python scripts/design_ladder.py task <job> t99
```

Every idea gets its Task; choosing among ideas is t99's ranking, never the opening.

`scripts/design_ladder.py run <folder> <type> [<target>]` makes any Run's folder and card (`run-<type>-<target>/
run.yaml` with `run · kind · type · scope · target · skill · agent · signs · status · by · started_at · finished_at ·
usage`; reason, generate, verify and rank are hard and get `result/`). It refuses a type that does not belong in that
folder (a generate outside a design Task), and names a verify by the draft it reads (`-v<k>`, k = 1 + the revise
passes). Each command writes only what is missing.

## Boundaries

- Ends at a person's release. Sending, allocation, the experiment and its measurement belong downstream; what an
  experiment returns comes back once, per Block, as per-arm totals (`run-add-observed`), never rows.
- Placeholders only in this skill and its references: no application, project, patient or vendor content.
- Generated or Run-written files (a Run's `result/`, `delivery/designs.json`) are never edited by hand: change the
  source and run the Run again.

## Update an older Block

```text
/haipipe-design update <Block path>             audit, dry run, apply, verify
/haipipe-design update <Block path> --check     audit and dry run only; nothing is written
/haipipe-design update <design/ folder>         every Design Board in it
```

Read [ref/update.md](ref/update.md) first and follow it. It brings a Board that still names things the older way
(`inputs/i1`, `jNN_<goal name>_<method name>`) onto the current names and makes its Design Method Book
(`DesignMethodBook-<Channel>`), through `scripts/design_ladder.py audit` and `update [--apply]`
(`scripts/design_update.py`). It never rewrites a file whose hash a manifest records, never signs a method version
(a person does), and never touches another Block. The much older `B00_DesignBoard-<name>/` layout is not its job:
see Older layout below.

## Older layout

An older board (`B00_DesignBoard-<name>/` with `0-BR-brief/`, `2-Design[-M<NN>]/Design-NN-<slug>/`, Design Items,
Commission → Generate → Verify, `run-design-<step>-<MMDD>-<slug>`) keeps its contract in
[ref/legacy/design-folder.md](ref/legacy/design-folder.md) and its own workbench until it is carried over;
[ref/legacy/method-folders.md](ref/legacy/method-folders.md) keeps its method groups. New work never writes it.
`scripts/carry_over/` holds the one-time moves (`design_ladder_by_method.py` is the first ladder's `_by-<method>`
scaffold, still read by the workbench's tests).

## Files

```text
haipipe-design/
├── SKILL.md                              this door
├── agents/haipipe-designer-agent.md      reason · generate · revise
├── agents/haipipe-design-reviewer-agent.md   verify · rank · the fence check
├── ref/design-ladder.md                  the contract: tree · rules · Runs · Spaces
├── ref/update.md                         /haipipe-design update: an older Block onto the current names
├── ref/legacy/                           the older Design Folder board
├── scripts/design_ladder.py              the scaffold: block · book · method · job · task · run · audit · update
├── scripts/design_update.py              what audit and update do
├── scripts/carry_over/                   one-time moves
└── tests/test_ladder_scaffold.py         the scaffold, and that the workbench reads it
```
