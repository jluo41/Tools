"""Item addresses (ref/cards.md §2): resolve an address on a page to its item and owner page, and list the cards
whose address no longer resolves (they show as "moved", never vanish).

An address is segments joined by `.`, each `[A-Za-z0-9_-]+`, exact case, never a position or a version. Across pages
the full form is `<page path>:<address>`. Two families resolve on disk here:
  ladder rows   j02, j02.t01, j02.t01.r05   the folder number prefix (j02_*/t01_*/runs/r05_*), never the slug
  Draft ids     C1, C1.P2, C1.P2.s8, s8, B9 the draft Task's current Draft text (an older S8 is the same s8)
Every other address (RQ.H2, term.SNF, fn.make_cohort, decision.x, j01.d03, K01, …) is named by its workbench, which
says whether it exists by passing the addresses it drew (`known`); without that it is left unresolved, never moved.
"""
from __future__ import annotations

import re
from pathlib import Path

from live.item_cards import ADDRESS, cards
from live.sentence_id import sid

LADDER = re.compile(r"^(j\d+)(?:\.(t\d+)(?:\.(r\d+))?)?$")
DRAFT = re.compile(r"^([Ss]\d+[a-z]*|B\d+[a-z]*|C\d+|C\d+\.P\d+|C\d+\.P\d+\.[Ss]\d+[a-z]*)$")


def split(full: str, page: Path, root: Path) -> tuple[Path, str]:
    """`<page path>:<address>` -> (that page, address); a bare address stays on `page`."""
    if ":" in full:
        where, _, address = full.rpartition(":")
        return (Path(root) / where.strip("/")).resolve(), address
    return page, full


def _one(folder: Path, prefix: str) -> Path | None:
    hits = [d for d in folder.glob(prefix + "_*") if d.is_dir()] if folder.is_dir() else []
    return hits[0] if len(hits) == 1 else None


def ladder(page: Path, address: str) -> Path | None:
    """The folder a ladder address names below `page`: j02 -> j02_*/, j02.t01 -> j02_*/t01_*/, j02.t01.r05 ->
    j02_*/t01_*/runs/r05_*/. None when it names nothing (or more than one folder)."""
    m = LADDER.match(address)
    if not m:
        return None
    job = _one(page, m.group(1))
    task = _one(job, m.group(2)) if job and m.group(2) else None
    if m.group(2) and not task:
        return None
    if m.group(3):
        return _one(task / "runs", m.group(3)) if task else None
    return task or job


def _draft_ids(page: Path) -> set:
    """The ids the draft Task's current Draft carries: s and B ids, C<n>, C<n>.P<n>, C<n>.P<n>.s<n>, sentence ids
    lowercase (sid)."""
    try:
        from live.draft_steps_common import read_draft
        text = read_draft(page).get("text", [])
    except Exception:
        return set()
    ids = set()
    for _, body in text:
        for m in re.finditer(r"(?m)^- (B\d+[a-z]*) · ([Ss]\d+[a-z]*) ·", body):
            ids.update(map(sid, m.groups()))
    for m in re.finditer(r"(?m)^\s*(?:#+|-)\s*(C\d+(?:\.P\d+(?:\.[Ss]\d+[a-z]*)?)?)\b",
                         "\n".join(b for _, b in text)):
        ids.add(sid(m.group(1)))
    return ids


def resolve(page: Path, address: str, known: set | None = None) -> dict:
    """{kind, owner, path, exists}: exists is True or False when this page can tell, None when it cannot."""
    if not ADDRESS.match(address or ""):
        return {"kind": "bad", "owner": page, "path": None, "exists": False}
    if LADDER.match(address):
        hit = ladder(page, address)
        return {"kind": "ladder", "owner": page, "path": hit, "exists": hit is not None}
    if known is not None:
        return {"kind": "named", "owner": page, "path": None, "exists": address in known}
    if DRAFT.match(address) and (page / "draft").is_dir():
        ids = _draft_ids(page)
        return {"kind": "draft", "owner": page, "path": None, "exists": (sid(address) in ids) if ids else None}
    return {"kind": "named", "owner": page, "path": None, "exists": None}


def moved(page: Path, known: set | None = None) -> list:
    """The addresses on this page that carry cards but no longer name an item, in address order."""
    return sorted(a for a in cards(page) if resolve(page, a, known)["exists"] is False)
