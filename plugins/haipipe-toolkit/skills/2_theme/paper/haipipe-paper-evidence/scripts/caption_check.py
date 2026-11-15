#!/usr/bin/env python3
"""Is each display's caption short? (JL 261103: "for the Figure caption, do not add so much things, don't be too
long"; the caption rule, haipipe-display ref/display-revise-loop.md.) For each Task of a display Job it reads the newest
Run's result/float.tex and counts the words of the title (the caption's leading \\textbf{...}) and of the legend (the
rest). Prints one line per display; exit 1 when any is over. It changes no file.
It also checks each display's message (V6, JL 261104: "把这个加 message 也写到对应的 skill 里 ... 当做一个 checklist"): the same Run's
method.md opens with a ## Message of 1 to 3 sentences; a display with none, or a longer one, fails too.

    python caption_check.py <paper>/j01_evidence_display [--legend 75] [--table-legend 120] [--title 15]

And each caption's cross-references (M-D12): every "Figure N", "Table N", "Extended Data Fig. N" a caption names is a
display the current numbering has (each Task face's `label:`); a mismatch is named and fails.

A venue's limit wins over these defaults: `at most N words` in the caption row of the Board's venues/<venue>/call.md, or --legend.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LEGEND, TABLE_LEGEND, TITLE = 75, 120, 15
SENTENCES = 3


def _braced(text: str, start: int) -> str:
    """The text inside the brace group that opens at text[start]."""
    depth = 0
    for i in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return text[start + 1:i]
    return text[start + 1:]


def _words(tex: str) -> int:
    plain = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", tex)
    return len(re.findall(r"\S*[A-Za-z0-9]\S*", plain.replace("{", " ").replace("}", " ")))


def caption_words(float_tex: str):
    """(title words, legend words, is a table) of one float.tex; None when it holds no caption."""
    m = re.search(r"\\caption(\[[^\]]*\])?\{", float_tex)
    if not m:
        return None
    body = _braced(float_tex, m.end() - 1)
    t = re.match(r"\s*\\textbf\{", body)
    title = _braced(body, t.end() - 1) if t else ""
    legend = body[t.end() + len(title) + 1:] if t else body
    return _words(title), _words(legend), bool(re.search(r"\\begin\{table", float_tex))


def newest_float(task: Path):
    """The newest Run's float.tex of a display Task, by Run number."""
    found = sorted(task.glob("runs/r[0-9]*/result/float.tex"), key=lambda p: p.parts[-3])
    return found[-1] if found else None


