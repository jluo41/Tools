"""Source-backed files: the same tree and preview for a view and its whole page."""
from pathlib import Path
from os.path import commonpath
import builtins
import io
import keyword
import tokenize
from urllib.parse import quote, urlencode
from host_registry import static_path_allowed
from live import frame
from live.ui_parts import FOLDER_ICON, PB_CSS, PB_JS, _side_tabs

SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def roots_for(folder, root, view, topics, pages):
    from live import focus_page as f
    if not view:
        return [folder]
    paths = [t for t, _, _ in topics]
    if view.startswith('ui-'):
        kind = view.removeprefix('ui-')
        paths += [folder / 'ui' / (kind + '-views.md'), folder / 'walks' / (kind + '.html')]
        paths += [folder / 'ui' / 'structure.md']
    else:
        lanes = {'overview': ('requirements', 'context'), 'standing': ('runs', 'scripts', 'config'),
                 'findings': ('reports', 'results'), 'delivery': ()}.get(view, ())
        for page in pages:
            paths += [page / lane for lane in lanes]
            if view in ('overview', 'standing'):
                face = frame.face(page)
                if face:
                    paths.append(face)
        if view == 'delivery':
            paths += [p for p, _ in f.delivery_sources(folder, root)]
    return list(dict.fromkeys(p for p in paths if p.exists() and f.inside(p, root) and not p.is_symlink()))


def files_under(paths, root):
    from live import focus_page as f
    found = set()
    def visit(p):
        if p.is_symlink() or not f.inside(p, root) or p.name.startswith('.') or p.name in SKIP:
            return
        if p.is_file() and static_path_allowed(root, p):
            found.add(p)
        elif p.is_dir():
            for child in sorted(p.iterdir()):
                visit(child)
    for p in paths:
        visit(p)
    return sorted(found)


def allowed_folder(path, root):
    return path.is_dir() and not path.is_symlink() and static_path_allowed(root, path) and path.name not in SKIP


def folder_groups(folder, root, view=None, topics=(), pages=(), *, scope=None, skill_rows=None):
    """Five source types, all referencing existing directories within the served root."""
    from live import focus_page as f, skills_section
    from live import work_frame
    view = work_frame.view_key(view) if view else None
    if view and scope is None:
        scope = work_frame.shared_scope(folder, root, view, topics, f.interactions(folder, root), [])
    theme = frame.theme_of(folder, root)
    if skill_rows is None:
        actual = scope or work_frame.shared_scope(folder, root, None, topics, f.interactions(folder, root), [])
        skill_rows = work_frame.scope_skills(folder, root, theme, f.page_level(folder), view, actual)
    catalog = skills_section.catalog()
    skills = [catalog[name][2].parent for name, _ in skill_rows]
    if view:
        pages = scope['pages']
        blocks = [p for page in pages if (p := frame.face(page))]
        blocks += [t for t, _, _ in scope['topics']] + scope['runs']
        if view == 'delivery':
            blocks += [p for p, _ in f.delivery_sources(folder, root)]
        ui = view_code(view) + scope.get('ui_sources', [])
        if view.startswith('ui-'):
            ui += [folder / 'ui' / (view.removeprefix('ui-') + '-views.md'),
                   folder / 'walks' / (view.removeprefix('ui-') + '.html')]
        workspace, code = [], []
    else:
        pages = list(pages) or [folder]
        blocks = [folder] + [topic for topic, _, _ in topics]
        workspace, code = [root / '_WorkSpace'], [root / 'code']
        ui = [Path(__file__).resolve().parent, Path(__file__).resolve().parent.parent / ('workbench-' + theme)]
        ui += [page / 'ui' for page in pages]
    groups = [('🗂️ Workspace', workspace), ('🧩 Blocks', blocks), ('💻 Code', code),
              ('🧰 Tools · Skills', skills), ('🖥️ Tools · UI', ui)]
    return [(name, list(dict.fromkeys(p for p in paths if allowed_source(p, root)))) for name, paths in groups]


# The code that draws a view, its own first: the related code follows the view as its Blocks and Skills do (JL 261108:
# "they should update the related content"), not the same three files on every view.
VIEW_CODE = {
    'overview': (),                                              # Goal, Requirements, MindMap: work_frame and focus_page
    'standing': (),                                              # Jobs, Tasks and Runs: focus_page
    'findings': ('task_questions', 'page_reader'),               # Questions and answers, a report read in place
    'delivery': (),
    'ui': ('matrix_help', 'use_case_examples'),                  # the Type x View table and its examples
}
PAGE_CODE = ('work_frame', 'focus_page', 'ui_parts', 'frame')   # every view: the Work frame, the page, shared parts
AROUND_CODE = ('studio_tabs', 'interaction_section', 'skills_section', 'work_files')   # 🧭 Around the Work, on every view


def view_code(view):
    """[Path] of the modules that draw this view, found by import so a moved file is still found."""
    import importlib
    key = 'ui' if view.startswith('ui-') else view
    out = []
    for name in VIEW_CODE.get(key, ()) + PAGE_CODE + AROUND_CODE:
        try:
            out.append(Path(importlib.import_module('live.' + name).__file__))
        except Exception:
            continue
    return list(dict.fromkeys(out))


