"""The Page's structure as plain text you can click into and edit, like Scratch.

JL 260922: "我其实就只是想要一个文本而已。我可以点进去 edit，有点像 Scratch 一样 …
主要是方便我来去 operate." So the Structure card is one text block, one line per
Outline heading:

    C1 · Introduction
      C1.P1 · Establish consequential prescribing variation
      C1.P2 · Name the physician-psychology gap

Click the text and it becomes a box; Save writes the headings back into the
selected Outline. Supported edits: rename a section or paragraph, reorder the
lines, add a paragraph line (a new empty `### C<n>.P<m>` heading), and remove a
paragraph that has no points yet. A paragraph that already has Bullets cannot
be dropped or re-addressed here; that is `run-structure` work, and the save
says so. Bullets, Drafts, Notes and Evidence lines travel with their heading
untouched. There is no Mermaid map and no second source.
"""
from __future__ import annotations

import datetime as dt
import html
import re
import tempfile
from pathlib import Path

from src.outline_version import plan_dir, latest_outline, record_path
from src.plan_shape import canonical_plan
from src.plan_layout import (from_canonical, is_sectioned, normalize_overview, overview_lines,
                             set_overview, to_canonical)
from live.outline_preview import page_lock

_DIVISION_RE = re.compile(r"^## C(\d+)\b\s*(?:·\s*(.*))?$")
_PARAGRAPH_RE = re.compile(r"^### (C\d+\.P\d+)\b\s*(?:·\s*(.*))?$")
_SPAN_RE = re.compile(r"\s*·\s*S\d+\s+to\s+S\d+\s*$")
_LINE_RE = re.compile(r"^\s*(?:-\s*)?(C\d+(?:\.P\d+)?)\s*(?:·\s*(.*?))?\s*$")
MAX_TEXT = 20000


def _e(value) -> str:
    return html.escape(str(value), quote=True)


# ------------------------------------------------------------------ reading

def structure_rows(plan_text: str) -> list[dict]:
    """-> [{address, title, paragraphs: [{address, index, title, bullets, drafted}]}]

    Reads only the `## C<n>` divisions; the first other `## ` heading ends the
    plan's structure (Aims, Scratch and Notes follow it). Paragraph titles drop
    the `· S1 to S3` sentence-span suffix the Shape keeps for its own bookkeeping.
    """
    plan_text = canonical_plan(plan_text)
    rows: list[dict] = []
    division = paragraph = None
    index = 0
    for raw in plan_text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            match = _DIVISION_RE.match(line)
            if not match:
                if rows:
                    break
                continue
            division = {"address": "C%s" % match.group(1),
                        "title": (match.group(2) or "").strip(), "paragraphs": []}
            rows.append(division)
            paragraph = None
            continue
        if division is None:
            continue
        if line.startswith("### "):
            match = _PARAGRAPH_RE.match(line)
            if not match:
                # An unaddressed `### ` (e.g. `### Cut · …`) is a side note, not a
                # paragraph: it stays off the Structure text and moves with the
                # paragraph above it.
                paragraph = None
                continue
            title = (match.group(2) or "").strip()
            title = _SPAN_RE.sub("", title)
            index += 1
            paragraph = {"address": match.group(1) if match else "",
                         "index": "P%02d" % index, "title": title,
                         "bullets": 0, "drafted": 0}
            division["paragraphs"].append(paragraph)
            continue
        if paragraph is None:
            continue
        if re.match(r"^- ", line):
            paragraph["bullets"] += 1
        elif re.match(r"^\s+Draft:\s*\S", line):
            paragraph["drafted"] += 1
    return rows


def structure_text(plan_text: str) -> str:
    """The plain text: one line per heading, paragraphs indented two spaces."""
    lines = []
    for division in structure_rows(plan_text):
        lines.append("%s · %s" % (division["address"], division["title"]) if division["title"]
                     else division["address"])
        for paragraph in division["paragraphs"]:
            lines.append("  %s · %s" % (paragraph["address"], paragraph["title"])
                         if paragraph["title"] else "  " + paragraph["address"])
    return "\n".join(lines)


