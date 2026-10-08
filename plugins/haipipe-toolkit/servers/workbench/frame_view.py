"""GET /_board/workbench?path=<folder>[&space=<Space>][&sub=<subspace>][&theme=<name>][&format=json]
GET /_board/workbench?view=<view>&path=<Page .md>[&...]

The base frame (frame.py) over one Block, Job or Task folder, in the theme its Block belongs to
(or `theme=`), else the vanilla workbench. Without `path` it lists the Blocks under the root.

With `view=`, one Page Task view on its own, the page a Task Space shows in place (frame.PAGE_VIEWS).
Each was a route of its own (/_board/draft, /_board/runs, ...: the old Page workbench, one page per
tab); those addresses still answer, as this one (serve.py PAGE_VIEW_ROUTES; JL 261007: "why not
merge them into the base").
"""
from pathlib import Path
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse

from live import frame


def _blocks(root: Path, depth: int = 4) -> list:
    """Block folders under root (bNN_* with a face), shallow first; private and old folders skipped."""
    found, frontier = [], [root]
    for _ in range(depth):
        nxt = []
        for d in frontier:
            try:
                kids = sorted(p for p in d.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))
            except OSError:
                continue
            for p in kids:
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
        return self.guide_send(frame.render(theme, root, folder, space, get("sub")), code,
                               head_only=head_only)
