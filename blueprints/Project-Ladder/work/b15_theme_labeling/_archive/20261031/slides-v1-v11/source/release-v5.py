from pathlib import Path
import zipfile,xml.etree.ElementTree as E,re,posixpath,json,shutil
root=Path(__file__).resolve().parent.parent
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def art(z,i):
    doc=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    embed=doc.find('.//a:blip',ns).attrib['{'+ns['r']+'}embed']
    rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
    target=next(x.attrib['Target'] for x in rel if x.attrib['Id']==embed)
    return z.read(posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/'))
p=root/'build/v5/candidate.pptx'
with zipfile.ZipFile(p) as z,zipfile.ZipFile(root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v3.pptx') as old:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])==6
    for i in range(1,6):assert art(z,i)==art(old,i),f'Slide {i} altered'
    assert art(z,6)==(root/'assets/slide-06-v5.png').read_bytes()
    assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)])==6
    size=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns)
    assert (size.attrib['cx'],size.attrib['cy'])==('15240000','8572500')
report=json.loads((root/'build/v5/validation.json').read_text())
assert report['roundTripImport']=='passed'
report.update(packageIntegrity='passed',originalFiveIllustrations='unchanged',newSlideEmbedding='exact',visualReview='slide 6 rendered and inspected; corrected feedback connectors',aspectRatio='16:9')
(root/'build/v5/validation.json').write_text(json.dumps(report,indent=2)+'\n')
final=root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v5-illustrated.pptx'
assert not final.exists()
shutil.copy2(p,final)
print(final)
