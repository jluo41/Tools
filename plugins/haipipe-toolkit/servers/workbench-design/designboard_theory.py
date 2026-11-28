"""The theory of design: its files, the ASCII doc renderer, the methods studio, Related papers and the method
cards (split from designboard.py, which re-exports every name here; theory_page stays there, since the
tests set designboard.PAPERS and designboard.STUDIO)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live.design import _escape as _e, _read


# Guide › Method is one document: the six steps, then steps 2, 3, 4 and 6 in depth,
# why it works, and the reference, folded. The older
# view keys (design-theory, methods) read the same file.
METHODS = Path(__file__).resolve().parent / "guide" / "method.md"        # the theme's Guide (261007)
THEORY = METHODS
# The methods studio: one Excalidraw drawing of the loop, the families and the ten cards,
# opened in the self-hosted canvas and saved back to this file.
# The design theme's drawings live in its Block's topics, like any Block's: each sNN beside its Jobs
#, else in the Block's older studio/.
B12 = Path(__file__).resolve().parents[4] / "examples" / "Project-Ladder" / "blueprint" / "b12_theme_design"
B12_METHODS = next((p for p in (B12 / "s03-design-methods", B12 / "_archive" / "20261127" / "s03-design-methods",
                                B12 / "studio" / "s03-design-methods") if p.is_dir()),
                   B12 / "_archive" / "20261127" / "s03-design-methods")
STUDIO = B12_METHODS / "parts" / "design-methods.excalidraw"
# The design unit: See input → Conduct process → Check output, each step's parts with their options above,
# and one row per method below, its choice in every part.
# Written by Tools/examples/Project-Ladder/blueprint/b12_theme_design/_archive/20261127/s03-design-methods/design_unit_drawing.py.
UNIT = B12_METHODS / "parts" / "design-unit-methods.excalidraw"


def _pipe_rows(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """A pipe table's header words (lower case) and its body rows."""
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    body = [r for r in cells[1:] if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return [c.lower() for c in cells[0]], body


def _plain_md(text: str, table=None) -> str:
    """The ASCII doc style (underlined titles, paragraphs, `- ` lists, fenced blocks, pipe
    tables) as HTML. `table(head, rows)` may render a table it knows; None falls back."""
    out, para, items, lines = [], [], [], text.splitlines()

    def inline(t: str) -> str:
        t = _e(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        # a web link, [text](https://...), opens in a new tab (the people's wiki pages)
        t = re.sub(r"\[([^\]]+)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)",   # a DOI may hold (05)
                   r'<a href="\2" target=_blank rel=noopener>\1</a>', t)
        return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)

    def flush():
        if para:
            out.append(f'<p>{inline(" ".join(para))}</p>')
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre class=theory>" + _e("\n".join(lines[i + 1:j])) + "</pre>")
            i = j + 1
            continue
        if line.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            head, rows = _pipe_rows(lines[i:j])
            html_table = table(head, rows) if table else None
            out.append(html_table or (
                "<table class=mdt><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"))
            i = j
            continue
        if line.strip() and re.fullmatch(r"=+|-+|~+", nxt.strip()) and len(nxt.strip()) >= 3:
            flush()
            tag = {"=": "h1", "-": "h2", "~": "h3"}[nxt.strip()[0]]       # ~~~ under a title: a sub-section
            out.append(f'<{tag}>{inline(line.strip())}</{tag}>')
            i += 2
            continue
        if line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        elif items and not para and line.startswith("  ") and line.strip():
            items[-1] += " " + line.strip()          # a list item that wraps goes on, indented
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "".join(out)


# The Theory of Design Space has three views, all of them general: how to
# design, the methods a design can be made by, and the papers behind both. Knowledge of
# one channel (message theories for SMS) is not design theory and is not shown here.
THEORY_VIEWS = (("design-theory", "Design theory"), ("methods", "Design methods"), ("studio", "Methods studio"),
                ("papers", "Papers"), ("method", "Method"))
# `method` is Guide › Method's one page (the design theory lives there;
# no view named Design methods): the theory, its sections 1 to 9, then the method cards,
# 10 to 12, then the methods drawing. The other keys stay for old links and for Insight.


def studio_html(root: Path, drawing: Path = STUDIO, note: str = "") -> str:
    """Theory › Methods studio: the methods drawing in the Excalidraw canvas, editable, as
    the Paper workbench's RoadMap Draw shows a Story's drawing. It loads only when shown."""
    rel = _href(root, drawing) if Path(drawing).is_file() else ""
    if not rel:
        return '<div class=empty>No methods drawing yet: the design workbench keeps it as <code>b12_theme_design/_archive/20261127/s03-design-methods/parts/design-methods.excalidraw</code>.</div>'
    url = "/_excalidraw/?board=" + quote(rel.lstrip("/"), safe="/") + "&edit=1"
    note = note or ('The four kinds of reasoning, three inputs, Design and the Exp, the Revise and Learning loops, '
                    'three families, the cards and the tests.')
    return (f'<div class=st-bar><span class=mut>{_e(note)} Edits save to <code>{_e(Path(drawing).name)}</code>.</span>'
            f'<a href="{_e(url)}" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            f'<iframe class=st-frame title="Methods studio" referrerpolicy="no-referrer" data-src="{_e(url)}"></iframe>')


# Theory › Papers: the papers behind the theory, one card each. The rows are the
# workbench's own `related/papers.md`, the same for every board. The table's shape and check are the shared
# rule skills/0_utils/table-papers; its renderer is the shared live.related_papers
# (one rule for every board), imported here under the names it always had.
from .related_papers import (PAPER_ROLES, UTD24, _href, _paper_card, _paper_pdf, _run_abstract,  # noqa: E402,F401
                             is_utd24, paper_id, paper_rows, paper_runs, short_cite)
from .related_papers import papers_page as _papers_page  # noqa: E402

PAPERS = Path(__file__).resolve().parent / "related" / "papers.md"


def papers_page(board: Path, root: Path, table: Path = PAPERS) -> str:
    """Theory › Papers, through the shared Related Paper renderer."""
    return _papers_page(board, root, table)


def method_card_fields(path: Path) -> dict:
    """One method card file: its name, then the `key: value` fields of its head and of its
    two parts, What the literature says (`lit`) and Applied to AI (`ai`). A value may wrap
    onto indented lines."""
    lines = _read(path).splitlines()
    out = {"name": lines[0].strip() if lines else Path(path).stem, "head": {}, "lit": {}, "ai": {}}
    part, key = "head", None
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.strip() and re.fullmatch(r"-{3,}", nxt.strip()):
            part, key = ("ai" if line.strip().lower().startswith("applied") else "lit"), None
            continue
        m = re.match(r"^([A-Za-z][A-Za-z ]*):\s+(.*)$", line)
        if m and m.group(1).lower() in CARD_KEYS:
            key = m.group(1).lower()
            out[part][key] = m.group(2).strip()
        elif key and line.startswith("  ") and line.strip():
            out[part][key] += " " + line.strip()
        elif not line.strip():
            key = None
    return out


CARD_KEYS = {"family", "also", "reasoning", "move", "status", "taxonomy", "comes from", "reads", "returns", "test now", "test in use", "rationale", "context",
             "steps", "strengths", "limitations", "agent", "verify", "risk", "evidence on ai", "skill"}
LIT_FIELDS = (("rationale", "Rationale"), ("context", "Context"), ("steps", "Steps"),
              ("strengths", "Strengths"), ("limitations", "Limitations"))
AI_FIELDS = (("agent", "The agent"), ("steps", "Steps"), ("returns", "Returns"), ("verify", "Verify"),
             ("risk", "AI risk"), ("evidence on ai", "Evidence on AI"), ("skill", "Skill"))


def method_cards(board: Path, root: Path, doc_path: Path, table: Path = PAPERS, in_use: str = "in use", now: str = "now"):
    """The Design methods view's renderer for its card index.
    The index table names one card file per method. Closed, a card is the method's name,
    whether any study tests it, its move, what it reads and returns, and where it comes
    from. Open, What the literature says (as O'Cathain et al. 2019 describe approaches)
    stands beside Applied to AI, and the method's papers close it. Every paper links to
    its card in the Papers view, PDF and all. What a card reads is coloured by input: design requirements, internal insights, external insights; `now` and
    `in_use` name where the two kinds of test happen ("in Evaluate", the Revise loop, and
    "in the Exp", the Learning loop, for design methods)."""
    doc_path = Path(doc_path)
    doc = _read(doc_path)
    papers = paper_rows(table)
    index = paper_runs(board)
    by_group: dict[str, list[dict]] = {}
    for r in papers:
        for g in r.get("group", "").lower().split(";"):       # and counts on every card it serves
            by_group.setdefault(g.strip(), []).append(r)
    tests = {}
    for line in doc.splitlines():                       # T0 … T4 and what each asks, for the badges
        m = re.match(r"^\|\s*(T\d)\s+([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            tests[m.group(1)] = f"{m.group(1)} {m.group(2)}: {m.group(3)}"

    def chip(r: dict) -> str:
        has = _paper_pdf(r, table, index.get(r.get("doi", "").lower())) is not None
        return (f'<a class="pchip to-paper" href="#{paper_id(r)}" title="{_e(r.get("paper", ""))}">{_e(short_cite(r))}'
                + ('<span class=rp-pdf>PDF</span>' if has else "") + '</a>')

    def find(cite: str) -> dict | None:
        """The papers-table row a citation names: the same first author and year, if only one."""
        first_word = lambda t: t.replace(",", " ").split()[0].lower() if t.strip() else ""
        year = re.search(r"\b\d{4}\b", cite)
        hits = [p for p in papers if first_word(p.get("paper", "")) == first_word(cite)
                and (year is None or re.search(rf"\b{year.group(0)}\b", p.get("paper", "").partition(" · ")[0]))]
        if len(hits) > 1:                   # `O'Cathain 2019 taxonomy`: a title word picks one of two
            rest = [w for w in re.findall(r"[a-z]{4,}", cite.lower()) if w not in first_word(cite)]
            hits = [p for p in hits if all(w in p.get("paper", "").partition(" · ")[2].lower() for w in rest)] if rest else hits
        return hits[0] if len(hits) == 1 else None

    def cited(entry: str) -> str:
        """`Newell & Simon 1972, generate and test` -> the paper's link, then the idea it gives;
        an unmatched source stays text."""
        cite, _, idea = entry.strip().partition(", ")
        hit = find(cite)
        head = chip(hit) if hit else f'<span class=chip>{_e(cite)}</span>'
        return f'<span class=src>{head}{(" " + _e(idea)) if idea else ""}</span>'

    def prose(text: str) -> str:
        """A cell's text with each `[Author Year]` linked to its paper card, `(ours)` muted
        and test codes badged."""
        def link(m):
            parts = []
            for c in m.group(1).split(";"):
                hit = find(c.strip())
                has = hit is not None and _paper_pdf(hit, table, index.get(hit.get("doi", "").lower())) is not None
                parts.append(f'<a class="cite to-paper" href="#{paper_id(hit)}" title="{_e(hit.get("paper", ""))}">{_e(c.strip())}'
                             + ('<span class=rp-pdf>PDF</span>' if has else "") + '</a>' if hit else _e(c.strip()))
            return "[" + "; ".join(parts) + "]"
        links: list[str] = []

        def stash(m):                       # set each linked citation aside while the text is escaped
            links.append(link(m))
            return f"\x00{len(links) - 1}\x00"
        out = _e(re.sub(r"\[([^\]]+)\]", stash, text))
        out = re.sub(r"\bT\d\b", lambda m: f'<span class=tcode title="{_e(tests.get(m.group(0), ""))}">{m.group(0)}</span>', out)
        out = out.replace("(ours)", '<span class=ours title="this workbench\'s own judgment">(ours)</span>')
        return re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], out)

    def lines(text: str, steps: bool = False) -> str:
        """Steps one per line (`1. … 2. …`); otherwise one sentence per line."""
        numbered = steps and re.search(r"\b1\.\s", text)
        parts = re.split(r"\s(?=\d\.\s)", text) if numbered else re.split(r"(?<=\.)\s+(?=[A-Z])", text)
        return "".join(f"<div class=line>{prose(p)}</div>" for p in parts if p.strip())

    def ranked(rs: list[dict]) -> list[dict]:
        return sorted(rs, key=lambda r: (not r.get("key"), r.get("role", "").lower() != "evidence"))

    def tested(cell: str) -> str:
        return re.sub(r"\bT\d\b", lambda m: f'<span class=tcode title="{_e(tests.get(m.group(0), ""))}">{m.group(0)}</span>',
                      _e(cell))

    def card(n: int, f: dict) -> str:
        name, h, lit, ai = f["name"], f["head"], f["lit"], f["ai"]
        group = by_group.get(name.lower(), [])
        studies = sum(p.get("role", "").lower() == "evidence" for p in group)
        future = h.get("status", "").lower().startswith("future")
        status = (f'<span class="mc-status future" title="{_e(h["status"])}">future · not run yet</span>' if future else
                  f'<span class="mc-status ok">tested in {studies} stud{"y" if studies == 1 else "ies"}</span>' if studies
                  else '<span class="mc-status gap">no study tests it yet</span>')
        def kind(x: str) -> str:            # an input's chip is coloured by its kind; any other stays plain
            w = x.lower()
            return next((f'class="chip {c}"' for c, k in (("in-req", "design requirements"), ("in-int", "internal insights"),
                                                          ("in-ext", "external insights")) if w.startswith(k)), "class=chip")
        reads = "".join(f"<span {kind(x.strip())}>{_e(x.strip())}</span>" for x in h.get("reads", "").split("·") if x.strip())
        frm = '<span class=mut> · </span>'.join(cited(e) for e in h.get("comes from", "").split(";") if e.strip())
        skill, _, note = ai.get("skill", "").partition(" ")

        def dl(fields: tuple, part: dict) -> str:
            rows = []
            for key, label in fields:
                if key == "skill" and skill:
                    body = f'<code>{_e(skill)}</code>' + (f' <span class=mut>{_e(note)}</span>' if note else "")
                elif part.get(key):
                    body = lines(part[key], steps=key == "steps")
                else:
                    continue
                rows.append(f"<dt>{_e(label)}</dt><dd>{body}</dd>")
            return "<dl>" + "".join(rows) + "</dl>"
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        return (f'<details class="mcard{" future" if future else ""}" id="method-{slug}"><summary><span class="bjt-chev">▸</span><div class=mc-sum>'
                f'<div class=mc-top><span class=mnum>{n}</span><span class=mc-name>{_e(name)}</span>{status}</div>'
                f'<div class=mc-move>{_e(h.get("move", ""))}</div>'
                + (f'<div class=mc-from><span class=lbl>reasoning</span>{_e(h["reasoning"])}</div>' if h.get("reasoning") else "")
                +                 f'<div class=mc-io><span class=lbl>reads</span>{reads}<span class=arrow>→</span>'
                f'<span class=lbl>returns</span>{_e(h.get("returns", ""))}</div>'
                + (f'<div class=mc-from><span class=lbl>comes from</span>{frm}</div>' if frm else "")
                + (f'<div class=mc-from><span class=lbl>taxonomy</span>{prose(h["taxonomy"])}</div>' if h.get("taxonomy") else "")
                + '</div></summary><div class=mc-body><div class=mc-cols>'
                f'<div class=mc-col><div class=mc-h>What the literature says</div>{dl(LIT_FIELDS, lit)}</div>'
                f'<div class="mc-col ai"><div class=mc-h>Applied to AI</div>{dl(AI_FIELDS, ai)}</div></div>'
                f'<div class=mc-tests><span class=lbl>tested</span><span class=when>{_e(now)}</span> {tested(h.get("test now", ""))}'
                f'<span class=when>{_e(in_use)}</span> {tested(h.get("test in use", ""))}</div>'
                + (f'<div class=mc-papers><span class=lbl>papers</span>{"".join(chip(p) for p in ranked(group))}</div>' if group else "")
                + '</div></details>')

    def render(head: list[str], rows: list[list[str]]):
        if head != ["family", "method", "card"]:
            return None
        out, family = [], None
        for n, r in enumerate(rows, start=1):
            path = doc_path.parent / r[2] if len(r) > 2 else None
            if path is None or not path.is_file():
                out.append(f'<div class="mcard missing">{n} · {_e(r[1] if len(r) > 1 else "")}: no card at <code>{_e(r[2] if len(r) > 2 else "")}</code></div>')
                continue
            f = method_card_fields(path)
            label, _, gloss = f["head"].get("family", r[0]).partition(":")
            if label.strip() != family:
                family = label.strip()
                out.append(f'<div class=mc-fam><b>{_e(family)}</b>'
                           + (f' <span class=mut>· {_e(gloss.strip())}</span>' if gloss.strip() else "") + '</div>')
            out.append(card(n, f))
        return f'<div class=mcards>{"".join(out)}</div>'
    return render
