"""b34 s01: walk every display unit in the sibling SPACEs and write inventory.csv (one row per unit, relative paths).

    python build_s01_display_inventory.py        about 3 minutes; the SPACEs are large

Written by the survey agent on 2026-10-16 and moved here so the table can be made again.
"""
import os, re, csv, collections, sys
from pathlib import Path
ROOT=str(Path(__file__).resolve().parents[5])   # the folder holding the SPACEs (Desktop)
SPACES=['WellDoc','DrFirst','Physician','REACH','Knowledge']
PRUNE={'.git','.venv','node_modules'}
units={}   # abs path -> dict
mdfiles=[]
for sp in SPACES:
    base=f'{ROOT}/{sp}-SPACE'
    if not os.path.isdir(base): continue
    for d,dirs,files in os.walk(base):
        dirs[:]=[x for x in dirs if x not in PRUNE and not (d==base and x=='Tools')]
        b=os.path.basename(d)
        if re.match(r'Display\d+-',b): units[d]=sp
        elif 'README.md' in files:
            try:
                if re.search(r'^accepted:',open(d+'/README.md',errors='ignore').read(),re.M): units[d]=sp
            except: pass
        for f in files:
            if f.endswith(('.md','.tex')): mdfiles.append(d+'/'+f)
# references: Display<N>-slug names in md/tex files outside any unit and outside delivery
unitset=set(units)
def inunit(p):
    q=os.path.dirname(p)
    while q.startswith(ROOT) and len(q)>len(ROOT)+5:
        if q in unitset: return True
        q=os.path.dirname(q)
    return False
refs=collections.defaultdict(set)
pat=re.compile(r'(Display\d+-[A-Za-z0-9_-]+)')
unames={os.path.basename(u) for u in units}
unames_plain={os.path.basename(u) for u in units if not re.match(r'Display\d+-',os.path.basename(u))}
for p in mdfiles:
    if '/delivery/' in p or inunit(p): continue
    try: t=open(p,errors='ignore').read()
    except: continue
    for m in pat.findall(t): refs[m].add(p)
    for n in unames_plain:
        if n in t: refs[n].add(p)
def paperroot(u):
    parts=u.split('/')
    for i,s in enumerate(parts):
        if s.startswith('Paper-'): return '/'.join(parts[:i+1])
    return '/'.join(parts[:5])
def home(rel):
    if '/delivery/' in rel: return 'delivery-copy'
    if '/payload/' in rel: return 'page-result-payload'
    if '/display/' in rel or '/displays/' in rel or '/_archive/' in rel and 'display' in rel: return 'old-display-lane'
    return 'other'
def kindof(u,readme,files,assets):
    m=re.search(r'^kind:\s*([A-Za-z-]+)',readme,re.M)
    k=m.group(1).lower() if m else ''
    for key,val in [('tab','table'),('fig','figure'),('diag','diagram'),('illus','illustration'),('tex','tex')]:
        if k.startswith(key): return val
    a=' '.join(assets)
    if 'table-body.tex' in a or 'table-body.tex' in files: return 'table'
    ft=u+'/float.tex'
    if os.path.exists(ft):
        t=open(ft,errors='ignore').read()
        if re.search(r'\\begin\{(table|longtable|threeparttable)',t) or 'tabular' in t: return 'table'
        if 'includegraphics' in t: return 'figure'
    if any(x.endswith(('.png','.jpg','.svg')) for x in assets) or any(f.startswith('figure.') for f in files): return 'figure'
    if any(f.endswith('.md') and False for f in files): pass
    n=os.path.basename(u).lower()
    if re.search(r'(^|-)(tab|table)',n) : return 'table'
    if re.search(r'(^|-)(fig|figure|plot|forest|curve)',n): return 'figure'
    if 'diagram' in n: return 'diagram'
    return 'unknown'
bykey=collections.defaultdict(list)
for u in units: bykey[(paperroot(u),os.path.basename(u))].append(u)
def nested(u):
    q=os.path.dirname(u)
    while len(q)>len(ROOT)+5:
        if q in unitset: return True
        q=os.path.dirname(q)
    return False
