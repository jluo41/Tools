"""
The still event JSON (b51 s07-D02, s17): three parts, as step's and sleep's, one class with them (JL 261021).

    {"raw":    {"type", "rows": [{column: text, ...}, ...], "day"?, "start"?, "end"?},   what arrives, as it arrives
     "input":  {"start", "end", "device", "total", "items", "timeline"},                 the minutes, as the API is asked
     "output": {"<local hour>": {"minutes", "asleep_min", "moving_min", "still_min",     each hour's minutes, four ways
                                 "unknown_min", "unknown_why", "still_no_step_row"}}}

raw.type picks the preprocess step (RAW_TYPES). The timeline holds the minutes as stretches, as sleep's: minutes in a
row with the same steps (null when no step row), worn (a heart-rate reading in that minute) and sleep level (null out
of bed) are one {"from", "to", "steps", "worn", "level"}, "to" not included. items is null: a minute has no
words to describe, so there is no /normalize, as step's.

ONE MINUTE, ONE WAY (s07-D02). In bed asleep: asleep. In bed restless: unknown (asleep or awake, not told). In bed
awake: still. Out of bed, steps above the rule: moving (a step counted says the device was on). Out of bed, worn, steps
at or under the rule: still. Out of bed, no heart rate: unknown, never still. So each hour's four add to its minutes.
"""

RAW_TYPES = {
    "minutes": "minute rows: {time | from, to; steps? (a stretch's, shared by its minutes), bpm?, worn?, sleep?}, "
               "a time 'HH:MM' on raw.day, "
               "'day 3 10:07' or '2026-10-27 10:07'",
    "mcphases": "mcPhases rows as they come, each with its file: steps.csv, heart_rate.csv, sleep.csv",
}
INPUT_KEYS = ("start", "end", "device", "total", "items", "timeline")
ASLEEP_LEVELS = {"asleep", "light", "deep", "rem"}        # Fitbit's levels
RESTLESS_LEVELS = {"restless"}                            # in bed, not told: unknown
AWAKE_LEVELS = {"awake", "wake"}                          # in bed, awake: still
LEVELS = ASLEEP_LEVELS | RESTLESS_LEVELS | AWAKE_LEVELS
# How few steps make a worn, awake minute still: not decided yet (s17 Open 1, a j07 Task's rule, checked against
# Fitbit's sedentary minutes). Until then, 0: any step makes the minute moving.
STILL_MAX_STEPS = 0
RULE_NOTE = "provisional: 0 steps, until j07's rule Task (s17 Open 1)"
