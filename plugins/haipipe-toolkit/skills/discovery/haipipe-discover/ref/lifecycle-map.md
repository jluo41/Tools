# Discovery Lifecycle Map

A discovery is **one research topic, stored as its own folder** — exactly the
way a task is one runnable unit stored as its own folder. Each stage of the
lifecycle fills one IO file inside that folder, the same way each task run fills
`configs/` / `results/` / `notebooks/`.

This file is the CANONICAL contract for the discovery layer. Do not restate it
in SKILL.md or DESIGN.md; point here and edit here.

## Hierarchy (mirrors task)

```
task:       tasks/{G}{NN}_group/   ⊃  {NN}_taskname/   (one runnable unit)
discovery:  discoveries/<GROUP>/   ⊃  <NN>_<topic>/    (one research topic)
```

Each time it is a different topic, so each gets its own folder. Discoveries
accumulate under `discoveries/` over the project's life, just like task-folders
accumulate under `tasks/`.

## The discovery-folder = the unit (one topic)

```
discoveries/<GROUP>/<NN>_<topic>/
├── discovery.yaml   spec: question · parent · role · requested sources · expected_outputs · verdict
├── sources.md       search output
├── notes.md         read output
├── verdict.md       review / idea output
├── status.yaml      machine snapshot
└── site.md          human panel
```

Its IO channels map one-to-one onto the task-folder:

| task-folder (one run) | discovery-folder (one topic) |
|---|---|
| `configs/<run>.yaml`  (spec) | `discovery.yaml` |
| `results/<run>/`      (output) | `sources.md` · `notes.md` · `verdict.md` |
| `runtime.yaml`        (state) | `status.yaml` |
| `notebooks/<run>.ipynb` (record) | `site.md` |

`sources.md` / `notes.md` / `verdict.md` ARE the discovery's `results/`: a task
emits one result bundle per run, a discovery emits one file per stage.

## Lifecycle: fill the folder's IO files

Scaffold the folder once (like scaffolding a task-folder), then each work stage
reads the previous output and writes the next `expected_output`:

| stage | skill (the tool) | `files_in` | `files_out` |
|---|---|---|---|
| `open` *(bookend, scaffold)* | `haipipe-discover` + `ref/discovery-yaml-schema.md` | parent ref | `discovery.yaml` · `status.yaml` · `site.md` (creates the folder) |
| `search` | `1_search/`: arxiv · semantic-scholar · exa-search | `discovery.yaml` | `sources.md` |
| `read` | `2_read/`: alphaxiv · deepxiv · paper-analyzer | `sources.md` | `notes.md` |
| `review` | `3_review/`: research-lit · comm-lit-review · academic-researcher | `notes.md` | `verdict.md` (+ `discovery.yaml` verdict block) |
| `idea` *(topic-type alt to review)* | `4_idea/`: idea-creator · novelty-check | `notes.md` | `verdict.md` |
| `post` *(bookend, handoff)* | `haipipe-discover` | `verdict.md` · `discovery.yaml` | `discovery.yaml` consumed_by · `status.yaml` · `_haipipe/project.{status.yaml,log.jsonl}` |

`open` and `post` are one-time bookends (scaffold the unit, hand it off) — the
same role as scaffolding a task-folder and handing its results to a probe. The
real work stages are `search → read → review` (or `idea`), each producing one of
the `expected_outputs` declared in `discovery.yaml`.

## Parent model (narrative retired)

```
Delivery-open (paper / application)  ->  L* landscape / novelty / benchmark
Probe-open                           ->  P* / B* / C* / S* claim-level evidence
```

A delivery lifecycle reads the landscape/novelty verdicts at its open need; a
probe reads claim-level verdicts at Probe-post.

## Command routing

```
/haipipe-discover                          -> dashboard (list discovery-folders)
/haipipe-discover open <role> <question>   -> scaffold a discovery-folder
/haipipe-discover search <discovery>       -> fill sources.md
/haipipe-discover read <discovery>         -> fill notes.md
/haipipe-discover review <discovery>       -> fill verdict.md
/haipipe-discover post <discovery>         -> link verdict to parent
/haipipe-discover <discovery>              -> run remaining stages
/haipipe-discover <specialist> [args]      -> one-off bucket skill (NO folder)
```

A one-off capability call (just run arxiv / alphaxiv / research-lit) does NOT
create a folder. The discovery-folder exists only for durable, project-tracked
topics — the same split as running a quick script vs scaffolding a task-folder.
