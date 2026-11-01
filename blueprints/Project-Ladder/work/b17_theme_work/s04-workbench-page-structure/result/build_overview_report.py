"""Build the b17 Overview–Report design preview from its existing register.
Generated HTML is disposable; edit this builder/template, never the output.
"""
from pathlib import Path
import html, json, re, sys
from urllib.parse import quote, urlencode
import yaml

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]                           # this builder sits in s04's result/, s04 beside the Jobs
ROOT = BLOCK.parents[3]

def field(text, key):
    m = re.search(r'^' + re.escape(key) + r':\s*(.*)$', text, re.M)
    return m.group(1).strip() if m else ''

def plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("**", "").replace("`", "")

def section(text, name, depth=2):
    m = re.search(r'^' + '#' * depth + r' ' + re.escape(name) + r'\s*\n(.*?)(?=^#{1,' + str(depth) + r'} |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''

def url(path):
    path = path.resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.exists():
        return ''
    return '/' + quote(path.relative_to(ROOT.resolve()).as_posix(), safe='/')

def reader(path):
    return '/_board/page?' + urlencode({'path':url(path)})

def wb(path, **extra):
    return '/_board/workbench?' + urlencode({'path':path.relative_to(ROOT).as_posix(), **extra})

text = (BLOCK / 'board.md').read_text()
register = section(text, 'Questions')
match = re.search(r'```yaml\s*\n(.*?)```', register, re.S)
rows = yaml.safe_load(match.group(1))['questions']
topics=[]
for folder in sorted((BLOCK/'studio').glob('s[0-9][0-9]-*')):
    face=folder/(folder.name+'.md')
    if not face.exists(): continue
    body=face.read_text()
    tags=re.search(r'\*\*Tags:\*\*\s*(.*)',body)
    purpose=re.search(r'\*\*Topic:\*\*\s*(.*)',body)
    files=[]
    for label, target in [('Draw',folder/(folder.name+'.excalidraw')),('Mind map',folder/(folder.name+'.mindmap.html'))]:
        if target.exists():
            link=('/_excalidraw/?'+urlencode({'board':target.relative_to(ROOT).as_posix()})) if label=='Draw' else url(target)
            files.append({'label':label,'url':link})
    topics.append({'id':folder.name,'tags':tags.group(1).split(' · ') if tags else [],'purpose':purpose.group(1) if purpose else '', 'files':files,'text':body})
items=[]
for q in rows:
    report=(BLOCK/q['report']).resolve()
    if not report.is_relative_to(ROOT.resolve()) or not report.is_file(): continue
    report_text=report.read_text()
    opening=section(report_text,'Opening').split('\n\n')[0]
    answer=section(report_text,'Answer',3).split('\n\n')[0]
    evidence=[]
    for label, ref in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',section(report_text,'Evidence',3)):
        target=(report.parent/ref).resolve()
        link=url(target)
        if link:
            if target.suffix=='.excalidraw': link='/_excalidraw/?'+urlencode({'board':target.relative_to(ROOT).as_posix()})
            evidence.append({'title':label,'url':link})
    linked=[]
    for work in q.get('work',[]):
        ref=work if isinstance(work,str) else work.get('path','')
        target=(BLOCK/ref).resolve()
        if ref and url(target): linked.append({'title':target.name,'url':wb(target,layout='focus') if target.is_dir() else url(target)})
    associated=[{k:v for k,v in t.items() if k!='text'} for t in topics if report.parent.name in t['text'] or re.search(r'\b'+re.escape(q['id'])+r'\b',t['text'])]
    items.append({'id':q['id'],'title':q['title'],'goal':q['question'],'acceptance':q.get('acceptance',''),'status':field(report_text,'answer-status') or 'Not recorded','state':field(report_text,'state'),'opening':plain(opening),'answer':plain(answer),'next':plain(section(report_text,'Next',3)),'evidence':evidence,'work':linked,'topics':associated,'report':reader(report),'source':url(report)})
def navigation_page(folder):
    face = next((f for f in [folder/(folder.name+'.md'), folder/'board.md'] if f.is_file()), None)
    heading = re.search(r'^#\s+(.+)$', face.read_text(), re.M) if face else None
    identity = folder.name.split('_', 1)[0]
    title = plain(heading.group(1)) if heading else folder.name.partition('_')[2].replace('_', ' ')
    title = re.sub(r'^'+re.escape(identity)+r'\s*[·:–-]\s*', '', title, flags=re.I)
    return {'id':identity, 'title':title or folder.name, 'folder':folder.name,
            'url':wb(folder,layout='focus'), 'current':folder==BLOCK}

data={'title':'b17 · Theme: work','goal':field(text,'spine'),'close':field(text,'close'),'items':items,'topics':[{k:v for k,v in t.items() if k!='text'} for t in topics], 'siblings':[navigation_page(p) for p in sorted(BLOCK.parent.glob('b*')) if p.is_dir() and (p/'board.md').exists()], 'children':[navigation_page(p) for p in sorted(BLOCK.glob('j[0-9][0-9]*')) if p.is_dir()], 'parent':{'title':'Blueprints','url':wb(BLOCK.parent,layout='focus',section='folders')}, 'existing':wb(BLOCK,studio=1),'source':reader(BLOCK/'board.md')}
data['timeline']=[{'date':'2026-10-28','title':'Page structure agreed','text':'Separate page hierarchy, primary goal, sections and views; combine Map and Executive Report under Overview.','url':reader(HERE.parent/'s04-workbench-page-structure.md')}]
data['folders']=[{'title':f.name,'url':wb(f,layout='focus',section='folders') if f.is_dir() else reader(f) if f.suffix=='.md' else url(f),'directory':f.is_dir()} for f in sorted(BLOCK.iterdir()) if not f.name.startswith('.') and (f.is_dir() or f.suffix=='.md')]
data['deliveries']=[{'title':f.relative_to(BLOCK/'delivery').as_posix(),'url':url(f)} for f in sorted((BLOCK/'delivery').rglob('*')) if f.is_file() and f.suffix.lower() in ('.pdf','.docx','.html','.png','.svg','.pptx')]
encoded=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
output=HERE/'overview-report.html'
# Use the shared skill renderer; the authored map remains the single map source.
sys.path.insert(0, str(ROOT/'plugins/haipipe-toolkit/skills/1_base/project/haipipe-mindmap/scripts'))
import mmmap
import mmhtml

def map_url(path):
    path = path.resolve()
    if not url(path):
        return ''
    if path.suffix == '.md':
        return reader(path)
    if path.suffix == '.excalidraw':
        return '/_excalidraw/?' + urlencode({'board':path.relative_to(ROOT).as_posix()})
    return url(path)

map_html = mmmap.fragment(HERE/'b17-overview.mindmap.md', editable=False, url_of=map_url)
crumbs = ' <span aria-hidden="true">/</span> '.join(
    '<a href="'+html.escape(href, quote=True)+'"'+(' aria-current="page"' if current else '')+'>'+label+'</a>'
    for label, href, current in [
        ('Tools', wb(ROOT, layout='focus', section='folders'), False),
        ('Blueprints', wb(BLOCK.parents[2], layout='focus', section='folders'), False),
        (BLOCK.name, '#overview', True),
    ])
# the Executive report left the face on 261031 (s04-D05) and is kept whole, with the old face, in face-history-261031.md
exec_report = mmhtml.blocks(section((HERE/'face-history-261031.md').read_text(),'Executive report'))
template = (HERE/'overview-report.template.html').read_text()
output.write_text(template.replace('__DATA__',encoded).replace('__MINDMAP__',map_html).replace('__BREADCRUMBS__',crumbs).replace('__EXEC_REPORT__',exec_report))
print(f'Built {output}: {len(items)} source-backed items; '+str(len(data['children']))+' Jobs')
