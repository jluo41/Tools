(function () {
  var KEY = 'board-comments:' + location.pathname;
  var UK = 'board-users', WK = 'board-user-last';
  var db = [], users = [];
  try { db = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { db = []; }
  try { users = JSON.parse(localStorage.getItem(UK) || 'null') || ['JL','CC']; }
  catch (e) { users = ['JL','CC']; }
  users = users.filter(function (u) { return u !== 'RA'; });
  if (!users.length) users = ['JL','CC'];
  localStorage.setItem(UK, JSON.stringify(users));
  if (localStorage.getItem(WK) === 'RA') localStorage.removeItem(WK);
  var pend = null;

  function mk(tag, id, html) {
    var e = document.createElement(tag); e.id = id; e.innerHTML = html || ''; return e;
  }
  var btn = mk('button', 'cbtn', '\u{1F4AC} Comment');
  var box = mk('div', 'cbox',
    '<div class="qq"></div><textarea placeholder="Write a comment…"></textarea>' +
    '<div class="row"><select></select><span style="flex:1"></span>' +
    '<button class="cx">Cancel</button><button class="ok cs">Save</button></div>' +
    '<input class="nu" placeholder="New initials, e.g. ZW — press Enter">');
  var dock = mk('button', 'cdock', '');
  var panel = mk('div', 'cpanel', '');
  var toast = mk('div', 'ctoast', '');
  [btn, box, dock, panel, toast].forEach(function (e) { document.body.appendChild(e); });

  function save() { localStorage.setItem(KEY, JSON.stringify(db)); marks(); paint(); }
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.style.display = 'none'; }, 3000);
  }
