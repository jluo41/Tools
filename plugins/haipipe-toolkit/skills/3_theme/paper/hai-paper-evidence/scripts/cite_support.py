"""cite_support.py · does each cited source say what the citing sentence says? One recorded reading per citing
sentence and key, before any co-author round (AgreeableJama-Board 261123: a co-author found a sentence saying an
opioid prescription "was filled" after 21.6% of visits, where the source says "the rate of opioid prescribing was
21.6%"; cite_tasks.py checks the entry, DOI, signature and card, and no check read the source).

    python cite_support.py sources <paper>/j03_evidence_cite      fetch each DOI's PubMed abstract (cached)
    python cite_support.py sheet   <paper>/j03_evidence_cite      write or refresh the reading sheet
    python cite_support.py check   <paper>/j03_evidence_cite      one line per reading; exit = prints-wrong count

Files, all in the paper-wide Task `j03_evidence_cite/t99_paper_citation_check/`:

    sources/<key>.txt   the source's text as fetched: the PubMed abstract found by its DOI (NCBI E-utilities,
                        esearch `<doi>[doi]` then efetch), or a file a person put there (a PDF's text, a web page)
    support.yaml        one row per citing sentence and key: section, sentence, key, text, hash, source, and the
                        reading's four fields, filled by hai-draft-evidence-cite-agent or a person:
                          reading   supports | looser | wrong | not checkable
                          passage   the source's own words the reading rests on (quoted, not paraphrased)
                          note      what differs, for looser or wrong
                          by        who read it, and the date

`sheet` keeps every reading whose sentence text is unchanged; a changed sentence keeps its old reading under
`was:` and is read again. `check` sorts the rows into what the paper prints wrong (wrong, looser, and a number the
sentence quotes that its passage does not hold) and what is not recorded yet (no reading, no passage, a stale
reading, no source text); `not checkable` waits on a person.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import cite_tasks as ct  # noqa: E402
import paper_text as pt  # noqa: E402

READINGS = ("supports", "looser", "wrong", "not checkable")
SAME = {"partly": "looser", "does not": "wrong", "unclear": "not checkable"}   # the cite agent's per-Section words
FIELDS = ("reading", "passage", "note", "by")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
NUMBER = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(%|percent)|(?<![\w.])(\d+\.\d+)(?![\w.])")


def task_dir(j03: Path) -> Path:
    return Path(j03).resolve() / ct.CHECK_TASK


def plain(text: str) -> str:
    """The sentence as a reader sees it: citation commands dropped, LaTeX made plain, one space."""
    t = ct.CITE.sub("", text)
    t = re.sub(r"\\(?:emph|textit|textbf)\{([^}]*)\}", r"\1", t)
    t = t.replace("\\%", "%").replace("~", " ").replace("\\&", "&")
    return re.sub(r"\s+", " ", re.sub(r"\s+([.,;:])", r"\1", t)).strip()


def digest(text: str) -> str:
    return hashlib.sha1(plain(text).encode("utf-8")).hexdigest()[:10]


def numbers(text: str) -> list[str]:
    """The numbers a sentence quotes from a source: a percent or a decimal (a year or a count is not one)."""
    return [m[1] or m[3] for m in NUMBER.finditer(plain(text))]


def citing(paper) -> list[dict]:
    """Every citing sentence of the printed Sections, once per key, in print order."""
    rows = []
    for sec in pt.sections(paper.job):
        for sid, _, text, keys in ct.text_of(sec):
            for k in keys:
                if k != "TOADD":
                    rows.append({"section": sec.name, "sentence": sid, "key": k, "text": plain(text),
                                 "hash": digest(text)})
    return rows


def dois(paper) -> dict:
    """{key: doi} from the Sections' bib files and the version's reference.bib."""
    out = {}
    files = [f for s in pt.sections(paper.job) for f in sorted((s / "draft" / "evidence" / "bibex").glob("*.bib"))]
    files.append(paper.board / "delivery" / paper.job.name / "latex" / "reference.bib")
    for f in files:
        if f.is_file():
            for k, e in ct.parse_bib(f.read_text(encoding="utf-8")).items():
                d = ct.norm_doi(e["fields"].get("doi"))
                if d:
                    out.setdefault(k, d)
    return out


# ── sources ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "hai-cite-support"})
    for wait in (2, 5, 10, None):                           # NCBI answers 429 when asked too fast: wait, then again
        try:
            time.sleep(0.4)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait is None:
                raise
            time.sleep(wait)


def pubmed_abstract(doi: str) -> tuple[str, str] | None:
    """(pmid, abstract text) for a DOI, or None when PubMed holds no record of it."""
    q = urllib.parse.urlencode({"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json", "tool": "haipipe"})
    ids = json.loads(_get(EUTILS + "esearch.fcgi?" + q))["esearchresult"].get("idlist") or []
    if len(ids) != 1:
        return None
    q = urllib.parse.urlencode({"db": "pubmed", "id": ids[0], "rettype": "abstract", "retmode": "text", "tool": "haipipe"})
    return ids[0], _get(EUTILS + "efetch.fcgi?" + q).decode("utf-8", "replace").strip()


def sources(j03: Path, fetch=pubmed_abstract) -> int:
    paper = ct.Paper(j03)
    folder = task_dir(j03) / "sources"
    folder.mkdir(parents=True, exist_ok=True)
    keys = list(dict.fromkeys(r["key"] for r in citing(paper)))
    doi = dois(paper)
    got = kept = 0
    for k in keys:
        f = folder / f"{k}.txt"
        if f.is_file():
            kept += 1
            continue
        if not doi.get(k):
            print(f"⬜ {k}: no DOI; put the source's text at sources/{k}.txt")
            continue
        try:
            hit = fetch(doi[k])
        except Exception as e:                              # noqa: BLE001 (a network error is reported, not raised)
            print(f"❗ {k}: {doi[k]}: {e}")
            continue
        if hit is None:
            print(f"⬜ {k}: {doi[k]} has no PubMed record; put the source's text at sources/{k}.txt")
            continue
        pmid, text = hit
        f.write_text(f"key: {k}\ndoi: {doi[k]}\npmid: {pmid}\nfetched: {date.today()} PubMed abstract\n\n{text}\n",
                     encoding="utf-8")
        got += 1
        print(f"✅ {k}: PubMed {pmid}")
    print(f"sources: {got} fetched, {kept} already there, {len(keys) - got - kept} without a source text")
    return 0


# ── sheet ───────────────────────────────────────────────────────────────────────────────────────────────────────────
HEAD = ("# cite_support.py sheet: one row per citing sentence and key. Fill reading (supports | looser | wrong |\n"
        "# not checkable), passage (the source's own words), note, by. Rerun sheet after an edit; check reads it.\n")


def load(path: Path) -> list[dict]:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or []) if path.is_file() else []


def sheet(j03: Path) -> int:
    paper = ct.Paper(j03)
    path = task_dir(j03) / "support.yaml"
    old = {(r.get("section"), str(r.get("sentence")), r.get("key")): r for r in load(path)}
    out, kept, again = [], 0, 0
    for r in citing(paper):
        r["source"] = f"sources/{r['key']}.txt" if (task_dir(j03) / "sources" / f"{r['key']}.txt").is_file() else ""
        o = old.get((r["section"], r["sentence"], r["key"]))
        for f in FIELDS:
            r[f] = ""
        if o and o.get("hash") == r["hash"]:
            r.update({f: o.get(f) or "" for f in FIELDS})
            if o.get("was"):
                r["was"] = o["was"]
            kept += bool(r["reading"])
        elif o and o.get("reading"):
            r["was"] = {"text": o.get("text"), **{f: o.get(f) or "" for f in FIELDS}}
            again += 1
        out.append(r)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEAD + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    print(f"{path}: {len(out)} rows; {kept} readings kept; {again} sentences changed, to read again")
    return 0


# ── check ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def norm_num(s: str) -> str:
    return re.sub(r"\s+", "", s.replace("·", ".").replace(",", ""))


def judge(rows: list[dict], folder: Path) -> dict:
    """{'wrong': [...], 'missing': [...], 'person': [...], 'ok': [...]}, each item (row, why)."""
    out = {"wrong": [], "missing": [], "person": [], "ok": []}
    held = {}                                               # (section, sentence) -> the passages that support it
    for r in rows:
        if r.get("reading") == "supports":
            held.setdefault((r["section"], str(r["sentence"])), []).append(norm_num(r.get("passage") or ""))
    for r in rows:
        reading = (r.get("reading") or "").strip().split(":")[0].strip()
        reading = SAME.get(reading, reading)
        src = folder / (r.get("source") or f"sources/{r['key']}.txt")
        if not reading:
            why = "not read against its source" + ("" if src.is_file() else "; no source text yet")
            out["missing"].append((r, why + ("; its sentence changed since the last reading" if r.get("was") else "")))
        elif reading not in READINGS:
            out["missing"].append((r, f"reading {reading!r} is none of {', '.join(READINGS)}"))
        elif reading in ("wrong", "looser"):
            out["wrong"].append((r, f"{reading}: {r.get('note') or 'no note'}"))
        elif reading == "not checkable":
            out["person"].append((r, r.get("note") or "the source text does not settle it"))
        elif not (r.get("passage") or "").strip():
            out["missing"].append((r, "supports, with no passage quoted"))
        else:
            lost = [n for n in numbers(r["text"]) if not any(norm_num(n) in p for p in held[(r["section"], str(r["sentence"]))])]
            if lost:
                out["wrong"].append((r, f"quotes {', '.join(lost)}, which no supporting passage holds"))
            else:
                out["ok"].append((r, "supports"))
    return out


def where(r: dict) -> str:
    return f"{r['section']} {r['sentence']} · {r['key']}"


def check(j03: Path, quiet=False) -> int:
    paper = ct.Paper(j03)
    rows = load(task_dir(j03) / "support.yaml")
    now = {(r["section"], r["sentence"], r["key"]): r["hash"] for r in citing(paper)}
    for r in rows:                                          # a sheet older than the text: the row is stale
        if now.get((r.get("section"), str(r.get("sentence")), r.get("key"))) != r.get("hash"):
            r["reading"], r["was"] = "", r.get("was") or {"text": r.get("text")}
    have = {(r.get("section"), str(r.get("sentence")), r.get("key")) for r in rows}
    rows += [{"section": s, "sentence": i, "key": k, "text": "", "hash": h} for (s, i, k), h in now.items()
             if (s, i, k) not in have]
    rows = [r for r in rows if (r.get("section"), str(r.get("sentence")), r.get("key")) in now]
    J = judge(rows, task_dir(j03))
    if not quiet:
        for mark, group in (("❗", "wrong"), ("⬜", "missing"), ("🙋", "person")):
            for r, why in J[group]:
                print(f"{mark} {where(r)}: {why}")
        print(f"cite_support: {len(rows)} citing sentence-key pairs: {len(J['ok'])} supported, {len(J['wrong'])} "
              f"printed wrong, {len(J['missing'])} not recorded, {len(J['person'])} for a person")
    return len(J["wrong"]) + len(J["missing"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("verb", choices=("sources", "sheet", "check"))
    ap.add_argument("j03", type=Path, help="the paper Board's j03_evidence_cite")
    a = ap.parse_args(argv)
    return {"sources": sources, "sheet": sheet, "check": check}[a.verb](a.j03)


if __name__ == "__main__":
    sys.exit(main())
