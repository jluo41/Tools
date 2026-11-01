/* A building Task's views (labeling_focus.py, decision_report_view.py; b15 j01 t03 s58 C2).
   1. Each section folds by its heading bar, open by default; what the reader folds stays folded in this browser.
   2. The Decide view's inbox (slide 17): each row's Open shows that card under the rows, one card at a time.
   3. Its card (slide 16) saves a draft or submits the answers to POST /_board/labeling/act. Nothing is chosen for the
      person: a radio is checked only by their own click or their own saved draft. Nothing is called saved or submitted
      without a 200 from the server; a 409 means this page is out of date. After a Save draft, while the report
      has no submission, each card's pill says what the server will say on a reload: Draft saved or Needs your
      judgment. */
(function () {
  'use strict';
  if (window.decisionReportView) return;
  window.decisionReportView = true;

  var STALE = 'This report changed or another tab saved first; reload';
  var NAME_KEY = 'dec-human-id';
  var PILL = {wait: 'Needs your judgment', draft: 'Draft saved'};
  function get(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* no storage: nothing is kept */ } }
  function drop(k) { try { window.localStorage.removeItem(k); } catch (e) { /* no storage */ } }
  function query(name) { try { return new URLSearchParams(window.location.search).get(name) || ''; } catch (e) { return ''; } }
  function each(root, sel, fn) { Array.prototype.forEach.call(root.querySelectorAll(sel), fn); }
  function calm() { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return true; } }

  /* 1 · folds */
  function folds() {
    var key = 'dec-fold:' + query('path') + ':' + query('section') + ':' + query('group'), shut = {};
    try { shut = JSON.parse(get(key) || '{}') || {}; } catch (e) { shut = {}; }
    each(document, 'details.dec-sec[data-fold]', function (d) {
      if (shut[d.dataset.fold]) d.open = false;
      d.addEventListener('toggle', function () {
        if (d.open) delete shut[d.dataset.fold]; else shut[d.dataset.fold] = 1;
        put(key, JSON.stringify(shut));
      });
    });
  }

  /* 2 · the inbox: Open on a row shows its card under the rows; one card open at a time */
  function inbox(list) {
    var buttons = Array.prototype.slice.call(list.querySelectorAll('[data-open]'));
    list.addEventListener('click', function (e) {
      var b = e.target.closest('[data-open]');
      if (!b || !list.contains(b)) return;
      var shown = null;
      buttons.forEach(function (x) {
        var on = x === b, card = document.getElementById(x.getAttribute('aria-controls')), row = x.closest('.dec-row');
        x.setAttribute('aria-expanded', on ? 'true' : 'false');
        if (row) row.classList.toggle('on', on);
        if (card) { card.hidden = !on; if (on) shown = card; }
      });
      if (shown) {
        var box = shown.closest('.dec-cardbox') || shown, r = box.getBoundingClientRect();
        if (r.top < 0 || r.top > window.innerHeight - 80) box.scrollIntoView({block: 'start', behavior: calm() ? 'auto' : 'smooth'});
        var q = shown.querySelector('.dec-cq');
        if (q) { q.tabIndex = -1; q.focus({preventScroll: true}); }
      }
    });
  }

  /* 3 · the card */
  function slug(name) {    // the actor id the server keeps for a name (labeling.py, labeling_decision_act)
    return String(name || '').trim().replace(/[^A-Za-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 64);
  }
  function newId() {        // one id per Submit click, kept for a retry of the same answers
    var a = new Uint8Array(8), i;
    try { window.crypto.getRandomValues(a); } catch (e) { for (i = 0; i < 8; i++) a[i] = Math.floor(Math.random() * 256); }
    return 'sub-' + Date.now().toString(36) + '-' + Array.prototype.map.call(a, function (b) {
      return ('0' + b.toString(16)).slice(-2);
    }).join('');
  }

  function form(box) {
    var human = box.querySelector('[data-human]'), confirm = box.querySelector('[data-confirm]'),
      save = box.querySelector('[data-save]'), submit = box.querySelector('[data-submit]'),
      status = box.querySelector('[data-status]'), cards = Array.prototype.slice.call(box.querySelectorAll('[data-decision]')),
      report = box.dataset.report, revision = Number(box.dataset.revision) || 0, drafts = {}, expected = 0,
      dirty = false, busy = false;
    try { drafts = JSON.parse(box.dataset.drafts || '{}') || {}; } catch (e) { drafts = {}; }

    function say(words, kind, reload) {
      status.textContent = words;
      status.className = 'dec-status' + (kind ? ' ' + kind : '');
      if (reload) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'dec-btn'; b.textContent = 'Reload';
        b.addEventListener('click', function () { window.location.reload(); });
        status.appendChild(b);
      }
    }
    function gate() { save.disabled = busy; submit.disabled = busy || !confirm.checked; }
    function sync(card) {    // the chosen option shows its effect; the own-rule box shows only under "None of these"
      each(card, 'input[type=radio]', function (r) {
        var effect = r.closest('label') && r.closest('label').querySelector('[data-effect]');
        if (effect) effect.hidden = !r.checked;
      });
      var none = card.querySelector('input[type=radio][value=none]'), own = card.querySelector('[data-own]');
      if (own) own.hidden = !(none && none.checked);
    }
    function pills(answers) {   // after a save, before any submission: Draft saved or Needs your judgment
      if (box.dataset.submitted === '1') return;
      cards.forEach(function (card, i) {
        var a = answers[card.dataset.decision], state = a && a.kind && a.kind !== 'unanswered' ? 'draft' : 'wait';
        each(box, '[data-pill="' + i + '"]', function (p) {
          p.textContent = PILL[state];
          p.className = 'dec-pill ' + state;
          p.dataset.state = state;
        });
      });
    }
    function answers() {     // every card, its kind said out loud: chosen, custom, reject_options, defer or unanswered
      var out = {};
      cards.forEach(function (card) {
        var pick = card.querySelector('input[type=radio]:checked'), own = card.querySelector('[data-own]'),
          note = card.querySelector('[data-comment]'), a = {kind: 'unanswered'};
        if (pick && pick.value === 'chosen') a = {kind: 'chosen', option_id: pick.dataset.option};
        else if (pick && pick.value === 'none') a = own && own.value.trim() ? {kind: 'custom', text: own.value.trim()} : {kind: 'reject_options'};
        else if (pick && pick.value === 'defer') a = {kind: 'defer'};
        if (note && note.value.trim()) a.comment = note.value.trim();
        out[card.dataset.decision] = a;
      });
      return out;
    }
    function restore(d) {    // the person's own saved draft, back into the cards
      cards.forEach(function (card) {
        var a = (d.answers || {})[card.dataset.decision] || {}, own = card.querySelector('[data-own]'),
          note = card.querySelector('[data-comment]');
        each(card, 'input[type=radio]', function (r) {
          r.checked = (a.kind === 'chosen' && r.value === 'chosen' && r.dataset.option === a.option_id)
            || ((a.kind === 'custom' || a.kind === 'reject_options') && r.value === 'none')
            || (a.kind === 'defer' && r.value === 'defer');
        });
        if (own) own.value = a.kind === 'custom' ? (a.text || '') : '';
        if (note) note.value = a.comment || '';
        sync(card);
      });
    }
    function adopt(fill) {   // the draft this page holds for the name in "Your name"
      var d = drafts[slug(human.value)], current = d && Number(d.report_revision) === revision;
      expected = d ? Number(d.draft_revision) || 0 : 0;
      if (!d) { if (fill) say('', ''); return; }
      if (!current) {
        say('Your saved draft answered an earlier revision of this report, so it is not filled in.', '');
        return;
      }
      if (fill) {
        restore(d);
        dirty = false;
        say('Your saved draft is filled in' + (d.last_saved_at ? ' (saved ' + d.last_saved_at + ').' : '.'), 'ok');
      }
    }
    function payload(action) {
      return {action: action, path: box.dataset.path, report_id: report, report_revision: revision,
        answers: answers(), comments: '', human_id: human.value.trim(), attest: true};
    }
    function send(body) {
      return window.fetch(box.dataset.act, {method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
        .then(function (r) {
          return r.text().then(function (t) {
            var j = null;
            try { j = JSON.parse(t); } catch (e) { j = null; }
            return {status: r.status, body: j && typeof j === 'object' ? j : {}};
          });
        });
    }
    function refused(res, verb) {
      if (res.status === 409) { say(STALE + (res.body.err ? ' (' + res.body.err + ').' : '.'), 'err', true); return; }
      say(verb + ': ' + (res.body.err || 'the server answered ' + res.status) + '.', 'err');
    }
    function named() {
      if (slug(human.value)) return true;
      say('Type your name first.', 'err');
      human.focus();
      return false;
    }

    box.addEventListener('change', function (e) {
      var card = e.target.closest('[data-decision]');
      if (card && e.target.type === 'radio') sync(card);
      if (e.target === human) {
        put(NAME_KEY, human.value.trim());
        adopt(!dirty);
      } else if (e.target === confirm) {
        gate();
      } else {
        dirty = true;
      }
    });
    box.addEventListener('input', function (e) {
      if (e.target.matches('textarea')) dirty = true;
    });

    save.addEventListener('click', function () {
      if (busy || !named()) return;
      var body = payload('decision_draft_save');
      body.expected_draft_revision = expected;
      busy = true; gate(); say('Saving the draft…', '');
      send(body).then(function (res) {
        busy = false; gate();
        if (res.status === 200 && res.body.ok === true) {
          var d = res.body.draft || {}, n = Number(d.draft_revision);
          if (isFinite(n) && n > 0) expected = n;
          drafts[slug(human.value)] = {draft_revision: expected, report_revision: revision, answers: body.answers,
            last_saved_at: d.last_saved_at || ''};
          pills(body.answers);
          dirty = false;
          say('Draft saved' + (d.last_saved_at ? ' (' + d.last_saved_at + ')' : '') + '. Nothing is submitted yet.', 'ok');
          return;
        }
        refused(res, 'Not saved');
      }, function () {
        busy = false; gate();
        say('Not saved: the server did not answer. Try again.', 'err');
      });
    });

    submit.addEventListener('click', function () {
      if (busy || !named()) return;
      if (!confirm.checked) { say('Tick "I confirm these are my answers" first.', 'err'); return; }
      var body = payload('decision_feedback_submit'), key = 'dec-pending:' + box.dataset.path + ':' + report + ':'
        + revision + ':' + slug(human.value), same = JSON.stringify([body.answers, body.comments]), pending = null;
      try { pending = JSON.parse(get(key) || 'null'); } catch (e) { pending = null; }
      body.request_id = pending && pending.same === same && pending.id ? pending.id : newId();
      body.confirmed = true;
      put(key, JSON.stringify({id: body.request_id, same: same}));
      busy = true; gate(); say('Submitting…', '');
      send(body).then(function (res) {
        busy = false;
        if (res.status === 200 && res.body.ok === true) {
          var r = res.body.receipt || {}, id = r.submission_id || r.request_id || '';
          drop(key);
          confirm.checked = false; gate();
          say('Submitted' + (id ? ' (receipt ' + id + ')' : '') + '. Reload to see each card’s state.', 'ok', true);
          return;
        }
        gate();
        if (res.status < 500) drop(key);      // refused: nothing was received, so the next click is a new request
        refused(res, 'Not submitted');
      }, function () {
        busy = false; gate();
        say('Not submitted: the server did not answer. Submit again; the same answers keep the same request id.', 'err');
      });
    });

    human.value = get(NAME_KEY) || '';
    cards.forEach(sync);
    adopt(true);
    gate();
  }

  function start() {
    folds();
    each(document, '.dec-view .dec-inbox', inbox);
    each(document, '[data-dec-form]', form);
  }
  if (document.readyState !== 'loading') start(); else document.addEventListener('DOMContentLoaded', start);
})();
