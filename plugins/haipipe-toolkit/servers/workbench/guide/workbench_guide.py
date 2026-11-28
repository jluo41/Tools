"""Shared Guide Space over family definitions; no instance ledger or writer.

The existing Excalidraw proxy opens virtual, source-backed Guide scenes in
its isolated viewing mode. Working Studio files and their save API retain
their native ownership. Guide's SPACE link may use a configured SPACE URL; its Project link and other URLs
are origin-relative.

The Guide is split by responsibility; this module keeps the pages (guide_html, method_page_html), the HTTP mixin and
thin re-exports so `from live.workbench_guide import ...` keeps working:
  guide_core.py         paths, Views, URLs, a family's profile, declared sources, mount_guide
  guide_drawing.py      the RoadMap drawing: Excalidraw scenes and their SVG projection
  guide_tables.py       the Workbench Table, its rows and the Guide Space's Runs panel
  guide_level_cards.py  the card Guide (Block · Job · Task) and level_steps
"""

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

from live.guide_families import ALIASES, FAMILIES, LEVEL_NAMES, family_key  # noqa: F401
from live.guide_core import (  # noqa: F401
    DRAW_NAMES, HERE, OLD_VIEWS, REPOSITORY, STUDIO_INDEX, VIEWS, contract_path, drawing_url, esc,
    family_drawing, family_profile, folder_matches, instance, mount_guide, script_json, url)
from live.guide_drawing import Scene, flow_scene, guide_scene, table_scene, wrap  # noqa: F401
from live.guide_tables import TABLE_COLUMNS, TABLE_HEAD, guide_runs, table_rows, workbench_table  # noqa: F401
from live.guide_level_cards import (  # noqa: F401
    FOLDED, LEVEL_CSS, LEVEL_HEAD, LEVEL_WORD, _card, _count, _level_folders, drawing_cards_html,
    level_steps, level_view, paper_cards_html, project_link, space_cards_html, step_cards_html)


def drawing_row(family, view, context, opened=False):
    params = dict(family=family, view=view, **context)
    canvas = url(mode="canvas", guide="1", board=url(mode="scene", **params).lstrip("/"), **params)
    vector = url(mode="svg", **params)
    return (f'<details class="wg-drawing" data-drawing="{view}"{" open" if opened else ""}>'
            # the card is its name only (JL 261003: "Make the card clean")
            f'<summary><span><strong>{DRAW_NAMES[view]}</strong></span></summary><div class="wg-drawing-body">'
            f'<div class="wg-canvas-actions"><span>{esc(family)} / {view}.excalidraw</span>'
            f'<span><a href="{esc(url(mode="scene", **params))}" download="{esc(family)}-{view}.excalidraw">Download Excalidraw</a> · '
            f'<a href="{esc(canvas)}" target="_blank" rel="noopener">Open full screen ↗</a></span></div>'
            f'<iframe title="{esc(DRAW_NAMES[view])}" referrerpolicy="no-referrer" data-src="{esc(canvas)}"></iframe>'
            f'<noscript><img src="{esc(vector)}" alt="{esc(DRAW_NAMES[view])}"></noscript>'
            '</div></details>')


def explain_html(profile, view, context, family=None):
    """A family's own explanation page for one Guide View (its optional `explain` entry:
    view -> (route, params)), opened inside Guide. The family's presenter renders and owns
    it; Guide only frames it, for the instance the context names."""
    explain = (profile.get("explain") or {}).get(view)
    if not explain:
        return ""
    route, params, title = (tuple(explain) + ("", ""))[:3]
    drawing = route == "/_excalidraw/"
    # a design drawing opens read-only in Guide's viewing mode (guide=1), at a fixed canvas height
    source = (drawing_url(family, "explain-" + view, family_drawing(profile, "explain-" + view) or "") if drawing and family else
              route + "?" + urlencode(dict(params, guide="1") if drawing else dict(params, path=context.get("path") or "")))
    size = "height:550px" if drawing else "min-height:70vh"
    # a titled explanation folds like the RoadMap card, closed at first so the View opens as a list
    # of cards (JL 261003: "why this draw cannot be hidden?", "make it into this style"), and its
    # frame loads when the card opens (guide.js); an untitled one is the View's body and stays open
    head, tail = ((f'<details class="wg-drawing wg-explain" data-drawing="{esc(view)}-explain"><summary><span><strong>' + esc(title)
                   + '</strong></span></summary><div class="wg-drawing-body">', '</div></details>') if title else
                  ('<section class="wg-explain">', '</section>'))
    return (head +
            f'<iframe class="wg-explain-frame" title="{esc(profile["label"])} · {esc(view)}" {"data-src" if title else "src"}="{esc(source)}" '
            # no referrer: the Excalidraw viewer refuses a same-site embed that sends one
            'referrerpolicy="no-referrer" '
            f'style="display:block;width:100%;{size};border:0"></iframe>'
            '<script>addEventListener("message",function(e){if(e.origin!==location.origin||'
            'e.data?.kind!=="hai-explain-height")return;document.querySelectorAll(".wg-explain-frame").forEach('
            'function(f){if(f.contentWindow===e.source)f.style.height=Math.ceil(e.data.height)+"px"})})</script>' + tail)


