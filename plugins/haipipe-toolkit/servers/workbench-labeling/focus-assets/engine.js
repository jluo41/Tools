(() => {
  function flatten() {
    document.querySelectorAll('details').forEach(d => {
      const s = document.createElement('section');
      [...d.attributes].forEach(a => { if (a.name !== 'open') s.setAttribute(a.name, a.value); });
      s.dataset.staticContent = 'true';
      const heading = d.querySelector(':scope > summary');
      if (heading) { const h = document.createElement('div'); h.setAttribute('role','heading'); h.setAttribute('aria-level','3'); h.append(...heading.childNodes); heading.replaceWith(h); }
      s.append(...d.childNodes); d.replaceWith(s);
    });
  }
  let queued = false;
  function update() {
    if (queued) return; queued = true;
    requestAnimationFrame(() => {
      queued = false; flatten();
      const height = Math.ceil(document.body.getBoundingClientRect().height) + 20;
      parent.postMessage({type:'labeling-focus:height',height}, location.origin);
    });
  }
  new MutationObserver(update).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden','class']});
  new ResizeObserver(update).observe(document.body);
  update();
})();
