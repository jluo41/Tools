"""Codex OAuth transport (OAuth via ~/.codex/auth.json)."""
from __future__ import annotations

import time

from ..types import LLMResult, Usage


async def call(
    system_prompt: str,
    user_message: str,
    model: str = "gpt-5.5",
) -> LLMResult:
    from codex_oauth import CodexOAuthClient

    started = time.time()
    try:
        async with CodexOAuthClient(model=model) as client:
            response = await client.complete(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
    except Exception as e:
        return LLMResult(
            transport="codex_oauth", model=model,
            wall_time_s=round(time.time() - started, 2),
            is_error=True, error=f"{type(e).__name__}: {e}",
            ts=time.strftime("%Y-%m-%d %H:%M:%S"),
        )
    elapsed = time.time() - started

    return LLMResult(
        text=response.content,
        model=response.model,
        transport="codex_oauth",
        usage=Usage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        ),
        meta={"raw_usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        }},
        wall_time_s=round(elapsed, 2),
        is_error=not bool(response.content),
        ts=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
