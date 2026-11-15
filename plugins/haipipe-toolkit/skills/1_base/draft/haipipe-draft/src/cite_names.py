"""Citations in name-year form for a reader's page (must-check M-D02): the web export (delivery/<job>/<task>/web/
index.html, page_workspace.render_page) prints `\\cite{wolff2018}` as "(Wolff et al. 2018)", its keys on hover. A key
with no entry in the Page's draft/evidence/bibex/*.bib, or an entry without author or year, shows the key and a visible
"not in Bib" mark. The LaTeX, PDF and Word lanes keep the keys and never read this.

The Draft Lab server keeps its own copy of the same reading: servers/workbench/workbench-task-draft/
draft_step_evidence.py `_bib_names` and `_cite_names` (no import either way); keep the two alike.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path

CITE = re.compile(r"\\cite(p|t|alp|author|year)?\*?\{([^}]*)\}")
_SKIP = re.compile(r"(?is)(<(code|pre|script|style|textarea)\b.*?</\2>|<[^>]*>)")


def bib_names(folder) -> dict:
    """{key: "Barnett et al. 2017"} from `folder`/draft/evidence/bibex/*.bib; an entry without author or year is left out."""
    out = {}
    bibdir = Path(folder) / "draft" / "evidence" / "bibex"
    for bib in sorted(bibdir.glob("*.bib")) if bibdir.is_dir() else []:
        text = bib.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", text, re.S):
            body = m.group(2)

            def get(k):
                x = re.search(r"\b" + k + r"\s*=\s*[{\"]((?:[^{}]|\{[^{}]*\})*)[}\"]", body, re.I)
                return re.sub(r"[{}]", "", x.group(1)).strip() if x else ""
            raw = re.search(r"\bauthor\s*=\s*\{\s*\{([^{}]+)\}\s*\}", body, re.I)
            names = [raw.group(1).strip()] if raw else [a.strip() for a in re.split(r"\s+and\s+", get("author")) if a.strip()]
            last = lambda a: a.split(",")[0].strip() if "," in a else a.split()[-1]
            who = ((names[0] if raw else last(names[0])) + (" et al." if len(names) > 2 else f" and {last(names[1])}"
                   if len(names) == 2 else "")) if names else ""
            year = (re.search(r"\d{4}", get("year")) or [""])[0]
            if who and year:
                # the reader sees "Medicare & Medicaid", not the bib's LaTeX escape "\&" (JL 261115, AITC t03)
                who = re.sub(r"\\([&%$#_])", r"\1", who)
                out.setdefault(m.group(1), f"{who} {year}")
    return out


def _miss(k: str) -> str:
    return (f'{escape(k)} <span class=cite-miss style="font-size:.8em;color:#c92a2a;border:1px solid #f1aeb5;'
            f'border-radius:4px;padding:0 3px" title="no entry for {escape(k)} in draft/evidence/bibex/*.bib">not in Bib</span>')


def cite_html(m: re.Match, names: dict) -> str:
    """One `\\cite…{keys}` as the reader sees it: (Name Year; …), or Name (Year) for \\citet."""
    kind, keys = m.group(1) or "", [k.strip() for k in m.group(2).split(",") if k.strip()]
    if not keys:
        return m.group(0)
    if kind == "t":
        parts = []
        for k in keys:
            who, _, year = names.get(k, "").rpartition(" ")
            parts.append(escape(f"{who} ({year})") if k in names else _miss(k))
        shown = "; ".join(parts)
    else:
        shown = "(" + "; ".join(escape(names[k]) if k in names else _miss(k) for k in keys) + ")"
    return f'<span class="cite cite-ay" title="{escape(", ".join(keys))}">{shown}</span>'


def name_year(html: str, folder) -> str:
    """`html` with every \\cite in its text (never inside a tag, code, pre, script or style) in name-year form."""
    if "\\cite" not in html:
        return html
    names = bib_names(folder)
    parts = _SKIP.split(html)
    out, i = [], 0
    # re.split with two groups yields: text, whole-match, inner-tag-name, text, …
    while i < len(parts):
        out.append(CITE.sub(lambda m: cite_html(m, names), parts[i]))
        if i + 1 < len(parts):
            out.append(parts[i + 1])
        i += 3
    return "".join(out)
