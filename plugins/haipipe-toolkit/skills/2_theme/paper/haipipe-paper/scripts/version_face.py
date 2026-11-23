"""version_face.py: what paper_ladder.py writes into a version Job's face for each new Section Task: its row in
## Narrative, and its line in the compile-order block the build reads (LLMRecJamaAI 261122: the block stayed empty,
was filled by guessing as a numbered list, and the build stopped on "invalid compile-order entry")."""
from __future__ import annotations

import re

# a version's per-Section narrative (JL 261109: "not just the claims ... the narratives, the arc"): the workbench's
# Story by Section reads it, haipipe-paper-story writes it; a new Section adds its row with placeholders
NARRATIVE_HEAD = ("| Section | reader question | entry | ordered moves | must refuse | displays | exit |\n"
                  "|---|---|---|---|---|---|---|\n")


def narrative_row(face_text: str, stem: str) -> str:
    """The version face with a placeholder row for `stem` in its ## Narrative table, when the table is there and has none."""
    m = re.search(r"(?ms)^## Narrative[ \t]*\n(.*?)(?=^## |\Z)", face_text)
    if m is None or re.search(rf"(?m)^\|\s*{re.escape(stem)}\s*\|", m.group(1)):
        return face_text
    rows = list(re.finditer(r"(?m)^\|.*\|[ \t]*$", m.group(1)))
    if not rows or not re.match(r"\|\s*Section\s*\|", rows[0].group(0)):
        return face_text
    at = m.start(1) + rows[-1].end()
    row = f"\n| {stem} | <what the reader asks here> | <what they hold coming in> | <a → b → c> | <what it must not say> | <displays> | <what they leave with> |"
    return face_text[:at] + row + face_text[at:]


ORDER = re.compile(r"(<!--\s*haipipe:compile-order:start\s*-->)(.*?)(<!--\s*haipipe:compile-order:end\s*-->)", re.S)


def order_add(face_text: str, stem: str, lane: str) -> str:
    """The face with `- <stem>` under `main:` or `appendix:` of its compile-order block (the one form the build reads),
    kept in tNN order; a letter (lane "") and a face with no block are left as they are."""
    m = ORDER.search(face_text)
    if not lane or m is None:
        return face_text
    lanes: dict = {"main": [], "appendix": []}
    at = None
    for line in m.group(2).splitlines():
        s = line.strip()
        if s in ("main:", "appendix:"):
            at = s[:-1]
        elif at and re.match(r"-\s*\S", s):
            lanes[at].append(s[1:].strip())
    if stem in lanes["main"] + lanes["appendix"]:
        return face_text
    lanes[lane] = sorted(lanes[lane] + [stem])
    body = "".join(f"{k}:\n" + "".join(f"- {i}\n" for i in v) for k, v in lanes.items() if v)
    return face_text[:m.start(2)] + "\n" + body + face_text[m.end(2):]
