#!/usr/bin/env python3
"""scope_guard.py · the computable half of a Section's scope guard (must-check M-A08, M-A13, M-A18, M-D08, M-D11).

    python3 scope_guard.py <section Task> [--json]

Reads, all read only:
  - the Section's newest Draft, `draft/<stem>-draft-v<N>.md`, its `## 3 · Draft` sentences (`- B<k> · s<n> · text`
    under `### C<c>.P<p> · ...`), each keyed by its full address (C2.P4.s17, must-check M-D05);
  - the version face's `## Narrative` (and the Board Story's § 8, `story-current:` in board.md): its `8.6` text
    (what every Section receives unchanged) and this Section's `8.3` row, column `must refuse`;
  - the venue's `venues/<venue>/call.md` limits table, when it states a word cap or a display count.

What it flags, one line per hit with the sentence's full address:
  rule     a semicolon outside a parenthesis (M-A13), an em-dash (M-A18), a phrase § 8.6 says "never" to (M-D08)
  refuse   a quoted phrase in the Section's `must refuse` cell with no condition ("first", "because") (M-A08)
  read     a quoted must-refuse phrase with a condition ("no effect" without an interval): printed for the reading
           half of the scope guard (hai-draft-eval-sentence-agent), never counted as a hit
  venue    the Abstract over its word cap, or the Section calling more main displays than the venue allows (M-D11)

Exit 1 on any rule, refuse or venue hit; 0 otherwise. It writes nothing. The judgment a script cannot make (a claim
wider than its interval, a cause that was not tested) is the reading agent's.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PARA = re.compile(r"^#{3,4}\s+(C\d+\.P\d+)\b")
SENT = re.compile(r"^-\s*B\d+[a-z]*\s*·\s*([Ss]\d+[a-z]*)\s*·\s*(.*)$")
DRAFT_HEAD = re.compile(r"(?m)^## \d+ · Draft\b")
QUOTED = re.compile(r"[\"“]([^\"”]{1,80})[\"”]")
CONDITION = re.compile(r"\b(without|unless|as a|beyond|before|outside|instead of)\b", re.I)
EM_DASH = re.compile("\u2014|" r"(?<!-)---(?!-)")
# ordinary uses of a refused word that make no claim: "at first", an enumeration's "First,"
IDIOM = {"first": re.compile(r"\bat first\b|\bfirst,", re.I)}


def version_of(path: Path) -> tuple:
    m = re.search(r"-draft-v(\d+(?:\.\d+)*)\.md$", path.name)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def newest_draft(task: Path) -> Path | None:
    drafts = [p for p in (task / "draft").glob(f"{task.name}-draft-v*.md") if version_of(p)]
    return max(drafts, key=version_of) if drafts else None


def draft_version(path: Path | None) -> str:
    return "v" + ".".join(map(str, version_of(path))) if path else ""


def sentences(draft_text: str) -> list:
    """[(address, text)] of the Draft's `## 3 · Draft` section, in order."""
    m = DRAFT_HEAD.search(draft_text or "")
    if not m:
        return []
    body = re.split(r"(?m)^## ", draft_text[m.end():], maxsplit=1)[0]
    out, pid = [], ""
    for line in body.splitlines():
        h = PARA.match(line)
        if h:
            pid = h.group(1)
            continue
        s = SENT.match(line.strip())
        if s:
            sid = s.group(1).lower()
            out.append((f"{pid}.{sid}" if pid else sid, s.group(2).strip()))
    return out


def board_of(path: Path) -> Path | None:
    return next((p for p in [path, *path.parents] if (p / "board.md").is_file()), None)


def _read(p: Path | None) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p and p.is_file() else ""


def narrative_texts(task: Path) -> list:
    """The version face's `## Narrative` and the Board Story's face, as text (either may hold 8.3 and 8.6)."""
    texts = []
    face = _read(task.parent / f"{task.parent.name}.md")
    m = re.search(r"(?m)^## Narrative\b", face)
    if m:
        texts.append(re.split(r"(?m)^## ", face[m.end():], maxsplit=1)[0])
    board = board_of(task)
    if board:
        cur = re.search(r"(?m)^story-current:\s*(\S+)", _read(board / "board.md"))
        if cur:
            texts.append(_read(board / cur.group(1) / f"{cur.group(1)}.md"))
    return texts


