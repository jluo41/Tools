"""Draft Space feedback composer · the ONE browser write, into the Run journal.

Each paragraph row of Draft Space carries a (+) and a folded note thread. A
saved note becomes one `#### Feedback F<nn>` item inside a PENDING Step of the
Page Writing Run (RP) that owns the paragraph, appended to that Run's current
Version journal `results/<run>/v<NNN>.md`. The plan file under `outline/` and
the Page source are never written here: the agent completes the pending Step
on its next turn through the fast feedback path of
`haipipe-page-workflow/ref/interactive-writing-run.md`.

The owning Run is chosen in this order:

  1. an open `rp-para-NN_Pxx[-Pyy]` whose paragraph range covers the paragraph
  2. an open `rp-struct-NN` (the structure is still being settled)
  3. an open `rp-sec-NN` covering the paragraph
  4. the latest finished `rp-para-NN` covering it, reopened in a new Version
  5. a newly allocated `rp-para-NN_Pxx` (ticket + paired results/)

`Kind` separates the author's story notes from wording requests:
`explore` (what this paragraph should explore or say), `wording` (change the
current Draft), `accept` (the person accepts the current wording).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import re
import secrets
from pathlib import Path

from live.outline_preview import page_lock
from src.outline_version import latest_outline

KINDS = ("explore", "wording", "accept")
OPEN_STATUSES = {"", "ready", "running", "waiting-for-feedback", "open"}
# A Feedback item aimed at more paragraphs than this is Section-level history;
# it belongs to Run Space, not to one paragraph's note thread.
MAX_GROUP = 4
_ID_RE = re.compile(r"fb-[0-9a-f]{8,32}")
_PARAGRAPH_RE = re.compile(r"C\d+\.P\d+")
_BULLET_RE = re.compile(r"C\d+\.P\d+\.B\d+")


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%y%m%d %H%M UTC")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def plan_path(page: Path) -> Path | None:
    return latest_outline(page.parent / "outline", page.stem)


# ── the plan's paragraphs ──────────────────────────────────────────────────

def paragraphs(page: Path) -> dict[str, dict]:
    """Return `C<n>.P<m>` → {address, p, brief, bullets} from the current plan."""
    plan = plan_path(page)
    out: dict[str, dict] = {}
    if plan is None or not plan.is_file():
        return out
    cn = 0
    current = ""
    for line in _read(plan).splitlines():
        division = re.match(r"^## C(\d+)\b", line)
        if division:
            cn = int(division.group(1))
            current = ""
            continue
        if line.startswith("## "):
            # Any other `## ` heading ends the plan's divisions.
            if cn:
                break
            continue
        heading = re.match(r"^### C(\d+)\.P(\d+)\s*·\s*(.*)$", line)
        if heading:
            cn = int(heading.group(1))
            p = int(heading.group(2))
            brief = re.sub(r"\s*·\s*S\d+\s+to\s+S\d+\s*$", "", heading.group(3)).strip()
            current = "C%d.P%d" % (cn, p)
            out[current] = {"address": current, "p": p, "brief": brief, "bullets": []}
            continue
        bullet = re.match(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·", line)
        if bullet and current:
            out[current]["bullets"].append("%s.B%s" % (current, bullet.group(1)))
    return out


# ── Run inventory · RP tickets paired with results/<run>/ ──────────────────

def _front(text: str) -> dict[str, str]:
    """Read `key: value` lines from a front matter block or a flat YAML file."""
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    body = front.group(1) if front else text
    fields = {}
    for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)[ \t]*$", body, re.M):
        fields.setdefault(match.group(1), match.group(2).strip().strip("\"'"))
    return fields


def _prange(fields: dict[str, str], every: set[int]) -> set[int]:
    text = fields.get("paragraphs", "")
    found: set[int] = set()
    for a, b in re.findall(r"P(\d+)(?:\s*[-–]\s*P(\d+))?", text):
        lo, hi = int(a), int(b or a)
        found.update(range(min(lo, hi), max(lo, hi) + 1))
    if found:
        return found
    target = fields.get("target", "")
    if re.search(r"whole\s+page", target, re.I) or re.search(r"whole\s+page", text, re.I):
        return set(every)
    ps = [int(x) for x in re.findall(r"\.P(\d+)", target)]
    if len(ps) >= 2:
        return set(range(min(ps), max(ps) + 1))
    if ps:
        return {ps[0]}
    return set()


def _kind_of(stem: str) -> str:
    if stem.startswith("rp-para-"):
        return "para"
    if stem.startswith("rp-sec-"):
        return "sec"
    if stem.startswith("rp-struct-"):
        return "struct"
    return ""


def run_rows(page: Path, every: set[int]) -> list[dict]:
    """Enumerate Page Writing Runs (RP) with status, version, and covered paragraphs."""
    runs_dir = page.parent / "runs"
    results_dir = page.parent / "results"
    rows = []
    if not runs_dir.is_dir():
        return rows
    for ticket in sorted(runs_dir.glob("rp-*.md")):
        stem = ticket.stem
        kind = _kind_of(stem)
        if not kind:
            continue
        number = re.search(r"-(\d+)", stem)
        ticket_fields = _front(_read(ticket))
        runtime = results_dir / stem / "runtime.yaml"
        runtime_fields = _front(_read(runtime)) if runtime.is_file() else {}
        fields = dict(ticket_fields)
        fields.update({k: v for k, v in runtime_fields.items() if v})
        versions = sorted((results_dir / stem).glob("v[0-9][0-9][0-9].md")) \
            if (results_dir / stem).is_dir() else []
        version = runtime_fields.get("version") or (versions[-1].stem if versions else "")
        rows.append({
            "id": stem,
            "kind": kind,
            "nn": int(number.group(1)) if number else 0,
            "ticket": ticket,
            "results": results_dir / stem,
            "runtime": runtime,
            "status": (fields.get("status") or "").lower(),
            "version": version,
            "step": runtime_fields.get("step", ""),
            "covers": _prange(fields, every),
        })
    return rows


def _owning_run(rows: list[dict], p: int) -> tuple[dict | None, str]:
    def covers(row):
        return p in row["covers"]
    open_rows = [r for r in rows if r["status"] in OPEN_STATUSES]
    for kind in ("para", "struct", "sec"):
        candidates = [r for r in open_rows if r["kind"] == kind and covers(r)]
        if candidates:
            return max(candidates, key=lambda r: r["nn"]), "append"
    finished = [r for r in rows if r["kind"] == "para" and covers(r)]
    if finished:
        return max(finished, key=lambda r: r["nn"]), "reopen"
    return None, "allocate"


# ── reading the note thread back ───────────────────────────────────────────

def _section_body(text: str, heading: str) -> str:
    hit = re.search(
        rf"^###[ \t]+{re.escape(heading)}[ \t]*$\n(.*?)(?=^###[ \t]+|^##[ \t]+|\Z)",
        text, re.M | re.S)
    return hit.group(1) if hit else ""


def _target_paragraphs(target: str, every: dict[int, str]) -> list[int]:
    found: set[int] = set()
    addressed = [int(x) for x in re.findall(r"C\d+\.P(\d+)", target)]
    if re.search(r"C\d+\.P\d+(?:\.B\d+(?:\s*[-–]\s*B\d+)?)?\s*[-–]\s*C\d+\.P\d+", target) \
            and len(addressed) >= 2:
        found.update(range(min(addressed), max(addressed) + 1))
    else:
        found.update(addressed)
    for a, b in re.findall(r"(?<![.\w])P(\d{2,})(?:\s*[-–]\s*P(\d{2,}))?", target):
        lo, hi = int(a), int(b or a)
        found.update(range(min(lo, hi), max(lo, hi) + 1))
    return sorted(p for p in found if p in every)


def feedback_items(page: Path) -> dict[str, list[dict]]:
    """Return `C<n>.P<m>` → Feedback items from every RP Version journal."""
    paras = paragraphs(page)
    every = {v["p"]: k for k, v in paras.items()}
    out: dict[str, list[dict]] = {k: [] for k in paras}
    results_dir = page.parent / "results"
    if not results_dir.is_dir():
        return out
    for vfile in sorted(results_dir.glob("rp-*/v[0-9][0-9][0-9].md")):
        text = _read(vfile)
        steps = list(re.finditer(r"^##[ \t]+Step[ \t]+(s\d{3})\b.*$", text, re.M))
        closure = re.search(r"^##[ \t]+Version closure[ \t]*$", text, re.M)
        for index, match in enumerate(steps):
            end = steps[index + 1].start() if index + 1 < len(steps) else (
                closure.start() if closure and closure.start() > match.end() else len(text))
            section = text[match.end():end]
            human = _section_body(section, "Human feedback")
            saved = _section_body(section, "Saved result")
            pending = bool(human.strip()) and not saved.strip()
            dispositions = dict(re.findall(r"^\|[ \t]*(F\d+)[ \t]*\|[ \t]*([^|]*?)[ \t]*\|", saved, re.M))
            source = re.search(r"^Source:[ \t]*(.*)$", human, re.M)
            for item in re.finditer(r"^####[ \t]+Feedback[ \t]+(F\d+)[ \t]*$\n(.*?)(?=^####[ \t]+|\Z)",
                                    human, re.M | re.S):
                label, body = item.group(1), item.group(2)
                fields = {k.strip(): v.strip() for k, v in
                          re.findall(r"^- ([A-Za-z][A-Za-z /]*?):[ \t]*(.*)$", body, re.M)}
                targets = _target_paragraphs(fields.get("Target", ""), every)
                if not targets or len(targets) > MAX_GROUP:
                    continue
                by = fields.get("By", "")
                origin = source.group(1).strip() if source else ""
                date = re.search(r"\d{6} \d{4} UTC", by or origin)
                # A composer note is signed `By: <name> · <date>`; a historical
                # chat Step carries only its Source line, so it reads as `chat`.
                author = re.split(r"\s*·\s*", by)[0].strip() if by else "chat"
                record = {
                    "run": vfile.parent.name, "version": vfile.stem, "step": match.group(1),
                    "label": label, "id": fields.get("Id", ""),
                    "kind": (fields.get("Kind") or "feedback").lower(),
                    "author": author, "date": date.group(0) if date else "",
                    "target": fields.get("Target", ""),
                    "comment": fields.get("Human comment", "").strip("`"),
                    "group": targets,
                    "pending": pending,
                    "disposition": "pending" if pending else (dispositions.get(label) or "recorded"),
                }
                for p in targets:
                    out[every[p]].append(record)
    return out


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
      var response = await fetch('/_board/outline', {
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


# ── the write · one pending Step item in the owning Run's journal ──────────

def _step_numbers(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"^##[ \t]+Step[ \t]+s(\d{3})\b", text, re.M)]


def _pending_last_step(text: str) -> bool:
    steps = list(re.finditer(r"^##[ \t]+Step[ \t]+s\d{3}\b.*$", text, re.M))
    if not steps:
        return False
    tail = text[steps[-1].end():]
    if re.search(r"^##[ \t]+Version closure", tail, re.M):
        return False
    return bool(_section_body(tail, "Human feedback").strip()) and \
        not _section_body(tail, "Saved result").strip()


def _item_block(number: int, fid: str, target: str, p: int, kind: str, author: str, now: str,
                reviewed: str, comment: str) -> str:
    one_line = " ".join(comment.split())
    block = (
        "#### Feedback F%02d\n\n"
        "- Id: %s\n"
        "- Target: `%s` · P%02d\n"
        "- Kind: %s\n"
        "- By: %s · %s\n"
        "- Selected quote: explicitly absent\n"
        "- Source Version/Step: %s\n"
        "- Human comment: %s\n"
        "- Agent interpretation: pending\n"
        % (number, fid, target, p, kind, author, now, reviewed, one_line))
    if "\n" in comment.strip():
        block += "\n```text\n%s\n```\n" % comment.strip()
    return block


def _step_block(step: int, run_id: str, reviewed: str, paragraph: str, p: int, brief: str,
                base: str, author: str, now: str, comment: str, item: str) -> str:
    return (
        "\n## Step s%03d\n\n"
        "### Human feedback\n\n"
        "```text\n"
        "Source: Draft Space feedback composer · %s · %s\n"
        "Reviewed output: %s\n"
        "Mode: pending · the agent chooses local-edit | paragraph-rewrite | structure when it completes this Step\n"
        "Scope: %s · P%02d · %s\n"
        "Base: %s\n"
        "Protected: every other paragraph and all accepted text until this Step is completed\n"
        "```\n\n"
        "#### Original request\n\n"
        "```text\n%s\n```\n\n"
        "%s" % (step, author, now, reviewed, paragraph, p, brief or "no brief in the plan", base,
                comment.strip(), item))


def _version_header(run_id: str, version: str, prior: str, note: str) -> str:
    return ("Run: %s\nVersion: %s\nState: open\nPrior Version: %s\n%s\n"
            % (run_id, version, prior, note))


def _set_yaml_key(text: str, key: str, value: str) -> str:
    pattern = re.compile(r"^%s:[ \t]*.*$" % re.escape(key), re.M)
    line = "%s: %s" % (key, value)
    if pattern.search(text):
        return pattern.sub(lambda _m: line, text, count=1)
    return text.rstrip("\n") + "\n" + line + "\n"


def _write_runtime(row: dict, page: Path, version: str, step: str, vfile: Path,
                   prior_file: Path | None) -> None:
    runtime = row["runtime"]
    rel_result = "results/%s" % row["id"]
    if runtime.is_file():
        text = _read(runtime)
    else:
        text = (
            "run: %s\nfamily: page\noperation: interactive-writing\ninteraction: human-feedback\n"
            "target: %s\nparagraphs: %s\nticket: runs/%s.md\nresult: %s\n"
            "status: ready\nversion: %s\nstep: s000\nversion_file: %s/%s.md\nversion_sha256: null\n"
            "worker:\n  kind: skill\n  name: haipipe-writing\n"
            "started_at: null\nfinished_at: null\nsupersedes: null\nfailure: null\n"
            "analysis:\n  status: deferred\n  task_run: null\n  input_sha256: null\n  result: null\n"
            % (row["id"], row.get("target", ""), row.get("paragraphs", ""), row["id"], rel_result,
               version, rel_result, version))
    text = _set_yaml_key(text, "status", "waiting-for-feedback")
    text = _set_yaml_key(text, "version", version)
    text = _set_yaml_key(text, "step", step)
    text = _set_yaml_key(text, "version_file", "%s/%s" % (rel_result, vfile.name))
    text = _set_yaml_key(text, "version_sha256", _sha(vfile))
    text = _set_yaml_key(text, "finished_at", "null")
    if prior_file is not None:
        text = _set_yaml_key(text, "supersedes", "%s/%s" % (rel_result, prior_file.name))
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(text, encoding="utf-8")


_WORKING_KEYS = ("Current version/step", "Current", "State", "Open feedback", "Next action", "Next")


def _write_working(row: dict, version: str, step: str, label: str, kind: str, paragraph: str,
                   author: str, now: str) -> None:
    path = row["results"] / "working.md"
    text = _read(path) if path.is_file() else "# %s · working state\n\n" % row["id"]
    values = {
        "Current version/step": "%s/%s" % (version, step),
        "Current": "%s/%s" % (version, step),
        "State": "waiting-for-feedback · Draft Space note %s pending an agent Step" % label,
        "Open feedback": "%s · %s on %s · from Draft Space by %s · %s · agent Step pending"
                         % (label, kind, paragraph, author, now),
        "Next action": "the agent completes Step %s (fast feedback path) for %s" % (step, label),
        "Next": "the agent completes Step %s (fast feedback path) for %s" % (step, label),
    }
    seen = set()
    for key in _WORKING_KEYS:
        pattern = re.compile(r"^(\s*[-*]?\s*(?:\*\*)?)(%s)((?:\*\*)?:)[ \t]*.*$" % re.escape(key),
                             re.M | re.I)
        if pattern.search(text):
            text = pattern.sub(lambda m: "%s%s%s %s" % (m.group(1), m.group(2), m.group(3), values[key]),
                               text, count=1)
            seen.add(key.split(" ")[0].lower())
    lines = []
    if "current" not in seen:
        lines.append("- Current version/step: %s" % values["Current"])
    if "state" not in seen:
        lines.append("- State: %s" % values["State"])
    if "open" not in seen:
        lines.append("- Open feedback: %s" % values["Open feedback"])
    if "next" not in seen:
        lines.append("- Next action: %s" % values["Next action"])
    if lines:
        text = text.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _allocate(page: Path, paragraph: str, para: dict, rows: list[dict], author: str, now: str) -> dict:
    nn = max([r["nn"] for r in rows if r["kind"] == "para"], default=0) + 1
    run_id = "rp-para-%02d_P%02d" % (nn, para["p"])
    ticket = page.parent / "runs" / ("%s.md" % run_id)
    ticket.parent.mkdir(parents=True, exist_ok=True)
    plan = plan_path(page)
    ticket.write_text(
        "---\nfamily: page\noperation: interactive-writing\ninteraction: human-feedback\n"
        "target: %s\nparagraphs: P%02d\nresult: results/%s\npage: %s\nrun: %s\n---\n\n"
        "# %s\n\n"
        "- Goal: capture and settle Draft Space feedback on P%02d · %s · %s.\n"
        "- RP kind: %s\n"
        "- Mermaid Structure description: P%02d · %s · %s\n"
        "- Page and Board: `%s`\n"
        "- Scope: P%02d at %s only; every other paragraph is protected.\n"
        "- Sources: current Page source, `%s`, and the closed `rp-struct-01` result when present.\n"
        "- Success: the person explicitly accepts or revises P%02d after the note is answered.\n"
        "- Review: P%02d read as one paragraph.\n"
        "- Allocated by: Draft Space feedback composer · %s · %s\n"
        % (paragraph, para["p"], run_id, page.stem, run_id, run_id,
           para["p"], paragraph, para.get("brief") or "no brief in the plan", run_id,
           para["p"], paragraph, para.get("brief") or "no brief in the plan", page.name,
           para["p"], paragraph, "outline/%s" % plan.name if plan else "the current plan",
           para["p"], para["p"], author, now),
        encoding="utf-8")
    results = page.parent / "results" / run_id
    results.mkdir(parents=True, exist_ok=True)
    return {"id": run_id, "kind": "para", "nn": nn, "ticket": ticket, "results": results,
            "runtime": results / "runtime.yaml", "status": "ready", "version": "", "step": "",
            "covers": {para["p"]}, "target": paragraph, "paragraphs": "P%02d" % para["p"]}


def _already_saved(row: dict, fid: str) -> bool:
    if not row["results"].is_dir():
        return False
    return any(("- Id: %s" % fid) in _read(v) for v in row["results"].glob("v[0-9][0-9][0-9].md"))


def save_feedback(page: Path, payload: dict, read_only: bool = False):
    """Append one Feedback item to the owning Run's journal; return (result, error)."""
    if read_only:
        return None, "This Page is served read-only; notes cannot be saved here"
    paragraph = str(payload.get("paragraph") or "").strip()
    if not _PARAGRAPH_RE.fullmatch(paragraph):
        return None, "Choose a paragraph"
    kind = str(payload.get("kind") or "explore").strip().lower()
    if kind not in KINDS:
        return None, "Kind must be explore, wording, or accept"
    bullet = str(payload.get("bullet") or "").strip()
    if bullet and not _BULLET_RE.fullmatch(bullet):
        return None, "Bullet address is not valid"
    author = " ".join(str(payload.get("author") or "").split())
    if not author or len(author) > 80 or "·" in author:
        return None, "Sign the note with a name (no middle-dot separator, at most 80 characters)"
    comment = str(payload.get("comment") or "").strip()
    if not comment or len(comment) > 8000:
        return None, "Write the note (at most 8,000 characters)"
    fid = str(payload.get("feedback_id") or "").strip()
    if not _ID_RE.fullmatch(fid):
        fid = "fb-" + secrets.token_hex(8)
    now = _now()

    with page_lock(page):
        paras = paragraphs(page)
        if paragraph not in paras:
            return None, "Paragraph is not in the current plan; reload Draft Space"
        para = paras[paragraph]
        if bullet and bullet not in para["bullets"]:
            return None, "Bullet is not in that paragraph; reload Draft Space"
        every = {v["p"] for v in paras.values()}
        rows = run_rows(page, every)
        row, mode = _owning_run(rows, para["p"])
        if mode == "allocate":
            row = _allocate(page, paragraph, para, rows, author, now)
            mode = "append"
        elif _already_saved(row, fid):
            items = feedback_items(page).get(paragraph, [])
            return _result(page, row, row.get("version", ""), row.get("step", ""), "", fid, paragraph,
                           items, None), None

        results = row["results"]
        results.mkdir(parents=True, exist_ok=True)
        versions = sorted(results.glob("v[0-9][0-9][0-9].md"))
        current = results / ("%s.md" % row["version"]) if row["version"] else None
        if current is not None and not current.is_file():
            current = versions[-1] if versions else None
        prior_file = None
        target = bullet or paragraph
        plan = plan_path(page)
        base = "; ".join(filter(None, [
            ("outline/%s SHA-256 %s" % (plan.name, _sha(plan))) if plan else "",
            "%s SHA-256 %s" % (page.name, _sha(page)) if page.is_file() else "",
        ]))
        reopen = mode == "reopen" or (current is not None and
                                      re.search(r"^##[ \t]+Version closure", _read(current), re.M))
        if current is None:
            version = "v001"
            vfile = results / "v001.md"
            text = _version_header(row["id"], version, "none",
                                   "Opened by: Draft Space feedback composer · %s · %s" % (author, now))
            reviewed = "initial state"
        elif reopen:
            prior_file = current
            version = "v%03d" % (int(current.stem[1:]) + 1)
            vfile = results / ("%s.md" % version)
            prior_step = row.get("step") or ("s%03d" % max(_step_numbers(_read(current)) or [0]))
            text = _version_header(
                row["id"], version, "%s · SHA-256 %s" % (current.name, _sha(current)),
                "Reopened by: Draft Space feedback composer · %s · %s · kind %s · target %s\n"
                "Protected: the accepted text of this Run's paragraphs stays byte-for-byte until a "
                "completed Step changes it" % (author, now, kind, target))
            reviewed = "%s %s/%s" % (row["id"], current.stem, prior_step)
        else:
            version = current.stem
            vfile = current
            text = _read(current)
            steps = _step_numbers(text)
            reviewed = ("%s %s/s%03d" % (row["id"], version, steps[-1])) if steps else "initial state"

        if vfile.is_file() and _pending_last_step(text):
            step_number = max(_step_numbers(text))
            existing = len(re.findall(r"^####[ \t]+Feedback[ \t]+F\d+", text[text.rfind("## Step s"):], re.M))
            item = _item_block(existing + 1, fid, target, para["p"], kind, author, now, reviewed, comment)
            text = text.rstrip("\n") + "\n\n" + item
            label = "F%02d" % (existing + 1)
        else:
            step_number = (max(_step_numbers(text)) + 1) if _step_numbers(text) else 1
            item = _item_block(1, fid, target, para["p"], kind, author, now, reviewed, comment)
            text = text.rstrip("\n") + "\n" + _step_block(
                step_number, row["id"], reviewed, paragraph, para["p"], para.get("brief", ""),
                base, author, now, comment, item)
            label = "F01"
        step = "s%03d" % step_number
        vfile.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
        _write_runtime(row, page, version, step, vfile, prior_file)
        _write_working(row, version, step, label, kind, paragraph, author, now)
        items = feedback_items(page).get(paragraph, [])
        return _result(page, row, version, step, label, fid, paragraph, items, vfile), None


def _result(page: Path, row: dict, version: str, step: str, label: str, fid: str, paragraph: str,
            items: list[dict], vfile: Path | None) -> dict:
    if vfile is None:
        vfile = row["results"] / ("%s.md" % version) if version else row["results"]
    try:
        shown = str(vfile.relative_to(page.parent))
    except ValueError:
        shown = str(vfile)
    if not label:
        label = next((i["label"] for i in items if i.get("id") == fid), "")
    return {
        "run": row["id"], "run_version": version, "step": step, "feedback": label, "id": fid,
        "file": shown, "paragraph": paragraph,
        "count": len(items), "pending": sum(1 for i in items if i["pending"]),
        "summary": feedback_summary(items), "list_html": feedback_list_html(items),
    }
