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
from src.common import delivery_dir, delivery_read_lane_dir, delivery_relative
import re

from .outline_version import (plan_files, plan_dir, PREVIOUS, RECORD_KINDS, RECORDS, latest_outline,
                              version_policy_issues)
from .plan_shape import iter_plan_bullets

FAIL, WARN, INFO, OK = "FAIL", "WARN", "INFO", "OK"
ICON = {FAIL: "❌", WARN: "⚠️", INFO: "ℹ️", OK: "✅"}
HEAD_SCAN = 3000  # fallback only: `arc:` belongs in the header block, before the first `## `
REALIZES = re.compile(r"^(.*?)\s*<!-- realizes: (C\d+\.P\d+\.B\d+[a-z]*) -->", re.M)
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


def check_structure(plan: Path, text: str, out: list):
    """Section 1 (Structure) and section 3 (Draft) describe the same paragraphs and sentences (JL 261102: "when you
    update the draft, you should also udpate teh structure as well"); a Draft edited without its Structure fails."""
    from .plan_layout import structure_draft_mismatches
    for issue in structure_draft_mismatches(text):
        out.append(Finding(FAIL, "structure", issue + "; update both in the same edit", plan.name))


def _page_sentences(page_text: str) -> dict:
    """Map each `realizes:` address to its Page text.

    A tagged line opens the Bullet; following untagged prose lines, and a pipe table its
    Draft carries, continue it until a blank line, heading, list, comment lane, or the
    next tagged line.
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
              and not line.lstrip().startswith(("#", ">", "<!--", "-", "```", "*"))):
            page[current].append(line)   # prose, or a table the Bullet's Draft carries (JL 261004)
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
    latex = delivery_read_lane_dir(folder, "latex")
    if not latex.is_dir():
        out.append(Finding(INFO, "delivery", "no delivery/latex/ yet"))
        return
    snapshot = delivery_read_lane_dir(folder, "web") / page.name
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


def examples_state(folder: Path, head: str) -> tuple[bool, str]:
    """Is this Section's 📚 Examples ready? (JL 261104: "This is a must to do when you call the task for the
    /haipipe-paper-draft".) Ready: its face says `examples: none · <reason>`, or a Board topic that names this Task holds
    3 or more `reads/*/reading.yaml`, and the face's `examples:` names it."""
    m = re.search(r"(?m)^examples:[ \t]*(.*)$", head)
    said = m.group(1).strip() if m else ""
    if re.match(r"none\s*·\s*\S", said):
        return True, ""
    board = next((p for p in folder.parents if (p / "board.md").is_file()), None)
    if board is None:
        return False, "no Board above it, so no examples topic"
    path = folder.relative_to(board).as_posix()
    best = 0
    for t in board.glob("s[0-9]*"):
        faces = sorted(t.glob("s[0-9]*.md"))
        text = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in faces if ".mindmap." not in f.name and ".ideas." not in f.name)
        if path in text:
            best = max(best, len(list(t.glob("reads/*/reading.yaml"))))
    if best < 3:
        return False, f"{best} published papers read for {path}; 3 to 4 are required before it is written"
    return (True, "") if said else (False, "its face has no `examples:` line naming the topic")


def check_steps(folder: Path, page: Path, plan: Path | None, out: list):
    """A draft Task's seven steps, each by the file it leaves (ref/page-checklist.md § 6; JL 261102: "what is the
    checklist for the /haipipe-draft and /haipipe-paper-draft, why dont you make them to be complete?"). One WARN per
    step whose file is missing, so a Task is never called complete with a step skipped; Studio and Display are
    optional and only counted. Applies only to a face that says `task-type: draft`."""
    head = _header(page.read_text(encoding="utf-8"))
    if not re.search(r"(?m)^task-type:\s*draft\b", head):
        return
    stem, d = page.stem, plan_dir(folder)
    rec = lambda kind: (d / RECORDS / f"{stem}-{kind}.md").is_file() or (d / f"{stem}-{kind}.md").is_file()
    plan_text = plan.read_text(encoding="utf-8") if plan else ""
    approved = bool(re.search(r"(?m)^approved:\s*✅", plan_text))
    has_items = (d / f"{stem}-evidence-items.md").is_file() or (folder / "evidence" / "cards.yaml").is_file()
    built = [lane for lane in ("web", "latex", "word") if delivery_read_lane_dir(folder, lane).is_dir()]
    steps = []
    if re.search(r"(?m)^page-type:\s*section\b", head):   # a paper Section, Abstract or letter: examples before words
        ready, why = examples_state(folder, head)
        steps.append(("0 · Examples", ready, f"📚 Examples not ready: {why} (haipipe-paper-draft § Examples first)"))
    steps += [
        ("1 · Plan", rec("context"), f"no draft/records/{stem}-context.md (cli/context-record.py {page.name})"),
        ("1 · Plan", rec("requirement"), f"no draft/records/{stem}-requirement.md (its W rules)"),
        ("1 · Plan", bool(plan_text), "no draft/<stem>-draft-v<N>.md"),
        ("1 · Plan", approved, "plan not signed: `approved:` does not start with ✅ (a person signs)"),
        ("2 · Write", bool(re.search(r"(?m)^## \d+ · Draft\b", plan_text)), "no `## 3 · Draft` sentences"),
        ("3 · Evidence", has_items, f"no draft/{stem}-evidence-items.md or evidence/cards.yaml"),
        ("5 · Revise", rec("revise"), f"no draft/records/{stem}-revise.md (a Revise pass)"),
        ("Delivery", len(built) == 3, f"delivery lanes built: {', '.join(built) or 'none'} of web, latex, word (page.py export)"),
    ]
    missing = [(step, why) for step, ok, why in steps if not ok]
    for step, why in missing:
        out.append(Finding(WARN, "steps", f"{step}: {why}"))
    if not missing:
        out.append(Finding(INFO, "steps", "every step has its file (Studio and Display optional); a person still signs, accepts and sends"))


