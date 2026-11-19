"""Item marks (ref/cards.md §4, §6): the mark strip after an item and the card slot under it.

Only content carries marks and cards (sentences, the paper's question, RQ rows, designs, rules, insight questions
and cells, labeling rules and items, decisions, findings, terms, notes, and Job, Task and Run rows: ladder_cards).
Structure (folds, tabs, view bars, file lists, rails, section bars) shows at most a page's orange roll-up.
A workbench plugs in with these calls and nothing else:
  marks(address, page_cards, derived)   on content: 💬 N  📝 N (orange)  ✓  and any derived marks it passes
  rollup(page_cards, waiting)           on a structure row linking to a page: 🙋 N  📝 N, nothing else
  card_slot(address, page_cards, page_rel, cols=0)   the cards under the item: a <div>, or a full-width <tr> when cols
  ASSETS                                once per page: the CSS and the one script, keyed by data-addr
where page_cards = item_cards.cards(page). A click posts to /_board/item-card; the writer answers with the new strip and
slot, which replace the old ones in place. A mark with nothing behind it is not drawn; a quiet ＋ opens an empty slot.
"""
from __future__ import annotations

from live.frame import esc

# derived marks a workbench may pass, in strip order: 🙋 decisions waiting (orange), ★ score, evidence, 🕘 versions,
# 🧵 the sessions that changed it (ref/three-views.md § 4.4)
DERIVED = ("🙋", "★", "📊", "❝", "🖼️", "📎", "🕘", "🧵")
ORANGE = {"🙋", "📝"}


def _counts(entry: dict) -> tuple[int, int, bool]:
    open_comments = sum(1 for c in entry.get("comments", []) if c["state"] != "done")
    waiting_edits = sum(1 for e in entry.get("edits", []) if e["state"] == "proposed")
    return open_comments, waiting_edits, entry.get("checked") is not None


def marks(address: str, page_cards: dict, derived: dict | None = None) -> str:
    """The strip after an item. `derived` maps a mark to its count or text ({'🙋': 2, '★': '7'}); zero or empty is
    not drawn. Card marks sit in their own slot, apart from the workbench's own state marks."""
    entry = page_cards.get(address, {})
    n_comments, n_edits, checked = _counts(entry)
    a = esc(address)
    parts = []
    for mark in DERIVED:
        v = (derived or {}).get(mark)
        if v:
            cls = "im-mk im-w" if mark in ORANGE else "im-mk"
            parts.append(f'<button type="button" class="{cls}" data-im-open="{a}">{mark}'
                         + (f' {esc(str(v))}' if v is not True else '') + '</button>')
    if n_comments:
        parts.append(f'<button type="button" class="im-mk" data-im-open="{a}">💬 {n_comments}</button>')
    if n_edits:
        parts.append(f'<button type="button" class="im-mk im-w" data-im-open="{a}">📝 {n_edits}</button>')
    if checked:
        parts.append(f'<button type="button" class="im-mk im-ok" data-im-open="{a}" title="checked">✓</button>')
    parts.append(f'<button type="button" class="im-mk im-add" data-im-open="{a}" aria-label="Open cards">＋</button>')
    return f'<span class="im-marks" data-addr="{a}">{"".join(parts)}</span>'


def rollup(page_cards: dict, waiting: int = 0) -> str:
    """A structure row that links to a page (a Job, Task or Run row, a fold, a tab) never carries cards: it shows at
    most that page's orange roll-up, 🙋 N for `waiting` decisions and 📝 N for its edit cards waiting for Accept."""
    edits = sum(1 for entry in page_cards.values() for e in entry.get("edits", []) if e["state"] == "proposed")
    parts = ([f'<span class="im-mk im-w">🙋 {waiting}</span>'] if waiting else []) + \
            ([f'<span class="im-mk im-w">📝 {edits}</span>'] if edits else [])
    return f'<span class="im-marks im-roll">{"".join(parts)}</span>' if parts else ""


def _comment(c: dict, a: str) -> str:
    thread = "".join(f'<li class="im-{w.lower()}"><small>{esc(t)}</small> {esc(words)}</li>' for w, t, words in c["thread"])
    state, n = c["state"], esc(c["n"])
    acts = ('<button type="button" data-im-act="reopen">Reopen</button>' if state == "done" else
            '<button type="button" data-im-act="done">Done</button>')
    if not any(w == "Reply" for w, _, _ in c["thread"]):
        acts += '<button type="button" data-im-act="delete">Delete</button>'
    return (f'<article class="im-card im-c-{esc(state)}" data-n="{n}" data-was="{esc(state)}">'
            + (f'<blockquote>{esc(c["quote"])}</blockquote>' if c["quote"] else '')
            + f'<ul>{thread}</ul><div class="im-acts"><input type="text" placeholder="Reply" aria-label="Reply">'
            f'<button type="button" data-im-act="reply">Reply</button>{acts}</div></article>')


def _edit(e: dict) -> str:
    state = e["state"]
    acts = ('<button type="button" data-im-act="accept">✓ Accept</button>'
            '<button type="button" data-im-act="reject">✗ Reject</button>' if state == "proposed" else
            '<button type="button" data-im-act="undo">↺ Undo</button>')
    return (f'<article class="im-card im-edit im-e-{esc(state)}" data-card="{esc(e["head"])}" data-was="{esc(state)}">'
            + (f'<p class="im-why">{esc(e["why"])}</p>' if e["why"] else '')
            + (f'<p><del>{esc(e["original"])}</del></p>' if e["original"] else '')
            + f'<p><ins>{esc(e["expected"])}</ins></p><div class="im-acts">{acts}</div></article>')


