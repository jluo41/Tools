"""Is the co-authors' Word file the same as the build? One compare command (AgreeableJama-Board 261122).

    python word_compare.py <theirs.docx> <build.docx>     sentence and table-cell diff by section
    python word_compare.py <theirs.docx> <build.pdf>      every Word sentence and cell looked up in the PDF's text
    python word_compare.py <theirs.docx> <build.pdf> --reverse   also: PDF sentences not in the Word file (rough)
    python word_compare.py <file.docx> --citations        only: citation numbers in order of first citation?
    ... --out report.md                                   write the report there instead of printing it

Word's accepted view is read: deleted text is dropped, inserted text kept, equations (OMML) read as their text.
Both sides are folded before they are compared: Unicode NFKC (so a PDF's U+037E Greek question mark is a ";"),
curly quotes and dashes made plain, and for the PDF line breaks, hyphenation and punctuation folded away. A
sentence not found as it is is tried again with its digits ignored (a citation number that differs), then as its
pieces in order (a superscript mark the PDF prints elsewhere on the line). Numbered citations (superscript runs or
[n] brackets) in the main text are checked against the order of first citation, as AMA style requires.
Reads files only; it writes nothing but --out.
"""
from __future__ import annotations

import argparse
import difflib
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
SUP_ON, SUP_OFF = "\x10", "\x11"          # a superscript run, kept marked until the text is compared
REFERENCES = re.compile(r"^(references|bibliography|works cited|literature cited)$", re.I)
PLAIN = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-",
                       "\u2212": "-", "\u00a0": " ", "\u2009": " ", "\u202f": " "})


def plain(text: str) -> str:
    """NFKC (U+037E becomes ';', ligatures split) with curly quotes, dashes and odd spaces made plain."""
    return unicodedata.normalize("NFKC", text).translate(PLAIN)


def unmark(text: str) -> str:
    return text.replace(SUP_ON, "").replace(SUP_OFF, "")


# ── reading a .docx ───────────────────────────────────────────────────────────
def _style_names(z: zipfile.ZipFile) -> dict[str, str]:
    if "word/styles.xml" not in z.namelist():
        return {}
    root = ET.fromstring(z.read("word/styles.xml"))
    out = {}
    for s in root.iter(W + "style"):
        name = s.find(W + "name")
        out[s.get(W + "styleId") or ""] = (name.get(W + "val") if name is not None else "") or ""
    return out


def _superscript(run: ET.Element) -> bool:
    rpr = run.find(W + "rPr")
    va = rpr.find(W + "vertAlign") if rpr is not None else None
    return va is not None and va.get(W + "val") == "superscript"


def _para_text(p: ET.Element) -> str:
    out: list[str] = []

    def walk(e: ET.Element) -> None:
        for c in e:
            if c.tag in (W + "del", W + "moveFrom", W + "delText"):
                continue
            if c.tag == W + "r":
                sup = _superscript(c)
                text = "".join((t.text or "") if t.tag == W + "t" else " " for t in c
                               if t.tag in (W + "t", W + "tab", W + "br"))
                out.append(SUP_ON + text + SUP_OFF if sup and text.strip() else text)
            elif c.tag == M + "t":
                out.append(c.text or "")
            elif c.tag == W + "pPr":
                continue
            else:
                walk(c)
    walk(p)
    return " ".join(plain("".join(out)).split())


def paragraphs(path: Path) -> list[dict]:
    """Each paragraph of the accepted view: {text, cell, heading}; text keeps superscripts marked."""
    with zipfile.ZipFile(path) as z:
        names = _style_names(z)
        body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    cells = {id(p) for t in body.iter(W + "tbl") for p in t.iter(W + "p")}
    out = []
    for p in body.iter(W + "p"):
        text = _para_text(p)
        if not text:
            continue
        ppr = p.find(W + "pPr")
        sid = ppr.find(W + "pStyle").get(W + "val") if ppr is not None and ppr.find(W + "pStyle") is not None else ""
        style = names.get(sid, sid).lower()
        bare = unmark(text)
        heading = id(p) not in cells and (style.startswith("heading") or
                                          (bare.isupper() and len(bare.split()) <= 6 and len(bare) > 3))
        out.append({"text": text, "cell": id(p) in cells, "heading": bool(heading)})
    return out


