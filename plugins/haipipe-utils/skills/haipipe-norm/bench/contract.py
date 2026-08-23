"""B1 CONTRACT -- ten invariants, no labels, every noun.

Each check is one sentence a caller is entitled to believe. None of them needs
a gold, which is why B1 can run on day one and on every noun at once, and why
it is the honest evidence for the word NORMALIZED. B2 measures whether an
answer is right; only B1 measures whether four skills are one system.

Every check states the rule it enforces and the defect that earned it.
"""
import json
import traceback
from typing import Dict, List, Optional

CHECKS = [
    ("C01", "keys",         "the promised keys are on every result, hit and miss alike"),
    ("C02", "vocabulary",   "confidence is a declared word, and trusted is a prefix"),
    ("C03", "rule3",        "an untrusted result writes no governed value"),
    ("C04", "rule4",        "a scaled number states the scale it is on"),
    ("C05", "rule5",        "the source column answers even when nothing resolved"),
    ("C06", "determinism",  "the same input twice gives byte-identical output"),
    ("C07", "batch_eq_one", "a batch answers what one-at-a-time answers"),
    ("C08", "order_dupes",  "order is preserved and a duplicate repeats verbatim"),
    ("C09", "empty",        "an empty batch is an empty list, not an error"),
    ("C10", "blank_null",   "a blank and a None are typed, never crashed on"),
    ("C12", "none_not_nan",  "an absent value is None; NaN is not a null this contract has"),
    ("C13", "echo",         "a number the caller supplied survives a bank miss"),
]


def _key(d: Dict) -> str:
    return json.dumps(d, sort_keys=True, default=str)


def _null(v) -> bool:
    """A value counts as absent whether it is None or NaN.

    They are NOT the same object and C12 is about exactly that difference, but
    the other checks are about the RULES, and letting a dtype accident make
    rule 3 read as violated would hide the real finding behind a false one.
    """
    if v is None:
        return True
    return isinstance(v, float) and v != v


class Ctx:
    """Everything a check may read, gathered once."""

    def __init__(self, prof, cases: List[Dict]):
        self.prof = prof
        self.cases = cases            # [{name, request, expected, results|error}]
        self.rows = [(c["name"], r) for c in cases
                     for r in (c.get("results") or [])]


# ------------------------------------------------------------------ checks --

def c01_keys(p, ctx):
    """A caller must never branch on the SHAPE of a reply, only on its
    confidence. That is only true if a miss carries the same keys as a hit --
    describe-exercise says so in its own contract, 'always all eleven'."""
    bad, extra = [], set()
    for name, r in ctx.rows:
        missing = [k for k in p.required if k not in r]
        if missing:
            bad.append({"case": name, "missing": missing})
        extra |= (set(r) - set(p.required) - set(p.optional))
    return _res(bad, len(ctx.rows), undeclared=sorted(extra))


def c02_vocabulary(p, ctx):
    """A confidence nobody can rank is decoration. xinfo-v1 made the order a
    declared field precisely so a benchmark could read it instead of hard-coding
    GOOD/OK/ALIAS -- describe-food ranks MEASURED/ESTIMATED and is no less
    ordered for it."""
    bad = []
    if list(p.trusted) != list(p.conf_order[:len(p.trusted)]):
        bad.append({"case": "<declaration>",
                    "why": f"trusted {p.trusted} is not a prefix of {p.conf_order}"})
    for name, r in ctx.rows:
        v = r.get(p.conf_field)
        if v not in p.conf_order:
            bad.append({"case": name, "why": f"{p.conf_field}={v!r} not in {p.conf_order}"})
    return _res(bad, len(ctx.rows) + 1)


def c03_rule3(p, ctx):
    """TRUSTED ONLY. A confidently wrong value is worse than a missing one,
    because nothing downstream can tell it apart from a measurement.

    One-directional on purpose: untrusted implies null, but trusted does NOT
    imply non-null. Insulin glargine is peakless and its PeakMin is a real
    NULL in a fully resolved row."""
    bad = []
    for name, r in ctx.rows:
        if r.get(p.conf_field) in p.trusted:
            continue
        wrote = [k for k in p.governed if not _null(r.get(k))]
        if wrote:
            bad.append({"case": name, "conf": r.get(p.conf_field), "wrote": wrote})
    return _res(bad, len(ctx.rows))


def c04_rule4(p, ctx):
    """BASIS IS A COLUMN. Never invent the quantity the log did not state; say
    on what scale the number you did give is reported."""
    if not p.scaled or not p.basis_field:
        return {"status": "NA", "n": 0, "failures": [],
                "why_na": "this noun reports nothing that sits on a scale"}
    bad = []
    for name, r in ctx.rows:
        if any(not _null(r.get(k)) for k in p.scaled) and _null(r.get(p.basis_field)):
            bad.append({"case": name,
                        "wrote": [k for k in p.scaled if not _null(r.get(k))]})
    return _res(bad, len(ctx.rows))


