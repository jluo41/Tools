"""Explicit synthetic design examples, owned and addressed only by a Block.

This reader does not create production workflow state, signatures or workers. Only
Blocks explicitly declaring the preview contract opt in; legacy readers are unchanged.
"""
from html import escape
from pathlib import Path
import re

KINDS = {"itemization", "guideline-generation", "labeling-at-scale"}


def render_block_preview(folder: Path, root: Path) -> str | None:
    folder, root = Path(folder).resolve(), Path(root).resolve()
    if not folder.is_relative_to(root):
        raise ValueError("Folder outside root")
    face = folder / "board.md"
    if not face.is_file():
        return None
    text = face.read_text(encoding="utf-8")
    if not re.search(r"^preview-only:\s*true\s*$", text, re.M):
        return None
    kind = re.search(r"^labeling-block-type:\s*(\S+)\s*$", text, re.M)
    if not kind or kind[1] not in KINDS:
        return None
    path = (folder / "delivery/ui/block.html").resolve()
    if not path.is_relative_to(folder):
        raise ValueError("Preview outside its Block")
    content = path.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(?:b\d+\s*·\s*)?(.+)$", text, re.M)
    name = title[1] if title else folder.name
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(name)}</title><style>body{{margin:0}}'
            'body>div[data-labeling-block]{max-width:1060px;margin:auto;padding:24px 32px}'
            '@media(max-width:600px){body>div[data-labeling-block]{padding:16px}}'
            '</style></head><body>' + content + '</body></html>')
