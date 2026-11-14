"""4 · Display of the draft Task: the display units under display/, the Tables and Figures the text calls, their
cards and the step's view (_display_step); draft_step_evidence.py re-exports them."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live.frame import _rel, esc
from live.draft_steps_assets import CARDS_CSS, CARDS_JS, EV_CSS
from live.draft_steps_common import (
    _code, FLAT, _fold, INK, _kv, _not_yet, _prompt_box, _step_box, _word)


# ── 4 · Display ───────────────────────────────────────────────────────────────────────────────────
# A display (a figure or a table) is one unit, display/Display<n>-<slug>/ (haipipe-display), built on evidence cards and
# accepted by a person; it has its own step after 3 · Evidence (JL 261020: "If we have the display, hwo do we make it?
# will it be the DISPLAY X? Or we want to have a new display view after the 3 - Evidence? ... Please do it"; b34 s41
# Open 1). DISPLAY <n> is the unit's own number, as CITE <n> and VALUE <n> are the cards'.
DISPLAY_INK = "#e8590c"
CALLS = re.compile(r"\b(?:e?(?:Table|Figure)\s+\d+[A-Za-z]?|Overview Figure)\b", re.I)   # a venue's own case: Lancet writes "table 1" (JL 261031)
REFS = re.compile(r"\\(?:ref|cref|Cref|autoref)\{([^}]+)\}")


def _field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^\s*{name}\s*:\s*(.+?)\s*$", text)
    return m.group(1).strip() if m else ""


def _units(folder: Path) -> list:
    """The Task's display units by number: display/Display<n>-<slug>/ (their one home, b34 s41 Ⓐ), and a unit that is
    still only in a display Run's newest pass (runs/run-display-*/passes/<pass>/payload/), where display/ has none of
    that name. What its README says: claim, kind, the name the text calls it by (`shown as:`, else the Table or Figure
    its Placement names), its \\label, built_on, accepted, status."""
    found = {}
    for p in sorted((folder / "runs").glob("run-display-*/passes/*/payload/Display*")) + sorted((folder / "display").glob("Display*")):
        if p.is_dir():
            found[p.name] = p                       # the newest pass, then display/, wins
    out = []
    for name, p in found.items():
        m = re.match(r"Display(\d+)-(.+)$", name)
        if not m:
            continue
        readme = p / "README.md"
        text = readme.read_text(encoding="utf-8", errors="replace") if readme.is_file() else ""
        tex = (p / "float.tex").read_text(encoding="utf-8", errors="replace") if (p / "float.tex").is_file() else ""
        place = re.search(r"(?ms)^##\s*Placement\s*\n(.*?)(?=^## |\Z)", text)
        head = re.search(r"(?m)^# (.+)$", text)
        # the name the text calls it by: `shown as:`, else a Table or Figure in its `label:`, its heading or its Placement
        hit = next((h for h in (CALLS.search(x) for x in (_field(text, "label"), head.group(1) if head else "",
                                                           place.group(1) if place else "")) if h), None)
        shown = _field(text, "shown as") or (hit.group(0) if hit else "")
        status = re.search(r"(?ms)^##\s*Status\s*\n+\s*(\S.*?)\s*$", text)
        pic = next((x for x in (p / "preview.png", p / "assets" / "figure.png", p / "assets" / "figure.svg") if x.is_file()), None)
        out.append({"n": int(m.group(1)), "slug": m.group(2), "dir": p, "readme": readme if readme.is_file() else None,
                    "claim": _field(text, "claim"), "shown": shown, "labels": set(re.findall(r"\\label\{([^}]+)\}", text + tex)),
                    "kind": _field(text, "kind") or ("table" if (p / "assets" / "table-body.tex").is_file() else "figure" if pic else ""),
                    "built_on": _field(text, "built_on"), "accepted": _field(text, "accepted"),
                    "layout": _field(text, "layout"), "made_by": _field(text, "made by"),
                    "status": (status.group(1) if status else _field(text, "status")).split(" (")[0], "pic": pic,
                    "pdf": p / "preview.pdf" if (p / "preview.pdf").is_file() else None,
                    "built": bool(pic or (p / "preview.pdf").is_file() or any((p / "assets").glob("*")))})
    return sorted(out, key=lambda u: u["n"])


def _calls(d: dict | None) -> dict:
    """What the text calls a display by, and its sentences in order: {"Table 1": ["S1", "S5"]}; a \\ref{label} too."""
    out = {}
    for _, body in (d or {}).get("text", []):
        for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", body):
            for name in [n[0].upper() + n[1:] if n[:1] in "tfo" else n for n in CALLS.findall(m.group(2))] + REFS.findall(m.group(2)):
                out.setdefault(name, []).append(m.group(1)) if m.group(1) not in out.get(name, []) else None
    return out


def _displays(folder: Path, d: dict | None) -> list:
    """Each display of the Section: every unit with the sentences that call it (by its `shown as` name or its \\label),
    then every name the text calls that no unit answers, not made yet."""
    from live.draft_step_evidence import _s_key  # lazy: draft_step_evidence imports this module
    calls, out, used = _calls(d), [], set()
    for u in _units(folder):
        names = [n for n in calls if (u["shown"] and n.lower() == u["shown"].lower()) or n in u["labels"]]
        used.update(names)
        words = u["slug"].replace("-", " ")
        out.append({**u, "label": f"DISPLAY {u['n']}", "names": names, "made": True,
                    "title": f"{u['shown']} · {words}" if u["shown"] else words,
                    "calls": sorted({s for n in names for s in calls[n]}, key=_s_key),
                    "ok": bool(u["accepted"]) and not u["accepted"].startswith("⬜")})
    # a label another Section of the same version owns (the Results text calls an eTable of the Supplement): shown from
    # that Section's unit, not as "no unit" (JL 261023: the box said "tab:e-models · no unit in display/ yet")
    others = [(t, u) for t in sorted(folder.parent.glob("t*")) if t.is_dir() and t != folder for u in _units(t)]
    for name, ss in calls.items():
        if name in used:
            continue
        hit = next(((t, u) for t, u in others if name in u["labels"] or (u["shown"] and name.lower() == u["shown"].lower())), None)
        if hit:
            t, u = hit
            out.append({**u, "label": f"{u['shown'] or 'DISPLAY'} · {t.name}", "names": [name], "made": True,
                        "title": u["shown"] or u["slug"].replace("-", " "), "calls": ss, "ok": bool(u["accepted"]) and not u["accepted"].startswith("⬜")})
        else:
            out.append({"label": name, "names": [name], "made": False, "title": name, "calls": ss, "ok": False})
    return out


def _display_card(x: dict, root: Path, big: bool = False) -> str:
    """One display: its DISPLAY number in orange, what the text calls it, accepted or not; its picture; its claim.
    Opened on its own (`big`), the picture at full width and the README's fields: built on, the sentences, the files."""
    chip = ('<span class="st st-ok">✓ accepted</span>' if x["ok"] else
            '<span class="st st-warn">✍ to accept</span>' if x.get("built") else
            '<span class=st>⬜ planned, not built</span>' if x["made"] else '<span class=st>⬜ not made yet</span>')
    head = (f'<b style="color:{DISPLAY_INK}">{esc(x["label"])}</b> · {esc(x["title"])} {chip}' if x["made"] else
            f'<b style="color:{DISPLAY_INK}">{esc(x["title"])}</b> {chip}')
    pic = ""
    if x.get("pic"):
        u = "/" + quote(_rel(x["pic"], root))
        pic = (f'<a href="{esc(u)}" target=_blank><img src="{esc(u)}" alt="{esc(x["title"])}" style="display:block;'
               f'max-width:100%;max-height:{"none" if big else "260px"};margin:8px 0 4px;border:1px solid var(--line)"></a>')
    elif x.get("pdf"):
        pic = f'<p style="margin:6px 0">{_code(x["pdf"], root)}</p>'
    body = head + pic + (f'<p class=mut style="margin:4px 0">{esc(x["claim"])}</p>' if x.get("claim") else "")
    if big:
        rows = [("Called by", esc(", ".join(x["calls"])) or '<span class=mut>no sentence yet</span>')]
        if x["made"]:
            rows += [("Kind", esc(x["kind"]) or "—"), ("Layout", esc(x["layout"]) or "—"),
                     ("Built on", esc(x["built_on"]) or '<span class=mut>not named yet</span>'), ("Made by", esc(x["made_by"]) or "—"),
                     ("Status", esc(x["status"]) or "—"), ("Accepted", esc(x["accepted"]) or '<span class=mut>not yet: only you write it</span>'),
                     ("Unit", _code(x["readme"], root) if x["readme"] else f'<code>{esc(_rel(x["dir"], root))}/</code>')]
        body += _kv(rows)
    return f'<div class="rv-card ev-card" data-s="{esc(x["calls"][0] if x["calls"] else "")}">{body}</div>'


