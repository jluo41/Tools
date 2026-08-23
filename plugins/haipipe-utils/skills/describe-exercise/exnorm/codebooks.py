"""
The vendor code books. Transcribed, never inferred.

A cohort's ExerciseType is a vendor enum, and EntrySourceID says whose. This
file holds one dict per vendor namespace and NOTHING ELSE -- no Compendium
picks, no MET, no policy. A code becomes a LABEL here; alias_dict.py turns a
label into a MET. Keeping those apart is what lets a codebook be re-transcribed
from its source without touching a single curated judgement.

PROVENANCE, one per table, because a codebook with no source is a guess:

  APPLE_HK       Apple's own header. HKWorkoutActivityType in
                 HealthKit.framework/Headers/HKWorkout.h, iPhoneOS14.5 SDK,
                 fetched 2026-08-22 from github.com/theos/sdks. The enum starts
                 at 1, increments implicitly, and ends at Other = 3000; the
                 values below were parsed from that declaration, not typed out.

                 VERIFIED AGAINST OUR OWN DATA, and this is the reason it is
                 trusted at all: WellDoc's EntrySourceID-20 codes are '20' +
                 this enum. Of the 54 distinct codes in 1-SourceStore, 47 have a
                 suffix that is a valid case here and 7 do not -- and those 7
                 are exactly 20901..20906 and 20999, a contiguous private band.
                 A wrong hypothesis does not miss in one clean block.

                 iOS 14.5 predates a few later cases (swimBikeRun, transition,
                 underwaterDiving). None appears in our data; a cohort exported
                 after ~2022 could carry one, and it would MISS rather than
                 mis-resolve.

  VALIDIC        WellDoc's own data dictionary, ExternalExerciseType, from
                 gdrive:2-Documentation/Dictionary/2-CodeTable.xlsx sheet DSM.
                 On this machine at
                 _WorkSpace/0-RawDataStore/_WellDocInfo/Dictionary/, which has
                 been there since 2025-07-10 -- process_LabVitals in the WellDoc
                 SourceFn already decodes two other enums out of it.
                 Resolves 18,608 of 18,608 numeric rows under EntrySourceID
                 23/24/25/34/35/36. Validic is an AGGREGATOR: six sources share
                 one enum because Validic normalises six vendors before WellDoc
                 sees them.
                 Code 9002 has a blank label in the source spreadsheet and is
                 therefore absent here (103 rows). That is a gap in the
                 dictionary, not in this file.

  WELLDOC_APP    Same dictionary, InternalExerciseType. EntrySourceID 1/2, the
                 app's own Mobile/Web enum.

Both WellDoc tables define 1-5 identically and diverge above that, so a code is
ALWAYS looked up in its own namespace's book and never in a merged one.
"""

# EntrySourceID -> which book issued this row's code. From the same dictionary's
# EntrySourceID sheet, which is also where the vendor names below come from.
SOURCE_TO_BOOK = {
    20: "apple",                                            # AppleHealthKit
    23: "validic", 24: "validic", 25: "validic",            # Validic_FitBit / Misfit / Garmin
    34: "validic", 35: "validic", 36: "validic",            # Validic_Nokia / Polar / Strava
    1: "welldoc_app", 2: "welldoc_app",                     # Mobile / Web
    37: "google_fit", 40: "google_fit",                     # Google_Fit
}

# EntrySourceID -> the vendor's name, for provenance strings a person reads.
SOURCE_VENDOR = {
    1: "Mobile", 2: "Web", 18: "CGM", 20: "AppleHealthKit",
    23: "Validic_FitBit", 24: "Validic_Misfit", 25: "Validic_Garmin",
    34: "Validic_Nokia", 35: "Validic_Polar", 36: "Validic_Strava",
    37: "Google_Fit", 40: "Google_Fit",
}

# Apple prefixes its workout codes with the EntrySourceID itself: 20052 is
# source 20, HKWorkoutActivityType 52 (walking).
APPLE_PREFIX = 20000

