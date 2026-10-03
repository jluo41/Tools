(function(){
  'use strict';
  var configNode=document.getElementById('wb-guide-mount');if(!configNode)return;
  var config=JSON.parse(configNode.textContent), nav=document.querySelector(config.nav);if(!nav)return;
  var native=Array.from(document.querySelectorAll(config.native));
  native.forEach(function(node){node.classList.add('wb-guide-native')});nav.classList.add('wb-guide-nav');
  var button=document.createElement('button');button.type='button';button.className='wb-guide-button';button.textContent='Guide';
  button.setAttribute('aria-selected','false');button.setAttribute('aria-controls','wb-guide-frame');
  if(nav.getAttribute('role')==='tablist')button.setAttribute('role','tab');
  var navLabel=nav.firstElementChild;
  if(navLabel&&navLabel.tagName==='SPAN')navLabel.after(button);else nav.prepend(button);
  var frame=document.createElement('iframe');frame.id='wb-guide-frame';frame.className='wb-guide-frame';frame.title=config.family+' Guide';frame.hidden=true;
  nav.after(frame);
  var remembered=new Map();
  function open(view){
    view=['skill-set','methods','workbench','folder-map','roadmap-draw'].indexOf(view)>=0?view:'skill-set';
    var parameters=new URLSearchParams(config.context);parameters.set('family',config.family);parameters.set('view',view);parameters.set('embed','1');
    var source='/_board/guide?'+parameters.toString();
    if(frame.getAttribute('src')!==source)frame.src=source;
    frame.hidden=false;document.body.classList.add('wb-guide-open');button.setAttribute('aria-selected','true');
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
