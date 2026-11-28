"""Paper rows of `page.py health` that read beyond one Page Folder (hai-paper ref/must-check.md).

M-D09: while a version drafts, each Section's plan is the truth for that Section; a Narrative row that differs from
it is one quiet INFO on the version Job (narrative_finding), never a Section FAIL or a re-sign. Once the version is
sent, a changed Story § 8 row is named by its id (`C6`, or a label such as `TITLE`) to the Sections whose contract
names it (story_row_findings), read against the rows kept at the sign (draft/records/<stem>-sign.md, else the
version's records/narrative-sign.md).
M-D19: `page.py sync-narrative` rebuilds the rows (src/narrative_sync.py); at the final gate an unrebuilt Narrative
is a WARN on the version Job.
M-D11: a version Job's main text against the venue's shared cap (src/paper_budget.py).
M-D15: Content may hold adopted text while the plan is unsigned; health says so as a WARN that names the sign.
"""
from __future__ import annotations

import re
from pathlib import Path

ROWS_HEAD = "## Story rows it was signed against"
LABEL = re.compile(r"^([A-Z][A-Z0-9]*(?: [A-Z0-9]+)*(?: \([A-Z]\))?)\s{2,}\S")


def kept_text(record: Path, heading: str) -> str | None:
    """The raw body under one `## ` heading of a sign record, else None."""
    if not record.is_file():
        return None
    m = re.search(rf"(?ms)^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", record.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1) if m else None


def story_rows(text: str) -> dict:
    """{row id: its text, whitespace-normalized}: a table row by its first cell (`| C6 | … |`), a text-block line by
    its capital label (`TITLE   …`), with the label's continuation lines joined to it."""
    rows, last = {}, None
    for line in (text or "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            last = None
            if cells and cells[0] and not set(cells[0]) <= set("-: ") and cells[0].lower() != "id":
                rows[cells[0]] = " ".join(cells)
            continue
        m = LABEL.match(line)
        if m:
            last = m.group(1)
            rows[last] = re.sub(r"\s+", " ", s)
        elif last and line.startswith(" ") and s and not s.startswith("```"):
            rows[last] += " " + re.sub(r"\s+", " ", s)
        else:
            last = None
    return rows


def section_claims(folder: Path) -> set:
    """The Story claim ids this Section's contract names: its Narrative row's last cell, else `claim-ids:`."""
    from .folder_health import governing_row
    row, _face = governing_row(folder)
    if row:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        last = next((c for c in reversed(cells) if c), "")
        return set(re.findall(r"\bC\d+\b", last))
    face = folder / f"{folder.name}.md"
    head = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    m = re.search(r"(?m)^claim-ids:\s*(.+)$", head)
    return set(re.findall(r"(?:^|·)\s*(C\d+)\b", m.group(1))) if m else set()


def story_row_findings(folder: Path, story: str, sface: Path) -> list | None:
    """[(level, message)] for the Story rows that changed since this Section's basis; None when no basis can be
    read row by row (the caller keeps its whole-text message)."""
    from .folder_health import NARRATIVE_SIGN, sign_record
    basis = kept_text(sign_record(folder, folder.name), ROWS_HEAD)
    since = "this Section's plan was signed"
    if basis is None:
        basis = kept_text(folder.parent / NARRATIVE_SIGN, "## What it was signed against")
        since = "the version's Narrative was signed"
    if basis is None:
        return None
    old, new = story_rows(basis), story_rows(story)
    if not old or not new:
        return None
    changed = sorted((k for k in set(old) | set(new) if old.get(k) != new.get(k)),
                     key=lambda k: (not re.match(r"C\d+$", k), int(k[1:]) if re.match(r"C\d+$", k) else 0, k))
    if not changed:
        return []
    claims = section_claims(folder)
    mine = [k for k in changed if not re.match(r"C\d+$", k) or k in claims]
    other = [k for k in changed if k not in mine]
    out = []
    for k in mine:
        what = "is new" if k not in old else "is gone" if k not in new else "changed"
        out.append(("WARN", f"Story row {k} in {sface.name} § 8 {what} since {since}; {folder.name} restates it: "
                            f"check the Draft sentences that carry {k}, then re-sign the plan (page.py sign)"))
    if other:
        out.append(("INFO", f"Story row(s) {', '.join(other)} changed since {since}; {folder.name} does not name them"))
    return out


def unsigned_content(folder: Path, page: Path, plan: Path | None, approved: bool) -> str | None:
    """M-D15: the WARN when Content holds adopted text and the plan is unsigned, else None."""
    if approved or plan is None:
        return None
    text = page.read_text(encoding="utf-8", errors="ignore")
    head = re.split(r"(?m)^## ", text, maxsplit=1)[0]
    if not (re.search(r"(?m)^content:\s*(?:draft|outline) v", head) or "<!-- realizes:" in text):
        return None
    m = re.search(r"-(?:draft|outline)-v([\d.]+)\.md$", plan.name)
    return f"Content holds text from an unsigned plan (v{m.group(1) if m else '?'}); sign the plan"


def narrative_finding(folder: Path, final: bool) -> dict | None:
    """M-D09 and M-D19: one line on the version Job when its Narrative rows differ from the Section plans; quiet while
    drafting, a WARN at the final gate (before a send). An unsigned Narrative names the sign."""
    from .folder_health import _header
    from .narrative_sync import differing
    face = folder / f"{folder.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"(?m)^## Narrative\b", text):
        return None
    n = len(differing(folder))
    if n and final:
        return {"level": "WARN", "check": "narrative", "where": "", "message": f"the Narrative was not rebuilt since "
                f"the Sections changed ({n} Section plans differ): page.py sync-narrative, then page.py sign-narrative"}
    if n:
        return {"level": "INFO", "check": "narrative", "where": "", "message": f"the Narrative differs from {n} "
                "Section plans; rebuild it with page.py sync-narrative when the Sections are good"}
    from .narrative_sync import narrative_table
    if narrative_table(text)[0] and not re.search(r"(?m)^narrative-approved:\s*✅", _header(text)):
        return {"level": "WARN", "check": "narrative", "where": "",
                "message": "the Narrative is not signed: the person signs it once (page.py sign-narrative)"}
    return None


def job_report(target: Path, final: bool = False) -> dict | None:
    """A version Job's own health (the main-text budget, the Narrative), or None when the target is not a version Job."""
    from .page_structure import is_version_job
    from .paper_budget import budget, budget_line, over_budget
    folder = Path(target).expanduser().resolve()
    folder = folder.parent if folder.is_file() else folder
    if not is_version_job(folder):
        return None
    over = over_budget(folder)
    findings = [{"level": "WARN" if over else "OK", "check": "budget", "where": "",
                 "message": over or budget_line(budget(folder))}]
    note = narrative_finding(folder, final)
    findings += [note] if note else []
    verdict = "WARN" if any(f["level"] == "WARN" for f in findings) else "OK"
    return {"page": folder.name, "plan": None, "verdict": verdict, "findings": findings}
