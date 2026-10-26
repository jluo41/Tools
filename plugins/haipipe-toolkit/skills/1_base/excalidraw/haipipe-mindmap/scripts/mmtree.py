"""The `.mindmap.md` grammar (ref/grammar.md): read a file into a tree, write the tree back.

A mind map's one source is a Markdown file: a front matter, a `# <root>` line, a nested bullet list (one node a
bullet, its id in a trailing `<!-- id -->` comment) and, from the next `## ` heading on, free notes kept as written.
The canvas and the web page are views of it (mmcanvas.py, mmhtml.py).
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

SUFFIX = ".mindmap.md"
ID_MARK = re.compile(r"\s*<!--\s*([^\s#>][^\s>]*?)(?:\s+#([0-9a-f]{6}))?\s*-->\s*$")
BULLET = re.compile(r"^([ \t]*)(?:[-*+]|\d+[.)])\s+(.*)$")
PERSON_ID = re.compile(r"^n(\d+)$")


class GrammarError(ValueError):
    """The file does not follow ref/grammar.md; the message says where."""


@dataclass
class Node:
    id: str
    text: str
    children: list = field(default_factory=list)
    note: list = field(default_factory=list)      # lines under the bullet, drawn small under the box
    hash: str = ""                                # a built node: the hash of the words its builder last wrote

    @property
    def built(self) -> bool:
        """Made by a builder (from-work, from-topic): its id starts with @."""
        return self.id.startswith("@")

    @property
    def edited(self) -> bool:
        """A built node whose words a person changed since its builder wrote them."""
        return self.built and bool(self.hash) and self.hash != words_hash(self.text)


@dataclass
class MindMap:
    meta: dict
    root: Node
    tail: str = ""                                # from the first `## ` after the list: notes, kept as written


def words_hash(text: str) -> str:
    return hashlib.sha1(" ".join(str(text).split()).encode("utf-8")).hexdigest()[:6]


def views(md: Path) -> dict:
    """The three views of one source: `<stem>.excalidraw`, `<stem>.png`, `<stem>.mindmap.html`."""
    md = Path(md)
    if not md.name.endswith(SUFFIX):
        raise GrammarError(f"{md.name}: a mind map's file ends in {SUFFIX}")
    stem = md.name[: -len(SUFFIX)]
    return {"md": md, "canvas": md.with_name(stem + ".excalidraw"), "png": md.with_name(stem + ".png"),
            "html": md.with_name(stem + ".mindmap.html"), "stem": stem}


# ── words shown on the canvas ──────────────────────────────────────────────────────────────────────────────
def display(text: str) -> str:
    """A node's words as the canvas shows them: the Markdown marks taken off, spaces made single."""
    s = re.sub(r"`([^`]*)`", r"\1", str(text))
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", s)
    return " ".join(s.split())


# ── read ───────────────────────────────────────────────────────────────────────────────────────────────────
def _split_id(s: str) -> tuple:
    m = ID_MARK.search(s)
    if not m:
        return s.strip(), "", ""
    return s[: m.start()].strip(), m.group(1), m.group(2) or ""


def parse(text: str, name: str = "the file") -> MindMap:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i, meta = 0, {}
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), None)
        if end is None:
            raise GrammarError(f"{name}: the front matter opened on line 1 never closes with ---")
        for ln in lines[1:end]:
            if ":" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip()
        i = end + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].startswith("# "):
        raise GrammarError(f"{name}: line {i + 1} should be the root, '# <words>'")
    text_, _id, h = _split_id(lines[i][2:])
    root = Node("root", text_, hash=h)
    i += 1
    while i < len(lines) and not BULLET.match(lines[i]) and not lines[i].startswith("## "):
        root.note.append(lines[i].rstrip())
        i += 1
    root.note = _trim(root.note)
    stack, last = [(-1, root)], None
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("## ") or ln.startswith("# "):
            break
        m = BULLET.match(ln)
        if m:
            indent = len(m.group(1).expandtabs(4))
            t, nid, h = _split_id(m.group(2))
            while stack[-1][0] >= indent:
                stack.pop()
            node = Node(nid, t, hash=h)
            stack[-1][1].children.append(node)
            stack.append((indent, node))
            last = node
        elif ln.strip():
            if last is None:
                raise GrammarError(f"{name}: line {i + 1} is text inside the list before any bullet")
            last.note.append(ln.strip())
        i += 1
    tail = "\n".join(lines[i:]).strip("\n")
    return MindMap(meta, root, tail)


def _trim(lines: list) -> list:
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def load(md: Path) -> MindMap:
    md = Path(md)
    return parse(md.read_text(encoding="utf-8"), md.name)


# ── ids ────────────────────────────────────────────────────────────────────────────────────────────────────
def walk(node: Node, parent: Node | None = None, depth: int = 0):
    """Every node once, root first: (node, parent, depth, index among its siblings)."""
    def go(n, p, d, k):
        yield n, p, d, k
        for j, c in enumerate(n.children):
            yield from go(c, n, d + 1, j)
    yield from go(node, parent, depth, 0)


def next_ids(taken: set):
    k = max([int(m.group(1)) for t in taken for m in [PERSON_ID.match(t)] if m] or [0])
    while True:
        k += 1
        yield f"n{k:02d}"


def ensure_ids(mm: MindMap, taken: set = frozenset()) -> int:
    """A bullet a person typed without an id gets the next free nNN (never one the canvas still remembers).
    Returns how many were given. Two bullets with one id: the second gets a new one."""
    seen, gave = set(), 0
    fresh = next_ids({n.id for n, *_ in walk(mm.root)} | set(taken))
    for n, p, *_ in walk(mm.root):
        if p is None:
            continue
        if not n.id or n.id in seen or n.id == "root":
            n.id, n.hash = next(fresh), ""
            gave += 1
        seen.add(n.id)
    return gave


def flat(mm: MindMap) -> dict:
    """{id: {text (as shown), parent, order}}: the shape the canvas and the file are compared in."""
    return {n.id: {"text": display(n.text), "parent": p.id if p else None, "order": k}
            for n, p, _d, k in walk(mm.root)}


def find(mm: MindMap, nid: str):
    """(node, parent) by id, or (None, None)."""
    for n, p, *_ in walk(mm.root):
        if n.id == nid:
            return n, p
    return None, None


# ── write ──────────────────────────────────────────────────────────────────────────────────────────────────
def _mark(n: Node) -> str:
    return f" <!-- {n.id}{' #' + n.hash if n.hash else ''} -->"


def dump(mm: MindMap) -> str:
    out = ["---"] + [f"{k}: {v}" for k, v in mm.meta.items()] + ["---", ""]
    out.append(f"# {mm.root.text}" + (f" <!-- root #{mm.root.hash} -->" if mm.root.hash else ""))
    out.append("")
    if mm.root.note:
        out += mm.root.note + [""]

    def go(n, depth):
        for c in n.children:
            out.append("  " * depth + "- " + c.text + _mark(c))
            out.extend("  " * depth + "  " + ln for ln in c.note)
            go(c, depth + 1)
    go(mm.root, 0)
    if mm.tail:
        out += ["", mm.tail]
    return "\n".join(out).rstrip("\n") + "\n"


def save(mm: MindMap, md: Path) -> None:
    """UTF-8 with LF line ends on every platform."""
    with open(md, "w", encoding="utf-8", newline="\n") as f:
        f.write(dump(mm))
