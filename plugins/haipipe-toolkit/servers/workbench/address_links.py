"""Clickable Run addresses (JL 261103: "b52.j01.t01.r01 <--- how could you make this to be clickable").

One helper for every page that prints an address: the workbench views import it as ``live.address_links``, and a skill
script that writes a preview (values.html, citations.html) imports it by path. Standard library only.

- ``resolve(addr, project)``: ``bNN.jNN[.tNN[.rNN]]`` (or ``bNN jNN tNN``) to its folder inside the Project, work/
  first, then discovery/; a Run number that is shared or missing falls back to the Task, then the Job, then the Block.
- ``href(folder, space_root)``: that folder's focus page, ``/_board/workbench?path=<rel>&layout=focus``.
- ``page_linker(folder, space_root)``: ``linkify`` set up for one page (its Project, its paper Board's writing Jobs);
  ``linked_views(views, link)`` passes each of a page's view builders through it.
- ``linkify(html, project, space_root, sections=())``: every address in the text of an HTML string (never inside a tag,
  an attribute, a link, a button, a script, a style or a textarea) as a link with ``target=_top``; a Section name
  ``tNN_<name>`` found in one of ``sections`` (writing Jobs, first hit wins) links to that Task's Work > Write view.
  Unresolvable addresses stay plain text.
"""
from __future__ import annotations

import html as _html
import re
from pathlib import Path
from urllib.parse import quote

ROUTE = "/_board/workbench"
WORLDS = ("work", "discovery")
# bNN then jNN, tNN, rNN, joined by one separator, a dot or a space, the same throughout
ADDRESS = re.compile(r"(?<![\w./-])b(\d+)(?P<sep>[. ])j(\d+)(?:(?P=sep)t(\d+)(?:(?P=sep)r(\d+))?)?(?![\w-]|\.\w)")
SECTION = re.compile(r"(?<![\w./-])t\d\d_[a-z](?:[a-z0-9_-]*[a-z0-9])?(?![\w-])")
WRITE = "&section=work&group=write"
# text inside these is left alone: a link in a link, a button or a script is wrong or does nothing
SKIP = {"a", "button", "script", "style", "textarea", "select", "option", "title", "svg", "head"}
RAW = re.compile(r"<(script|style|textarea)\b.*?</\1\s*>", re.S | re.I)
TAG = re.compile(r"<!--.*?-->|<[^>]*>", re.S)
TAGNAME = re.compile(r"<\s*(/?)\s*([a-zA-Z][\w-]*)")


def parts(addr: str) -> list[str]:
    """`b52.j01.t01.r01` or `b52 j01 t01` to ['b52', 'j01', 't01', 'r01']; [] if it is not an address."""
    m = ADDRESS.fullmatch(str(addr).strip())
    if not m:
        return []
    b, _, j, t, r = m.groups()
    return [x for x in (f"b{b}", f"j{j}", t and f"t{t}", r and f"r{r}") if x]


def _one(folder: Path, prefix: str) -> Path | None:
    hits = [c for c in sorted(folder.glob(f"{prefix}_*")) if c.is_dir()]
    return hits[0] if len(hits) == 1 else None


def _deepest(world: Path, bits: list[str]) -> tuple[int, Path | None]:
    """(how many levels matched, the deepest folder that matched once) of an address in one world."""
    here, depth = _one(world, bits[0]), 1
    if here is None:
        return 0, None
    for bit in bits[1:]:
        nxt = _one(here / "runs" if bit.startswith("r") else here, bit)
        if nxt is None:
            break
        here, depth = nxt, depth + 1
    return depth, here


def resolve(addr: str, project: Path) -> Path | None:
    """The folder an address names inside its Project: the deepest level that matches once, work/ before discovery/."""
    bits = parts(addr)
    if not bits or project is None:
        return None
    best = (0, None)
    for world in WORLDS:
        if (Path(project) / world).is_dir():
            got = _deepest(Path(project) / world, bits)
            if got[0] > best[0]:
                best = got
    return best[1]


def href(folder: Path, space_root: Path, extra: str = "") -> str:
    """The folder's focus page, origin-relative."""
    rel = Path(folder).resolve().relative_to(Path(space_root).resolve()).as_posix()
    return f"{ROUTE}?path={quote(rel, safe='/')}&layout=focus{extra}"


def project_of(folder: Path, space_root: Path | None = None) -> Path | None:
    """The Project a folder sits in: the nearest folder (itself included) with project.yaml or project.md, or named
    Project-*; None above the SPACE root."""
    folder = Path(folder).resolve()
    stop = Path(space_root).resolve() if space_root else None
    for d in (folder, *folder.parents):
        if stop is not None and d == stop.parent:
            break
        if (d / "project.yaml").is_file() or (d / "project.md").is_file() or d.name.startswith("Project-"):
            return d
    return None


