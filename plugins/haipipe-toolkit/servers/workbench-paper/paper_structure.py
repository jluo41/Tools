"""A paper version's Structure view (JL 261111: "it should be a view for the job workbench UI"). Read-only, nothing
copied: one section, "1 · 🗺️ Structure", open by default, as left tabs and right content:

- 🧭 The story: the Board Story's § 8 as its parts (title, the story in one line, the rest smaller); when the Story has
  no § 8, the version face's own ## Narrative. The version's sign beside it (`narrative-approved:`; stale when § 8
  changed since, compared with `<version>/records/narrative-sign.md`).
- Claims: one tab per claim C<n>, with the Sections that carry it and the displays that show it.
- Sections, grouped by the face's compile-order block: Main, Appendix, then Not printed (closed). Each panel: the
  reader's question, the moves, the claims and figures it carries, entry, must refuse and exit (the face's per-Section
  table), the Section's Plan mind map read-only, and the venue's example papers drawn live.
"""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc
from live.ui_parts import _section, _plain
from live.board_read import _num
from live.paper_reading import _tables      # one Markdown table reader for the paper views
from live.address_links import href as _href

STRUCTURE_CSS = """<style>
.st-sign{flex:0 1 260px;font-size:13px;line-height:1.45;padding:10px 12px;border:1px solid var(--line);border-radius:8px}
.st-sign b{display:block;font-size:14px;margin:0 0 2px}.st-ok b{color:var(--ok,#2b8a3e)}.st-no b{color:var(--warn,#c2410c)}
.st-title{font-size:22px;font-weight:700;line-height:1.3;margin:0 0 6px}.st-story{font-size:16px;margin:0 0 8px;line-height:1.45}
.st-more{font-size:13px;color:var(--muted);margin:0 0 3px;line-height:1.45}.st-more b{color:inherit;font-weight:600;margin-right:4px}
.st-links{font-size:12.5px;margin:8px 0 0}.st-links a{margin-right:14px}
.st-state{font-size:12.5px;white-space:nowrap}
.st-moves{font-size:13px;color:var(--muted);margin:5px 0 0;line-height:1.5}
.st-tags{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:7px 0 0;font-size:12px}
.st-chip{border:1px solid var(--line);border-radius:10px;padding:1px 8px;white-space:nowrap}.st-fig{background:var(--soft,rgba(0,0,0,.04))}
.st-kv{margin:8px 0}.st-kv div{margin:0 0 3px}.st-kv b{display:inline-block;min-width:10ch;color:var(--muted);font-weight:600}
.st-tabs h5{margin:12px 0 4px;font-size:13px}.st-paras{margin:0;padding-left:20px}.st-paras li{margin:0 0 2px}
.st-c{color:var(--muted);font-size:12px;margin:6px 0 2px;font-weight:600}
.st-fold>summary.pb-lgroup{cursor:pointer;list-style:none}.st-fold>summary::-webkit-details-marker{display:none}
.st-fold>summary.pb-lgroup::before{content:"▸ "}.st-fold[open]>summary.pb-lgroup::before{content:"▾ "}
.st-tabs .pb-side{grid-template-columns:230px minmax(0,1fr)}
.st-tabs .pb-item b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}.st-tabs .pb-item span:empty{display:none}
.st-tabs .st-sign{margin:12px 0 0;max-width:420px}.st-tabs p.st-state{margin:0 0 8px;color:var(--muted)}.st-cid{color:var(--muted);margin-right:8px}
.st-num{font-size:14px;margin:0 0 10px}
.st-tabs .pb-read{max-height:none;overflow:visible}
@media(max-width:700px){.st-tabs .pb-side{grid-template-columns:minmax(0,1fr)}.st-tabs .pb-list{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:6px;padding-bottom:4px}
.st-tabs .pb-item{flex:0 0 auto;max-width:220px}.st-tabs .pb-lgroup{flex:0 0 auto;white-space:nowrap;align-self:center;margin:0 2px}}
</style>"""

