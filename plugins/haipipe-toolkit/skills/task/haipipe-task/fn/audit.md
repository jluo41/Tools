# fn/audit — Task Folder Run/Result consistency

Use for `/haipipe-task audit <task|job|block-path>`. The operation is read-only.

## Scope

- Task Folder: audit that Folder.
- Job: enumerate its direct `tNN_*` Task Folders.
- Block: enumerate `jNN_*/tNN_*` Task Folders.

Every Task candidate must have a same-stem Page, `scripts/`,
`scripts/config/`, and `runs/`. A container with no valid Task Folder is a
finding, not an execution target.

## Discover Run names

For each Task Folder:

```text
CONFIGS   stems of scripts/config/rNN_*.{yaml,yml,do}
TICKETS   stems of runs/rNN_*.{sh,ps1}
RESULTS   directory names in $OUTPUT_ROOT/results/<task>/
NOTEBOOKS stems in $OUTPUT_ROOT/notebooks/<task>/*.ipynb, excluding _source
ALL_RUNS  union of the four sets
```

Shared files in `scripts/config/` omit the `rNN_` prefix and are not Runs.
Stata Tasks may omit notebooks; route engine-specific config semantics to
`haipipe-task-for-stata`.

## Pairing checks

For every Run:

```text
<task>/scripts/config/<run>.<engine-config>
<task>/runs/<run>.<ticket-extension>
$OUTPUT_ROOT/results/<task>/<run>/runtime.yaml
$OUTPUT_ROOT/notebooks/<task>/<run>.ipynb   when notebook policy is not off
```

Check exact stem equality, `rNN_` grammar, receipt fields, config hash, Ticket
path, Result path, terminal status, and required Result artifacts. A Result
directory without `runtime.yaml` is always a finding.

## Classification

```text
missing_config     Ticket exists without its matching Run config
missing_ticket     Run config exists without its matching Ticket
missing_receipt    Result directory exists without runtime.yaml
missing_result     terminal receipt names a required artifact that is absent
missing_notebook   expected notebook record is absent
orphan_result      Result exists without matching config and Ticket
stale_review       CODE_REVIEW.md does not match current git SHA
stale_reading      Task Page reading receipt predates a load-bearing Run
```

Report each issue with the full Task and Run address plus exact path. Do not
repair during audit.

## Workflow checks

Read `workflow/plan.yaml` and `workflow/report.yaml` when present. Verify that
the Report mirrors the Plan, every output claim names an existing artifact,
and Task closure agrees with current Run and READING receipts.

## Return

```yaml
status: ok | issues_found
task_folders:
  - path: <full tNN path>
    type: <detected type>
    runs:
      r01_example:
        config: true
        ticket: true
        result: true
        receipt: true
        notebook: true
    issues: []
summary:
  task_count: 1
  run_count: 1
  finding_count: 0
```
