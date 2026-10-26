"""A Studio topic's mind map, drawn by the structure map it shares with a draft Task's §1 (mapview.py; JL 261026:
"做出来一模一样的东西", "这样的话他们就共享了"): the root is the Section, a first-level node a paragraph (its `→
<question>` note line the question it hands to the next), a node under it a point (`[role] words` its role pill),
deeper nodes lines under their point. On top of §1: ▸ opens a point's detail (its other note lines), and a point that
names a file carries a chip that opens it.

    fragment(md, rel, editable, url_of)   the map for the workbench card (read only for the static page)
    act(root, payload)                    one change from the map (the payload §1's map sends), written into the file
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import mapview as MV
import mmhtml as MH
import mmtree as MT

esc = lambda s: html.escape(str(s), quote=True)
norm = lambda s: " ".join(str(s or "").split())
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
FULL_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")
ROLE = re.compile(r"^\[([^\]]{1,24})\]\s+(?!\()")      # `[role] words`; `[name](link)` is a link, not a role
IMAGE = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
ENDPOINT = "/_board/mindmap"


def split_note(n: MT.Node) -> tuple:
    """(the question a node hands to the next one, its detail lines)."""
    ask = next((ln[2:].strip() for ln in n.note if ln.startswith("→ ")), "")
    return ask, [ln for ln in n.note if not ln.startswith("→ ")]


def split_role(text: str) -> tuple:
    raw = MT.ID_MARK.sub("", text)
    m = ROLE.match(raw)
    return (m.group(1), raw[m.end():]) if m else ("", raw)


def _opens(raw: str, base: Path | None, url_of) -> str:
    """A chip per file the words link, as §1's evidence chips: 🖼 a picture, ↗ anything else, in the pop-out; a link
    to a file not on disk gets none."""
    out = []
    for label, target in LINK.findall(raw):
        if re.match(r"^[a-z]+:", target):
            url = target
        else:
            path = (base / target) if base else None
            url = (url_of(path) if path.exists() else None) if (url_of and path is not None) else target
        if url:
            kind = "🖼" if target.lower().endswith(IMAGE) else "↗"
            out.append(f' <a class="pm-card pm-open" data-pop="{esc(label)}" href="{esc(url)}" target=_blank '
                       f'rel=noopener title="open {esc(label)}">{kind}</a>')
    return "".join(out)


def _resolve(md: str, base: Path | None, url_of) -> str:
    """A detail's links and pictures pointed where the host opens them; one to a file not on disk keeps its words."""
    def one(m):
        bang, label, target = m.groups()
        if re.match(r"^[a-z]+:", target) or not (base and url_of):
            return m.group(0)
        path = base / target
        return f"{bang}[{label}]({url_of(path)})" if path.exists() else label
    return FULL_LINK.sub(one, md)


def _inline(words: str) -> str:
    return MH.inline(LINK.sub(lambda m: m.group(1), words))     # a link's words; its chip opens it


def draw(mm: MT.MindMap, rel: str = "", editable: bool = True, base: Path | None = None, url_of=None) -> str:
    """The map of a tree already read, through the shared renderer; read only: no typing, no ＋, no ✎."""
    nodes = {n.id: n for n, *_ in MT.walk(mm.root)}
    labels = {}
    paras, asks = [], {}
    for k, b in enumerate(mm.root.children):
        kind, name = split_role(b.text)
        labels[b.id] = kind                          # the grey line over a branch's name: its kind, or nothing
        asks[b.id] = split_note(b)[0]
        points = []
        for j, c in enumerate(b.children):
            labels[c.id] = f"{k + 1}.{j + 1}"           # a point's number, as §1's S1
            role, words = split_role(c.text)
            points.append((c.id, role, words, "\n".join(split_note(c)[1])))
        paras.append((b.id, name, points))

    def more(s, note):
        body = MH.blocks(_resolve(note, base, url_of)) if note else ""
        pen = f'<button type=button class=pm-pen data-raw="{esc(note)}" title="edit the detail">✎</button>'
        btn = (f'<button type=button class=pm-more aria-expanded=false title="{"its detail" if note else "add a detail"}"'
               f'{"" if note else " data-empty=1"}>▸</button>')
        return btn, f'<div class=pm-detail hidden>{body}{pen}</div>'

    def sub(s):                                         # the lines under a point, and theirs, indented
        n = nodes[s]
        if not n.children:
            return ""
        items = []
        for j, c in enumerate(n.children):
            labels[c.id] = f"{labels[s]}.{j + 1}"
            role, words = split_role(c.text)
            btn, detail = more(c.id, "\n".join(split_note(c)[1]))
            items.append(f'<li data-s="{esc(c.id)}"><span class=pm-s draggable=true>{esc(labels[c.id])}</span>'
                         f'{MV.editable("role", role, esc(role), "span class=pm-role")}<span class=pm-w>'
                         f'{MV.editable("words", words, _inline(words), "span class=pm-t")}{_opens(words, base, url_of)}'
                         f'{btn}</span>{detail}{sub(c.id)}</li>')
        return f'<ul class=pm-sub>{"".join(items)}</ul>'

    arc = MT.display(" ".join(split_note(mm.root)[1]))
    out = MV.render(MT.display(mm.root.text), arc, [], asks, paras, task=rel, file=rel, inline=_inline,
                    chips=lambda s, words, note: _opens(words, base, url_of), plabel=lambda x: labels.get(x, x),
                    pnode=lambda pid: _opens(nodes[pid].text, base, url_of), more=more, sub=sub,
                    endpoint=ENDPOINT, extras=True)
    if not editable:                                   # the static page: read, nothing to type into
        out = out.replace(" contenteditable=plaintext-only", "")
        out = re.sub(r"<li class=pm-add>.*?</li>|<div class=pm-addp>.*?</div>|<button type=button class=pm-pen[^>]*>✎</button>",
                     "", out)
    return out


