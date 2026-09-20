"""Human-first Scratch Runs for Draft Space.

Scratch is deliberately smaller than writing or feedback.  It records a
person's rough plan for one Page target, then asks the AI to produce a short
summary when the person closes it.  The current Scratch registry lives in the
selected Outline Markdown; the paired Run ticket and Result journal keep the
durable execution receipt in ``runs/`` and ``results/``.
"""
from __future__ import annotations

import datetime as dt
import html
import os
import re
import subprocess
import tempfile
from pathlib import Path

from src.outline_version import latest_outline


SCOPES = ("section", "subsection", "paragraph")
_RECORD_RE = re.compile(
    r"^###\s+(?P<run>rp-scratch-\d+_[A-Za-z0-9._-]+)\s+·\s+"
    r"(?P<scope>section|subsection|paragraph)\s+·\s+(?P<target>[A-Za-z0-9._-]+)\s*$",
    re.I | re.M,
)
_RUN_RE = re.compile(r"^rp-scratch-(?P<number>\d+)_", re.I)
_FIELD_RE = re.compile(r"^-\s+(?P<name>[A-Za-z][A-Za-z ]*):\s*(?P<value>.*)$")


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _clean(value: object, label: str, *, required: bool = True) -> str:
    if not isinstance(value, str):
        raise ValueError("%s must be text" % label)
    value = value.replace("\x00", "").strip()
    if required and not value:
        raise ValueError("%s is required" % label)
    if len(value) > 12000:
        raise ValueError("%s is too long" % label)
    return value


