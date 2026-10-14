"""GET /_board/workbench?path=<folder>[&space=<Space>][&sub=<subspace>][&studio=1][&theme=<name>][&format=json]
GET /_board/workbench?view=<view>&path=<Page .md>[&...]
GET /_board/workbench?view=docx&path=<file .docx>       a Word file read in place (frame.docx_preview)
GET /_board/workbench?view=pptx&path=<file .pptx>       a deck drawn slide by slide (frame.pptx_preview)

The base frame (frame.py) over one Block, Job or Task folder, in the theme its Block belongs to
(or `theme=`), else the vanilla workbench. Without `path` it lists the Blocks under the root.

A link to a folder that was renamed still opens (JL 261012: "I cannot open you anymore"): the folder keeps
its old name in its face, `renamed-from: <old name>` (or a list), and the old address answers 302 to the new one
(`renamed`), the Space, subspace and anchor kept.

With `view=`, one Page Task view on its own, the page a Task Space shows in place (frame.PAGE_VIEWS).
Each was a route of its own (/_board/draft, /_board/runs, ...: the old Page workbench, one page per
tab); those addresses still answer, as this one (serve.py PAGE_VIEW_ROUTES; JL 261007: "why not
merge them into the base").
"""
import re
from pathlib import Path
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse

import yaml

from live import frame


def renamed(root: Path, raw: str) -> str:
    """A missing SPACE-relative path, each gone part replaced by the sibling folder whose face says
    `renamed-from: <that part>`; '' when some part has no such sibling."""
    here, out = root, []
    for part in [x for x in raw.strip("/").split("/") if x]:
        if (here / part).is_dir() or (here / part).is_file():
            here, out = here / part, out + [part]
            continue
        found = None
        for sib in (sorted(p for p in here.iterdir() if p.is_dir()) if here.is_dir() else []):
            md = frame.face(sib)
            if not md:
                continue
            text = md.read_text(encoding="utf-8", errors="ignore")[:4000]
            m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
            # a cowork face keeps its fields as bare lines under its title, not as front matter
            head = m.group(1) if m else "\n".join(x for x in text.splitlines()[:60] if x.startswith("renamed-from:"))
            try:
                was = (yaml.safe_load(head) or {}).get("renamed-from") if head else None
            except yaml.YAMLError:
                was = None
            if part in ([was] if isinstance(was, str) else was or []):
                found = sib
                break
        if found is None:
            return ""
        here, out = found, out + [found.name]
    return "/".join(out)


def _blocks(root: Path, depth: int = 4) -> list:
    """Block folders under root (bNN_* with a face), shallow first; private and old folders skipped, and
    a link to a folder outside the root (WellDoc's Tools -> ../Tools-SPACE, 261009), which no path= reaches."""
    found, frontier, top = [], [root], root.resolve()
    for _ in range(depth):
        nxt = []
        for d in frontier:
            try:
                kids = sorted(p for p in d.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))
            except OSError:
                continue
            for p in kids:
                if top not in p.resolve().parents:
                    continue
                if frame.level_of(p) == "Block" and frame.face(p):
                    found.append(p)
                elif p.name not in ("node_modules", "results", "runs"):
                    nxt.append(p)
        frontier = nxt
    return found[:300]


# a Page Task view -> the method that draws it (workbench/task-page/); each reads path= and file=
VIEW_METHODS = {"folder": "folderstat_view", "draft": "outline_view", "value": "value_view",
                "evidence": "evidence_tab_view", "delivery": "delivery_tab_view", "runs": "runs_view",
                "pageruns": "pageruns_view"}


