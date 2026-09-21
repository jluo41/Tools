"""Compose a patient/clinician report from (patient_ctx, forecast).

Layered call:
  1. Build user message — basics + current + forecast summary
  2. claude_agent_sdk.query() with persona system prompt + user msg
  3. Extract <report> XML block from response
  4. Parse XML → Report pydantic model
  5. Return Report + telemetry

SDK pattern adapted from
  /home/jluo41/Physician-SPACE/examples/ProjA-PhyTraitLandScape/
    tasks/A3_cross_family_judge/run_sdk_judge.py
"""

from __future__ import annotations

import asyncio
import os
import re
import statistics
import xml.etree.ElementTree as ET
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock

from report_schema import Report

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_TIMEOUT_S = 120

_AMP_RE = re.compile(r"&(?!(?:amp|lt|gt|apos|quot|#\d+|#x[0-9a-fA-F]+);)")

# Code → label mappings, per code/haifn/fn_record/record/Ptt.py:46 and
# CGMacrosV251227.py:235 (1=Male, 2=Female) and tetoken transform.py:33
# (DiseaseType:T1D|T2D).
_GENDER_MAP = {1: "Male", 2: "Female", 0: "Unknown"}
_DISEASE_MAP = {1: "Type 1 diabetes", 2: "Type 2 diabetes"}


def _decode_gender(v) -> str:
    if v is None:
        return "Unknown"
    try:
        return _GENDER_MAP.get(int(float(v)), f"Unknown (code={v})")
    except (ValueError, TypeError):
        return str(v)


def _decode_disease(v) -> str:
    if v is None:
        return "Unknown"
    try:
        return _DISEASE_MAP.get(int(float(v)), f"Unknown (code={v})")
    except (ValueError, TypeError):
        return str(v)


def _age_from_yob(yob, ref_year: Optional[int] = None) -> Optional[int]:
    if yob is None:
        return None
    try:
        ref = ref_year or datetime.now().year
        return int(ref) - int(yob)
    except (ValueError, TypeError):
        return None


# ─── user-message construction ────────────────────────────────────────


def _summarize_recent_cgm(ctx: dict, window: int = 288) -> Dict[str, Any]:
    """Last `window` CGM points → min/max/mean + last_bg + last_obs_dt."""
    cgm = ctx["tables"].get("CGM")
    if cgm is None or len(cgm) == 0:
        raise ValueError("No CGM data in patient context")

    tail = cgm.tail(window)
    bgs = [float(x) for x in tail["BGValue"].tolist()]
    last = tail.iloc[-1]
    return {
        "last_obs_dt": str(last["ObservationDateTime"]),
        "last_bg_mg_dl": float(last["BGValue"]),
        "recent_window_n": len(tail),
        "recent_min": min(bgs),
        "recent_max": max(bgs),
        "recent_mean": round(statistics.mean(bgs), 2),
    }


def _summarize_forecast(forecast_resp: dict) -> Dict[str, Any]:
    """Summarize the last returned window under the Endpoint ordering contract.

    The response need not expose timestamps. This selection alone does not
    prove the segment ends at the latest observation or represents "now".
    """
    models = forecast_resp.get("models", []) or []
    if not models:
        raise ValueError("Endpoint response has no models[]")
    fcst = models[0].get("forecast", []) or []
    if not fcst:
        raise ValueError("Endpoint response forecast list is empty")

    last = fcst[-1].get("y_pred_h24") or []
    if not last:
        raise ValueError("Last forecast window has no y_pred_h24 values")
    last_vals = [float(x) for x in last]
    trend = _classify_trend(last_vals)
    low, high = min(last_vals) < 70, max(last_vals) > 300
    safety_flag = "hypo_and_hyper_risk" if low and high else "hypo_risk" if low else "hyper_risk" if high else "none"

    return {
        "expected_safety_flag": safety_flag,  # computed before display rounding
        "anchor_verified": False,
        "selection_rule": "last_returned_window; chronological anchor unavailable",
        "_trend_evidence": trend,
        "horizon_minutes": len(last_vals) * 5,
        "n_windows": len(fcst),
        "pred_min": round(min(last_vals), 2),
        "pred_max": round(max(last_vals), 2),
        "pred_mean": round(statistics.mean(last_vals), 2),
        # Convenience: keep the trajectory for the most recent window so
        # a downstream renderer (chart, ASCII spark, judge) doesn't need
        # to peel forecast_resp again.
        "_trajectory": [round(v, 2) for v in last_vals],
    }


