"""A draft sentence id, read in either case and written in lowercase.

A sentence id is ``s8`` (``s3b`` for a split one); its full address is
``C1.P2.s8``. Older drafts wrote ``S8``; every reader accepts both and compares
through ``sid()``, every writer writes ``s``. Paragraph ``P``, Section ``C`` and
Bullet ``B`` stay uppercase, and Studio topic ids (``s01``, ``s02-D01``) are a
different thing that never passes through here.

The same helper lives in the hai-draft skill at
``skills/1_base/draft/hai-draft/src/sentence_id.py``; keep the two alike.
"""
from __future__ import annotations

import re

SENT = r"[Ss]\d+[a-z]*"                      # a sentence id, either case, as a regex fragment
_SEG = re.compile(r"(?<![A-Za-z0-9])[Ss](\d+[a-z]*)(?![A-Za-z0-9])")


def sid(x) -> str:
    """``S8`` -> ``s8``, ``C1.P2.S8`` -> ``C1.P2.s8``; anything else is returned as it is.

    Only a segment that is a whole sentence id is lowered, so ``C1.P2`` and
    ``B3`` are untouched."""
    if x is None:
        return ""
    return _SEG.sub(lambda m: "s" + m.group(1), str(x))


def label(n, letter: str = "") -> str:
    """The written sentence id for number ``n`` (``label(8) == "s8"``)."""
    return f"s{str(n).lstrip('Ss')}{letter}"
