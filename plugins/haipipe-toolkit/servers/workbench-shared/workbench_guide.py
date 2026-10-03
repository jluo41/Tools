"""Shared Guide Space over family definitions; no instance ledger or writer.

The existing Excalidraw proxy opens virtual, source-backed Guide scenes in
its isolated viewing mode. Working Studio files and their save API retain
their native ownership. All URLs are origin-relative.
"""

import hashlib
import html
import json
import re
import textwrap
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

from live.guide_families import FAMILIES

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[3]
VIEWS = (("skill-set", "Skill set", "Which skills do what, and how do they cooperate?"),
         ("methods", "Methods", "How does this family reach a supported answer or product?"),
         ("workbench", "Workbench", "Where do I go to do or read something?"),
         ("folder-map", "Folder map", "Which owners, folders and files supply this UI?"),
         ("roadmap-draw", "RoadMap Draw", "The family's four explanatory drawings"))
DRAW_NAMES = {"skill-set": "Skill map", "methods": "Method flow", "workbench": "UI map", "folder-map": "Folder map"}


def esc(value):
    return html.escape(str(value), quote=True)


def url(**values):
    return "/_board/guide?" + urlencode(values)


def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def family_profile(family, context):
    profile = FAMILIES[family]
    if family == "design" and context.get("file") not in (None, "", "board.md"):
        return dict(profile, presenter="plugins/haipipe-toolkit/servers/workbench-design/design.py",
                    spaces=[("Design Goal", "The current design task and its criteria"),
                                     ("Design", "Independent items, rationale and supporting work"),
                                     ("Delivery", "Items whose independent Verify is currently ready")],
                    folders=[("Design Goal", "Design Page owner", "<same-stem Page>.md", "*.md"),
                             ("Design items", "Design Folder owner", "draft/<stem>-design-items.md", "draft/*-design-items.md"),
                             ("Runs", "Design Run owner", "runs/", "runs"),
                             ("Delivery", "Design delivery owner", "delivery/", "delivery")])
    return profile


def mount_guide(document, family, context, nav, native):
    """Attach one Guide button to a native Space row; retain its own layout."""
    if family not in FAMILIES or not (context.get("path") or context.get("file")):
        return document
    config = dict(family=family, context=context, nav=nav, native=native)
    styles = (HERE / "assets/guide-mount.css").read_text(encoding="utf-8")
    javascript = (HERE / "assets/guide-mount.js").read_text(encoding="utf-8")
    insertion = (f'<style>{styles}</style><script type="application/json" id="wb-guide-mount">'
                 f'{script_json(config)}</script><script>{javascript}</script>')
    return document.replace("</body>", insertion + "</body>", 1)


def contract_path(family, index, context=None):
    profile = family_profile(family, context or {})
    paths = ([item["path"] for item in profile["skills"]] + [profile["presenter"],
             "plugins/haipipe-toolkit/servers/workbench-shared/guide_families.py",
             "plugins/haipipe-toolkit/servers/workbench-shared/workbench_guide.py"])
    if index < 0 or index >= len(paths):
        raise ValueError("Unknown Guide source")
    candidate = (REPOSITORY / paths[index]).resolve()
    candidate.relative_to(REPOSITORY.resolve())
    if not candidate.is_file():
        raise FileNotFoundError(paths[index])
    return candidate


def folder_matches(root, source, family, row, context, allowed=None):
    """Resolve declared patterns inside the instance, with the static boundary."""
    from host_registry import static_path_allowed
    allowed = allowed or (lambda candidate: static_path_allowed(root, candidate))
    folders = family_profile(family, context)["folders"]
    if row < 0 or row >= len(folders):
        raise ValueError("Unknown folder mapping")
    pattern = folders[row][3]
    base = source.parent
    matches = []
    for candidate in base.glob(pattern):
        if allowed(candidate):
            matches.append(candidate)
            if len(matches) >= 80:
                break
    return sorted(matches)