def fragment(md: Path, rel: str = "", editable: bool = True, url_of=None) -> str:
    """The map of one `.mindmap.md`. `rel`: the file's path from the host's root, where its edits post; `url_of(path)`:
    where the host opens a linked file (a picture, a drawing, a page)."""
    mm = MT.load(md)
    if editable and MT.ensure_ids(mm):
        MT.save(mm, md)                               # a bullet typed by hand gets its id before it can be edited
    return draw(mm, rel, editable, Path(md).parent, url_of)


# ── one change into the file: the payload §1's map sends ───────────────────────────────────────────────────
def act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """(status, reply) for one change made on the map, the payload a draft's §1 map sends to `/_board/draft-plan`:
    `words` or `role` of a point `s`; `para` (a first-level node's words) or `ask` (the question it hands on) of `p`;
    `arc` (the root's line); `add` (a point under `p`, after `after`, with its `role`); `addpara` (a first-level node
    after `after`); `drop` a point; `move` a point `s` into `p`, before `before`; and `note` (a point's detail, lines).
    `was` is what the page showed: a change to words that changed on disk since is refused."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    md = (root / str(p.get("task") or p.get("file") or "").strip("/")).resolve()
    if not (md.is_file() and md.name.endswith(MT.SUFFIX) and root in md.parents):
        return 400, {"ok": False, "err": "no such mind map"}
    what, value, was = str(p.get("what") or ""), norm(p.get("value")), norm(p.get("was"))
    if any(c in value for c in "<>") or len(value) > 4000:
        return 400, {"ok": False, "err": "plain words only"}
    mm = MT.load(md)
    MT.ensure_ids(mm)
    s, pid = str(p.get("s") or ""), str(p.get("p") or "")
    gone = (409, {"ok": False, "err": "it changed on disk; reload"})
    out = {"ok": True}
    if what in ("words", "role", "drop", "note"):
        node, parent = MT.find(mm, s)
        if node is None or parent is None:
            return gone
        role, words = split_role(node.text)
        if what == "note":
            ask, lines = split_note(node)
            if norm("\n".join(lines)) != was:
                return gone
            new = [ln.rstrip() for ln in str(p.get("value") or "").replace("\r", "").split("\n") if ln.strip()]
            node.note = ([f"→ {ask}"] if ask else []) + [MT.BULLET.sub(lambda m: m.group(1) + "· " + m.group(2), ln)
                                                         for ln in new]      # a detail line never becomes a node
        elif norm(role if what == "role" else words) != was:
            return gone
        elif what == "drop":
            k = parent.children.index(node)
            parent.children[k:k + 1] = node.children          # what hung under it moves up
        else:
            if what == "words" and not value:
                return 400, {"ok": False, "err": "empty: take the point out instead"}
            role, words = (value, words) if what == "role" else (role, value)
            node.text = (f"[{role}] " if role else "") + words
            out["html"] = esc(value) if what == "role" else _inline(value)
    elif what in ("para", "ask"):
        node, parent = MT.find(mm, pid)
        if node is None or parent is not mm.root:
            return gone
        ask, lines = split_note(node)
        if what == "para":
            kind, name = split_role(node.text)
            if norm(name) != was:
                return gone
            if not value:
                return 400, {"ok": False, "err": "a branch needs a name"}
            node.text = (f"[{kind}] " if kind else "") + value
        else:
            if norm(ask) != was:
                return gone
            node.note = ([f"→ {value}"] if value else []) + lines
        out["html"] = esc(value)
    elif what == "arc":
        if MT.display(" ".join(split_note(mm.root)[1])) != was:
            return gone
        mm.root.note = [value] if value else []
        out["html"] = esc(value)
    elif what in ("add", "addpara"):
        if not value:
            return 400, {"ok": False, "err": "empty"}
        under = mm.root if what == "addpara" else MT.find(mm, pid)[0]
        if under is None:
            return gone
        role = norm(p.get("role"))
        new = MT.Node(next(MT.next_ids({n.id for n, *_ in MT.walk(mm.root)})),
                      (f"[{role}] " if role and what == "add" else "") + value)
        ids, after = [c.id for c in under.children], str(p.get("after") or "")
        under.children.insert(ids.index(after) + 1 if after in ids else (0 if not after and what == "add" else len(ids)), new)
        out["s"] = new.id
    elif what == "move":
        node, parent = MT.find(mm, s)
        under = MT.find(mm, pid)[0]
        if node is None or parent is None or under is None:
            return gone
        if any(x is under for x, *_ in MT.walk(node)):
            return 400, {"ok": False, "err": "a point cannot go under itself"}
        parent.children.remove(node)
        ids = [c.id for c in under.children]
        before = str(p.get("before") or "")
        under.children.insert(ids.index(before) if before in ids else len(ids), node)
    else:
        return 400, {"ok": False, "err": f"unknown change {what!r}"}
    MT.save(mm, md)
    with open(MT.views(md)["html"], "w", encoding="utf-8", newline="\n") as f:     # the static page follows the file
        f.write(MH.page(mm))
    return 200, out
