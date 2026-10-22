"""
The exercise event JSON (b51 s02-D08 to D25): three parts, as food's.

    {"raw":    {"type", "file"?, "rows": [{column: text, ...}, ...]},   what arrives, as it arrives
     "input":  {"start", "end", "total", "items", "timeline"},          the event, as the API is asked
     "output": {"<local hour>": {"start", "end", "total", "items",      each hour its own part (s02-D23): its own
                                 "timeline"}, ...}}                     minutes, MET, MET-minutes, kcal; no share

raw.type picks the preprocess step (RAW_TYPES). The input's total is the event's own numbers as the raw states them
(s02-D14): minutes, calories, distance_m, and a stream's MET-minutes and steps summed; a 0 or an empty cell is "not
given" and left out. An item is {"id", "activity", "met"}: its words, and the MET a device gives (null when none);
items is null when nothing is named (s02-D18). The timeline is null for a logged workout; a stream fills it, one point a
sample with every number the device gives under one name (s02-D21): met, hr, steps, calories, motion.
"""

RAW_TYPES = {
    "device_code": "a logged row (ELogExerciseEntry) whose code a vendor's book names: Validic, Apple, Google Fit",
    "app_list": "a logged row from the WellDoc app's own list",
    "other": "a logged row the vendor names only Other: kept for its total when it has minutes (s02-D18)",
    "log": "a logged row of any of the three: the code book says which",
    "text": "words typed or said: an activity and its minutes, 'brisk walking 30 min'",
    "met_stream": "a wearable's MET every minute (CGMacros: Timestamp, METs, HR, Calories (Activity))",
    "steps_stream": "a wearable's steps on a clock (MetaboNet: date, steps; OhioT1DM 2018: ts, basis_steps)",
    "named_stream": "a wearable that names each stretch (AI-READI's Garmin: activity_name, base_movement_quantity)",
    "strap_stream": "a chest strap (D1NAMO: time, HR, Activity): no rule reads it, it stays a stream",
    "motion_stream": "motion only (OhioT1DM 2020: ts, acceleration): no rule reads it, it stays a stream",
    "lab_stream": "a lab's measured MET a minute (GOTOV: minute, METS, wristSVM): a ruler",
    "wearable": "a wearable's file, its stream type not given: found by its columns (the try page's upload)",
}
INPUT_KEYS = ("start", "end", "total", "items", "timeline")
STREAM_NAMES = ("met", "hr", "steps", "calories", "motion")      # a stream's numbers, one name each (s02-D21)
CODEBOOK_RELEASE = "EventNormV7"     # the release that pins exercise's code book S20260930 (the book's own words)
