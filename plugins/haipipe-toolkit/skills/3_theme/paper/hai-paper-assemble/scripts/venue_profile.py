"""One reader for venues/: a series folder's rules, then one journal's few changes on top (JL 261123).

    venue_profile = <series>                             venues/<series>/profile.toml
    venue_profile = <series>/<journal>                   venues/<series>/profile.toml, then its
                                                          [journals.<journal>] table

A table key ([latex]) merges key by key, so a journal or a paper that sets one LaTeX key keeps the others.
build_delivery.py and latex_room_to_docx.py both read venues through `load`; neither names a venue.
"""
from __future__ import annotations

import tomllib
from pathlib import Path

VENUES = Path(__file__).resolve().parents[1] / "venues"


def merge(base: dict, top: dict) -> dict:
    out = dict(base)
    for key, value in top.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = {**out[key], **value}
        else:
            out[key] = value
    return out


def split(name: str) -> tuple[str, str]:
    series, _, journal = str(name or "").strip().lower().partition("/")
    return series, journal


def path(name: str) -> Path | None:
    series, _ = split(name)
    return VENUES / series / "profile.toml" if series else None


def load(name: str, paper: dict | None = None) -> dict:
    """The series rules, the journal's table over them, then the paper's own [profile] over both."""
    series, journal = split(name)
    prof: dict = {}
    if series:
        file = VENUES / series / "profile.toml"
        if not file.exists():
            raise FileNotFoundError(f"Venue profile not found: {file}")
        prof = tomllib.loads(file.read_text(encoding="utf-8"))
        journals = prof.pop("journals", {}) or {}
        if journal:
            if journal not in journals:
                raise KeyError(f"{file}: no [journals.{journal}] (has: {', '.join(sorted(journals)) or 'none'})")
            prof = merge(prof, journals[journal])
    return merge(prof, paper or {})
