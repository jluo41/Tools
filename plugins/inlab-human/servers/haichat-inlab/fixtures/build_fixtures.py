"""SYNTHETIC fixtures for the In-Lab Console: no real person, record or study is in here.

Writes, under fixtures/ (beside this file):

    store/<dataset>/patients/<human_id>.json   three data types, five synthetic humans each (the json copy)
    recstore/SynthCGM_v0/                      the glucose humans as a haipipe record set, read in place
    casestore/SynthCGM_v0/@v0CaseSet-Meal/     a cooked case set: one case per meal, with two facets
    projects/examples-0-synthetic/Project-Synthetic/tasks/   a ladder: one Block, two Jobs, four Tasks
    endpoints/<package>/                       two packaged endpoints the engine can list and card
    registry.json                              {package: stub endpoint URL}

The record store and the case set follow the layouts the haipipe Record and Case stages write
(RecordSet._save_data_to_disk, CaseSet._save_data_to_disk); they need pyarrow.

    SynthCGM_v0       a 5-minute glucose timeline with meals, exercise and insulin (forecast endpoint)
    SynthDialogue_v0  a doctor–patient visit: encounter, dialogue, note (risk-score endpoint)
    SynthReview_v0    a physician profile and its reviews (no endpoint: browse and cases only)

Every value is generated from a fixed seed, so the fixtures are the same on every machine. Run:

    python build_fixtures.py [--port 8192]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYNTH = "SYNTHETIC fixture for the In-Lab Console: generated, no real person or record"
rng = random.Random(261009)

FIRST = ["Avery", "Blake", "Casey", "Drew", "Emery", "Finley", "Gray", "Harper", "Indigo", "Jules"]
LAST = ["Example", "Sample", "Testcase", "Fixture", "Placeholder"]


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1), encoding="utf-8")


def iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%d %H:%M:%S")


# ── SynthCGM_v0 ─────────────────────────────────────────────────────────────────────────────────
def cgm_human(i: int) -> dict:
    pid = f"synth-cgm-{i:03d}"
    start = datetime(2024, 3, 4, 0, 0) + timedelta(days=i)
    n = 2 * 288 + 24                                   # two days and two hours of 5-minute readings
    meals = [(7, 45), (12, 60), (18, 70), (31, 40), (36, 55), (42, 65)]     # (hour from start, carbs g)
    cgm, diet, exer, med = [], [], [], []
    base = 110 + 8 * i
    for k in range(n):
        t = start + timedelta(minutes=5 * k)
        h = 5 * k / 60
        bump = sum(c * 1.1 * math.exp(-((h - mh) - 1.0) ** 2 / 0.8) for mh, c in meals if h >= mh)
        bg = base + 18 * math.sin(2 * math.pi * h / 24) + bump + rng.gauss(0, 4)
        cgm.append({"PatientID": pid, "DT_s": iso(t), "BGValue": round(bg, 1)})
    for mh, carbs in meals:
        t = start + timedelta(hours=mh)
        diet.append({"PatientID": pid, "DT_s": iso(t), "FoodName": rng.choice(["oatmeal", "sandwich", "rice bowl",
                     "pasta", "salad", "yogurt"]), "Carbs": carbs, "Calories": carbs * 9})
        med.append({"PatientID": pid, "DT_s": iso(t - timedelta(minutes=10)), "MedicationID": "rapid-insulin",
                    "medication": "rapid-acting insulin (synthetic)", "Dose": round(carbs / 10, 1)})
    for eh in (10, 34):
        exer.append({"PatientID": pid, "DT_s": iso(start + timedelta(hours=eh)), "ExerciseType": "walking",
                     "ExerciseIntensity": "moderate", "ExerciseDuration": 30})
    last = cgm[-1]["DT_s"]
    tables = {"Ptt": [{"PatientID": pid, "Gender": rng.choice(["F", "M"]), "BirthYear": 1960 + 3 * i}],
              "CGM": cgm, "Diet": diet, "Exercise": exer, "Medication": med}
    record = {f"Rec.{k}5Min": {"columns": list(v[0].keys()), "n_rows": len(v), "rows": v}
              for k, v in tables.items() if k != "Ptt"}
    return {
        "_synthetic": SYNTH, "patient_id": pid,
        "summary": {"cohort": "SynthCGM", "birth_date": f"{1960 + 3 * i}-01-01", "sex": tables["Ptt"][0]["Gender"],
                    "race": None, "table_counts": {k: len(v) for k, v in tables.items()}, "cgm_last": last,
                    "anchor": last},
        "provenance": [{"endpoint_package": "synth_cgm_forecast_v0001",
                        "triggers": [{"PID": pid, "ObsDT": last}]}],
        "source_tables": tables,
        "layers": {
            "raw": {"files": [{"name": f"{pid}_cgm_export.csv", "bytes": 64 * len(cgm),
                               "preview": "time,glucose_mg_dl\n" + "\n".join(f"{r['DT_s']},{r['BGValue']}"
                                                                          for r in cgm[:12])}]},
            "record": {"tables": record},
        },
    }


# ── SynthDialogue_v0 ────────────────────────────────────────────────────────────────────────────
VISITS = [
    ("follow-up for blood pressure", "I have been taking the pill every morning but forget on weekends."),
    ("new cough for two weeks", "It is worse at night and I do not have a fever."),
    ("knee pain after running", "It hurts going down stairs, less on flat ground."),
    ("medication review", "The new tablet makes me a little dizzy in the morning."),
    ("annual check-up", "Nothing new, just here for the yearly visit."),
]


def dialogue_human(i: int) -> dict:
    pid = f"synth-dlg-{i:03d}"
    day = datetime(2024, 5, 1) + timedelta(days=7 * i)
    cc, said = VISITS[i % len(VISITS)]
    turns = [f"[doctor] What brings you in today?", f"[patient] A {cc}.", f"[doctor] Tell me more.",
             f"[patient] {said}", "[doctor] Thank you. Let us review your medications and set a plan.",
             "[patient] That sounds good."]
    enc = [{"EncounterID": f"enc-{i:03d}", "ContactDate": day.strftime("%Y-%m-%d"), "EncType": "Office visit",
            "DepSpeciality": "Family medicine", "ChiefComplaint": cc}]
    dlg = [{"EncounterID": f"enc-{i:03d}", "ContactDate": day.strftime("%Y-%m-%d"), "Dialogue": "\n".join(turns)}]
    note = [{"EncounterID": f"enc-{i:03d}", "ContactDate": day.strftime("%Y-%m-%d"),
             "Note": f"S: {cc}; {said}\nO: vitals within normal range (synthetic)\nA: see plan\nP: follow up in 4 weeks"}]
    vital = [{"MeasDispName": "Blood pressure", "MeasName": "BP", "MeasValue": f"{118 + 4 * i}/{76 + i}",
              "RecordedTime": day.strftime("%Y-%m-%d")}]
    dx = [{"ICD10Code": "Z00.00", "DxName": "General exam (synthetic)", "EncContactDate": day.strftime("%Y-%m-%d")}]
    tables = {"Encounter": enc, "Dialogue": dlg, "Note": note, "Vital": vital, "Dx": dx}
    return {
        "_synthetic": SYNTH, "patient_id": pid,
        "summary": {"cohort": "SynthDialogue", "birth_date": f"{1950 + 6 * i}-06-15", "sex": rng.choice(["F", "M"]),
                    "race": None, "table_counts": {k: len(v) for k, v in tables.items()}},
        "provenance": [{"endpoint_package": "synth_risk_v0001",
                        "triggers": [{"PID": pid, "ObsDT": day.strftime("%Y-%m-%d")}]}],
        "source_tables": tables,
        "layers": {"record": {"tables": {f"Rec.{k}": {"columns": list(v[0].keys()), "n_rows": len(v), "rows": v}
                                         for k, v in tables.items()}}},
    }


# ── SynthReview_v0 ──────────────────────────────────────────────────────────────────────────────
REVIEWS = ["Listened carefully and explained the plan clearly.", "Long wait, but the visit itself was thorough.",
           "Friendly staff; the doctor seemed rushed.", "Answered every question without hurry.",
           "Hard to reach the office by phone.", "Kind, patient, and clear about next steps."]


def review_human(i: int) -> dict:
    pid = f"synth-phy-{i:03d}"
    name = f"Dr. {FIRST[i]} {LAST[i % len(LAST)]}"
    profile = [{"ProviderID": pid, "DisplayName": name, "Specialty": rng.choice(["Family medicine", "Cardiology",
                "Endocrinology"]), "Credential": "MD"}]
    reviews = [{"ReviewID": f"{pid}-r{k}", "ContactDate": f"2024-0{1 + k}-1{i}", "Rating": rng.randint(2, 5),
                "ReviewText": rng.choice(REVIEWS)} for k in range(4)]
    tables = {"Profile": profile, "Review": reviews}
    return {
        "_synthetic": SYNTH, "patient_id": pid,
        "summary": {"cohort": "SynthReview", "birth_date": None, "sex": None, "race": None,
                    "table_counts": {k: len(v) for k, v in tables.items()},
                    "not_scoreable_reason": "no endpoint scores physicians in the synthetic fixtures"},
        "provenance": [],
        "source_tables": tables,
        "layers": {"record": {"tables": {f"Rec.{k}": {"columns": list(v[0].keys()), "n_rows": len(v), "rows": v}
                                         for k, v in tables.items()}}},
    }


# ── the two packaged endpoints ──────────────────────────────────────────────────────────────────
def endpoints(root: Path) -> None:
    cgm = root / "synth_cgm_forecast_v0001"
    write(cgm / "manifest.json", {
        "_synthetic": SYNTH, "endpoint_name": "synth-cgm-forecast", "endpoint_version": "v0001",
        "created_at": "2026-10-09T00:00:00", "deployment": {"kind": "stub", "host": "loopback"},
        "inference_functions": {"Input2SrcFn": "CGMDecoder (synthetic stub)", "TrigFn": "last CGM reading",
                                "InferenceArgs": {"mode": "forecast", "horizon": 12, "obs_dt_index": 287}}})
    write(cgm / "meta.json", {"modelMetadata": [{"predictionType": "glucose forecast", "unit": "mg/dL"}],
                              "inputSchema": {"CGM": ["PatientID", "DT_s", "BGValue"]}})
    write(cgm / "model" / "config.json", {"modelinstance_set_name": "SynthCGM-forecast", "aidata_name": "SynthCGM",
                                          "ModelArgs": {"model_tuner_name": "stub", "model_tuner_args": {
                                              "model_name_or_path": "none (stub)", "max_seq_length": 300,
                                              "value_range": [40, 400], "architecture_config": {"kind": "stub"}}}})
    write(cgm / "model" / "prefn_config.json", {
        "InputArgs": {"input_casefn_list": ["CGMValueBf24h"], "input_args": {"window_build": {"obs_dt_index": 287}}},
        "TriggerArgs": {"Trigger": "CGM5MinLTS", "min_segment_length": 576, "max_consecutive_missing": 3, "stride": 1}})
    risk = root / "synth_risk_v0001"
    write(risk / "manifest.json", {
        "_synthetic": SYNTH, "endpoint_name": "synth-risk", "endpoint_version": "v0001",
        "created_at": "2026-10-09T00:00:00", "deployment": {"kind": "stub", "host": "loopback"},
        "inference_functions": {"Input2SrcFn": "SourceTables (synthetic stub)", "TrigFn": "encounter date"}})
    write(risk / "meta.json", {"modelMetadata": [{"predictionType": "risk score", "unit": "probability"}]})
    write(risk / "examples" / "example_000" / "payload.json", {
        "models": "synth-risk/v0001", "source_tables": {"Encounter": [], "Dialogue": [], "Vital": []},
        "dataframe_records": [{"PID": "synth-dlg-000", "ObsDT": "2024-05-01"}]})


# ── the glucose humans as a record store, and their cooked cases ─────────────────────────────────
GRAIN = "5Min"


def parquet(path: Path, rows: list[dict], types: dict | None = None) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq
    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(rows)
    for col, t in (types or {}).items():
        if col in table.column_names:
            table = table.set_column(table.column_names.index(col), col, table.column(col).cast(t))
    pq.write_table(table, path)


def record_store(root: Path, humans: list[dict]) -> None:
    """One record set in the Record stage's layout: a Human table and one Record per source table."""
    import pyarrow as pa
    rs = root / "SynthCGM_v0"
    human = "HmSynth"
    write(rs / "manifest.json", {"_synthetic": SYNTH, "record_set_name": "SynthCGM_v0",
                                 "source_set_manifest": {"source_name": "SynthCGM", "cohort": "SynthCGM"},
                                 "Partition_Args": {"record_set_label": 1}, "structure": {
                                     "humans": [human],
                                     "records": [[human, "Ptt"]] + [[human, f"{t}{GRAIN}"] for t in
                                                                    ("CGM", "Diet", "Exercise", "Medication")]}})
    parquet(rs / f"Human-{human}" / "Human2RawNum.parquet",
            [{"PID": h["patient_id"], "PatientID": h["patient_id"], "record_set_label": 1,
              **{f"{t}_n": n for t, n in h["summary"]["table_counts"].items()}} for h in humans])
    ts = pa.timestamp("s")
    for table in ("Ptt", "CGM", "Diet", "Exercise", "Medication"):
        name = table if table == "Ptt" else f"{table}{GRAIN}"
        rows, k = [], 0
        for h in humans:
            for r in h["source_tables"][table]:
                row = {"PID": h["patient_id"], **r}
                if "DT_s" in row:
                    row["DT_s"] = datetime.strptime(row["DT_s"], "%Y-%m-%d %H:%M:%S")
                    row[f"{name}ID"] = k
                    k += 1
                rows.append(row)
        parquet(rs / f"Record-{human}.{name}" / "RecAttr.parquet", rows, {"DT_s": ts})
        parquet(rs / f"Record-{human}.{name}" / "RecIndex.parquet",
                [{"PID": h["patient_id"], "n": len(h["source_tables"][table])} for h in humans])


