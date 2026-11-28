"""
The stress event JSON (b51 j08, s10): three parts, as step's, sleep's and still's, one class with them: the day's
hours, measured by a device.

    {"raw":    {"type", "rows": [{column: text, ...}, ...], "offset"?, "start"?, "end"?},   what arrives, as it arrives
     "input":  {"start", "end", "device", "total", "items", "timeline"},                    the event, as the API is asked
     "output": {"<local hour>": {"minutes", "rest_min", "low_min", "medium_min", "high_min",   each hour's minutes, six
                                 "active_min", "unknown_min", "unknown_why", "scored_min",     ways, and the mean of
                                 "mean"}}}                                                     its scored minutes

raw.type picks the preprocess step (RAW_TYPES). The timeline holds the minutes as stretches: minutes in a row at one
level are one {"from", "to", "level", "minutes", "mean"}, "to" not included; this stretch is b01's Stress row (one
stress stretch: back-to-back readings at one level, JL 261107). items is null: a score has no words to describe, so
there is no /normalize, as step's.

ONE MINUTE, ONE LEVEL. A Garmin reading of 0 to 100 is scored: rest, low, medium or high by Garmin's own bands
(BANDS). -2 is active: the watch saw too much movement to score, so the minute is the person moving, never calm.
-1 is unknown (not_measured): the watch could not score it, most often off the wrist. A minute of the span with no
reading at all is unknown (no_reading). So each hour's six add to its minutes.

TWO SCORES, TWO DIRECTIONS (DIRECTION). Garmin's stress level: higher is more stress. Fitbit's Stress Management
Score (mcPhases): higher is calmer, one a day. They are never put on one scale; a day score stays its day, its hours
unknown, as a whole day of steps does (s05).
"""

RAW_TYPES = {
    "readings": "a Garmin's stress readings, one a minute: {time, value}, or AI-READI's own "
                "{stress: {value}, effective_time_frame: {date_time}}; UTC plus raw.offset minutes when given",
    "day_score": "mcPhases' stress_score.csv rows of one person's one day (a day is sent 1 to 4 times): Fitbit's "
                 "Stress Management Score",
}
INPUT_KEYS = ("start", "end", "device", "total", "items", "timeline")
BANDS = (("rest", 0, 25), ("low", 26, 50), ("medium", 51, 75), ("high", 76, 100))     # Garmin's own
ACTIVE, NOT_MEASURED = -2, -1                 # Garmin's codes: too much movement; could not score
SCORED = tuple(b[0] for b in BANDS)
LEVELS = SCORED + ("active", "unknown")
WHY = ("not_measured", "no_reading")
DIRECTION = {"readings": "higher is more stress (Garmin stress level, 0 to 100)",
             "day_score": "higher is calmer (Fitbit Stress Management Score, 1 to 100)"}
DAY_READY = ("READY", "READY_NOT_PREMIUM")    # mcPhases status with a score; NO_DATA and IN_PROGRESS carry a 0
DAY_PARTS = {"sleep": ("sleep_points", "max_sleep_points"),
             "responsiveness": ("responsiveness_points", "max_responsiveness_points"),
             "exertion": ("exertion_points", "max_exertion_points")}
