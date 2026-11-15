"""5 · Revise of the draft Task: where a Section stands in haipipe-paper-draft's method (ref/section-method.md § Where a
Section stands), one line of marks above the text, `S1 ⬜ S2 ⬜ S3 ✅ · D1 ✅ D2 ⬜ D3 ⬜ D4 🙋 D5 ⬜`. Each mark is read from
its record on disk; marks only, no state words (AGENTS § Page words). S1, S2 and D3 have no record type yet: ⬜.

S3 a new Draft version (one in draft/previous/) · D1 a review Run at the current version (this Task's own newest pass
read `on draft <version>` with its review report, or a review Job's paragraph-logic or sentence-review Run naming this
Section and version) · D2 a Draft version newer than a blind A/B Run on this Section · D4 the person's cards decided (🙋
while one waits) · D5 every sentence ✓ at its current words.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from live.frame import esc

STEPS = (("S1", "check the structure"), ("S2", "compare with the venue's examples"),
         ("S3", "a new Draft version"), ("D1", "rate: paragraph and sentence review"),
         ("D2", "auto loop: blind A/B, adopted"), ("D3", "highlight for the person"),
         ("D4", "the person's feedback: cards decided"), ("D5", "the person checks every sentence"))


def _small(f: Path) -> str:
    try:
        return f.read_text(encoding="utf-8", errors="replace") if f.stat().st_size < 400_000 else ""
    except OSError:
        return ""


def _names(task: Path, text: str, version: str) -> bool:
    """Does a record name this Section (its folder name) and the Draft version?"""
    return task.name in text and bool(version) and re.search(r"(?<![\w.])" + re.escape(version) + r"(?![\d.]*\d)", text)


def _review_run(task: Path, version: str) -> bool:
    board = task.parents[1] if len(task.parents) > 1 else task
    for run in sorted(board.glob("j*review*/t*/runs/*")):
        if not re.search(r"paragraph_logic|sentence_review", run.parent.parent.name):
            continue
        files = [run / "run.yaml"] + sorted((run / "result").glob("*.md")) + sorted((run / "result").glob("*/*.md"))
        if any(_names(task, _small(f), version) for f in files if f.is_file()):
            return True
    return False


def _blind_then_adopted(task: Path, d: dict) -> bool:
    board = task.parents[1] if len(task.parents) > 1 else task
    draft = Path(d.get("file") or "")
    if not draft.is_file():
        return False
    for key in sorted(board.glob("j*/t*/runs/*/result/key.json")) + sorted(task.glob("runs/*/result/key.json")):
        try:
            data = json.loads(key.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        mine = any(isinstance(v, dict) and task.name.startswith(str(v.get("section") or "\0")) for v in data.values())
        if mine and draft.stat().st_mtime > key.stat().st_mtime and d.get("previous"):
            return True
    return False


def stands(d: dict, revise: Path, task: Path, cards: list, words: dict, ok: set, rep_title: str) -> dict:
    """{step: mark} for the eight steps."""
    version = d.get("version") or ""
    marks = dict.fromkeys((k for k, _ in STEPS), "⬜")
    if d.get("previous"):
        marks["S3"] = "✅"
    if (rep_title and re.search(r"\bon draft " + re.escape(version) + r"\b", rep_title)) or _review_run(task, version):
        marks["D1"] = "✅"
    if _blind_then_adopted(task, d):
        marks["D2"] = "✅"
    states = [(c.get("state") or "proposed").split()[0].lower() for _, c in cards]
    if states:
        marks["D4"] = "🙋" if any(s in ("proposed", "jl's", "jl") for s in states) else "✅"
    if words and set(words) <= ok:
        marks["D5"] = "✅"
    return marks


def stands_line(marks: dict) -> str:
    def one(k, what):
        return f'<span title="{esc(k)} · {esc(what)}">{esc(k)} {marks[k]}</span>'
    s = " ".join(one(k, w) for k, w in STEPS[:3])
    dl = " ".join(one(k, w) for k, w in STEPS[3:])
    return (f'<p class=sx-stands style="margin:0 0 8px;font-size:13px;letter-spacing:.01em">{s} · {dl}</p>')
