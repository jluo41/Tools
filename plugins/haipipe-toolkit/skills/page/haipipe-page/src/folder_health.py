"""Folder health: does one Page Folder agree with itself?

`check.py` judges writing and form rules across a Board, and Page CHECK judges
one built version's prose. Neither asks whether the Folder's own parts agree:
one current Outline, records where they belong, every Bullet parseable, Page
sentences equal to their Drafts, Evidence ids and Result paths that resolve,
and delivery files newer than the Page they project. This module answers that
question mechanically, one finding per row, so a "done" claim can be tested
before it is made.

Levels: FAIL blocks a completion claim, WARN needs a look, INFO is a count.
"""
from dataclasses import asdict, dataclass
from pathlib import Path
import re

from .outline_version import (plan_files, plan_dir, PREVIOUS, RECORD_KINDS, RECORDS, latest_outline,
                              version_policy_issues)
from .plan_shape import iter_plan_bullets

FAIL, WARN, INFO, OK = "FAIL", "WARN", "INFO", "OK"
ICON = {FAIL: "❌", WARN: "⚠️", INFO: "ℹ️", OK: "✅"}
HEAD_SCAN = 3000  # fallback only: `arc:` belongs in the header block, before the first `## `
REALIZES = re.compile(r"^(.*?)\s*<!-- realizes: (C\d+\.P\d+\.B\d+) -->", re.M)
EVIDENCE_ID = re.compile(r"^\s*Evidence:\s*(E\d+-[A-Z]+-[A-Za-z0-9-]+)", re.M)
RESULT_PATH = re.compile(r"^\s*(?:Answered|Drawn):.*?·\s*Result\s+(\S+)", re.M)
VERSIONED = re.compile(r"-(?:outline|draft)-v\d")
ITEM_HEAD = re.compile(r"^### (E\d+-[A-Z]+-[A-Za-z0-9-]+)\b", re.M)


@dataclass
class Finding:
    level: str
    check: str
    message: str
    where: str = ""


def _page_md(target: Path) -> Path:
    target = Path(target).expanduser().resolve()
    if target.is_file():
        return target
    page = target / f"{target.name}.md"
    if not page.is_file():
        raise ValueError(f"No Page Face {page.name} in {target}")
    return page


def _header(text: str) -> str:
    """The key: value block above the first `## ` heading."""
    match = re.search(r"(?m)^## ", text)
    return text[: match.start()] if match else text


def check_layout(folder: Path, stem: str, out: list):
    outline = plan_dir(folder)
    if not outline.is_dir():
        out.append(Finding(FAIL, "layout", "no draft/ or outline/ folder"))
        return None
    plans = [p for p in plan_files(outline, stem) if VERSIONED.search(p.name)]
    if len(plans) != 1:
        names = ", ".join(p.name for p in plans) or "none"
        out.append(Finding(FAIL, "layout",
                           f"{outline.name}/ must hold exactly one current plan; found {len(plans)}: {names}"))
    loose = [p.name for kind in RECORD_KINDS for p in outline.glob(f"*-{kind}.md")
             if not VERSIONED.search(p.name)]
    if loose:
        out.append(Finding(WARN, "layout",
                           f"process records outside {outline.name}/{RECORDS}/: {', '.join(sorted(loose))} "
                           f"(page.py outline-tidy moves them)"))
    # `draft/evidence/bibex/` is still written by the Page export (src/common.py
    # evidence_lane_dir), so only the other retired lanes and files are flagged.
    # A `display/` lane whose units have no DISPLAY Result yet is still read by the
    # paper delivery, so it is reported apart and archived only after those Results exist.
    from .layout_check import LIVE_LANES, unconverted_display_units
    unconverted = unconverted_display_units(folder)
    retired = sorted(p.name for p in (outline / "evidence").iterdir()
                     if p.name not in LIVE_LANES and not (p.name == "display" and unconverted)) \
        if (outline / "evidence").is_dir() else []
    retired += sorted(p.name for p in outline.glob("*-evidence.md"))
    if retired:
        out.append(Finding(WARN, "layout",
                           f"retired Outline evidence still in {outline.name}/: {', '.join(retired)}; "
                           "archive it under _archive/legacy-outline-evidence/"))
    if unconverted:
        out.append(Finding(WARN, "layout",
                           f"{len(unconverted)} legacy display unit(s) in {outline.name}/evidence/display/ "
                           f"have no DISPLAY Result yet ({', '.join(unconverted[:3])}); make each a Result at "
                           "results/<re-run>/payload/<unit>/, then archive the lane"))
    return latest_outline(outline, stem)


