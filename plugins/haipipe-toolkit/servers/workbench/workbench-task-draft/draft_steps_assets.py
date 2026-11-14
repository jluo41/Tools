"""The draft steps' inline stylesheets and scripts (draft_steps.py and its step modules), kept apart from the
Python that draws the steps; constants only, each pasted into a page as it is."""


# the frame as tall as what it holds, no inner scroll, no border (JL 261020 on 5 · Revise, then 4 · Revise: "The UI here is still not
# good"): it follows its page as you type or open a Scratch note
FIT_STYLE = "height:160px;min-height:0;border:0"
FIT = ("(function(f){try{var d=f.contentDocument,fit=function(){f.style.height=(d.body.scrollHeight+8)+'px';};"
       "fit();new f.contentWindow.ResizeObserver(fit).observe(d.body);}catch(e){}})(this)")


OFF_CSS = ("<style>.pm-off{display:block;margin-top:3px;font-size:11.5px;font-weight:600;color:#e03131}"
           ".pm-okr{display:block;margin-top:3px;font-size:11.5px;color:var(--mut)}</style>")


EX_CSS = """<style>
.ex-review td{vertical-align:top;font-size:13px;line-height:1.45}
@media(max-width:1000px){.ex-review{overflow-x:auto}}
</style>"""


# what is happening, in a corner of the screen while it happens (JL 261020: "when it is loading, could you state that
# status?"): loading the editor, saving, updating the text, saved; a refusal stays, in red
WRITE_JS = """<style>
.wr-msg{position:fixed;right:24px;bottom:20px;z-index:20;padding:6px 12px;border:1px solid var(--line);border-radius:6px;
 background:var(--card);color:var(--fg);font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,.12);max-width:420px}
.wr-msg:empty{display:none}.wr-msg.bad{color:#c92a2a;border-color:#c92a2a}.wr-split .rv-left.wr-old{opacity:.55}
/* the text and "Write it yourself" side by side, each in the same height with its own scroll bar (JL 261102: "here we
   should have the scroll bar as well"): the editor frame stops growing with its page and scrolls inside */
.wr-split{align-items:stretch}.wr-split>.rv-left{max-height:72vh;overflow-y:auto;padding-right:6px}
.wr-split>.rv-right{display:flex;flex-direction:column;max-height:72vh;min-height:0}
.wr-split>.rv-right>iframe.space-frame{flex:1 1 auto;height:auto!important;min-height:40vh;overflow:auto}
@media(max-width:700px){.wr-split>.rv-left,.wr-split>.rv-right{max-height:none}.wr-split>.rv-right>iframe.space-frame{height:70vh!important}}
</style><script>
(function(){if(window.__wrSplit)return;window.__wrSplit=1;
 function say(sp,t,bad,ms){var m=sp.parentNode.querySelector('.wr-msg');if(!m)return;m.textContent=t||'';m.classList.toggle('bad',!!bad);
  clearTimeout(m._t);if(ms)m._t=setTimeout(function(){m.textContent='';},ms);}
 function row(sp,s){try{return s?sp.querySelector('iframe').contentDocument.querySelector('.revise-rows>div[data-s="'+s+'"]'):null;}catch(e){return null;}}
 /* a sentence lit on both sides; from the editor, the text scrolls on its own to show it */
 function light(sp,s,on,scroll){var t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]'),r=row(sp,s);
  if(r)r.classList.toggle('wr-lit',on);if(!t)return;t.classList.toggle('rv-lit',on);var l=t.closest('.rv-left');
  if(on&&scroll&&l.scrollHeight>l.clientHeight&&(t.offsetTop<l.scrollTop||t.offsetTop+t.offsetHeight>l.scrollTop+l.clientHeight))
   l.scrollTo({top:Math.max(0,t.offsetTop-l.clientHeight/3),behavior:'smooth'});}
 /* the text again from the server once a box saved: its new words, their evidence boxed */
 function refresh(sp){var l=sp.querySelector('.rv-left');say(sp,'Updating the text…');l.classList.add('wr-old');
  fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(h){
   var n=new DOMParser().parseFromString(h,'text/html').querySelector('.wr-split .rv-left');
   if(n)l.innerHTML=n.innerHTML;l.classList.remove('wr-old');say(sp,'✓ Saved',false,2000);})
  .catch(function(){l.classList.remove('wr-old');say(sp,'Saved, but the text did not update; reload the page',true);});}
 window.wrHook=function(f){var sp=f.closest('.wr-split'),d;try{d=f.contentDocument;}catch(e){return;}
  if(!sp||!d||!d.body||d.__wr||d.location.href==='about:blank')return;d.__wr=1;var cur='';
  say(sp,d.querySelector('.revise-rows')?'':'The editor did not load; reload the page',!d.querySelector('.revise-rows'));
  var st=d.createElement('style');st.textContent='.revise-rows>div.wr-lit{background:#fff3bf;border-radius:3px}';d.head.appendChild(st);
  function on(s){if(!s||s===cur)return;light(sp,cur,false);cur=s;light(sp,cur,true,true);}
  function at(){var x=d.getSelection(),n=x&&x.anchorNode;while(n&&!(n.parentNode&&n.parentNode.classList&&n.parentNode.classList.contains('revise-rows')))n=n.parentNode;
   return n&&n.getAttribute?n.getAttribute('data-s'):'';}
  d.addEventListener('mouseover',function(e){var r=e.target.closest&&e.target.closest('.revise-rows>div[data-s]');if(r)on(r.getAttribute('data-s'));});
  d.addEventListener('keyup',function(){on(at());});d.addEventListener('click',function(){on(at());});
  /* the text follows the typing at once (JL 261020: "I see it will need to wait for a while"); the save, when the
     box is left, then reads it again with its evidence boxed */
  d.addEventListener('input',function(e){var r=e.target.closest&&e.target.closest('.revise-rows');if(!r)return;
   [].forEach.call(r.children,function(x){var s=x.getAttribute('data-s'),t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]');
    if(!t)return;var w=x.innerText.replace(/\\s+/g,' ').trim(),l=t.firstElementChild,tx=t.querySelector('.s-tx');
    if(t.dataset.typed!==w){t.dataset.typed=w;if(tx){tx.textContent=w;return;}
     t.textContent=' '+w;if(l&&l.classList.contains('mut'))t.insertBefore(l,t.firstChild);}});});
  /* the mouse gone from the editor: back to the row being typed in, or nothing lit */
  d.documentElement.addEventListener('mouseleave',function(){var s=at();if(cur&&cur!==s){light(sp,cur,false);cur='';}on(s);});
  /* the editor's own status line, said in the corner: Saving…, then the text again, or why it did not save */
  new MutationObserver(function(ms){var b=null;ms.forEach(function(m){var t=m.target.nodeType===1?m.target:m.target.parentNode;
    b=(t&&t.closest&&t.closest('.revise-status'))||b;});if(!b)return;var t=b.textContent.trim();
    if(b.classList.contains('err')&&t)say(sp,t,true);else if(/^Saving|^Adding/.test(t))say(sp,t);
    else if(/^Saved/.test(t))refresh(sp);else if(/^Nothing changed/.test(t))say(sp,'Nothing changed',false,1500);})
   .observe(d.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['class']});};
 document.querySelectorAll('.wr-split iframe').forEach(function(f){try{if(f.contentDocument.readyState==='complete')window.wrHook(f);}catch(e){}});
 document.addEventListener('mouseover',function(e){var t=e.target.closest&&e.target.closest('.wr-split .rv-left li[data-s]');
  if(t)light(t.closest('.wr-split'),t.dataset.s,true);});
 document.addEventListener('mouseout',function(e){var t=e.target.closest&&e.target.closest('.wr-split .rv-left li[data-s]');
  if(t&&!t.contains(e.relatedTarget))light(t.closest('.wr-split'),t.dataset.s,false);});
})();
</script>"""


