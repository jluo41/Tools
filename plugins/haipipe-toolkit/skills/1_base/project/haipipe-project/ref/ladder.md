# The ladder · what each level may hold

One table for the shape of every level under a Project world:
Block → Job → Task → Run → pass. `scripts/ladder.py` reads the yaml block below, so
`/haipipe-project audit <path>` checks a Block, a Job, a Task or a Run against it, and
`/haipipe-project update <path>` fixes what is safe. Edit the table here, never in the script.

This skill checks the **shape** (names, faces, which folders sit where, the Run card).
The owning skill keeps the **content**: a Page's sections belong to haipipe-page, a
ticket's body to haipipe-task, a Run's kinds and passes to haipipe-run.

## The levels

```text
level   name            face               may hold                                     children
Block   bNN_<topic>/    board.md           studio/ reports/ delivery/ resources/ src/   jNN_<job>/
Job     jNN_<job>/      jNN_<job>.md       studio/ reports/ delivery/ src/ sbatch/      tNN_<task>/
                                           runs/ (soft Runs only)
Task    tNN_<task>/     tNN_<task>.md      studio/ reports/ delivery/ scripts/ draft/   runs/<run>/
                                           displays/ notebooks/ tests/ workflow/
Run     runs/<run>/     run.yaml           the ticket · config.yaml · result/ · passes/  pNN-<MMDD>/
```

1. **Face**: a Block's face is `board.md` (the rename to `bNN_<topic>.md` is still an open
   design question, so both pass); a Job's and a Task's face is its own name plus `.md`.
2. **Task kind**: a Task face may say `task-kind: page`; a Page Task holds soft Runs only.
   Without the field a Task is a work Task.
3. **Hard and soft**: a hard Run (`rNN_<slug>`, ticket `.sh`, `.cmd` where only cmd.exe runs, or a runner `.yaml`) writes only
   its own `result/` and lives in a work Task. A soft Run (`run-<type>-<target>`, ticket `.md`; a Page's Delivery Run `run-delivery-<lane>` keeps its one command, `.sh`)
   writes into its scope's items, has no `result/`, and may sit at Block, Job or Task. Its name
   carries no date; the date is in its passes. haipipe-run owns the definitions.
4. **Old layout**: `runs/<run>.sh` beside `results/<run>/` is the layout before one folder per
   Run. The audit reports it as debt; `update --apply` moves it (see `fn/update.md`).
5. **Families**: a Block's `workbench:` field (default `task`) adds its family's extras below.

## The table

```yaml
levels:
  block:
    may_hold: [studio, reports, delivery, resources, src, runs, _old]
    debt:
      diagram: "diagram/ is retired: drawings go in studio/"
      diagram-ceiling: "diagram/ is retired: drawings go in studio/"
  job:
    may_hold: [studio, reports, delivery, src, sbatch, runs, _old]
    debt:
      diagram: "diagram/ is retired: drawings go in studio/"
      scripts: "a Job holds no scripts/: src/ and sbatch/ mark a Job; local code goes in a Task"
      results: "a Job holds no results/: evidence sits in a Task's runs/<run>/result/"
      notebooks: "a Job holds no notebooks/: they belong to a Task's Runs"
      workflow: "workflow/ at a Job is not in the ladder"
  task:
    may_hold: [studio, reports, delivery, scripts, draft, displays, notebooks, tests, workflow,
               runs, _old]
    debt:
      results: "old layout: results/<run>/ moves into runs/<run>/result/"
      diagram: "diagram/ is retired: drawings go in studio/"
  run:
    may_hold: [result, passes, run.yaml, config.yaml]

names:
  block: '^(b\d{2}_[A-Za-z0-9][A-Za-z0-9_-]*|Paper-[A-Za-z0-9][A-Za-z0-9-]*)$'   # a paper Board: Paper-<Slug>/
  job:   '^j\d{2,3}_[A-Za-z0-9][A-Za-z0-9_-]*$'                                    # kebab tails (paper, design)
  task:  '^t\d{2}_[A-Za-z0-9][A-Za-z0-9_-]*$'
  hard:  '^r\d{2,3}_[A-Za-z0-9][A-Za-z0-9_.-]*$'
  soft:  '^run-[a-z]+-[A-Za-z0-9][A-Za-z0-9_.-]*$'
  soft_dated: '^run-[a-z]+-\d{4}-'

families:
  task: {}
  discovery: {}
  insight:
    block: [meta, datasets]
    hard: '^[a-z0-9]+_[a-z0-9_]+$'       # <dataset>_<partition>; its vNNN are passes
  paper:
    block: [venues, related]             # a paper Board's venues and related papers (a meeting is a comments report)
  cowork:
    job: [emails, meetings, materials, design]  # a cowork Job's lanes (haipipe-cowork), text only
  labeling:
    task: [labeling]
    hard: '^rl\d{2}_[a-z0-9_-]+$'        # rlNN_<operation>_<target>, owned by subjective-label

checks:
  heavy_mb: 10                           # AGENTS rule 10: a Result is light
  absolute_path: '/(Users|home)/[^/\s]+/' # AGENTS rule 7
```

## What the audit reports

`failed` breaks the contract; `debt` is a known older shape that `update` or its owner
fixes later; `ok` is clean. A folder's status is its worst finding.

```text
failed   a hard Run in a Page Task, a Job or a Block · a soft Run with result/ ·
         a Run with no ticket · run.yaml disagreeing with its folder (run, kind) ·
         a hard Run marked done with no result/ · a heavy file in a Result ·
         an absolute path in a ticket, run.yaml or receipt · a Run name neither hard nor soft
debt     a missing face · the old runs/ + results/ layout · a dated soft name ·
         a Run with no run.yaml · a folder the ladder does not list (named in the finding)
```
