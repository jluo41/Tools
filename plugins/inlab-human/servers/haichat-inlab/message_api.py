"""message_api — the three steps AFTER a prediction, plus the human's verdict.

    ① ▶ Run          (console_api /predict)   deterministic, no LLM
    ② ✉️ Compose     POST /api/message        forecast ──▶ patient message
    ③ ⚖️ Judge       POST /api/judge          message  ──▶ rubric scores
    ④ 🩺 Feedback    POST /api/feedback       human verdict, append-only

THE WALL, and the reason this file exists:

    the endpoint answers with `forecast` AND `observed` — the truth the model
    was not given. `observed` is how the console draws MAE. It must NEVER
    reach the composer or the judge: a message written with hindsight is not
    the message a patient would have received, and scoring it proves nothing.
    `_blind()` strips it, once, at the door.

Styles and rubrics are NOT authored here — they are the persona folders shipped
by the haipipe individual-inference skills, so a new style is a new folder and
never a code change:

    …/skills/task/4_individual/haipipe-individual-inference-report/personas/*
    …/skills/task/4_individual/haipipe-individual-inference-judge/personas/*

Config:
    INLAB_PERSONA_ROOT   dir holding the two skills. Unset ⇒ walk up for Tools/.
    INLAB_RUN_STORE      where run records land. Unset ⇒ ./.runs
"""
from __future__ import annotations

import json
import os
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")

REPORT_SKILL = "haipipe-individual-inference-report"
JUDGE_SKILL = "haipipe-individual-inference-judge"


# ── where the personas live ──────────────────────────────────────────────────
def _persona_root() -> Path | None:
    env = os.environ.get("INLAB_PERSONA_ROOT")
    if env:
        p = Path(env).expanduser()
        return p if p.is_dir() else None
    here = Path(__file__).resolve()
    # this folder lives inside plugins/inlab-human/servers/, so the toolkit is a
    # sibling plugin three levels up; the walk-up below covers any other layout
    sibling = here.parents[3] / "haipipe-toolkit/skills/task/4_individual"
    if sibling.is_dir():
        return sibling
    for parent in here.parents:
        cand = parent / "Tools/plugins/haipipe-toolkit/skills/task/4_individual"
        if cand.is_dir():
            return cand
    return None


def _persona_dirs(skill: str) -> list[Path]:
    """Where a style may live, nearest first: the console's own `personas/` overlay,
    then the shipped skill. The overlay lets this service add an audience without
    editing the Tools submodule; a same-named local folder wins."""
    out = []
    local = Path(__file__).parent / "personas" / skill / "personas"
    if not local.is_dir():
        local = Path(__file__).parent / "personas" / skill
    if local.is_dir():
        out.append(local)
    root = _persona_root()
    if root and (root / skill / "personas").is_dir():
        out.append(root / skill / "personas")
    return out