def ai_summarize_scratch(page_src: Path, scope: str, target: str, notes: str) -> str:
    """Ask the local Claude CLI for the close-summary; never write on failure."""
    prompt = (
        "Summarize one person's rough Scratch notes for a Page writing workflow.\n"
        f"Target: {scope} {target}\n\n"
        "Raw Scratch notes:\n---\n"
        f"{notes}\n"
        "---\n\n"
        "Return only one concise paragraph of 2–4 sentences. State the intended "
        "purpose and sequence of the target, preserve unresolved decisions, and "
        "do not invent facts. Do not use a heading, bullets, quotation marks, or "
        "a preamble."
    )
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    try:
        run = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text",
             "--model", "haiku", "--effort", "low",
             "--no-session-persistence", "--permission-prompt", "none",
             "--tools", ""],
            capture_output=True, text=True, timeout=120,
            cwd=page_src.parent, env=env,
        )
    except FileNotFoundError as exc:
        raise ValueError("AI summary unavailable: claude CLI not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise ValueError("AI summary timed out; Scratch remains open") from exc
    except OSError as exc:
        raise ValueError("AI summary unavailable: %s" % exc) from exc
    if run.returncode != 0:
        detail = (run.stderr or run.stdout or "unknown AI error").strip()
        raise ValueError("AI summary failed: %s" % detail[:300])
    summary = re.sub(r"^```(?:text|markdown)?\s*|\s*```$", "",
                     (run.stdout or "").strip(), flags=re.I)
    summary = _clean(" ".join(summary.split()), "AI summary")
    return summary


def _plan(page_src: Path) -> Path:
    plan = latest_outline(page_src.parent / "outline", page_src.stem)
    if plan is None:
        raise ValueError("This Page has no selected Outline Markdown")
    return plan


def _target_exists(page_src: Path, scope: str, target: str) -> bool:
    text = _plan(page_src).read_text(encoding="utf-8", errors="replace")
    sections = set(re.findall(r"^##\s+C(\d+)\b", text, re.M))
    subsections = set(re.findall(r"^###\s+(C\d+\.P\d+)\b", text, re.M))
    if scope == "section":
        return target.startswith("C") and target[1:] in sections
    if scope == "subsection":
        return target in subsections
    # Scratch is deliberately not a symbol/Bullet-level operation. A
    # paragraph is the whole C.P group; its B rows are reading material only.
    return target in subsections


def _scratch_section(text: str) -> tuple[int | None, int | None]:
    match = re.search(r"^##\s+Scratch\s*$", text, re.M)
    if not match:
        return None, None
    end_match = re.search(r"^##\s+", text[match.end():], re.M)
    end = match.end() + end_match.start() if end_match else len(text)
    return match.start(), end


def _record_spans(body: str) -> list[tuple[int, int, dict[str, str]]]:
    headers = list(_RECORD_RE.finditer(body))
    records = []
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(body)
        records.append((header.start(), end, {
            "run": header.group("run"),
            "scope": header.group("scope").lower(),
            "target": header.group("target"),
            "text": body[header.end():end].strip(),
        }))
    return records


def _block_value(body: str, label: str) -> str:
    """Read an indented multiline field written by ``_format_record``."""
    hit = re.search(
        rf"^-\s+{re.escape(label)}:[ \t]*\|?[ \t]*\n"
        rf"((?:^[ \t]{{2}}.*(?:\n|$))*)",
        body, re.M,
    )
    if not hit:
        return ""
    lines = hit.group(1).splitlines()
    return "\n".join(line[2:] if line.startswith("  ") else line for line in lines).strip()


def _field(body: str, label: str) -> str:
    hit = re.search(rf"^-\s+{re.escape(label)}:\s*(.*?)\s*$", body, re.M)
    return hit.group(1).strip() if hit else ""


def read_scratch(page_src: Path) -> dict:
    """Return all records plus the latest record for each target."""
    plan = _plan(page_src)
    text = plan.read_text(encoding="utf-8", errors="replace")
    start, end = _scratch_section(text)
    if start is None or end is None:
        return {"records": [], "latest": {}}
    body = text[start:end]
    records = []
    for _from, _to, raw in _record_spans(body):
        record = dict(raw)
        record["status"] = _field(raw["text"], "Status") or "open"
        record["started"] = _field(raw["text"], "Started")
        record["updated"] = _field(raw["text"], "Updated")
        record["notes"] = _block_value(raw["text"], "Notes")
        record["summary"] = _block_value(raw["text"], "Summary")
        records.append(record)
    latest = {}
    for record in records:
        latest[(record["scope"], record["target"])] = record
    return {"records": records, "latest": latest}


def _next_run_id(page_src: Path) -> str:
    inventory = read_scratch(page_src)
    numbers = [int(match.group("number")) for record in inventory["records"]
               if (match := _RUN_RE.match(record["run"]))]
    results = page_src.parent / "results"
    if results.is_dir():
        numbers.extend(int(match.group("number")) for path in results.iterdir()
                       if (match := _RUN_RE.match(path.name)))
    number = max(numbers, default=0) + 1
    return "rp-scratch-%02d" % number


def _target_suffix(target: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", target).strip("-") or "page"


def _run_id(base: str, target: str) -> str:
    return "%s_%s" % (base, _target_suffix(target))


def _format_block(record: dict) -> str:
    def indented(value: str) -> str:
        lines = value.splitlines() or [""]
        return "\n".join("  " + line for line in lines)

    return (
        "### {run} · {scope} · {target}\n"
        "- Scope: {scope}\n"
        "- Target: {target}\n"
        "- Status: {status}\n"
        "- Started: {started}\n"
        "- Updated: {updated}\n"
        "- Run: {run}\n"
        "- Notes: |\n{notes}\n"
        "- Summary: |\n{summary}\n"
    ).format(
        run=record["run"], scope=record["scope"], target=record["target"],
        status=record["status"], started=record["started"],
        updated=record["updated"], notes=indented(record["notes"]),
        summary=indented(record.get("summary", "")),
    )


def _update_plan(plan: Path, record: dict) -> None:
    text = plan.read_text(encoding="utf-8", errors="replace")
    start, end = _scratch_section(text)
    block = _format_block(record).rstrip() + "\n"
    if start is None or end is None:
        text = text.rstrip() + "\n\n## Scratch\n\n" + block
    else:
        section = text[start:end]
        spans = _record_spans(section)
        existing = next((pair for pair in spans if pair[2]["run"] == record["run"]), None)
        if existing:
            left, right, _old = existing
            section = section[:left] + block + section[right:]
        else:
            section = section.rstrip() + "\n\n" + block
        text = text[:start] + section + text[end:]
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent,
                                     prefix=plan.name + ".scratch-", delete=False) as tmp:
        tmp.write(text)
        temporary = Path(tmp.name)
    temporary.replace(plan)


def _write_run(page_src: Path, record: dict, *, closed: bool) -> dict:
    base = page_src.parent
    runs = base / "runs"
    result = base / "results" / record["run"]
    runs.mkdir(parents=True, exist_ok=True)
    result.mkdir(parents=True, exist_ok=True)
    status = "complete" if closed else "running"
    ticket = (
        "---\n"
        "family: page\n"
        "operation: interactive-writing\n"
        "interaction: human-scratch\n"
        "mode: scratch\n"
        "target_scope: {scope}\n"
        "target: {target}\n"
        "run: {run}\n"
        "ticket: runs/{run}.md\n"
        "result: results/{run}\n"
        "---\n\n"
        "# {run}\n\n"
        "- Purpose: capture the person's rough thinking for {scope} {target}.\n"
        "- Close rule: Finish asks the AI for a concise Summary.\n"
    ).format(**record)
    (runs / (record["run"] + ".md")).write_text(ticket, encoding="utf-8")
    version = "v001"
    version_file = result / (version + ".md")
    version_file.write_text(
        "Run: {run}\nVersion: {version}\nState: {state}\n\n"
        "## Step s001\n\n### Human scratch\n\n"
        "- Scope: {scope}\n- Target: {target}\n\n"
        "#### Raw scratch\n\n{notes}\n\n"
        "#### Summary\n\n{summary}\n\n"
        "## Version closure\n\n### Human close\n\n"
        "{closure}\n".format(
            run=record["run"], version=version,
            state="closed" if closed else "open", scope=record["scope"],
            target=record["target"], notes=record["notes"],
            summary=record.get("summary", "") or "Not closed yet.",
            closure=("AI generated the Scratch Summary and the person closed the Run."
                     if closed else "Waiting for the person to Finish Scratch."),
        ), encoding="utf-8",
    )
    (result / "working.md").write_text(
        "# {run} · Scratch\n\n"
        "- State: {state}.\n"
        "- Target: {scope} {target}.\n"
        "- Summary: {summary}\n".format(
            run=record["run"], state="complete" if closed else "open",
            scope=record["scope"], target=record["target"],
            summary=record.get("summary", "") or "pending",
        ), encoding="utf-8",
    )
    runtime = (
        "run: {run}\nfamily: page\noperation: interactive-writing\n"
        "interaction: human-scratch\nmode: scratch\n"
        "target_scope: {scope}\ntarget: {target}\n"
        "ticket: runs/{run}.md\nresult: results/{run}\n"
        "status: {status}\nversion: v001\nstep: s001\n"
        "version_file: results/{run}/v001.md\n"
        "summary: {summary}\n".format(
            run=record["run"], scope=record["scope"], target=record["target"],
            status=status, summary=record.get("summary", "") or "pending",
        )
    )
    (result / "runtime.yaml").write_text(runtime, encoding="utf-8")
    return {
        "run": record["run"], "scope": record["scope"],
        "target": record["target"], "status": record["status"],
        "summary": record.get("summary", ""), "version": version,
        "file": str(result.relative_to(base)),
    }


def save_scratch(page_src: Path, payload: dict, *, read_only: bool = False,
                 summarizer=None) -> tuple[dict | None, str | None]:
    """Save an open Scratch or close it after an AI-generated Summary."""
    if read_only:
        return None, "This Page is read-only"
    try:
        scope = _clean(payload.get("scope"), "scope").lower()
        if scope not in SCOPES:
            raise ValueError("scope must be section, subsection, or paragraph")
        target = _clean(payload.get("target"), "target")
        if not _target_exists(page_src, scope, target):
            raise ValueError("target does not exist in the selected Outline")
        notes = _clean(payload.get("notes"), "notes")
        phase = _clean(payload.get("phase", "save"), "phase").lower()
        if phase not in {"save", "finish"}:
            raise ValueError("phase must be save or finish")
        summary = ""
        if phase == "finish":
            make_summary = summarizer or ai_summarize_scratch
            summary = _clean(make_summary(page_src, scope, target, notes),
                             "AI summary")
            summary = " ".join(summary.split())
        inventory = read_scratch(page_src)
        key = (scope, target)
        requested_run = _clean(payload.get("run_id", ""), "run_id", required=False)
        current = inventory["latest"].get(key)
        if requested_run:
            if not re.fullmatch(r"rp-scratch-\d+_[A-Za-z0-9._-]+", requested_run, re.I):
                raise ValueError("invalid Scratch Run id")
            record = next((item for item in inventory["records"]
                           if item["run"] == requested_run), None)
            if record is None or record["scope"] != scope or record["target"] != target:
                raise ValueError("Scratch Run does not match this target")
            if record["status"].lower() == "closed":
                raise ValueError("closed Scratch Runs are immutable; start a new one")
        elif current and current["status"].lower() != "closed":
            record = current
        else:
            record = {"run": _run_id(_next_run_id(page_src), target),
                      "scope": scope, "target": target,
                      "started": _now()}
        record.update({"status": "closed" if phase == "finish" else "open",
                       "updated": _now(), "notes": notes, "summary": summary})
        plan = _plan(page_src)
        _update_plan(plan, record)
        result = _write_run(page_src, record, closed=phase == "finish")
        return result, None
    except (OSError, ValueError) as exc:
        return None, str(exc)


def _e(value: object) -> str:
    return html.escape(str(value), quote=True)


def _scratch_dom_id(scope: str, target: str) -> str:
    return "scratch-%s-%s" % (re.sub(r"[^A-Za-z0-9_-]+", "-", scope),
                               _target_suffix(target))


def scratch_heading_attr(scope: str, target: str, *, read_only: bool = False) -> str:
    """Return the target hook used by a Scratch-mode heading."""
    if read_only:
        return ""
    return ' data-scratch-heading="%s"' % _e(_scratch_dom_id(scope, target))


def scratch_flag_html(scope: str, target: str, record: dict | None = None,
                      *, read_only: bool = False) -> str:
    """Return the minimal heading mark for a target with saved Scratch notes."""
    if read_only or not record or not str(record.get("notes", "")).strip():
        return ""
    label = "Scratch available for %s %s" % (scope, target)
    return '<span class="scratch-flag" title="%s" aria-label="%s"></span>' % (
        _e(label), _e(label)
    )


def scratch_draft_trigger_html(scope: str, target: str, *, read_only: bool = False) -> str:
    """Return the compact heading action that reveals clean current prose."""
    if read_only:
        return ""
    slot_id = _scratch_dom_id(scope, target)
    preview_id = slot_id + "-draft"
    return (
        '<button type="button" class="scratch-draft-toggle" '
        'data-scratch-slot="%s" aria-controls="%s" aria-expanded="false" '
        'title="Show current draft without Bullet labels" '
        'aria-label="Show current draft">Show draft</button>'
    ) % (_e(slot_id), _e(preview_id))


def scratch_control_html(scope: str, target: str, record: dict | None = None,
                         *, read_only: bool = False, reading: bool = False,
                         path_q: str = "", file_q: str = "") -> str:
    """One Scratch box and a clean full-draft preview rendered below a heading.

    ``path`` and ``file`` stay in the form because POST /_board/outline needs
    the same Board target that produced this view.
    """
    if read_only:
        return ""
    record = record or {}
    closed = record.get("status", "").lower() == "closed"
    run_id = record.get("run", "") if not closed else ""
    notes = record.get("notes", "")
    editor_class = "scratch-editor open" if notes else "scratch-editor"
    locked = " readonly" if closed else ""
    mode_class = " reading-only" if reading else " table-only"
    preview_id = _scratch_dom_id(scope, target) + "-draft"
    draft_button = scratch_draft_trigger_html(scope, target)
    source_label = "Insert text"
    source_title = "Insert current %s text into Scratch" % scope
    if closed:
        actions = draft_button + '<span class="scratch-status">Closed</span>'
    else:
        actions = (
            draft_button
            + '<button type="button" data-scratch-source title="%s">%s</button>'
            '<button type="button" data-scratch-finish>Finish Scratch</button>'
            % (_e(source_title), _e(source_label))
        )
    return (
        '<div id="%s" class="scratch-slot%s" data-scratch-scope="%s" '
        'data-scratch-target="%s">'
        '<div class="%s">'
        '<form data-scratch-form data-scratch-autosave autocomplete="off">'
        '<input type="hidden" name="scope" value="%s">'
        '<input type="hidden" name="target" value="%s">'
        '<input type="hidden" name="path" value="%s">'
        '<input type="hidden" name="file" value="%s">'
        '<input type="hidden" name="run_id" value="%s">'
        '<textarea name="notes" aria-label="Scratch notes" rows="1" '
        'placeholder="What should this part do?"%s>%s</textarea>'
        '<div class="scratch-actions">%s'
        '<span class="scratch-status" role="status"></span></div>'
        '</form></div>'
        '<div id="%s" class="scratch-current-draft" '
        'data-scratch-draft-preview></div></div>'
    ) % (
        _e(_scratch_dom_id(scope, target)), mode_class, _e(scope), _e(target),
        editor_class, _e(scope), _e(target), _e(path_q), _e(file_q), _e(run_id),
        locked, _e(notes), actions, _e(preview_id),
    )


def scratch_assets_html(path_q: str = "", file_q: str = "") -> str:
    """CSS and the tiny same-origin controller emitted once per Draft.

    The Board write route resolves a Page from the ``path`` and ``file``
    fields before it can dispatch a Scratch action.  The form carries those
    route fields explicitly; the JavaScript fallback covers callers that
    render this asset without passing route arguments.
    """
    return r"""<style>
.scratch-slot{display:none;margin:6px 0 12px}
.scratch-flag{display:inline-block;width:6px;height:6px;margin:0 2px 1px 1px;border-radius:50%;background:var(--acc);vertical-align:middle}
.scratch-draft-toggle{appearance:none;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--mut);padding:3px 7px;cursor:pointer;font:600 11px/1 system-ui,sans-serif;vertical-align:middle;flex:none}
.scratch-draft-toggle:hover,.scratch-draft-toggle:focus-visible{border-color:var(--acc);color:var(--acc);outline:none}
.scratch-editor{display:none;position:static;width:auto;margin:7px 0 0;padding:0;border:0;border-radius:0;background:transparent;box-shadow:none;text-transform:none;letter-spacing:normal}
.scratch-editor.open{display:block}
.scratch-editor>summary{display:none}
.scratch-editor form{display:grid;gap:7px}
.scratch-editor textarea{resize:vertical;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:6px;text-transform:none;letter-spacing:normal}
.scratch-editor textarea[name="notes"]{height:1.45em;min-height:0;max-height:280px;overflow-y:hidden;box-sizing:border-box}
.scratch-editor textarea[readonly]{cursor:default;opacity:.8}
.scratch-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap}.scratch-actions button{border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg);padding:4px 7px;cursor:pointer;font:600 11px system-ui,sans-serif}.scratch-actions button[data-scratch-source]{border-color:transparent;color:var(--acc)}.scratch-actions button[data-scratch-finish]{border-color:var(--acc);color:var(--acc)}
.scratch-status{color:var(--mut);font:11px/1.4 system-ui,sans-serif}
.scratch-current-draft{display:none;margin:7px 0 0;padding:10px 12px;border-left:2px solid var(--acc);background:var(--card);color:var(--fg);font:16px/1.65 Georgia,serif;white-space:pre-wrap;user-select:text;cursor:text}
.scratch-current-draft.open{display:block}
.draft-lens[data-draft-mode="scratch"] .scratch-slot{display:block}.draft-lens[data-draft-mode="scratch"] .paragraph-bullets{display:none}.draft-lens[data-draft-mode="scratch"] .paragraph-reading{display:none}.draft-lens[data-draft-mode="scratch"] .paragraph-group{margin-bottom:24px}.draft-lens[data-draft-mode="scratch"] details.paragraph-group>summary{cursor:pointer}
.draft-lens[data-draft-mode="scratch"] details.paragraph-group.scratch-editor-open .paragraph-reading,.draft-lens[data-draft-mode="scratch"] details.paragraph-group.scratch-draft-open .paragraph-reading{display:none}
.draft-lens[data-draft-mode="scratch"] .reading-line{position:relative}.draft-lens[data-draft-mode="scratch"] .reading-copy{max-width:70ch}
.section-scratch{margin:0 0 6px}
.paragraph-scratch{margin:0}
.scratch-slot.reading-only{display:none}
.scratch-slot.table-only{display:none}
</style><script>
(function(){
  function closeEditors(except){document.querySelectorAll('.scratch-editor.open').forEach(function(x){if(x!==except){x.classList.remove('open');var slot=x.closest('.scratch-slot');if(slot)slot.classList.remove('scratch-editing');var owner=x.closest('details.paragraph-group');if(owner)owner.classList.remove('scratch-editor-open');}});}
  function closeDrafts(except){document.querySelectorAll('.scratch-current-draft.open').forEach(function(x){if(x!==except){x.classList.remove('open');var button=document.querySelector('.scratch-draft-toggle[aria-controls="'+x.id+'"]');if(button)button.setAttribute('aria-expanded','false');var owner=x.closest('details.paragraph-group');if(owner)owner.classList.remove('scratch-draft-open');}});}
  function slotFor(button){var id=button.getAttribute('aria-controls');return id?document.getElementById(id):null;}
  function openScratch(slot,owner){var editor=slot&&slot.querySelector('.scratch-editor');if(!editor)return;var wasOpen=editor.classList.contains('open');closeEditors(editor);closeDrafts(null);if(wasOpen){editor.classList.remove('open');if(slot)slot.classList.remove('scratch-editing');if(owner){owner.classList.remove('scratch-editor-open');owner.open=false;}return;}editor.classList.add('open');if(slot)slot.classList.add('scratch-editing');if(owner){owner.open=true;owner.classList.add('scratch-editor-open');}var note=editor.querySelector('[name=notes]');if(note)note.focus();}
  function readingText(node){return Array.from(node.querySelectorAll('.paragraph-reading .reading-copy')).map(function(x){return (x.innerText||x.textContent||'').trim();}).filter(Boolean).join('\n\n');}
  function sourceTextFor(slot){var group=slot.closest('.paragraph-group');if(group)return readingText(group);var section=slot.closest('.section-scratch'),out=[],node=section&&section.nextElementSibling;while(node&&!node.classList.contains('division-title')){if(node.matches&&node.matches('details.paragraph-group')){var text=readingText(node);if(text)out.push(text);}node=node.nextElementSibling;}return out.join('\n\n');}
  function resizeScratch(note){if(!note)return;note.style.height='auto';var cs=getComputedStyle(note),line=parseFloat(cs.lineHeight)||20,pad=(parseFloat(cs.paddingTop)||0)+(parseFloat(cs.paddingBottom)||0),min=line+pad+2,max=parseFloat(cs.maxHeight)||280,needed=Math.max(min,note.scrollHeight);note.style.height=Math.min(needed,max)+'px';note.style.overflowY=needed>max?'auto':'hidden';}
  var scratchSelectionPending=false;
  document.querySelectorAll('.scratch-editor textarea[name="notes"]').forEach(function(note){resizeScratch(note);note.addEventListener('input',function(){resizeScratch(note);});note.addEventListener('select',function(){if(note.selectionStart!==note.selectionEnd)scratchSelectionPending=true;});});
  var scratchPointerDown=false,scratchPointerMoved=false,scratchSuppressClick=false,scratchPointerField=null,scratchPointerX=0,scratchPointerY=0,scratchSuppressTimer=0;
  function scratchPointerStart(event){var field=event.target.closest&&event.target.closest('.scratch-editor textarea,.scratch-editor input');scratchPointerDown=!!field;scratchPointerField=field||null;scratchPointerMoved=false;scratchPointerX=event.clientX;scratchPointerY=event.clientY;}
  function scratchPointerMove(event){if(scratchPointerDown&&(Math.abs(event.clientX-scratchPointerX)>4||Math.abs(event.clientY-scratchPointerY)>4))scratchPointerMoved=true;}
  function scratchPointerEnd(event){var releasedOutside=!!scratchPointerField&&!(event.target.closest&&event.target.closest('.scratch-editor'));if(scratchPointerDown&&(scratchPointerMoved||releasedOutside)){scratchSuppressClick=true;clearTimeout(scratchSuppressTimer);scratchSuppressTimer=window.setTimeout(function(){scratchSuppressClick=false;},500);}scratchPointerDown=false;scratchPointerField=null;}
  ['mousedown','pointerdown'].forEach(function(type){document.addEventListener(type,scratchPointerStart);});
  ['mousemove','pointermove'].forEach(function(type){document.addEventListener(type,scratchPointerMove);});
  ['mouseup','pointerup'].forEach(function(type){document.addEventListener(type,scratchPointerEnd);});
  function scratchTextSelected(){var field=document.activeElement;return !!(field&&field.matches&&field.matches('.scratch-editor textarea,.scratch-editor input')&&typeof field.selectionStart==='number'&&field.selectionStart!==field.selectionEnd);}
  document.addEventListener('selectionchange',function(){if(scratchTextSelected())scratchSelectionPending=true;});
  document.addEventListener('click',function(event){var outsideEditor=!(event.target.closest&&event.target.closest('.scratch-editor'));var clickDuringScratchDrag=scratchPointerDown&&scratchPointerField&&outsideEditor;var clickAfterScratchSelection=(scratchTextSelected()||scratchSelectionPending)&&outsideEditor;if(scratchSuppressClick||clickDuringScratchDrag||clickAfterScratchSelection){scratchSuppressClick=false;scratchSelectionPending=false;clearTimeout(scratchSuppressTimer);event.preventDefault();event.stopImmediatePropagation();}},true);
  /* Scratch owns keyboard focus.  Keep editing shortcuts from reaching the
     surrounding <details>/<summary> controls, so cut/paste never changes the
     paragraph's open state.  The browser still performs the native shortcut
     inside the textarea (on macOS that is Command+X). */
  document.querySelectorAll('.scratch-editor').forEach(function(editor){
    editor.addEventListener('keydown',function(event){
      if(event.target.closest&&event.target.closest('textarea,input,button'))event.stopPropagation();
    });
  });
  document.querySelectorAll('[data-scratch-heading]').forEach(function(heading){function open(event){if(event.type==='keydown'&&event.key!=='Enter'&&event.key!==' ')return;if(event.type==='click'){if(scratchSuppressClick){scratchSuppressClick=false;event.preventDefault();event.stopPropagation();return;}var selection=window.getSelection&&window.getSelection();if(selection&&!selection.isCollapsed&&selection.containsNode&&selection.containsNode(heading,true)){event.preventDefault();event.stopPropagation();return;}}if(event.target.closest&&event.target.closest('.scratch-draft-toggle'))return;event.preventDefault();event.stopPropagation();var slot=document.getElementById(heading.getAttribute('data-scratch-heading'));openScratch(slot,heading.closest('details.paragraph-group'));}heading.addEventListener('click',open);heading.addEventListener('keydown',open);});
  document.querySelectorAll('.scratch-draft-toggle').forEach(function(button){button.addEventListener('click',function(event){event.preventDefault();event.stopPropagation();var slot=document.getElementById(button.getAttribute('data-scratch-slot')),preview=slot&&slot.querySelector('[data-scratch-draft-preview]'),editor=slot&&slot.querySelector('.scratch-editor'),owner=button.closest('details.paragraph-group');if(!preview)return;var opening=!preview.classList.contains('open');closeEditors(editor);if(opening){closeDrafts(null);if(editor)editor.classList.add('open');if(owner){owner.open=true;owner.classList.add('scratch-editor-open');owner.classList.add('scratch-draft-open');}preview.textContent=sourceTextFor(slot)||'No draft yet';preview.classList.add('open');button.setAttribute('aria-expanded','true');}else{preview.classList.remove('open');button.setAttribute('aria-expanded','false');if(owner)owner.classList.remove('scratch-draft-open');}});});
  document.querySelectorAll('[data-scratch-source]').forEach(function(button){button.addEventListener('click',function(){var form=button.closest('form'),slot=form.closest('.scratch-slot'),note=form.querySelector('[name=notes]'),status=form.querySelector('.scratch-status'),text=sourceTextFor(slot);if(!text){status.textContent='No text to insert';return;}var existing=note.value.trimEnd();note.value=existing?(existing+'\n\n'+text):text;note.dispatchEvent(new Event('input',{bubbles:true}));note.focus();status.textContent='Text inserted';});});
  function scratchPayload(form,phase){var payload={action:'scratch',phase:phase};new FormData(form).forEach(function(value,key){payload[key]=value;});var params=new URLSearchParams(location.search);if(!payload.path)payload.path=params.get('path')||'';if(!payload.file)payload.file=params.get('file')||'';return payload;}
  function requestScratch(form,phase){return fetch('/_board/outline',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(scratchPayload(form,phase))}).then(function(response){return response.json().then(function(result){if(!response.ok||!result.ok)throw new Error(result.err||'Unable to save Scratch');return result;});});}
  document.querySelectorAll('[data-scratch-form]').forEach(function(form){var note=form.querySelector('[name=notes]'),status=form.querySelector('.scratch-status'),runInput=form.querySelector('[name=run_id]'),finish=form.querySelector('[data-scratch-finish]');if(!note||note.readOnly)return;var timer=null,queued=false,inFlight=null,finishing=false;function schedule(delay){clearTimeout(timer);queued=true;timer=setTimeout(flush,delay);}function flush(){if(!queued||finishing||inFlight)return;queued=false;if(!note.value.trim()){status.textContent='';return;}var snapshot=note.value;status.textContent='Saving…';var request=requestScratch(form,'save');inFlight=request;request.then(function(result){if(result.run&&runInput)runInput.value=result.run;if(note.value===snapshot)status.textContent='Saved';if(note.value!==snapshot&&note.value.trim())schedule(650);},function(error){status.textContent=error.message;}).then(function(){if(inFlight===request)inFlight=null;if(queued&&!finishing)schedule(0);});}note.addEventListener('input',function(){status.textContent=note.value.trim()?'Unsaved':'';schedule(650);});note.addEventListener('blur',function(){if(note.value.trim())schedule(0);});if(finish)finish.addEventListener('click',async function(event){event.preventDefault();if(finishing)return;finishing=true;clearTimeout(timer);queued=false;status.textContent='Summarizing with AI…';try{if(inFlight)await inFlight;if(!note.value.trim())throw new Error('Notes are required');var result=await requestScratch(form,'finish');if(result.run&&runInput)runInput.value=result.run;status.textContent='Closed ✓';var slot=form.closest('.scratch-slot'),editor=form.closest('.scratch-editor'),owner=form.closest('details.paragraph-group');if(editor)editor.classList.remove('open');if(slot)slot.classList.remove('scratch-editing');if(owner){owner.classList.remove('scratch-editor-open');owner.open=false;}setTimeout(function(){location.reload();},180);}catch(error){finishing=false;status.textContent=error.message;}});});
  document.addEventListener('click',function(event){if(scratchSuppressClick){scratchSuppressClick=false;event.preventDefault();event.stopPropagation();return;}if(!event.target.closest('.scratch-slot,.scratch-draft-toggle,[data-scratch-heading]')){closeEditors(null);closeDrafts(null);}});
})();
</script>"""
