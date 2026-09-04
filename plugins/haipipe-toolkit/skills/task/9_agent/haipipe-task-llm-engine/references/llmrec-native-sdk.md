# Physician LLMRec native-SDK contract

## Source-of-truth files

| Purpose | Path |
|---|---|
| Provider adapter and session isolation | `examples/Project-LLMRec-Physician/tasks/llmrec_agent_sdk.py` |
| A1 live search | `tasks/B03_llm_search/01_search_roster/01_search_roster.py` |
| A2 cards and same-session recommendation | `tasks/B04_llm_record_recommend/01_followup_recommend/01_followup_recommend.py` |
| B fresh search plus recommendation | `tasks/B01_llm_open_rec/02_run_audit/06_run_b_search_recommend.py` |
| Stage auditors (one per job, 260830) | `j01_A1_search_physicians/scripts/src/audit_a1_outputs.py` · `j02_A2_followup_from_A1_session/scripts/src/audit_a2_outputs.py` · `j03_B_open_recommendation/scripts/src/audit_b_outputs.py`; shared checks in `code/haiutils/agent_sdk/audit.py` |
| Deterministic verifier | `tasks/verify_llmrec_agent_sdk.py` |
| Per-job batch runner | `jNN_*/sbatch/run_all_arms.sh <scale>` (the cross-job chain scripts were retired with j05 on 260830; order is held by `required_audits` receipts) |

All `tasks/...` paths above are relative to
`examples/Project-LLMRec-Physician/` unless otherwise stated.

## Protocol

```text
A1: patient search request
    fresh session + live web → broad physician roster
                         │
                         ├── immutable minimal provenance card
                         │
A2: patient recommendation follow-up
    exact A1 session + no tools → ranked physicians, target seven

B: combined search and recommendation
   different fresh session + live web → ranked physicians, target seven
```

The A1 card is a pointer with identity and hashes. It must not duplicate the raw
prompt, response, or tool trace. A2 resumes the SDK rollout; it does not receive
a pasted copy of A1 as a replacement for session memory.

## Storage

```text
_WorkSpace/A-LLMRecPhy/4-LLMCallStore/
├── sdk_homes/<provider>/<model>/<campaign>/
│   ├── isolated OAuth seed and provider config
│   └── persisted provider rollouts
└── v2026-08/<scale>/
    ├── a-search/<provider-model>/<run>/
    ├── a-record/<provider-model>/<run>/
    ├── a-recommend/<provider-model>/<run>/
    └── b-search-recommend/<provider-model>/<run>/
```

Receipts live at:

```text
_WorkSpace/A-LLMRecPhy/4-LLMCallStore/v2026-08/audits/
  <scale>/<provider-model>/audit_receipt_v5.json
```

## Provider behavior

| Provider | Package | Live-web mapping | No-tool mapping |
|---|---|---|---|
| Claude | `claude-agent-sdk` | expose only `WebSearch`, `WebFetch` | expose no tools and disallow web tools |
| Codex | `openai-codex` | `web_search="live"` | `web_search="disabled"` |
| DeepSeek | `claude-agent-sdk` via `https://api.deepseek.com/anthropic` | expose only `WebSearch`, `WebFetch` | expose no tools and disallow web tools |

For Codex, deny approvals, use a read-only sandbox, and explicitly disable shell,
unified execution, memories, apps, plugins, multi-agent, browser, computer use,
and image generation. For Claude and DeepSeek, set
`permission_mode="dontAsk"`, clear setting sources, skills, and plugins, and
expose only the protocol's allowed tools. DeepSeek requires
`DEEPSEEK_API_KEY`; translate it to the Anthropic-compatible child environment
for the call only, and never copy it into the isolated SDK home or artifacts.

## Adding a model

1. Use the exact provider model id in configs, campaign SDK home, output path,
   manifest, and receipt.
2. Create isolated smoke1 A1/A2/B configs.
3. Run the smoke1 model gate.
4. Verify actual resolved model, required web events, A2 no-tool trace, fresh B
   session, persisted rollout, and target-seven ranking.
5. Issue a passing smoke1 receipt before generating larger-scale configs.

## Recovery

- Existing artifacts are immutable and resumable by identity and hash.
- An `inflight` or `needs_recovery` journal means the provider might already have
  accepted the call. Inspect the provider rollout before any manual repair.
- Do not delete or rewrite artifacts to force a rerun.
- A retry is allowed automatically only for explicit transient provider errors;
  never switch transport or model silently.
