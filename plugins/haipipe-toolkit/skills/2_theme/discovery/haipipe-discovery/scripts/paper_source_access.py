#!/usr/bin/env python3
"""Build deterministic, human-clickable source access for one paper Result.

Google and Google Scholar URLs are constructed as navigation links only.  The
script never scrapes either service.  Crossref, PubMed, and OpenAlex lookups are
best-effort; DOI-based links are still emitted when an index is unavailable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


USER_AGENT = "haipipe-discovery/0.9.3 (paper source access)"
MIN_ABSTRACT_WORDS = 30


def _get(url: str, timeout: float) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _get_json(url: str, timeout: float) -> tuple[dict[str, Any] | None, str]:
    try:
        payload = json.loads(_get(url, timeout).decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeError) as exc:
        return None, f"error: {type(exc).__name__}"
    return payload if isinstance(payload, dict) else None, "ok"


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _same_page(a: str, b: str) -> bool:
    norm = lambda u: re.sub(r"^https?://(dx\.)?", "", (u or "").strip().lower()).rstrip("/")
    return norm(a) == norm(b)


def _jats_text(text: str) -> str:
    """A Crossref JATS abstract as plain text: tags dropped, entities decoded, a leading 'Abstract' label removed."""
    import html
    plain = re.sub(r"<[^>]+>", " ", text)                      # JATS tags (<jats:p>)
    plain = re.sub(r"</?(?:i|b|em|sub|sup)>", "", html.unescape(plain))  # escaped inline markup (&lt;i&gt;)
    plain = _clean_text(html.unescape(plain))
    return re.sub(r"^Abstract\s+", "", plain)


# The article's own identifiers. A bare `.//ArticleIdList` also matches every cited
# reference's list, so a PMC id or DOI from the reference list would pass as this paper's
# (Ashokkumar 2026, PMID 42420458, carried its reference 1's PMC id).
OWN_IDS = "./PubmedArticle/PubmedData/ArticleIdList/ArticleId"


def _pubmed(doi: str, timeout: float) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "term": f"{doi}[AID]"}
    )
    search_api = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{query}"
    search_page = "https://pubmed.ncbi.nlm.nih.gov/?" + urllib.parse.urlencode(
        {"term": f"{doi}[AID]"}
    )
    payload, state = _get_json(search_api, timeout)
    record: dict[str, Any] = {
        "state": state,
        "search_url": search_page,
        "record_url": None,
        "pmid": None,
        "pmcid": None,
        "abstract": None,
    }
    ids = (((payload or {}).get("esearchresult") or {}).get("idlist") or [])
    if not ids:
        if state == "ok":
            record["state"] = "not-found"
        return record

    pmid = str(ids[0])
    record.update(
        state="found",
        pmid=pmid,
        record_url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    )
    fetch_query = urllib.parse.urlencode(
        {"db": "pubmed", "id": pmid, "retmode": "xml"}
    )
    fetch_api = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{fetch_query}"
    try:
        root = ET.fromstring(_get(fetch_api, timeout))
    except (urllib.error.URLError, TimeoutError, ET.ParseError):
        # The search hit cannot be checked against the DOI (see below), so it is not kept.
        record.update(state="unverified-record", pmid=None, record_url=None)
        return record

    # `<doi>[AID]` is not an exact match: PubMed answers `10.1086/699976[AID]` (JPE)
    # with `10.3389/fpsyg.2021.699976`, a different paper sharing the suffix. A record
    # whose DOI disagrees is not this paper's, so neither its PMID nor its abstract is kept.
    record_dois = [
        (node.text or "").strip().casefold()
        for node in root.findall(OWN_IDS)
        if node.attrib.get("IdType", "").casefold() == "doi"
    ]
    if record_dois and doi.strip().casefold() not in record_dois:
        record.update(state="doi-mismatch", pmid=None, record_url=None)
        return record

    abstract_parts: list[str] = []
    for node in root.findall(".//Abstract/AbstractText"):
        body = _clean_text("".join(node.itertext()))
        label = _clean_text(node.attrib.get("Label", ""))
        if body:
            abstract_parts.append(f"{label}: {body}" if label else body)
    if abstract_parts:
        record["abstract"] = "\n\n".join(abstract_parts)

    for node in root.findall(OWN_IDS):
        if node.attrib.get("IdType", "").casefold() == "pmc" and node.text:
            record["pmcid"] = node.text.strip().upper()
            break
    return record


def _openalex(doi: str, timeout: float) -> dict[str, Any]:
    # One work by its DOI, not a filtered search: OpenAlex charges searches against a
    # daily budget shared by the whole network and answers 429 once it is spent, while a
    # single-work lookup still answers (2026-10-02).
    api_url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/")
    payload, state = _get_json(api_url, timeout)
    if not (payload or {}).get("id"):
        return {"state": "not-found" if state == "ok" else state}
    work = payload
    oa = work.get("open_access") or {}
    best = work.get("best_oa_location") or {}
    # OpenAlex stores an abstract as word -> positions; rebuild the text. It covers the
    # business, OR and IS journals PubMed does not index.
    inverted = work.get("abstract_inverted_index") or {}
    words = {i: w for w, places in inverted.items() for i in places}
    # A repository's boilerplate ("International audience") or a one-line teaser is
    # not an abstract: under MIN_ABSTRACT_WORDS words the Run stays metadata-only.
    abstract = (_clean_text(" ".join(words[i] for i in sorted(words)))
                if len(words) >= MIN_ABSTRACT_WORDS else None)
    primary = work.get("primary_location") or {}
    return {
        "state": "found",
        "id": work.get("id"),
        "record_url": work.get("id"),
        "is_oa": bool(oa.get("is_oa")),
        "landing_page_url": best.get("landing_page_url")
        or primary.get("landing_page_url"),
        "pdf_url": best.get("pdf_url"),
        "abstract": abstract,
    }


def build_record(
    doi: str,
    title: str,
    bib_url: str,
    timeout: float,
    *,
    offline: bool = False,
    pmid_hint: str | None = None,
    pmcid_hint: str | None = None,
) -> dict[str, Any]:
    doi = doi.strip()
    title = _clean_text(title)
    doi_url = f"https://doi.org/{doi}"
    encoded_doi = urllib.parse.quote(doi, safe="")
    crossref_api = f"https://api.crossref.org/works/{encoded_doi}"
    crossref, crossref_state = (None, "offline") if offline else _get_json(crossref_api, timeout)
    message = (crossref or {}).get("message") or {}
    publisher_url = message.get("URL") or doi_url

    pubmed_search = "https://pubmed.ncbi.nlm.nih.gov/?" + urllib.parse.urlencode(
        {"term": f"{doi}[AID]"}
    )
    pubmed = (
        {
            "state": "found-from-local-identity" if pmid_hint else "offline",
            "search_url": pubmed_search,
            "record_url": (
                f"https://pubmed.ncbi.nlm.nih.gov/{pmid_hint}/"
                if pmid_hint
                else None
            ),
            "pmid": pmid_hint,
            "pmcid": pmcid_hint,
            "abstract": None,
        }
        if offline
        else _pubmed(doi, timeout)
    )
    openalex = {"state": "offline"} if offline else _openalex(doi, timeout)
    full_text_url = None
    full_text_kind = None
    if pubmed.get("pmcid"):
        full_text_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pubmed['pmcid']}/"
        full_text_kind = "pmc"
    elif openalex.get("is_oa") and openalex.get("pdf_url"):
        full_text_url = openalex["pdf_url"]
        full_text_kind = "openalex-pdf"
    elif openalex.get("is_oa") and openalex.get("landing_page_url") and not _same_page(
        openalex["landing_page_url"], doi_url
    ):  # an "open" landing page that is only the DOI page itself is not a full-text route
        full_text_url = openalex["landing_page_url"]
        full_text_kind = "openalex-landing"

    exact_title = f'"{title}"'
    # PubMed first; OpenAlex when PubMed has no abstract (non-medical journals).
    if pubmed.get("abstract"):
        abstract_text, abstract_source = pubmed["abstract"], pubmed.get("record_url")
    elif openalex.get("abstract"):
        abstract_text, abstract_source = openalex["abstract"], openalex.get("record_url")
    elif len(_jats_text(message.get("abstract") or "").split()) >= MIN_ABSTRACT_WORDS:
        # last: the publisher-deposited Crossref abstract (an SSRN posting OpenAlex holds no text for)
        abstract_text, abstract_source = _jats_text(message["abstract"]), crossref_api
    else:
        abstract_text, abstract_source = None, None
    reading_depth = "abstract" if abstract_text else "metadata-only"
    return {
        "schema_version": 1,
        "subject": {"kind": "paper", "title": title, "doi": doi},
        "links": {
            "article": doi_url,
            "doi": doi_url,
            "publisher": publisher_url,
            "pubmed": pubmed.get("record_url") or pubmed["search_url"],
            "pubmed_search": pubmed["search_url"],
            "google_scholar": "https://scholar.google.com/scholar?"
            + urllib.parse.urlencode({"hl": "en", "q": exact_title}),
            "google": "https://www.google.com/search?"
            + urllib.parse.urlencode({"q": exact_title}),
            "bibtex": bib_url,
            "crossref": crossref_api,
            "openalex": openalex.get("record_url"),
            "full_text": full_text_url,
        },
        "retrieval": {
            "crossref": crossref_state,
            "pubmed": pubmed.get("state"),
            "openalex": openalex.get("state"),
            "full_text": "found" if full_text_url else "not-found",
            "full_text_kind": full_text_kind,
            "reading_depth": reading_depth,
            "claim_support": "pending",
            "locator_status": "pending",
        },
        "identifiers": {
            "pmid": pubmed.get("pmid"),
            "pmcid": pubmed.get("pmcid"),
            "openalex": openalex.get("id"),
        },
        "abstract": {
            "source": abstract_source,
            "text": abstract_text,
        },
    }


def render_markdown(record: dict[str, Any]) -> str:
    links = record["links"]
    retrieval = record["retrieval"]
    rows = [
        ("Article", links.get("article")),
        ("Publisher", links.get("publisher")),
        ("PubMed", links.get("pubmed")),
        ("Google Scholar", links.get("google_scholar")),
        ("Google", links.get("google")),
        ("BibTeX source", links.get("bibtex")),
        ("Crossref", links.get("crossref")),
        ("OpenAlex", links.get("openalex")),
        ("Full text", links.get("full_text")),
    ]
    lines = ["# Source access", ""]
    for label, url in rows:
        lines.append(f"- **{label}:** [{url}]({url})" if url else f"- **{label}:** not found")
    lines.extend(
        [
            "",
            "## Retrieval scope",
            "",
            f"- **Reading depth:** {retrieval['reading_depth']}",
            f"- **Claim support:** {retrieval['claim_support']}",
            f"- **Locator:** {retrieval['locator_status']}",
            f"- **Full-text route:** {retrieval['full_text']}",
            "",
            "> Google and Google Scholar links are navigation aids, not evidence authority.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(record: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source-access.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "source-access.md").write_text(
        render_markdown(record), encoding="utf-8"
    )
    abstract = record["abstract"].get("text")
    if abstract:
        (output_dir / "abstract.md").write_text(
            "# Retrieved abstract\n\n"
            f"Source: {record['abstract']['source']}\n\n{abstract}\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--bib-url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Construct deterministic navigation links without remote lookups.",
    )
    parser.add_argument(
        "--identity-hints",
        type=Path,
        help="Existing facts/card text containing trusted PMID or PMCID identifiers.",
    )
    args = parser.parse_args()
    hints = ""
    if args.identity_hints and args.identity_hints.is_file():
        hints = args.identity_hints.read_text(encoding="utf-8", errors="replace")
    pmid_match = re.search(r"\bPMID\s+(\d+)\b", hints, re.IGNORECASE)
    pmcid_match = re.search(r"\bPMCID\s+(PMC\d+)\b", hints, re.IGNORECASE)
    record = build_record(
        args.doi,
        args.title,
        args.bib_url,
        args.timeout,
        offline=args.offline,
        pmid_hint=pmid_match.group(1) if pmid_match else None,
        pmcid_hint=pmcid_match.group(1).upper() if pmcid_match else None,
    )
    write_outputs(record, args.output_dir)
    print(
        json.dumps(
            {
                "reading_depth": record["retrieval"]["reading_depth"],
                "pubmed": record["retrieval"]["pubmed"],
                "full_text": record["retrieval"]["full_text"],
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
