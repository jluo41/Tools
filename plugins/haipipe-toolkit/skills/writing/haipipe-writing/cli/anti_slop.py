#!/usr/bin/env python3
"""Audit prose for AI-writing tells and compare fact tokens across rewrites.

This is a diagnostic companion to ``wdiff.py``.  It never rewrites prose and
never decides whether a paragraph is accepted.  The rule data and the
pattern-density/structure scoring are adapted from the MIT-licensed
``aashaexo/soundshuman`` scanner.  The fact-token comparison follows the
MIT-licensed preservation check in ``Aboudjem/humanizer-skill``.

Usage::

    python3 anti_slop.py audit paragraph.md
    python3 anti_slop.py audit paragraph.md --format json
    python3 anti_slop.py compare --before before.md --after after.md \
        --check-facts --format json

An audit score is a worklist signal, not an AI detector and not an
"undetectability" promise.  A rewrite still goes through ``wdiff.py`` and the
Page Paragraph promotion contract.
"""

# Copyright (c) 2026 aasha, adapted from aashaexo/soundshuman (MIT).
# Fact-token preservation logic adapted from Adam Boudjemaa's
# Aboudjem/humanizer-skill (MIT).  See ref/anti-slop-attribution.md.

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Any, Callable, Iterable


DEFAULT_RULES = Path(__file__).resolve().parent.parent / "ref" / "anti-slop-rules.json"
MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}
FACT_KINDS = (
    "urls",
    "emails",
    "dates",
    "percentages",
    "versions",
    "numbers",
    "acronyms",
    "citations",
    "quoted_terms",
)
FACT_SIBLINGS = {"versions": ("numbers",), "numbers": ("versions",)}
ACRONYM_STOPWORDS = {
    "OK",
    "TODO",
    "FIXME",
    "NOTE",
    "TIP",
    "WARNING",
    "IMPORTANT",
    "CAUTION",
    "AND",
    "OR",
    "NOT",
    "THE",
    "FOR",
    "YES",
    "NO",
}
_CITATION_AUTHOR = r"[A-Z][A-Za-z'’.-]{1,60}"
_CITATION_AUTHORS = (
    rf"{_CITATION_AUTHOR}(?:\s+et\s+al\.)?"
    rf"(?:\s*(?:,|&|and)\s*{_CITATION_AUTHOR})*"
)
_CITATION_PATTERNS = (
    re.compile(
        rf"\((?P<authors>{_CITATION_AUTHORS}),?\s*"
        rf"(?P<year>(?:19|20)\d{{2}}[a-z]?)\)",
    ),
    re.compile(
        rf"(?P<authors>{_CITATION_AUTHORS})\s*"
        rf"\((?P<year>(?:19|20)\d{{2}}[a-z]?)\)",
    ),
)


def _blank(match: str) -> str:
    """Replace a match with spaces while preserving newlines and offsets."""

    return re.sub(r"[^\n]", " ", match)


def prepare_text(raw: str, *, ignore_quotes: bool = False) -> str:
    """Mask non-prose regions without changing line numbers or character offsets."""

    text = str(raw or "")
    text = re.sub(
        r"\A---\n[\s\S]*?\n---\n",
        lambda m: _blank(m.group(0)),
        text,
        count=1,
    )
    text = re.sub(
        r"^(```|~~~)[^\n]*\n[\s\S]*?^\1\s*$",
        lambda m: _blank(m.group(0)),
        text,
        flags=re.M,
    )
    text = re.sub(r"`[^`\n]+`", lambda m: _blank(m.group(0)), text)
    text = re.sub(r"\bhttps?://\S+", lambda m: _blank(m.group(0)), text)
    text = re.sub(r"\]\([^\)\n]+\)", lambda m: _blank(m.group(0)), text)
    if ignore_quotes:
        text = re.sub(
            r"^[ \t]*>[^\n]*$",
            lambda m: _blank(m.group(0)),
            text,
            flags=re.M,
        )
    return text


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'’\-]*", text)