def check_header(plan: Path, text: str, out: list):
    head = _header(text)
    for key in ("approved", "status"):
        if not re.search(rf"(?m)^{key}:\s*\S", head):
            out.append(Finding(WARN, "header", f"no `{key}:` line; status tools show this plan blank",
                               plan.name))
    cut = re.search(r"(?m)^## ", text)
    if not re.search(r"(?m)^arc:\s*\S", text[:cut.start()] if cut else text[:HEAD_SCAN]):
        where = "below the header block" if re.search(r"(?m)^arc:\s*\S", head) else "missing"
        out.append(Finding(WARN, "header", f"`arc:` line {where}; check.py reports plan-no-arc", plan.name))
    for issue in version_policy_issues(plan, text):
        out.append(Finding(WARN, "header", issue, plan.name))


def check_bullets(plan: Path, text: str, out: list):
    """A Bullet line that lost its two-space indent silently empties the Bullet."""
    in_division, in_bullet = False, False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            # Draft-first plans keep Bullets under `## C<n>`; a three-section
            # Draft Markdown keeps them under `## 1 · Structure` and `## 3 · Draft`.
            in_division = bool(re.match(r"^## (?:C\d+\b|\d+ · (?:Structure|Draft)\b)", line))
            in_bullet = False
            continue
        if not in_division or line.startswith("#"):
            in_bullet = False
            continue
        if re.match(r"^- (?:\[[ xX]\]\s*)?(?:B|S)\d+\s*·", line):
            in_bullet = True
            continue
        if in_bullet and line.strip() and not line.startswith(("  ", "- ", ">")):
            out.append(Finding(FAIL, "bullets",
                               "unindented line inside a Bullet; the parser drops the Bullet's "
                               "Draft and fields (indent it by two spaces)", f"{plan.name}:{number}"))
        if not line.strip():
            in_bullet = False
    blocks = iter_plan_bullets(text)
    empty = [b["address"] for b in blocks
             if not b["draft"] and not b["continuation"] and "Point:" in text]
    if empty:
        out.append(Finding(FAIL, "bullets",
                           f"{len(empty)} Bullet(s) parse with no Draft and no fields: {', '.join(empty[:6])}",
                           plan.name))
    return blocks


def _page_sentences(page_text: str) -> dict:
    """Map each `realizes:` address to its Page text.

    A tagged line opens the Bullet; following untagged prose lines continue it
    until a blank line, heading, list, comment lane, or the next tagged line.
    One address may also be tagged on several lines; their text is joined.
    """
    page: dict = {}
    current = held = None  # held: the Bullet a blank line paused, resumed only by a `$$` display block
    in_math = False
    for line in page_text.splitlines():
        stripped = line.strip()
        if in_math:
            page[current].append(line)
            in_math = stripped != "$$"
            continue
        match = REALIZES.match(line)
        if match:
            current, held = match.group(2), None
            page.setdefault(current, []).append(match.group(1))
        elif stripped == "$$" and (current or held):
            current, held, in_math = current or held, None, True
            page[current].append(line)
        elif (current and stripped
              and not line.lstrip().startswith(("#", ">", "<!--", "-", "|", "```", "*"))):
            page[current].append(line)
        elif not stripped:
            held, current = current or held, None
        else:
            current = held = None
    return {address: " ".join(" ".join(parts).split()) for address, parts in page.items()}


def check_sync(page_text: str, blocks: list, plan_text: str, out: list):
    drafts = {b["address"]: " ".join(b["draft"].split()) for b in blocks if b["draft"]}
    addresses = {b["address"] for b in blocks}
    page = _page_sentences(page_text)
    orphans = sorted(a for a in page if a not in addresses)
    head = _header(plan_text)
    gated = bool(re.search(r"(?m)^promotion-gate:\s*\S", head))
    if orphans:
        out.append(Finding(WARN if gated else FAIL, "sync",
                           f"{len(orphans)} Page sentence(s) realize an address the current plan lacks: "
                           f"{', '.join(orphans[:6])}"
                           + ("; the plan declares an open promotion-gate, so the Page still shows an "
                              "earlier Shape until release" if gated else "")))
    shared = [a for a in drafts if a in page]
    differ = [a for a in shared if drafts[a] != page[a]]
    unadopted = [a for a in drafts if a not in page]
    if not drafts:
        out.append(Finding(INFO, "sync", "plan carries no Drafts; nothing to compare"))
        return
    if differ or unadopted:
        out.append(Finding(WARN, "sync",
                           f"{len(shared) - len(differ)} of {len(drafts)} Drafts equal their Page sentence; "
                           f"{len(differ)} differ ({', '.join(differ[:6])}), "
                           f"{len(unadopted)} not on the Page ({', '.join(unadopted[:6])}); "
                           "fine while a CONTENT pass is pending, stale otherwise"))
    else:
        out.append(Finding(OK, "sync", f"all {len(drafts)} Drafts equal their Page sentence"))
        if "pending" in head.lower() and "adopt" in head.lower():
            out.append(Finding(WARN, "header",
                               "header says Page Content adoption is pending, but every Draft is "
                               "already on the Page"))


