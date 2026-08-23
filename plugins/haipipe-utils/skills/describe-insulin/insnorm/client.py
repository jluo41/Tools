"""
The door. describe-insulin turns an insulin product name into pharmacokinetics.

    from insnorm import normalize
    normalize(["Insulin lispro-aabc"])
    normalize(["basal insulin"], dia_hours=[7.0])     # per-patient override

WHERE ITS INPUT COMES FROM
================================================================================
describe-medication's `DrugKey`. That field is the SEAM between the two skills:
it carries the FDA ingredient when the Directory listed the drug, and the words
the log itself used when it did not. Routing on the FDA ingredient alone would
lose all 5,026 OhioT1DM rows (which log a CLASS, never a product) and 419 of
Shanghai's (whose products the Directory does not list) -- 5,445 rows, which is
the whole reason this is a separate skill rather than a lane inside the other
one. Shanghai is worse than that number suggests: its column declares 3,490
insulin rows and only 1,197 get a curve from either half.

    describe-medication  →  DrugKey  →  describe-insulin
                            "insulin lispro" / "Novolin R" / "basal insulin"

WHAT COMES BACK IS PARAMETERS, NOT A CURVE
================================================================================
    InsulinClass  rapid | short | intermediate | long | ultra_long | premix
    OnsetMin      time to the start of effect
    PeakMin       time to maximum effect, or NULL when the drug is PEAKLESS
    DurationMin   time until the effect is no longer meaningful
    Biphasic      True for premixes, where one triple is an approximation

Insulin-on-board is a CURVE and it is deliberately not computed here. Turning
(onset, peak, duration) into an IOB series is a convolution over a 5-minute
grid, which is a RecordFn's job; a normalizer answers one row with one row. Put
the curve in here and the door stops being the family's door.

CONFIDENCE, and the one way to reach GOOD
================================================================================
    GOOD   the caller supplied a DIA measured on THIS patient. WellDoc's
           MedPrescription carries one for 15.7% of prescriptions -- 5.0, 7.0 or
           2.0 hours -- and that beats any table.
    OK     the curated table. Population values from FDA labels.
    ALIAS  a combination product resolved to its insulin component.
    MISS   not an insulin this table knows.
"""
import os
import re
from typing import Dict, List, Optional, Sequence, Union

from .pk_table import (ALIASES, COMBINATIONS, PK, PK_BASIS, REFERENCE_BASIS,
                       UNSUPPORTED_BASIS)

DEFAULT_TRANSPORT = os.environ.get("INSNORM_TRANSPORT", "local")
DEFAULT_URL = os.environ.get("INSNORM_URL", "http://127.0.0.1:8080")

GOOD, OK, ALIAS, MISS = "GOOD", "OK", "ALIAS", "MISS"
TRUSTED = (GOOD, OK, ALIAS)

FIELDS = ("InsulinClass", "OnsetMin", "PeakMin", "DurationMin", "Biphasic",
          "InsulinResolved", "DeliveryMode", "PKBasis", "PKSource", "PKConf")

# TWO FIELDS ADDED 260822, AND THEY ANSWER DIFFERENT QUESTIONS (rule 5)
# ---------------------------------------------------------------------------
# DeliveryMode  WHAT THE LOG SAID. An echo of the caller's input, exactly like
#               `dia_hours`, and like it, it must SURVIVE A BANK MISS: a route
#               the log stated is a fact whether or not we recognised the drug.
#               mdi | pump_bolus | pump_basal | pump_suspend | iv | None
#
# PKBasis       THE SCALE THESE NUMBERS ARE ON, which is rule 4. The bench
#               profile used to declare `scaled=()` and argue that onset, peak
#               and duration are properties of the drug that do not scale, so
#               rule 4 had nothing to govern here. Shanghai's 29 intravenous
#               rows falsify that: with no subcutaneous depot there is no
#               absorption phase, and a 4.5-hour curve is wrong by an order of
#               magnitude. A duration of 270 minutes is not interpretable
#               without the route it was measured on.
#               subcutaneous_bolus | subcutaneous_rate | intravenous |
#               subcutaneous_reference  (the log did not say; see rule 4)

Scalarish = Union[None, float, int, str, Sequence]

