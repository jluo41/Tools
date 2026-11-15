"""A Question Book's parts on the shared work page: its questions (by release, newest, by level), each version,
the proposals and the segments."""

from __future__ import annotations

import re
from pathlib import Path

from live import insight_views as V
from live.frame import esc, pop
from live.ui_parts import _kv
from live.insight_view_parts import _pill, _side_tabs
from live.insight_prototype_facts import (
    ORDER, LEVEL, CSS, _proto, _computes, _scripts, q_state, q_word, _ready, r_word, _label, _proposals,
    _p_word, _focus, KIND_WORD)
from live.insight_prototype_status import _open_btn, _release_waits


# ── the parts ───────────────────────────────────────────────────────────────────────────────────────────────────
def _q_row(q: dict, root: Path, with_change: bool = False) -> str:
    """One question in words: its id and short question, its state; its ask; its script and its question file."""
    short = str(q.get("question") or q.get("name") or q["id"]).strip()
    ask = str(q.get("ask") or "").strip()
    links = [V._open(s, root, s.name) for s in _scripts(q)]
    links.append(pop(_focus(Path(q["task"]), root), q["id"], "its page ↗") if q.get("task") else "")
    change = str(q.get("change") or "")
    return (f'<li><div class=h><b>{esc(q["id"])}</b><span>{esc(short[:1].upper() + short[1:])}</span>{_pill(q_word(q))}</div>'
            + (f'<p class=ask>{esc(ask)}</p>' if ask and not ask.startswith("<") else "")
            + f'<p class=by>{"".join(x for x in links if x)}'
            + (f'<span>{esc(change)}</span>' if with_change and change else "") + '</p></li>')


def _by_level(qs: list, root: Path, with_change: bool = False) -> str:
    out = []
    for lv in ORDER:
        mine = [q for q in qs if q["id"][:1] == lv]
        if mine:
            out.append(f'<p class=pb-lv><b>{esc(LEVEL[lv])}</b></p><ul class=pq>'
                       + "".join(_q_row(q, root, with_change) for q in mine) + '</ul>')
    return "".join(out)


def _level_word(qs: list) -> str:
    ready = sum(_ready(q) for q in qs)
    if ready == len(qs):
        return "agreed · scripted" if any(_computes(q) for q in qs) else "agreed"
    return V.far(sum(q_state(q)[0] == 'agreed' for q in qs), len(qs), "agreed")


def _questions_by_release(proto: dict, root: Path) -> tuple:
    rs = list(reversed(proto["releases"]))                  # the newest release first, open
    if not rs:
        return None
    items = [(_label(r), r_word(r)) for r in rs]
    panels = [_by_level(list(r["questions"].values()), root, True) or "<p>This release asks no question yet.</p>" for r in rs]
    signed = sum(r_word(r).startswith("closed") for r in rs)
    word = "✅" if rs and signed == len(rs) else "🏃" if signed else "⬜"
    return ("❓ Questions", word, CSS + _side_tabs("prq", items, panels), "")


def _questions_newest(proto: dict, root: Path) -> tuple | None:
    """The Question Book's questions as they stand: the newest version's, by DIKW level, each marked new or kept (JL
    261109, review: the list once, the newest first; an older version's own list is on its page)."""
    if not proto["releases"]:
        return None
    r = proto["releases"][-1]
    body = _by_level(list(r["questions"].values()), root, True) or "<p>This version asks no question yet.</p>"
    return ("❓ Questions", f"{_label(r)} · {r_word(r)}", CSS + body, "")


def _version_part(proto: dict, r: dict, root: Path) -> tuple:
    """One question version on the Versions view: its sign, what it added (never the whole list again), its segments,
    and the way into it."""
    qs = list(r["questions"].values())
    new = [q for q in qs if str(q.get("change") or "") == "new"]
    first = proto["releases"] and r is proto["releases"][0]
    if first or len(new) == len(qs):
        added = '<p>Its questions are all new.</p>' if qs else "<p>It asks no question yet.</p>"
    elif new:
        added = '<p class=pb-lv><b>New in this version</b></p><ul class=pq>' + "".join(_q_row(q, root) for q in new) + '</ul>'
    else:
        added = "<p>It keeps every question of the version before.</p>"
    cuts = _cuts_part(r, qs, root, "prc-" + r["name"])
    segs = ('<p class=pb-lv><b>Segments</b></p>' + cuts[2]) if cuts else ""
    go = (f'<div class=find-verbs>{_open_btn(_focus(r["job"], root), _label(r), "Open " + _label(r))}</div>'
          if r.get("job") else "")
    return (f"📜 {_label(r)}", r_word(r), CSS + added + segs + go, _release_waits(r, proto))