# the text and the cards as 5 · Revise lays them out, one column with no gap between sentences and the cards at their
# sentences (JL 261020: "I want it to be left to be the orignal text, and the right to be the evidence";
# "我想要保证这个 draft 在 revise、evidence、display 这里都保持一样的风格 ... 所以句子跟句子之间不要有空格"); only the cards' own look here
EV_CSS = """<style>
.ev-card{padding:4px 12px;margin:0 0 8px}.ev-card td{vertical-align:top}
.ev-card tr+tr td,.ev-list tr+tr td{border-top:1px solid var(--line)}.ev-list td{vertical-align:top}
</style>"""


NOTES_CSS = """<style>
.nt-gut{flex:0 0 46px;display:flex;justify-content:flex-end;align-items:center;gap:3px;align-self:flex-start;padding-top:4px}
.nt-plus{width:20px;height:20px;padding:0;border:1px solid var(--line);border-radius:10px;background:var(--card);
 color:var(--acc);font-size:14px;font-weight:700;line-height:17px;cursor:pointer;opacity:0}
.rv-left li[data-s]:hover .nt-plus,.nt-plus:focus{opacity:1}
/* a paragraph takes a comment too (JL 261021: "比如说这个 paragraph 也可以加 comments 呢？"): a + after its heading */
.rv-board .rv-left h4[data-p],.rv-board .rv-left h3[data-p]{display:flex;align-items:center;gap:8px}
.rv-board .rv-left h4[data-p] .nt-gut,.rv-board .rv-left h3[data-p] .nt-gut{flex:0 0 auto;padding:0;align-self:center}
.rv-left h4[data-p]:hover .nt-plus,.rv-left h3[data-p]:hover .nt-plus{opacity:1}
.nt-mark{font-size:13px;cursor:pointer}
/* in Revise the evidence stays boxed (JL 261021: "I think we still need the box"), but its CITE labels go, as the
   words are what is read there (3 · Evidence keeps them) */
.rv-board .rv-left mark+sup{display:none}
.nt-sel{position:fixed;z-index:50;display:none}
/* a comment is a thread: rounded, a round mark for who wrote each message, small text actions */
.rv-right .rv-note{border-radius:10px;padding:10px 12px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.nt-head{display:flex;align-items:center;gap:6px}
.nt-s{font-size:12px;font-weight:600;color:var(--mut);background:var(--wash);border-radius:10px;padding:1px 8px}
.nt-state{font-size:12px;border-radius:10px;padding:1px 8px;background:#fff4e6;color:#d9480f}
.nt-state.nt-answered{background:#f3f0ff;color:#6741d9}.nt-state.nt-done{background:#ebfbee;color:#2b8a3e}
.nt-quote{margin:6px 0 2px;font-size:13px;color:var(--mut);font-style:italic}
.nt-msg{display:grid;grid-template-columns:26px minmax(0,1fr);gap:8px;margin:8px 0 0}
.nt-av{width:26px;height:26px;border-radius:13px;background:#e7f5ff;color:#1971c2;font-size:10px;font-weight:700;
 display:flex;align-items:center;justify-content:center}
.nt-ai .nt-av{background:#f3f0ff;color:#6741d9}
.nt-who{font-size:12px;color:var(--mut)}.nt-who b{color:var(--fg);font-weight:600;margin-right:4px}
.nt-text{font-size:14px;line-height:1.5;margin-top:1px}
.nt-ai .nt-text{background:var(--wash);border-radius:8px;padding:6px 10px;margin-top:3px}
.nt-cards{margin:6px 0 0 34px;font-size:12px;color:var(--mut)}
.nt-acts{display:flex;align-items:center;gap:2px;margin:6px 0 0 30px}
.nt-btn{border:0;background:none;color:var(--acc);font:inherit;font-size:13px;font-weight:500;padding:3px 8px;border-radius:6px;cursor:pointer}
.nt-btn:hover{background:var(--wash)}.nt-danger{color:#c92a2a}
.nt-send{background:var(--acc);color:#fff}.nt-send:hover{background:var(--acc);opacity:.9}
.rv-note .nt-box{display:none;width:calc(100% - 34px);box-sizing:border-box;margin:8px 0 0 34px;font:inherit;font-size:14px;
 padding:7px 10px;border:1px solid var(--line);border-radius:8px;resize:vertical;outline:none}
.rv-note .nt-box:focus{border-color:var(--acc)}
.rv-note.writing .nt-box,.rv-note.nt-new .nt-box{display:block}
.rv-note .nt-w{display:none}.rv-note.writing .nt-w,.rv-note.nt-new .nt-w{display:inline-block}.rv-note.writing .nt-st{display:none}
</style>"""
NOTES_JS = """<script>
(function(){if(window.__rvNotes)return;window.__rvNotes=1;
 function board(x){return (x&&x.closest('.rv-board'))||document.querySelector('.rv-board');}
 function again(){if(window.rvAlign)window.rvAlign();marks();}
 function msg(c,t,bad){var m=c.querySelector('.rv-msg');if(m){m.textContent=t||'';m.style.color=bad?'#c92a2a':'';}}
 /* a + beside each sentence; a 💬 after each sentence a comment still waits on */
 /* S1, S2 restart in every paragraph: each sentence also gets its full address C1.P2.S2 from the heading above it */
 function addr(){document.querySelectorAll('.rv-board .rv-left li[data-s]').forEach(function(li){if(li.dataset.a)return;
  var x=li.closest('ul');x=x&&x.previousElementSibling;while(x&&!(x.tagName==='H4'&&x.dataset.p))x=x.previousElementSibling;
  if(x)li.dataset.a=x.dataset.p+'.'+li.dataset.s;});}
 function pluses(){addr();document.querySelectorAll('.rv-board .rv-left li[data-s]').forEach(function(li){if(li.querySelector('.nt-gut'))return;
  var g=document.createElement('span');g.className='nt-gut';var b=document.createElement('button');b.type='button';b.className='nt-plus';
  b.textContent='+';b.title='Comment on '+(li.dataset.a||li.dataset.s);g.appendChild(b);li.appendChild(g);});
  document.querySelectorAll('.rv-board .rv-left h4[data-p],.rv-board .rv-left h3[data-p]').forEach(function(h){if(h.querySelector('.nt-gut'))return;
   var g=document.createElement('span');g.className='nt-gut';var b=document.createElement('button');b.type='button';b.className='nt-plus';
   b.textContent='+';b.title='Comment on '+(h.tagName==='H3'?'the Section ':'the paragraph ')+h.dataset.p;g.appendChild(b);h.appendChild(g);});}
 function tgt(el){return el.dataset.a||el.dataset.s||el.dataset.p;}
 function marks(){addr();document.querySelectorAll('.rv-board .nt-mark').forEach(function(x){x.remove();});
  document.querySelectorAll('.rv-board .rv-note[data-n]').forEach(function(c){if(c.dataset.state==='done')return;
   var li=board(c).querySelector('.rv-left li[data-a="'+c.dataset.s+'"],.rv-left li[data-s="'+c.dataset.s+'"]')||(c.dataset.p&&board(c).querySelector('.rv-left h4[data-p="'+c.dataset.p+'"],.rv-left h3[data-p="'+c.dataset.p+'"]'));
   if(!li||li.querySelector('.nt-mark'))return;
   var m=document.createElement('span');m.className='nt-mark';m.textContent='💬';m.title='Comment '+c.dataset.n;var g=li.querySelector('.nt-gut');if(g)g.insertBefore(m,g.firstChild);});}
 /* a new comment's card goes in reading order: before the first card on its sentence or a later one */
 function place(card,li){var sp=li.closest('.rv-split'),right=sp.querySelector('.rv-right'),before=right.querySelector('.rv-tail');
  [].some.call(right.children,function(c){if(!c.classList.contains('rv-card'))return false;var s=(c.dataset.s||'').split(' ')[0];
   var t=s&&sp.querySelector('.rv-left li[data-a="'+s+'"],.rv-left li[data-s="'+s+'"]');
   if(t&&(t===li||(li.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING))){before=c;return true;}return false;});
  right.insertBefore(card,before||null);}
 function open(li,quote){var c=document.createElement('div');c.className='rv-card rv-note nt-new';c.dataset.s=tgt(li);c.dataset.quote=quote||'';
  if(li.dataset.p&&!li.dataset.s)c.dataset.p=li.dataset.p;
  c.innerHTML='<div class=nt-head><span class=nt-s>'+tgt(li)+'</span> <span class=nt-state>New comment</span></div>'+
   (quote?'<div class=nt-quote></div>':'')+'<textarea class=nt-box rows=2 placeholder="Comment on '+tgt(li)+'…"></textarea>'+
   '<div class=nt-acts><button type=button class="nt-btn nt-w nt-send" data-note-act=add>Comment</button>'+
   '<button type=button class="nt-btn nt-w" data-note-act=cancel>Cancel</button><span class="rv-msg mut"></span></div>';
  if(quote)c.querySelector('.nt-quote').textContent='“'+quote+'”';
  var row=li.closest('.sx-row');if(row)row.classList.add('sx-open');place(c,li);again();c.querySelector('textarea').focus();li.classList.add('rv-lit');setTimeout(function(){li.classList.remove('rv-lit');},1400);}
 /* select words in a sentence: a 💬 Comment button opens a comment on them */
 var sel=document.createElement('button');sel.type='button';sel.className='work-act nt-sel';sel.textContent='💬 Comment';
 document.addEventListener('DOMContentLoaded',function(){document.body.appendChild(sel);});if(document.body)document.body.appendChild(sel);
 function picked(){var s=window.getSelection&&window.getSelection();if(!s||s.isCollapsed||!s.rangeCount)return null;
  var a=s.anchorNode&&(s.anchorNode.nodeType===1?s.anchorNode:s.anchorNode.parentNode),f=s.focusNode&&(s.focusNode.nodeType===1?s.focusNode:s.focusNode.parentNode);
  var li=a&&a.closest&&a.closest('.rv-board .rv-left li[data-s]');if(!li||!f||li!==(f.closest&&f.closest('li[data-s]')))return null;
  var q=s.toString().replace(/\\s+/g,' ').replace(/^\\s*S\\d+[a-z]?\\s+/,'').replace(/[+💬]/g,'').trim();return q?{li:li,q:q,r:s.getRangeAt(0).getBoundingClientRect()}:null;}
 document.addEventListener('mouseup',function(e){if(e.target===sel)return;setTimeout(function(){var p=picked();
  if(!p){sel.style.display='none';return;}sel._p=p;sel.style.left=Math.max(4,p.r.left)+'px';sel.style.top=(p.r.bottom+6)+'px';sel.style.display='block';},0);});
 document.addEventListener('mousedown',function(e){if(e.target!==sel)sel.style.display='none';});
 document.addEventListener('click',function(e){if(e.target===sel&&sel._p){e.preventDefault();sel.style.display='none';open(sel._p.li,sel._p.q);return;}
  var plus=e.target.closest&&e.target.closest('.nt-plus');if(plus){e.preventDefault();e.stopPropagation();open(plus.closest('li[data-s],h4[data-p],h3[data-p]'),'');return;}
  var mk=e.target.closest&&e.target.closest('.nt-mark');if(mk){var li=mk.closest('li[data-s],h4[data-p],h3[data-p]'),c=board(li).querySelector('.rv-note[data-s="'+tgt(li)+'"]');
   if(c){c.scrollIntoView({behavior:'smooth',block:'center'});}return;}
  var b=e.target.closest&&e.target.closest('[data-note-act]');if(!b)return;e.preventDefault();
  var c=b.closest('.rv-note'),act=b.dataset.noteAct,box=c.querySelector('.nt-box'),bd=board(c);
  if(act==='reply'){if(window.rvPin)window.rvPin(c);c.classList.add('writing');box.focus();again();return;}
  if(act==='cancel'){if(c.classList.contains('nt-new'))c.remove();else c.classList.remove('writing');again();return;}
  var body={task:bd.dataset.task,act:act==='save'?'reply':act,n:c.dataset.n||'',s:c.dataset.s,was:c.dataset.state||''};
  if(act==='add'||act==='save'){body.text=box.value;if(!body.text.trim()){msg(c,'write the comment first',true);return;}}
  if(act==='add')body.quote=c.dataset.quote||'';
  b.disabled=true;msg(c,'…');
  fetch('/_board/draft-comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){b.disabled=false;if(!j.ok){msg(c,j.err||'not saved',true);return;}
    if(!j.html){c.remove();}else{var t=document.createElement('div');t.innerHTML=j.html;c.replaceWith(t.firstElementChild);}again();})
   .catch(function(err){b.disabled=false;msg(c,String(err),true);});});
 function start(){pluses();marks();}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();setTimeout(start,80);
})();
</script>"""


