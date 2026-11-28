"""The Story views beside the logic tree: High-level logic + Low-level work, Related Papers and RoadMap Draw.
Moved from paper.py, which re-exports every name here so `from live.paper import related_html` keeps working."""
import json
import re
from pathlib import Path
from urllib.parse import quote

from live.paper import (_addresses, _disc_lookup, _file_link, _find, _links, _tree_url, current_stories, esc, read,
                        scalar)
from live.paper_story_tree import _lw_row, _q_block, _rest_block, story_tree


def logic_work_html(d):
    """Story › High-level logic + Low-level work (JL 260929): one tree, visually split.
    Each question is a block; its left side is the high-level logic (hypotheses, potential
    claims, potential contributions), its right side the low-level work that tests it,
    each piece named as a question, in the order it runs, with its B → J → T → R."""
    # board.md `story-current:` names the Story being worked on (JL 260930: one paper in this
    # tree, no Story labels); without it every Story's questions are drawn, as before
    blocks = []
    for s in current_stories(d):
        T = story_tree(s)
        blocks += [_q_block(d, T, q) for q in T["questions"]]
        blocks.append(_rest_block(d, T))
    if not blocks:
        return '<div class="space-empty">No research question yet.</div>'
    head = _lw_row("", "High-level logic", "Low-level work · B → J → T → R", "lw-head", report="Report")
    return '<div class="lw">%s%s</div>' % (head, "".join(blocks))


# Story › Related Papers (JL 260930): papers from the venue the paper is written for,
# one card each, the original PDF readable inside the card. The rows are the Story's
# §5.3 P-board; each names the Discovery Paper Run that holds the paper (its Bib,
# abstract, facts and, when a free copy exists, paper.pdf).
RELATED_ROLES = (("closest", "Closest to this paper", "hyp"), ("question", "For one research question", "claim"),
                 ("background", "Background", "found"), ("caution", "Cautions and framing", "contrib"))


def _cell(heads, row, name):
    """The cell under the first header starting with `name` ('' when none)."""
    i = next((k for k, h in enumerate(heads) if h.strip().lower().startswith(name)), None)
    return row[i].strip() if i is not None and i < len(row) else ""


def _disc_run(d, addr):
    """`b01j02t01r03` → that Paper Run's Result folder in the Discovery home, or None."""
    m = re.fullmatch(r"(b\d{2}j\d{2}t\d{2})(r\d{2})", addr or "")
    hit = _disc_lookup(d, m.group(1)) if m else None
    task = hit[2] if hit else None
    if task is None:
        return None
    own = _find(task["dir"] / "runs", m.group(2))            # one folder per Run: runs/<run>/result/
    if own is not None and (own / "result").is_dir():
        return own / "result"
    return _find(task["dir"] / "results", m.group(2))


def _yaml_block(text, block):
    """The `key: value` lines indented under one top-level `block:` of a small YAML file."""
    out, on = {}, False
    for line in (text or "").splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            on = line.split(":", 1)[0].strip() == block
            continue
        m = re.match(r"^\s+([\w-]+):\s*(.*?)\s*$", line) if on else None
        if m:
            out.setdefault(m.group(1), m.group(2).strip().strip("\"'"))
    return out


def _scalar_yaml(v):
    """One YAML scalar as `yaml.safe_dump` writes it: plain, 'single' ('' escapes) or "double"."""
    v = v.strip()
    if len(v) > 1 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) > 1 and v[0] == v[-1] == '"':
        try:
            return json.loads(v)
        except ValueError:
            return v[1:-1]
    return v


def logic_work_data(path):
    """A Paper Run's logic-work.yaml (hai-discovery 0.20): top-level `key: value` scalars and
    `key:` lists of `- item` strings, as the Discovery builder writes them. {} when absent."""
    out, key = {}, None
    for line in read(path).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^-\s+(.*)$", line) or re.match(r"^\s+-\s+(.*)$", line)
        if m and key:
            out.setdefault(key, [])
            if isinstance(out[key], list):
                out[key].append(_scalar_yaml(m.group(1)))
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = _scalar_yaml(m.group(2)) if m.group(2).strip() else []
    return out


