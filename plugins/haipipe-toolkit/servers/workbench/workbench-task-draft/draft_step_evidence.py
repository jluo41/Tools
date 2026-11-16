"""3 · Evidence and 4 · Display of the draft Task (draft_steps.py): evidence rows, the sentence board's slots, the open
points, the display units, and both steps' views; draft_steps re-exports them all."""
from __future__ import annotations

import re
from html import unescape
from pathlib import Path
from urllib.parse import quote

from live.frame import _rel, esc
from live.sentence_id import sid as _sid
from live.draft_steps_assets import CARDS_CSS, CARDS_JS, EV_CSS
from live.draft_steps_common import (
    _code, FLAT, _fold, INK, _inline, _kv, _marks, _md, _not_yet, _parts, _poss, _prompt_box, _step_box, _word)
# 4 · Display moved out (600-line rule); every name stays importable here
from live.draft_step_evidence_display import (  # noqa: F401
    _calls, CALLS, _display_card, DISPLAY_INK, _display_step, _displays, _field, float_url, REFS, _units)
# the sentence board's look (SX_ROWS) and the open points moved out (700-line rule); every name stays importable here
from live.draft_step_evidence_rows import SX_ROWS  # noqa: F401
from live.draft_step_evidence_open import (  # noqa: F401
    MARK, OPEN_KIND, _open_fold, _open_points, _open_row, _s_key)


EV_STATE = {"have": '<span title="have">✅</span>', "need": '<span title="asked">❓</span>',
            "missing": '<span title="not found">❗</span>'}