CARDS_CSS = """<style>
/* "by" badges: who made a change (JL 261113) */
.by{display:inline-block;font:600 10.5px/1.5 system-ui,-apple-system,sans-serif;padding:0 5px;border-radius:8px;margin-left:3px;vertical-align:1px;letter-spacing:.02em;background:#eef0f3;color:#55606e}
.by-jl{background:#e7f0ff;color:#1c5fc2}.by-ra{background:#f3e8ff;color:#7a3db8}.by-gg{background:#e6f6ec;color:#2b7a46}
.by-ai{background:#f1f1f1;color:#777}
@media (prefers-color-scheme:dark){.by{background:#2a2f36;color:#b8c0cc}.by-jl{background:#1d2c45;color:#8fb6f5}.by-ra{background:#33244a;color:#cba6f2}.by-gg{background:#1d3626;color:#8fd3a5}}
.rv-card .rv-edit{display:none;margin:6px 0;padding:6px 10px;border-left:2px solid var(--acc);background:var(--wash);outline:none;line-height:1.6}
.rv-card.editing .rv-edit{display:block}.rv-card.editing .rv-change{display:none}
.rv-card [data-card-act=undo],.rv-card [data-card-act=save],.rv-card [data-card-act=cancel]{display:none}
.rv-card:not([data-state=proposed]) [data-card-act=undo]{display:inline-block}
.rv-card:not([data-state=proposed]) [data-card-act=accept],.rv-card:not([data-state=proposed]) [data-card-act=reject],
.rv-card:not([data-state=proposed]) [data-card-act=edit]{display:none}
.rv-card.editing [data-card-act]{display:none}.rv-card.editing [data-card-act=save],.rv-card.editing [data-card-act=cancel]{display:inline-block}
/* a plain box: no coloured side bar, no hover tint (JL 261020: "this is too AI"); the chip says the state */
.rv-card{border:1px solid var(--line);border-radius:3px;background:var(--card);padding:10px 14px;margin:0 0 12px}
.rv-card[data-state=rejected]{opacity:.55}
/* a card already written into the text has nothing left to decide */
.rv-card[data-state=written]:not(.has-opts) .rv-acts{display:none}
.rv-choices{margin:8px 0 0;display:flex;flex-direction:column;gap:4px}
.rv-choice{display:block;padding:6px 8px;border:1px solid var(--line);border-radius:8px;cursor:pointer;line-height:1.5}
.rv-choice:hover{background:var(--wash)}.rv-choice.sel{border-color:var(--acc);background:var(--wash)}
.rv-choice input{accent-color:var(--acc);margin:0 4px 0 0;vertical-align:-2px}
.rv-choice .rv-opt-diff{display:none}.rv-choice.sel .rv-opt-diff{display:inline}.rv-choice.sel .rv-opt-plain{display:none}
.rv-drop .rv-opt-text{color:var(--mut)}.rv-confirm{font-weight:600}
.rv-card.editing .rv-choices{display:none}
.rv-opts{margin:8px 0 0}.rv-opt{padding:6px 0;border-top:1px solid var(--line)}
.rv-opt-text{line-height:1.55;margin:2px 0 0}.rv-opt .rv-opt-mark{display:none}
/* the option in the card shows its change; the others read as plain sentences; the card's own change is that option's */
.rv-card.has-opts .rv-change{display:none}.rv-opt .rv-opt-diff{display:none}.rv-opt.chosen .rv-opt-diff{display:inline}
.rv-opt.chosen .rv-opt-plain{display:none}
.rv-card.has-opts:not(.show-opts) .rv-opt:not(.chosen){display:none}.rv-card.has-opts:not(.show-opts) .rv-opt.chosen{border-top:0}
/* every card in the column is one compact line until clicked, as a comment in a shared document is, so each stays
   beside its sentence (JL 261021: the Logic cards "应该是放到右边的"); a click opens it whole, with its buttons */
.rv-right .rv-card:not(.open):not(.peek):not(.rv-rev):not(.writing):not(.nt-new):not(.editing)>*:not(:first-child){display:none}
.rv-right .rv-card:not(.open):not(.peek):not(.rv-rev):not(.writing):not(.nt-new):not(.editing){padding-top:6px;padding-bottom:6px;margin-bottom:6px}
.rv-right .rv-card:not(.open):not(.peek):not(.rv-rev):not(.writing):not(.nt-new):not(.editing) [data-opts-more]{display:none}
.rv-right .rv-card:not(.rv-rev){cursor:pointer}.rv-right .rv-card.open{cursor:default}
/* pointed at, a card opens over the cards below it (they do not move), and folds again when the pointer leaves;
   a click pins it open in its place (JL 261021: "能不能我的鼠标一放上去的时候，它就自己打开了") */
.rv-right .rv-card.peek{position:relative;z-index:6;background:var(--card);box-shadow:0 8px 24px rgba(0,0,0,.16)}
.rv-right .rv-handle{cursor:pointer;display:inline-flex;align-items:center;gap:5px}.rv-right .rv-handle:hover{text-decoration:underline dotted}
.rv-card .rv-peek{display:block;font-size:13px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.rv-board > .rv-card .rv-peek,.rv-right .rv-card.open .rv-peek,.rv-right .rv-card.peek .rv-peek,.rv-right .rv-card.writing .rv-peek,.rv-right .rv-card.editing .rv-peek{display:none}
.rv-opt.chosen .rv-opt-mark{display:inline}.rv-opt.chosen .rv-opt-use{display:none}.rv-opt-use{margin-left:6px;padding:0 8px}
.sx-bar{display:none}.rv-board .sx-bar{display:flex;gap:6px;margin:0 0 6px}
.sx-sum,.sx-hb{font:inherit;font-size:12.5px;line-height:1.4;padding:2px 10px;border:1px solid var(--line);border-radius:12px;
 background:transparent;color:var(--mut);cursor:pointer}.sx-sum.wait{border-color:#b35c00;color:#b35c00}
.rv-board .sx-row:not(.sx-open)>.rv-right>.rv-card:not(.nt-new),.rv-board .sx-row:not(.sx-hist)>.rv-right>.sx-old{display:none}
.rv-board .sx-row:not(.sx-open) .sx-sum~.sx-hb{display:none}.rv-board .sx-row.sx-hist>.rv-right>.sx-old{opacity:.5}
.sx-row.sx-open .sx-sum,.sx-row.sx-hist .sx-hb{border-color:var(--acc);color:var(--acc)}
.sx-sim{font-size:12px}.sx-sim.low{color:#c92a2a;font-weight:600}
.rv-board.hide-notes .rv-right .rv-note,.rv-board.hide-logic .rv-right .rv-rev,.rv-board.hide-ev .rv-right .rv-ev{display:none}
.rv-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin:0 0 10px}
.rv-kinds{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:6px;margin-left:auto}
.rv-kind{font:inherit;font-size:13px;font-weight:600;padding:3px 12px;border-radius:14px;border:1px solid var(--acc);
 background:transparent;color:var(--acc);cursor:pointer}
.rv-kind span{font-weight:400;opacity:.75;margin-left:2px}.rv-kind[aria-pressed=true]{background:var(--acc);color:#fff}
.ev-k{font-size:12px;color:#1971c2}
.ev-item{margin:6px 0 0;padding:6px 0 0;border-top:1px solid var(--line);font-size:13.5px;line-height:1.5}
.ev-item a{color:var(--acc)}.ev-quote{margin:3px 0;color:var(--fg)}.ev-meta{font-size:12px;color:var(--mut)}
.rv-board.hide-edits .rv-card:not(.rv-note):not(.rv-rev):not(.rv-ev){display:none}
/* a Logic card: small, dashed, its scores and link in one line */
.rv-right .rv-rev{background:transparent;border-style:dashed;border-radius:8px;padding:6px 10px;font-size:13px}
.lg-head{display:flex;flex-wrap:wrap;align-items:center;gap:5px}.lg-k{font-size:12px;color:#6741d9}
.lg-link{font-size:12px;color:#2b8a3e}.lg-link.lg-weak{color:#d9480f}
.lg-text{margin:3px 0 0;line-height:1.45}.rv-right .rv-rev{margin-bottom:6px;cursor:pointer}
.rv-rev:not(.open):not(.peek) .lg-clip{display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
.rv-rev:not(.open):not(.peek) .lg-more{display:none}
.rv-rev:not(.open):not(.peek) .lg-clip2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
li.rv-lit,h4.rv-lit,tr.rv-lit td{background:#fff3bf;border-radius:3px}
.rv-board .rv-right{position:relative;clip-path:inset(0 -30px -100000px -30px)}
.sx-row:hover>.rv-left li[data-s]{background:#fff8db;border-radius:3px}
.sx-row:hover>.rv-right>.rv-card{border-color:#f08c00}
.rv-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:start}
/* the text reads as prose (JL 261021: "把字体变大一些"; "像 S5 这种东西能不能放到最左边"): larger type, no bullets, each
   sentence's number hung in a gutter on the left so every sentence starts on one line; a paragraph's head stays at
   the far left, above the numbers */
.rv-left{font-size:17px;line-height:1.65}
.rv-left h3.rv-part{font-size:19px;margin:26px 0 6px;padding-top:10px;border-top:1px solid var(--line)}
.rv-left h3.rv-part:first-child{border-top:0;margin-top:4px;padding-top:0}
.rv-left ul{list-style:none;margin:0 0 6px;padding:0}
.rv-left li[data-s]{display:flex;align-items:baseline;margin:0 0 10px;border-radius:3px}
.rv-left li[data-s] .s-no{color:#9a9890;font-size:12.5px}
.ev-mark{background:none;color:inherit;padding:0;border-bottom:2px solid color-mix(in srgb,var(--ink) 45%,transparent)}
.rv-left li[data-s]:hover .ev-mark,.rv-left li.rv-lit .ev-mark{background:color-mix(in srgb,var(--ink) 14%,transparent);border-radius:2px}
.rv-left li[data-s] .s-no{flex:0 0 42px;box-sizing:border-box;padding-right:12px;text-align:right;font-variant-numeric:tabular-nums}
.rv-left li[data-s] .s-tx{flex:1 1 auto;min-width:0}
.rv-left h4{font-size:16px}
.cite{color:var(--mut);font-size:.78em;white-space:nowrap}
.rv-left li.disp-embed{margin:6px 0 12px 42px}.rv-left li.disp-embed figure{margin:0}
.rv-left li.disp-embed img{display:block;max-width:100%;max-height:340px;border:1px solid var(--line);border-radius:4px}
.rv-left li.disp-embed figcaption{font-size:13px;color:var(--mut);margin-top:4px;line-height:1.45}
.rv-left li.disp-none figure{border:1px dashed #e8590c;border-radius:6px;padding:6px 10px}
.rv-right .rv-card{cursor:pointer}
/* the text and its cards scroll as one page, so each card stays beside its sentence (JL 261113: the text scrolled
   in its own box while the cards stayed, "the UI here is very bad"); the Write view keeps its own scroll bars */
.rv-split:not(.wr-split) .rv-left{padding-right:8px}
@media(max-width:1000px){.rv-split{grid-template-columns:minmax(0,1fr)}.rv-split .rv-left{position:static;max-height:none}}
/* the sentence board: one row per sentence, its cards beside it or under it (_sx_board) */
.sx-board{font-size:17px;line-height:1.65}
.sx-lay{display:flex;justify-content:flex-end;gap:4px;margin:0 0 4px}
.sx-lay button{font:inherit;font-size:12.5px;line-height:1.4;padding:2px 10px;border:1px solid var(--line);border-radius:12px;
 background:transparent;color:var(--mut);cursor:pointer}
.sx-lay button[aria-pressed=true]{border-color:var(--acc);color:var(--acc);font-weight:600}
.sx-board>h3.rv-part{font-size:19px;margin:26px 0 6px;padding-top:10px;border-top:1px solid var(--line)}
.sx-board>ul{list-style:none;margin:0 0 6px;padding:0}
.sx-row{padding:6px 0;border-top:1px solid color-mix(in srgb,var(--line) 55%,transparent)}
.sx-row.sx-p,.sx-board>h3+.sx-row{border-top:0}.sx-row.sx-p{padding-top:14px}
.sx-row .rv-left ul{margin:0}.sx-row .rv-left li[data-s]{margin:0}.sx-row .rv-left h4{margin:0!important}
.sx-row>.rv-right>.rv-card:last-child{margin-bottom:0}
.sx-board.sx-ud .sx-row{grid-template-columns:minmax(0,1fr);gap:4px}
.sx-board.sx-ud .sx-row>.rv-right{padding-left:42px}
.sx-board.sx-ud .sx-row>.rv-right:empty{display:none}
.sx-lay+.sx-row{border-top:0}
@media(max-width:1000px){.sx-row{gap:4px}.sx-row>.rv-right{padding-left:42px}.sx-row>.rv-right:empty{display:none}
 .sx-lay{display:none}}
</style>"""
CARDS_JS = """<script>
(function(){if(window.__rvCards)return;window.__rvCards=1;
 var CHIP={proposed:'<span class="st st-warn">🔶 proposed</span>',accepted:'<span class="st st-ok">✓ accepted</span>',
           rejected:'<span class=st>✗ rejected</span>',written:'<span class="st st-ok">✓ written</span>'};
 function msg(c,t,bad){var m=c.querySelector('.rv-msg');m.textContent=t||'';m.style.color=bad?'#c92a2a':'';}
 /* a card's sentences in the text: data-s holds one id (a Revise card) or several (an Evidence card), else its paragraph */
 function targets(c){var sp=c.closest('.rv-split'),root=sp?sp.querySelector('.rv-left'):document,out=[];
  (c.dataset.s||'').split(' ').forEach(function(s){var t=s&&root.querySelector('li[data-a="'+s+'"],li[data-s="'+s+'"]');if(t)out.push(t);});
  var h=!out.length&&c.dataset.p&&root.querySelector('h4[data-p="'+c.dataset.p+'"],h3[data-p="'+c.dataset.p+'"]');if(h)out.push(h);return out;}
 function target(c){return targets(c)[0]||null;}
 /* a card's sentence lights in the text, which scrolls on its own to show it (the text stays beside the cards) */
 function lit(c,on){var ts=targets(c),t=ts[0];if(!t)return;ts.forEach(function(x){x.classList.toggle('rv-lit',on);});var left=t.closest('.rv-left');
  if(on&&left&&left.scrollHeight>left.clientHeight&&(t.offsetTop<left.scrollTop||t.offsetTop+t.offsetHeight>left.scrollTop+left.clientHeight))
   left.scrollTo({top:Math.max(0,t.offsetTop-left.clientHeight/3),behavior:'smooth'});}
 /* each sentence is a row that holds its own cards (_sx_board), so no card is measured or moved; align() stays as the
    name other code calls */
 function align(){}
 function peekOff(c){if(!c.classList.contains('peek'))return;c.classList.remove('peek');c.style.marginBottom='';}
 /* a card being written in stays open in its place */
 window.rvPin=function(c){if(!c)return;c.classList.remove('peek');c.style.marginBottom='';c.classList.add('open');};
 document.addEventListener('mouseout',function(e){var c=e.target.closest&&e.target.closest('.rv-right .rv-card');
  if(c&&!c.contains(e.relatedTarget)&&!c.matches('.writing,.editing'))peekOff(c);});
 /* cards beside each sentence or under it (JL 261113: "it can be left-right, and it can also be up-down"), kept */
 function lay(v){document.querySelectorAll('.sx-board:not(.sx-fixed)').forEach(function(b){b.classList.toggle('sx-ud',v==='ud');
  b.querySelectorAll('[data-sx-lay]').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.sxLay===v);});});}
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-sx-lay]');if(!b)return;e.preventDefault();
  lay(b.dataset.sxLay);try{localStorage.setItem('sxLay',b.dataset.sxLay);}catch(err){}});
 function layStart(){var v='lr';try{v=localStorage.getItem('sxLay')||'lr';}catch(err){}lay(v);}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',layStart);else layStart();
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.sx-sum,.sx-hb');if(!b)return;e.preventDefault();
  var r=b.closest('.sx-row');if(b.classList.contains('sx-sum')){var on=r.classList.toggle('sx-open');if(!on)r.classList.remove('sx-hist');}
  else{var h=r.classList.toggle('sx-hist');if(!r.querySelector('.sx-sum'))r.classList.toggle('sx-open',h);}});
 window.rvAlign=align;
 /* a display under its sentence opens over the page, not in a new tab (JL 261023: "pop out, not a new link") */
 document.addEventListener('click',function(e){var i=e.target.closest&&e.target.closest('.disp-embed img');
  if(!i||e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();var b=document.createElement('div');
  b.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(20,20,20,.82);display:flex;align-items:center;justify-content:center;cursor:zoom-out';
  var g=document.createElement('img');g.src=i.src;g.style.cssText='max-width:96vw;max-height:94vh;background:#fff;border-radius:4px';
  b.appendChild(g);var k=function(ev){if(ev.key==='Escape')x();};var x=function(){b.remove();document.removeEventListener('keydown',k);};
  b.addEventListener('click',x);document.addEventListener('keydown',k);document.body.appendChild(b);},true);
 /* JL 261024: a click opens a card, a second click closes it; never open by itself */
 document.addEventListener('click',function(e){if(!e.target.closest||e.target.closest('[data-card-act],[data-note-act],.rv-edit,textarea,a,.rv-choice'))return;
  var c=e.target.closest('.rv-right .rv-card');if(!c)return;c.classList.remove('peek');c.style.marginBottom='';c.classList.toggle('open');});
 function rowlit(r,on){var sp=r.closest('.rv-split');if(!sp)return;
  r.dataset.s.split(' ').forEach(function(s){var t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]');if(t)t.classList.toggle('rv-lit',on);});}
 /* a sentence pointed at lights the evidence rows that name it; its row's cards light by CSS (.sx-row:hover) */
 function sentlit(li,on){var sp=li.closest('.rv-split');if(!sp)return;
  sp.querySelectorAll('.rv-right tr[data-s~="'+li.dataset.s+'"]').forEach(function(r){r.classList.toggle('rv-lit',on);});}
 document.addEventListener('mouseover',function(e){if(!e.target.closest)return;var li=e.target.closest('.rv-left li[data-s]');if(li){sentlit(li,true);return;}
  var r=e.target.closest('.rv-rows tr[data-s]');if(r&&r.dataset.s){var rc=r.closest('.rv-card');if(rc)lit(rc,false);rowlit(r,true);return;}
  var c=e.target.closest('.rv-card');if(c)lit(c,true);});
 document.addEventListener('mouseout',function(e){if(!e.target.closest)return;var li=e.target.closest('.rv-left li[data-s]');if(li&&!li.contains(e.relatedTarget))sentlit(li,false);
  var r=e.target.closest('.rv-rows tr[data-s]');if(r&&!r.contains(e.relatedTarget))rowlit(r,false);});
 document.addEventListener('mouseout',function(e){var c=e.target.closest&&e.target.closest('.rv-card');if(c&&!c.contains(e.relatedTarget))lit(c,false);});
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-opts-more]');if(!b)return;e.preventDefault();
  e.stopPropagation();var c=b.closest('.rv-card'),on=c.classList.toggle('show-opts');b.textContent=b.textContent.replace(on?'▸':'▾',on?'▾':'▸');align();},true);
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-cards-kind]');if(!b)return;e.preventDefault();
  var bd=b.closest('.rv-board'),k=b.dataset.cardsKind,off=!bd.classList.contains('hide-'+k);bd.classList.toggle('hide-'+k,off);
  b.setAttribute('aria-pressed',!off);align();});
 /* ✓ Accept all shows while a card is still proposed */
 function scope(x){return x&&(x.closest('.rv-board')||x.closest('.rv-right'));}
 function allbtn(right){var b=right&&right.querySelector('[data-cards-all]');
  if(b)b.style.display=right.querySelector('.rv-card[data-state=proposed]')?'':'none';}
 /* one card's act, written in the cards file; resolves true once saved */
 function send(c,act,b){var ed=c.querySelector('.rv-edit');
  var body={task:c.dataset.task,pass:c.dataset.pass,card:c.dataset.card,was:c.dataset.state,
            state:{accept:'accepted',reject:'rejected',undo:'proposed',save:c.dataset.state,option:'accepted'}[act]};
  if(act==='save')body.expected=ed.innerText;
  if(act==='option'){body.expected=b.dataset.text;body.option=b.dataset.opt;}
  if(act==='confirm'){var r=c.querySelector('.rv-choice.sel');if(!r){msg(c,'pick one first',true);return Promise.resolve(false);}
   if(r.dataset.opt==='drop'){body.state='rejected';}
   else if(c.dataset.state==='written'&&r.dataset.opt===c.dataset.chosen){msg(c,'already in the text');return Promise.resolve(false);}
   else{body.state='accepted';body.expected=r.dataset.text;body.option=r.dataset.opt;}}
  if(b)b.disabled=true;msg(c,'…');
  return fetch('/_board/draft-card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){if(b)b.disabled=false;
     if(!j.ok){msg(c,j.err||'not saved',true);return false;}
     c.dataset.state=j.state;c.querySelector('.rv-chip').innerHTML=CHIP[j.state]||j.state;
     var ch=c.querySelector('.rv-change');if(j.change&&ch){ch.innerHTML=j.change;}if(body.expected)ed.innerText=body.expected;
     if(body.option)c.dataset.chosen=body.option;
     if(body.option)c.querySelectorAll('.rv-opt').forEach(function(o){o.classList.toggle('chosen',o.dataset.opt===body.option);});c.classList.remove('editing');msg(c,j.note||'');
     if(j.state==='written'&&body.state==='accepted'){msg(c,'written into the text');setTimeout(function(){if(window.sxKeep)window.sxKeep(c);location.reload();},400);}
     allbtn(scope(c));align();return true;})
   .catch(function(err){if(b)b.disabled=false;msg(c,String(err),true);return false;});}
 document.addEventListener('change',function(e){var i=e.target;if(!i.closest||!i.closest('.rv-choice'))return;
  var c=i.closest('.rv-card');c.querySelectorAll('.rv-choice').forEach(function(x){x.classList.toggle('sel',x.contains(i));});align();});
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-card-act]');if(!b)return;e.preventDefault();
  var c=b.closest('.rv-card'),act=b.dataset.cardAct,ed=c.querySelector('.rv-edit');
  if(act==='edit'){if(window.rvPin)window.rvPin(c);c.classList.add('editing');c.dataset.before=ed.innerText;ed.focus();align();return;}
  if(act==='cancel'){ed.innerText=c.dataset.before||ed.innerText;c.classList.remove('editing');align();return;}
  send(c,act,b);});
})();
</script>"""