SENT_END = re.compile(r"(?<=[.?!])(?:\x10[^\x11]*\x11)?\s+(?=[A-Z(\"'])")


def sentences(text: str) -> list[str]:
    """A paragraph cut at sentence ends; a citation mark right after the stop stays with its sentence."""
    out, pos = [], 0
    for m in SENT_END.finditer(text):
        end = m.start() + len(m.group(0).rstrip())
        out.append(text[pos:end].strip())
        pos = m.end()
    out.append(text[pos:].strip())
    return [s for s in out if s]


def units(path: Path) -> list[tuple[str, str, str]]:
    """(section, kind, text) for every sentence ("s") and table cell ("cell"); kind "head" for a heading."""
    sec, out = "Front matter", []
    for p in paragraphs(path):
        if p["heading"]:
            sec = unmark(p["text"]).title()
            out.append((sec, "head", p["text"]))
            continue
        if p["cell"]:
            out.append((sec, "cell", p["text"]))
            continue
        out += [(sec, "s", s) for s in sentences(p["text"])]
    return out


# ── folding for comparison ────────────────────────────────────────────────────
def fold(s: str, digits: bool = True) -> str:
    s = unicodedata.normalize("NFKD", plain(unmark(s))).lower()
    return re.sub(r"[^a-z0-9]" if digits else r"[^a-z]", "", s)


def no_marks(s: str) -> str:
    """The sentence with its superscript runs taken out (citation numbers, footnote letters)."""
    return re.sub(r"\x10[^\x11]*\x11", " ", s)


def pieces(s: str) -> list[str]:
    """The sentence's folded text between its superscripts and digits: what must appear, in order."""
    return [f for f in (fold(x, False) for x in re.split(r"\x10[^\x11]*\x11|\d+", s)) if len(f) >= 4]


def in_order(parts: list[str], hay: str, gap: int = 40) -> bool:
    """Every piece found, each within `gap` letters after the one before it."""
    return bool(parts) and any(_chain(parts, hay, j, gap) for j in _all(hay, parts[0]))


def _all(hay: str, needle: str):
    k = hay.find(needle)
    while k >= 0:
        yield k
        k = hay.find(needle, k + 1)


def _chain(parts: list[str], hay: str, at: int, gap: int) -> bool:
    start = at + len(parts[0])
    for part in parts[1:]:
        k = hay.find(part, start)
        if k < 0 or k - start > gap:
            return False
        start = k + len(part)
    return True


def pdf_text(pdf: Path) -> str:
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext is not installed (poppler)")
    txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    lines = [l for l in txt.replace("\f", "\n").split("\n") if not re.fullmatch(r"\s*\d{1,3}\s*", l)]
    joined = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", "\n".join(lines))     # hyphenation at a line end
    return plain(" ".join(joined.split()))


# ── citation order (AMA: numbered in the order first cited) ───────────────────
CITE_SUP = re.compile(r"(\S?)\x10\s*([\d,\s\-]+?)\s*\x11")
CITE_BRACKET = re.compile(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]")


def _expand(group: str) -> list[int]:
    out = []
    for part in re.split(r"\s*,\s*", group.strip()):
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m and int(m.group(1)) <= int(m.group(2)) <= int(m.group(1)) + 50:
            out += range(int(m.group(1)), int(m.group(2)) + 1)
        elif part.isdigit():
            out.append(int(part))
    return out