def paper_card_data(run):
    """What one Paper Run's Result folder says about its paper."""
    subj = _yaml_block(read(run / "runtime.yaml"), "subject")
    try:
        acc = json.loads(read(run / "source-access.json") or "{}")
    except ValueError:
        acc = {}
    abstract = " ".join(ln.strip() for ln in read(run / "abstract.md").splitlines()
                        if ln.strip() and not ln.lstrip().startswith(("#", "Source:", ">")))
    doi = subj.get("doi", "")
    return {"title": subj.get("title", ""), "authors": subj.get("authors", ""), "venue": subj.get("venue", ""),
            "abstract": abstract, "pdf": (run / "paper.pdf") if (run / "paper.pdf").is_file() else None,
            # other open PDFs the Run holds (a supplement, a peer-review file, an earlier version): linked, never
            # shown as the paper, because they are not the article
            "more_pdfs": sorted(x for x in run.glob("*.pdf") if x.name != "paper.pdf"),
            "publisher": (acc.get("links") or {}).get("publisher") or ("https://doi.org/" + doi if doi else ""),
            "card": run / (run.name + ".md"),
            # the paper's own logic and work, written by the Run's ticket (JL 261002)
            "lw": logic_work_data(run / "logic-work.yaml")}


def _first_author(authors):
    """`Xiao Gu; Wei Tang; …` → `Gu et al.`; `Frey, Nathan C.` keeps the surname; a group
    author (`AI-READI Consortium`) keeps its whole name."""
    names = [a.strip() for a in (authors or "").split(";") if a.strip()]
    if not names:
        return ""
    group = re.search(r"\b(Consortium|Group|Committee|Collaboration|Investigators|Study)\b", names[0])
    first = names[0] if group else names[0].split(",")[0].strip() if "," in names[0] else names[0].split()[-1]
    return first + (" et al." if len(names) > 1 else "")


def venue_name(d):
    """The target venue: the H1 of board.md's `venue-page`, before its colon."""
    rel = _links(read(d["board"] / "board.md")).get("venue-page", "")
    h1 = re.search(r"^#\s+(.+)$", read((d["board"] / rel).resolve()), re.M) if rel else None
    return h1.group(1).split(":")[0].strip() if h1 else ""


def _short_venue(v):
    """`Nature Machine Intelligence 8, 220-233 (2026) · Article` → (`Nature Machine Intelligence`, `2026`);
    `NeurIPS 2022 · Conference paper` → (`NeurIPS`, `2022`); `arXiv preprint 2001.08361 (2020)` → (`arXiv`, `2020`);
    `Nature 656(8126), 115-122 (2026)` → (`Nature`, `2026`): a parenthesized issue number is not a year."""
    v = v or ""
    year = re.search(r"\(((?:19|20)\d{2})\)", v) or re.search(r"\b((?:19|20)\d{2})\b", v)
    name = "arXiv" if v.startswith("arXiv") else re.sub(r"\s*\b(?:19|20)\d{2}\b", "", re.sub(
        r"\s+\d+,.*$", "", re.sub(r"\s*\(\d{4}\)", "", v.split(" · ")[0]))).strip()
    return name, year.group(1) if year else ""


BEARS = (("support", "ok", "supports"), ("contradict", "bad", "contradicts"), ("limit", "warn", "limits"),
         ("method", "acc", "method"), ("frame", "mut", "frames"))


def _bears(cell):
    """`Q1 limits; Q2 supports` → one chip per question, coloured by its verdict (JL 261002)."""
    chips = []
    for part in [x.strip() for x in re.split(r"[;,·]", cell or "") if x.strip()]:
        m = re.match(r"^(\S+)\s+(.*)$", part)
        q, verb = (m.group(1), m.group(2)) if m else (part, "")
        cls, word = next(((c, w) for k, c, w in BEARS if k in verb.lower()), ("mut", verb or "bears on"))
        chips.append('<span class="rp-bear rp-bear-%s"><b>%s</b> %s</span>' % (cls, esc(q), esc(word)))
    return '<div class="rp-bears">%s</div>' % "".join(chips) if chips else ""


