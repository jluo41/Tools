"""A file-backed, portable Page Folder, independent of Board membership.

The manifest selects a Page Face and optional imported content. Imported bytes
remain the content authority; HTML is generated, never edited in place.
"""
from dataclasses import dataclass
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import threading
import tomllib
from urllib.parse import quote, unquote, urlsplit, urlencode

ENGINE = Path(__file__).resolve().parents[1]
LOCK = threading.RLock()
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".html", ".htm", ".css", ".js",
                   ".json", ".yaml", ".yml", ".toml", ".py", ".ts", ".tsx",
                   ".jsx", ".svg", ".csv", ".tex", ".bib", ".sql", ".r"}
MAX_SOURCE_BYTES = 2 * 1024 * 1024
PRIVATE_LANES = {"studio", "workflow", "runs", "scripts", "src", "tests",
                 "results", "__pycache__", "node_modules", "server-state"}
PRIVATE_FILES = {"env.sh", "server.json", "server.toml", "server.yaml", "server.yml",
                 "credentials.json", "credentials.toml", "secrets.json",
                 "secrets.toml", "auth.json", "token.json", "tokens.json"}


@dataclass(frozen=True)
class PageContext:
    source: Path
    folder: Path
    content: Path | None
    title: str


class SourceConflictError(ValueError):
    """An on-disk edit invalidated the browser's loaded source hash."""


def confined(folder, relative):
    """Resolve a declared relative file, refusing hidden paths and symlinks."""
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or any(p in {"..", "."} or p.startswith(".") for p in rel.parts):
        raise ValueError("Expected a visible file inside the Page Folder")
    current = Path(folder)
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Page files cannot be symlinks")
    path = current.resolve()
    if not path.is_relative_to(Path(folder).resolve()):
        raise ValueError("File escapes the Page Folder")
    return path


def load_page(target):
    target = Path(target).expanduser().resolve()
    folder = target if target.is_dir() else target.parent
    manifest = folder / "page.toml"
    content = None
    if manifest.is_file():
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        if type(data.get("version")) is not int or data["version"] != 1:
            raise ValueError("Unsupported page.toml version (expected 1)")
        source = confined(folder, data.get("source", ""))
        if target.is_file() and target not in {source, manifest}:
            raise ValueError("Use the Page Folder or its declared Page Face")
        if data.get("content"):
            content = confined(folder, data["content"])
            if not content.is_file():
                raise ValueError("The declared imported content is missing")
        title = data.get("title")
        if title is not None and not isinstance(title, str):
            raise ValueError("Page title must be a string")
    else:
        source = folder / (folder.name + ".md") if target.is_dir() else target
        title = None
    if source.suffix.lower() != ".md" or not source.is_file():
        raise ValueError("No Page Face found; use init --file INPUT --dest FOLDER")
    raw = source.read_text(encoding="utf-8")
    if not re.search(r"^## (?:🚪 )?Opening\s*$", raw, re.M):
        raise ValueError("Input is not a Page Face; use init --file INPUT --dest FOLDER")
    title = next((x.lstrip("# ") for x in raw.splitlines() if x.startswith("# ")), None) or title or source.stem
    if content is not None:
        declared = re.search(r"^source-content:\s*(.+)$", raw, re.M)
        if not declared or confined(folder, declared[1].strip()) != content:
            raise ValueError("page.toml content and Page source-content must match")
    return PageContext(source, folder, content, title)


def render_confined(folder, relative):
    path = confined(folder, relative)
    parts = path.relative_to(Path(folder).resolve()).parts
    if parts[0].lower() in PRIVATE_LANES or any(p.lower() in PRIVATE_FILES for p in parts):
        raise ValueError("Private Page lane cannot be rendered or downloaded")
    return path


class _References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "href", "poster", "data"} and value:
                self.urls.append(value)
            elif key == "srcset" and value:
                self.urls.extend(part.strip().split()[0] for part in value.split(",") if part.strip())


def references(path):
    """Static relative dependencies only; never execute code or fetch URLs."""
    if path.suffix.lower() not in {".md", ".markdown", ".html", ".htm", ".css", ".svg"}:
        return []
    text = path.read_text(encoding="utf-8")
    parser = _References()
    parser.feed(text)
    urls = parser.urls
    urls += re.findall(r"!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", text)
    urls += re.findall(r"url\(\s*['\"]?([^)'\"]+)", text)
    urls += re.findall(r"@import\s+['\"]([^'\"]+)", text)
    return urls


