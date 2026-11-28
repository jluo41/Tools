import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const build=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(build);
const spec=JSON.parse(await fs.readFile(path.join(build,'deck-content.json'),'utf8'));
const presentation=Presentation.create({slideSize:{width:1600,height:900}});
for(const [i,item] of spec.slides.entries()){
  const slide=presentation.slides.add();
  slide.background.fill='#ffffff';
  const bytes=await fs.readFile(path.resolve(build,item.image));
  slide.images.add({blob:bytes,contentType:'image/png',alt:item.title+'. '+item.notes,fit:'contain',position:{left:0,top:0,width:1600,height:900}});
  slide.speakerNotes.text=item.notes+'\n\nSource: '+spec.source;
}
await fs.mkdir(path.join(build,'previews'),{recursive:true});
for(const [i,slide] of presentation.slides.items.entries()){
  const png=await presentation.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(build,'previews',`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidate);
const imported=await PresentationFile.importPptx(await FileBlob.load(candidate));
if(imported.slides.items.length!==5)throw new Error('Expected exactly five slides');
await fs.writeFile(path.join(build,'import-check.txt'),'Imported successfully: 5 slides.\nImage-based diagrams; editable speaker notes.\n');
console.log('Built and rendered five slides; PPTX reimport succeeded.');