def _personas(skill: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for d in _persona_dirs(skill):
        for p in sorted(d.iterdir()):
            if p.name in seen or not (p / "system.md").exists():
                continue
            seen.add(p.name)
            meta = _yaml_lite((p / "persona.yaml").read_text()) if (p / "persona.yaml").exists() else {}
            out.append({
                "name": p.name,
                "audience": meta.get("audience") or meta.get("target_audience"),
                "tone": meta.get("tone"),
                "model": meta.get("model"),
                "dimensions": meta.get("dimensions") or [],
                "safety_rules": meta.get("safety_rules") or [],
            })
    return out


def _yaml_lite(text: str) -> dict[str, Any]:
    """The persona files are flat `key: value` + `- item` lists. A 30-line reader
    beats adding a yaml dependency to a service that needs nothing else from it."""
    out: dict[str, Any] = {}
    key = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and key:
            out.setdefault(key, []).append(line.lstrip()[2:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            out[key] = v if v else []
    return out


def _persona_files(skill: str, name: str) -> tuple[str, dict[str, Any]] | None:
    for base in _persona_dirs(skill):
        d = base / name
        sysmd = d / "system.md"
        if not sysmd.exists():
            continue
        meta = _yaml_lite((d / "persona.yaml").read_text()) if (d / "persona.yaml").exists() else {}
        system = sysmd.read_text()
        schema = (d / "schema.md").read_text() if (d / "schema.md").exists() else ""
        if schema:
            system = f"{system}\n\n{schema}"
        return system, meta
    return None


# ── the wall ─────────────────────────────────────────────────────────────────
def _blind(resp: dict[str, Any]) -> dict[str, Any]:
    """The endpoint's answer minus everything the model was not given.

    `observed` (and any metric derived from it) is ground truth. It is what the
    console compares the forecast against — and exactly what a message composed
    at prediction time cannot know. Strip it here so no downstream prompt can
    accidentally read it."""
    out = json.loads(json.dumps(resp))
    for m in out.get("models", []) or []:
        m.pop("observed", None)
        m.pop("metrics", None)
        meta = m.get("metadata")
        if isinstance(meta, dict):
            meta.pop("mae", None)
            meta.pop("rmse", None)
    return out


# ── prompt inputs, from OUR shapes (flat forecast list, patient JSON) ─────────
_GENDER = {1: "male", 2: "female", "1": "male", "2": "female"}


def _forecast_of(resp: dict[str, Any]) -> list[float]:
    for m in resp.get("models", []) or []:
        f = m.get("forecast")
        if isinstance(f, list) and f and isinstance(f[0], (int, float)):
            return [float(x) for x in f]
        # the skill's shape: a list of windows, each with y_pred_h24
        if isinstance(f, list) and f and isinstance(f[0], dict):
            last = f[-1].get("y_pred_h24") or []
            if last:
                return [float(x) for x in last]
    return []


def _context_of(resp: dict[str, Any]) -> list[float]:
    for m in resp.get("models", []) or []:
        c = m.get("context")
        if isinstance(c, list) and c:
            return [float(x) for x in c]
    return []


def _spark(vals: list[float]) -> str:
    if not vals:
        return ""
    blocks = "▁▂▃▄▅▆▇█"
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    s = "".join(blocks[min(7, int((v - lo) / span * 7))] for v in vals)
    return f"{vals[0]:.0f} {s} {vals[-1]:.0f}"


def _events_near(patient: dict[str, Any], anchor: str | None, hours: int = 6) -> list[str]:
    """Meals / exercise / medication shortly BEFORE the anchor — the context that
    explains a forecast. Nothing after the anchor: that is the future."""
    if not anchor:
        return []
    try:
        end = datetime.strptime(anchor, "%m/%d/%Y %I:%M:%S %p")
    except ValueError:
        return []
    out = []
    for name, label in (("Diet", "meal"), ("Exercise", "exercise"), ("Medication", "medication")):
        for r in (patient.get("source_tables", {}).get(name) or []):
            raw = r.get("ObservationDateTime") or r.get("AdministrationDate")
            try:
                t = datetime.strptime(str(raw), "%m/%d/%Y %I:%M:%S %p")
            except (ValueError, TypeError):
                continue
            mins = (end - t).total_seconds() / 60
            if not (0 <= mins <= hours * 60):
                continue
            if label == "meal":
                d = f"{r.get('FoodName') or 'meal'}"
                if r.get("Carbs") not in (None, ""):
                    d += f", {r.get('Carbs')}g carbs"
            elif label == "exercise":
                d = f"{r.get('ExerciseType') or 'exercise'}"
                if r.get("ExerciseDuration") not in (None, ""):
                    d += f", {r.get('ExerciseDuration')} min"
            else:
                d = "medication"
                if r.get("Dose") not in (None, ""):
                    d += f", dose {r.get('Dose')}"
            out.append(f"{int(mins)} min before: {d}")
    out.sort(key=lambda s: int(s.split()[0]), reverse=True)
    return out[:8]


def _compose_user_msg(patient: dict[str, Any], resp: dict[str, Any],
                      anchor: str | None) -> str:
    fc = _forecast_of(resp)
    ctx = _context_of(resp)
    if not fc:
        raise ValueError("the run carries no forecast to write about")

    summary = patient.get("summary", {}) or {}
    ptt = (patient.get("source_tables", {}).get("Ptt") or [{}])[0]
    yob = ptt.get("YearOfBirth") or summary.get("year_of_birth")
    age = None
    try:
        age = datetime.now().year - int(yob)
    except (TypeError, ValueError):
        pass

    basics = {
        "individual_id": patient.get("patient_id"),
        "dataset": summary.get("cohort"),
        "gender": _GENDER.get(ptt.get("Gender") or summary.get("sex"), "unknown"),
        "age_years": age,
    }
    current: dict[str, Any] = {"last_obs_dt": anchor}
    if ctx:
        recent = ctx[-288:]
        current.update({
            "last_bg_mg_dl": round(recent[-1], 1),
            "recent_window_n": len(recent),
            "recent_min": round(min(recent), 1),
            "recent_max": round(max(recent), 1),
            "recent_mean": round(statistics.mean(recent), 1),
        })
    forecast = {
        "horizon_minutes": len(fc) * 5,
        "pred_min": round(min(fc), 1),
        "pred_max": round(max(fc), 1),
        "pred_mean": round(statistics.mean(fc), 1),
    }

    def kv(d):
        return "\n".join(f"  {k}: {v}" for k, v in d.items() if v is not None)

    events = _events_near(patient, anchor)
    ev_block = ("\nRECENT EVENTS (before the forecast anchor)\n"
                + "\n".join(f"  {e}" for e in events) + "\n") if events else ""

    return (
        "PATIENT BASICS\n" + kv(basics) + "\n\n"
        "CURRENT STATUS\n" + kv(current) + "\n"
        + ev_block +
        "\nMODEL FORECAST (next ~2h, anchored at last_obs_dt)\n" + kv(forecast)
        + f"\n  trajectory: {_spark(fc)}\n\n"
        "You do NOT know what actually happened after the anchor. Write only from "
        "the forecast above.\n\n"
        "Compose the <report> per the schema. Output ONLY the <report> block."
    )


def _judge_user_msg(report_nl: str, report_json: dict[str, Any],
                    resp: dict[str, Any]) -> str:
    fc = _forecast_of(resp)
    return (
        "THE FORECAST THE MESSAGE WAS WRITTEN FROM\n"
        f"  pred_min: {round(min(fc), 1) if fc else '—'}\n"
        f"  pred_max: {round(max(fc), 1) if fc else '—'}\n"
        f"  trajectory: {_spark(fc)}\n\n"
        "THE MESSAGE UNDER REVIEW\n"
        f"{report_nl}\n\n"
        "ITS STRUCTURED LAYER\n"
        f"{json.dumps(report_json, indent=2)[:2000]}\n\n"
        "Score it per the rubric. Output ONLY the judgment block."
    )


# ── the SDK call ─────────────────────────────────────────────────────────────
async def _ask(system_prompt: str, user_msg: str, model: str | None) -> str:
    from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions,
                                  ClaudeSDKClient, TextBlock)
    options = ClaudeAgentOptions(
        cwd=None, allowed_tools=[], permission_mode="default", max_turns=1,
        model=model or os.environ.get("INLAB_MESSAGE_MODEL") or None,
        system_prompt=system_prompt,
    )
    text = ""
    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_msg)
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        text += block.text
    return text


def _tag(text: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>.*?</{tag}>", text, re.DOTALL)
    return m.group(0) if m else None


def _xml_to_dict(xml: str) -> dict[str, Any]:
    """Shallow XML → dict. The persona schemas are one or two levels deep, and a
    tolerant reader beats a strict one when an LLM is the author."""
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;)", "&amp;", xml))
    except ET.ParseError:
        return {}

    def walk(el):
        kids = list(el)
        if not kids:
            return (el.text or "").strip()
        out: dict[str, Any] = {}
        for k in kids:
            v = walk(k)
            if k.tag in out:
                if not isinstance(out[k.tag], list):
                    out[k.tag] = [out[k.tag]]
                out[k.tag].append(v)
            else:
                out[k.tag] = v
        return out
    return {root.tag: walk(root)}


# ── the run store ────────────────────────────────────────────────────────────
def _store() -> Path:
    p = Path(os.environ.get("INLAB_RUN_STORE")
             or Path(__file__).parent / ".runs").expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return p


def _run_path(run_ref: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", run_ref)
    return _store() / f"{safe}.json"


def _load_run(run_ref: str) -> dict[str, Any]:
    p = _run_path(run_ref)
    return json.loads(p.read_text()) if p.exists() else {}


def _save_run(run_ref: str, patch: dict[str, Any]) -> dict[str, Any]:
    rec = _load_run(run_ref)
    rec.update(patch)
    rec["run_ref"] = run_ref
    _run_path(run_ref).write_text(json.dumps(rec, indent=2))
    return rec


def _patient(patient_id: str) -> dict[str, Any]:
    store = os.environ.get("INLAB_PATIENT_STORE", "")
    p = Path(store).expanduser() / f"{patient_id}.json"
    if not p.exists():
        raise ValueError(f"unknown patient: {patient_id}")
    return json.loads(p.read_text())


# ── routes ───────────────────────────────────────────────────────────────────
@router.get("/personas")
def personas():
    """The styles a clinician can pick: message personas + judge rubrics."""
    root = _persona_root()
    return {
        "root": str(root) if root else None,
        "message": _personas(REPORT_SKILL),
        "judge": _personas(JUDGE_SKILL),
        "reason": None if root else
            "persona root not found — set INLAB_PERSONA_ROOT to the "
            "skills/task/4_individual dir",
    }


@router.post("/message")
async def message(body: dict[str, Any]):
    """② compose — forecast in, patient message out. Never sees `observed`."""
    patient_id = body.get("patient_id") or ""
    persona = body.get("persona") or "patient-friendly"
    resp = body.get("response") or {}
    run_ref = body.get("run_ref") or f"{patient_id}-{persona}"
    if not resp:
        return JSONResponse({"error": "no prediction response supplied — run ▶ Run first"},
                            status_code=400)
    files = _persona_files(REPORT_SKILL, persona)
    if not files:
        return JSONResponse({"error": f"unknown message style: {persona}"}, status_code=404)
    system, meta = files

    try:
        patient = _patient(patient_id)
        blind = _blind(resp)
        user_msg = _compose_user_msg(patient, blind, body.get("anchor"))
        text = await _ask(system, user_msg, meta.get("model"))
    except Exception as e:  # noqa: BLE001 — surface the cause, don't 500 blankly
        return JSONResponse({"error": f"compose failed: {e}"}, status_code=500)

    xml = _tag(text, "report")
    parsed = _xml_to_dict(xml) if xml else {}
    report = parsed.get("report", {}) if isinstance(parsed, dict) else {}
    nl = report.get("nl") if isinstance(report, dict) else None

    # Two audiences share this route — the abstract promises messages to patients
    # AND care providers, so they are the same engine with a different persona.
    # They are stored apart so a run can hold both at once.
    slot = body.get("slot") or (
        "interpretation" if (meta.get("audience") or "").startswith("care") else "message")

    out = {
        "run_ref": run_ref,
        "slot": slot,
        "persona": persona,
        "persona_meta": meta,
        "nl": nl or (text.strip() if not xml else ""),
        "report": report,
        "prompt": user_msg,
        "blinded": True,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _save_run(run_ref, {"patient_id": patient_id, slot: out})
    return out


@router.post("/judge")
async def judge(body: dict[str, Any]):
    """③ LLM-as-judge — scores the MESSAGE, not the forecast. Also blind."""
    rubric = body.get("rubric") or "patient-comprehension"
    run_ref = body.get("run_ref") or ""
    rec = _load_run(run_ref)
    msg = body.get("message") or rec.get("message")
    if not msg:
        return JSONResponse({"error": "no message to judge — compose one first"},
                            status_code=400)
    files = _persona_files(JUDGE_SKILL, rubric)
    if not files:
        return JSONResponse({"error": f"unknown rubric: {rubric}"}, status_code=404)
    system, meta = files

    try:
        blind = _blind(body.get("response") or rec.get("response") or {})
        user_msg = _judge_user_msg(msg.get("nl") or "", msg.get("report") or {}, blind)
        text = await _ask(system, user_msg, meta.get("model"))
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"judge failed: {e}"}, status_code=500)

    xml = _tag(text, "judgment") or _tag(text, "judgement") or _tag(text, "report")
    parsed = _xml_to_dict(xml) if xml else {}
    judgment = next(iter(parsed.values()), {}) if parsed else {}

    out = {
        "run_ref": run_ref,
        "rubric": rubric,
        "dimensions": meta.get("dimensions") or [],
        "judgment": judgment,
        "raw": None if xml else text.strip(),
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if run_ref:
        _save_run(run_ref, {"judge": out})
    return out


@router.post("/feedback")
def feedback(body: dict[str, Any]):
    """④ the human's verdict. NOT a run: append-only, attributed, never replaced —
    this is the clinical-expert record the LLM judge is measured against."""
    run_ref = (body.get("run_ref") or "").strip()
    verdict = (body.get("verdict") or "").strip()
    if not run_ref or not verdict:
        return JSONResponse({"error": "run_ref and verdict are required"}, status_code=400)
    entry = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "by": body.get("by") or "clinician",
        "verdict": verdict,                      # agree | disagree | unsafe | …
        "note": body.get("note") or "",
        "agrees_with_judge": body.get("agrees_with_judge"),
    }
    rec = _load_run(run_ref)
    rec.setdefault("feedback", []).append(entry)
    rec["run_ref"] = run_ref
    _run_path(run_ref).write_text(json.dumps(rec, indent=2))
    return {"run_ref": run_ref, "n": len(rec["feedback"]), "entry": entry}


@router.get("/runrecord")
def runrecord(run_ref: str):
    """The whole chain for one run: prediction ▸ message ▸ judge ▸ feedback."""
    return _load_run(run_ref) or {"run_ref": run_ref, "empty": True}
