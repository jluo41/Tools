from pathlib import Path
import zipfile,xml.etree.ElementTree as E,re,posixpath,json,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
root=Path(__file__).resolve().parent.parent
spec=json.loads((root/'source/deck-content-v6.json').read_text())
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def art(z,i):
    doc=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    embed=doc.find('.//a:blip',ns).attrib['{'+ns['r']+'}embed']
    rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
    target=next(x.attrib['Target'] for x in rel if x.attrib['Id']==embed)
    return z.read(posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/'))
p=root/'build/v6/candidate.pptx'
with zipfile.ZipFile(p) as z,zipfile.ZipFile(root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v3.pptx') as old:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])==14
    for i in range(1,6):assert art(z,i)==art(old,i),f'Slide {i} altered'
    for i,s in enumerate(spec['slides'],1):assert art(z,i)==(root/'source'/s['image']).read_bytes()
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)])==14
    size=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns)
    assert (size.attrib['cx'],size.attrib['cy'])==('15240000','8572500')
report=json.loads((root/'build/v6/validation.json').read_text())
assert report['roundTripImport']=='passed'
report.update(packageIntegrity='passed',originalFiveIllustrations='unchanged',illustrationEmbedding='exact',visualReview='new nine illustrations inspected; loop and preparation corrections incorporated',aspectRatio='16:9')
base='agent-mediated-labeling-workflows-and-evaluation-v6-illustrated'
final=root/'deliverables'/f'{base}.pptx'
pdf=root/'build/v6/candidate.pdf'
assert not final.exists()
assert not (root/'deliverables'/f'{base}.pdf').exists()
c=canvas.Canvas(str(pdf),pagesize=(1200,675),pageCompression=1)
c.setTitle('Agent-mediated labeling: meaning and expression loops')
c.setSubject('Training-free end-to-end agent workflow. Proposed design for discussion.')
for i,s in enumerate(spec['slides'],1):
    img=ImageReader(str((root/'source'/s['image']).resolve()))
    iw,ih=img.getSize();scale=min(1200/iw,675/ih)
    w,h=iw*scale,ih*scale
    c.drawImage(img,(1200-w)/2,(675-h)/2,width=w,height=h)
    key=f'slide-{i}'
    c.bookmarkPage(key)
    c.addOutlineEntry(f'{i}. {s["title"]}',key,level=0)
    c.showPage()
c.save()
r=PdfReader(str(pdf))
assert len(r.pages)==14
for page in r.pages:
    assert float(page.mediabox.width)==1200 and float(page.mediabox.height)==675
report.update(pdfPageCount=14,pdfPageSize='1200 x 675 pt',pdfBookmarks=14)
(root/'build/v6/validation.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copy2(p,final)
shutil.copy2(pdf,root/'deliverables'/f'{base}.pdf')
print(final)
print(root/'deliverables'/f'{base}.pdf')
