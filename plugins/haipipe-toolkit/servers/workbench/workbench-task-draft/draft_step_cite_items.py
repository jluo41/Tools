"""A Section's CITE evidence items as citation cards beside their sentences in 5 · Revise (must-check M-D18, M-D20).

The items live in draft/<stem>-evidence-items.md (`### E<nn>-CITE-<slug>`, its Label or its BibTeX naming the key).
A Section whose evidence/cards.yaml holds no card for an item still gets its ❝ card, drawn from what exists:

1. its Local Run, when bound (`Page · Evidence Item · reuse · P.j03.t01.r01 → <result>`, written by
   `cite_tasks.py bind`): the Run linked to its Result;
2. otherwise the citation Job's newest check that holds the key (jNN_*/tNN_*/runs/*/result/citations.csv), the Run
   linked to its citations.csv;
3. otherwise "not read yet": no Run has checked the key.

The reference (who, year, title, venue, link) is read from the discovery Run the check names (its one-entry .bib),
else the BibTeX in the item, else the Page's Bib (draft/evidence/bibex/*.bib), else the check's title and year.
Nothing here writes.
"""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

from live.frame import esc

BIB_HEAD = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,")
PAPER_RUN = re.compile(r"^[pP]\.?j(\d+)\.?t(\d+)\.?r(\d+)$")
DISC_RUN = re.compile(r"\bb(\d+)\.j(\d+)\.t(\d+)\.r(\d+)\b")


def bib_text_ref(text: str, key: str = "") -> dict:
    """One BibTeX entry (the one named `key`, else the first) as a reference: who ("Ibrahim and Zaki"), year, title,
    venue, and a link (its DOI, else its URL, else its arXiv id)."""
    text = text or ""
    if key:
        heads = list(BIB_HEAD.finditer(text))
        for i, m in enumerate(heads):
            if m.group(2) == key:
                text = text[m.start():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
                break
    get = lambda k: ((m := re.search(r"\b" + k + r"\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", text, re.I)) and
                     re.sub(r"[{}]", "", m[1]).strip()) or ""
    raw = re.search(r"\bauthor\s*=\s*\{\s*\{([^{}]+)\}\s*\}", text)        # {{U.S. Congress}}: one name, kept whole
    names = [raw[1].strip()] if raw else [a.strip() for a in re.split(r"\s+and\s+", get("author")) if a.strip()]
    last = lambda a: a.split(",")[0].strip() if "," in a else a.split()[-1]
    who = ((names[0] if raw else last(names[0])) + (" et al." if len(names) > 2 else f" and {last(names[1])}"
           if len(names) == 2 else "")) if names else ""
    doi, url, eprint = get("doi"), get("url") or get("howpublished").replace("\\url", "").strip(), get("eprint")
    link = (f"https://doi.org/{doi}" if doi else url if url.startswith("http") else
            f"https://arxiv.org/abs/{eprint}" if eprint else "")
    venue = get("journal") or get("booktitle") or ("arXiv" if eprint else get("howpublished")
                                                     if not get("howpublished").startswith("\\url") else "")
    return {"who": re.sub(r"\\([&%$#_])", r"\1", who), "year": (re.search(r"\d{4}", get("year")) or [""])[0],
            "title": get("title"), "venue": venue, "link": link}


def item_key(it: dict) -> str:
    """The BibTeX key an item cites: the key of the entry its Local Input or Expected holds, else its Label."""
    m = BIB_HEAD.search(it.get("local_input", "") + " " + it.get("expected", ""))
    return m.group(2) if m else (it.get("label") or "").strip()


def _num(name: str) -> str:
    return (re.match(r"[a-z](\d+)", name) or [None, ""])[1]


@lru_cache(maxsize=64)
def _csv_rows(path: str, mtime: float) -> dict:
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["key"]: r for r in csv.DictReader(fh) if r.get("key")}


def checks(board: Path) -> dict:
    """{key: (run folder, its citations.csv row, P.jNN.tNN.rNN)}: the citation Run that checked each key, a claim
    group's own Run before the paper-wide t99, the newest Run of a Task first."""
    out = {}
    files = sorted(Path(board).glob("j*/t*/runs/*/result/citations.csv"), key=lambda f: (f.parents[3].name.startswith("t99"), f.parents[3].name,
                                         -int(_num(f.parents[1].name) or 0)))
    for f in files:
        try:
            rows = _csv_rows(str(f), f.stat().st_mtime)
        except (OSError, KeyError, csv.Error):
            continue
        run, task, job = f.parents[1], f.parents[3], f.parents[4]
        addr = f"P.j{_num(job.name)}.t{_num(task.name)}.r{_num(run.name)}"
        for k, r in rows.items():
            out.setdefault(k, (run, r, addr))
    return out


def _local(value: str) -> tuple:
    """(address, result path) of a bound Local Run, ("", "") when the item names none."""
    left, _, result = (value or "").partition("→")
    parts = [p.strip() for p in left.split("·")]
    if len(parts) < 4 or [p.lower() for p in parts[:2]] != ["page", "evidence item"]:
        return "", ""
    return parts[3], result.strip()


