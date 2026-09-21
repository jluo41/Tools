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
from typing import Any, Dict, Optional, Sequence, Tuple

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


def _expected_verdict(scores: Dict[str, Optional[int]], issues: list[dict]) -> str:
    """Apply the shared, exhaustive verdict policy used by judge personas."""
    available = [score for score in scores.values() if score is not None]
    if any(score <= 2 for score in available) or any(
        issue["severity"] == "critical" for issue in issues
    ):
        return "fail"
    if len(available) != len(scores) or any(score == 3 for score in available):
        return "warn"
    return "pass"


def parse_judgment_xml(
    xml_str: str,
    judge_persona_name: str,
    expected_dimensions: Sequence[str],
) -> Judgment:
    root = ET.fromstring(xml_str)
    if root.tag != "judgment":
        raise ValueError(f"Expected <judgment> root, got <{root.tag}>")

    expected = list(expected_dimensions)
    if not expected or any(not name for name in expected) or len(set(expected)) != len(expected):
        raise ValueError("Judge persona must declare unique, non-empty dimensions")

    rubric_dimensions: Dict[str, Dict[str, Any]] = {}
    scores: Dict[str, Optional[int]] = {}
    rd_root = root.find("rubric_dimensions")
    if rd_root is None:
        raise ValueError("Missing required <rubric_dimensions>")
    for d in rd_root.findall("dimension"):
        name = _ftext(d, "name")
        if not name:
            raise ValueError("Every <dimension> must have a non-empty <name>")
        if name in rubric_dimensions:
            raise ValueError(f"Duplicate rubric dimension {name!r}")
        raw_score = _ftext(d, "score")
        if not raw_score:
            raise ValueError(f"Dimension {name!r} is missing <score>")
        if raw_score == "unavailable":
            score = None
        elif raw_score in {"1", "2", "3", "4", "5"}:
            score = int(raw_score)
        else:
            raise ValueError(
                f"Dimension {name!r} score must be an integer 1-5 or 'unavailable'; "
                f"got {raw_score!r}"
            )
        reasoning = _ftext(d, "reasoning")
        if not reasoning:
            raise ValueError(f"Dimension {name!r} is missing <reasoning>")
        rubric_dimensions[name] = {"score": score, "reasoning": reasoning}
        scores[name] = score

    actual_names = set(rubric_dimensions)
    expected_names = set(expected)
    missing = [name for name in expected if name not in actual_names]
    extra = sorted(actual_names - expected_names)
    if missing or extra:
        raise ValueError(f"Rubric dimension mismatch; missing={missing}, unexpected={extra}")

    issues = []
    iss_root = root.find("issues")
    if iss_root is None:
        raise ValueError("Missing required <issues> (use an empty element for no issues)")
    for i in iss_root.findall("issue"):
        severity = _ftext(i, "severity")
        if severity not in {"info", "warning", "critical"}:
            raise ValueError(f"Issue severity must be info, warning, or critical; got {severity!r}")
        location = _ftext(i, "location")
        issue_text = _ftext(i, "issue")
        if not location or not issue_text:
            raise ValueError("Every issue must have non-empty <location> and <issue>")
        issues.append({
            "severity": severity,
            "location": location,
            "issue": issue_text,
            "suggestion": _ftext(i, "suggestion") or None,
        })

    overall_verdict = _ftext(root, "overall_verdict")
    if overall_verdict not in {"pass", "warn", "fail"}:
        raise ValueError(f"Invalid or missing overall verdict: {overall_verdict!r}")
    expected_verdict = _expected_verdict(scores, issues)
    if overall_verdict != expected_verdict:
        raise ValueError(
            f"Overall verdict {overall_verdict!r} contradicts the rubric policy; "
            f"expected {expected_verdict!r} from scores and critical issues"
        )

    raw_overall_score = _ftext(root, "overall_score")
    if not raw_overall_score:
        raise ValueError("Missing required <overall_score>")
    available_scores = [score for score in scores.values() if score is not None]
    expected_score = round(statistics.mean(available_scores), 2) if available_scores else None
    if raw_overall_score == "unavailable":
        overall_score = None
    else:
        try:
            overall_score = float(raw_overall_score)
        except ValueError as exc:
            raise ValueError(f"Invalid overall score {raw_overall_score!r}") from exc
        if not (0.0 <= overall_score <= 5.0):
            raise ValueError("Overall score must be between 0 and 5")
        if expected_score is None or abs(overall_score - expected_score) > 0.01:
            raise ValueError(
                f"Overall score must be the mean of available rubric scores; "
                f"expected {expected_score if expected_score is not None else 'unavailable'}"
            )
    if expected_score is None and overall_score is not None:
        raise ValueError("Overall score must be unavailable when no dimension is assessed")
    if expected_score is not None and overall_score is None:
        raise ValueError(f"Overall score is required; expected {expected_score}")

    summary = _ftext(root, "summary")
    if not summary:
        raise ValueError("Missing required <summary>")

    return Judgment(
        judge_persona=judge_persona_name,
        rubric_dimensions=rubric_dimensions,
        issues=issues,
        overall_verdict=overall_verdict,
        overall_score=round(overall_score, 2) if overall_score is not None else None,
        summary=summary,
    )


# ─── public entry point ──────────────────────────────────────────────


def judge_report(
    report: Dict[str, Any],
    *,
    system_prompt: str,
    judge_persona_name: str,
    expected_dimensions: Sequence[str],
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
    judgment = parse_judgment_xml(xml_str, judge_persona_name, expected_dimensions)

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
