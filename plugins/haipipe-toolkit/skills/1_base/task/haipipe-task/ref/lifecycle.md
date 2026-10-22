# A Task's life · plan ▶ build ▶ run ▶ read ▶ close

One `tNN_<task>/` from its first line to its close. The words Plan, Build, Execute and Report are
commands on the Task (`fn/stage-plan.md`, `fn/stage-report.md`, `ref/task-lifecycle.workflow.js`);
they are not phases that own anything. What each step leaves on disk:

```text
step    what it leaves                                              who writes it
plan    the Job's ## Deliverables item it feeds (haipipe-job)        the agent that knows the Job
        the face's goal: and close: lines (ref/task-page.md)
        each planned Run's folder and card, status: planned (haipipe-run)
        workflow/plan.yaml only when several Runs share routes or gates
build   scripts/<worker>, the Run's config, its ticket, its card    the type skill's creator
        CODE_REVIEW.md when the lifecycle Workflow runs             the reviewer agent
run     result/runtime.yaml: running ▶ complete | partial | failed   the ticket
        result/ files, heavy.yaml, passes/pNN-<MMDD>/ when rerun
read    result/headline.txt, a describe Run, a figures Run          their own Runs
        the face's reading (a Task Page's READING table)            a person
        workflow/report.yaml when a plan.yaml exists                fn/stage-report.md
close   the close: line is true and the Job's items it feeds tick   checked from disk
```

## Plan

1. **Start from what the Job hands on**: the Job face's `## Deliverables` names the item this Task
   makes and the files it lands as. A Task no item needs is a question for the Job, not a new folder.
2. **Write the face's two lines**: `goal:` (what this Task delivers, one line a stranger reads) and
   `close:` (what must be true to close it).
3. **One Run per independently closable piece**: a fold, a model, a source, a retry. Its card says its
   `role:` (haipipe-run `run_roles.py` proposes one). An uncommissioned future Run stays a line in the
   plan, with no folder and no number.
4. **A plan file only when it pays**: `workflow/plan.yaml` (haipipe-run `ref/workflow.md` and
   `ref/plan-schema.md`) when Runs share routes, gates, a human HOLD or a resume point; the workbench's
   Plan view reads it. Each type skill's `ref/workflow-plan-sample.yaml` is its example.

## Build

1. **The worker** goes in `scripts/` in the type's language; shared code goes in the Job's `src/`.
2. **The config** holds every value the worker reads, with `_meta.purpose` (`ref/config-meta-template.yaml`).
3. **The ticket** starts from the type skill's template, else `ref/run-sh-template.sh`; it names one
   config and finds its own address from its path (`ref/task-folder.md` § A Run inside the Task).
4. **Review**: the reviewer agent checks the code against the Task's intent before it runs (Gate 1).
   Creator and reviewer stay separate; `revise` returns specific feedback, `fail` stops for a person.

## Run

1. **Who presses Run**: a quick, local, unpaid Run that a request leads to is run and reported; a paid
   (LLM, search API), long or shared-store Run waits for a person (AGENTS working rule 2).
2. **The receipt is the record**: `running` before expensive work, then `complete` only when the Result
   gate passed, `partial` when some of it did, `failed` with the reason. A process exit alone proves
   nothing. A Run that ran before its ticket wrote receipts gets one rebuilt from its files (haipipe-run
   `ref/receipts-and-inventory.md` § Rebuilt receipts).
3. **Long Runs** run in `tmux` on the machine that holds the data; a supervisor in `sbatch/` runs
   tickets in order and leaves each ticket's own receipt.

## Read

1. **The headline**: each Result says its numbers in one line (`result/headline.txt` or the receipt's
   `headline:`); the workbench shows it beside the Run.
2. **Describe and figures Runs**: a stored table gets its Table Card from a `role: describe` Run, and
   charts come from a `role: figures` Run; neither is drawn by hand.
3. **The face's reading**: a Task with a Task Page carries its `#### READING · current` table
   (`ref/task-page.md` § Reading and closure); only a person writes `✅ read`.
4. **A report file** (`workflow/report.yaml`) mirrors a `plan.yaml` when there is one: actual Runs from
   their receipts, planned and actual counts kept apart, missing pairs shown as findings.

## Close

```text
task_ready    = every planned Run terminal + its Result gate passed + its receipt current
page_ready    = (a Task Page only) every Page Run closed, every number bound to its Run, READING current
task_closed   = task_ready AND page_ready AND the close: line is true
```

The Job's Goal view ticks the items this Task feeds from disk; that is the visible close. A new,
rerun or replaced Run reopens only what read it: its items, its reading, its Page version. It never
renames the Task.

## Rules that hold at every step

- A Task is one computation, one output contract, one code path (`ref/task-folder.md` § What earns a Task).
- Every config and ticket share the Run's exact stem; one Run, one folder.
- A configured name that does not resolve raises and names what is missing.
- Big files go to `HEAVY_DIR`; the Result keeps `heavy.yaml`.
- Never hand-edit a generated file (a notebook, a figure, a Table Card, a board): change its source and
  rerun the Run that writes it (AGENTS working rule 6).
- Refuse overwrites and name collisions; preserve a failed Run's record.
