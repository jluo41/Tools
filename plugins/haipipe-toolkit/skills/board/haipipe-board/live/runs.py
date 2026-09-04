"""The ⚙️ Runs tab: real page-local Run → Result pairs, read-only.

Evidence owns why an item needs work. Its ``outline/evidence/supporting-runs/`` binding map may
cite external Supporting Runs and a planned local route. This presenter answers
the distinct question: which local work has actually been allocated here?
It walks only ``<page>/runs/`` and paired ``<page>/results/``.

``new-*`` is a plan, not a Run. Supporting Runs stay in Evidence lineage and
never become duplicate rows here. Nothing in this module executes or edits a
Run or Result.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.item_table import (compact_global_run, compact_paper_run, read_items,
                            readable_global_run, readable_paper_route, repo_root)


_TICKET_SUFFIXES = {".sh", ".ps1", ".py", ".do", ".r", ".R", ".yaml", ".yml", ".md"}
_TICKET_NAME = re.compile(
    r"(?:^r\d+|^run[-_]|^b\d+[._]j\d+[._]t\d+[._]r\d+|^p[._]?j\d+[._]t\d+[._]r\d+)",
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
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.route{font-weight:650}.state{font-weight:650;white-space:nowrap}
.state.ready{color:var(--acc)}.state.running{color:var(--warn)}.state.done{color:var(--ok)}.state.failed,.state.held{color:var(--bad)}
.repo-path{white-space:normal;overflow-wrap:anywhere;word-break:break-word;user-select:text}.detail[hidden]{display:none}
.detail td{padding:0 7px 10px;background:var(--card)}.detailbox{border-left:3px solid var(--acc);padding:7px 9px;margin:3px 0;font-size:12.5px}
.detailbox p{margin:3px 0}.detailbox b{display:inline-block;min-width:82px;color:var(--mut)}.refs{margin:5px 0 0;padding-left:18px}
.empty{max-width:620px;margin:30px auto;padding:14px 16px;border:1px solid var(--line);border-radius:8px;color:var(--mut)}
"""


def _fields(runtime: Path | None) -> dict[str, str]:
    """Read portable receipt keys without declaring a new receipt dialect."""
    if runtime is None or not runtime.is_file():
        return {}
    text = runtime.read_text(encoding="utf-8", errors="replace")

    def field(name: str) -> str:
        hit = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", text, re.M)
        return hit.group(1).strip().strip('"') if hit else ""

    return {name: field(name) for name in ("global_id", "status", "target", "result", "ticket")}


def _status(runtime: Path | None, fields: dict[str, str]) -> str:
    if runtime is None:
        return "Ready"
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
    """Read allocated page-local Tickets and their paired local Results only."""
    page_dir = page_src.parent
    runs_dir, results_dir = page_dir / "runs", page_dir / "results"
    rows = []
    for ticket in _ticket_files(runs_dir):
        runtime = _runtime_for(ticket, runs_dir, results_dir)
        fields = _fields(runtime)
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
            "result": fields.get("result", "") or (str(runtime.parent.relative_to(page_dir)) if runtime else ""),
            "target": fields.get("target", "") or "page-local work",
            "status": _status(runtime, fields),
            "refs": _evidence_refs(
                page_src,
                run_id=global_id,
                ticket=ticket,
            ),
        })
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
        return path.name


def _detail(row: dict, root: Path) -> str:
    fields = [
        ("Run", _linked(row["ticket"], label=_shown_path(row["ticket"], root), root=root)),
        ("Result", _linked(row["runtime"], label=_shown_path(row["runtime"], root), root=root)),
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
    return "<div class=detailbox>%s</div>" % "".join(chunks)


def render(page_src: Path, _path_q: str, _file_q: str) -> str:
    rows = local_runs(page_src)
    counts = {state: sum(row["status"] == state for row in rows)
              for state in ("Ready", "Running", "Done", "Failed", "Held")}
    root = repo_root(page_src.parent)
    if rows:
        table_rows = []
        for index, row in enumerate(rows):
            run_label = str(row["ticket"].relative_to(page_src.parent))
            result_label = (str(row["runtime"].relative_to(page_src.parent))
                            if row["runtime"] else "—")
            state = row["status"].lower()
            table_rows.append(
                '<tr class="run" data-i="%d" tabindex="0"><td><code class=route>%s</code></td>'
                '<td>%s</td><td>%s</td><td><span class="state %s">%s</span></td></tr>'
                '<tr class="detail" data-i="%d" hidden><td colspan=4>%s</td></tr>' % (
                    index, html.escape(row["run_id"]),
                    _linked(row["ticket"], label=run_label, root=root),
                    _linked(row["runtime"], label=result_label, root=root),
                    html.escape(state), html.escape(row["status"]), index, _detail(row, root)))
        main = ("<div class=summary><b>%d local runs</b><span>Ready %d</span><span>Running %d</span>"
                "<span>Done %d</span><span>Failed %d</span><span>Held %d</span></div>"
                "<div class=wrap><p class=note>Click a row for the exact Run and Result paths and any Evidence Item binding. "
                "Supporting Runs and unallocated plans stay in 🧾 Evidence Items.</p>"
                "<table><thead><tr><th>Run</th><th>Run path</th><th>Result path</th><th>Status</th></tr></thead>"
                "<tbody id=rows>%s</tbody></table></div>" %
                (len(rows), counts["Ready"], counts["Running"], counts["Done"], counts["Failed"], counts["Held"], "".join(table_rows)))
    else:
        main = ("<div class=empty><b>No local Run allocated.</b><br>"
                "This page has no real Run in <code>runs/</code> yet. Supporting Runs, rerun findings, and <code>new-*</code> plans are Evidence lineage—not local Runs. "
                "Allocate a Run only when you are ready to execute it; its paired Result belongs under <code>results/</code>.</div>")
    return f"""<!doctype html><meta charset=utf-8>
<title>⚙️ Runs · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<header><h1>⚙️ Runs · {html.escape(page_src.stem)}</h1>
<p class=lead>allocated page-local Run → Result pairs · read-only</p></header>{main}
<script>
(function () {{ var rows=document.getElementById('rows'); if(!rows)return;
 function toggle(i){{var d=rows.querySelector('tr.detail[data-i="'+i+'"]');if(d)d.hidden=!d.hidden;}}
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
