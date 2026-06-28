---
name: haipipe-task-llm-engine
description: "Owns code/haiutils/llm_engine/ -- the unified LLM call runtime for agent task-folders. Two OAuth transports (Claude Agent SDK + Codex OAuth) with API-key fallback. On trigger: CHECK the deployed code exists, CREATE it from ref/engine/ if missing, EVALUATE it if present, UPDATE if stale."
trigger: llm engine, llm call, llm transport, oauth engine, call claude, call codex, engine test, engine status
---

# haipipe-task-llm-engine

Skill that **owns and maintains** the LLM engine at `code/haiutils/llm_engine/`.

The engine is a Python package that any agent task `.py` script imports to make LLM calls. This skill carries the reference implementation in `ref/engine/` and manages the deployed copy.

## What the engine provides

```python
from haiutils.llm_engine import llm_call, batch_call, LLMResult

result = await llm_call(
    system_prompt = "...",
    user_message  = "...",
    model         = "opus",           # or "codex/gpt-5.5"
    transport     = "auto",           # sdk | api | codex_oauth | auto
)
result.text        # str
result.meta        # dict (full provider telemetry)
result.cost_usd    # float (equivalent cost, $0 under OAuth subscription)
result.transport   # "claude_sdk" | "claude_api" | "codex_oauth"
```

## Transports

```
Transport       Auth source              Billing            Package
──────────────  ───────────────────────  ─────────────────  ────────────────
claude_sdk      ~/.claude OAuth          $0 (subscription)  claude_agent_sdk
claude_api      ANTHROPIC_API_KEY        $$$ (metered)      anthropic
codex_oauth     ~/.codex/auth.json       $0 (ChatGPT sub)   codex_oauth
```

## Model routing (transport="auto")

```
model string               transport
─────────────────────────  ─────────────────
"opus" / "sonnet" / "haiku"  claude_sdk (OAuth)
"claude-opus-4-7"            claude_sdk (OAuth)
"codex/gpt-5.5"              codex_oauth
"api:claude-opus-4-7"        claude_api (force API key)
```

## Data storage

All per-call artifacts go to `_WorkSpace/LLMCallStore/`:

```
_WorkSpace/LLMCallStore/
├── .sdk_sessions/                    SDK .jsonl (isolated from user sessions)
└── <project>/<group>/<task>/<run>/
    └── <case_id>/
        ├── input.json                prompt + context sent
        ├── response.json             raw model output
        └── meta.json                 transport, model, cost, timing
```

Task `results/` holds only aggregated outputs (summaries, tables), not raw per-call data.

## Claude SDK gotchas

- Set `cwd` to `_WorkSpace/LLMCallStore/.sdk_sessions/` so SDK session .jsonl files don't pollute the user's real session list
- Set `allowed_tools=[]` to prevent tool-use attempts
- System prompt should include "Do NOT use any tools" to avoid `stop_reason: tool_use`

## Codex OAuth notes

- Only `gpt-5.5` works via the ChatGPT backend; smaller models (gpt-4.1-mini, o4-mini) are rejected
- Package installed from github: `pip install -e /tmp/codex_oauth` (not on PyPI)
- Requires `httpx`; reads `~/.codex/auth.json` written by `codex login`

## Anthropic billing status (as of 2026-06-27)

Anthropic planned to meter Agent SDK usage starting June 15, 2026 (separate credit pool at API rates: Max=$100-200/mo). This change was PAUSED. OAuth is still free under subscription. The engine tracks `cost_usd` for when it flips.

## Commands

```
/haipipe-task-llm-engine              check status of deployed code
/haipipe-task-llm-engine create       create code/haiutils/llm_engine/ from ref/engine/
/haipipe-task-llm-engine update       update deployed code from ref/engine/
/haipipe-task-llm-engine evaluate     audit deployed code vs ref/ spec
/haipipe-task-llm-engine test         run the smoke test task
```

## On trigger

1. CHECK `code/haiutils/llm_engine/` exists
   - missing  -> CREATE from `ref/engine/`
   - exists   -> EVALUATE (compare against ref/, check imports, test auth)
   - stale    -> UPDATE (diff ref/ vs deployed, apply changes)
2. Return status + usage instructions

## Proof-of-concept

Working test at:
```
examples/ProjC-LLMRecPhysicain/tasks/B01_llm_open_rec/00_llm_engine_test/
```
Both transports PASS. Claude ~5s/call, Codex ~50s/call.
