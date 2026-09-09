"""The ⚙️ Runs tab: real Folder-owned Run → Result pairs, read-only.

Evidence owns why an item needs work. Its ``outline/evidence/supporting-runs/`` binding map may
cite external Supporting Runs and a planned local route. This presenter answers
the distinct question: which local work has actually been allocated here?
It resolves Folder-local pairs and canonical Task pairs whose Result lives in
the containing Job.

``new-*`` is a plan, not a Run. Supporting Runs stay in Evidence lineage and
never become duplicate rows here. Nothing in this module executes or edits a
Run or Result.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from src.item_table import (compact_global_run, compact_paper_run, read_items,
                            readable_global_run, readable_paper_route, repo_root)
from src.dialect_task_block import page_info as task_page_info


_TICKET_SUFFIXES = {".sh", ".ps1", ".py", ".do", ".r", ".R", ".yaml", ".yml", ".md"}
_TICKET_NAME = re.compile(
    r"(?:^r\d+|^run[-_]|^b\d+[._]j\d+[._]t\d+[._]r\d+|^p[._]?j\d+[._]?t\d+[._]?r\d+)",
    re.I,
)
_STATE_ORDER = {"Running": 0, "Failed": 1, "Held": 2, "Ready": 3, "Done": 4}


_CSS = """
:root{--bg:#fff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;
 --acc:#3b6ea5;--ok:#287443;--warn:#a95b12;--bad:#b13c3c}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--ok:#74b68a;--warn:#e0a05c;--bad:#e77b7b}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 -apple-system,
 BlinkMacSystemFont,'Segoe UI',sans-serif}header{padding:10px 16px 7px}h1{font-size:16px;margin:0}
.mut{color:var(--mut);font-size:12.5px}.lead{margin:3px 0 0}.summary{display:flex;gap:8px;
 padding:7px 16px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:12.5px}
