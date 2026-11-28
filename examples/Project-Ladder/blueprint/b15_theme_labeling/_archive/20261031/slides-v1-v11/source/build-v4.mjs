import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const require=createRequire(import.meta.url);
const {icons}=require('lucide');
const sharp=require('sharp');
const ROOT=path.resolve(import.meta.dirname,'..');
const OUT=path.join(ROOT,'build/v4');
const spec=JSON.parse(await fs.readFile(path.join(import.meta.dirname,'deck-content-v4.json'),'utf8'));
const P=Presentation.create({slideSize:{width:1600,height:900}});
const C={ink:'#21354A',muted:'#65778A',blue:'#276CA6',purple:'#8060AE',green:'#267E6A',amber:'#AD761F',red:'#AA5550',bg:'#FAFCFE',line:'#A7B8C9'};
const FONT='Helvetica Neue';
const objects=[];
function txt(s,str,x,y,w,h,size=26,color=C.ink,bold=false,align='left'){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=str;t.text.style={typeface:FONT,fontSize:size,color,bold,autoFit:'none',insets:0};t.text.alignment=align;
 objects.push({slide:P.slides.items.indexOf(s)+1,text:str,x,y,w,h,size});return t;
}
function box(s,x,y,w,h,fill,stroke=C.line){return s.shapes.add({geometry:'roundRect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:1.4},borderRadius:12});}
function line(s,x1,y1,x2,y2,color=C.line,end=false,both=false){
 const reverse=x2<x1||y2<y1;
 const p={left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1)};
 const a={geometry:end?'connector':'line',position:p,line:{fill:color,width:2.5},fill:'none'};
 if(end){a.kind='straight';a[reverse?'head':'tail']={type:'triangle',width:'sm',length:'sm'};if(both)a[reverse?'tail':'head']={type:'triangle',width:'sm',length:'sm'};}
 return s.shapes.add(a);
}
function route(s,pts,color=C.line,arrow=true){for(let i=1;i<pts.length;i++)line(s,...pts[i-1],...pts[i],color,arrow&&i===pts.length-1);}
const cache=new Map();
async function icon(s,name,x,y,size=62,color=C.blue){
 const key=name+color;
 if(!cache.has(key)){
  if(!icons[name])throw Error('Missing source icon '+name);
  const svg='<svg xmlns="http://www.w3.org/2000/svg" width="192" height="192" viewBox="0 0 24 24" fill="none" stroke="'+color+'" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'+icons[name].map(([tag,attrs])=>'<'+tag+' '+Object.entries(attrs).map(([k,v])=>k+'="'+v+'"').join(' ')+'/>').join('')+'</svg>';
  cache.set(key,await sharp(Buffer.from(svg)).png().toBuffer());
 }
 const b=cache.get(key);s.images.add({blob:new Uint8Array(b),contentType:'image/png',alt:name,position:{left:x,top:y,width:size,height:size}});
}
function slide(title,subtitle,index){
 const s=P.slides.add();s.background.fill=C.bg;
 txt(s,title,64,43,1470,72,51,C.ink,true);
 txt(s,subtitle,66,124,1450,48,29,C.muted);
 txt(s,String(index),1505,852,35,28,20,C.muted);
 s.speakerNotes.text=spec.slides[index-1].notes+'\n\nDesign reference: IRB/team-workspace deck shared by the user, 27 October 2026. Helvetica Neue, outline icons, muted role colors and native editable diagram shapes. Icons: Lucide, ISC license, https://lucide.dev. This deck describes proposed workflows and evaluation, not observed results.';
 return s;
}
async function node(s,ic,title,desc,x,y,w,col){await icon(s,ic,x+(w-72)/2,y,72,col);txt(s,title,x,y+90,w,76,31,col,true,'center');if(desc)txt(s,desc,x,y+178,w,90,26,C.muted,false,'center');}

// 1: The existing item-by-item workflow and its two human burdens.
{
 const s=slide('The conventional labeling workflow','The human writes the standard and applies it item by item.',1);
 const data=[['UserRound','Human','A concept in mind',70,260,C.green],['FileText','Guideline','Write the rules',435,260,C.green],['ListChecks','Item-by-item\nlabeling','Repeat the judgment',795,280,C.blue],['Files','Labeled corpus','Errors can accumulate',1220,300,C.purple]];
 for(const [ic,title,desc,x,w,col]of data)await node(s,ic,title,desc,x,250,w,col);
 line(s,335,290,415,290,C.line,true);line(s,705,290,775,290,C.line,true);line(s,1090,290,1200,290,C.line,true);
 const warnings=[['MessageSquare','Tacit preferences\nare hard to express',335],['Clock','Repeated decisions\ntake time and effort',745],['TriangleAlert','Conflicts and exceptions\ncan remain hidden',1150]];
 for(const [ic,label,x]of warnings){await icon(s,ic,x,600,42,C.red);txt(s,label,x+61,591,320,95,25,C.red);}
 txt(s,'Articulating the standard and applying it are both difficult.',80,770,1430,55,34,C.ink,true);
}

// 2 and 3: identical downstream rows, different entry evidence.
for(const existing of [false,true]){
 const n=existing?3:2;
 const s=slide(existing?'Use case 2: an existing labeled corpus':'Use case 1: a human with an idea',existing?'Recover a standard from existing labels, then apply it to new items.':'The agent mediates communication between the human and the corpus.',n);
 if(existing){
  await icon(s,'Files',85,219,60,C.purple);txt(s,'Labeled corpus',164,213,350,44,31,C.purple,true);txt(s,'Existing labels + optional guideline',85,287,380,35,23,C.muted);
  await icon(s,'UserRoundCheck',88,340,36,C.green);txt(s,'Human reviewer',139,330,245,35,25,C.green,true);txt(s,'Confirm, revise or defer',139,366,270,32,22,C.muted);
  line(s,425,242,685,242,C.purple,true);txt(s,'Patterns in existing labels',429,207,250,32,21,C.purple);
  line(s,685,350,425,350,C.green,true);txt(s,'Candidate rules + issues',439,310,250,32,21,C.green);
  line(s,425,394,715,394,C.green,true);txt(s,'Review decisions',447,363,245,28,21,C.green);
 }else{
  await icon(s,'UserRound',92,229,66,C.green);txt(s,'Human',179,232,230,48,34,C.green,true);txt(s,'A rough conception',92,312,300,40,25,C.muted);
  line(s,685,242,415,242,C.green,true);txt(s,'Proposed rules + contrasts',425,203,260,34,21,C.green);
  line(s,415,322,685,322,C.green,true);txt(s,'Judgments + exceptions',437,338,250,35,21,C.green);
 }
 await icon(s,'Bot',714,223,66,C.amber);txt(s,'Agent',802,228,185,47,34,C.amber,true);txt(s,existing?'Rules + issue groups':'Organizes the dialogue',701,298,285,38,23,C.muted);
 await icon(s,'LibraryBig',1250,223,60,C.purple);txt(s,'Large unlabeled\ncorpus',1320,212,260,80,28,C.purple,true);txt(s,'New items and edge cases',1250,312,300,36,23,C.muted);
 line(s,1230,242,1000,242,C.purple,true);txt(s,'Examples + boundaries',998,202,250,34,21,C.purple);
 line(s,1000,322,1230,322,C.purple,true);txt(s,'Inspect cases + test rules',991,343,260,32,21,C.purple);
 txt(s,'Accepted outputs',65,462,240,40,24,C.muted,true);
 route(s,[[845,365],[845,412],[530,412],[530,450]],C.amber);
 route(s,[[845,412],[1075,412],[1075,450]],C.amber);
 txt(s,'Two linked outputs',872,374,260,29,22,C.amber);
 box(s,325,452,420,132,'#F0F8F5','#A4C9BC');box(s,880,452,420,132,'#F0F8F5','#A4C9BC');
 await icon(s,'FileCheck2',345,476,55,C.green);txt(s,'Structured, adaptive\nguideline',420,466,315,66,28,C.green,true);txt(s,'Human-approved rules + exceptions',345,544,390,30,22,C.muted);
 await icon(s,'Files',900,477,53,C.green);txt(s,'Labeled data',972,476,310,41,30,C.green,true);txt(s,'Human-approved + guideline-consistent',900,537,385,40,21,C.muted);
 line(s,762,516,862,516,C.green,true,true);txt(s,'Align',780,477,100,30,22,C.green);
 route(s,[[530,585],[530,617],[700,617],[700,664]],C.blue);
 route(s,[[1090,585],[1090,634],[880,634],[880,664]],C.blue);
 txt(s,'Execute at scale',65,670,240,40,24,C.muted,true);
 await icon(s,'Cpu',575,681,59,C.blue);txt(s,'Executor models',655,682,365,45,32,C.blue,true);txt(s,'Test across models using approved labels',575,746,470,60,23,C.muted);
 line(s,1018,712,1090,712,C.blue,true);
 await icon(s,'Files',1120,681,57,C.purple);txt(s,'Large-scale labeling',1193,678,370,45,30,C.purple,true);txt(s,'Apply the guideline + audit batches',1120,744,410,55,23,C.muted);
 route(s,[[1495,354],[1495,650],[1395,650],[1395,673]],C.purple);txt(s,'Supply items',1328,604,155,32,22,C.purple);
 route(s,[[560,716],[282,716],[282,518],[317,518]],C.blue);
 txt(s,'Refine wording,\npreserve meaning',290,740,260,66,22,C.blue);
 txt(s,'Human review or an explicit audit policy governs acceptance.',420,842,1030,32,22,C.muted);
}

// 4: Human effort, labeling quality, and useful conflict detection.
{
 const s=slide('Evaluation 1: effort and labeling quality','Compare workflows on matched tasks with independent quality assessment.',4);
 const arms=[['UserRound','Manual labeling','Item-by-item judgments',240],['FileText','Human-authored guideline','One fixed executor',390],['Bot','Agent-mediated workflow','Rules, cases and human judgments',540]];
 for(const [ic,title,desc,y]of arms){await icon(s,ic,80,y,54,title.startsWith('Agent')?C.amber:C.green);txt(s,title,155,y-2,410,43,29,C.ink,true);txt(s,desc,155,y+51,425,40,24,C.muted);line(s,585,y+26,640,y+26,C.line);}
 line(s,640,266,640,566,C.line);line(s,640,416,702,416,C.blue,true);
 box(s,715,274,380,285,'#F0F6FC','#A6C4DD');await icon(s,'ClipboardCheck',743,302,55,C.blue);txt(s,'Independent review',815,305,265,80,30,C.blue,true);
 txt(s,'Held-out items\nBlinded adjudication\nGuideline consistency',744,411,330,130,27,C.ink);
 line(s,1100,416,1150,416,C.blue,true);
 txt(s,'Measure',1170,251,340,50,33,C.ink,true);
 txt(s,'Human time + burden\nLabel quality + coverage\nCorrection effort\nUseful conflict flags',1170,332,365,240,27,C.ink);
 txt(s,'Goal: less effort at comparable quality',90,720,1430,54,36,C.ink,true);
 txt(s,'Counterbalance task order. Evaluate natural conflicts separately from planted errors.',90,795,1390,48,24,C.muted);
 s.speakerNotes.text+='\nThe human study should randomize or counterbalance task order, match task difficulty and avoid exposing the same test cases during guideline development. Blinded independent reviewers assess the accepted labels. For subjective labels, specify whose standard is assessed and report unresolved cases. Audit utility includes precision and review effort; planted errors and natural disagreements are distinct evaluation targets.';
}

// 5: Meaning held fixed; weights fixed; test boundary explicit.
{
 const s=slide('Evaluation 2: guideline portability and scale','Can cheaper models follow the same human-approved standard?',5);
 await node(s,'PencilLine','Develop','Initial vs. single-model\nvs. multi-model refinement',80,230,410,C.amber);
 await node(s,'LockKeyhole','Freeze','Lock the guideline\nand quality thresholds',605,230,350,C.green);
 await node(s,'Cpu','Test','Small, mid-range and\nstrong executor models',1080,230,430,C.blue);
 line(s,510,267,580,267,C.line,true);line(s,975,267,1050,267,C.line,true);
 txt(s,'Approved meaning stays fixed',80,510,440,34,23,C.amber);txt(s,'Keep test cases unseen',605,510,370,34,23,C.green);txt(s,'Fixed weights; fresh contexts',1080,510,440,34,23,C.blue);
 txt(s,'Measure',85,604,600,45,32,C.ink,true);txt(s,'Quality and coverage by model\nAbstentions and cost per accepted item\nGuideline development + human review cost',85,670,700,128,26,C.ink);
 txt(s,'Success criteria',890,604,620,45,32,C.ink,true);txt(s,'Raise the weakest model’s quality\nPreserve strong-model performance\nLower cost at acceptable quality',890,670,620,128,26,C.ink);
 txt(s,'A smaller model gap alone is not enough. Include unseen models where feasible.',85,838,1400,35,24,C.muted);
}

await fs.mkdir(OUT,{recursive:true});
for(const [i,s]of P.slides.items.entries()){
 const png=await P.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(OUT,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(OUT,'candidate.pptx');
await(await PresentationFile.exportPptx(P)).save(candidate);
const reimport=await PresentationFile.importPptx(await FileBlob.load(candidate));
if(reimport.slides.items.length!==5)throw Error('Expected 5 slides');
for(const o of objects)if(o.x<0||o.y<0||o.x+o.w>1600||o.y+o.h>900)throw Error('Out of bounds '+o.text);
await fs.writeFile(path.join(OUT,'source-layout.json'),JSON.stringify(objects,null,2));
await fs.writeFile(path.join(OUT,'validation.json'),JSON.stringify({slides:5,roundTripImport:'passed',sourceGeometry:'passed',style:'IRB reference: Helvetica Neue, Lucide icons, native editable shapes',content:'Proposed method and evaluation; no observed results',hashes:'Not used, per repository instructions'},null,2));
console.log(candidate);