def check_evidence(folder: Path, stem: str, plan_text: str, out: list):
    items_file = plan_dir(folder) / f"{stem}-evidence-items.md"
    used = sorted(set(EVIDENCE_ID.findall(plan_text)))
    if used and not items_file.is_file():
        out.append(Finding(FAIL, "evidence", f"plan names {len(used)} Evidence Item(s) but "
                           f"{items_file.parent.name}/{items_file.name} is missing"))
    elif used:
        declared = set(ITEM_HEAD.findall(items_file.read_text(encoding="utf-8")))
        missing = [e for e in used if e not in declared]
        if missing:
            out.append(Finding(FAIL, "evidence",
                               f"Evidence Item(s) used in the plan but not declared: {', '.join(missing)}"))
    unresolved = []
    for path in sorted(set(RESULT_PATH.findall(plan_text))):
        if not (folder / path).exists():
            unresolved.append(path)
    if unresolved:
        out.append(Finding(WARN, "evidence",
                           f"{len(unresolved)} bound Result path(s) do not exist: {', '.join(unresolved[:4])}"))
    if used and not unresolved and not any(f.check == "evidence" for f in out):
        out.append(Finding(OK, "evidence", f"{len(used)} Evidence Item(s) declared; bound Results resolve"))


def _reader_text(text: str) -> str:
    """Page text with backstage-only parts removed: status lines and the generated contract block."""
    text = re.sub(r"(?s)<!-- haipipe:contract:start.*?<!-- haipipe:contract:end -->", "", text)
    return "\n".join(line for line in text.splitlines()
                     if not re.match(r"^(state|contract-source-hash):", line)).strip()


def check_delivery(folder: Path, page: Path, out: list):
    latex = folder / "delivery" / "latex"
    if not latex.is_dir():
        out.append(Finding(INFO, "delivery", "no delivery/latex/ yet"))
        return
    snapshot = folder / "delivery" / "web" / page.name
    if snapshot.is_file():
        # The export keeps the source it built from; compare what a reader sees, not file times.
        if _reader_text(page.read_text(encoding="utf-8")) != _reader_text(snapshot.read_text(encoding="utf-8")):
            out.append(Finding(WARN, "delivery",
                               f"Page text changed since the last export (delivery/web/{page.name})"))
        return
    source = page.stat().st_mtime
    stale = [p.name for p in (latex / f"{page.stem}.tex", latex / f"{page.stem}.pdf")
             if p.is_file() and p.stat().st_mtime < source]
    if stale:
        out.append(Finding(WARN, "delivery", f"older than the Page source: {', '.join(stale)}"))


def check_threads(folder: Path, stem: str, out: list):
    discussion = plan_dir(folder) / RECORDS / f"{stem}-discussion.md"
    if discussion.is_file():
        ids = re.findall(r"(?m)^#{3,4} (D\d+)\b", discussion.read_text(encoding="utf-8"))
        if ids:
            out.append(Finding(INFO, "threads", f"{len(ids)} open thread(s): {', '.join(ids)}"))


def folder_health(target: Path) -> dict:
    page = _page_md(target)
    folder, stem = page.parent, page.stem
    out: list = []
    plan = check_layout(folder, stem, out)
    if plan is not None:
        plan_text = plan.read_text(encoding="utf-8")
        check_header(plan, plan_text, out)
        blocks = check_bullets(plan, plan_text, out)
        check_sync(page.read_text(encoding="utf-8"), blocks, plan_text, out)
        check_evidence(folder, stem, plan_text, out)
    check_delivery(folder, page, out)
    check_threads(folder, stem, out)
    verdict = FAIL if any(f.level == FAIL for f in out) else (
        WARN if any(f.level == WARN for f in out) else OK)
    return {"page": stem, "plan": plan.name if plan else None, "verdict": verdict,
            "findings": [asdict(f) for f in out]}


def render(report: dict) -> str:
    lines = [f"{ICON[report['verdict']]} {report['page']} · plan {report['plan']}"]
    for f in report["findings"]:
        where = f" · {f['where']}" if f["where"] else ""
        lines.append(f"   {ICON[f['level']]} {f['check']:<9} {f['message']}{where}")
    return "\n".join(lines)