def structure_card_html(page_src: Path, *, read_only: bool = False,
                        path_q: str = "", file_q: str = "") -> str:
    """The Structure card: the text, and (unless read-only) the box behind it."""
    plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
    if plan is None or not plan.is_file():
        return ""
    raw = plan.read_text(encoding="utf-8", errors="replace")
    text = structure_text(raw)
    if not text:
        return ""
    entries = overview_lines(raw) if is_sectioned(raw) else []
    if entries:
        text = overview_box_text(entries)
    editor = "" if read_only else (
        '<form class="structure-form" hidden data-path="%s" data-file="%s" autocomplete="off">'
        '<textarea name="text" class="structure-box" aria-label="Structure text" '
        'spellcheck="false">%s</textarea>'
        '<div class="structure-actions"><button type="submit" class="structure-save">Save</button>'
        '<button type="button" class="structure-cancel" data-structure-cancel>Cancel</button>'
        '<span class="structure-status" role="status" aria-live="polite"></span></div></form>'
        % (_e(path_q), _e(file_q), _e(text)))
    hint = "" if read_only else '<span class="structure-hint"></span>'  # save feedback only
    edit = "" if read_only else ' data-structure-edit tabindex="0"'
    shown = ('<div class="structure-text structure-overview"%s data-text="%s">%s</div>'
             % (edit, _e(text), overview_html(entries)) if entries else
             '<pre class="structure-text"%s>%s</pre>' % (edit, _e(text)))
    return (
        '<details class="card structure-card" aria-label="Structure">'
        '<summary class="structure-heading"><span>Structure</span>%s</summary>'
        '<div class="structure-body">%s%s</div></details>'
        % (hint, shown, editor)
    )


def overview_box_text(entries: list[str]) -> str:
    """The Structure Overview as the box edits it: `C…` lines, `→` lines indented."""
    return "\n".join(line[2:] if line.startswith("- ") else line for line in entries)


def overview_html(entries: list[str]) -> str:
    """Division lines, then one block per paragraph: title, sentences and job, next question."""
    out, current = [], None
    for line in entries:
        entry = re.match(r"^- (C\d+(?:\.P\d+)?)\s*(?:·\s*(.*))?$", line)
        if entry:
            address, rest = entry.group(1), (entry.group(2) or "").strip()
            if "." not in address:
                title = rest.partition(" · ")[0]  # counts or notes after the title stay in the Markdown
                out.append('<div class=sov-division><span class=sov-addr>%s</span><b>%s</b></div>'
                           % (_e(address), _e(title)))
                current = None
                continue
            current = [('<div class=sov-title><span class=sov-addr>%s</span><b>%s</b></div>'
                        % (_e(address), _e(rest)))]
            out.append(current)
            continue
        note = line.strip().lstrip("→").strip()
        if current is None:
            continue
        span = re.match(r"^(S\d+(?:\s+to\s+S\d+)?)\s*(?:·\s*(.*))?$", note)
        nxt = re.match(r"^(C\d+\.P\d+)\s*:\s*(.*)$", note)
        if span:
            current.append('<div class=sov-job><span class=sov-span>%s</span>%s</div>'
                           % (_e(span.group(1)), _e(span.group(2) or "")))
        elif nxt:
            current.append('<div class=sov-next>→ <span class=sov-addr>%s</span>%s</div>'
                           % (_e(nxt.group(1)), _e(nxt.group(2))))
        else:
            current.append('<div class=sov-job>%s</div>' % _e(note))
    return "".join(x if isinstance(x, str) else '<div class=sov-para>%s</div>' % "".join(x) for x in out)


# ------------------------------------------------------------------- saving

def _parse_text(text: str) -> list[dict]:
    """-> [{address, title, paragraphs: [{address, title}]}] from the box's lines."""
    rows: list[dict] = []
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.strip().startswith("→"):
            continue  # a `→` line is a Structure Overview note, not a heading
        match = _LINE_RE.match(raw)
        if not match:
            raise ValueError("line %d must start with C<n> or C<n>.P<m>: %s" % (number, raw.strip()[:60]))
        address, title = match.group(1), (match.group(2) or "").strip()
        if "·" in title and not title.replace("·", "").strip():
            title = ""
        if "." not in address:
            if any(r["address"] == address for r in rows):
                raise ValueError("%s appears twice" % address)
            rows.append({"address": address, "title": title, "paragraphs": []})
            continue
        if not rows:
            raise ValueError("line %d: %s comes before any C<n> section line" % (number, address))
        division = rows[-1]
        if not address.startswith(division["address"] + "."):
            raise ValueError("%s is not inside %s; keep paragraph addresses under their section"
                             % (address, division["address"]))
        if any(p["address"] == address for d in rows for p in d["paragraphs"]):
            raise ValueError("%s appears twice" % address)
        division["paragraphs"].append({"address": address, "title": title})
    if not rows:
        raise ValueError("the structure needs at least one C<n> section line")
    return rows


