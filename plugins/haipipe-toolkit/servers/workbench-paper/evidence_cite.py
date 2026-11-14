"""A paper's citations as its Runs returned them: a claim group's (or the whole-paper check's) `citations.csv`, each key
counted once, the bib and abstract behind a key, the sentences that cite it. Moved from evidence_read.py, which
re-exports every name here so `from live.evidence_read import cite_rows` and `er.cite_panel` keep working."""
from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import quote

import yaml

from live.frame import esc
from live.ui_parts import _side_tabs, plural_word
from live.evidence_common import CITE_WORDS, VALUE_CSS, _kv, _pop, check_task, item_tasks, newest


# ── Citations ──────────────────────────────────────────────────────────────────────────────────────────────────
def cite_rows(task: Path | None) -> list:
    """A claim group's (or the check's) newest citations.csv, one dict per key."""
    f = newest(task, "citations.csv") if task is not None else None
    if f is None:
        return []
    try:
        with f.open(encoding="utf-8", newline="") as fh:
            return [r for r in csv.DictReader(fh) if r.get("key")]
    except Exception:
        return []


def job_cites(job: Path) -> list:
    """Every key a citation Job checks, once: the whole-paper check's rows, else its claim groups' put together."""
    rows = cite_rows(check_task(job))
    if not rows:
        rows = [r for t in item_tasks(job) for r in cite_rows(t)]
    seen, out = set(), []
    for r in rows:
        if r["key"] not in seen:
            seen.add(r["key"])
            out.append(r)
    return out


def cite_state(rows: list) -> tuple:
    """(word, waiting line) of a set of keys: none. A page carries no check tally ("41 of 70 keys verified", "2 keys
    not in the bib"); each key's own row shows its status (AGENTS § Page words). The counts stay in the check's own
    receipt. Kept so callers still unpack a pair."""
    return "", ""


def cite_waits(rows: list) -> bool:
    """Does a key wait on the person (not in the bib)? For a to-do row's pill, never shown as a count."""
    return any(r.get("status") in ("missing-bib", "TOADD", "toadd") for r in rows)


def _cite_cls(status: str) -> str:
    return "ok" if status == "verified" else "bad" if status in ("missing-bib", "TOADD", "toadd") else "wait"


def cite_row(r: dict) -> str:
    """One key as a card that stacks at phone width: its title and year, its status in words, where it is cited, its
    DOI, its signature and its source card."""
    st = r.get("status", "")
    title = " · ".join(x for x in (r.get("title", ""), r.get("year", "")) if x) or "no bib entry yet"
    return (f'<div class="ev-row {_cite_cls(st)}"><b>{esc(r["key"])}</b>' + _kv((
        ("Status", esc(CITE_WORDS.get(st, st))), ("Paper", esc(title)), ("Cited in", esc(r.get("cited_in", ""))),
        ("DOI", esc(r.get("doi", "") or "none")), ("Verified by", esc(verified_by(r.get("verified", "")))),
        ("Source card", esc(r.get("cite_card", "") or "none yet: a Discovery card on the citing sentence")),
        ("Discovery Run", esc(r.get("discovery_runs", ""))))) + '</div>')


def verified_by(said: str) -> str:
    """Who verified a key, in words (r02: "Signed: no signed Result")."""
    return "nobody yet" if not said or said.startswith("no signed") else said


def cite_panel(task: Path, root: Path) -> str:
    """A claim group's keys, each a card (no framed page: it hid Status and DOI at 390 px), the Run's own page one Pop
    out away; no count line (each card shows its own status)."""
    rows = cite_rows(task)
    if not rows:
        return ""
    page = newest(task, "citations.html")
    return (VALUE_CSS
            + (f'<div class=pb-verbs>{_pop(f"⤢ Open {task.name}{chr(39)}s table", page, root, task.name + " · citations")}</div>' if page else "")
            + '<div class=ev-rows>' + "".join(cite_row(r) for r in rows) + '</div>')


_ENTRY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")


