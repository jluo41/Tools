# plan.yaml · Workflow Run Spec graph

## Definition schema

```yaml
name: build-lbp-data-pipeline
purpose: build, validate, and review one bounded data artifact
owner: haipipe-task-for-data

input:
  args: {name: run_lbp, group: A01_pretraining}
  files_in: [ref/source_fn_template.py]

run_specs:
  - id: author
    run_type: authoring.write-file
    purpose: create the requested bounded artifact
    target: tasks/A01_pretraining/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-for-data}
    action: author-file
    input: [ref/source_fn_template.py]
    depends_on: []
    entry_gate: {mode: automatic, assertion: required inputs resolve}
    exit_gate: {mode: automatic, assertion: file exists and syntax check passes}
    routes: {pass: review, fail: HOLD}
    result:
      payload: {status: ok, file_path: tasks/A01_pretraining/build_lbp.py}
      receipt: results/author/runtime.yaml
    cardinality: 1
    skill_bindings: [haipipe-task-for-data]
    workspace_bindings: [create, runtime]

  - id: review
    run_type: evaluation.validate
    purpose: independently review the authored artifact
    target: tasks/A01_pretraining/build_lbp.py
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
    skill_bindings: [haipipe-task-reviewer-agent]
    workspace_bindings: [review, runtime]

entry: [author]
terminal: [CLOSE, HOLD]

output:
  returns: [status, artifacts, verdict, receipts]
  files_out: [tasks/A01_pretraining/build_lbp.py]
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
    target: tasks/A01_pretraining/build_lbp.py
    actor: {mode: agent, owner: haipipe-task-for-data}
    status: complete
    gate_outcome: pass
    route_taken: review
    result: results/author/result.yaml
    receipt: results/author/runtime.yaml
  - run_id: r02_review
    run_spec_id: review
    run_type: evaluation.validate
    target: tasks/A01_pretraining/build_lbp.py
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
  files_created: [tasks/A01_pretraining/build_lbp.py]
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
| skill/workspace bindings | yes | execution and presentation bindings |

`run_specs` is the only workflow row roster. Do not add `phases:` or treat a
Step as a row. Low-level engine progress groups may be generated separately.