def _parse_plan(lines: list[str]) -> tuple[list[str], list[dict], list[str]]:
    """Split the plan into preamble, division blocks (with their bodies), and tail."""
    first = end = None
    for i, line in enumerate(lines):
        if _DIVISION_RE.match(line):
            if first is None:
                first = i
        elif line.startswith("## ") and first is not None:
            end = i
            break
    if first is None:
        return lines, [], []
    if end is None:
        end = len(lines)
    blocks: list[dict] = []
    division = paragraph = None
    for line in lines[first:end]:
        d = _DIVISION_RE.match(line)
        if d:
            division = {"address": "C%s" % d.group(1), "title": (d.group(2) or "").strip(),
                        "heading": line, "body": [], "paragraphs": []}
            blocks.append(division)
            paragraph = None
            continue
        p = _PARAGRAPH_RE.match(line) if line.startswith("### ") else None
        if p:
            paragraph = {"address": p.group(1), "title": _SPAN_RE.sub("", (p.group(2) or "").strip()),
                         "heading": line, "body": []}
            division["paragraphs"].append(paragraph)
            continue
        (paragraph["body"] if paragraph is not None else division["body"]).append(line)
    return lines[:first], blocks, lines[end:]


def _points(body: list[str]) -> int:
    return sum(1 for line in body if re.match(r"^- ", line))


def _strip_trailing_blank(body: list[str]) -> list[str]:
    out = list(body)
    while out and not out[-1].strip():
        out.pop()
    return out


def save_structure(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """Rewrite the Outline's C/P headings from the box text; bodies travel untouched."""
    if read_only:
        return None, "This host is read-only; Structure edits are disabled"
    text = payload.get("text")
    if not isinstance(text, str) or len(text) > MAX_TEXT:
        return None, "text must be a string of at most 20,000 characters"
    if "<!--" in text:
        return None, "the structure text accepts headings, not hidden records"
    try:
        wanted = _parse_text(text)
    except ValueError as exc:
        return None, str(exc)
    with page_lock(page_src):
        plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        raw_source = plan.read_text(encoding="utf-8", errors="replace")
        source = to_canonical(raw_source)
        entries = None
        if is_sectioned(raw_source) and overview_lines(raw_source):
            try:
                entries = normalize_overview(text)
            except ValueError as exc:
                return None, str(exc)
        if _parse_text(structure_text(source)) == wanted:
            if entries is None or entries == overview_lines(raw_source):
                return {"text": text if entries else structure_text(source), "changed": False,
                        "summary": "nothing changed"}, None
            # Only the jobs and next questions changed: rewrite the overview alone.
            _atomic_write(plan, set_overview(raw_source, entries))
            return {"text": overview_box_text(entries), "changed": True,
                    "summary": "overview updated", "outline": str(plan)}, None
        lines = source.splitlines()
        preamble, blocks, tail = _parse_plan(lines)
        old_divisions = {b["address"]: b for b in blocks}
        old_paragraphs = {p["address"]: (b, p) for b in blocks for p in b["paragraphs"] if p["address"]}
        kept_paragraphs = {p["address"] for d in wanted for p in d["paragraphs"]}
        kept_divisions = {d["address"] for d in wanted}
        for address, (_block, paragraph) in old_paragraphs.items():
            if address not in kept_paragraphs and _points(paragraph["body"]):
                n = _points(paragraph["body"])
                return None, ("%s has %d point%s; move or remove them with run-structure before "
                              "dropping the paragraph" % (address, n, "s"[:n != 1]))
        for address, block in old_divisions.items():
            if address not in kept_divisions:
                unnamed = [p for p in block["paragraphs"] if not p["address"]]
                if unnamed or _points(block["body"]):
                    return None, "%s still holds content; move it with run-structure before dropping the section" % address
        changes = {"renamed": 0, "added": 0, "removed": 0, "moved": 0}
        out: list[str] = list(preamble)
        if out and out[-1].strip():
            out.append("")
        for position, division in enumerate(wanted):
            old = old_divisions.get(division["address"])
            if old is None:
                out.append("## %s · %s" % (division["address"], division["title"]) if division["title"]
                           else "## " + division["address"])
                changes["added"] += 1
                body: list[str] = []
                old_par_order: list[str] = []
            else:
                if division["title"] != old["title"]:
                    out.append("## %s · %s" % (division["address"], division["title"]) if division["title"]
                               else "## " + division["address"])
                    changes["renamed"] += 1
                else:
                    out.append(old["heading"])
                body = _strip_trailing_blank(old["body"])
                old_par_order = [p["address"] for p in old["paragraphs"]]
            out.extend(body)
            new_order = [p["address"] for p in division["paragraphs"]]
            if [a for a in old_par_order if a in kept_paragraphs] != [a for a in new_order if a in old_paragraphs]:
                changes["moved"] += 1
            for paragraph in division["paragraphs"]:
                previous = old_paragraphs.get(paragraph["address"])
                if previous is None:
                    out.append("### %s · %s" % (paragraph["address"], paragraph["title"]) if paragraph["title"]
                               else "### " + paragraph["address"])
                    changes["added"] += 1
                    continue
                _block, old_p = previous
                if paragraph["title"] != old_p["title"]:
                    # Keep the Shape's own `· S<a> to S<b>` span on a renamed heading.
                    span = _SPAN_RE.search(old_p["heading"])
                    span = span.group(0) if span else ""
                    out.append(("### %s · %s" % (paragraph["address"], paragraph["title"]) if paragraph["title"]
                                else "### " + paragraph["address"]) + span)
                    changes["renamed"] += 1
                else:
                    out.append(old_p["heading"])
                out.extend(_strip_trailing_blank(old_p["body"]))
            if old is not None:
                for p in old["paragraphs"]:
                    if not p["address"]:
                        out.append(p["heading"])
                        out.extend(_strip_trailing_blank(p["body"]))
            if position + 1 < len(wanted) or tail:
                out.append("")
        changes["removed"] = (len(old_paragraphs) - len([a for a in old_paragraphs if a in kept_paragraphs])
                              + len([a for a in old_divisions if a not in kept_divisions]))
        out.extend(tail)
        updated = from_canonical(raw_source, "\n".join(out).rstrip("\n") + "\n")
        if entries is not None:
            updated = set_overview(updated, entries)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent,
                                         prefix=plan.name + ".structure-", delete=False) as tmp:
            tmp.write(updated)
            temporary = Path(tmp.name)
        temporary.replace(plan)
        summary = ", ".join("%d %s" % (n, k) for k, n in changes.items() if n) or "headings rewritten"
        log = record_path(plan_dir(page_src.parent), page_src.stem, "log")
        log.parent.mkdir(parents=True, exist_ok=True)
        if log.is_file():
            with log.open("a", encoding="utf-8") as fh:
                fh.write("\n### %s · Structure text edited in Draft Space\n- **Headings**: %s\n"
                         % (dt.datetime.now().strftime("%y%m%d %H%M"), summary))
    return {"text": overview_box_text(entries) if entries is not None else structure_text(updated),
            "changed": True, "summary": summary, "outline": str(plan)}, None


