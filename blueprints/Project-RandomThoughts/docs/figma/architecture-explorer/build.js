// Editable Figma draft. Source: PRINCIPLE.md and the b10 c01 Chat record.
// Run through use_figma with figma-use and figma-generate-design.
const C = {
  paper: $fig.getVar('a4865545b526a5b3399a512667f40c9efe0c2fc4'),
  soft: $fig.getVar('34f184ba91e9ebb52258b767a603f5c2c97956a2'),
  ink: $fig.getVar('cf92d4e8c6a5a5ed82f024d47d11c21d5162ac3c'),
  muted: $fig.getVar('3184ed9d395b6588f571919557ce051337792211'),
  border: $fig.getVar('395870afebb3397e858358930ffdd69a5ec0f73d'),
};
const S = {
  small: $fig.getVar('15bb1c0f339146e931cf0dc15f89ed57dcbd907e'),
  medium: $fig.getVar('16bc6f84b6e7e20e4234ef79030ee580ec0f4505'),
  large: $fig.getVar('be3115966ea99eef888c9f25751b54695c7e88d2'),
  page: $fig.getVar('9acadea8b7c7c9884455b896e21c88b8bc62d6da'),
  radius: $fig.getVar('9e82491aff6fe809fe71856da5612db502221455'),
};
const semantic = $fig.varCollection({name:'Architecture / roles',modes:['Light']});
for (const [key,hex] of Object.entries({chat:'#6F4AB6',chatSoft:'#F1ECFA',skill:'#986422',job:'#2565A8',studio:'#2D7763',accent:'#246B60',accentSoft:'#EAF4F0'})) {
  C[key]=semantic.colorVar({name:key,values:{Light:hex},scopes:['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR']});
}
const bodyStyle=$fig.getStyle('cebee1b62ea594fa8f97b0b247fd163730736f2a');
const headingStyle=$fig.getStyle('dfbe5c8aedd892ba1aa0fe61bf528889ff866e4f');
const paint=color=>[{type:'SOLID',color}];
function txt(characters,size=14,color=C.ink,weight='Regular',width) {
  return $fig.text({name:characters.slice(0,64),characters,textStyle:size>=24?headingStyle:bodyStyle,
    fontName:{family:'Inter',style:weight},fontSize:size,lineHeight:{unit:'PERCENT',value:145},
    fills:paint(color),...(width?{width,textAutoResize:'HEIGHT'}:{})});
}
function mono(characters,width=680,color=C.ink,size=13) {
  return $fig.text({name:characters.slice(0,64),characters,fontName:{family:'IBM Plex Mono',style:'Regular'},
    fontSize:size,lineHeight:{unit:'PERCENT',value:170},width,textAutoResize:'HEIGHT',fills:paint(color)});
}
function v(name,width,children,opts={}) {
  return $fig.autoLayout({name,layoutMode:'VERTICAL',width,layoutSizingHorizontal:'FIXED',
    itemSpacing:S.medium,fills:[],...opts},children);
}
function h(name,children,opts={}) {
  return $fig.autoLayout({name,layoutMode:'HORIZONTAL',itemSpacing:S.medium,
    counterAxisAlignItems:'CENTER',fills:[],...opts},children);
}
function panel(name,width,children,opts={}) {
  return v(name,width,children,{paddingTop:S.large,paddingBottom:S.large,paddingLeft:S.large,
    paddingRight:S.large,cornerRadius:S.radius,fills:paint(C.paper),strokes:paint(C.border),strokeWeight:1,...opts});
}
function rule(width) { return $fig.rectangle({name:'Divider',width,height:1,fills:paint(C.border)}); }
const targets=[];
function button(label,to,primary=false) {
  const b=$fig.instance('cc8b558dc7d9684011b6b99ce8e6509399bc836b',{
    name:label,props:{'Label#2:0':label,Variant:primary?'Primary':'Neutral',Size:'Small',State:'Default'}});
  if(to)targets.push([b,to]);
  return b;
}
const navComp=$fig.component({name:'Explorer / Tree row',layoutMode:'HORIZONTAL',width:240,
  layoutSizingHorizontal:'FIXED',paddingTop:10,paddingBottom:10,paddingLeft:12,paddingRight:12,
  itemSpacing:12,cornerRadius:S.radius,fills:[]},[
  txt('C',12,C.chat,'Semi Bold').textProp('Kind'),
  txt('Chat',14,C.ink,'Medium').textProp('Label'),
]);
const detailComp=$fig.component({name:'Explorer / File detail',layoutMode:'VERTICAL',width:904,
  layoutSizingHorizontal:'FIXED',paddingTop:S.medium,paddingBottom:S.medium,itemSpacing:4,fills:[]},[
  txt('File',15,C.ink,'Medium',856).textProp('File'),
  txt('Purpose',13,C.muted,'Regular',856).textProp('Purpose'),
]);
const qaComp=$fig.component({name:'Chat / QA summary',layoutMode:'VERTICAL',width:836,
  layoutSizingHorizontal:'FIXED',paddingTop:S.medium,paddingBottom:S.medium,paddingLeft:S.medium,
  paddingRight:S.medium,itemSpacing:8,cornerRadius:S.radius,fills:paint(C.paper),strokes:paint(C.border)},[
  txt('q01',12,C.chat,'Semi Bold').textProp('Address'),
  txt('Question',15,C.ink,'Medium',804).textProp('Question'),
  txt('Output',14,C.muted,'Regular',804).textProp('Output'),
  mono('Changed files',804,C.accent,12).textProp('Files'),
]);
const dataComp=$fig.component({name:'Inspector / Property',layoutMode:'VERTICAL',width:232,
  layoutSizingHorizontal:'FIXED',itemSpacing:5,fills:[]},[
  txt('Property',11,C.muted,'Medium').textProp('Property'),
  txt('Value',14,C.ink,'Regular',232).textProp('Value'),
]);
const components=v('Local components',960,[navComp,detailComp,qaComp,dataComp],{x:3100,y:0,paddingTop:24});
function nav(label,kind=' ',selected=false,to) {
  const n=$fig.instance(navComp,{props:{Label:label,Kind:kind},
    ...(selected?{fills:paint(C.chatSoft)}:{})});
  if(to)targets.push([n,to]);
  return n;
}
function file(name,purpose,to) {
  const n=$fig.instance(detailComp,{props:{File:name,Purpose:purpose}});
  if(to)targets.push([n,to]);
  return n;
}
function property(name,value) { return $fig.instance(dataComp,{props:{Property:name,Value:value}}); }
function qa(address,question,output,files,to) {
  const n=$fig.instance(qaComp,{props:{Address:address,Question:question,Output:output,Files:files}});
  if(to)targets.push([n,to]);
  return n;
}
const names=['File System','UI System','Mapping'];
function shell(title,index,x,y,body) {
  const tabs=h('System views',names.map((label,i)=>{
    const n=$fig.instance('18aa207708b43593a2af7096b2dfd531553f3414',{
      name:label,props:{'Label#157:36':label,State:'Default',Active:i===index?'On':'Off'}});
    targets.push([n,['files','ui','mapping'][i]]);return n;
  }),{itemSpacing:24});
  return v(title,1440,[
    h('Masthead',[v('Project',1000,[txt('TOOLS  /  BLUEPRINTS',11,C.muted,'Medium'),
      txt('Project-RandomThoughts',26,C.ink,'Semi Bold')],{itemSpacing:4}),txt('Architecture',14,C.muted)],{width:1376,layoutSizingHorizontal:'FIXED',primaryAxisAlignItems:'SPACE_BETWEEN'}),
    tabs,rule(1376),body,
  ],{x,y,height:1000,layoutSizingVertical:'FIXED',paddingTop:28,paddingBottom:28,
    paddingLeft:S.page,paddingRight:S.page,itemSpacing:S.large,fills:paint(C.paper),clipsContent:true});
}
function folderSidebar() {
  return v('Folder tree',264,[
    txt('FILE SYSTEM',11,C.muted,'Semi Bold'),nav('Skill folders','S'),
    nav('haipipe-chat',' ',false,'skill'),rule(240),
    txt('Project-Ladder',15,C.ink,'Semi Bold'),nav('work/',' '),
    nav('b10_project_workbench','B'),
    v('Block children',240,[nav('jNN · Jobs','J'),nav('sNN · Studio','S'),
      nav('cNN · Chats','C',true,'session'),nav('c01 · Plugin principle',' ',true,'files')],{paddingLeft:12,itemSpacing:2}),
    rule(240),txt('A Block holds its work,\nits thinking, and its chats.',13,C.muted,'Regular',236),
  ],{itemSpacing:12});
}
const fileBody=v('Selected Chat folder',1072,[
  txt('Block  /  b10_project_workbench  /  c01',12,C.muted),
  h('Folder heading',[v('Chat title',720,[txt('Plugin principle and Chat',28,C.ink,'Semi Bold'),
    txt('c01_plugin_principle_and_chat/',13,C.chat)],{itemSpacing:6}),button('View in UI','ui',true)]),
  panel('Files',1072,[txt('Files',17,C.ink,'Semi Bold'),
    file('c01_plugin_principle_and_chat.md','The concise QA record, with links to changed files.','session'),
    rule(1024),
    h('File contract',[
      property('CONTAINS','Question · Output · Changed files'),property('WRITER','haipipe-chat / qa.py'),
      property('UPDATE POINT','Once an answer ends'),property('READ BY','Block → Sessions')],{itemSpacing:24}),
  ]),
  panel('File lifecycle',1072,[txt('How this file is produced',17,C.ink,'Semi Bold'),
    h('Creation and update',[
      v('Create',300,[txt('01  Open a Chat',14,C.chat,'Semi Bold'),mono('new_chat.py',280),txt('Creates cNN and its Markdown record.',14,C.muted,'Regular',296)]),
      txt('→',24,C.muted),
      v('Refresh',300,[txt('02  Finish an answer',14,C.chat,'Semi Bold'),mono('qa.py refresh',280),txt('Refreshes the QAs and changed-file links.',14,C.muted,'Regular',296)]),
      txt('→',24,C.muted),
      v('Read',300,[txt('03  Read the page',14,C.chat,'Semi Bold'),mono('frame_sessions.py',280),txt('Renders the record in Sessions.',14,C.muted,'Regular',296)]),
    ],{counterAxisAlignItems:'MIN',itemSpacing:18}),
  ]),
  h('Related views',[button('Inspect mapping','mapping'),button('Open QA record','session'),button('Inspect skill','skill')]),
],{itemSpacing:24});
const screens={};
screens.files=shell('01 · File System',0,0,0,h('Explorer',[folderSidebar(),fileBody],{counterAxisAlignItems:'MIN',itemSpacing:40}));
const uiOutline=v('Page outline',264,[txt('UI SYSTEM',11,C.muted,'Semi Bold'),
  nav('Project page','P'),nav('Theme view','V'),nav('Block page','B'),
  v('Page parts',240,[nav('Report',' '),nav('Studio',' '),nav('Sessions','C',true,'session'),nav('QA row',' ',true,'session')],{paddingLeft:12,itemSpacing:2}),
  rule(240),txt('Select a page part to see\nthe files behind it.',13,C.muted,'Regular',236),
]);
const blockPreview=panel('Block page preview',820,[txt('Project-Ladder  /  Work',12,C.muted),
  txt('Project workbench',28,C.ink,'Semi Bold'),
  txt('How should a plugin connect its folders, pages and sessions?',15,C.ink,'Regular',772),rule(772),
  txt('Sessions',18,C.ink,'Semi Bold'),
  v('Selected session',772,[txt('Plugin principle and Chat',17,C.chat,'Semi Bold'),
    txt('c01',12,C.muted),
    txt('q10  ·  What should chat tracing keep?',15,C.ink,'Semi Bold',724),
    txt('One QA contains the question, output and changed files.',14,C.muted,'Regular',724),
    mono('scripts/qa.py',700,C.accent),button('Open session','session')],
    {paddingTop:24,paddingBottom:24,paddingLeft:24,paddingRight:24,
      cornerRadius:S.radius,fills:paint(C.chatSoft),strokes:paint(C.chat),strokeWeight:1,itemSpacing:12}),
]);
const uiInspector=v('Source inspector',232,[txt('QA ELEMENT',11,C.chat,'Semi Bold'),
  property('SOURCE FOLDER','c01_plugin_principle_and_chat/'),
  property('SOURCE FILE','c01_plugin_principle_and_chat.md'),
  property('ELEMENT ADDRESS','c01.q10'),
  property('READER','frame_sessions.py'),rule(232),
  button('Show file','files'),button('Show mapping','mapping'),
]);
screens.ui=shell('02 · UI System',1,1540,0,h('UI inspector',[
  v('Outline',264,[...[]]),h('Rendered page and source',[blockPreview,uiInspector],{counterAxisAlignItems:'MIN',itemSpacing:24})
],{counterAxisAlignItems:'MIN',itemSpacing:32}));
// Replace the outline placeholder with the authored tree before flushing.
screens.ui.children[screens.ui.children.length-1].children[0].replace(uiOutline);
const mapNode=(title,label,detail,color,width=368)=>panel(title,width,[txt(label,11,color,'Semi Bold'),txt(title,21,C.ink,'Semi Bold',width-48),txt(detail,14,C.muted,'Regular',width-48)]);
const mappingBody=v('Mapping detail',1376,[
  h('Mapping heading',[v('Mapping title',1000,[txt('The same QA, across both systems',28,C.ink,'Semi Bold'),
    txt('c01.q10  ·  Plugin principle and Chat',13,C.chat)],{itemSpacing:6}),button('Open session','session')],{primaryAxisAlignItems:'SPACE_BETWEEN',width:1376,layoutSizingHorizontal:'FIXED'}),
  h('Read relationship',[
    mapNode('Chat record','FILE SYSTEM','c01_…/c01_….md\nQuestion, output, changed files',C.chat),
    v('Read arrow',112,[txt('READ',11,C.muted,'Semi Bold'),txt('→',28,C.chat)],{counterAxisAlignItems:'CENTER'}),
    mapNode('Sessions reader','MAPPING','frame_sessions.py\nReads the saved QA record',C.accent),
    v('Display arrow',112,[txt('RENDER',11,C.muted,'Semi Bold'),txt('→',28,C.chat)],{counterAxisAlignItems:'CENTER'}),
    mapNode('QA row','UI SYSTEM','Block → Sessions → c01.q10\nQuestion · Output · Changed files',C.chat),
  ],{itemSpacing:0}),
  panel('Write path',1376,[txt('When the next answer ends',18,C.ink,'Semi Bold'),
    h('Update sequence',[
      v('Answer',300,[txt('Answer completes',17,C.ink,'Medium'),txt('The completed turn is ready to keep.',14,C.muted,'Regular',280)]),txt('→',24,C.muted),
      v('Writer',300,[mono('qa.py refresh',280),txt('Updates the existing Chat record.',14,C.muted,'Regular',280)]),txt('→',24,C.muted),
      v('File',300,[mono('c01_….md',280,C.chat),txt('The concise QA and file links are saved.',14,C.muted,'Regular',280)]),txt('→',24,C.muted),
      v('UI',220,[txt('Sessions reads it',17,C.ink,'Medium'),txt('The next QA appears on the page.',14,C.muted,'Regular',220)]),
    ],{itemSpacing:16,counterAxisAlignItems:'MIN'}),
  ]),
  panel('Navigation loop',1376,[txt('Follow the work in either direction',18,C.ink,'Semi Bold'),
    h('Cross links',[button('QA → Changed file','files'),txt('→',20,C.muted),button('File → UI element','ui'),
      txt('→',20,C.muted),button('Element → Session','session')]),
    txt('The file owns the record. Each view reaches the same source.',14,C.muted),
  ]),
],{itemSpacing:28});
screens.mapping=shell('03 · Mapping',2,0,1100,mappingBody);
const sessionContent=v('Session detail',904,[txt('Block  /  Sessions  /  c01',12,C.muted),
  txt('Plugin principle and Chat',28,C.ink,'Semi Bold'),
  txt('Questions, outputs, and the files they changed.',14,C.muted),
  qa('c01.q09','Create haipipe-chat.','The skill was built, and this conversation was saved as a cNN record.',
    'new_chat.py  ·  chat-contract.md  ·  SKILL.md','files'),
  qa('c01.q10','What should chat tracing keep?','One QA keeps the question, output and changed files.',
    'scripts/qa.py','mapping'),
  qa('c01.q11','Update the Chat once, at the end of the answer.','Refresh after the answer ends; keep the record concise.',
    'Related: chat_hook.py','mapping'),
  h('Session navigation',[button('Show folder','files'),button('Show UI element','ui'),button('Inspect mapping','mapping')]),
],{itemSpacing:20});
const sessionInspector=panel('Chat ownership',424,[txt('Kept with its Block',21,C.ink,'Semi Bold'),
  mono('b10_project_workbench/\n  jNN_…/\n  sNN-…/\n  c01_plugin_principle_and_chat/',376,C.ink,12),
  rule(376),txt('Writer',12,C.muted),mono('haipipe-chat/scripts/qa.py',376),
  txt('The full native conversation stays with its chat provider. The Block keeps concise QAs.',14,C.muted,'Regular',376),
  button('Inspect skill','skill'),
]);
screens.session=shell('04 · Session detail',1,1540,1100,h('Session and source',[sessionContent,sessionInspector],{counterAxisAlignItems:'MIN',itemSpacing:48}));
const skillBody=v('Skill structure',1072,[txt('Skill folders  /  haipipe-chat',12,C.muted),
  txt('How a Chat record is made',28,C.ink,'Semi Bold'),
  panel('Skill files',1072,[file('SKILL.md','The entry point: when to use the skill and how.'),
    file('ref/chat-contract.md','The folder, QA and update contract.'),
    file('scripts/new_chat.py','Allocates a cNN folder and creates its record.'),
    file('scripts/qa.py','Refreshes concise QAs from a saved session.'),
    file('scripts/chat_hook.py','Connects the refresh to the end of an answer.'),
    file('tests/test_new_chat.py','Checks the folder and record behavior.')]),
  h('Skill navigation',[button('See generated file','files',true),button('Inspect mapping','mapping')]),
],{itemSpacing:24});
screens.skill=shell('05 · Skill structure',0,0,2200,h('Skill explorer',[folderSidebar(),skillBody],{counterAxisAlignItems:'MIN',itemSpacing:40}));
const annotation=v('Design notes — outside product screens',1440,[txt('Architecture explorer · draft',30,C.ink,'Semi Bold'),
  txt('Start with File System. Follow one real Chat through its files, rendered QA and read/write mapping.',18,C.muted,'Regular',1376),
  txt('The cNN location follows PRINCIPLE.md. These screens propose presentation and navigation; they do not implement a new storage service.',16,C.muted,'Regular',1376),
  txt('QA copy is shortened in English for the mockup. The source record preserves the original wording. Cross-Block references remain an open design question.',16,C.muted,'Regular',1376),
  txt('Typography: Inter from Simple Design System; IBM Plex Mono for paths. The running workbench uses a platform system-font stack.',14,C.muted,'Regular',1376),
],{x:1540,y:2200,paddingTop:32,paddingLeft:32,paddingRight:32,paddingBottom:32,fills:paint(C.soft)});
await $fig.done();
let linked=0;
for(const [node,key] of targets) {
  let top=node.node;
  while(top.parent && top.parent.type!=='PAGE') top=top.parent;
  if(top.id===screens[key].node.id) continue;
  await node.node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{
    type:'NODE',destinationId:screens[key].node.id,navigation:'NAVIGATE',transition:null,preserveScrollPosition:false}]}]);
  linked++;
}
const bounds=Object.fromEntries(Object.entries(screens).map(([key,n])=>[key,{id:n.node.id,name:n.node.name,width:n.node.width,height:n.node.height}]));
return {screens:bounds,components:components.node.id,notes:annotation.node.id,prototypeLinks:linked};