def _lw_table(lw):
    """The paper's own logic beside its work (JL 261002: "a table like its High Logic and Low
    Work"): left what it asks, finds and contributes; right the data and method that do the
    work. Read from the Run's logic-work.yaml; nothing is shown when the Run has none."""
    if not lw.get("question"):
        return ""
    pill = lambda k: '<span class="item-kind">%s</span>' % esc(k)
    item = lambda k, txt: '<div class="lw-c"><div class="lw-top">%s</div><div class="lw-body">%s</div></div>' % (pill(k), esc(txt))
    lst = lambda k, xs: "".join(item("%s %d" % (k, i + 1), x) for i, x in enumerate(xs if isinstance(xs, list) else [xs]))
    src = {"pdf": "the PDF", "full-text": "the full text", "supplement": "the supplement", "abstract": "the abstract only"}
    head = _lw_row("", "Their logic", "Their work · read from %s" % esc(src.get(lw.get("read_from"), lw.get("read_from") or "?")), "lw-head")
    rows = [_lw_row("", item("Question", lw["question"]), item("Data", lw.get("data", ""))),
            _lw_row("", lst("Finding", lw.get("findings") or []), lst("Method", lw.get("method") or [])),
            _lw_row("", item("Contribution", lw.get("contribution", "")), "")]
    # it folds, closed, as the Abstract does (JL 261005: "make this collapsable as well")
    return ('<details class="rp-lwd"><summary>Their logic · Their work</summary><div class="lw rp-lw">%s%s</div></details>'
            % (head, "".join(rows)))


def _paper_card(d, s, row):
    """One related paper. Closed, two plain lines (JL 260930: "too messy … no need to
    show all the details in the card front face"): the title, then who, when and where,
    with the question and a 📄 when the PDF is inside. Open: why it matters, its links,
    the abstract (folded) and the PDF itself; no facts line (JL 260930: "not relevant").
    Returns (html, has_pdf, venue)."""
    heads, pid = s["pp_h"], row[0]
    addr = next(iter(_addresses(_cell(heads, row, "discovery") or " ".join(row[1:]))), "")
    run = _disc_run(d, addr)
    m = paper_card_data(run) if run is not None else {}
    title = m.get("title") or _cell(heads, row, "paper") or pid
    venue, year = _short_venue(m.get("venue"))
    who = " · ".join(x for x in (_first_author(m.get("authors")), year, venue) if x) or _cell(heads, row, "paper")
    q = _cell(heads, row, "question")
    qword = "All" if q.lower() in ("all", "every question") else q
    pdf = m.get("pdf")
    marks = ('<span class="rp-q">%s</span>' % esc(qword) if q else "") + ('<span title="PDF inside">📄</span>' if pdf else "")
    summary = ('<summary><span class="bjt-chev">▸</span><div class="lw-sum"><div class="rp-title">%s</div>'
               '<div class="rp-sub"><span>%s</span><span class="rp-marks">%s</span></div></div></summary>'
               % (esc(title), esc(who) if run is not None else
                  '<span class="warn">no Paper Run at %s</span>' % esc(addr or "this row"), marks))
    url = _tree_url(d, pdf) if pdf else ""
    acts = [('<a href="%s" target="_blank" rel="noopener">Open the PDF in a new tab ↗</a>' % esc(url)) if url else "",
            ('<a href="%s" target="_blank" rel="noopener">Publisher page ↗</a>' % esc(m["publisher"])) if m.get("publisher") else "",
            _file_link(d, m["card"], "Paper Run ↗") if m.get("card") is not None and m["card"].is_file() else ""]
    acts += ['<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (esc(_tree_url(d, x)), esc(x.stem.replace("-", " ").capitalize()))
             for x in m.get("more_pdfs", [])]
    # why OUR paper keeps this one (JL 261002): the P-board's `keep` cell, else its `why it matters`;
    # `bears on` marks each of our questions it supports, limits or contradicts
    keep, why = _cell(heads, row, "keep"), _cell(heads, row, "why")
    body = [('<div class="rp-keep"><div class="rp-keep-h">Why we keep it</div><p>%s</p>%s</div>'
             % (esc(keep), _bears(_cell(heads, row, "bears"))) if keep else
             ('<p class="rp-why">%s</p>%s' % (esc(why), _bears(_cell(heads, row, "bears")))) if why else _bears(_cell(heads, row, "bears"))),
            _lw_table(m.get("lw") or {}),
            '<div class="rp-acts">%s</div>' % "".join('<span>%s</span>' % a for a in acts if a)]
    if m.get("abstract"):
        body.append('<details class="rp-absd"><summary>Abstract</summary><p>%s</p></details>' % esc(m["abstract"]))
    body.append('<iframe class="rp-frame" title="%s" data-pdf="%s"></iframe>' % (esc("PDF · " + title), esc(url)) if url else
                ('<div class="rp-nopdf mut">No free full text of the article. The open files are linked above.</div>' if m.get("more_pdfs") else
                 '<div class="rp-nopdf mut">No free full text. Read it on the publisher page; it may need a subscription.</div>'))
    return ('<details class="rp-card" data-key="%s">%s<div class="rp-body">%s</div></details>'
            % (esc(pid), summary, "".join(body)), bool(pdf), m.get("venue", ""))


