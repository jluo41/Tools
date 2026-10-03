"""Check a Related Paper table (skills/0_utils/table-papers/SKILL.md).

    python check_papers_table.py <name>-papers.md [--online] [--format md|blocks]

The table is the one Markdown table in the file whose header is exactly
group | role | key | paper | venue | doi | why here | pdf. Offline, the check reads the
rules a row can break on its own; `--online` also looks every DOI up on OpenAlex (then
Crossref) and compares the title and the year with the row.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

COLUMNS = ["group", "role", "key", "paper", "venue", "doi", "why here", "pdf"]
ROLES = ("classic", "review", "evidence", "practice")
# `Authors Year · Title`; a standard writes its number before the year (`ISO 9241-210:2019 · ...`);
# an undated web page writes `n.d.` for its year
PAPER = re.compile(r"^(?P<who>.+?)[\s:]+(?P<year>\d{4}[a-z]?|n\.d\.)\s+·\s+(?P<title>.+)$")
DOI = re.compile(r"^10\.\d{4,9}/\S+$")


def read_table(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if cells == COLUMNS:
            rows = []
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                values = [c.strip() for c in row.strip().strip("|").split("|")]
                rows.append(dict(zip(COLUMNS, values + [""] * (len(COLUMNS) - len(values)))))
            return rows
    raise SystemExit(f"{path}: no table with the header {' | '.join(COLUMNS)}")


def first_group(row: dict) -> str:
    """A paper that serves two groups (`a; b`) shows under the first."""
    return row["group"].split(";")[0].strip()


def check(rows: list[dict], table: Path) -> tuple[list[str], list[str]]:
    """(problems, warnings): a problem fails the check; a warning is shown and passes."""
    problems, warnings, seen = [], [], {}
    readme = table.parent / "papers" / "README.md"
    licensed = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    for n, r in enumerate(rows, 1):
        where = f'row {n} ({r["paper"][:60] or "no paper"})'
        for col in ("group", "role", "paper", "why here"):
            if not r[col]:
                problems.append(f"{where}: empty {col}")
        if r["role"] and r["role"].lower() not in ROLES:
            problems.append(f'{where}: role "{r["role"]}" is not one of {", ".join(ROLES)}')
        if r["key"] not in ("", "★"):
            problems.append(f'{where}: key is "{r["key"]}"; write ★ or leave it empty')
        if r["paper"] and not PAPER.match(r["paper"]):
            problems.append(f"{where}: paper must read `Authors Year · Title`")
        doi = r["doi"]
        if doi and not (DOI.match(doi) or doi.startswith("https://")):
            problems.append(f'{where}: doi "{doi}" is neither a bare DOI (10.x/...) nor an https page')
        if doi:
            if doi.lower() in seen:
                problems.append(f"{where}: same doi as row {seen[doi.lower()]}")
            seen.setdefault(doi.lower(), n)
        if r["pdf"]:
            if not (table.parent / r["pdf"]).is_file():
                problems.append(f'{where}: pdf {r["pdf"]} is not on disk')
            elif Path(r["pdf"]).name not in licensed:
                problems.append(f'{where}: pdf {Path(r["pdf"]).name} is not listed with its license in papers/README.md')
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(first_group(r), []).append(r)
    for group, members in groups.items():
        if not any(m["key"] == "★" for m in members):
            # the view then shows every paper of the group unfolded
            warnings.append(f'group "{group}": no key paper (★); mark at least one')
    return problems, warnings


def lookup(doi: str) -> list[tuple[str, int | None]]:
    """(title, year) from every registry that knows the DOI: OpenAlex, Crossref, DataCite.
    All three are asked because one can be wrong (OpenAlex has mapped an arXiv DOI to
    another work); arXiv DOIs are registered with DataCite, not Crossref."""
    quoted = urllib.parse.quote(doi, safe="/")
    sources = ((f"https://api.openalex.org/works/doi:{quoted}?select=title,publication_year",
                lambda d: (d.get("title") or "", d.get("publication_year"))),
               (f"https://api.crossref.org/works/{quoted}",
                lambda d: ((d["message"].get("title") or [""])[0],
                           ((d["message"].get("issued") or {}).get("date-parts") or [[None]])[0][0])),
               (f"https://api.datacite.org/dois/{quoted}",
                lambda d: (((d["data"]["attributes"].get("titles") or [{}])[0]).get("title", ""),
                           d["data"]["attributes"].get("publicationYear"))))
    found = []
    for address, pick in sources:
        try:
            with urllib.request.urlopen(urllib.request.Request(address, headers={"User-Agent": "table-papers-check"}),
                                        timeout=15) as response:
                found.append(pick(json.load(response)))
        except Exception:
            continue
    return found


def plain(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def check_online(rows: list[dict]) -> list[str]:
    problems = []
    for n, r in enumerate(rows, 1):
        doi, match = r["doi"], PAPER.match(r["paper"])
        if not DOI.match(doi or "") or not match:
            continue
        found = lookup(doi)
        where = f'row {n} ({r["paper"][:60]})'
        if not found:
            problems.append(f"{where}: doi {doi} not found on OpenAlex, Crossref or DataCite")
            continue
        a = plain(match["title"])
        same = lambda b: a.startswith(b) or b.startswith(a) or difflib.SequenceMatcher(None, a, b).ratio() >= .85
        titled = [(title, year) for title, year in found if title and same(plain(title))]
        if not titled:
            problems.append(f'{where}: title differs from every record: "{found[0][0]}"')
        elif match["year"][:4].isdigit() and not any(
                year and abs(int(match["year"][:4]) - int(year)) <= 1 for _, year in titled):
            problems.append(f"{where}: year {match['year']} but the record says {titled[0][1]}")
    return problems


def blocks(rows: list[dict]) -> str:
    out, group = [], None
    for r in rows:
        if first_group(r) != group:
            group = first_group(r)
            out.append(f"\n{group}")
        out.append(f'  {r["key"] or " "} {r["role"]:<9} {r["paper"]}\n'
                   f'              {r["venue"] or "—"} · {r["doi"] or "no doi"}{" · pdf" if r["pdf"] else ""}\n'
                   f'              {r["why here"]}')
    return "\n".join(out).lstrip("\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", type=Path)
    ap.add_argument("--online", action="store_true", help="also look each DOI up on OpenAlex / Crossref")
    ap.add_argument("--format", choices=("md", "blocks"), default=None, help="print the table first")
    args = ap.parse_args()
    rows = read_table(args.table)
    if args.format == "blocks":
        print(blocks(rows) + "\n")
    elif args.format == "md":
        print("| " + " | ".join(COLUMNS) + " |\n|" + "---|" * len(COLUMNS))
        print("\n".join("| " + " | ".join(r[c] for c in COLUMNS) + " |" for r in rows) + "\n")
    problems, warnings = check(rows, args.table)
    problems += check_online(rows) if args.online else []
    groups = len({first_group(r) for r in rows})
    with_doi = sum(bool(DOI.match(r["doi"] or "")) for r in rows)
    print(f"{len(rows)} papers · {groups} groups · {sum(r['key'] == '★' for r in rows)} key · "
          f"{with_doi} with a DOI{' (looked up)' if args.online else ''} · {sum(bool(r['pdf']) for r in rows)} with a PDF")
    for problem in problems:
        print("  ✗ " + problem)
    for warning in warnings:
        print("  ! " + warning)
    print("check: " + ("PASS" if not problems else f"FAIL ({len(problems)})"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
