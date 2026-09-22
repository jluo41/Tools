"""Revise view: one box per paragraph, pre-filled with its current Draft, edit in place.

JL 260922: "我想让每一个 paragraph 是一个方框，然后你把现在的 draft（也就是更新后的
draft）copy 过去 … 这样我就可以在上面改了." So each paragraph is one text box
holding its Draft sentences, one sentence per line, and one Save. The Draft a
reader sees in Reading view is the Draft field of each Outline Bullet, so on
Save the box's lines go back to the paragraph's Bullets in order: line 1 → B1,
line 2 → B2, … Extra lines join the last Bullet's Draft; missing lines clear
the Bullets left over. Nothing else in the Outline moves.

Every Save does two things under the page lock:

1. writes the changed Draft fields back into the selected Outline Markdown,
   guarded by the Bullet and Draft tokens the page was rendered with;
2. opens or extends the paragraph's Revise Run (`rp-revise-NN_<C.P>`,
   haipipe-page-revise) with one Step whose Saved result is a change ledger in
   the Step-template `#### Track changes` shape, one card per changed Bullet,
   Decision `accept` because the person typed it. Run Space renders it.

Nothing here touches Page Content; adopting Drafts stays at the release boundary.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

from src.outline_version import latest_outline, version_tag
from src.plan_shape import iter_plan_bullets
from live.outline_preview import (bullet_token, draft_path, page_lock, read_drafts,
                                  reader_prose, record_token, write_drafts)

_RUN_RE = re.compile(r"^rp-revise-(?P<number>\d{2,})_(?P<target>[A-Za-z0-9._-]+)$")
_ADDRESS_RE = re.compile(r"^C\d+\.P\d+$")
_BULLET_RE = re.compile(r"^C\d+\.P\d+\.B\d+$")
MAX_TEXT = 40000


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


_REALIZES_RE = re.compile(r"(?m)^([^\n]*?)<!--\s*realizes:\s*(C\d+\.P\d+\.[BS]\d+)\s*-->\s*$")


def page_realizations(page_src: Path) -> dict[str, str]:
    """Bullet address -> the Page Content sentence(s) that realize it.

    The same reading the Table and Reading views fall back to when an Outline
    Bullet has no Draft field: the box starts from these sentences, and they
    are the ledger's Before when a Save writes the first Draft over them.
    """
    try:
        text = page_src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    found: dict[str, list[str]] = {}
    for match in _REALIZES_RE.finditer(text):
        address = re.sub(r"\.S(\d+)$", r".B\1", match.group(2))
        prose = reader_prose(match.group(1)).strip()
        if prose:
            found.setdefault(address, []).append(prose)
    return {address: " ".join(lines) for address, lines in found.items()}


def _effective(records: dict, realized: dict, address: str) -> str:
    draft = " ".join(((records.get(address) or {}).get("text", "")).split())
    return draft or " ".join(realized.get(address, "").split())


_PROTECT_RE = re.compile(r"\b(?:e\.g\.|i\.e\.|et al\.|cf\.|vs\.|Dr\.|Mr\.|Ms\.|Prof\.|Fig\.|Eq\.|No\.|St\.|Jr\.|Inc\.|Ltd\.|[A-Z]\.)", re.I)
_END_RE = re.compile(r"[.!?]['\"”’)\]]*\s+(?=[\"“'(\[A-Z0-9])|[。！？]['\"”’)\]]*\s*")


def split_sentences(text: str) -> list[str]:
    """One sentence per line for the box (JL: "each sentence separated with a new line").

    Abbreviations, initials, decimals and citation braces are protected so a
    split lands only after a real sentence end. A wrong split is harmless: on
    Save the lines of one point are joined back with spaces.
    """
    text = " ".join(text.split())
    if not text:
        return []
    guarded = re.sub(r"(?<=\d)\.(?=\d)", "\u0000", text)
    guarded = _PROTECT_RE.sub(lambda m: m.group(0).replace(".", "\u0000"), guarded)
    guarded = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(".", "\u0000").replace(" ", "\u0001"), guarded)
    parts, start = [], 0
    for match in _END_RE.finditer(guarded):
        parts.append(guarded[start:match.end()])
        start = match.end()
    parts.append(guarded[start:])
    cleaned = [p.replace("\u0000", ".").replace("\u0001", " ").strip() for p in parts]
    return [p for p in cleaned if p]


def box_text(texts: list[str]) -> str:
    """The box: each point's sentences one per line, a blank line between points."""
    return "\n\n".join("\n".join(split_sentences(t)) for t in texts if t and t.strip())


