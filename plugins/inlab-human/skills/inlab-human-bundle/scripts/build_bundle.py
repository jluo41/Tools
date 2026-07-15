#!/usr/bin/env python3
"""build_bundle.py — deterministic review_bundle.json builder (v0.1).

Source mode `--from-examples`: builds one case per examples/example_NNN/ in an
Endpoint_Set package — payload.json becomes the clinician-facing presentation,
the LIVE endpoint response becomes model_output, df_case_example.json's
ground_truth_label becomes gold. (CaseStore mode lands in a later version.)

The narrator agent's text is merged afterwards with --merge-narratives (the
narrative is the ONLY LLM-produced field; everything here stays deterministic).

    python3 build_bundle.py --endpoint-path <Endpoint_Set dir> --endpoint-url URL \
        --bundle-id adhd-demo-r1 --out review_bundle.json [--seed 41]
    python3 build_bundle.py --merge-narratives narratives.json --out review_bundle.json

Contract: ../../../ref/review-bundle-schema.md (v0.1). Stdlib only.
"""
import argparse
import json
import os
import random
import sys
from datetime import datetime, date


# ---------------------------------------------------------------- helpers
def _ym(dt_str):
    """Coarsen any datetime string to YYYY-MM (de-id hygiene)."""
    if not dt_str or str(dt_str) in ("NaT", "None", "nan"):
        return None
    return str(dt_str)[:7]


def _age_at(birth, obs):
    try:
        b = datetime.fromisoformat(str(birth)[:10]).date()
        o = datetime.fromisoformat(str(obs)[:10]).date()
        return (o - b).days // 365
    except (ValueError, TypeError):
        return None


def build_presentation(payload, obs_dt):
    """payload source_tables -> presentation block. De-id rules: pseudonymous
    case ids only, dates coarsened to YYYY-MM, no zipcode/geo, age in years."""
    st = payload.get("source_tables", {})
    ptt = (st.get("Ptt") or [{}])[0]

    demographics = {
        "age_years": _age_at(ptt.get("BirthDate"), obs_dt),
        "sex": ptt.get("GenderAbbr") or ptt.get("Gender"),
        "race": ptt.get("FirstRace"),
        "ethnicity": ptt.get("EthnicGroup"),
        "language": ptt.get("Language"),
    }

    problem_list = [{
        "icd10": d.get("ICD10Code"),
        "label": d.get("DxName"),
        "primary": d.get("PrimaryDxYN"),
        "chronic": d.get("DxChronicYN"),
        "month": _ym(d.get("EncContactDate")),
    } for d in st.get("Dx", [])]

    medications = [{
        "name": d.get("MedDisplayName") or d.get("MedName"),
        "dose": d.get("Dose"), "unit": d.get("Unit"), "frequency": d.get("Frequency"),
        "start_month": _ym(d.get("StartDate")), "end_month": _ym(d.get("EndDate")),
    } for d in st.get("Med", [])]

    measurements = [{
        "name": d.get("MeasDispName") or d.get("MeasName"),
        "value": d.get("MeasValue"),
        "month": _ym(d.get("RecordedTime") or d.get("EncContactDate")),
    } for d in st.get("Vital", []) + st.get("Lab", [])]

    questionnaires = [{
        "form": d.get("FormName"), "question": d.get("Question"),
        "answer": d.get("QuestAnswer"), "month": _ym(d.get("EncContactDate")),
    } for d in st.get("Questionnaire", [])]

    visit_history = sorted([{
        "month": _ym(d.get("ContactDate")), "type": d.get("EncType"),
        "department": d.get("DepSpeciality") or d.get("DepartmentName"),
    } for d in st.get("Encounter", [])], key=lambda r: r["month"] or "")

    return {
        "demographics": demographics,
        "visit_context": f"index visit {_ym(obs_dt)}",
        "problem_list": problem_list,
        "medications": medications,
        "measurements": measurements,
        "questionnaires": questionnaires,
        "visit_history": visit_history,
    }


def extract_model_output(response):
    """Endpoint response -> model_output block. Score copied verbatim."""
    pred = response["models"][0]["predictions"][0]
    score_keys = [k for k in pred if "score" in k.lower()]
    score = pred[score_keys[0]] if score_keys else None
    band = (pred.get("risk_level") or "").lower() or None
    return {
        "risk_score": score,
        "risk_band": band,
        "attribution_available": False,   # this endpoint returns no SHAP (yet)
        "shap_top": [],
        "narrative": "",                  # merged later via --merge-narratives
        "narrative_agent": None,
        "endpoint_response_raw": response,
    }