def case_store(root: Path, humans: list[dict]) -> None:
    """One cooked case set in the Case stage's layout: a case per meal, with the two hours of glucose before
    it and the meal itself as facets (row for row with df_case)."""
    import pyarrow as pa
    cs = root / "SynthCGM_v0" / "@v0CaseSet-Meal"
    write(cs / "manifest.json", {"_synthetic": SYNTH, "case_set_name": "@v0CaseSet-Meal",
                                 "record_set_manifest": {"record_set_name": "SynthCGM_v0"},
                                 "trigger_info": {"TriggerName": "Meal", "TriggerArgs": {"Trigger": "Meal"}},
                                 "casefn_info": {"CaseFn_list": ["CGMBf2h", "DietAt"]}})
    base, before, meal = [], [], []
    for h in humans:
        cgm = [(datetime.strptime(r["DT_s"], "%Y-%m-%d %H:%M:%S"), r["BGValue"]) for r in h["source_tables"]["CGM"]]
        for d in h["source_tables"]["Diet"]:
            at = datetime.strptime(d["DT_s"], "%Y-%m-%d %H:%M:%S")
            base.append({"PID": h["patient_id"], "ObsDT": at})
            before.append({"PID": h["patient_id"],
                           "CGMBf2h--val": [v for t, v in cgm if at - timedelta(hours=2) <= t < at]})
            meal.append({"PID": h["patient_id"], "DietAt--carbs": d["Carbs"], "DietAt--food": d["FoodName"]})
    parquet(cs / "df_case.parquet", base, {"ObsDT": pa.timestamp("s")})
    parquet(cs / "@CGMBf2h.parquet", before)
    parquet(cs / "@DietAt.parquet", meal)


