"""Move a Draft to its next version: `page.py bump <page> [--to v0.6] [--dry-run]`.

Run when the person says the draft is ok (JL 261020: "until I feel it is ok, and we can upgrade it to v0.5"); between
oks the Draft is edited in place. The current `draft/<stem>-draft-v<N>.md` becomes `draft/<stem>-draft-v<N+1>.md`
(the last number up by one, or `--to`), its header saying the new version, the one it supersedes and today's date;
the old file moves to `draft/previous/`. Nothing else changes: the person's `approved:` and `status:` stay as they are.
"""
from __future__ import annotations

import datetime
import re
import shutil
from pathlib import Path

from .folder_health import _page_md
from .outline_version import latest_outline, plan_dir

VERSION = re.compile(r"-draft-v(\d+(?:\.\d+)*)\.md$")


def bump(target, *, to: str | None = None, dry_run: bool = False) -> dict:
    page = _page_md(Path(target))
    folder, stem = page.parent, page.stem
    drafts = plan_dir(folder)
    plan = latest_outline(drafts, stem)
    report = {"page": str(page), "from": None, "to": None, "refused": None, "written": False}
    if plan is None or plan.parent != drafts or not VERSION.search(plan.name):
        report["refused"] = f"no current draft/{stem}-draft-v<N>.md"
        return report
    cur = VERSION.search(plan.name).group(1)
    parts = cur.split(".")
    new = (to or "").lstrip("v") or ".".join(parts[:-1] + [str(int(parts[-1]) + 1)])
    target_path = drafts / f"{stem}-draft-v{new}.md"
    report["from"], report["to"] = f"v{cur}", f"v{new}"
    if target_path.exists():
        report["refused"] = f"{target_path.name} already exists"
        return report
    text = plan.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^(# .*?draft )v" + re.escape(cur) + r"\b", lambda m: m.group(1) + f"v{new}", text, count=1)
    text = re.sub(r"(?m)^draft-version: .*$", f"draft-version: v{new}", text, count=1)
    text = (re.sub(r"(?m)^supersedes: .*$", f"supersedes: v{cur}", text, count=1) if re.search(r"(?m)^supersedes:", text)
            else re.sub(r"(?m)^(draft-version: .*)$", lambda m: m.group(1) + f"\nsupersedes: v{cur}", text, count=1))
    text = re.sub(r"(?m)^date: .*$", f"date: {datetime.date.today():%y%m%d}", text, count=1)
    if not dry_run:
        target_path.write_text(text, encoding="utf-8")
        (drafts / "previous").mkdir(exist_ok=True)
        shutil.move(str(plan), str(drafts / "previous" / plan.name))
        report["written"] = True
    return report


def render(report: dict) -> str:
    name = Path(report["page"]).stem
    if report["refused"]:
        return f"❌ {name} · not bumped: {report['refused']}"
    return (f"{'✏️' if report['written'] else '🔎'} {name} · draft {report['from']} → {report['to']}"
            + (f" (the old one in draft/previous/)" if report["written"] else ""))
