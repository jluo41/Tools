"""A work page's core views as bands in one view (JL 261124: "I want them into one view, and each previous view will
be the section name"; "the things here to the band"; then "I just asked for the overview and plan and Findings to be in
one view ... do you want to make them back?"): Overview, Plan + Results, Findings and Delivery are bands of the one Main
view; every other view (Design, Block UI, Job UI, Task UI, Docs, ...) keeps its own button beside Main. An old link that
names a core view scrolls to its band (#band-<key>)."""
from __future__ import annotations

import json
import re

from live import frame

CORE = ("overview", "mindmap", "standing", "findings", "delivery")   # the views that become bands of Main
MAIN = "Main"
EMOJI = {"overview": "🧭", "design": "📐", "standing": "📊", "findings": "🔎", "delivery": "📦", "docs": "📚"}
OWN_HEAD = re.compile(r"<h3 class=wk-band>📋 Review Content</h3>|<h2>📋 Review Content</h2>")


PANE_CSS = "<style>.view-pane>.view-band>h2{display:none}</style>"
PANE_JS = """<script>(function(){if(window.__panesOn)return;window.__panesOn=1;
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.section-views a[data-pane-to]');
 if(!a||e.metaKey||e.ctrlKey||e.shiftKey||e.button)return;e.preventDefault();var k=a.dataset.paneTo;
 document.querySelectorAll('[data-pane]').forEach(function(p){p.hidden=p.dataset.pane!==k;});
 a.parentNode.querySelectorAll('a').forEach(function(x){x.toggleAttribute('aria-current',x===a);if(x===a)x.setAttribute('aria-current','page');});
 history.replaceState(null,'',a.href);});   // a view switch is a button, not a new page (JL 261125)
})();</script>"""


def panes(views: dict, group: str = "") -> str:
    """Main (the core views as bands) and each other view as its own pane, all built once; the bar's buttons show one
    pane and hide the rest, so switching a view never reloads the page (JL 261125: "why I change the view, the whole
    page will be refreshed?")."""
    core, rest = split(views)
    shown = group if group in rest else "main"
    out = [f'<div data-pane="main"{"" if shown == "main" else " hidden"}>{merge(core, group if shown == "main" else "")}</div>']
    for key, view in rest.items():
        out.append(f'<div class="view-pane" data-pane="{frame.esc(key)}"{"" if shown == key else " hidden"}>{merge({key: view})}</div>')
    return PANE_CSS + "".join(out) + PANE_JS


def merge(views: dict, group: str = "") -> str:
    """Every view's body under its own band, in the views' order; a view that draws nothing is not shown."""
    out = []
    for key, (name, body) in views.items():
        html = body() if callable(body) else body
        html = OWN_HEAD.sub("", html or "", count=1)          # its own Review Content heading: the band names it now
        if not re.sub(r"<style\b.*?</style>|<script\b.*?</script>|\s", "", html, flags=re.S):
            continue
        name = re.sub(r"^\W+\s*", "", name) or name
        out.append(f'<section class="work-section-group view-band" id="band-{frame.esc(key)}" data-view="{frame.esc(key)}">'
                   f'<h2>{EMOJI.get(key, "📋")} {frame.esc(name)}</h2>{html}</section>')
    jump = (f'<script>(function(){{var b=document.getElementById({json.dumps("band-" + group)});'
            f'if(b)b.scrollIntoView();}})();</script>' if group and group in views else "")
    return "".join(out) + jump


def split(views: dict) -> tuple[dict, dict]:
    """(the core views, drawn as bands of Main; the other views, each its own button)."""
    return ({k: v for k, v in views.items() if k in CORE}, {k: v for k, v in views.items() if k not in CORE})


def bar(views: dict, current: str, url) -> str:
    """Main first, then one button per other view; `url(key)` is the link of a view (None: Main)."""
    core, rest = split(views)
    keys = [(None, MAIN)] + [(k, n) for k, (n, _) in rest.items()]
    return ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(url(k))}" data-pane-to="{frame.esc(k or "main")}"'
        + (' aria-current="page"' if (k or MAIN) == (current or MAIN) else '')
        + f'>{frame.esc(n)}</a>' for k, n in keys) + '</nav>')
