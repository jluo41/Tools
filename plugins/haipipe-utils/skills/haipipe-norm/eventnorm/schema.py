"""
The event JSON (s01-D20, D21, D23, D24, D36): three parts, the three kinds of data.

    {"raw":    {"type", "file"?, "rows": [{column: text, ...}, ...]},     what arrives, as it arrives
     "input":  {"start", "end", "logged_at", "meal_type", "total",        what the preprocess step makes of it,
                "items", "timeline"},                                     normalized, coarse to fine
     "output": {"<local hour>": {"share", "start", "end", "logged_at",    the event by local hour, its total and
                                 "meal_type", "total", "items",           items enriched from the tables
                                 "timeline"}, ...}}

raw.type picks the preprocess step (RAW_TYPES). Times are local with their offset ("2021-04-14 07:17 -04:00"), or
bare when the raw names no zone. A number is text with its unit ("32.45 g"); one the raw does not give is left out
of the input's total, never written as 0 (s01-D28). "timeline" is the time layer of every event type: for food each
point is a bite {"at", "parts": [{"item", "amount"}]}. No cohort logs an end or a timeline today, so both are null.
"""

RAW_TYPES = {
    "app_log": "a row per food, a vendor's code each (the WellDoc app's ELogFoodItem)",
    "text": "words: a cell of foods a line (Shanghai's Dietary intake and 饮食), or text typed or said",
    "photo": "a meal photo and its row (CGMacros); the photo API names the foods",
    "numbers_only": "a time and the meal's own numbers, no food (OhioT1DM, dubosson)",
}
INPUT_KEYS = ("start", "end", "logged_at", "meal_type", "total", "items", "timeline")
ITEM_KEYS = ("id", "food", "amount", "food_zh")
RAW_DROP = {"PatientID", "id", "Unnamed: 0",           # whose row it is: never read, never written back;
            "ObservationCreatedBy"}                   # the app account that typed the row (s01-D42)
