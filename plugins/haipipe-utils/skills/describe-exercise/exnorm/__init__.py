"""
describe-exercise: a logged activity, in a cohort's own dialect, becomes a MET
and -- when the log stated minutes and the patient's mass is known -- a kcal
that carries its own provenance.

    from exnorm import normalize
    normalize(["Walking"], minutes=30, weight_kg=82)
    # [{'METValue': 3.8, 'ActiveMinutes': 30.0, 'CaloriesBurnedEst': 159.6,
    #   'ActivityResolved': 'Walking, 2.8 to 3.4 mph, level, moderate pace...',
    #   'ActivityCode': '17190', 'MajorHeading': 'Walking',
    #   'ExerciseSource': 'compendium2024:alias:17190', 'ExerciseConf': 'ALIAS',
    #   'ExerciseBasis': 'per_session', 'TypeSource': 'logged:session',
    #   'TypeConf': 'typed'}]

`normalize` is the whole public surface. Everything else is an implementation
detail and may be rewritten without notice -- see haipipe-norm rule 1.

WHAT THIS CANNOT DO YET, stated here so nobody has to discover it:
103 of the 135 activity types in 1-SourceStore are opaque vendor codes with no
codebook on this machine. They are TYPED (`opaque_code`) and PARKED, never
guessed. SKILL.md, section PARKED, has the four namespaces and what it would
take to unpark them.
"""
from .client import DEFAULT_TRANSPORT, DEFAULT_URL, TRANSPORTS, normalize
from .constants import (BASES, FIELDS, IDENTITY, PROVENANCE, TRUSTED, TYPES,
                        VALUES)

__all__ = ["normalize", "FIELDS", "VALUES", "IDENTITY", "PROVENANCE",
           "TYPES", "BASES", "TRUSTED", "TRANSPORTS",
           "DEFAULT_TRANSPORT", "DEFAULT_URL"]
__version__ = "0.1.0"
