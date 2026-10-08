(function(){
  'use strict';
  // A trackpad pinch or ctrl-scroll zooms the whole tab, every 127.0.0.1 port at once, and on a workbench
  // it only happens by accident (JL 261003: "zoom in and zoom out very quickly"). Keyboard zoom still works;
  // an Excalidraw canvas is its own document and keeps its own pinch zoom.
  if(!window.__wbNoPinch){window.__wbNoPinch=true;
    addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false});
    ['gesturestart','gesturechange','gestureend'].forEach(function(t){addEventListener(t,function(e){e.preventDefault()},{passive:false})});}
  var boot=JSON.parse(document.getElementById('wg-boot').textContent);
  var key='haipipe-guide-folds:'+boot.family+':'+boot.context.path+':'+boot.context.file+':'+boot.view;
  // the drawing cards and, in the card Guide, the Block · Job · Task sections (b03 s31-D07): the server opens
  // the section of the level the Guide was opened from; a person's own folds, once made, are kept
  var folds=Array.from(document.querySelectorAll('.wg-drawing,.wg-level'));
  function load(fold){
    if(!fold.open)return;
    var frame=fold.querySelector('iframe[data-src]');if(!frame)return;  // a design-drawing fold loads its own src
    // Keep the iframe alive on collapse: pan/zoom and other local view state survive.
    if(frame&&!frame.hasAttribute('src'))frame.src=frame.dataset.src;   // an explanation fold loads at once
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