def guide_html(family, view, context, embedded=False, tab_url=None, prelude="", title=None, root=None,
               index_url=STUDIO_INDEX):
    """One Guide View. A host page may supply its own View links and a prelude above them."""
    view = OLD_VIEWS.get(view, view)
    profile = family_profile(family, context)
    tab_url = tab_url or (lambda key: url(family=family, view=key, embed=int(embedded), **context))
    css = (HERE / "assets/guide.css").read_text(encoding="utf-8")
    js = (HERE / "assets/guide.js").read_text(encoding="utf-8")
    parsed_index = urlparse(index_url)
    if not (index_url.startswith("/") and not index_url.startswith("//")) and not (
            parsed_index.scheme in ("http", "https") and parsed_index.netloc):
        index_url = STUDIO_INDEX
    # SPACE and Project leave the whole workbench, including when Guide is shown in its iframe: SPACE opens
    # the SPACE Home, Project the Home showing only this folder's Project (JL 261012: "could you make the
    # index to be SPACE, and also I want to have a link to the Project"); a bar parts them from the Views.
    tabs = f'<a href="{esc(index_url)}" target="_top" data-guide-index>SPACE</a>'
    project = project_link(context, root)
    if project:
        tabs += (f'<a href="{esc(project[0])}" target="_top" data-guide-project '
                 f'title="{esc(project[1])}">Project</a>')
    tabs += '<span class="wg-views-bar" aria-hidden="true"></span>'
    tabs += "".join(f'<a href="{esc(tab_url(key))}" '
                   f'aria-current="{("page" if key == view else "false")}">{label}</a>' for key, label, _ in VIEWS)
    source_links = "".join(f'<li><a href="{esc(url(mode="source", family=family, source=i))}" '
                          f'target="_blank" rel="noopener">{esc(Path(item["path"]).parent.name)}</a>'
                          f'<span>{esc(item["role"])}</span></li>' for i, item in enumerate(profile["skills"]))
    explain = profile.get("explain") or {}

    def lead(keys):
        """A family's own explanation pages for these View keys: before the View's body or after it."""
        first = "".join(explain_html(profile, key, context, family) for key in keys
                        if len(explain.get(key) or ()) > 3 and explain[key][3] in ("first", "only"))
        after = "".join(explain_html(profile, key, context, family) for key in keys
                        if explain.get(key) and not (len(explain[key]) > 3 and explain[key][3] in ("first", "only")))
        return first, after

    section = lambda title, text: f'<section class="wg-explanation"><h2>{esc(title)}</h2><p>{esc(text)}</p></section>'
    if view == "description":
        first, after = lead(["description"])
        content = first + f'<section class="wg-explanation"><p>{esc(profile.get("description") or profile["boundary"])}</p></section>'
        content += "".join(section(name + " Space", body) for name, body in profile["spaces"])
        content += after
    elif view == "method":
        first, after = lead(["method", "methods"])
        # "only": the family's page carries its own steps, so Guide's list would repeat them (JL 261003,
        # Design: "why we still have this? I am thinking to merge this together")
        only = (explain.get("method") or ())[3:4] == ("only",)
        steps = "" if only else "".join(section(f"{i}. {name}", body) for i, (name, body) in enumerate(profile["method"], 1))
        content = first + steps + after
    elif view == "roadmap-draw":
        first, after = lead(["roadmap-draw", "skill-set", "workbench", "folder-map"])
        folders = "".join((f'<li><a href="{esc(url(mode="folder", family=family, row=i, **context))}" target="_blank" '
                           f'rel="noopener">{esc(surface)} · <code>{esc(pattern)}</code> ↗</a></li>') if instance(context) else
                          f'<li>{esc(surface)} · <code>{esc(pattern)}</code></li>'
                          for i, (surface, _, pattern, _) in enumerate(profile["folders"]))
        # a family with a Workbench Table shows it in place of the Skills and Workbench lists (JL 261002)
        table = workbench_table(profile)
        lists = table or ('<section class="wg-explanation"><h2>Skills</h2><ul class="wg-sources">' + source_links + '</ul></section>'
                          '<section class="wg-explanation"><h2>Workbench</h2><ul class="wg-sources">' +
                          "".join(f'<li>{esc(name)} Space<span>{esc(body)}</span></li>' for name, body in profile["spaces"]) +
                          '</ul></section>')
        # a family with a Workbench Table shows no Folders list beside it (JL 261002: "remove this part")
        folders = ('' if table else
                   f'<section class="wg-explanation"><h2>Folders</h2><ul class="wg-sources">{folders}</ul></section>')
        content = first + drawing_row(family, view, context, not first) + lists + folders + after
    else:
        first, after = lead(["related-paper"])
        # a family's papers table (skills/0_utils/table-papers) renders here through the shared
        # Related Paper cards; a family whose own papers page leads the View needs neither
        papers = ""
        if profile.get("papers_table") and not (profile.get("explain") or {}).get("related-paper"):
            from live.related_papers import PAPERS_CSS, PAPERS_JS, papers_page
            papers = ('<style>.wg-papers{--line:var(--wg-rule);--mut:var(--wg-muted);--acc:var(--wg-blue);'
                      '--fg:var(--wg-ink);--soft:var(--wg-wash);--ok:#2f9e44}' + PAPERS_CSS
                      # Guide's frame takes its page's height: a PDF sized by the viewport would grow it without end
                      + '.wg-papers .rp-frame{height:720px}</style>'
                      '<section class="wg-papers">' + papers_page(None, REPOSITORY.parent, REPOSITORY / profile["papers_table"])
                      + f'</section><script>{PAPERS_JS}</script>')
        none = ('' if papers or (profile.get("explain") or {}).get("related-paper") else
                '<section class="wg-explanation"><p>No related papers are declared for this family yet. '
                'A workbench keeps them in <code>ref/&lt;name&gt;-papers.md</code> beside its skill '
                '(skills/0_utils/table-papers) and names it as <code>papers_table</code> in its '
                '<code>guide_families.py</code> entry.</p></section>')
        content = first + papers + none + after
    if profile.get("levels"):                       # the card Guide (b03 s31-D05 to D08)
        if view == "description":                   # the earlier body leads with the same paragraph
            content = ('<section class="wg-explanation"><h2>Skills</h2><ul class="wg-sources">' + source_links
                       + f'</ul></section><section class="wg-explanation"><h2>Boundary</h2><p>{esc(profile.get("boundary", ""))}</p></section>')
        content = level_view(family, view, profile, context, root, content)
        css += LEVEL_CSS
    heading = prelude or ('' if embedded else f'<header><h1>{esc(profile["label"])} Workbench</h1><p>Guide</p></header>')
    boot = dict(family=family, view=view, context=context)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title or profile["label"] + " · Guide")}</title><link rel="icon" href="data:,"><style>{css}</style></head><body>'
            # the Views and their content sit in one box, as a workbench Space's content does (JL 261003)
            # the Guide Space's runs sit in the shared Runs panel on the right, as every Space's do
            f'{heading}<div class="split wg-split"><div class="wg-shell space-main"><nav class="wg-views" aria-label="Guide Views">{tabs}</nav><main>'
            f'<h1>{dict((key, label) for key, label, _ in VIEWS)[view]}</h1>{content}</main></div>{guide_runs(profile, view)}</div>'
            f'<script type="application/json" id="wg-boot">{script_json(boot)}</script><script>{js}</script></body></html>')