def bib_entries(board: Path) -> dict:
    """{key: (entry text, file)} from the Board's Section bibex files (`*/t*/draft/evidence/bibex/*.bib`), the entry each
    Section cites; the first file found wins. Each key opens on it in the Citations view (JL 261110: "show the
    things like the title, abstract, and then references, and the bibex")."""
    out = {}
    for f in sorted(board.glob("j*/t*/draft/evidence/bibex/*.bib")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in _ENTRY.finditer(text):
            depth, end = 0, None
            for j in range(m.start(), len(text)):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            if end and m[1] not in out:
                out[m[1]] = (text[m.start():end], f)
    return out


def abstract_bank(job: Path) -> dict:
    """{doi: {key, title, abstract, source}} from any `result/abstracts.yaml` a Run of the citation Job wrote (one fetch
    per DOI, so the page never reaches the web)."""
    out = {}
    for f in sorted(job.glob("*/runs/*/result/abstracts.yaml")):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        out.update({str(k).lower(): v for k, v in data.items() if isinstance(v, dict)})
    return out


def _field(entry: str, name: str) -> str:
    m = re.search(r"(?is)\b" + name + r"\s*=\s*(\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))", entry)
    if not m:
        return ""
    v = m[2] if m[2] is not None else (m[3] if m[3] is not None else m[4] or "")
    v = v.replace("\\&", "&").replace("\\times", "×").replace("$", "").replace("--", "–")
    v = re.sub(r"\\[a-zA-Z]+\s*", "", v).replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", v).strip()


def reference(entry: str) -> str:
    """One bib entry as a reference line: Authors (year). Title. Journal, volume(number), pages."""
    corporate = re.search(r"(?is)\bauthor\s*=\s*\{\s*\{", entry)       # author = {{Centers for Medicare ...}}
    names = [n.strip() for n in re.split(r"\s+and\s+", _field(entry, "author")) if n.strip()]
    if not corporate:
        names = [n.split(",")[0].strip() if "," in n else n.split()[-1] for n in names]
    who = (", ".join(names[:-1]) + " and " + names[-1]) if len(names) > 1 else (names[0] if names else "")
    if len(names) > 3:
        who = names[0] + " et al."
    where = _field(entry, "journal") or _field(entry, "booktitle") or _field(entry, "publisher") or _field(entry, "howpublished")
    vol, num, pages = _field(entry, "volume"), _field(entry, "number"), _field(entry, "pages")
    tail = where + (f", {vol}" if vol else "") + (f"({num})" if num else "") + (f", {pages}" if pages else "")
    return " ".join(x for x in (f"{who} ({_field(entry, 'year')})." if who else "", _field(entry, "title") + ".", tail + "." if tail else "") if x)


CK_CSS = ("<style>details.ck>summary{list-style:none;cursor:pointer}details.ck>summary::-webkit-details-marker{display:none}"
          "details.ck>summary .n:before{content:'▸ ';color:var(--mut,#888)}details.ck[open]>summary .n:before{content:'▾ '}"
          ".ck-body{margin:2px 0 12px 18px;font-size:13px;line-height:1.5}.ck-body h5{margin:8px 0 2px;font-size:12px;color:var(--mut,#666)}"
          ".ck-body pre{white-space:pre-wrap;font-size:11.5px;background:var(--soft,#f6f8fa);padding:8px;border-radius:6px;margin:0}"
          ".ck-body .src{color:var(--mut,#666);font-size:12px}.ck-body p{margin:3px 0 6px;max-width:760px}"
          ".ck-cite{border-left:3px solid var(--line,#d0d7de);padding-left:8px}"
          "details.ck-bib>summary{cursor:pointer;color:var(--mut,#666);font-size:12px;margin-top:8px}</style>")


_PART = re.compile(r"(?:^|(?<=[.!?])\s+|\s{2,})((?:BACKGROUND|OBJECTIVES?|IMPORTANCE|METHODS?|DESIGN[^:]{0,60}|SETTING[^:]{0,40}|"
                   r"PARTICIPANTS|EXPOSURES?|MAIN OUTCOMES?[^:]{0,40}|RESULTS?|CONCLUSIONS?(?: AND RELEVANCE)?|INTERPRETATION|"
                   r"FINDINGS|CONTEXT|AIMS?|PURPOSE|Background|Objectives?|Importance|Methods?|Results?|Conclusions?(?: and Relevance)?|"
                   r"Design, Setting, and Participants|Main Outcomes and Measures|Exposures?|Prologue)\s*:\s*)")


def abstract_html(text: str) -> str:
    """An abstract as short paragraphs: a structured one split at its labels (Objectives, Methods, Results, ...),
    each label bold; a plain one as it is."""
    parts = _PART.split(text.strip())
    if len(parts) < 3:
        return f"<p>{esc(text)}</p>"
    out = f"<p>{esc(parts[0])}</p>" if parts[0].strip() else ""
    for k in range(1, len(parts) - 1, 2):
        label = parts[k].strip().rstrip(":").strip().capitalize()
        out += f"<p><b>{esc(label)}.</b> {esc(parts[k + 1].strip())}</p>"
    return out


_CITE_CMD = re.compile(r"\\cite[pt]?\*?\{([^}]*)\}")


def citing_sentences(board: Path, cited_in: str, key: str, limit: int = 3) -> list:
    """[(Section, S-id, sentence)] where the paper cites `key`, read from each Section's newest Draft (`cited_in` is the
    ledger's 't01_introduction S2, S4 · t02_literature-review S28'); the key shown as [key], other keys dropped."""
    out = []
    for part in [x.strip() for x in re.split(r"[·;]", cited_in) if x.strip()]:   # the ledger writes either
        sec, _, ids = part.partition(" ")
        drafts = sorted(board.glob(f"j*/{sec}/draft/{sec}-draft-v*.md"), key=lambda f: f.stat().st_mtime)
        if not drafts:
            continue
        text = drafts[-1].read_text(encoding="utf-8", errors="ignore")
        for sid in [x.strip() for x in ids.split(",") if x.strip()]:
            hits = re.findall(r"(?m)^- B\d+ · " + re.escape(sid) + r" · (.+)$", text)
            if not hits:
                continue
            sent = _CITE_CMD.sub(lambda m: "[" + key + "]" if key in m[1].split(",") else "", hits[-1])
            sent = re.sub(r"\s+([.,;])", r"\1", re.sub(r"\s{2,}", " ", sent)).strip()
            out.append((sec, sid, sent))
            if len(out) >= limit:
                return out
    return out


def key_detail(r: dict, bib, ab, board: Path | None = None) -> str:
    """A key opened, in the order a reader needs it (JL 261110: "how could you make them to be more readable?"): where
    it is from and its links; why we cite it (our own citing sentences); its abstract split into its parts; the
    reference line; and the BibTeX entry folded away."""
    doi = (r.get("doi") or "").strip()
    title = (ab or {}).get("title") or r.get("title") or ""
    venue = (_field(bib[0], "journal") or _field(bib[0], "booktitle") or _field(bib[0], "publisher")) if bib else ""
    links = " · ".join(x for x in (
        esc(r.get("year", "")), esc(venue),
        f'<a href="https://doi.org/{esc(doi)}" target=_blank>DOI</a>' if doi else "",
        f'<a href="https://scholar.google.com/scholar?q={quote(title)}" target=_blank>Scholar</a>' if title else "") if x)
    parts = [f'<p class=src>{links}</p>' if links else ""]
    cites = citing_sentences(board, r.get("cited_in", ""), r["key"]) if board is not None and r.get("cited_in") else []
    if cites:
        parts.append("<h5>Why we cite it</h5>" + "".join(
            f'<p class=ck-cite>{esc(s).replace(esc("[" + r["key"] + "]"), "<b>[" + esc(r["key"]) + "]</b>")}'
            f' <span class=src>{esc(sec)} {esc(sid)}</span></p>' for sec, sid, s in cites))
    elif r.get("status") == "not cited yet":
        parts.append('<h5>Why we cite it</h5><p class=src>Not cited in the text yet.</p>')
    abstract = (ab or {}).get("abstract")
    parts.append("<h5>Abstract</h5>" + (abstract_html(abstract) + f'<p class=src>From {esc(ab.get("source", "the DOI record"))}.</p>'
                                        if abstract else '<p class=src>No abstract found online for this key.</p>'))
    parts.append("<h5>Reference</h5>" + (f"<p>{esc(reference(bib[0]))}</p>" if bib else "<p class=src>No bib entry yet.</p>"))
    if bib:
        parts.append(f'<details class=ck-bib><summary>BibTeX · {esc(bib[1].name)}</summary><pre>{esc(bib[0])}</pre></details>')
    return '<div class=ck-body>' + "".join(parts) + '</div>'


def cite_lines(task: Path, root: Path) -> str:
    """A claim group in the Citations view: its claim first, then one line per key (the key and its paper, its status in
    words) and one Open; the cards are the Check view's (r02: the Citations tab drew the same three cards as Check)."""
    from live.board_read import _task_url
    rows = cite_rows(task)
    if not rows:
        return ""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    claim = (re.search(r"(?m)^answers:\s*(.+?)\s*$", text) or [None, ""])[1]
    order = {"missing-bib": 0, "TOADD": 0, "toadd": 0, "bib-only": 1, "card-only": 1, "verified": 2}
    bibs, abstracts = bib_entries(task.parent.parent), abstract_bank(task.parent)
    lines = "".join(
        f'<details class=ck><summary class=fd-row><span class=n>{esc(r["key"])}</span><span class=d>{esc(r.get("title") or "no bib entry yet")}</span>'
        f'<span class="w {"fd-ok" if r.get("status") == "verified" else "fd-you" if _cite_cls(r.get("status", "")) == "bad" else ""}">'
        f'{esc(CITE_WORDS.get(r.get("status", ""), r.get("status", "")))}</span></summary>'
        + key_detail(r, bibs.get(r["key"]), abstracts.get((r.get("doi") or "").lower()), task.parent.parent) + '</details>'
        for r in sorted(rows, key=lambda r: order.get(r.get("status", ""), 3)))
    return (VALUE_CSS + CK_CSS + (f'<p class=ev-line><b>Claim</b> · {esc(claim)}</p>' if claim else "") + lines
            + f'<p style="margin-top:10px"><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>')


def cite_key_tabs(rows: list, eid: str) -> str:
    """A claim group's keys, one side tab each (the key; its status in words), its card on the right."""
    if not rows:
        return ""
    order = {"missing-bib": 0, "TOADD": 0, "toadd": 0, "bib-only": 1, "card-only": 1, "verified": 2}
    rows = sorted(rows, key=lambda r: order.get(r.get("status", ""), 3))
    return VALUE_CSS + _side_tabs(eid, [(r["key"], CITE_WORDS.get(r.get("status", ""), r.get("status", ""))) for r in rows],
                                  [cite_row(r) for r in rows])
