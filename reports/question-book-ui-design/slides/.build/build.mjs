import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
import sharp from 'sharp';
const require=createRequire(import.meta.url), icons=require('lucide');
const root=path.resolve('reports/question-book-ui-design/slides');
const build=path.join(root,'.build');
const C={bg:'#FAF9F5',ink:'#183C3B',muted:'#607574',blue:'#2563A6',teal:'#128879',amber:'#B87425',pale:'#E7F0EB',line:'#CCD9D3',white:'#FFFFFF'};
const font='Arial Unicode MS';
const p=Presentation.create({slideSize:{width:1280,height:720}});
const source='内容来源：本次 Question Book 设计讨论及 ../DESIGN.md。视图与交互为设计提案。图标：Lucide v1.8.0，ISC License，https://lucide.dev。';
function box(s,x,y,w,h,fill=C.pale,stroke='none',round=18){return s.shapes.add({geometry:'roundRect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:stroke==='none'?0:2},borderRadius:round});}
function txt(s,text,x,y,w,h,size=26,color=C.ink,bold=false,align='left'){let a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=text;a.text.style={typeface:font,fontSize:size,color,bold,alignment:align,verticalAlignment:'middle',insets:0};return a;}
function arrow(s,x,y,w,color=C.teal){return s.shapes.add({geometry:'connector',position:{left:x,top:y,width:w,height:0},line:{fill:color,width:3},tail:{type:'triangle',width:'med',length:'med'}});}
function link(s,a,b,from='right',to='left',color=C.teal){return s.shapes.connect(a,b,{kind:'elbow',fromSide:from,toSide:to,line:{fill:color,width:2.5},tail:{type:'triangle'}});}
async function icon(s,name,x,y,size=76,color=C.teal){const data=icons[name];if(!data)throw Error(name);const body=data.map(([tag,attrs])=>`<${tag} ${Object.entries(attrs).map(([k,v])=>`${k}="${v}"`).join(' ')}/>`).join('');const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;const buf=await sharp(Buffer.from(svg)).png().toBuffer();s.images.add({blob:buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength),contentType:'image/png',position:{left:x,top:y,width:size,height:size},alt:name});}
function slide(title,sub=''){const s=p.slides.add();s.background.fill=C.bg;txt(s,title,64,40,1152,72,44,C.ink,true);if(sub)txt(s,sub,66,118,1140,44,23,C.muted);txt(s,String(p.slides.items.length).padStart(2,'0'),1160,665,54,24,16,C.muted,false,'right');s.speakerNotes.text=source;return s;}
function note(s,t){s.speakerNotes.text=source+'\n'+t;}
// 1
{
let s=slide('');txt(s,'Question Book',70,115,770,95,68,C.ink,true);txt(s,'问题集如何持续演进',74,222,800,80,48,C.ink,true);txt(s,'层级 · 视图 · 版本 · 发现',76,332,820,45,29,C.muted);await icon(s,'BookOpen',940,135,190);
const items=[['LibraryBig','整本问题集'],['Layers','一个版本'],['FileQuestionMark','一个问题']];
for(let i=0;i<3;i++){let x=80+i*405;await icon(s,items[i][0],x,490,60);txt(s,items[i][1],x+80,488,205,70,29,C.ink,true);if(i<2)arrow(s,x+290,524,70);}
txt(s,'Question Book UI 设计提案',76,650,800,32,20,C.muted);
}
// 2
{
let s=slide('三个层级，三个工作范围','Block 管整本书，Job 制作一版，Task 准备一个问题');
const levels=[['LibraryBig','Block','问题体系','目标、问题目录与版本演进'],['Layers','Job','问题集的一个版本','升级依据、计划结果与评审'],['FileQuestionMark','Task','本版中的一个问题','问题定义、证据需求与回答方法']];
for(let i=0;i<3;i++){const x=70+i*405;await icon(s,levels[i][0],x+120,210,100,i===1?C.blue:C.teal);txt(s,levels[i][1],x,330,340,45,29,C.blue,true,'center');txt(s,levels[i][2],x,385,340,52,34,C.ink,true,'center');txt(s,levels[i][3],x-5,463,360,86,25,C.muted,false,'center');if(i<2)arrow(s,x+340,263,62);}
}
// 3
{
let s=slide('每一层，都有不同的观察角度','View 改变看什么，层级决定看多大范围');
const rows=[['BookOpen','Block','概览','问题目录','改进想法','计划与结果','发现'],['Layers','Job','版本依据','本版问题','','计划与结果','发现'],['FileQuestionMark','Task','问题定义','证据与方法','','计划与结果','发现']];
for(let i=0;i<3;i++){let y=208+i*130;await icon(s,rows[i][0],66,y+8,54);txt(s,rows[i][1],140,y+8,120,52,28,C.ink,true);for(let j=2;j<7;j++){if(!rows[i][j])continue;let x=290+(j-2)*183;box(s,x,y,165,76,j>=5?C.pale:'#EEEFEA');txt(s,rows[i][j],x+8,y+8,149,60,24,j>=5?C.teal:C.ink,true,'center');}}
txt(s,'同一份内容，用目录、进度、证据或发现的角度查看',290,610,900,42,24,C.muted);
note(s,'视图名称为建议结构，并非宣称服务器已全部实现。Block 的版本历史纳入计划与结果视图。');
}
//4
{
let s=slide('一个版本，先说清为什么要改','动机与证据确定目标，目标再落到具体问题');
const top=[['Search','遇到了什么','上一版留下的问题'],['Files','依据是什么','数据表现、审查或文献'],['Target','这版要改什么','目标、范围与完成标准']];let nodes=[];
for(let i=0;i<3;i++){let x=80+i*405;await icon(s,top[i][0],x+90,196,84);txt(s,top[i][1],x,298,300,45,31,C.ink,true,'center');txt(s,top[i][2],x-5,354,320,50,24,C.muted,false,'center');nodes.push(box(s,x+135,425,2,2,'none'));}
const center=box(s,300,490,680,115,C.pale);txt(s,'计划 + 结果',330,506,620,47,34,C.teal,true,'center');txt(s,'每项改变都有对应 Task、产出与状态',330,555,620,34,24,C.ink,false,'center');for(const n of nodes)link(s,n,center,'bottom','top');
}
//5
{
let s=slide('Plan + Results 放在同一项工作里','展开一个计划，就能同时看到预期、实际结果和下一步');
box(s,70,195,1140,406,C.white,C.line,16);txt(s,'新增 K02：比较前后半段的差异',102,220,850,48,33,C.ink,true);txt(s,'示例：进行中',970,228,210,32,23,C.amber,true);
box(s,102,285,490,220,'#F0F3ED');box(s,620,285,555,220,'#EAF2EF');await icon(s,'ClipboardList',122,304,43);await icon(s,'FileCheck2',640,304,43);
txt(s,'计划',182,301,360,48,28,C.ink,true);txt(s,'准备问题定义与 E1–E4 证据需求\n完成标准：方法完整，审查通过',122,366,450,112,25,C.ink);
txt(s,'结果',700,301,400,48,28,C.teal,true);txt(s,'已有：问题草稿与证据计划\n待完成：方法审查与脚本验证',640,366,510,112,25,C.ink);
txt(s,'下一步',102,529,130,43,25,C.amber,true);txt(s,'补齐 E3 的计算方法，再提交审查',246,529,870,43,25,C.ink);
note(s,'展示状态为设计样例，不表示真实问题已经通过审查。这里的结果是问题与方法的准备产物，不是对数据的分析结论。');
}
//6
{
let s=slide('Results 是产出，Findings 是认识','一条发现可以由多个结果共同支撑');
const a=box(s,75,213,340,120,C.pale);await icon(s,'FileText',100,240,55);txt(s,'问题定义',181,247,215,46,30,C.ink,true);
const b=box(s,75,395,340,120,C.pale);await icon(s,'ListChecks',100,423,55);txt(s,'方法审查',181,431,215,46,30,C.ink,true);
const c=box(s,565,257,620,235,'#EAF0F6');await icon(s,'Lightbulb',594,287,66,C.blue);txt(s,'Finding',691,290,450,50,34,C.blue,true);txt(s,'描述每日变化，仍不足以回答\n组间差异是否随时间变化',594,366,560,93,29,C.ink);
link(s,a,c);link(s,b,c);txt(s,'产出',85,555,320,45,27,C.muted,false,'center');txt(s,'发现保留依据，并说明对下一步的影响',565,555,620,45,25,C.muted,false,'center');note(s,'Finding 为演示性方法认识；不能把准备工作的结果冒充实证研究结论。');
}
//7
{
let s=slide('同一条 Finding，在多层查看','记录只存一份，上层通过引用显示摘要和详情');
const src=box(s,70,270,360,176,C.ink);await icon(s,'FileSymlink',101,298,65,'#FFFFFF');txt(s,'F01',195,292,200,60,36,'#FFFFFF',true);txt(s,'归属 Task K02',101,381,300,40,25,'#FFFFFF');
const destinations=[['FileQuestionMark','Task','看具体依据'],['Layers','Job','看本版认识'],['LibraryBig','Block','看跨版本积累']];
for(let i=0;i<3;i++){const y=190+i*140;const b=box(s,760,y,440,108,C.pale);await icon(s,destinations[i][0],783,y+24,58);txt(s,destinations[i][1],864,y+12,290,38,28,C.teal,true);txt(s,destinations[i][2],864,y+53,290,36,24,C.ink);link(s,src,b);}
txt(s,'新的综合判断另记一条，并引用原发现',70,590,1100,48,27,C.muted);note(s,'引用按稳定身份去重，保留 owner、version 和 evidence_refs。更新同一实时源会反映在各视图，已经发布的历史版本保持固定。文件、产物也遵循同源引用原则。');
}
//8
{
let s=slide('版本升级是一轮有依据的工作','每个 Job 制作一版，评审确认后冻结，旧版历史保持不变');
const steps=[['Lightbulb','收集想法'],['Target','确定目标'],['Wrench','准备问题'],['ClipboardCheck','整版评审'],['ShieldCheck','确认发布']];
for(let i=0;i<5;i++){const x=65+i*247;await icon(s,steps[i][0],x+60,225,90,i===4?C.blue:C.teal);txt(s,steps[i][1],x,345,215,45,29,C.ink,true,'center');if(i<4)arrow(s,x+175,272,96);}
box(s,80,463,1120,149,C.pale);txt(s,'v1',105,490,100,45,32,C.ink,true);txt(s,'沿用问题保留原引用',240,485,470,45,27,C.ink);txt(s,'v2',105,550,100,45,32,C.blue,true);txt(s,'新增或修改的问题形成新定义',240,544,690,45,27,C.ink);await icon(s,'GitBranch',1042,500,73,C.blue);note(s,'新版本保留旧版本历史；未变 Task 不复制，真正修改的问题创建版本化定义。完成任务不自动等于发布，需整版审查和人确认。');
}
//9
{
let s=slide('Question Book 与 Insight 的交接','Question Book 定义问什么，Insight 用固定数据回答');
const q=box(s,62,222,300,218,C.pale);await icon(s,'BookMarked',170,242,72);txt(s,'Question Book',78,331,268,42,29,C.ink,true,'center');txt(s,'已发布的问题集版本',74,382,276,35,23,C.muted,false,'center');
const d=box(s,435,222,300,218,'#EAF0F6');await icon(s,'Database',545,242,72,C.blue);txt(s,'数据版本',451,331,268,42,29,C.ink,true,'center');txt(s,'固定的数据快照',447,382,276,35,23,C.muted,false,'center');
txt(s,'×',376,285,46,60,44,C.teal,true,'center');arrow(s,752,325,58);
const j=box(s,835,222,380,218,C.ink);await icon(s,'ChartNoAxesCombined',983,242,72,'#FFFFFF');txt(s,'Insight Job',857,331,336,42,31,'#FFFFFF',true,'center');txt(s,'Task 回答其中一个问题',849,382,350,35,23,'#FFFFFF',false,'center');
txt(s,'证据与发现',878,502,300,42,27,C.teal,true,'center');txt(s,'Design 制作与验证方案',750,565,460,48,29,C.ink,true,'center');txt(s,'缺口回到 Ideas，推动下一版',65,565,600,48,28,C.ink);note(s,'Insight Job 的身份是整个问题集版本乘以数据版本。Insight 的 Task 才是单个问题的回答。Design 环节为后续衔接，不把全部发现自动当成已确认的设计依据。');
}
//10
{
let s=slide('一个具体的升级例子','v1 的 I02 保留原引用，v2 新增 K02');
const ex=[['ChartLine','已有问题 I02','每天的结果怎样变化？'],['Search','发现缺口','组间差异也会随时间变吗？'],['FilePlus2','新增问题 K02','比较前后半段的组间差异']];
for(let i=0;i<3;i++){let x=65+i*412;await icon(s,ex[i][0],x+115,204,95,i===2?C.blue:C.teal);txt(s,ex[i][1],x,325,350,48,31,C.ink,true,'center');txt(s,ex[i][2],x-3,396,365,88,27,C.muted,false,'center');if(i<2)arrow(s,x+330,253,80);}
box(s,77,533,1126,93,C.pale);txt(s,'这版要交付：问题定义、证据需求、方法与审查记录',103,550,1075,58,29,C.teal,true,'center');note(s,'来源：blueprints/Project-Ladder/insight/InsightQuestionBook-Example/j02_question-v2_example-follow-up/release.yaml。例子采用中文摘要。此处只说明问题集的设计与准备，不预先判断数据分析结果。');
}
await fs.copyFile(require.resolve('lucide/LICENSE'),path.join(build,'LUCIDE-LICENSE.txt'));
await (await PresentationFile.exportPptx(p)).save(path.join(build,'candidate.pptx'));
for(let i=0;i<p.slides.items.length;i++){let png=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));}
console.log('Built '+p.slides.items.length+' slides');