# Guide › Method's family page (JL 261003: "create a method canvas as they do"): the family's
# method file with its method cards, then its methods canvas, as Insight's and Design's pages show
# them. A family names `method_doc` and `method_drawing` in its guide_families.py entry and points
# its `explain["method"]` here (mode=method); the cards and the papers are drawn by the Design
# workbench's renderer, so every family's cards look the same. The canvas opens editable: it is
# the source, and edits save back to the skill's ref/.
def method_page_html(family, profile, editable=True):
    from live.designboard import _CSS, _plain_md, method_cards
    doc = REPOSITORY / profile["method_doc"]
    papers = REPOSITORY / profile.get("papers_table", "")
    if doc.is_file():
        cards = method_cards(REPOSITORY, REPOSITORY.parent, doc, papers) if papers.is_file() else None
        page = re.sub(r"<h1>.*?</h1>", "", _plain_md(doc.read_text(encoding="utf-8"), cards), count=1)
        # every part folds, in the card style of Design's Method page (JL 261003: "make each
        # section collapsable", "this is not updated following others"), and every card starts
        # closed, so the page opens as a list of its parts (JL 261003: "make it into this style")
        lead, *parts = re.split(r"(?=<h2>)", page)

        def fold(part):
            title = re.match(r"<h2>(.*?)</h2>", part)
            name = re.sub(r"<[^>]+>", "", title.group(1))
            return (f'<details class=sec-fold><summary><strong>{name}</strong>'
                    f'</summary><div class=sec-body>{part[title.end():]}</div></details>')
        page = lead + "".join(fold(part) for part in parts)
        body = f'<article class=theory>{page}</article>'
    else:
        body = f'<div class=empty>No method file yet: this family keeps it as <code>{esc(profile["method_doc"])}</code>.</div>'
    drawing = profile.get("method_drawing", "")
    if drawing and (REPOSITORY / drawing).is_file():
        # view only inside Guide; it is edited full screen, in its own tab (JL 261003: an editable
        # methods canvas open in Guide beside a Page's editable RoadMap shared the browser's
        # drawing storage, and the RoadMap saved the methods drawing into its own file)
        src = drawing_url(family, "method", drawing)
        edit = "/_excalidraw/?board=" + quote("Tools/" + drawing, safe="/") + "&edit=1"
        # no file notes on screen (JL 261003): the bar holds only the way to open it full screen;
        # a host that cannot edit (`--only`) shows no edit link
        canvas = ('<div class=st-bar><span></span>'
                  + (f'<a href="{esc(edit)}" target="_blank" rel="noopener">Edit full screen ↗</a>' if editable else '')
                  + '</div>'
                  # no referrer: Excalidraw refuses a same-site embed that sends one
                  f'<iframe class=st-frame title="{esc(profile["label"])} methods" referrerpolicy="no-referrer" '
                  f'data-src="{esc(src)}"></iframe>'
                  # the canvas loads only near view: it takes focus as it loads, and a canvas loaded at
                  # once scrolls Guide down to it and leaves the page blank above (as Insight's does)
                  "<script>(function(){var fs=document.querySelectorAll('iframe.st-frame[data-src]'),"
                  "go=function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)};"
                  "if(!window.IntersectionObserver){fs.forEach(go);return}"
                  "var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)"
                  "{go(e.target);io.unobserve(e.target)}})},{rootMargin:'400px'});fs.forEach(function(f){io.observe(f)});"
                  # a reader may have left the drawing card closed: opening it loads the canvas (as Design's does)
                  "document.addEventListener('toggle',function(ev){var d=ev.target;if(d.matches&&d.matches('details.draw-fold')&&d.open)"
                  "d.querySelectorAll('iframe.st-frame[data-src]').forEach(go)},true)})()</script>")
    else:
        canvas = (f'<div class=empty>No methods drawing yet: draw it from the method file with '
                  f'<code>servers/workbench/guide/method_canvas.py</code>.</div>')
    height = ("<script>(function(){function post(){parent.postMessage({kind:'hai-explain-height',"
              "height:document.documentElement.scrollHeight},location.origin)}"
              "if(window.ResizeObserver)new ResizeObserver(post).observe(document.body);"
              "addEventListener('load',post);document.addEventListener('toggle',post,true)})()</script>")
    # a reader's folds are kept per family and part, so the page opens as it was left
    remember = ("<script>(function(){document.querySelectorAll('details.sec-fold,details.draw-fold').forEach(function(d,i){"
                f"var k='method-fold:{esc(family)}:'+i;try{{var v=localStorage.getItem(k);if(v!==null)d.open=v==='1'}}catch(e){{}}"
                "d.addEventListener('toggle',function(){try{localStorage.setItem(k,d.open?'1':'0')}catch(e){}})})})()</script>")
    # the page sits inside Guide: a pinch over it must not zoom the tab (guide-mount.js says why)
    no_pinch = ("<script>addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false})</script>")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            # inside Guide the frame takes this page's height, so nothing here is sized by the viewport
            f'<title>{esc(profile["label"])} · Method</title><link rel="icon" href="data:,"><style>{_CSS}body{{max-width:none;padding:2px 2px 12px}}'
            '.st-frame{height:640px;min-height:0}'
            # the folding cards (draw-fold, sec-fold) are Design's, from its _CSS above
            'article.theory h3{font-size:14.5px;margin:18px 0 6px}</style></head><body><main>'
            # the picture first, in the card Guide › RoadMap Draw gives "Workbench design", then the
            # document's parts (JL 261003, as Design's Method page)
            '<details class=draw-fold><summary><strong>Method design</strong></summary>'
            f'<div class=draw-body>{canvas}</div></details>{body}</main>{remember}{height}{no_pinch}</body></html>')


