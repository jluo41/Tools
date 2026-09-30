#!/usr/bin/env python3
"""Build one Discovery Paper Result from a DOI, so a Paper Run's Ticket can rebuild it.

A Paper Run's Ticket (`runs/rNN_<author><year>_<slug>.sh`) calls this script with the
paper's DOI and the two lines a person or agent wrote after reading the abstract
(the readout and the reuse). It writes the Result the Paper Workbench's Related Papers
cards read (haipipe-workbench-paper 0.16.0):

  results/<run>/runtime.yaml          identity, venue string, reading depth, the bib block
  results/<run>/<run>.bib             one verbatim entry (paper_bib_fetch.py)
  results/<run>/source-access.json    links and identifiers (paper_source_access.py),
  results/<run>/source-access.md      plus `local_pdf` when a free copy was saved
  results/<run>/abstract.md           the PubMed abstract (paper_source_access.py)
  results/<run>/facts.md              the identity and one fact per abstract sentence
  results/<run>/<run>.md              the Result card: question, readout, limits, reuse
  results/<run>/paper.pdf             a free copy, when one exists (--pdf-from or OpenAlex)

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
    return {"title": html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title))).strip(),
            "authors": authors, "first_family": fam, "year": year, "journal": journal, "venue": venue.strip(),
            "landing": ((m.get("resource") or {}).get("primary") or {}).get("URL") or "https://doi.org/" + doi,
            "n_authors": len(m.get("author") or [])}


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


def save_pdf(result, pdf_from, doi, space_root):
    """A free copy as paper.pdf: a file already on disk, else OpenAlex's open-access PDF.
    Returns the local_pdf record or None."""
    dest = result / "paper.pdf"
    if pdf_from:
        src = (space_root / pdf_from).resolve()
        shutil.copyfile(src, dest)
        return {"path": "paper.pdf", "version": "published", "source": pdf_from}
    try:
        w = json.load(fetch("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)))
    except Exception:
        return None
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
            ver = ("preprint" if (loc.get("version") == "submittedVersion" or "rxiv" in url) else
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
    ap.add_argument("--trigger", default="", help="the request that found the paper")
    a = ap.parse_args()

    task = a.task.resolve()
    space_root = next((p for p in [task] + list(task.parents) if (p / "env.sh").is_file()), None)
    if space_root is None:
        sys.exit("no env.sh above %s" % task)
    result = task / "results" / a.run
    result.mkdir(parents=True, exist_ok=True)
    y = (task / "discovery.yaml").read_text(encoding="utf-8") if (task / "discovery.yaml").is_file() else ""
    qm = re.search(r"(?ms)^question:\s*\|\s*\n(.*?)(?=^\S)", y)
    question = " ".join(x.strip() for x in (qm.group(1) if qm else "").splitlines() if x.strip())

    meta = crossref(a.doi)
    bib_url = "https://api.crossref.org/works/%s/transform/application/x-bibtex" % urllib.parse.quote(a.doi, safe="")
    subprocess.run([sys.executable, str(HERE / "paper_source_access.py"), "--doi", a.doi, "--title", meta["title"],
                    "--bib-url", bib_url, "--output-dir", str(result)], check=True, stdout=subprocess.DEVNULL)
    sa = json.loads((result / "source-access.json").read_text(encoding="utf-8"))
    abstract = (sa.get("abstract") or {}).get("text") or ""
    depth = "abstract" if abstract else "metadata-only"
    pdf = save_pdf(result, a.pdf_from, a.doi, space_root)
    sa["retrieval"].update({"reading_depth": depth, "claim_support": "supported" if abstract else "not-assessed",
                            "locator_status": "complete" if abstract else "metadata-only",
                            "depth_note": ("The Run reads the PubMed abstract. The full text was not read."
                                           if abstract else "No abstract was available; identity and metadata only.")})
    if pdf:
        sa["local_pdf"] = pdf
    (result / "source-access.json").write_text(json.dumps(sa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
        "  claim_support: %s" % ("supported" if abstract else "not-assessed"),
        "  locator_status: %s" % ("complete" if abstract else "metadata-only"),
        "  scope_note: %s" % q("Only the PubMed abstract was read; every fact is a sentence of it. No full-text claim is made."
                               if abstract else "No abstract was available; the card rests on metadata only."),
        "worker:",
        "  kind: api",
        "  name: %s" % q("Crossref + PubMed + OpenAlex; haipipe-discovery scripts/paper_result_build.py"),
        "  calls:",
        "    - %s" % q("Crossref works lookup by DOI"),
        "    - %s" % q("PubMed E-utilities abstract (paper_source_access.py)"),
        "    - %s" % q("OpenAlex open-access location"),
        "    - %s" % q("Crossref BibTeX transform through scripts/paper_bib_fetch.py"),
        "executed_at: %s" % q(now),
        "",
    ])
    (result / "runtime.yaml").write_text(runtime, encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "paper_bib_fetch.py"), "--doi", a.doi, "--title", meta["title"],
                    "--result-dir", str(result)], check=True, stdout=subprocess.DEVNULL)
    key = re.search(r"@\w+\s*\{\s*([^,\s]+)", (result / (a.run + ".bib")).read_text(encoding="utf-8")).group(1)

    cite = "%s %s" % (who(meta), meta["year"])
    facts = ["# %s · facts from the abstract" % cite, "",
             "- `F01` · Subject identity: %s, %s; %s; DOI %s%s. Locator: Crossref record." % (
                 q(meta["title"]), meta["authors"], meta["venue"], a.doi,
                 ("; PMID %s" % ids["pmid"]) if ids.get("pmid") else "")]
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
        "Abstract depth only; the paper body was not read%s. Numbers and claims are the authors' own." % (
            ", even though a local PDF is saved" if pdf else ""), "",
        "## Reuse", "", a.reuse, "",
    ])
    (result / (a.run + ".md")).write_text(card, encoding="utf-8")
    print("built %s · %s · %s · %s" % (a.address, cite, depth, ("pdf " + pdf["version"]) if pdf else "no pdf"))


if __name__ == "__main__":
    main()
