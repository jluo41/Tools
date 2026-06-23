fn-execute: Execute a data-pipeline task-folder
==================================================

Stage-aware execution of an existing data-pipeline task. Detects the
pipeline stage from the script, reads partition config, and runs via
notebook (papermill) or CLI.


Step 1 — Detect stage from script
-----------------------------------

Read the task `.py` and infer stage from imports:

```
from haipipe.source_base import Source_Pipeline   → Stage 1 (Source)
from haipipe.record_base import Record_Pipeline   → Stage 2 (Record)
from haipipe.case_base import Case_Pipeline       → Stage 3 (Case)
from haipipe.aidata_base import AIData_Pipeline   → Stage 4 (AIData)
```


Step 2 — Read config for partition parameters
-----------------------------------------------

```yaml
# Stage 2 config example:
RecordArgs:
  partition_number: 20       # → NUM_PARTITIONS=20
  use_cache: true

# Stage 3 config example:
CaseArgs:
  # partition_number not needed — auto-discovers from RecordSet partitions
  use_cache: false
```


Step 3 — Execute
-----------------

Two execution paths. Notebook is the default; CLI is available for
parallel workers or scripted pipelines.

### Path A: Notebook (papermill) — via run.sh

```bash
bash runs/<RUN>.sh
```

This:
1. Converts `{TASK_NAME}.py` → `{TASK_NAME}.ipynb` (template)
2. Runs `papermill {template} notebooks/<RUN>.ipynb -p CONFIG {config}`
3. Writes `results/<RUN>/runtime.yaml`

The `.py` already has `NUM_PARTITIONS` and `PARTITION_INDEX` in its
parameters cell. papermill can override them:
```bash
papermill ... -p NUM_PARTITIONS 20 -p PARTITION_INDEX 5
```

### Path B: CLI (direct) — for parallel workers

```bash
# Stage 1 — no partitions
python -m scripts.haistep.source --config <config>

# Stage 2 — partition by patients
python -m scripts.haistep.record --config <config> --num-partitions 20 --use-cache

# Stage 3 — auto-discover + parallel
python -m scripts.haistep.case --config <config> --num-partitions 0 --num-workers 4 --use-cache

# Stage 4 — auto-discover CaseSet partitions
python -m scripts.haistep.aidata --config <config>

# Retry a single failed partition:
python -m scripts.haistep.record --config <config> --num-partitions 20 --partition-index 5
python -m scripts.haistep.case --config <config> --num-partitions 0 --partition-index 5
```


Step 4 — Per-stage notes
--------------------------

### Stage 1 (Source)
- No partitions. Single run.
- Output: `_WorkSpace/1-SourceStore/{raw_data_name}/@{SourceFnName}/`

### Stage 2 (Record)
- Partitions by patients. Each partition loads only its patient slice
  via Ptt.parquet + pyarrow predicate pushdown.
- Memory: ~30 GB per partition for MIMIC-IV scale (vs 120 GB+ full load).
- Sequential recommended (each partition loads SourceSet, I/O heavy).
- Output: `_WorkSpace/2-RecStore/{name}_v{N}RecSet/@i{i}n{n}/`

### Stage 3 (Case)
- Follows RecordSet partitions. Each partition is independent.
- **Embarrassingly parallel** — use `--num-workers 4` for 4x speedup.
- Memory per worker: ~100 MB (RecordSet partitions are small).
- Output: `_WorkSpace/3-CaseStore/{RecSet}/@i{i}n{n}/@v{ver}CaseSet-{Trigger}/`

### Stage 4 (AIData)
- Merges all CaseSet partitions into one AIDataSet.
- Auto-discovers partitions via `record_set_name` + `CaseArgs` in config.
- Streaming HF Dataset conversion (memory-efficient).
- Output: `_WorkSpace/4-AIDataStore/{name}/@{version}/`


Step 5 — Write runtime.yaml
------------------------------

If running via CLI (not run.sh), manually write:
```
results/<RUN>/runtime.yaml
```
with status, started, ended, duration, cmd, config, partitions.


Step 6 — Report
-----------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was executed
artifacts: [_WorkSpace paths written, results/<RUN>/runtime.yaml]
next:      suggested next stage or /haipipe-data-{stage} review
```


Cross-references
-----------------

- CLI scripts: `code/scripts/haistepcli/{source,record,case,aidata}.py`
- Notebook templates: `code/scripts/haistepnb/{a1,a2,a3,a4}_{stage}_nb.py`
- Pipeline skills: `/haipipe-data-{source,record,case,aidata}`
