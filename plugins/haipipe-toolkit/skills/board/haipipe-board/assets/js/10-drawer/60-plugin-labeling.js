/* 🏷 Labeling · the subjective-label plugin's surface, registered into the 🔌 Plugin menu.
 *
 * THIS IS THE WORKFLOW FOR A LABELING PAGE, AND IT CARRIES THAT PLUGIN'S NAME, NOT
 * A GENERIC ONE (JL 260807: "Labeling is the workflow"). A display plugin will register
 * 🖼 Display and that entry will be the display workflow. There is deliberately no
 * abstract "Workflow" entry: it would name a concept no plugin owns, and it would show
 * on every page whether or not it meant anything there.
 *
 * WHAT IT IS. The page's own lifecycle, drawn left to right, one cell per step,
 * with exactly one cell live and everything after it locked.
 *
 * ⚠️ WHERE THIS FILE OUGHT TO LIVE. With its plugin, at
 * `subjective-label/skills/haipipe-board-page-for-labeling/`, beside the contract it
 * serves. It sits in the board engine's assets only because `assets.py` concatenates
 * `assets/js/**` from THIS skill and has no way to load a file a plugin contributes.
 * That loader is owed; until it exists this file is a guest here, and the registration
 * below is written so that moving it changes nothing but the path.
 *
 * WHERE ITS DATA COMES FROM. `## States`, and nothing else. Each `### A<n>` group
 * in States is one STEP, and the step's state is the WORST of its rows. There is no
 * second source and no new markdown: a page that keeps States true keeps this true.
 * JL 260807: "这个console就是我们人机交互的地方" — so it lives in the live layer,
 * where it cannot go stale against the file the way a `## Console` section would.
 *
 * WHY THE AIM GROUPS ARE THE STEPS. Every page type already declares an ordered
 * lifecycle in its own Aims: a labeling page runs init/round/gates/evaluate/complete,
 * a display page runs the acceptance ladder, a slide page runs per-slide acceptance.
 * Reading the groups means this surface generalizes with zero per-type declaration.
 *
 * LOCKED IS COMPUTED, NEVER STORED. The Board has five states (⬜ 🔨 🧠 ✅ ❄️) and no
 * "locked". A step is locked when an earlier step is not yet ✅, which is derived here
 * and never written back, so no page has to invent a sixth state to be drawn.
 *
 * SCRIPTS OFF. This whole surface disappears and the page's prose is untouched, which
 * is the invariant build.py asserts on every build.
 */
