"""Official openai-codex SDK transport with an isolated OAuth home."""

from __future__ import annotations

import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any

from ..types import LLMResult, Usage


_SAFE_ENV_KEYS = {"HOME", "LANG", "LC_ALL", "LC_CTYPE", "NO_PROXY", "PATH", "TMPDIR", "TZ"}
_SECRET_NAME = re.compile(r"(KEY$|TOKEN$|SECRET$|PASSWORD$|CREDENTIAL|SERP|BRAVE|ANTHROPIC_API)", re.I)


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", by_alias=True)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return repr(value)


def _prepare_home(path: Path) -> dict[str, str]:
    path.mkdir(parents=True, exist_ok=True)
    (path / "sqlite").mkdir(exist_ok=True)
    source = Path.home() / ".codex/auth.json"
    destination = path / "auth.json"
    if not source.is_file():
        raise RuntimeError(f"Codex OAuth credential is missing: {source}")
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    shutil.copy2(source, temporary)
    temporary.chmod(0o600)
    os.replace(temporary, destination)
    environment = {key: value for key, value in os.environ.items() if key in _SAFE_ENV_KEYS}
    environment.update({key: "" for key in os.environ if _SECRET_NAME.search(key)})
    environment["CODEX_HOME"] = str(path)
    environment["CODEX_SQLITE_HOME"] = str(path / "sqlite")
    return environment


async def call(
    system_prompt: str,
    user_message: str,
    model: str = "gpt-5.6-luna",
    sdk_session_dir: Path | str | None = None,
) -> LLMResult:
    from openai_codex import ApprovalMode, Codex, CodexConfig, Sandbox

    sdk_home = Path(sdk_session_dir or "/tmp/haipipe-openai-codex").resolve()
    started = time.monotonic()
    try:
        environment = _prepare_home(sdk_home)
        config = CodexConfig(cwd=str(sdk_home), env=environment)
        with Codex(config) as codex:
            thread = codex.thread_start(
                approval_mode=ApprovalMode.deny_all,
                base_instructions=system_prompt,
                config={
                    "project_doc_max_bytes": 0,
                    "project_doc_fallback_filenames": [],
                    "web_search": "disabled",
                    "features": {
                        "shell_tool": False,
                        "unified_exec": False,
                        "memories": False,
                        "apps": False,
                        "plugins": False,
                        "multi_agent": False,
                        "browser_use": False,
                        "computer_use": False,
                        "image_generation": False,
                    },
                },
                cwd=str(sdk_home),
                ephemeral=False,
                model=model,
                sandbox=Sandbox.read_only,
            )
            response = thread.run(user_message, sandbox=Sandbox.read_only)
    except Exception as error:
        return LLMResult(
            transport="openai_codex_sdk",
            model=model,
            wall_time_s=round(time.monotonic() - started, 2),
            is_error=True,
            error=f"{type(error).__name__}: {error}",
            ts=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    usage_value = _jsonable(response.usage) or {}
    if not isinstance(usage_value, dict):
        usage_value = {}
    total_usage = usage_value.get("total", usage_value)
    if not isinstance(total_usage, dict):
        total_usage = {}
    input_tokens = int(
        total_usage.get("inputTokens", total_usage.get("input_tokens", 0)) or 0
    )
    output_tokens = int(
        total_usage.get("outputTokens", total_usage.get("output_tokens", 0)) or 0
    )
    text = response.final_response or ""
    return LLMResult(
        text=text,
        model=model,
        transport="openai_codex_sdk",
        usage=Usage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        ),
        meta={
            "session_id": thread.id,
            "turn_id": response.id,
            "status": _jsonable(response.status),
            "raw_usage": usage_value,
            "items": [_jsonable(item) for item in response.items],
        },
        wall_time_s=round(time.monotonic() - started, 2),
        is_error=not bool(text.strip()),
        error=json.dumps(_jsonable(response.error), sort_keys=True) if response.error else None,
        ts=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
