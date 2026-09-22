(function () {
  // The Page has no comment composer. Shared helpers also serve explicit workbench workspaces.
  function mk(tag, id, html) {
    var e = document.createElement(tag); e.id = id; e.innerHTML = html || ''; return e;
  }
  var btn = mk('button', 'cbtn', '⧉ Copy prompt');
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Copy prompt for selected passage');
  var toast = mk('div', 'ctoast', '');
  [btn, toast].forEach(function (e) { document.body.appendChild(e); });
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.style.display = 'none'; }, 3000);
  }
