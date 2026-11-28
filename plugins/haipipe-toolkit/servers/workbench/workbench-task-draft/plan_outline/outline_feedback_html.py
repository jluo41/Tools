"""Feedback on the page: the badge, the fold, the list, and their stylesheet and script."""
from __future__ import annotations

from live.outline_feedback_read import _e

# ── HTML · badge, fold, list, assets ───────────────────────────────────────

def _state_class(disposition: str) -> str:
    low = disposition.lower()
    if low == "pending":
        return "pending"
    if low.startswith(("applied", "accepted")):
        return "done"
    if "not" in low or "decision" in low or "partly" in low:
        return "open"
    return "note"


def feedback_list_html(items: list[dict]) -> str:
    if not items:
        return ('<p class=fb-empty>No notes yet. Press + to say what this paragraph '
                'should explore or change.</p>')
    parts = []
    for item in items:
        where = "%s · %s/%s · %s" % (item["run"], item["version"], item["step"], item["label"])
        group = (" · group P%s" % "-P".join("%02d" % p for p in (item["group"][0], item["group"][-1]))
                 if len(item["group"]) > 1 else "")
        parts.append(
            '<article class="fb-item fb-%s" data-fb-id="%s"><header>'
            '<span class="fb-kind %s">%s</span>'
            '<b class=fb-author>%s</b><span class=fb-date>%s</span>'
            '<span class="fb-state %s">%s</span></header>'
            '<p class=fb-text>%s</p><footer class=fb-where>%s%s</footer></article>'
            % (_state_class(item["disposition"]), _e(item["id"]), _e(item["kind"]), _e(item["kind"]),
               _e(item["author"] or "unsigned"), _e(item["date"]),
               _state_class(item["disposition"]), _e(item["disposition"]),
               _e(item["comment"] or "(no text)"), _e(where), _e(group)))
    return "".join(parts)


def feedback_summary(items: list[dict]) -> str:
    pending = sum(1 for item in items if item["pending"])
    text = "💬 Notes · %d" % len(items)
    if pending:
        text += " · %d pending" % pending
    return text


def feedback_badge_html(paragraph: str, items: list[dict], read_only: bool = False) -> str:
    pending = sum(1 for item in items if item["pending"])
    badge = ('<span class="fb-badge%s%s" data-fb-badge="%s" title="%d note%s%s">%s</span>'
             % (" on" if items else "", " pending" if pending else "", _e(paragraph),
                len(items), "s"[:len(items) != 1],
                (" · %d pending" % pending) if pending else "",
                ("💬 %d" % len(items)) if items else ""))
    add = ("" if read_only else
           '<button type=button class=fb-add data-fb-add="%s" title="Add a note to %s" '
           'aria-label="Add a note to %s">+</button>' % (_e(paragraph), _e(paragraph), _e(paragraph)))
    return badge + add


def feedback_fold_html(paragraph: str, para: dict, items: list[dict], path_q: str,
                       file_q: str, read_only: bool = False) -> str:
    listing = feedback_list_html(items)
    form = ""
    if not read_only:
        options = "".join('<option value="%s">%s</option>' % (_e(b), _e(b)) for b in para.get("bullets", []))
        form = (
            '<form class=fb-form data-paragraph-feedback autocomplete=off>'
            '<input type=hidden name=action value=feedback>'
            '<input type=hidden name=path value="%s"><input type=hidden name=file value="%s">'
            '<input type=hidden name=paragraph value="%s">'
            '<div class=fb-row>'
            '<label>Kind<select name=kind>'
            '<option value=explore>explore · what this paragraph should say or try</option>'
            '<option value=wording>wording · change the current Draft</option>'
            '<option value=accept>accept · the current wording is right</option>'
            '</select></label>'
            '<label>Bullet<select name=bullet><option value="">whole paragraph</option>%s</select></label>'
            '<label>Name<input name=author maxlength=80 required placeholder="JL"></label>'
            '</div>'
            '<label class=fb-comment>Note<textarea name=comment rows=3 maxlength=8000 required '
            'placeholder="What should this paragraph explore, argue, or change?"></textarea></label>'
            '<div class=fb-actions><button type=submit>Save note</button>'
            '<span role=status class=fb-status></span></div>'
            '<small class=fb-hint>Saved at once into the owning Run\'s journal under <code>results/</code> '
            'as a pending Step. The agent answers it on its next turn; the plan and the Page are not edited here.</small>'
            '</form>' % (_e(path_q or ""), _e(file_q or ""), _e(paragraph), options))
    return ('<details class=paragraph-feedback data-paragraph="%s">'
            '<summary data-fb-summary>%s</summary>'
            '<div class=fb-list data-fb-list>%s</div>%s</details>'
            % (_e(paragraph), _e(feedback_summary(items)), listing, form))


