"""Validate and release v10 through exact-byte checks, honoring the no-hash policy."""
from pathlib import Path
import zipfile, xml.etree.ElementTree as E, re, posixpath, json, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
root=Path(__file__).resolve().parent.parent
spec=json.loads((root/'source/deck-content-v10.json').read_text())
slides=json.loads((root/'source/deck-content-v8.json').read_text())['slides']+json.loads((root/'source/deck-content-v9.json').read_text())['slides']
changed={s['n'] for s in spec['updates']}
for s in spec['updates']:
    if s['n']<=20: slides[s['n']-1]=s
    else: slides.append(s)
assert len(slides)==21
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def art(z,i):
    doc=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    embed=doc.find('.//a:blip',ns).attrib['{'+ns['r']+'}embed']
    rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
    target=next(x.attrib['Target'] for x in rel if x.attrib['Id']==embed)
    return z.read(posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/'))
def notes(z,i):
    doc=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
    return [x.text for x in doc.findall('.//a:t',ns)]
p=root/'build/v10/candidate.pptx'
prior=root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v9-ui-concepts.pptx'
with zipfile.ZipFile(p) as z,zipfile.ZipFile(prior) as old:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])==21
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)])==21
    for i in range(1,21):
        if i in changed: continue
        assert art(z,i)==art(old,i),f'Source slide {i} altered'
        assert notes(z,i)==notes(old,i),f'Source notes {i} altered'
    for i,s in enumerate(slides,1):
        assert art(z,i)==(root/'source'/s['image']).read_bytes(),f'Slide image {i}'
    size=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns)
    assert (size.attrib['cx'],size.attrib['cy'])==('15240000','8572500')
    for name in z.namelist():
        if name.endswith(('.xml','.rels')):E.fromstring(z.read(name))
        if not name.endswith('.rels'):continue
        rels=E.fromstring(z.read(name))
        base='' if name=='_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
        for rel in rels:
            if rel.attrib.get('TargetMode')=='External':continue
            target=posixpath.normpath(posixpath.join(base,rel.attrib['Target'])).lstrip('/')
            assert target in z.namelist(),(name,target)
report=json.loads((root/'build/v10/validation.json').read_text())
assert report['roundTripImport']=='passed'
review_path=root/'source/visual-review-v10.json'
review=json.loads(review_path.read_text())
assert review['inspectedSlides']==[6,7,12,13,17,19,21]
assert review['status']=='passed'
report.update(packageIntegrity='passed',unchangedSlideIllustrations='exact',unchangedSlideNotes='exact',illustrationEmbedding='exact',aspectRatio='16:9',visualReview=review)
base='agent-mediated-labeling-workflows-and-evaluation-v10-data-splits'
final=root/'deliverables'/f'{base}.pptx'
assert not final.exists()
def make_pdf(slides,path):
    c=canvas.Canvas(str(path),pagesize=(1200,675),pageCompression=1)
    c.setTitle('Agent-mediated labeling: Train and Test')
    c.setSubject('Proposed UI with synthetic examples. No model results.')
    for i,s in slides:
        img=ImageReader(str((root/'source'/s['image']).resolve()))
        iw,ih=img.getSize();scale=min(1200/iw,675/ih);w,h=iw*scale,ih*scale
        c.drawImage(img,(1200-w)/2,(675-h)/2,width=w,height=h)
        key=f'slide-{i}';c.bookmarkPage(key);c.addOutlineEntry(f'{i}. {s["title"]}',key,level=0);c.showPage()
    c.save()
    r=PdfReader(str(path));assert len(r.pages)==len(slides)
    for page in r.pages:assert (float(page.mediabox.width),float(page.mediabox.height))==(1200,675)
allslides=list(enumerate(slides,1))
make_pdf(allslides,root/'build/v10/candidate.pdf')
make_pdf([allslides[i-1] for i in (6,7,12,13,17,19,21)],root/'build/v10/data-splits.pdf')
outputs=[(p,final),(root/'build/v10/candidate.pdf',root/'deliverables'/f'{base}.pdf'),(root/'build/v10/data-splits.pdf',root/'deliverables/subjective-labeling-data-splits-v10.pdf')]
for src,dst in outputs:
    assert not dst.exists(),dst
report.update(pdfPageCount=21,dataExcerptPageCount=7,pdfPageSize='1200 x 675 pt')
(root/'build/v10/validation.json').write_text(json.dumps(report,indent=2)+'\n')
for src,dst in outputs:
    shutil.copy2(src,dst)
    assert src.read_bytes()==dst.read_bytes()
    print(dst)
