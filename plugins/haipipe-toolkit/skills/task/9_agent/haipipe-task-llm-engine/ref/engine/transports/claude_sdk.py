"""Claude Agent SDK transport (OAuth via ~/.claude)."""
from __future__ import annotations

import time
from dataclasses import asdict, is_dataclass
from pathlib import Path

from ..types import LLMResult, Usage


async def call(
    system_prompt: str,
    user_message: str,
    model: str,
    sdk_session_dir: Path | str | None = None,
) -> LLMResult:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    from claude_agent_sdk.types import AssistantMessage, TextBlock, ResultMessage

    cwd = str(sdk_session_dir) if sdk_session_dir else "/tmp"
    if sdk_session_dir:
        Path(sdk_session_dir).mkdir(parents=True, exist_ok=True)

    options = ClaudeAgentOptions(
        cwd=cwd,
        allowed_tools=[],
        permission_mode="acceptEdits",
        max_turns=1,
        model=model,
        system_prompt=system_prompt,
    )

    response_text = ""
    result_meta = None

    started = time.time()
    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_message)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text = block.text
            elif isinstance(message, ResultMessage):
                if is_dataclass(message):
                    result_meta = asdict(message)
                else:
                    result_meta = {
                        f: getattr(message, f, None)
                        for f in (
                            "subtype", "duration_ms", "duration_api_ms",
                            "is_error", "num_turns", "session_id",
                            "stop_reason", "total_cost_usd", "usage",
                            "model_usage",
                        )
                    }
    elapsed = time.time() - started
    rm = result_meta or {}

    model_usage = rm.get("model_usage") or {}
    first_model_usage = next(iter(model_usage.values()), {}) if model_usage else {}

    return LLMResult(
        text=response_text,
        model=model,
        transport="claude_sdk",
        cost_usd=rm.get("total_cost_usd"),
        usage=Usage(
            input_tokens=first_model_usage.get("inputTokens", 0),
            output_tokens=first_model_usage.get("outputTokens", 0),
            total_tokens=(
                first_model_usage.get("inputTokens", 0)
                + first_model_usage.get("outputTokens", 0)
            ),
        ),
        meta={
            "session_id": rm.get("session_id"),
            "stop_reason": rm.get("stop_reason"),
            "is_error": rm.get("is_error", False),
            "duration_ms": rm.get("duration_ms"),
            "model_usage": model_usage,
        },
        wall_time_s=round(elapsed, 2),
        is_error=not bool(response_text),
        ts=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