def _basics_block(ctx: dict) -> Dict[str, Any]:
    """Patient demographics, decoded to human-readable labels.

    Raw Ptt parquet stores numeric codes (Gender 1/2, DiseaseType 1.0/2.0).
    The LLM has no way to know those conventions, so we decode them here
    BEFORE the prompt is built — that's the right layer for unit/code
    translation, not the prompt itself."""
    ptt = ctx["tables"].get("Ptt")
    out: Dict[str, Any] = {
        "individual_id": ctx.get("individual_id"),
        "dataset": ctx.get("dataset"),
    }
    if ptt is None or len(ptt) == 0:
        return out
    row = ptt.iloc[0].to_dict()
    yob = row.get("YearOfBirth")
    out.update(
        {
            "gender": _decode_gender(row.get("Gender")),
            "year_of_birth": int(yob) if yob is not None else None,
            "age_years": _age_from_yob(yob),
            "disease_type": _decode_disease(row.get("DiseaseType")),
        }
    )
    return out


def _trajectory_sparkline(vals: List[float]) -> str:
    """Compact text spark of the forecast trajectory.

    e.g. "150 ▁▂▃▅▆▇█ 90"  — start, sparkline, end. Helps the LLM see
    direction without listing 24 floats."""
    if not vals:
        return ""
    blocks = "▁▂▃▄▅▆▇█"
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    spark = "".join(blocks[min(7, int((v - lo) / span * 7))] for v in vals)
    return f"{vals[0]:.0f} {spark} {vals[-1]:.0f}"


def _classify_trend(vals: List[float]) -> Dict[str, Any]:
    """Describe adjacent-step directions without a magnitude cutoff.

    A constant series is stable. A series with increases and no decreases is
    rising; one with decreases and no increases is falling; a series with
    both is mixed. Equality and direction are exact comparisons of the
    supplied numeric values. These labels describe the series only and do
    not establish clinical significance.
    """
    if not vals:
        raise ValueError("Cannot classify an empty forecast trajectory")
    values = [float(v) for v in vals]
    if any(not (-float("inf") < v < float("inf")) for v in values):
        raise ValueError("Forecast trajectory must contain finite values")

    increases = sum(current > previous for previous, current in zip(values, values[1:]))
    decreases = sum(current < previous for previous, current in zip(values, values[1:]))
    unchanged = len(values) - 1 - increases - decreases
    if increases == 0 and decreases == 0:
        label = "stable"
    elif increases > 0 and decreases == 0:
        label = "rising"
    elif decreases > 0 and increases == 0:
        label = "falling"
    else:
        label = "mixed"
    return {
        "verdict": label,
        "increasing_steps": increases,
        "decreasing_steps": decreases,
        "unchanged_steps": unchanged,
        "total_steps": len(values) - 1,
    }


def build_user_msg(ctx: dict, forecast_resp: dict) -> str:
    """Single string the LLM sees as the user message."""
    basics = _basics_block(ctx)
    current = _summarize_recent_cgm(ctx)
    fcst = _summarize_forecast(forecast_resp)
    traj = fcst.pop("_trajectory", [])
    trend = fcst.pop("_trend_evidence")
    spark = _trajectory_sparkline(traj)

    def _kv(d):
        return "\n".join(f"  {k}: {v}" for k, v in d.items())

    fcst_block = _kv(fcst)
    if spark:
        fcst_block += f"\n  trajectory: {spark}"
    fcst_block += (
        "\n  derived_trend_rule: Compare every adjacent pair in the supplied "
        "series. Constant is stable; increases with no decreases is rising; "
        "decreases with no increases is falling; both increase and decrease "
        "steps is mixed. This is descriptive and does not establish clinical significance."
        f"\n  derived_trend_evidence: verdict={trend['verdict']}; "
        f"increasing_steps={trend['increasing_steps']}; "
        f"decreasing_steps={trend['decreasing_steps']}; "
        f"unchanged_steps={trend['unchanged_steps']}; "
        f"total_steps={trend['total_steps']}"
        "\n  confidence_evidence: unavailable; this input contains a point "
        "trajectory but no forecast calibration or predictive-uncertainty evidence."
    )

    return (
        "PATIENT BASICS\n"
        f"{_kv(basics)}\n\n"
        "CURRENT STATUS\n"
        f"{_kv(current)}\n\n"
        "SELECTED MODEL FORECAST (anchor time not independently verified)\n"
        f"{fcst_block}\n\n"
        "Do not claim this forecast starts now or at last_obs_dt without anchor evidence. "
        "State that timing is unverified and preserve expected_safety_flag, which uses unrounded predictions. "
        "Use the supplied derived_trend_evidence.verdict exactly as interpretation.verdict; "
        "the listed adjacent-step rule defines the labels and may not be reinterpreted. "
        "In interpretation.why, describe only evidence in the supplied data; do not infer a cause from association. "
        "If no cause is established, say that the cause is unknown. "
        "Set interpretation.confidence to unavailable: no calibration or predictive-uncertainty "
        "evidence was supplied. Do not infer confidence from trajectory spread. "
        "Compose the <report> per the schema. "
        "Output ONLY the <report> block."
    )


# ─── SDK call ─────────────────────────────────────────────────────────


async def _query_sdk(
    system_prompt: str, user_msg: str, model: str
) -> Dict[str, Any]:
    """Single-shot SDK call. Returns response text + ResultMessage telemetry."""
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


