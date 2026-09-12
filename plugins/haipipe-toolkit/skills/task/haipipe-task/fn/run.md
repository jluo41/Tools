# fn/run — create or execute one Task Run

Use for `/haipipe-task run <task-folder-path> [run-name]`.

## Input contract

The target must be a canonical Task Folder:

```text
tasks/bNN_<block>/jNN_<job>/tNN_<task>/
```

Require the same-stem Task Page, `scripts/`, `scripts/config/`, and `runs/`.
Reject a Job, Block, or any path outside this hierarchy.

The Run name must match `rNN_<noun>_<qualifier>`. If omitted, select it only
when exactly one Ticket exists; otherwise ask once or return `blocked` in auto
mode.

## Resolve the Run spine

```text
config    <task>/scripts/config/<run>.yaml
Ticket    <task>/runs/<run>.sh
Result    $OUTPUT_ROOT/<task>/results/<run>/
notebook  $OUTPUT_ROOT/<task>/notebooks/<run>.ipynb
receipt   $OUTPUT_ROOT/<task>/results/<run>/runtime.yaml
```

`RESULT_STORE` wins output-root resolution. Next read `store:` from
`<job>/src/config-defaults.yaml`. Otherwise `$OUTPUT_ROOT` is the Job.

## Scaffold

When the Run does not yet exist:

1. Check that the requested stem does not collide in any projection.
2. Copy `ref/config-meta-template.yaml` to the config path and fill its required
   purpose and notebook policy.
3. Copy `ref/run-sh-template.sh` to the Ticket path.
4. Set `TASK_NAME`, `RUN_FAMILY`, `RUN_OPERATION`, `RUN_TARGET`,
   `REQUIRED_RESULTS`, and any extra `RUN_INPUTS`.
5. Make the Ticket executable.
6. Create the Result directory under `$OUTPUT_ROOT` and write a complete
   `status: planned` receipt atomically.
7. Run `bash -n` on the Ticket and the structural checker on the Block.

Do not create generated Results in the Task Folder.

## Execute

Before launch:

- confirm config and Ticket stems match;
- confirm all declared input paths resolve;
- confirm `CODE_REVIEW.md` is current for the checked-out code, unless the
  explicit skip flag is present;
- confirm the Result path belongs to this `<task>/<run>` identity.

Execute the exact Ticket. The Ticket writes `running` before expensive work,
applies its declared Result gate, then writes a truthful terminal receipt.

## Return

```text
status:    ok | blocked | failed
summary:   created or executed <bNNjNNtNNrNN>
artifacts: [config, Ticket, runtime receipt, Result paths]
next:      /haipipe-task report <task-folder-path>
```

## Must not

- Accept a container in place of a Task Folder.
- Invent a Run name without checking sibling indices and the stranger test.
- Execute more than one Ticket.
- Put a batch loop in `runs/`.
- Mark a Run complete before its Result gate passes.
- Touch another Run's config, Ticket, Result, or notebook.
