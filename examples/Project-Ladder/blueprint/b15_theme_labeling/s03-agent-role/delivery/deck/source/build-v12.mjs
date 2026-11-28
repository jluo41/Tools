import fs from 'node:fs/promises';
import path from 'node:path';
import {PresentationFile, FileBlob} from '@oai/artifact-tool';
const source=import.meta.dirname, root=path.dirname(source), out=path.join(root,'build/v12');
const spec=JSON.parse(await fs.readFile(path.join(source,'deck-content-v12.json'),'utf8'));
const deck=await PresentationFile.importPptx(await FileBlob.load(path.join(root,'deliverables/agent-mediated-labeling-workflows-and-evaluation-v11-alignment-audit.pptx')));
if(deck.slides.items.length!==22)throw Error('Expected 22 source slides');
const originals=[...deck.slides.items];
for(const item of spec.updates){
 if(item.id==='12a')continue;
 const slide=originals[Number(item.id)-1], pic=slide.images.items[0], frame=pic.frame;
 if(slide.images.items.length!==1)throw Error('Expected one illustration');
 pic.replace({blob:await fs.readFile(path.resolve(source,item.image)),contentType:'image/png',alt:item.title,fit:'contain'});pic.frame=frame;
 slide.speakerNotes.text=item.notes;
}
for(const item of spec.noteUpdates) originals[item.n-1].speakerNotes.text += '\n\nVersion 12 clarification: '+item.notes;
const item=spec.updates.find(x=>x.id==='12a');
const bridge=deck.slides.add({background:{fill:'#ffffff'}});
deck.slides.reorder([...originals.slice(0,12),bridge,...originals.slice(12)].map(s=>s.id.startsWith('sl/')?s.id:'sl/'+s.id));
bridge.images.add({blob:await fs.readFile(path.resolve(source,item.image)),contentType:'image/png',alt:item.title,fit:'contain',position:{left:0,top:0,width:1600,height:900}});
bridge.speakerNotes.text=item.notes;
if(deck.slides.items[12].id!==bridge.id||deck.slides.items.length!==23)throw Error('Insertion failed');
await fs.mkdir(out,{recursive:true});
for(const [i,slide]of deck.slides.items.entries()){
 const png=await deck.export({slide,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
await(await PresentationFile.exportPptx(deck)).save(path.join(out,'candidate.pptx'));
const check=await PresentationFile.importPptx(await FileBlob.load(path.join(out,'candidate.pptx')));
if(check.slides.items.length!==23)throw Error('Round-trip count failed');
await fs.writeFile(path.join(out,'validation.json'),JSON.stringify({slides:23,roundTripImport:'passed',base:'v11',stableSlideIds:'1–12, 12a, 13–22',illustrations:'raster',speakerNotes:'editable'},null,2));
console.log('Built and rendered 23 slides; transition inserted after Step 5.');
