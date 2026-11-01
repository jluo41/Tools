"""Validate and release v12 through exact-byte checks, honoring the no-hash policy."""
from pathlib import Path
import zipfile, xml.etree.ElementTree as E, re, posixpath, json, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
root=Path(__file__).resolve().parent.parent
spec=json.loads((root/'source/deck-content-v12.json').read_text())
slides=spec['slides']
changed={int(s['id']) for s in spec['updates'] if s['id']!='12a'}
note_changes={s['n'] for s in spec.get('noteUpdates',[])}
assert len(slides)==23
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
p=root/'build/v12/candidate.pptx'
prior=root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v11-alignment-audit.pptx'
with zipfile.ZipFile(p) as z,zipfile.ZipFile(prior) as old:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])==spec["totalSlides"]
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)])==spec["totalSlides"]
    for i in range(1,23):
        if i in changed: continue
        new_i=i if i<=12 else i+1
        assert art(z,new_i)==art(old,i),f'Source slide {i} altered'
        if i not in note_changes: assert notes(z,new_i)==notes(old,i),f'Source notes {i} altered'
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
report=json.loads((root/'build/v12/validation.json').read_text())
assert report['roundTripImport']=='passed'
review_path=root/'source/visual-review-v12.json'
review=json.loads(review_path.read_text())
assert review['inspectedSlideIds']==['06','10','12','12a','21']
assert review['status']=='passed'
report.update(packageIntegrity='passed',unchangedSlideIllustrations='exact',unchangedSlideNotes='exact',illustrationEmbedding='exact',aspectRatio='16:9',visualReview=review)
base='agent-mediated-labeling-workflows-and-evaluation-v12-preference-return'
final=root/'deliverables'/f'{base}.pptx'
assert not final.exists()
def make_pdf(slides,path):
    c=canvas.Canvas(str(path),pagesize=(1200,675),pageCompression=1)
    c.setTitle('Agent-mediated labeling: Returning to the Meaning Loop')
    c.setSubject('Proposed UI with synthetic examples. No model results.')
    for i,s in slides:
        img=ImageReader(str((root/'source'/s['image']).resolve()))
        iw,ih=img.getSize();scale=min(1200/iw,675/ih);w,h=iw*scale,ih*scale
        c.drawImage(img,(1200-w)/2,(675-h)/2,width=w,height=h)
        key=f'slide-{i}';c.bookmarkPage(key);c.addOutlineEntry(f'{s["stableId"]}. {s["title"]}',key,level=0);c.showPage()
    c.save()
    r=PdfReader(str(path));assert len(r.pages)==len(slides)
    for page in r.pages:assert (float(page.mediabox.width),float(page.mediabox.height))==(1200,675)
allslides=list(enumerate(slides,1))
make_pdf(allslides,root/'build/v12/candidate.pdf')
make_pdf([allslides[i-1] for i in spec["excerptSlides"]],root/'build/v12/discussion.pdf')
outputs=[(p,final),(root/'build/v12/candidate.pdf',root/'deliverables'/f'{base}.pdf'),(root/'build/v12/discussion.pdf',root/'deliverables/subjective-labeling-preference-return-v12-discussion.pdf')]
for src,dst in outputs:
    assert not dst.exists(),dst
report.update(pdfPageCount=spec["totalSlides"],discussionExcerptPageCount=len(spec["excerptSlides"]),pdfPageSize='1200 x 675 pt')
(root/'build/v12/validation.json').write_text(json.dumps(report,indent=2)+'\n')
for src,dst in outputs:
    shutil.copy2(src,dst)
    assert src.read_bytes()==dst.read_bytes()
    print(dst)