(function () {
  'use strict';

  /* The five current states, PLUS the legacy ones src/common.py still parses. A page
     written or edited by anything that reaches for 🟡 must not fall out of the strip
     (JL 260808: "why starting from Step 2?" — A1 had one 🟡 row and vanished whole). */
  var RANK = { '❄️': -1, '⏸️': -1, '⬜': 0, '🔨': 1, '🟡': 1, '🟠': 1,
               '🧠': 2, '✅': 3 };
  var LABEL = { '-1': 'on ice', '0': 'not started', '1': 'working',
                '2': 'waiting on a person', '3': 'done' };

  function livePage() {
    var secs = document.querySelectorAll('.wrap section.slide.q');
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].offsetParent !== null) return secs[i];
    }
    return secs[0] || null;
  }

  /* One STEP per `### A<n>` group in States. Worst row wins, because a step with one
     row still open is not a step anybody may treat as finished. */
  function readSteps(page) {
    var now = page.querySelector('.sect.col.now');
    if (!now) return [];
    var out = [];
    now.querySelectorAll('details.csec').forEach(function (g) {
      var head = g.querySelector('summary');
      if (!head) return;
      // The summary reads "<emoji> <name> A<n>⧉🤖": the id TRAILS the name and drags the
      // copy and chat affordances with it. Take the id from the tail, then cut the tail off.
      var raw = (head.textContent || '').trim();
      /* States also holds `### Decision Now`, which is a question for a person and not a
         step. Only a group that carries an Aim id is one (JL 260808: it showed up as a
         seventh door). */
      if (!/\bA\d+\b/.test(raw)) return;
      var idm = /\bA(\d+)\s*[^A-Za-z0-9]*$/.exec(raw);
      var aid = idm ? idm[1] : null;
      var name = raw.replace(/\s*\bA\d+\s*[^A-Za-z0-9]*$/, '').trim();
      var worst = null, rows = [];
      g.querySelectorAll('.bt').forEach(function (r) {
        var ti = r.querySelector('.ti'), tl = r.querySelector('.ttl');
        var em = ti ? (ti.textContent || '').trim() : '';
        if (!(em in RANK)) return;
        rows.push({ emoji: em, text: tl ? (tl.textContent || '').trim() : '' });
        if (worst === null || RANK[em] < RANK[worst]) worst = em;
      });
      /* NEVER drop a group. A step that vanishes is worse than a step whose state is
         unreadable: the first hides that the step exists at all. */
      if (!rows.length) {
        out.push({ name: name, aid: aid, emoji: '❔', rank: 0, unknown: true,
                   rows: [{ emoji: '❔', text: 'no row here uses a state this surface '
                            + 'knows; the step is real, its state is not readable' }] });
        return;
      }
      out.push({ name: name, aid: aid, emoji: worst, rank: RANK[worst], rows: rows });
    });
    return out;
  }

  /* The live step is the first one not yet done. Everything after it is LOCKED, and
     an ❄️ step is skipped rather than blocking, because parking is deliberate. */
  function mark(steps) {
    var live = -1;
    for (var i = 0; i < steps.length; i++) {
      if (steps[i].rank !== 3 && steps[i].rank !== -1) { live = i; break; }
    }
    steps.forEach(function (s, i) {
      s.live = (i === live);
      s.locked = (live >= 0 && i > live && s.rank !== 3);
    });
    return live;
  }

  /* QF1 §1's five doors, in Aim-group order. `null` means the step closes on a human
     signoff and no command may stand in for it (QF1 §3.1), so the surface offers none. */
  var DOOR = { '1': '/sl-init', '2': '/sl-round', '3': null,
               '4': '/sl-evaluate', '5': '/sl-complete' };

  /* Each door's own options, asked BEFORE it runs (JL 260808: "provide the option and
     run"). A field is only here when the door genuinely takes it: inventing a knob the
     command ignores would teach a person a setting that does nothing. */
  var FIELDS = {
    '1': [ {k:'corpus', label:'data',            ph:'_WorkSpace/InLabStore/runs/<run>/items.jsonl'},
           {k:'trait',  label:'trait',           ph:'authority'},
           {k:'embed',  label:'embedding model', ph:'bge-m3'} ],
    '2': [ {k:'n',      label:'batch size',      ph:'60'} ],
    '4': [],
    '5': []
  };

  /* ⚠️ The map above is by Aim NUMBER, so it is only true on a page whose Aim groups ARE
     the five doors. A page organized by SUBJECT has an A1 that means the policy, not
     init, and offering `/sl-init` there would hand a person the wrong command with a
     straight face. So the surface checks first and says nothing rather than lying.
     The two shapes disagree today, which is an open Decision Now row on QBt11; this
     check is what keeps that disagreement from becoming a wrong button. */
  function stepShaped(steps) {
    return steps.some(function (s) { return /Step\s*[①②③④⑤]/.test(s.name); });
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* `A2 · 🔁 Step ② round` → the `§2` division this step opens. The Aim id's number
     is the division number, which is the base contract's own 1:1 rule between an Aim
     group and the Content division it belongs to; the checker enforces it as
     `group-no-division`, so this mapping is never a guess. */
  function divisionOf(step) { return step.aid; }

  function render(host, page) {
    var steps = readSteps(page);
    if (!steps.length) {
      host.innerHTML = '<div class="wf-empty">This page declares no Aim groups, '
        + 'so it has no lifecycle to walk. Workflow reads <code>## States</code>.</div>';
      return;
    }
    var live = mark(steps);
    var pid = page.id || '';

    var cells = steps.map(function (s, i) {
      var cls = 'wf-step' + (s.live ? ' live' : '') + (s.locked ? ' locked' : '')
              + (s.rank === 3 ? ' done' : '');
      var done = s.rows.filter(function (r) { return r.emoji === '✅'; }).length;
      if (s.unknown) cls += ' unknown';
      return '<button class="' + cls + '" type="button" data-i="' + i + '"'
        + ' title="' + esc(s.name) + '">'
        + '<span class="wf-n">' + (i + 1) + '</span>'
        + '<span class="wf-t">' + esc(s.name) + '</span>'
        + '<span class="wf-s">' + s.emoji + ' '
        + (s.unknown ? 'state unreadable' : LABEL[String(s.rank)]) + '</span>'
        + '<span class="wf-c">' + done + '/' + s.rows.length + '</span>'
        + (s.locked ? '<span class="wf-lock">🔒</span>' : '')
        + (s.live ? '<span class="wf-here">▲ you are here</span>' : '')
        + '</button>';
    }).join('<span class="wf-arrow">›</span>');

    var cur = live >= 0 ? steps[live] : null;
    var detail = '';
    if (cur) {
      var div = divisionOf(cur);
      detail =
        '<div class="wf-detail">'
        + '<div class="wf-dh">' + cur.emoji + ' ' + esc(cur.name) + '</div>'
        + '<ul class="wf-rows">'
        + cur.rows.map(function (r) {
            return '<li><span class="ti">' + r.emoji + '</span> ' + esc(r.text) + '</li>';
          }).join('')
        + '</ul>'
        + (div
            ? '<a class="wf-jump" href="#' + esc(pid) + '">§' + esc(div)
              + ' · open this step in Content ↗</a>'
            : '')
        + action(cur, stepShaped(steps))
        + '</div>';
    } else {
      detail = '<div class="wf-detail"><div class="wf-dh">✅ every step is done</div>'
             + '<p class="mut">Nothing on this page is waiting.</p></div>';
    }

    host.innerHTML =
      '<div class="wf-head">\u{1F3F7} Labeling · <b>' + esc(pid) + '</b>'
      + '<span class="mut"> · read from <code>## States</code>, never stored</span></div>'
      + '<div class="wf-strip">' + cells + '</div>'
      + detail;

    /* Live preview: the command line updates as the options are typed, so RUN never
       sends something the person has not read. */
    function refresh() {
      var el = host.querySelector('.wf-cmd');
      if (el && cur) el.textContent = composed(cur, host);
    }
    host.querySelectorAll('.wf-f').forEach(function (i) { i.oninput = refresh; });
    refresh();

    host.querySelectorAll('.wf-copy').forEach(function (b) {
      b.onclick = function () {
        try { navigator.clipboard.writeText(composed(cur, host)); b.textContent = 'copied'; }
        catch (e) {}
        setTimeout(function () { b.textContent = 'copy'; }, 1600);
      };
    });

    host.querySelectorAll('.wf-run').forEach(function (b) {
      b.onclick = function () {
        var note = host.querySelector('.wf-note');
        b.disabled = true; b.textContent = '…';
        sendToChat(prompt(cur, host, pid), function (err) {
          b.disabled = false; b.textContent = '▶ RUN';
          if (!note) return;
          note.textContent = err ? '⚠️ ' + err
            : '✅ handed to 💬 GUI Chat — watch the pane on the right';
        });
      };
    });

    host.querySelectorAll('.wf-step').forEach(function (b) {
      b.onclick = function () {
        var s = steps[+b.dataset.i];
        var d = divisionOf(s);
        var t = page.querySelector('.sect.col.content');
        if (t) t.open = true;
        if (d) {
          var heads = page.querySelectorAll('.sect.col.content details.csec');
          var want = heads[+d - 1];
          if (want) { want.open = true; want.scrollIntoView({ block: 'center' }); }
        }
      };
    });
  }

  /* QB7's law: what lands is what an author would have typed. The button copies the
     command; it does not run it, and it invents no syntax only a button could produce.
     A step whose door is null offers nothing, because a human signoff has no command. */
  /* One line, exactly what will be typed, shown before it is typed. QB7's law survives
     the change from copy to run: what lands is still what an author would have typed. */
  function composed(step, host) {
    var cmd = DOOR[step.aid];
    if (!cmd) return '';
    var parts = [cmd];
    (FIELDS[step.aid] || []).forEach(function (f) {
      var el = host.querySelector('.wf-f[data-k="' + f.k + '"]');
      var v = el && el.value.trim();
      if (v) parts.push('--' + f.k + ' ' + v);
    });
    return parts.join(' ');
  }

  /* RUN does not execute a program (JL 260808: "相当于是你通过点那个 button，然后它就是
     自动地去打开 GUI，然后去跟它交流"). It opens the GUI chat and says the task, so the
     agent does the work in a conversation a person can watch, interrupt and correct. That
     is why the chat is the right surface and a shell was the wrong one: this step is a
     judgment call with a person in it, not a batch job. */
  function shell() {
    try {
      var w = window.parent;
      return (w && w !== window && w.document.getElementById('mgui')) ? w : null;
    } catch (e) { return null; }
  }

  function sendToChat(text, done) {
    var sh = shell();
    if (!sh) return done('open this page inside the board viewer to use RUN');
    sh.document.getElementById('mgui').click();          // switch the pane to GUI
    var tries = 0;
    (function wait() {
      var ta = null;
      try { ta = sh.frames.chat.document.querySelector('#chat textarea'); } catch (e) {}
      if (!ta) {
        if (++tries > 40) return done('the GUI chat did not come up');
        return setTimeout(wait, 250);
      }
      ta.focus();
      ta.value = text;
      ta.dispatchEvent(new sh.frames.chat.Event('input', { bubbles: true }));
      ta.dispatchEvent(new sh.frames.chat.KeyboardEvent('keydown',
        { key: 'Enter', bubbles: true }));
      done(null);
    })();
  }

  /* What the agent is actually asked. The command line stays in it verbatim, so the
     person still sees exactly what they authorized, and the page is named so the agent
     writes its record back where it belongs. */
  function prompt(step, host, pid) {
    var lines = [
      'Run ' + step.name.replace(/^A\d+\s*·\s*/, '') + ' for this labeling page.',
      '',
      'page: ' + pid,
      'command: ' + composed(step, host)
    ];
    (FIELDS[step.aid] || []).forEach(function (f) {
      var el = host.querySelector('.wf-f[data-k="' + f.k + '"]');
      if (el && el.value.trim()) lines.push(f.label + ': ' + el.value.trim());
    });
    lines.push('', 'Follow the step contract on this page, stop at its human gate, '
      + 'and append the record to the page rather than only reporting it here.');
    return lines.join('\n');
  }

  function action(step, shaped) {
    if (!shaped) {
      return '<div class="wf-act wf-human">📄 This page\u2019s Content is organized by '
           + 'SUBJECT, not by the five doors, so no step command can be offered here. '
           + 'The shape is an open decision on <code>QBt11</code>.</div>';
    }
    var cmd = DOOR[step.aid];
    if (step.rank === 2) {
      return '<div class="wf-act wf-human">🧠 This step is waiting on a person. '
           + 'No command closes it.</div>';
    }
    if (!cmd) return '';
    var fs = (FIELDS[step.aid] || []).map(function (f) {
      return '<label class="wf-fl">' + esc(f.label)
        + '<input class="wf-f" data-k="' + esc(f.k) + '" placeholder="' + esc(f.ph) + '"></label>';
    }).join('');
    return '<div class="wf-act">'
      + (fs ? '<div class="wf-form">' + fs + '</div>' : '')
      + '<div class="wf-runrow">'
      + '<code class="wf-cmd">' + esc(cmd) + '</code>'
      + '<button class="wf-run" type="button" data-aid="' + esc(step.aid) + '">▶ RUN</button>'
      + '<button class="wf-copy" type="button">copy</button>'
      + '<span class="wf-note">opens 💬 GUI Chat and hands it this step</span>'
      + '</div></div>';
  }

  function panel() {
    var p = document.getElementById('wfpanel');
    if (p) return p;
    p = document.createElement('div');
    p.id = 'wfpanel';
    p.hidden = true;
    p.innerHTML = '<button class="wf-x" type="button" title="close (Esc)">✕ close</button>'
                + '<div class="wf-body"></div>';
    document.body.appendChild(p);
    p.querySelector('.wf-x').onclick = function () { p.hidden = true; };
    return p;
  }

  /* A surface a person cannot shut is worse than one they cannot open (JL 260808:
     "我关不掉labeling了"). Three ways out: the ✕, Escape, and choosing the entry again. */
  function open() {
    var page = livePage();
    if (!page) return;
    var p = panel();
    if (!p.hidden) { p.hidden = true; return; }        // the entry TOGGLES
    render(p.querySelector('.wf-body'), page);
    p.hidden = false;
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    var p = document.getElementById('wfpanel');
    if (p && !p.hidden) { p.hidden = true; }
  });

  /* Re-render in place when the router swaps the page under an open panel, so the
     surface can never show one page's steps under another page's title. */
  window.addEventListener('board:updated', function () {
    var p = document.getElementById('wfpanel');
    if (p && !p.hidden) open();
  });

  /* Registered, not wired: the engine holds no branch for this surface, and `applies`
     keeps it off every page that is not a labeling page. */
  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'labeling',
      label: '\u{1F3F7} Labeling',
      hint: 'this run’s steps, left to right, one live',
      // 🪜 A WORKFLOW, not a plugin (JL 260808): it opens along the bottom and its
      // whole content is where THIS page stands, which is why it is type-gated and
      // GUI Chat is not. Page's four phases join this menu, not the other one.
      menu: 'workflow',
      applies: function (page, type) { return type === 'labeling'; },
      open: function () { open(); }
    });
  }

  window.boardWorkflowOpen = open;   // kept for direct calls and for the tests
})();
