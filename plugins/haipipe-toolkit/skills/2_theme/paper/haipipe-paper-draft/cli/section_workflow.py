#!/usr/bin/env python3
"""Where a paper Section stands in its workflow, read from disk, and the step to run next (ref/workflow.md).

    python3 section_workflow.py <Section Task folder>

Six steps (JL 261116: "when I open a new secton draft, then I can run the tasks one by one and get a close to review
draft"): W0 Examples, W1 Plan (the person signs), W2 Write, W3 Rate, W4 Fix loop (the AI accepts what the blind
reader keeps, comments on the rest, stops after two rounds that keep nothing), W5 Ready (the person joins). Each step
is judged from a file, never from memory, so the line printed here is the one a page may show. Read only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROW = re.compile(r"(?m)^- B\d+[a-z]* · [Ss]\d+[a-z]* · ")
PASS = re.compile(r"(?m)^## Pass (\d+)[^\n]*?on draft v([\d.]+)")
SCORES = re.compile(r"(?m)^- (?:C\d+\.P\d+\.)?[Ss]\d+[a-z]* · (?:\([^)]*\) · )?logic (\d+(?:\.\d+)?)/10 · read "
                    r"(\d+(?:\.\d+)?)/10(?: · ai (\d+(?:\.\d+)?)/10)?")
STEPS = (("W0", "examples"), ("W1", "plan"), ("W2", "write"), ("W3", "rate"), ("W4", "fix loop"), ("W5", "ready"))


def vkey(p: Path) -> list:
    return [int(x) for x in re.findall(r"\d+", p.stem.rsplit("-v", 1)[-1])]


def newest_draft(task: Path) -> Path | None:
    drafts = sorted(task.glob("draft/*-draft-v*.md"), key=vkey)
    return drafts[-1] if drafts else None


def face(task: Path) -> str:
    f = task / f"{task.name}.md"
    return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else ""


def line(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.*?)\s*$", text)
    return m.group(1) if m else ""


def examples(task: Path) -> tuple:
    said = line(face(task), "examples")
    if said.startswith("none"):
        return True, f"none, {said}"
    if not said:
        return False, "no examples: line on the face"
    for up in (task, *list(task.parents)[:3]):
        topic = up / said
        if topic.is_dir():
            shots = list(topic.glob("reads/*/shots/*.jpg"))
            return bool(shots), f"{said}, {len(shots)} section screenshots" if shots else f"{said} has no screenshots"
    return False, f"{said} not found"


def split(draft: Path) -> tuple:
    text = draft.read_text(encoding="utf-8", errors="replace")
    i = text.find("## 3 ·")
    return text[:i] if i >= 0 else text, text[i:] if i >= 0 else ""


def newest_pass(task: Path) -> tuple:
    """(pass number, draft version it rated, its text) of the revise record's last Pass with sentence lines."""
    rec = next(iter(task.glob("draft/records/*-revise.md")), None)
    if not rec:
        return None
    text = rec.read_text(encoding="utf-8", errors="replace")
    heads = list(PASS.finditer(text))
    for k in range(len(heads) - 1, -1, -1):
        body = text[heads[k].end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        if SCORES.search(body):
            return int(heads[k].group(1)), heads[k].group(2), body
    return None


def open_ai_comments(task: Path) -> int:
    rec = next(iter(task.glob("draft/records/*-comments.md")), None)
    if not rec:
        return 0
    blocks = re.split(r"(?m)^### Comment ", rec.read_text(encoding="utf-8", errors="replace"))[1:]
    return sum(1 for b in blocks if re.search(r"(?m)^State:\s*open", b) and re.search(r"\bAI:", b))


def status(task: Path) -> list:
    """[(step, name, done, what was read)] in order."""
    out = []
    ok, said = examples(task)
    out.append(ok and said)
    draft = newest_draft(task)
    plan, prose = split(draft) if draft else ("", "")
    head = draft.read_text(encoding="utf-8", errors="replace")[:4000] if draft else ""
    signed = "✅" in line(head, "approved")
    out.append(signed and f"{draft.name} approved")
    n_plan, n_text = len(ROW.findall(plan)), len(ROW.findall(prose))
    out.append(n_text and n_text >= n_plan and f"{n_text} sentences in § 3 for {n_plan} Bullets")
    p = newest_pass(task)                   # a Pass on an older version is stale: the text changed after it
    version = draft.stem.rsplit("-v", 1)[-1] if draft else ""
    rated = p and p[1] == version
    out.append(rated and f"Pass {p[0]} rated v{p[1]}" + ("" if "Standard:" in p[2] else " (no Standard: line)"))
    low = [min(float(a), float(b), float(c or 10)) for a, b, c in SCORES.findall(p[2])] if p else []
    under = sum(v < 8 for v in low)
    asks = open_ai_comments(task)
    out.append((rated and (under == 0 or under <= asks), f"{under} under 8, {asks} open AI comments" if rated else ""))
    built = sorted(task.parents[2].glob(f"delivery/{task.parent.name}/{task.name}/*.pdf")) if len(task.parents) > 2 else []
    out.append(bool(out[4][0]) and bool(built) and draft and built[-1].stat().st_mtime >= draft.stat().st_mtime
               and f"{built[-1].name} built after {draft.name}")
    out = [d if isinstance(d, tuple) else (d, d) for d in out]
    return [(s, n, bool(d), str(w or "")) for (s, n), (d, w) in zip(STEPS, out)]


NEXT = {
    "W0": "read 3 to 4 published papers of the same article type and venue: SKILL.md § Examples first",
    "W1": "propose § 1 Structure against the examples and the Narrative row, then the person signs (page.py sign)",
    "W2": "write § 3 from the signed plan, then page.py adopt and page.py export",
    "W3": "rate with fresh agents: haipipe-draft-eval-paragraph-agent and haipipe-draft-eval-sentence-agent",
    "W4": "rewrite each item under 8, blind A/B, adopt what is kept, comment the rest; then W3 again",
    "W5": "page.py export, then page.py health --final; the person reads the 🤖 comments and checks each sentence",
}


def main(argv: list) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    task = Path(argv[0]).resolve()
    rows = status(task)
    print(task.name)
    for s, n, done, what in rows:
        print(f"  {'✅' if done else '⬜'} {s} {n:<9} {what}")
    nxt = next(((s, n) for s, n, done, _ in rows if not done), None)
    print(f"next: {nxt[0]} {nxt[1]}: {NEXT[nxt[0]]}" if nxt else "next: 🙋 the person: read the open comments, ✓ each sentence")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
