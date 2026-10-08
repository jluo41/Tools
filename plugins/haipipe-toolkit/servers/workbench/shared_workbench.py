"""The Shared Workbench's own site, laid out like every other workbench.

`/_board/shared?guide=<view>` has the same header, band and Space row as the
Insight or Paper workbench, with the shared Guide mounted on that row the same
way (`mount_guide`). Guide is its only Space and explains the Shared Workbench
itself (the `shared` entry in `guide_families.py`). It has no Board, so it
reads nothing but this folder and writes nothing. All URLs are origin-relative.
"""

from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from live.guide_families import FAMILIES
from live.workbench_guide import OLD_VIEWS, VIEWS, esc, mount_guide

HERE = Path(__file__).resolve().parent
# The look of the other workbenches (servers/workbench-insight/insightboard.py).
CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--acc:#3e5c84;--acc-soft:#e6edf5}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--acc:#8aa7cc;--acc-soft:#22304a}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1600px}h1{font-size:18px;margin:0 0 2px}a{color:var(--acc)}.mut{color:var(--mut);font-size:13px}
.dataset{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;background:var(--acc-soft);color:var(--acc);font-size:14px}
.spaces{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}
.shell{border:1px solid var(--line);border-radius:10px;padding:12px 16px 16px}
@media(max-width:600px){body{padding:12px}.spaces{flex-wrap:nowrap;overflow-x:auto}}
"""


# No tab icon of its own (JL 261003: "just the default one"). An empty icon keeps the
# browser's default: without it the browser asks for /favicon.ico, which the host forwards
# to the Excalidraw service, and the tab shows Excalidraw's mark.
ICON = "data:,"


def band():
    """One line, like a Board's dataset band: what this Workbench is and who reuses it."""
    users = [profile["label"] for key, profile in FAMILIES.items() if key != "shared"]
    modules = len(list(HERE.glob("*.py")))
    return (f"workbench · reused by {len(users)} Workbench families ({', '.join(users)}) · "
            f"Studio: draw, chat, terminal · Guide: read-only · {modules} Python modules")


def page_html():
    document = ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
                f'<title>🧩 Shared Workbench</title><link rel="icon" href="{ICON}"><style>{CSS}</style></head><body><main>'
                '<header><h1>🧩 Shared Workbench</h1></header>'
                f'<div class=dataset>{esc(band())}</div>'
                '<nav class=spaces></nav>'
                '<section class=pane><div class=shell><p class=mut>Guide is this Workbench\'s only Space. '
                'Studio has no page of its own: it appears inside each workbench that draws or chats.</p></div></section>'
                '</main></body></html>')
    return mount_guide(document, "shared", {"path": "", "file": ""}, "nav.spaces", ".pane")


class SharedWorkbenchMixin:
    def shared_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        requested = (query.get("guide") or [""])[0]
        view = OLD_VIEWS.get(requested, requested)
        long_form = urlparse(self.path).path.rstrip("/") == "/_board/shared"
        if long_form or view != requested or view not in dict((key, label) for key, label, _ in VIEWS):
            # One address, /w/shared?guide=<view>: Guide is the only Space, so a View is always open.
            self.send_response(303)
            target = view if view in dict((key, label) for key, label, _ in VIEWS) else VIEWS[0][0]
            self.send_header("Location", "/w/shared?" + urlencode({"guide": target}))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        return self.guide_send(page_html(), head_only=head_only)
