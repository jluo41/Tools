"""`page.py structure <Section Task | version Job>`: the current structure of a Section, printed one way every time.

hai-paper ref/must-check.md M-D14: "what is the current section structure" is answered by this command's output,
verbatim. A Section prints its newest Draft's `## 3 · Draft`: each claim (`### C<n> · <claim>`, else the Structure
Overview's `- C<n> · <claim>`) at the left, each paragraph indented under it with its full heading (wrapped, never
cut), its sentence range, sentence count and words. A paragraph outside the paper's 4 to 7 sentences
(src/paragraph_length.py, its exemptions and `reason:` lines) gets a ⚠. When the paper's review Job has a
t03_paragraph_logic Run for this Section, its score per paragraph is a last column. A version Job prints every
Section in compile order, then the shared main-text budget (src/paper_budget.py). Plain text, no ANSI, deterministic.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

from .outline_version import latest_outline, plan_dir, plan_files, version_key, PREVIOUS
from .paragraph_length import RANGE, exempt, paragraphs as planned, section_kind
from .sentence_id import sid

HEAD_W = 40                                  # the heading column; a longer heading wraps onto the next line
DRAFT = re.compile(r"(?m)^## \d+ · Draft\b")
PARA = re.compile(r"^#{3,4}\s+(C(\d+)\.P(\d+))\s*·\s*(.*?)\s*$")
TAIL = re.compile(r"\s*·\s*[Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?\s*$")
SENT = re.compile(r"^-\s*B\d+[a-z]*\s*·\s*([Ss]\d+[a-z]*)\s*·\s*(.*)$")
CLAIM_HEAD = re.compile(r"(?m)^###\s+(C\d+)\s*·\s*(.+?)\s*$")
CLAIM_LINE = re.compile(r"(?m)^-\s*(C\d+)\s*·\s*(.+?)\s*$")
SIGN = re.compile(r"(?m)^approved:\s*(.*?)\s*$")


def words(text: str) -> int:
    """Printed words of one sentence: a \\ref or \\cite counts as one, other LaTeX commands and comments as none."""
    t = re.sub(r"<!--.*?-->", " ", text or "")
    t = re.sub(r"\\(?:auto|C|c)?ref\{[^}]*\}|\\cite\w*\{[^}]*\}", " X ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    return len(re.findall(r"\S*[A-Za-z0-9]\S*", t))


def draft_body(text: str) -> str:
    m = DRAFT.search(text or "")
    return re.split(r"(?m)^## ", text[m.end():], maxsplit=1)[0] if m else ""


def read_draft(text: str) -> dict:
    """{claims: {C1: claim}, paras: [{pid, c, p, heading, ids, words}]} from one Draft Markdown."""
    claims = dict(CLAIM_HEAD.findall(text)) or {c: t for c, t in CLAIM_LINE.findall(text)}
    paras = []
    for line in draft_body(text).splitlines():
        h = PARA.match(line)
        if h:
            paras.append({"pid": h.group(1), "c": int(h.group(2)), "p": int(h.group(3)),
                          "heading": TAIL.sub("", h.group(4)), "ids": [], "words": 0})
            continue
        s = SENT.match(line.strip())
        if s and paras:
            paras[-1]["ids"].append(sid(s.group(1)))
            paras[-1]["words"] += words(s.group(2))
    return {"claims": claims, "paras": paras}


def draft_version(path: Path) -> str:
    m = re.search(r"-(?:draft|outline)-v([\d.]+)\.md$", path.name)
    return m.group(1) if m else "?"


def plan_sign(text: str) -> str:
    """The plan's sign as `page.py health` reads it (`approved: ✅ …`): `✅ JL 261113`, else `⬜`."""
    m = SIGN.search(text or "")
    if not m or not m.group(1).startswith("✅"):
        return "⬜"
    return m.group(1).split(" · ", 1)[0].strip()


def previous_draft(folder: Path) -> Path | None:
    """The Draft version just before the current one (draft/previous/), else None."""
    cur = latest_outline(plan_dir(folder), folder.name)
    older = [p for p in plan_files(plan_dir(folder) / PREVIOUS, folder.name) if "-draft-v" in p.name]
    older = [p for p in older if cur is None or version_key(p) < version_key(cur)]
    return max(older, key=version_key) if older else None