# ---------------------------------------------------------------- rendering

def revise_rows_html(paragraph: str, display_paragraph: str, rows: list[dict], *,
                     read_only: bool = False, path_q: str = "", file_q: str = "") -> str:
    """One form per paragraph: one box with the current Draft, one Save.

    `rows` carry address, bullet_id, text, bullet_token and record_token for
    every Bullet of the paragraph, in plan order. The box shows the drafted
    sentences one per line; the Bullet list rides along as data so a Save can
    map lines back and detect a page rendered before someone else's edit.
    """
    if not rows:
        return '<div class="revise-empty">No points to revise yet; shape the paragraph first.</div>'
    text = box_text([row["text"] for row in rows])
    bullets = json.dumps([{"address": r["address"], "bullet": r["bullet_token"], "record": r["record_token"]}
                          for r in rows], separators=(",", ":"))
    disabled = " disabled" if read_only else ""
    box = ('<textarea name="text" class="revise-box" data-bullets="%s" aria-label="Draft of %s" '
           'placeholder="One sentence per line; a blank line separates points (%s, %s …)"%s>%s</textarea>'
           % (_e(bullets), _e(display_paragraph), _e(rows[0]["bullet_id"]),
              _e(rows[1]["bullet_id"]) if len(rows) > 1 else "B2", disabled, _e(text)))
    actions = ('<div class="revise-actions"><span class="mut">read-only host</span></div>' if read_only else
               '<div class="revise-actions"><input type="text" name="why" class="revise-why" '
               'placeholder="Why (optional)" aria-label="Why this change">'
               '<button type="button" class="revise-reset" data-revise-reset>Reset</button>'
               '<button type="submit" class="revise-save" data-revise-save>Save</button>'
               '<span class="revise-status" role="status" aria-live="polite"></span></div>')
    return (
        '<form class="revise-form" data-paragraph="%s" data-display="%s" data-path="%s" '
        'data-file="%s" data-points="%d" autocomplete="off">%s%s</form>'
        % (_e(paragraph), _e(display_paragraph), _e(path_q), _e(file_q), len(rows), box, actions)
    )


def assets_html(read_only: bool = False) -> str:
    """CSS always; the Save script only where a Save exists (read-only hosts get none)."""
    css, _, script = _ASSETS.partition('</style>')
    return css + '</style>' + ('' if read_only else script)


