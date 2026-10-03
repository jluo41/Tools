"""Related Paper, shared by every workbench (skills/0_utils/table-papers).

A workbench keeps its papers in one table beside its skill,
`skills/<family>/haipipe-workbench-<name>/ref/<name>-papers.md`, eight columns:
group · role · key · paper · venue · doi · why here · pdf. `papers_page` shows that table
as the Paper workbench shows a Story's Related Papers: one band per group, the key
papers (★) first and the rest folded; closed, a card is the title, then who · year ·
journal; open, why it is here, its links, the abstract and the PDF. Moved here from the
Design workbench (JL 261003: "this is the rule and should be shared"); Design, Insight
and Guide › Related Paper all render through it. Read-only: it writes nothing.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


def _e(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _read(path: Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


# A papers table's roles (skills/0_utils/table-papers): `practice` is a guideline,
# documentation or engineering article rather than a peer-reviewed study.
PAPER_ROLES = ("classic", "review", "evidence", "practice")
# The UT Dallas list of 24 leading business journals (JL 261002: "is there a paper from
# the UTD24 list?"): a card in one of them carries the mark, and the head counts them.
UTD24 = ("the accounting review", "journal of accounting and economics", "journal of accounting research",
         "journal of finance", "journal of financial economics", "review of financial studies",
         "information systems research", "informs journal on computing", "mis quarterly",
         "journal of consumer research", "journal of marketing", "journal of marketing research", "marketing science",
         "management science", "operations research", "journal of operations management",
         "manufacturing & service operations management", "production and operations management",
         "academy of management journal", "academy of management review", "administrative science quarterly",
         "organization science", "journal of international business studies", "strategic management journal")


def is_utd24(venue: str) -> bool:
    name = re.sub(r"^the\s+", "", (venue or "").strip().lower())
    return name in {re.sub(r"^the\s+", "", v) for v in UTD24}


def paper_rows(table: Path) -> list[dict]:
    """The papers table: one dict per row, keyed by the header words."""
    rows, head = [], []
    for line in _read(Path(table)).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not head:
            head = [c.lower() for c in cells]
        elif not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
    return rows


def _href(root: Path, path: Path) -> str:
    """A plain server path for a file under the SPACE root, or reached through a folder
    linked in under it (`Tools` -> `../Tools-SPACE`); '' when it is neither."""
    root, path = Path(root), Path(path).resolve()
    try:
        return "/" + path.relative_to(root.resolve()).as_posix()
    except ValueError:
        pass
    for link in (c for c in root.iterdir() if c.is_symlink()):
        try:
            return "/" + (Path(link.name) / path.relative_to(link.resolve())).as_posix()
        except ValueError:
            continue
    return ""


def paper_runs(board: Path) -> dict[str, Path]:
    """DOI -> the Discovery Paper Run that holds it in the board's Project (its Bib, its
    abstract and, when a free copy exists, paper.pdf), so a card can read it."""
    out: dict[str, Path] = {}
    if board is None:
        return out
    for rt in sorted(Path(board).parent.parent.glob("discoveries/b*/j*/t*/results/r*/runtime.yaml")):
        doi = re.search(r'(?m)^\s+doi:\s*"?([^"\s]+)"?\s*$', _read(rt))
        if doi:
            out.setdefault(doi.group(1).lower(), rt.parent)
    return out


def _run_abstract(run: Path) -> str:
    """The retrieved abstract, without its heading and source line."""
    return " ".join(ln.strip() for ln in _read(run / "abstract.md").splitlines()
                    if ln.strip() and not ln.lstrip().startswith(("#", "Source:", ">")))


def _paper_pdf(row: dict, table: Path, run: Path | None) -> Path | None:
    """The paper's full text: its copy beside the table, else its Paper Run's free copy."""
    kept = Path(table).parent / row["pdf"] if row.get("pdf") else None
    if kept is not None and kept.is_file():
        return kept
    return run / "paper.pdf" if run is not None and (run / "paper.pdf").is_file() else None


def _paper_card(root: Path, row: dict, table: Path, run: Path | None) -> str:
    who_year, _, title = row.get("paper", "").partition(" · ")
    year = (re.search(r"(\d{4})\s*$", who_year) or re.search(r"(\d{4})", who_year))
    names = (who_year[:year.start()] if year else who_year).strip(" :")
    # one author by name, two as `A & B`, three or more as `A et al.`, as a citation says them
    first = names if "," not in names else names.split(",")[0].strip() + " et al."
    who = " · ".join(x for x in (first, year.group(1) if year else "", row.get("venue", "")) if x)
    role = row.get("role", "").lower()
    # the doi cell holds a DOI, or the page of a work that has none (an article, a guide)
    page = row.get("doi", "") if row.get("doi", "").startswith(("https://", "http://")) else ""
    doi = "" if page else row.get("doi", "")
    pdf = _paper_pdf(row, table, run)
    card = run / f"{run.name}.md" if run is not None else None
    pdf_url = _href(root, pdf) if pdf is not None else ""
    acts = [f'<a href="{_e(pdf_url)}" target="_blank" rel="noopener">Open the PDF in a new tab ↗</a>' if pdf_url else "",
            f'<a href="https://doi.org/{_e(doi)}" target="_blank" rel="noopener">Publisher page ↗</a>' if doi else "",
            f'<a href="{_e(page)}" target="_blank" rel="noopener">Source page ↗</a>' if page else "",
            f'<a href="{_e(_href(root, card))}" target="_blank" rel="noopener">Paper Run ↗</a>'
            if card is not None and card.is_file() and _href(root, card) else ""]
    abstract = _run_abstract(run) if run is not None else ""
    if pdf_url:
        tail = f'<iframe class="rp-frame" title="{_e("PDF · " + (title or row.get("paper", "")))}" data-pdf="{_e(pdf_url)}"></iframe>'
    elif doi:
        tail = '<div class="rp-nopdf mut">No free full text here. Read it on the publisher page; it may need a subscription.</div>'
    elif page:
        tail = '<div class="rp-nopdf mut">Read it on its source page.</div>'
    else:
        tail = '<div class="rp-nopdf mut">A book or report with no DOI: read it in print or on its publisher\'s page.</div>'
    return (f'<details class="rp-card{" has-pdf" if pdf_url else ""}" id="{paper_id(row)}"><summary><span class="bjt-chev">▸</span><div class="lw-sum">'
            f'<div class="rp-title">{_e(title or row.get("paper", ""))}</div>'
            f'<div class="rp-sub"><span>{_e(who)}</span><span class="rp-marks">'
            + ('<span class=rp-pdf title="the PDF opens inside this card">PDF</span>' if pdf_url else "")
            + ('<span class=rp-utd title="on the UTD24 journal list">UTD24</span>' if is_utd24(row.get("venue", "")) else "")
            + f'<span class="rp-q rp-{_e(role)}">{_e(role)}</span></span></div>'
            '</div></summary><div class="rp-body">'
            + (f'<p class="rp-why">{_e(row.get("why here", ""))}</p>' if row.get("why here") else "")
            + '<div class="rp-acts">' + "".join(f"<span>{a}</span>" for a in acts if a) + '</div>'
            + (f'<details class="rp-absd"><summary>Abstract</summary><p>{_e(abstract)}</p></details>' if abstract else "")
            + f'{tail}</div></details>')


def papers_page(board: Path | None, root: Path, table: Path) -> str:
    """A workbench's Related Paper view: one band per group, in the file's order, each a count
    and one box of cards; the journals they come from are named above the bands. `board`
    lends the Discovery Paper Runs of its Project (abstracts, free copies); None reads none."""
    rows = paper_rows(table)
    if not rows:
        return (f'<div class=empty>No related paper yet: this workbench keeps them in '
                f'<code>ref/{_e(Path(table).name)}</code> (group · role · key · paper · venue · doi · why here · pdf).</div>')
    groups: dict[str, list[dict]] = {}
    for row in rows:
        # a paper may serve two methods (`by a; by b`): it shows once, in its first group
        groups.setdefault(row.get("group", "").split(";")[0].strip() or "other", []).append(row)
    # the three study roles are always counted, as they always were; `practice` only when present
    roles = " · ".join(f"{n} {k}" for k in PAPER_ROLES
                       if (n := sum(r.get('role', '').lower() == k for r in rows)) or k != "practice")
    index = paper_runs(board)
    run_of = {id(r): index.get(r.get("doi", "").lower()) for r in rows}
    pdfs = sum(_paper_pdf(r, table, run_of[id(r)]) is not None for r in rows)
    venues: dict[str, int] = {}
    for row in rows:
        venues[row.get("venue", "") or "—"] = venues.get(row.get("venue", "") or "—", 0) + 1
    utd = sum(is_utd24(r.get("venue", "")) for r in rows)
    keys = sum(bool(r.get("key")) for r in rows)
    head = (f'<div class="rp-head">{len(rows)} papers · {keys} key · {roles} · {utd} in UTD24 journals · {pdfs} with a PDF</div>'
            + (f'<div class=rp-tools><button type=button class=rp-only aria-pressed=false>Show only the {pdfs} papers with a PDF</button></div>'
               if pdfs else "")
            + f'<details class=rp-venues><summary>{len(venues)} journals and publishers</summary><div class=mut>'
            + " · ".join(f"{_e(v)} ({n})" for v, n in sorted(venues.items(), key=lambda kv: (-kv[1], kv[0])))
            + '</div></details>')
    card = lambda r: _paper_card(root, r, table, run_of[id(r)])
    # each band shows its key papers (★ in `key`) and folds the rest (JL 261002: "collapse the
    # less important papers"); a band with no key paper shows all of its papers
    def band(group: str, rs: list[dict]) -> str:
        top = [r for r in rs if r.get("key")] or rs
        rest = [r for r in rs if r not in top]
        cards = [card(r) for r in top], [card(r) for r in rest]
        has = any("rp-card has-pdf" in c for c in cards[0] + cards[1])
        more = (f'<details class=rp-more><summary>{len(rest)} more paper{"s" if len(rest) != 1 else ""}</summary>'
                f'<div class="rp-group">{"".join(cards[1])}</div></details>' if rest else "")
        return (f'<section class="rp-band{" has-pdf" if has else ""}">'
                f'<div class="lw-k">{_e(group[:1].upper() + group[1:])}<span class="lw-kn">{len(rs)}</span></div>'
                f'<div class="rp-group">{"".join(cards[0])}</div>{more}</section>')
    bands = "".join(band(g, rs) for g, rs in groups.items())
    return f'<div class="rp-list">{head}{bands}</div>'


def paper_id(row: dict) -> str:
    """A paper card's anchor: its DOI, else its citation, as `paper-<slug>`."""
    return "paper-" + re.sub(r"[^a-z0-9]+", "-", (row.get("doi") or row.get("paper", "")).lower()).strip("-")[:80]


