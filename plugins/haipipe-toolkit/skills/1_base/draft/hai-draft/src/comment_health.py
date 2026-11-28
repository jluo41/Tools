"""`page.py health` row `comments`: a person's page comment that has no reply after it (hai-draft CONSTITUTION A01;
JL 261118: "every time pay attention to the comments I have and then update it my comments quickly").

A comment block in `draft/records/<stem>-comments.md` is `### Comment N · <address>`, `State: …`, then `- Note · <time> · …`
and `- Reply · <time>: …` lines in order. A Note whose text does not start with `AI:` is the person's. The block waits
for the session when its last person Note has no `- Reply` after it. WARN while writing, FAIL with --final."""
from __future__ import annotations

import re
from pathlib import Path

BLOCK = re.compile(r"(?m)^### Comment (\d+)\s*·\s*([^\n]*)$")
LINE = re.compile(r"(?m)^- (Note|Reply) · [^\n]*$")


def unanswered(comments_file: Path) -> list:
    """[(number, address, the person's words)] for each comment whose last person Note has no Reply after it."""
    if not comments_file.is_file():
        return []
    text = comments_file.read_text(encoding="utf-8", errors="replace")
    heads = list(BLOCK.finditer(text))
    out = []
    for k, h in enumerate(heads):
        body = text[h.end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        if re.search(r"(?m)^State:\s*(closed|resolved|withdrawn|done)\b", body):
            continue
        waiting = None
        for m in LINE.finditer(body):
            kind, line = m.group(1), m.group(0)
            if kind == "Note" and not re.search(r"·\s*AI:", line):
                waiting = line.split(":", 2)[-1].strip() if line.count(":") >= 2 else line
            elif kind == "Reply":
                waiting = None
        if waiting is not None:
            out.append((h.group(1), h.group(2).strip(), waiting[:80]))
    return out


def check_comments(comments_file: Path, out: list, Finding, WARN, OK):
    if not comments_file.is_file():
        return
    left = unanswered(comments_file)
    if left:
        out.append(Finding(WARN, "comments", f"{len(left)} person comment(s) with no reply: " + "; ".join(
            f"Comment {n} · {a} \"{w}\"" for n, a, w in left) + " · reply under each (fix the sentence or answer) first"))
    else:
        out.append(Finding(OK, "comments", "every person comment has a reply"))
