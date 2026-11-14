"""3 · Evidence and 4 · Display of the draft Task (draft_steps.py): evidence rows, the sentence board's slots, the open
points, the display units, and both steps' views; draft_steps re-exports them all."""
from __future__ import annotations

import re
from html import unescape
from pathlib import Path
from urllib.parse import quote

from live.frame import _rel, esc
from live.draft_steps_assets import CARDS_CSS, CARDS_JS, EV_CSS
from live.draft_steps_common import (
    _code, FLAT, _fold, INK, _inline, _kv, _marks, _md, _not_yet, _parts, _poss, _prompt_box, _step_box, _word)
# 4 · Display moved out (600-line rule); every name stays importable here
from live.draft_step_evidence_display import (  # noqa: F401
    _calls, CALLS, _display_card, DISPLAY_INK, _display_step, _displays, _field, REFS, _units)


EV_STATE = {"have": '<span title="have">✅</span>', "need": '<span title="asked">❓</span>',
            "missing": '<span title="not found">❗</span>'}


def _s_ids(it: dict) -> list:
    """An item's sentences, `for: [2, 4]` (or "2a"), as the text's ids: S2, S4."""
    return ["S" + str(n).lstrip("S") for n in it.get("for") or []]


def _s_key(s: str) -> tuple:
    m = re.match(r"S?(\d+)([a-z]?)$", str(s))
    return (int(m.group(1)), m.group(2)) if m else (10 ** 6, "")


def _num(v) -> str:
    """A value read from a Run as a reader writes it: 73931, 0.7169, 19."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else f"{x:.4g}"


def _evidence_row(c: dict, it: dict, n: int, sentences: bool = False, brief: bool = False) -> str:
    """One item as a row: its id, the card's label and its place in the card (CITE 1.4), in the card's ink and as the
    text's mark names it (JL 261020: "should the evidence item have some index as well?"; the card's title on hover);
    have or asked; the words it backs with the value read, and under them what backs them (the paper, the Run and its
    key, or what is still asked). Hovering a row lights its sentences. In a card's own list (`sentences`), the sentences
    it backs follow its id. Beside the text (`brief`) the row is one line and what backs it shows on hover, so the cards
    keep closer to their sentences; the card's own fold shows it all."""
    ink = INK.get(c["kind"], INK["value"])
    value = it.get("value")
    words = " · ".join(f"“{esc(a)}”" for a in it.get("anchor") or []) or esc(it.get("cite") or "")
    if c["kind"] != "cite" and it["state"] == "have" and value not in ("", None):
        words += f" <b>= {esc(_num(value))}</b>"
    fact = it.get("fact")
    fact = ", ".join(map(str, fact)) if isinstance(fact, list) else str(fact or "")
    if it["state"] == "missing":
        detail = esc(str(value))
    elif c["kind"] == "cite" and it["state"] == "have":
        detail = esc(" · ".join(x for x in (str(value or it.get("cite") or ""), fact) if x))
    else:
        where = ((f'<code>{esc(c["source"])}.{esc(it["run"])}</code>' + (f' · {esc(it["file"])}' if it.get("file") else "")
                  + (f' <code>{esc(it["key"])}</code>' if it.get("key") else "")) if it.get("run") else "")
        detail = " · ".join(x for x in (esc(it.get("what") or it.get("need") or fact), where) if x)
    title = c["title"] + (f" · {c['source']}" if c["source"] else "")
    hover = f' title="{esc(re.sub("<[^>]+>", "", detail))}"' if brief and detail else ""
    return (f'<tr data-s="{esc(" ".join(_s_ids(it)))}"{hover}>'
            f'<td style="white-space:nowrap;width:1%;padding:5px 8px 5px 0"><b style="color:{ink};font-size:12.5px" '
            f'title="{esc(title)}">{esc(c["label"])}.{n}</b></td>'
            + (f'<td class=mut style="white-space:nowrap;width:1%;padding:5px 8px 5px 0;font-size:12.5px">'
               f'{esc(" · ".join(_s_ids(it)) or "—")}</td>' if sentences else "")
            + f'<td style="width:1%;padding:5px 8px 5px 0">{EV_STATE[it["state"]]}</td>'
            f'<td style="padding:5px 0;line-height:1.5">{words}'
            + (f'<br><span class=mut style="font-size:12.5px">{detail}</span>' if detail and not brief else "") + '</td></tr>')


def _card_folds(ev: dict) -> str:
    """Each Evidence card on its own, folded under the text (JL 261020: "To show each evidenence card seperately?"): its
    label in its ink, its title and where it comes from; opened, a row per item, CITE 1.4 and the sentences it backs."""
    out = []
    for c in ev["cards"]:
        ink = INK.get(c["kind"], INK["value"])
        rows = "".join(_evidence_row(c, it, n, sentences=True) for n, it in enumerate(c["items"], 1))
        word = ""                                # each item row shows its own ✅ / ❓; no "N of M found" (AGENTS § Page words)
        out.append(f'<details class="topic work-task"><summary><span class=related-head><b style="color:{ink}">'
                   f'{esc(c["label"])}</b> · {esc(c["title"])}'
                   + (f' <span class=mut>· {esc(c["source"])}</span>' if c["source"] else "") + f'</span>{_word(word)}</summary>'
                   f'<div class=work-body><table class="rv-rows ev-list" style="border-collapse:collapse;width:100%">'
                   f'{rows}</table></div></details>')
    return "".join(out)


def _ev_card(s: str, rows: list) -> str:
    return (f'<div class="rv-card ev-card" data-s="{esc(s)}"><table class=rv-rows style="border-collapse:collapse;'
            f'width:100%">{"".join(rows)}</table></div>')