def _role_bands(cards):
    """[(role, card)] → the role bands in their fixed order, each a count and one box of rows."""
    groups = {k: [c for r, c in cards if r == k] for k, _, _ in RELATED_ROLES}
    return "".join('<div class="lw-k lw-k-%s">%s<span class="lw-kn">%d</span></div><div class="rp-group">%s</div>'
                   % (cls, esc(label), len(groups[k]), "".join(groups[k])) for k, label, cls in RELATED_ROLES if groups[k])


def related_html(d):
    """Story › Related Papers: the §5.3 P-board. The target venue's papers come first and
    other venues follow (JL 260930: "this is not limited to NMI"); inside each, the
    papers are grouped by the role they play."""
    rows = [(s, r) for s in current_stories(d) for r in s["pp"]]
    if not rows:
        return '<div class="space-empty">No related paper yet.</div>'
    venue, n_pdf, roles = venue_name(d), 0, {k for k, _, _ in RELATED_ROLES}
    here, away = [], []
    for s, r in rows:
        role = (_cell(s["pp_h"], r, "role").split() or ["background"])[0].lower()
        card, has, where = _paper_card(d, s, r)
        n_pdf += has
        at_venue = not venue or where.lower().startswith(venue.lower())
        (here if at_venue else away).append((role if role in roles else "background", card))
    head = '<div class="rp-head">%d paper%s · %d with a PDF</div>' % (len(rows), "" if len(rows) == 1 else "s", n_pdf)
    if not venue:
        return '<div class="rp-list">%s%s</div>' % (head, _role_bands(here))
    parts = [('<h3 class="rp-venue">At %s<span class="lw-kn">%d</span></h3>%s' % (esc(venue), len(here), _role_bands(here))) if here else "",
             ('<h3 class="rp-venue">Other venues<span class="lw-kn">%d</span></h3>%s' % (len(away), _role_bands(away))) if away else ""]
    return '<div class="rp-list">%s%s</div>' % (head, "".join(parts))


