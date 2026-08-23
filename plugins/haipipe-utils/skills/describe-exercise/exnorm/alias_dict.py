"""
The curated map: a canonical activity name -> ONE PA Compendium entry.

WHY A HUMAN PICKED EACH ROW
================================================================================
A log that says 'Walking' has not said how fast. The compendium has twelve level
walking entries from 2.3 MET (strolling) to 8.5 MET (5 mph), a 3.7x spread, and
a text matcher choosing among them is choosing an INTENSITY it has no evidence
for. So each bare noun gets one deliberate representative -- the general or
moderate-effort entry -- and every value derived through this map is stamped
ALIAS, so a reader can see the assumption rather than infer it from a MET.

THE ASSUMPTION, STATED ONCE: a bare activity noun is read as MODERATE EFFORT.
That is the compendium's own 'general' convention and it is wrong for any
individual bout. It is a defensible population default and nothing more.

'sports' IS DELIBERATELY ABSENT. 457 rows say 'Sports' or 'Sport' and the
compendium's Sports heading runs 3.0 MET (frisbee) to 12.3 (boxing). There is no
representative to pick, so it falls through to the fuzzy tier, scores WEAK, and
writes NULL. That is the correct outcome, not a gap to be filled.
"""

# canonical name (from dialect.TEXT_CANON) -> (activity_code, why this one)
ALIAS_CODE = {
    "walking":             ("17190", "Walking, 2.8-3.4 mph, level, moderate pace"),
    "walking, treadmill":  ("17190", "same pace assumption; the belt is not the activity"),
    "hiking":              ("17082", "normal pace through fields, no load"),
    "running":             ("12020", "Jogging, general, self-selected pace"),
    "bicycling":           ("01014", "Bicycling, general"),
    "swimming":            ("18310", "leisurely, not lap swimming; a lap swimmer logs laps"),
    "yoga":                ("02150", "Yoga, Hatha -- the unqualified default style"),
    "resistance training": ("02054", "multiple exercises, 8-15 reps at varied resistance"),
    "aerobics":            ("02000", "Aerobic, general"),
    "dancing":             ("03070", "Contemporary dancing, general"),
    "elliptical trainer":  ("02048", "Elliptical trainer, moderate effort"),
    "circuit training":    ("02035", "Circuit training, moderate effort"),
    "home activities":     ("05030", "Cleaning, house or cabin, general, moderate effort"),
    "gardening":           ("08245", "Gardening, general, moderate effort"),
    "skiing":              ("19075", "Skiing, general"),
    "tennis":              ("15675", "Tennis, general, moderate effort"),
    "golf":                ("15255", "Golf, general"),
    "conditioning exercise": ("02030", "Calisthenics, light or moderate effort, general"),
}

# ---------------------------------------------------------------------------
# Added 2026-08-22, when WellDoc's data dictionary and Apple's HKWorkoutActivity
# Type enum turned 32,394 rows of opaque vendor code into labels. Each pick was
# made by hand against the bank, and several had to be, because the fuzzy tier's
# top hit was actively wrong:
#
#     'cycling'                   -> 'Aquatic cycling, 90+ RPM'
#     'mind and body'             -> 'Body weight resistance exercises'
#     'preparation and recovery'  -> 'Cooking or food preparation, walking'
#     'traditional strength ...'  -> 'Pilates, traditional, mat'
#
# Every one of those scores well and means something else. That is the whole
# argument for this file existing.
# ---------------------------------------------------------------------------
ALIAS_CODE.update({
    # --- the big ones, by row count ---------------------------------------
    "cycling":              ("01014", "Bicycling, general -- NOT the fuzzy tier's 'Aquatic cycling'"),
    "traditional strength training": ("02054", "Apple's barbell/machine sense; same pick as 'resistance training'"),
    "functional strength training":  ("02056", "Apple: 'free weights and/or body weight and/or accessories'"),
    "high intensity interval training": ("02210", "High intensity interval exercise, moderate"),
    "core training":        ("02024", "Calisthenics: curl ups, crunches, plank"),
    "preparation and recovery": ("02101", "Apple's warm-up/cool-down type. Stretching, mild"),
    "mixed cardio":         ("02035", "Apple: a bout mixing modalities. Circuit training, moderate"),
    "dance":                ("03070", "Contemporary dancing, general; same pick as 'dancing'"),
    "mind and body":        ("15670", "Apple's own gloss is 'Qigong, meditation, etc.'"),
    "stair climbing":       ("17131", "Stair climbing, general"),
    "stairs":               ("17131", "Apple's stepper type; same activity"),
    "cross training":       ("02035", "Apple: 'any mix of cardio and/or strength training'"),
    "rowing":               ("02072", "Rowing, stationary, 100-149 watts"),
    "rowing machine":       ("02072", "same"),
    "flexibility":          ("02101", "Stretching, mild"),
    "stretching":           ("02101", "same"),
    "pilates":              ("02105", "Pilates, general"),
    "hand cycling":         ("02117", "Arm ergometer, hand bike, 25-30W"),

    # --- sports, all with a 'general' or recreational representative -------
    "american football":    ("15210", "Football, competitive"),
    "archery":              ("15010", "Archery, non-hunting"),
    "badminton":            ("15030", "social singles and doubles, general -- not the competitive entry"),
    "basketball":           ("15055", "Basketball, general"),
    "bowling":              ("15092", "Bowling, indoor, bowling alley"),
    "boxing":               ("15110", "Boxing, punching bag -- the recreational form"),
    "cricket":              ("15150", "Cricket, batting, bowling, fielding"),
    "hockey":               ("15360", "Hockey, ice, general"),
    "ice hockey":           ("15360", "same"),
    "kickboxing":           ("15457", "Kickboxing"),
    "lacrosse":             ("15460", "Lacrosse"),
    "martial arts":         ("15425", "Martial arts, different types, slower pace"),
    "racquetball":          ("15530", "Racquetball, general"),
    "rugby":                ("15562", "Rugby, touch, non-competitive"),
    "soccer":               ("15610", "Soccer, casual, general"),
    "table tennis":         ("15660", "Table tennis, ping pong"),
    "tai chi":              ("15670", "Tai chi, qi gong, general"),
    "volleyball":           ("15710", "Volleyball, non-competitive"),

    # --- snow, water, studio ----------------------------------------------
    "downhill skiing":      ("19160", "downhill/alpine, moderate effort, general"),
    "snowboarding":         ("19201", "Snowboarding, recreational, moderate pace"),
    "snow shoeing":         ("19190", "Snow shoeing, moderate effort"),
    "snow sports":          ("19075", "Apple's catch-all snow type. Skiing, general"),
    "mountain biking":      ("01009", "Bicycling, mountain, general"),
    "water fitness":        ("02120", "Water aerobics, water calisthenics, water exercise"),
    "jump rope":            ("02068", "Rope skipping exercise, general"),
    "step training":        ("02004", "Bench step class, general"),
    "barre":                ("03010", "Ballet, modern or jazz, rehearsal or class"),
})

# DELIBERATELY ABSENT, and each for its own reason:
#   'wheelchair walk pace' / 'wheelchair run pace'  (3 rows)
#       The compendium's wheelchair entries are for a person PUSHING one. There
#       is no self-propelled entry, and an arm-ergometer proxy is a guess.
#   'inline skating'  (1 row)
#       The bank's skating entries are all ice.
#   'sports', 'other', 'generic'
#       Category words. See the module docstring.
