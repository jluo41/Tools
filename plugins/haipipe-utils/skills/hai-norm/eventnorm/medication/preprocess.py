"""
The medication preprocess step: raw, as it arrives, to the input JSON (b51 s13's engine 1). raw["type"] picks it:

    app_id       one WellDoc MedAdministration row: its MedicationID named through WellDoc's catalog (ext_med_lexicon,
                 describe-medication's bank) into the drug's name and NDC; an id the catalog lacks is asked bare
    text         one Shanghai cell (its time and its column) or typed words: each drug and its dose, split by
                 describe-medication's own dialect (a cell may name several: 'metformin 0.5 g, acarbose 50 mg')
    pump         one Shanghai pump cell: the number is the dose (bolus) or the rate (basal); the header names the drug
    class_word   one OhioT1DM <bolus>, <basal> or <temp_basal> event: a class word, the product from the patient's tag

Each returns {"input": the input JSON, "kind": what the step found, "step": what it did, in one line}. A WellDoc time
is UTC plus the row's offset in minutes (UserAdministrationDate equals it in every LLY row); Shanghai's is local, +08:00
(the SourceFn's 480); OhioT1DM's is local with no zone, day first.
"""
import re

from ..preprocess.common import clock, frame
from .schema import RAW_TYPES, RATES, SENTINELS

SHANGHAI_ZONE = "+08:00"
# Shanghai's medication headers, as ShanghaiExtV260926 folds them (_MED_COLS, _MED_ALIASES): a key word -> its column
SHANGHAI_COLS = {"insulin dose - s.c.": ("text", "mdi"), "皮下注射胰岛素": ("text", "mdi"),
                 "insulin dose - i.v.": ("text", "iv"), "静脉注射胰岛素": ("text", "iv"),
                 "non-insulin hypoglycemic agents": ("text", None), "非胰岛素降糖药": ("text", None),
                 "口服降糖药": ("text", None),
                 "csii - bolus insulin": ("pump", "pump_bolus"), "胰岛素泵大剂量": ("pump", "pump_bolus"),
                 "csii - basal insulin": ("pump", "pump_basal"), "胰岛素泵基础量": ("pump", "pump_basal")}
CATEGORY = {"mdi": "Insulin dose - s.c.", "iv": "Insulin dose - i.v.", None: "Non-insulin hypoglycemic agents"}
IV_INSULIN = re.compile(r"([0-9]*\.?[0-9]+)\s*IU\s+([A-Za-z][A-Za-z0-9 \-]*?)\s*(?:,|$)", re.I)
HEAD_DRUG = re.compile(r"\(([^,()]+?)\s*[, ]\s*IU", re.I)        # 'CSII - basal insulin (Novolin R, IU / H)'
CLASS = {"bolus": ("bolus insulin", "pump_bolus"), "basal": ("basal insulin", "pump_basal"),
         "temp_basal": ("basal insulin", "pump_temp_basal")}


