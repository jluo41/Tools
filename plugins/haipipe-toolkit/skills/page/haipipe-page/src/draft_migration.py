"""Move a Page to the 0.118 layout: `draft/`, a three-section Draft Markdown, runs by Space.

    page.py draft-layout <page> [--sort-runs] [--dry-run]

1. `outline/` becomes `draft/` (nothing else moves inside it).
2. The current plan is written again as `<stem>-draft-v<G>.<S+1>.md` in three
   sections with the same Bullets; the old version goes to `previous/`.
3. With `--sort-runs`, each ticket in a flat `runs/` moves to its Space folder
   (`src/run_folders.py`), a moved shell script finds the Page two folders up,
   and `runs/<name>` citations inside the Page follow the move. `results/` stays.

Every step refuses rather than guesses: a plan that would parse to different
Bullets is not written, and an existing `draft/` beside `outline/` stops the run.
"""
from __future__ import annotations

from pathlib import Path
import re

from .outline_version import latest_outline, plan_dir, retire_superseded, version_tag
from .plan_layout import is_sectioned, to_sectioned
from .plan_shape import iter_plan_bullets
from .run_folders import folder_for

TEXT = {".md", ".yaml", ".yml", ".json", ".sh", ".txt", ".py", ".tex", ".mmd", ".html"}


def _bullets(text: str):
    return [(b["address"], b["draft"], b["head"], tuple(b["continuation"])) for b in iter_plan_bullets(text)]


def _next_shape(tag: str) -> str:
    m = re.fullmatch(r"v(\d+)(?:\.(\d+))?(?:\.\d+)?", tag or "")
    return "v%s.%d" % (m.group(1), int(m.group(2) or 0) + 1) if m else "v0.1"


def draft_layout(page_folder: Path, *, sort_runs: bool = False, dry_run: bool = False) -> dict:
    folder = Path(page_folder).expanduser().resolve()
    if folder.is_file():
        folder = folder.parent
    stem = folder.name
    report = {"page": stem, "dry_run": dry_run, "renamed": None, "plan": None, "runs_moved": 0,
              "scripts_fixed": 0, "citations": 0}
    outline, draft = folder / "outline", folder / "draft"
    if outline.is_dir() and not outline.is_symlink():
        if draft.exists():
            raise ValueError("both outline/ and draft/ exist; merge them by hand first")
        report["renamed"] = "outline/ → draft/"
        if not dry_run:
            outline.rename(draft)
    home = draft if (draft.is_dir() or not dry_run) else plan_dir(folder)
    current = latest_outline(home, stem)
    if current is None:
        raise ValueError(f"no plan in {home}")
    text = current.read_text(encoding="utf-8")
    if is_sectioned(text):
        report["plan"] = f"{current.name} is already three sections"
    else:
        old_tag = version_tag(current)
        new_tag = _next_shape(old_tag)
        body = to_sectioned(text)
        body = re.sub(r"(?m)^# (.+?) · outline v[\d.]+", rf"# \1 · draft {new_tag}", body, count=1)
        body = re.sub(r"(?m)^outline-version:.*$", f"draft-version: {new_tag}", body, count=1)
        if re.search(r"(?m)^supersedes:", body):
            body = re.sub(r"(?m)^supersedes:.*$", f"supersedes: {old_tag}", body, count=1)
        if _bullets(body) != _bullets(text):
            raise ValueError(f"{current.name}: the three-section layout would change a Bullet; nothing written")
        target = current.parent / f"{stem}-draft-{new_tag}.md"
        report["plan"] = f"{current.name} → {target.name}"
        if not dry_run:
            target.write_text(body, encoding="utf-8")
            retire_superseded(current.parent, stem)
    if sort_runs:
        report.update(_sort_runs(folder, dry_run=dry_run))
    return report


def _sort_runs(folder: Path, *, dry_run: bool) -> dict:
    runs = folder / "runs"
    moves = {}
    for ticket in sorted(p for p in runs.iterdir() if p.is_file()) if runs.is_dir() else []:
        space = folder_for(ticket.stem) or ("draft-auto-run" if ticket.name.startswith("rp-") else None)
        if space:
            moves[ticket.name] = space
    fixed = cited = 0
    if dry_run:
        return {"runs_moved": len(moves), "scripts_fixed": 0, "citations": 0}
    for name, space in moves.items():
        (runs / space).mkdir(exist_ok=True)
        (runs / name).rename(runs / space / name)
        moved = runs / space / name
        if moved.suffix == ".sh":
            text = moved.read_text(encoding="utf-8")
            new, n = re.subn(r'"\)/\.\." && pwd\)', '")/../.." && pwd)', text)
            if n:
                moved.write_text(new, encoding="utf-8")
                fixed += n
    stems = {re.sub(r"\.(md|sh)$", "", name): space for name, space in moves.items()}
    token = re.compile(r"(?<![A-Za-z0-9_])((?:[\w.-]+/)?)runs/([A-Za-z0-9._-]+)")

    swapped = [0]

    def swap(match):
        owner, name = match.group(1), match.group(2)
        sibling = owner.rstrip("/")
        if sibling and sibling != folder.name and (folder.parent / sibling).is_dir():
            return match.group(0)  # another Page's runs keep their own paths
        space = stems.get(re.sub(r"\.(md|sh)$", "", name))
        if not space:
            return match.group(0)
        swapped[0] += 1
        return f"{owner}runs/{space}/{name}"

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix in TEXT:
            text = path.read_text(encoding="utf-8", errors="replace")
            new = token.sub(swap, text)
            if new != text:
                path.write_text(new, encoding="utf-8")
    cited = swapped[0]
    return {"runs_moved": len(moves), "scripts_fixed": fixed, "citations": cited}
