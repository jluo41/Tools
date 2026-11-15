"""Acceptance prose compiled into v2 criteria: quoted phrases and {PLACEHOLDER}s become contains, excludes,
starts_with or ends_with checks, a character cap becomes max_chars, and anything else a judged criterion
(split out of design_actions.py)."""
from __future__ import annotations

import re

# A quote opens after a space or line start and closes before one, so the apostrophe
# in "it's" or "doesn't" is never read as a quote mark (audit H1, 260918).
_QUOTED = re.compile(r"(?<!\w)['\"‘“](.+?)['\"’”](?!\w)")
_NEGATIVE = re.compile(r"\b(?:no|not|never|without|excludes?|avoids?|don['’]t|doesn['’]t|isn['’]t)\b", re.I)
_ENDS = re.compile(r"\b(?:ends|ending|finishes)\s+with\b", re.I)
_STARTS = re.compile(r"\b(?:starts|starting|begins|opens)\s+with\b", re.I)
_RENDER = re.compile(r"\brender(?:s|ed|ing)?\b", re.I)
_PLACEHOLDER = re.compile(r"\{[A-Za-z_]+\}")
_MAX_CHARS = re.compile(r"(≤|<=|<|at most|max(?:imum)?|no more than|under|fewer than|less than)\s*(\d+)\s*(?:chars?|characters?|字)", re.I)
_STRICT = ("<", "under", "fewer than", "less than")
_MAX_CHARS_2 = re.compile(r"(\d+)\s*(?:chars?|characters?)\s*(?:max|cap|or fewer|or less)", re.I)


# --------------------------------------------------------------- criteria --

_CLAUSE = re.compile(r",|;|\band\b|\bbut\b|\bwhile\b|\bthen\b", re.I)
_CONNECTOR = re.compile(r"^(?:\s|,|\bor\b|\bnor\b|\band\b)*$", re.I)


def _phrases(rule: str) -> list[tuple[str, str]]:
    """(kind, phrase) for every quoted phrase and {PLACEHOLDER} of a rule, in order.

    Each phrase reads the words just before it, back to the last clause break:
    "keeps 'Hi' and does not say 'urgent'" contains Hi and excludes urgent.  A
    phrase with only "or"/"and"/commas before it shares the previous one's kind,
    so "no 'urgent', 'act now' or 'hurry'" excludes all three."""
    quoted = [(m.start(), m.end(), m.group(1)) for m in _QUOTED.finditer(rule)]
    spans = quoted + [(m.start(), m.end(), m.group(0)) for m in _PLACEHOLDER.finditer(rule)
                      if not any(a <= m.start() < b for a, b, _ in quoted)]
    out, prev_end, prev_kind = [], 0, None
    for start, end, phrase in sorted(spans):
        before = rule[prev_end:start]
        part = _CLAUSE.split(before)[-1]
        if prev_kind and _CONNECTOR.match(before):
            kind = prev_kind
        else:
            words = part if part.strip() else before
            kind = ("excludes" if _NEGATIVE.search(words) else "ends_with" if _ENDS.search(words)
                    else "starts_with" if _STARTS.search(words) else "contains")
        out.append((kind, phrase))
        prev_end, prev_kind = end, kind
    return out


def compile_criteria(acceptance: list[str]) -> list[dict]:
    """Turn acceptance prose into v2 criteria; anything not mechanical is semantic.

    Rule N compiles to criterion ``rNN``; a rule quoting several phrases adds
    ``rNNb``, ``rNNc`` for the rest, so "no 'urgent' or 'act now'" excludes both.
    A negative word (no, not, does not, never, without, avoid) before a quoted
    phrase or a {PLACEHOLDER} makes it ``excludes``; "ends with 'X'" is
    ``ends_with``; "under N characters" allows N - 1.
    """
    criteria = []
    for index, rule in enumerate(acceptance, start=1):
        cid = f"r{index:02d}"
        rubric_kind = None
        lowered = rule.casefold()
        for label in ("semantic", "visual"):
            if lowered.startswith(label + ":"):
                rubric_kind = label
                break
        if rubric_kind:
            fields = {}
            for part in rule.split("|"):
                key, sep, value = part.partition(":")
                if not sep or not value.strip():
                    raise ValueError(
                        f"{rubric_kind} criterion {cid} needs criterion, observe, pass, fail, "
                        "and not-verifiable fields separated by |"
                    )
                key = key.strip().casefold()
                if key in fields:
                    raise ValueError(f"{rubric_kind} criterion {cid} repeats {key}")
                fields[key] = value.strip()
            required = {rubric_kind, "observe", "pass", "fail", "not-verifiable"}
            if set(fields) != required:
                missing = ", ".join(sorted(required - set(fields))) or ""
                extra = ", ".join(sorted(set(fields) - required))
                detail = f"missing {missing}" if missing else f"unknown fields {extra}"
                raise ValueError(f"{rubric_kind} criterion {cid} has {detail}")
            criteria.append({
                "id": cid, "kind": rubric_kind, "description": fields[rubric_kind],
                "observation": fields["observe"], "pass_when": fields["pass"],
                "fail_when": fields["fail"],
                "not_verifiable_when": fields["not-verifiable"],
            })
            continue
        hit = _MAX_CHARS.search(rule)
        if hit:
            limit = int(hit.group(2))
            criteria.append({"id": cid, "kind": "max_chars",
                             "value": limit - 1 if hit.group(1).lower() in _STRICT else limit})
            continue
        hit = _MAX_CHARS_2.search(rule)
        if hit:
            criteria.append({"id": cid, "kind": "max_chars", "value": int(hit.group(1))})
            continue
        phrases = _phrases(rule)
        if phrases:
            for n, (kind, phrase) in enumerate(phrases):
                criteria.append({"id": cid + ("" if n == 0 else chr(ord("a") + n)), "kind": kind, "value": phrase})
        else:
            # A rule no built-in check can compute is judged by a reader. The
            # person writes it as a plain sentence; the method is derived from
            # it, so nothing has to be re-typed. Spelling the method out
            # (`semantic: … | observe: …`) stays available and wins.
            criteria.append(_judged_criterion(cid, rule))
    return criteria


def _judged_criterion(cid: str, rule: str) -> dict:
    """A plain acceptance sentence as a judged criterion with its method named."""
    visual = bool(_RENDER.search(rule))
    return {
        "id": cid, "kind": "visual" if visual else "semantic", "description": rule,
        "observation": ("Look at the rendered screen of this draft and judge the rule as written."
                        if visual else
                        "Read this draft as its recipient and judge the rule as written."),
        "pass_when": f"The draft does what the rule says: {rule}",
        "fail_when": f"The draft does not do what the rule says: {rule}",
        "not_verifiable_when": ("The render is missing or does not show what the rule names."
                                if visual else
                                "The draft does not show enough to judge the rule either way."),
    }
