"""
LLM Engine -- unified LLM call runtime with OAuth-first transport selection.

Transports:
  claude_sdk    OAuth via ~/.claude (free under subscription)
  claude_api    ANTHROPIC_API_KEY (metered)
  codex_oauth   OAuth via ~/.codex/auth.json (free under ChatGPT subscription)

Usage:
  from llm_engine import llm_call, batch_call, LLMResult

  result = await llm_call(
      system_prompt="You are helpful.",
      user_message="Hello",
      model="haiku",
  )
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .types import LLMResult, Usage
from .router import resolve_transport
from .batch import batch_call, write_call_artifacts


def _find_workspace_root(start: Path | None = None) -> Path | None:
    p = start or Path.cwd()
    for _ in range(10):
        if (p / "_WorkSpace").exists():
            return p
        p = p.parent
    return None


def get_default_store_paths(workspace_root: Path | None = None) -> tuple[Path, Path]:
    root = workspace_root or _find_workspace_root()
    if root is None:
        raise FileNotFoundError("Cannot find _WorkSpace/ in parent directories")
    store = root / "_WorkSpace" / "LLMCallStore"
    sdk_dir = store / ".sdk_sessions"
    sdk_dir.mkdir(parents=True, exist_ok=True)
    return store, sdk_dir


async def llm_call(
    system_prompt: str,
    user_message: str,
    model: str = "haiku",
    transport: str = "auto",
    store_path: Path | str | None = None,
    sdk_session_dir: Path | str | None = None,
    **kwargs: Any,
) -> LLMResult:
    """Make a single LLM call through the resolved transport.

    Args:
        system_prompt: system message
        user_message: user message
        model: model string (see router.py for conventions)
        transport: "auto" | "claude_sdk" | "claude_api" | "codex_oauth"
        store_path: if set, write input/response/meta.json here
        sdk_session_dir: where Claude SDK writes .jsonl sessions
        **kwargs: passed to the transport (e.g. max_tokens, timeout, api_key)
    """
    transport_name, resolved_model = resolve_transport(model, transport)

    if sdk_session_dir is None:
        try:
            _, sdk_session_dir = get_default_store_paths()
        except FileNotFoundError:
            sdk_session_dir = "/tmp"

    if transport_name == "claude_sdk":
        from .transports.claude_sdk import call
        result = await call(system_prompt, user_message, resolved_model,
                            sdk_session_dir=sdk_session_dir)
    elif transport_name == "claude_api":
        from .transports.claude_api import call
        result = await call(system_prompt, user_message, resolved_model, **kwargs)
    elif transport_name == "codex_oauth":
        from .transports.codex_oauth import call
        result = await call(system_prompt, user_message, resolved_model)
    else:
        result = LLMResult(
            transport=transport_name, model=resolved_model,
            is_error=True, error=f"Unknown transport: {transport_name}",
        )

    if store_path:
        write_call_artifacts(
            Path(store_path),
            input_data={
                "system_prompt": system_prompt,
                "user_message": user_message,
                "model": resolved_model,
                "transport": transport_name,
            },
            result=result,
        )

    return result


def llm_call_sync(
    system_prompt: str,
    user_message: str,
    **kwargs: Any,
) -> LLMResult:
    """Sync wrapper around llm_call for simple scripts."""
    import asyncio
    return asyncio.run(llm_call(system_prompt, user_message, **kwargs))


__all__ = [
    "llm_call",
    "llm_call_sync",
    "batch_call",
    "write_call_artifacts",
    "get_default_store_paths",
    "resolve_transport",
    "LLMResult",
    "Usage",
]