# Apple's private band. NOT workout types: 20901..20906 are daily device
# roll-ups (one per patient per day, at local midnight, CaloriesBurned zero in
# 100.0% of 88,467 rows) and 20999 is an unmapped-type bucket that behaves like
# a real session (695 distinct times of day, median 33 min, 4.1% zero kcal).
APPLE_ROLLUP = frozenset(str(c) for c in range(20901, 20907))
APPLE_UNMAPPED = "20999"

APPLE_HK = {
    1: 'american football',
    2: 'archery',
    3: 'australian football',
    4: 'badminton',
    5: 'baseball',
    6: 'basketball',
    7: 'bowling',
    8: 'boxing',
    9: 'climbing',
    10: 'cricket',
    11: 'cross training',
    12: 'curling',
    13: 'cycling',
    14: 'dance',
    15: 'dance inspired training',
    16: 'elliptical',
    17: 'equestrian sports',
    18: 'fencing',
    19: 'fishing',
    20: 'functional strength training',
    21: 'golf',
    22: 'gymnastics',
    23: 'handball',
    24: 'hiking',
    25: 'hockey',
    26: 'hunting',
    27: 'lacrosse',
    28: 'martial arts',
    29: 'mind and body',
    30: 'mixed metabolic cardio training',
    31: 'paddle sports',
    32: 'play',
    33: 'preparation and recovery',
    34: 'racquetball',
    35: 'rowing',
    36: 'rugby',
    37: 'running',
    38: 'sailing',
    39: 'skating sports',
    40: 'snow sports',
    41: 'soccer',
    42: 'softball',
    43: 'squash',
    44: 'stair climbing',
    45: 'surfing sports',
    46: 'swimming',
    47: 'table tennis',
    48: 'tennis',
    49: 'track and field',
    50: 'traditional strength training',
    51: 'volleyball',
    52: 'walking',
    53: 'water fitness',
    54: 'water polo',
    55: 'water sports',
    56: 'wrestling',
    57: 'yoga',
    58: 'barre',
    59: 'core training',
    60: 'cross country skiing',
    61: 'downhill skiing',
    62: 'flexibility',
    63: 'high intensity interval training',
    64: 'jump rope',
    65: 'kickboxing',
    66: 'pilates',
    67: 'snowboarding',
    68: 'stairs',
    69: 'step training',
    70: 'wheelchair walk pace',
    71: 'wheelchair run pace',
    72: 'tai chi',
    73: 'mixed cardio',
    74: 'hand cycling',
    75: 'disc sports',
    76: 'fitness gaming',
    77: 'cardio dance',
    78: 'social dance',
    79: 'pickleball',
    80: 'cooldown',
    3000: 'other',
}

