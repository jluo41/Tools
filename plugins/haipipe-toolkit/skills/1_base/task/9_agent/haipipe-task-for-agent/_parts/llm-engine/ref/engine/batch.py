"""Batch runner with concurrency control and circuit breaker."""
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any, Callable

from .types import LLMResult


def write_call_artifacts(call_dir: Path, input_data: dict, result: LLMResult):
    call_dir.mkdir(parents=True, exist_ok=True)
    (call_dir / "input.json").write_text(json.dumps(input_data, indent=2, default=str))
    (call_dir / "response.json").write_text(json.dumps({"text": result.text}, indent=2, default=str))
    (call_dir / "meta.json").write_text(json.dumps({
        "transport": result.transport,
        "model": result.model,
        "wall_time_s": result.wall_time_s,
        "cost_usd": result.cost_usd,
        "usage": {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "total_tokens": result.usage.total_tokens,
        },
        "is_error": result.is_error,
        "error": result.error,
        "meta": result.meta,
        "ts": result.ts,
    }, indent=2, default=str))


async def batch_call(
    cases: list[Any],
    call_fn: Callable,
    store_dir: Path | None = None,
    case_id_fn: Callable | None = None,
    skip_fn: Callable | None = None,
    max_workers: int = 1,
    max_consecutive_failures: int = 5,
) -> list[tuple[Any, LLMResult | None]]:
    """Run call_fn on each case, with idempotent skip and circuit breaker.

    Args:
        cases: list of case objects
        call_fn: async (case) -> LLMResult
        store_dir: base dir for per-case artifacts (optional)
        case_id_fn: (case) -> str for artifact subdirs (optional)
        skip_fn: (case) -> bool, skip if True (optional)
        max_workers: concurrency (1 = serial)
        max_consecutive_failures: halt after N consecutive failures (0 = disable)

    Returns:
        list of (case, result_or_None) pairs
    """
    results = []
    consecutive_failures = 0
    total = len(cases)

    for i, case in enumerate(cases):
        if skip_fn and skip_fn(case):
            results.append((case, None))
            continue

        ts = time.strftime("%H:%M:%S")
        case_id = case_id_fn(case) if case_id_fn else str(i)
        print(f"[{ts}] [{i+1}/{total}] {case_id} ...", flush=True)

        try:
            result = await call_fn(case)
            if store_dir and case_id_fn:
                write_call_artifacts(
                    store_dir / case_id,
                    input_data={"case_id": case_id, "case": str(case)},
                    result=result,
                )
            results.append((case, result))
            if result.is_error:
                print(f"[{ts}] x  {case_id}: {result.error}", flush=True)
                consecutive_failures += 1
            else:
                print(f"[{ts}] ok {case_id}  ({result.wall_time_s}s)", flush=True)
                consecutive_failures = 0
        except Exception as e:
            print(f"[{ts}] x  {case_id}: {e}", flush=True)
            results.append((case, None))
            consecutive_failures += 1

        if max_consecutive_failures and consecutive_failures >= max_consecutive_failures:
            print(f"[{time.strftime('%H:%M:%S')}] {consecutive_failures} consecutive "
                  f"failures -- halting.", flush=True)
            break

    return results
