"""🪜 Page workflow passes · one Page's Run receipts, served as JSON.

WHAT THIS ANSWERS: the 📄 Page Runs stepper (65-workbench-pageflow.js) has to
say where ONE Page stands in its Run list (context · structure · evidence ·
writing · check). That truth is not in
the rendered page: the run contract (haipipe-page-workflow) writes it to
`<board>/_runs/page/<page-id>/<run-id>.json`, one legacy-named receipt trail
per workflow pass. So
the stepper asks this route, and this route reads those files and nothing
else — the same one-source rule that keeps the labeling stepper honest about
`## States`.

WHY LIVE AND NOT A WRITTEN VIEW: a run lands whenever an orchestrator
finishes, with no rebuild in between. A stored view would show the previous
run until someone rebuilt the board, which reads as "the run never happened".

NO RECEIPTS IS AN ANSWER, NOT AN ERROR: most Pages have no workflow pass. The
route returns an empty list and the surface states the contract's own entry
rule (an existing Page starts at check, a new one at context).

Matching is by the receipt's OWN `page` field, basename against basename,
never by directory name: the `<page-id>` folder is a filing convention the
orchestrator owns, and a convention is not evidence.
"""
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# keep payloads small: the strip needs the trail's shape, not its artifacts
TRAIL_KEYS = ("step", "round", "run", "route", "verdict", "status")
# Receipts written before 2026-09-22 say `phase` with uppercase tokens; read them
# through the one legacy map in src/page_progress.py.
try:
    from src.page_progress import run_of as _run_of
except ImportError:  # pragma: no cover
    def _run_of(token):
        return str(token or "").lower()
MAX_RUNS = 20


def _route(value) -> str:
    """A route is a Run key, CLOSE, or HOLD; legacy uppercase Run words map like receipts."""
    raw = str(value or "").strip()
    return raw.upper() if raw.upper() in {"CLOSE", "HOLD"} else _run_of(raw)


def page_runs(board: Path, page_file: str):
    """Return workflow-pass summaries; name retained for route compatibility."""
    want = Path(page_file).name
    runs_dir = board / "_runs" / "page"
    if not runs_dir.is_dir():
        return []
    out = []
    for rf in runs_dir.glob("*/*.json"):
        try:
            run = json.loads(rf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(run, dict):
            continue
        if Path(str(run.get("page", ""))).name != want:
            continue
        receipts = [r for r in run.get("receipts", []) if isinstance(r, dict)]
        trail = [{**{k: r.get(k, "") for k in TRAIL_KEYS},
                  "run": _run_of(r.get("run") or r.get("phase", "")),
                  "route": _route(r.get("route", ""))} for r in receipts]
        packet = run.get("packet") if isinstance(run.get("packet"), dict) else {}
        last = receipts[-1] if receipts else {}
        out.append({
            "run_id": str(run.get("run_id", rf.stem)),
            "file": str(rf.relative_to(board)),
            "mtime": rf.stat().st_mtime,
            "status": str(run.get("status", "")),
            "start_run": _run_of(packet.get("start_run") or packet.get("start_phase", "")),
            "steps": len(receipts),
            "rounds": max((int(r.get("round", 1) or 1) for r in receipts),
                          default=0),
            "last": {
                "run": _run_of(last.get("run") or last.get("phase", "")),
                "route": _route(last.get("route", "")),
                "verdict": str(last.get("verdict", "")),
                "reason": str(last.get("reason", "")),
                "status": str(last.get("status", "")),
            },
            "trail": trail,
        })
    out.sort(key=lambda r: r["mtime"], reverse=True)
    return out[:MAX_RUNS]


class PageRunsMixin:

    # ---- GET /_board/pageruns?path=…&file=… ----------------------------
    def pageruns_view(self):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0], "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            return self._pageruns_send({"ok": False, "err": got[1]}, 404)
        f, board = got
        try:
            runs = page_runs(Path(board), f)
        except OSError as exc:
            return self._pageruns_send({"ok": False, "err": str(exc)}, 500)
        return self._pageruns_send(
            {"ok": True, "page": Path(f).name, "runs": runs}, 200)

    def _pageruns_send(self, payload, code):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