_ASSETS = r'''<style>
.paragraph-revise{display:none}
.draft-lens[data-draft-mode="revise"] .paragraph-bullets,.draft-lens[data-draft-mode="revise"] .paragraph-reading{display:none}
.draft-lens[data-draft-mode="revise"] .paragraph-revise{display:block}
.draft-lens[data-draft-mode="revise"] details.paragraph-group>summary{cursor:pointer}
.draft-lens[data-draft-mode="revise"] .paragraph-group{margin-bottom:22px}
.revise-run-note{display:none;margin:-5px 0 12px;padding:7px 10px;border-left:2px solid var(--acc);color:var(--mut);font-size:12px;line-height:1.5}
.draft-lens[data-draft-mode="revise"] .revise-run-note{display:block}
.revise-form{display:block;padding:4px 0 2px}
.revise-box{box-sizing:border-box;width:100%;max-width:78ch;min-height:5.5em;resize:vertical;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);padding:10px 12px;font:15px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;field-sizing:content}
.revise-box:focus{border-color:var(--acc);outline:none}
.revise-box.changed{border-color:var(--acc);box-shadow:inset 3px 0 0 var(--acc)}
.revise-box:disabled{background:transparent;border-color:var(--line)}
.revise-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 0 0}
.revise-why{flex:1 1 12em;min-width:0;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);padding:4px 8px;font:12.5px system-ui,sans-serif}
.revise-save,.revise-reset{font:600 12px/1.4 system-ui,sans-serif;border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer;background:var(--card);color:var(--fg)}
.revise-save{border-color:var(--acc);color:var(--acc)}
.revise-save:disabled,.revise-reset:disabled{opacity:.5;cursor:default}
.revise-status{font:12px system-ui,sans-serif;color:var(--mut)}
.revise-status.err{color:var(--warn)}
.revise-empty{color:var(--mut);font-size:12.5px;padding:6px 0}
@media (max-width:700px){.revise-box{font-size:15px;padding:8px 10px}}
</style><script>
(function(){
 if(window.__draftRevise)return; window.__draftRevise=true;
 function box(form){return form.querySelector('.revise-box');}
 function dirty(form){var b=box(form);return b&&b.value.trim()!==b.defaultValue.trim();}
 function mark(form){var d=dirty(form);var b=box(form);if(b)b.classList.toggle('changed',d);var save=form.querySelector('[data-revise-save]');if(save)save.disabled=!d;var reset=form.querySelector('[data-revise-reset]');if(reset)reset.disabled=!d;return d;}
 function status(form,text,err){var s=form.querySelector('.revise-status');if(!s)return;s.textContent=text;s.classList.toggle('err',!!err);}
 function payload(form){var params=new URLSearchParams(location.search);var why=form.querySelector('.revise-why');var b=box(form);return{action:'revise',path:form.dataset.path||params.get('path')||'',file:form.dataset.file||params.get('file')||'',paragraph:form.dataset.paragraph,display:form.dataset.display||'',why:why?why.value.trim():'',text:b.value,bullets:JSON.parse(b.dataset.bullets||'[]')};}
 function reflect(change){var line=document.querySelector('.reading-line[data-point="'+change.address+'"] .reading-copy');if(line)line.textContent=change.text||'Not drafted';var id='bullet-'+change.address.replace(/\./g,'-');var row=document.getElementById(id);var copy=row?row.querySelector('.preview-copy'):null;if(copy)copy.textContent=change.text||'Not drafted';}
 document.addEventListener('input',function(e){var form=e.target.closest&&e.target.closest('form.revise-form');if(form&&e.target.classList.contains('revise-box'))mark(form);});
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-revise-reset]');if(!b)return;var form=b.closest('form.revise-form');var t=box(form);t.value=t.defaultValue;mark(form);status(form,'');});
 document.addEventListener('keydown',function(e){var t=e.target.closest&&e.target.closest('.revise-box');if(t&&(e.metaKey||e.ctrlKey)&&e.key==='Enter'){e.preventDefault();t.form.requestSubmit();}});
 document.addEventListener('submit',function(e){
  var form=e.target.closest&&e.target.closest('form.revise-form');if(!form)return;e.preventDefault();
  if(!dirty(form)){status(form,'No changes to save.');return;}
  var body=payload(form),save=form.querySelector('[data-revise-save]');if(save)save.disabled=true;status(form,'Saving…');
  fetch('/_board/outline',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||'Unable to save');return j;});})
   .then(function(j){var b=box(form);b.value=j.text;b.defaultValue=j.text;b.dataset.bullets=JSON.stringify(j.bullets||[]);(j.changed||[]).forEach(reflect);
     var why=form.querySelector('.revise-why');if(why)why.value='';mark(form);
     var n=(j.changed||[]).length;status(form,n?'Saved · '+j.run+' · '+j.step+' · '+n+' sentence'+(n===1?'':'s')+' → Run Space':'Nothing changed.');})
   .catch(function(err){status(form,String(err.message||err),true);mark(form);});
 });
 window.addEventListener('beforeunload',function(e){if(Array.prototype.some.call(document.querySelectorAll('form.revise-form'),dirty)){e.preventDefault();e.returnValue='';}});
 document.querySelectorAll('form.revise-form').forEach(mark);
})();
</script>'''


# ------------------------------------------------------------------- saving

def _clean_line(value: str, address: str) -> str:
    text = " ".join(value.split())
    if "<!--" in text or text.startswith(("> Comment ", "## ", "- ")):
        raise ValueError("%s: Draft accepts prose, not hidden address records" % address)
    return text


def _open_run(page_src: Path, target: str) -> tuple[str, bool]:
    """-> (run id, existing) · reuse the target's running Revise Run, else allocate."""
    base = page_src.parent
    numbers = []
    candidates = []
    for folder in (base / "runs", base / "results"):
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            match = _RUN_RE.match(path.stem if path.is_file() else path.name)
            if not match:
                continue
            numbers.append(int(match.group("number")))
            if match.group("target") == target and path.is_dir():
                candidates.append(path)
    for result in sorted(candidates):
        runtime = result / "runtime.yaml"
        if runtime.is_file():
            status = re.search(r"(?m)^status:\s*([^#\n]+)", runtime.read_text(encoding="utf-8", errors="replace"))
            if status and status.group(1).strip().lower() in {"running", "open", "waiting-for-feedback"}:
                return result.name, True
    return "rp-revise-%02d_%s" % (max(numbers, default=0) + 1, target), False