def dependency_files(source, root):
    """Bounded closure. Fail on missing/escaping local assets before creation."""
    pending, found = [source], set()
    while pending:
        file = pending.pop()
        if file in found:
            continue
        if len(found) >= 200:
            raise ValueError("Import exceeds 200 static files; select a narrower input")
        found.add(file)
        if sum(p.stat().st_size for p in found) > 50 * 1024 * 1024:
            raise ValueError("Import exceeds 50 MiB")
        for url in references(file):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if parsed.path.startswith("/"):
                raise ValueError(f"Root-relative asset is not portable: {url}")
            raw_asset = file.parent / unquote(parsed.path)
            if any(part.is_symlink() for part in (raw_asset, *raw_asset.parents)):
                raise ValueError(f"Symlink asset is not a portable import: {url}")
            asset = raw_asset.resolve()
            if not asset.is_relative_to(root) or not asset.is_file():
                raise ValueError(f"Missing or outside-input-directory asset: {url}")
            confined(root, asset.relative_to(root))
            pending.append(asset)
    return sorted(found)


def create_page(input_file, destination, title=None):
    original = Path(input_file).expanduser().resolve()
    destination = Path(destination).expanduser().absolute()
    if not original.is_file():
        raise ValueError("Input file does not exist")
    if any(c in original.name for c in "\n\r"):
        raise ValueError("Input filename must be one line")
    if destination.exists():
        raise ValueError("Destination already exists; refusing to overwrite a Page Folder")
    slug = destination.name
    if not re.fullmatch(r"[\w][\w.-]*", slug) or slug.startswith("."):
        raise ValueError("Choose a Page Folder name using letters, numbers, hyphens or underscores")
    files = dependency_files(original, original.parent)
    title = (title or original.stem.replace("_", " ").replace("-", " ")).strip()
    if not title or "\n" in title or "\r" in title:
        raise ValueError("Title must be one nonempty line")
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".page-create-", dir=destination.parent))
    try:
        materials = stage / "outline/evidence/materials"
        for file in files:
            target = materials / file.relative_to(original.parent)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
        content = (Path("outline/evidence/materials") / original.name).as_posix()
        source = slug + ".md"
        manifest = (f'version = 1\nsource = {json.dumps(source, ensure_ascii=False)}\n'
                    f'content = {json.dumps(content, ensure_ascii=False)}\ntitle = {json.dumps(title, ensure_ascii=False)}\n'
                    f'input_sha256 = "{sha256(original.read_bytes()).hexdigest()}"\n')
        (stage / "page.toml").write_text(manifest, encoding="utf-8")
        face = (f"# {title}\nstate: 🟡\nowner: unassigned\nsource-content: {content}\n\n"
                f"## Opening\n\nWorking Page for {original.name}. The imported copy is editable; the original file is unchanged.\n\n"
                "## Content\n\n### 1 · Source\n\n"
                "The attached source is rendered here directly. Edit its file in the Source workspace.\n\n"
                "## Aims\n\n### A1 · Source\n\n"
                "- ⬜ A1.1 · Review and refine the imported source.\n"
                "  **Done when:** the owner has reviewed the edited source and its rendered Page.\n"
                "  **Now:** imported draft; not yet reviewed.\n")
        (stage / source).write_text(face, encoding="utf-8")
        # rename cannot silently replace a populated destination.
        if destination.exists():
            raise ValueError("Destination appeared during creation; no files replaced")
        stage.rename(destination)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return load_page(destination)


def source_files(context):
    candidates = [context.source]
    for path in sorted(context.folder.rglob("*")):
        relative = path.relative_to(context.folder)
        if path == context.source or relative.parts[0] in {"delivery", "workflow", "runs", "results", "studio"}:
            continue
        try:
            render_confined(context.folder, relative)
        except ValueError:
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS and path.stat().st_size <= MAX_SOURCE_BYTES:
            candidates.append(path)
    return candidates


