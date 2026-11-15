"""★ AI-eval: how readable each section of a page is for a person, marked on the section's bar.

JL 261114: "everytime you updated a section content, you evaluate it, AI-eval, and mark how readable it is for the
human to read them"; "for each view's section ... we need to have the icon of star, to show the AI comments and eval".

A page's evals live beside its face, `<page folder>/ai-eval/readability.json`:

    {"Overview": {"🗺️ The map": {"score": 7, "hash": "3f2a…", "comments": ["…"], "by": "…", "at": "261114 23:10"}}}

keyed by the view's button name and the section's title (its number left out: numbers move). `hash` is the section's
text when it was read, so an eval of text that has changed since shows `★ 7?`; a section never read shows `☆`.
Opened, the section starts with the eval's comments. Viewing writes nothing.

The eval itself is a fresh reader's (never the one who wrote the section):

    python section_eval.py packet <page folder> --root <SPACE> --base http://127.0.0.1:<port>   # every section's text
    python section_eval.py check  <page folder> --root <SPACE> --base http://127.0.0.1:<port>   # ★ / ★? / ☆ per section
"""
import hashlib
import html as H
import json
import re
import sys
from pathlib import Path

STORE = Path('ai-eval') / 'readability.json'
_CARD = re.compile(r'<div class=ai-eval>.*?<!--/ai-eval--></div>', re.S)
CSS = ('<style>.ai-star{margin-left:10px;font-size:13px;font-weight:600;color:light-dark(#9a7400,#e8c35a);'
       'white-space:nowrap}.ai-star.old{opacity:.55}.ai-star.none{color:var(--muted);font-weight:400}'
       '.ai-eval{border-radius:10px;padding:10px 14px;margin:0 0 12px;background:light-dark(#fff8e1,#2e2a1a)}'
       '.ai-eval b{color:light-dark(#9a7400,#e8c35a)}.ai-eval ul{margin:4px 0 0;padding-left:18px}'
       '.ai-eval li{margin:2px 0}.ai-eval small{color:var(--muted)}</style>')


def _store(folder: Path) -> dict:
    path = folder / STORE
    try:
        return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}
    except (OSError, ValueError):
        return {}


def view_name(page: str) -> str:
    nav = re.search(r'<nav class="section-views".*?</nav>', page, re.S)
    m = re.search(r'aria-current="page"[^>]*>([^<]+)</a>', nav.group(0)) if nav else None
    return H.unescape(m.group(1)).strip() if m else ''


def text_of(body: str) -> str:
    body = _CARD.sub('', body)
    body = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', body)
    body = re.sub(r'(?is)<title>(.*?)</title>', r' \1 ', body)        # a drawing's hover words are its text
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', body))).strip()


def digest(body: str) -> str:
    return hashlib.sha1(text_of(body).encode('utf-8')).hexdigest()[:12]


def sections(page: str):
    """[(start, end, title, summary_end, body_start)] of each numbered top-level `details.band-sec`."""
    out, i = [], 0
    while (i := page.find('<details class=band-sec', i)) != -1:
        depth, j = 0, i
        for m in re.finditer(r'<details\b|</details>', page[i:]):
            depth += 1 if m.group(0) == '<details' else -1
            if depth == 0:
                j = i + m.end()
                break
        head = re.search(r'<span class=bt>(.*?)</span>', page[i:j], re.S)
        title = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', head.group(1)))).strip() if head else ''
        num = re.match(r'^\d+ · (.+)$', title)
        s_end, b_start = page.find('</summary>', i), page.find('<div class=band-jobs>', i)
        if num and -1 < s_end < j and -1 < b_start < j:
            out.append((i, j, num.group(1), s_end, b_start + len('<div class=band-jobs>')))
        i = j if j > i else i + 1
    return out


def mark(page: str, folder: Path) -> str:
    """The page with each numbered section's ★ on its bar and, opened, its comments first."""
    found = sections(page)
    if not found:
        return page
    evals = _store(folder).get(view_name(page), {})
    for start, end, title, s_end, b_start in reversed(found):
        e = evals.get(title)
        if not e:
            star, card = '<span class="ai-star none" title="AI readability: not read yet">☆</span>', ''
        else:
            score = e.get('score', '')
            fresh = e.get('hash') == digest(page[b_start:end])
            star = (f'<span class="ai-star{"" if fresh else " old"}" title="AI readability {score}/10'
                    f'{"" if fresh else ", read before this section last changed"}">★ {score}{"" if fresh else "?"}</span>')
            items = ''.join(f'<li>{H.escape(str(c))}</li>' for c in e.get('comments') or [])
            card = (f'<div class=ai-eval><b>★ {score}/10</b> AI readability{"" if fresh else " (text changed since)"}'
                    f'<ul>{items}</ul><small>{H.escape(str(e.get("by", "")))} · {H.escape(str(e.get("at", "")))}</small>'
                    '<!--/ai-eval--></div>')
        page = page[:b_start] + card + page[b_start:]
        page = page[:s_end] + star + page[s_end:]
    return page.replace('</head>', CSS + '</head>', 1) if '</head>' in page else CSS + page


# ── the command line: the text a fresh reader scores, and where each section stands ─────────────────────────────
VIEWS = ('overview', 'standing', 'findings', 'delivery')


def _pages(folder: Path, root: Path, base: str):
    from urllib.parse import quote
    from urllib.request import urlopen
    rel = folder.resolve().relative_to(root.resolve()).as_posix()
    for v in VIEWS:
        url = f'{base}/_board/workbench?layout=focus&group={v}&path={quote(rel, safe="")}'
        page = urlopen(url, timeout=120).read().decode('utf-8', 'replace')
        yield view_name(page), page


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('cmd', choices=('packet', 'check'))
    ap.add_argument('folder', type=Path)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--base', default='http://127.0.0.1:5694')
    a = ap.parse_args(argv)
    evals, rows, packet = _store(a.folder), [], []
    for view, page in _pages(a.folder, a.root, a.base):
        for start, end, title, s_end, b_start in sections(page):
            h, e = digest(page[b_start:end]), evals.get(view, {}).get(title)
            mark_ = '☆' if not e else f"★ {e.get('score')}" + ('' if e.get('hash') == h else '?')
            rows.append(f'{mark_:6} {view} › {title}')
            packet.append({'view': view, 'title': title, 'hash': h, 'text': text_of(page[b_start:end])[:8000]})
    if a.cmd == 'check':
        print('\n'.join(rows))
        return 0
    out = a.folder / 'ai-eval' / 'packet.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=1), encoding='utf-8')
    print(out, len(packet), 'sections')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
