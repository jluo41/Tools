# Lesson 14: Agent Workspace on Databricks — Use claude-agent-sdk

## The Problem

Running AI agent workspaces on Databricks — where an agent can execute haipipe-toolkit skills autonomously (e.g., `/haipipe-application`, `/haipipe-task`, `/dikw`) — seems to require installing Claude Code CLI + Node.js on the cluster, which is heavy and fragile.

## The Fix

Use `claude-agent-sdk` (the Python package). It bundles a native Claude Code binary — no Node.js, no CLI install needed. Just `pip install`.

```python
%pip install claude-agent-sdk

import os
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("scope", "anthropic-key")

from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio

async def run_skill(prompt: str, cwd: str = "/Workspace/REACH-SPACE"):
    options = ClaudeAgentOptions(
        cwd=cwd,
        allowed_tools=["Bash", "Read", "Write", "Edit", "Skill", "Agent"],
        permission_mode="acceptEdits",
    )
    results = []
    async for msg in query(prompt=prompt, options=options):
        if hasattr(msg, "result"):
            results.append(msg.result)
    return "\n".join(results)

# Example: run a haipipe skill
result = asyncio.run(run_skill("/haipipe-task execute examples/REACH_ADHD/tasks/A01_data/01_source/"))
```

## Why This Works

```
claude-agent-sdk architecture:

  Your Python code
    → spawns bundled native binary (not Node.js)
      → calls api.anthropic.com over HTTPS

  The binary IS Claude Code — it understands .claude/skills/
  No separate Claude Code CLI or Node.js installation needed
```

The old `claude-code-sdk` package required Node.js (`spawn node → cli.js`). The new `claude-agent-sdk` ships pre-compiled platform binaries (Linux x86-64, macOS, Windows) via `pip install`.

## Skill Maturity Model

Skills should reach "auto-pilot" level before deploying on Databricks:

```
Stage 1: INIT       — human types /haipipe-task, answers every ASK step
Stage 2: CO-PILOT   — human answers ≤3 questions, rest is auto
Stage 3: AUTO-PILOT — claude -p "/haipipe-task ..." runs zero-interaction
                      ← deploy to Databricks at this stage
```

Once a skill runs in `claude -p` headless mode, wrapping it with `claude-agent-sdk` on Databricks is trivial.

## Per-Patient Agent Pattern

```python
async def analyze_patient(patient_id: str):
    return await run_skill(
        f"/haipipe-application analyze patient {patient_id}",
        cwd="/Workspace/REACH-SPACE"
    )

# Batch
patient_ids = ["P001", "P002", "P003"]
tasks = [analyze_patient(pid) for pid in patient_ids]
results = await asyncio.gather(*tasks)
```

## Databricks Setup Checklist

| Step | How |
|------|-----|
| Repo on Databricks | Databricks Repos sync or `git clone` to `/Workspace/` |
| Install SDK | `%pip install claude-agent-sdk` or cluster Libraries |
| API key | `dbutils.secrets.get("scope", "anthropic-key")` |
| Python env | `pip install -e .` for haipipe in init script or Libraries |
| Data access | `_WorkSpace/` via Volumes or DBFS mount |

## Things to Verify

- Native binary runs on Databricks Runtime Linux (expected: yes, standard x86-64)
- Skill Bash commands work in cluster environment (may need tweaks)
- File paths: Databricks Repos uses `/Workspace/`, not `/home/`
- Network: `api.anthropic.com` reachable from cluster (check firewall)
- Alternative auth: supports Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`) and Vertex (`CLAUDE_CODE_USE_VERTEX=1`)

## Key Distinction

| Package | Node.js needed? | Status |
|---------|----------------|--------|
| `claude-code-sdk` (old) | Yes — spawned `node cli.js` | Deprecated |
| `claude-agent-sdk` (current) | **No** — native binary bundled | Active |

## When This Applies

- Building per-patient agent workspaces on Databricks
- Running haipipe-toolkit skills in batch/automated mode
- Any scenario where Claude Code skills need to run on cloud infrastructure

## Source

REACH-SPACE architecture discussion, 2026-06-27. Researched Claude Agent SDK, Databricks Sandbox, MCP, and agent workspace patterns.
