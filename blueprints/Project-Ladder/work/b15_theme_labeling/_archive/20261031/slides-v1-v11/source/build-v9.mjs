import fs from 'node:fs/promises';
import path from 'node:path';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const source=import.meta.dirname;
const root=path.dirname(source);
const out=path.join(root,'build/v9');
const spec=JSON.parse(await fs.readFile(path.join(source,'deck-content-v9.json'),'utf8'));
const prior=path.join(root,'deliverables/agent-mediated-labeling-workflows-and-evaluation-v8-illustrated.pptx');
const deck=await PresentationFile.importPptx(await FileBlob.load(prior));
if(deck.slides.items.length!==15)throw Error('Expected fifteen source slides');
if(spec.slides.length!==5)throw Error('Expected five UI concept additions');
for(const item of spec.slides){
 const s=deck.slides.add();s.background.fill='#ffffff';
 const bytes=await fs.readFile(path.resolve(source,item.image));
 s.images.add({blob:bytes,contentType:'image/png',alt:item.title,fit:'contain',position:{left:0,top:0,width:1600,height:900}});
 s.speakerNotes.text=item.notes+'\n\nSource: '+spec.source;
}
if(deck.slides.items.length!==20)throw Error('Expected twenty slides');
await fs.mkdir(out,{recursive:true});
for(const [i,s] of deck.slides.items.entries()){
 const png=await deck.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(out,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
const imported=await PresentationFile.importPptx(await FileBlob.load(candidate));
if(imported.slides.items.length!==20)throw Error('Round-trip count mismatch');
await fs.writeFile(path.join(out,'validation.json'),JSON.stringify({slides:20,roundTripImport:'passed',base:'v8 illustrated',changedSlides:[],addedSlides:[16,17,18,19,20],illustrations:'raster',speakerNotes:'editable',claims:'Proposed UI, synthetic examples, no measured model results',verification:'Exact bytes and logical versions; no content hashes'},null,2));
console.log(candidate);
