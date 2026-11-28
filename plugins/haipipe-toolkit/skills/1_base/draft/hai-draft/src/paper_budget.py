"""A paper version's shared main-text word budget (hai-paper ref/must-check.md M-D11).

A venue caps the main text, not one Section: NMI counts the Introduction, Results and Discussion together against
3,500 words. The cap and what counts are read from the Board's `venues/<venue>/call.md` row `| words | up to N |
<what counts> |`; the version Job's `venue:` names the venue (else the Board's one call.md). The Sections are the
version's compile order (the `haipipe:compile-order` block, the same one hai-paper-evidence paper_text.py and
the delivery build read), else its Task folders in order. Each Section's words are its newest Draft's `## 3 · Draft`
(src/page_structure.py). `page.py structure <job>` prints the line; `page.py health <job>` WARNs when the sum is over
the cap and names who grew since their previous Draft.
"""
from __future__ import annotations

import re
from pathlib import Path

TASK = re.compile(r"^t(\d+)_")
KINDS = ("introduction", "background", "results", "discussion", "conclusion", "conclusions", "methods",
         "abstract", "summary")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


def compile_order(job: Path) -> list:
    m = re.search(r"(?s)<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->",
                  _read(job / f"{job.name}.md"))
    return re.findall(r"(?m)^\s*-\s*(t\d+_[\w.-]+)", m.group(1)) if m else []


def job_sections(job: Path) -> list:
    """The version's Section Tasks in compile order, then any Task folder the order leaves out (letters)."""
    every = sorted((p for p in job.iterdir() if p.is_dir() and TASK.match(p.name)),
                   key=lambda p: (int(TASK.match(p.name).group(1)), p.name))
    order = [job / n for n in compile_order(job) if (job / n).is_dir()]
    return order + [t for t in every if t not in order] if order else every


def venue_call(job: Path) -> Path | None:
    board = next((p for p in [job, *job.parents] if (p / "board.md").is_file()), None)
    if board is None:
        return None
    calls = sorted((board / "venues").glob("*/call.md"))
    head = _read(job / f"{job.name}.md") + "\n" + _read(board / "board.md")
    m = re.search(r"(?m)^venue:\s*(.+?)\s*$", head)
    want = re.sub(r"[^a-z0-9]+", "-", m.group(1).lower()).strip("-") if m else ""
    hit = next((c for c in calls if want and (c.parent.name.lower() == want or want in c.parent.name.lower())), None)
    return hit or (calls[0] if len(calls) == 1 else None)


def word_cap(call_text: str) -> tuple:
    """(cap, kinds that count) from a `| words | up to N | counts |` row; (None, ()) without one."""
    m = re.search(r"(?mi)^\|\s*words\s*\|\s*(?:up to|not more than|at most|maximum)?\s*([\d,]+)[^|]*\|([^|\n]*)", call_text)
    if not m:
        return None, ()
    counts = re.split(r";|\bnot\b|\bexcluding\b", m.group(2), maxsplit=1)[0].lower()
    return int(m.group(1).replace(",", "")), tuple(k for k in KINDS if re.search(rf"\b{k}\b", counts))


def _kind(section: Path) -> str:
    m = re.search(r"(?m)^section_kind:\s*(\S+)", _read(section / f"{section.name}.md"))
    return m.group(1).lower() if m else TASK.sub("", section.name).lower()


def budget(job: Path) -> dict:
    """{cap, call, counted: [(Section, words, previous words or None)], total} for one version Job."""
    from .page_structure import previous_draft, section_words
    job = Path(job).expanduser().resolve()
    call = venue_call(job)
    cap, kinds = word_cap(_read(call)) if call else (None, ())
    secs = job_sections(job)
    if kinds:
        counted = [s for s in secs if _kind(s) in kinds]
    else:                                       # no counts column: the Sections whose face says they share the cap
        counted = [s for s in secs if re.search(r"(?i)main-text (?:word )?cap", _read(s / f"{s.name}.md"))]
    rows = []
    for s in counted:
        prev = previous_draft(s)
        rows.append((s.name, section_words(s), section_words(s, prev) if prev else None))
    return {"cap": cap, "call": f"venues/{call.parent.name}/call.md" if call else None, "counted": rows,
            "total": sum(r[1] for r in rows)}


def budget_line(b: dict) -> str:
    parts = " + ".join(f"{n} {w:,}" for n, w, _p in b["counted"]) or "no Section counted"
    if b["cap"] is None:
        return f"Main text: {b['total']:,} words ({parts}) · no word cap read from the venue's call.md"
    over = b["total"] - b["cap"]
    tail = f", {over:,} over ⚠" if over > 0 else ""
    return f"Main text: {b['total']:,} of {b['cap']:,} words{tail} ({parts}) · {b['call']}"


def grew(b: dict) -> list:
    """['t02_results +201'] for each counted Section longer than its previous Draft."""
    return [f"{n} +{w - p:,}" for n, w, p in b["counted"] if p is not None and w > p]


def over_budget(job: Path) -> str | None:
    """The health message when the main text is over the cap, else None."""
    b = budget(job)
    if b["cap"] is None or b["total"] <= b["cap"]:
        return None
    who = grew(b)
    names = ", ".join(n for n, _w, _p in b["counted"])
    msg = (f"main text is {b['total']:,} words, over the {b['cap']:,} cap of {b['call']} by "
           f"{b['total'] - b['cap']:,} (counted: {names})")
    return msg + (f"; grew since the previous Draft: {', '.join(who)}" if who else "")