def venue_limit(job: Path):
    """The legend limit in the caption row of the Board's venues/<venue>/call.md, else None (JL 261104: "let's follow the venue")."""
    for call in sorted(job.parent.glob("venues/*/call.md")):
        m = re.search(r"(?m)^\|\s*caption\s*\|.*?at most (\d+) words", call.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return int(m.group(1))
    return None


def check(job: Path, legend: int = None, table_legend: int = TABLE_LEGEND, title: int = TITLE) -> list:
    """One row per display Task with a drawn caption: (task, run, title words, legend words, limit, over)."""
    legend = legend or venue_limit(job) or LEGEND
    rows = []
    for task in sorted(t for t in job.glob("t[0-9]*_*") if t.is_dir()):
        f = newest_float(task)
        got = caption_words(f.read_text(encoding="utf-8", errors="ignore")) if f else None
        if got is None:
            continue
        ti, le, is_table = got
        limit = table_legend if is_table else legend
        rows.append((task.name, f.parts[-3], ti, le, limit, ti > title or le > limit))
    return rows


def message_sentences(method_md: str) -> int:
    """How many sentences the ## Message part of a method.md holds; 0 when it has none."""
    m = re.search(r"(?ms)^##\s*Message\s*\n(.*?)(?=^##\s|\Z)", method_md)
    return len(re.findall(r"[.!?](?:\s|$)", m.group(1).strip())) or int(bool(m.group(1).strip())) if m else 0


def messages(job: Path) -> list:
    """One row per drawn display Task: (task, run, sentences, problem or ""), for the newest Run that drew a float."""
    rows = []
    for task in sorted(t for t in job.glob("t[0-9]*_*") if t.is_dir()):
        f = newest_float(task)
        if f is None:
            continue
        method = f.parent / "method.md"
        n = message_sentences(method.read_text(encoding="utf-8", errors="ignore")) if method.is_file() else 0
        rows.append((task.name, f.parts[-3], n, "no ## Message" if n == 0 else f"{n} sentences, at most {SENTENCES}" if n > SENTENCES else ""))
    return rows


# ── cross-references (haipipe-paper ref/must-check.md M-D12) ────────────────────────────────────────────────────────
# A caption that names "Figure 2 and Table 1" must name displays the current numbering has; the numbering is each
# display Task face's `label:` (Figure 4, Extended Data Figure 1, Extended Data Table 2), its caption the float.tex of
# the Run the face says is `printed:` (else the newest Run).
REF = re.compile(r"\b(Extended\s+Data\s+|Supplementary\s+)?(Fig(?:ure)?s?\.?|Tables?)\s+(\d+)((?:\s*(?:,|and|to|–|-)\s*\d+)*)")


def _key(ed: str, word: str, n: int) -> str:
    kind = "Table" if word.lower().startswith("table") else "Figure"
    return ("Extended Data " if ed and ed.strip().lower().startswith("extended") else "") + f"{kind} {n}"


def refs(text: str) -> list:
    """Every display a text names, as 'Figure 2', 'Table 1', 'Extended Data Figure 3' (a range or list expanded);
    a Supplementary one is left out."""
    t = re.sub(r"~|\\[ ,]", " ", text)
    out = []
    for m in REF.finditer(t):
        if m.group(1) and m.group(1).strip().lower().startswith("supplementary"):
            continue
        nums, prev, ranged = [int(m.group(3))], int(m.group(3)), False
        for sep, n in re.findall(r"(,|and|to|–|-)\s*(\d+)", m.group(4) or ""):
            n = int(n)
            nums += list(range(prev + 1, n + 1)) if sep in ("to", "–", "-") and n > prev else [n]
            prev = n
        out += [_key(m.group(1) or "", m.group(2), n) for n in nums]
    return out


def numbering(job: Path) -> dict:
    """{'Figure 4': task name} from each display Task face's `label:`."""
    have = {}
    for task in sorted(t for t in job.glob("t[0-9]*_*") if t.is_dir()):
        face = task / f"{task.name}.md"
        m = re.search(r"(?m)^label:\s*(.+)$", face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else None
        got = refs(m.group(1).split("·")[0]) if m else []
        if got:
            have[got[0]] = task.name
    return have


def printed_float(task: Path):
    face = task / f"{task.name}.md"
    m = re.search(r"(?m)^printed:\s*(\S+)", face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else None
    f = task / "runs" / m.group(1) / "result" / "float.tex" if m else None
    return f if f and f.is_file() else newest_float(task)


def caption_text(float_tex: str) -> str:
    m = re.search(r"\\caption(\[[^\]]*\])?\{", float_tex)
    return _braced(float_tex, m.end() - 1) if m else ""


def cross_refs(job: Path) -> list:
    """One row per caption reference the numbering lacks: (task, run, the reference)."""
    have = numbering(job)
    rows = []
    for task in sorted(t for t in job.glob("t[0-9]*_*") if t.is_dir()):
        f = printed_float(task)
        if f is None:
            continue
        for ref in dict.fromkeys(refs(caption_text(f.read_text(encoding="utf-8", errors="ignore")))):
            if ref not in have:
                rows.append((task.name, f.parts[-3], ref))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("job", type=Path)
    ap.add_argument("--legend", type=int, default=None)
    ap.add_argument("--table-legend", type=int, default=TABLE_LEGEND)
    ap.add_argument("--title", type=int, default=TITLE)
    a = ap.parse_args()
    rows = check(a.job, a.legend, a.table_legend, a.title)
    for task, run, ti, le, limit, over in rows:
        print(f"{'❗' if over else '✅'} {task} · {run}: title {ti}/{a.title}, legend {le}/{limit} words")
    bad = sum(r[-1] for r in rows)
    print(f"{len(rows) - bad} of {len(rows)} captions short enough")
    said = messages(a.job)
    for task, run, _n, problem in said:
        if problem:
            print(f"❗ {task} · {run}: {problem}")
    missing = sum(bool(r[-1]) for r in said)
    print(f"{len(said) - missing} of {len(said)} displays say their message")
    wrong = cross_refs(a.job)
    for task, run, ref in wrong:
        print(f"❗ {task} · {run}: the caption names {ref}, which the current numbering does not have")
    print(f"captions name only displays that exist: {'no' if wrong else 'yes'}")
    return 1 if bad or missing or wrong else 0


if __name__ == "__main__":
    sys.exit(main())