def read_source(context, relative):
    path = confined(context.folder, relative)
    if path not in source_files(context) or path.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("File is not an editable Page source")
    data = path.read_bytes()
    return {"path": path.relative_to(context.folder).as_posix(),
            "text": data.decode("utf-8"), "sha256": sha256(data).hexdigest()}


def save_source(context, relative, text, expected_sha256):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise ValueError("Source exceeds the 2 MiB editor limit")
    path = confined(context.folder, relative)
    # Match the shared Outline lock: a raw edit cannot race its own structured
    # operation. External editors are detected via content hashes.
    from live.outline_preview import page_lock
    with LOCK, page_lock(context.source):
        current = read_source(context, relative)
        if not expected_sha256 or current["sha256"] != expected_sha256:
            raise SourceConflictError("Source changed on disk; reload before saving")
        if path.name == "page.toml":
            raise ValueError("Edit Page registration on disk, not through the web editor")
        if path == context.source:
            if not re.search(r"^## (?:🚪 )?Opening\s*$", text, re.M):
                raise ValueError("Keep the Page Face's ## Opening section; edit the imported file for raw content")
            if context.content:
                declared = re.search(r"^source-content:\s*(.+)$", text, re.M)
                if not declared or render_confined(context.folder, declared[1].strip()) != context.content:
                    raise ValueError("Keep source-content bound to the registered imported file")
        fd, temporary = tempfile.mkstemp(prefix=".page-save-", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(text.encode("utf-8"))
            os.chmod(temporary, path.stat().st_mode)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return read_source(context, relative)


def render_page(context):
    # Revalidate registration on every request, including on-disk edits.
    current = load_page(context.source)
    if current.content != context.content:
        raise ValueError("Page registration changed; restart the Page server")
    context = current
    from . import body as grammar
    from .page_parse import parse_page
    from .page_question import render_question
    identifier = re.sub(r"[^A-Za-z0-9_-]", "-", context.source.stem)
    page = parse_page(identifier, context.source.read_text(encoding="utf-8"), file=context.source.name)
    page["standalone"] = True
    names = ("BASE", "PAGE_DIR", "RENDER_ROOT", "LINKS", "PAPER", "CARDS", "EMBEDS", "EMBED_SEEN", "FACE_IDS", "GROUP_IDS", "CHIP_N")
    with LOCK:
        old = {key: getattr(grammar, key, None) for key in names}
        try:
            grammar.BASE = context.folder
            grammar.PAGE_DIR = context.folder
            grammar.RENDER_ROOT = context.folder
            grammar.LINKS, grammar.PAPER = {}, None
            grammar.CARDS, grammar.EMBEDS = [], []
            grammar.EMBED_SEEN, grammar.FACE_IDS, grammar.GROUP_IDS = set(), set(), set()
            grammar.CHIP_N = 0
            content = render_question(page, None, None)
            if context.content:
                content = content.replace('<details class="sect content">', '<details class="sect content" open>')
            from .source_content import _SafeMarkup
            sanitizer = _SafeMarkup()
            sanitizer.feed(content)
            content = ''.join(sanitizer.parts)
        finally:
            for key, value in old.items():
                setattr(grammar, key, value)
    selected = context.content or context.source
    options = ''.join(f'<option value="{escape(p.relative_to(context.folder).as_posix())}"{" selected" if p == selected else ""}>{escape(p.relative_to(context.folder).as_posix())}</option>' for p in source_files(context) if p.name != "page.toml")
    query = urlencode({"path": "/", "file": context.source.name})
    plugin_config = json.dumps({
        "page": context.source.name,
        "default": "outline",
        "plugins": [
            {"id": "outline", "label": "🧭 Outline", "hint": "Context, Bullets, and Evidence",
             "order": 10, "url": f"/_board/outline?{query}&lens=div"},
            {"id": "runs", "label": "⚙️ Runs", "hint": "Local Run → Result pairs",
             "order": 30, "url": f"/_board/runs?{query}"},
            {"id": "delivery", "label": "📤 Delivery", "hint": "What leaves this Page",
             "order": 40, "url": f"/_board/delivery?{query}"},
            {"id": "folder", "label": "📂 Folder", "hint": "Files, lanes, and freshness",
             "order": 50, "url": f"/_board/folderstat?{query}"},
        ],
    }, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    from .page_assets import css as page_css
    css = page_css() + '\n' + (ENGINE / "assets/page.css").read_text(encoding="utf-8")
    css += (ENGINE / "assets/workspace.css").read_text(encoding="utf-8")
    js = (ENGINE / "assets/workspace.js").read_text(encoding="utf-8")
    js += (ENGINE / "assets/page.js").read_text(encoding="utf-8")
    js += (ENGINE / "assets/plugins.js").read_text(encoding="utf-8")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(context.title)} · Page</title><style>{css}</style></head>'
            '<body class="single split standalone" data-live="false"><header class="page-toolbar" id="top"><strong>haipipe / page</strong>'
            '<nav><a href="#reading">Page</a><a class="live-only" href="#source-editor">Source</a>'
            '<button class="live-only" id="page-plugin-button" type="button" aria-expanded="false" aria-controls="page-plugin-menu">🔌 Plugins</button>'
            '<div class="page-plugin-menu live-only" id="page-plugin-menu" role="menu" hidden></div></nav></header>'
            '<div class="page-stage"><div class="page-primary">'
            f'<main id="reading" class="wrap">{content}</main><section id="source-editor" class="live-only">'
            '<h2>Source workspace</h2><p>Save edits to the Page Folder. Generated HTML is not an edit target.</p>'
            f'<label for="source-file">File</label><select id="source-file">{options}</select>'
            '<button id="save-source" disabled>Save source</button><span id="editor-status"></span>'
            '<label for="source-text" class="sr-only">Source code</label><textarea id="source-text" spellcheck="false"></textarea></section>'
            '<footer class="page-footer">Page Folder · source-owned · Board optional</footer></div>'
            '<aside class="page-plugin-pane live-only" id="page-plugin-pane" aria-label="Page plugins" hidden>'
            '<div class="page-plugin-tabs" id="page-plugin-tabs" role="tablist"></div>'
            '<div class="page-plugin-frames" id="page-plugin-frames"></div></aside></div>'
            f'<script type="application/json" id="page-plugin-config">{plugin_config}</script>'
            f'<script>{js}</script></body></html>')


