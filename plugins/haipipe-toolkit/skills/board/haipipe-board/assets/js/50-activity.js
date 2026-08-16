/* ── the Activity readout ───────────────────────────────────────────────
   Runtime data, so it is enhancement-only by definition: the static shell
   above still explains the measurement when this script or serve.py is
   absent. One POST on load, one more whenever the page reports a write.

   The FOCUS TIMER that used to live here was deleted on 260816 (JL: keep the
   log tracker, drop the rest). It wrote browser spans into a SQLite file at
   `.haipipe-board/activity.sqlite3` that nothing ever read back, and it was
   also, accidentally, what fetched this readout: every heartbeat returned the
   stats and the panel drew them. So the display had to be given a request of
   its own before the timer could go, which is this. */
(function () {
  function escAct(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function status(text, cls) {
    var s = document.getElementById('activity-status');
    if (!s) return;
    s.textContent = text;
    s.className = 'act-status' + (cls ? ' ' + cls : '');
  }

  /* ── the dashboard counts UPDATES, not time (QD8 -> QC2, JL 260726) ──────
     "I don't care about the time. What I care is about the numbers of
     updates." One update = one dated line in one page's ## Log. That unit is
     written by whoever did the work in whatever tool, so it sees the days a
     browser timer structurally could not: most work on these boards arrives
     through Claude Code, and the timer only ever watched a tab. */
  function sampleData() {
    var title = (document.querySelector('.h1') || {}).textContent || 'This board';
    var path = boardDirPath().replace(/^\//, '');
    var vals = [0,0,0,4,11,0,7,22,9,0,14,31,18,26];
    var days = [], now = new Date();
    vals.forEach(function (v, i) {
      var d = new Date(now); d.setDate(now.getDate() - 13 + i);
      var key = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') +
        '-' + String(d.getDate()).padStart(2,'0');
      days.push({ day:key, updates:v, here:Math.round(v * .6) });
    });
    return {
      sample: true, unit: 'updates', days: days,
      totals: {today:26, week:89, updates:142, boards:3, pages:24},
      boards: [
        {board:path,title:title,updates:86,days:5,pages:12,last:days[13].day},
        {board:'sample/paper',title:'Paper lifecycle',updates:38,days:3,pages:8,last:days[12].day},
        {board:'sample/data',title:'CMS store',updates:18,days:2,pages:4,last:days[10].day}
      ],
      current: {
        board:path,title:title,updates:86,days:5,pages:12,last:days[13].day,
        groups:[
          {group:'QA · Defining a board',updates:44,
           pages:[
             {page:'QA4',title:'Shared Q/S Page Layout',updates:26,last:days[13].day},
             {page:'QA2',title:'Shared Q/S source template',updates:18,last:days[12].day}
           ]},
          {group:'QD · Working on the board',updates:28,
           pages:[{page:'QD2',title:'SDK version: the chat box',updates:28,last:days[11].day}]},
          {group:'QC · Index and structure',updates:14,
           pages:[{page:'QC2',title:'Index page design',updates:14,last:days[13].day}]}
        ]
      }
    };
  }
  function agoAct(day) {
    if (!day) return '';
    var d = Math.round((new Date().setHours(0,0,0,0) -
      new Date(day + 'T00:00:00').getTime()) / 86400000);
    return d <= 0 ? 'today' : d === 1 ? 'yesterday' : d + 'd ago';
  }
  function rowHtml(kind, name, updates, max, meta, current) {
    var f = max ? Math.max(1, updates / max * 100) : 0;
    return '<div class="act-row ' + kind + (current ? ' current' : '') +
      '" title="' + escAct(name + ': ' + updates + ' update' +
      (updates === 1 ? '' : 's') + (meta ? ' · ' + meta : '')) + '">' +
      '<span class="act-name">' + escAct(name) + '</span>' +
      '<span class="act-track" style="--focus:' + f.toFixed(2) +
      ';--changed:0"><i class="act-focus"></i></span>' +
      '<span class="act-time">' + updates + '</span></div>';
  }
  function render(raw) {
    var body = document.getElementById('activity-body');
    if (!body) return;
    var data = raw;
    if (!data || !data.totals || Number(data.totals.updates || 0) < 1) data = sampleData();
    status(data.sample ? 'layout preview · no logs read' : 'counting · ## Log',
      data.sample ? 'sample' : 'live');
    var t = data.totals, dayMax = Math.max.apply(null, data.days.map(function (d) {
      return Number(d.updates || 0);
    }).concat([1]));
    var days = data.days.map(function (d) {
      var n = Number(d.updates || 0), h = Number(d.here || 0);
      var f = n / dayMax * 100, c = h / dayMax * 100;
      var date = new Date(d.day + 'T12:00:00');
      var label = ['S','M','T','W','T','F','S'][date.getDay()] + d.day.slice(8);
      return '<div class="act-day" title="' + escAct(d.day + ': ' + n +
        ' update' + (n === 1 ? '' : 's') + ' across all boards, ' + h +
        ' on this one') + '">' +
        '<span class="act-day-n' + (n ? '' : ' zero') + '">' +
        escAct(n ? String(n) : '·') + '</span>' +
        '<div class="act-day-bars" style="--focus:' + f.toFixed(2) +
        ';--changed:' + c.toFixed(2) + '"><i class="act-day-focus"></i>' +
        '<i class="act-day-changed"></i>' +
        (h && h !== n ? '<span class="act-day-here">' + escAct(String(h)) +
         '</span>' : '') + '</div>' +
        '<span class="act-day-label">' + escAct(label) + '</span></div>';
    }).join('');
    var boardMax = Math.max.apply(null, data.boards.map(function (b) {
      return Number(b.updates || 0);
    }).concat([1]));
    var boards = data.boards.slice(0, 6).map(function (b) {
      return rowHtml('board', b.title, Number(b.updates || 0), boardMax,
        b.pages + ' pages · ' + b.days + ' active days · last ' + agoAct(b.last),
        b.board === data.current.board);
    }).join('');
    var groupMax = Math.max.apply(null, (data.current.groups || []).map(function (g) {
      return Number(g.updates || 0);
    }).concat([1]));
    var groups = (data.current.groups || []).map(function (g) {
      var html = rowHtml('group', g.group, Number(g.updates || 0), groupMax,
        (g.pages || []).length + ' pages', false);
      (g.pages || []).forEach(function (p) {
        html += rowHtml('page', p.page + ' · ' + p.title, Number(p.updates || 0),
          groupMax, 'last ' + agoAct(p.last), false);
      });
      return html;
    }).join('');
    body.innerHTML =
      '<div class="act-metrics">' +
      '<div class="act-metric"><b>' + Number(t.today || 0) + '</b><span>updates today</span></div>' +
      '<div class="act-metric"><b>' + Number(t.week || 0) + '</b><span>last 7 days</span></div>' +
      '<div class="act-metric"><b>' + Number(t.updates || 0) + '</b><span>all boards</span></div>' +
      '<div class="act-metric"><b>' + Number(t.boards || 0) + '</b><span>boards with a log</span></div>' +
      '<div class="act-metric"><b>' + Number(t.pages || 0) + '</b><span>pages ever updated</span></div>' +
      '</div>' +
      '<div class="act-block"><div class="act-block-head"><b>Last 14 days</b>' +
      '<span class="act-legend"><i></i>all boards <i class="changed"></i>this board</span></div>' +
      '<div class="act-days">' + days + '</div></div>' +
      '<div class="act-block"><div class="act-block-head"><b>Across boards</b>' +
      '<span class="act-legend">top 6 · every ## Log line ever</span></div><div class="act-tree">' +
      boards + '</div></div>' +
      '<div class="act-block"><div class="act-block-head"><b>This board: Group → Page</b>' +
      '<span class="act-legend">' + Number(data.current.updates || 0) +
      ' updates</span></div><div class="act-tree">' + groups + '</div></div>' +
      (data.sample ? '<p class="act-empty">Preview data shows the layout only. It disappears once any page carries a dated ## Log line.</p>' : '');
  }


  function load() {
    fetch('/_board/activity', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ op: 'stats', path: boardPath() })
    }).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).then(render).catch(function () {
      status('counts unavailable', '');
    });
  }
  window.addEventListener('board:updated', load);

  status('reading logs', '');
  load();
})();