def citations(path: Path) -> list[tuple[int, str, str]]:
    """(number, section, words before it) for each numbered citation in the main text, in reading order:
    from the first heading to the references heading; table cells and the title page are left out."""
    sec, started, out = "", False, []
    for p in paragraphs(path):
        bare = unmark(p["text"]).strip()
        if p["heading"]:
            if REFERENCES.match(bare):
                break
            sec, started = bare.title(), True
            continue
        if not started or p["cell"]:
            continue
        text = p["text"].replace("\u2013", "-")
        for m in sorted(list(CITE_SUP.finditer(text)) + list(CITE_BRACKET.finditer(text)), key=lambda m: m.start()):
            before = unmark(text[:m.start() + len(m.group(1)) if m.re is CITE_SUP else m.start()])
            words = before.split()
            if m.re is CITE_SUP and m.group(1).isalnum() and words and len(words[-1]) == 1:
                continue                                      # R², x²: a power; "(Supplement 1)²³" is a citation
            for n in _expand(m.group(2) if m.re is CITE_SUP else m.group(1)):
                out.append((n, sec, " ".join(words[-4:])))
    return out


def is_supplement(path: Path) -> bool:
    """A supplement file: its name or its title lines say so (its numbers follow the main text's list)."""
    top = []
    for p in paragraphs(path):                       # the title lines: up to and including the first heading
        top.append(unmark(p["text"]))
        if p["heading"]:
            break
    top = " ".join(top)
    return bool(re.search(r"supplement|esupp", path.stem + " " + top, re.I))


def citation_order(path: Path) -> list[str]:
    """Lines naming each reference first cited after a higher number, and the numbers never cited in the text.
    One reference cited early or late flags only itself, not every number after it."""
    if is_supplement(path):
        return ["not checked: a supplement reuses the main text's reference numbers"]
    first: dict[int, tuple[str, str]] = {}
    for n, sec, near in citations(path):
        first.setdefault(n, (sec, near))
    order = list(first)
    lines = []
    for i, n in enumerate(order):
        higher = [m for m in order[:i] if m > n]
        if higher:
            sec, near = first[n]
            lines.append(f"- {n} is first cited after {', '.join(map(str, higher))} ({sec}: \"{near}{n}\")")
    if lines:
        lines.insert(0, "citation numbers not in order of first citation:")
    gaps = [n for n in range(1, max(order, default=0) + 1) if n not in first]
    if gaps:
        lines.append("not found cited in the main text by this tool (a table or figure note, or a form it misses, may cite it): " + ", ".join(map(str, gaps)))
    return lines


# ── the two comparisons ───────────────────────────────────────────────────────
def word_vs_word(a: Path, b: Path) -> tuple[dict, list[str]]:
    ua, ub = units(a), units(b)
    key = lambda u: fold(u[2], False) if u[1] != "head" else fold(u[2])
    A, B = [key(u) for u in ua], [key(u) for u in ub]
    stats: dict[str, list[int]] = {}
    out: list[str] = []
    bump = lambda sec, i: stats.setdefault(sec, [0, 0, 0, 0]).__setitem__(i, stats[sec][i] + 1)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i1, i2):
                if ua[k][1] != "head":
                    bump(ua[k][0], 0)
                if unmark(ua[k][2]) != unmark(ub[j1 + k - i1][2]) and ua[k][1] != "head":
                    what = "digits differ" if fold(ua[k][2]) != fold(ub[j1 + k - i1][2]) else "case or punctuation differ"
                    out.append(f"\n### {ua[k][0]} · {what} ({ua[k][1]})\n"
                               f"- {a.name}: {unmark(ua[k][2])}\n- {b.name}: {unmark(ub[j1 + k - i1][2])}")
            continue
        olds, news, used = ua[i1:i2], ub[j1:j2], set()
        for o in olds:
            best, bi = 0.0, None
            for n_i, n in enumerate(news):
                if n_i not in used:
                    r = difflib.SequenceMatcher(None, key(o), key(n)).ratio()
                    if r > best:
                        best, bi = r, n_i
            if bi is not None and best >= 0.5:
                used.add(bi)
                bump(o[0], 1)
                out.append(f"\n### {o[0]} · changed ({o[1]}, {best:.2f})\n- {a.name}: {unmark(o[2])}\n"
                           f"- {b.name}: {unmark(news[bi][2])}")
            else:
                bump(o[0], 2)
                out.append(f"\n### {o[0]} · only in {a.name} ({o[1]})\n- {unmark(o[2])}")
        for n_i, n in enumerate(news):
            if n_i not in used:
                bump(n[0], 3)
                out.append(f"\n### {n[0]} · only in {b.name} ({n[1]})\n- {unmark(n[2])}")
    return {"columns": ["same", "changed", f"only {a.name}", f"only {b.name}"], "rows": stats}, out


