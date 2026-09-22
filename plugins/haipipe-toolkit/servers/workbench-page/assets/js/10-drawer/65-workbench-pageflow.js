/* 📄 Page Runs · internal lifecycle view (no Workbench row).
 *
 * The Run list is context → structure ⇄ evidence → writing → check. The check
 * gate routes to the Run that owns a finding; only check may CLOSE. Receipts
 * written before 2026-09-22 carry uppercase tokens; runOf() maps them.
 *
 * INDEX LEFT, CONTENT RIGHT (JL 260816: "把 workflow 放在最左边…跟具体的内容分开").
 * The LEFT column is an index — context … check, names only, one row per
 * Run — and the RIGHT column holds the selected Run's content plus the pass
 * record, the same left-index-right-content language the board itself speaks. The
 * layout classes (`wf-cols` / `wf-index` / `wf-ix` / `wf-main`) live in
 * 85-workflow.css and are SHARED with 🏷 Labeling: the ruling was about what a
 * workflow surface is, so one member owning the shape would be the drift.
 *
 * WHERE ITS DATA COMES FROM. `GET /_board/pageruns` is a compatibility route
 * for the receipts the Page workflow-pass contract
 * (haipipe-page-workflow) writes to `<board>/_runs/page/<page-id>/<run-id>.json` —
 * and nothing else. Not `## States` (those are the page's Aims, not its
 * construction), and not the DOM. NO RECEIPTS IS AN ANSWER: most pages have no
 * workflow pass, and the empty state says the contract's entry rule instead of an error.
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

  /* One row per Run, in list order; id = the skill suffix (haipipe-page-<id>). */
  var RUNS = [
    { run: 'context', icon: '🧭', name: 'Context', skill: 'haipipe-page-context',
      job: 'collect, resolve, and freeze the Page context before planning' },
    { run: 'structure', icon: '🧩', name: 'Structure', skill: 'haipipe-page-structure',
      job: 'SHAPE the Bullet plan, then SURVEY every Evidence Item run graph' },
    { run: 'evidence', icon: '🔍', name: 'Evidence', skill: 'haipipe-page-evidence',
      job: 'LAND supporting and local Results, then EMBED them into Bullets' },
    { run: 'writing', icon: '✏️', name: 'Writing', skill: 'haipipe-page-writing',
      job: 'WRITE each division through Draft, Revise, Build, and Pre-check' },
    { run: 'check',  icon: '✅', name: 'Check',  skill: 'haipipe-page-check',
      job: 'judge the BUILT version and route its authority; only check may CLOSE' }
  ];
  /* Receipts written before 2026-09-22 carry uppercase tokens; map them once. */
  var LEGACY = { CONTEXT: 'context', OUTLINE: 'structure', PROBE: 'evidence', EVIDENCE: 'evidence',
                 DRAFT: 'writing', REVISE: 'writing', COMPILE: 'writing', CONTENT: 'writing', CHECK: 'check' };
  function runOf(v) {
    v = String(v || '').trim();
    if (!v) return '';
    if (v === 'CLOSE' || v === 'HOLD' || v.toUpperCase() === 'CLOSE' || v.toUpperCase() === 'HOLD') return v.toUpperCase();
    return LEGACY[v.toUpperCase()] || v.toLowerCase();
  }

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

  /* The suggested entry Run is the CONTRACT's, not a guess: the newest pass's
     last route when one exists and is a Run; else check, the run contract's
     default for an existing page whose next need is unknown. */
  function nextRun(run) {
    var last = run && run.last ? runOf(run.last.route, run) : '';
    if (last && RUNS.some(function (p) { return p.run === last; })) {
      return last;
    }
    return 'check';
  }

  function render(host, page, data) {
    var pid = page.id || '';
    var file = pageFile(page);
    var runs = (data && data.runs) || [];
    var cur = runs[0] || null;
    var lastRun = cur && cur.last ? runOf(cur.last.run, cur) : '';
    var route = cur && cur.last ? runOf(cur.last.route, cur) : '';
    var closed = cur && (cur.status === 'closed' || route === 'CLOSE');
    var next = nextRun(cur);
    var sel = lastRun || next;      // the Run whose content opens first

    function visits(pidRun) {
      if (!cur) return 0;
      return (cur.trail || []).filter(function (r) {
        return runOf(r.run, cur) === pidRun;
      }).length;
    }

    function draw() {
      var index = RUNS.map(function (p, i) {
        var cls = 'wf-ix' + (p.run === sel ? ' sel' : '')
                + (p.run === lastRun ? ' live' : '');
        var mark = '';
        if (p.run === lastRun) mark = closed ? '🏁' : '▲ here';
        else if (p.run === next && !closed) mark = cur ? '· next' : '· enter';
        var n = visits(p.run);
        return '<button class="' + cls + '" type="button" data-p="' + p.run + '">'
          + p.icon + ' <b>' + p.name + '</b>'
          + (n ? '<span class="wf-ixc">×' + n + '</span>' : '')
          + (mark ? '<span class="wf-ixmark">' + mark + '</span>' : '')
          + '</button>';
      }).join('')
        + '<div class="wf-ixnote">↩ a loop: the check gate routes backward, no locks</div>';

      var p = RUNS.filter(function (x) { return x.run === sel; })[0];
      var role;
      if (p.run === lastRun) {
        role = closed ? 'last acted in this pass · the pass CLOSED here'
                      : 'last acted in this pass · routed → ' + esc(route || '?');
      } else if (p.run === next && !closed) {
        role = cur ? 'next · ' + esc(lastRun || 'the pass') + ' routed here'
                   : 'where a workflow pass would enter this page';
      } else if (cur) {
        role = visits(p.run) ? 'visited earlier in this pass' : 'not visited in this pass';
      } else {
        role = 'no workflow pass recorded yet';
      }

      var content =
        '<div class="pf-ph">'
        + '<div class="wf-dh">' + p.icon + ' ' + p.name
        + ' <span class="mut">· ' + esc(role) + '</span></div>'
        + '<ul class="wf-rows">'
        + '<li><span class="ti">🎯</span> ' + esc(p.job) + '</li>'
        + '<li><span class="ti">📜</span> contract: <code>runs/'
        + p.skill + '</code></li>'
        + '</ul></div>';

      var runBlock;
      if (cur) {
        var edges = (cur.trail || []).map(function (r) {
          return esc(runOf(r.run, cur)) + (r.verdict ? '(' + esc(r.verdict) + ')' : '');
        });
        if (cur.last && cur.last.route) edges.push(esc(runOf(cur.last.route, cur)));
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
                + ' earlier workflow pass' + (runs.length > 2 ? 'es' : '')
                + ' in <code>_runs/page/</code></li>'
              : '')
          + '</ul>'
          + (closed ? '' : cmdRow(file, next))
          + '</div>';
      } else {
        runBlock =
          '<div class="pf-run">'
          + '<div class="wf-dh">🧭 no workflow pass recorded for this page</div>'
          + '<ul class="wf-rows">'
          + '<li><span class="ti">🚪</span> The workflow-pass entry rule: '
          + 'an existing page enters at CHECK so a fresh judge routes it; '
          + 'a brand-new page enters at CONTEXT so policy and requirements '
          + 'are frozen before the Structure Run.</li>'
          + '</ul>'
          + cmdRow(file, next)
          + '</div>';
      }

      host.innerHTML =
        '<div class="wf-head">📄 Page Runs · <b>' + esc(pid) + '</b>'
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
  function cmdRow(file, run) {
    var name = file.split('/').pop();
    return '<div class="wf-act"><div class="wf-runrow">'
      + '<code class="wf-cmd">/haipipe-page-workflow run ' + esc(name)
      + ' from ' + esc(run) + '</code>'
      + '<button class="wf-copy" type="button">copy</button>'
      + '<span class="wf-note">paste into the 💬 Chat pane to start '
      + 'this workflow pass</span>'
      + '</div></div>';
  }

  function panel() {
    var p = document.getElementById('pfpanel');
    if (p) return p;
    p = document.createElement('div');
    p.run = 'pfpanel';
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
          + '<code>serve.py</code> to read its workflow passes — a bare file has no '
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
     registers a reader-facing row: Page Runs is process state, not a Workbench. */
})();
