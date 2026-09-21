# plan.yaml · Workflow Run Spec graph

## Definition schema

```yaml
name: build-lbp-data-pipeline
purpose: build, validate, and review one bounded data artifact
owner: haipipe-task-for-data

plugin:
  id: data-workbench
  workspace_roster_ref: plugins/data-workbench.yaml#workspace_roster
  workspace_ids: [create, review, runtime]

input:
  args: {name: run_lbp, task_folder: tasks/b01_data/j01_lbp/t01_source}
  files_in: [ref/source_fn_template.py]

run_specs:
  - id: author
    run_type: authoring.write-file
    purpose: create the requested bounded artifact
    target: tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-for-data}
    action: author-file
    input: [ref/source_fn_template.py]
    depends_on: []
    entry_gate: {mode: automatic, assertion: required inputs resolve}
    exit_gate: {mode: automatic, assertion: file exists and syntax check passes}
    routes: {pass: review, fail: HOLD}
    result:
      payload: {status: ok, file_path: tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py}
      receipt: results/author/runtime.yaml
    cardinality: 1
    cells:
      - {workspace_id: create, mode: action, owner_skill: haipipe-task-for-data, worker_skill_chain: [haipipe-task-for-data], interaction: author file, authority_change: create, source_projection: authoritative Result}
      - {workspace_id: review, mode: empty, owner_skill: none, worker_skill_chain: [], interaction: none, authority_change: none, source_projection: none}
      - {workspace_id: runtime, mode: read-only, owner_skill: haipipe-plugin-runs, worker_skill_chain: [], interaction: inspect status, authority_change: none, source_projection: same Run/receipt}

  - id: review
    run_type: evaluation.validate
    purpose: independently review the authored artifact
    target: tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-reviewer-agent}
    action: code-review
    input: [results/author/result.yaml]
    depends_on: [author]
    exit_gate: {mode: agent, assertion: verdict is pass, warn, or fail with findings}
    routes: {pass: CLOSE, warn: author, fail: author, blocked: HOLD}
    result:
      payload: {verdict: pass, issues: []}
      receipt: results/review/runtime.yaml
    cardinality: 1
    cells:
      - {workspace_id: create, mode: read-only, owner_skill: haipipe-task-for-data, worker_skill_chain: [], interaction: inspect candidate, authority_change: none, source_projection: author Result}
      - {workspace_id: review, mode: review, owner_skill: haipipe-task-reviewer-agent, worker_skill_chain: [haipipe-task-reviewer-agent], interaction: independent review, authority_change: bind, source_projection: authoritative verdict}
      - {workspace_id: runtime, mode: read-only, owner_skill: haipipe-plugin-runs, worker_skill_chain: [], interaction: inspect status, authority_change: none, source_projection: same Run/receipt}

entry: [author]
terminal: [CLOSE, HOLD]

output:
  returns: [status, artifacts, verdict, receipts]
  files_out: [tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py]
```

## Report schema

The report mirrors Run Specs with actual Run Instances:

```yaml
name: build-lbp-data-pipeline
plan: ref/plan.yaml
executed_at: "2026-09-15T14:30:00-04:00"
workflow_runtime_id: runtime-20260915-143000
runs:
  - run_id: r01_author
    run_spec_id: author
    run_type: authoring.write-file
    target: tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-for-data}
    status: complete
    gate_outcome: pass
    route_taken: review
    result: results/author/result.yaml
    receipt: results/author/runtime.yaml
  - run_id: r02_review
    run_spec_id: review
    run_type: evaluation.validate
    target: tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-reviewer-agent}
    status: complete
    gate_outcome: pass
    route_taken: CLOSE
    result: results/review/result.yaml
    receipt: results/review/runtime.yaml
summary:
  status: closed
  runtime_status: complete
  planned_cardinality: 2
  actual_runs: 2
  terminal_route: CLOSE
  files_created: [tasks/b01_data/j01_lbp/t01_source/scripts/build_lbp.py]
```

## Field requirements

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | stable Run Spec id |
| `run_type` | yes | resolved catalogue key |
| `purpose` | yes | why this Run independently closes |
| `target` | yes | bounded goal/target |
| `actor` | yes | decision/execution mode and owner |
| `action` | yes | action or interaction boundary |
| `input` | no | frozen inputs; may be empty |
| `depends_on` | no | upstream Run Specs |
| `entry_gate` | no | omitted means open |
| `exit_gate` | yes or inherited | testable close semantics |
| `routes` | yes unless terminal default CLOSE | outcome mapping |
| `result.payload` | no | payload may be none |
| `result.receipt` | yes | durable runtime/terminal record |
| `cardinality` | yes | planned demand, never actual count |
| `steps` | no | internal procedure annotations; no Run allocation or independent routing |
| `cells` | when a Plugin roster is declared | one Cell per member Workspace; Skills and surface behavior bind here |

`run_specs` is the only workflow row roster. Do not add `phases:` or treat a
Step, Version, or actual Run Instance as a row. Low-level engine progress
groups may be generated separately. The Workflow references the Plugin-owned
Workspace roster; it does not create or rename Workspaces.

## Internal procedure annotations and projections

`run_specs[].steps` may document `label`, `section`, `required`, `prompt`,
`files_in`, and `files_out`. A section groups Steps; it is not a Workflow unit.
`runs[].steps` may record observed status and evidence for these same labels.
Steps have no Run ids, Cells, cardinality, or independent routes.
A script plan projection contains only `plan`, `run_spec_ids`, and `steps`;
a script report projection contains only `report`, `run_ids`, and `steps`.
Both reference the authoritative Task plan/report and cannot allocate Runs.
Resolve the Run catalogue key and all Plugin Workspace Cells before execution;
Angle-bracket values in templates require resolution.
A standalone definition may omit `plugin` and `cells` when it declares no
Workspace surfaces. An explicitly declared but unresolved Plugin roster is a
blocked definition. Missing catalogue data also blocks the definition; neither
case permits inventing Workspaces or a run_type.