class Scene:
    """Deterministic Excalidraw elements, plus an accessible SVG projection."""
    def __init__(self, family, view):
        self.prefix = family + "-" + view
        self.elements, self.svg = [], []
        self.height = 120

    def add(self, kind, x, y, width, height, **extra):
        identity = self.prefix + "-" + str(len(self.elements))
        element = dict(id=identity, type=kind, x=x, y=y, width=width, height=height,
                       angle=0, strokeColor="#495057", backgroundColor="transparent",
                       fillStyle="solid", strokeWidth=1.5, strokeStyle="solid",
                       roughness=1, opacity=100, groupIds=[], frameId=None,
                       roundness=None, seed=int(hashlib.sha256(identity.encode()).hexdigest()[:7], 16),
                       version=1, versionNonce=1, isDeleted=False, boundElements=None,
                       updated=1, link=None, locked=False)
        element.update(extra)
        self.elements.append(element)
        self.height = max(self.height, y + height + 24)
        return element

    def text(self, x, y, value, size=18, color="#495057", mono=False):
        lines = str(value).splitlines()
        self.add("text", x, y, max(map(len, lines), default=0) * size * .62,
                 len(lines) * size * 1.25, text=value, originalText=value, fontSize=size,
                 fontFamily=3 if mono else 8, textAlign="left", verticalAlign="top",
                 containerId=None, autoResize=True, lineHeight=1.25, strokeColor=color)
        for index, line in enumerate(lines):
            self.svg.append(f'<text x="{x}" y="{y + size + index * size * 1.25}" fill="{color}" '
                            f'font-size="{size}" font-family="{("monospace" if mono else "sans-serif")}">{esc(line)}</text>')

    def box(self, x, y, width, title, body="", link=None, color="#1864ab"):
        title = "\n".join(textwrap.wrap(title, width=max(1, int((width - 28) / 11.2))))
        title_height = max(52, len(title.splitlines()) * 22.5 + 24)
        height = title_height + (len(body.splitlines()) * 22 if body else 0)
        start = len(self.elements)
        box = self.add("rectangle", x, y, width, height, backgroundColor="#f8f9fa", link=link,
                       roundness={"type": 3})
        self.svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="#f8f9fa" stroke="#ced4da"/>')
        self.text(x + 14, y + 12, title, 18, color)
        if body:
            self.text(x + 14, y + title_height - 12, body, 16)
        for element in self.elements[start:]:
            element["groupIds"] = [box["id"] + "-group"]
        return height

    def arrow(self, x, y, dx, dy, label):
        self.add("arrow", x, y, abs(dx), abs(dy), points=[[0, 0], [dx, dy]],
                 lastCommittedPoint=None, startBinding=None, endBinding=None,
                 startArrowhead=None, endArrowhead="arrow", elbowed=False)
        self.svg.append(f'<path d="M{x} {y} l{dx} {dy}" stroke="#495057" fill="none" marker-end="url(#arrow)"/>')
        self.text(x + (dx / 2 - 24 if dx else 12), y + (dy / 2 - 10 if dy else -25), label, 14)

    def data(self):
        return dict(type="excalidraw", version=2, source="haipipe-workbench-guide",
                    elements=self.elements, appState={"viewBackgroundColor": "#ffffff", "gridSize": None}, files={})

    def vector(self, title):
        return ('<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 1340 %s">'
                '<title>%s</title><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
                'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="#495057"/></marker></defs>%s</svg>'
                % (self.height, esc(title), "".join(self.svg)))


