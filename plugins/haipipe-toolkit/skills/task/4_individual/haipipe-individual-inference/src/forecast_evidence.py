"""Bind report evidence and compare the selected forecast without an LLM."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from statistics import mean


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def forecast_facts(forecast: dict) -> dict:
    models = forecast.get("models") or []
    if len(models) != 1:
        raise ValueError("Report requires exactly one selected forecast model")
    windows = models[0].get("forecast") or []
    if not windows:
        raise ValueError("No forecast windows")
    values = [float(v) for v in windows[-1].get("y_pred_h24", [])]
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError("Selected forecast has no finite trajectory")
    low, high = min(values) < 70, max(values) > 300
    flag = "hypo_and_hyper_risk" if low and high else "hypo_risk" if low else "hyper_risk" if high else "none"
    return {
        "selection": {"model_index": 0, "window_index": len(windows) - 1,
                      "rule": "last_returned_window"},
        "summary": {"n_windows": len(windows), "horizon_minutes": len(values) * 5,
                    "pred_min": round(min(values), 2), "pred_max": round(max(values), 2),
                    "pred_mean": round(mean(values), 2)},
        "expected_safety_flag": flag,
    }


def load_ground_truth(report_dir: Path, report: dict, *, report_path: Path | None = None) -> dict:
    """Missing legacy evidence stays unavailable; a mismatched bundle fails closed."""
    forecast_path, meta_path = report_dir / "forecast.json", report_dir / "meta.json"
    if not meta_path.is_file():
        return {"status": "unavailable", "reason": "meta.json missing"}
    meta = json.loads(meta_path.read_text())
    binding = meta.get("evidence_binding")
    if not binding and meta.get("schema") == "haipipe-report-bundle/v1":
        raise ValueError("Modern report bundle is missing evidence_binding")
    if not binding:
        return {"status": "unavailable", "reason": "legacy report has no evidence binding"}
    if not forecast_path.is_file():
        raise ValueError("Bound forecast.json is missing")
    actual_report_path = report_path or report_dir / "report.json"
    for name, path in (("forecast", forecast_path), ("report", actual_report_path)):
        if not path.is_file():
            raise ValueError(f"Bound {name} file is missing")
        if file_sha256(path) != binding.get(f"{name}_sha256"):
            raise ValueError(f"{name}.json differs from the report evidence binding")
    if json.loads(actual_report_path.read_text()) != report:
        raise ValueError("Report object differs from its bound file")
    forecast = json.loads(forecast_path.read_text())
    facts = forecast_facts(forecast)
    if facts["selection"] != binding.get("selection"):
        raise ValueError("Selected forecast window differs from the report evidence binding")
    summary = report.get("forecast_summary") or {}
    mismatches = []
    for key, expected in facts["summary"].items():
        actual = summary.get(key)
        if not isinstance(actual, (float, int)) or not math.isclose(actual, expected, abs_tol=0.011, rel_tol=0):
            mismatches.append({"field": f"forecast_summary.{key}", "expected": expected, "actual": actual})
    actual = (report.get("interpretation") or {}).get("safety_flag")
    if actual != facts["expected_safety_flag"]:
        mismatches.append({"field": "interpretation.safety_flag", "expected": facts["expected_safety_flag"], "actual": actual})
    return {"status": "verified_binding", "facts": facts, "mismatches": mismatches,
            "forecast": forecast, "source_observation": meta.get("source_observation"),
            "limitation": "Last returned window per endpoint ordering contract; chronology is not independently established without window timestamps."}
