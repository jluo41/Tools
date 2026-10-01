#!/usr/bin/env python3
"""Fetch ONE verbatim BibTeX entry for a Discovery Paper/Source Result.

Identity first, entry second.  A resolved DOI, arXiv identifier, or exact dblp
venue record is required before any entry is written, because title-only
lookup can return a different paper: Crossref answered the bibliographic query "Large Language
Models are Zero-Shot Rankers for Recommender Systems" with the unrelated
"LLM-BL: ... for Bug Localization" (10.1109/icpc66645.2025.00064).  Title mode
therefore only PROPOSES candidates and refuses to write.

Fetch ladder for a DOI: Crossref REST transform, then doi.org content
negotiation, then DataCite.  doi.org is second because publishers may ignore the
Accept header: 10.1038/s41746-026-03117-z answers 302 text/html there while
Crossref returns the correct entry.

The script copies an entry; it never composes one.  A browser-exported,
exact-record dblp entry enters through `--dblp-bib-file --dblp-record` and
retains its curated-index provenance.  `--bib-file` carries a person-supplied
or Google-Scholar-exported entry and is stamped with the weaker
`person-export` class.  Google Scholar is never fetched by this script.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


USER_AGENT = "haipipe-discovery/0.18.0 (paper bib fetch)"
BIBTEX_ACCEPT = "application/x-bibtex"
AUTHORITATIVE = "authoritative-export"
CURATED_INDEX = "curated-index-export"
PERSON_EXPORT = "person-export"
TRUSTED_HOSTS = {
    "api.crossref.org": "crossref",
    "doi.org": "doi-content-negotiation",
    "dx.doi.org": "doi-content-negotiation",
    "api.datacite.org": "datacite",
    "arxiv.org": "arxiv",
}
# Crossref work types that are a preprint-server posting rather than a venue
# record.  A posting may legitimately be the Subject; it may not silently stand
# in for one, because titles collide across servers.
POSTING_TYPES = {"posted-content"}


def _checker() -> Any:
    """Reuse paper_runs' entry grammar so the writer and the checker agree."""
    script = Path(__file__).with_name("paper_runs.py")
    spec = importlib.util.spec_from_file_location("paper_runs_for_bib", script)
    if spec is None or spec.loader is None:  # pragma: no cover - install error
        raise RuntimeError(f"cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = _checker()


def _get(url: str, timeout: float, accept: str | None = None) -> tuple[int, str, str]:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, response.headers.get_content_type(), body
    except urllib.error.HTTPError as exc:
        return exc.code, "", ""
    except (urllib.error.URLError, TimeoutError, UnicodeError) as exc:
        return 0, f"error: {type(exc).__name__}", ""


def parse_entries(text: str) -> list[tuple[str, str, str]]:
    """Return (entry_type, key, entry_text) using the checker's own grammar."""
    entries: list[tuple[str, str, str]] = []
    for match in CHECKER.BIB_START_RE.finditer(text):
        if match.group(1).lower() in CHECKER.NON_ENTRY_TYPES:
            continue
        entries.append(
            (match.group(1).lower(), match.group(3), CHECKER._balanced_entry(text, match))
        )
    return entries


def entry_doi(entry_text: str) -> str | None:
    match = CHECKER.DOI_RE.search(entry_text)
    return match.group(1).strip().casefold() if match else None


def field_value(entry_text: str, name: str) -> str | None:
    """Read one field, counting braces.

    Crossref returns a whole entry on a single line, so a lazy regex reads past
    the closing brace and swallows every later field.
    """
    match = re.search(rf"(?i)(?:^|[,{{(\s]){re.escape(name)}\s*=\s*", entry_text)
    if not match:
        return None
    index = match.end()
    if index >= len(entry_text):
        return None
    opener = entry_text[index]
    if opener == "{":
        depth = 0
        for position in range(index, len(entry_text)):
            char = entry_text[position]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return entry_text[index + 1 : position].strip()
        return None
    if opener == '"':
        end = entry_text.find('"', index + 1)
        return entry_text[index + 1 : end].strip() if end != -1 else None
    end = re.search(r"[,}\n)]", entry_text[index:])
    return entry_text[index : index + (end.start() if end else 0)].strip() or None


def entry_title(entry_text: str) -> str | None:
    title = field_value(entry_text, "title")
    return re.sub(r"\s+", " ", re.sub(r"[{}]", "", title)).strip() if title else None


def first_author_family(entry_text: str) -> str | None:
    """Read the first author surname for a review hint, not an identity proof."""
    authors = field_value(entry_text, "author")
    if not authors:
        return None
    first = re.split(r"\s+and\s+", authors, maxsplit=1, flags=re.IGNORECASE)[0]
    first = re.sub(r"[{}]", "", first).strip()
    if not first:
        return None
    return (first.split(",", 1)[0] if "," in first else first.split()[-1]) or None


def dblp_record_url(url: str) -> tuple[str, str]:
    """Require one venue record, rather than a person/search export or CoRR."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "dblp.org" or parsed.query or parsed.fragment:
        raise ValueError("dblp-record-must-be-an-exact-https-dblp.org-record")
    path = re.sub(r"\.(?:bib|html)$", "", parsed.path)
    match = re.fullmatch(r"/rec/((?:conf|journals)/[A-Za-z0-9_./-]+)", path)
    if not match or match.group(1).startswith("journals/corr/"):
        raise ValueError("dblp-record-must-be-a-conference-or-journal-venue-record")
    key = match.group(1)
    return f"https://dblp.org/rec/{key}", key


def read_dblp_export(path: Path, record_url: str) -> tuple[str, str, dict[str, Any]]:
    """Read a browser-saved single-record export and check its dblp binding."""
    canonical, record_key = dblp_record_url(record_url)
    bibtex = path.read_text(encoding="utf-8").strip() + "\n"
    entries = parse_entries(bibtex)
    if len(entries) != 1:
        raise ValueError(f"dblp-export-entry-count: expected 1, found {len(entries)}")
    entry_type, key, entry = entries[0]
    if key != f"DBLP:{record_key}":
        raise ValueError(f"dblp-export-key-mismatch: {key!r} versus {record_key!r}")
    if entry_type not in {"article", "inproceedings"}:
        raise ValueError(f"dblp-export-is-not-a-venue-article: {entry_type}")
    biburl = field_value(entry, "biburl")
    if biburl != canonical + ".bib":
        raise ValueError("dblp-export-biburl-mismatch: use the exact record's BibTeX export")
    bibsource = field_value(entry, "bibsource")
    if not bibsource or "dblp" not in bibsource.casefold():
        raise ValueError("dblp-export-bibsource-missing")
    venue = field_value(entry, "booktitle") or field_value(entry, "journal")
    if not venue:
        raise ValueError("dblp-export-venue-missing")
    record = {
        "state": "found",
        "type": "conference-paper" if entry_type == "inproceedings" else "journal-article",
        "publisher": field_value(entry, "publisher"),
        "year": entry_year(entry),
        "venue": venue,
        "landing_page": canonical,
    }
    return bibtex, canonical + ".bib", record


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def title_similarity(left: str, right: str) -> float:
    return difflib.SequenceMatcher(
        None, _normalize_title(left), _normalize_title(right)
    ).ratio()


def titles_agree(expected: str, found: str, minimum: float) -> tuple[bool, float]:
    """Similarity, but a registered SHORT title is a match, not a mismatch.

    Publishers register titles without the subtitle: SAGE holds "The Face of
    Success" for the paper whose full title is "The Face of Success: Inferences
    From Chief Executive Officers' Appearance Predict Company Profits".  Found
    in a read-only audit of 384 real Discovery Results, where three such pairs
    were the only "mismatches".  A prefix counts only when the shorter title is
    substantial, so "Attention" never stands in for a real title.
    """
    ratio = title_similarity(expected, found)
    left, right = _normalize_title(expected), _normalize_title(found)
    shorter = min(left, right, key=len)
    substantial = len(shorter) >= 15 and len(shorter.split()) >= 3
    if substantial and (left.startswith(right) or right.startswith(left)):
        return True, ratio
    return ratio >= minimum, ratio


def fetch_by_doi(doi: str, timeout: float) -> tuple[str, str, str] | None:
    """Try Crossref, then doi.org content negotiation, then DataCite."""
    encoded = urllib.parse.quote(doi, safe="")
    routes = [
        (
            "crossref",
            f"https://api.crossref.org/works/{encoded}/transform/{BIBTEX_ACCEPT}",
            None,
        ),
        ("doi-content-negotiation", f"https://doi.org/{doi}", BIBTEX_ACCEPT),
        ("datacite", f"https://api.datacite.org/{BIBTEX_ACCEPT}/{doi}", None),
    ]
    for channel, url, accept in routes:
        status, content_type, body = _get(url, timeout, accept)
        if status != 200 or not body.strip():
            continue
        # A publisher that ignores Accept: returns its HTML landing page.
        if content_type.startswith("text/html") or not parse_entries(body):
            continue
        return body.strip() + "\n", url, channel
    return None


def crossref_record(doi: str, timeout: float) -> dict[str, Any]:
    """Read type/publisher/year/venue so a title collision is visible.

    A DOI passed on the command line agrees with itself, so DOI-agreement proves
    nothing and an identical title scores 1.0.  10.65215/2q58a426 is a 2025
    posting on a Shenzhen preprint server that reuses the exact title "Attention
    Is All You Need"; only these fields tell it apart from the 2017 paper.
    """
    encoded = urllib.parse.quote(doi, safe="")
    status, _, body = _get(f"https://api.crossref.org/works/{encoded}", timeout)
    if status != 200:
        return {"state": f"http-{status}"}
    try:
        message = json.loads(body)["message"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return {"state": "unparsed"}
    container = message.get("container-title") or []
    parts = (message.get("issued") or {}).get("date-parts") or [[None]]
    return {
        "state": "found",
        "type": message.get("type"),
        "publisher": message.get("publisher"),
        "year": parts[0][0] if parts and parts[0] else None,
        "venue": container[0] if container else None,
        "landing_page": ((message.get("resource") or {}).get("primary") or {}).get("URL"),
    }


def fetch_by_publisher(url: str, timeout: float) -> tuple[str, str, str] | None:
    """A venue's own .bib endpoint, e.g. proceedings.neurips.cc/.../-Bibtex.bib."""
    status, content_type, body = _get(url, timeout, BIBTEX_ACCEPT)
    if status != 200 or content_type.startswith("text/html") or not parse_entries(body):
        return None
    return body.strip() + "\n", url, "publisher"


def fetch_by_arxiv(arxiv_id: str, timeout: float) -> tuple[str, str, str] | None:
    url = f"https://arxiv.org/bibtex/{arxiv_id}"
    # arXiv throttles a burst (the Result builder has just fetched the abstract and the PDF), so a
    # refusal is retried after a pause before the entry is declared missing.
    for pause in (0, 5, 15):
        time.sleep(pause)
        status, _, body = _get(url, timeout)
        if status == 200 and parse_entries(body):
            return body.strip() + "\n", url, "arxiv"
    return None


def _crossref_candidates(
    title: str, timeout: float, rows: int
) -> tuple[str, list[dict[str, Any]]]:
    query = urllib.parse.urlencode(
        {
            "rows": str(rows),
            "query.bibliographic": title,
            "select": "DOI,title,issued,container-title,type,publisher",
        }
    )
    status, _, body = _get(f"https://api.crossref.org/works?{query}", timeout)
    if status != 200:
        return f"http-{status}", []
    try:
        items = json.loads(body)["message"]["items"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "unparsed", []
    candidates = []
    for item in items:
        found = (item.get("title") or [""])[0]
        container = item.get("container-title") or []
        candidates.append(
            {
                "channel": "crossref",
                "doi": item.get("DOI"),
                "arxiv": None,
                "title": found,
                "venue": container[0] if container else None,
                "year": ((item.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                "type": item.get("type"),
                "publisher": item.get("publisher"),
                "title_similarity": round(title_similarity(title, found), 3),
            }
        )
    return "ok", candidates


def _openalex_candidates(
    title: str, timeout: float, rows: int
) -> tuple[str, list[dict[str, Any]]]:
    """Crossref is DOI-only; an arXiv-native or DOI-less venue paper needs this."""
    query = urllib.parse.urlencode(
        {"filter": f"title.search:{title}", "per-page": str(rows)}
    )
    status, _, body = _get(f"https://api.openalex.org/works?{query}", timeout)
    if status != 200:
        # 503 "Anonymous search is paused" is common; it must be VISIBLE, not
        # read as "this channel found nothing".
        return f"http-{status}", []
    try:
        results = json.loads(body).get("results") or []
    except json.JSONDecodeError:
        return "unparsed", []
    candidates = []
    for work in results:
        found = work.get("title") or ""
        ids = work.get("ids") or {}
        primary = (work.get("primary_location") or {}).get("source") or {}
        arxiv = None
        for location in work.get("locations") or []:
            landing = (location.get("landing_page_url") or "")
            match = re.search(r"arxiv\.org/abs/([0-9.]+|[a-z-]+/\d+)", landing)
            if match:
                arxiv = match.group(1)
                break
        candidates.append(
            {
                "channel": "openalex",
                "doi": (ids.get("doi") or "").replace("https://doi.org/", "") or None,
                "arxiv": arxiv,
                "title": found,
                "venue": primary.get("display_name"),
                "year": work.get("publication_year"),
                "type": work.get("type"),
                "publisher": primary.get("host_organization_name"),
                "title_similarity": round(title_similarity(title, found), 3),
            }
        )
    return "ok", candidates


def _arxiv_candidates(
    title: str, timeout: float, rows: int
) -> tuple[str, list[dict[str, Any]]]:
    query = urllib.parse.urlencode(
        {"search_query": f'ti:"{title}"', "max_results": str(rows)}
    )
    status, _, body = _get(f"https://export.arxiv.org/api/query?{query}", timeout)
    if status != 200 or not body:
        return (f"http-{status}" if status != 200 else "empty-body"), []
    namespace = "{http://www.w3.org/2005/Atom}"
    candidates = []
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return "unparsed", []
    for entry in root.findall(f"{namespace}entry"):
        found = _clean_text((entry.findtext(f"{namespace}title") or ""))
        identifier = (entry.findtext(f"{namespace}id") or "").rsplit("/", 1)[-1]
        published = (entry.findtext(f"{namespace}published") or "")[:4]
        candidates.append(
            {
                "channel": "arxiv",
                "doi": None,
                "arxiv": re.sub(r"v\d+$", "", identifier) or None,
                "title": found,
                "venue": "arXiv",
                "year": int(published) if published.isdigit() else None,
                "type": "preprint",
                "publisher": "arXiv",
                "title_similarity": round(title_similarity(title, found), 3),
            }
        )
    return "ok", candidates


def arxiv_id_year(arxiv_id: str | None) -> int | None:
    """A new-style arXiv id encodes YYMM, so 1706.03762 is 2017-06."""
    if not arxiv_id:
        return None
    match = re.match(r"^(\d{2})(\d{2})\.\d{4,5}$", arxiv_id)
    if not match:
        return None
    return 2000 + int(match.group(1))


def flag_identifier_conflicts(candidates: list[dict[str, Any]]) -> None:
    """Mark a row whose identifiers disagree with its year.

    OpenAlex merges records: its top hit for "Attention Is All You Need" carries
    arXiv 1706.03762 (2017) AND doi 10.65215/2q58a426, a 2025 posting on another
    server, under one work with year 2025.  Taking the DOI from such a row ships
    the wrong paper.
    """
    for row in candidates:
        id_year = arxiv_id_year(row.get("arxiv"))
        row["arxiv_id_year"] = id_year
        row["identifier_conflict"] = bool(
            id_year and row.get("year") and abs(id_year - row["year"]) > 1
        )


def propose_titles(title: str, timeout: float, rows: int = 5) -> list[dict[str, Any]]:
    """Title mode: return candidates for a person to resolve.  Never writes.

    Crossref alone is not enough: it indexes DOIs, so an arXiv-native paper or a
    pre-2022 proceedings record can be absent while five wrong papers rank above
    it.  arXiv and OpenAlex cover those, and the caller still picks.
    """
    candidates: list[dict[str, Any]] = []
    channels: dict[str, str] = {}
    for name, fetch in (
        ("crossref", _crossref_candidates),
        ("openalex", _openalex_candidates),
        ("arxiv", _arxiv_candidates),
    ):
        state, rows_found = fetch(title, timeout, rows)
        channels[name] = f"{state}:{len(rows_found)}" if state == "ok" else state
        candidates.extend(rows_found)
    flag_identifier_conflicts(candidates)
    candidates.sort(key=lambda row: row["title_similarity"], reverse=True)
    return channels, candidates


def entry_year(entry_text: str) -> int | None:
    raw = field_value(entry_text, "year")
    match = re.search(r"\d{4}", raw) if raw else None
    return int(match.group(0)) if match else None


def validate(
    bibtex: str,
    *,
    expected_doi: str | None,
    expected_title: str | None,
    min_similarity: float,
    expected_year: int | None = None,
    expected_first_author: str | None = None,
    expected_venue: str | None = None,
    year_tolerance: int = 1,
    channel: str | None = None,
    record: dict[str, Any] | None = None,
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Return (errors, warnings, facts) for one fetched entry."""
    errors: list[str] = []
    warnings: list[str] = []
    entries = parse_entries(bibtex)
    facts: dict[str, Any] = {"entries": len(entries)}
    if len(entries) != 1:
        errors.append(f"bib-entry-count: expected exactly 1, found {len(entries)}")
        return errors, warnings, facts

    entry_type, key, entry_text = entries[0]
    facts.update({"entry_type": entry_type, "key": key})
    found_doi = entry_doi(entry_text)
    found_title = entry_title(entry_text)
    facts["doi"] = found_doi
    facts["title"] = found_title
    first_author = first_author_family(entry_text)
    facts["first_author_family"] = first_author
    found_venue = field_value(entry_text, "booktitle") or field_value(entry_text, "journal")
    facts["venue"] = found_venue

    if expected_doi:
        if channel == "dblp-browser-export" and not found_doi:
            warnings.append(
                "dblp-venue-doi-missing: the expected publication DOI cannot be "
                "cross-checked in this export; inspect the exact venue record "
                "before person verification"
            )
        elif found_doi and found_doi != expected_doi.casefold():
            errors.append(
                f"bib-doi-mismatch: entry carries {found_doi!r}, asked for "
                f"{expected_doi.casefold()!r}"
            )
    if expected_title and not found_title:
        errors.append("bib-title-missing: expected a title in the exported entry")
    if expected_title and found_title:
        agree, raw_ratio = titles_agree(expected_title, found_title, min_similarity)
        ratio = round(raw_ratio, 3)
        facts["title_similarity"] = ratio
        if not agree:
            errors.append(
                f"bib-title-mismatch: similarity {ratio} < {min_similarity}: "
                f"got {found_title!r}"
            )
        elif ratio < min_similarity:
            warnings.append(
                f"title-is-a-registered-short-form: the record says "
                f"{found_title!r}; confirm it is the same publication"
            )

    found_year = entry_year(entry_text)
    facts["year"] = found_year
    if expected_year is not None:
        allowed_year_gap = 0 if channel == "dblp-browser-export" else year_tolerance
        if found_year is None:
            errors.append(f"bib-year-missing: expected {expected_year}, entry has none")
        elif abs(found_year - expected_year) > allowed_year_gap:
            errors.append(
                f"bib-year-mismatch: entry says {found_year}, you expected "
                f"{expected_year} (tolerance {allowed_year_gap}); an identical title "
                "on a different paper passes every other guard"
            )
    elif expected_doi:
        warnings.append(
            "no-year-cross-check: a DOI agrees with itself and an identical title "
            "scores 1.0, so pass --expected-year to catch a title collision"
        )

    if expected_first_author:
        expected_family = re.sub(r"[^\w]+", "", expected_first_author).casefold()
        found_family = re.sub(r"[^\w]+", "", first_author or "").casefold()
        if not found_family:
            finding = "bib-first-author-missing: check the export against the venue record"
            (errors if channel == "dblp-browser-export" else warnings).append(finding)
        elif found_family != expected_family:
            finding = (
                f"bib-first-author-mismatch: entry says {first_author!r}, "
                f"expected {expected_first_author!r}; check name order and the venue record"
            )
            (errors if channel == "dblp-browser-export" else warnings).append(finding)

    if expected_venue:
        if not found_venue:
            warnings.append("bib-venue-missing: check the exported entry against the accepted record")
        else:
            agree, ratio = titles_agree(expected_venue, found_venue, 0.80)
            if not agree:
                warnings.append(
                    f"bib-venue-mismatch: entry says {found_venue!r}, expected "
                    f"{expected_venue!r} (similarity {ratio:.3f}); inspect the "
                    "accepted venue record before verification"
                )

    if record and record.get("type") in POSTING_TYPES:
        warnings.append(
            f"subject-is-a-posting: Crossref type {record.get('type')!r}, publisher "
            f"{record.get('publisher')!r}, year {record.get('year')!r}; confirm this "
            "posting IS the Subject and not a same-title record elsewhere"
        )

    scholar_shape = (
        "; this is the Google Scholar export signature"
        if channel == "google-scholar-export"
        else ""
    )
    if found_doi is None:
        warnings.append(
            "no-doi-in-entry: the Result cannot take part in bib-doi-conflict "
            f"detection{scholar_shape}"
        )
    if re.match(r"(?i)^https?://", key):
        warnings.append(
            f"url-shaped-key: @{key} is unusable in \\citep{{}}; ask the person "
            "for a citable key before promotion"
        )
    # Sentence case is legitimate for many venues (npj Digital Medicine uses it),
    # so only a CASE-ONLY difference from the expected title is a finding.
    if expected_title and found_title and found_title != expected_title:
        if _normalize_title(found_title) == _normalize_title(expected_title):
            warnings.append(
                f"title-case-differs: entry says {found_title!r}, you expected "
                f"{expected_title!r}{scholar_shape}"
            )
    return errors, warnings, facts


def build_bib_block(
    *,
    source: str,
    channel: str,
    source_class: str,
    fetched_at: str,
    verification: str | None,
    record: dict[str, Any] | None = None,
) -> str:
    lines = [
        "bib:",
        f"  source: {source!r}".replace("'", '"'),
        "  mode: verbatim_copy",
        f"  source_class: {source_class}",
        f"  channel: {channel}",
        f"  fetched_at: {fetched_at!r}".replace("'", '"'),
    ]
    # The accepted record's own type/publisher/year, so a reviewer can see a
    # same-title decoy without re-querying anything.
    if record and record.get("state") == "found":
        lines.append("  record:")
        for key in ("type", "publisher", "year", "venue", "landing_page"):
            value = record.get(key)
            if value is not None:
                lines.append(f"    {key}: {str(value)!r}".replace("'", '"'))
    if verification is not None:
        lines.append(verification.rstrip("\n"))
    else:
        lines.extend(
            [
                "  verification:",
                "    status: pending",
            ]
        )
    return "\n".join(lines) + "\n"


BIB_BLOCK_RE = re.compile(r"(?m)^bib:\s*\n(?:^[ \t]+.*(?:\n|$))*")
VERIFICATION_RE = re.compile(r"(?m)^[ \t]+verification:\s*\n(?:^[ \t]{4,}.*(?:\n|$))*")


def stamp_runtime(
    runtime_path: Path,
    block: str,
    *,
    keep_verification: str | None,
) -> str:
    text = runtime_path.read_text(encoding="utf-8")
    had_verification = existing_verification(runtime_path) is not None
    if BIB_BLOCK_RE.search(text):
        new_text = BIB_BLOCK_RE.sub(block, text, count=1)
        action = "replaced"
    else:
        new_text = text.rstrip("\n") + "\n" + block
        action = "appended"
    runtime_path.write_text(new_text, encoding="utf-8")
    # A new entry invalidates a person's earlier reading of the old one.
    if had_verification and keep_verification is None:
        return f"{action}+verification-reset"
    return action


def existing_verification(runtime_path: Path) -> str | None:
    if not runtime_path.is_file():
        return None
    block = BIB_BLOCK_RE.search(runtime_path.read_text(encoding="utf-8"))
    if not block:
        return None
    found = VERIFICATION_RE.search(block.group(0))
    return found.group(0) if found else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    identity = parser.add_mutually_exclusive_group(required=True)
    identity.add_argument("--doi", help="Resolved publication DOI when no exact dblp venue export is chosen.")
    identity.add_argument("--arxiv", help="Resolved arXiv identifier.")
    identity.add_argument(
        "--publisher-url",
        help="A venue's own .bib endpoint; stamped authoritative-export/publisher.",
    )
    identity.add_argument(
        "--dblp-bib-file",
        type=Path,
        help="Browser-saved BibTeX for one exact dblp venue record; use with --dblp-record.",
    )
    identity.add_argument(
        "--bib-file",
        type=Path,
        help="Person-supplied or Scholar-exported entry; stamped person-export.",
    )
    identity.add_argument(
        "--resolve-title",
        help="Propose Crossref, OpenAlex, and arXiv candidates. Never writes a Result.",
    )
    parser.add_argument("--title", help="Expected title; guards against a wrong paper.")
    parser.add_argument("--dblp-record", help="Exact https://dblp.org/rec/<venue-record> URL for --dblp-bib-file.")
    parser.add_argument("--expected-doi", help="Known publication DOI to compare with an imported export.")
    parser.add_argument("--expected-first-author", help="Known first-author surname; a dblp mismatch blocks import.")
    parser.add_argument("--expected-venue", help="Accepted conference or journal name; mismatch prompts review.")
    parser.add_argument(
        "--source-url", help="Required with --bib-file: where the person got the entry."
    )
    parser.add_argument(
        "--result-dir",
        type=Path,
        help="results/<RUNNAME>/; writes <RUNNAME>.bib and stamps runtime.yaml.",
    )
    parser.add_argument("--output", type=Path, help="Explicit .bib path instead.")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--min-title-similarity", type=float, default=0.90)
    parser.add_argument(
        "--expected-year",
        type=int,
        help="The Subject's publication year; guards against a different "
        "paper carrying an identical title.",
    )
    parser.add_argument("--year-tolerance", type=int, default=1)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Refuse on a warning too. Off by default: an arXiv preprint has no "
        "DOI, so the no-DOI warning must not block the commonest fetch.",
    )
    parser.add_argument("--no-runtime", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.resolve_title:
        channels, candidates = propose_titles(args.resolve_title, args.timeout)
        down = [name for name, state in channels.items() if not state.startswith("ok")]
        strong = [c for c in candidates if c["title_similarity"] >= 0.80]
        notes = []
        if down:
            notes.append(
                f"DEGRADED: {', '.join(down)} did not answer, so this sweep is "
                "narrower than it looks. Re-run before trusting a single hit."
            )
        if len(strong) > 1:
            notes.append(
                f"{len(strong)} candidates score >= 0.80, so this title is NOT "
                "unique; read publisher and year before picking."
            )
        elif len(strong) == 1 and not down:
            notes.append(
                "exactly one candidate scores >= 0.80 across every live channel, "
                "which is evidence the title is unique."
            )
        print(
            json.dumps(
                {
                    "mode": "resolve-title",
                    "written": False,
                    "refused": "title-only identity is not a Subject; pick one "
                    "candidate's DOI, arXiv id, exact dblp venue record, or publisher .bib URL. Skip any "
                    "row with identifier_conflict: its ids and year disagree.",
                    "channels": channels,
                    "degraded": bool(down),
                    "strong_matches": len(strong),
                    "notes": notes,
                    "candidates": candidates,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    if args.bib_file and not args.source_url:
        parser.error("--bib-file requires --source-url")
    if args.dblp_bib_file and not args.dblp_record:
        parser.error("--dblp-bib-file requires --dblp-record")
    if args.dblp_record and not args.dblp_bib_file:
        parser.error("--dblp-record requires --dblp-bib-file")
    if args.dblp_bib_file and (not args.title or args.expected_year is None):
        parser.error("--dblp-bib-file requires --title and --expected-year")
    if args.doi and args.expected_doi and args.doi.casefold() != args.expected_doi.casefold():
        parser.error("--expected-doi disagrees with --doi")
    if not args.dry_run and not (args.result_dir or args.output):
        parser.error("one of --result-dir or --output is required")

    source_class = AUTHORITATIVE
    record: dict[str, Any] | None = None
    if args.doi:
        record = crossref_record(args.doi, args.timeout)
    if args.dblp_bib_file:
        try:
            bibtex, source, record = read_dblp_export(args.dblp_bib_file, args.dblp_record)
        except (OSError, ValueError) as exc:
            print(json.dumps({"written": False, "refused": str(exc)}, ensure_ascii=False, indent=2))
            return 4
        channel = "dblp-browser-export"
        source_class = CURATED_INDEX
    elif args.bib_file:
        bibtex = args.bib_file.read_text(encoding="utf-8").strip() + "\n"
        source, channel = args.source_url, "person-supplied"
        source_class = PERSON_EXPORT
        host = urllib.parse.urlparse(args.source_url).hostname or ""
        if host.endswith("scholar.google.com"):
            channel = "google-scholar-export"
    else:
        if args.doi:
            fetched = fetch_by_doi(args.doi, args.timeout)
        elif args.arxiv:
            fetched = fetch_by_arxiv(args.arxiv, args.timeout)
        else:
            fetched = fetch_by_publisher(args.publisher_url, args.timeout)
        if fetched is None:
            print(
                json.dumps(
                    {
                        "written": False,
                        "refused": "no authoritative export found",
                        "identity": args.doi or args.arxiv or args.publisher_url,
                        "next": "For a computer-science venue paper, inspect its exact dblp venue record "
                        "and import that BibTeX export; otherwise use the venue/publisher export. "
                        "Use Google Scholar only as a manually checked last resort.",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 3
        bibtex, source, channel = fetched

    errors, warnings, facts = validate(
        bibtex,
        expected_doi=args.expected_doi or args.doi,
        expected_title=args.title,
        min_similarity=args.min_title_similarity,
        expected_year=args.expected_year,
        expected_first_author=args.expected_first_author,
        expected_venue=args.expected_venue,
        year_tolerance=args.year_tolerance,
        channel=channel,
        record=record,
    )
    blocked = bool(errors) or (bool(warnings) and args.strict)
    summary: dict[str, Any] = {
        "identity": args.doi or args.arxiv or args.dblp_record or args.publisher_url or args.source_url,
        "record": record,
        "channel": channel,
        "source": source,
        "source_class": source_class,
        **facts,
        "errors": errors,
        "warnings": warnings,
    }

    if args.dry_run or blocked:
        summary["written"] = False
        if blocked and not args.dry_run:
            summary["refused"] = "validation failed; nothing was written"
        summary["bibtex"] = bibtex
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if args.dry_run and not errors else (4 if blocked else 0)

    if args.result_dir:
        bib_path = args.result_dir / f"{args.result_dir.name}.bib"
        runtime_path = args.result_dir / "runtime.yaml"
    else:
        bib_path = args.output
        runtime_path = None

    unchanged = bib_path.is_file() and bib_path.read_text(encoding="utf-8") == bibtex
    bib_path.parent.mkdir(parents=True, exist_ok=True)
    bib_path.write_text(bibtex, encoding="utf-8")
    summary["written"] = str(bib_path)

    if runtime_path and runtime_path.is_file() and not args.no_runtime:
        keep = existing_verification(runtime_path) if unchanged else None
        block = build_bib_block(
            source=source,
            channel=channel,
            source_class=source_class,
            fetched_at=datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            verification=keep,
            record=record,
        )
        summary["runtime"] = stamp_runtime(runtime_path, block, keep_verification=keep)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
