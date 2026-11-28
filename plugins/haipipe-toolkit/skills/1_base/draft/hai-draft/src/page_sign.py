"""Sign a draft Task's plan, or a version's `## Narrative`, with the person's word from chat (JL 261111: "the Plan
sign is a real gate").

The person says it in chat ("go with B", "this structure"); the agent never decides it. A plan's sign is
`approved: ✅ <who> <yymmdd> · in chat: "<quote>"` on the current Draft Markdown; a version's is
`narrative-approved: ✅ …` on the version face's header. Each also keeps what was signed against, as text, in a
record (no hash; staleness is a content compare): `draft/records/<stem>-sign.md` holds the row that governs the
Section (its Job's `## Narrative` row, else the Story's § 8 row), `<job>/records/narrative-sign.md` the Story's § 8.
`page.py health` reads the record back and says when what it holds has moved.
"""
from datetime import date
from pathlib import Path
import re

from .folder_health import (_header, _page_md, governing_row, story_narrative, NARRATIVE_SIGN, sign_record)
from .outline_version import latest_outline, plan_dir
from .paper_health import ROWS_HEAD


def _record(path: Path, title: str, line: str, face: Path | None, text: str | None, dry_run: bool,
            extra: str = "") -> str:
    if text is None:
        return "nothing governs it yet: no record kept"
    body = (f"# {title}\n\n{line.split(': ', 1)[1]}\nsigned-against: {face.name}\n\n"
            f"## What it was signed against\n\n{text.strip()}\n" + extra)
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return f"kept what it was signed against in {path.parent.name}/{path.name} (from {face.name})"


def sign(target: Path, quote: str, who: str = "JL", dry_run: bool = False) -> dict:
    if not quote.strip():
        return {"ok": False, "message": "no quote: the sign is the person's own words in chat, quoted"}
    page = _page_md(target)
    plan = latest_outline(plan_dir(page.parent), page.stem)
    if plan is None:
        return {"ok": False, "message": f"no current Draft Markdown for {page.stem}"}
    text = plan.read_text(encoding="utf-8")
    line = f'approved: ✅ {who} {date.today():%y%m%d} · in chat: "{quote.strip()}"'
    if re.search(r"(?m)^approved:", text):
        text = re.sub(r"(?m)^approved:.*$", lambda _: line, text, count=1)
    else:
        text = re.sub(r"(?m)^(# .*)$", lambda m: m.group(1) + "\n" + line, text, count=1)
    if not dry_run:
        plan.write_text(text, encoding="utf-8")
    row, face = governing_row(page.parent)
    story, _sface = story_narrative(page.parent)   # M-D09: the Story rows this plan answers, read back by health
    extra = f"\n{ROWS_HEAD}\n\n{story.strip()}\n" if story else ""
    kept = _record(sign_record(page.parent, page.stem), f"{page.stem} · the plan's sign", line, face, row, dry_run,
                   extra)
    return {"ok": True, "plan": plan.name, "approved": line, "row": kept, "dry_run": dry_run}


def sign_narrative(job: Path, quote: str, who: str = "JL", dry_run: bool = False) -> dict:
    """Sign a version's `## Narrative`: `narrative-approved:` and a readable `story-at-sign:` on the face's header."""
    if not quote.strip():
        return {"ok": False, "message": "no quote: the sign is the person's own words in chat, quoted"}
    job = Path(job).expanduser().resolve()
    face = job if job.is_file() else job / f"{job.name}.md"
    if not face.is_file():
        return {"ok": False, "message": f"no Job face {face.name}"}
    text = face.read_text(encoding="utf-8")
    if not re.search(r"(?m)^## Narrative\b", text):
        return {"ok": False, "message": f"{face.name} has no ## Narrative to sign"}
    day = f"{date.today():%y%m%d}"
    line = f'narrative-approved: ✅ {who} {day} · in chat: "{quote.strip()}"'
    story, sface = story_narrative(face.parent / "_")     # the Story is found from inside the Job
    head, body = _header(text), text[len(_header(text)):]
    head = re.sub(r"(?m)^(?:narrative-approved|story-at-sign):.*\n?", "", head).rstrip("\n") + "\n" + line + "\n"
    if story is not None:
        head += f"story-at-sign: {sface.stem} § 8 as of {day} ({NARRATIVE_SIGN})\n"
    if not dry_run:
        face.write_text(head + "\n" + body.lstrip("\n"), encoding="utf-8")
    kept = _record(face.parent / NARRATIVE_SIGN, f"{face.parent.name} · the Narrative's sign", line, sface, story, dry_run)
    return {"ok": True, "plan": face.name, "approved": line, "row": kept, "dry_run": dry_run}


def render(r: dict) -> str:
    if not r["ok"]:
        return "❌ " + r["message"]
    return "%s%s\n  %s\n  %s" % ("(dry run) " if r["dry_run"] else "✅ ", r["plan"], r["approved"], r["row"])
