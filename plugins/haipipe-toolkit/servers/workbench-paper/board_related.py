"""A paper Board's Related section: the Board's related/related.md papers as side tabs, each PDF embedded."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import _file_url, esc, related_items, related_rows
from live.ui_parts import _cap, _plain, _section
from live.board_displays import _grouped_tabs


RELATED_CSS = ("<style>.pb-relhead{margin:0 0 4px;font-weight:600}.pb-relsaid{margin:0 0 8px;font-size:12.5px;color:var(--muted)}"
               ".pb-relpdf{display:block;width:100%;height:62vh;border:1px solid var(--line);border-radius:6px;background:var(--paper)}</style>"
               # a PDF loads only once its tab and section are on screen; the browser's loading=lazy fetched all 22 on page open
               "<script>document.addEventListener('DOMContentLoaded',function(){var o=new IntersectionObserver(function(es){es.forEach(function(e){"
               "if(e.isIntersecting){e.target.src=e.target.dataset.src;o.unobserve(e.target);}});});"
               "document.querySelectorAll('iframe.pb-relpdf[data-src]').forEach(function(f){o.observe(f);});});</script>")


ARXIV = re.compile(r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/([^\s?#]+?)(?:\.pdf)?$")


def _related_tab(item: dict, row: dict, board: Path, root: Path) -> tuple:
    """One related paper as a left tab and its right side: ((short name, author and venue), the panel). A kept PDF or an
    arXiv paper shows its PDF embedded, loaded only when its tab opens (JL 261104: "I want to embed the pdf here as
    well"), with Pop out beside it ("I want it can pop out and read"); arXiv's PDF may be framed though its abstract page
    may not. Any other web address links out, since a publisher's page refuses to be framed."""
    target, title = item["target"] or "", item["title"]
    star = "★ " if row.get("key") else ""
    who = re.search(r"\(([^()]*\d{4}[a-z]?)\)\s*$", title)
    bare = title[:who.start()].strip() if who else title
    tab = (star + bare.split(": ", 1)[0], " · ".join(x for x in (who[1] if who else "", _plain(row.get("venue", ""))) if x))
    said = _plain(row.get("why here", ""))
    head = f'<p class=pb-relhead>{esc(star + title)}</p>' + (f'<p class=pb-relsaid>{esc(said)}</p>' if said else "")
    path = board / "related" / target if target else None
    arxiv = ARXIV.match(target)
    url = f"https://arxiv.org/pdf/{arxiv[1]}" if arxiv else (_file_url(path, root) if path is not None and not re.match(r"https?://", target) and path.is_file() else "")
    if url:
        pop = f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(title)}" href="{esc(url)}" target=_blank rel=noopener>Pop out</a></div>'
        if arxiv or path.suffix.lower() == ".pdf":
            return tab, head + pop + f'<iframe class=pb-relpdf title="{esc(title)}" data-src="{esc(url)}"></iframe>'
        return tab, head + pop
    if re.match(r"https?://", target):
        return tab, head + f'<p class=pb-state>No PDF to show here: this site opens only in its own tab.</p><div class=pb-verbs><a class=fd-btn href="{esc(target)}" target=_blank rel=noopener>Open the paper ↗</a></div>'
    return tab, head + '<p class=pb-state>No PDF or link yet.</p>'


def related_section(board: Path, root: Path, n: int) -> tuple:
    """Story, the Board's related/related.md rows (JL 261104: "could you put the related section to be here?").
    Left tabs, one per paper, under a small name per `bears on`; the open paper's PDF on the right (JL 261104: "please
    change all type of these into this style"). Returns (html, the last section number)."""
    items = related_items(board)
    if not items:
        return "", n
    rows = related_rows(board)[1]
    groups = {}
    for item in items:
        row = rows[item["row"]] if item["row"] is not None else {}
        bears = _plain(row.get("bears on", "")) or ("Not in the table yet" if item["row"] is None else (item["groups"] or ["Other"])[0].capitalize())
        groups.setdefault(bears, []).append(_related_tab(item, row, board, root))
    return _section(f"{n + 1} · 📚 Related", RELATED_CSS + _grouped_tabs("rl", [(_cap(bears), tab, body) for bears, papers in groups.items() for tab, body in papers])), n + 1
