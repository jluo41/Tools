/* 📄 Page phases · internal lifecycle view (no Plugin row).
 *
 * The Page phases view remains a LOOP — OUTLINE/EVIDENCE
 * (the OUTLINE part) then DRAFT/REVISE/COMPILE/CHECK (the DRAFT part), selected by
 * authority, CHECK routes backward, and
 * only CHECK may CLOSE. So this surface lights the last acted phase and names where
 * it routed; it draws no locks, because the loop has none. SEVEN since 260817, four
 * before it: haipipe-page-workflow §"Why each split" carries the reason for each.
 *
 * INDEX LEFT, CONTENT RIGHT (JL 260816: "把 workflow 放在最左边…跟具体的内容分开").
 * The LEFT column is an index — ① 🧭 OUTLINE … ⑦ ✅ CHECK, names only, one row per
 * phase — and the RIGHT column holds the selected phase's content plus the run
 * record, the same left-index-right-content language the board itself speaks. The
 * layout classes (`wf-cols` / `wf-index` / `wf-ix` / `wf-main`) live in
 * 85-workflow.css and are SHARED with 🏷 Labeling: the ruling was about what a
 * workflow surface is, so one member owning the shape would be the drift.
 *
 * WHERE ITS DATA COMES FROM. `GET /_board/pageruns` — the receipts the RUN contract
 * (haipipe-page-workflow) writes to `<board>/_runs/page/<page-id>/<run-id>.json` —
 * and nothing else. Not `## States` (those are the page's Aims, not its
 * construction), and not the DOM. NO RECEIPTS IS AN ANSWER: most pages were never
 * RUN, and the empty state says the contract's own entry rule instead of an error.
 *
 * READ-ONLY ON PURPOSE (v1). The one action is the labeling stepper's smallest one:
 * the command a person would type, shown and copyable, never executed here. QB7's
 * law holds — what lands is what an author would have typed.
 *
 * OWN PANEL, SHARED CLOTHES. #pfpanel reuses the wf-* frame from 85-workflow.css
 * so the two workflows look like one surface, but it is not #wfpanel: the two
 * entries toggle independently, and opening one closes the other (one bottom, one
 * occupant — two stacked panels would eat the page).
 */