PARA_HEAD = re.compile(r"(?m)^###\s+(C\d+\.P\d+)\s*·\s*(.+?)\s*$")
CLAIM = re.compile(r"\bC\d+\b")
FIG = re.compile(r"(Extended Data (?:Figure|Fig\.?|Table)s?|Figure|Fig\.?|Table)\s+(\d+(?:\s*(?:to|-|–)\s*\d+)?)", re.I)


def _sections(version: Path) -> list:
    """The version's Sections in reading order: t00-t29 (the letters t3N and the check t99 are not the paper)."""
    return [t for t in sorted(version.glob("t[0-9]*_*"), key=_num) if t.is_dir() and _num(t) < 30]


def _plan(task: Path):
    from src.outline_version import latest_outline, plan_dir
    return latest_outline(plan_dir(task), task.name)


def _paragraphs(task: Path) -> list:
    """[(C1.P1, name)] from the Section's current Draft Markdown, its `## 1 · Structure` part."""
    plan = _plan(task)
    if plan is None:
        return []
    text = plan.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"(?ms)^## 1 · Structure\b(.*?)(?=^## \d+ · |\Z)", text)
    return [(a, re.sub(r"\s*·\s*[Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?\s*$", "", b)) for a, b in PARA_HEAD.findall(m.group(1) if m else text)
            if not a.endswith(".P0")]                       # P0 is the title, not a paragraph


def _plan_sign(task: Path) -> tuple:
    """(signed, its words) from the current Draft's `approved:` line."""
    plan = _plan(task)
    head = plan.read_text(encoding="utf-8", errors="ignore")[:1500] if plan is not None else ""
    m = re.search(r"(?m)^approved:\s*(.+)$", head)
    return (bool(m and m.group(1).startswith("✅")), m.group(1).strip() if m else "")


def _narrative_block(text: str) -> str:
    m = re.search(r"(?ms)^## Narrative[^\n]*\n(.*?)(?=^## |\Z)", text)
    return m.group(1).strip() if m else ""


def _story_parts(story: str) -> dict:
    """{TITLE: …, STORY (C): …} from the § 8 ```text block (a capitalised key, two spaces, its value; an indented
    line carries on the one above)."""
    m = re.search(r"(?s)```(?:text)?\n(.*?)```", story or "")
    out, key = {}, None
    for line in (m.group(1).splitlines() if m else []):
        k = (re.match(r"([A-Z][A-Z0-9 ()/&-]+?)\s{2,}(\S.*)$", line)
             or re.match(r"([^\w\s]+\s+(?:[A-Z]{2,}\b\s?)+?)\s+(\S.*)$", line))   # "🎯 IDENTITY  one study", a version's
        if k:
            key = k.group(1).strip()
            out[key] = k.group(2).strip()
        elif key and line.startswith(" ") and line.strip():
            out[key] += " " + line.strip()
    return out


def _claims(story: str) -> list:
    """[(C1, claim, number)] from the § 8 table whose first two headers are an id and `claim`."""
    for t in _tables(story or ""):
        if t and "claim" in t[0]:
            first = next(iter(t[0]))
            num = next((k for k in t[0] if k.startswith("number")), "")
            return [(_plain(r.get(first, "")), _plain(r.get("claim", "")), _plain(r.get(num, "")) if num else "") for r in t
                    if CLAIM.fullmatch(_plain(r.get(first, "")))]
    return []


def _rows(mine: str, story: str) -> dict:
    """{t01_introduction: row} from the per-Section table (`section` + `reader question`): the version face's, else an
    older Story's § 8."""
    for body in (mine, story):
        for t in _tables(body or ""):
            if t and "section" in t[0] and any("question" in k for k in t[0]):
                return {_plain(r["section"]).strip("`"): r for r in t if _plain(r.get("section", ""))}
    return {}


