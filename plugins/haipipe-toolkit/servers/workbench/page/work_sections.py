"""A page's own sections, written on its face, in place of the fixed work frame.

A Block (or Job, or Task) whose material does not fit Goal · Requirements · MindMap or Data · Values · Displays
names its own sections on its face (JL 261114: "If I give you the random things ... propose the new structure"):

    ## Review Content              the Overview's sections
    ### 🗓️ The week                one numbered section; its body is Markdown
    embed: src/review/week.md      a line that brings in a .md (rendered) or an .svg drawing (an .html never)

    ## Plan + Results              sections after its Jobs, the same way (a replay's days, a plan's steps)
    ## Findings                    the Findings view's sections, the same way
    ## Design                      a Design view of its own, after Overview (the person's high-level design)
    each: src/review/area-*.md     one section per file, titled by the file's `# ` line

A face without these sections keeps the fixed frame. Viewing writes nothing.
"""
from pathlib import Path
import re

from live import frame

KEYS = {'overview': 'review content', 'standing': 'plan + results', 'findings': 'findings', 'design': 'design'}
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
        return (f'<div class=ws-pic style="overflow-x:auto;border:1px solid var(--line);border-radius:12px">{svg}</div>'
                + PICK_JS)                                   # a click on a station opens it in the pop-out
    return f.markdown(_titled(path)[1], path.parent, root)     # the section already carries the title


# A drawing's station that carries `data-card` (JSON: tm, ti, chips, blocks) opens as a card under the drawing on a
# click (JL 261114: "I can just see but cannot click it"), drawn as the timeline's cards; the station it came from rings.
PICK_JS = """<script>(function(){if(window.__wsPick)return;window.__wsPick=1;
var T={'Asked':'ask','Decided':'dd','Built':'done','Done':'done','Returned':'done'};
function e(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function cardDoc(d){var b=(d.blocks||[]).filter(function(k){return k[1]}).map(function(k){
var w=/^\S+ asked$/.test(k[0])?'Asked':k[0];return '<div class="blk '+(T[w]||'')+'"><span class=ov>'+e(w)+'</span><p>'+e(k[1])+'</p></div>'}).join('');
var c=(d.chips||[]).filter(Boolean).map(function(x){return '<span class=chip>'+e(x)+'</span>'}).join('');
return '<!doctype html><meta charset=utf-8><style>body{margin:0;padding:18px 20px;font:15px/1.55 -apple-system,Segoe UI,'+
'sans-serif;color:#1b1c1f;background:#fff}h1{font-size:18px;margin:0 0 4px}.tm{color:#5f6368;font-size:13px}'+
'.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 14px}.chip{font-size:12px;padding:3px 9px;border-radius:8px;'+
'background:#eef2f7;color:#5f6368}.blk{border-radius:10px;padding:10px 14px;margin:0 0 10px;background:#f6f6f7}'+
'.blk p{margin:0}.ov{display:block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;'+
'color:#5f6368;margin-bottom:2px}.ask{background:#fff1e0}.ask .ov{color:#8a4b08}.ask p{font-style:italic}'+
'.dd{background:#e7f5ff}.dd .ov{color:#1864ab}.done{background:#e8f6ec}.done .ov{color:#1e7b34}</style>'+
'<div class=tm>'+e(d.tm)+'</div><h1>'+e(d.ti)+'</h1><div class=chips>'+c+'</div>'+b}
document.addEventListener('click',function(ev){var s=ev.target.closest&&ev.target.closest('.ws-pic [data-card]');if(!s)return;
var d;try{d=JSON.parse(s.getAttribute('data-card'))}catch(x){return}
var dlg=document.querySelector('#focus-viewer');if(!dlg)return;ev.preventDefault();
document.querySelectorAll('.ws-pic .ws-on').forEach(function(x){x.classList.remove('ws-on')});s.classList.add('ws-on');
var f=dlg.querySelector('iframe'),go=dlg.querySelector('[data-viewer-go]'),href=s.getAttribute('data-href');
dlg.querySelector('[data-viewer-title]').textContent=(d.tm?d.tm+' · ':'')+(d.ti||'');
if(href){f.removeAttribute('srcdoc');f.src=href;if(go){go.href=href;go.hidden=false}}
else{f.removeAttribute('src');f.srcdoc=cardDoc(d);if(go)go.hidden=true}
dlg.showModal();if(!dlg.__ws){dlg.__ws=1;dlg.addEventListener('close',function(){f.removeAttribute('srcdoc');if(go)go.hidden=false})}
});
/* hover: a small hint at once (time, title, first line), the click above opens the whole thing (JL 261115: "keep both") */
var tip=null;function hide(){if(tip){tip.remove();tip=null}}
document.addEventListener('mouseover',function(ev){var s=ev.target.closest&&ev.target.closest('.ws-pic [data-card]');if(!s){hide();return}
var t=s.querySelector('title');if(t){s.setAttribute('aria-label',t.textContent);t.remove()}   /* no slow native tooltip on top */
var d;try{d=JSON.parse(s.getAttribute('data-card'))}catch(x){return}hide();
var first=(d.blocks||[]).filter(function(k){return k[1]})[0];
tip=document.createElement('div');tip.className='ws-tip';
tip.innerHTML='<div class=ws-tip-h><span>'+e(d.tm)+'</span> <b>'+e(d.ti)+'</b></div>'+
(first?'<div class=ws-tip-b>'+e(first[1]).slice(0,180)+'</div>':'')+'<div class=ws-tip-f>click to open</div>';
document.body.appendChild(tip);var r=s.getBoundingClientRect(),w=tip.offsetWidth,h=tip.offsetHeight;
var L=Math.min(Math.max(8,r.left+r.width/2-w/2),innerWidth-w-8),Y=r.top-h-10;if(Y<8)Y=r.bottom+10;
tip.style.left=L+'px';tip.style.top=Y+'px'});
addEventListener('scroll',hide,true);document.addEventListener('click',hide,true);
})();</script>"""


