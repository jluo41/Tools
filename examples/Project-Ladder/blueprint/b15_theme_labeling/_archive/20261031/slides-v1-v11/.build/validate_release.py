from pathlib import Path
import json, re, shutil, zipfile
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent.parent
p=root/'.build/candidate.pptx'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(p) as z:
    slides=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide[0-9]+.xml',n))
    assert len(slides)==5
    pres=ET.fromstring(z.read('ppt/presentation.xml'))
    size=pres.find('p:sldSz',ns)
    assert (int(size.attrib['cx']),int(size.attrib['cy']))==(15240000,8572500)
    for name in slides:
        doc=ET.fromstring(z.read(name)); pics=doc.findall('.//p:pic',ns)
        assert len(pics)==1,(name,len(pics))
        for pic in pics:
            x=pic.find('.//a:xfrm',ns);off=x.find('a:off',ns);ext=x.find('a:ext',ns)
            left,top=int(off.attrib['x']),int(off.attrib['y'])
            width,height=int(ext.attrib['cx']),int(ext.attrib['cy'])
            assert left>=-1 and top>=-1 and left+width<=15240001 and top+height<=8572501
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide[0-9]+.xml',n)]
    assert len(notes)==5
assert '5 slides' in (root/'.build/import-check.txt').read_text()
# The repository forbids content hashes; validate dimensions, relationships, counts,
# text/image review and successful round-trip import without hash-based receipts.
report={'slides':5,'size':'16:9','package_integrity':'passed','geometry':'passed','round_trip_import':'passed','visual_review':'revised slides 2 and 3 inspected; other three slides unchanged from reviewed version','illustrations':'raster','speaker_notes':'editable','validation_note':'No content hashes; project instruction takes precedence over hash-based finalizer.'}
(root/'.build/validation.json').write_text(json.dumps(report,indent=2))
final=root/'deliverables/agent-mediated-labeling-workflows-and-evaluation-v3.pptx'
assert not final.exists()
shutil.copy2(p,final)
spec=json.loads((root/'.build/deck-content.json').read_text())
prompts='# Image generation prompts\n\nBuilt-in imagegen. Five slides, 2026-10-27.\n\n'
for i,s in enumerate(spec['slides'],1):prompts+=f'## Slide {i}: {s["title"]}\n\n{s["prompt"]}\n\n'
prompts+='## Slide 3 arrow revision\n\n'+spec['revisionPromptForSlide3']+'\n'

for i,s in enumerate(spec['slides'],1):
    if s.get('revisionPromptV2'): prompts+=f'\n## Slide {i}: version 2 revision\n\n'+s['revisionPromptV2']+'\n'
for i,s in enumerate(spec['slides'],1):
    if s.get('revisionPromptV3'): prompts+=f'\n## Slide {i}: version 3 revision\n\n'+s['revisionPromptV3']+'\n'
(root/'generation-prompts-v3.md').write_text(prompts)
print(final)
