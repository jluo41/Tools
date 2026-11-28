"""
The medication event JSON (b51 s03, s13): three parts, as food's and exercise's.

    {"raw":    {"type", "file"?, "rows": [{column: text, ...}]},            what arrives, as it arrives
     "input":  {"start", "end", "logged_at", "total", "items",              the event, as the API is asked
                "timeline", "source"},
     "output": {"<local hour>": {"share", "start", "end", "logged_at",      the event by local hour: a dose is a
                                 "total", "items", "timeline", "source"}}}  moment, so its start's hour holds it all

raw.type picks the preprocess step (RAW_TYPES). An input item is {"id", "drug", "ndc", "dose", "unit", "delivery"}
(the shape s14's insulin path reuses, b51-j04-Insulin-Job 261027): the drug's words as the raw names it (a WellDoc id
named through WellDoc's catalog first), its NDC when the catalog gives one, the dose as logged with its unit when the
raw states one, and how it went in when the raw says (DELIVERY). A dose is one moment and has no end; a pump's basal is
a rate, units an hour, from its start: its total says "rate", never "doses" (s14's ask 1). The input's total is the
event's own numbers as the raw states them: {"doses": n, "dose": d, "unit": u}, a "not given" sentinel left out
(SENTINELS). "source" says how it became known: {"kind": "logged"}, with the app's meter type when the row gives one
(MeterType; s14's ask 2).
"""

RAW_TYPES = {
    "app_id": "a WellDoc MedAdministration row: MedicationID (WellDoc's own id), Dose, AdministrationDate (UTC) and "
              "AdministrationTimeZoneOffset, EntryDateTime, MeterType",
    "text": "a cell naming one drug or several, each with its dose (Shanghai's Insulin dose - s.c., Insulin dose - "
            "i.v., Non-insulin hypoglycemic agents), or words typed: 'metformin 500 mg'",
    "pump": "a pump's cell: the number is the dose or the rate, the column's header names the drug (Shanghai's "
            "CSII bolus and basal columns, 胰岛素泵基础量)",
    "class_word": "an insulin pump's own log, a class and no product in the event (OhioT1DM's <bolus>, <basal>, "
                  "<temp_basal>); the product is on the patient's tag (insulin_type) when the file gives it",
}
INPUT_KEYS = ("start", "end", "logged_at", "total", "items", "timeline", "source")
ITEM_KEYS = ("id", "drug", "ndc", "dose", "unit", "delivery")
DELIVERY = {"mdi": "an injection: a pen or a syringe", "iv": "into a vein", "pump_bolus": "a pump's bolus: one dose",
            "pump_basal": "a pump's basal: a rate, units an hour", "pump_temp_basal": "a pump's temporary basal: a "
            "rate for a stretch"}
RATES = ("pump_basal", "pump_temp_basal")
SENTINELS = (-1, 255, 999)            # a Dose meaning "not given" (j03 t03 adapter_medication_named.py)
OUTPUT_ITEM_KEYS = ("id", "ingredient", "brand", "class", "form", "route", "ndc", "dose", "unit", "delivery",
                    "insulin", "conf")
