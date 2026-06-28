"""Claude API transport (ANTHROPIC_API_KEY, metered)."""
from __future__ import annotations

import os
import time

from ..types import LLMResult, Usage


async def call(
    system_prompt: str,
    user_message: str,
    model: str,
    max_tokens: int = 8192,
    timeout: int = 300,
    api_key: str | None = None,
) -> LLMResult:
    import anthropic

    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return LLMResult(
            transport="claude_api", model=model,
            is_error=True, error="ANTHROPIC_API_KEY not set",
            ts=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    client = anthropic.Anthropic(api_key=key)

    started = time.time()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
            timeout=timeout,
        )
    except Exception as e:
        return LLMResult(
            transport="claude_api", model=model,
            wall_time_s=round(time.time() - started, 2),
            is_error=True, error=f"{type(e).__name__}: {e}",
            ts=time.strftime("%Y-%m-%d %H:%M:%S"),
        )
    elapsed = time.time() - started

    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    usage_obj = getattr(resp, "usage", None)
    in_tok = getattr(usage_obj, "input_tokens", 0) if usage_obj else 0
    out_tok = getattr(usage_obj, "output_tokens", 0) if usage_obj else 0

    return LLMResult(
        text=text,
        model=getattr(resp, "model", model),
        transport="claude_api",
        usage=Usage(input_tokens=in_tok, output_tokens=out_tok, total_tokens=in_tok + out_tok),
        meta={
            "id": getattr(resp, "id", None),
            "stop_reason": getattr(resp, "stop_reason", None),
            "max_tokens": max_tokens,
        },
        wall_time_s=round(elapsed, 2),
        is_error=not bool(text),
        ts=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