def number(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else (int(x) if x == int(x) else x)


def dose_of(v):
    """A logged dose as a number, None when empty or a "not given" sentinel (-1, 255, 999)."""
    d = number(v)
    return None if d is None or d in SENTINELS else d


def unit_of(u, rate=False):
    """describe-medication's unit word as the event writes it: 'iu' a dose, 'iu/h' a rate."""
    if not u:
        return None
    return f"{u}/h" if rate else u


def total_of(items):
    """The event's own total, as the raw states it: one dose and its unit, or a rate; several drugs are counted."""
    if not items:
        return None
    if len(items) == 1:
        it = items[0]
        if it.get("delivery") in RATES:
            return {k: v for k, v in (("rate", it.get("dose")), ("unit", it.get("unit"))) if v is not None} or None
        return {"doses": 1, **{k: v for k, v in (("dose", it.get("dose")), ("unit", it.get("unit"))) if v is not None}}
    return {"doses": len(items)}


def item(k, drug, ndc=None, dose=None, unit=None, delivery=None, **more):
    return {"id": f"i{k}", "drug": drug, "ndc": ndc or None, "dose": dose, "unit": unit, "delivery": delivery, **more}


def shanghai_column(rows):
    """The one medication column a Shanghai row holds -> (its header, the raw type, its delivery)."""
    for c in rows.columns:
        key = re.sub(r"\s+", " ", str(c).strip().lower())
        for word, (kind, how) in SHANGHAI_COLS.items():
            if key.startswith(word) or word in str(c):
                return c, kind, how
    return None, None, None


def lexicon_name(medication_id):
    """WellDoc's catalog: an id -> (name, NDC), or None when the catalog lacks it."""
    from mednorm import bank
    hit = bank.lexicon_lookup(str(medication_id).strip())
    return (hit["MedicationName"], hit.get("NDC") or None) if hit else None


def app_id(rows):
    r = rows.iloc[0]
    mid = str(number(r.get("MedicationID")) if number(r.get("MedicationID")) is not None else r.get("MedicationID"))
    named = lexicon_name(mid)
    dose = dose_of(r.get("Dose"))
    it = item(1, named[0], named[1], dose) if named else item(1, mid, None, dose)
    meter = str(r.get("MeterType")).strip() if "MeterType" in rows.columns and r.get("MeterType") not in (None, "") \
        and str(r.get("MeterType")) not in ("nan", "None") else None
    inp = {"start": clock(rows, "AdministrationDate", "AdministrationTimeZoneOffset"), "end": None,
           "logged_at": clock(rows, "EntryDateTime", "AdministrationTimeZoneOffset"), "total": total_of([it]),
           "items": [it], "timeline": None,
           "source": {"kind": "logged", **({"meter_type": meter} if meter else {})}}
    step = (f"WellDoc's id {mid} named by the catalog: {named[0]}" if named else
            f"WellDoc's id {mid} is not in the catalog: asked as the bare id") + \
           ("; the Dose is a 'not given' sentinel" if dose is None and number(r.get("Dose")) in SENTINELS else "")
    return {"input": inp, "kind": "app_id" if named else "unknown_id", "step": step}


def split_cell(cell, delivery):
    """A Shanghai cell (or typed words) -> items: describe-medication's dialect splits it into each drug and its dose
    (mg for g); an i.v. cell names a drip and the insulin in it ('500ml 0.9% sodium chloride, 12 IU Novolin R, ...'):
    only the insulin is a drug here."""
    from mednorm import dialect
    text = str(cell or "").strip()
    if delivery == "iv":
        found = IV_INSULIN.findall(text)
        return [item(k + 1, d.strip(), None, number(v), "iu", "iv") for k, (v, d) in enumerate(found)]
    p = dialect.parse(CATEGORY.get(delivery, CATEGORY[None]), payload={"MedicationName": text})
    comps = p.components or ([(p.key, p.dose, p.unit)] if p.key else [])
    return [item(k + 1, n, None, number(v), u, delivery) for k, (n, v, u) in enumerate(comps)]


def two_part_note(cell):
    """The step's words for a combination pill's two-part dose ('Janumet 50/1000 mg'): its drug is kept, no dose."""
    from mednorm import dialect
    two = dialect.two_part_doses(cell)
    return f"; a two-part dose ({', '.join(two)}) is no one number: its drug kept, no dose" if two else ""


def text(rows):
    r = rows.iloc[0]
    if "text" in rows.columns:                                  # words typed: "metformin 500 mg", and when
        items = split_cell(r["text"], None)
        given = str(r.get("time") or "").strip()                   # the try page's "2026-10-27 08:05 -04:00", kept
        start = given if re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d [+-]\d\d:\d\d$", given) else clock(rows, "time")
        return {"input": {"start": start, "end": None, "logged_at": start, "total": total_of(items), "items": items,
                          "timeline": None, "source": {"kind": "logged"}},
                "kind": "text", "step": f"words split into {len(items)} drug{'s' * (len(items) != 1)}"
                                        + two_part_note(r["text"])}
    col, kind, how = shanghai_column(rows)
    if col is None:
        raise ValueError("a text row needs 'text' (and 'time'), or a Shanghai medication column and its Date")
    items = split_cell(r[col], how)
    start = clock(rows, "Date", zone=SHANGHAI_ZONE)
    return {"input": {"start": start, "end": None, "logged_at": start, "total": total_of(items), "items": items,
                      "timeline": None, "source": {"kind": "logged"}},
            "kind": "several" if len(items) > 1 else "text",
            "step": f"{col.strip()}: the cell split into {len(items)} drug{'s' * (len(items) != 1)}"
                    + two_part_note(r[col])}


def pump(rows):
    r = rows.iloc[0]
    col, kind, how = shanghai_column(rows)
    if col is None or kind != "pump":
        raise ValueError("a pump row needs a Shanghai CSII column and its Date")
    m = HEAD_DRUG.search(str(col))
    drug = m.group(1).strip() if m else "insulin"
    v = number(r[col])
    it = item(1, drug, None, v, "iu/h" if how in RATES else "iu", how)
    start = clock(rows, "Date", zone=SHANGHAI_ZONE)
    return {"input": {"start": start, "end": None, "logged_at": start, "total": total_of([it]), "items": [it],
                      "timeline": None, "source": {"kind": "logged"}},
            "kind": "pump", "step": f"the header names the drug ({drug}); the cell is the "
                                    f"{'rate, units an hour' if how in RATES else 'dose'}"}


def class_word(rows):
    r = rows.iloc[0]
    el = str(r.get("element") or "").strip()
    if el not in CLASS:
        raise ValueError("a class_word row needs element: bolus, basal or temp_basal (OhioT1DM's XML)")
    word, how = CLASS[el]
    tcol = "ts" if "ts" in rows.columns and str(r.get("ts")) not in ("None", "nan") else "ts_begin"
    start = clock(rows, tcol, dayfirst=True)
    end = clock(rows, "ts_end", dayfirst=True) if el == "temp_basal" else None
    product = str(r.get("insulin_type") or "").strip() or None
    v = number(r.get("dose") if el == "bolus" else r.get("value"))
    it = item(1, product or word, None, v, "iu/h" if how in RATES else "iu", how, class_word=word)
    return {"input": {"start": start, "end": end, "logged_at": start, "total": total_of([it]), "items": [it],
                      "timeline": None, "source": {"kind": "logged"}},
            "kind": "class_word", "step": f"<{el}>: {word}" + (f", the patient's insulin_type {product}" if product
                                                                 else ", no product named")}


STEPS = {"app_id": app_id, "text": text, "pump": pump, "class_word": class_word}


def preprocess(raw: dict) -> dict:
    """raw {"type", "rows": [one row]} -> {"input", "kind", "step"}; a ValueError says what is wrong."""
    t = (raw or {}).get("type")
    if t not in STEPS:
        raise ValueError(f"raw.type must be one of {sorted(RAW_TYPES)}")
    return STEPS[t](frame(raw))