nested_units=[u for u in units if nested(u)]
for u in nested_units: del units[u]
unitset=set(units)
rows=[]
for u,sp in sorted(units.items()):
    rel=os.path.relpath(u,ROOT)
    ent=os.listdir(u)
    readme=''
    if 'README.md' in ent: readme=open(u+'/README.md',errors='ignore').read()
    assets=os.listdir(u+'/assets') if os.path.isdir(u+'/assets') else []
    h=home(rel)
    name=os.path.basename(u); pr=paperroot(u)
    archived='_archive' in rel or '/_old/' in rel or 'legacy' in rel.lower()
    man=u+'/intake/manifest.yaml'
    src='no'; srcnote=''
    if os.path.exists(man):
        t=open(man,errors='ignore').read()
        if re.search(r'origin:|holder:|artifact:',t): src='manifest'
    if src=='no':
        m=re.search(r'^source:\s*(\S.*)$',readme,re.M)
        if m: src='readme-source-line'
    if src=='no' and os.path.isdir(u+'/recipe'): 
        pass
    m=re.search(r'^accepted:\s*(.*)$',readme,re.M)
    acc='no-tick'; accv=''
    if m:
        v=m.group(1).strip(); accv=v[:60]
        acc='ticked' if v.startswith('✅') else 'open'
    peers=[x for x in bykey[(pr,name)] if x!=u]
    dup_of=''
    if h=='delivery-copy': 
        s=[x for x in peers if home(os.path.relpath(x,ROOT))!='delivery-copy']
        dup_of=os.path.relpath(s[0],ROOT) if s else ''
    has_src_copy_elsewhere = any(home(os.path.relpath(x,ROOT))=='delivery-copy' for x in peers) if h!='delivery-copy' else False
    claim_m=re.search(r'^claim:\s*(.*)$',readme,re.M)
    serves='yes' if re.search(r'^serves:',readme,re.M) else 'no'
    rf=refs.get(name,set())
    rf={x for x in rf if '/Tools/' not in x and not x.endswith('SKILL.md')}
    same=[x for x in rf if x.startswith(pr+'/')]
    body=[x for x in same if not re.search(r'(-log|evidence-items|evidence\.md|outline|README|records/|/_archive/|/_old/)',x)]
    allt=readme+(open(man,errors='ignore').read() if os.path.exists(man) else '')
    bo='yes' if re.search(r'built_on',allt) else 'no'
    rows.append(dict(space=sp,path=rel,home=h,archived='yes' if archived else 'no',kind=kindof(u,readme,ent,assets),
      has_readme='README.md' in ent, has_recipe='yes' if os.path.isdir(u+'/recipe') else ('legacy-source' if os.path.isdir(u+'/source') else 'no'),name_form='Display<N>-prefix' if re.match(r'Display\d+-',name) else ('prefixed-Display' if re.search(r'Display\d+-',name) else 'other-name'),
      has_intake=os.path.isdir(u+'/intake'),has_assets=os.path.isdir(u+'/assets') or any(f.startswith('figure.') for f in ent),
      has_float_tex='float.tex' in ent,has_preview=any(f.startswith('preview.') and f.endswith(('.pdf','.png')) for f in ent),
      names_data_source=src,has_serves_line=serves,accepted=acc,accepted_value=accv,
      delivery_copy_of=dup_of,has_delivery_copy='yes' if has_src_copy_elsewhere else 'no',
      same_name_elsewhere_in_paper=len(peers),cited_by_page_files=len(rf),cited_same_paper=len(same),cited_in_page_body=len(body),names_built_on=bo,
      cited_example=os.path.relpath(sorted(rf)[0],ROOT) if rf else ''))
for r in rows:
    for k,v in r.items():
        if v is True: r[k]='yes'
        elif v is False: r[k]='no'
out=sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent / "inventory.csv")
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
