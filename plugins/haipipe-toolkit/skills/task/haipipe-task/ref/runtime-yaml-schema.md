runtime.yaml — Schema
======================

Location: `$OUTPUT_ROOT/results/<NAME>/runtime.yaml` for a flat Job, or
`$OUTPUT_ROOT/results/<task>/<NAME>/runtime.yaml` for a canonical nested Task.
Owner: the Run scaffolder creates `status: planned`; the authored Ticket
updates the same receipt automatically from launch onward; never edit it by hand.
Status: source of truth for the lifecycle facts of one Run. The typed payload,
when the worker owns one, is a separate sibling such as `result.yaml`,
`values.yaml`, or `metrics.json`.


Required Run fields
-------------------

These base fields follow `haipipe-run` and never disappear:

| Field | Type | Rule |
|---|---|---|
| `run` | string | local immutable RUNNAME |
| `family` | string | declared Run family |
| `operation` | string | independently closable operation |
| `target` | string | bounded target |
| `status` | enum | `planned`, `running`, `complete`, `failed`, `blocked`, or `superseded` |
| `ticket` | path | authored Ticket path |
| `result` | path | paired Result directory under resolved `$OUTPUT_ROOT` |
| `inputs` | list | frozen authoritative paths and hashes |
| `worker` | mapping | worker kind and name |
| `started_at` | ISO 8601/null | written before expensive work |
| `finished_at` | ISO 8601/null | written at terminal state |
| `supersedes` | Run id/null | prior Run when this is a materially new contract |
| `failure` | string/null | truthful terminal reason |

A canonical Task receipt also records `address`, `git_sha`, `git_dirty`,
`host`, `config_file`, `config_sha256`, and `settings`. `settings` must
account for every value that varied for this Run; at minimum it records the
pinned configuration and Ticket arguments. `notebook`, `duration`,
`exit_code`, and `headline` are useful Task-dialect extensions.


Lifecycle and gate
------------------

```text
SCAFFOLD          write runtime.yaml.tmp with status: planned and null times
                  → atomic mv to runtime.yaml
LAUNCH            replace it atomically with status: running
EXECUTE           run the worker
VALIDATE          apply the Ticket's declared REQUIRED_RESULTS and any
                  worker-specific semantic checks
TERMINATE         complete only when the Result gate passes;
                  otherwise failed/blocked with failure
```

A zero process exit is necessary but not sufficient for `complete`. On crash
or interruption, the last `running` receipt remains so an auditor can identify
the abandoned attempt. Always write through `runtime.yaml.tmp` and atomically
rename it so readers never observe a partial receipt.


Example — running
-----------------

```yaml
run: r01_page-evidence-item_e01-display-effect
family: Page
operation: evidence-item
target: E01-DISPLAY-effect
status: running
ticket: t01_example/runs/r01_page-evidence-item_e01-display-effect.sh
result: results/t01_example/r01_page-evidence-item_e01-display-effect/
inputs:
  - path: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
    sha256: <64-hex>
worker:
  kind: script
  name: t01_example/scripts/render_effect.py
started_at: 2026-09-04T16:00:00-04:00
finished_at: null
supersedes: null
failure: null
address: b01j01t01r01
git_sha: e2d67d63
git_dirty: false
host: aikong/jluo41
config_file: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
config_sha256: <64-hex>
settings:
  config_file: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
  ticket_args: []
```


Example — complete
------------------

```yaml
run: r01_page-evidence-item_e01-display-effect
family: Page
operation: evidence-item
target: E01-DISPLAY-effect
status: complete
ticket: t01_example/runs/r01_page-evidence-item_e01-display-effect.sh
result: results/t01_example/r01_page-evidence-item_e01-display-effect/
inputs:
  - path: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
    sha256: <64-hex>
worker:
  kind: script
  name: t01_example/scripts/render_effect.py
started_at: 2026-09-04T16:00:00-04:00
finished_at: 2026-09-04T16:03:00-04:00
supersedes: null
failure: null
address: b01j01t01r01
git_sha: e2d67d63
git_dirty: false
host: aikong/jluo41
exit_code: 0
config_file: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
config_sha256: <64-hex>
settings:
  config_file: t01_example/scripts/config/r01_page-evidence-item_e01-display-effect.yaml
  ticket_args: []
duration: 3m00s
headline: effect figure rendered
```

`headline` is only a scannable shortcut. It never substitutes for the typed
Result or its acceptance checks.
