"""Page Run names (JL 260928): readable words, one grammar.

    run-delivery-webpage · run-delivery-latex · run-delivery-word   fixed, rebuilt in place
    run-<kind>-<MMDD>-<slug>                                         every other run

`kind` is a word: structure · section · paragraph · scratch · revise · auto-write ·
evidence-embed · context · check · citation · value · display. `MMDD` is the day the
run started, from the clock. `slug` is two to four lowercase words: the run's purpose
(`readability-cleanup`), its target (`c1-p2`), or its Evidence Item's slug
(`score-validation`). A name already taken on the Page gets `-2`, `-3`.

A run is one ticket and one result folder with the same name, in a flat `runs/`:
`runs/<name>.md` ↔ `results/<name>/`. The ticket is written when the run opens and
the result folder when it closes; in between only the Page's text changes.

Older names stay readable (`rp-sec-07`, `re-value-07_x`, `rd01_latex`,
`run_delivery_latex`): `kind_of` maps both forms, and `page.py run-names` renames a
Page's runs once.
"""
from __future__ import annotations

import datetime as dt
import re

KINDS = ("structure", "section", "paragraph", "scratch", "revise", "auto-write",
         "evidence-embed", "context", "check", "citation", "value", "display")
LANES = ("webpage", "latex", "word")
# Which Space shows a kind (the Runs panel). Context sits in the Draft Table view (JL 260929).
SPACE = {"structure": "draft", "section": "draft", "paragraph": "draft", "scratch": "draft",
         "revise": "draft", "auto-write": "draft", "evidence-embed": "draft",
         "citation": "evidence", "value": "evidence", "display": "evidence",
         "delivery": "delivery", "check": "delivery", "context": "draft"}
# Old short tokens → the kind word.
OLD_PAGE = {"struct": "structure", "sec": "section", "para": "paragraph", "scratch": "scratch",
            "revise": "revise", "auto": "auto-write", "embed": "evidence-embed",
            "context": "context", "check": "check"}
OLD_EVIDENCE = {"value": "value", "cite": "citation", "display": "display"}
ITEM_KIND = {"VALUE": "value", "CITE": "citation", "DISPLAY": "display", "TABLE": "display"}

_KIND = "|".join(re.escape(k) for k in sorted(KINDS, key=len, reverse=True))
NAME = re.compile(r"^run-(?P<kind>%s)-(?P<mmdd>\d{4})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$" % _KIND)
DELIVERY = re.compile(r"^run-delivery-(?P<lane>%s)$" % "|".join(LANES))
_OLD_PAGE = re.compile(r"^rp-(?P<kind>%s)-\d" % "|".join(OLD_PAGE), re.I)
_OLD_EVIDENCE = re.compile(r"^re-(?P<kind>%s)-\d" % "|".join(OLD_EVIDENCE), re.I)
_OLD_DELIVERY = re.compile(r"^(?:rd\d+_(?!commission|generate|verify|adopt|revise|reject)|run_delivery_)", re.I)
STOPWORDS = {"a", "an", "the", "of", "and", "or", "for", "to", "in", "on", "with", "after",
             "before", "by", "from", "at", "into", "is", "are", "be", "this", "that", "its"}


def is_run_name(run_id: str) -> bool:
    """A name in the new grammar (either form)."""
    return bool(NAME.match(run_id or "") or DELIVERY.match(run_id or ""))


def kind_of(run_id: str) -> str | None:
    """The kind word of a new or old Page Run name, `delivery` for builds, else None."""
    run_id = run_id or ""
    if DELIVERY.match(run_id) or _OLD_DELIVERY.match(run_id):
        return "delivery"
    for pattern, table in ((NAME, None), (_OLD_PAGE, OLD_PAGE), (_OLD_EVIDENCE, OLD_EVIDENCE)):
        found = pattern.match(run_id)
        if found:
            kind = found.group("kind").lower()
            return table[kind] if table else kind
    return None


def space_of_kind(kind: str | None) -> str:
    return SPACE.get(kind or "", "other")


def slugify(text: str, words: int = 4) -> str:
    """`whole-Section readability cleanup after …` → `whole-section-readability-cleanup`."""
    parts = [w for w in re.split(r"[^a-z0-9]+", (text or "").lower()) if w]
    kept = [w for w in parts if w not in STOPWORDS] or parts
    return "-".join(kept[:words])[:48].strip("-")


def target_slug(target: str) -> str:
    """`C1.P2` → `c1-p2`; `P01-P02` → `p01-p02`."""
    return slugify(target, words=6)


def item_slug(item_id: str) -> str:
    """`E11-VALUE-score-validation` → `score-validation`."""
    found = re.match(r"^E\d+-[A-Z]+-(?P<slug>.+)$", item_id or "")
    return slugify(found.group("slug") if found else item_id)


def item_kind(item_id: str) -> str | None:
    found = re.match(r"^E\d+-(?P<type>[A-Z]+)", item_id or "")
    return ITEM_KIND.get(found.group("type")) if found else None


def mmdd(day=None) -> str:
    """The run's day as MMDD; `day` is a date, a datetime, an ISO string, or None (today)."""
    if day is None:
        return dt.date.today().strftime("%m%d")
    if isinstance(day, (dt.date, dt.datetime)):
        return day.strftime("%m%d")
    found = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(day))
    if found:
        return found.group(2) + found.group(3)
    found = re.fullmatch(r"\d{2}(\d{2})(\d{2})", str(day).strip())   # YYMMDD
    return (found.group(1) + found.group(2)) if found else dt.date.today().strftime("%m%d")


def mint(kind: str, slug: str, *, day=None, taken=()) -> str:
    """A new run name; `-2`, `-3` when the Page already has it."""
    if kind == "delivery":
        raise ValueError("a Delivery run has a fixed name: run-delivery-<lane>")
    if kind not in KINDS:
        raise ValueError("unknown run kind %r" % kind)
    slug = slugify(slug, words=4) or "run"
    base = "run-%s-%s-%s" % (kind, mmdd(day), slug)
    taken = set(taken)
    if base not in taken:
        return base
    n = 2
    while "%s-%d" % (base, n) in taken:
        n += 1
    return "%s-%d" % (base, n)


def delivery_name(lane: str) -> str:
    lane = {"web": "webpage"}.get(lane, lane)
    if lane not in LANES:
        raise ValueError("unknown delivery lane %r" % lane)
    return "run-delivery-%s" % lane
