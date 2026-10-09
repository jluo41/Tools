"""Build a Page's LaTeX and Word delivery from the terminal, exactly as a click does.

The LaTeX and Word doors are `ExportMixin.export_latex` / `export_word` in
`servers/workbench/task-page/export.py`. Until 260928 they ran only inside a server
(POST /_board/latex, /_board/word), so an agent with no server improvised its
own call and wrote views that linked differently (JL 260928 field test). This
runs the same two methods in-process with the Board server's root, the
repository root, so the files match what the server would write.
"""
from __future__ import annotations

from pathlib import Path
import sys

SERVERS = next(p for p in Path(__file__).resolve().parents if p.name == "skills").parent / "servers"


def repo_root(folder: Path) -> Path:
    """The folder the Board server serves: the one holding pyproject.toml and code/."""
    folder = Path(folder).resolve()
    for d in (folder, *folder.parents):
        if (d / "pyproject.toml").is_file() and (d / "code").is_dir():
            return d
    return folder.parent


def _exporter(root: Path):
    host = str(SERVERS / "_host")
    if host not in sys.path:
        sys.path.insert(0, host)
    import host_paths
    host_paths.bootstrap()
    from live.base import BaseMixin
    from live.export import ExportMixin

    class Exporter(BaseMixin, ExportMixin):
        def __init__(self, root):
            self.root = Path(root).resolve()

    return Exporter(root)


# One fixed Delivery Run per lane (JL 260928), named by the one grammar: run-delivery-webpage · latex · word.
from src.run_names import delivery_name  # noqa: E402

RUN_NAMES = {lane: delivery_name(lane) for lane in ("web", "latex", "word")}
_TICKET = """#!/usr/bin/env bash
# {run} · build delivery/{lane}/ from this Page. Every rebuild reruns this same Run;
# the files in delivery/{lane}/ are its result and their file time says when it last ran.
# Written by `page.py export`; never edited by hand (AGENTS.md rule 6).
set -euo pipefail
page="$(cd "$(dirname "$0")/{up}" && pwd)"
root="$page"
until [ -f "$root/pyproject.toml" ] && [ -d "$root/code" ]; do
  root="$(dirname "$root")"
  [ "$root" = / ] && {{ echo "{run}: no repository root above $page" >&2; exit 1; }}
done
exec "$root/.venv/bin/python" "$root/Tools/plugins/haipipe-toolkit/skills/1_base/page/haipipe-page/cli/page.py" \\
  export "$page" --lane {lane}{author}
"""


_BUILT = {"web": ("index.html",), "latex": ("{stem}.pdf", "{stem}.tex"), "word": ("{stem}.docx",)}


def built_lanes(folder: Path, stem: str) -> list[str]:
    """The lanes whose files a build already wrote (web, latex, word)."""
    return [lane for lane, names in _BUILT.items()
            if any((Path(folder) / "delivery" / lane / n.format(stem=stem)).is_file() for n in names)]


def docx_author(folder: Path, stem: str) -> str | None:
    """The comment author the last Word build used, so a rerun keeps it."""
    import re
    import zipfile
    docx = Path(folder) / "delivery" / "word" / (stem + ".docx")
    try:
        xml = zipfile.ZipFile(docx).read("word/comments.xml").decode("utf-8", "replace")
    except (OSError, KeyError, zipfile.BadZipFile):
        return None
    m = re.search(r'w:author="([^"]+)"', xml)
    return m.group(1) if m else None


def write_ticket(folder: Path, lane: str, author: str | None = None) -> Path:
    """Write `runs/run-delivery-<lane>/run-delivery-<lane>.sh`, the command that reruns this lane's
    one Delivery Run, and its card (one folder per Run, 0.122). An older flat ticket
    `runs/run-delivery-<lane>.sh` is the same Run: it is removed so the lane keeps one ticket."""
    from src.run_folders import ticket_dir, write_card
    run = RUN_NAMES[lane]
    ticket = ticket_dir(folder, run) / (run + ".sh")        # the run's own folder
    ticket.parent.mkdir(parents=True, exist_ok=True)
    up = "/".join([".."] * len(ticket.parent.relative_to(Path(folder)).parts))
    quoted = ' --author "%s"' % author.replace('"', "") if lane == "word" and author else ""
    text = _TICKET.format(run=run, lane=lane, author=quoted, up=up)
    if not ticket.is_file() or ticket.read_text(encoding="utf-8") != text:
        ticket.write_text(text, encoding="utf-8")
        ticket.chmod(0o755)
    flat = Path(folder) / "runs" / (run + ".sh")
    if flat.is_file() and flat != ticket:
        flat.unlink()
    if not (ticket.parent / "run.yaml").is_file():
        write_card(folder, run, type="delivery", target=lane, skill="haipipe-page-delivery",
                   status="done", writes=["delivery/%s/" % lane], feeds=[])
    return ticket


def export(folder: Path, lanes, *, author: str | None = None, root: Path | None = None) -> dict:
    """Run the `latex` and/or `word` door for the Page in `folder`; {lane: result}."""
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root else repo_root(folder)
    exporter = _exporter(root)
    path = "/" + folder.relative_to(root).as_posix()
    results = {}
    for lane in lanes:
        payload = {"path": path, "file": ""}      # `target()` derives the Page Face from the folder
        if lane == "word" and author:
            payload["author"] = author
        door = exporter.export_latex if lane == "latex" else exporter.export_word
        res, err = door(payload)
        results[lane] = {"ok": not err, **({"err": err} if err else {}), **(res or {})}
    return results
