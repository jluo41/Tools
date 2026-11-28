"""A row of view buttons that stays one line (s07 Topic rows preview, JL 261125 20:50: "what I want is this
version"): it never wraps; what does not fit scrolls sideways under a faded edge, a mouse can drag it, and the picked
button is scrolled into view. Any `<nav class="jrow">` gets this; `window.jrowFit(row)` re-measures a row just shown."""

CSS = """<style>
.jrow{flex-wrap:nowrap!important;overflow:auto hidden;overscroll-behavior-x:contain;scrollbar-width:none;padding:2px;margin-left:-2px;margin-right:-2px;--fs:0px;--fe:0px}
.jrow::-webkit-scrollbar{display:none}.jrow>*{flex:none}.jrow a{white-space:nowrap}
.jrow.scrollable{cursor:grab;-webkit-mask-image:linear-gradient(to right,transparent,#000 var(--fs),#000 calc(100% - var(--fe)),transparent);mask-image:linear-gradient(to right,transparent,#000 var(--fs),#000 calc(100% - var(--fe)),transparent)}
.jrow.at-start-no{--fs:10px}.jrow.at-end-no{--fe:14px}.jrow.dragging{cursor:grabbing}.jrow.scrollable a{cursor:inherit;user-select:none;-webkit-user-select:none}
</style>"""

JS = """<script>(function(){if(window.jrowFit)return;
function fit(r){var lim=r.scrollWidth-r.clientWidth;r.classList.toggle('scrollable',lim>1);
 r.classList.toggle('at-start-no',r.scrollLeft>1);r.classList.toggle('at-end-no',lim-r.scrollLeft>1);
 var c=r.querySelector('[aria-current]');if(c&&!c.hidden){var b=r.getBoundingClientRect(),x=c.getBoundingClientRect();
  if(x.left<b.left+2)r.scrollLeft+=x.left-b.left-12;else if(x.right>b.right-2)r.scrollLeft+=x.right-b.right+16;}}
window.jrowFit=fit;
function wire(r){if(r.__jrow)return;r.__jrow=1;var d=null,stop=false;
 r.addEventListener('scroll',function(){r.classList.toggle('at-start-no',r.scrollLeft>1);
  r.classList.toggle('at-end-no',r.scrollWidth-r.clientWidth-r.scrollLeft>1);},{passive:true});
 r.addEventListener('pointerdown',function(e){stop=false;if(e.pointerType!=='mouse'||e.button||r.scrollWidth<=r.clientWidth)return;
  d={id:e.pointerId,x:e.clientX,o:r.scrollLeft,on:false};});
 r.addEventListener('pointermove',function(e){if(!d||d.id!==e.pointerId)return;if(!(e.buttons&1)){d=null;r.classList.remove('dragging');return;}
  var k=e.clientX-d.x;if(!d.on){if(Math.abs(k)<6)return;d.on=true;stop=true;r.setPointerCapture(e.pointerId);r.classList.add('dragging');}
  r.scrollLeft=d.o-k;e.preventDefault();});
 ['pointerup','pointercancel','lostpointercapture'].forEach(function(n){r.addEventListener(n,function(){d=null;r.classList.remove('dragging');});});
 r.addEventListener('click',function(e){if(stop&&e.detail){e.preventDefault();e.stopImmediatePropagation();}stop=false;},true);
 if(window.ResizeObserver)new ResizeObserver(function(){fit(r);}).observe(r);fit(r);}
function all(){document.querySelectorAll('.jrow').forEach(wire);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',all);else all();
})();</script>"""
