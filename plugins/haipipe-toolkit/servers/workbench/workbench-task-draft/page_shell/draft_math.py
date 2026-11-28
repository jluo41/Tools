"""Draft Lab typesets the paper's LaTeX math: $$…$$ and \\[…\\] as display, $…$ and \\(…\\) inline, by KaTeX's
auto-render (cdnjs, version pinned), on each row as the board streams in. The source keeps its LaTeX; \\citep and \\ref
are printed by draft_card_text before this runs, and a text box being edited is never typeset."""

KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"

MATH_JS = f"""<link rel=stylesheet href="{KATEX}/katex.min.css">
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"></script>
<script>(function(){{if(window.sxMath)return;window.sxMath=1;
 var opts={{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\[',right:'\\\\]',display:true}},
  {{left:'\\\\(',right:'\\\\)',display:false}},{{left:'$',right:'$',display:false}}],throwOnError:false,
  ignoredTags:['script','noscript','style','textarea','pre','code','option','input'],ignoredClasses:['rv-edit','editing']}};
 function run(){{if(!window.renderMathInElement)return;
  document.querySelectorAll('.sx-board .sx-row:not([data-math])').forEach(function(r){{
   // a Revise card keeps an empty edit box (rv-edit, contenteditable) in every row: skip only a box being typed in,
   // and leave edit boxes untyped (ignoredClasses), so the sentence beside it is still typeset (JL 261116)
   if(r.querySelector('.editing,[contenteditable]:focus'))return;r.dataset.math=1;
   if(/\\$|\\\\[(\\[]/.test(r.textContent))window.renderMathInElement(r,opts);}});}}
 window.addEventListener('load',run);
 var due=0;new MutationObserver(function(){{if(due)return;due=1;requestAnimationFrame(function(){{due=0;run();}});}})
  .observe(document.documentElement,{{childList:true,subtree:true}});
}})();</script>"""