def drawing_html(svg: str) -> str:
    """A drawing in a section: inline (its stations' hover titles show), scrolling sideways, a click opening a station
    in the workbench pop-out."""
    return (CSS + f'<div class=ws-pic style="overflow-x:auto;border:1px solid var(--line);border-radius:12px">{svg}</div>'
            + PICK_JS) if svg else ''


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
TINTS = {'Asked': 'ask', 'Decided': 'dd', 'Built': 'done', 'Done': 'done'}
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
       '.ws-tip{position:fixed;z-index:60;max-width:320px;pointer-events:none;background:var(--paper,#fff);'
       'border:1px solid var(--line);border-radius:10px;padding:8px 10px;box-shadow:0 4px 14px #00000026;font-size:13px;'
       'line-height:1.45}.ws-tip-h span{color:var(--muted)}.ws-tip-b{margin-top:3px}'
       '.ws-tip-f{margin-top:4px;font-size:11px;color:var(--accent)}'
       '.ws-pic [data-card]{cursor:pointer}.ws-pic [data-card]:hover,.ws-pic .ws-on{stroke:var(--accent);stroke-width:3}'
       '@media(max-width:600px){.ws-chips{grid-column:1/-1}}</style>')


def _card(head, subs):
    """One entry: its summary row (time, title, chips) and its blocks; a phase is a tonal milestone."""
    phase, timed = _PHASE.match(head), _TIME.match(head)
    chips, blocks = [], []
    for sub in subs:
        m = _LABEL.match(re.sub(r'<[^>]+>', '', sub)) if ':' in sub[:24] else None
        label = 'Asked' if m and re.fullmatch(r'\S+ asked', m.group(1)) else m.group(1) if m else ''   # an old `<name> asked:` reads as Asked
        if m and m.group(1) in CHIPS:
            chips += [f'<span class=ws-chip>{c.strip()}</span>' for c in m.group(2).split(',') if c.strip()]
        elif m and label in TINTS:
            text = sub.split(':', 1)[1].strip()
            blocks.append(f'<div class="ws-blk {TINTS[label]}"><span class=ws-ov>{label}</span><p>{text}</p></div>')
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
    `Session:` and `Area:` lines become chips, `Asked:`, `Decided:` and `Built:` tinted blocks; a list whose items
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
    return (CSS + out) if ('ws-card' in out or 'ws-pic' in out) else out


def view_html(folder, root, data, view, section, start=1):
    """The view's numbered sections from `start`, or '' when the face names none (the caller keeps its fixed frame)."""
    parts = declared(folder, root, data, view)
    return ''.join(section(n, title, folded(body)) for n, (title, body) in enumerate(parts, start))
