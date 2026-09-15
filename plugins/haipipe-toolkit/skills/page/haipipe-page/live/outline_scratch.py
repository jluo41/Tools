"""Human-first Scratch Runs for Draft Space.

Scratch is deliberately smaller than writing or feedback.  It records a
person's rough plan for one Page target, then closes only after that person
confirms a short summary.  The current Scratch registry lives in the selected
Outline Markdown; the paired Run ticket and Result journal keep the durable
execution receipt in ``runs/`` and ``results/``.
"""
from __future__ import annotations

import datetime as dt
import html
import re
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
        rf"^-\s+{re.escape(label)}:\s*\|?\s*$\n"
        rf"((?:^[ \t]{2}.*(?:\n|$))*)",
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
        "- Close rule: the person confirms a Summary.\n"
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
            closure=("Human confirmed the Scratch Summary."
                     if closed else "Waiting for the person to confirm a Summary."),
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


def save_scratch(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """Save an open Scratch or close it after Summary confirmation."""
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
        summary = _clean(payload.get("summary", ""), "summary", required=False)
        if phase == "finish" and not summary:
            raise ValueError("summary is required before closing Scratch")
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


def scratch_control_html(scope: str, target: str, record: dict | None = None,
                         *, read_only: bool = False, reading: bool = False) -> str:
    """Compact control rendered beside a section, subsection, or paragraph."""
    if read_only:
        return ""
    record = record or {}
    closed = record.get("status", "").lower() == "closed"
    run_id = record.get("run", "") if not closed else ""
    notes = record.get("notes", "") if not closed else ""
    summary = record.get("summary", "") if not closed else ""
    mode_class = " reading-only" if reading else " table-only"
    return (
        '<div class="scratch-slot%s" data-scratch-scope="%s" '
        'data-scratch-target="%s">'
        '<button type="button" class="scratch-plus" title="Add Scratch" '
        'aria-label="Add %s Scratch">+</button>'
        '%s%s'
        '<div class="scratch-editor">'
        '<form data-scratch-form autocomplete="off">'
        '<input type="hidden" name="scope" value="%s">'
        '<input type="hidden" name="target" value="%s">'
        '<input type="hidden" name="run_id" value="%s">'
        '<label>Scratch<textarea name="notes" rows="3" placeholder="What should this part do?">%s</textarea></label>'
        '<label>Summary<textarea name="summary" rows="2" placeholder="Summarize when you are done">%s</textarea></label>'
        '<div class="scratch-actions"><button type="button" data-scratch-save>Save</button>'
        '<button type="button" data-scratch-finish>Finish Scratch</button>'
        '<span class="scratch-status" role="status"></span></div>'
        '</form></div></div>'
    ) % (
        mode_class, _e(scope), _e(target), _e(scope),
        '<span class="scratch-done" title="Scratch closed">Scratch ✓</span>' if closed else "",
        ('<span class="scratch-closed-summary">%s</span>' % _e(record.get("summary", ""))
         if closed and record.get("summary") else ""),
        _e(scope), _e(target), _e(run_id), _e(notes), _e(summary),
    )


def scratch_assets_html() -> str:
    """CSS and the tiny same-origin controller emitted once per Draft."""
    return r"""<style>
.scratch-slot{display:none;align-items:baseline;gap:4px;margin-left:7px;vertical-align:baseline}
.scratch-plus{appearance:none;border:0;background:none;color:var(--acc);font:600 16px/1 system-ui,sans-serif;padding:0 3px;cursor:pointer;opacity:.72}
.scratch-plus:hover,.scratch-plus:focus-visible{opacity:1;outline:1px solid var(--acc);border-radius:3px}
.scratch-editor{display:none;position:absolute;z-index:3;width:min(360px,calc(100vw - 34px));margin:5px 0 0;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);box-shadow:0 8px 24px rgba(0,0,0,.12);text-transform:none;letter-spacing:normal}
.scratch-editor.open{display:block}
.scratch-editor>summary{display:none}
.scratch-editor form{display:grid;gap:7px}
.scratch-editor label{display:grid;gap:3px;color:var(--mut);font:600 11px/1.4 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.04em}
.scratch-editor textarea{resize:vertical;min-height:42px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:6px;text-transform:none;letter-spacing:normal}
.scratch-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap}.scratch-actions button{border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg);padding:4px 7px;cursor:pointer;font:600 11px system-ui,sans-serif}.scratch-actions button[data-scratch-finish]{border-color:var(--acc);color:var(--acc)}
.scratch-status{color:var(--mut);font:11px/1.4 system-ui,sans-serif}.scratch-done{display:none;color:var(--ok);font:600 11px/1.4 system-ui,sans-serif}.scratch-closed-summary{display:none;color:var(--mut);font:12px/1.45 system-ui,sans-serif;font-weight:400}
.draft-lens[data-draft-mode="scratch"] .scratch-slot{display:inline-flex}.draft-lens[data-draft-mode="scratch"] .scratch-slot.table-only{display:inline-flex}.draft-lens[data-draft-mode="scratch"] .scratch-slot.reading-only{display:inline-flex}.draft-lens[data-draft-mode="scratch"] .scratch-done,.draft-lens[data-draft-mode="scratch"] .scratch-closed-summary{display:inline}
.draft-lens[data-draft-mode="scratch"] .paragraph-bullets{display:none}.draft-lens[data-draft-mode="scratch"] .paragraph-reading{display:block}.draft-lens[data-draft-mode="scratch"] .paragraph-group{margin-bottom:24px}.draft-lens[data-draft-mode="scratch"] details.paragraph-group>summary{cursor:pointer}
.draft-lens[data-draft-mode="scratch"] .reading-line{position:relative}.draft-lens[data-draft-mode="scratch"] .reading-copy{max-width:70ch}
.draft-lens[data-draft-mode="scratch"] .scratch-slot.reading-only{margin-left:3px}
.scratch-slot.reading-only{display:none}
.scratch-slot.table-only{display:none}
.scratch-slot .scratch-editor textarea[name="summary"]{min-height:34px}
</style><script>
(function(){
  function closeEditors(except){document.querySelectorAll('.scratch-editor.open').forEach(function(x){if(x!==except)x.classList.remove('open');});}
  document.querySelectorAll('.scratch-plus').forEach(function(button){button.addEventListener('click',function(event){event.preventDefault();event.stopPropagation();var slot=button.closest('.scratch-slot'),editor=slot&&slot.querySelector('.scratch-editor');if(!editor)return;var was=editor.classList.contains('open');closeEditors(editor);editor.classList.toggle('open',!was);if(!was){var note=editor.querySelector('[name=notes]');if(note)note.focus();}});});
  document.querySelectorAll('[data-scratch-save],[data-scratch-finish]').forEach(function(button){button.addEventListener('click',async function(){var form=button.closest('form'),slot=form.closest('.scratch-slot'),status=form.querySelector('.scratch-status'),finish=button.hasAttribute('data-scratch-finish');var payload={action:'scratch',phase:finish?'finish':'save'};new FormData(form).forEach(function(value,key){payload[key]=value;});status.textContent='Saving…';try{var response=await fetch('/_board/outline',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}),result=await response.json();if(!response.ok||!result.ok)throw new Error(result.err||'Unable to save Scratch');status.textContent=finish?'Closed ✓':'Saved';if(result.run&&!payload.run_id){form.querySelector('[name=run_id]').value=result.run;}if(finish){slot.querySelector('.scratch-editor').classList.remove('open');setTimeout(function(){location.reload();},180);}}catch(error){status.textContent=error.message;}});});
  document.addEventListener('click',function(event){if(!event.target.closest('.scratch-slot'))closeEditors(null);});
})();
</script>"""