def _order(version: Path, text: str) -> list:
    """[(group, Section)] in compile order: Main, then Appendix (the face's compile-order block, `main:` and
    `appendix:`), then every other Section folder as Not printed (JL 261113, via the AgreeableRx version session)."""
    m = re.search(r"(?s)haipipe:compile-order:start -->(.*?)<!--", text)
    secs, out, group = {t.name: t for t in _sections(version)}, [], "Main"
    for line in (m.group(1).splitlines() if m else []):
        if re.match(r"\s*appendix\s*:", line, re.I):
            group = "Appendix"
        n = re.match(r"\s*-\s*(t\d+_\S+)", line)
        if n and n.group(1) in secs and all(t.name != n.group(1) for _, t in out):
            out.append((group, secs[n.group(1)]))
    if not out:                                   # no compile order: every Section is the paper, in folder order
        return [("Sections", t) for t in secs.values()]
    return out + [("Not printed", t) for t in secs.values() if all(t is not x for _, x in out)]


def _tabs(eid: str, items: list, folded=("Not printed",)) -> str:
    """Side tabs in groups, as board_displays._grouped_tabs, with a group in `folded` closed under its name."""
    from live.board_displays import DISPLAY_CSS
    rows, panels, k = "", "", 0
    for group in dict.fromkeys(g for g, _, _ in items):
        cards = ""
        for g, (h, w), body in items:
            if g != group:
                continue
            cards += (f'<button type=button class="pb-item{" on" if k == 0 else ""}" data-pbtab="{eid}{k}"><b>{esc(h)}</b>'
                      + (f'<span title="{esc(w)}">{esc(w)}</span>' if w else "") + '</button>')
            panels += f'<div class=pb-panel data-pbpanel="{eid}{k}"{"" if k == 0 else " hidden"}>{body}</div>'
            k += 1
        rows += (f'<details class=st-fold><summary class=pb-lgroup>{esc(group)}</summary>{cards}</details>' if group in folded
                 else f'<div class=pb-lgroup>{esc(group)}</div>{cards}')
    return (DISPLAY_CSS + f'<div class="pb-tabset pb-side pb-thin"><div class=pb-list>{rows}</div>'
            f'<div class=pb-read>{panels}</div></div>')


def _examples_topic(task: Path) -> Path | None:
    """The Section examples topic the Task face names in `examples:` (a Board topic beside the version Job)."""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    m = re.search(r"(?m)^examples:\s*(\S+)", text)
    d = task.parent.parent / m.group(1).strip("`") if m else None
    return d if d is not None and d.is_dir() else None


def _nice(t: Path) -> str:
    return re.sub(r"^t\d+_", "", t.name).replace("-", " ").replace("_", " ").capitalize()


def _claim(c: str) -> str:
    """A claim as the reader says it (JL 261111: "what does the C mean here?"): C3 is Claim 3; the files keep C<n>."""
    return re.sub(r"^C(\d+)$", r"Claim \1", c)


def _chips(carried: list, figs: list) -> str:
    return ("".join(f'<span class=st-chip>{esc(_claim(c))}</span>' for c in carried)
            + "".join(f'<span class="st-chip st-fig">{esc(f)}</span>' for f in figs))


def _read_only(html: str) -> str:
    """A map shown to read: nothing typed in place, no drag, no ＋ buttons."""
    html = re.sub(r"\s(?:contenteditable=plaintext-only|draggable=true)", "", html)
    html = re.sub(r"<div class=pm-addp>.*?</div>", "", html, flags=re.S)
    html = re.sub(r"<button type=button class=pm-plus[^>]*>.*?</button>", "", html, flags=re.S)
    # a hand-on question slot with nothing in it is only room for typing one (JL 261111: "why we have this issue?")
    return re.sub(r"<div class=pm-q><span[^>]*></span></div>", "", html)



def _plan_mind_map(task: Path, name: str) -> str:
    """The Section's Plan mind map, drawn by the draft Task's own code (JL 261111: "the same mindmap from the plan view
    of the draft task"; draft_steps._plan_map over hai-mindmap's mapview), read-only here: nothing typed in place."""
    try:
        from live import draft_steps as dst
        d = dst.read_draft(task)
        if not d or not d.get("structure"):
            return ""
        html = dst._plan_map(d, dst._evidence(task), name, "", dst._kind_of(task))
    except Exception:
        return ""
    return _read_only(html)