def short_cite(row: dict) -> str:
    """`Dow, Glassco, Kass et al. 2010 · …` -> `Dow et al. 2010`; `A & B 2001` stays."""
    who_year = row.get("paper", "").partition(" · ")[0]
    year = re.search(r"(\d{4})\s*$", who_year) or re.search(r"(\d{4})", who_year)
    names = (who_year[:year.start()] if year else who_year).strip(" :")
    names = names.split(",")[0].strip() + " et al." if "," in names else names
    return f"{names} {year.group(1)}" if year else names


# The cards' look, for a page that does not carry it already. It reads the host page's
# --line, --mut, --acc, --soft, --fg and --ok colors.
PAPERS_CSS = """
.rp-head{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}
details.rp-venues{margin:0 0 10px}details.rp-more{margin:2px 0 4px}details.rp-more>summary{font-size:12.5px;color:var(--mut);padding:2px 0}details.rp-more[open]>summary{margin-bottom:4px}details.rp-venues>div{margin-top:4px;line-height:1.6}
.lw-k{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--acc);margin:14px 0 6px}.lw-kn{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85;margin-left:6px}
.rp-group{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 4px}
.rp-card+.rp-card{border-top:1px solid var(--line)}
.rp-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}
.rp-card>summary::-webkit-details-marker{display:none}.rp-card>summary:hover,.rp-card[open]>summary{background:var(--soft)}
.bjt-chev{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}.rp-card[open]>summary .bjt-chev{transform:rotate(90deg)}
.lw-sum{min-width:0}.rp-title{font-weight:600;font-size:14.5px;line-height:1.4;color:var(--fg)}
.rp-sub{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}
.rp-marks{display:flex;gap:10px;flex:none}.rp-utd{font:700 10.5px -apple-system,sans-serif;color:#9c6500;border:1px solid #e3c27a;border-radius:4px;padding:0 4px;letter-spacing:.03em}.rp-q{color:var(--acc);font-weight:600}.rp-q.rp-evidence{color:var(--ok)}.rp-q.rp-classic{color:var(--mut)}
.rp-body{padding:6px 14px 14px calc(14px + 1em + 6px)}.rp-why{font-size:14.5px;line-height:1.55;margin:4px 0 6px}
.rp-acts{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}.rp-nopdf{font-size:13.5px;margin-top:8px}
details.rp-absd>summary{font-size:13px;color:var(--mut);cursor:pointer}details.rp-absd>p{font-size:13.5px;line-height:1.55;margin:4px 0 6px}
.rp-frame{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}
.rp-pdf{font:700 10.5px -apple-system,sans-serif;color:#fff;background:var(--acc);border-radius:4px;padding:1px 5px;letter-spacing:.03em}
.rp-tools{margin:2px 0 8px}.rp-only{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:14px;padding:3px 11px;cursor:pointer}
.rp-only[aria-pressed=true]{background:var(--acc);color:#fff}
.rp-list.only-pdf .rp-card:not(.has-pdf),.rp-list.only-pdf .rp-band:not(.has-pdf),.rp-list.only-pdf details.rp-more>summary{display:none}
"""

# A card's PDF loads only when the card opens; "Show only the papers with a PDF" hides the
# rest and opens the folds so every PDF card shows.
PAPERS_JS = (
    "document.addEventListener('toggle',function(ev){var w=ev.target;if(!(w.matches&&w.matches('details.rp-card')))return;"
    "var f=w.open&&w.querySelector('iframe[data-pdf]');if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf)},true);"
    "document.querySelectorAll('.rp-only').forEach(function(b){b.onclick=function(){var l=b.closest('.rp-list'),"
    "on=!l.classList.contains('only-pdf');l.classList.toggle('only-pdf',on);b.setAttribute('aria-pressed',on);"
    "if(on)l.querySelectorAll('details.rp-more').forEach(function(d){d.open=true})}});"
)
