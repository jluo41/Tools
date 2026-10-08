#!/usr/bin/env python3
"""Build one Discovery Paper Result from a DOI, so a Paper Run's Ticket can rebuild it.

A Paper Run's Ticket (`runs/rNN_<author><year>_<slug>.sh`) calls this script with the
paper's DOI and the two lines a person or agent wrote after reading the abstract
(the readout and the reuse). It writes the Result the Paper Workbench's Related Papers
cards read (workbench-paper 0.16.0):

  results/<run>/runtime.yaml          identity, venue string, reading depth, the bib block
  results/<run>/<run>.bib             one verbatim entry (paper_bib_fetch.py)
  results/<run>/source-access.json    links and identifiers (paper_source_access.py),
  results/<run>/source-access.md      plus `local_pdf` when a free copy was saved
  results/<run>/abstract.md           the abstract: PubMed, else OpenAlex, else Crossref, else arXiv (--arxiv or an arXiv DOI)
  results/<run>/facts.md              the identity and one fact per abstract sentence
  results/<run>/<run>.md              the Result card: question, readout, limits, reuse
  results/<run>/paper.pdf             a free copy, when one exists (--pdf-from, OpenAlex, then arXiv)
  results/<run>/logic-work.yaml       the paper's own logic and work, when the Task holds the authored
                                      readout scripts/readouts/<run>/logic-work.yaml

The task's question comes from its discovery.yaml. Every path written is relative to
the Task folder. Nothing here judges relevance: the readout and reuse are inputs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "haipipe-discovery (paper result build; mailto:jjluo211@gmail.com)"}


def fetch(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)


def crossref(doi):
    m = json.load(fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    year = next((d["date-parts"][0][0] for d in (m.get("published-print"), m.get("issued"))    # the issue's year,
                 if d and (d.get("date-parts") or [[None]])[0][0]), None)                      # not online-first
    journal = (m.get("container-title") or [""])[0]
    vol, iss, page = m.get("volume"), m.get("issue"), m.get("page")
    venue = journal + (" %s" % vol if vol else "") + ("(%s)" % iss if iss and vol else "") + (
        ", %s" % page if page else "") + (" (%s)" % year if year else "")
    authors = "; ".join(" ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("name", "")
                        for a in m.get("author") or [])
    fam = ((m.get("author") or [{}])[0].get("family") or (m.get("author") or [{}])[0].get("name") or "anon")
    journal, venue = html.unescape(journal), html.unescape(venue)
    title = re.sub(r"\s*</(?:sub|sup)>", "", re.sub(r"\s*<(?:sub|sup)>\s*", "", (m.get("title") or [""])[0]))  # HbA<sub>1C</sub> → HbA1C
    title = re.sub(r"[{}]", "", title)    # a deposited `{GS-Fuse}` keeps its case braces; a reader sees GS-Fuse
    sub = ((m.get("subtitle") or [""])[0] or "").strip()
    if sub and sub.lower() not in title.lower():     # a book's `Frame Innovation` + `Create New Thinking by Design`:
        title = "%s: %s" % (title.rstrip(" :"), sub)  # its BibTeX entry carries both, and so should the card
    return {"title": html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title))).strip(),
            "authors": authors, "first_family": fam, "year": year, "journal": journal, "venue": venue.strip(),
            "landing": ((m.get("resource") or {}).get("primary") or {}).get("URL") or "https://doi.org/" + doi,
            "n_authors": len(m.get("author") or [])}


def arxiv_id(doi, given=""):
    """The arXiv id: `--arxiv`, else the one an arXiv DataCite DOI (10.48550/arXiv.<id>) carries."""
    m = re.match(r"(?i)^10\.48550/arxiv\.(.+)$", doi or "")
    return (given or (m.group(1) if m else "")).strip()


def arxiv(aid):
    """Identity and abstract from the arXiv API, for a paper Crossref and PubMed do not hold
    (a machine-learning venue with no DOI, or a DOI with no PubMed abstract)."""
    import xml.etree.ElementTree as ET
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(fetch("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid)).read())
    e = root.find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        raise SystemExit("arXiv has no record for %s" % aid)
    text = lambda tag: " ".join((e.findtext(tag, "", ns) or "").split())
    names = [" ".join((a.findtext("a:name", "", ns) or "").split()) for a in e.findall("a:author", ns)]
    year = int(text("a:published")[:4]) if text("a:published") else None
    # arxiv.org/bibtex dates its entry by the LATEST version (<updated>), not the first posting,
    # so the Bib year guard compares against that; the arXiv id itself is the identity check.
    bib_year = int(text("a:updated")[:4]) if text("a:updated") else year
    # a conference with no DOI (ICLR, NeurIPS before its proceedings) is named only in the authors' comment
    said = re.search(r"(?i)\b(?:accepted|published)\s+(?:by|at|to|in|for)\s+(?:the\s+)?(.+?)\s*(?:[.;]|$)", text("x:comment"))
    venue = text("x:journal_ref") or (
        "%s · arXiv %s, venue from the authors' comment" % (said.group(1), aid) if said else
        "arXiv preprint arXiv:%s (%s)" % (aid, year))
    return {"title": text("a:title"), "authors": "; ".join(names),
            "first_family": (names[0].split()[-1] if names else "anon"), "year": year,
            "journal": "arXiv", "venue": venue, "landing": "https://arxiv.org/abs/" + aid,
            "n_authors": len(names), "abstract": text("a:summary"), "bib_year": bib_year}


# The paper's own logic and work (haipipe-discovery 0.20): what it asks, the data and method it
# uses, what it finds and contributes. Authored by the Discovery creator after reading the paper,
# kept at <task>/scripts/readouts/<run>/logic-work.yaml, and copied into the Result by the ticket.
# It carries only the paper's own content; why a consumer keeps the paper stays on the consumer's side.
LW_TEXT = ("question", "data", "contribution")
LW_LIST = ("method", "findings")
LW_READ = ("pdf", "full-text", "supplement", "abstract")


def logic_work(task, run, address):
    """Validate the authored readout and return the Result's logic-work.yaml text, or None."""
    src = task / "scripts" / "readouts" / run / "logic-work.yaml"
    if not src.is_file():
        return None
    import yaml          # only a Run that has a readout needs PyYAML
    spec = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
    bad = [k for k in LW_TEXT if not str(spec.get(k) or "").strip()]
    bad += [k for k in LW_LIST if not (isinstance(spec.get(k), list) and all(str(x).strip() for x in spec[k]) and spec[k])]
    if spec.get("read_from") not in LW_READ:
        bad.append("read_from (one of %s)" % ", ".join(LW_READ))
    if bad:
        sys.exit("logic-work readout %s is missing or malformed: %s" % (src, ", ".join(bad)))
    out = {"run": run, "address": address, "source": str(src.relative_to(task)),
           "read_from": spec["read_from"], "kind": spec.get("kind", ""),
           "question": spec["question"], "data": spec["data"], "method": list(spec["method"]),
           "findings": list(spec["findings"]), "contribution": spec["contribution"]}
    return yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=1000)