# Strength and formulation suffixes that do not change the molecule.
# Strength and formulation suffixes that do not change the molecule -- plus the
# DEVICE words, added 260822. 'ADMELOG' resolved and 'ADMELOG SOLO' did not,
# because `solostar` was here and its abbreviation `solo` was not; the same held
# for FlexTouch, KwikPen and the Humalog Junior pen. A device is not a drug.
_STRIP = re.compile(
    r"\b(u-?\d+|\d+\s*unit(s)?/?m?l?|injection|solution|soln|susp|suspension|"
    r"pen|kwikpen|kwpn|kwk|kwik|flexpen|flextouch|flex|solostar|solos|solo|"
    r"tempo|sensor|cartridge|vial|insuln|inj|max|jr|junior|disp)\b",
    re.I)


def canon(name) -> str:
    """Fold a drug string to an ALIASES key."""
    s = str(name or "").lower()
    s = re.sub(r"\(([^)]*)\)", r" \1 ", s)      # unwrap a parenthesised brand
    s = _STRIP.sub(" ", s)
    s = re.sub(r"[^a-z0-9/ -]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _spread(v, n, name):
    if v is None:
        return [None] * n
    if isinstance(v, (int, float, str)):
        return [v] * n
    v = list(v)
    if len(v) != n:
        raise ValueError(f"{name} has {len(v)} values for {n} items")
    return v


def _empty(source: str) -> Dict:
    d = {k: None for k in FIELDS}
    d["PKSource"] = source
    d["PKConf"] = MISS
    return d


def _basis(mode) -> str:
    """The scale these numbers are on. Never None while a number is written.

    An unstated route is not an unknown scale: it is the REFERENCE scale, named
    so, which is rule 4's shape. `None` would let a duration be written with no
    scale beside it, and 270 minutes without a route is not interpretable.
    """
    m = str(mode or "").strip().lower()
    return PK_BASIS.get(m, REFERENCE_BASIS if not m else m)


def _lookup(name):
    """(pk key, confidence, source) for one drug string."""
    c = canon(name)
    if not c:
        return None, MISS, "not_resolvable:empty"
    if c in COMBINATIONS:
        key, note = COMBINATIONS[c]
        return key, ALIAS, f"combination:{note.split(';')[0]}"
    if c in ALIASES:
        return ALIASES[c], OK, f"label_table:{ALIASES[c]}"
    # A brand or generic buried in a longer string: match the LONGEST alias
    # contained in it, so 'insulin lispro-aabc' never matches 'insulin lispro'.
    best = None
    for a in ALIASES:
        if a in c and (best is None or len(a) > len(best)):
            best = a
    if best:
        return ALIASES[best], OK, f"label_table:{ALIASES[best]}"
    return None, MISS, "label_table:no_match"


def _more_specific(a, b):
    """Of two resolved keys, the one that says MORE -- or None if neither does.

    'insulin aspart 70/30' says everything 'insulin aspart' says and adds the
    premix ratio, so its token set is a STRICT SUPERSET. Same for
    'insulin glargine u300' over 'insulin glargine'. Anything else -- disagreeing
    keys, equal keys -- is not a specificity question and this returns None
    rather than guessing which source to trust.
    """
    if a is None or b is None or a == b:
        return None
    ta, tb = set(a.split()), set(b.split())
    if ta > tb:
        return a
    if tb > ta:
        return b
    return None


def _normalize_local(items, dia_hours=None, delivery=None, raw=None,
                     **kw) -> List[Dict]:
    n = len(items)
    dias = _spread(dia_hours, n, "dia_hours")
    modes = _spread(delivery, n, "delivery")
    raws = _spread(raw, n, "raw")
    cache, out = {}, []
    for i, item in enumerate(items):
        k = str(item)
        if k not in cache:
            cache[k] = _lookup(item)
        key, conf, src = cache[k]

        # THE SEAM CAN BE COARSER THAN THE LOG, AND BOTH ARE AVAILABLE.
        # describe-medication resolves 'insulin aspart 70/30' to the ingredient
        # `insulin aspart` and the premix ratio is gone before this door sees
        # the string -- 356 Shanghai rows read `rapid` when they are `premix`,
        # which loses a whole second rise. TOUJEO MAX loses U-300 the same way.
        #
        # Rule 9 says the seam carries the best string available. When a caller
        # can hand over the LOG's words as well, the best string is knowable
        # rather than assumed: take whichever resolves to the more specific key,
        # and record in PKSource that the raw string was the one used.
        alt = raws[i]
        if alt not in (None, ""):
            ak = str(alt)
            if ak not in cache:
                cache[ak] = _lookup(alt)
            akey, aconf, asrc = cache[ak]
            # `akey is not None` FIRST. Without it, a raw string that resolves
            # to nothing makes _more_specific return None, which then compares
            # EQUAL to akey and overwrites a perfectly good seam answer with
            # nothing. Caught by the probe 'insulin lispro' + 'some junk'.
            if akey is not None and _more_specific(akey, key) == akey:
                key, conf = akey, aconf
                src = f"raw_more_specific:{akey}+{src}"
        mode = modes[i]
        mode = str(mode).strip().lower() if mode not in (None, "") else None
        basis = _basis(mode)
        d = _empty(src)
        # RULE 9: the route the log stated survives a bank miss. A drug we could
        # not name was still given by some route, and erasing that would lose a
        # fact the caller handed us.
        d["DeliveryMode"] = mode
        d["PKBasis"] = basis
        if key is None:
            out.append(d)
            continue

        # RULE 3: on a route this table was not measured on, write no numbers.
        # A confidently wrong duration is worse than a missing one, and nothing
        # downstream can tell an intravenous 4.5 hours from a real measurement.
        if basis in UNSUPPORTED_BASIS:
            d["PKSource"] = f"route_unsupported:{mode}+{src}"
            d["PKConf"] = MISS
            d["InsulinResolved"] = key
            out.append(d)
            continue
        cls, onset, peak, dur, biph, note = PK[key]
        d.update(InsulinClass=cls, OnsetMin=onset, PeakMin=peak,
                 DurationMin=dur, Biphasic=biph, InsulinResolved=key,
                 DeliveryMode=mode, PKBasis=basis, PKSource=src, PKConf=conf)
        # A DIA measured on this patient beats the table, and only the DURATION
        # is measured -- onset and peak stay the table's, so the record says
        # plainly which parts are this patient's and which are the population's.
        dia = dias[i]
        try:
            dia = float(dia) if dia is not None else None
        except (TypeError, ValueError):
            dia = None
        if dia and dia > 0:
            d["DurationMin"] = dia * 60.0
            d["PKSource"] = f"patient_dia:{dia}h+{src}"
            d["PKConf"] = GOOD
        out.append(d)
    return out


def _normalize_http(items, dia_hours=None, delivery=None, raw=None, url=None,
                    timeout=None, **kw):
    import requests
    base = (url or DEFAULT_URL).rstrip("/")
    body = {"items": list(items)}
    if dia_hours is not None:
        body["dia_hours"] = (dia_hours if isinstance(dia_hours, (int, float, str))
                             else list(dia_hours))
    if delivery is not None:
        body["delivery"] = (delivery if isinstance(delivery, str)
                            else list(delivery))
    if raw is not None:
        body["raw"] = raw if isinstance(raw, str) else list(raw)
    r = requests.post(f"{base}/normalize/batch", json=body,
                      timeout=int(timeout or os.environ.get("INSNORM_TIMEOUT", "600")))
    r.raise_for_status()
    return r.json()["results"]


TRANSPORTS = {"local": _normalize_local, "http": _normalize_http}


def normalize(items: Sequence[str], dia_hours: Scalarish = None,
              delivery: Scalarish = None, raw: Scalarish = None,
              transport: Optional[str] = None, **kw) -> List[Dict]:
    """Batch, order-preserving, one result per input, duplicates resolved once.

    `delivery` is how the row entered the body, one per item or one for all:
    mdi | pump_bolus | pump_basal | pump_suspend | iv. It is optional and
    unknown is the honest default -- most logs do not say.

    `raw` is the LOG's OWN STRING when the caller has it, beside the seam string
    in `items`. Used only when it resolves to a strictly MORE SPECIFIC key --
    a premix ratio or a concentration the upstream bank stripped. Never used to
    override a disagreement.
    """
    t = transport or DEFAULT_TRANSPORT
    if t not in TRANSPORTS:
        raise ValueError(f"unknown transport {t!r}; have {sorted(TRANSPORTS)}")
    return TRANSPORTS[t](list(items), dia_hours=dia_hours, delivery=delivery,
                         raw=raw, **kw)