class FrameMixin:
    def page_task_view(self, view, head_only=False):
        """One Page Task view, drawn by its own method from the same query, `view=` left out."""
        rest = [(k, v) for k, v in parse_qsl(urlparse(self.path).query, keep_blank_values=True) if k != "view"]
        self.path = frame.ROUTE + ("?" + urlencode(rest) if rest else "")
        method = getattr(self, VIEW_METHODS[view])
        return method() if view == "pageruns" else method(head_only=head_only)

    def workbench_frame_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        get = lambda key: (query.get(key) or [""])[0]
        if get("view") in VIEW_METHODS:
            return self.page_task_view(get("view"), head_only=head_only)
        root = Path(self.root).resolve()
        if get("view") == "docx":                    # a Word file read in place, read only (JL 261011)
            doc = (root / get("path").lstrip("/")).resolve()
            if root not in doc.parents or doc.suffix.lower() != ".docx" or not doc.is_file():
                return self.guide_send("<h1>Not found</h1><p>No such .docx under this root.</p>", 404,
                                       head_only=head_only)
            try:
                return self.guide_send(frame.docx_preview(doc, root), 200, head_only=head_only)
            except Exception as err:                 # a broken package says so, never the server
                return self.guide_send(f"<p>This .docx could not be read: {frame._e(err)}</p>", 200,
                                       head_only=head_only)
        if get("view") == "pptx":                    # a deck drawn slide by slide, read only (JL 261014)
            deck = (root / get("path").lstrip("/")).resolve()
            if root not in deck.parents or deck.suffix.lower() != ".pptx" or not deck.is_file():
                return self.guide_send("<h1>Not found</h1><p>No such .pptx under this root.</p>", 404,
                                       head_only=head_only)
            if get("media"):                         # one picture of a slide, from inside the package
                got = frame.pptx_media(deck, get("media"))
                if not got:
                    return self.guide_send("<h1>Not found</h1>", 404, head_only=head_only)
                return self.guide_send(got[0], 200, got[1], head_only=head_only)
            try:
                return self.guide_send(frame.pptx_preview(deck, root), 200, head_only=head_only)
            except Exception as err:                 # a broken package says so, never the server
                return self.guide_send(f"<p>This .pptx could not be read: {frame._e(err)}</p>", 200,
                                       head_only=head_only)
        if get("view") == "eml":                     # an email saved as it came, read only (b10 s04-D08)
            mail = (root / get("path").lstrip("/")).resolve()
            if root not in mail.parents or mail.suffix.lower() != ".eml" or not mail.is_file():
                return self.guide_send("<h1>Not found</h1><p>No such .eml under this root.</p>", 404,
                                       head_only=head_only)
            try:
                return self.guide_send(frame.eml_preview(mail, root), 200, head_only=head_only)
            except Exception as err:                 # a broken message says so, never the server
                return self.guide_send(f"<p>This .eml could not be read: {frame._e(err)}</p>", 200,
                                       head_only=head_only)
        if get("view") == "dir":                     # one folder's rows, for Studio › Folder when it opens (b10 s09)
            here = (root / get("path").lstrip("/")).resolve()
            if not (here == root or root in here.parents) or not here.is_dir():
                return self.guide_send("<li class=mut>No such folder under this root.</li>", 404, head_only=head_only)
            return self.guide_send(frame.folder_rows(here, root, None if get("all") else 300), 200, head_only=head_only)
        raw = get("path").lstrip("/")
        code = 200
        if not raw:
            rows = "".join(f'<li><a href="{frame.ROUTE}?{urlencode({"path": frame._rel(b, root)})}">'
                           f'{frame._e(frame._rel(b, root))}</a></li>' for b in _blocks(root))
            body = ('<!doctype html><meta charset=utf-8><title>🧭 Workbench · Blocks</title>'
                    f'<h1>🧭 Workbench · Blocks</h1><ul>{rows or "<li>No Blocks under this root.</li>"}</ul>')
            return self.guide_send(body, code, head_only=head_only)
        folder = (root / raw).resolve()
        if folder.is_file():
            folder = folder.parent
        if root not in folder.parents and folder != root or not folder.is_dir():
            moved = renamed(root, raw) if root in folder.parents else ""
            if moved:                                # an old link to a renamed folder: send it on
                pairs = [(k, moved if k == "path" else v) for k, v in parse_qsl(urlparse(self.path).query,
                                                                                keep_blank_values=True)]
                self.send_response(302)
                self.send_header("Location", f"{frame.ROUTE}?{urlencode(pairs)}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            return self.guide_send("<h1>Not found</h1><p>No such folder under this root.</p>", 404,
                                   head_only=head_only)
        themes = frame.themes()
        name = get("theme") or frame.theme_of(folder, root)
        theme = themes.get(name, frame.VANILLA)
        if get("format") == "json":
            return self.guide_send(frame.frame_json(theme, root, folder, get("sub")), code,
                                   "application/json; charset=utf-8", head_only=head_only)
        # an older link (`/w/<block>?view=questions#question-QNN`) opens the same rows in Audience Report
        space = get("space") or ("Audience Report" if get("view") == "questions" else "")
        return self.guide_send(frame.render(theme, root, folder, space, get("sub"), studio=get("studio") == "1"), code,
                               head_only=head_only)
