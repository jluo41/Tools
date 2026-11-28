/* Studio selects content; hai-mindmap owns all map interaction. */
(function(){
 'use strict';
 function render(){
  const hash=location.hash.slice(1)||'jobs-rules';
  const key=hash.replace(/-draw$/,'');
  const draw=hash.endsWith('-draw');
  document.body.dataset.mode=draw?'draw':'structure';
  const id=document.getElementById(key)?key:'jobs-rules';
  document.querySelectorAll('main>section').forEach(s=>s.hidden=s.id!==id);
  if(window.pmDraw)requestAnimationFrame(window.pmDraw);
 }
 window.addEventListener('hashchange',render);
 render();
})();
