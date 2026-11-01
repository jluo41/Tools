"""
The step event JSON (b51 s05-D01, D02; s15-D03): three parts, as food's and exercise's.

    {"raw":    {"type", "file"?, "rows": [{column: text, ...}, ...]},   what arrives, as it arrives
     "input":  {"start", "end", "device", "total", "items", "timeline"},  the event, as the API is asked
     "output": {"<local hour>": {"share", "start", "end", "total",      a logged row: each hour its share to the
                                 "in_hour", "items", "timeline"}, ...}}  second and its own minutes and steps
     "walks":  [{"start", "end", "minutes", "steps", "spm", "to"}, ...]  a stream's brisk runs, for POST /exercise/event

raw.type picks the preprocess step (RAW_TYPES). A logged row's kind is how long it is, to the second (KINDS): a whole
day keeps its day, its hours unknown (never 24 equal hours). The input's total is the row's own numbers as the raw
states them; a 0 or a -1 is "not given" and left out. items is null: a count has no words to describe (so there is no
/normalize, s15-D03 as s12-D08). device names who counted it (EntrySourceID through WellDoc's dictionary), so a day
two devices count can keep one. A stream fills the timeline, one point a sample.
"""

RAW_TYPES = {
    "log": "a WellDoc StepEntry row: StartDateTime, EndDateTime (UTC), TimezoneOffset, NumberOfSteps, EntrySourceID",
    "steps_stream": "a wearable's steps on a clock (MetaboNet: date, steps; OhioT1DM 2018: ts, basis_steps), "
                    "the shapes exercise's steps_stream reads",
}
INPUT_KEYS = ("start", "end", "device", "total", "items", "timeline")
KINDS = {"minute": "up to 2 minutes", "hour": "up to 61 minutes", "part_day": "under 1,379 minutes",
         "day": "1,379 minutes or more, so a 23-hour clock-change day counts"}
STATED = {"steps": "NumberOfSteps", "distance_m": "DistanceInMeters", "calories": "CaloriesBurned"}
WELLDOC_FMT = "%m/%d/%Y %I:%M:%S %p"          # WellDoc's step times, UTC
HEALTH_CONNECT = "40"                         # in no dictionary; every row carries a HealthConnectMetaDataId
