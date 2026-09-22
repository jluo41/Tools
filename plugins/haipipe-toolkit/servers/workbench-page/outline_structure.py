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

from src.outline_version import latest_outline
from live.outline_preview import page_lock

_DIVISION_RE = re.compile(r"^## C(\d+)\b\s*(?:·\s*(.*))?$")
_PARAGRAPH_RE = re.compile(r"^### (C\d+\.P\d+)\b\s*(?:·\s*(.*))?$")
_SPAN_RE = re.compile(r"\s*·\s*S\d+\s+to\s+S\d+\s*$")
_LINE_RE = re.compile(r"^\s*(C\d+(?:\.P\d+)?)\s*(?:·\s*(.*?))?\s*$")
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
            title = ((match.group(2) or "") if match else line[4:]).strip()
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
    plan = latest_outline(page_src.parent / "outline", page_src.stem)
    if plan is None or not plan.is_file():
        return ""
    text = structure_text(plan.read_text(encoding="utf-8", errors="replace"))
    if not text:
        return ""
    editor = "" if read_only else (
        '<form class="structure-form" hidden data-path="%s" data-file="%s" autocomplete="off">'
        '<textarea name="text" class="structure-box" aria-label="Structure text" '
        'spellcheck="false">%s</textarea>'
        '<div class="structure-actions"><button type="submit" class="structure-save">Save</button>'
        '<button type="button" class="structure-cancel" data-structure-cancel>Cancel</button>'
        '<span class="structure-status" role="status" aria-live="polite"></span></div></form>'
        % (_e(path_q), _e(file_q), _e(text)))
    hint = "" if read_only else '<span class="structure-hint">click to edit</span>'
    return (
        '<details class="card structure-card" open aria-label="Structure">'
        '<summary class="structure-heading"><span>Structure</span>%s<code>%s</code></summary>'
        '<div class="structure-body"><pre class="structure-text"%s>%s</pre>%s</div></details>'
        % (hint, _e("outline/" + plan.name), "" if read_only else ' data-structure-edit tabindex="0"',
           _e(text), editor)
    )


# ------------------------------------------------------------------- saving

def _parse_text(text: str) -> list[dict]:
    """-> [{address, title, paragraphs: [{address, title}]}] from the box's lines."""
    rows: list[dict] = []
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
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
        if line.startswith("### "):
            paragraph = {"address": "", "title": line[4:].strip(), "heading": line, "body": []}
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
        plan = latest_outline(page_src.parent / "outline", page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        source = plan.read_text(encoding="utf-8", errors="replace")
        if _parse_text(structure_text(source)) == wanted:
            return {"text": structure_text(source), "changed": False, "summary": "nothing changed"}, None
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
                    out.append("### %s · %s" % (paragraph["address"], paragraph["title"]) if paragraph["title"]
                               else "### " + paragraph["address"])
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
        updated = "\n".join(out).rstrip("\n") + "\n"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent,
                                         prefix=plan.name + ".structure-", delete=False) as tmp:
            tmp.write(updated)
            temporary = Path(tmp.name)
        temporary.replace(plan)
        summary = ", ".join("%d %s" % (n, k) for k, n in changes.items() if n) or "headings rewritten"
        log = page_src.parent / "outline" / (page_src.stem + "-log.md")
        if log.is_file():
            with log.open("a", encoding="utf-8") as fh:
                fh.write("\n### %s · Structure text edited in Draft Space\n- **Headings**: %s\n"
                         % (dt.datetime.now().strftime("%y%m%d %H%M"), summary))
    return {"text": structure_text(updated), "changed": True, "summary": summary,
            "outline": str(plan)}, None


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
'''

STRUCTURE_JS = r'''<script>
(function(){
 if(window.__structureEdit)return; window.__structureEdit=true;
 function card(el){return el.closest('.structure-card');}
 function open(c){var form=c.querySelector('.structure-form');if(!form)return;form.hidden=false;c.classList.add('editing');var box=form.querySelector('.structure-box');box.value=c.querySelector('.structure-text').textContent;box.focus();}
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
  fetch('/_board/outline',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||'Unable to save');return j;});})
   .then(function(j){c.querySelector('.structure-text').textContent=j.text;close(c);
     if(j.changed){var s=c.querySelector('.structure-hint');if(s)s.textContent='saved · '+j.summary+' · reload to refresh the table';}})
   .catch(function(err){status.textContent=String(err.message||err);status.classList.add('err');});
 });
 window.addEventListener('beforeunload',function(e){var c=document.querySelector('.structure-card.editing');if(!c)return;var box=c.querySelector('.structure-box');if(box&&box.value.trim()!==c.querySelector('.structure-text').textContent.trim()){e.preventDefault();e.returnValue='';}});
})();
</script>'''