VALIDIC = {
    1: 'Cardiovascular',
    2: 'StrengthTraining',
    3: 'Sports',
    4: 'FitnessClass',
    5: 'YogaPilates',
    6: 'Lift_weights',
    7: 'Cross_train',
    8: 'Nike_training',
    9: 'Body_weight_exercise',
    10: 'Crosslift',
    11: 'P90X',
    12: 'Zumba',
    13: 'TRX',
    14: 'Swim',
    15: 'Bike',
    16: 'Elliptical',
    17: 'Bar_method',
    18: 'Kinect_exercises',
    19: 'Soccer',
    20: 'Ski_snowboard',
    21: 'Dance',
    22: 'Hike',
    23: 'Stationary_bike',
    24: 'Game',
    25: 'Other',
    1001: 'Walking',
    1002: 'Running',
    2001: 'Baseball',
    2002: 'Softball',
    2003: 'Cricket',
    3001: 'Golf',
    3002: 'Billiards',
    3003: 'Bowling',
    4001: 'Field_hockey',
    4002: 'Rugby',
    4003: 'Basketball',
    4004: 'Football',
    4005: 'Handball',
    4006: 'American_football',
    5001: 'Volleyball',
    5002: 'Beach_volleyball',
    6001: 'Squash',
    6002: 'Tennis',
    6003: 'Badminton',
    6004: 'Table_Tennis',
    6005: 'Racquetball',
    7001: 'Tai_chi',
    7002: 'Boxing',
    7003: 'Martial_arts',
    8001: 'Ballet',
    8002: 'Dancing',
    8003: 'Ballroom_dance',
    9001: 'Pilates',
    10001: 'Stretching',
    10002: 'Skipping',
    10003: 'Hula_hooping',
    10004: 'Push_up',
    10005: 'Pull_up',
    10006: 'Sit_up',
    10007: 'Circuit_training',
    11001: 'Inline_skating',
    11002: 'Hang_gliding',
    11003: 'Pistol_shooting',
    11004: 'Archery',
    11005: 'Horseback_riding',
    11007: 'Cycling',
    11008: 'Frisbee',
    11009: 'Roller_skiing',
    12001: 'Aerobic',
    13001: 'Hiking',
    13002: 'Rock_climbing',
    13003: 'Backpacking',
    13004: 'Mountain_biking',
    13005: 'Orienteering',
    14001: 'Not_Lap_Swimming',
    14002: 'Aquarobics',
    14003: 'Canoeing',
    14004: 'Sailing',
    14005: 'Skin_diving_Scuba_diving',
    14006: 'Snorkeling',
    14007: 'Kayaking',
    14008: 'Kite_surfing',
    14009: 'Rafting',
    14010: 'Rowing',
    14011: 'Windsurfing',
    14012: 'Yachting',
    14013: 'Water_Skiing',
    15001: 'Step_Machine',
    15002: 'Weight_Machine',
    15003: 'Stationary_Bicycle',
    15004: 'Rowing_machine',
    15006: 'Elliptical',
    16001: 'Cross_country_skiing',
    16002: 'Skiing',
    16003: 'Ice_Dancing',
    16004: 'Ice_Skating',
    16006: 'Ice_Hockey',
    16007: 'Snowboarding',
    16008: 'Alpine_skiing',
    16009: 'Snow_shoeing',
}

WELLDOC_APP = {
    1: 'Cardiovascular',
    2: 'StrengthTraining',
    3: 'Sports',
    4: 'FitnessClass',
    5: 'YogaPilates',
    100: 'Walking',
    101: 'Running',
    102: 'Hiking',
    103: 'Bicycling',
    104: 'Swimming',
    105: 'Strength_training',
    106: 'Home_activities',
    107: 'Gardening__Lawn',
    108: 'Dancing__Aerobics',
    109: 'Skiing__Skating',
    110: 'Yoga_Pilates',
    111: 'Other',
}

# ── Google Fit ───────────────────────────────────────────────────────────────
# Sources 37 and 40 (Google_Fit) emit Google's own activity-type enum offset by
# a FIXED 30000 -- not by the EntrySourceID the way Apple does, which is why
# source 40 also speaks 30xxx. Transcribed 2026-08-22 from
# https://developers.google.com/fit/rest/v1/reference/activity-types
#
# HOW THE OFFSET WAS CHECKED RATHER THAN ASSUMED. Google's enum is not dense:
# it skips 2, 6, 72, 107, 109-112 and 121. All 17 distinct codes this corpus
# actually carries land on VALID entries after subtracting 30000, and none in a
# hole. Under a wrong offset roughly one or two of seventeen would be expected
# to fall in a gap. The frequencies agree too: 30007 (Walking) is 78% of the
# Google Fit rows, which is what a step-counting app should look like.
GOOGLE_FIT_PREFIX = 30000

# Codes that are NOT exercise. Google's enum covers device state, not just
# workouts; these belong with the placeholders, never with a Compendium entry.
GOOGLE_FIT_NOT_EXERCISE = frozenset({0, 3, 4, 5, 108, 117, 118})

