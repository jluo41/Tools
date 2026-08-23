"""
Stage 2: a typed activity becomes a compendium entry, or honestly nothing.

THE LADDER
================================================================================
    ALIAS   the curated map named this exact entry. A human chose it and wrote
            down why (alias_dict.py). VALUE IS WRITTEN.
    OK      RESERVED AND CURRENTLY UNREACHABLE. See CONF_CAP.
    WEAK    the fuzzy tier found something plausible. VALUE IS NULL; the
            candidate rides along in ActivityResolved so a person can promote it
            into the curated map, which is the only way it ever becomes a value.
    MISS    nothing. VALUE IS NULL.

WHY THE FUZZY TIER MAY NOT WRITE A VALUE
================================================================================
It was measured and it is not good enough, and the failure is not random. A
one-token query scores 1.0 against any description containing that token, so
'sports' -- 457 rows across three cohorts -- returns 'Sports spectator, very
excited', MET 3.3, head-anchored, perfect score. A patient who logged Sports was
not watching one.

Tightening the scorer would move that one case and leave the class of case
intact, because the query genuinely does not identify an activity. The class is
only fixable by a person adding a line to alias_dict.py, so the ladder is built
to ASK for that line rather than to paper over its absence. This is rule 3 of
haipipe-norm: a confidently wrong MET is worse than a missing one, because
nothing downstream can tell it from a measurement.

WHY GOOD IS UNREACHABLE
================================================================================
The bank on this machine is a third-party mirror of the 2024 Compendium, not the
publisher's file -- pacompendium.com returns 403 to non-browser clients. It
checks out on every structural test available (1,111 of 1,114 activities, the
standard 5-digit codes, all 22 major headings), and that is still not the
publisher. So nothing this bank produces may be stamped GOOD until someone
replaces the file. The cap is code, not a note, because a note would not survive
the next person's confidence.
"""
from typing import Dict, Optional, Tuple

from .alias_dict import ALIAS_CODE
from .constants import ALIAS, MISS, OK, WEAK
from .dialect import Activity
from .constants import SESSION
from . import met_db

# Highest confidence this bank may issue. See the docstring.
CONF_CAP = OK

# A fuzzy hit below this is not worth showing a person.
FUZZY_FLOOR = 0.5


def resolve(act: Activity, path=None) -> Tuple[Optional[Dict], str, str]:
    """One typed activity -> (compendium row or None, confidence, source).

    Only a SESSION reaches the bank. A daily roll-up, a placeholder, and an
    opaque vendor code each return a DIFFERENT source string, because they are
    different failures: 'this is not a bout', 'nothing was named', and 'the
    codebook is not on this machine'. Rule 5 -- they may not share a column.
    """
    if act.kind != SESSION:
        return None, MISS, f"not_resolvable:{act.kind}"

    hit = ALIAS_CODE.get(act.name)
    if hit:
        row = met_db.by_code(hit[0], path)
        if row is not None:
            return row, ALIAS, f"compendium2024:alias:{hit[0]}"

    cands = met_db.search(act.name, k=3, path=path)
    top = cands[0] if cands else None
    if top and top["__anchored"] and top["__score"] >= FUZZY_FLOOR:
        # WEAK on purpose. The row travels so a person can curate it; the VALUE
        # does not travel, because aggregate.py writes only for TRUSTED.
        return top, WEAK, f"compendium2024:fuzzy:{top['activity_code']}"

    return None, MISS, "compendium2024:no_match"