def _atomic_write(plan: Path, text: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent,
                                     prefix=plan.name + ".structure-", delete=False) as tmp:
        tmp.write(text)
        temporary = Path(tmp.name)
    temporary.replace(plan)


# ------------------------------------------------------------------- assets

STRUCTURE_CSS = r'''
.structure-card{margin-bottom:14px;padding:0;overflow:hidden}
.structure-heading{display:flex;align-items:baseline;gap:8px;margin:0;padding:9px 14px;
 cursor:pointer;list-style:none;font-size:15px;font-weight:650;line-height:1.3}
.structure-heading::-webkit-details-marker{display:none}
.structure-heading::marker{display:none}
.structure-heading::before{content:"▸";color:var(--mut);font-size:13px;flex:0 0 auto}
.structure-card[open]>.structure-heading::before{content:"▾"}
.structure-card[open]>.structure-heading{border-bottom:1px solid var(--line)}
.structure-hint{color:var(--mut);font-size:11px;font-weight:500}
.structure-heading code{margin-left:auto;color:var(--mut);font-size:10.5px;font-weight:500}
.structure-body{padding:8px 14px 10px}
.structure-text{margin:0;padding:6px 8px;white-space:pre-wrap;overflow-wrap:anywhere;
 font:13.5px/1.6 ui-monospace,Menlo,monospace;color:var(--fg);border:1px solid transparent;border-radius:6px}
.structure-text[data-structure-edit]{cursor:text}
.structure-text[data-structure-edit]:hover,.structure-text[data-structure-edit]:focus-visible{border-color:var(--line);background:color-mix(in srgb,var(--acc) 4%,var(--card));outline:none}
.structure-card.editing .structure-text{display:none}
.structure-form[hidden]{display:none}
.structure-box{box-sizing:border-box;width:100%;min-height:8em;resize:vertical;border:1px solid var(--acc);border-radius:6px;
 background:var(--bg);color:var(--fg);padding:6px 8px;font:13.5px/1.6 ui-monospace,Menlo,monospace;field-sizing:content}
.structure-box:focus{outline:none}
.structure-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 0 0}
.structure-save,.structure-cancel{font:600 12px/1.4 system-ui,sans-serif;border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer;background:var(--card);color:var(--fg)}
.structure-save{border-color:var(--acc);color:var(--acc)}
.structure-status{font:12px system-ui,sans-serif;color:var(--mut)}
.structure-status.err{color:var(--warn)}
.run-structure pre.structure-text{border-color:transparent}
.structure-overview{font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:6px 8px}
.sov-division{display:flex;gap:8px;align-items:baseline;margin:0 0 8px}
.sov-para{padding:6px 0 7px 12px;border-left:2px solid var(--line);margin:0 0 6px}
.sov-title{display:flex;gap:8px;align-items:baseline}
.sov-addr{font:500 11.5px ui-monospace,Menlo,monospace;color:var(--mut)}
.sov-mut{color:var(--mut);font-size:12.5px}
.sov-job{color:var(--fg);font-size:13px;margin-top:2px}
.sov-span{font:500 11.5px ui-monospace,Menlo,monospace;color:var(--mut);margin-right:6px}
.sov-next{color:var(--acc);font-size:13px;margin-top:2px}
.sov-next .sov-addr{color:var(--acc);margin-right:5px}
'''