def _card(number: int, address: str, before: str, after: str, why: str) -> str:
    kind = "first draft" if not before else "deletion" if not after else "wording"
    return (
        "##### R%02d · %s\n\n"
        "###### Target\n%s\n\n"
        "###### Before\n%s\n\n"
        "###### After\n%s\n\n"
        "###### Why\n%s\n\n"
        "###### Decision\naccept\n\n"
        "###### Preference status\nedited directly by the person in Draft Space → Revise\n"
        % (number, kind, address, before or "(no draft)", after or "(removed)", why)
    )


def _write_ledger(page_src: Path, run_id: str, existing: bool, target: str, display: str,
                  plan: Path, changes: list[dict], why: str) -> dict:
    base = page_src.parent
    runs = base / "runs"
    result = base / "results" / run_id
    runs.mkdir(parents=True, exist_ok=True)
    result.mkdir(parents=True, exist_ok=True)
    version_file = result / "v001.md"
    text = version_file.read_text(encoding="utf-8", errors="replace") if existing and version_file.is_file() else ""
    step_number = len(re.findall(r"(?m)^## Step s\d+", text)) + 1
    card_start = len(re.findall(r"(?m)^##### R\d+ ·", text)) + 1
    step = "s%03d" % step_number
    stamp = _now()
    why = why or "Edited directly in Draft Space → Revise."
    cards = "".join(_card(card_start + i, c["address"], c["before"], c["after"], why)
                    for i, c in enumerate(changes))
    block = (
        "## Step %s\n\n"
        "### Human feedback\n"
        "Direct edit of %s in Draft Space → Revise · %s.\n\n"
        "### Saved result\n\n"
        "#### Inputs\n"
        "- Before: %s · Draft fields as rendered (the Page's own sentence where no Draft existed)\n"
        "- After: the same file after this Save\n"
        "- Target: %s (%s)\n\n"
        "#### Summary\n"
        "%d sentence%s changed in %s.\n\n"
        "#### Track changes\n\n%s"
        % (step, display, stamp, "outline/" + plan.name, target, display,
           len(changes), "s"[:len(changes) != 1], display, cards)
    )
    if not text:
        text = ("Run: %s\nVersion: v001\nState: open\nTarget: %s\n\n" % (run_id, target)) + block
    else:
        text = text.rstrip("\n") + "\n\n" + block
    version_file.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
    if not existing or not (runs / (run_id + ".md")).is_file():
        (runs / (run_id + ".md")).write_text(
            "---\n"
            "family: page\noperation: interactive-writing\ninteraction: human-revise\n"
            "mode: revise\ntarget_scope: paragraph\ntarget: %s\nrun: %s\n"
            "ticket: runs/%s.md\nresult: results/%s\n"
            "---\n\n# %s\n\n"
            "- Purpose: the person revises the Draft of %s in place; every Save appends one Step "
            "with a change ledger.\n"
            "- Close rule: the person closes the Run when the paragraph reads right; the accepted "
            "Drafts stay in the Outline for the writing Run to adopt.\n"
            % (target, run_id, run_id, run_id, run_id, display), encoding="utf-8")
    total = len(re.findall(r"(?m)^##### R\d+ ·", text))
    summary = "%d change%s over %d Step%s" % (total, "s"[:total != 1], step_number, "s"[:step_number != 1])
    (result / "working.md").write_text(
        "# %s · Revise\n\n- State: open.\n- Target: paragraph %s (%s).\n- Summary: %s.\n"
        "- Latest: %s · %d sentence%s.\n"
        % (run_id, target, display, summary, step, len(changes), "s"[:len(changes) != 1]),
        encoding="utf-8")
    (result / "runtime.yaml").write_text(
        "run: %s\nfamily: page\noperation: interactive-writing\ninteraction: human-revise\n"
        "mode: revise\ntarget_scope: paragraph\ntarget: %s\n"
        "ticket: runs/%s.md\nresult: results/%s\nstatus: running\nversion: v001\nstep: %s\n"
        "version_file: results/%s/v001.md\nsummary: %s\n"
        % (run_id, target, run_id, run_id, step, run_id, summary), encoding="utf-8")
    return {"run": run_id, "step": step, "summary": summary,
            "result": str(result.relative_to(base))}


