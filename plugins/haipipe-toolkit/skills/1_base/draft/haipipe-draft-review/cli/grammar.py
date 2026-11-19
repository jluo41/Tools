#!/usr/bin/env python3
"""Grammar errors a machine can see in a draft's sentences (haipipe-paper-draft CONSTITUTION A04, JL 261118).

    python3 grammar.py <draft.md> [<draft.md> ...]     # exit 1 when any sentence has a finding

The draft loop rated logic, read and ai for 13 rounds on ScalingGlucose Methods and never read grammar, so the
errors were first seen in Word's grammar underline. This script reads every sentence row of the Draft text
(`- B<n> · s<n> · <sentence>`, after `## 3 ·`) and names three kinds:

  e-notation       a number in code form in prose ("1e-3", "8.0e-4"); write 0.001 or 1 x 10^-3 in math
  opening-comma    an opening phrase with no comma before its subject ("For all three traits we report")
  label-noun       a script label used as an English noun ("the selection patients", "each share MLP")

The reviewer still reads every sentence for grammar (ref/sentence-logic.md check 7); this list is only what a
pattern can catch. Math between $...$ and text in backticks are skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROW = re.compile(r"(?m)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · (.+)$")
OPENERS = ("for", "in", "at", "after", "before", "with", "over", "across", "within", "among", "on", "under", "from",
           "because", "when", "if", "although", "once", "since", "unlike", "beyond", "below", "above", "during",
           "to", "by", "per", "as")
SUBJECTS = r"(?:we|our|each|every|all|both|this|these|the)"
VERBS = r"(?:report|reports|used|use|uses|fitted|fit|fits|trained|train|trains|scored|score|scores|ran|run|runs|" \
        r"kept|keep|keeps|set|sets|took|take|takes|chose|choose|chooses|computed|compute|computes|averaged|" \
        r"held|hold|holds|gives|gave|give|shows|showed|show|is|are|was|were|has|have|had|stopped|stops|" \
        r"standardized|standardizes|predicted|predicts|measured|measures|compared|compares|drew|draws|counted)"
E_NOTATION = re.compile(r"(?<![\w.])\d+(?:\.\d+)?e[-+]?\d+(?![\w])", re.I)
# script labels that read as an English noun phrase only to the person who wrote the script
LABELS = re.compile(r"\b(?:the|each|every|a) (?:selection|fitting|scoring|holdout) (?:patients|rows)\b"
                    r"|\b(?:each|every|the|a) share MLPs?\b", re.I)


def prose(text: str) -> str:
    """The sentence without math and code, so a pattern never fires inside them."""
    return re.sub(r"`[^`]*`", " ", re.sub(r"(?<!\\)\$[^$]*\$", " ", text))


def findings(sentence: str) -> list:
    s = prose(sentence)
    out = [("e-notation", m.group(0)) for m in E_NOTATION.finditer(s)]
    words = s.split()
    if words and words[0].lower().strip("(") in OPENERS:
        head = " ".join(words[:16])
        cut = head.split(",", 1)[0]
        # the subject that starts the main clause: the first candidate with an opening phrase of 2+ words before it
        m = next((m for m in re.finditer(rf"(?=\s({SUBJECTS})\s+(?:\w+\s+){{0,3}}?{VERBS}\b)", cut, re.I)
                  if len(cut[: m.start()].split()) >= 2), None)
        if m:
            out.append(("opening-comma", cut[: m.start()].strip() + " ⟵ comma here"))
    out += [("label-noun", m.group(0)) for m in LABELS.finditer(s)]
    return out


def check(draft: Path) -> list:
    text = draft.read_text(encoding="utf-8", errors="replace")
    i = text.find("## 3 ·")
    body = text[i:] if i >= 0 else text
    return [(sid, kind, what) for sid, sentence in ROW.findall(body) for kind, what in findings(sentence)]


def main(argv: list) -> int:
    if not argv:
        print(__doc__)
        return 2
    bad = 0
    for arg in argv:
        found = check(Path(arg))
        bad += len(found)
        print(f"{'❗' if found else '✅'} {Path(arg).name}: {len(found)} grammar findings")
        for sid, kind, what in found:
            print(f"   {sid} · {kind} · {what}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