def q(s):
    return json.dumps(s, ensure_ascii=False)


def sentences(text):
    out = []
    for para in (text or "").splitlines():
        para = para.strip()
        if not para:
            continue
        label = re.match(r"^([A-Z][A-Z &]+):\s*", para)
        body = para[label.end():] if label else para
        for i, s in enumerate(re.split(r"(?<=[.!?])\s+(?=[A-Z(])", body)):
            s = s.strip()
            if s:
                out.append(((label.group(1).title() + ": ") if label and i == 0 else "") + s)
    return out


def who(meta):
    fam = meta["first_family"]
    return fam if meta["n_authors"] == 1 else ("%s and co-authors" % fam if meta["n_authors"] == 2 else "%s et al." % fam)


def _pdf_text(path, pages=3):
    """The first pages' text (pypdf, else pdftotext), or None when neither can read it."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return len(reader.pages), " ".join((pg.extract_text() or "") for pg in reader.pages[:pages])
    except Exception:
        pass
    if shutil.which("pdftotext") and shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
        n = re.search(r"(?m)^Pages:\s+(\d+)", info)
        text = subprocess.run(["pdftotext", "-f", "1", "-l", str(pages), str(path), "-"],
                              capture_output=True, text=True).stdout
        return (int(n.group(1)) if n else 0), text
    return None


def is_the_paper(path, title):
    """A listed free copy can be something else: OpenAlex lists a library's one-page table of
    contents as the open copy of a book. The copy must have at least two pages and carry most
    of the title's words (60 percent, of words over three letters) on its first pages."""
    got = _pdf_text(path)
    if got is None:                 # nothing here can read a PDF: keep it, unchecked
        return True
    n, text = got
    words = [w for w in re.findall(r"[a-z0-9]+", (title or "").lower()) if len(w) > 3]
    have = set(re.findall(r"[a-z0-9]+", text.lower()))
    need = -(-len(words) * 3 // 5)  # ceil(60%)
    return n >= 2 and sum(w in have for w in words) >= need


def save_pdf(result, pdf_from, doi, space_root, aid="", pmcid="", title="", pdf_url="", pdf_version="published"):
    """A free copy as paper.pdf: a file already on disk, else OpenAlex's open-access PDF,
    else the arXiv preprint, else Europe PMC's copy of a PubMed Central article (a
    publisher that refuses a script, such as Science Advances, still deposits there).
    Returns the local_pdf record or None."""
    dest = result / "paper.pdf"
    if pdf_from:
        src = (space_root / pdf_from).resolve()
        shutil.copyfile(src, dest)
        return {"path": "paper.pdf", "version": pdf_version, "source": pdf_from}   # what the Ticket says it is
    try:
        w = json.load(fetch("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)))
    except Exception:
        w = {}
    if pdf_url:  # a lawful free copy the Ticket names (an author page, a preprint server): tried first,
        w["oa_locations"] = [{"pdf_url": pdf_url, "version": pdf_version, "named": True}] + list(
            w.get("oa_locations") or [])                                     # under its stated version
        w["best_oa_location"] = None
    if aid:      # the arXiv copy is free for every arXiv paper; tried after OpenAlex's
        w.setdefault("oa_locations", []).append({"pdf_url": "https://arxiv.org/pdf/" + aid,
                                                 "version": "submittedVersion"})
    if pmcid:    # last: the PubMed Central deposit, rendered by Europe PMC
        w.setdefault("oa_locations", []).append({"pdf_url": "https://europepmc.org/api/getPdf?pmcid=%s" % pmcid,
                                                 "version": "publishedVersion"})
    for loc in [w.get("best_oa_location")] + list(w.get("oa_locations") or []):
        url = (loc or {}).get("pdf_url")
        if not url:
            continue
        try:
            data = fetch(url, timeout=60).read()
        except Exception:
            continue
        if data[:4] == b"%PDF":
            dest.write_bytes(data)
            if title and not is_the_paper(dest, title):
                dest.unlink()
                continue
            ver = loc["version"] if loc.get("named") else (
                   "preprint" if (loc.get("version") == "submittedVersion" or "rxiv" in url) else
                   "accepted" if loc.get("version") == "acceptedVersion" else "published")
            return {"path": "paper.pdf", "version": ver, "source": url}
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True, type=Path, help="the Discovery Task folder (tNN_<slug>/)")
    ap.add_argument("--run", required=True, help="rNN_<author><year>_<slug>")
    ap.add_argument("--address", required=True, help="bNN.jNN.tNN.rNN")
    ap.add_argument("--doi", required=True)
    ap.add_argument("--readout", required=True, help="what the paper shows, from its abstract")
    ap.add_argument("--reuse", required=True, help="what this study takes from it")
    ap.add_argument("--pdf-from", default="", help="a free copy already on disk, relative to the SPACE root")
    ap.add_argument("--pdf-url", default="", help="a lawful free copy to download first (author page, "
                                                  "preprint server); OpenAlex and arXiv remain the fallbacks")
    ap.add_argument("--pdf-version", choices=("preprint", "accepted", "published"), default="published",
                    help="what the --pdf-from or --pdf-url copy is; recorded in source-access and the card")
    ap.add_argument("--trigger", default="", help="the request that found the paper")
    ap.add_argument("--arxiv", default="", help="the arXiv id, for an abstract and free copy PubMed and "
                                                "OpenAlex do not hold (read from a 10.48550/arXiv DOI)")
    ap.add_argument("--bib-from", choices=("doi", "arxiv", "dblp"), default="doi",
                    help="verbatim BibTeX source; choose dblp for a confirmed conference/journal record")
    ap.add_argument("--dblp-bib-file", type=Path, help="browser-saved exact-record dblp .bib export")
    ap.add_argument("--dblp-record", help="the exact https://dblp.org/rec/... venue record URL")
    ap.add_argument("--bib-key", default="", help="a citation key in place of the exporter's, when it "
                                                   "collides with another Result's in this Task")
    ap.add_argument("--set-aside-abstract", default="", metavar="REASON",
                    help="the retrieved abstract is not this paper's (say why); the Run stays metadata-only")
    a = ap.parse_args()
    if a.bib_from == "dblp" and (not a.dblp_bib_file or not a.dblp_record):
        ap.error("--bib-from dblp requires --dblp-bib-file and --dblp-record")
    if a.bib_from != "dblp" and (a.dblp_bib_file or a.dblp_record):
        ap.error("--dblp-bib-file and --dblp-record require --bib-from dblp")

    task = a.task.resolve()
    space_root = next((p for p in [task] + list(task.parents) if (p / "env.sh").is_file()), None)
    if space_root is None:
        sys.exit("no env.sh above %s" % task)
    result = task / "results" / a.run
    result.mkdir(parents=True, exist_ok=True)
    y = (task / "discovery.yaml").read_text(encoding="utf-8") if (task / "discovery.yaml").is_file() else ""
    qm = re.search(r"(?ms)^question:\s*\|\s*\n(.*?)(?=^\S)", y)
    question = " ".join(x.strip() for x in (qm.group(1) if qm else "").splitlines() if x.strip())

    aid = arxiv_id(a.doi, a.arxiv)
    ax = None
    try:
        meta, id_src = crossref(a.doi), "Crossref"
        bib_url = "https://api.crossref.org/works/%s/transform/application/x-bibtex" % urllib.parse.quote(a.doi, safe="")
    except urllib.error.HTTPError as err:
        if err.code != 404 or not aid:      # only a DOI Crossref does not register (a DataCite arXiv DOI)
            raise
        meta = ax = arxiv(aid)
        id_src = "arXiv"
        bib_url = "https://arxiv.org/bibtex/" + aid   # DataCite keys an arXiv entry by its URL, which \cite cannot take
    if a.bib_from == "dblp":
        if id_src != "Crossref":
            sys.exit("a dblp venue export needs the venue publication DOI, not an arXiv-only identity")
        bib_url = re.sub(r"\.(?:bib|html)$", "", a.dblp_record.rstrip("/")) + ".bib"
    subprocess.run([sys.executable, str(HERE / "paper_source_access.py"), "--doi", a.doi, "--title", meta["title"],
                    "--bib-url", bib_url, "--output-dir", str(result)], check=True, stdout=subprocess.DEVNULL)
    sa = json.loads((result / "source-access.json").read_text(encoding="utf-8"))
    if a.set_aside_abstract:            # a person read the retrieved text and found it is not this paper's
        sa["abstract"] = {"source": (sa.get("abstract") or {}).get("source"), "text": None,
                          "set_aside": a.set_aside_abstract}
        (result / "abstract.md").unlink(missing_ok=True)
    abstract = (sa.get("abstract") or {}).get("text") or ""
    _src = (sa.get("abstract") or {}).get("source") or ""
    abs_src = "OpenAlex" if "openalex.org" in _src else "Crossref" if "api.crossref.org" in _src else "PubMed"
    if not abstract and aid:                # no PubMed abstract: a machine-learning paper's is on arXiv
        ax = ax or arxiv(aid)
        abstract, abs_src = ax["abstract"], "arXiv"
        sa["abstract"] = {"source": "https://arxiv.org/abs/" + aid, "text": abstract}
        (result / "abstract.md").write_text("# Retrieved abstract\n\nSource: https://arxiv.org/abs/%s\n\n%s\n"
                                            % (aid, abstract), encoding="utf-8")
    depth = "abstract" if abstract else "metadata-only"
    pdf = save_pdf(result, a.pdf_from, a.doi, space_root, aid, (sa.get("identifiers") or {}).get("pmcid") or "",
                   meta["title"], a.pdf_url, a.pdf_version)
    sa["retrieval"].update({"reading_depth": depth, "claim_support": "supported" if abstract else "pending",
                            "locator_status": "complete" if abstract else "pending",
                            "depth_note": ("The Run reads the %s abstract. The full text was not read." % abs_src
                                           if abstract else "No abstract was available; identity and metadata only.")})
    if pdf:
        sa["local_pdf"] = pdf
    (result / "source-access.json").write_text(json.dumps(sa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # paper_source_access.py wrote the human summary before this Run read the abstract;
    # carry the updated retrieval state into it so the .md never disagrees with the .json.
    access_md = (result / "source-access.md").read_text(encoding="utf-8")
    for label, key in (("Reading depth", "reading_depth"), ("Claim support", "claim_support"),
                       ("Locator", "locator_status")):
        access_md = re.sub(r"(?m)^- \*\*%s:\*\* .*$" % label,
                           lambda _m, label=label, key=key: "- **%s:** %s" % (label, sa["retrieval"][key]), access_md)
    (result / "source-access.md").write_text(access_md, encoding="utf-8")
    if pdf:
        with (result / "source-access.md").open("a", encoding="utf-8") as f:
            f.write("\n- **Local copy:** paper.pdf (%s), source %s\n" % (pdf["version"], pdf["source"]))

    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    ids = sa.get("identifiers") or {}
    runtime = "\n".join([
        "run: %s" % a.run,
        "address: %s" % a.address,
        "address_compact: %s" % a.address.replace(".", ""),
        "family: discovery",
        "operation: paper-analysis",
        "status: complete",
        "result_contract: paper-source-v2",
        "ticket: runs/%s.sh" % a.run,
        "result: results/%s/" % a.run,
        "trigger:",
        "  kind: user_request",
        "  input: %s" % q(a.trigger or question),
        "  resolved: %s" % q("https://doi.org/" + a.doi),
        "subject:",
        "  kind: paper",
        "  title: %s" % q(meta["title"]),
        "  canonical_url: %s" % q(meta["landing"]),
        "  doi: %s" % q(a.doi),
        "  authors: %s" % q(meta["authors"]),
        "  venue: %s" % q(meta["venue"]),
        "source_access:",
        "  manifest: source-access.json",
        "  summary: source-access.md",
        "analysis:",
        "  reading_depth: %s" % depth,
        "  claim_support: %s" % ("supported" if abstract else "pending"),
        "  locator_status: %s" % ("complete" if abstract else "pending"),
        "  scope_note: %s" % q("Only the %s abstract was read; every fact is a sentence of it. No full-text claim is made."
                               % abs_src if abstract else "The retrieved abstract was set aside: %s" % a.set_aside_abstract
                               if a.set_aside_abstract else "No abstract was available; the card rests on metadata only."),
        "worker:",
        "  kind: api",
        "  name: %s" % q("%s + %s + OpenAlex; haipipe-discovery scripts/paper_result_build.py"
                         % (id_src, abs_src) if abstract else "%s + OpenAlex; haipipe-discovery scripts/paper_result_build.py" % id_src),
        "  calls:",
        "    - %s" % q("%s lookup by %s" % (id_src, "DOI" if id_src == "Crossref" else "arXiv id")),
        "    - %s" % q("PubMed E-utilities abstract (paper_source_access.py)" if abs_src == "PubMed"
                       else "OpenAlex abstract_inverted_index (paper_source_access.py; no PubMed abstract)"
                       if abs_src == "OpenAlex" else "Crossref deposited abstract (paper_source_access.py; no PubMed or OpenAlex text)"
                       if abs_src == "Crossref" else "arXiv API abstract (no PubMed record)"),
        "    - %s" % q("OpenAlex open-access location" + (", then the arXiv PDF" if aid else "")),
        "    - %s" % q("BibTeX through scripts/paper_bib_fetch.py (%s)" % (
            "dblp exact venue record" if a.bib_from == "dblp" else
            "arXiv export" if (id_src == "arXiv" or a.bib_from == "arxiv") else "Crossref, doi.org, then DataCite")),
        "executed_at: %s" % q(now),
        "",
    ])
    (result / "runtime.yaml").write_text(runtime, encoding="utf-8")
    if a.bib_from == "arxiv" and not aid:
        sys.exit("--bib-from arxiv needs --arxiv or an arXiv DOI")
    ident = (["--dblp-bib-file", str(a.dblp_bib_file), "--dblp-record", a.dblp_record,
              "--expected-doi", a.doi] if a.bib_from == "dblp" else
             ["--arxiv", aid] if (id_src == "arXiv" or a.bib_from == "arxiv") else ["--doi", a.doi])
    arxiv_bib = id_src == "arXiv" or a.bib_from == "arxiv"
    bib_year = ((ax or arxiv(aid)).get("bib_year") if arxiv_bib and aid else None) or meta["year"]
    bib = subprocess.run([sys.executable, str(HERE / "paper_bib_fetch.py")] + ident + ["--title", meta["title"],
                          "--expected-first-author", meta["first_family"],
                          "--expected-venue", meta["venue"], "--result-dir", str(result)] +
                         (["--key", a.bib_key] if a.bib_key else []) +
                         (["--expected-year", str(bib_year)] if bib_year else []),
                         stdout=subprocess.PIPE, text=True)
    try:
        bib_review = json.loads(bib.stdout or "{}")
    except json.JSONDecodeError:
        bib_review = {}
    if bib.returncode != 0:     # no verbatim entry: the Result is not complete, and its receipt must say so
        findings = bib_review.get("errors") or bib_review.get("warnings") or []
        why = "; ".join(findings) if findings else bib_review.get("refused", "BibTeX fetch failed")
        (result / "runtime.yaml").write_text(
            runtime.replace("status: complete\n", "status: blocked\nblocked_reason: %s\n" % q(
                "%s (%s); rerun the Ticket" % (why, " ".join(ident)))), encoding="utf-8")
        sys.exit("blocked %s · %s" % (a.address, why))
    for warning in bib_review.get("warnings") or []:
        print("Bib review warning: %s" % warning, file=sys.stderr)
    key = re.search(r"@\w+\s*\{\s*([^,\s]+)", (result / (a.run + ".bib")).read_text(encoding="utf-8")).group(1)

    cite = "%s %s" % (who(meta), meta["year"])
    facts = ["# %s · facts from the abstract" % cite, "",
             "- `F01` · Subject identity: %s, %s; %s; DOI %s%s. Locator: %s record." % (
                 q(meta["title"]), meta["authors"], meta["venue"], a.doi,
                 ("; PMID %s" % ids["pmid"]) if ids.get("pmid") else "", id_src)]
    for i, s in enumerate(sentences(abstract), start=2):
        facts.append("- `F%02d` · Abstract sentence: %s Locator: abstract S%d." % (i, q(s), i - 1))
    (result / "facts.md").write_text("\n".join(facts) + "\n", encoding="utf-8")

    pdf_line = ("Local full text: %s copy saved as paper.pdf (%s)." % (pdf["version"], pdf["source"])
                if pdf else "No free full-text copy was found.")
    card = "\n".join([
        "# %s" % meta["title"], "",
        "- run: %s" % a.run,
        "- address: %s" % a.address,
        "- cite: @%s" % key,
        "- subject: [%s](%s) · DOI [%s](https://doi.org/%s)" % (meta["journal"] or "article", meta["landing"], a.doi, a.doi),
        "- venue: %s" % meta["venue"],
        "- status: complete",
        "- citation verification: pending person-level confirmation", "",
        "## Question", "", question or "(the Task's question)", "",
        "## Readout", "", a.readout, "",
        "## Source access", "",
        "Links and the verbatim BibTeX source are in `source-access.md`. %s%s" % (
            pdf_line, " The abstract is in `abstract.md`." if abstract else ""), "",
        "## Retrieval scope", "",
        "- Reading depth: %s." % depth,
        "- Claim support: %s." % ("supported for the abstract only; nothing about the full text is claimed" if abstract else "not assessed"),
        "- Locator: %s." % ("complete; each fact in `facts.md` names its abstract sentence" if abstract else "metadata only"), "",
        "## Limits", "",
        ("Abstract depth only; the paper body was not read%s. Numbers and claims are the authors' own." % (
            ", even though a local PDF is saved" if pdf else "") if abstract else
         "Metadata only; neither the abstract nor the paper body was read%s, so this Result supports no "
         "claim about the paper's content." % (", even though a local PDF is saved" if pdf else "")), "",
        "## Reuse", "", a.reuse, "",
    ])
    (result / (a.run + ".md")).write_text(card, encoding="utf-8")
    lw = logic_work(task, a.run, a.address)
    (result / "logic-work.yaml").unlink(missing_ok=True)
    if lw:
        (result / "logic-work.yaml").write_text(lw, encoding="utf-8")
    print("built %s · %s · %s · %s%s" % (a.address, cite, depth, ("pdf " + pdf["version"]) if pdf else "no pdf",
                                        " · logic-work" if lw else ""))


if __name__ == "__main__":
    main()