def _lines_to_bullets(text: str, addresses: list[str]) -> dict[str, str]:
    """Blank-line blocks → Bullets in order; a block's lines are one point's sentences.

    Without any blank line, each line is one point (the short form). Extra
    blocks join the last Bullet; missing blocks clear the Bullets left over.
    """
    blocks: list[list[str]] = [[]]
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if not line:
            if blocks[-1]:
                blocks.append([])
            continue
        blocks[-1].append(line)
    blocks = [b for b in blocks if b]
    if len(blocks) == 1 and len(addresses) > 1 and len(blocks[0]) > 1:
        blocks = [[line] for line in blocks[0]]
    joined = [" ".join(b) for b in blocks]
    mapped: dict[str, str] = {}
    for i, address in enumerate(addresses):
        if i < len(joined):
            mapped[address] = joined[i] if i < len(addresses) - 1 else " ".join(joined[i:])
        else:
            mapped[address] = ""
    return mapped


def save_revise(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """Map the box's lines onto the paragraph's Bullets, save what changed, extend the Revise Run."""
    if read_only:
        return None, "This host is read-only; Revise saves are disabled"
    paragraph = str(payload.get("paragraph") or "").strip()
    if not _ADDRESS_RE.match(paragraph):
        return None, "paragraph must be a C<n>.P<m> address"
    text = payload.get("text")
    if not isinstance(text, str) or len(text) > MAX_TEXT:
        return None, "text must be a string of at most 40,000 characters"
    listed = payload.get("bullets")
    if not isinstance(listed, list) or not listed or not all(isinstance(b, dict) for b in listed):
        return None, "bullets must list the paragraph's Bullets as rendered"
    why = str(payload.get("why") or "").strip()
    if len(why) > 500 or "<!--" in why:
        return None, "why must be one short line"
    addresses = [str(b.get("address") or "").strip() for b in listed]
    if not all(_BULLET_RE.match(a) and a.startswith(paragraph + ".") for a in addresses):
        return None, "every listed Bullet must sit inside %s" % paragraph
    with page_lock(page_src):
        plan = latest_outline(page_src.parent / "outline", page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        blocks = {b["address"]: b for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace"))}
        current = [a for a in blocks if a.startswith(paragraph + ".")]
        if current != addresses:
            return None, "%s's points changed since this page was opened; reload before saving" % paragraph
        records = read_drafts(page_src)
        realized = page_realizations(page_src)
        for item in listed:
            address = str(item.get("address"))
            if str(item.get("bullet") or "") != bullet_token(blocks[address]):
                return None, "Point %s changed; reload and review before saving" % address
            if str(item.get("record") or "") != record_token(records.get(address)):
                return None, "Draft %s changed in another editor; reload before saving" % address
        try:
            mapped = {a: _clean_line(t, a) for a, t in _lines_to_bullets(text, addresses).items()}
        except ValueError as exc:
            return None, str(exc)
        changed = []
        for address in addresses:
            before = _effective(records, realized, address)
            if before == mapped[address]:
                continue
            changed.append({"address": address, "before": before, "after": mapped[address]})
        if not changed:
            fresh = read_drafts(page_src)
            return {"paragraph": paragraph, "changed": [], "run": "", "step": "",
                    "text": box_text([_effective(fresh, realized, a) for a in addresses]),
                    "bullets": [{"address": a, "bullet": bullet_token(blocks[a]),
                                 "record": record_token(fresh.get(a))} for a in addresses],
                    "message": "nothing changed"}, None
        for item in changed:
            records[item["address"]] = {**records.get(item["address"], {}),
                                        "plan": version_tag(plan),
                                        "bullet-sha256": bullet_token(blocks[item["address"]]),
                                        "text": item["after"]}
        write_drafts(page_src, records)
        fresh = read_drafts(page_src)
        display = str(payload.get("display") or paragraph).strip() or paragraph
        run_id, existing = _open_run(page_src, paragraph)
        ledger = _write_ledger(page_src, run_id, existing, paragraph, display, plan, changed, why)
    return {
        "paragraph": paragraph,
        "run": ledger["run"], "step": ledger["step"], "summary": ledger["summary"],
        "result": ledger["result"], "outline": str(draft_path(page_src)),
        "version": version_tag(plan),
        "text": box_text([_effective(fresh, realized, a) for a in addresses]),
        "bullets": [{"address": a, "bullet": bullet_token(blocks[a]), "record": record_token(fresh.get(a))}
                    for a in addresses],
        "changed": [{"address": c["address"], "text": c["after"]} for c in changed],
    }, None