def card_slot(address: str, page_cards: dict, page_rel: str, cols: int = 0, words: str = "") -> str:
    """The cards under an item, closed until a mark is clicked: its open comments, then its waiting edit cards, then
    the closed ones folded; a box to add a comment, and ✓ to check the item (`words`: what the person sees)."""
    entry = page_cards.get(address, {})
    a = esc(address)
    live = [c for c in entry.get("comments", []) if c["state"] != "done"]
    closed = [c for c in entry.get("comments", []) if c["state"] == "done"]
    edits = entry.get("edits", [])
    body = ("".join(_comment(c, a) for c in live) + "".join(_edit(e) for e in edits if e["state"] == "proposed")
            + ("<details class=im-old><summary>Closed</summary>" + "".join(_comment(c, a) for c in closed)
               + "".join(_edit(e) for e in edits if e["state"] != "proposed") + "</details>"
               if closed or any(e["state"] != "proposed" for e in edits) else ""))
    check = ('<button type="button" data-im-act="uncheck">✓ Checked</button>' if entry.get("checked") is not None
             else '<button type="button" data-im-act="check">✓ Check</button>')
    inner = (f'<div class="im-slot-in">{body}<div class="im-new"><textarea rows="2" placeholder="Comment" '
             f'aria-label="Comment"></textarea><button type="button" data-im-act="add">Comment</button>{check}</div></div>')
    attrs = f'class="im-slot" data-im-slot="{a}" data-page="{esc(page_rel)}" data-words="{esc(words)}" hidden'
    if cols:
        return f'<tr {attrs}><td colspan="{cols}">{inner}</td></tr>'
    return f'<div {attrs}>{inner}</div>'


ASSETS = """<style>
.im-marks{display:inline-flex;gap:4px;margin-left:6px;vertical-align:1px;white-space:nowrap}
.im-mk{border:0;background:none;padding:0 3px;font:12px/1.4 system-ui,-apple-system,sans-serif;color:var(--mut);cursor:pointer}
.im-mk:hover{color:var(--accent)}.im-mk.im-w{color:#b35c00;font-weight:600}.im-mk.im-ok{color:#2b8a3e}
.im-mk.im-add{opacity:0}.im-marks:hover .im-add,.im-mk.im-add:focus,tr:hover .im-add,li:hover .im-add{opacity:.7}
.im-slot-in{margin:6px 0 10px;padding:8px 10px;border-left:3px solid var(--line);display:grid;gap:8px}
.im-card{border:1px solid var(--line);border-radius:8px;padding:6px 9px;background:var(--card);font-size:13px}
.im-card ul{margin:0;padding:0;list-style:none;display:grid;gap:3px}.im-card small{color:var(--mut)}
.im-card blockquote{margin:0 0 4px;color:var(--mut);font-style:italic}.im-c-done,.im-e-rejected{opacity:.6}
.im-edit{border-color:#f0a040}.im-edit del{color:var(--mut)}.im-edit ins{text-decoration:none;font-weight:600}
.im-acts,.im-new{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:5px}
.im-acts input,.im-new textarea{flex:1 1 200px;min-width:0;font:inherit;font-size:13px}
.im-acts button,.im-new button{font-size:12px;cursor:pointer}.im-err{color:#c92a2a;font-size:12px}
</style><script>
(function(){if(window.__imCards)return;window.__imCards=1;
function slot(a){return document.querySelector('[data-im-slot="'+CSS.escape(a)+'"]');}
document.addEventListener('click',function(e){
 var o=e.target.closest&&e.target.closest('[data-im-open]');
 if(o){e.preventDefault();var s=slot(o.dataset.imOpen);if(s)s.hidden=!s.hidden;return;}
 var b=e.target.closest&&e.target.closest('[data-im-act]');if(!b)return;
 var s=b.closest('[data-im-slot]');if(!s)return;e.preventDefault();
 var card=b.closest('.im-card'),act=b.dataset.imAct,box=b.parentNode.querySelector('textarea,input');
 var td=s.tagName==='TR'&&s.querySelector(':scope>td[colspan]');
 var p={page:s.dataset.page,address:s.dataset.imSlot,act:act,text:box?box.value:'',words:s.dataset.words,cols:td?+td.getAttribute('colspan'):0};
 if(card){p.n=card.dataset.n||'';p.card=card.dataset.card||'';p.was=card.dataset.was||'';}
 b.disabled=true;
 fetch('/_board/item-card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)})
 .then(function(r){return r.json();}).then(function(j){
  if(!j.ok){var m=document.createElement('p');m.className='im-err';m.textContent=j.err||'refused';b.parentNode.appendChild(m);b.disabled=false;return;}
  var a=s.dataset.imSlot;
  if(j.marks)document.querySelectorAll('.im-marks[data-addr="'+CSS.escape(a)+'"]').forEach(function(x){x.outerHTML=j.marks;});
  if(j.slot){var t=document.createElement(s.tagName==='TR'?'tbody':'div');t.innerHTML=j.slot;var n=t.firstElementChild;
   if(n){n.hidden=false;s.replaceWith(n);}}
 }).catch(function(){b.disabled=false;});
});})();
</script>"""