def section_words(folder: Path, draft: Path | None = None) -> int:
    draft = draft or latest_outline(plan_dir(folder), folder.name)
    if draft is None:
        return 0
    return sum(p["words"] for p in read_draft(draft.read_text(encoding="utf-8", errors="ignore"))["paras"])


def _board(folder: Path) -> Path | None:
    return next((p for p in [folder, *folder.parents] if (p / "board.md").is_file()), None)


def logic_scores(folder: Path) -> dict:
    """{C1.P2: '7/10'} from the newest t03_paragraph_logic Run of the Board's review Jobs that names this Section;
    {} when there is none (best effort)."""
    board = _board(folder)
    if board is None:
        return {}
    found = sorted(board.glob(f"j*_review*/t03_paragraph_logic/runs/r[0-9]*/result/logic-{folder.name}.md"),
                   key=lambda p: (p.parts[-5], p.parts[-3]))
    if not found:
        return {}
    text = found[-1].read_text(encoding="utf-8", errors="ignore")
    return {m.group(1): f"{m.group(2)}/10" for m in re.finditer(r"(?m)^###\s+(C\d+\.P\d+)\s*·.*·\s*(\d+)/10\s*$", text)}


def _range(ids: list) -> str:
    if not ids:
        return "-"
    return ids[0] if ids[0] == ids[-1] else f"{ids[0]}-{ids[-1]}"


def section_block(folder: Path) -> list:
    """The printed lines of one Section Task."""
    folder = Path(folder).expanduser().resolve()
    draft = latest_outline(plan_dir(folder), folder.name)
    if draft is None:
        return [f"{folder.name} · no Draft"]
    text = draft.read_text(encoding="utf-8", errors="ignore")
    got = read_draft(text)
    face = folder / f"{folder.name}.md"
    kind = section_kind(face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else ""
    reasons = {pid: why for pid, _n, why in planned(text)}
    scores = logic_scores(folder)
    total = sum(p["words"] for p in got["paras"])
    lines = [f"{folder.name} · Draft v{draft_version(draft)} · plan {plan_sign(text)} · {total:,} words"]
    paras = got["paras"]
    rw = max((len(_range(p["ids"])) for p in paras), default=1)
    nw = max((len(str(len(p["ids"]))) for p in paras), default=1)
    ww = max((len(f"{p['words']:,}") for p in paras), default=1)
    claims = sorted({int(c[1:]) for c in got["claims"]} | {p["c"] for p in paras})
    for c in claims:
        claim = got["claims"].get(f"C{c}", "")
        lines.append(f"C{c:<3}{claim}".rstrip())
        for p in (q for q in paras if q["c"] == c):
            n = len(p["ids"])
            wrapped = textwrap.wrap(p["heading"], HEAD_W) or [""]
            cols = f"{_range(p['ids']):<{rw}}  {n:>{nw}} sent  {p['words']:>{ww},} w"
            if scores:
                cols += f"  {scores.get(p['pid'], '-'):>5}"
            lo, hi = RANGE
            if p["p"] and not exempt(kind) and not lo <= n <= hi and not reasons.get(p["pid"]):
                cols += "  ⚠"
            pad = f"  {'P' + str(p['p']):<5}"
            lines.append(f"{pad}{wrapped[0]:<{HEAD_W}}  {cols}")
            lines += [f"{' ' * len(pad)}{w}" for w in wrapped[1:]]
    return lines


def is_version_job(folder: Path) -> bool:
    face = folder / f"{folder.name}.md"
    if not face.is_file():
        return False
    text = face.read_text(encoding="utf-8", errors="ignore")
    return "haipipe:compile-order:start" in text or bool(re.search(r"(?m)^## Narrative\b", text))


def structure(target: Path) -> str:
    folder = Path(target).expanduser().resolve()
    folder = folder.parent if folder.is_file() else folder
    if not is_version_job(folder):
        return "\n".join(section_block(folder))
    from .paper_budget import budget, budget_line, job_sections
    out = []
    for sec in job_sections(folder):
        out += section_block(sec) + [""]
    out.append(budget_line(budget(folder)))
    return "\n".join(out)
