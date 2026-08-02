"""Managed requirements and page-writing sources for S pages.

This module is intentionally independent of the board parser. The parser calls
``contract_status`` after it has assembled the page map; ``stage.py`` calls the
other helpers when it explicitly creates or synchronizes a stage.
"""
import hashlib
import re
from pathlib import Path

START = "<!-- haipipe:contract:start"
END = "<!-- haipipe:contract:end -->"
STYLE_START = "<!-- haipipe:style:start"
STYLE_END = "<!-- haipipe:style:end -->"


def refs(value):
    """Comma-separated explicit references, in authored order."""
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def _resolve(board, token, by_id):
    page = by_id.get(token.casefold())
    if page and page.get("file"):
        return board / page["file"], page
    path = Path(token)
    path = path if path.is_absolute() else board / path
    if path.is_file():
        return path, None
    return None, None


def contract_digest(board, page, by_id):
    """Hash only explicit contract sources, never the destination page."""
    h = hashlib.sha256()
    for kind, value in (("requires", page.get("requires", "")),
                        ("style-from", page.get("style_from", ""))):
        for token in refs(value):
            path, _ = _resolve(Path(board), token, by_id)
            h.update(f"{kind}:{token}\0".encode("utf-8"))
            if path:
                h.update(path.resolve().as_posix().encode("utf-8"))
                h.update(b"\0")
                h.update(path.read_bytes())
            else:
                h.update(b"<missing>")
    return h.hexdigest()[:16]


def contract_status(board, page, by_id):
    """Return one parser warning for a missing or stale managed contract."""
    if page.get("kind") != "stage":
        return ""
    if not refs(page.get("requires", "")) and not refs(page.get("style_from", "")):
        return ""
    for value in (page.get("requires", ""), page.get("style_from", "")):
        for token in refs(value):
            path, _ = _resolve(Path(board), token, by_id)
            if not path:
                return f"{page['id']} Stage Contract source not found: {token}"
    source = Path(board) / page.get("file", "")
    text = source.read_text(encoding="utf-8") if source.is_file() else ""
    saved = page.get("contract_source_hash", "")
    current = contract_digest(board, page, by_id)
    if START not in text or END not in text or not saved:
        return f"{page['id']} has dependencies but its Stage Contract has not been synchronized"
    if saved != current:
        return (
            f"{page['id']} Stage Contract is stale "
            f"(saved {saved}, current {current}); run stage.py sync"
        )
    return ""


def managed_span(text):
    """Return the managed block's [start, end) span, or None."""
    start = text.find(START)
    if start < 0:
        return None
    end = text.find(END, start)
    if end < 0:
        return None
    return start, end + len(END)


def managed_style_span(text):
    """Return the managed Writing Style block's [start, end) span, or None."""
    start = text.find(STYLE_START)
    if start < 0:
        return None
    end = text.find(STYLE_END, start)
    if end < 0:
        return None
    return start, end + len(STYLE_END)


def replace_managed(text, block):
    """Replace only the generated block; preserve all authored prose."""
    span = managed_span(text)
    if span:
        return text[:span[0]] + block + text[span[1]:]
    heading = re.search(r"^## Stage Contract\s*$", text, re.M)
    if heading:
        at = heading.end()
        return text[:at] + "\n\n" + block + text[at:]
    before = re.search(r"^## (?:Diagram|Content)\s*$", text, re.M)
    at = before.start() if before else len(text.rstrip())
    prefix = text[:at].rstrip()
    suffix = text[at:].lstrip()
    out = prefix + "\n\n## Stage Contract\n\n" + block + "\n\n"
    return out + suffix


def replace_managed_style(text, block):
    """Replace only generated prose inside ``## Writing Style``."""
    span = managed_style_span(text)
    if span:
        return text[:span[0]] + block + text[span[1]:]
    heading = re.search(r"^## Writing Style\s*$", text, re.M)
    if not heading:
        before = re.search(r"^## (?:Stage Contract|Diagram|Content)\s*$", text, re.M)
        at = before.start() if before else len(text.rstrip())
        prefix = text[:at].rstrip()
        suffix = text[at:].lstrip()
        out = prefix + "\n\n## Writing Style\n\n" + block + "\n\n"
        return out + suffix
    at = heading.end()
    return text[:at] + "\n\n" + block + text[at:]
