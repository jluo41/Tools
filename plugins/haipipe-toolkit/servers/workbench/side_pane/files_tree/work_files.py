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
from live.ui_parts import FOLDER_ICON
from live.file_icons import file_icon
from live.frame_base import chain
from live.page_spec import spec_dir

SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def roots_for(folder, root, view, topics, pages):
    from live import focus_page as f
    if not view:
        return [folder]
    paths = [t for t, _, _ in topics]
    if view.startswith('ui-'):
        kind = view.removeprefix('ui-')
        paths += [spec_dir(folder) / (kind + '-views.md'), folder / 'walks' / (kind + '.html')]
        paths += [spec_dir(folder) / 'structure.md']
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
        blocks += [t for t, _, _ in scope['topics']] + scope['runs'] + scope.get('source_paths', [])
        if view == 'delivery':
            blocks += [p for p, _ in f.delivery_sources(folder, root)]
        ui = view_code(view) + scope.get('ui_sources', [])
        if view.startswith('ui-'):
            ui += [spec_dir(folder) / (view.removeprefix('ui-') + '-views.md'),
                   folder / 'walks' / (view.removeprefix('ui-') + '.html')]
        workspace, code = [], []
    else:
        pages = list(pages) or [folder]
        blocks = [folder] + [topic for topic, _, _ in topics]
        workspace, code = [root / '_WorkSpace'], [root / 'code']
        ui = [Path(__file__).resolve().parents[2], Path(__file__).resolve().parents[3] / ('workbench-' + theme)]
        ui += [spec_dir(page) for page in pages]
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
    return ('<li class="file-leaf" data-path="' + frame.esc(frame.rel(item, root)) + '"><a data-pop="' + frame.esc(item.name) + '" href="'
            + frame.esc(url) + '"><span aria-hidden="true">' + file_icon(item) + '</span> ' + frame.esc(item.name) + '</a>'
            + '</li>')


def folder_url(path, root, fragment=False):
    params = {'view': 'focus-folder', 'path': frame.rel(path, root)}
    if fragment:
        params['fragment'] = '1'
    return frame.ROUTE + '?' + urlencode(params)


def folder_node(path, root, label=None, children=None, *, expanded=False):
    source = ('data-loaded="1"' if children is not None else
              'data-folder-src="' + frame.esc(folder_url(path, root, True)) + '"')
    rel = frame.esc(frame.rel(path, root))
    return ('<li><details class="file-branch" ' + source + ' data-folder-path="' + rel + '"'
            + (' open' if expanded else '') + '><summary>' + FOLDER_ICON + '<span title="' + rel + '">'
            + frame.esc(label or path.name) + '</span>'
            + '</summary><div class="folder-children">'
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


def source_branch(label, children):
    if not children:
        return ''
    return ('<li><details class="file-group"><summary>' + FOLDER_ICON + '<span>' + frame.esc(label)
            + '</span></summary><div class="folder-children"><ul>' + children + '</ul></div></details></li>')


def open_rows(folder, target, root):
    """One folder's rows, with the branch that leads to `target` (the page's own folder) already open."""
    if not allowed_folder(folder, root):
        return ''
    rows = []
    for item in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold())):
        if item.is_symlink() or item.name in SKIP or not static_path_allowed(root, item):
            continue
        if item.is_dir() and (item == target or item in target.parents):
            rows.append(folder_node(item, root, children=open_rows(item, target, root) if item != target
                                    else tree_rows(item, root), expanded=True))
        elif item.is_dir():
            rows.append(folder_node(item, root))
        elif item.is_file():
            rows.append(file_node(item, root))
    return '<ul>' + ''.join(rows) + '</ul>' if rows else '<p class="mut">Empty folder.</p>'


def shown_rel(path, root):
    """A path as the SPACE names it: the real one when it lies inside, else as written (a OneDrive folder is a link that
    leads outside the SPACE, and resolving it would name the cloud folder instead)."""
    try:
        return frame.rel(path, root)
    except ValueError:
        return path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name


