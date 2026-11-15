"""Static checks only. This does not claim browser or assistive-technology QA."""
import ast
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import tempfile

from build import HERE, ROOT, contrast
from findings import FINDINGS, PARTS


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hashes, self.articles, self.resources = [], [], [], []

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'article':
            self.articles.append(attrs)
        if attrs.get('href', '').startswith('#'):
            self.hashes.append(attrs['href'][1:])
        for key in ('src', 'srcset'):
            if key in attrs:
                self.resources.append(attrs[key])
        if tag == 'link':
            self.resources.append(attrs.get('href', ''))


def main():
    page = (HERE / 'index.html').read_text()
    parsed = Page()
    parsed.feed(page)
    assert len(parsed.ids) == len(set(parsed.ids)), 'Duplicate HTML ids'
    assert set(parsed.hashes) <= set(parsed.ids), 'Broken internal anchors'
    assert {x['id'] for x in parsed.articles} == {f['id'] for f in FINDINGS}
    assert all(r.startswith('data:') for r in parsed.resources), 'External asset'
    assert 'connect-src \'none\'' in page
    assert 'fetch(' not in page and 'XMLHttpRequest' not in page
    receipt = json.loads((HERE / 'source-receipt.json').read_text())
    for name, digest in receipt['sources'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, f'Source changed: {name}'
    for f in FINDINGS:
        for path, start, end in f['evidence']:
            lines = (ROOT / path).read_text().splitlines()
            snippet = '\n'.join(f'{n}: {lines[n - 1]}' for n in range(start, end + 1))
            assert escape(snippet) in page, (path, start, end)
    for file in HERE.iterdir():
        if file.is_file() and file.suffix in ('.py', '.html', '.md'):
            assert len(file.read_text().splitlines()) < 700, file.name
    scripts = re.findall(r'<script>(.*?)</script>', page, re.S)
    assert len(scripts) == 1
    with tempfile.TemporaryDirectory(prefix='space-ui-review-') as tmp:
        script = Path(tmp) / 'review.js'
        script.write_text(scripts[0])
        subprocess.run(['node', '--check', str(script)], check=True)
    # Execute only the reviewed pure section helpers, not the application host.
    tree = ast.parse((ROOT / PARTS).read_text())
    names = {'_section', 'word_span', 'waits_on_you'}
    constants = {'WAITS_WORDS', 'DONE_WORDS'}
    nodes = [n for n in tree.body if
             (isinstance(n, ast.FunctionDef) and n.name in names) or
             (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in n.targets))]
    scope = {'esc': escape, 're': re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(ROOT / PARTS), 'exec'), scope)
    empty = scope['_section']('结果', '', 'nothing yet')
    placeholder = scope['_section']('结果', '<p class=mut>Nothing here yet.</p>', 'nothing yet')
    assert empty == '' and '<section' in placeholder and 'Nothing here yet.' in placeholder
    assert 'nothing yet' not in scope['word_span']('nothing yet')
    assert contrast('#e8e8e6', '#eef3fb') < 4.5
    assert contrast('#e8e8e6', '#253749') >= 4.5
    assert contrast('#a0a09c', '#253749') >= 4.5
    print('PASS: source hashes/excerpts, HTML ids/anchors, offline assets, file lengths, JS syntax, section-helper reproduction, specified-color contrast.')
    print('NOT RUN: browser layout, filtering interactions, touch devices, screen reader, production integration.')


if __name__ == '__main__':
    main()
