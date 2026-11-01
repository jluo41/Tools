import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const source=import.meta.dirname;
const root=path.dirname(source);
const out=path.join(root,'build/v8');
const spec=JSON.parse(await fs.readFile(path.join(source,'deck-content-v8.json'),'utf8'));
const deck=Presentation.create({slideSize:{width:1600,height:900}});
for(const item of spec.slides){
 const s=deck.slides.add();s.background.fill='#ffffff';
 const bytes=await fs.readFile(path.resolve(source,item.image));
 s.images.add({blob:bytes,contentType:'image/png',alt:item.title,fit:'contain',position:{left:0,top:0,width:1600,height:900}});
 s.speakerNotes.text=item.notes+'\n\nSource: '+spec.source;
}
if(deck.slides.items.length!==15)throw Error('Expected fifteen slides');
await fs.mkdir(out,{recursive:true});
for(const [i,s] of deck.slides.items.entries()){
 const png=await deck.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(out,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
const imported=await PresentationFile.importPptx(await FileBlob.load(candidate));
if(imported.slides.items.length!==15)throw Error('Round-trip count mismatch');
const final=path.join(root,'deliverables/agent-mediated-labeling-workflows-and-evaluation-v8-illustrated.pptx');
try {await fs.access(final);throw Error('Release already exists; choose a new version');}catch(e){if(e.code!=='ENOENT')throw e;}
await fs.writeFile(path.join(out,'validation.json'),JSON.stringify({slides:15,roundTripImport:'passed',base:'v7 illustrated',changedSlides:[6,9,10,11],addedSlides:[15],illustrations:'raster',speakerNotes:'editable'},null,2));
console.log(candidate);
