"""The sentence board's look and behaviour (SX_ROWS: its fonts, folds, switches and the script that keeps them),
moved out of draft_step_evidence.py (700-line rule); draft_step_evidence re-exports SX_ROWS."""


# Each sentence folds its cards away and keeps its whole text (JL 261113: "why we don't have things like > to click and we can save more spaces"; "I want them to show the whole sentence"):
# ▸ opens it with its cards, ▾ folds it; a folded line ends in its marks, 📎 evidence, 🕘 earlier wordings and decided
# cards, 🙋 cards that wait for you, and a sentence with a waiting card starts open. ▸ on a paragraph heading folds the
# paragraph's rows. The text reads in Source Serif 4, a journal-like serif (Literata before it, JL 261113: "please update
# it again"), on a pale paper tone, with the
# cards white on it (JL 261113: "make the font ... more classic and easier to read"; "could we give some background
# light color to the main text"); without the web font it falls back to the system's Charter or Georgia.
SX_ROWS = """<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
.sx-board .rv-left li[data-s],.sx-board .rv-left h4,.sx-board h3.rv-part{font-family:"Source Serif 4",Charter,"Bitstream Charter",
 "Sitka Text","Iowan Old Style",Cambria,Georgia,serif}
.sx-board .rv-left{font-size:19.5px;line-height:1.7}   /* larger text (JL 261113: "how could you make the font size larger?") */
.sx-board{font-size:19.5px;line-height:1.7;background:color-mix(in srgb,#efe6d4 30%,var(--card,#fff));
 padding:10px 16px 14px;border-radius:8px;border:1px solid color-mix(in srgb,#e6dcc8 55%,var(--line,#ddd))}
.sx-board .rv-left li[data-s]{color:color-mix(in srgb,var(--ink,#222) 92%,#5a4a2a)}
.sx-board .rv-right .rv-card{background:var(--card,#fff)}
.sx-board .rv-left .s-no{font-family:system-ui,-apple-system,sans-serif}
/* the numbers start on one line, S1 under S3b (JL 261113: "why the index here are not aligned?") */
.sx-board .rv-left li[data-s] .s-no{flex:0 0 38px;text-align:left;padding-right:4px;font-size:11px;color:#b5b3ab}
/* two numbers (JL 261113: "the sentence fix index, and the index that shown in the order"): the reading position,
   1, 2, 3 in each part as the text reads now, then the sentence's fixed id (S3b), small, which cards and comments use */
.sx-board .rv-left li[data-s]>.s-ord{flex:0 0 24px;box-sizing:border-box;text-align:right;padding-right:7px;
 font:600 13px/1.9 system-ui,-apple-system,sans-serif;color:var(--ink,#333);font-variant-numeric:tabular-nums}
.sx-board .rv-left li[data-s]>.sx-tog{display:none}   /* no arrow: the marks after the sentence open its cards (JL 261113) */
/* the text set full width, flush on both edges, as a printed paper is (JL 261113: "fully aligned") */
/* left-aligned: a long \\citep{...} would stretch a justified line into gaps (JL 261113 screenshot of S3) */
.sx-board .rv-left li[data-s] .s-tx{text-align:left;hyphens:auto;-webkit-hyphens:auto}
/* the cards read at the page's own size, not the text's 18px (JL 261113: "the edit card here is too large") */
.sx-row>.rv-right{font-size:13.5px;line-height:1.45}
.sx-row>.rv-right .rv-card{padding:6px 10px;margin-bottom:6px}
.sx-row>.rv-right .rv-handle,.sx-row>.rv-right .rv-card b{font-size:13.5px}
.sx-tog,.sx-ptog{border:0;background:none;cursor:pointer;color:var(--ink,#333);font-size:15px;width:20px;padding:0;margin:0 2px 0 0;
 font-family:system-ui,sans-serif;vertical-align:baseline}
.sx-tog:hover,.sx-ptog:hover{color:var(--acc)}
.sx-tog::before,.sx-ptog::before{content:'▾'}
.sx-row.sx-fold .sx-tog::before,.sx-row.sx-pfold .sx-ptog::before{content:'▸'}
.sx-marks{font:12px/1 system-ui,-apple-system,sans-serif;color:var(--mut);white-space:nowrap;margin-left:6px}
.s-tx>.sx-marks{display:inline;vertical-align:1px}   /* right after the sentence's last word, as a footnote mark */
.sx-marks span{margin-left:8px}.sx-marks .w{color:#b35c00;font-weight:600}
.sx-row:not(.sx-fold) .sx-marks>span:not(.sx-clk){display:none}
/* the clock is the History switch (JL 261113: "when I click the clock, could I hide the History button"): one control */
.rv-board .sx-hb,.rv-board .sx-sum{display:none!important}
/* the cards are the pen after the clock (JL 261113: "like it should be things like the pen?"); orange while one waits */
.sx-pen{cursor:pointer;border-radius:8px;padding:0 3px}.sx-pen:hover{color:var(--acc)}
.sx-row.sx-open .sx-pen{color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,transparent);font-weight:600}
.sx-row:not(.sx-fold) .sx-marks>span.sx-pen,.sx-row:not(.sx-fold) .sx-marks>span.sx-evm{display:inline}
.sx-evm{cursor:pointer;border-radius:8px;padding:0 3px}.sx-evm:hover{color:var(--acc)}
.sx-board .sx-row.sx-evon>.rv-right>.rv-ev{display:block!important}.sx-row.sx-evon .sx-evm{color:var(--acc)}
/* a card under its sentence starts where the sentence's text starts (position 24 + id 38) */
.sx-board.sx-ud .sx-row>.rv-right{padding-left:62px}
/* a card's text runs exactly as wide as the sentence's (JL 261113: "make the card width the same to the sentences"):
   the box steps out by its own border and padding, and earlier wordings use the sentence's own face and size */
.sx-board.sx-ud .sx-row>.rv-right>.rv-card{margin-left:-11px;margin-right:3px}   /* text edges = the sentence's */
.sx-board .sx-histcard .sx-h{font-size:18px;line-height:1.7;text-align:justify;hyphens:auto;-webkit-hyphens:auto}
@media(max-width:1000px){.sx-board .sx-row>.rv-right{padding-left:62px}.sx-board .sx-row>.rv-right>.rv-card{margin-left:-11px;margin-right:3px}}
.sx-clk{cursor:pointer;border-radius:8px;padding:0 3px}
/* 🕘 shows only the earlier versions; the edits stay under 📝 */
.rv-board .sx-row:not(.sx-ver)>.rv-right>.sx-histcard{display:none!important}
.rv-board .sx-row.sx-ver>.rv-right>.rv-card.sx-histcard{display:block}
.sx-pen.faint{opacity:.55}.sx-clk:hover{color:var(--acc)}
.sx-row.sx-ver .sx-clk{color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,transparent);font-weight:600}
.sx-row.sx-fold{padding:1px 0;grid-template-columns:minmax(0,1fr)}
.sx-row.sx-fold>.rv-right{display:none}
/* a folded sentence keeps its whole text (JL 261113: "I want them to show the whole sentence"); only its cards fold */
.sx-row.sx-fold .rv-left li[data-s]{cursor:pointer}
.sx-row.sx-hide{display:none}
.sx-row.sx-p .sx-marks,.sx-row.sx-c .sx-marks{display:inline}
.sx-row.sx-c{padding-top:22px;margin-top:10px;border-top:1px solid var(--line)}
.sx-row.sx-c h3.rv-part{font-size:19px;margin:0;display:flex;align-items:center;gap:6px}
.sx-row.sx-c:has(>.rv-right:empty){grid-template-columns:minmax(0,1fr)}
.sx-row.sx-p:has(>.rv-right:empty){grid-template-columns:minmax(0,1fr)}
.sx-histcard .sx-h{padding:6px 0;border-top:1px solid var(--line);font-family:Charter,"Iowan Old Style",Georgia,serif;
 font-size:15px;line-height:1.55}
.sx-histcard .sx-h:first-of-type{border-top:0}
.sx-histcard .sx-hw{display:block;font:12px/1.4 system-ui,sans-serif;color:var(--mut);margin-bottom:2px}
.sx-histcard .sx-h.now .sx-hw{color:var(--acc);font-weight:600}
/* an edit is a card with a coloured edge; evidence is a quiet line under it; scores read by colour */
.sx-row>.rv-right .rv-ev{border:0!important;background:transparent!important;padding:1px 2px!important;margin:0 0 2px!important;
 color:var(--mut);box-shadow:none}
/* no coloured edge on a card, and a decided edit shows its change, not its A/B choices (JL 261113: "I don't want this") */
.sx-row>.rv-right .rv-card.sx-old .rv-choices,.sx-row>.rv-right .rv-card.sx-old .rv-acts{display:none}
/* quiet marks, so the eye stays on the sentence (JL 261113: "I don't want this to be too colorful") */
.sx-ai{font-weight:400;color:var(--mut)}.sx-ai.old{opacity:.55}.sx-ai.low{color:color-mix(in srgb,var(--mut) 70%,#8a3b2b)}
.sx-ok{cursor:pointer;color:color-mix(in srgb,var(--mut) 55%,transparent);font-weight:600;padding:0 2px}
.sx-ok:hover{color:var(--ink,#333)}.sx-ok.on{color:var(--ink,#333)}
.sx-board .sx-ok.stale{color:#b06d1a;background:color-mix(in srgb,#e8a33d 16%,transparent);border-radius:9px;padding:0 6px}
.sx-row:not(.sx-fold) .sx-marks>.sx-ok{display:inline!important}
.sx-board .rv-left li[data-checked="1"] .sx-ai,.sx-board .sx-row:has(.rv-left li[data-checked="1"])>.rv-right :is(.rv-rev,.rv-card[data-state=proposed]){display:none!important}   /* checked: no review, no proposal (JL 261114) */
.sx-cmt{cursor:pointer;opacity:.75}.sx-cmt:hover{opacity:1}
.nt-co .nt-av{background:color-mix(in srgb,#b8894a 18%,transparent);color:#7a5a2e}   /* a co-author's comment: their initials */
.sx-board .rv-left h4[data-p] .p-ord{font:600 13px/1 system-ui,-apple-system,sans-serif;color:var(--ink,#333);min-width:16px;text-align:right;margin-right:6px}
.sx-board .rv-left h4[data-p] .p-no{font:400 10.5px/1 system-ui,-apple-system,sans-serif;color:#b5b3ab;margin-left:6px}
/* comments open: the row shows its comments, the other cards stay folded */
.sx-row.sx-cm-on>.rv-right>.rv-card:not(.rv-note){display:none!important}
.sx-row.sx-cm-on>.rv-right>.rv-note.nt-new{display:none!important}
.sx-row.sx-add-on>.rv-right>.rv-card:not(.nt-new){display:none!important}
.sx-row.sx-cm-on>.rv-right>.rv-note{display:block!important}
.sx-row.sx-cm-on .sx-cmt{opacity:1;color:var(--ink,#333)}
.sx-wc{color:var(--mut);font-size:11.5px}
.sx-evm{font-family:"Source Serif 4",Georgia,serif}   /* the ❝ citation mark in one colour (JL 261113) */
.sx-row:not(.sx-fold) .sx-marks>.sx-wc{display:inline!important}
/* one card look beside the sentences (JL 261113: "the card style here is not fit well"): a thin grey line, white, the
   page's sans at one size; hover darkens the line, never orange; an edit keeps a muted left edge */
.sx-board .sx-row>.rv-right .rv-card:not(.rv-ev){border:1px solid color-mix(in srgb,var(--line,#ddd) 85%,transparent);
 border-radius:6px;background:var(--card,#fff);box-shadow:none;padding:8px 12px;font:13.5px/1.5 system-ui,-apple-system,sans-serif}
.sx-board .sx-row:hover>.rv-right>.rv-card:not(.rv-ev),.sx-board .sx-row>.rv-right>.rv-card.open:not(.rv-ev){
 border-color:color-mix(in srgb,var(--ink,#333) 28%,transparent)}
/* a card with choices has no coloured edge (JL 261113: "I don't want this"; 261114 again of the line at a row's edge) */
.sx-board .sx-row>.rv-right .rv-card.has-choice{border-left:1px solid var(--line)}
.sx-board .sx-row>.rv-right .rv-note .nt-box{font:14px/1.5 system-ui,-apple-system,sans-serif;border-radius:6px}
/* the history reads like the text: the sentence in the text's serif, its date and source small above it */
.sx-board .sx-histcard .sx-h{font-family:"Source Serif 4",Charter,"Iowan Old Style",Georgia,serif;font-size:16px;line-height:1.6;text-align:left}
.sx-board .sx-histcard .sx-hw{font:11.5px/1.4 system-ui,-apple-system,sans-serif;color:var(--mut)}
.sx-board .sx-histcard .sx-h.now .sx-hw{color:var(--ink,#333);font-weight:600}
/* evidence opened: a reference list, no lone icon line above it */
.sx-board .sx-row>.rv-right .rv-ev.open>.lg-head{display:none}
.sx-board .sx-row>.rv-right .rv-ev .ev-ref{font:14px/1.5 system-ui,-apple-system,sans-serif;color:var(--ink,#333);margin:2px 0}
.sx-board .sx-row>.rv-right .rv-ev .ev-ref a{color:inherit;text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--mut) 50%,transparent)}
.sx-board .sx-row>.rv-right .rv-ev .ev-run{font-size:11.5px;color:var(--mut);white-space:nowrap;margin-left:4px}
.sx-board .sx-row>.rv-right .rv-ev .ev-quote{font-size:13px;color:var(--mut);margin:0 0 4px 22px}
/* the review card in plain words: verdict, problem, suggestion */
/* a sentence that reads well needs no card until its ★ is clicked */
.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="8"],.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="9"],
.sx-row:not(.sx-rev-on)>.rv-right .rv-rev[data-low="10"]{display:none}
.sx-ai{cursor:pointer}
.sx-row>.rv-right .rv-rev .lg-head{display:flex;align-items:baseline;gap:10px}
.sx-row>.rv-right .rv-rev .lg-q{font-size:13.5px}
.sx-row>.rv-right .rv-rev .lg-sc{margin-left:auto;font-size:11.5px;color:var(--mut);white-space:nowrap}
.sx-row>.rv-right .rv-rev .lg-prob{margin:3px 0 0}
.sx-row>.rv-right .rv-rev .lg-sugg{margin:3px 0 0;color:var(--ink,#333)}
.sx-row>.rv-right .rv-rev .lg-lab{font-size:11.5px;font-weight:600;color:var(--mut);margin-right:4px}
/* the cards start where the sentence text starts (JL 261113: "why cards and sentences are not fully aligned") */
.sx-board.sx-ud .sx-row>.rv-right{padding-left:62px!important}
.sx-board.sx-ud .sx-row.sx-p>.rv-right,.sx-board.sx-ud .sx-row.sx-c>.rv-right{padding-left:22px!important}
.sx-row:not(.sx-fold) .sx-marks>.sx-cmt,.sx-row:not(.sx-fold) .sx-marks>.sx-ai{display:inline!important}
.sx-board .cite{white-space:normal}.cite-miss{font-size:.8em;color:#c92a2a;border:1px solid #f1aeb5;border-radius:4px;padding:0 3px}.sx-board .cite-ay{font-size:.9em;color:color-mix(in srgb,var(--ink,#333) 70%,transparent)}
.sx-board .cite-tex{font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);overflow-wrap:anywhere}
/* a checked ✓ is a soft grey-green chip; the sentence itself keeps its look (JL 261113: "the grey green I mean for
   this icon only, not the whole sentence element") */
.sx-board .sx-ok.on{color:#3f7a52;background:color-mix(in srgb,#5f9e72 18%,transparent);border-radius:9px;padding:0 6px;
 box-shadow:0 0 0 1px color-mix(in srgb,#5f9e72 35%,transparent)}
/* a narrow gutter (JL 261113: "the left right take a large space"): ▸, then the reading number with the fixed id
   small under it, in one 46px column; the + and 💬 float in the margin instead of holding a column on the right */
/* the number sits at the left edge, the text where it was (JL 261113: "the index can be a bit to the left") */
.sx-board .rv-left li[data-s]{display:grid!important;grid-template-columns:0 28px minmax(0,1fr) auto;column-gap:0;
 position:relative;align-items:baseline}
.sx-board .rv-left li[data-s]>.sx-tog{grid-column:1;grid-row:1;width:0;overflow:visible;flex:none}
.sx-board .rv-left li[data-s]>.s-ord{grid-column:2;grid-row:1;flex:none;padding:0;text-align:right}
.sx-board .rv-left li[data-s]>.s-no{grid-column:2;grid-row:2;flex:none;padding:0;text-align:right;font-size:10px;line-height:1.2}
.sx-board .rv-left li[data-s]>.s-tx{grid-column:3;grid-row:1/span 3;margin-left:34px}   /* air after the number (JL 261113: "this is too close") */
.sx-board .rv-left li[data-s]>.sx-marks{grid-column:4;grid-row:1}
.sx-board .rv-left li[data-s]>.nt-gut{position:absolute;right:-30px;top:2px;margin:0;padding:0}
/* the sentence just changed, found again after the page loads (sxKeep) */
/* a sentence scored below 7 looks like every other: its ★ is the only mark (JL 261114: "too alarming"; "no such a things") */
.sx-board .sx-flash{animation:sxflash 2.6s ease-out}
@keyframes sxflash{0%,35%{box-shadow:0 0 0 3px color-mix(in srgb,#e8a33d 70%,transparent);border-radius:6px}100%{box-shadow:0 0 0 3px transparent}}
/* the margin keeps only +: the old open-comment 💬 repeated the 💬N in the marks (JL 261114: "maybe we don't need it") */
.sx-board .nt-mark{display:none!important}
</style><script>
(function(){if(window.__sxRows)return;window.__sxRows=1;
 function marks(r){var g=r.querySelector('.rv-right');if(!g)return'';
  var ev=g.querySelectorAll('.rv-ev,.ev-card').length,w=g.querySelectorAll('.rv-card[data-state=proposed],.rv-card[data-state=open]').length,h=0;
  var pen=g.querySelectorAll('.rv-card:not(.sx-old):not(.rv-ev):not(.ev-card):not(.sx-histcard):not(.rv-rev):not(.rv-note)').length;
  /* 🕘 counts the sentence's earlier versions; 📝 its edits, current ones first and decided ones after (JL 261113) */
  g.querySelectorAll('.sx-histcard').forEach(function(c){h+=+(c.dataset.n||1);});var old=g.querySelectorAll('.sx-old:not(.sx-histcard)').length;
  var sum=function(k){var t=0;g.querySelectorAll('.rv-ev').forEach(function(c){t+=+(c.dataset[k]||0);});return t;};
  var nv=sum('value'),nc=sum('cite'),nd=sum('display'),ek='<span class=sx-evm role=button tabindex=0 title="';
  /* one mark per kind of evidence, each opening the sentence's cards (JL 261113: "how to add the things like the citation?") */
  var evm=(nv?ek+nv+' value'+(nv>1?'s':'')+'">📊'+nv+'</span>':'')+(nc?ek+nc+' citation'+(nc>1?'s':'')+'">❝︎'+nc+'</span>':'')
   +(nd?ek+nd+' display'+(nd>1?'s':'')+'">🖼️'+nd+'</span>':'')+(ev&&!(nv||nc||nd)?ek+'evidence">📎'+ev+'</span>':'');
  /* the reviewer's score, the lowest of logic, read and AI (JL 261113: "another icon should be AI rating"), and 💬 to
     comment on the sentence, with how many comments it has (JL 261113: "where is the things like the comments icon") */
  /* only a sentence's own review card carries a score; the paragraph Flow card (.rv-flow) has none and gave ★NaN (JL 261115) */var rv=g.querySelector('.rv-rev[data-low]'),lo=rv?+rv.dataset.low:0,nt=g.querySelectorAll('.rv-note:not(.nt-new)').length;
  var fx=rv&&rv.dataset.fixed,so=rv&&rv.dataset.stale;  /* fixed by the reviewer's words, or changed since: the score is old */
  var ai=rv?'<span class="sx-ai '+(so?'old':fx||lo>=8?'ok':lo>=7?'mid':'low')+'" role=button tabindex=0 title="'+(fx?'fixed since the review; ':so?'scored before the last change; ':'')+(rv.dataset.scores||'')+'">★'+(fx?'✓':so?'–':lo)+'</span>':'';
  /* the sentence's length in words, its citations left out (JL 261113: "could you also show the number of words") */
  var tx=r.querySelector('.rv-left li[data-s] .s-tx'),nw=0;
  if(tx){var cl=tx.cloneNode(true);cl.querySelectorAll('.cite,.sx-marks').forEach(function(x){x.remove();});
   nw=(cl.textContent.match(/[A-Za-z0-9][A-Za-z0-9'’.,%-]*/g)||[]).length;}
  /* the word count lives in the ★ card, not in the row (JL 261113: "I want the wc just in the star, I click it and see it") */
  /* 💬 only where there are comments (JL 261113: "if there are no comments, we can hide this icon"); a new one starts
     from the + in the margin */
  var cm=nt?'<span class=sx-cmt role=button tabindex=0 title="the comments on this sentence">💬'+nt+'</span>':'';
  /* ✓ the person's own pass on the sentence (JL 261113: "a button, which means check ... no need to modify it") */
  var li0=r.querySelector('.rv-left li[data-s]'),on=li0&&li0.dataset.checked==='1',st=li0&&li0.dataset.checked==='stale';
  cm=cm+(li0?'<span class="sx-ok'+(on?' on':st?' stale':'')+'" role=button tabindex=0 title="'+(on?'you checked this sentence; click to take it back':st?'you checked an earlier wording; the words changed, so check it again':'check: this sentence passes, leave it as it is')+'">'+(st?'✓?':'✓')+'</span>':'');   /* ✓ last (JL 261113) */
  return [w,ai+evm+(h?'<span class=sx-clk role=button tabindex=0 title="earlier versions of this sentence">🕘'+h+'</span>':'')
   +(pen||old?'<span class="sx-pen'+(w?' w':'')+(pen?'':' faint')+'" role=button tabindex=0 title="edits: '+pen+' current'+(w?' ('+w+' wait for you)':'')+', '+old+' decided">📝'+(pen||old)+'</span>':'')+cm];}
 /* ★ opens the reviewer's card on the sentence, a good one too (JL 261113: "when I click ★8, why there are no ...") */
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.sx-ai');if(!a)return;e.preventDefault();
  e.stopImmediatePropagation();var r=a.closest('.sx-row');if(!r)return;var on=!r.classList.contains('sx-rev-on');   /* its own toggle: ❝ or 🕘 open beside it do not count */
  /* a second click hides the cards again (JL 261113: "I want to hide it by clicking it, it doesn't work anymore") */
  r.classList.toggle('sx-rev-on',on);
  if(on){r.classList.remove('sx-fold');r.classList.add('sx-open');var c=r.querySelector('.rv-rev');if(c)c.classList.add('open');}
  else{r.classList.remove('sx-open','sx-hist');if(!r.classList.contains('sx-evon')&&!r.classList.contains('sx-ver'))r.classList.add('sx-fold');}},true);
 document.addEventListener('click',function(e){var k=e.target.closest&&e.target.closest('.sx-ok');if(!k)return;e.preventDefault();e.stopImmediatePropagation();   /* the ✓ only marks; it opens no card (JL 261113) */
  var li=k.closest('li[data-s]'),bd=k.closest('.rv-board'),on=!k.classList.contains('on');if(!li||!bd)return;
  fetch('/_board/draft-comment',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({task:bd.dataset.task,act:on?'check':'uncheck',s:li.dataset.a||li.dataset.s})})
   .then(function(r){return r.json();}).then(function(j){if(!j.ok){k.title=j.err||'not saved';return;}
    k.classList.toggle('on',j.checked);k.classList.remove('stale');k.textContent='✓';li.dataset.checked=j.checked?'1':'';
    k.title=j.checked?'you checked this sentence; click to take it back':'check: this sentence passes, leave it as it is';});},true);
 /* 💬 opens the sentence's comments: the earlier ones, then a box for a new one under them; a second click closes them
    (JL 261113: "does this mean adding the comments, or showing the previous comments? they are different right?") */
 document.addEventListener('click',function(e){var c=e.target.closest&&e.target.closest('.sx-cmt');if(!c)return;e.preventDefault();
  e.stopImmediatePropagation();var li=c.closest('li[data-s],h4[data-p],h3[data-p]'),r=c.closest('.sx-row');if(!li||!r)return;
  var g=r.querySelector('.rv-right');
  if(r.classList.contains('sx-cm-on')){r.classList.remove('sx-cm-on');
   if(r.dataset.cmWasFold==='1')r.classList.add('sx-fold');if(r.dataset.cmWasOpen!=='1')r.classList.remove('sx-open');return;}
  /* 💬 only shows the comments; the + in the margin only adds one (JL 261113: "how to make 💬1 to just show the
     comments, and + to just add the comments") */
  r.dataset.cmWasFold=r.classList.contains('sx-fold')?'1':'';r.dataset.cmWasOpen=r.classList.contains('sx-open')?'1':'';r.classList.add('sx-cm-on');r.classList.remove('sx-fold');r.classList.add('sx-open');
  g&&g.querySelectorAll('.rv-note:not(.nt-new)').forEach(function(n){n.classList.add('open');});},true);
 /* the + only adds a comment: it leaves the comments view, so its new box shows */
 document.addEventListener('click',function(e){var p=e.target.closest&&e.target.closest('.nt-plus');if(!p)return;
  var r=p.closest('.sx-row');if(!r)return;r.classList.remove('sx-cm-on');
  if(!r.classList.contains('sx-add-on')){r.dataset.addWasOpen=r.classList.contains('sx-open')?'1':'';r.classList.add('sx-add-on');}},true);
 /* the new box closed (Comment or Cancel): the row goes back to how it was */
 document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.nt-new [data-note-act=cancel],.nt-new [data-note-act=add]');
  if(!a)return;var r=a.closest('.sx-row');if(!r||!r.classList.contains('sx-add-on'))return;
  setTimeout(function(){if(r.querySelector('.rv-note.nt-new'))return;r.classList.remove('sx-add-on');
   if(r.dataset.addWasOpen!=='1')r.classList.remove('sx-open');},1200);},true);
 function fold(r,on){r.classList.toggle('sx-fold',on);if(on){r.classList.remove('sx-open','sx-hist');}else if(r.querySelector('.sx-sum'))r.classList.add('sx-open');}
 /* a paragraph folds its sentences; a Section folds its paragraphs and their sentences */
 window.sxPfold=pfold;function pfold(h,on){h.classList.toggle('sx-pfold',on);var sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){
   n.classList.toggle('sx-hide',on);if(!on)n.classList.remove('sx-pfold');n=n.nextElementSibling;}}
 /* row by row, as each arrives: the page streams in, so a board can be half drawn when this first runs */
 /* a card for a sentence not in the text yet (S14a, a new sentence after S14) sits under the sentence it follows */
 function adopt(){document.querySelectorAll('.sx-board .rv-card[data-s]').forEach(function(c){var s=c.dataset.s;
  if(!/^[Ss]\\d+[a-z]$/.test(s)||c.dataset.moved||document.querySelector('.sx-board .rv-left li[data-s="'+s+'"]'))return;
  var a=s.replace(/[a-z]$/,''),prev=String.fromCharCode(s.charCodeAt(s.length-1)-1),li=null;
  if(prev>='a')li=document.querySelector('.sx-board .rv-left li[data-s="'+a+prev+'"]');
  li=li||document.querySelector('.sx-board .rv-left li[data-s="'+a+'"]');var g=li&&li.closest('.sx-row')&&li.closest('.sx-row').querySelector('.rv-right');
  if(!g)return;c.dataset.moved=1;g.appendChild(c);if(c.dataset.state==='proposed'){c.classList.add('open');var row=g.closest('.sx-row');row.classList.remove('sx-fold');row.classList.add('sx-open');}});}
 setTimeout(function(){adopt();},1500);setTimeout(function(){adopt();},4000);
 function setup(){adopt();document.querySelectorAll('.sx-board .sx-row:not([data-sx])').forEach(function(r){r.dataset.sx=1;
  (function(){var li=r.querySelector('.rv-left li[data-s]'),h=r.querySelector('.rv-left h4[data-p]');
   if(li){var t=document.createElement('button');t.type='button';t.className='sx-tog';t.title='open or fold this sentence';
    li.insertBefore(t,li.firstChild);var o=document.createElement('span');o.className='s-ord';t.after(o);var m=marks(r),s=document.createElement('span');s.className='sx-marks';s.innerHTML=m?m[1]:'';
    (li.querySelector('.s-tx')||li).appendChild(s);/* the person's waiting edit cards show open, their change in view (JL 261114: "show them out in the UI ... currently all of them are hidden") */r.querySelectorAll('.rv-right .rv-card[data-state=proposed]').forEach(function(c){c.classList.add('open');});/* a sentence the reviewer scored below 7 on any axis stands out and opens on its edit cards (JL 261114: "for the sentence below 7, highlight and show what is the editing cards") */var rv7=r.querySelector('.rv-rev[data-low]'),lo7=rv7&&!rv7.dataset.fixed&&!rv7.dataset.stale?+rv7.dataset.low:10;if(lo7<7)r.classList.add('sx-low');fold(r,!(m&&m[0])&&lo7>=7);}
   else if(r.classList.contains('sx-p')||r.classList.contains('sx-c')){h=h||r.querySelector('.rv-left h3[data-p]');if(!h)return;
    var p=document.createElement('button');p.type='button';p.className='sx-ptog';
    p.title=r.classList.contains('sx-c')?'fold or open this Section':'fold or open this paragraph';h.insertBefore(p,h.firstChild);
    var pm=marks(r),ps=document.createElement('span');ps.className='sx-marks';ps.innerHTML=pm?pm[1]:'';h.appendChild(ps);}})();});order();}
 /* each sentence's place in reading order, counted again in each part (C1 title, C2 text, C3 keywords) */
 /* a paragraph is numbered as a sentence is (JL 261113: "it should be just like the sentences"): its place in reading
    order large, its fixed id (C1.P30) small after its title, so P30 no longer reads as if P4 to P29 were missing */
 function porder(){document.querySelectorAll('.sx-board').forEach(function(b){var m=0;
  b.querySelectorAll('h3.rv-part,.rv-left h4[data-p]').forEach(function(h){if(h.tagName==='H3'){m=0;return;}m+=1;
   var o=h.querySelector(':scope>.p-ord');
   if(!o){var tn=[].find.call(h.childNodes,function(c){return c.nodeType===3&&/C\\d+\\.P\\d+\\s*·/.test(c.nodeValue);});
    if(tn){tn.nodeValue=tn.nodeValue.replace(/^\\s*C\\d+\\.P\\d+\\s*·\\s*/,'');}
    o=document.createElement('span');o.className='p-ord';var tg=h.querySelector(':scope>.sx-ptog');h.insertBefore(o,tg?tg.nextSibling:h.firstChild);
    var id=document.createElement('span');id.className='p-no';id.textContent=h.dataset.p.split('.').pop();
    var mk=h.querySelector(':scope>.sx-marks,:scope>.nt-gut');h.insertBefore(id,mk||null);}
   o.textContent=m;o.title='paragraph '+m+' in reading order; '+h.dataset.p+' is its fixed id';});});}
 /* paragraphs keep their old fixed id, "C2.P2 · title" (JL 261113: "I want the old paragraph index, current one
    is so ugly"); porder stays unused */
 /* the large number counts again in each paragraph (JL 261114: "it is section level, how could we make it sentence
    level"): 1, 2, 3 within the paragraph; the fixed id (S7) stays small under it, as cards and comments name it */
 function order(){document.querySelectorAll('.sx-board').forEach(function(b){var n=0;
  b.querySelectorAll('h3.rv-part,.rv-left h4[data-p],.rv-left li[data-s]').forEach(function(x){if(x.tagName==='H3'||x.tagName==='H4'){n=0;return;}
   var o=x.querySelector(':scope>.s-ord');if(!o)return;n+=1;o.textContent=n;o.title='sentence '+n+' of its paragraph; '+
   (x.dataset.a||x.dataset.s)+' is its fixed id';});});}
 document.addEventListener('click',function(e){if(!e.target.closest)return;
  /* ❝ 📊 🖼️ open the sentence's evidence only, on their own toggle (JL 261113: "when I click it, there are not reaction"):
     sharing the 📝 toggle, a click on ❝ after ★ had opened the row closed it again */
  var v=e.target.closest('.sx-evm');if(v){e.preventDefault();e.stopPropagation();var vr=v.closest('.sx-row');
   vr.classList.remove('sx-fold');vr.classList.toggle('sx-evon');return;}
  var q=e.target.closest('.sx-pen');if(q){e.preventDefault();e.stopPropagation();var qr=q.closest('.sx-row');
   qr.classList.remove('sx-fold');var qon=!qr.classList.contains('sx-open');qr.classList.toggle('sx-open',qon);qr.classList.toggle('sx-hist',qon);return;}
  var k=e.target.closest('.sx-clk');if(k){e.preventDefault();e.stopPropagation();var kr=k.closest('.sx-row');
   kr.classList.remove('sx-fold');kr.classList.toggle('sx-ver');return;}
  var t=e.target.closest('.sx-tog');if(t){e.preventDefault();e.stopPropagation();var r=t.closest('.sx-row');fold(r,!r.classList.contains('sx-fold'));return;}
  var p=e.target.closest('.sx-ptog');if(p){e.preventDefault();e.stopPropagation();var h=p.closest('.sx-row');pfold(h,!h.classList.contains('sx-pfold'));return;}
  var a=e.target.closest('[data-sx-all]');if(a){e.preventDefault();var b=a.closest('.sx-board'),on=a.dataset.sxAll==='fold';
   b.querySelectorAll('.sx-row.sx-p,.sx-row.sx-c').forEach(function(h){pfold(h,false);});
   b.querySelectorAll('.sx-row').forEach(function(r){if(r.querySelector('.sx-tog'))fold(r,on);});return;}
  var li=e.target.closest('.sx-row.sx-fold .rv-left li[data-s]');if(li&&!e.target.closest('a')){e.preventDefault();fold(li.closest('.sx-row'),false);}},true);
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup);else setup();
 /* a row's cards can stream in after its row was set up, so its marks are counted again once the page is whole
    (S6a lost its 📊 and 🕘 when its cards came late) */
 /* after a written change the page loads again; it comes back to the same sentence, flashed, instead of the top
    (JL 261114: "the focal sentence is jump to another places and it is hard for me to find") */
 /* a confirmed card or ✓ Use this changes its sentence IN PLACE, no reload (JL 261114: "the changes is not realy time ... it
    seems to be of stuck": each write reloaded the page, 2 s white and a jump); a sentence with citations or maths, whose
    words the page renders, still reloads */
 window.sxInPlace=function(el,words){try{var r=el&&el.closest&&el.closest('.sx-row'),tx=r&&r.querySelector('.rv-left li[data-s] .s-tx');
  if(!tx||words==null)return false;var cs=el.closest&&el.closest('.rv-card');if(cs&&cs.dataset.s&&cs.dataset.s!==tx.closest('li').dataset.s)return false;   /* a new sentence's card reloads */words=String(words).replace(/^\\s*["\u201c]([\\s\\S]*)["\u201d]\\s*$/,'$1').trim();
  if(/\\\\[a-zA-Z]|\\$/.test(words)||tx.querySelector('.cite,.katex'))return false;
  if(words==='(cut)')return false;   /* a cut renumbers the paragraph, so the page reloads (JL 261114: numbers read 1, 2, 3, 6, 7) */
  var mk=tx.querySelector('.sx-marks');Array.prototype.slice.call(tx.childNodes).forEach(function(n){if(n!==mk&&!(n.classList&&n.classList.contains('mut')))tx.removeChild(n);});
  tx.insertBefore(document.createTextNode(words+' '),mk||null);var rv=r.querySelector('.rv-rev[data-low]');if(rv)rv.dataset.fixed='1';
  r.classList.remove('sx-low');window.sxQuiet=Date.now()+6000;if(window.sxRemark)window.sxRemark();
  r.classList.remove('sx-flash');void r.offsetWidth;var li=r.querySelector('.rv-left li[data-s]');if(li){li.classList.add('sx-flash');}return true;}catch(x){return false;}};
 window.sxKeep=function(el){try{var r=el&&el.closest&&el.closest('.sx-row'),li=r&&r.querySelector('.rv-left li[data-s]');
  if(li)sessionStorage.setItem('sx-keep',li.dataset.a||li.dataset.s);}catch(x){}};
 (function(){var k=null;try{k=sessionStorage.getItem('sx-keep');sessionStorage.removeItem('sx-keep');}catch(x){}if(!k)return;window.sxKept=k;
  var n=0;(function go(){var li=document.querySelector('.sx-board .rv-left li[data-a="'+k+'"]')||document.querySelector('.sx-board .rv-left li[data-s="'+k+'"]');
   if(!li){if(++n<40)setTimeout(go,150);return;}
   var row=li.closest('.sx-row'),hs=[];for(var x=row&&row.previousElementSibling;x;x=x.previousElementSibling){
    if(x.classList.contains('sx-c')){hs.unshift(x);break;}if(x.classList.contains('sx-p')&&!hs.length)hs.push(x);}
   hs.forEach(function(h){if(h.classList.contains('sx-pfold')&&window.sxPfold)window.sxPfold(h,false);});   /* open its folded paragraph */
   var land=function(){li.scrollIntoView({block:'center'});};land();setTimeout(land,700);
   var r=li.closest('.sx-row')||li;r.classList.add('sx-flash');setTimeout(function(){r.classList.remove('sx-flash');},2600);})();})();
 /* ✓ Use this on a reviewer's suggestion: an accepted Edit card with its words (card_act adopt), then the page again */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.lg-use');if(!b)return;
  e.preventDefault();e.stopPropagation();var t=b.closest('[data-task]')||document.querySelector('[data-task]'),m=b.nextElementSibling;
  if(!t){if(m)m.textContent='no Task here';return;}b.disabled=true;
  fetch('/_board/draft-card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task:t.dataset.task,
   act:'adopt',s:b.dataset.adopt,original:b.dataset.orig,expected:b.dataset.new})}).then(function(r){return r.json();})
   .then(function(j){if(!j.ok){b.disabled=false;if(m)m.textContent=j.err||'not saved';return;}if(m)m.textContent='accepted';
    if(window.sxInPlace&&window.sxInPlace(b,b.dataset.new)){if(m)m.textContent='written into the text';return;}
    setTimeout(function(){if(window.sxKeep)window.sxKeep(b);location.reload();},400);}).catch(function(x){b.disabled=false;if(m)m.textContent=String(x);});},true);
 /* 🔄 the page follows its files (JL 261114: "How to make the UI to be auto refreshed to show the changes?"): every 4 s
    it asks /_board/draft-stamp for the folder's newest change; when that moves and the reader is not typing, editing a
    card, writing a comment or selecting text, it reloads and comes back to the sentence in view (sxKeep) */
 (function live(){if(window.__sxLive)return;var bd=document.querySelector('.rv-board[data-task]');
  if(!bd){setTimeout(live,1000);return;}window.__sxLive=1;   /* the board streams in after this script */
  var url='/_board/draft-stamp?path='+encodeURIComponent(bd.dataset.task),last=null,due=false;
  function busy(){var a=document.activeElement;if(a&&(a.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)))return true;
   if(document.querySelector('.rv-card.editing,.rv-note.writing,.rv-note.nt-new'))return true;
   var sel=window.getSelection&&window.getSelection();return !!(sel&&String(sel).trim());}
  function inView(){var best=null,d=1e9,mid=innerHeight/2;document.querySelectorAll('.sx-board .rv-left li[data-s]').forEach(function(li){
   var r=li.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;var x=Math.abs((r.top+r.bottom)/2-mid);if(x<d){d=x;best=li;}});return best;}
  function reload(){var li=inView();if(li&&window.sxKeep)window.sxKeep(li);location.reload();}
  function tick(){if(document.hidden)return;fetch(url,{cache:'no-store'}).then(function(r){return r.json();}).then(function(j){
   if(last===null||Date.now()<(window.sxQuiet||0)){last=j.stamp;due=false;return;}if(j.stamp!==last){last=j.stamp;due=true;}
   if(due&&window.sxPill)window.sxPill(reload);else if(due&&!busy())reload();}).catch(function(){});}
  setInterval(tick,4000);tick();})();
 window.sxRemark=function(){remark();};
 function remark(){document.querySelectorAll('.sx-board .sx-row[data-sx]').forEach(function(r){
  var li=r.querySelector('.rv-left li[data-s]'),s=li&&li.querySelector('.sx-marks');if(!s)return;var m=marks(r);
  /* compare with the last marks written, never with innerHTML: the browser rewrites quotes, so innerHTML never equals
     the string, and each rewrite fired the observer again, every frame; a ✓ swapped out between mouse down and up lost
     its click (JL 261113: "the check doesn't work anymore") */
  if(m&&s.dataset.m!==m[1]){s.innerHTML=m[1];s.dataset.m=m[1];}});}
 document.addEventListener('DOMContentLoaded',remark);window.addEventListener('load',remark);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))setup();
  if(document.readyState==='complete')remark();});}).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>"""
