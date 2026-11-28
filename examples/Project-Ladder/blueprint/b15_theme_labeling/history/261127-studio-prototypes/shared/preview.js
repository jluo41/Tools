/* Studio Effect only. All actions stay in memory; no fetch, form submission or storage writes. */
'use strict';
const model = JSON.parse(document.getElementById('preview-data').textContent);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state = {job:model.jobs[0].id, view:'main', section:'Jobs', case:0, answers:{}, generated:{}, validated:{}, approved:{}, queued:new Set(), recipe:{}};
const remembered = new Map();
const job = () => model.jobs.find(j => j.id === state.job);
const marks = {done:'✓',waiting:'🙋',ready:'',planned:'⬜',running:'🏃',blocked:'⬜'};
const mark = (s, text='') => `<span class="mark ${s==='waiting'?'wait':s==='done'?'done':''}" title="${esc(text||s)}" aria-label="${esc(text||s)}">${marks[s]||''}</span>`;
const button = (label, key, value, on, title='') => `<button type="button" data-${key}="${esc(value)}" aria-pressed="${on}" title="${esc(title||label)}">${esc(label)}</button>`;
const table = (head, rows) => `<div class="data-scroll"><table class="data"><thead><tr>${head.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>`<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
const facts = rows => `<dl class="kv">${rows.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
const action = (name, id, disabled=false, primary=false) => `<button class="action${primary?' primary':''}" type="button" data-action="${esc(id)}"${disabled?' disabled':''}>${esc(name)}</button>`;
const fold = (name, body, s='', output='') => `<details class="fold"><summary><span class="fold-title">${esc(name)}</span>${output?`<span class="fold-output">${esc(output)}</span>`:''}${mark(s)}</summary><div class="fold-content">${body}</div></details>`;
const band = (name, content, dot=false) => `<section><h2 class="band-title">${esc(name)}${dot?'<button class="open-dot" data-action="open-view" title="Open this design view" aria-label="Open this design view">•</button>':''}</h2>${content}</section>`;
function taskState(t){
 if(t.action==='decisions' && state.generated[state.job]) return 'done';
 if(t.action==='evaluation' && state.generated[state.job]) return state.validated[state.job]?'done':'planned';
 if(t.action==='recipe' && state.recipe[state.job]) return 'ready';
 if(t.action==='queue' && state.queued.has(state.job)) return 'running';
 return t.state;
}
function runRows(t){
 const rows=[...t.runs];
 if(t.action==='decisions'&&state.generated[state.job])rows.push(['r02','Generate guideline-v3 · preview','done']);
 if(t.action==='evaluation'&&state.validated[state.job])rows.push(['r03','Validate guideline-v3 · synthetic fixture','done']);
 return rows.map(r=>`<div class="run-row"><span>${esc(r[0])}</span><span>${esc(r[1])}</span>${mark(t.action==='queue'&&state.queued.has(state.job)&&r[2]==='planned'?'running':r[2])}</div>`).join('');
}
function taskOutput(t){
 if(t.action==='decisions'&&state.generated[state.job])return 'guideline-v3 draft';
 if(t.action==='evaluation'&&state.generated[state.job])return state.validated[state.job]?'guideline-v3 checks':'';
 if(t.action==='recipe'&&state.recipe[state.job])return '';
 return t.output;
}
const reviewed = () => model.cases?.every((_,i)=>state.answers[state.job+':'+i]);
const revision = () => table(['Case','Interpretation'],model.cases.map((c,i)=>[c.id,state.answers[state.job+':'+i]]));
const revisionEvidence = () => facts([['Candidate','guideline-v3 · '+job().name],['Meaning','Current case judgments'],['Checks','Each case has a rule; uncertainty is retained'],['Evidence','Synthetic validation fixture']]);
function packageForJob(){
 if(model.kind==='guideline'&&state.approved[state.job]) return {title:'Response safety · guideline-v3',facts:[['Meaning','Reviewed boundary judgments'],['Expression',job().name],['Validation','Synthetic validation fixture'],['Signature','Design reviewer · preview confirmation'],['Version','guideline-v3'],['Existing scale binding','guideline-v2']]};
 return job().delivery;
}
function taskBody(t, compact=false){
 let body = facts(t.facts||[]) + (t.columns?table(t.columns,t.rows):'');
 if(t.action==='decisions'&&state.generated[state.job]) body=revision();
 if(t.action==='evaluation'&&state.generated[state.job]) body=state.validated[state.job]?revisionEvidence():facts([['Candidate','guideline-v3'],['Required action','Validate the current revision in Studio']]);
 if(!compact) body += t.runs.length?band('⚙️ Runs',runRows(t)):'';
 else body += runRows(t);
 if(t.action==='recipe') body += `<div class="actions">${action('Review recipe','studio',false,true)}</div>`;
 if(t.action==='decisions') body += `<div class="actions">${action('Review cases','studio',false,true)}</div>`;
 if(t.action==='queue') body += queueAction();
 if(t.action==='qualify' && !job().qualified) body += `<p class="reason">Executor qualification is required before Run all.</p>`;
 return body;
}
function queueAction(){
 const j=job(), enabled=j.signed&&j.qualified&&!state.queued.has(j.id)&&!j.complete;
 const reason=!j.signed?'Choose a signed guideline.':!j.qualified?'Qualify this executor against the held-out set.':'';
 return `<div class="actions">${action('Run all','queue',!enabled,true)}</div>${reason?`<p class="reason">${reason}</p>`:''}`;
}
function jobMain(){
 const j=job(), pkg=packageForJob();
 const inputs=fold('Inputs',facts(j.inputs)+(model.kind==='scale'?queueAction():''));
 const tasks=j.tasks.map(t=>fold(`${t.id} · ${t.name}`,taskBody(t,true),taskState(t),taskOutput(t))).join('');
 const waiting=j.tasks.filter(t=>taskState(t)==='waiting'||taskState(t)==='blocked');
 let body=band('📊 Plan + Results',inputs+tasks,true);
 if(waiting.length) body+=band('🔎 Findings',waiting.map(t=>fold(t.issue||t.name,`<p>${esc(t.reason||'Review the evidence and record a decision in Studio.')}</p><div class="actions">${action(t.state==='blocked'?'Inspect task':'Review','finding:'+t.id,false,true)}</div>`,t.state)).join(''));
 if(pkg) body+=band('📦 Delivery',fold(pkg.title,facts(pkg.facts)+`<div class="actions">${action('Inspect package','package')}</div>`,'done'));
 return body;
}
function selectedTask(){const t=job().tasks.find(t=>t.id===state.view);return band('📊 Plan + Results',fold(t.name,taskBody(t),taskState(t)),true);}
function studio(){
 if(model.kind==='items'){
  const r=job().recipe, accepted=r.accepted||state.recipe[state.job];
  const content=table(['Source','Unit','Context'],[['conversation-01',r.unit,r.context],['conversation-02',r.unit,r.context]])
    +facts([['Boundary',r.boundary],['Provenance','Conversation ID, source turns and source snapshot'],['Label fields','Excluded from model-visible context']])
    +`<div class="actions">${action('Accept recipe','accept-recipe',accepted,true)}</div>`;
  return band('🎨 Item boundaries',fold(job().name,content,accepted?'done':'waiting'));
 }
 if(model.kind==='scale') return band('🎨 Audit review',fold('Ambiguous predictions',table(['Item','Model label','Review'],[['conversation-02/reply-01','Uncertain','Needs the guideline owner']])+`<p>Semantic questions return to Guideline Generation. Existing labels retain their original guideline version.</p><div class="actions">${action('Prepare feedback','feedback',false,true)}</div>`,'waiting'));
 const cases=model.cases, c=cases[state.case], key=state.job+':'+state.case;
 const choices=['Safe','Unsafe','Needs context'];
 const all=reviewed();
 const approved=state.approved[state.job];
 const content=`<div class="side-tabs"><nav class="side-list" aria-label="Review cases">${cases.map((c,i)=>button(c.id,'case',i,state.case===i)).join('')}</nav><article><blockquote class="context">${esc(c.context)}</blockquote><p class="case-text">${esc(c.text)}</p><div class="choices">${choices.map(v=>`<label><input type="radio" name="judgment" value="${esc(v)}" ${state.answers[key]===v?'checked':''} ${approved?'disabled':''}>${esc(v)}</label>`).join('')}</div><p class="case-rule">${esc(c.rule)}</p></article></div><div class="actions">${action('Generate revision','generate',!all||!!state.generated[state.job],true)}</div>`;
 const candidate=state.generated[state.job]?band('📋 Revision',fold(job().name,revision()+(state.validated[state.job]?revisionEvidence():`<div class="actions">${action('Validate revision','validate',false,true)}</div>`),state.validated[state.job]?'done':'')):'';
 const release=facts([['Candidate','guideline-v3'],['Previous release','guideline-v2'],['Scope','Response safety on conversational replies']])+`<div class="actions">${action('Confirm guideline','approve',!state.validated[state.job]||!!approved,true)}</div>`;
 return band('🎨 Human–AI review',fold('Boundary cases',content,all?'done':'waiting'))+candidate+band('📦 Guideline release',fold('Response safety',release,approved?'done':'waiting'));
}
function delivery(){
 const pkg=packageForJob();
 return band('📦 Delivery',pkg?fold(pkg.title,facts(pkg.facts)+`<div class="actions">${action('Inspect package','package')}</div>`,'done'):
   fold('Required evidence',facts(model.releaseRequirements),'',model.releaseName));
}
function draw(){
 const j=job();document.getElementById('section-name').textContent=state.section;
 document.querySelector('#navigation').hidden=state.section!=='Jobs';
 const topics=[...new Set(model.jobs.map(j=>j.topic))];
 document.querySelector('[data-row="job-topic"]').innerHTML=topics.map(v=>button(v,'topic',v,j.topic===v)).join('');
 document.querySelector('[data-row="job"]').innerHTML=model.jobs.filter(x=>x.topic===j.topic).map(x=>button(`${x.id} · ${x.name}`,'job',x.id,j.id===x.id,x.goal)).join('');
 const groups=[...new Set(j.tasks.map(t=>t.group))];
 const selected=j.tasks.find(t=>t.id===state.view);
 document.querySelector('[data-row="task-topic"]').innerHTML=button('Main','view','main',state.view==='main')+groups.map(g=>button(g,'taskgroup',g,selected?.group===g)).join('');
 const row=document.querySelector('[data-row="task"]');row.hidden=!selected;
 row.innerHTML=selected?j.tasks.filter(t=>t.group===selected.group).map(t=>button(`${t.id} · ${t.name}`,'view',t.id,t.id===state.view)).join(''):'';
 document.getElementById('body').innerHTML=state.section==='Studio'?studio():state.section==='Delivery'?delivery():state.view==='main'?jobMain():selectedTask();
 const waits=j.tasks.filter(t=>['waiting','blocked'].includes(taskState(t)));
 if(model.kind==='guideline'&&!state.approved[state.job]&&!waits.length) waits.push({});
 const tray=document.getElementById('wait-tray');tray.hidden=!waits.length;tray.textContent='🙋 '+waits.length;
 document.title=model.name+' · '+j.name+' · '+state.section;
 const q=new URLSearchParams({job:state.job,view:state.view,section:state.section});history.replaceState(null,'',location.pathname+'?'+q);
}
function dialog(title,body){document.getElementById('dialog-title').textContent=title;document.getElementById('dialog-body').innerHTML=body;document.getElementById('dialog').showModal();}
let toastTimer;
function notify(text){const n=document.getElementById('toast');n.textContent=text;n.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>n.hidden=true,5000);}
function keepFolds(){const opened=[...document.querySelectorAll('details[open]')].map(d=>d.querySelector('.fold-title').textContent);draw();document.querySelectorAll('details').forEach(d=>d.open=opened.includes(d.querySelector('.fold-title').textContent));}
function act(id){
 if(id==='open-view'){window.open(location.href,'_blank','noopener');return;}
 if(id==='about'){dialog('Design preview','<p>All examples are synthetic. Actions change this preview only; they do not sign a real guideline, start a worker or write files.</p>');return;}
 if(id==='studio'){document.getElementById('dialog').close();state.section='Studio';draw();return;}
 if(id==='accept-recipe'){state.recipe[state.job]=true;keepFolds();notify('Recipe accepted in this preview. Build items can now run.');return;}
 if(id==='generate'){if(!reviewed())return;state.generated[state.job]=true;keepFolds();notify('Preview revision prepared. Inspect it before validation.');return;}
 if(id==='validate'){if(!state.generated[state.job])return;state.validated[state.job]=true;keepFolds();notify('Synthetic validation evidence attached to this revision.');return;}
 if(id==='approve'){
  if(!state.validated[state.job]) return;
  state.approved[state.job]=true;keepFolds();notify('Preview confirmation saved. Existing scale jobs still reference guideline-v2.');return;
 }
 if(id==='queue'){
  const j=job();if(!j.signed||!j.qualified||j.complete||state.queued.has(j.id))return;
  state.queued.add(j.id);draw();notify('Preview queued. Completed batches are kept; no worker was started.');return;
 }
 if(id==='feedback'){dialog('Guideline feedback',facts([['Guideline','guideline-v2'],['Item','conversation-02/reply-01'],['Reason','Context changes the interpretation']])+'<p>This proposal routes evidence back to Guideline Generation. The current release stays immutable.</p>');return;}
 if(id==='package'){const pkg=packageForJob();dialog(pkg.title,facts(pkg.facts));return;}
 if(id==='waits'){dialog('Review',model.kind==='guideline'?`<p>Review the current revision and its validation evidence.</p>${action('Review guideline','studio')}`:job().tasks.filter(t=>['waiting','blocked'].includes(taskState(t))).map(t=>`<p>${esc(t.issue||t.name)}</p>${action('Inspect','finding:'+t.id)}`).join(''));return;}
 if(id.startsWith('finding:')){document.getElementById('dialog').close();const t=job().tasks.find(t=>t.id===id.slice(8));state.section=t.state==='blocked'?'Jobs':'Studio';state.view=t.id;draw();}
}
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b||b.disabled)return;
 if(b.dataset.action){act(b.dataset.action);return;}
 if(b.dataset.section){state.section=b.dataset.section;document.getElementById('sections').hidePopover();}
 if(b.dataset.topic){state.job=model.jobs.find(j=>j.topic===b.dataset.topic).id;state.view='main';}
 if(b.dataset.job){state.job=b.dataset.job;state.view='main';}
 if(b.dataset.taskgroup){state.view=remembered.get(state.job+':'+b.dataset.taskgroup)||job().tasks.find(t=>t.group===b.dataset.taskgroup).id;}
 if(b.dataset.view){state.view=b.dataset.view;if(state.view!=='main'){const t=job().tasks.find(t=>t.id===state.view);remembered.set(state.job+':'+t.group,t.id);}}
 if(b.dataset.case!==undefined){state.case=Number(b.dataset.case);keepFolds();return;}
 if(b.dataset.close!==undefined){document.getElementById('dialog').close();return;}
 if(b.dataset.job||b.dataset.topic||b.dataset.taskgroup||b.dataset.view||b.dataset.section)draw();
});
document.addEventListener('change',e=>{
 if(e.target.name!=='judgment')return;
 state.answers[state.job+':'+state.case]=e.target.value;
 state.generated[state.job]=false;state.validated[state.job]=false;keepFolds();
});
const initial=new URLSearchParams(location.search);
if(model.jobs.some(j=>j.id===initial.get('job')))state.job=initial.get('job');
if(job().tasks.some(t=>t.id===initial.get('view')))state.view=initial.get('view');
if(['Jobs','Studio','Delivery'].includes(initial.get('section')))state.section=initial.get('section');
draw();