def guide_scene(family, view, context):
    profile = family_profile(family, context)
    scene = Scene(family, view)
    scene.text(24, 14, profile["label"] + " · " + DRAW_NAMES[view], 26, "#1e1e1e")
    if view == "skill-set":
        for i, item in enumerate(profile["skills"]):
            scene.box(24, 68 + i * 96, 1292, Path(item["path"]).parent.name,
                      item["role"], url(mode="source", family=family, source=i), "#2b8a3e")
    elif view == "methods":
        y = 68
        for i, (name, description) in enumerate(profile["method"]):
            height = scene.box(150, y, 1030, name, description)
            if i < len(profile["method"]) - 1:
                scene.arrow(665, y + height + 4, 0, 42, "informs")
            y += height + 52
        scene.text(150, y, "Review findings and remaining questions can revise the earlier reasoning or plan.", 16)
    elif view == "workbench":
        scene.box(24, 68, 1292, "Guide Space · family explanations",
                  "Skill set / Methods / Workbench / Folder map / RoadMap Draw")
        for i, (name, content) in enumerate(profile["spaces"]):
            scene.box(24, 172 + i * 96, 1292, name + " Space", content, color="#2b8a3e")
        scene.text(24, 180 + len(profile["spaces"]) * 96,
                   "Choose Space, then its View directly underneath. Each family owns its working content and layout.", 16)
    elif view == "folder-map":
        scene.text(24, 64, "Space / View", 18)
        scene.text(300, 64, "Native owner", 18)
        scene.text(742, 64, "Repository definitions / instance conventions", 18)
        rows = [("Guide / Views", "Shared Guide owner",
                 "Repository: plugins/haipipe-toolkit/servers/workbench-shared/guide_families.py",
                 url(mode="source", family=family, source=len(profile["skills"]) + 1, **context), "defined in"),
                ("Working / UI", "Family presenter owner", "Repository: " + profile["presenter"],
                 url(mode="source", family=family, source=len(profile["skills"]), **context), "defined in")]
        rows += [(surface, owner, "Instance: " + pattern,
                  url(mode="folder", family=family, row=i, **context), "stored at")
                 for i, (surface, owner, pattern, _) in enumerate(profile["folders"])]
        y = 104
        for surface, owner, pattern, link, relationship in rows:
            scene.box(24, y, 210, surface)
            scene.box(300, y, 340, owner, color="#2b8a3e")
            # Preserve folder and file names when wrapping long source paths.
            lines, line = [], ""
            for part in re.findall(r'[^/\s]+[/\s]*|[/\s]+', pattern):
                if line and len(line + part) > 52:
                    lines.append(line.rstrip())
                    line = ""
                line += part
            if line:
                lines.append(line.rstrip())
            body = "\n".join(lines)
            height = scene.box(742, y, 574, "Source", body, link)
            scene.arrow(239, y + 28, 56, 0, "reads")
            scene.arrow(645, y + 28, 92, 0, relationship)
            y += height + 14
        scene.text(24, y + 16,
                   "Paths are conventions. Open a source node to resolve it within the selected instance.", 16)
    return scene


def drawing_row(family, view, context, opened=False):
    params = dict(family=family, view=view, **context)
    canvas = url(mode="canvas", guide="1", board=url(mode="scene", **params).lstrip("/"), **params)
    vector = url(mode="svg", **params)
    question = next(question for key, _, question in VIEWS if key == view)
    return (f'<details class="wg-drawing" data-drawing="{view}"{" open" if opened else ""}>'
            f'<summary><span><strong>{DRAW_NAMES[view]}</strong><span>{esc(question)}</span></span>'
            '<small>Family definition</small></summary><div class="wg-drawing-body">'
            f'<div class="wg-canvas-actions"><span>{esc(family)} / {view}.excalidraw</span>'
            f'<span><a href="{esc(url(mode="scene", **params))}" download="{esc(family)}-{view}.excalidraw">Download Excalidraw</a> · '
            f'<a href="{esc(canvas)}" target="_blank" rel="noopener">Open full screen ↗</a></span></div>'
            f'<iframe title="{esc(DRAW_NAMES[view])}" referrerpolicy="no-referrer" data-src="{esc(canvas)}"></iframe>'
            f'<noscript><img src="{esc(vector)}" alt="{esc(DRAW_NAMES[view])}"></noscript>'
            '</div></details>')