def c05_rule5(p, ctx):
    """PROVENANCE NEVER FOLDS. The source column carries the REASON, so it is
    non-null on a miss too -- 'the bank did not know it' and 'the log named
    nothing' are different failures with different fixes."""
    bad = [{"case": n} for n, r in ctx.rows if not r.get(p.source_field)]
    return _res(bad, len(ctx.rows))


def c06_determinism(p, ctx):
    """A resolver with a nondeterministic answer cannot be benchmarked at all,
    and a cook re-run would silently rewrite a column."""
    bad = []
    a, b = p.door(list(p.probe)), p.door(list(p.probe))
    for i, (x, y) in enumerate(zip(a, b)):
        if _key(x) != _key(y):
            bad.append({"case": p.probe[i], "first": x, "second": y})
    return _res(bad, len(p.probe))


def c07_batch_eq_one(p, ctx):
    """BATCH IS THE UNIT is a performance claim; it becomes a correctness claim
    the moment a caller may choose either. Any cache, any dedup, any
    cross-row inference breaks this and nothing else would catch it."""
    bad = []
    batch = p.door(list(p.probe))
    for i, s in enumerate(p.probe):
        one = p.door([s])[0]
        if _key(one) != _key(batch[i]):
            bad.append({"case": s, "alone": one, "in_batch": batch[i]})
    return _res(bad, len(p.probe))


def c08_order_dupes(p, ctx):
    """One result per input, in order, duplicates resolved once and returned
    verbatim. Every door dedups internally; a fan-out that lost the order
    would shift every later row onto the wrong event."""
    xs = list(p.probe) + [p.probe[0]]
    out = p.door(xs)
    bad = []
    if len(out) != len(xs):
        bad.append({"case": "<length>", "want": len(xs), "got": len(out)})
    else:
        ref = p.door(list(p.probe))
        for i, s in enumerate(p.probe):
            if _key(out[i]) != _key(ref[i]):
                bad.append({"case": s, "why": "position moved"})
        if _key(out[-1]) != _key(out[0]):
            bad.append({"case": p.probe[0], "why": "duplicate did not repeat verbatim"})
    return _res(bad, len(xs))


def c09_empty(p, ctx):
    out = p.door([])
    bad = [] if out == [] else [{"case": "<empty>", "got": out}]
    return _res(bad, 1)


def c10_blank_null(p, ctx):
    """TYPE, DO NOT DELETE. A blank is a real row in every cohort; it must come
    back as one untrusted result, not as a crash and not as a dropped row."""
    bad = []
    for label, xs in (("''", [""]), ("None", [None]), ("' '", ["   "])):
        try:
            out = p.door(xs)
        except Exception as e:                                   # noqa: BLE001
            bad.append({"case": label, "raised": f"{type(e).__name__}: {e}"})
            continue
        if len(out) != 1:
            bad.append({"case": label, "why": f"returned {len(out)} results"})
        elif out[0].get(p.conf_field) in p.trusted:
            bad.append({"case": label, "why": f"a blank was trusted: {out[0]}"})
    return _res(bad, 3)


def c12_none_not_nan(p, ctx):
    """A float NaN is not the absence this contract promises, and three
    separate things break when one leaks through:

        `x is None` is False, so every downstream guard silently passes
        `NaN == NaN` is False, so no two results ever compare equal
        json.dumps writes the bare token NaN, which is not JSON, so the
            local door and the HTTP door stop agreeing

    It is a dtype accident, never a decision: a pandas column holding one
    number and one blank is float64, and the blank becomes NaN on the way out.
    Which is why it is BATCH-DEPENDENT and a single-row test cannot see it.
    """
    bad = []
    for name, r in ctx.rows:
        nan = [k for k, v in r.items() if isinstance(v, float) and v != v]
        if nan:
            bad.append({"case": name, "nan_fields": nan})
    return _res(bad, len(ctx.rows))