def _questions_by_level(r: dict, root: Path) -> tuple | None:
    qs = list(r["questions"].values())
    lvs = [lv for lv in ORDER if any(q["id"][:1] == lv for q in qs)]
    if not lvs:
        return None
    items = [(LEVEL[lv], _level_word([q for q in qs if q["id"][:1] == lv])) for lv in lvs]
    panels = [_by_level([q for q in qs if q["id"][:1] == lv], root, True) for lv in lvs]
    return ("❓ Questions", _level_word(qs), CSS + _side_tabs("prl", items, panels), "")


def _proposals_part(ps: list, root: Path) -> tuple | None:
    if not ps:
        return None
    items, panels = [], []
    for p in ps:
        body = Path(p["file"]).read_text(encoding="utf-8", errors="ignore") if Path(p["file"]).is_file() else ""
        text = re.sub(r"(?s)^---\n.*?\n---\n", "", body).strip()
        why = " ".join(ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#"))
        items.append((str(p.get("title") or "").replace("-", " ").capitalize(), _p_word(p)))
        panels.append(_kv([("kind", esc(KIND_WORD.get(str(p.get("kind") or ""), str(p.get("kind") or "—")))), ("level", esc(str(p.get("level") or "—"))),
                           ("from", esc(str(p.get("from") or "—")))])
                      + (f'<p>{esc(why)}</p>' if why else "") + f'<p class=by>{V._open(p["file"], root, p["file"].name)}</p>')
    open_ = [p for p in ps if str(p.get("state") or "open").lower() in ("open", "proposed", "")]
    waits = (f'🙋 {str(open_[0].get("title") or "").replace("-", " ")}: a proposed {KIND_WORD.get(str(open_[0].get("kind")), open_[0].get("kind") or "change")} '
             'waits for your yes or no') if open_ else ""
    word = f"{len(open_)} wait for you" if len(open_) > 1 else "1 waits for you" if open_ else "all triaged"
    return ("📮 Ideas", word, _side_tabs("prp", items, panels), waits)


def _cuts_part(r: dict, qs: list, root: Path, eid: str = "prc") -> tuple | None:
    parts = r.get("partitions") or []
    if not parts:
        return None
    power = (r.get("thresholds") or {}).get("power") or {}
    floor = power.get("smallest_effect_pp")
    items, panels = [], []
    for p in parts:
        name = str(p.get("name") or "")
        asks = [q["id"] for q in qs if q.get("asked") == "all" or name in (q.get("asked") or [])
                or (name == "cross" and any(n.get("cut") == "cross" for n in (q.get("needs") or {}).values() if isinstance(n, dict)))]
        items.append((name, V._where(p)))
        panels.append(_kv([("where", f'<code>{esc(V._where(p))}</code>'), ("why", esc(str(p.get("why") or "—"))),
                           ("asked by", esc(", ".join(asks) or "—"))]))
    head = (f'<p>Set in {esc(_label(r))}, before any result is seen'    # its files are 📦 Delivery's (round 2: shown once)
            + (f'; a segment too small to show a {esc(floor)}-point gap is not answered' if floor else "") + '.</p>')
    return ("✂️ Segments", f"smallest gap to detect: {floor} points" if floor else _label(r), head + _side_tabs(eid, items, panels), "")


def parts(folder: Path, root: Path, level: str) -> list:
    """A Question Book's Findings parts: [(title, word, html, waits)]."""
    folder, root = Path(folder), Path(root).resolve()
    proto = _proto(folder, level)
    out = []
    if level == "Block":
        out += [_questions_by_release(proto, root), _proposals_part(_proposals(proto), root)]
        if proto["releases"]:
            r = proto["releases"][-1]
            out.append(_cuts_part(r, list(r["questions"].values()), root))
    elif level == "Job":
        r = next((x for x in proto["releases"] if x.get("job") == folder or Path(x.get("job") or "").name == folder.name), None)
        if r:
            out += [_questions_by_level(r, root), _proposals_part(_proposals(proto, r), root),
                    _cuts_part(r, list(r["questions"].values()), root)]
    return [x for x in out if x]