# ── a project ladder for the Tasks view ─────────────────────────────────────────────────────────
TASKS = [  # (job, task, scope line or None, task-type, has results)
    ("j01_example_cohort_job", "t01_example_cohort_summary", None, "data", True),
    ("j01_example_cohort_job", "t02_example_cohort_model", None, "fit", False),
    ("j02_example_individual_job", "t01_example_one_person_readout", "individual", "eval", True),
    ("j02_example_individual_job", "t02_example_one_person_check", "individual", "eval", False),
]


def projects(root: Path) -> None:
    blk = root / "examples-0-synthetic" / "Project-Synthetic" / "tasks" / "b01_example_block"
    blk.mkdir(parents=True, exist_ok=True)
    (blk / "board.md").write_text("# Synthetic example block\n\nboard-kind: task-block\n", encoding="utf-8")
    for job, task, scope, ttype, done in TASKS:
        t = blk / job / task
        t.mkdir(parents=True, exist_ok=True)
        head = [f"# Synthetic example: {task[4:].replace('_', ' ')}", "", f"task-type: {ttype}", f"task: {task}",
                f"job: {job}"] + ([f"scope: {scope}"] if scope else [])
        (t / f"{task}.md").write_text("\n".join(head) + "\n\n## Opening\n\nA placeholder Task.\n", encoding="utf-8")
        (t / "runs").mkdir(exist_ok=True)
        if done:
            (t / "results" / "r01").mkdir(parents=True, exist_ok=True)
            (t / "results" / "r01" / "synthetic.txt").write_text(SYNTH + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8192, help="the stub endpoint's port")
    a = ap.parse_args()
    for d in ("store", "endpoints", "recstore", "casestore", "projects"):
        shutil.rmtree(HERE / d, ignore_errors=True)
    glucose = []
    for ds, make in (("SynthCGM_v0", cgm_human), ("SynthDialogue_v0", dialogue_human),
                     ("SynthReview_v0", review_human)):
        for i in range(5):
            h = make(i)
            write(HERE / "store" / ds / "patients" / f"{h['patient_id']}.json", h)
            if ds == "SynthCGM_v0":
                glucose.append(h)
    record_store(HERE / "recstore", glucose)
    case_store(HERE / "casestore", glucose)
    projects(HERE / "projects")
    endpoints(HERE / "endpoints")
    url = f"http://127.0.0.1:{a.port}"
    write(HERE / "registry.json", {"synth_cgm_forecast_v0001": url, "synth_risk_v0001": url})
    print(f"fixtures written under {HERE.name}/: 3 datasets × 5 humans, a record set, a case set "
          f"({sum(len(h['source_tables']['Diet']) for h in glucose)} cases), a 4-Task ladder, 2 endpoints, "
          f"registry → {url}")


if __name__ == "__main__":
    main()
