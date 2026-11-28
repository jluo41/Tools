# Idea Blocks and Paper handoff

Date: 2026-11-24

User request:

> I’m thinking about to make the idea to be one specific block them self. And one idea will be a job and then in the task, they are a series of skills to evaluate it and check it. Do you get what I mean? I hope each idea will be developed to one paper later. What is your thoughts

> After make the plan and then do the implementation to update the content in the plugin

## Decision

Use an Ideation Block for one bounded research direction, one Job for each
admitted idea, and Tasks for the questions that develop or assess that idea.
A Task can apply several skills; a skill invocation does not allocate a Task
or Run. Keep the current public skill names and their installation paths.

```text
ideation/b01_<direction>/
├── board.md + ideation.yaml           direction and index of Idea Jobs
├── j01_<idea>/                        one scientific proposition
│   ├── ideation.yaml + cards/         one canonical Idea Card
│   ├── t01_<question>/                a bounded assessment
│   │   └── runs/run-assess-<target>/   shared soft Run contract
│   └── t02_<question>/                another assessment or development output
└── j02_<idea>/                        independent candidate and history

selected Idea Job ── human receipt ──▶ paper/Paper-<slug>/
                                        versions → sections → writing Runs
```

Local assessment Runs preserve reasoning, reviews and decisions. Source
acquisition remains Discovery's; new scientific computation remains Work's.
Those owners' Results are referenced, never copied into a second evidence bank.
An idea can also remain open, be deferred, be abandoned, or be explicitly split
or merged. A paper is an intended outcome, not a promised result of every idea.

## Implementation order and files

Paths below are relative to `plugins/haipipe-toolkit/skills/`.

| Step | Files | Change |
|---|---|---|
| 1. Ownership | `1_base/ideation/hai-ideation/{SKILL.md,CONSTITUTION.md,references/idea-block.md}` | Define Block → Idea Job → question Task; preserve canonical IDs and legacy task portfolios. |
| 2. Workflow | Ideation `references/{workflow-runs,workflow-table,manifest-and-sync,idea-card,receipts,end-to-end-example}.md`, `_parts/{generate,test,select}/PART.md` | Place one existing semantic unit in each new Idea Job; map assessments to Tasks/soft Runs; keep evidence owners and human selection. |
| 3. Mechanical guard | Ideation `scripts/check_idea_block.py`, `scripts/selection_contract.py`, new tests | Check Job/card ownership and Task structure; allow a new Idea Job to select without an existing Paper projection, while retaining exact semantic revision, evidence, target and human-receipt checks. Keep legacy checks unchanged. |
| 4. Paper adapter | `3_theme/paper/hai-paper{,-ideation}` and `workbench-paper` skills/references | Paper Idea view projects its source Job. Default selected Jobs lead to separate Paper Blocks. Existing Paper-local portfolios remain readable. Record reciprocal origin links; no automatic movement of old data. |
| 5. Cross-owner vocabulary | Base Block/Job/Task/Project entrypoints and Project structure, Discovery BJTR alignment, plugin README | Link the canonical contract and remove the blanket prohibition on local assessment Runs. |
| 6. Verify | Unit tests, skill frontmatter/link checks, fresh-context realistic invocation | Exercise multiple ideas, repeated evaluation, absent Paper, human selection, stale revision, and legacy portfolio compatibility. |

## Identity, compatibility and handoff

- Keep `iNN` as the stable semantic identity within a Block; `jNN` is the Job
  address. They need not have the same number. Never renumber to match ranking.
- Reuse the existing `kind: ideation-unit` semantic schemas inside a Job with
  an explicit `layout: idea-job` marker. The Block owns a pointer-only index.
- Each Job retains its own bounded context, evidence pointers, one Card, tests,
  sync revision and immutable human decisions. The Block aggregates pointers.
- New Idea Jobs can finish evaluation before a Paper exists. A missing Paper
  working projection is not missing scientific evidence. Selection still
  binds the exact semantic revision and all existing scientific/human gates.
- Legacy multi-card Task units stay at their current paths. Converting an
  existing portfolio is a separate scoped migration with an alias/path map,
  preserved receipts and link verification; this change migrates no live data.
- After selection, the Paper owner creates or binds the destination. Repeating
  a handoff reuses the recorded destination. Revisions of the same paper are
  Paper Jobs; splitting/merging scientific ideas needs explicit lineage.

## UI map and scope

The plugin documentation will map Block to the candidate index, Job to one
idea's evidence and decisions, and Task to its assessment and Run history.
Faces and links support the existing generic workbench. A new dedicated Idea
Board renderer, new controls and live page rollout are separate work, and
must not be described as shipped by a content update.

Keep Related in both Paper Idea and Story, and Story by Section in both Story
and Displays. The new source link changes ownership, not those placements.

## Completion evidence

Implemented the plugin-content plan on 2026-11-24. The public skill paths are
unchanged. The Idea Block contract, scientific owner routes, Paper source
adapter, base ladder vocabulary, Constitutions, examples and topic record
now agree on the new structure. No live portfolio was moved or converted.

The independent trial exposed additional changes needed to make the content
usable, which were implemented in the same update:

- Registered `task-type: ideation` with the existing `hai-ideation` owner;
  added its Type contract and `references/assessment-task.md`, routing in the
  Task skill, and lazy Task scaffolding in `hai-job/scripts/new_job.py`.
- Allowed an empty Opportunity Map for an indexed new Idea Job with explicit
  evidence gaps. Kept Test/Select evidence gates intact. Moved projection
  validation out of the oversized checker into `projection_contract.py`.
- Routed the shared Task tree check to the Idea owner; registered Ideation's
  folders in the ladder schema and extracted family detection into
  `hai-project/scripts/ladder_family.py`. The previously oversized ladder
  file shrank; its unrelated audit/update mechanics stayed in place.

Actual automated checks:

| Suite/check | Result |
|---|---|
| Ideation legacy and new Block/selection regressions | 54 passed |
| Job scaffold regressions | 13 passed |
| Project ladder/update regressions | 19 passed |
| Task contract/vocabulary regressions | 10 passed |
| Changed public skill frontmatter | 9 valid |
| New local links, file-size rules, `git diff --check` | Passed |

Fresh-context validation used a temporary research fixture with two provisional
ideas, one typed evaluation Task, and one shared soft Run with repeated passes.
Structure, Generate, Sync, both Job checks, the shared Task checker and the
structural ladder audit passed. A missing canonical Card was rejected.
Scientific Test remained unresolved and Select/Handoff rejected missing human
selection, as required. No evidence, pilot, human decision or Paper was invented.

The minimal fixture's optional `ladder.py audit --today` still reports its
missing Block Studio/Questions content; the structural audit is clean. Those
project-content obligations do not justify manufacturing empty topics.
Dedicated Idea Board rendering, origin-file UI controls, and a live-page
rollout remain separate work, recorded as open in the Paper topic register.
This implementation does not claim those UI cases fixed.