def allowed_source(path, root):
    return (path.is_file() or path.is_dir()) and not path.is_symlink() and path.name not in SKIP and static_path_allowed(root, path)


def file_node(item, root):
    url = (frame._draw_url(item, root) if item.suffix.lower() == '.excalidraw' else
           frame._file_url(item, root) if item.suffix.lower() in ('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.html', '.htm', '.docx', '.pptx', '.eml') else
           frame.ROUTE + '?' + urlencode({'view': 'focus-file', 'path': frame.rel(item, root)}))
    return ('<li class="file-leaf"><a data-pop="' + frame.esc(item.name) + '" href="'
            + frame.esc(url) + '"><span aria-hidden="true">▤</span> ' + frame.esc(item.name) + '</a></li>')


def folder_url(path, root, fragment=False):
    params = {'view': 'focus-folder', 'path': frame.rel(path, root)}
    if fragment:
        params['fragment'] = '1'
    return frame.ROUTE + '?' + urlencode(params)


def folder_node(path, root, label=None, children=None):
    source = ('data-loaded="1"' if children is not None else
              'data-folder-src="' + frame.esc(folder_url(path, root, True)) + '"')
    return ('<li><details class="file-branch" ' + source
            + '><summary>' + FOLDER_ICON + '<span title="' + frame.esc(frame.rel(path, root)) + '">'
            + frame.esc(label or path.name) + '</span></summary><div class="folder-children">'
            + (children or '') + '</div></details></li>')


def grouped_tree(paths, root):
    """Merge selected source paths; ancestor branches never list unrelated directories."""
    paths = sorted(set(p for p in paths if allowed_source(p, root)))
    paths = [p for p in paths if not any(q != p and q in p.parents for q in paths)]
    if not paths:
        return ''
    base = Path(commonpath([p if p.is_dir() else p.parent for p in paths]))
    def branch(parent, selected, label=None):
        if parent in selected:
            return folder_node(parent, root, label) if parent.is_dir() else file_node(parent, root)
        groups = {}
        for path in selected:
            child = parent / path.relative_to(parent).parts[0]
            groups.setdefault(child, []).append(path)
        children = '<ul>' + ''.join(branch(p, group) for p, group in sorted(groups.items())) + '</ul>'
        return folder_node(parent, root, label, children)
    label = root.name + ('/' + base.relative_to(root).as_posix() if base != root else '') + '/'
    return branch(base, paths, label)


def tree_rows(folder, root):
    """Only one directory level, fetched on expansion; children retain their ancestors."""
    if not allowed_folder(folder, root):
        return ''
    rows = []
    for item in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold())):
        if item.is_symlink() or item.name in SKIP or not static_path_allowed(root, item):
            continue
        if item.is_dir():
            rows.append(folder_node(item, root))
        elif item.is_file():
            rows.append(file_node(item, root))
    return '<ul>' + ''.join(rows) + '</ul>' if rows else '<p class="mut">Empty folder.</p>'


def render(folder, root, view=None, topics=(), pages=(), *, scope=None, skill_rows=None):
    groups = [(name, paths) for name, paths in folder_groups(folder, root, view, topics, pages, scope=scope, skill_rows=skill_rows) if paths]
    if not groups:
        return '<p class="mut">No files linked to this view.</p>'
    panels = []
    for name, paths in groups:
        panels.append('<section class="folder-type-content file-tree" aria-label="' + frame.esc(name)
                      + '"><ul>' + grouped_tree(paths, root) + '</ul></section>')
    return PB_CSS + TYPE_STYLE + '<div class="folder-types">' + _side_tabs('folder-type-', [(n, '') for n, _ in groups], panels) + '</div>' + PB_JS + TYPE_SCRIPT


def browse(folder, root):
    """Compatibility for existing Open Folder URLs: the same tree and pop-out viewer."""
    if not allowed_folder(folder, root):
        return ''
    from live import focus_page as f
    return f.document(folder.name, TYPE_STYLE + '<main class="focus-page"><section class="file-tree"><ul>'
                      + folder_node(folder, root, root.name + '/' + frame.rel(folder, root) + '/')
                      + '</ul></section></main>' + TYPE_SCRIPT)


