"""bbl_labels.py: the author-date citation labels LaTeX itself printed, read from master.bbl, so the Word copy cites
as the PDF does: "(Lu & Rui, 2018)", "(Centers for Medicare & Medicaid Services, 2026a, 2026b)" (Pp-AgreeableRx 261122:
the Word file printed "Lu and Rui" and the same author twice with no year letters).
latex_parse.py runs this file inside its own namespace (_load_part), so MASTER, LATEX_ROOM, BIB and latex_to_text
come from there. Without a .bbl (a Word-only build) the labels fall back to author_date_label's own reading."""
from __future__ import annotations

import re

_LABELS: dict[str, tuple[str, str, str]] | None = None   # key -> (parenthetical who, narrative who, year)


def _group(text: str, at: int) -> tuple[str, int]:
    """The {...} group that opens at or after text[at], and the index after it."""
    at = text.index("{", at)
    depth, k = 0, at
    while k < len(text):
        depth += (text[k] == "{") - (text[k] == "}")
        k += 1
        if depth == 0:
            break
    return text[at + 1:k - 1], k


def _apa_text(value: str, amp: str) -> str:
    value = value.replace("%\n", "").replace("\\protect", "")
    value = re.sub(r"\\BBA\s*\{\}", amp, value)
    value = re.sub(r"\\BOthers\s*\{\.\}", "et al.", value)
    value = re.sub(r"\\BCBL\s*\{\}", ",", value)
    value = re.sub(r"\\BCnt\s*\{(\d+)\}", lambda m: chr(96 + int(m.group(1))), value)
    value = re.sub(r"\\APAC(?:year|exlab)\s*", "", value)
    value = value.replace("\\ ", " ").replace("\\&", "&")
    value = re.sub(r"[{}%]", "", value)
    return re.sub(r"\s+", " ", value).replace(" ,", ",").strip()


def bbl_cite_labels() -> dict[str, tuple[str, str, str]]:
    global _LABELS
    if _LABELS is not None:
        return _LABELS
    _LABELS = {}
    bbl = next((p for p in (MASTER.with_suffix(".bbl"), LATEX_ROOM / "master.bbl") if p.is_file()), None)
    if bbl is None:
        return _LABELS
    text = bbl.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\\bibitem\s*\[", text):
        start = m.end()
        if text.startswith("\\protect \\citeauthoryear", start) or text.startswith("\\protect\\citeauthoryear", start):
            _long, k = _group(text, start)          # apacite: {long names}{short names}{year}
            short, k = _group(text, k)
            year, k = _group(text, k)
            close = text.index("]", k)
            key, _ = _group(text, close)
            _LABELS[key.replace("%", "").strip()] = (_apa_text(short, "&"), _apa_text(short, "and"),
                                                    _apa_text(year, "").replace(" ", ""))
            continue
        close, depth = start, 0                     # natbib: [Short(Year)Long] or [{Short}(Year){Long}]
        while close < len(text) and not (text[close] == "]" and depth == 0):
            depth += (text[close] == "{") - (text[close] == "}")
            close += 1
        label = text[start:close]
        key, _ = _group(text, close)
        nm = re.match(r"\s*\{?(.*?)\}?\s*\(([^()]*)\)", label, re.S)
        if nm:   # INFORMS (informs2014.bst) writes "and" as \protect\BIBand{}, which latex_to_text would drop
            raw = re.sub(r"(?:\\protect\s*)?\\BIBand\s*\{\}", "and", nm.group(1))
            who = re.sub(r"\s+", " ", latex_to_text(raw)).strip()
            _LABELS[key.replace("%", "").strip()] = (who, who, nm.group(2).strip())
    return _LABELS


def cite_label(key: str, narrative: bool = False) -> tuple[str, str]:
    """(who, year) for one key: LaTeX's own label when the .bbl has it, else author_date_label's."""
    found = bbl_cite_labels().get(key)
    if found:
        return (found[1] if narrative else found[0]), found[2]
    who, _, year = author_date_label(key).rpartition(", ")
    return who, year


def author_date_group(keys: list[str]) -> str:
    """One parenthetical citation; the same author's works share one name: "CMS, 2026a, 2026b"."""
    parts: list[list[str]] = []
    for key in keys:
        who, year = cite_label(key)
        if parts and parts[-1][0] == who and who:
            parts[-1].append(year)
        else:
            parts.append([who, year])
    return "; ".join(", ".join(x for x in [p[0]] + sorted(p[1:]) if x) for p in parts)   # 2026a before 2026b, as the PDF