(function () {
  'use strict';

  var PHASES = [
    { id: 'OUTLINE', icon: '🧭', name: 'OUTLINE', skill: 'haipipe-page-outline',
      job: 'agree the SHAPE: sections, paragraphs, bullets, and what each owes' },
    { id: 'DRAFT',  icon: '✏️',  name: 'DRAFT',  skill: 'haipipe-page-draft',
      job: 'plan it: purpose, Aims, and each division’s own promise' },
    { id: 'EVIDENCE', icon: '🔍', name: 'EVIDENCE', skill: 'haipipe-page-evidence',
      job: 'land every promised claim\u2019s card: citation, value, display intake' },
    { id: 'REVISE', icon: '🖊', name: 'REVISE', skill: 'haipipe-page-revise',
      job: 'write the prose, citing every landed card by id' },
    { id: 'COMPILE', icon: '📄', name: 'COMPILE', skill: 'haipipe-page-revise',
      job: 'rebuild latex, pdf and word from that prose' },
    { id: 'CHECK',  icon: '✅',       name: 'CHECK',  skill: 'haipipe-page-check',
      job: 'judge the BUILT version and route its authority; only CHECK may CLOSE' }
  ];
  /* PROBE retired 260901: the item table (OUTLINE's SURVEY cycle) took its
     MATCH half and EVIDENCE's LAND cycle its outbound card. Every stored
     receipt naming PROBE draws on the EVIDENCE step. Before that, PROBE meant
     two different phases depending on WHEN the receipt was written: it was
     EVIDENCE's name from 260816 until 260817, then a phase of its own until 260901.
     Receipts on disk are immutable, so the token resolves against the run's own
     date rather than through a global alias, which would relabel every future
     PROBE as EVIDENCE. An unparseable date reads as CURRENT. */
  var PROBE_SPLIT = 260817;
  function runDate(run) {
    var m = /^(\d{6})/.exec((run && run.run_id) || '');
    return m ? parseInt(m[1], 10) : PROBE_SPLIT;
  }
  function phaseId(v, run) {
    v = String(v || '').toUpperCase();
    if (v === 'PROBE') return 'EVIDENCE';
    return v;
  }
  var NUM = ['①', '②', '③', '④', '⑤', '⑥', '⑦'];

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function livePage() {
    var secs = document.querySelectorAll('.wrap section.slide.q');
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].offsetParent !== null) return secs[i];
    }
    return secs[0] || null;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function age(mtime) {
    var d = Math.max(0, (Date.now() / 1000) - mtime);
    if (d >= 86400) return Math.floor(d / 86400) + 'd ago';
    if (d >= 3600) return Math.floor(d / 3600) + 'h ago';
    if (d >= 60) return Math.floor(d / 60) + 'm ago';
    return 'just now';
  }

  /* The suggested entry phase is the CONTRACT's, not a guess: the newest run's
     last route when one exists and is a phase; else CHECK, the run contract's
     default for an existing page whose next need is unknown. */
  function nextPhase(run) {
    var last = run && run.last ? phaseId(run.last.route, run) : '';
    if (last && PHASES.some(function (p) { return p.id === last; })) {
      return last;
    }
    return 'CHECK';
  }

  function render(host, page, data) {
    var pid = page.id || '';
    var file = pageFile(page);
    var runs = (data && data.runs) || [];
    var cur = runs[0] || null;
    var lastPhase = cur && cur.last ? phaseId(cur.last.phase, cur) : '';
    var route = cur && cur.last ? phaseId(cur.last.route, cur) : '';
    var closed = cur && (cur.status === 'closed' || route === 'CLOSE');
    var next = nextPhase(cur);
    var sel = lastPhase || next;      // the phase whose content opens first

    function visits(pidPhase) {
      if (!cur) return 0;
      return (cur.trail || []).filter(function (r) {
        return phaseId(r.phase, cur) === pidPhase;
      }).length;
    }

    function draw() {
      var index = PHASES.map(function (p, i) {
        var cls = 'wf-ix' + (p.id === sel ? ' sel' : '')
                + (p.id === lastPhase ? ' live' : '');
        var mark = '';
        if (p.id === lastPhase) mark = closed ? '🏁' : '▲ here';
        else if (p.id === next && !closed) mark = cur ? '· next' : '· enter';
        var n = visits(p.id);
        return '<button class="' + cls + '" type="button" data-p="' + p.id + '">'
          + '<span class="wf-ixn">' + NUM[i] + '</span> '
          + p.icon + ' <b>' + p.name + '</b>'
          + (n ? '<span class="wf-ixc">×' + n + '</span>' : '')
          + (mark ? '<span class="wf-ixmark">' + mark + '</span>' : '')
          + '</button>';
      }).join('')
        + '<div class="wf-ixnote">↩ a loop: CHECK routes backward, no locks</div>';

      var p = PHASES.filter(function (x) { return x.id === sel; })[0];
      var role;
      if (p.id === lastPhase) {
        role = closed ? 'last acted in this run · the run CLOSED here'
                      : 'last acted in this run · routed → ' + esc(route || '?');
      } else if (p.id === next && !closed) {
        role = cur ? 'next · ' + esc(lastPhase || 'the run') + ' routed here'
                   : 'where RUN would enter this page';
      } else if (cur) {
        role = visits(p.id) ? 'visited earlier in this run' : 'not visited in this run';
      } else {
        role = 'no run recorded yet';
      }

      var content =
        '<div class="pf-ph">'
        + '<div class="wf-dh">' + p.icon + ' ' + p.name
        + ' <span class="mut">· ' + esc(role) + '</span></div>'
        + '<ul class="wf-rows">'
        + '<li><span class="ti">🎯</span> ' + esc(p.job) + '</li>'
        + '<li><span class="ti">📜</span> contract: <code>page-workflows/'
        + p.skill + '</code></li>'
        + '</ul></div>';

      var runBlock;
      if (cur) {
        var edges = (cur.trail || []).map(function (r) {
          return esc(phaseId(r.phase, cur)) + (r.verdict ? '(' + esc(r.verdict) + ')' : '');
        });
        if (cur.last && cur.last.route) edges.push(esc(phaseId(cur.last.route, cur)));
        runBlock =
          '<div class="pf-run">'
          + '<div class="wf-dh">' + (closed ? '🏁' : '🧭') + ' '
          + esc(cur.run_id) + ' <span class="mut">· ' + esc(cur.status || 'open')
          + ' · ' + cur.steps + ' step' + (cur.steps === 1 ? '' : 's')
          + ' · round ' + cur.rounds + ' · ' + age(cur.mtime) + '</span></div>'
          + '<ul class="wf-rows">'
          + '<li><span class="ti">🧶</span> ' + edges.join(' → ') + '</li>'
          + (cur.last && cur.last.reason
              ? '<li><span class="ti">💬</span> ' + esc(cur.last.reason) + '</li>'
              : '')
          + (runs.length > 1
              ? '<li><span class="ti">🗂</span> ' + (runs.length - 1)
                + ' earlier run' + (runs.length > 2 ? 's' : '')
                + ' in <code>_runs/page/</code></li>'
              : '')
          + '</ul>'
          + (closed ? '' : cmdRow(file, next))
          + '</div>';
      } else {
        runBlock =
          '<div class="pf-run">'
          + '<div class="wf-dh">🧭 no run recorded for this page</div>'
          + '<ul class="wf-rows">'
          + '<li><span class="ti">🚪</span> The run contract’s entry rule: '
          + 'an existing page enters at CHECK so a fresh judge routes it; '
          + 'a brand-new page enters at DRAFT after CREATE.</li>'
          + '</ul>'
          + cmdRow(file, next)
          + '</div>';
      }

      host.innerHTML =
        '<div class="wf-head">📄 Page phases · <b>' + esc(pid) + '</b>'
        + '<span class="mut"> · read from <code>_runs/page/</code> receipts, '
        + 'never stored</span></div>'
        + '<div class="wf-cols">'
        + '<div class="wf-index">' + index + '</div>'
        + '<div class="wf-main">' + content + runBlock + '</div>'
        + '</div>';

      host.querySelectorAll('.wf-ix').forEach(function (b) {
        b.onclick = function () { sel = b.dataset.p; draw(); };
      });
      host.querySelectorAll('.wf-copy').forEach(function (b) {
        b.onclick = function () {
          var el = host.querySelector('.wf-cmd');
          try {
            navigator.clipboard.writeText(el ? el.textContent : '');
            b.textContent = 'copied';
          } catch (e) {}
          setTimeout(function () { b.textContent = 'copy'; }, 1600);
        };
      });
    }

    draw();
  }

  /* The one action: the command an author would type, shown before it is in
     their hands. Copy only — running it is the chat's job, not this strip's. */
  function cmdRow(file, phase) {
    var name = file.split('/').pop();
    return '<div class="wf-act"><div class="wf-runrow">'
      + '<code class="wf-cmd">/haipipe-page-workflow run ' + esc(name)
      + ' from ' + esc(phase) + '</code>'
      + '<button class="wf-copy" type="button">copy</button>'
      + '<span class="wf-note">paste into the 💬 Chat pane to start '
      + 'this run</span>'
      + '</div></div>';
  }

  function panel() {
    var p = document.getElementById('pfpanel');
    if (p) return p;
    p = document.createElement('div');
    p.id = 'pfpanel';
    p.hidden = true;
    p.innerHTML = '<button class="wf-x" type="button" title="close (Esc)">✕ close</button>'
                + '<div class="wf-body"></div>';
    document.body.appendChild(p);
    p.querySelector('.wf-x').onclick = function () { p.hidden = true; };
    if (window.boardPanelResize) window.boardPanelResize(p);
    return p;
  }

  function open() {
    var page = livePage();
    if (!page) return;
    var p = panel();
    if (!p.hidden) { p.hidden = true; return; }        // the entry TOGGLES
    var other = document.getElementById('wfpanel');    // one bottom, one occupant
    if (other) other.hidden = true;
    var host = p.querySelector('.wf-body');
    host.innerHTML = '<div class="wf-empty">reading <code>_runs/page/</code>…</div>';
    p.hidden = false;
    fetch('/_board/pageruns?path=' + encodeURIComponent(board())
          + '&file=' + encodeURIComponent(pageFile(page)))
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) {
          host.innerHTML = '<div class="wf-empty">⚠️ ' + esc(j.err || 'refused')
            + '</div>';
          return;
        }
        render(host, page, j);
      })
      .catch(function () {
        host.innerHTML = '<div class="wf-empty">⚠️ open this page through '
          + '<code>serve.py</code> to read its runs — a bare file has no '
          + 'server to ask.</div>';
      });
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    var p = document.getElementById('pfpanel');
    if (p && !p.hidden) { p.hidden = true; }
  });

  /* Re-render in place when the router swaps the page under an open panel, so the
     surface can never show one page's runs under another page's title. */
  window.addEventListener('board:updated', function () {
    var p = document.getElementById('pfpanel');
    if (p && !p.hidden) { p.hidden = true; open(); }
  });

  /* The lifecycle engine remains available to internal callers. It no longer
     registers a reader-facing row: Page phases is process state, not a Plugin. */
})();