def guide_html(family, view, context, embedded=False):
    profile = family_profile(family, context)
    css = (HERE / "assets/guide.css").read_text(encoding="utf-8")
    js = (HERE / "assets/guide.js").read_text(encoding="utf-8")
    tabs = "".join(f'<a href="{esc(url(family=family, view=key, embed=int(embedded), **context))}" '
                   f'aria-current="{("page" if key == view else "false")}">{label}</a>' for key, label, _ in VIEWS)
    source_links = "".join(f'<li><a href="{esc(url(mode="source", family=family, source=i))}" '
                          f'target="_blank" rel="noopener">{esc(Path(item["path"]).parent.name)}</a>'
                          f'<span>{esc(item["role"])}</span></li>' for i, item in enumerate(profile["skills"]))
    if view == "roadmap-draw":
        content = "".join(drawing_row(family, key, context, key == "methods") for key in DRAW_NAMES)
    else:
        content = drawing_row(family, view, context, True)
        if view == "skill-set":
            content += '<ul class="wg-sources">' + source_links + '</ul>'
        elif view == "methods":
            content += "".join(f'<section class="wg-explanation"><h2>{esc(title)}</h2><p>{esc(body)}</p></section>'
                               for title, body in profile["method"])
        elif view == "workbench":
            content += "".join(f'<section class="wg-explanation"><h2>{esc(name)} Space</h2><p>{esc(body)}</p></section>'
                               for name, body in profile["spaces"])
        elif view == "folder-map":
            content += '<section class="wg-explanation"><h2>View → owner → folder / file</h2><p>Follow reads to the native owner, then stored at to the source. Paths below resolve inside the current instance.</p></section>'
            content += (f'<p class="wg-path"><a href="{esc(url(mode="source", family=family, source=len(profile["skills"]) + 1, **context))}" '
                        'target="_blank" rel="noopener">Guide · shared family definitions ↗</a></p>'
                        f'<p class="wg-path"><a href="{esc(url(mode="source", family=family, source=len(profile["skills"]), **context))}" '
                        f'target="_blank" rel="noopener">Working UI · <code>{esc(profile["presenter"])}</code> ↗</a></p>')
            content += "".join(f'<p class="wg-path"><a href="{esc(url(mode="folder", family=family, row=i, **context))}" '
                               f'target="_blank" rel="noopener">{esc(surface)} · <code>{esc(pattern)}</code> ↗</a></p>'
                               for i, (surface, _, pattern, _) in enumerate(profile["folders"]))
        content += f'<section class="wg-explanation"><p>{esc(profile["boundary"])}</p></section>'
    heading = '' if embedded else f'<header><h1>{esc(profile["label"])} Workbench</h1><p>Guide</p></header>'
    boot = dict(family=family, view=view, context=context)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(profile["label"])} · Guide</title><style>{css}</style></head><body>'
            f'{heading}<nav class="wg-views" aria-label="Guide Views">{tabs}</nav><main>'
            f'<h1>{dict((key, label) for key, label, _ in VIEWS)[view]}</h1>{content}</main>'
            f'<script type="application/json" id="wg-boot">{script_json(boot)}</script><script>{js}</script></body></html>')


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
        family, mode = get("family"), get("mode")
        only = getattr(self, "only", None)
        if family not in FAMILIES or (only and family not in only):
            return self.guide_send("Guide family is not served by this host.", 404, head_only=head_only)
        try:
            contract_path(family, 0)  # optional plugins must actually be present
            if mode == "source":
                path = contract_path(family, int(get("source", "0")), {"file": get("file")})
                body = f'<!doctype html><meta charset="utf-8"><title>{esc(path.name)}</title><h1>{esc(path.relative_to(REPOSITORY))}</h1><pre style="white-space:pre-wrap;overflow-wrap:anywhere">{esc(path.read_text(encoding="utf-8"))}</pre>'
                return self.guide_send(body, head_only=head_only)
            context = {"path": get("path"), "file": get("file")}
            if family == "labeling" and not context["path"] and only == {"labeling"}:
                source, error = self._labeling_page_target(context["file"])
                result = (source, error)
            else:
                result = self.target(context)
            if result[0] is None:
                return self.guide_send(esc(result[1]), 404, head_only=head_only)
            source = Path(result[0])
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
            view = get("view", "skill-set")
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
            return self.guide_send(guide_html(family, view, context, get("embed") == "1"), head_only=head_only)
        except (ValueError, OSError, RuntimeError) as error:
            return self.guide_send(esc(error), 404, head_only=head_only)
