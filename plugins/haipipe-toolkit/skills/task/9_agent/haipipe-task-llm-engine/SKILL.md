---
name: haipipe-task-llm-engine
description: Inspect, maintain, and run Physician-SPACE native LLM Agent SDK runtimes. Use for LLM engine status, Claude, Codex, or DeepSeek calls, OAuth/API-key model routing, LLMRec A1/A2/B search-and-recommend campaigns, SDK-session isolation, CallStore recovery, adding models or scales, and validating LLM task folders. Route existing LLMRec work to its project adapter; deploy the generic engine only when explicitly requested.
---

# LLM engine task specialist

Use provider-native SDKs and preserve auditable session evidence. Inspect before
changing anything; a status or explanation request is read-only.

## Route to the correct runtime

| Context | Runtime | Rule |
|---|---|---|
| Physician LLMRec | `examples/Project-LLMRec-Physician/tasks/llmrec_agent_sdk.py` | This is the active experiment runtime. Never replace it with `ref/engine/`. |
| Generic agent task | `code/haiutils/llm_engine/` | Maintain only when that package exists or the user explicitly asks to create it. |
| Generic reference | `ref/engine/` | Template for generic tasks, not an LLMRec protocol implementation. |

For LLMRec details, read [references/llmrec-native-sdk.md](references/llmrec-native-sdk.md).

## Status workflow

1. Run `scripts/status.py --root <repository-root>`.
2. Identify the active runtime and installed SDK versions.
3. Inspect configs and immutable audit receipts for actual model support; do not
   infer account access from aliases or documentation alone.
4. Report status without creating packages, changing credentials, starting
   calls, or modifying queues unless the user requested those actions.

## LLMRec invariants

- Use `claude-agent-sdk` for Claude and DeepSeek's official
  Anthropic-compatible route; use official `openai-codex` for Codex.
- Never fall back to a provider CLI or API-key route inside an SDK campaign.
- Give every provider/model/protocol campaign a separate SDK home and output
  directory. Seed OAuth credentials into that home with mode `0600` for OAuth
  providers. For DeepSeek, inject only the required Anthropic-compatible child
  environment from `DEEPSEEK_API_KEY`; never persist the key in the SDK home.
  Never expose `env.sh` or unrelated research secrets to the child runtime.
- Run from a neutral working directory outside the repository. Disable shell,
  file, memory, plugin, app, browser, computer-use, and multi-agent tools.
- A1 requires live web search. A2 resumes exactly the matching A1 session with
  every tool disabled. B starts a fresh session and requires live web search.
- Preserve raw SDK events, tool traces, model identity, usage, rollout path,
  session id, prompts, and immutable manifests.
- Treat `turn_journals/status=needs_recovery` as a manual recovery gate. Never
  delete a journal or make an automatic duplicate provider call.
- Call a scale complete only when its `audit_receipt_v5.json` verdict is `pass`.

## Current validated model arms

Treat this list as project evidence dated 2026-08-17, not a permanent provider
guarantee:

- Claude: `claude-sonnet-5`, `claude-haiku-4-5-20251001`, `claude-opus-5`
- Codex: `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`
- DeepSeek: `deepseek-v4-pro`, `deepseek-v4-flash`

Before adding a model to a fold, run the isolated smoke1 A1 → cards → A2 → B
gate and issue its receipt. Never use an alias such as `opus` when experimental
identity requires an exact model id.

## Commands

From the repository root:

```bash
# Read-only engine status
.venv/bin/python .codex/skills/haipipe-task-llm-engine/scripts/status.py --root .

# Deterministic LLMRec contract validation; no provider call
.venv/bin/python examples/Project-LLMRec-Physician/tasks/verify_llmrec_agent_sdk.py

# Isolated DeepSeek smoke1 gates (A1 -> cards -> A2 -> independent B -> receipt)
examples/Project-LLMRec-Physician/tasks/run_llmrec_model_smoke1.sh \
  <deepseek_v4_pro|deepseek_v4_flash>

# One configured model/scale cell
examples/Project-LLMRec-Physician/tasks/run_llmrec_model_scale.sh \
  <claude_sonnet|claude_haiku|claude_opus|codex_luna|codex_terra|codex_sol> \
  <smoke50|fold00|fold01>
```

Run a provider call only when the user asked to execute or continue a campaign.
Prefer durable, sequential provider queues over launching many concurrent agents.

## Generic engine maintenance

If the request is specifically about a generic agent task:

1. Check whether `code/haiutils/llm_engine/` exists.
2. If absent, report that fact. Create it from `ref/engine/` only when explicitly
   asked to build or deploy the generic runtime.
3. If present, compare structure and behavior with `ref/engine/`; preserve local
   extensions and update only the stale pieces in scope.
4. Validate imports and router behavior without making a provider call. Run a
   live smoke only when requested.

The generic engine offers one-shot `llm_call`/`batch_call`; it does not implement
LLMRec's A1/A2 session protocol or receipt auditor.
