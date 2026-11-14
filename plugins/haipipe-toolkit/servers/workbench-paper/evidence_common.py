"""The names the evidence readers share: where a Job's check and item Tasks are, a Task's newest Result file, its
Pop out link, the key-and-value rows and their CSS, and a citation status in plain words. Imports neither
evidence_read nor evidence_cite, so both import it at their top; evidence_read re-exports every name."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc

CITE_WORDS = {"verified": "verified", "card-only": "source card, not in the bib", "bib-only": "in the bib, no source card",
              "missing-bib": "not in the bib", "TOADD": "to add", "toadd": "to add"}


def is_check(task: Path) -> bool:
    """A whole-paper check Task (t99_*): it reads every other Task of its Job, so it is shown once, as a verdict."""
    return task.name.startswith("t99_")


def check_task(job: Path) -> Path | None:
    return next((t for t in sorted(job.glob("t99_*")) if t.is_dir()), None)


def item_tasks(job: Path) -> list:
    """A Job's Tasks without its whole-paper check, in their number order."""
    return sorted((t for t in job.glob("t[0-9]*_*") if t.is_dir() and not is_check(t)), key=lambda t: t.name)


def newest(task: Path, name: str) -> Path | None:
    """The newest Run's result file `name` of a Task (by Run name, then time), else None."""
    found = list(task.glob(f"runs/*/result/{name}")) if task is not None else []
    return max(found, key=lambda f: (f.parent.parent.name, f.stat().st_mtime)) if found else None


def url(f: Path, root: Path) -> str:
    return "/" + quote(ds._rel(f, root))


def _pop(label: str, f: Path | None, root: Path, name: str = "") -> str:
    return (f'<a class=fd-btn data-pop="{esc(name or label)}" href="{esc(url(f, root))}">{esc(label)}</a>'
            if f is not None and f.is_file() else "")


VALUE_CSS = """<style>.ev-line{margin:0 0 10px;font-size:13.5px}.ev-verdict{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;
margin:0 0 12px;padding:7px 12px;border:1px solid var(--line);border-radius:8px;font-size:13.5px}.ev-verdict b{font-weight:600}
.ev-verdict .fd-btn{margin-left:auto}
.ev-rows{display:grid;gap:6px;margin:0 0 12px}.ev-row{border:1px solid var(--line);border-radius:8px;padding:7px 11px;font-size:13.5px}
.ev-row.bad{border-left:3px solid light-dark(#c92a2a,#ff8787)}.ev-row.wait{border-left:3px solid light-dark(#b35c00,#ffc078)}
.ev-row.ok{border-left:3px solid light-dark(#2b8a3e,#8bd49a)}
.ev-row>b{display:block;font-size:14px;margin:0 0 3px;overflow-wrap:anywhere}
.ev-kv{display:grid;grid-template-columns:110px minmax(0,1fr);gap:2px 10px;margin:0;font-size:13px}
.ev-kv dt{color:var(--muted)}.ev-kv dd{margin:0;overflow-wrap:anywhere}
@media(max-width:600px){.ev-kv{grid-template-columns:1fr;gap:0}.ev-kv dt{margin-top:4px}.ev-verdict .fd-btn{margin-left:0}}</style>"""


def _kv(pairs) -> str:
    return '<dl class=ev-kv>' + "".join(f'<dt>{esc(k)}</dt><dd>{v}</dd>' for k, v in pairs if v) + '</dl>'
