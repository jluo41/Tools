# Transport Reference

## Claude Agent SDK (claude_sdk)

Auth: reads OAuth token from `~/.claude/` (written by `claude login`).

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock, ResultMessage

options = ClaudeAgentOptions(
    cwd=str(sdk_session_dir),       # isolate .jsonl from user sessions
    allowed_tools=[],               # no tool use
    permission_mode="acceptEdits",
    max_turns=1,                    # single-shot
    model="haiku",                  # or "sonnet", "opus"
    system_prompt=system_prompt,
)

async with ClaudeSDKClient(options=options) as client:
    await client.query(user_message)
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    response_text = block.text
        elif isinstance(message, ResultMessage):
            meta = asdict(message)  # cost_usd, usage, session_id, etc.
```

Gotchas:
- `cwd` determines where SDK writes session .jsonl -- point to LLMCallStore/.sdk_sessions/
- `allowed_tools=[]` prevents tool-use attempts
- `cost_usd` in ResultMessage is the API-equivalent cost, not actual charge under OAuth

## Claude API (claude_api)

Auth: `ANTHROPIC_API_KEY` env var (sk-ant-api...).

```python
import anthropic

client = anthropic.Anthropic(api_key=api_key)
resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8192,
    system=system_prompt,
    messages=[{"role": "user", "content": user_message}],
    timeout=300,
)
text = "".join(b.text for b in resp.content if b.type == "text")
```

This is the metered path -- every token is billed.

## Codex OAuth (codex_oauth)

Auth: reads `~/.codex/auth.json` (written by `codex login`).
Package: `pip install -e <path-to-codex_oauth-clone>` (not on PyPI).
Source: https://github.com/zeron-G/codex_oauth

```python
from codex_oauth import CodexOAuthClient

async with CodexOAuthClient(model="gpt-5.5") as client:
    response = await client.complete(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    text = response.content
    usage = response.usage  # .input_tokens, .output_tokens, .total_tokens
```

Auth waterfall inside codex_oauth:
1. `CODEX_OAUTH_ACCESS_TOKEN` env var
2. `CODEX_OAUTH_AUTH_JSON` env var -> custom path
3. `~/.codex/auth.json` (default)

Supported models: only `gpt-5.5` works via ChatGPT backend.
gpt-4.1-mini, o4-mini, codex-mini all rejected with 400 error.

Auto JWT refresh: on 401 the client refreshes the token via auth.openai.com/oauth/token and persists the new token back to auth.json.
