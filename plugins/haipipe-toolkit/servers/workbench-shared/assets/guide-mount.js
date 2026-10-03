(function(){
  'use strict';
  // A trackpad pinch or ctrl-scroll zooms the whole tab, every 127.0.0.1 port at once, and on a workbench
  // it only happens by accident (JL 261003: "zoom in and zoom out very quickly"). Keyboard zoom still works;
  // an Excalidraw canvas is its own document and keeps its own pinch zoom.
  if(!window.__wbNoPinch){window.__wbNoPinch=true;
    addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false});
    ['gesturestart','gesturechange','gestureend'].forEach(function(t){addEventListener(t,function(e){e.preventDefault()},{passive:false})});}
  var configNode=document.getElementById('wb-guide-mount');if(!configNode)return;
  var config=JSON.parse(configNode.textContent), nav=document.querySelector(config.nav);if(!nav)return;
  var native=Array.from(document.querySelectorAll(config.native));
  native.forEach(function(node){node.classList.add('wb-guide-native')});nav.classList.add('wb-guide-nav');
  var button=document.createElement('button');button.type='button';button.className='wb-guide-button';button.textContent='Guide';
  button.setAttribute('aria-selected','false');button.setAttribute('aria-controls','wb-guide-frame');
  if(nav.getAttribute('role')==='tablist')button.setAttribute('role','tab');
  var navLabel=nav.firstElementChild;
  // Guide's look is guide-mount.css; the workbenches' own tabs follow it (JL 261003: "follow this style")
  if(navLabel&&navLabel.tagName==='SPAN')navLabel.after(button);else nav.prepend(button);
  var frame=document.createElement('iframe');frame.id='wb-guide-frame';frame.className='wb-guide-frame';frame.title=config.family+' Guide';frame.hidden=true;
  nav.after(frame);
  var remembered=new Map();
  function open(view){
    var old={'skill-set':'roadmap-draw',methods:'method',workbench:'roadmap-draw','folder-map':'roadmap-draw'};
    view=old[view]||view;view=['description','method','roadmap-draw','related-paper'].indexOf(view)>=0?view:'description';
    var parameters=new URLSearchParams(config.context);parameters.set('family',config.family);parameters.set('view',view);parameters.set('embed','1');
    var source='/_board/guide?'+parameters.toString();
    if(frame.getAttribute('src')!==source)frame.src=source;
    frame.hidden=false;document.body.classList.add('wb-guide-open');button.setAttribute('aria-selected','true');
    // A canvas inside Guide takes focus as it loads, and the browser scrolls this page to it, past the Space
    // tabs (JL 261003: "where are other spaces?"). Hold the scroll for a few seconds unless the person moves it.
    var keep=scrollY,until=Date.now()+6000,moved=false;
    function mark(){moved=true}
    ['wheel','keydown','touchstart','pointerdown'].forEach(function(t){addEventListener(t,mark,{passive:true,once:true})});
    function hold(){if(Date.now()>until){removeEventListener('scroll',hold);return}if(!moved&&Math.abs(scrollY-keep)>2)scrollTo(scrollX,keep)}
    addEventListener('scroll',hold);
    Array.from(nav.querySelectorAll('[aria-selected]:not(.wb-guide-button)')).forEach(function(item){
      if(!remembered.has(item))remembered.set(item,item.getAttribute('aria-selected'));item.setAttribute('aria-selected','false');
    });
    var address=new URL(location.href);address.searchParams.set('guide',view);history.replaceState({},'',address);
  }
  function close(){
    frame.hidden=true;document.body.classList.remove('wb-guide-open');button.setAttribute('aria-selected','false');
    remembered.forEach(function(value,item){item.setAttribute('aria-selected',value)});remembered.clear();
    var address=new URL(location.href);address.searchParams.delete('guide');history.replaceState({},'',address);
  }
  button.addEventListener('click',function(event){event.stopPropagation();open(new URL(location.href).searchParams.get('guide'))});
  nav.addEventListener('click',function(event){if(!button.contains(event.target)&&event.target.closest('button,a'))close()},true);
  addEventListener('message',function(event){
    if(event.origin!==location.origin||event.source!==frame.contentWindow||event.data?.kind!=='haipipe-guide-height')return;
    var value=Number(event.data.height);if(Number.isFinite(value)&&value>0&&value<100000)frame.style.height=Math.ceil(value)+'px';
    if(document.body.classList.contains('wb-guide-open')){
      var address=new URL(location.href);address.searchParams.set('guide',event.data.view);history.replaceState({},'',address);
    }
  });
  var requested=new URL(location.href).searchParams.get('guide');if(requested)open(requested);
})();
