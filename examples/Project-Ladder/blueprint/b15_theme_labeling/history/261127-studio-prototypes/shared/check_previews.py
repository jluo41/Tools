"""Check proposal assets, scope, immutable bindings and Studio baseline registration."""
from pathlib import Path
import json
import re
from urllib.parse import parse_qs, urlsplit
from html import unescape

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[2]
ROOT = next(p for p in HERE.parents if (p / 'PRINCIPLE.md').is_file())
TOPICS = ('s11-itemization-job-preview', 's12-guideline-job-preview', 's14-scale-job-preview')


def check():
    count = 0
    kinds = set()
    for name in TOPICS:
        topic = BLOCK / name
        preview = topic / 'delivery/ui/job-preview.html'
        content = preview.read_text()
        data = json.loads(re.search(r'<script type="application/json" id="preview-data">(.*?)</script>', content, re.S)[1])
        kinds.add(data['kind'])
        for ref in re.findall(r'(?:src|href)="([^"]+)"', content):
            assert not urlsplit(ref).scheme, ref
            assert (preview.parent / ref).is_file(), ref
            count += 1
        page = (topic / (name + '.html')).read_text()
        refs = [unescape(x) for x in re.findall(r'data-src="([^"]+)"', page)]
        assert any(x.startswith('/_board/workbench?') for x in refs)
        assert len(refs) == len(set(refs))
        for ref in refs:
            if ref.startswith('/_board/workbench?'):
                path = parse_qs(urlsplit(ref).query)['path'][0]
                assert (ROOT / path).is_dir(), path
            else:
                assert (topic / ref).is_file(), ref
            count += 1
        assert len({j['id'] for j in data['jobs']}) == len(data['jobs'])
        for j in data['jobs']:
            assert len({t['id'] for t in j['tasks']}) == len(j['tasks'])
            assert j['inputs'] and j['tasks']
            for t in j['tasks']:
                assert t['group'] and t['state'] in {'done','waiting','ready','planned','blocked','running'}
                assert len({r[0] for r in t['runs']}) == len(t['runs'])
                count += 1
            if data['kind'] == 'scale':
                binding = dict(j['inputs'])
                assert all(binding.get(k) for k in ['Items','Guideline','Executor'])
                assert binding['Guideline'] == 'guideline-v2'
                if j['complete']:
                    assert j['signed'] and j['qualified'] and j['delivery']
                    assert all(t['state'] == 'done' for t in j['tasks'])
                if not j['qualified']:
                    assert not j['complete']
                    assert any(t['state'] == 'blocked' for t in j['tasks'])
                count += 1
        drawing=json.loads((topic / (name+'.excalidraw')).read_text())
        assert drawing['type']=='excalidraw' and len(drawing['elements'])>=30
        assert len({e['id'] for e in drawing['elements']})==len(drawing['elements'])
        assert (topic/(name+'.png')).stat().st_size>1000
        assert 'draw the idea here' not in (topic/(name+'.excalidraw')).read_text()
        for suffix in ['.md','.mindmap.md','.html']:
            assert len((topic/(name+suffix)).read_text().splitlines())<700
        count += 5
    assert kinds == {'items','guideline','scale'}
    js=(HERE/'preview.js').read_text()
    assert not re.search(r'\b(fetch|XMLHttpRequest|localStorage|sessionStorage)\b', re.sub(r'/\*.*?\*/','',js,flags=re.S))
    print(f'PASS: {len(TOPICS)} Studio proposals; {count} asset, identity and workflow checks')


if __name__ == '__main__':
    check()