TYPE_STYLE = '''<style>
.folder-types>.pb-side{grid-template-columns:170px minmax(0,1fr)}
.folder-type-content{min-width:0}.file-tree ul{list-style:none;padding:0;margin:0}
.file-tree .folder-children>ul{margin-left:10px;padding-left:15px;border-left:1px solid var(--line)}
.file-tree li{padding:3px 0;min-width:0}.file-tree summary{display:flex;align-items:flex-start;gap:7px;cursor:pointer;padding:5px 0;list-style:none;font-size:13px}
.file-tree summary::-webkit-details-marker{display:none}.file-tree summary::before{content:"▸";flex:none;width:10px}
.file-tree details[open]>summary::before{content:"▾"}.file-tree summary>span{min-width:0;overflow-wrap:anywhere}
.file-tree .folder-icon{margin-top:2px}.file-leaf a{display:block;padding:5px 0 5px 17px;overflow-wrap:anywhere;text-decoration:none;color:var(--accent);font-size:13px}
.file-leaf a:hover{text-decoration:underline}.file-leaf a>span{color:var(--muted);margin-right:5px}.folder-children>.mut{font-size:13px;margin:4px 0 8px 28px}
@media(max-width:600px){.folder-types>.pb-side{grid-template-columns:1fr}.folder-types .pb-list{position:static;display:flex;flex-direction:row;flex-wrap:wrap}.file-tree summary,.file-leaf a{min-height:32px}}
</style>'''
TYPE_SCRIPT = '''<script>(function(){
async function load(branch){
 if(!branch.open||branch.dataset.loaded||branch.dataset.loading)return;
 branch.dataset.loading='1';var box=branch.querySelector(':scope>.folder-children');box.setAttribute('aria-busy','true');
 try{var response=await fetch(branch.dataset.folderSrc);if(!response.ok)throw Error('unavailable');
 box.innerHTML=await response.text();branch.dataset.loaded='1';}
 catch(e){box.textContent='Unable to open folder. Close and expand to retry.';}
 finally{delete branch.dataset.loading;box.removeAttribute('aria-busy');}
}
document.addEventListener('toggle',function(e){if(e.target.matches('.file-branch'))load(e.target);},true);
})();</script>'''


def python_preview(source):
    """Highlight tokens without importing or executing the inspected source."""
    offsets = [0]
    for line in io.StringIO(source):
        offsets.append(offsets[-1] + len(line))
    position = lambda point: min(len(source), offsets[min(point[0] - 1, len(offsets) - 1)] + point[1])
    parts, cursor, declaration = [], 0, False
    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            start, end = position(token.start), position(token.end)
            if end <= cursor:
                continue
            style = {tokenize.STRING: 'string', tokenize.COMMENT: 'comment',
                     tokenize.NUMBER: 'number', tokenize.OP: 'operator'}.get(token.type, '')
            if token.type == tokenize.NAME:
                style = ('keyword' if keyword.iskeyword(token.string) else 'function' if declaration
                         else 'builtin' if token.string in vars(builtins) else '')
                declaration = token.string in ('def', 'class')
            parts.append(frame.esc(source[cursor:start]))
            value = frame.esc(source[start:end])
            parts.append('<span class="py-' + style + '">' + value + '</span>' if style else value)
            cursor = end
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass  # Incomplete files and bounded previews still show every remaining character.
    parts.append(frame.esc(source[cursor:]))
    return '<pre class="python-code"><code>' + ''.join(parts) + '</code></pre>'


def preview(path, root):
    """Bounded, escaped text preview with the same access gate as raw downloads."""
    if not path.is_file() or not static_path_allowed(root, path):
        return ''
    raw_url = '/' + quote(frame.rel(path, root))
    actions = '<p class="preview-tools"><a href="' + frame.esc(frame._file_url(path, root)) + '" target="_blank" rel="noopener">Open ↗</a> · <a download href="' + frame.esc(raw_url) + '">Download</a></p>'
    if path.suffix.lower() not in ('.md', '.txt', '.py', '.json', '.yaml', '.yml', '.csv', '.tsv', '.log', '.js', '.ts', '.css', '.sh', '.toml', '.ini', '.cfg', '.xml', '.sql', '.r'):
        return '<!doctype html><meta charset="utf-8"><p>Preview unavailable.</p>' + actions
    with path.open('rb') as stream:
        raw = stream.read(200001)
    text = raw[:200000].decode('utf-8', errors='replace')
    if path.suffix.lower() != '.md':
        actions = actions.replace('</p>', ' <label><input id="wrap-lines" type="checkbox" checked> Line wrap</label></p>')
    from live import focus_page as f
    body = (f.markdown(text, path.parent, root) if path.suffix.lower() == '.md' else
            python_preview(text) if path.suffix.lower() == '.py' else '<pre>' + frame.esc(text) + '</pre>')
    if len(raw) > 200000:
        body += '<p>Preview truncated. Open or download the full file.</p>'
    return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font:15px/1.6 system-ui;padding:16px;color:#222;background:#fff}pre{white-space:pre-wrap;overflow-wrap:anywhere;overflow-x:auto}body:has(#wrap-lines:not(:checked)) pre{white-space:pre;overflow-wrap:normal}.preview-tools{position:sticky;top:0;background:#fff;padding:8px 0;margin-top:0;font-size:13px}.preview-tools label{display:inline-flex;align-items:center;gap:4px;margin-left:18px;cursor:pointer}img{max-width:100%}table{display:block;overflow:auto}.python-code{font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;tab-size:4}.py-keyword{color:#a626a4;font-weight:600}.py-string{color:#246b35}.py-comment{color:#657080;font-style:italic}.py-number{color:#986018}.py-function{color:#0969b8}.py-builtin{color:#8a4800}.py-operator{color:#50505e}</style>' + actions + body