def word_vs_pdf(a: Path, pdf: Path, reverse: bool = False) -> tuple[dict, list[str]]:
    text = pdf_text(pdf)
    hay, hay_letters = fold(text), fold(text, False)
    stats: dict[str, list[int]] = {}
    out: list[str] = []
    for sec, kind, s in units(a):
        if kind == "head":
            continue
        f = fold(s)
        if len(fold(s, False)) < (2 if kind == "cell" else 12):
            continue
        row = stats.setdefault(sec, [0, 0, 0, 0])
        if f in hay:
            row[0] += 1
        elif fold(s, False) in hay_letters:
            row[1] += 1
            out.append(f"\n### {sec} · digits differ ({kind})\n- {unmark(s)}")
        elif fold(no_marks(s)) in hay or in_order(pieces(s), hay_letters):
            row[2] += 1
            out.append(f"\n### {sec} · same words, a mark placed elsewhere ({kind})\n- {unmark(s)}")
        else:
            row[3] += 1
            out.append(f"\n### {sec} · not found in the PDF ({kind})\n- {unmark(s)}")
    if reverse:
        word_all = fold(" ".join(p["text"] for p in paragraphs(a)))
        pdf_sents = [x for x in re.split(r"(?<=[.?!])\s+(?=[A-Z(])", text) if len(fold(x)) >= 25]
        missing = [x for x in pdf_sents if fold(x) not in word_all]
        out.append(f"\n## PDF sentences not found in {a.name} (rough: pdftotext glues captions and cells to "
                   f"their neighbours)\n" + "\n".join(f"- {x[:220]}" for x in missing))
    return {"columns": ["same", "digits differ", "mark elsewhere", "not found"], "rows": stats}, out


def table(stats: dict) -> list[str]:
    cols = stats["columns"]
    lines = ["| Section | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
    for sec, v in stats["rows"].items():
        lines.append(f"| {sec} | " + " | ".join(str(x) for x in v) + " |")
    total = [sum(v[i] for v in stats["rows"].values()) for i in range(len(cols))]
    lines.append("| **All** | " + " | ".join(f"**{x}**" for x in total) + " |")
    return lines


def report(a: Path, b: Path | None, *, reverse: bool = False, citations_only: bool = False) -> str:
    lines = [f"# {a.name}" + (f" against {b.name}" if b else ": citation order"), ""]
    if not citations_only and b is not None:
        stats, diffs = word_vs_pdf(a, b, reverse) if b.suffix.lower() == ".pdf" else word_vs_word(a, b)
        lines += ["## By section", ""] + table(stats) + ["", "## Differences"] + (diffs or ["", "none"]) + [""]
    for path in [a] + ([b] if b is not None and b.suffix.lower() == ".docx" and not citations_only else []):
        found = citation_order(path)
        lines += [f"## Citation order · {path.name}", ""] + (found or ["in order of first citation"]) + [""]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("theirs", type=Path, help="the co-authors' .docx")
    ap.add_argument("build", type=Path, nargs="?", help="the build: a .docx or a .pdf")
    ap.add_argument("--citations", action="store_true", help="only the citation-order check")
    ap.add_argument("--reverse", action="store_true", help="with a PDF: also list PDF sentences not in the Word file")
    ap.add_argument("--out", type=Path, help="write the report here")
    a = ap.parse_args(argv)
    if a.build is None and not a.citations:
        ap.error("give the build (.docx or .pdf), or --citations")
    text = report(a.theirs, a.build, reverse=a.reverse, citations_only=a.citations)
    if a.out:
        a.out.write_text(text, encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
