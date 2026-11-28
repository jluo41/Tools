"""The 🧵 Trace section of a work page (JL 261127: "for there, do you think we can add the a trace here?", on the
page's section menu beside Timeline). One left tab per trace that touches this page's folder, newest first, its mark
(✅ closed, 🏃 files touched, ⬜ only planned); the right side reads it: the aim, the plan with each file's mark, the
prompts, the check and the summary. The traces are the Block's own and other Blocks' that planned or changed a file
here (trace_view.traces and visiting); a Job or Task page keeps those with a file under its own folder.
"""
from __future__ import annotations

from pathlib import Path

from live import frame
from live.file_icons import STATE_MARKS
from live.trace_view import _bullets, _when, overall, read, sections, states, traces, visiting, warm

MARK = {"done": "✅", "edit": "🏃", "plan": "⬜"}


def block_of(folder: Path) -> Path | None:
    """The bNN_ Block this folder is in (itself, for a Block)."""
    for p in (folder, *folder.parents):
        if p.name[:1] == "b" and p.name[1:3].isdigit() and "_" in p.name and (p / "board.md").is_file():
            return p
    return None


def found(folder: Path, root: Path) -> list[tuple[Path, dict]]:
    """The traces with a planned or changed file under this folder, newest first."""
    folder, root = folder.resolve(), root.resolve()
    block = block_of(folder)
    if block is None:
        return []
    mine = folder.relative_to(root).as_posix() + "/"
    out = []
    for face, meta in sorted(traces(block) + visiting(block, root), key=lambda x: _when(*x)[0], reverse=True):
        paths = [str(i.get("path") or "") for i in meta.get("plan") or [] if isinstance(i, dict)]
        paths += [str(p) for p in meta.get("changed") or []]
        if folder == block and face.is_relative_to(block) or any(p.strip().startswith(mine) for p in paths):
            out.append((face, meta))
    return out


def _panel(face: Path, meta: dict, rows: dict, root: Path) -> str:
    esc, parts = frame.esc, sections(face)
    plan = "".join(
        f'<li><span class="tr-m" title="{esc(r["state"])}">{STATE_MARKS.get(r["state"], ("", ""))[0]}</span>'
        f'<code>{esc(r["do"])}</code> <a href="{esc(frame.reader(root / p, root))}">{esc(p.rsplit("/", 1)[-1])}</a>'
        + (f' <span class=mut>{esc(r["what"])}</span>' if r["what"] else "") + "</li>" for p, r in rows.items())
    lists = "".join(f"<h4>{name}</h4><ul>" + "".join(f"<li>{esc(b)}</li>" for b in _bullets(parts[name])) + "</ul>"
                    for name in ("Prompts", "Check") if parts.get(name))
    _, day, hm = _when(face, meta)
    return (f'<p class="tr-aim">{esc(str(meta.get("aim") or ""))}</p>'
            + (f"<h4>Plan</h4><ul class=tr-plan>{plan}</ul>" if plan else "") + lists
            + (f'<h4>Summary</h4><p>{esc(" ".join(parts["Summary"].split()))}</p>' if parts.get("Summary") else "")
            + f'<p class=mut><a href="{esc(frame.reader(face, root))}">{esc(day)} {esc(hm)} · {esc(face.name)}</a></p>')


def html(folder: Path, root: Path) -> str:
    """The section body, or '' when no trace touches this folder (the section is then not shown)."""
    from live.ui_parts import _side_tabs
    root = root.resolve()
    rows = found(folder, root)
    if not rows:
        return ""
    warm(root, [m for _, m in rows])
    tabs, panels = [], []
    for face, meta in rows:
        files = states(meta, root, keep=True)
        _, day, hm = _when(face, meta)
        tabs.append((f'{MARK.get(overall(meta, files), "⬜")} {day} {hm} · {meta.get("title") or face.stem}', ""))
        panels.append(_panel(face, meta, files, root))
    return STYLE + _side_tabs("work-trace-", tabs, panels)


STYLE = """<style>.tr-aim{font-size:15px;margin:0 0 10px}.tr-plan{list-style:none;padding:0}.tr-plan li{margin:4px 0}
.tr-m{display:inline-block;width:18px}.tr-plan code{font-size:11.5px;color:var(--muted);margin-right:4px}</style>"""
