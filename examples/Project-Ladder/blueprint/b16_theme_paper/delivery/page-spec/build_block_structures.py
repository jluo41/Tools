"""Build Paper-family Block Structure instances using the shared Studio tools.

Author types.md and the three structure outlines. Structure uses b17's folder
tree and S71's common level colours; the outline parser is only a data reader.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
BLOCK = ROOT / 'examples/Project-Ladder/blueprint/b16_theme_paper'
SHARED = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
MAPS = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-mindmap/scripts'
TOPICS = ('s01-idea-block-structure', 's02-grant-block-structure', 's03-paper-block-structure')
sys.path[:0] = [str(SHARED), str(MAPS), str(ROOT / 'plugins/haipipe-toolkit/servers/_host')]
import block_types_pages as type_pages
import mmtree


def map_text(title, lines):
    return f'---\nmindmap: 1\ntitle: {title}\n---\n\n# {title} <!-- root -->\n\n' + '\n'.join(lines) + '\n'


def source_link(path):
    rel = path.relative_to(ROOT).as_posix()
    return '/_board/page?path=' + quote(rel, safe='')


def block_link(path):
    """Select a Job/Task in its real Block using the existing Jobs navigation."""
    block = next((p for p in (path, *path.parents) if (p / 'board.md').is_file()), None)
    if block is None or not block.is_relative_to(ROOT):
        raise ValueError(f'No owning Block: {path}')
    parts = path.relative_to(block).parts
    query = {'path': block.relative_to(ROOT).as_posix(), 'layout': 'focus'}
    if parts:
        query.update(section='jobs', group=parts[0][:3])
        if len(parts) > 1:
            query['task'] = parts[1][:3]
    return '/_board/workbench?' + urlencode(query)


def type_outputs(topic):
    """Reuse shared pages, adapting only their destination to the Block route."""
    outputs = type_pages.build(topic)

    def destination(match):
        url = html.unescape(match.group(1))
        query = parse_qs(urlparse(url).query)
        path = ROOT / query['path'][0]
        return 'href="' + html.escape(block_link(path), quote=True) + '"'

    for target, text in list(outputs.items()):
        if target.suffix == '.html':
            outputs[target] = re.sub(r'href="(/_board/workbench\?[^"]+)"', destination, text)
    return outputs


def example_maps(topic):
    example, _ = type_pages.read_types(topic / 'types.md')
    if not example:
        return {}
    block = ROOT / example
    if not (block / 'board.md').is_file():
        raise ValueError(f'Example is not a real Block: {example}')
    folder, jobs, studio = [], [], []
    counter = 0

    def line(out, depth, label, note=''):
        nonlocal counter
        counter += 1
        out.append('  ' * depth + f'- {label} <!-- example{counter} -->')
        if note:
            out.append('  ' * (depth + 1) + note)

    def walk(path, depth=0):
        for child in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
            if child.name.startswith('.') or child.name in ('__pycache__', 'node_modules'):
                continue
            if child.is_symlink():
                continue
            line(folder, depth, child.name + ('/' if child.is_dir() else ''), str(child.relative_to(block)))
            if child.is_dir():
                walk(child, depth + 1)

    walk(block)
    for job in sorted(block.glob('j[0-9]*_*/')):
        face = job / (job.name + '.md')
        kind = type_pages.field(face, 'job-type')
        line(jobs, 0, job.name, f'[Source]({source_link(face)})' + (f' · {kind}' if kind else ''))
        for task in sorted(job.glob('t[0-9]*_*/')):
            face = task / (task.name + '.md')
            kind = type_pages.field(face, 'task-type')
            line(jobs, 1, task.name, f'[Source]({source_link(face)})' + (f' · {kind}' if kind else ''))
    from host_paths import bootstrap
    bootstrap()
    from live import frame, studio_tabs
    from live.frame_groups import studio_group_order
    band_names, bands = studio_tabs.studio_bands(block, ROOT), {}
    order = studio_group_order(block)
    for item in sorted(block.glob('s[0-9][0-9]-*/')):
        face = item / (item.name + '.md')
        facts = frame._note_facts(face) if face.is_file() else {}
        tags = facts.get('tags') or []
        tags = [tags] if isinstance(tags, str) else tags
        band = band_names.get(item.name[1]) or next((b for b in order if b in tags), None) or next(iter(tags), 'Other')
        bands.setdefault(band, []).append((item, face))
    for band in dict.fromkeys([*(b for b in order if b in bands), *bands]):
        line(studio, 0, band)
        for item, face in bands[band]:
            line(studio, 1, item.name, f'[Source]({source_link(face)})')
    return {topic / 'structure' / f'example-{key}.mindmap.md': map_text(block.name + ' · ' + title, rows)
            for key, title, rows in [('folder', 'Folder', folder), ('jobs', 'Job-Task', jobs), ('studio', 'Studio', studio)]}


def canvas_elements(topic):
    """One canvas, three tree frames, every source node and relationship retained."""
    import quick_draw as q
    out, offset = [], 0
    for key, title, colour in [('folder', 'Folder', '#547b9d'),
                               ('jobs', 'Job-Task', '#277d67'),
                               ('studio', 'Studio', '#7651a5')]:
        tree = mmtree.load(topic / 'structure' / f'{key}.mindmap.md')
        rows = list(mmtree.walk(tree.root))
        widths = {}
        for node, _, depth, _ in rows:
            widths[depth] = max(widths.get(depth, 0), len(node.text) * 22 * q.WIDE + 50)
        xs, cursor = {}, offset + 40
        for depth in sorted(widths):
            xs[depth], cursor = cursor, cursor + widths[depth] + 80
        ys, leaf = {}, [125]

        def place(node):
            if node.children:
                ys[node.id] = sum(place(c) for c in node.children) / len(node.children)
            else:
                ys[node.id], leaf[0] = leaf[0], leaf[0] + 70
            return ys[node.id]

        place(tree.root)
        frame = q._el('frame', key + '-frame', offset, 0, cursor - offset, leaf[0] + 20,
                      stroke='#aabfce', fill='#ffffff', name=title)
        out.append(frame)

        def add(items):
            for item in items:
                item.update(frameId=frame['id'], roughness=0)
            out.extend(items)

        add(q.text(key + '-title', offset + 40, 35, title, 34, colour))
        for node, parent, depth, _ in rows:
            x, y = xs[depth], ys[node.id]
            label = q.text(key + '-' + node.id, x, y - 14, node.text, 22, colour)
            label[0]['customData'] = {'map': key, 'node': node.id, 'parent': parent.id if parent else None}
            add(label)
            if parent:
                start = xs[depth - 1] + len(parent.text) * 22 * q.WIDE + 12
                add(q.line(key + '-' + node.id + '-edge',
                           [(start, ys[parent.id]), (x - 38, ys[parent.id]), (x - 38, y), (x - 12, y)], colour))
        offset = cursor + 100
    return out


def structure_document(topic):
    """Bind the existing folder-tree renderer to the three authored outlines."""
    source = ROOT / 'examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py'
    spec = importlib.util.spec_from_file_location('work_folder_tree', source)
    shared = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shared)
    sections = []
    roles = ('', 'Job group', 'Job name', 'Task group', 'Task name')
    levels = ('', 'job-group', 'job-name', 'task-group', 'task-name')
    for key in ('folder', 'jobs', 'studio'):
        model = mmtree.load(topic / 'structure' / f'{key}.mindmap.md')
        rows = list(mmtree.walk(model.root))

        def tree(node):
            return shared.node(node.text, *(tree(c) for c in node.children))

        rendered = shared.tree_html(tree(model.root), folder=key == 'folder', roles=roles if key == 'jobs' else ())
        row_iter = iter(rows)

        def annotate(match):
            node, parent, depth, _ = next(row_iter)
            level = levels[depth] if key == 'jobs' else ''
            detail = mmtree.display(' '.join(node.note))
            if not detail:
                detail = ('Contains ' + ', '.join(c.text for c in node.children)) if node.children else node.text
            attrs = {'title': detail, 'data-node': node.id, 'data-parent': parent.id if parent else '', 'data-level': level}
            tag = 'summary' if match.group(0) == '<summary>' else 'span'
            classes = 'lvl' if tag == 'summary' else 'leaf lvl'
            return '<' + tag + ' class="' + classes + '" ' + ' '.join(
                name + '="' + html.escape(value, quote=True) + '"' for name, value in attrs.items()) + '>'

        rendered = re.sub(r'<summary>|<span class="leaf">', annotate, rendered)
        parents = iter((n, d) for n, _, d, _ in rows if n.children)

        def opened(_):
            node, depth = next(parents)
            keep = depth == 0 or (depth == 1 and (key == 'jobs' or (key == 'folder' and node.id == 'jobs')))
            return '<details open>' if keep else '<details>'

        rendered = re.sub(r'<details open>', opened, rendered)
        sections.append(f'<section id="{key}-rules" hidden><div class="drawing"><ul class="tree rule"><li>'
                        + rendered + '</li></ul></div></section>')
    # S71 names this stylesheet as the source of the shared level palette.
    css = '/examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css'
    script = ("function pick(){const id=location.hash.slice(1)||'folder-rules';"
              "document.querySelectorAll('main>section').forEach(s=>s.hidden=s.id!==id);}"
              "addEventListener('hashchange',pick);pick();")
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Block Structure</title><style>' + shared.STYLE + '</style>'
            f'<link rel="stylesheet" href="{css}"></head><body><main class="content">'
            + ''.join(sections) + '</main><script>' + script + '</script></body></html>\n')


def build(topic, draw=True, structure_only=False):
    if not structure_only:
        for target, text in example_maps(topic).items():
            target.write_text(text, encoding='utf-8')
        for target, text in type_outputs(topic).items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding='utf-8')
    (topic / 'structure/jobs.html').write_text(structure_document(topic), encoding='utf-8')
    if draw:
        import canvas
        import render_png
        drawing = topic / 'structure/type.excalidraw'
        canvas.write(drawing, canvas_elements(topic), source='hai-studio: Block Structure', palette=False)
        render_png.render(drawing, topic / 'structure/type.png', s=0.5)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--no-draw', action='store_true')
    ap.add_argument('--structure-only', action='store_true')
    args = ap.parse_args()
    for name in TOPICS:
        build(BLOCK / name, not args.no_draw and not args.structure_only, args.structure_only)
        print(name)


if __name__ == '__main__':
    main()