PERSON_STEPS = ("plan not signed",)   # a person's step stays a WARN even at the final gate


def check_printed(folder: Path, page: Path, blocks: list, out: list):
    """The final gate's last look (JL 261102: "the final draft is not consistent with the sturcutre"): every sentence
    of the current Draft is in the built LaTeX PDF, read back with pdftotext, so a reader gets what the plan says."""
    import subprocess
    pdf = delivery_read_lane_dir(folder, "latex") / f"{page.stem}.pdf"
    if not pdf.is_file():
        out.append(Finding(FAIL, "printed", f"no delivery latex/{pdf.name} to read back (page.py export)"))
        return
    try:
        text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, timeout=120).stdout
    except (OSError, subprocess.TimeoutExpired):
        out.append(Finding(WARN, "printed", "pdftotext is not available; the printed text was not read back"))
        return
    norm = lambda t: re.sub(r"\s+", " ", re.sub(r"<!--.*?-->|\\[a-zA-Z]+\*?|[{}$~\\]", " ", t)).translate(
        str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "-": None, "–": None, "—": None})).strip()
    # A sentence that crosses a page must still match: drop the page number and the running head between its halves.
    printed = norm(re.sub(r"(?m)^\s*(\d{1,4}|DRAFT)\s*$", " ", text.replace("\f", "\n")))
    drafts = [(b["address"], norm(b["draft"])) for b in blocks if b.get("draft")]
    gone = [a for a, d in drafts if d and len(d) > 12 and d[:40] not in printed]
    if gone:
        out.append(Finding(FAIL, "printed", f"{len(gone)} of {len(drafts)} Draft sentences are not in the printed "
                           f"{pdf.name}: {', '.join(gone[:6])}; adopt, then export"))
    else:
        out.append(Finding(OK, "printed", f"all {len(drafts)} Draft sentences are in the printed {pdf.name}"))


def finalize(report: dict) -> dict:
    """The final gate: what may wait while writing is under way may not wait at "finished". A WARN becomes a FAIL,
    except a person's own step (the sign), which stays a WARN so it is named and never ticked by the agent."""
    for f in report["findings"]:
        if f["level"] == WARN and not any(k in f["message"] for k in PERSON_STEPS):
            f["level"] = FAIL
    report["verdict"] = FAIL if any(f["level"] == FAIL for f in report["findings"]) else (
        WARN if any(f["level"] == WARN for f in report["findings"]) else OK)
    report["final"] = True
    return report


def folder_health(target: Path, final: bool = False) -> dict:
    page = _page_md(target)
    folder, stem = page.parent, page.stem
    out: list = []
    plan = check_layout(folder, stem, out)
    if plan is not None:
        plan_text = plan.read_text(encoding="utf-8")
        check_header(plan, plan_text, out)
        blocks = check_bullets(plan, plan_text, out)
        check_structure(plan, plan_text, out)
        check_sync(page.read_text(encoding="utf-8"), blocks, plan_text, out)
        check_evidence(folder, stem, plan_text, out)
    check_delivery(folder, page, out)
    check_steps(folder, page, plan, out)
    from .page_adopt import content_gap
    gap = content_gap(page)
    if gap:
        out.append(Finding(WARN, "content", f"Content prints {gap['printed']}; the current draft is {gap['current']}: "
                           f"{gap['why']}, then page.py export"))
    if final and plan is not None:
        check_printed(folder, page, blocks, out)
    check_threads(folder, stem, out)
    verdict = FAIL if any(f.level == FAIL for f in out) else (
        WARN if any(f.level == WARN for f in out) else OK)
    report = {"page": stem, "plan": plan.name if plan else None, "verdict": verdict,
              "findings": [asdict(f) for f in out]}
    return finalize(report) if final else report


def render(report: dict) -> str:
    lines = [f"{ICON[report['verdict']]} {report['page']} · plan {report['plan']}"]
    for f in report["findings"]:
        where = f" · {f['where']}" if f["where"] else ""
        lines.append(f"   {ICON[f['level']]} {f['check']:<9} {f['message']}{where}")
    return "\n".join(lines)