def _s_ids(it: dict) -> list:
    """An item's sentences, `for: [2, 4]` (or "2a", or an older "S2"), as the text's ids: s2, s4."""
    return ["s" + str(n).lstrip("Ss") for n in it.get("for") or []]


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
    (JL 261021: "如果我们有图片或者表格的话 ... PNG TO EMBED UNDER THAT SENTENCE"): the typeset float at full box
    width (float_url: page 1 of float.pdf, else of preview.pdf cut to its float), which opens full size, and one line
    under it, its name and Run; without a rasterizer its preview.png; one not built yet says so. The unit stays the source (its
    README, recipe and the Run that made the asset); the page only shows its picture."""
    order = [_sid(m) for _, b in (d or {}).get("text", []) for m in re.findall(r"(?m)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · ", b)]
    from live.draft_step_support import xref_spans   # an Extended Data name reads as a reference to its Section
    html = xref_spans(html, xs)
    for x in xs or ():
        if x.get("owner"):  # another Section's display shows only where the paper prints it (JL 261114: "only need to show in first place ... should be in the results")
            continue
        first = next((sid for sid in order if sid in map(_sid, x.get("calls", []))), "")
        m = first and re.search(r'<li data-s="' + re.escape(first) + r'"[^>]*>.*?</li>', html, re.S)
        if not m:
            continue
        # the name a reader knows (Table 2), never the LaTeX label (JL 261023: the box said "tab:online-ratings")
        name = x.get("shown") or (x["names"][0] if x.get("names") else x["title"])
        # the typeset float, figure and caption as the paper prints them, and one line under it: its name and Run.
        # No caption rebuilt in HTML: it leaked LaTeX ("95\\% interval"; M-D18)
        line = esc(" · ".join(w for w in (name, x.get("run", "")) if w))
        src = float_url(x, root)
        if src:
            fig = (f'<a href="{esc(src)}" target=_blank><img src="{esc(src)}" loading=lazy '
                   f'alt="{esc(x.get("alt") or name)}"></a><figcaption>{line}</figcaption>')
        elif x.get("pdf"):
            fig = f'<figcaption>{line} · {_code(x["pdf"], root)}</figcaption>'
        else:
            fig = (f'<figcaption><b>{esc(name)}</b> · ' + ("not built yet" if x.get("made") else "no unit in display/ yet")
                   + (f' · {esc(x["claim"])}' if x.get("claim") else "") + '</figcaption>')
        html = html[:m.end()] + f'<li class="disp-embed{" disp-none" if not src else ""}"><figure>{fig}</figure></li>' + html[m.end():]
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
            who = re.sub(r"\\([&%$#_])", r"\1", who)   # a Bib's LaTeX escape reads as the sign (AITC 261115: "Medicare \& Medicaid")
            if who and year:                   # an entry without author or year reads as "not in Bib"
                out.setdefault(m.group(1), f"{who} {year}")
    return out


def _cite_names(html: str, d: dict, marks: bool = True) -> str:
    """Each citation as the compiled paper prints it, "(Barnett et al. 2017; Hoppe et al. 2017)", its keys on hover; the
    source keeps \\citep{...} (JL 261113, after trying the raw LaTeX: "how about we just make the citations to be the
    readable one?"). A key with no Bib entry (or one without author and year) shows the key and a visible "not in Bib"
    mark (must-check M-D02). The web export does the same with its own copy, haipipe-draft `src/cite_names.py`."""
    names = _bib_names(d)
    # marks only on the current Draft's own sentences: a card or history row shows an old key as plain text (M-D18)
    miss = (lambda k: f'{esc(k)} <span class=cite-miss title="no entry for {esc(k)} in draft/evidence/bibex/*.bib">not in Bib</span>'
            ) if marks else esc
    # a cited key the citation Job has not verified carries a quiet mark; a verified one its state on hover (M-D18)
    from live.draft_step_support import cite_states
    states = cite_states(Path(d["file"]).parent.parent) if marks and d.get("file") else {}
    def unv(keys):
        """One quiet mark per citation for its keys the citation Job has not verified, which it names on hover."""
        out = [f'{k}: {states.get(k, (False, "no citation check names it"))[1]}' for k in keys
               if marks and k in names and not states.get(k, (False, ""))[0]]
        return f'<span class=cite-unv title="not verified · {esc("; ".join(out))}">?</span>' if out else ""
    shown_one = lambda k: esc(names[k]) if k in names else miss(k)
    def one(m):
        keys = [k.strip() for k in m.group(1).split(";") if k.strip()]
        shown = "; ".join(shown_one(k) for k in keys)
        return f'<span class="cite cite-ay" title="{esc(", ".join(keys))}">({shown}){unv(keys)}</span>'
    html = CITE_SPAN.sub(one, html)
    # \\citet is the narrative form, as natbib prints it: "Barnett et al. (2017)", so the two never look alike (JL 261113:
    # "if we have this issue, maybe using the \\cite should be better")
    def narr(m):
        keys = [k.strip() for k in m.group(1).split(",") if k.strip()]
        parts = []
        for k in keys:
            who, _, year = names.get(k, k).rpartition(" ")
            parts.append(esc(f"{who} ({year})") if k in names and who and year.isdigit() else shown_one(k))
        return f'<span class="cite cite-ay cite-t" title="{esc(", ".join(keys))}">{"; ".join(parts)}{unv(keys)}</span>'
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
    if d.get("file"):                    # \ref reads "Figure 2" (M-D18)
        from live.draft_card_text import ref_names, ref_text
        text = ref_text(text, ref_names(Path(d["file"]).parent.parent))
        from live.draft_step_support import support_marks   # each sentence's support (M-D18)
        text = support_marks(text, d, Path(d["file"]).parent.parent)
    seq = [_sid(m) for _, b in d["text"] for m in re.findall(r"(?m)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · ", b)]
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
            m = re.match(r"^- (B\d+[a-z]*) · ([Ss]\d+[a-z]*) · ", line)
            if m:
                if not out:
                    out.append(("", []))
                out[-1][1].append((m.group(1), _sid(m.group(2))))
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
    if b and not re.match(r"[^·]+·\s*[Ss]\d", head):
        hit = next((f"{pid}.{sid}" if pid else sid for pid, bs in paras if pid == b.group(1) for bb, sid in bs
                    if bb == b.group(2)), "")
        if hit:
            return hit
    for tok in _sid(s).split():
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


SX_OLD = ("accepted", "written", "applied", "rejected", "superseded", "done", "history")   # decided: folded (M-D13)


def _sx_bar(cards: list) -> str:
    """A sentence's cards, folded under one button that says where they stand (JL 261113: "by default hidden, click it
    to show its status, and after click it, we can click a new button to show its faded history"): open shows the
    cards still current; History adds the decided ones, faded."""
    if not cards:
        return ""
    old = [c for c in cards if _sx_attr(c, "data-state") in SX_OLD]
    now = len(cards) - len(old)
    wait = sum(_sx_attr(c, "data-state") in ("proposed", "open") for c in cards)
    # a label names a thing, no count (AGENTS § Page words); only "N wait for you" stays, being the answer itself
    said = "Cards" + (f" · {wait} wait for you" if wait else "")
    return ('<div class=sx-bar>' + (f'<button type=button class="sx-sum{" wait" if wait else ""}">{said}</button>' if now else "")
            + ('<button type=button class=sx-hb>History</button>'
               if old else "") + '</div>'
            + "".join(c.replace('class="rv-card', 'class="rv-card sx-old', 1) if c in old else c for c in cards))


def _sx_board(rows: str, cls: str = "") -> str:
    """The rows, with the switch between cards beside each sentence and cards under it (CARDS_JS keeps the choice),
    and the switch that folds every sentence to one line or opens them all (SX_ROWS)."""
    from live.draft_autofold import AUTOFOLD_JS; from live.draft_math import MATH_JS   # folds; math typeset (KaTeX)
    return SX_ROWS + AUTOFOLD_JS + MATH_JS + f'<div class="sx-board sx-ud sx-fixed{(" " + cls) if cls else ""}">' + rows + '</div>'





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