def subsection(text: str, number: str) -> str:
    m = re.search(rf"(?m)^#{{2,5}}\s*{re.escape(number)}\b.*$", text or "")
    if not m:
        return ""
    return re.split(r"(?m)^#{2,5}\s", text[m.end():], maxsplit=1)[0]


def forbidden(texts: list) -> list:
    """[(phrase, why)]: each quoted phrase a § 8.6 sentence puts after "never", and a `forbidden:` list's items."""
    out = []
    for text in texts:
        body = subsection(text, "8.6")
        for sent in re.split(r"(?<=[.!?])\s+", body):
            low = sent.lower()
            if "never" in low:
                for q in QUOTED.findall(sent[low.index("never"):]):
                    out.append((q.strip(), "What every Section receives unchanged: never \"" + q.strip() + "\""))
        for line in re.findall(r"(?mi)^\s*[-*]?\s*forbidden(?: words)?:\s*(.+)$", body):
            for w in re.split(r"[,;·]", line):
                w = w.strip().strip("\"“”`")
                if w:
                    out.append((w, f"What every Section receives unchanged, forbidden: {w}"))
    return list(dict.fromkeys(out))


def must_refuse(texts: list, task: str) -> str:
    """This Section's `must refuse` cell from an 8.3 table whose first header is `Section`."""
    for text in texts:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
        head = None
        for ln in lines:
            cells = [c.strip().strip("`") for c in ln.strip("|").split("|")]
            if cells and cells[0].lower() == "section":
                head = [c.lower() for c in cells]
                continue
            if head and cells and cells[0] == task and "must refuse" in head:
                i = head.index("must refuse")
                return cells[i] if i < len(cells) else ""
    return ""


def refuse_phrases(cell: str) -> list:
    """[(phrase, conditional?, part)] from a must-refuse cell, split on commas outside quotes."""
    out = []
    for part in re.split(r",\s*(?=(?:[^\"“”]*[\"“][^\"”]*[\"”])*[^\"“”]*$)", cell or ""):
        for q in QUOTED.findall(part):
            rest = part.split(q, 1)[-1]
            out.append((q.strip(), bool(CONDITION.search(rest)), part.strip()))
    return out


def has_phrase(text: str, phrase: str) -> bool:
    idiom = IDIOM.get(phrase.lower())
    text = idiom.sub(" ", text) if idiom else text
    return bool(re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text, re.I))


def outside_parens(text: str) -> str:
    prev = None
    while prev != text:
        prev, text = text, re.sub(r"\([^()]*\)", " ", text)
    return text


def plain(text: str) -> str:
    """The reader's words: comments, LaTeX commands and maths out, a \\ref or \\cite as one token."""
    t = re.sub(r"<!--.*?-->", " ", text or "")
    t = re.sub(r"\\(?:auto|C|c)?ref\{[^}]*\}|\\cite\w*\{[^}]*\}", " X ", t)
    t = re.sub(r"\$[^$]*\$", " X ", t)
    return re.sub(r"\\[a-zA-Z]+\*?", " ", t)


def words(text: str) -> int:
    return len(re.findall(r"\S*[A-Za-z0-9]\S*", plain(text)))


