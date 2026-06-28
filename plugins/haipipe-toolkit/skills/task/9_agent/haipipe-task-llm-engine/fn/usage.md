---
name: haipipe-task-llm-engine-usage
description: "How to wire the LLM engine into a task .py script"
---

# Wiring the LLM engine into a task script

## Before code/haiutils/llm_engine/ exists (current state)

Copy the transport functions from the proof-of-concept:
```
examples/ProjC-LLMRecPhysicain/tasks/B01_llm_open_rec/00_llm_engine_test/00_llm_engine_test.py
```

Key patterns to follow:

### 1. Workspace root detection
```python
WORKSPACE_ROOT = Path(__file__).parent
for _ in range(10):
    if (WORKSPACE_ROOT / "_WorkSpace").exists():
        break
    WORKSPACE_ROOT = WORKSPACE_ROOT.parent

LLMCALL_STORE = WORKSPACE_ROOT / "_WorkSpace" / "LLMCallStore"
SDK_SESSION_DIR = LLMCALL_STORE / ".sdk_sessions"
```

### 2. Call store path convention
```
_WorkSpace/LLMCallStore/<project>/<task_group>/<task>/<run>/<transport>/
    input.json, response.json, meta.json
```

### 3. Write artifacts for every call
```python
def _write_call_artifacts(call_dir, input_data, response_data, meta):
    call_dir.mkdir(parents=True, exist_ok=True)
    (call_dir / "input.json").write_text(json.dumps(input_data, indent=2, default=str))
    (call_dir / "response.json").write_text(json.dumps(response_data, indent=2, default=str))
    (call_dir / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
```

### 4. Task results/ holds only summaries
The raw per-call data lives in LLMCallStore. Task `results/<run>/` holds only
aggregated outputs (summary.json, tables, scores).

## After code/haiutils/llm_engine/ exists (future state)

```python
from haiutils.llm_engine import llm_call, LLMResult

result = await llm_call(
    system_prompt=system_prompt,
    user_message=user_message,
    model="opus",
    store_path=CALL_STORE / case_id,
)
# result.text, result.meta, result.cost_usd, result.transport
```

The engine handles transport selection, auth, artifact writing, and SDK session
isolation internally. Task scripts just call `llm_call()`.
