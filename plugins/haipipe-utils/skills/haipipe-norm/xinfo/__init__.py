"""
The shared writer for every `_<Noun>Info/` folder.

WHY THIS IS CODE, IN A SKILL THAT SAYS IT SHIPS NONE
================================================================================
haipipe-norm owns the contract and no RESOLVER code; that rule stands. This is
not a resolver. It is the contract's own writer, and it lives here because the
alternative was measured and rejected.

`_FoodInfo` and `_ExerciseInfo` were built independently by two sessions. Both
are good. They share exactly TWO keys -- `cohort` and `rows` -- and each invented
the half the other was missing:

    _FoodInfo      SHAPE x LABEL as orthogonal axes, a frozen gold corpus, a
                   JSON Schema contract with worked specimens
    _ExerciseInfo  the HONEST DENOMINATOR, and putting the resolver's OUTPUT on
                   the per-cohort page instead of only its input

Neither exposed the two columns the whole family discipline rests on:
the CONFIDENCE distribution (rule 3) and the BASIS distribution (rule 4).

Three normalizers writing three folders produced three schemas. A fourth would
have produced a fourth, and the calibration benchmark would have to be written
once per noun. So the writer is shared and the schema is one file.


WHAT A MEMBER STILL OWNS
================================================================================
Everything that is actually about its noun: how to type a row, what its golds
are, what its per-cohort page says. A member calls `write()` with a list of
cohort records and its own rendered pages; this module owns only the SHAPE.

    from xinfo import CohortStats, write

    stats = [CohortStats(noun="medication", cohort=c, rows=n, ...) ...]
    write(noun="medication", emoji="💊", dest=..., stats=stats, pages=...)
"""
from .writer import (CohortStats, copy_api_examples, link_reference,
                     render_index, validate, write)

__all__ = ["CohortStats", "write", "validate", "render_index",
           "link_reference", "copy_api_examples"]
__version__ = "1.0.0"