def _frame_folder(root, path):
    """True for a Block, Job or Task folder inside root, named as the frame names it: its face file,
    or the folder itself when it has no face."""
    from live import frame
    try:
        at = (root / path.lstrip("/")).resolve()
        at.relative_to(root.resolve())
    except (ValueError, OSError, RuntimeError):
        return False
    folder = at.parent if at.suffix == ".md" and at.is_file() else at
    return bool(path) and folder.is_dir() and frame.level_of(folder) is not None


class WorkbenchGuideMixin:
    def guide_path_allowed(self, path):
        from host_registry import static_path_allowed
        return static_path_allowed(Path(self.root), path)

    def guide_send(self, body, code=200, content_type="text/html; charset=utf-8", head_only=False):
        raw = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(raw)

    def guide_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        get = lambda key, default="": (query.get(key) or [default])[0]
        family, mode = family_key(get("family")), get("mode")
        only = getattr(self, "only", None)
        served = {family_key(name) for name in (only or ())}
        if family not in FAMILIES or (only and family not in served):
            return self.guide_send("Guide family is not served by this host.", 404, head_only=head_only)
        try:
            contract_path(family, 0)  # optional plugins must actually be present
            if mode == "method":
                return self.guide_send(method_page_html(family, family_profile(family, {}), editable=not only),
                                       head_only=head_only)
            if mode in ("drawing", "drawing-scene"):
                key = get("drawing")
                rel = family_drawing(family_profile(family, {}), key)
                if not rel or not (REPOSITORY / rel).is_file():
                    return self.guide_send("This family's Guide declares no such drawing.", 404, head_only=head_only)
                if mode == "drawing-scene":
                    return self.guide_send((REPOSITORY / rel).read_text(encoding="utf-8"),
                                           content_type="application/json; charset=utf-8", head_only=head_only)
                canonical = drawing_url(family, key, rel)
                if query != parse_qs(urlparse(canonical).query):
                    self.send_response(303)
                    self.send_header("Location", canonical)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                # the same viewer and storage isolation as mode=canvas, read only (guide=1)
                original = self.path
                self.path = "/_excalidraw/?" + urlparse(original).query
                try:
                    return self.proxy_excalidraw(head_only=head_only)
                finally:
                    self.path = original
            if mode == "source":
                path = contract_path(family, int(get("source", "0")), {"file": get("file")})
                body = f'<!doctype html><meta charset="utf-8"><title>{esc(path.name)}</title><h1>{esc(path.relative_to(REPOSITORY))}</h1><pre style="white-space:pre-wrap;overflow-wrap:anywhere">{esc(path.read_text(encoding="utf-8"))}</pre>'
                return self.guide_send(body, head_only=head_only)
            context = {"path": get("path"), "file": get("file")}
            if get("level") in LEVEL_NAMES:         # the level tab the Guide was opened from (frame.py)
                context["level"] = get("level")
            if family == "labeling" and not context["path"] and only == {"labeling"}:
                source, error = self._labeling_page_target(context["file"])
                result = (source, error)
            elif not instance(context):
                result = (None, None)  # family-only Guide (the Shared Workbench): no instance to resolve
            else:
                result = self.target(context)
                if result[0] is None and _frame_folder(Path(self.root), context.get("path") or ""):
                    # a Block, Job or Task the frame names (by its face, or by its path when it has
                    # none) that is not a Board Page: the family's Guide, its level cards read from
                    # that folder (b03 s31-D06)
                    result = (None, None)
            if result[0] is None and result[1] is not None:
                return self.guide_send(esc(result[1]), 404, head_only=head_only)
            source = Path(result[0]) if result[0] else None
            if mode == "folder" and source is None:
                return self.guide_send("Folder paths resolve only inside a Board. Open Guide from that Board.",
                                       404, head_only=head_only)
            if mode == "folder":
                matches = folder_matches(Path(self.root), source, family, int(get("row", "0")), context,
                                         self.guide_path_allowed)
                entries = []
                for match in matches:
                    entries.append(f'<h2>{esc(match.relative_to(self.root))}</h2>')
                    children = sorted(match.iterdir())[:100] if match.is_dir() else [match]
                    for child in children:
                        if not self.guide_path_allowed(child):
                            continue
                        relative = child.relative_to(self.root).as_posix()
                        entries.append(f'<p><code>{esc(child.name)}</code></p>' if child.is_dir() else
                                       f'<p><a href="/{esc(quote(relative, safe="/"))}">{esc(child.name)}</a></p>')
                message = "".join(entries) or '<p>No accessible source at this declared path in the current instance. Open the owning Workbench for private sources or external stores.</p>'
                return self.guide_send('<!doctype html><meta charset="utf-8"><title>Guide · source paths</title>' + message, head_only=head_only)
            view = OLD_VIEWS.get(get("view"), get("view") or VIEWS[0][0])
            if view not in dict((key, label) for key, label, _ in VIEWS):
                return self.guide_send("Unknown Guide View.", 404, head_only=head_only)
            if mode in ("scene", "svg", "canvas") and view not in DRAW_NAMES:
                return self.guide_send("This View has no standalone drawing.", 404, head_only=head_only)
            if mode == "scene":
                return self.guide_send(json.dumps(guide_scene(family, view, context).data()),
                                       content_type="application/json; charset=utf-8", head_only=head_only)
            if mode == "svg":
                scene = guide_scene(family, view, context)
                return self.guide_send(scene.vector(DRAW_NAMES[view]), content_type="image/svg+xml; charset=utf-8", head_only=head_only)
            if mode == "canvas":
                canonical = url(mode="canvas", guide="1",
                                board=url(mode="scene", family=family, view=view, **context).lstrip("/"),
                                family=family, view=view, **context)
                if query != parse_qs(urlparse(canonical).query):
                    # Guide uses only its own generated scene and viewing mode.
                    self.send_response(303)
                    self.send_header("Location", canonical)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                # The proxy's boot script reads board= from the browser URL.
                # Keep its existing per-iframe storage isolation and viewing mode.
                original = self.path
                self.path = "/_excalidraw/?" + urlparse(original).query
                try:
                    return self.proxy_excalidraw(head_only=head_only)
                finally:
                    self.path = original
            # Guide alone has no Spaces: a family that names its board page (`board_route`) opens there,
            # Guide open on this View, so its Spaces are beside it (JL 261003: "where are other spaces?")
            profile = family_profile(family, context)
            route = profile.get("board_route")
            if get("embed") != "1" and route and context.get("path"):
                board = Path(context["path"]).parent.as_posix()
                self.send_response(303)
                self.send_header("Location", route.format(board=quote(board, safe="/")) + "&guide=" + quote(view))
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            prelude = ""
            if get("embed") != "1" and route and profile.get("boards"):
                found = sorted(b.parent.relative_to(Path(self.root)).as_posix() for b in Path(self.root).glob(profile["boards"])
                               if self.guide_path_allowed(b))
                links = " · ".join(f'<a href="{esc(route.format(board=quote(b, safe="/")) + "&guide=" + quote(view))}">{esc(Path(b).name)}</a>'
                                   for b in found)
                prelude = (f'<header><h1>{esc(profile["label"])} Workbench</h1><p>Guide · open it on a board to see its Spaces: '
                           + (links or "no board found") + '</p></header>')
            return self.guide_send(guide_html(family, view, context, get("embed") == "1", prelude=prelude,
                                              root=Path(self.root),
                                              index_url=getattr(self, "workbench_index_url", STUDIO_INDEX)), head_only=head_only)
        except (ValueError, OSError, RuntimeError) as error:
            return self.guide_send(esc(error), 404, head_only=head_only)
