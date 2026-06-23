"""Judge a Report against a rubric persona via Claude Agent SDK.

Same SDK skeleton as compose_report.py — only the schemas, prompts,
and XML root differ. Output XML root is <judgment>.

Input: a Report (or report.json path)
Output: a Judgment + raw response + telemetry
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import statistics
import xml.etree.ElementTree as ET
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock

from judgment_schema import Judgment

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_TIMEOUT_S = 120

_AMP_RE = re.compile(r"&(?!(?:amp|lt|gt|apos|quot|#\d+|#x[0-9a-fA-F]+);)")


# ─── user-message construction ────────────────────────────────────────


def build_user_msg(
    report: Dict[str, Any],
    *,
    extra_context: Optional[Dict[str, Any]] = None,
) -> str:
    """Build the message the judge LLM sees: the Report + optional ground
    truth (raw forecast / ctx) it can fact-check against."""
    blocks = ["REPORT TO JUDGE", json.dumps(report, indent=2, default=str)]
    if extra_context:
        blocks += [
            "\n--- GROUND TRUTH (for fact-checking; do not reproduce) ---",
            json.dumps(extra_context, indent=2, default=str),
        ]
    blocks += [
        "\nProduce ONE <judgment>...</judgment> XML block per the schema.",
        "No prose outside the <judgment> block.",
    ]
    return "\n".join(blocks)


# ─── SDK call (1:1 with compose_report) ────────────────────────────────


async def _query_sdk(
    system_prompt: str, user_msg: str, model: str
) -> Dict[str, Any]:
    options = ClaudeAgentOptions(
        cwd=None,
        allowed_tools=[],
        permission_mode="default",
        max_turns=1,
        model=model,
        system_prompt=system_prompt,
    )
    response_text = ""
    result_msg_dict: Optional[Dict[str, Any]] = None
    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_msg)
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        response_text = block.text
            elif isinstance(msg, ResultMessage):
                if is_dataclass(msg):
                    result_msg_dict = asdict(msg)
                else:
                    result_msg_dict = {
                        f: getattr(msg, f, None)
                        for f in (
                            "subtype", "duration_ms", "duration_api_ms", "is_error",
                            "num_turns", "session_id", "stop_reason", "total_cost_usd",
                            "usage", "result", "model_usage",
                        )
                    }
    return {"text": response_text, "result_msg": result_msg_dict}


# ─── XML parsing ──────────────────────────────────────────────────────


def extract_judgment_xml(text: str) -> str:
    m = re.search(r"<judgment>.*?</judgment>", text, re.DOTALL)
    if not m:
        raise ValueError("no <judgment>...</judgment> block in SDK output")
    return _AMP_RE.sub("&amp;", m.group(0))


def _ftext(elem, tag, default=""):
    v = elem.findtext(tag)
    return v.strip() if v else default


def _fnum(elem, tag, cast=float):
    v = elem.findtext(tag)
    if v is None or not v.strip():
        return None
    try:
        return cast(v.strip())
    except (ValueError, TypeError):
        return None


def parse_judgment_xml(xml_str: str, judge_persona_name: str) -> Judgment:
    root = ET.fromstring(xml_str)

    rubric_dimensions: Dict[str, Dict[str, Any]] = {}
    rd_root = root.find("rubric_dimensions")
    if rd_root is not None:
        for d in rd_root.findall("dimension"):
            name = (d.findtext("name") or "").strip()
            if not name:
                continue
            score = _fnum(d, "score", int)
            reasoning = _ftext(d, "reasoning")
            if score is None:
                # missing score → skip silently rather than fail; surfaced in summary
                continue
            rubric_dimensions[name] = {"score": score, "reasoning": reasoning}

    issues = []
    iss_root = root.find("issues")
    if iss_root is not None:
        for i in iss_root.findall("issue"):
            sev = _ftext(i, "severity") or "info"
            issues.append(
                {
                    "severity": sev if sev in {"info", "warning", "critical"} else "info",
                    "location": _ftext(i, "location"),
                    "issue": _ftext(i, "issue"),
                    "suggestion": _ftext(i, "suggestion") or None,
                }
            )

    overall_verdict = (_ftext(root, "overall_verdict") or "warn").lower()
    if overall_verdict not in {"pass", "warn", "fail"}:
        overall_verdict = "warn"

    overall_score = _fnum(root, "overall_score") or (
        statistics.mean([d["score"] for d in rubric_dimensions.values()])
        if rubric_dimensions
        else 0.0
    )

    summary = _ftext(root, "summary")

    return Judgment(
        judge_persona=judge_persona_name,
        rubric_dimensions=rubric_dimensions,
        issues=issues,
        overall_verdict=overall_verdict,
        overall_score=round(float(overall_score), 2),
        summary=summary,
    )


# ─── public entry point ──────────────────────────────────────────────


def judge_report(
    report: Dict[str, Any],
    *,
    system_prompt: str,
    judge_persona_name: str,
    extra_context: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout_s: int = DEFAULT_TIMEOUT_S,
) -> Tuple[Judgment, str, Dict[str, Any]]:
    """Judge a Report. Returns (judgment, raw_response_text, telemetry)."""
    if "ANTHROPIC_BASE_URL" in os.environ:
        os.environ.pop("ANTHROPIC_BASE_URL", None)
    if "ANTHROPIC_AUTH_TOKEN" in os.environ:
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

    user_msg = build_user_msg(report, extra_context=extra_context)

    sdk_out = asyncio.run(
        asyncio.wait_for(_query_sdk(system_prompt, user_msg, model), timeout=timeout_s)
    )
    raw_text = sdk_out["text"] or ""
    rm = sdk_out["result_msg"] or {}

    if rm.get("is_error"):
        raise RuntimeError(f"SDK reported error: stop={rm.get('stop_reason')!r}")
    if not raw_text:
        raise RuntimeError("Empty response from SDK")

    xml_str = extract_judgment_xml(raw_text)
    judgment = parse_judgment_xml(xml_str, judge_persona_name)

    telemetry = {
        "model": model,
        "session_id": rm.get("session_id"),
        "cost_usd_equiv": rm.get("total_cost_usd"),
        "stop_reason": rm.get("stop_reason"),
        "duration_ms": rm.get("duration_ms"),
        "duration_api_ms": rm.get("duration_api_ms"),
        "num_turns": rm.get("num_turns"),
        "usage": rm.get("usage"),
        "user_msg_chars": len(user_msg),
        "response_chars": len(raw_text),
        "system_prompt_chars": len(system_prompt),
        "ts": datetime.now().isoformat(timespec="seconds"),
    }
    return judgment, raw_text, telemetry


def load_report_json(path: str | Path) -> Dict[str, Any]:
    """Convenience: load a report.json from disk."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No report.json at {p}")
    if p.is_dir():
        p = p / "report.json"
    return json.loads(p.read_text())