STRUCTURE_JS = r'''<script>
(function(){
 if(window.__structureEdit)return; window.__structureEdit=true;
 function card(el){return el.closest('.structure-card');}
 function open(c){var form=c.querySelector('.structure-form');if(!form)return;form.hidden=false;c.classList.add('editing');var box=form.querySelector('.structure-box');var shown=c.querySelector('.structure-text');box.value=shown.dataset.text||shown.textContent;box.focus();}
 function close(c){var form=c.querySelector('.structure-form');if(!form)return;form.hidden=true;c.classList.remove('editing');var s=form.querySelector('.structure-status');if(s){s.textContent='';s.classList.remove('err');}}
 document.addEventListener('click',function(e){
  var pre=e.target.closest&&e.target.closest('.structure-text[data-structure-edit]');
  if(pre){open(card(pre));return;}
  var cancel=e.target.closest&&e.target.closest('[data-structure-cancel]');
  if(cancel){close(card(cancel));}
 });
 document.addEventListener('keydown',function(e){
  var pre=e.target.closest&&e.target.closest('.structure-text[data-structure-edit]');
  if(pre&&(e.key==='Enter'||e.key===' ')){e.preventDefault();open(card(pre));return;}
  var box=e.target.closest&&e.target.closest('.structure-box');
  if(!box)return;
  if(e.key==='Escape'){close(card(box));}
  if((e.metaKey||e.ctrlKey)&&e.key==='Enter'){e.preventDefault();box.form.requestSubmit();}
 });
 document.addEventListener('submit',function(e){
  var form=e.target.closest&&e.target.closest('form.structure-form');if(!form)return;e.preventDefault();
  var c=card(form),status=form.querySelector('.structure-status'),params=new URLSearchParams(location.search);
  var body={action:'structure',path:form.dataset.path||params.get('path')||'',file:form.dataset.file||params.get('file')||'',text:form.querySelector('.structure-box').value};
  status.textContent='Saving…';status.classList.remove('err');
  fetch('/_board/draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||'Unable to save');return j;});})
   .then(function(j){var shown=c.querySelector('.structure-text');if(shown.dataset.text!==undefined){if(j.changed){location.reload();return;}shown.dataset.text=j.text;}else{shown.textContent=j.text;}close(c);
     if(j.changed){var s=c.querySelector('.structure-hint');if(s)s.textContent='saved · '+j.summary+' · reload to refresh the table';}})
   .catch(function(err){status.textContent=String(err.message||err);status.classList.add('err');});
 });
 window.addEventListener('beforeunload',function(e){var c=document.querySelector('.structure-card.editing');if(!c)return;var box=c.querySelector('.structure-box');var shown=c.querySelector('.structure-text');if(box&&box.value.trim()!==(shown.dataset.text||shown.textContent).trim()){e.preventDefault();e.returnValue='';}});
})();
</script>'''
