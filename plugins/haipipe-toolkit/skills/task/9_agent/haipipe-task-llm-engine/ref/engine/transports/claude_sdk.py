"""Claude Agent SDK transport (OAuth via ~/.claude)."""
from __future__ import annotations

import os
import re
import shutil
import time
from dataclasses import asdict, is_dataclass
from pathlib import Path

from ..types import LLMResult, Usage


_SAFE_ENV_KEYS = {"HOME", "LANG", "LC_ALL", "LC_CTYPE", "NO_PROXY", "PATH", "TMPDIR", "TZ"}
_SECRET_NAME = re.compile(r"(KEY$|TOKEN$|SECRET$|PASSWORD$|CREDENTIAL|SERP|BRAVE|ANTHROPIC_API)", re.I)


def _prepare_home(path: Path) -> dict[str, str]:
    path.mkdir(parents=True, exist_ok=True)
    source = Path.home() / ".claude/.credentials.json"
    destination = path / ".credentials.json"
    if not source.is_file():
        raise RuntimeError(f"Claude OAuth credential is missing: {source}")
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    shutil.copy2(source, temporary)
    temporary.chmod(0o600)
    os.replace(temporary, destination)
    environment = {key: value for key, value in os.environ.items() if key in _SAFE_ENV_KEYS}
    environment.update({key: "" for key in os.environ if _SECRET_NAME.search(key)})
    environment["CLAUDE_CONFIG_DIR"] = str(path)
    return environment


async def call(
    system_prompt: str,
    user_message: str,
    model: str,
    sdk_session_dir: Path | str | None = None,
) -> LLMResult:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    from claude_agent_sdk.types import AssistantMessage, TextBlock, ResultMessage

    sdk_home = Path(sdk_session_dir or "/tmp/haipipe-claude-agent-home").resolve()
    environment = _prepare_home(sdk_home)
    cwd = Path("/private/tmp/haipipe-claude-agent").resolve()
    cwd.mkdir(parents=True, exist_ok=True)

    options = ClaudeAgentOptions(
        cwd=str(cwd),
        tools=[],
        allowed_tools=[],
        disallowed_tools=["WebSearch", "WebFetch"],
        permission_mode="dontAsk",
        max_turns=1,
        model=model,
        system_prompt=system_prompt,
        setting_sources=[],
        skills=[],
        plugins=[],
        env=environment,
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
                        response_text += block.text
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
