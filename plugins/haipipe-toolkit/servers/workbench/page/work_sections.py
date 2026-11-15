"""A page's own sections, written on its face, in place of the fixed work frame.

A Block (or Job, or Task) whose material does not fit Goal · Requirements · MindMap or Data · Values · Displays
names its own sections on its face (JL 261114: "If I give you the random things ... propose the new structure"):

    ## Review Content              the Overview's sections
    ### 🗓️ The week                one numbered section; its body is Markdown
    embed: src/review/week.md      a line that brings in a .md (rendered) or an .svg drawing (an .html never)

    ## Plan + Results              sections after its Jobs, the same way (a replay's days, a plan's steps)
    ## Findings                    the Findings view's sections, the same way
    each: src/review/area-*.md     one section per file, titled by the file's `# ` line

A face without these sections keeps the fixed frame. Viewing writes nothing.
"""
from pathlib import Path
import re

from live import frame

KEYS = {'overview': 'review content', 'standing': 'plan + results', 'findings': 'findings'}
_HEAD = re.compile(r'^###\s+(.+?)\s*#*\s*$')
_LINE = re.compile(r'^(embed|each):\s*(\S.*?)\s*$')


def _file(rel, folder, root):
    path = (folder / rel).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def _embed(path, folder, root):
    from live import focus_page as f
    # Markdown, or a drawing: page content maps to the page's own sections, never a framed website (JL 261114)
    if path is None or not path.is_file() or path.suffix not in ('.md', '.svg'):
        return ''
    if path.suffix == '.svg':                    # a picture (a map), inline so its stations' hover titles show
        svg = path.read_text(encoding='utf-8', errors='replace')
        svg = re.sub(r'(?is)<script.*?</script>|<foreignObject.*?</foreignObject>', '', svg)
        svg = re.sub(r'(?i)\son\w+\s*=\s*("[^"]*"|\'[^\']*\')', '', svg)    # no event handlers
        svg = re.sub(r'\A.*?(?=<svg)', '', svg, flags=re.S)
        return f'<div class=ws-pic style="overflow-x:auto;border:1px solid var(--line);border-radius:12px">{svg}</div>'
    return f.markdown(_titled(path)[1], path.parent, root)     # the section already carries the title


def _titled(path):
    """A file's `# ` line as its title, and the rest as its body."""
    text = path.read_text(encoding='utf-8', errors='replace')
    m = re.match(r'\A\s*#\s+(.+?)\s*\n', text)
    return (m.group(1), text[m.end():]) if m else (path.stem, text)


def declared(folder, root, data, view):
    """[(title, html)] for a view's own sections, or [] when the face names none."""
    from live import focus_page as f
    text = data['sections'].get(KEYS.get(view, ''), '')
    if not text:
        return []
    out, title, lines, fence = [], None, [], False

    def close():
        if title is not None:
            out.append((title, ''.join(lines_html(lines))))

    def lines_html(chunk):
        md, inside = [], False
        for line in chunk + ['']:
            if line.lstrip().startswith('```'):
                inside = not inside
            m = _LINE.match(line) if not inside else None
            if m and m.group(1) == 'embed':
                if md:
                    yield f.markdown('\n'.join(md), folder, root)
                    md = []
                yield _embed(_file(m.group(2), folder, root), folder, root)
            else:
                md.append(line)
        if any(l.strip() for l in md):
            yield f.markdown('\n'.join(md), folder, root)

    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            fence = not fence
        head = _HEAD.match(line) if not fence else None
        each = _LINE.match(line) if not fence else None
        if head:
            close()
            title, lines = head.group(1), []
        elif each and each.group(1) == 'each':
            close()
            title, lines = None, []
            for path in sorted(folder.glob(each.group(2))):
                if _file(str(path.relative_to(folder)), folder, root) and path.suffix == '.md':
                    name, body = _titled(path)
                    out.append((name, f.markdown(body, path.parent, root)))
        elif title is not None:
            lines.append(line)
    close()
    return out


