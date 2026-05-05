"""End-to-end demo: subject + persona → report.

Pipeline:
  1. load_patient_ctx(subject)              ← haipipe-subject-inference
  2. build_payload(subject) → POST → forecast  ← haipipe-subject-inference
  3. load_persona(persona)                  ← this skill
  4. compose_report(ctx, forecast, system_prompt, model)  ← this skill
  5. write report.json + report.txt + meta.json

    python make_report_cli.py --subject Subject-18 --persona patient-friendly
    python make_report_cli.py --subject Subject-18 --persona /path/to/custom-persona/
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Sibling skill imports — haipipe-subject-inference owns load_patient + build_payload + client
SKILL_DIR = Path(__file__).resolve().parents[1]
SIBLING_SUBJ_INF = SKILL_DIR.parent / "haipipe-subject-inference" / "src"
sys.path.insert(0, str(SIBLING_SUBJ_INF))
sys.path.insert(0, str(SKILL_DIR / "src"))

from build_payload import build_payload, build_payload_summary  # noqa: E402
from client import call_predict, slice_last_window  # noqa: E402
from compose_report import compose_report  # noqa: E402
from load_patient import load_patient_ctx, summarize_ctx  # noqa: E402
from persona_loader import load_persona  # noqa: E402

DEFAULT_OUTPUT_ROOT = Path("/home/jluo41/WellDoc-SPACE/_WorkSpace/7-AgentWorkspace/reports")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--persona", default="patient-friendly",
                    help="persona name (under personas/) or absolute path")
    ap.add_argument("--endpoint-url", default=None,
                    help="defaults to env CGM_ENDPOINT_URL or http://127.0.0.1:8765/invocations")
    ap.add_argument("--model", default=None,
                    help="override persona's default model")
    ap.add_argument("--output-dir", default=None,
                    help=f"defaults to {DEFAULT_OUTPUT_ROOT}/<subject>/<persona>/<ts>/")
    ap.add_argument("--single-window", action="store_true",
                    help="Slice the endpoint response to only the most recent "
                         "forecast window (anchored at last CGM observation).")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    log = (lambda *a, **k: None) if args.quiet else print

    # ── 1. load patient ctx
    log("📥  loading patient context ...")
    ctx = load_patient_ctx(args.subject)
    ctx_summary = summarize_ctx(ctx)
    log(f"     {ctx_summary['subject_id']}  ({ctx_summary['dataset']})")
    log(f"     CGM rows: {ctx_summary['tables'].get('CGM', {}).get('rows', 0)}")

    # ── 2. build payload + POST
    log("🌐  hitting prediction endpoint ...")
    payload = build_payload(args.subject)
    forecast_resp = call_predict(payload, endpoint_url=args.endpoint_url)
    if args.single_window:
        forecast_resp = slice_last_window(forecast_resp)
    n_windows = len((forecast_resp.get("models", [{}])[0]).get("forecast", []) or [])
    log(f"     forecast windows: {n_windows}")

    # ── 3. load persona
    log(f"🎭  loading persona {args.persona!r} ...")
    persona = load_persona(args.persona)
    model = args.model or persona["meta"].get("model") or "claude-haiku-4-5-20251001"
    log(f"     persona: {persona['persona_name']}  audience={persona['meta'].get('audience')}")
    log(f"     model:   {model}")

    # ── 4. compose
    log("🤖  composing report (Claude SDK) ...")
    report, raw_text, telemetry = compose_report(
        ctx, forecast_resp,
        system_prompt=persona["system_prompt"],
        model=model,
    )

    # ── 5. write artifacts
    out_dir = Path(args.output_dir) if args.output_dir else (
        DEFAULT_OUTPUT_ROOT
        / ctx_summary["subject_id"]
        / persona["persona_name"]
        / datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "forecast.json").write_text(json.dumps(forecast_resp, indent=2, default=str))
    (out_dir / "report.json").write_text(report.model_dump_json(indent=2))
    (out_dir / "report.txt").write_text(report.nl + "\n")
    (out_dir / "response.xml").write_text(raw_text)
    (out_dir / "meta.json").write_text(
        json.dumps(
            {
                "subject": args.subject,
                "subject_id": ctx_summary["subject_id"],
                "dataset": ctx_summary["dataset"],
                "persona": persona["persona_name"],
                "persona_dir": persona["persona_dir"],
                "endpoint_url": args.endpoint_url,
                "n_forecast_windows": n_windows,
                "telemetry": telemetry,
            },
            indent=2,
            default=str,
        )
    )

    log(f"📂  wrote → {out_dir}")
    log()
    log("──────────  PATIENT MESSAGE  ──────────")
    log(report.nl)
    log("───────────────────────────────────────")
    log(f"verdict={report.interpretation.verdict}  "
        f"confidence={report.interpretation.confidence}  "
        f"safety={report.interpretation.safety_flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