def related_by_question_html(d, questions):
    """Block › Audience Report › Related Papers (JL 261009: "a Related Paper after the Related Questions"): the
    same cards as Description › Related, under the research question each bears on, with no venue order (b16
    s05: the Board is venue-free). `questions` is the Board's register as [(id, title)]; a row's `RQ3` is Q03,
    and `all` (or no question) is the whole paper, shown first. Inside a question the closest come first."""
    rows = [(s, r) for s in current_stories(d) for r in s["pp"]]
    if not rows:
        return '<div class="space-empty">No related paper yet.</div>'
    rank = {k: i for i, (k, _, _) in enumerate(RELATED_ROLES)}
    role = lambda s, r: (_cell(s["pp_h"], r, "role").split() or ["background"])[0].lower()
    groups, n_pdf = {}, 0
    for s, r in sorted(rows, key=lambda x: rank.get(role(*x), len(rank))):
        card, has, _ = _paper_card(d, s, r)
        n_pdf += has
        ids = ["Q%02d" % int(n) for n in re.findall(r"(?i)\bR?Q(\d+)\b", _cell(s["pp_h"], r, "question"))]
        for k in ids or ["all"]:
            groups.setdefault(k, []).append(card)
    titles = dict(questions)
    keys = ["all"] + list(titles) + sorted(k for k in groups if k != "all" and k not in titles)
    head = '<div class="rp-head">%d paper%s · %d with a PDF · by the question each bears on</div>' % (
        len(rows), "" if len(rows) == 1 else "s", n_pdf)
    parts = ['<h3 class="rp-venue">%s<span class="lw-kn">%d</span></h3><div class="rp-group">%s</div>'
             % (esc("The whole paper" if k == "all" else "%s · %s" % (k, titles[k]) if titles.get(k) else k),
                len(groups[k]), "".join(groups[k])) for k in keys if k in groups]
    none = [k for k in titles if k not in groups]
    tail = ('<p class="mut">No related paper yet for %s.</p>' % esc(" · ".join(none))) if none else ""
    return '<div class="rp-list">%s%s%s</div>' % (head, "".join(parts), tail)


def roadmap_html(d):
    """Story › RoadMap Draw (JL 260930, JL's name: "a view … to show the excalidraw draw
    which will be saved here: studio"): the paper's Excalidraw canvas, editable, on a
    drawing in `<paper>/studio/`. It opens `<Story stem>.excalidraw` (the Story board.md
    `story-current:` names) when that exists, else the first drawing there; with none, the
    Story's own, which the server writes empty the first time the canvas opens
    (`mint_board_scene`). Every other drawing in `studio/` is one click away."""
    stems = [s["stem"] for s in d["story"]]
    cur = scalar(read(d["board"] / "board.md"), "story-current").strip()
    stem = cur if cur in stems else next((x for x in stems if re.match(r"^Story[A-Z]", x)), stems[0] if stems else "")
    if not stem:
        return '<div class="space-empty">No Story yet.</div>'
    studio = Path(d["board"]) / "studio"
    own = studio / (stem + ".excalidraw")
    files = sorted(studio.glob("*.excalidraw"), key=lambda f: (f.name != own.name, f.name)) if studio.is_dir() else []
    files = files or [own]

    def generated(f):
        """A drawing a script writes (its `source` names the script, as hai-draw draft's paper
        map does) opens view only: it is redrawn from its files, never edited (JL 261003)."""
        try:
            return str(json.loads(f.read_text(encoding="utf-8")).get("source", "")).endswith(".py")
        except (OSError, ValueError, AttributeError):
            return False
    urls = [(f, "/_excalidraw/?board=%s%s" % (quote(_tree_url(d, f).lstrip("/"), safe="/"),
                                              "" if generated(f) else "&edit=1")) for f in files]
    chips = "".join('<button type=button class="rd-file%s" data-src="%s">%s</button>'
                    % (" on" if i == 0 else "", esc(u), esc(f.stem + (" · generated" if generated(f) else "")))
                    for i, (f, u) in enumerate(urls)) if len(urls) > 1 else ""
    return ('<div class="rd-bar">%s<a class="rd-open" href="%s" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer, as the Draw panel does: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            '<iframe class="rd-frame" title="RoadMap Draw" referrerpolicy="no-referrer" data-src="%s"></iframe>'
            % (chips, esc(urls[0][1]), esc(urls[0][1])))
