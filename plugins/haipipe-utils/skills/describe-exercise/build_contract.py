"""
Emit _ExerciseInfo/4-contract: the exnorm/v1 API contract and one worked
specimen per situation, each built from a real row.

Mirrors _FoodInfo/4-contract. The difference is what a specimen IS: food's
contract describes a RECORD, so a specimen is one record. This one describes an
API, so a specimen is a REQUEST AND ITS RESPONSE -- a contract you can only
argue with if both halves are on the page.

GENERATED. Code stays under git in the skill; only data artifacts are written to
_WorkSpace, and every one of them is regenerable:

    source .venv/bin/activate && source env.sh
    Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh   # another shell
    python Tools/plugins/haipipe-utils/skills/describe-exercise/build_contract.py
"""
import glob, json, os, sys, urllib.request
import pandas as pd

URL = os.environ.get("EXNORM_URL", "http://127.0.0.1:8078").rstrip("/")
OUT = "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/4-contract"
LB = 0.45359237

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "exnorm/v1",
    "title": "describe-exercise · one normalized activity",
    "description":
        "The response body of POST /normalize, and one element of the results "
        "array of POST /normalize/batch. FOURTEEN KEYS, ALWAYS ALL FOURTEEN, on "
        "a hit and on a miss alike: a caller never branches on shape, only on "
        "ExerciseConf.",
    "type": "object",
    "additionalProperties": False,
    "required": ["METValue", "ActiveMinutes", "CaloriesBurnedEst",
                 "ActivityResolved", "ActivityCode", "MajorHeading",
                 "METReference", "METScale", "METScaleFactor",
                 "ExerciseSource", "ExerciseConf", "ExerciseBasis",
                 "TypeSource", "TypeConf"],
    "properties": {
        "METValue": {"type": ["number", "null"], "minimum": 0.9, "maximum": 25,
            "description": "Metabolic equivalent: a RATE, the multiple of resting "
            "metabolism. THE BEST ESTIMATE AVAILABLE for this row, so a caller never "
            "branches to find the good number. It equals METReference unless a scale "
            "tier applied, and METScale says which. Null unless ExerciseConf is in "
            "{GOOD, OK, ALIAS}."},
        "ActiveMinutes": {"type": ["number", "null"], "exclusiveMinimum": 0,
            "description": "The duration the LOG stated, reported verbatim even when "
            "it is not believed. Null when none was stated or it was zero."},
        "CaloriesBurnedEst": {"type": ["number", "null"], "exclusiveMinimum": 0,
            "description": "MET x 3.5 x body_mass_kg / 200 x minutes. A DOSE. Issued "
            "only when minutes AND body mass are both known AND the duration is "
            "within EXNORM_MAX_BOUT_MINUTES. There is no default body mass."},
        "ActivityResolved": {"type": ["string", "null"],
            "description": "The PA Compendium 2024 activity description this resolved "
            "to. Travels even at WEAK, so a person can curate the candidate; the "
            "VALUE does not travel with it."},
        "ActivityCode": {"type": ["string", "null"], "pattern": "^[0-9]{5}$",
            "description": "The Compendium activity_code. The resolved identity, kept "
            "as a column rather than discarded. NOT the cohort's ExerciseType: the two "
            "code spaces overlap by coincidence (Compendium 20050 is 'Eating at "
            "church'; WellDoc 20050 is strength training)."},
        "MajorHeading": {"type": ["string", "null"],
            "description": "One of the Compendium's 22 major headings."},
        "METReference": {"type": ["number", "null"], "minimum": 0.9, "maximum": 25,
            "description": "The Compendium's own published MET for ActivityCode, "
            "always unmodified. It is what makes any adjustment auditable and "
            "reversible: METValue / METReference is exactly METScaleFactor."},
        "METScale": {"enum": ["population", "device", "person", "person_activity"],
            "description": "WHOSE rate METValue is -- a SECOND axis, not the same one "
            "as ExerciseBasis, which says rate-or-dose. population is the Compendium's "
            "own number and the floor every caller gets without passing an identity. "
            "device adjusts for the wearable that measured the calories (Apple and "
            "FitBit disagree by 68% about the same named walk). person adjusts for "
            "this patient, fit only on bouts earlier than this one. Present on a miss "
            "too, where it reads population because nothing was adjusted."},
        "METScaleFactor": {"type": ["number", "null"], "minimum": 0.4, "maximum": 2.5,
            "description": "The multiplier applied to METReference. 1.0 at the "
            "population floor. Null when there is no MET to scale. A factor rides "
            "only on a TRUSTED identity: scaling a WEAK guess would dress an unnamed "
            "activity in a personal-looking number."},
        "ExerciseSource": {"type": "string",
            "description": "Where the VALUE came from, or why there is none. "
            "'compendium2024:alias:<code>' a curated pick · "
            "'compendium2024:fuzzy:<code>' a candidate, value withheld · "
            "'compendium2024:no_match' the bank does not list it · "
            "'not_resolvable:daily_rollup' not a bout at all · "
            "'not_resolvable:placeholder' the log named nothing · "
            "'not_resolvable:opaque_code' a vendor code with no book here. "
            "May carry a suffix '|bout>Nmin' when a dose was refused, and "
            "'|scale:<tier>:<key>:n<rows>:<as_of>' when a scale tier applied."},
        "ExerciseConf": {"enum": ["GOOD", "OK", "ALIAS", "WEAK", "MISS"],
            "description": "Only GOOD/OK/ALIAS may carry a value. GOOD is currently "
            "unreachable: the bank is a third-party mirror, not the publisher's file."},
        "ExerciseBasis": {"enum": ["per_session", "per_minute", None],
            "description": "The SCALE the numbers are on. per_session: kcal is this "
            "bout's total. per_minute: only a rate is reportable. Never absent when a "
            "value is present."},
        "TypeSource": {"type": "string",
            "description": "'<kind>|<how the name was obtained>'. kind is one of "
            "session, daily_rollup, placeholder, opaque_code. The second half is "
            "'text' when a patient wrote words, 'codebook:apple' / 'codebook:validic' "
            "/ 'codebook:welldoc_app' when a vendor code was translated, 'none' when "
            "no name was obtained. A typed name and a decoded one are different "
            "evidence and may not share a column."},
        "TypeConf": {"enum": ["LOGGED", "CODEBOOK", None],
            "description": "LOGGED: the words are the log's own. CODEBOOK: read off a "
            "vendor enum."},
    },
}

REQUEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "exnorm/v1/request",
    "title": "describe-exercise · POST /normalize",
    "type": "object",
    "additionalProperties": False,
    "required": ["activity"],
    "properties": {
        "activity": {"type": "string",
            "description": "ExerciseType exactly as the cohort logged it: 'Walk', "
            "'20052', '1001'. The only required field."},
        "source_id": {"type": ["integer", "string", "null"],
            "description": "EntrySourceID. A vendor code is meaningless without it, "
            "because ExerciseType is a vendor enum and this says whose. Free text "
            "does not need it."},
        "minutes": {"type": ["number", "null"],
            "description": "Bout duration. Without it there is no dose to report and "
            "none is invented."},
        "weight_kg": {"type": ["number", "null"],
            "description": "Body mass. Same. There is no default."},
    },
}

CASES = [
    ("1-apple-codebook",      "session", "codebook:apple",
     "A vendor code decoded through Apple's HKWorkoutActivityType. The cohort's "
     "code carries the EntrySourceID as a prefix: 20059 is source 20, HK case 59."),
    ("2-validic-codebook",    "session", "codebook:validic",
     "The same shape through a different book. Validic aggregates six vendors "
     "into one enum, which is why six EntrySourceIDs share this code space."),
    ("3-typed-text",          "session", "text",
     "A patient's own word. Reaches the SAME Compendium entry as the two code "
     "specimens above through one curated pick, and TypeSource still tells "
     "them apart."),
    ("4-rate-only",           "session", "no_dose",
     "Same activity, no body mass on file. The rate is still reportable, the "
     "dose is not, and ExerciseBasis says which of the two you are holding."),
    ("5-daily-rollup",        "daily_rollup", None,
     "Not an exercise event: a device's once-a-day summary, posted at local "
     "midnight, 88,467 rows across the board. Pricing one as a bout claims a "
     "patient did a single short workout every day for four years and never "
     "burned a calorie."),
    ("6-named-nothing",       "placeholder", None,
     "The log recorded a duration and no activity. Typed, never dropped: "
     "dropping it would make the cohort read as a bank failure."),
    ("7-no-codebook",         "opaque_code", None,
     "A vendor code with no book on this machine. A KNOWN unknown, and "
     "deliberately not the same ExerciseSource as a bank miss -- they have "
     "different fixes."),
    ("8-refused-dose",        "long_bout", None,
     "A duration past EXNORM_MAX_BOUT_MINUTES. The MET survives and the claimed "
     "duration is still reported verbatim; only the dose is refused, and "
     "ExerciseSource records why. 306 rows are treated this way. The extreme of "
     "the class is a log claiming 4,680 minutes, which would otherwise have made "
     "THIS PACKAGE the source of an 18,829 kcal estimate."),
    ("9-category-word",       "weak", None,
     "'Sports' head-anchors at a perfect score onto 'Sports spectator, very "
     "excited'. The query does not identify an activity, so the candidate "
     "travels for a person to curate and the number does not."),
]