def _embed_displays(html: str, d: dict, xs, root: Path) -> str:
    """Each Table or Figure the text calls, shown under the first sentence that calls it, as it will stand in the paper
    (JL 261021: "如果我们有图片或者表格的话 ... PNG TO EMBED UNDER THAT SENTENCE"): its rendered preview.png, which
    opens full size; a unit with only preview.pdf links it; one not built yet says so. The unit stays the source (its
    README, recipe and the Run that made the asset); the page only shows its picture."""
    order = [m for _, b in (d or {}).get("text", []) for m in re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", b)]
    for x in xs or ():
        if x.get("owner"):  # another Section's display shows only where the paper prints it (JL 261114: "only need to show in first place ... should be in the results")
            continue
        first = next((sid for sid in order if sid in x.get("calls", [])), "")
        m = first and re.search(r'<li data-s="' + re.escape(first) + r'"[^>]*>.*?</li>', html, re.S)
        if not m:
            continue
        # the name a reader knows (Table 2), never the LaTeX label (JL 261023: the box said "tab:online-ratings")
        name = x.get("shown") or (x["names"][0] if x.get("names") else x["title"])
        if x.get("pic"):
            u = "/" + quote(_rel(x["pic"], root))
            fig = (f'<a href="{esc(u)}" target=_blank><img src="{esc(u)}" alt="{esc(name)}"></a>'
                   f'<figcaption><b>{esc(name)}</b> · {esc(x.get("claim") or x.get("slug", "").replace("-", " ") or x["title"])}</figcaption>')
        elif x.get("pdf"):
            fig = f'<figcaption><b>{esc(name)}</b> · {_code(x["pdf"], root)}</figcaption>'
        else:
            fig = (f'<figcaption><b>{esc(name)}</b> · ' + ("not built yet" if x.get("made") else "no unit in display/ yet")
                   + (f' · {esc(x["claim"])}' if x.get("claim") else "") + '</figcaption>')
        html = html[:m.end()] + f'<li class="disp-embed{" disp-none" if not x.get("pic") else ""}"><figure>{fig}</figure></li>' + html[m.end():]
    return html


CITE_SPAN = re.compile(r'<span class=cite>\[([^\]<]*)\]</span>')


def _bib_names(d: dict) -> dict:
    """{key: "Barnett et al. 2017"} from the Page's own Bib files (draft/evidence/bibex/*.bib), as the compiled paper
    prints an author-year citation."""
    task = Path(d.get("file") or ".").parent.parent
    out = {}
    for bib in sorted((task / "draft" / "evidence" / "bibex").glob("*.bib")) if (task / "draft").is_dir() else []:
        text = bib.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", text, re.S):
            body = m.group(2)
            get = lambda k: ((x := re.search(r"\b" + k + r"\s*=\s*[{\"]((?:[^{}]|\{[^{}]*\})*)[}\"]", body, re.I))
                             and re.sub(r"[{}]", "", x.group(1)).strip()) or ""
            raw = re.search(r"\bauthor\s*=\s*\{\s*\{([^{}]+)\}\s*\}", body, re.I)
            names = [raw.group(1).strip()] if raw else [a.strip() for a in re.split(r"\s+and\s+", get("author")) if a.strip()]
            last = lambda a: a.split(",")[0].strip() if "," in a else a.split()[-1]
            who = ((names[0] if raw else last(names[0])) + (" et al." if len(names) > 2 else f" and {last(names[1])}"
                   if len(names) == 2 else "")) if names else ""
            year = (re.search(r"\d{4}", get("year")) or [None])[0] if get("year") else ""
            if who:
                out.setdefault(m.group(1), f"{who} {year}".strip())
    return out


def _cite_names(html: str, d: dict) -> str:
    """Each citation as the compiled paper prints it, "(Barnett et al. 2017; Hoppe et al. 2017)", its keys on hover; the
    source keeps \\citep{...} (JL 261113, after trying the raw LaTeX: "how about we just make the citations to be the
    readable one?"). A key with no Bib entry stays a key."""
    names = _bib_names(d)
    def one(m):
        keys = [k.strip() for k in m.group(1).split(";") if k.strip()]
        shown = "; ".join(esc(names.get(k, k)) for k in keys)
        return f'<span class="cite cite-ay" title="{esc(", ".join(keys))}">({shown})</span>'
    html = CITE_SPAN.sub(one, html)
    # \\citet is the narrative form, as natbib prints it: "Barnett et al. (2017)", so the two never look alike (JL 261113:
    # "if we have this issue, maybe using the \\cite should be better")
    def narr(m):
        keys = [k.strip() for k in m.group(1).split(",") if k.strip()]
        parts = []
        for k in keys:
            who, _, year = names.get(k, k).rpartition(" ")
            parts.append(f"{who} ({year})" if who and year.isdigit() else names.get(k, k))
        return f'<span class="cite cite-ay cite-t" title="{esc(", ".join(keys))}">{esc("; ".join(parts))}</span>'
    return re.sub(r"\\citet\{([^}]*)\}", narr, html)


def _text_rows(d: dict, marks: dict, right: dict, rest_head: str, xs=(), root: Path | None = None) -> str:
    """The text as one column, read on with no gap between sentences, and beside it the cards, `right[S]` at sentence
    S's line (CARDS_JS `align`): each pushed down only to clear the card above it, so the text never moves for a card;
    the column stays beside the cards and scrolls itself to the sentence a card lights, as 5 · Revise's (JL 261020:
    "我不想让句子跟句子之间有这么大的空格 ... 在 revise、evidence、display 这里都保持一样的风格"). Used by 3 · Evidence and
    4 · Display; a card for a sentence the text no longer has, or for none, ends the column."""
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "")
                   + _md(b, marks, _parts(d), rows=True) for t, b in d["text"])
    text = _embed_displays(text, d, xs, root) if xs else text
    text = _cite_names(text, d)
    seq = [m for _, b in d["text"] for m in re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", b)]
    at = {sid: i for i, sid in enumerate(seq)}
    # in the order the text reads, which an S number need not follow once a sentence has moved
    order = sorted(right, key=lambda s: (0, at[s], "") if s in at else (1,) + _s_key(s) if s else (2, 10 ** 7, ""))
    return _sx_board(_sx_fill(text, [right[s] for s in order], _sx_paras(d), rest_head), "ev-split")


# ── the sentence board ────────────────────────────────────────────────────────────────────────────
# The sentence is the unit (JL 261113: "the sentences will be the basic unit. We can be sentence comments to be
# left-right, and it can also be up-down"): each sentence is one row, and every card on it, Revise, Logic, Evidence,
# Display or a comment, sits in that row, beside the sentence or under it. A card finds its row by the sentence it
# names: a full address (C1.P2.S2), a bare one (S2, the first paragraph that has it), or a Bullet in its head
# (`Edit · C1.P1.B2 · …`, the sentence §3 gives that Bullet: `- B2 · S2 · …`), which before 261113 placed it at the
# paragraph's top beside no sentence. A card on a paragraph sits in the paragraph heading's row; one on no sentence
# the text has ends the board.

SX_SLOT = re.compile(r'<div class=rv-right data-slot="([^"]*)"></div>')


def _sx_paras(d: dict) -> list:
    """[(paragraph id, [(Bullet, sentence)])] of the draft's §3 text, in reading order."""
    out = []
    for _, b in (d or {}).get("text", []):
        for line in b.splitlines():
            h = re.match(r"^#{1,6}\s*(C\d+\.P\d+)\b", line)
            if h:
                out.append((h.group(1), []))
                continue
            m = re.match(r"^- (B\d+[a-z]*) · (S\d+[a-z]*) · ", line)
            if m:
                if not out:
                    out.append(("", []))
                out[-1][1].append((m.group(1), m.group(2)))
    return out


def _sx_attr(html: str, name: str) -> str:
    m = re.search(r'\s' + name + r'="([^"]*)"', html)
    return unescape(m.group(1)) if m else ""


def _sx_key(card: str, paras: list) -> str:
    """The row a card belongs to: a sentence's full address (C1.P2.S2), a paragraph id (C1.P2), or "" for none."""
    first, pids = {}, {pid for pid, _ in paras if pid}
    for pid, bs in paras:
        for _, sid in bs:
            first.setdefault(sid, f"{pid}.{sid}" if pid else sid)
    full = set(first.values()) | {f"{pid}.{sid}" for pid, bs in paras for _, sid in bs if pid}
    cls, s, p, head = _sx_attr(card, "class"), _sx_attr(card, "data-s"), _sx_attr(card, "data-p"), _sx_attr(card, "data-card")
    part = re.match(r"[^·]+·\s*(C\d+)\s*·", head)          # `Section question · C1 · …`: the Section's own row
    if part:
        return part.group(1)
    if re.fullmatch(r"C\d+", s.strip()):                    # a comment on the whole Section
        return s.strip()
    if "rv-flow" in cls.split() and p in pids:          # a paragraph's flow card names all its sentences
        return p
    b = re.search(r"\b(C\d+\.P\d+)\.(B\d+[a-z]*)\b", head)
    if b and not re.match(r"[^·]+·\s*S\d", head):
        hit = next((f"{pid}.{sid}" if pid else sid for pid, bs in paras if pid == b.group(1) for bb, sid in bs
                    if bb == b.group(2)), "")
        if hit:
            return hit
    for tok in s.split():
        if tok in full:
            return tok
        if tok in first:
            return first[tok]
        if tok in pids:
            return tok
    return p if p in pids else ""


def _sx_fill(html: str, cards: list, paras: list, rest_head: str) -> str:
    """Each card into its row's slot, in the order given; a card on a sentence with no `data-s` (a Bullet card) gets the
    sentence's address, so it lights its sentence; cards on no sentence the text has end the board in one row."""
    slots, groups, rest = set(SX_SLOT.findall(html)), {}, []
    for c in cards:
        k = _sx_key(c, paras)
        if k and k in slots:
            if not re.fullmatch(r"C\d+\.P\d+", k):
                c = c.replace(' data-s=""', f' data-s="{esc(k)}"', 1)
            groups.setdefault(k, []).append(c)
        else:
            rest.append(c)
    html = SX_SLOT.sub(lambda m: f'<div class=rv-right data-slot="{m.group(1)}">{_sx_bar(groups.get(unescape(m.group(1)), []))}</div>', html)
    if rest:
        html += (f'<div class="rv-split sx-row sx-rest"><div class=rv-left><h4 class=mut style="margin:0">{esc(rest_head)}'
                 f'</h4></div><div class=rv-right>{"".join(rest)}</div></div>')
    return html


SX_OLD = ("written", "applied", "rejected", "superseded", "done", "history")


def _sx_bar(cards: list) -> str:
    """A sentence's cards, folded under one button that says where they stand (JL 261113: "by default hidden, click it
    to show its status, and after click it, we can click a new button to show its faded history"): open shows the
    cards still current; History adds the decided ones, faded."""
    if not cards:
        return ""
    old = [c for c in cards if _sx_attr(c, "data-state") in SX_OLD]
    now = len(cards) - len(old)
    wait = sum(_sx_attr(c, "data-state") in ("proposed", "open") for c in cards)
    said = f'{now} card{"s" * (now != 1)}' + (f" · {wait} wait for you" if wait else "")
    return ('<div class=sx-bar>' + (f'<button type=button class="sx-sum{" wait" if wait else ""}">{said}</button>' if now else "")
            + (f'<button type=button class=sx-hb>History {sum(int(_sx_attr(c, "data-n") or 1) for c in old)}</button>'
               if old else "") + '</div>'
            + "".join(c.replace('class="rv-card', 'class="rv-card sx-old', 1) if c in old else c for c in cards))


def _sx_board(rows: str, cls: str = "") -> str:
    """The rows, with the switch between cards beside each sentence and cards under it (CARDS_JS keeps the choice),
    and the switch that folds every sentence to one line or opens them all (SX_ROWS)."""
    from live.draft_autofold import AUTOFOLD_JS; from live.draft_math import MATH_JS   # folds; math typeset (KaTeX)
    return SX_ROWS + AUTOFOLD_JS + MATH_JS + f'<div class="sx-board sx-ud sx-fixed{(" " + cls) if cls else ""}">' + rows + '</div>'


# Each sentence folds its cards away and keeps its whole text (JL 261113: "why we don't have things like > to click and we can save more spaces"; "I want them to show the whole sentence"):
# ▸ opens it with its cards, ▾ folds it; a folded line ends in its marks, 📎 evidence, 🕘 earlier wordings and decided
# cards, 🙋 cards that wait for you, and a sentence with a waiting card starts open. ▸ on a paragraph heading folds the
# paragraph's rows. The text reads in Source Serif 4, a journal-like serif (Literata before it, JL 261113: "please update
# it again"), on a pale paper tone, with the
# cards white on it (JL 261113: "make the font ... more classic and easier to read"; "could we give some background
# light color to the main text"); without the web font it falls back to the system's Charter or Georgia.
SX_ROWS = """<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
.sx-board .rv-left li[data-s],.sx-board .rv-left h4,.sx-board h3.rv-part{font-family:"Source Serif 4",Charter,"Bitstream Charter",
 "Sitka Text","Iowan Old Style",Cambria,Georgia,serif}
.sx-board .rv-left{font-size:19.5px;line-height:1.7}   /* larger text (JL 261113: "how could you make the font size larger?") */
.sx-board{font-size:19.5px;line-height:1.7;background:color-mix(in srgb,#efe6d4 30%,var(--card,#fff));
 padding:10px 16px 14px;border-radius:8px;border:1px solid color-mix(in srgb,#e6dcc8 55%,var(--line,#ddd))}
.sx-board .rv-left li[data-s]{color:color-mix(in srgb,var(--ink,#222) 92%,#5a4a2a)}
.sx-board .rv-right .rv-card{background:var(--card,#fff)}
.sx-board .rv-left .s-no{font-family:system-ui,-apple-system,sans-serif}
/* the numbers start on one line, S1 under S3b (JL 261113: "why the index here are not aligned?") */
.sx-board .rv-left li[data-s] .s-no{flex:0 0 38px;text-align:left;padding-right:4px;font-size:11px;color:#b5b3ab}
/* two numbers (JL 261113: "the sentence fix index, and the index that shown in the order"): the reading position,
   1, 2, 3 in each part as the text reads now, then the sentence's fixed id (S3b), small, which cards and comments use */
.sx-board .rv-left li[data-s]>.s-ord{flex:0 0 24px;box-sizing:border-box;text-align:right;padding-right:7px;
 font:600 13px/1.9 system-ui,-apple-system,sans-serif;color:var(--ink,#333);font-variant-numeric:tabular-nums}
.sx-board .rv-left li[data-s]>.sx-tog{display:none}   /* no arrow: the marks after the sentence open its cards (JL 261113) */
/* the text set full width, flush on both edges, as a printed paper is (JL 261113: "fully aligned") */
/* left-aligned: a long \\citep{...} would stretch a justified line into gaps (JL 261113 screenshot of S3) */
.sx-board .rv-left li[data-s] .s-tx{text-align:left;hyphens:auto;-webkit-hyphens:auto}
/* the cards read at the page's own size, not the text's 18px (JL 261113: "the edit card here is too large") */
.sx-row>.rv-right{font-size:13.5px;line-height:1.45}
.sx-row>.rv-right .rv-card{padding:6px 10px;margin-bottom:6px}
.sx-row>.rv-right .rv-handle,.sx-row>.rv-right .rv-card b{font-size:13.5px}
.sx-tog,.sx-ptog{border:0;background:none;cursor:pointer;color:var(--ink,#333);font-size:15px;width:20px;padding:0;margin:0 2px 0 0;
 font-family:system-ui,sans-serif;vertical-align:baseline}
.sx-tog:hover,.sx-ptog:hover{color:var(--acc)}
.sx-tog::before,.sx-ptog::before{content:'▾'}
.sx-row.sx-fold .sx-tog::before,.sx-row.sx-pfold .sx-ptog::before{content:'▸'}
.sx-marks{font:12px/1 system-ui,-apple-system,sans-serif;color:var(--mut);white-space:nowrap;margin-left:6px}
.s-tx>.sx-marks{display:inline;vertical-align:1px}   /* right after the sentence's last word, as a footnote mark */
.sx-marks span{margin-left:8px}.sx-marks .w{color:#b35c00;font-weight:600}
.sx-row:not(.sx-fold) .sx-marks>span:not(.sx-clk){display:none}
/* the clock is the History switch (JL 261113: "when I click the clock, could I hide the History button"): one control */
.rv-board .sx-hb,.rv-board .sx-sum{display:none!important}
/* the cards are the pen after the clock (JL 261113: "like it should be things like the pen?"); orange while one waits */
.sx-pen{cursor:pointer;border-radius:8px;padding:0 3px}.sx-pen:hover{color:var(--acc)}
.sx-row.sx-open .sx-pen{color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,transparent);font-weight:600}
.sx-row:not(.sx-fold) .sx-marks>span.sx-pen,.sx-row:not(.sx-fold) .sx-marks>span.sx-evm{display:inline}
.sx-evm{cursor:pointer;border-radius:8px;padding:0 3px}.sx-evm:hover{color:var(--acc)}
.sx-board .sx-row.sx-evon>.rv-right>.rv-ev{display:block!important}.sx-row.sx-evon .sx-evm{color:var(--acc)}
/* a card under its sentence starts where the sentence's text starts (position 24 + id 38) */
.sx-board.sx-ud .sx-row>.rv-right{padding-left:62px}
/* a card's text runs exactly as wide as the sentence's (JL 261113: "make the card width the same to the sentences"):
   the box steps out by its own border and padding, and earlier wordings use the sentence's own face and size */
.sx-board.sx-ud .sx-row>.rv-right>.rv-card{margin-left:-11px;margin-right:3px}   /* text edges = the sentence's */
.sx-board .sx-histcard .sx-h{font-size:18px;line-height:1.7;text-align:justify;hyphens:auto;-webkit-hyphens:auto}
@media(max-width:1000px){.sx-board .sx-row>.rv-right{padding-left:62px}.sx-board .sx-row>.rv-right>.rv-card{margin-left:-11px;margin-right:3px}}
.sx-clk{cursor:pointer;border-radius:8px;padding:0 3px}
/* 🕘 shows only the earlier versions; the edits stay under 📝 */
.rv-board .sx-row:not(.sx-ver)>.rv-right>.sx-histcard{display:none!important}
.rv-board .sx-row.sx-ver>.rv-right>.rv-card.sx-histcard{display:block}
.sx-pen.faint{opacity:.55}.sx-clk:hover{color:var(--acc)}
.sx-row.sx-ver .sx-clk{color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,transparent);font-weight:600}
.sx-row.sx-fold{padding:1px 0;grid-template-columns:minmax(0,1fr)}
.sx-row.sx-fold>.rv-right{display:none}
/* a folded sentence keeps its whole text (JL 261113: "I want them to show the whole sentence"); only its cards fold */
.sx-row.sx-fold .rv-left li[data-s]{cursor:pointer}
.sx-row.sx-hide{display:none}
.sx-row.sx-p .sx-marks,.sx-row.sx-c .sx-marks{display:inline}
.sx-row.sx-c{padding-top:22px;margin-top:10px;border-top:1px solid var(--line)}
.sx-row.sx-c h3.rv-part{font-size:19px;margin:0;display:flex;align-items:center;gap:6px}
.sx-row.sx-c:has(>.rv-right:empty){grid-template-columns:minmax(0,1fr)}
.sx-row.sx-p:has(>.rv-right:empty){grid-template-columns:minmax(0,1fr)}
.sx-histcard .sx-h{padding:6px 0;border-top:1px solid var(--line);font-family:Charter,"Iowan Old Style",Georgia,serif;
 font-size:15px;line-height:1.55}
.sx-histcard .sx-h:first-of-type{border-top:0}
.sx-histcard .sx-hw{display:block;font:12px/1.4 system-ui,sans-serif;color:var(--mut);margin-bottom:2px}
.sx-histcard .sx-h.now .sx-hw{color:var(--acc);font-weight:600}
/* an edit is a card with a coloured edge; evidence is a quiet line under it; scores read by colour */
.sx-row>.rv-right .rv-ev{border:0!important;background:transparent!important;padding:1px 2px!important;margin:0 0 2px!important;
 color:var(--mut);box-shadow:none}
/* no coloured edge on a card, and a decided edit shows its change, not its A/B choices (JL 261113: "I don't want this") */
.sx-row>.rv-right .rv-card.sx-old .rv-choices,.sx-row>.rv-right .rv-card.sx-old .rv-acts{display:none}
/* quiet marks, so the eye stays on the sentence (JL 261113: "I don't want this to be too colorful") */
.sx-ai{font-weight:400;color:var(--mut)}.sx-ai.old{opacity:.55}.sx-ai.low{color:color-mix(in srgb,var(--mut) 70%,#8a3b2b)}
.sx-ok{cursor:pointer;color:color-mix(in srgb,var(--mut) 55%,transparent);font-weight:600;padding:0 2px}
.sx-ok:hover{color:var(--ink,#333)}.sx-ok.on{color:var(--ink,#333)}
.sx-board .sx-ok.stale{color:#b06d1a;background:color-mix(in srgb,#e8a33d 16%,transparent);border-radius:9px;padding:0 6px}
.sx-row:not(.sx-fold) .sx-marks>.sx-ok{display:inline!important}
.sx-board .rv-left li[data-checked="1"] .sx-ai{display:none!important}
.sx-cmt{cursor:pointer;opacity:.75}.sx-cmt:hover{opacity:1}
.nt-co .nt-av{background:color-mix(in srgb,#b8894a 18%,transparent);color:#7a5a2e}   /* a co-author's comment: their initials */
.sx-board .rv-left h4[data-p] .p-ord{font:600 13px/1 system-ui,-apple-system,sans-serif;color:var(--ink,#333);min-width:16px;text-align:right;margin-right:6px}
.sx-board .rv-left h4[data-p] .p-no{font:400 10.5px/1 system-ui,-apple-system,sans-serif;color:#b5b3ab;margin-left:6px}
/* comments open: the row shows its comments, the other cards stay folded */
.sx-row.sx-cm-on>.rv-right>.rv-card:not(.rv-note){display:none!important}
.sx-row.sx-cm-on>.rv-right>.rv-note.nt-new{display:none!important}
.sx-row.sx-add-on>.rv-right>.rv-card:not(.nt-new){display:none!important}
.sx-row.sx-cm-on>.rv-right>.rv-note{display:block!important}
.sx-row.sx-cm-on .sx-cmt{opacity:1;color:var(--ink,#333)}
.sx-wc{color:var(--mut);font-size:11.5px}
.sx-evm{font-family:"Source Serif 4",Georgia,serif}   /* the ❝ citation mark in one colour (JL 261113) */
.sx-row:not(.sx-fold) .sx-marks>.sx-wc{display:inline!important}
/* one card look beside the sentences (JL 261113: "the card style here is not fit well"): a thin grey line, white, the
   page's sans at one size; hover darkens the line, never orange; an edit keeps a muted left edge */
.sx-board .sx-row>.rv-right .rv-card:not(.rv-ev){border:1px solid color-mix(in srgb,var(--line,#ddd) 85%,transparent);
 border-radius:6px;background:var(--card,#fff);box-shadow:none;padding:8px 12px;font:13.5px/1.5 system-ui,-apple-system,sans-serif}
.sx-board .sx-row:hover>.rv-right>.rv-card:not(.rv-ev),.sx-board .sx-row>.rv-right>.rv-card.open:not(.rv-ev){
 border-color:color-mix(in srgb,var(--ink,#333) 28%,transparent)}
.sx-board .sx-row>.rv-right .rv-card.has-choice{border-left:3px solid color-mix(in srgb,#b8894a 70%,transparent)}
.sx-board .sx-row>.rv-right .rv-card.has-choice[data-state=written]{border-left-color:color-mix(in srgb,#5f9e72 70%,transparent)}
.sx-board .sx-row>.rv-right .rv-note .nt-box{font:14px/1.5 system-ui,-apple-system,sans-serif;border-radius:6px}
/* the history reads like the text: the sentence in the text's serif, its date and source small above it */
.sx-board .sx-histcard .sx-h{font-family:"Source Serif 4",Charter,"Iowan Old Style",Georgia,serif;font-size:16px;line-height:1.6;text-align:left}
.sx-board .sx-histcard .sx-hw{font:11.5px/1.4 system-ui,-apple-system,sans-serif;color:var(--mut)}
.sx-board .sx-histcard .sx-h.now .sx-hw{color:var(--ink,#333);font-weight:600}
/* evidence opened: a reference list, no lone icon line above it */
.sx-board .sx-row>.rv-right .rv-ev.open>.lg-head{display:none}
.sx-board .sx-row>.rv-right .rv-ev .ev-ref{font:14px/1.5 system-ui,-apple-system,sans-serif;color:var(--ink,#333);margin:2px 0}
.sx-board .sx-row>.rv-right .rv-ev .ev-ref a{color:inherit;text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--mut) 50%,transparent)}
.sx-board .sx-row>.rv-right .rv-ev .ev-run{font-size:11.5px;color:var(--mut);white-space:nowrap;margin-left:4px}
.sx-board .sx-row>.rv-right .rv-ev .ev-quote{font-size:13px;color:var(--mut);margin:0 0 4px 22px}
/* the review card in plain words: verdict, problem, suggestion */
/* a sentence that reads well needs no card until its ★ is clicked */
.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="8"],.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="9"],
.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="10"]{display:none}
.sx-ai{cursor:pointer}
.sx-row>.rv-right .rv-rev .lg-head{display:flex;align-items:baseline;gap:10px}
.sx-row>.rv-right .rv-rev .lg-q{font-size:13.5px}
.sx-row>.rv-right .rv-rev .lg-sc{margin-left:auto;font-size:11.5px;color:var(--mut);white-space:nowrap}
.sx-row>.rv-right .rv-rev .lg-prob{margin:3px 0 0}
.sx-row>.rv-right .rv-rev .lg-sugg{margin:3px 0 0;color:var(--ink,#333)}
.sx-row>.rv-right .rv-rev .lg-lab{font-size:11.5px;font-weight:600;color:var(--mut);margin-right:4px}
/* the cards start where the sentence text starts (JL 261113: "why cards and sentences are not fully aligned") */
.sx-board.sx-ud .sx-row>.rv-right{padding-left:62px!important}
.sx-board.sx-ud .sx-row.sx-p>.rv-right,.sx-board.sx-ud .sx-row.sx-c>.rv-right{padding-left:22px!important}
.sx-row:not(.sx-fold) .sx-marks>.sx-cmt,.sx-row:not(.sx-fold) .sx-marks>.sx-ai{display:inline!important}
.sx-board .cite{white-space:normal}.sx-board .cite-ay{font-size:.9em;color:color-mix(in srgb,var(--ink,#333) 70%,transparent)}
.sx-board .cite-tex{font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);overflow-wrap:anywhere}
/* a checked ✓ is a soft grey-green chip; the sentence itself keeps its look (JL 261113: "the grey green I mean for
   this icon only, not the whole sentence element") */
.sx-board .sx-ok.on{color:#3f7a52;background:color-mix(in srgb,#5f9e72 18%,transparent);border-radius:9px;padding:0 6px;
 box-shadow:0 0 0 1px color-mix(in srgb,#5f9e72 35%,transparent)}
/* a narrow gutter (JL 261113: "the left right take a large space"): ▸, then the reading number with the fixed id
   small under it, in one 46px column; the + and 💬 float in the margin instead of holding a column on the right */
/* the number sits at the left edge, the text where it was (JL 261113: "the index can be a bit to the left") */
.sx-board .rv-left li[data-s]{display:grid!important;grid-template-columns:0 28px minmax(0,1fr) auto;column-gap:0;
 position:relative;align-items:baseline}
.sx-board .rv-left li[data-s]>.sx-tog{grid-column:1;grid-row:1;width:0;overflow:visible;flex:none}
.sx-board .rv-left li[data-s]>.s-ord{grid-column:2;grid-row:1;flex:none;padding:0;text-align:right}
.sx-board .rv-left li[data-s]>.s-no{grid-column:2;grid-row:2;flex:none;padding:0;text-align:right;font-size:10px;line-height:1.2}
.sx-board .rv-left li[data-s]>.s-tx{grid-column:3;grid-row:1/span 3;margin-left:34px}   /* air after the number (JL 261113: "this is too close") */
.sx-board .rv-left li[data-s]>.sx-marks{grid-column:4;grid-row:1}
.sx-board .rv-left li[data-s]>.nt-gut{position:absolute;right:-30px;top:2px;margin:0;padding:0}
/* the sentence just changed, found again after the page loads (sxKeep) */
.sx-board .sx-row.sx-low .rv-left li[data-s]{background:color-mix(in srgb,#e8590c 10%,transparent)}   /* a tint only, no edge line (JL 261114: "I don't like this") */
.sx-board .sx-flash{animation:sxflash 2.6s ease-out}
@keyframes sxflash{0%,35%{box-shadow:0 0 0 3px color-mix(in srgb,#e8a33d 70%,transparent);border-radius:6px}100%{box-shadow:0 0 0 3px transparent}}
/* the margin keeps only +: the old open-comment 💬 repeated the 💬N in the marks (JL 261114: "maybe we don't need it") */
.sx-board .nt-mark{display:none!important}
</style><script>
(function(){if(window.__sxRows)return;window.__sxRows=1;
 function marks(r){var g=r.querySelector('.rv-right');if(!g)return'';
  var ev=g.querySelectorAll('.rv-ev,.ev-card').length,w=g.querySelectorAll('.rv-card[data-state=proposed],.rv-card[data-state=open]').length,h=0;
  var pen=g.querySelectorAll('.rv-card:not(.sx-old):not(.rv-ev):not(.ev-card):not(.sx-histcard):not(.rv-rev):not(.rv-note)').length;
  /* 🕘 counts the sentence's earlier versions; 📝 its edits, current ones first and decided ones after (JL 261113) */
  g.querySelectorAll('.sx-histcard').forEach(function(c){h+=+(c.dataset.n||1);});var old=g.querySelectorAll('.sx-old:not(.sx-histcard)').length;
  var sum=function(k){var t=0;g.querySelectorAll('.rv-ev').forEach(function(c){t+=+(c.dataset[k]||0);});return t;};
  var nv=sum('value'),nc=sum('cite'),nd=sum('display'),ek='<span class=sx-evm role=button tabindex=0 title="';
  /* one mark per kind of evidence, each opening the sentence's cards (JL 261113: "how to add the things like the citation?") */
  var evm=(nv?ek+nv+' value'+(nv>1?'s':'')+'">📊'+nv+'</span>':'')+(nc?ek+nc+' citation'+(nc>1?'s':'')+'">❝︎'+nc+'</span>':'')
   +(nd?ek+nd+' display'+(nd>1?'s':'')+'">🖼️'+nd+'</span>':'')+(ev&&!(nv||nc||nd)?ek+'evidence">📎'+ev+'</span>':'');
  /* the reviewer's score, the lowest of logic, read and AI (JL 261113: "another icon should be AI rating"), and 💬 to
     comment on the sentence, with how many comments it has (JL 261113: "where is the things like the comments icon") */
  var rv=g.querySelector('.rv-rev'),lo=rv?+rv.dataset.low:0,nt=g.querySelectorAll('.rv-note:not(.nt-new)').length;
  var fx=rv&&rv.dataset.fixed,so=rv&&rv.dataset.stale;  /* fixed by the reviewer's words, or changed since: the score is old */
  var ai=rv?'<span class="sx-ai '+(so?'old':fx||lo>=8?'ok':lo>=7?'mid':'low')+'" role=button tabindex=0 title="'+(fx?'fixed since the review; ':so?'scored before the last change; ':'')+(rv.dataset.scores||'')+'">★'+(fx?'✓':so?'–':lo)+'</span>':'';
  /* the sentence's length in words, its citations left out (JL 261113: "could you also show the number of words") */
  var tx=r.querySelector('.rv-left li[data-s] .s-tx'),nw=0;
  if(tx){var cl=tx.cloneNode(true);cl.querySelectorAll('.cite,.sx-marks').forEach(function(x){x.remove();});
   nw=(cl.textContent.match(/[A-Za-z0-9][A-Za-z0-9'’.,%-]*/g)||[]).length;}
  /* the word count lives in the ★ card, not in the row (JL 261113: "I want the wc just in the star, I click it and see it") */
  /* 💬 only where there are comments (JL 261113: "if there are no comments, we can hide this icon"); a new one starts
     from the + in the margin */
  var cm=nt?'<span class=sx-cmt role=button tabindex=0 title="the comments on this sentence">💬'+nt+'</span>':'';
  /* ✓ the person's own pass on the sentence (JL 261113: "a button, which means check ... no need to modify it") */
  var li0=r.querySelector('.rv-left li[data-s]'),on=li0&&li0.dataset.checked==='1',st=li0&&li0.dataset.checked==='stale';
  cm=cm+(li0?'<span class="sx-ok'+(on?' on':st?' stale':'')+'" role=button tabindex=0 title="'+(on?'you checked this sentence; click to take it back':st?'you checked an earlier wording; the words changed, so check it again':'check: this sentence passes, leave it as it is')+'">'+(st?'✓?':'✓')+'</span>':'');   /* ✓ last (JL 261113) */
  return [w,ai+evm+(h?'<span class=sx-clk role=button tabindex=0 title="earlier versions of this sentence">🕘'+h+'</span>':'')
   +(pen||old?'<span class="sx-pen'+(w?' w':'')+(pen?'':' faint')+'" role=button tabindex=0 title="edits: '+pen+' current'+(w?' ('+w+' wait for you)':'')+', '+old+' decided">📝'+(pen||old)+'</span>':'')+cm];}
 /* ★ opens the reviewer's card on the sentence, a good one too (JL 261113: "when I click ★8, why there are no ...") */
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.sx-ai');if(!a)return;e.preventDefault();
  e.stopImmediatePropagation();var r=a.closest('.sx-row');if(!r)return;var on=!r.classList.contains('sx-rev-on');   /* its own toggle: ❝ or 🕘 open beside it do not count */
  /* a second click hides the cards again (JL 261113: "I want to hide it by clicking it, it doesn't work anymore") */
  r.classList.toggle('sx-rev-on',on);
  if(on){r.classList.remove('sx-fold');r.classList.add('sx-open');var c=r.querySelector('.rv-rev');if(c)c.classList.add('open');}
  else{r.classList.remove('sx-open','sx-hist');if(!r.classList.contains('sx-evon')&&!r.classList.contains('sx-ver'))r.classList.add('sx-fold');}},true);
 document.addEventListener('click',function(e){var k=e.target.closest&&e.target.closest('.sx-ok');if(!k)return;e.preventDefault();e.stopImmediatePropagation();   /* the ✓ only marks; it opens no card (JL 261113) */
  var li=k.closest('li[data-s]'),bd=k.closest('.rv-board'),on=!k.classList.contains('on');if(!li||!bd)return;
  fetch('/_board/draft-comment',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({task:bd.dataset.task,act:on?'check':'uncheck',s:li.dataset.s})})
   .then(function(r){return r.json();}).then(function(j){if(!j.ok){k.title=j.err||'not saved';return;}
    k.classList.toggle('on',j.checked);k.classList.remove('stale');k.textContent='✓';li.dataset.checked=j.checked?'1':'';
    k.title=j.checked?'you checked this sentence; click to take it back':'check: this sentence passes, leave it as it is';});},true);
 /* 💬 opens the sentence's comments: the earlier ones, then a box for a new one under them; a second click closes them
    (JL 261113: "does this mean adding the comments, or showing the previous comments? they are different right?") */
 document.addEventListener('click',function(e){var c=e.target.closest&&e.target.closest('.sx-cmt');if(!c)return;e.preventDefault();
  e.stopImmediatePropagation();var li=c.closest('li[data-s],h4[data-p],h3[data-p]'),r=c.closest('.sx-row');if(!li||!r)return;
  var g=r.querySelector('.rv-right');
  if(r.classList.contains('sx-cm-on')){r.classList.remove('sx-cm-on');
   if(r.dataset.cmWasFold==='1')r.classList.add('sx-fold');if(r.dataset.cmWasOpen!=='1')r.classList.remove('sx-open');return;}
  /* 💬 only shows the comments; the + in the margin only adds one (JL 261113: "how to make 💬1 to just show the
     comments, and + to just add the comments") */
  r.dataset.cmWasFold=r.classList.contains('sx-fold')?'1':'';r.dataset.cmWasOpen=r.classList.contains('sx-open')?'1':'';r.classList.add('sx-cm-on');r.classList.remove('sx-fold');r.classList.add('sx-open');
  g&&g.querySelectorAll('.rv-note:not(.nt-new)').forEach(function(n){n.classList.add('open');});},true);
 /* the + only adds a comment: it leaves the comments view, so its new box shows */
 document.addEventListener('click',function(e){var p=e.target.closest&&e.target.closest('.nt-plus');if(!p)return;
  var r=p.closest('.sx-row');if(!r)return;r.classList.remove('sx-cm-on');
  if(!r.classList.contains('sx-add-on')){r.dataset.addWasOpen=r.classList.contains('sx-open')?'1':'';r.classList.add('sx-add-on');}},true);
 /* the new box closed (Comment or Cancel): the row goes back to how it was */
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.nt-new [data-note-act=cancel],.nt-new [data-note-act=add]');
  if(!a)return;var r=a.closest('.sx-row');if(!r||!r.classList.contains('sx-add-on'))return;
  setTimeout(function(){if(r.querySelector('.rv-note.nt-new'))return;r.classList.remove('sx-add-on');
   if(r.dataset.addWasOpen!=='1')r.classList.remove('sx-open');},1200);},true);
 function fold(r,on){r.classList.toggle('sx-fold',on);if(on){r.classList.remove('sx-open','sx-hist');}else if(r.querySelector('.sx-sum'))r.classList.add('sx-open');}
 /* a paragraph folds its sentences; a Section folds its paragraphs and their sentences */
 window.sxPfold=pfold;function pfold(h,on){h.classList.toggle('sx-pfold',on);var sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){
   n.classList.toggle('sx-hide',on);if(!on)n.classList.remove('sx-pfold');n=n.nextElementSibling;}}
 /* row by row, as each arrives: the page streams in, so a board can be half drawn when this first runs */
 function setup(){document.querySelectorAll('.sx-board .sx-row:not([data-sx])').forEach(function(r){r.dataset.sx=1;
  (function(){var li=r.querySelector('.rv-left li[data-s]'),h=r.querySelector('.rv-left h4[data-p]');
   if(li){var t=document.createElement('button');t.type='button';t.className='sx-tog';t.title='open or fold this sentence';
    li.insertBefore(t,li.firstChild);var o=document.createElement('span');o.className='s-ord';t.after(o);var m=marks(r),s=document.createElement('span');s.className='sx-marks';s.innerHTML=m?m[1]:'';
    (li.querySelector('.s-tx')||li).appendChild(s);/* a sentence the reviewer scored below 7 on any axis stands out and opens on its edit cards (JL 261114: "for the sentence below 7, highlight and show what is the editing cards") */var rv7=r.querySelector('.rv-rev'),lo7=rv7&&!rv7.dataset.fixed&&!rv7.dataset.stale?+rv7.dataset.low:10;if(lo7<7)r.classList.add('sx-low');fold(r,!(m&&m[0])&&lo7>=7);}
   else if(r.classList.contains('sx-p')||r.classList.contains('sx-c')){h=h||r.querySelector('.rv-left h3[data-p]');if(!h)return;
    var p=document.createElement('button');p.type='button';p.className='sx-ptog';
    p.title=r.classList.contains('sx-c')?'fold or open this Section':'fold or open this paragraph';h.insertBefore(p,h.firstChild);
    var pm=marks(r),ps=document.createElement('span');ps.className='sx-marks';ps.innerHTML=pm?pm[1]:'';h.appendChild(ps);}})();});order();}
 /* each sentence's place in reading order, counted again in each part (C1 title, C2 text, C3 keywords) */
 /* a paragraph is numbered as a sentence is (JL 261113: "it should be just like the sentences"): its place in reading
    order large, its fixed id (C1.P30) small after its title, so P30 no longer reads as if P4 to P29 were missing */
 function porder(){document.querySelectorAll('.sx-board').forEach(function(b){var m=0;
  b.querySelectorAll('h3.rv-part,.rv-left h4[data-p]').forEach(function(h){if(h.tagName==='H3'){m=0;return;}m+=1;
   var o=h.querySelector(':scope>.p-ord');
   if(!o){var tn=[].find.call(h.childNodes,function(c){return c.nodeType===3&&/C\\d+\\.P\\d+\\s*·/.test(c.nodeValue);});
    if(tn){tn.nodeValue=tn.nodeValue.replace(/^\\s*C\\d+\\.P\\d+\\s*·\\s*/,'');}
    o=document.createElement('span');o.className='p-ord';var tg=h.querySelector(':scope>.sx-ptog');h.insertBefore(o,tg?tg.nextSibling:h.firstChild);
    var id=document.createElement('span');id.className='p-no';id.textContent=h.dataset.p.split('.').pop();
    var mk=h.querySelector(':scope>.sx-marks,:scope>.nt-gut');h.insertBefore(id,mk||null);}
   o.textContent=m;o.title='paragraph '+m+' in reading order; '+h.dataset.p+' is its fixed id';});});}
 /* paragraphs keep their old fixed id, "C2.P2 · title" (JL 261113: "I want the old paragraph index, current one
    is so ugly"); porder stays unused */
 /* the large number counts again in each paragraph (JL 261114: "it is section level, how could we make it sentence
    level"): 1, 2, 3 within the paragraph; the fixed id (S7) stays small under it, as cards and comments name it */
 function order(){document.querySelectorAll('.sx-board').forEach(function(b){var n=0;
  b.querySelectorAll('h3.rv-part,.rv-left h4[data-p],.rv-left li[data-s]').forEach(function(x){if(x.tagName==='H3'||x.tagName==='H4'){n=0;return;}
   var o=x.querySelector(':scope>.s-ord');if(!o)return;n+=1;o.textContent=n;o.title='sentence '+n+' of its paragraph; '+
   (x.dataset.a||x.dataset.s)+' is its fixed id';});});}
 document.addEventListener('click',function(e){if(!e.target.closest)return;
  /* ❝ 📊 🖼️ open the sentence's evidence only, on their own toggle (JL 261113: "when I click it, there are not reaction"):
     sharing the 📝 toggle, a click on ❝ after ★ had opened the row closed it again */
  var v=e.target.closest('.sx-evm');if(v){e.preventDefault();e.stopPropagation();var vr=v.closest('.sx-row');
   vr.classList.remove('sx-fold');vr.classList.toggle('sx-evon');return;}
  var q=e.target.closest('.sx-pen');if(q){e.preventDefault();e.stopPropagation();var qr=q.closest('.sx-row');
   qr.classList.remove('sx-fold');var qon=!qr.classList.contains('sx-open');qr.classList.toggle('sx-open',qon);qr.classList.toggle('sx-hist',qon);return;}
  var k=e.target.closest('.sx-clk');if(k){e.preventDefault();e.stopPropagation();var kr=k.closest('.sx-row');
   kr.classList.remove('sx-fold');kr.classList.toggle('sx-ver');return;}
  var t=e.target.closest('.sx-tog');if(t){e.preventDefault();e.stopPropagation();var r=t.closest('.sx-row');fold(r,!r.classList.contains('sx-fold'));return;}
  var p=e.target.closest('.sx-ptog');if(p){e.preventDefault();e.stopPropagation();var h=p.closest('.sx-row');pfold(h,!h.classList.contains('sx-pfold'));return;}
  var a=e.target.closest('[data-sx-all]');if(a){e.preventDefault();var b=a.closest('.sx-board'),on=a.dataset.sxAll==='fold';
   b.querySelectorAll('.sx-row.sx-p,.sx-row.sx-c').forEach(function(h){pfold(h,false);});
   b.querySelectorAll('.sx-row').forEach(function(r){if(r.querySelector('.sx-tog'))fold(r,on);});return;}
  var li=e.target.closest('.sx-row.sx-fold .rv-left li[data-s]');if(li&&!e.target.closest('a')){e.preventDefault();fold(li.closest('.sx-row'),false);}},true);
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup);else setup();
 /* a row's cards can stream in after its row was set up, so its marks are counted again once the page is whole
    (S6a lost its 📊 and 🕘 when its cards came late) */
 /* after a written change the page loads again; it comes back to the same sentence, flashed, instead of the top
    (JL 261114: "the focal sentence is jump to another places and it is hard for me to find") */
 window.sxKeep=function(el){try{var r=el&&el.closest&&el.closest('.sx-row'),li=r&&r.querySelector('.rv-left li[data-s]');
  if(li)sessionStorage.setItem('sx-keep',li.dataset.a||li.dataset.s);}catch(x){}};
 (function(){var k=null;try{k=sessionStorage.getItem('sx-keep');sessionStorage.removeItem('sx-keep');}catch(x){}if(!k)return;window.sxKept=k;
  var n=0;(function go(){var li=document.querySelector('.sx-board .rv-left li[data-a="'+k+'"]')||document.querySelector('.sx-board .rv-left li[data-s="'+k+'"]');
   if(!li){if(++n<40)setTimeout(go,150);return;}
   var row=li.closest('.sx-row'),hs=[];for(var x=row&&row.previousElementSibling;x;x=x.previousElementSibling){
    if(x.classList.contains('sx-c')){hs.unshift(x);break;}if(x.classList.contains('sx-p')&&!hs.length)hs.push(x);}
   hs.forEach(function(h){if(h.classList.contains('sx-pfold')&&window.sxPfold)window.sxPfold(h,false);});   /* open its folded paragraph */
   var land=function(){li.scrollIntoView({block:'center'});};land();setTimeout(land,700);
   var r=li.closest('.sx-row')||li;r.classList.add('sx-flash');setTimeout(function(){r.classList.remove('sx-flash');},2600);})();})();
 /* ✓ Use this on a reviewer's suggestion: an accepted Edit card with its words (card_act adopt), then the page again */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.lg-use');if(!b)return;
  e.preventDefault();e.stopPropagation();var t=b.closest('[data-task]')||document.querySelector('[data-task]'),m=b.nextElementSibling;
  if(!t){if(m)m.textContent='no Task here';return;}b.disabled=true;
  fetch('/_board/draft-card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task:t.dataset.task,
   act:'adopt',s:b.dataset.adopt,original:b.dataset.orig,expected:b.dataset.new})}).then(function(r){return r.json();})
   .then(function(j){if(!j.ok){b.disabled=false;if(m)m.textContent=j.err||'not saved';return;}if(m)m.textContent='accepted';
    setTimeout(function(){if(window.sxKeep)window.sxKeep(b);location.reload();},400);}).catch(function(x){b.disabled=false;if(m)m.textContent=String(x);});},true);
 /* 🔄 the page follows its files (JL 261114: "How to make the UI to be auto refreshed to show the changes?"): every 4 s
    it asks /_board/draft-stamp for the folder's newest change; when that moves and the reader is not typing, editing a
    card, writing a comment or selecting text, it reloads and comes back to the sentence in view (sxKeep) */
 (function live(){if(window.__sxLive)return;var bd=document.querySelector('.rv-board[data-task]');
  if(!bd){setTimeout(live,1000);return;}window.__sxLive=1;   /* the board streams in after this script */
  var url='/_board/draft-stamp?path='+encodeURIComponent(bd.dataset.task),last=null,due=false;
  function busy(){var a=document.activeElement;if(a&&(a.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)))return true;
   if(document.querySelector('.rv-card.editing,.rv-note.writing,.rv-note.nt-new'))return true;
   var sel=window.getSelection&&window.getSelection();return !!(sel&&String(sel).trim());}
  function inView(){var best=null,d=1e9,mid=innerHeight/2;document.querySelectorAll('.sx-board .rv-left li[data-s]').forEach(function(li){
   var r=li.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;var x=Math.abs((r.top+r.bottom)/2-mid);if(x<d){d=x;best=li;}});return best;}
  function reload(){var li=inView();if(li&&window.sxKeep)window.sxKeep(li);location.reload();}
  function tick(){if(document.hidden)return;fetch(url,{cache:'no-store'}).then(function(r){return r.json();}).then(function(j){
   if(last===null||Date.now()<(window.sxQuiet||0)){last=j.stamp;due=false;return;}if(j.stamp!==last){last=j.stamp;due=true;}
   if(due&&window.sxPill)window.sxPill(reload);else if(due&&!busy())reload();}).catch(function(){});}
  setInterval(tick,4000);tick();})();
 function remark(){document.querySelectorAll('.sx-board .sx-row[data-sx]').forEach(function(r){
  var li=r.querySelector('.rv-left li[data-s]'),s=li&&li.querySelector('.sx-marks');if(!s)return;var m=marks(r);
  /* compare with the last marks written, never with innerHTML: the browser rewrites quotes, so innerHTML never equals
     the string, and each rewrite fired the observer again, every frame; a ✓ swapped out between mouse down and up lost
     its click (JL 261113: "the check doesn't work anymore") */
  if(m&&s.dataset.m!==m[1]){s.innerHTML=m[1];s.dataset.m=m[1];}});}
 document.addEventListener('DOMContentLoaded',remark);window.addEventListener('load',remark);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))setup();
  if(document.readyState==='complete')remark();});}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>"""


# ── what the text and its plan leave unsure ───────────────────────────────────────────────────────
# 3 · Evidence shows every point still open beside its sentence, card or no card (JL 261021: "我们的 evidence 该怎么把这些
# 不确定的 ... 都加上去"): the writer's own marks in §3 and each §1 point that says it has no evidence. OPEN <n> in
# reading order; the Evidence prompt turns each into a card item, or leaves it as the paper's own reasoning.
OPEN_KIND = {"check": ("❓", "to check", "#e03131"), "find": ("❓", "to find", "#e03131"),
             "pending": ("⏳", "waits on a Run", "#e67700"), "none": ("⚪", "no evidence", "#868e96")}
MARK = re.compile(r"⟦([^⟦⟧]*(?:⟦[^⟦⟧]*⟧[^⟦⟧]*)*)⟧")


def _open_points(d: dict | None) -> list:
    """[{s, kind, what}] in reading order: each ⟦…⟧ in a §3 sentence (⟦check: …⟧ a source named but not yet verified,
    ⟦pending …⟧ or a one- or two-word ⟦x⟧ a value a Run has not given, any other a source still to find), then each §1
    point whose evidence line says `Evidence: none · <why>`."""
    out = []
    for _, body in (d or {}).get("text", []):
        for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", body):
            for mk in MARK.findall(m.group(2)):
                low = mk.strip().lower()
                kind = ("check" if low.startswith("check") else
                        "pending" if low.startswith("pending") or (len(low.split()) <= 2 and ":" not in low) else "find")
                out.append({"s": m.group(1), "kind": kind,
                            "what": re.sub(r"^(check|pending)\b\s*:?\s*", "", mk.strip(), flags=re.I)})
    if d and d.get("structure"):
        for m in re.finditer(r"(?ms)^- B\d+[a-z]* · (S\d+[a-z]*) · .*?(?=^- B\d+[a-z]* · |^#{2,4} |\Z)", d["structure"][1]):
            e = re.search(r"(?m)^\s*Evidence:\s*none\b\s*·?\s*(.*)$", m.group(0))
            if e:
                out.append({"s": m.group(1), "kind": "none", "what": e.group(1).strip()})
    return sorted(out, key=lambda o: _s_key(o["s"]))


def _open_row(o: dict, n: int, sentences: bool = False) -> str:
    icon, word, ink = OPEN_KIND[o["kind"]]
    return (f'<tr data-s="{esc(o["s"])}"><td style="white-space:nowrap;width:1%;padding:5px 8px 5px 0">'
            f'<b style="color:{ink};font-size:12.5px">OPEN {n}</b></td>'
            + (f'<td class=mut style="white-space:nowrap;width:1%;padding:5px 8px 5px 0;font-size:12.5px">{esc(o["s"])}</td>'
               if sentences else "")
            + f'<td style="width:1%;padding:5px 8px 5px 0">{icon}</td><td style="padding:5px 0;line-height:1.5">'
            f'<span style="color:{ink}">{word}</span>' + (f' · <span class=mut>{esc(o["what"])}</span>' if o["what"] else "")
            + '</td></tr>')


def _open_fold(opens: list) -> str:
    """Every open point in one list, the sentence beside each, the ones to check or find first."""
    if not opens:
        return ""
    rank = {"check": 0, "find": 0, "pending": 1, "none": 2}
    rows = "".join(_open_row(o, n, sentences=True) for n, o in
                   sorted(enumerate(opens, 1), key=lambda x: (rank[x[1]["kind"]], x[0])))
    # a label carries no count (AGENTS.md § Page words): each point shows its own mark where it sits
    return (f'<details class="topic work-task"><summary><span class=related-head><b>❓ Open points</b></span></summary>'
            f'<div class=work-body><table class="rv-rows ev-list" style="border-collapse:collapse;width:100%">{rows}'
            '</table></div></details>')


def _text_and_evidence(d: dict, ev: dict, root: Path, opens: list = (), xs=()) -> str:
    """The text on the left, read on as one column, and at each sentence on the right its card: a row per item that backs
    it, then the points still open there (OPEN n). An item backing two sentences shows beside both; a sentence the cards
    name that the text no longer has, or an item naming none, ends the column. With no text yet, the cards alone."""
    by, one = {}, []
    for c in ev["cards"]:
        for n, it in enumerate(c["items"], 1):
            one.append({"kind": c["kind"], "label": f'{c["label"]}.{n}', "items": [it]})
            for s in _s_ids(it) or [""]:
                by.setdefault(s, []).append(_evidence_row(c, it, n, brief=True))
    for n, o in enumerate(opens, 1):
        by.setdefault(o["s"], []).append(_open_row(o, n))
    if not d or not d["text"]:
        order = sorted(by, key=lambda s: _s_key(s) if s else (10 ** 7, ""))
        return EV_CSS + CARDS_CSS + "".join(_ev_card(s, by[s]) for s in order) + CARDS_JS
    marks = _marks({"cards": one})      # each mark names its item, CITE 1.4, as its row does
    body = (f'<p class=space-reads>{_code(d["file"], root)}'                 # no "· —" when no cards file yet (r02)
            + (f' · {_code(ev["path"], root)}' if ev.get("path") and Path(ev["path"]).is_file() else "") + '</p>'
            + _text_rows(d, marks, {s: _ev_card(s, rows) for s, rows in by.items()}, "Cards for no sentence in this text",
                         xs, root))
    return EV_CSS + CARDS_CSS + _fold(f"🔎 The text and its Evidence · {d['version']}", body, open_=True) + CARDS_JS


def _evidence_step(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, ev = f["draft"], f["ev"]
    open_asks = sum(not t for t, _ in ev["proposals"])
    opens = _open_points(d)
    # no tallies (AGENTS § Page words): each card item, open point and problem shows its own mark where it sits
    rows = [("Reads", esc(f"§1 at the plan · the text {d['version']} as a reader" if d else "§1 at the plan")),
            ("Cards", _code(ev["path"], root) if ev["path"] else '<span class=mut>no evidence/cards.yaml yet</span>'),
            ("Asks", (_code(ev["props_path"], root) + (esc(f" · {open_asks} wait{'s' * (open_asks == 1)} for you")
                                                       if open_asks else "")) if ev["props_path"] else '<span class=mut>none</span>'),
            ("Check", ('<span class="st st-ok">✅</span>' if not ev["problems"] else '<span class="st st-warn">❗</span>')
             if ev["path"] else '<span class=mut>—</span>')]
    prompt = (f"/haipipe-evidence {f['t']}: a card for each claim in {_poss(f['section'])} plan (have, ask a Job, ask a "
              f"person, soften), the asks in proposals.md; then read {f['section']} as a reader for claims the plan "
              "missed. Give every open point an item: each ⟦check⟧ its source verified, each source still to find a "
              "need with a proposal, each ⟦pending⟧ the Run it waits on, and each 'Evidence: none' a reader could "
              "doubt a source or our own value; leave the paper's own reasoning as it is. Stop for my tick.")
    op = _step_box("🔎 Stage 3 · Evidence", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "evidence"))
    cards = (_text_and_evidence(d, ev, root, opens, f["displays"]) + _card_folds(ev) + _open_fold(opens) if ev["cards"] or opens else
             _not_yet("No Evidence cards yet."))
    if ev["proposals"]:
        lines = "".join(f'<li>{"☑" if t else "☐"} {_inline(line, {})}</li>' for t, line in ev["proposals"])
        cards += _fold("✍ Asks, for you to tick", f'<p class=space-reads>{_code(ev["props_path"], root)}</p>'
                       f'<ul style="list-style:none;padding-left:4px">{lines}</ul>', open_=open_asks > 0,
                       word=f'{open_asks} wait{"s" if open_asks == 1 else ""} for you' if open_asks else "")
    if ev["problems"]:                           # each problem is a line below; no "N to fix" on the bar
        cards += _fold("❗ What does not resolve", "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in ev["problems"]) + "</ul>")
    return op, cards, ()
