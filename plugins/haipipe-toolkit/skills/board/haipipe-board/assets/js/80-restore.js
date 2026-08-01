/* ── the reload must not cost you your place (QD2/QD6, JL 260731) ──────────
   Two reports, one cause. When BUILD ships new assets, the tab must take the
   new JS, and the asset-stamp guard reloads it — deferred while a turn runs,
   so it lands the moment the turn ends. A full reload destroys the drawer's
   transcript ("第二个 talk 的时候 thinking 都不见了") and re-collapses every
   section you had opened ("我一旦打开它，它就应该一直在那，直到我选择把它关上").
   The reload itself is right: stale JS wiring new markup is worse. So make it
   lossless instead: remember what was open before unload, put it back after.
   Sections persist across sessions because that is what "until I close it"
   means; the drawer's open/closed state is per tab, like the tab itself. */
(function () {
  var DK = 'board-open:' + location.pathname;     // sections, sticky
  var CK = 'board-drawer:' + location.pathname;   // drawer, this tab only

  function key(d) {
    var s = d.querySelector('summary');
    return s ? s.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  function save() {
    try {
      var open = [];
      document.querySelectorAll('div.wrap details[open]').forEach(function (d) {
        var k = key(d); if (k) open.push(k);
      });
      localStorage.setItem(DK, JSON.stringify(open));
      sessionStorage.setItem(CK, JSON.stringify({
        on: !!(window.__boardDrawerOpen && window.__boardDrawerOpen()),
        term: !!(window.__boardTermOn && window.__boardTermOn()),
        y: Math.round(window.scrollY)
      }));
    } catch (e) {}
  }
  function restoreSections() {
    var want = {}, n = 0;
    try { (JSON.parse(localStorage.getItem(DK)) || []).forEach(function (k) { want[k] = 1; n++; }); }
    catch (e) { return; }
    if (!n) return;
    document.querySelectorAll('div.wrap details').forEach(function (d) {
      if (want[key(d)]) d.open = true;
    });
  }

  /* LOAD ONLY. Replaying the drawer on every router swap would fight the user:
     close it, navigate, and the saved "it was open" would reopen it. A swap is
     not a new page load, and `follow()` already keeps an open drawer bound. */
  function restoreDrawer() {
    var st;
    try { st = JSON.parse(sessionStorage.getItem(CK) || 'null'); } catch (e) { st = null; }
    if (!st) return;
    if (st.y) window.scrollTo(0, st.y);
    /* Reopening replays this page's saved log, so the conversation comes back
       even though the live trace of the interrupted turn cannot. */
    if (st.on && window.__boardDrawerReopen) {
      try {
        var opened = window.__boardDrawerReopen();
        /* A parked PTY is still running, so a drawer that comes back showing the
           chat box is showing the wrong half of QD1's one-session-per-page Law.
           Reattach to the terminal if one is genuinely still alive; the check
           lives in __boardTermReopen so a reload never SPAWNS one. */
        if (st.term && window.__boardTermReopen) {
          Promise.resolve(opened).then(function () {
            try { window.__boardTermReopen(); } catch (e) {}
          });
        }
      } catch (e) {}
    }
  }

  window.addEventListener('pagehide', save);      // fires on reload AND on close
  window.addEventListener('beforeunload', save);
  /* Saving ONLY at unload leaves one gap that reads as the feature not working
     at all (JL 260801, twice): a tab running JS from before this block existed
     never wrote anything, so the FIRST refresh after it opened the drawer has
     nothing to restore from, and only the second one works. Some mobile
     browsers also drop `beforeunload` entirely. So record the drawer the moment
     it opens or closes: one class flip on #chat, watched directly, no coupling
     to the chat code. */
  var chatEl = document.getElementById('chat');
  if (window.MutationObserver) {
    var watch = new MutationObserver(save);
    if (chatEl) watch.observe(chatEl, { attributes: true, attributeFilter: ['class'] });
    /* <body> too, and not as belt-and-braces: opening the terminal toggles
       `termon` on BODY and touches nothing on #chat, so watching only the
       drawer meant the terminal view was never recorded when it opened, and
       the flag existed only if `pagehide` happened to run (JL 260801: "still
       the same problem, when I refresh it switches from terminal to GUI"). */
    watch.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  window.addEventListener('board:updated', restoreSections);
  restoreSections();
  restoreDrawer();
})();
