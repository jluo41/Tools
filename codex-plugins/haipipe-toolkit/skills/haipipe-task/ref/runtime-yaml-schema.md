runtime.yaml — Schema
======================

Location: `results/<NAME>/runtime.yaml`
Owner:    Written by `runs/<NAME>.sh` (auto). NEVER edit by hand.
Status:   Source-of-truth for post-run machine facts about ONE run.


Fields (10 fixed, in this order)
---------------------------------

| Field      | Type     | When written | Source                          |
|------------|----------|--------------|---------------------------------|
| status     | enum     | start + end  | `running` \| `ok` \| `failed` \| `aborted` |
| started    | ISO 8601 | start        | `date -Iseconds` at launch      |
| ended      | ISO 8601 | end          | `date -Iseconds` at finalize    |
| duration   | string   | end          | derived from started/ended      |
| git_sha    | string   | start        | `git rev-parse --short HEAD`    |
| host       | string   | start        | `hostname/whoami`               |
| exit_code  | int      | end          | `$?` after script exits         |
| cmd        | string   | start        | the actual command line         |
| config     | path     | start        | `configs/<NAME>.yaml`           |
| notebook   | path     | start        | `notebooks/<NAME>.ipynb`        |
| headline   | string   | end (opt)    | best-effort from `metrics.json` |


Lifecycle
---------

```
Step 1 (run.sh launches):
  write runtime.yaml.tmp with status=running + start fields
  atomic mv runtime.yaml.tmp -> runtime.yaml

Step 2 (run.sh finalizes):
  write runtime.yaml.tmp with status=ok|failed + all fields
  atomic mv runtime.yaml.tmp -> runtime.yaml

On crash / Ctrl-C:
  runtime.yaml stays in status=running state
  /log task can scan for these to detect abandoned runs
```


Example — running state
-----------------------

```yaml
status:     running
started:    2026-05-24T14:30:01-04:00
git_sha:    e2d67d63
host:       aikong/jluo41
cmd:        bash runs/run_seed42_baseline.sh
config:     configs/run_seed42_baseline.yaml
notebook:   notebooks/run_seed42_baseline.ipynb
```

Example — finalized (ok)
-------------------------

```yaml
status:     ok
started:    2026-05-24T14:30:01-04:00
ended:      2026-05-24T14:59:33-04:00
duration:   29m32s
git_sha:    e2d67d63
host:       aikong/jluo41
exit_code:  0
cmd:        bash runs/run_seed42_baseline.sh
config:     configs/run_seed42_baseline.yaml
notebook:   notebooks/run_seed42_baseline.ipynb
headline:   MAE 24.7
```

Example — finalized (failed)
-----------------------------

```yaml
status:     failed
started:    2026-05-24T15:10:00-04:00
ended:      2026-05-24T15:40:11-04:00
duration:   30m11s
git_sha:    e2d67d63
host:       aikong/jluo41
exit_code:  137
cmd:        bash runs/run_seed42_baseline_v2.sh
config:     configs/run_seed42_baseline_v2.yaml
notebook:   notebooks/run_seed42_baseline_v2.ipynb
headline:   -
```


Headline extraction
-------------------

`headline` is best-effort. run.sh tries to extract a one-line metric from
`results/<NAME>/metrics.json` (priority order):

1. `summary.headline` if explicitly set by the script
2. `summary.best_val` / `summary.best_test_id` / etc. (first match)
3. The largest metric value in `metrics.json`
4. fallback: `-`

The headline does NOT replace metrics.json — it's a scannable shortcut.


Atomicity
---------

Always write to `runtime.yaml.tmp` then `mv` (POSIX atomic). This prevents
half-written YAML if the process is killed mid-write. Readers see either the
old content or the new content, never a partial blend.