# How an entry reads (the look of the replay page JL accepted, src/page.tpl.html in b41): a card per entry, its time in a
# column, chips on the right, the labelled lines as tinted blocks, phases as tonal milestones on one vertical line.
CHIPS = ('Session', 'Area')
TINTS = {'JL asked': 'ask', 'Asked': 'ask', 'Decided': 'dd', 'Built': 'done', 'Done': 'done'}
_LABEL = re.compile(r'^\s*([A-Z][A-Za-z ]{1,18}):\s*(.*)$', re.S)
_TIME = re.compile(r'^<b>((?:\d\d-\d\d )?\d\d:\d\d)</b>\s*·\s*(.*)$', re.S)
_PHASE = re.compile(r'^<b>([^·<]*\d\d:\d\d[^·<]*?)\s*·\s*([^<]*)</b>$', re.S)   # `**12:39 → 13:51 · title**`
CSS = ('<style>'
       '.ws-tl{list-style:none;margin:0 0 0 6px;padding:0 0 0 14px!important;border-left:2px solid var(--line)}'
       '.ws-tl>li{position:relative;margin:0 0 8px;padding-left:12px}'
       '.ws-tl>li::before{content:"";position:absolute;left:-21px;top:18px;width:10px;height:10px;border-radius:50%;'
       'background:var(--paper,#fff);border:2px solid var(--muted)}'
       '.ws-tl>li.ws-ph::before{width:12px;height:12px;left:-22px;top:16px;background:var(--accent);border-color:var(--accent)}'
       '.ws-card{border:1px solid var(--line);border-radius:12px;background:var(--paper,#fff);overflow:hidden}'
       '.ws-card[open]{box-shadow:0 1px 2px #0000001a,0 2px 8px #0000000f;border-color:transparent}'
       '.ws-card>summary{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;align-items:baseline;'
       'padding:10px 14px;cursor:pointer;list-style:none}.ws-card>summary::-webkit-details-marker{display:none}'
       '.ws-card>summary:hover{background:var(--wash)}'
       '.ws-tm{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}'
       '.ws-ti{font-weight:500;overflow-wrap:anywhere}'
       '.ws-chips{grid-column:2;display:flex;flex-wrap:wrap;gap:6px}.ws-chips:empty{display:none}'
       '.ws-chip{font-size:12px;line-height:16px;font-weight:500;padding:3px 9px;border-radius:8px;background:var(--wash);'
       'color:var(--muted);white-space:nowrap}'
       '.ws-body{display:flex;flex-direction:column;gap:8px;padding:0 14px 14px}'
       '.ws-blk{border-radius:8px;padding:10px 14px;background:var(--wash)}.ws-blk p{margin:0;overflow-wrap:anywhere}'
       '.ws-ov{display:block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);'
       'margin:0 0 2px}'
       '.ws-blk.ask{background:light-dark(#fff1e0,#3a2a18)}.ws-blk.ask .ws-ov{color:light-dark(#8a4b08,#ffb874)}'
       '.ws-blk.ask p{font-style:italic}'
       '.ws-blk.dd{background:var(--soft)}.ws-blk.dd .ws-ov{color:var(--accent)}'
       '.ws-blk.done{background:light-dark(#e8f6ec,#1c3324)}.ws-blk.done .ws-ov{color:light-dark(#1e7b34,#8bd49a)}'
       '.ws-ph>.ws-card{background:var(--soft);border-color:transparent}.ws-ph .ws-ti{font-weight:600}'
       '.ws-ph .ws-body p{margin:0;font-size:14px}'
       '.ws-plain{list-style:none;padding-left:0!important;margin:0}.ws-plain>li{margin:0 0 8px}'
       '.ws-pt{padding-left:16px;text-indent:-16px}.ws-pt::before{content:"•";display:inline-block;width:16px;'
       'text-indent:0;color:var(--muted)}.ws-tl>li.ws-pt::before{display:none}'
       '.ws-body>.ws-tl,.ws-body>.ws-plain{margin-top:6px}'
       '@media(max-width:600px){.ws-chips{grid-column:1/-1}}</style>')


