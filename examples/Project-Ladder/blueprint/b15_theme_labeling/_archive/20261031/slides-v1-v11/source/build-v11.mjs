import fs from 'node:fs/promises';
import path from 'node:path';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const source=import.meta.dirname, root=path.dirname(source), out=path.join(root,'build/v11');
const spec=JSON.parse(await fs.readFile(path.join(source,'deck-content-v11.json'),'utf8'));
const deck=await PresentationFile.importPptx(await FileBlob.load(path.join(root,'deliverables/agent-mediated-labeling-workflows-and-evaluation-v9-ui-concepts.pptx')));
if(deck.slides.items.length!==20)throw Error('Expected twenty source slides');
for(const item of spec.updates){
 const bytes=await fs.readFile(path.resolve(source,item.image));
 let slide;
 if(item.n<=20){
  slide=deck.slides.items[item.n-1];
  if(slide.images.items.length!==1)throw Error('Expected one illustration');
  const pic=slide.images.items[0], frame=pic.frame;
  pic.replace({blob:bytes,contentType:'image/png',alt:item.title,fit:'contain'});
  pic.frame=frame;
 }else{
  slide=deck.slides.add();slide.background.fill='#ffffff';
  slide.images.add({blob:bytes,contentType:'image/png',alt:item.title,fit:'contain',position:{left:0,top:0,width:1600,height:900}});
 }
 slide.speakerNotes.text=item.notes+'\n\nSource: '+spec.source;
}
for(const item of spec.noteUpdates ?? []) deck.slides.items[item.n-1].speakerNotes.text=item.notes;
if(deck.slides.items.length!==spec.totalSlides)throw Error('Final slide count mismatch');
await fs.mkdir(out,{recursive:true});
for(const [i,s] of deck.slides.items.entries()){
 const png=await deck.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(out,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
const imported=await PresentationFile.importPptx(await FileBlob.load(candidate));
if(imported.slides.items.length!==spec.totalSlides)throw Error('Round-trip count mismatch');
await fs.writeFile(path.join(out,'validation.json'),JSON.stringify({slides:spec.totalSlides,roundTripImport:'passed',base:'v9',changedSlides:spec.updates.filter(x=>x.n<=20).map(x=>x.n),addedSlides:spec.updates.filter(x=>x.n>20).map(x=>x.n),noteOnlyChanges:spec.noteUpdates.map(x=>x.n),illustrations:'raster',speakerNotes:'editable',claims:'Proposed workflow and synthetic UI; no measured model results'},null,2));
console.log(candidate);