def _sentences(text: str) -> list[str]:
    return [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+|\n{2,}", text)
        if _words(part)
    ]


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _mattr(tokens: list[str], window: int = 50) -> float:
    if not tokens:
        return 0.0
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    values = (
        len(set(tokens[index : index + window])) / window
        for index in range(len(tokens) - window + 1)
    )
    return _mean(values)


def _trigram_repetition(tokens: list[str]) -> float:
    if len(tokens) < 3:
        return 0.0
    trigrams = [
        " ".join(tokens[index : index + 3])
        for index in range(len(tokens) - 2)
    ]
    return 1.0 - len(set(trigrams)) / len(trigrams)


def compute_stats(text: str) -> dict[str, Any]:
    """Compute the transparent structure metrics used by the audit score."""

    sentences = _sentences(text)
    sentence_lengths = [len(_words(sentence)) for sentence in sentences]
    tokens = [word.lower() for word in _words(text)]
    word_count = len(tokens)
    mean_length = _mean(sentence_lengths)
    stdev = statistics.pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0
    cov = stdev / mean_length if mean_length else 0.0
    return {
        "word_count": word_count,
        "sentence_count": len(sentences),
        "mean_sentence_length": round(mean_length, 3),
        "sentence_length_stdev": round(stdev, 3),
        "sentence_length_cov": round(cov, 3),
        "burstiness": round(cov, 3),
        "mattr": round(_mattr(tokens), 3),
        "trigram_repetition": round(_trigram_repetition(tokens), 3),
        "short_sample": word_count < 40,
    }