def _card(head, subs):
    """One entry: its summary row (time, title, chips) and its blocks; a phase is a tonal milestone."""
    phase, timed = _PHASE.match(head), _TIME.match(head)
    chips, blocks = [], []
    for sub in subs:
        m = _LABEL.match(re.sub(r'<[^>]+>', '', sub)) if ':' in sub[:24] else None
        if m and m.group(1) in CHIPS:
            chips += [f'<span class=ws-chip>{c.strip()}</span>' for c in m.group(2).split(',') if c.strip()]
        elif m and m.group(1) in TINTS:
            text = sub.split(':', 1)[1].strip()
            blocks.append(f'<div class="ws-blk {TINTS[m.group(1)]}"><span class=ws-ov>{m.group(1)}</span><p>{text}</p></div>')
        else:
            blocks.append(f'<p>{sub}</p>')
    header = phase or _HEADER.match(head)
    if phase:
        tm, ti = phase.group(1), phase.group(2)
    elif header:
        tm, ti = '', head[3:-4]
    elif timed:
        tm, ti = timed.group(1), timed.group(2)
    else:
        tm, ti = '', head
    summary = ((f'<span class=ws-tm>{tm}</span>' if tm else '<span class=ws-tm></span>') + f'<span class=ws-ti>{ti}</span>'
               + f'<span class=ws-chips>{"".join(chips)}</span>')
    return (f'<li{" class=ws-ph" if header else ""}><details class=ws-card><summary>{summary}</summary>'
            f'<div class=ws-body>{"".join(blocks)}</div></details></li>'), bool(phase or timed)


_LI = re.compile(r'<li( style="margin-left:[^"]*")?>((?:(?!</li>).)*)</li>', re.S)
_HEADER = re.compile(r'^<b>[^<]*</b>$')


def _rows(inner):
    """[(line, [sub-items])] of a list the workbench Markdown drew flat (a sub-item is an indented sibling)."""
    rows = []
    for m in _LI.finditer(inner):
        if m.group(1) and rows:
            rows[-1][1].append(m.group(2))
        elif not m.group(1):
            rows.append((m.group(2).strip(), []))
    return rows


def _list(items, timed):
    cls = ' class=ws-tl' if timed else ' class=ws-plain'
    return f'<ul{cls}>{"".join(items)}</ul>'


def folded(body):
    """A list item with sub-items reads as one card that opens: its line is the summary, its sub-items the detail.
    `Session:` and `Area:` lines become chips, `JL asked:`, `Decided:` and `Built:` tinted blocks; a list whose items
    start with a bold time is a timeline. An item bold all through (`**12:39 → 13:51 · title**`, `**The decisions**`) is
    a header: it collects the items after it, up to the next header, so a long list opens as a few headers (JL 261114,
    the AI-eval: "walls of 100+ cards")."""
    def ul(list_html):
        rows = _rows(list_html.group(2))
        if not any(subs or _HEADER.match(line) for line, subs in rows):
            return list_html.group(0)                    # a plain list stays as it was
        top, group, timed = [], None, False
        for line, subs in rows:
            if _HEADER.match(line):
                group = [line, subs, [], False]
                top.append(group)
                continue
            if subs:
                card, is_timed = _card(line, subs)
            else:
                card, is_timed = f'<li class=ws-pt>{line}</li>', False
            if not group:
                timed = timed or is_timed                # the outer list is a timeline only for its own entries
            if group:
                group[2].append(card)
                group[3] = group[3] or is_timed
            else:
                top.append(card)
        out = []
        for item in top:
            if isinstance(item, str):
                out.append(item)
                continue
            line, subs, inner, inner_timed = item
            card, is_timed = _card(line, subs)
            timed = timed or is_timed                    # a timed header (a phase) puts the list on a line
            if inner:                                    # its entries inside it, under its own words
                card = card.replace('</div></details></li>', _list(inner, inner_timed) + '</div></details></li>', 1)
            out.append(card)
        return _list(out, timed)
    out = re.sub(r'<ul( [^>]*)?>(.*?)</ul>', ul, body, flags=re.S)
    return (CSS + out) if 'ws-card' in out else out


def view_html(folder, root, data, view, section, start=1):
    """The view's numbered sections from `start`, or '' when the face names none (the caller keeps its fixed frame)."""
    parts = declared(folder, root, data, view)
    return ''.join(section(n, title, folded(body)) for n, (title, body) in enumerate(parts, start))
