(function(){
  'use strict';
  var boot=JSON.parse(document.getElementById('wg-boot').textContent);
  var key='haipipe-guide-folds:'+boot.family+':'+boot.context.path+':'+boot.context.file+':'+boot.view;
  var folds=Array.from(document.querySelectorAll('.wg-drawing'));
  function load(fold){
    if(!fold.open)return;
    var frame=fold.querySelector('iframe[data-src]');
    // Keep the iframe alive on collapse: pan/zoom and other local view state survive.
    if(!frame.hasAttribute('src'))frame.src=frame.dataset.src;
  }
  function height(){
    if(parent!==window)parent.postMessage({kind:'haipipe-guide-height',height:document.body.getBoundingClientRect().height,view:boot.view},location.origin);
  }
  try{var saved=JSON.parse(sessionStorage.getItem(key));if(Array.isArray(saved))folds.forEach(function(f){f.open=saved.indexOf(f.dataset.drawing)>=0})}catch(e){}
  folds.forEach(function(fold){load(fold);fold.addEventListener('toggle',function(){
    load(fold);try{sessionStorage.setItem(key,JSON.stringify(folds.filter(function(f){return f.open}).map(function(f){return f.dataset.drawing})))}catch(e){}
    height();
  })});
  if(typeof ResizeObserver!=='undefined')new ResizeObserver(height).observe(document.body);
  addEventListener('load',height);height();
})();