def extract_report_xml(text: str) -> str:
    m = re.search(r"<report>.*?</report>", text, re.DOTALL)
    if not m:
        raise ValueError("no <report>...</report> block in SDK output")
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


def parse_report_xml(xml_str: str, *, expected_verdict: Optional[str] = None) -> Report:
    root = ET.fromstring(xml_str)

    b = root.find("basics") or ET.Element("basics")
    basics = {
        "individual_id": _ftext(b, "individual_id"),
        "dataset": _ftext(b, "dataset") or None,
        "gender": _ftext(b, "gender") or None,
        "year_of_birth": _fnum(b, "year_of_birth", int),
        "age_years": _fnum(b, "age_years", int),
        "disease_type": _ftext(b, "disease_type") or None,
    }

    c = root.find("current") or ET.Element("current")
    current = {
        "last_obs_dt": _ftext(c, "last_obs_dt"),
        "last_bg_mg_dl": _fnum(c, "last_bg_mg_dl") or 0.0,
        "recent_window_n": _fnum(c, "recent_window_n", int) or 0,
        "recent_min": _fnum(c, "recent_min"),
        "recent_max": _fnum(c, "recent_max"),
        "recent_mean": _fnum(c, "recent_mean"),
    }

    f = root.find("forecast_summary") or ET.Element("forecast_summary")
    forecast_summary = {
        "horizon_minutes": _fnum(f, "horizon_minutes", int) or 0,
        "n_windows": _fnum(f, "n_windows", int) or 0,
        "pred_min": _fnum(f, "pred_min") or 0.0,
        "pred_max": _fnum(f, "pred_max") or 0.0,
        "pred_mean": _fnum(f, "pred_mean") or 0.0,
    }

    i = root.find("interpretation") or ET.Element("interpretation")
    actions = []
    a_root = i.find("actions")
    if a_root is not None:
        for a in a_root.findall("action"):
            txt = (a.text or "").strip()
            if txt:
                actions.append(txt)
    verdict = _ftext(i, "verdict")
    why = _ftext(i, "why")
    confidence = _ftext(i, "confidence")
    safety_flag = _ftext(i, "safety_flag")
    for field, value in (
        ("verdict", verdict),
        ("why", why),
        ("confidence", confidence),
        ("safety_flag", safety_flag),
    ):
        if not value:
            raise ValueError(f"Missing required interpretation.{field} label")
    interpretation = {
        "verdict": verdict,
        "why": why,
        "actions": actions,
        "confidence": confidence,
        "safety_flag": safety_flag,
    }

    nl_node = root.find("nl")
    nl = ((nl_node.text or "") if nl_node is not None else "").strip()

    report = Report(
        basics=basics,
        current=current,
        forecast_summary=forecast_summary,
        interpretation=interpretation,
        nl=nl,
    )
    if expected_verdict is not None and report.interpretation.verdict != expected_verdict:
        raise ValueError(
            "Model verdict disagrees with deterministic forecast trend rule: "
            f"expected {expected_verdict!r}, got {report.interpretation.verdict!r}"
        )
    if report.interpretation.confidence != "unavailable":
        raise ValueError(
            "Confidence must be unavailable unless calibrated uncertainty "
            "evidence is supplied"
        )
    return report


# ─── public entry point ──────────────────────────────────────────────


def compose_report(
    ctx: dict,
    forecast_resp: dict,
    *,
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    timeout_s: int = DEFAULT_TIMEOUT_S,
) -> Tuple[Report, str, Dict[str, Any]]:
    """Compose a Report from a patient ctx + endpoint forecast response.

    Returns:
        (report, raw_response_text, telemetry_dict)
    """
    # Make sure ANTHROPIC_API_KEY can't override the OAuth subscription auth.
    # The SDK subprocess inherits env; if API key is set it bills via API
    # instead of subscription. Per repo memory, env.sh sets a CRS proxy key
    # that we want to bypass for SDK calls.
    if "ANTHROPIC_BASE_URL" in os.environ:
        os.environ.pop("ANTHROPIC_BASE_URL", None)
    if "ANTHROPIC_AUTH_TOKEN" in os.environ:
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

    trend = _summarize_forecast(forecast_resp)["_trend_evidence"]
    user_msg = build_user_msg(ctx, forecast_resp)

    sdk_out = asyncio.run(
        asyncio.wait_for(_query_sdk(system_prompt, user_msg, model), timeout=timeout_s)
    )
    raw_text = sdk_out["text"] or ""
    rm = sdk_out["result_msg"] or {}

    if rm.get("is_error"):
        raise RuntimeError(f"SDK reported error: stop={rm.get('stop_reason')!r}")
    if not raw_text:
        raise RuntimeError("Empty response from SDK")

    xml_str = extract_report_xml(raw_text)
    report = parse_report_xml(xml_str, expected_verdict=trend["verdict"])

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
    return report, raw_text, telemetry