def files_part(n, title, base, tree, root, cls=''):
    """One numbered part of the Files pane: its title, then where its folders sit, as a path from the SPACE root;
    a part with nothing in it is not drawn."""
    if not tree:
        return ''
    where = shown_rel(base, root) if base != root else ''
    return (f'<section class="files-part"><h3>{n} · {title}</h3>'
            f'<p class="files-where" title="{frame.esc(where)}/">{frame.esc(where + "/" if where else "./")}</p>'
            f'<ul class="{cls or "file-sources"}">{tree}</ul></section>')


def flat_tree(paths, root):
    """(base, rows): the selected folders and files under the folder they share, in their real nesting from there.
    A folder between the base and a selected one opens to show only the way down; a selected folder stays closed
    and loads its own rows when opened. One inside another is shown once, as the outer one."""
    paths = sorted(set(p for p in paths if allowed_source(p, root)))
    paths = [p for p in paths if not any(q != p and q in p.parents for q in paths)]
    if not paths:
        return root, ''
    base = Path(commonpath([p.parent for p in paths]))

    def rows(parent, selected):
        groups = {}
        for path in selected:
            groups.setdefault(parent / path.relative_to(parent).parts[0], []).append(path)
        out = []
        for child, below in sorted(groups.items(), key=lambda kv: kv[0].name.casefold()):
            if child in below:
                out.append(folder_node(child, root) if child.is_dir() else file_node(child, root))
            else:
                out.append(folder_node(child, root, children='<ul>' + rows(child, below) + '</ul>', expanded=True))
        return ''.join(out)
    return base, rows(base, paths)


SHARED_SKILLS = ('hai-trace', 'hai-stack')       # traces and rules, under skills/0_utils/
LEVEL_SKILLS = {'Block': 'haipipe-block', 'Job': 'haipipe-job', 'Task': 'haipipe-task', 'Topic': 'haipipe-studio'}


def own_skills(folder, root):
    """The skill folders that own this page, not every skill its sections touch (the side pane's Skills lists those):
    its level's skill, its theme's two, a Task's own task-type skill, and the shared ones every page works by."""
    from live import focus_page as f, skills_section
    from live.focus_themes import TYPE_SKILLS
    level, theme = f.page_level(folder), frame.theme_of(folder, root)
    names = [LEVEL_SKILLS.get(level, ''), 'haipipe-' + theme, 'workbench-' + theme, *SHARED_SKILLS]
    if level == 'Task':
        names.append(TYPE_SKILLS.get(frame.task_type(folder), ''))
    catalog = skills_section.catalog()
    return [catalog[n][2].parent for n in dict.fromkeys(names) if n in catalog]


def face_list(block, key):
    """The comma-separated values of one line of the Block's face (`waits-for: b01_irb, b11_azure_account`)."""
    from live.frame_base import _fields
    md = frame.face(block)
    if not md:
        return []
    return [v.strip() for k, line in _fields(md, (key,)) for v in line.split(',') if v.strip()]


def support_tree(block, root):
    """(base, rows): the Blocks this Block waits for (its face's `waits-for:` line), as closed folders beside it
    (JL 261125: "you can use b11 as the support ... as a new section below")."""
    kids = [block.parent / name for name in face_list(block, 'waits-for')]
    kids = [k for k in kids if allowed_folder(k, root) and k != block]
    return block.parent, ''.join(folder_node(k, root) for k in kids)


def project_of(block):
    """The Project folder a Block sits in: the nearest folder above it with a project.md, else two up (P/work/bNN)."""
    return next((p for p in block.parents if (p / 'project.md').is_file()), block.parent.parent)


def examples_tree(block, root):
    """(base, rows): the example Blocks this Block's design is drawn from (its face's `examples:` line, paths from the
    Project folder: `insight/Insight-Example`), as closed folders (JL 261126: "add 4. Block Examples")."""
    project = project_of(block)
    kids = [project / v for v in face_list(block, 'examples')]
    kids = [k for k in kids if k.is_dir() and allowed_folder(k, root) and k != block]
    if not kids:
        return project, ''
    base = Path(commonpath([str(k.parent) for k in kids]))
    homes = {}                                   # each example under its own theme folder (JL 261126: "the three
    for k in kids:                               # blocks are not happened in the same folder of work")
        homes.setdefault(k.parent, []).append(k)
    if list(homes) == [base]:
        return base, ''.join(folder_node(k, root) for k in kids)
    return base, ''.join(folder_node(home, root, label=frame.rel(home, base) if home != base else None,
                                     children=''.join(folder_node(k, root) for k in ks), expanded=True)
                         for home, ks in homes.items())