.wrap{padding:0 16px 16px;overflow:auto}.note{margin:9px 0;font-size:12.5px;color:var(--mut)}
table{width:100%;border-collapse:collapse;font-size:12.5px}th,td{text-align:left;vertical-align:top;
 border-bottom:1px solid var(--line);padding:8px 6px}th{font-size:11px;color:var(--mut);
 text-transform:uppercase;letter-spacing:.035em}tr.run{cursor:pointer}tr.run:hover td{background:var(--card)}
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.route{font-weight:650;overflow-wrap:anywhere}.state{font-weight:650;white-space:nowrap}
.state.ready{color:var(--acc)}.state.running{color:var(--warn)}.state.done{color:var(--ok)}.state.failed,.state.held{color:var(--bad)}
.repo-path{white-space:normal;overflow-wrap:anywhere;word-break:break-word;user-select:text}.detail[hidden]{display:none}
.detail td{padding:0 7px 10px;background:var(--card)}.detailbox{border-left:3px solid var(--acc);padding:7px 9px;margin:3px 0;font-size:12.5px}
.detailbox p{margin:3px 0}.detailbox b{display:inline-block;min-width:82px;color:var(--mut)}.refs{margin:5px 0 0;padding-left:18px}
.empty{max-width:620px;margin:30px auto;padding:14px 16px;border:1px solid var(--line);border-radius:8px;color:var(--mut)}
.run-preview{white-space:pre-wrap;overflow-wrap:anywhere;font-family:inherit;font-size:13px;line-height:1.6;margin:8px 0}
.detailbox h2{font-size:14px;margin:14px 0 5px}.summary{flex-wrap:wrap}
"""


def _fields(runtime: Path | None) -> dict[str, str]:
    """Read portable receipt keys without declaring a new receipt dialect."""
    if runtime is None or not runtime.is_file():
        return {}
    text = runtime.read_text(encoding="utf-8", errors="replace")
    if runtime.suffix == ".md":
        front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        text = front.group(1) if front else ""

    def field(name: str) -> str:
        hit = re.search(rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", text, re.M)
        return hit.group(1).strip().strip("\"'") if hit else ""

    return {name: field(name) for name in
            ("global_id", "status", "target", "result", "ticket", "family", "operation")}


def _preview_text(path: Path, boundary: Path) -> str:
    """Bounded plain-text preview of an owned file, never a referenced external path."""
    try:
        if not path.resolve().is_relative_to(boundary.resolve()) or not path.is_file():
            return ""
        with path.open("rb") as stream:
            data = stream.read(65537)
        text = data[:65536].decode("utf-8", errors="replace")
        return text + ("\n[Preview truncated at 64 KiB]" if len(data) > 65536 else "")
    except OSError:
        return ""


def _status(runtime: Path | None, fields: dict[str, str]) -> str:
    if runtime is None:
        return "Held" if fields.get("operation") == "paragraph-writing" else "Ready"
    status = fields.get("status", "").lower()
    if status in {"planned", "ticket", "queued"}:
        return "Ready"
    if status in {"running", "started"}:
        return "Running"
    if status in {"failed", "error"}:
        return "Failed"
    if status in {"blocked", "held", "rerun", "incomplete"}:
        return "Held"
    if status in {"complete", "completed", "done"}:
        if fields.get("operation") == "paragraph-writing":
            # Structural availability only; the writer owns semantic acceptance.
            return "Done" if all(_preview_text(runtime.parent / name, runtime.parent).strip()
                                 for name in ("paragraph.md", "trace.md")) else "Held"
        has_output = any(child.is_file() and child.name not in {"runtime.yaml", "receipt.yaml"}
                         for child in runtime.parent.iterdir())
        return "Done" if has_output else "Held"
    return "Held"


def _ticket_files(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return [path for path in sorted(runs_dir.rglob("*"))
            if path.is_file() and path.suffix in _TICKET_SUFFIXES
            and _TICKET_NAME.match(path.name) and not path.name.startswith(".")]


def _runtime_for(ticket: Path, runs_dir: Path, results_dir: Path) -> Path | None:
    """Pair by logical ticket address, then accept a receipt naming that ticket."""
    relative = ticket.relative_to(runs_dir).with_suffix("")
    candidates = (
        results_dir / relative / "runtime.yaml",
        results_dir / ticket.stem / "runtime.yaml",
        results_dir / (str(relative) + ".yaml"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    rel_text = str(ticket.relative_to(runs_dir))
    for candidate in sorted(results_dir.rglob("runtime.yaml")) if results_dir.is_dir() else []:
        fields = _fields(candidate)
        if fields.get("ticket") in {rel_text, ticket.name, str(ticket)}:
            return candidate
    return None


def _task_context(page_src: Path):
    """Return the Task adapter record and containing Job for a Task Page."""
    if len(page_src.parents) < 3:
        return None, None
    block = page_src.parents[2]
    info = task_page_info(block, page_src)
    return (info, page_src.parents[1]) if info else (None, None)


def _fallback_result(runtime: Path | None, base: Path) -> str:
    if runtime is None:
        return ""
    try:
        return str(runtime.parent.relative_to(base))
    except ValueError:
        return str(runtime.parent)


def _evidence_refs(page_src: Path, *, run_id: str, ticket: Path) -> list[str]:
    """Return Evidence Items only when their ledger has named this local run."""
    compact = compact_paper_run(run_id) or compact_global_run(run_id)
    needles = {run_id, ticket.name, str(ticket.relative_to(page_src.parent))}
    if compact:
        needles.update({compact, readable_paper_route(compact), readable_global_run(compact)})
    refs = []
    for item in read_items(page_src).values():
        declared = " ".join((item.get("local_run", ""), item.get("result", "")))
        if any(needle and needle in declared for needle in needles):
            refs.append(item["item"])
    return refs


def local_runs(page_src: Path) -> list[dict]:
    """Read allocated Folder-local or Job-backed Task Run pairs."""
    page_dir = page_src.parent
    instance_rows = (_insight_runs(page_src) if (page_dir / "workflow/insight.yaml").is_file() else [])
    item_tickets = {row["ticket"] for row in instance_rows}
    task_info, job_dir = _task_context(page_src)
    runs_dir = page_dir / "runs"
    if task_info:
        results_dir = job_dir / "results" / page_dir.name
        result_base = job_dir
    else:
        results_dir = page_dir / "results"
        result_base = page_dir
    rows = list(instance_rows)
    for ticket in _ticket_files(runs_dir):
        if ticket in item_tickets:
            continue
        runtime = _runtime_for(ticket, runs_dir, results_dir)
        fields = _fields(runtime)
        ticket_fields = _fields(ticket) if ticket.suffix == ".md" else {}
        for key in ("target", "family", "operation"):
            fields[key] = fields.get(key) or ticket_fields.get(key, "")
        if not fields.get("operation") and re.fullmatch(r"r\d+_page-writing_c\d+-p\d+", ticket.stem):
            fields["operation"] = "paragraph-writing"
        kind = ("Page · Paragraph Writing" if fields.get("operation") == "paragraph-writing"
                else fields.get("operation") or fields.get("family") or "Local Run")
        if task_info:
            compact = (compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            local_run = re.match(r"^(r\d{2})(?:_|$)", ticket.stem, re.I)
            if not compact and local_run:
                compact = f"{task_info['id']}{local_run.group(1).lower()}"
            global_id = readable_global_run(compact) if compact else ticket.stem
            run_id = global_id
        elif (fields.get("family") == "design" or
              re.fullmatch(r"r[0-9]{2,}_design_(?:generate|verify)_[a-z0-9][a-z0-9_-]*",
                           ticket.stem)):
            # Design uses its stable Folder address, never a fabricated Paper
            # or b/j/t identity. Its YAML Ticket is already a supported suffix.
            compact = ""
            global_id = fields.get("global_id") or f"{page_dir.as_posix()}#{ticket.stem}"
            run_id = ticket.stem
        else:
            paper_id = (compact_paper_run(fields.get("global_id", ""))
                        or compact_paper_run(ticket.stem))
            compact = (paper_id or compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            # The Paper Board is the local block. This view omits an inherited
            # ``bNN`` prefix, while ledger and receipt retain it for global lookup.
            global_id = (paper_id or readable_global_run(compact)) if compact else ticket.stem
            relative_id = readable_paper_route(compact) if compact else ""
            run_id = "P " + (relative_id or ticket.stem)
        rows.append({
            "run_id": run_id,
            "global_id": global_id,
            "compact_id": compact,
            "ticket": ticket,
            "runtime": runtime,
            "result": fields.get("result", "") or _fallback_result(runtime, result_base),
            "target": fields.get("target", "") or "page-local work",
            "kind": kind,
            "operation": fields.get("operation", ""),
            "status": _status(runtime, fields),
            "refs": _evidence_refs(
                page_src,
                run_id=global_id,
                ticket=ticket,
            ),
        })
    return sorted(rows, key=lambda row: (_STATE_ORDER.get(row["status"], 9), row["run_id"]))


def _insight_runs(page_src: Path) -> list[dict]:
    """The instance dialect has one ticket and several explicit executions."""
    from src.insight_instances import contract
    api = contract()
    try:
        manifest, items, errors = api.inspect(page_src.parent)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, api.yaml.YAMLError):
        return []  # the Outline item table displays the validation failure
    rows = []
    for item in items:
        if not item["ticket"]:
            continue  # proposed items are not allocated Runs
        run = item["item"]["run"]
        ticket = page_src.parent / "runs" / f"{run}.sh"
        for info in item["versions"] or [None]:
            ident = info["execution"] if info else f"{manifest['instance']}#{run}"
            directory = page_src.parent / "results" / run / info["version"] if info else None
            status = "Ready"
            if info:
                status = {"planned": "Ready", "running": "Running", "complete": "Done",
                          "failed": "Failed", "blocked": "Held"}.get(info["status"], "Held")
                if not info["valid"] or info["stale"]:
                    status = "Held"
            rows.append({"run_id": ident, "global_id": ident, "compact_id": ident if info else "",
                         "ticket": ticket, "runtime": directory / "runtime.yaml" if directory else None,
                         "result": str(directory / "result.yaml") if directory and (directory / "result.yaml").is_file() else "",
                         "target": item["item"].get("question", ""), "status": status,
                         "refs": _evidence_refs(page_src, run_id=ident, ticket=ticket)})
    return sorted(rows, key=lambda row: (_STATE_ORDER.get(row["status"], 9), row["run_id"]))


def _linked(path: Path | None, *, label: str, root: Path) -> str:
    """Show an exact selectable path without opening or downloading it."""
    if path is None:
        return "—"
    return '<code class=repo-path>%s</code>' % html.escape(label)


def _shown_path(path: Path | None, root: Path) -> str:
    if path is None:
        return "—"
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def _detail(row: dict, root: Path) -> str:
    fields = [
        ("Run", html.escape(row["run_id"])),
        ("Run path", _linked(row["ticket"], label=_shown_path(row["ticket"], root), root=root)),
        ("Result path", _linked(row["runtime"], label=_shown_path(row["runtime"], root), root=root)),
        ("Output", html.escape(row["result"] or "not written yet")),
        ("Target", html.escape(row["target"])),
    ]
    chunks = ["<p><b>%s</b><span>%s</span></p>" % (label, value) for label, value in fields]
    if row["refs"]:
        chunks.append("<p><b>Evidence</b></p><ul class=refs>%s</ul>" % "".join(
            "<li><code>%s</code></li>" % html.escape(ref) for ref in row["refs"]
        ))
    else:
        chunks.append("<p><b>Evidence</b><span>no item binding recorded</span></p>")
    if row.get("operation") == "paragraph-writing":
        if row["runtime"] is None:
            chunks.append("<p class=note>Missing runtime.yaml: this writing Run has no lifecycle receipt.</p>")
        previews = [("Writing instructions / Prompt", row["ticket"], row["ticket"].parent)]
        if row["runtime"]:
            directory = row["runtime"].parent
            previews.extend((label, directory / name, directory) for label, name in
                            (("Paragraph", "paragraph.md"), ("Trace / Review", "trace.md")))
        for label, path, boundary in previews:
            text = _preview_text(path, boundary)
            chunks.append("<h2>%s</h2><pre class=run-preview>%s</pre>" %
                          (label, html.escape(text or "Not available yet.")))
    return "<div class=detailbox>%s</div>" % "".join(chunks)


def render(page_src: Path, _path_q: str, _file_q: str) -> str:
    rows = local_runs(page_src)
    counts = {state: sum(row["status"] == state for row in rows)
              for state in ("Ready", "Running", "Done", "Failed", "Held")}
    root = repo_root(page_src.parent)
    if rows:
        table_rows = []
        for index, row in enumerate(rows):
            state = row["status"].lower()
            label = row["run_id"]
            if row.get("operation") == "paragraph-writing":
                local_id = re.match(r"r\d+(?=_)", row["ticket"].stem)
                if local_id:
                    label = local_id.group(0)  # Page-scoped overview; full id in detail.
            output = ("paragraph" if row.get("operation") == "paragraph-writing" and row["status"] == "Done"
                      else "inspect" if row["runtime"] else "—")
            table_rows.append(
                '<tr class="run" data-i="%d" tabindex="0" aria-expanded="false"><td><code class=route>%s</code></td>'
                '<td>%s</td><td>%s</td><td><span class="state %s">%s</span></td><td>%s</td></tr>'
                '<tr class="detail" data-i="%d" hidden><td colspan=5>%s</td></tr>' % (
                    index, html.escape(label),
                    html.escape(row.get("kind", "Local Run")), html.escape(row["target"]),
                    html.escape(state), html.escape(row["status"]), output, index, _detail(row, root)))
        main = ("<div class=summary><b>%d local runs</b><span>Ready %d</span><span>Running %d</span>"
                "<span>Done %d</span><span>Failed %d</span><span>Held %d</span></div>"
                "<div class=wrap><p class=note>Click a row for Run details; paragraph writing also shows its prompt, prose, and review. "
                "Supporting Runs and unallocated plans stay in 🧾 Evidence Items.</p>"
                "<table><thead><tr><th>Run</th><th>Kind</th><th>Target</th><th>Status</th><th>Result</th></tr></thead>"
                "<tbody id=rows>%s</tbody></table></div>" %
                (len(rows), counts["Ready"], counts["Running"], counts["Done"], counts["Failed"], counts["Held"], "".join(table_rows)))
    else:
        main = ("<div class=empty><b>No local Run allocated.</b><br>"
                "This page has no real Run in <code>runs/</code> yet. Supporting Runs, rerun findings, and <code>new-*</code> plans are Evidence lineage—not local Runs. "
                "Allocate a Run only when you are ready to execute it; its paired Result belongs at the Folder dialect's resolved Result address.</div>")
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1">
<title>⚙️ Runs · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<header><h1>⚙️ Runs · {html.escape(page_src.stem)}</h1>
<p class=lead>allocated Folder-owned Run → Result pairs · read-only</p></header>{main}
<script>
(function () {{ var rows=document.getElementById('rows'); if(!rows)return;
 function toggle(i){{var d=rows.querySelector('tr.detail[data-i="'+i+'"]');var r=rows.querySelector('tr.run[data-i="'+i+'"]');if(d){{d.hidden=!d.hidden;if(r)r.setAttribute('aria-expanded',String(!d.hidden));}}}}
 rows.addEventListener('click',function(e){{var r=e.target.closest('tr.run');if(r)toggle(r.dataset.i);}});
 rows.addEventListener('keydown',function(e){{var r=e.target.closest('tr.run');if(r&&(e.key==='Enter'||e.key===' ')){{e.preventDefault();toggle(r.dataset.i);}}}}); }})();
</script>"""


class RunsTabMixin:
    """Read-only page-local Runs view plus the shell's no-write POST twin."""

    def runs_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        path_q = (query.get("path") or [""])[0]
        file_q = (query.get("file") or [""])[0]
        page_src, error = self.target({"path": path_q, "file": file_q})
        if page_src is None:
            return self.reply(400, {"ok": False, "err": error})
        body = render(page_src, path_q, file_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_runs(self, payload):
        page_src, error = self.target(payload)
        if page_src is None:
            return None, error
        return {"url": "/_board/runs?path=%s&file=%s" %
                (quote(payload.get("path") or ""), quote(payload.get("file") or ""))}, None