def c13_echo(p, ctx):
    """A bank miss is a fact about the bank, and it is not a licence to forget
    what the log said.

    Rule 9 was written for the SEAM field -- DrugKey must survive a miss or the
    chain's second half never runs. The same argument covers every echoed
    input, and this check is where the family finds out whether it does. The
    probe list is mixed on purpose: the interesting rows are the ones that miss.

    NOT ONLY NUMBERS. This compared with `float()` on both sides until 260822,
    because the first two echoes it was written for were quantities -- an
    exercise ActiveMinutes and a medication DoseValue. describe-insulin echoes a
    ROUTE, which is a word, and the check ERRORED on it rather than failing or
    passing: the docstring above already claimed to cover every echoed input,
    so the coercion was the defect and not the profile that tripped it.
    """
    if not p.echo:
        return {"status": "NA", "n": 0, "failures": [],
                "why_na": "this door takes a name and nothing else to echo"}

    def same(got, want):
        try:
            return float(got) == float(want)
        except (TypeError, ValueError):
            # A word, and case/whitespace folding is the door's business.
            return str(got).strip().lower() == str(want).strip().lower()

    bad, n = [], 0
    for kwarg, (fieldname, value) in p.echo.items():
        for i, r in enumerate(p.door(list(p.probe), **{kwarg: value})):
            n += 1
            got = r.get(fieldname)
            if _null(got) or not same(got, value):
                bad.append({"case": p.probe[i], "sent": f"{kwarg}={value}",
                            "want": f"{fieldname}={value}", "got": got,
                            "conf": r.get(p.conf_field)})
    return _res(bad, n)


FNS = {"C01": c01_keys, "C12": c12_none_not_nan, "C13": c13_echo, "C02": c02_vocabulary, "C03": c03_rule3,
       "C04": c04_rule4, "C05": c05_rule5, "C06": c06_determinism,
       "C07": c07_batch_eq_one, "C08": c08_order_dupes, "C09": c09_empty,
       "C10": c10_blank_null}


def _res(bad, n, **extra):
    d = {"status": "PASS" if not bad else "FAIL", "n": n,
         "n_bad": len(bad), "failures": bad[:12]}
    d.update({k: v for k, v in extra.items() if v})
    return d


# -------------------------------------------------------------------- run --

def replay(prof, fixtures: List[Dict]) -> List[Dict]:
    """Send every fixture request back through the door.

    A fixture whose stored response is an error payload is an ERROR CASE: the
    contract is that the door REFUSES it, so a clean return is the failure.
    """
    cases = []
    for fx in fixtures:
        c = {"name": fx["name"], "group": fx["group"], "expects_error": fx["is_error"]}
        try:
            c["results"] = prof.call(fx["request"])
            c["raised"] = None
        except Exception as e:                                   # noqa: BLE001
            c["results"] = []
            c["raised"] = f"{type(e).__name__}: {e}"
            c["trace"] = traceback.format_exc().strip().splitlines()[-1]
        cases.append(c)
    return cases


def run_b1(prof, fixtures: List[Dict]) -> Dict:
    cases = replay(prof, fixtures)

    # The error fixtures are graded on their own terms and then set aside: a
    # 422 has no confidence column and would fail nine checks meaninglessly.
    errs = [c for c in cases if c["expects_error"]]
    err_bad = [{"case": c["name"], "why": "returned instead of refusing"}
               for c in errs if not c["raised"]]
    ok = [c for c in cases if not c["expects_error"]]
    crashed = [{"case": c["name"], "raised": c["raised"]} for c in ok if c["raised"]]

    ctx = Ctx(prof, [c for c in ok if not c["raised"]])
    results = {}
    for cid, name, why in CHECKS:
        try:
            r = FNS[cid](prof, ctx)
        except Exception as e:                                   # noqa: BLE001
            r = {"status": "ERROR", "n": 0, "n_bad": 1,
                 "failures": [{"case": "<check>",
                               "raised": f"{type(e).__name__}: {e}"}]}
        r.update({"name": name, "asserts": why})
        results[cid] = r

    if crashed:
        results["C00"] = {"name": "replay", "status": "FAIL",
                          "asserts": "every real fixture request replays through the door",
                          "n": len(ok), "n_bad": len(crashed), "failures": crashed[:12]}
    if err_bad:
        results["C11"] = {"name": "refusals", "status": "FAIL",
                          "asserts": "a request the service 422s on is refused locally too",
                          "n": len(errs), "n_bad": len(err_bad), "failures": err_bad}
    elif errs:
        results["C11"] = {"name": "refusals", "status": "PASS",
                          "asserts": "a request the service 422s on is refused locally too",
                          "n": len(errs), "n_bad": 0, "failures": []}

    n_fail = sum(1 for r in results.values() if r["status"] in ("FAIL", "ERROR"))
    return {
        "noun": prof.noun,
        "skill": prof.skill,
        "profile": prof.dict(),
        "n_fixtures": len(fixtures),
        "n_replayed": len(ctx.cases),
        "n_records": len(ctx.rows),
        "verdict": "PASS" if not n_fail else "FAIL",
        "n_checks_failed": n_fail,
        "checks": results,
    }