def _find(path: str, task: Path, root: Path | None) -> Path | None:
    """The one resolver the export and health use too (haipipe-draft src/result_paths.py)."""
    from src.result_paths import resolve
    return resolve(path.strip(), root or task, task)


def _discovery(task: Path, addr: str) -> Path | None:
    """The result/ folder of a discovery Run named b01.j03.t01.r01, in the Project above the Section."""
    m = DISC_RUN.search(addr or "")
    if not m:
        return None
    for base in task.parents:
        if (base / "discovery").is_dir():
            b, j, t, r = m.groups()
            hit = sorted((base / "discovery").glob(f"b{b}_*/j{j}_*/t{t}_*/runs/r{r}_*/result"))
            return hit[0] if hit else None
    return None


def _href(p: Path | None, root: Path | None) -> str:
    try:
        return "/" + quote(p.resolve().relative_to(root.resolve()).as_posix()) if p and root else ""
    except ValueError:
        return ""


def _link(text: str, href: str) -> str:
    return f'<a href="{esc(href)}" target=_blank>{esc(text)}</a>' if href else esc(text)


def cite_entries(task: Path, d: dict, ev: dict, root: Path | None = None) -> list:
    """[(sentence address, card, item, n)] for each CITE item of the Section that no evidence/cards.yaml card holds,
    on each sentence it targets; each item carries `peek` (the side card's line) and `html` (its opened line)."""
    from live.draft_step_support import _targets, evidence_items
    task = Path(task)
    items = [it for it in evidence_items(task) if it["kind"] == "CITE"]
    if not items:
        return []
    held = {str(it.get(f) or "") for c in ev.get("cards", []) if c.get("kind") == "cite" for it in c["items"]
            for f in ("item", "cite")} - {""}
    tmap = _targets(d)
    board = task.parent.parent
    seen = checks(board)
    bibdir = task / "draft" / "evidence" / "bibex"
    page_bib = "\n".join(b.read_text(encoding="utf-8", errors="replace") for b in sorted(bibdir.glob("*.bib"))) \
        if bibdir.is_dir() else ""
    card = {"kind": "cite", "label": "CITE", "source": "", "title": "", "items": []}
    out = []
    for n, it in enumerate(items, 1):
        key = item_key(it)
        name = f'{it["id"]}-CITE-{it["slug"]}'
        if name in held or key in held:
            continue
        addrs = [tmap.get(t) or tmap.get(t.lower()) for t in it["targets"]]
        addrs = [a for a in addrs if a]
        if not addrs:
            continue
        bound, result = _local(it.get("local_run", ""))
        check = seen.get(key)
        row = check[1] if check else {}
        disc = _discovery(task, row.get("discovery_runs", "") or it.get("supporting_runs", ""))
        refs = []
        if disc:
            refs.append(bib_text_ref("\n".join(b.read_text(encoding="utf-8", errors="replace")
                                               for b in sorted(disc.glob("*.bib")))))
        refs += [bib_text_ref(it.get("local_input", "") + " " + it.get("expected", ""), key),
                 bib_text_ref(page_bib, key) if key and re.search(r"@\w+\s*\{\s*" + re.escape(key) + r"\s*,", page_bib)
                 else {}, {"title": row.get("title", ""), "year": row.get("year", "")}]
        ref = next((r for r in refs if r.get("title")), {})
        who = next((r["who"] for r in refs if r.get("who")), "")
        year = ref.get("year") or next((r["year"] for r in refs if r.get("year")), "")
        if bound:
            at = _find(result, task, root) if result else None
            run = (('✅ ' if at else '❗ ') + 'Run ' + _link(bound, _href(at, root))) if result else f'Run {esc(bound)}'
            state = "have" if at else "missing"
        elif check:
            run = 'Run ' + _link(check[2], _href(check[0] / "result" / "citations.csv", root))
            state = "have"
        else:
            run, state = "<span class=ev-unread>not read yet</span>", "need"
        card_md = disc / f"{disc.parent.name}.md" if disc else None
        src = (' · card ' + _link(row.get("discovery_runs", "").split(",")[0].strip() or disc.parent.name,
                                  _href(card_md if card_md and card_md.is_file() else disc, root))) if disc else ""
        shown = esc(f"{who} ({year})" if who and year else who or key)
        title = ref.get("title") or ""
        title = _link(title, ref.get("link", "")) + "." if title else ""
        venue = f' <i>{esc(ref["venue"])}</i>.' if ref.get("venue") else ""
        html = (f'<div class="ev-item ev-ref">❝︎ {shown}. {title}{venue} '
                f'<span class=ev-run>{run}{src}</span></div>')
        peek = f"{who} {year}".strip() or key
        x = {"cite": key, "item": name, "state": state, "from_items": True, "peek": peek, "html": html}
        for a in dict.fromkeys(addrs):
            out.append((a, card, x, n))
    return out