GOOGLE_FIT = {
    1: 'Bicycling', 7: 'Walking', 8: 'Running', 9: 'Aerobics',
    10: 'Badminton', 11: 'Baseball', 12: 'Basketball', 13: 'Biathlon',
    14: 'Handcycling', 15: 'Mountain_biking', 16: 'Road_biking',
    17: 'Spinning', 18: 'Stationary_biking', 19: 'Utility_biking',
    20: 'Boxing', 21: 'Calisthenics', 22: 'Circuit_training', 23: 'Cricket',
    24: 'Dancing', 25: 'Elliptical', 26: 'Fencing', 27: 'Football',
    28: 'Australian_football', 29: 'Soccer', 30: 'Frisbee', 31: 'Gardening',
    32: 'Golf', 33: 'Gymnastics', 34: 'Handball', 35: 'Hiking', 36: 'Hockey',
    37: 'Horseback_riding', 38: 'Housework', 39: 'Jumping_rope',
    40: 'Kayaking', 41: 'Kettlebell_training', 42: 'Kickboxing',
    43: 'Kitesurfing', 44: 'Martial_arts', 45: 'Meditation',
    46: 'Mixed_martial_arts', 47: 'P90X', 48: 'Paragliding', 49: 'Pilates',
    50: 'Polo', 51: 'Racquetball', 52: 'Rock_climbing', 53: 'Rowing',
    54: 'Rowing_machine', 55: 'Rugby', 56: 'Jogging', 57: 'Running_on_sand',
    58: 'Treadmill_running', 59: 'Sailing', 60: 'Scuba_diving',
    61: 'Skateboarding', 62: 'Skating', 63: 'Cross_skating',
    64: 'Inline_skating', 65: 'Skiing', 66: 'Back_country_skiing',
    67: 'Cross_country_skiing', 68: 'Alpine_skiing', 69: 'Kite_skiing',
    70: 'Roller_skiing', 71: 'Sledding', 73: 'Snowboarding',
    74: 'Snowmobile', 75: 'Snow_shoeing', 76: 'Squash',
    77: 'Stair_climbing', 78: 'Stair_climbing_machine',
    79: 'Stand_up_paddleboarding', 80: 'Strength_training', 81: 'Surfing',
    82: 'Swimming', 83: 'Swimming_pool', 84: 'Open_water_swimming',
    85: 'Table_tennis', 86: 'Team_sports', 87: 'Tennis',
    88: 'Treadmill', 89: 'Volleyball', 90: 'Beach_volleyball',
    91: 'Indoor_volleyball', 92: 'Wakeboarding', 93: 'Fitness_walking',
    94: 'Nordic_walking', 95: 'Treadmill_walking', 96: 'Waterpolo',
    97: 'Weightlifting', 98: 'Wheelchair', 99: 'Windsurfing', 100: 'Yoga',
    101: 'Zumba', 102: 'Diving', 103: 'Ergometer', 104: 'Ice_Skating',
    105: 'Indoor_skating', 106: 'Curling', 113: 'Crossfit', 114: 'HIIT',
    115: 'Interval_Training', 116: 'Stroller_walking', 119: 'Archery',
    120: 'Softball', 122: 'Guided_Breathing',
}

BOOKS = {"apple": APPLE_HK, "validic": VALIDIC,
         "welldoc_app": WELLDOC_APP, "google_fit": GOOGLE_FIT}

# Which books prefix their codes, and by how much. TWO callers need this --
# dialect.py to resolve a row and the benchmark's taxonomy.py to type one --
# and they used to each carry their own copy, which is how adding Google Fit
# fixed the resolver and left every one of those rows still typed opaque_code.
# One table, one decoder, both read it.
PREFIX = {"apple": APPLE_PREFIX, "google_fit": GOOGLE_FIT_PREFIX}

# Codes inside a book that are not exercise at all.
NOT_EXERCISE = {"google_fit": GOOGLE_FIT_NOT_EXERCISE}


def decode(code, book):
    """A vendor code -> its own book's label, or None. Never another book's."""
    table = BOOKS.get(book)
    if not table:
        return None
    try:
        key = int(code) - PREFIX.get(book, 0)
    except (TypeError, ValueError):
        return None
    if key in NOT_EXERCISE.get(book, ()):
        return None
    return table.get(key)