def paper_board_of(folder: Path) -> Path | None:
    """The paper Board a folder sits in (<project>/paper/Paper-*), itself included."""
    folder = Path(folder).resolve()
    return next((d for d in (folder, *folder.parents) if d.parent.name == "paper" and d.name.startswith("Paper-")), None)


def writing_jobs(board: Path, first: Path | None = None) -> list[Path]:
    """A paper Board's version Jobs (not display, value, citation, evidence or submission Jobs), newest first; `first`
    (the Job a page sits in) leads. The same rule as workbench-paper's board_read.is_version."""
    if board is None:
        return []
    jobs = [d for d in sorted(Path(board).glob("j[0-9]*_*"), reverse=True)
            if d.is_dir() and not re.search(r"display|citation|cite|evidence|value|submission", d.name, re.I)]
    if first is not None and Path(first).resolve() in [j.resolve() for j in jobs]:
        jobs = [Path(first)] + [j for j in jobs if j.resolve() != Path(first).resolve()]
    return jobs


def _link(url: str, words: str, target: str) -> str:
    t = f' target="{target}"' if target else ""
    return f'<a class=addr-link href="{_html.escape(url)}"{t}>{words}</a>'


def _safe_link(folder, space_root, extra, words, target, here=None):
    """The link, or None when there is no folder, it is the page itself, or it sits outside the served root."""
    if folder is None or here is not None and Path(folder).resolve() == Path(here).resolve():
        return None
    try:
        return _link(href(folder, space_root, extra), words, target)
    except ValueError:
        return None


def linkify(text: str, project: Path | None, space_root: Path, sections=(), target: str = "_top", here: Path | None = None) -> str:
    """Every address (and Section name, when `sections` is given) in the text of `text` as a link; tags, attributes,
    comments, and the text inside a link, button, script, style or textarea stay as they are. `here`, the page's own
    folder, is never linked to itself."""
    if not text or project is None and not sections:
        return text
    cache: dict = {}

    def address(m):
        key = ("a", m.group(0))
        if key not in cache:
            f = resolve(m.group(0), project) if project is not None else None
            cache[key] = _safe_link(f, space_root, "", m.group(0), target, here)
        return cache[key] or m.group(0)

    def section(m):
        key = ("s", m.group(0))
        if key not in cache:
            f = next((Path(j) / m.group(0) for j in sections if (Path(j) / m.group(0)).is_dir()), None)
            cache[key] = _safe_link(f, space_root, WRITE, m.group(0), target, here)
        return cache[key] or m.group(0)

    def words(s: str) -> str:
        s = ADDRESS.sub(address, s) if project is not None else s
        if sections:                                 # Section names only in text the address pass left plain
            s = "".join(p if p.startswith("<a ") else SECTION.sub(section, p) for p in re.split(r"(<a [^>]*>.*?</a>)", s))
        return s

    out, depth, at = [], 0, 0
    for raw in [*RAW.finditer(text), None]:          # a script, style or textarea is copied whole
        chunk = text[at:raw.start() if raw else len(text)]
        pos = 0
        for m in TAG.finditer(chunk):
            if m.start() > pos:
                piece = chunk[pos:m.start()]
                out.append(piece if depth else words(piece))
            tag = m.group(0)
            name = TAGNAME.match(tag)
            if name and name.group(2).lower() in SKIP and not tag.endswith("/>"):
                depth = max(0, depth - 1) if name.group(1) else depth + 1
            out.append(tag)
            pos = m.end()
        if pos < len(chunk):
            out.append(chunk[pos:] if depth else words(chunk[pos:]))
        if raw:
            out.append(raw.group(0))
            at = raw.end()
    return "".join(out)


def page_linker(folder: Path, space_root: Path, target: str = "_top"):
    """`html -> html` for one page: addresses resolve in the page's Project; Section names in its paper Board's writing
    Jobs, the page's own Job first; the page itself is not linked. A page that cannot be linked comes back as it was."""
    project = project_of(folder, space_root)
    board = paper_board_of(folder)
    job = next((d for d in (Path(folder).resolve(), *Path(folder).resolve().parents) if board is not None and d.parent == board), None)
    sections = writing_jobs(board, first=job)

    def link(text):
        try:
            return linkify(text, project, space_root, sections, target, here=folder)
        except Exception:                            # a link is a help; the page itself always shows
            return text
    return link


def linked_views(views: dict, link) -> dict:
    """{key: (name, builder, ...)} with each builder's HTML (a callable or a string) passed through `link`
    (page_linker); None stays None."""
    def wrap(build):
        return (lambda: link(build())) if callable(build) else link(build) if isinstance(build, str) else build
    return {k: (v[0], wrap(v[1]), *v[2:]) if isinstance(v, tuple) and len(v) > 1 else v for k, v in views.items()}
