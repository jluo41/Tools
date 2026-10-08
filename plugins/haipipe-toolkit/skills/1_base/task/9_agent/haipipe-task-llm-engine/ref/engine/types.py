"""Unified response types for the LLM engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass
class LLMResult:
    text: str = ""
    model: str = ""
    transport: str = ""
    cost_usd: float | None = None
    usage: Usage = field(default_factory=Usage)
    meta: dict[str, Any] = field(default_factory=dict)
    wall_time_s: float = 0.0
    is_error: bool = False
    error: str | None = None
    ts: str = ""