def build_page(context, output=None):
    """Portable static reading bundle, with no server or Board dependency."""
    output = Path(output).expanduser().absolute() if output else context.folder / "delivery/web"
    for part in (output, *output.parents):
        if part.is_symlink():
            raise ValueError("Build output cannot traverse a symlink")
    output = output.resolve()
    if output == context.folder or context.folder.is_relative_to(output):
        raise ValueError("Build output cannot overwrite the Page Folder or an ancestor")
    if (output / ".haipipe-page-export").is_symlink():
        raise ValueError("Build marker cannot be a symlink")
    if output.exists() and (not output.is_dir() or any(output.iterdir()) and not (output / ".haipipe-page-export").is_file()):
        raise ValueError("Output is not an existing Page export; refusing to overwrite unrelated files")
    markup = render_page(context)
    # HTML is a read-only publication. Live workspaces belong to serve, not
    # a static host; disable deep links emitted by the shared Outline table.
    markup = re.sub(r'href="/_board/[^" ]*"', 'href="#static-workspace"', markup)
    markup = re.sub(r'(?=<footer\b)', '<p id="static-workspace">Static reading export. Use the Page server for editing and Outline/Evidence workspaces.</p>', markup, count=1)
    files = dependency_files(context.content or context.source, context.folder)
    # The generated projection can add assets not named as raw Markdown links
    # (e.g. a Display preview). Include only visible files inside this Folder.
    rendered_refs = _References()
    rendered_refs.feed(markup)
    for url in rendered_refs.urls:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            continue
        path = render_confined(context.folder, unquote(parsed.path))
        if path.is_file() and path not in files:
            files.extend(p for p in dependency_files(path, context.folder) if p not in files)
    output.mkdir(parents=True, exist_ok=True)
    for path in files:
        render_confined(context.folder, path.relative_to(context.folder))
        target = confined(output, path.relative_to(context.folder))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    confined(output, "index.html").write_text(markup, encoding="utf-8")
    (output / ".haipipe-page-export").write_text("Generated Page reading bundle\n", encoding="utf-8")
    return output / "index.html"