def _display_step(f: dict, folder: Path, root: Path, st: str) -> tuple:
    from live.draft_step_evidence import _text_rows  # lazy: draft_step_evidence imports this module
    d, xs = f["draft"], f["displays"]
    made = [x for x in xs if x["made"]]
    names = [x["names"][0] if x["names"] else x["label"] for x in xs]
    rows = [("Calls", esc(" · ".join(f"{x['title'] if not x['made'] else x['label']} ({', '.join(x['calls']) or 'no sentence'})"
                                     for x in xs)) or '<span class=mut>the text calls no Table or Figure yet</span>'),
            ("Units", esc(f"{len(made)} made: {sum(x['built'] for x in made)} built, {sum(x['ok'] for x in made)} accepted")
             if made else '<span class=mut>none yet in display/</span>'),
            ("Built on", _code(f["ev"]["path"], root) if f["ev"]["path"] else '<span class=mut>no evidence/cards.yaml yet</span>'),
            ("Accept", "only you write <code>accepted:</code> in a unit's README")]
    prompt = (f"/haipipe-display {f['t']}: for each display {f['section']} calls ({', '.join(names) or 'none yet'}), make or "
              "update its unit in display/Display<n>-<slug>/ (README: claim, kind, shown as, built_on its evidence cards; "
              "recipe, intake, assets, preview), its numbers read from the Runs its cards name; then check the numbers "
              "against the cards, and stop for my accept.")
    op = _step_box("🖼 Stage 4 · Display", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "display"))
    if not xs:
        return op, _not_yet("No display yet: the text calls no Table or Figure, and display/ is empty."), ()
    result = ""
    if d and d["text"]:
        marks = {n: (DISPLAY_INK if x["made"] else INK["need"], [x["label"]] if x["made"] else ["not made"])
                 for x in xs for n in x["names"]}
        right = {}
        for x in xs:
            right[x["calls"][0] if x["calls"] else ""] = right.get(x["calls"][0] if x["calls"] else "", "") + _display_card(x, root)
        body = (f'<p class=space-reads>{_code(d["file"], root)}</p>'
                + _text_rows(d, marks, right, "Displays no sentence calls", xs, root))
        result = EV_CSS + CARDS_CSS + _fold(f"🖼 The text and its displays · {d['version']}", body, open_=True) + CARDS_JS
    # each display on its own, folded, its picture at full width
    for x in xs:
        result += (f'<details class="topic work-task"><summary><span class=related-head><b style="color:{DISPLAY_INK}">'
                   f'{esc(x["label"] if x["made"] else x["title"])}</b>' + (f' · {esc(x["title"])}' if x["made"] else
                                                                            "" if FLAT.get() else " · not made yet")
                   + f'</span>{_word(("accepted" if x["ok"] else "made") if x["made"] else "not made yet")}</summary><div class=work-body>' + _display_card(x, root, big=True) + '</div></details>')
    return op, result, ()
