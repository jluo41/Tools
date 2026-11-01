"""
The sleep event JSON (b51 s06-D02, D05; s16-D03): three parts, as food's, exercise's and step's.

    {"raw":    {"type", "file"?, "rows": [{column: text}, ...], "pieces"?: [...]},  what arrives, as it arrives
     "input":  {"start", "end", "device", "total", "items", "timeline"},          the night, as the API is asked
     "output": {"<local hour>": {"in_bed_min", "asleep_min", "awake_in_bed_min"}   each hour its own minutes,
                               or {"in_bed_min", "unknown_min"}, ...}}             never a share

raw.type picks the preprocess step (RAW_TYPES). A row's kind is how long it is (KINDS). items is null: sleep has
nothing to look up (s06-D05). The timeline is the night's stretches asleep, {"from", "to", "state"}; the gaps between
them are awake in bed (still, s07 reads them). A watch's stages (light, deep, rem, wake) will fill state later.
"""

RAW_TYPES = {
    "log": "WellDoc SleepEntry rows of one person and device: the longest is the night (in bed); shorter rows inside "
           "it, in rows or in pieces, are its pieces (asleep), Apple's way",
}
INPUT_KEYS = ("start", "end", "device", "total", "items", "timeline")
KINDS = {"night": "3 hours or more", "nap": "15 minutes or more", "piece": "under 15 minutes"}
WELLDOC_FMT = "%m/%d/%Y %I:%M:%S %p"          # WellDoc's sleep times, UTC