def drive_rows(folder, depth=0):
    """A shared-drive folder's rows by name only: its files are not served from this host (they live outside the
    SPACE), so nothing links; folders start closed, two levels down."""
    try:
        items = sorted((p for p in folder.iterdir() if not p.name.startswith(('.', '~$'))),
                       key=lambda p: (not p.is_dir(), p.name.casefold()))
    except OSError:
        return '<li class="mut">not found on this computer</li>'
    rows = []
    for item in items:
        if item.is_dir():
            inner = drive_rows(item, depth + 1) if depth < 1 else ''
            rows.append('<li><details class="file-branch"><summary>' + FOLDER_ICON + '<span>' + frame.esc(item.name)
                        + '</span></summary><div class="folder-children"><ul>'
                        + (inner or '<li class="mut">open it in OneDrive</li>') + '</ul></div></details></li>')
        else:
            rows.append('<li class="file-leaf"><span><span aria-hidden="true">' + file_icon(item) + '</span> '
                        + frame.esc(item.name) + '</span></li>')
    return ''.join(rows) or '<li class="mut">empty</li>'


def onedrive_tree(block, root):
    """(base, rows): the Block's shared OneDrive folders (its face's `onedrive:` line), listed by name, closed."""
    folders = [root / v for v in face_list(block, 'onedrive')]
    if not folders:
        return root, ''
    base = Path(commonpath([str(f.parent) for f in folders]))
    rows = ''.join('<li><details class="file-branch"><summary>' + FOLDER_ICON + '<span title="'
                   + frame.esc(shown_rel(f, root)) + '">' + frame.esc(f.name)
                   + '</span></summary><div class="folder-children"><ul>' + drive_rows(f) + '</ul></div></details></li>'
                   for f in folders)
    return base, rows


def render(folder, root, view=None, topics=(), pages=(), *, scope=None, skill_rows=None):
    """The Files pane in numbered parts, each holding real folders only: 1 · Block (the Block's folder, open down to
    this page's own), then the Blocks it waits for and its shared OneDrive folders (from the Block's face; JL 261125),
    Code (the server code and page spec that draw this page), Skills (the skills that own this page), and the
    Block Examples its design is drawn from (the face's `examples:` line).
    No grouping folders, no 🧵 marks, no Sessions."""
    folder, root = folder.resolve(), root.resolve()
    if not allowed_folder(folder, root):
        return ''
    block = chain(folder, root).get('Block') or folder
    block = block.resolve() if allowed_folder(block, root) else folder
    groups = dict(folder_groups(folder, root, view, topics, pages, scope=scope, skill_rows=skill_rows))
    rows = open_rows(block, folder, root) if block != folder else tree_rows(block, root)
    ui = [p for p in groups.get('🖥️ Tools · UI', []) if block not in p.parents and p != block]   # the Block part has them
    from live import trace_view
    mine = own_skills(folder, root)          # only what the page owns; any other folder a trace touched is Also touched
    examples = examples_tree(block, root)
    covered = [block, *ui, *mine, *(block.parent / n for n in face_list(block, 'waits-for')),
               *(project_of(block) / n for n in face_list(block, 'examples'))]
    ui, skills = flat_tree(ui, root), flat_tree(mine, root)
    support, drive = support_tree(block, root), onedrive_tree(block, root)
    parts, n = [], 0
    for title, base, tree, cls in (('Block', block.parent, folder_node(block, root, children=rows, expanded=True),
                                    'fixed-folder'),
                                   ('Support Blocks', *support, ''), ('OneDrive', *drive, ''),
                                   ('Code', *ui, ''), ('Skills', *skills, ''), ('Block Examples', *examples, '')):
        if tree:                                  # numbered in reading order; an empty part is not drawn
            n += 1
            if title in ('Code', 'Skills') and not any('files-ext' in p for p in parts):
                parts.append('<p class="files-ext" aria-hidden="true">extends into</p>')   # what the Block reaches out to
            parts.append(files_part(n, title, base, tree, root, cls))
    from live import file_info       # the traces in play mark their files on this one tree
    return (TYPE_STYLE + trace_view.render(folder, root, '<div class="file-tree">' + ''.join(parts) + '</div>', covered)
            + TYPE_SCRIPT + file_info.CARD)