def venue_limits(task: Path) -> dict:
    """{abstract: N, main_displays: N} from the Board's venue call.md limits and displays tables."""
    board = board_of(task)
    calls = sorted(board.glob("venues/*/call.md")) if board else []
    face = _read(task.parent / f"{task.parent.name}.md")
    venue = re.search(r"(?m)^venue:\s*(.+)$", face)
    slug = re.sub(r"[^a-z0-9]+", "-", venue.group(1).lower()).strip("-") if venue else ""
    call = next((c for c in calls if c.parent.name == slug), calls[0] if len(calls) == 1 else None)
    out = {}
    for row in re.findall(r"(?m)^\|([^|]+)\|([^|]+)\|", _read(call)):
        what, limit = row[0].strip().lower(), row[1].strip().lower()
        n = re.search(r"(?:up to|at most|≤)\s*([\d,]+)", limit) or re.match(r"\s*([\d,]+)", limit)
        if not n:
            continue
        if what == "abstract" and "word" in limit:
            out["abstract"] = int(n.group(1).replace(",", ""))
        if what == "main limit":
            out["main_displays"] = int(n.group(1).replace(",", ""))
    if call:
        out["call"] = str(call.relative_to(board))
    return out


def is_abstract(task: Path) -> bool:
    kind = re.search(r"(?m)^section_kind:\s*(\S+)", _read(task / f"{task.name}.md"))
    return (kind.group(1).lower() == "abstract") if kind else "abstract" in task.name


def guard(task: Path) -> dict:
    task = Path(task).resolve()
    draft = newest_draft(task)
    sents = sentences(_read(draft))
    texts = narrative_texts(task)
    never = forbidden(texts)
    cell = must_refuse(texts, task.name)
    hits = []

    def hit(kind, rule, where, what, text=""):
        hits.append({"kind": kind, "rule": rule, "where": where, "what": what, "sentence": text})

    for addr, text in sents:
        if ";" in outside_parens(plain(text)).replace("&amp;", ""):
            hit("rule", "M-A13", addr, "semicolon in a sentence", text)
        if EM_DASH.search(text):
            hit("rule", "M-A18", addr, "em-dash", text)
        for phrase, why in never:
            if has_phrase(text, phrase):
                hit("rule", "M-D08", addr, why, text)
        for phrase, conditional, part in refuse_phrases(cell):
            if has_phrase(text, phrase):
                hit("read" if conditional else "refuse", "M-A08", addr, f"must refuse: {part}", text)
    lim = venue_limits(task)
    if is_abstract(task) and "abstract" in lim:
        n = sum(words(t) for a, t in sents if not a.startswith("C1.P0"))
        if n > lim["abstract"]:
            hit("venue", "M-D11", task.name, f"Abstract {n} words, the venue allows {lim['abstract']} ({lim['call']})")
    if "main_displays" in lim:
        calls = set()
        for _, t in sents:
            calls |= set(re.findall(r"\\ref\{((?:fig|tab):[^}]+)\}", t))
            calls |= {f"Figure {n}" for n in re.findall(r"(?<!Extended Data )\bFig(?:ure|\.)\s*(\d+)", t)}
        if len(calls) > lim["main_displays"]:
            hit("venue", "M-D11", task.name, f"{len(calls)} main displays called, the venue allows "
                f"{lim['main_displays']} ({lim['call']})")
    return {"task": task.name, "draft": draft.name if draft else None, "version": draft_version(draft),
            "sentences": len(sents), "never": [p for p, _ in never], "must_refuse": cell, "hits": hits,
            "failed": sum(h["kind"] != "read" for h in hits)}


def render(rep: dict) -> str:
    lines = [f"scope_guard {rep['task']} · Draft {rep['version'] or 'none'} · {rep['sentences']} sentences"]
    for h in rep["hits"]:
        tag = {"read": "READ", "rule": "HIT ", "refuse": "HIT ", "venue": "HIT "}[h["kind"]]
        text = f" · {h['sentence'][:140]}" if h["sentence"] else ""
        lines.append(f"{tag} {h['where']} {h['rule']} {h['what']}{text}")
    lines.append("no hits" if not rep["failed"] else f"hits: {rep['failed']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("task", type=Path, help="a paper Section Task folder (tNN_<section>)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not (a.task / "draft").is_dir():
        print(f"not a Section Task (no draft/): {a.task}", file=sys.stderr)
        return 2
    rep = guard(a.task)
    print(json.dumps(rep, indent=1, ensure_ascii=False) if a.json else render(rep))
    return 1 if rep["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
