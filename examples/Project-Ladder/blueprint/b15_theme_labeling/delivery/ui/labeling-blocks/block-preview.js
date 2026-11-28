(() => {
 'use strict';
 const root=document.getElementById('__BLOCK_ID__');
 const model=JSON.parse(root.querySelector('.lb-model').textContent);
 const first={block:model.blockId,job:model.jobs[0].id,task:'main',section:'Jobs',case:0,answers:{},generated:{},validated:{},approved:{},recipes:{},queued:{}};
 let state={...first}, remembered={};
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const job=()=>model.jobs.find(j=>j.id===state.job)||model.jobs[0];
 const marks={done:'✓',waiting:'🙋',ready:'',planned:'⬜',blocked:'⬜',running:'🏃'};
 const mark=s=>`<span class="lb-mark" data-mark="${esc(s)}" aria-label="${esc(s)}">${marks[s]||''}</span>`;
 const pick=(label,key,value,on)=>`<button type="button" data-${key}="${esc(value)}" aria-pressed="${!!on}">${esc(label)}</button>`;
 const action=(name,id,disabled=false)=>`<button type="button" class="lb-primary" data-action="${esc(id)}"${disabled?' disabled':''}>${esc(name)}</button>`;
 const facts=rows=>`<dl>${rows.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
 const table=(heads,rows)=>`<table><thead><tr>${heads.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>`<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
 const fold=(name,body,s='',output='')=>`<details><summary><span class="lb-label">${esc(name)}</span>${output?`<span class="lb-output">${esc(output)}</span>`:''}${mark(s)}</summary><div class="lb-fold">${body}</div></details>`;
 const band=(name,body)=>`<section><h2>${esc(name)}</h2>${body}</section>`;
 const reviewed=()=>model.cases?.every((_,i)=>state.answers[state.job+':'+i]);
 function notice(text){const p=root.querySelector('.lb-feedback');p.textContent=text;p.hidden=!text;}
 function taskState(t){
  if(t.action==='recipe'&&state.recipes[state.job])return 'ready';
  if(t.action==='decisions'&&state.generated[state.job])return 'done';
  if(t.action==='evaluation'&&state.generated[state.job])return state.validated[state.job]?'done':'planned';
  if(t.action==='queue'&&state.queued[state.job])return 'running';
  return t.state;
 }
 function revision(){return table(['Case','Interpretation','Proposed rule'],model.cases.map((c,i)=>{const label=state.answers[state.job+':'+i];return [c.id,label,c.rules[label]];}));}
 const evidence=()=>facts([['Candidate','guideline-v3 · '+job().name],['Basis','Current case judgments'],['Checks','Rule coverage and uncertainty handling'],['Evidence','Synthetic validation example']]);
 function delivered(){
  if(model.kind==='guideline'&&state.approved[state.job])return {title:'Response safety · guideline-v3',facts:[['Meaning','Reviewed boundary judgments'],['Expression',job().name],['Evidence','Synthetic validation example'],['Confirmation','Preview reviewer'],['Existing Scale binding','guideline-v2']]};
  return job().delivery;
 }
 function queue(){
  const j=job(),enabled=j.signed&&j.qualified&&!j.complete&&!state.queued[j.id];
  const reason=!j.signed?'Select a signed Guideline.':!j.qualified?'Qualify this executor before running batches.':'';
  return `<div class="lb-actions">${action('Run all','queue',!enabled)}</div>${reason?`<p class="lb-reason">${reason}</p>`:''}`;
 }
 function runs(t){
  const rows=[...t.runs];
  if(t.action==='decisions'&&state.generated[state.job])rows.push(['r02','Generate guideline-v3 · preview','done']);
  if(t.action==='evaluation'&&state.validated[state.job])rows.push(['r03','Validate guideline-v3 · synthetic example','done']);
  return rows.length?`<div class="lb-runs">${rows.map(r=>`<div class="lb-run"><span>${esc(r[1])}</span>${mark(t.action==='queue'&&state.queued[state.job]&&r[2]==='planned'?'running':r[2])}</div>`).join('')}</div>`:'';
 }
 function taskBody(t){
  let body=facts(t.facts||[])+(t.columns?table(t.columns,t.rows):'');
  if(t.action==='decisions'&&state.generated[state.job])body=revision();
  if(t.action==='evaluation'&&state.generated[state.job])body=state.validated[state.job]?evidence():facts([['Candidate','guideline-v3'],['Required action','Validate the current revision in Review']]);
  body+=runs(t);
  if(['recipe','decisions'].includes(t.action))body+=`<div class="lb-actions">${action(t.action==='recipe'?'Review recipe':'Review cases','review')}</div>`;
  if(t.action==='queue')body+=queue();
  return body;
 }
 function taskOutput(t){
  if(t.action==='recipe'&&state.recipes[state.job])return '';
  if(t.action==='evaluation'&&state.generated[state.job])return state.validated[state.job]?'guideline-v3 checks':'';
  return t.output;
 }
 function main(){
  const j=job(),pkg=delivered();
  let body=band('📊 Plan + Results',fold('Inputs',facts(j.inputs)) +j.tasks.map(t=>fold(t.name,taskBody(t),taskState(t),taskOutput(t))).join(''));
  const waits=j.tasks.filter(t=>['waiting','blocked'].includes(taskState(t)));
  if(waits.length)body+=band('🔎 Findings',waits.map(t=>fold(t.issue||t.name,`<p>${esc(t.reason)}</p><div class="lb-actions">${action('Review','finding:'+t.id)}</div>`,taskState(t))).join(''));
  if(pkg)body+=band('📦 Delivery',fold(pkg.title,facts(pkg.facts),'done'));
  return body;
 }
 function review(){
  if(model.kind==='items'){
   const r=job().recipe,accepted=r.accepted||state.recipes[state.job];
   return band('🎨 Item boundaries',fold(job().name,table(['Source','Unit','Context'],[['conversation-01',r.unit,r.context],['conversation-02',r.unit,r.context]])+facts([['Boundary',r.boundary],['Provenance','Conversation, source turns and snapshot'],['Label fields','Excluded from model-visible context']])+`<div class="lb-actions">${action('Accept recipe','recipe',accepted)}</div>`,accepted?'done':'waiting'));
  }
  if(model.kind==='scale')return band('🎨 Audit review',fold('Ambiguous predictions',table(['Item','Prediction','Review'],[['conversation-02/reply-01','Uncertain','Guideline meaning requires review']])+`<div class="lb-actions">${action('Prepare feedback','feedback')}</div>`,'waiting'));
  const c=model.cases[state.case],key=state.job+':'+state.case,approved=state.approved[state.job];
  const choices=['Safe','Unsafe','Needs context'];
  const content=`<div class="lb-case"><nav aria-label="Review cases">${model.cases.map((x,i)=>pick(x.id,'case',i,i===state.case)).join('')}</nav><article><blockquote>${esc(c.context)}</blockquote><p>${esc(c.text)}</p><div class="lb-choices">${choices.map(v=>`<label><input type="radio" name="${esc(model.blockId)}-judgment" value="${esc(v)}"${state.answers[key]===v?' checked':''}${approved?' disabled':''}>${esc(v)}</label>`).join('')}</div><p>${esc(c.rule)}</p></article></div><div class="lb-actions">${action('Generate revision','generate',!reviewed()||!!state.generated[state.job])}</div>`;
  const candidate=state.generated[state.job]?band('📋 Revision',fold(job().name,revision()+(state.validated[state.job]?evidence():`<div class="lb-actions">${action('Validate revision','validate')}</div>`),state.validated[state.job]?'done':'')):'';
  const release=facts([['Candidate','guideline-v3'],['Previous release','guideline-v2'],['Scope','Response safety on conversational replies']])+`<div class="lb-actions">${action('Confirm guideline','approve',!state.validated[state.job]||!!approved)}</div>`;
  return band('🎨 Human–AI review',fold('Boundary cases',content,reviewed()?'done':'waiting'))+candidate+band('📦 Guideline release',fold('Response safety',release,approved?'done':'waiting'));
 }
 function render(preserve=false){
  const open=preserve?[...root.querySelectorAll('details[open]')].map(d=>d.querySelector('.lb-label').textContent):[];
  const j=job(),t=j.tasks.find(t=>t.id===state.task);
  root.querySelector('.lb-navigation').hidden=state.section!=='Jobs';
  root.querySelectorAll('[data-section]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.section===state.section));
  root.querySelector('[data-row=topic]').innerHTML=[...new Set(model.jobs.map(j=>j.topic))].map(v=>pick(v,'topic',v,j.topic===v)).join('');
  root.querySelector('[data-row=job]').innerHTML=model.jobs.filter(x=>x.topic===j.topic).map(x=>pick(x.name,'job',x.id,x.id===j.id)).join('');
  root.querySelector('[data-row=group]').innerHTML=pick('Main','task','main',state.task==='main')+[...new Set(j.tasks.map(x=>x.group))].map(g=>pick(g,'group',g,g===t?.group)).join('');
  const row=root.querySelector('[data-row=task]');row.hidden=!t;
  row.innerHTML=t?j.tasks.filter(x=>x.group===t.group).map(x=>pick(x.name,'task',x.id,x.id===t.id)).join(''):'';
  const pkg=delivered();
  root.querySelector('.lb-content').innerHTML=state.section==='Review'?review():state.section==='Delivery'?band('📦 Delivery',pkg?fold(pkg.title,facts(pkg.facts),'done'):fold(model.releaseName,facts(model.releaseRequirements))):t?band('📊 Plan + Results',fold(t.name,taskBody(t),taskState(t))):main();
  root.querySelectorAll('details').forEach(d=>d.open=open.includes(d.querySelector('.lb-label').textContent));
  let waits=j.tasks.filter(t=>['waiting','blocked'].includes(taskState(t))).length;
  if(model.kind==='guideline'&&!state.approved[state.job])waits=Math.max(1,waits);
  const tray=root.querySelector('[data-action=waits]');tray.hidden=!waits;tray.textContent='🙋 '+waits;tray.setAttribute('aria-label','Review waiting items');
 }
 function save(){
  if(window.openai?.setWidgetState)window.openai.setWidgetState({modelContent:{block:model.name,job:job().name,section:state.section,task:job().tasks.find(t=>t.id===state.task)?.name||'Main'},privateContent:{state,remembered}}).catch(()=>{});
 }
 function restore(snapshot){
  const saved=snapshot?.privateContent?.state;
  if(saved?.block!==model.blockId)return;
  state={...first,...saved};remembered=snapshot.privateContent.remembered||{};
  if(!model.jobs.some(j=>j.id===state.job))state.job=first.job;
  if(state.task!=='main'&&!job().tasks.some(t=>t.id===state.task))state.task='main';
  if(!['Jobs','Review','Delivery'].includes(state.section))state.section='Jobs';
  state.case=Math.min(model.cases?.length-1||0,Math.max(0,state.case||0));
 }
 root.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||b.disabled)return;let keep=false;
  notice('');
  if(b.dataset.section)state.section=b.dataset.section;
  if(b.dataset.job){state.job=b.dataset.job;state.task='main';}
  if(b.dataset.topic){state.job=model.jobs.find(j=>j.topic===b.dataset.topic).id;state.task='main';}
  if(b.dataset.group)state.task=remembered[state.job+':'+b.dataset.group]||job().tasks.find(t=>t.group===b.dataset.group).id;
  if(b.dataset.task){state.task=b.dataset.task;if(state.task!=='main')remembered[state.job+':'+job().tasks.find(t=>t.id===state.task).group]=state.task;}
  if(b.dataset.case!==undefined){state.case=Number(b.dataset.case);keep=true;}
  const a=b.dataset.action;
  if(a==='about'){notice('Synthetic design example. These actions update the preview; they do not run workers or sign real releases.');return;}
  if(a==='review'||a==='waits')state.section='Review';
  if(a==='recipe'){state.recipes[state.job]=true;keep=true;notice('Recipe accepted for this preview. Item building can proceed.');}
  if(a==='generate'&&reviewed()){state.generated[state.job]=true;keep=true;}
  if(a==='validate'&&state.generated[state.job]){state.validated[state.job]=true;keep=true;}
  if(a==='approve'&&state.validated[state.job]){state.approved[state.job]=true;keep=true;notice('Preview guideline-v3 confirmed. Existing Scale Jobs remain bound to guideline-v2.');}
  if(a==='queue'&&job().signed&&job().qualified&&!job().complete&&!state.queued[state.job]){state.queued[state.job]=true;keep=true;notice('Preview batches queued; completed batches are retained. No worker was started.');}
  if(a==='feedback'){notice('Feedback prepared for the Guideline Generation Block: conversation-02/reply-01, guideline-v2, context changes interpretation.');return;}
  if(a?.startsWith('finding:')){const t=job().tasks.find(t=>t.id===a.slice(8));state.section=t.state==='blocked'?'Jobs':'Review';state.task=t.id;}
  render(keep);save();
 });
 root.addEventListener('change',e=>{
  if(e.target.type!=='radio')return;
  state.answers[state.job+':'+state.case]=e.target.value;
  state.generated[state.job]=false;state.validated[state.job]=false;notice('');render(true);save();
 });
 restore(window.openai?.widgetState);render();
 window.addEventListener('openai:set_globals',e=>{if(e.detail?.globals?.widgetState){restore(e.detail.globals.widgetState);render(true);}});
})();