def browse(folder, root):
    """Compatibility for existing Open Folder URLs: the same tree and pop-out viewer."""
    if not allowed_folder(folder, root):
        return ''
    from live import focus_page as f
    return f.document(folder.name, TYPE_STYLE + '<main class="focus-page"><section class="file-tree"><ul>'
                      + folder_node(folder, root, root.name + '/' + frame.rel(folder, root) + '/')
                      + '</ul></section></main>' + TYPE_SCRIPT)


TYPE_STYLE = '''<style>
.file-tree ul{list-style:none;padding:0;margin:0}
.file-tree .fixed-folder+.file-sources{border-top:1px solid var(--line);margin-top:8px;padding-top:5px}
.fixed-folder>li>details>summary,.file-group>summary{font-weight:600}
.files-part+.files-part{border-top:1px solid var(--line);margin-top:10px;padding-top:4px}.files-ext{display:flex;align-items:center;gap:8px;margin:16px 0 0;font-size:11px;color:var(--muted);letter-spacing:.06em}.files-ext::before,.files-ext::after{content:"";flex:1;border-top:1px dashed var(--line)}.files-ext+.files-part{border-top:0;margin-top:2px}.files-ext~.files-part>h3::before{content:"↳ "}.files-where{margin:0 0 4px;font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--muted);overflow-wrap:anywhere;user-select:all}.files-part>h3{margin:8px 0 2px;font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.file-tree .folder-children>ul{margin-left:10px;padding-left:15px;border-left:1px solid var(--line)}
.file-tree li{padding:0;margin:0;min-width:0}.file-tree summary{display:flex;align-items:flex-start;gap:7px;cursor:pointer;padding:1px 0;line-height:18px;list-style:none;font-size:13px}
.file-tree summary::-webkit-details-marker{display:none}.file-tree summary::before{content:"▸";flex:none;width:10px}
.file-tree details[open]>summary::before{content:"▾"}.file-tree summary>span{min-width:0;overflow-wrap:anywhere}
.file-tree .folder-icon{margin-top:1px}.file-leaf a{display:block;padding:1px 0 1px 17px;line-height:18px;overflow-wrap:anywhere;text-decoration:none;color:var(--accent);font-size:13px}
.file-leaf a:hover{text-decoration:underline}.file-leaf a>span{color:var(--muted);margin-right:5px}.folder-children>.mut{font-size:13px;margin:0 0 2px 28px}
@media(max-width:600px){.file-tree summary,.file-leaf a{min-height:32px}}
</style>'''
TYPE_SCRIPT = '''<script>(function(){
async function load(branch){
 if(!branch.open||branch.dataset.loaded||branch.dataset.loading)return;
 branch.dataset.loading='1';var box=branch.querySelector(':scope>.folder-children');box.setAttribute('aria-busy','true');
 try{var response=await fetch(branch.dataset.folderSrc);if(!response.ok)throw Error('unavailable');
 box.innerHTML=await response.text();branch.dataset.loaded='1';
 }
 catch(e){box.textContent='Unable to open folder. Close and expand to retry.';}
 finally{delete branch.dataset.loading;box.removeAttribute('aria-busy');}
}
// no folder is remembered: each page opens on the way down to itself, every other folder closed (JL 261126)
document.addEventListener('toggle',function(e){
 var branch=e.target;
 if(!branch.matches('.file-branch'))return;
 load(branch);
},true);
try{Object.keys(sessionStorage).forEach(function(k){if(k.indexOf('wb:folder:')===0)sessionStorage.removeItem(k);});}catch(e){}
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
