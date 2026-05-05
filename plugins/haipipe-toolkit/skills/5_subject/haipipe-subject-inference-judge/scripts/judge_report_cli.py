"""End-to-end demo: judge an existing report.

Pipeline:
  1. load_report_json(--report-dir)
  2. load_persona(--persona)
  3. judge_report(report, system_prompt, model)
  4. write judgment.json + response.xml + meta.json into the report dir

    python judge_report_cli.py \
        --report-dir _WorkSpace/7-AgentWorkspace/reports/18/patient-friendly/<ts>/ \
        --persona safety-review

    python judge_report_cli.py \
        --report-dir _WorkSpace/7-AgentWorkspace/reports/18/patient-friendly/<ts>/ \
        --persona patient-comprehension
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "src"))

from judge_report import judge_report, load_report_json  # noqa: E402
from persona_loader import load_persona  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-dir", required=True,
                    help="path to a report folder (containing report.json) or "
                         "directly to a report.json file")
    ap.add_argument("--persona", default="patient-comprehension",
                    help="judge persona name (under personas/) or absolute path")
    ap.add_argument("--model", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    log = (lambda *a, **k: None) if args.quiet else print

    report_path = Path(args.report_dir)
    report = load_report_json(report_path)
    report_dir = report_path if report_path.is_dir() else report_path.parent
    log(f"📥  loaded report   ← {report_dir}")
    log(f"     subject: {report['basics']['subject_id']}  "
        f"verdict: {report['interpretation']['verdict']}  "
        f"safety: {report['interpretation']['safety_flag']}")

    persona = load_persona(args.persona)
    model = args.model or persona["meta"].get("model") or "claude-haiku-4-5-20251001"
    log(f"⚖️  judge persona   : {persona['persona_name']}  "
        f"rubric={persona['meta'].get('rubric')}  model={model}")

    log("🤖  running judge (Claude SDK) ...")
    judgment, raw_text, telemetry = judge_report(
        report,
        system_prompt=persona["system_prompt"],
        judge_persona_name=persona["persona_name"],
        model=model,
    )

    out_subdir = report_dir / f"judge_{persona['persona_name']}"
    out_subdir.mkdir(parents=True, exist_ok=True)
    (out_subdir / "judgment.json").write_text(judgment.model_dump_json(indent=2))
    (out_subdir / "response.xml").write_text(raw_text)
    (out_subdir / "meta.json").write_text(json.dumps({
        "judge_persona": persona["persona_name"],
        "judge_persona_dir": persona["persona_dir"],
        "report_dir": str(report_dir),
        "telemetry": telemetry,
        "ts": datetime.now().isoformat(timespec="seconds"),
    }, indent=2, default=str))

    log(f"📂  wrote → {out_subdir}")
    log()
    log("──────────  JUDGMENT  ──────────")
    log(f"verdict: {judgment.overall_verdict}   "
        f"score: {judgment.overall_score:.2f}")
    for name, dim in judgment.rubric_dimensions.items():
        log(f"  {name:<28s}  {dim.score}/5   {dim.reasoning}")
    if judgment.issues:
        log()
        log("issues:")
        for i in judgment.issues:
            log(f"  [{i.severity}] {i.location}: {i.issue}")
            if i.suggestion:
                log(f"      → {i.suggestion}")
    log()
    log("summary:")
    log(f"  {judgment.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