def post(path, payload):
    req = urllib.request.Request(URL + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    os.makedirs(OUT, exist_ok=True)
    W = {}
    for p in glob.glob("_WorkSpace/1-SourceStore/*/*/Weight.parquet"):
        d = pd.read_parquet(p)
        if "Weight" not in d: continue
        d = d.assign(kg=pd.to_numeric(d.Weight, errors="coerce") * LB)
        for pid, g in d[d.kg.between(30, 300)].groupby("PatientID"):
            W[pid] = round(float(g.kg.median()), 1)

    frames = []
    for p in sorted(glob.glob("_WorkSpace/1-SourceStore/*/*/Exercise.parquet")):
        d = pd.read_parquet(p)
        if not len(d): continue
        if "EntrySourceID" not in d: d["EntrySourceID"] = None
        frames.append(d.assign(cohort=p.split("/")[2], __path=p, kg=d.PatientID.map(W)))
    a = pd.concat(frames, ignore_index=True)
    # Chunked: the whole corpus exceeds EXNORM_MAX_BATCH and the service
    # correctly answers 413 rather than quietly truncating.
    CH, out = 20000, []
    for i in range(0, len(a), CH):
        s_ = a.iloc[i:i+CH]
        out += post("/normalize/batch", {
            "activities": s_.ExerciseType.astype(str).tolist(),
            "minutes": [None if pd.isna(x) else float(x) for x in s_.ExerciseDuration],
            "weight_kg": [None if pd.isna(x) else float(x) for x in s_.kg],
            "source_ids": [None if pd.isna(x) else int(x) for x in s_.EntrySourceID],
        })["results"]
    r = pd.DataFrame(out)
    assert len(r) == len(a), (len(r), len(a))
    a["kind"] = r.TypeSource.str.split("|").str[0].values
    a["via"] = r.TypeSource.str.split("|").str[1].values

    def pick(kind=None, via=None, dose=True, special=None):
        g = a
        if special == "long_bout":
            g = a[r.ExerciseSource.fillna("").str.contains("bout>").values]
        elif special == "weak":
            g = a[(r.ExerciseConf == "WEAK").values]
        elif special == "no_dose":
            g = a[(a.kind == "session") & r.CaloriesBurnedEst.isna().values
                  & r.METValue.notna().values]
        else:
            g = a[(a.kind == kind)]
            if via: g = g[g.via == via]
            if dose: g = g[r.loc[g.index, "CaloriesBurnedEst"].notna()]
        if not len(g): return None
        # the MEDIAN row of its group, never an extreme
        if dose and "CaloriesBurnedEst" in r and r.loc[g.index, "CaloriesBurnedEst"].notna().any():
            c = r.loc[g.index, "CaloriesBurnedEst"]
            return g.loc[(c - c.median()).abs().idxmin()]
        return g.iloc[0]

    made = []
    for slug, kind, via, why in CASES:
        special = kind if kind in ("long_bout", "weak") else (via if via == "no_dose" else None)
        row = pick(kind if special is None else None, via if via and via != "no_dose" else None,
                   dose=(via not in (None, "no_dose") or kind == "session") and special is None,
                   special=special)
        if row is None:
            print(f"  SKIP {slug}"); continue
        req = {"activity": str(row.ExerciseType)}
        if pd.notna(row.EntrySourceID): req["source_id"] = int(row.EntrySourceID)
        if pd.notna(row.ExerciseDuration): req["minutes"] = round(float(row.ExerciseDuration), 1)
        if pd.notna(row.kg) and slug != "4-rate-only": req["weight_kg"] = float(row.kg)
        spec = {
            "schema": "exnorm/v1",
            "_from": f"{row.__path.replace('_WorkSpace/','')}, row read 260822, verbatim",
            "_why_this_row": why,
            "_cohort": row.cohort,
            "_logged_calories_for_comparison":
                None if pd.isna(row.CaloriesBurned) else round(float(row.CaloriesBurned), 1),
            "request": req,
            "response": post("/normalize", req),
        }
        json.dump(spec, open(f"{OUT}/{slug}.json", "w"), indent=2)
        made.append((slug, why))
        print(f"  {slug}")
    json.dump(SCHEMA, open(f"{OUT}/exnorm-v1.response.schema.json", "w"), indent=2)
    json.dump(REQUEST_SCHEMA, open(f"{OUT}/exnorm-v1.request.schema.json", "w"), indent=2)
    return made


if __name__ == "__main__":
    main()