FEEDBACK_CSS = """
.fb-badge{margin-left:auto;font:500 11px/1.4 system-ui,sans-serif;color:var(--mut);white-space:nowrap}
.fb-badge.on{color:var(--fg)}
.fb-badge.pending{color:var(--warn)}
.fb-add{flex:none;width:22px;height:22px;border:1px solid var(--line);border-radius:6px;background:var(--card);
 color:var(--acc);font:600 15px/1 system-ui,sans-serif;cursor:pointer;padding:0;margin-left:4px}
.fb-add:hover{background:color-mix(in srgb,var(--acc) 12%,var(--card))}
details.paragraph-feedback{margin:6px 0 0;border-top:1px dashed var(--line);padding:4px 0 0}
details.paragraph-feedback>summary{cursor:pointer;font:500 12px/1.6 system-ui,sans-serif;color:var(--mut);list-style:none;padding:4px 0;
 text-transform:none;letter-spacing:normal}
details.paragraph-feedback>summary::-webkit-details-marker{display:none}
details.paragraph-feedback>summary::before{content:"▸ ";color:var(--acc)}
details.paragraph-feedback[open]>summary::before{content:"▾ "}
.fb-list{display:flex;flex-direction:column;gap:6px;margin:4px 0 8px}
.fb-empty{font:12px/1.5 system-ui,sans-serif;color:var(--mut);margin:0}
.fb-item{border:1px solid var(--line);border-radius:7px;padding:7px 9px;background:var(--card)}
.fb-item.fb-pending{border-color:color-mix(in srgb,var(--warn) 60%,var(--line))}
.fb-item header{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:baseline;font:12px/1.4 system-ui,sans-serif;color:var(--mut)}
.fb-kind{font:600 10.5px/1.4 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.04em;padding:1px 6px;border-radius:9px;
 border:1px solid var(--line);color:var(--fg)}
.fb-kind.explore{background:color-mix(in srgb,var(--acc) 14%,var(--card))}
.fb-kind.wording{background:color-mix(in srgb,var(--warn) 16%,var(--card))}
.fb-kind.accept{background:color-mix(in srgb,#2e9e5b 16%,var(--card))}
.fb-author{color:var(--fg)}
.fb-state{margin-left:auto;font:500 11px/1.4 system-ui,sans-serif}
.fb-state.pending{color:var(--warn)}
.fb-state.done{color:#2e9e5b}
.fb-text{margin:5px 0 3px;font:14px/1.55 Georgia,serif;color:var(--fg);white-space:pre-wrap}
.fb-where{font:10.5px/1.4 ui-monospace,Menlo,monospace;color:var(--mut)}
.fb-form{display:flex;flex-direction:column;gap:6px;margin:4px 0 6px}
.fb-row{display:flex;flex-wrap:wrap;gap:8px}
.fb-form label{display:flex;flex-direction:column;gap:2px;font:500 11px/1.4 system-ui,sans-serif;color:var(--mut);min-width:0}
.fb-form select,.fb-form input,.fb-form textarea{font:13px/1.45 system-ui,sans-serif;color:var(--fg);background:var(--card);
 border:1px solid var(--line);border-radius:6px;padding:5px 7px;min-width:0}
.fb-form textarea{width:100%;box-sizing:border-box;resize:vertical;font:14px/1.5 Georgia,serif}
.fb-comment{flex:1}
.fb-actions{display:flex;gap:10px;align-items:center}
.fb-actions button{font:600 12px/1.4 system-ui,sans-serif;padding:5px 12px;border-radius:6px;border:1px solid var(--acc);
 background:var(--acc);color:#fff;cursor:pointer}
.fb-actions button[disabled]{opacity:.6;cursor:wait}
.fb-status{font:12px/1.4 system-ui,sans-serif;color:var(--mut)}
.fb-hint{font:11px/1.45 system-ui,sans-serif;color:var(--mut)}
.fb-hint code{font:10.5px ui-monospace,Menlo,monospace}
"""

