"""Send each shared style and script once per page (JL 261125: "It alswyas take a while to load").

Every left-tab set, mark and card writes its own copy of the same `<style>` and `<script>`, so a Block page carried
the same blocks 30 to 70 times (2.3 MB, of which about 1.3 MB repeats). The finished page keeps the first copy of each
identical `<style>` and of each script that already guards itself (`if(window.X)return`, so a second copy does
nothing); any other script runs where it stands and is kept every time.
"""
from __future__ import annotations

import re

_BLOCK = re.compile(r"<(style|script)\b([^>]*)>(.*?)</\1>", re.S | re.I)
_GUARD = re.compile(r"^\s*\(function\(\)\{\s*if\(window\.[\w$]+\)return")


def once(html: str) -> str:
    """The page with repeated identical style blocks and repeated self-guarding scripts dropped."""
    seen = set()

    def keep(m: re.Match) -> str:
        tag, attrs, body = m[1].lower(), m[2], m[3]
        if tag == "script" and ("src=" in attrs or not _GUARD.match(body)):
            return m[0]
        key = (tag, attrs.strip(), body)
        if key in seen:
            return ""
        seen.add(key)
        return m[0]

    return _BLOCK.sub(keep, html)