def _line_column(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    return line, index - line_start + 1


def _regex_flags(flag_string: str | None) -> int:
    flags = 0
    for flag in flag_string or "":
        if flag == "i":
            flags |= re.IGNORECASE
        elif flag == "m":
            flags |= re.MULTILINE
        elif flag == "s":
            flags |= re.DOTALL
        # JavaScript's g flag controls iteration and has no Python equivalent.
    return flags


def _findings_for(
    text: str,
    pattern: str,
    meta: dict[str, Any],
    *,
    flags: int = re.IGNORECASE,
) -> list[dict[str, Any]]:
    try:
        compiled = re.compile(pattern, flags)
    except re.error as exc:
        raise ValueError(f"invalid anti-slop rule {pattern!r}: {exc}") from exc
    found = []
    for match in compiled.finditer(text):
        line, column = _line_column(text, match.start())
        item = {
            **meta,
            "match": match.group(0).strip(),
            "line": line,
            "column": column,
            "start": match.start(),
            "end": match.end(),
        }
        found.append(item)
    return found


def _word_pattern(word: str) -> str:
    return rf"\b{re.escape(word)}\b"


def detect(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every rule match, with its exact source position."""

    findings: list[dict[str, Any]] = []
    vocabulary = rules.get("vocabulary", {})

    tier1 = vocabulary.get("tier1", {})
    for word in tier1.get("words", []):
        findings.extend(
            _findings_for(
                text,
                _word_pattern(word),
                {
                    "id": f"vocab:{word}",
                    "category": "vocabulary",
                    "tier": 1,
                    "weight": tier1.get("weight", 0),
                },
            )
        )

    tier2 = vocabulary.get("tier2", {})
    tier2_found: list[dict[str, Any]] = []
    for word in tier2.get("words", []):
        for item in _findings_for(text, _word_pattern(word), {"word": word}):
            tier2_found.append(item)
    distinct_tier2 = {item["word"].lower() for item in tier2_found}
    if len(distinct_tier2) >= tier2.get("minDistinct", 2):
        for item in tier2_found:
            findings.append(
                {
                    **{key: value for key, value in item.items() if key != "word"},
                    "id": f"vocab:{item['word']}",
                    "category": "vocabulary",
                    "tier": 2,
                    "weight": tier2.get("weight", 0),
                }
            )

    tier3 = vocabulary.get("tier3", {})
    tier3_found: list[dict[str, Any]] = []
    for word in tier3.get("words", []):
        for item in _findings_for(text, _word_pattern(word), {"word": word}):
            tier3_found.append(item)
    word_count = len(_words(text)) or 1
    density = len(tier3_found) / word_count * 100
    if density > tier3.get("maxDensityPct", 1.5):
        for item in tier3_found:
            findings.append(
                {
                    **{key: value for key, value in item.items() if key != "word"},
                    "id": f"vocab:{item['word']}",
                    "category": "vocabulary",
                    "tier": 3,
                    "weight": tier3.get("weight", 0),
                }
            )

    for phrase in rules.get("phrases", []):
        item = {
            "id": f"phrase:{phrase['match']}",
            "category": phrase.get("category", "phrase"),
            "weight": phrase.get("weight", 0),
        }
        if "fix" in phrase:
            item["fix"] = phrase["fix"]
        findings.extend(
            _findings_for(
                text,
                re.escape(phrase["match"]).replace("\\'", "['’]"),
                item,
            )
        )

    for rule in rules.get("regex", []):
        meta = {
            "id": rule["id"],
            "category": rule.get("category", "pattern"),
            "weight": rule.get("weight", 0),
        }
        if "note" in rule:
            meta["note"] = rule["note"]
        findings.extend(
            _findings_for(
                text,
                rule["pattern"],
                meta,
                flags=_regex_flags(rule.get("flags")),
            )
        )

    findings.sort(key=lambda item: (item["start"], item["end"], item["id"]))
    return findings


def _uniformity_score(stats: dict[str, Any]) -> float:
    score = 0.0
    burstiness = stats["burstiness"]
    mattr = stats["mattr"]
    repetition = stats["trigram_repetition"]
    if burstiness < 0.45:
        score += 40 * ((0.45 - burstiness) / 0.45)
    if 0 < mattr < 0.45:
        score += 30 * ((0.45 - mattr) / 0.45)
    if repetition > 0.04:
        score += 30 * min(1, (repetition - 0.04) / 0.1)
    if stats["word_count"] < 120:
        score *= stats["word_count"] / 120
    return min(100.0, score)


def _pattern_score(findings: list[dict[str, Any]], word_count: int) -> float:
    if not word_count:
        return 0.0
    weighted = sum(float(item.get("weight", 0)) for item in findings)
    per_100 = weighted / word_count * 100
    score = 34 * math.log1p(per_100)
    score += min(20, len({item["id"] for item in findings}) * 2)
    score += min(15, len({item["category"] for item in findings}) * 3)
    return min(100.0, score)


def verdict(score: int) -> str:
    if score <= 25:
        return "clean"
    if score <= 50:
        return "light"
    if score <= 75:
        return "moderate"
    return "heavy"


def audit_text(
    raw: str,
    rules: dict[str, Any],
    *,
    ignore_quotes: bool = False,
) -> dict[str, Any]:
    prepared = prepare_text(raw, ignore_quotes=ignore_quotes)
    stats = compute_stats(prepared)
    findings = detect(prepared, rules)
    pattern_score = _pattern_score(findings, stats["word_count"])
    uniformity_score = _uniformity_score(stats)
    score = round(0.7 * pattern_score + 0.3 * uniformity_score)
    word_count = stats["word_count"]
    confidence = "high" if word_count >= 120 else "medium" if word_count >= 40 else "low"
    return {
        "tool": "haipipe-writing/anti_slop.py",
        "rules_version": rules.get("version"),
        "score": score,
        "verdict": verdict(score) if word_count else "no-text",
        "diagnostic_only": True,
        "pattern_score": round(pattern_score),
        "uniformity_score": round(uniformity_score),
        "confidence": confidence,
        "stats": stats,
        "finding_count": len(findings),
        "findings": findings,
    }


def load_rules(path: str | Path | None = None) -> dict[str, Any]:
    rules_path = Path(path) if path else DEFAULT_RULES
    try:
        return json.loads(rules_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load anti-slop rules {rules_path}: {exc}") from exc


def _read_text(path: str | None) -> str:
    if not path or path == "-":
        return sys.stdin.read()
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def _normalize_date(match: str) -> str:
    iso = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", match)
    if iso:
        return f"{iso.group(1)}-{iso.group(2)}-{iso.group(3)}"
    lower = re.sub(r"\s+", " ", match.lower().replace(",", " ")).strip()
    month_first = re.fullmatch(r"([a-z]+) (\d{1,2}) (\d{4})", lower)
    if month_first and month_first.group(1) in MONTHS:
        return (
            f"{month_first.group(3)}-{MONTHS[month_first.group(1)]}-"
            f"{int(month_first.group(2)):02d}"
        )
    day_first = re.fullmatch(r"(\d{1,2}) ([a-z]+) (\d{4})", lower)
    if day_first and day_first.group(2) in MONTHS:
        return (
            f"{day_first.group(3)}-{MONTHS[day_first.group(2)]}-"
            f"{int(day_first.group(1)):02d}"
        )
    return lower


def _trim_url(match: str) -> str:
    value = re.sub(r"[.,;:!?]+$", "", match)
    while value.endswith(")"):
        if value.count(")") <= value.count("("):
            break
        value = re.sub(r"[.,;:!?]+$", "", value[:-1])
    return value


def _harvest(
    state: list[str],
    pattern: re.Pattern[str],
    normalize: Callable[[str], str | None],
) -> list[str]:
    found: list[str] = []

    def replace(match: re.Match[str]) -> str:
        value = normalize(match.group(0))
        if value is not None:
            found.append(value)
        return " " * len(match.group(0))

    state[0] = pattern.sub(replace, state[0])
    return found


def _unique(values: Iterable[str]) -> list[str]:
    return sorted(set(values))


def _normalize_citation(authors: str, year: str) -> str:
    authors = re.sub(r"\s+", " ", authors).strip(" ,")
    return f"{authors} {year.lower()}"


def _extract_citations(text: str) -> list[str]:
    citations = []
    for pattern in _CITATION_PATTERNS:
        citations.extend(
            _normalize_citation(match.group("authors"), match.group("year"))
            for match in pattern.finditer(text)
        )
    return _unique(citations)


def extract_facts(raw: str) -> dict[str, list[str]]:
    """Extract preservation-sensitive tokens in a deterministic order."""

    source = str(raw or "")
    state = [source]
    quoted_terms = [
        match
        for match in re.findall(r'"[^"\n]{2,80}"|\'[^\'\n]{2,80}\'', source)
        if re.search(r"[A-Za-z0-9]", match[1:-1])
    ]
    urls = _harvest(
        state,
        re.compile(r"https?://[^\s<>\[\]\"'`]+", re.IGNORECASE),
        _trim_url,
    )
    citations = _extract_citations(state[0])
    emails = _harvest(
        state,
        re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
        lambda match: match.lower(),
    )
    dates = _harvest(
        state,
        re.compile(
            r"\b\d{4}-\d{2}-\d{2}\b"
            r"|\b(?:january|february|march|april|may|june|july|august|"
            r"september|october|november|december)\s+\d{1,2},?\s+\d{4}\b"
            r"|\b\d{1,2}\s+(?:january|february|march|april|may|june|july|"
            r"august|september|october|november|december)\s+\d{4}\b",
            re.IGNORECASE,
        ),
        _normalize_date,
    )
    percentages = _harvest(
        state,
        re.compile(r"\b\d+(?:\.\d+)?\s?%"),
        lambda match: re.sub(r"\s+", "", match),
    )
    versions = _harvest(
        state,
        re.compile(r"\bv\d+(?:\.\d+)+\b|\b\d+(?:\.\d+){2,}\b", re.IGNORECASE),
        lambda match: re.sub(r"^v", "", match, flags=re.IGNORECASE),
    )
    numbers = _harvest(
        state,
        re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\b\d+(?:\.\d+)?\b"),
        lambda match: match.replace(",", ""),
    )
    acronyms = _harvest(
        state,
        re.compile(r"\b[A-Z][A-Z0-9]+\b"),
        lambda match: None if match in ACRONYM_STOPWORDS else match,
    )
    return {
        "urls": _unique(urls),
        "emails": _unique(emails),
        "dates": _unique(dates),
        "percentages": _unique(percentages),
        "versions": _unique(versions),
        "numbers": _unique(numbers),
        "acronyms": _unique(acronyms),
        "citations": citations,
        "quoted_terms": _unique(quoted_terms),
    }


def _facts_in_urls(facts: dict[str, list[str]]) -> dict[str, list[str]]:
    nested = {kind: [] for kind in FACT_KINDS}
    for url in facts["urls"]:
        inner = extract_facts(re.sub(r"^https?://", " ", url, flags=re.IGNORECASE))
        for kind in FACT_KINDS:
            nested[kind].extend(inner[kind])
    return {kind: _unique(values) for kind, values in nested.items()}


def compare_facts(before_text: str, after_text: str) -> dict[str, Any]:
    """Report tokens present before but absent after a rewrite."""

    before = extract_facts(before_text)
    after = extract_facts(after_text)
    nested = _facts_in_urls(after)
    missing: dict[str, list[str]] = {}
    added: dict[str, list[str]] = {}
    for kind in FACT_KINDS:
        present = set(after[kind]) | set(nested[kind])
        for sibling in FACT_SIBLINGS.get(kind, ()):
            present.update(after[sibling])
            present.update(nested[sibling])
        lost = [value for value in before[kind] if value not in present]
        new = [value for value in after[kind] if value not in set(before[kind])]
        if lost:
            missing[kind] = lost
        if new:
            added[kind] = new
    critical_kinds = {
        "urls",
        "emails",
        "dates",
        "percentages",
        "versions",
        "numbers",
        "citations",
    }
    critical_missing = sum(
        len(values) for kind, values in missing.items() if kind in critical_kinds
    )
    return {
        "ok": not missing,
        "missing": missing,
        "added": added,
        "critical_missing_count": critical_missing,
        "review_required": bool(missing),
        "counts": {
            "before": sum(len(values) for values in before.values()),
            "after": sum(len(values) for values in after.values()),
        },
    }


def _print_audit(result: dict[str, Any]) -> None:
    stats = result["stats"]
    print(
        f"anti_slop_score: {result['score']}/100  {result['verdict']} "
        "(diagnostic only)"
    )
    print(
        f"pattern: {result['pattern_score']}  "
        f"uniformity: {result['uniformity_score']}  "
        f"confidence: {result['confidence']}"
    )
    print(
        f"words: {stats['word_count']}  sentences: {stats['sentence_count']}  "
        f"findings: {result['finding_count']}"
    )
    for finding in result["findings"]:
        detail = ""
        if finding.get("fix") is not None:
            detail = f" -> {finding['fix']!r}"
        elif finding.get("note"):
            detail = f" ({finding['note']})"
        print(
            f"  L{finding['line']}:{finding['column']} "
            f"[{finding['category']}/{finding['id']}] "
            f"{finding['match']!r}{detail}"
        )


def _print_compare(result: dict[str, Any]) -> None:
    print(f"facts_ok: {str(result['ok']).lower()}")
    print(f"critical_missing_count: {result['critical_missing_count']}")
    print(f"review_required: {str(result['review_required']).lower()}")
    for kind, values in result["missing"].items():
        print(f"missing_{kind}: {', '.join(values)}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="find AI-writing tells")
    audit.add_argument("file", nargs="?", default="-", help="file, or stdin")
    audit.add_argument("--format", choices=("text", "json"), default="text")
    audit.add_argument("--rules", default=str(DEFAULT_RULES))
    audit.add_argument("--ignore-quotes", action="store_true")
    audit.add_argument(
        "--fail-above",
        type=int,
        default=None,
        help="exit 1 when the diagnostic score is at least N",
    )

    compare = subparsers.add_parser("compare", help="compare preservation-sensitive facts")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
    compare.add_argument("--format", choices=("text", "json"), default="text")
    compare.add_argument(
        "--check-facts",
        action="store_true",
        help="exit 1 when a before-token is missing after the rewrite",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "audit":
            result = audit_text(
                _read_text(args.file),
                load_rules(args.rules),
                ignore_quotes=args.ignore_quotes,
            )
            if args.format == "json":
                print(json.dumps(result, indent=2, sort_keys=True))
            else:
                _print_audit(result)
            if args.fail_above is not None and result["score"] >= args.fail_above:
                return 1
            return 0

        result = compare_facts(_read_text(args.before), _read_text(args.after))
        if args.format == "json":
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            _print_compare(result)
        return 1 if args.check_facts and not result["ok"] else 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