FEEDBACK_JS = r"""
(function () {
  var STORE = 'hai-outline-feedback-author';
  function remembered() { try { return localStorage.getItem(STORE) || ''; } catch (_) { return ''; } }
  function remember(v) { try { localStorage.setItem(STORE, v); } catch (_) {} }
  function freshId() {
    var bytes = new Uint8Array(8);
    (window.crypto || {}).getRandomValues ? crypto.getRandomValues(bytes)
      : bytes.forEach(function (_, i) { bytes[i] = Math.floor(Math.random() * 256); });
    return 'fb-' + Array.from(bytes, function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }
  document.querySelectorAll('form[data-paragraph-feedback]').forEach(function (form) {
    var author = form.elements.author;
    if (author && !author.value) author.value = remembered();
    form.addEventListener('input', function () { form.dataset.dirty = 'true'; });
  });
  document.addEventListener('click', function (event) {
    var add = event.target.closest('[data-fb-add]');
    if (!add) return;
    event.preventDefault();
    event.stopPropagation();
    var group = add.closest('details.paragraph-group');
    if (group) group.open = true;
    var fold = group && group.querySelector('details.paragraph-feedback');
    if (!fold) return;
    fold.open = true;
    var area = fold.querySelector('textarea[name=comment]');
    if (area) { area.focus(); area.scrollIntoView({block: 'center', behavior: 'smooth'}); }
  }, true);
  document.addEventListener('submit', async function (event) {
    var form = event.target.closest('form[data-paragraph-feedback]');
    if (!form) return;
    event.preventDefault();
    if (form.dataset.saving === 'true') return;
    var status = form.querySelector('.fb-status');
    var button = form.querySelector('button[type=submit]');
    var payload = Object.fromEntries(new FormData(form));
    payload.comment = (payload.comment || '').trim();
    payload.author = (payload.author || '').trim();
    if (!payload.comment) { status.textContent = 'Write the note first.'; return; }
    if (!payload.author) { status.textContent = 'Sign the note with your name.'; return; }
    var signature = JSON.stringify([payload.paragraph, payload.bullet, payload.kind, payload.author, payload.comment]);
    if (!form._attempt || form._attempt.signature !== signature) form._attempt = {signature: signature, id: freshId()};
    payload.feedback_id = form._attempt.id;
    form.dataset.saving = 'true';
    button.disabled = true;
    status.textContent = 'Saving…';
    try {
      var response = await fetch('/_board/draft', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
      });
      var result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.err || 'Save failed');
      remember(payload.author);
      var fold = form.closest('details.paragraph-feedback');
      fold.querySelector('[data-fb-list]').innerHTML = result.list_html;
      fold.querySelector('[data-fb-summary]').textContent = result.summary;
      var badge = document.querySelector('[data-fb-badge="' + payload.paragraph + '"]');
      if (badge) {
        badge.textContent = result.count ? ('💬 ' + result.count) : '';
        badge.classList.toggle('on', result.count > 0);
        badge.classList.toggle('pending', result.pending > 0);
      }
      if (form.elements.comment.value.trim() === payload.comment) {
        form.elements.comment.value = '';
        delete form.dataset.dirty;
        form._attempt = null;
        status.textContent = 'Saved · ' + result.file + ' · ' + result.step + ' ' + result.feedback;
      } else {
        status.textContent = 'Earlier note saved · new text unsaved';
      }
    } catch (error) {
      status.textContent = 'Not saved: ' + error.message;
      form.dataset.dirty = 'true';
    } finally {
      delete form.dataset.saving;
      button.disabled = false;
    }
  });
  window.addEventListener('beforeunload', function (event) {
    if (document.querySelector('form[data-paragraph-feedback][data-dirty="true"]')) {
      event.preventDefault(); event.returnValue = '';
    }
  });
})();
"""


def feedback_assets_html() -> str:
    """Style and script for the note thread, emitted once per Draft Space."""
    return "<style>%s</style><script>%s</script>" % (FEEDBACK_CSS, FEEDBACK_JS)