def validate(bundle):
    """Hard errors break the freeze; warnings are reported but tolerated in
    demo (from-examples) mode, where sampling can't be designed."""
    errs, warns = [], []
    seen_wrong = False
    for c in bundle["cases"]:
        for block in ("presentation", "model_output", "gold"):
            if block not in c:
                errs.append(f"{c['case_id']}: missing {block}")
        if c["gold"].get("outcome") not in (0, 1):
            errs.append(f"{c['case_id']}: gold.outcome must be 0/1")
        txt = json.dumps(c["presentation"]).lower()
        for leak in ("risk_score", "shap", "risk_level", "patientid", "zipcode"):
            if leak in txt:
                errs.append(f"{c['case_id']}: presentation leaks '{leak}'")
        band, out = c["strata"]["pred_band"], c["strata"]["outcome"]
        if (band == "high" and out == "neg") or (band == "low" and out == "pos") \
           or (band == "med" and out == "pos"):
            seen_wrong = True
    if not seen_wrong:
        warns.append("no model-wrong/miss cell in sample — clinicians will only "
                     "see cases the model got right; fine for a demo, not a study")
    return errs, warns


# ---------------------------------------------------------------- modes
def from_examples(args):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "mcp-servers", "endpoint-predict"))
    from server import tool_predict, tool_ping  # same code path as the MCP tool

    ep = os.path.abspath(args.endpoint_path)
    ping = tool_ping({"endpoint_url": args.endpoint_url})
    ex_root = os.path.join(ep, "examples")
    names = sorted(d for d in os.listdir(ex_root) if d.startswith("example_"))
    if args.max_cases:
        names = names[: args.max_cases]

    cases, build_log = [], []
    for i, name in enumerate(names):
        exd = os.path.join(ex_root, name)
        payload = json.load(open(os.path.join(exd, "payload.json")))
        info = json.load(open(os.path.join(exd, "df_case_example.json")))
        resp = tool_predict({"payload": payload, "endpoint_url": args.endpoint_url})["response"]
        mo = extract_model_output(resp)
        gold_outcome = int(info["ground_truth_label"])
        band = mo["risk_band"] or "unknown"
        band = {"moderate": "med"}.get(band, band)
        case = {
            "case_id": f"C{i:03d}",
            "strata": {"pred_band": band, "outcome": "pos" if gold_outcome else "neg"},
            "presentation": build_presentation(payload, info.get("ObsDT")),
            "model_output": mo,
            "gold": {
                "outcome": gold_outcome,
                "outcome_detail": "retrospective label from CaseStore (packaged example)",
                "label_source": "df_case_example.ground_truth_label",
            },
            "_source_example": name,     # provenance; stripped from reader display
        }
        cases.append(case)
        build_log.append({"case_id": case["case_id"], "example": name,
                          "risk_score": mo["risk_score"], "gold": gold_outcome})

    random.Random(args.seed).shuffle(cases)

    bundle = {
        "schema_version": "0.1",
        "bundle_id": args.bundle_id,
        "created": datetime.now().astimezone().isoformat(),
        "model": {
            "endpoint_name": ping["ping"].get("endpoint"),
            "endpoint_version": ping["ping"].get("version"),
            "endpoint_url_used": ping["endpoint_url"],
            "task_description": args.task_description,
            "horizon": args.horizon,
        },
        "sampling": {
            "source": f"Endpoint_Set packaged examples: {ep}",
            "design": "all packaged examples (demo mode)",
            "n_cases": len(cases),
            "note": "v0.1 demo sampling; stratified CaseStore sampling in a later version",
        },
        "blinding": {"case_order": f"shuffled, seed={args.seed}", "gold_hidden": True},
        "cases": cases,
    }

    errs, warns = validate(bundle)
    with open(args.out, "w") as f:
        json.dump(bundle, f, indent=2)
    log_path = args.out.replace(".json", ".build_log.json")
    with open(log_path, "w") as f:
        json.dump({"build_log": build_log, "validation_errors": errs,
                   "validation_warnings": warns}, f, indent=2)

    print(f"bundle: {args.out}  cases={len(cases)}")
    print(f"build log: {log_path}")
    for w in warns:
        print(f"WARNING: {w}")
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("validation: OK")
    return 0


def merge_narratives(args):
    bundle = json.load(open(args.out))
    narr = json.load(open(args.merge_narratives))  # {case_id: text} or {case_id: {narrative, agent}}
    n = 0
    for c in bundle["cases"]:
        v = narr.get(c["case_id"])
        if v is None:
            continue
        if isinstance(v, str):
            c["model_output"]["narrative"] = v
        else:
            c["model_output"]["narrative"] = v.get("narrative", "")
            c["model_output"]["narrative_agent"] = v.get("agent")
        n += 1
    with open(args.out, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"merged {n} narratives into {args.out}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint-path")
    ap.add_argument("--endpoint-url")
    ap.add_argument("--bundle-id", default="demo-r1")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=41)
    ap.add_argument("--max-cases", type=int)
    ap.add_argument("--task-description", default="")
    ap.add_argument("--horizon", default="")
    ap.add_argument("--merge-narratives")
    a = ap.parse_args()
    if a.merge_narratives:
        sys.exit(merge_narratives(a))
    if not a.endpoint_path:
        ap.error("--endpoint-path required (or use --merge-narratives)")
    sys.exit(from_examples(a))