def structure_view(version: Path, root: Path, md) -> str:
    """The Structure view's html: the story band, then a row per Section."""
    from live.frame import _file_url
    from src.folder_health import _header, story_narrative, NARRATIVE_SIGN, signed_against, _norm
    face = version / f"{version.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    story, sface = story_narrative(version / "_")
    mine = _narrative_block(text)
    sign = re.search(r"(?m)^narrative-approved:\s*(.+)$", _header(text))
    signed = bool(sign and sign.group(1).startswith("✅"))
    kept = signed_against(version / NARRATIVE_SIGN)
    stale = signed and kept is not None and story is not None and _norm(story) != kept

    # left tabs, right content (JL 261111: "please just do the left tab and right content"): the story, each claim,
    # then each Section; one panel shows at a time, the story first
    told = story or mine                         # no § 8 in the Story: the version's own ## Narrative (JL 261113)
    parts, claims = _story_parts(told), _claims(told)
    title = parts.pop("TITLE", "")
    tale = next((parts.pop(k) for k in list(parts) if k.startswith("STORY")), "")
    from src.folder_health import version_drafting
    if stale and version_drafting(version):
        # while Sections draft, their plans are the truth: one quiet note, no ❗, no re-sign (must-check M-D09, M-D19)
        state, cls = "✅", "st-ok"
        note = (esc(sign.group(1).lstrip("✅ ").strip())
                + "; rebuilt from the Section plans by page.py sync-narrative when the Sections are good")
    elif stale:
        state, cls = "❗", "st-no"           # the mark carries the state; the note says what to do (AGENTS § Page words)
        note = esc(sign.group(1)) + "; the Story's § 8 changed since: review and sign again"
    elif signed:
        state, cls = "✅", "st-ok"
        note = esc(sign.group(1).lstrip("✅ ").strip())
    else:
        state, cls = "⬜", "st-no"
        note = "Your word in chat signs this version's Narrative, before any Section's plan."
    links = []
    if sface is not None:
        links.append(f'<a href="{esc(_file_url(sface, root))}" data-pop="{esc(sface.parent.name)}">Story § 8 as written</a>')
    if mine:
        links.append(f'<a href="{esc(_file_url(face, root))}" data-pop="{esc(face.name)}">This version\'s Narrative as written</a>')
    def label(k):                                # "🎯 IDENTITY" reads "🎯 Identity"; "STORY (C)" reads "Story (C)"
        e, w = re.match(r"([^\w\s]*\s*)(.*)", k).groups()
        return e + re.sub(r"\((\w)\)", lambda m: f"({m.group(1).upper()})", w[:1] + w[1:].lower())
    more = "".join(f'<p class=st-more><b>{esc(label(k))}</b>{esc(v)}</p>' for k, v in parts.items())
    lead = ((f'<p class=st-title>{esc(title)}</p>' if title else "") + (f'<p class=st-story>{esc(tale)}</p>' if tale else "") + more)
    if not lead and told:                        # a § 8 with no text block still shows, in its own words
        lead = md(told, sface.parent if story else version)
    story_panel = ((lead or "<p class=mut>No story yet.</p>")
                   + (f'<div class="st-sign {cls}"><b>{state}</b>{note}</div>' if mine else "")
                   + (f'<p class=st-links>{"".join(links)}</p>' if links else ""))

    rows = _rows(mine, story)
    # which claims each display carries, from the face's "Claims to displays: C1 and C2 Figure 2 · C3 Figure 3" line
    by_fig: dict = {}
    m = re.search(r"Claims to displays:\s*(.+)", mine or "")
    for part in (re.split(r"\s*·\s*", m.group(1)) if m else []):
        cs, f = CLAIM.findall(part), FIG.search(part)
        if cs and f:
            by_fig.setdefault(f"{'Table' if 'table' in f.group(1).lower() else 'Fig'} {f.group(2)}", []).extend(cs)
    placed = _order(version, text)
    secs = [t for _, t in placed]
    paras = {t.name: _paragraphs(t) for t in secs}
    sec_tabs, sec_panels, carried_by = [], [], {}
    for t in secs:
        r = rows.get(t.name, {})
        q = _plain(r.get("reader question", ""))
        moves = _plain(r.get("ordered moves", "") or r.get("moves", ""))
        carried = list(dict.fromkeys(CLAIM.findall(" ".join(_plain(v) for v in r.values()))))
        figs = list(dict.fromkeys(f"{'ED ' if a.lower().startswith('extended') else ''}{'Table' if 'table' in a.lower() else 'Fig'} {b}"
                                  for a, b in FIG.findall(_plain(r.get("displays", "")) + " " + moves)))
        carried = list(dict.fromkeys(carried + [c for f in figs for c in by_fig.get(f, [])]))
        for c in carried:
            carried_by.setdefault(c, []).append(_nice(t))
        ok, _ = _plan_sign(t)
        ps = paras[t.name]
        kv = "".join(f'<div><b>{esc(n)}</b>{esc(_plain(r[k]))}</div>'
                     for k, n in (("entry", "Comes in"), ("must refuse", "Must refuse"), ("exit", "Leaves with"),
                                  ("displays", "Displays")) if _plain(r.get(k, "")))
        groups: dict = {}
        for a, b in ps:
            groups.setdefault(a.split(".")[0], []).append(b)
        plist = "".join(f'<p class=st-c>{esc(c)}</p><ol class=st-paras>' + "".join(f'<li>{esc(b)}</li>' for b in g) + '</ol>'
                        for c, g in groups.items())
        # each paper row opens that paper's own section picture (JL 261111: "how could I see the examples?")
        topic = _examples_topic(t)
        from live.board_canvas import live_canvas      # the topic's drawing live: pan, zoom, fit (JL 261111)
        drawing = live_canvas(topic / f"{topic.name}.excalidraw", root, topic.name) if topic is not None else ""
        sec_panels.append(                       # the tab's ✅ / ⬜ carries the plan's state; no state words here
            f'<p class=st-title>{esc(q or _nice(t))}</p>' + (f'<p class=st-state>{esc(_nice(t))}</p>' if q else "")
            + (f'<p class=st-moves>{esc(moves)}</p>' if moves else "")
            + (f'<div class=st-tags>{_chips(carried, figs)}</div>' if carried or figs else "")
            + (f'<div class=st-kv>{kv}</div>' if kv else "")
            + ((lambda mm: f'<h5>Its plan</h5>{mm}' if mm else (f'<h5>Its paragraphs</h5>{plist}' if plist else ""))(_plan_mind_map(t, _nice(t))))
            # one drawing holds each paper's area: its screenshot and its logic (JL 261111: "one draw should be okay")
            + (f'<h5>The venue\'s papers</h5>{drawing}' if drawing else "")
            + f'<p class=st-links><a href="{esc(_href(t, root, "&section=report"))}">Open {esc(t.name)}</a></p>')
        sec_tabs.append((f'{"✅" if ok else "⬜"} {_nice(t)}', ""))   # the mark is the state; no paragraph tally

    shows = {}
    for f, cs in by_fig.items():
        for c in cs:
            shows.setdefault(c, []).append(f.replace("Fig ", "Figure "))
    claim_tabs, claim_panels = [], []
    for c, w, n in claims:
        claim_tabs.append((f"{_claim(c)} · {w}", ""))
        claim_panels.append(f'<p class=st-title><span class=st-cid>{esc(_claim(c))}</span>{esc(w)}</p>'
                            + (f'<p class=st-num>{esc(n)}</p>' if n else "")
                            + '<div class=st-kv>'
                            + f'<div><b>Carried by</b>{esc(", ".join(carried_by.get(c, [])) or "no Section names it yet")}</div>'
                            + (f'<div><b>Shown in</b>{esc(", ".join(shows[c]))}</div>' if c in shows else "")
                            + '</div>')
    items = ([("Story", ("🧭 The story", ""), story_panel)]
             + [("Claims", t, b) for t, b in zip(claim_tabs, claim_panels)]
             + [(g, t, b) for (g, _), t, b in zip(placed, sec_tabs, sec_panels)])   # Main, Appendix, Not printed (closed)
    body = f'<div class=st-tabs>{_tabs("st", items)}</div>'
    html = _section("1 · 🗺️ Structure", STRUCTURE_CSS + body)
    return html.replace("<section class=fd-sec>", "<section class=fd-sec data-open>", 1)   # the page's main view starts open (JL 261113)
