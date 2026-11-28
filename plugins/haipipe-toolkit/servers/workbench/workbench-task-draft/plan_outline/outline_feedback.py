"""Draft Space feedback composer · the ONE browser write, into the Run journal.

Each paragraph row of Draft Space carries a (+) and a folded note thread. A
saved note becomes one `#### Feedback F<nn>` item inside a PENDING Step of the
Page Writing Run (RP) that owns the paragraph, appended to that Run's current
Version journal `results/<run>/v<NNN>.md`. The plan file under `draft/` and
the Page source are never written here: the agent completes the pending Step
on its next turn through the fast feedback path of
`hai-draft-workflow/ref/interactive-writing-run.md`.

The owning Run is chosen in this order:

  1. an open `run-paragraph-…` Run whose paragraph range covers the paragraph
  2. an open `run-structure-…` Run (the structure is still being settled)
  3. an open `run-section-…` Run covering the paragraph
  4. the latest finished `run-paragraph-…` Run covering it, reopened in a new Version
  5. a newly allocated `run-paragraph-p<NN>` (ticket + paired results/)

`Kind` separates the author's story notes from wording requests:
`explore` (what this paragraph should explore or say), `wording` (change the
current Draft), `accept` (the person accepts the current wording).
"""
from __future__ import annotations

import datetime as dt
import html
import re
import secrets
from pathlib import Path

from live.outline_preview import page_lock
from src.outline_version import plan_dir, latest_outline
from src.run_folders import result_dir, result_roots, ticket_dir, ticket_rel, working_dir, write_card
from src import run_names

# The parts of this module live in their own files; every name still answers here.
from live.outline_feedback_read import (  # noqa: F401
    KINDS, MAX_GROUP, OPEN_STATUSES, _BULLET_RE, _ID_RE, _PARAGRAPH_RE, _WRITING_KIND, _e, _front, _kind_of, _now,
    _owning_run, _prange, _read, _saved, _section_body, _target_paragraphs, feedback_items, paragraphs, plan_path,
    run_rows,
)
from live.outline_feedback_html import (  # noqa: F401
    FEEDBACK_CSS, FEEDBACK_JS, _state_class, feedback_assets_html, feedback_badge_html, feedback_fold_html,
    feedback_list_html, feedback_summary,
)


# ── the write · one pending Step item in the owning Run's journal ──────────

def _step_numbers(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"^##[ \t]+Step[ \t]+s(\d{3})\b", text, re.M)]


def _pending_last_step(text: str) -> bool:
    steps = list(re.finditer(r"^##[ \t]+Step[ \t]+s\d{3}\b.*$", text, re.M))
    if not steps:
        return False
    tail = text[steps[-1].end():]
    if re.search(r"^##[ \t]+Version closure", tail, re.M):
        return False
    return bool(_section_body(tail, "Human feedback").strip()) and \
        not _section_body(tail, "Saved result").strip()


def _item_block(number: int, fid: str, target: str, p: int, kind: str, author: str, now: str,
                reviewed: str, comment: str) -> str:
    one_line = " ".join(comment.split())
    block = (
        "#### Feedback F%02d\n\n"
        "- Id: %s\n"
        "- Target: `%s` · P%02d\n"
        "- Kind: %s\n"
        "- By: %s · %s\n"
        "- Selected quote: explicitly absent\n"
        "- Source Version/Step: %s\n"
        "- Human comment: %s\n"
        "- Agent interpretation: pending\n"
        % (number, fid, target, p, kind, author, now, reviewed, one_line))
    if "\n" in comment.strip():
        block += "\n```text\n%s\n```\n" % comment.strip()
    return block


def _step_block(step: int, run_id: str, reviewed: str, paragraph: str, p: int, brief: str,
                base: str, author: str, now: str, comment: str, item: str) -> str:
    return (
        "\n## Step s%03d\n\n"
        "### Human feedback\n\n"
        "```text\n"
        "Source: Draft Space feedback composer · %s · %s\n"
        "Reviewed output: %s\n"
        "Mode: pending · the agent chooses local-edit | paragraph-rewrite | structure when it completes this Step\n"
        "Scope: %s · P%02d · %s\n"
        "Base: %s\n"
        "Protected: every other paragraph and all accepted text until this Step is completed\n"
        "```\n\n"
        "#### Original request\n\n"
        "```text\n%s\n```\n\n"
        "%s" % (step, author, now, reviewed, paragraph, p, brief or "no brief in the plan", base,
                comment.strip(), item))


def _version_header(run_id: str, version: str, prior: str, note: str) -> str:
    return ("Run: %s\nVersion: %s\nState: open\nPrior Version: %s\n%s\n"
            % (run_id, version, prior, note))


def _set_yaml_key(text: str, key: str, value: str) -> str:
    pattern = re.compile(r"^%s:[ \t]*.*$" % re.escape(key), re.M)
    line = "%s: %s" % (key, value)
    if pattern.search(text):
        return pattern.sub(lambda _m: line, text, count=1)
    return text.rstrip("\n") + "\n" + line + "\n"


def _write_runtime(row: dict, page: Path, version: str, step: str, vfile: Path,
                   prior_file: Path | None) -> None:
    runtime = row["runtime"]
    rel_result = row["results"].relative_to(page.parent).as_posix()
    if runtime.is_file():
        text = _read(runtime)
    else:
        text = (
            "run: %s\nfamily: page\noperation: interactive-writing\ninteraction: human-feedback\n"
            "target: %s\nparagraphs: %s\nticket: %s\nresult: %s\n"
            "status: ready\nversion: %s\nstep: s000\nversion_file: %s/%s.md\n"
            "worker:\n  kind: skill\n  name: hai-draft\n"
            "started_at: null\nfinished_at: null\nsupersedes: null\nfailure: null\n"
            "analysis:\n  status: deferred\n  task_run: null\n  result: null\n"
            % (row["id"], row.get("target", ""), row.get("paragraphs", ""),
               ticket_rel(page.parent, row["id"]), rel_result, version, rel_result, version))
    text = _set_yaml_key(text, "status", "waiting-for-feedback")
    text = _set_yaml_key(text, "version", version)
    text = _set_yaml_key(text, "step", step)
    text = _set_yaml_key(text, "version_file", "%s/%s" % (rel_result, vfile.name))
    # An older runtime.yaml may still carry sha256 keys; they are dropped, never rewritten.
    text = re.sub(r"(?m)^[ \t]*[A-Za-z_]*sha256:[^\n]*\n?", "", text)
    text = _set_yaml_key(text, "finished_at", "null")
    if prior_file is not None:
        text = _set_yaml_key(text, "supersedes", "%s/%s" % (rel_result, prior_file.name))
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(text, encoding="utf-8")


_WORKING_KEYS = ("Current version/step", "Current", "State", "Open feedback", "Next action", "Next")


def _write_working(row: dict, version: str, step: str, label: str, kind: str, paragraph: str,
                   author: str, now: str) -> None:
    path = row["results"] / "working.md"
    text = _read(path) if path.is_file() else "# %s · working state\n\n" % row["id"]
    values = {
        "Current version/step": "%s/%s" % (version, step),
        "Current": "%s/%s" % (version, step),
        "State": "waiting-for-feedback · Draft Space note %s pending an agent Step" % label,
        "Open feedback": "%s · %s on %s · from Draft Space by %s · %s · agent Step pending"
                         % (label, kind, paragraph, author, now),
        "Next action": "the agent completes Step %s (fast feedback path) for %s" % (step, label),
        "Next": "the agent completes Step %s (fast feedback path) for %s" % (step, label),
    }
    seen = set()
    for key in _WORKING_KEYS:
        pattern = re.compile(r"^(\s*[-*]?\s*(?:\*\*)?)(%s)((?:\*\*)?:)[ \t]*.*$" % re.escape(key),
                             re.M | re.I)
        if pattern.search(text):
            text = pattern.sub(lambda m: "%s%s%s %s" % (m.group(1), m.group(2), m.group(3), values[key]),
                               text, count=1)
            seen.add(key.split(" ")[0].lower())
    lines = []
    if "current" not in seen:
        lines.append("- Current version/step: %s" % values["Current"])
    if "state" not in seen:
        lines.append("- State: %s" % values["State"])
    if "open" not in seen:
        lines.append("- Open feedback: %s" % values["Open feedback"])
    if "next" not in seen:
        lines.append("- Next action: %s" % values["Next action"])
    if lines:
        text = text.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _allocate(page: Path, paragraph: str, para: dict, rows: list[dict], author: str, now: str) -> dict:
    taken = ({r["id"] for r in rows} | {p.name for p in (page.parent / "results").glob("run-*")}
             | {p.name for p in (page.parent / "runs").glob("run-*") if p.is_dir()})
    run_id = run_names.mint("paragraph", "p%02d" % para["p"], taken=taken)
    ticket = ticket_dir(page.parent, run_id) / ("%s.md" % run_id)
    ticket.parent.mkdir(parents=True, exist_ok=True)
    plan = plan_path(page)
    ticket.write_text(
        "---\nfamily: page\noperation: interactive-writing\ninteraction: human-feedback\n"
        "target: %s\nparagraphs: P%02d\nresult: runs/%s/passes/\npage: %s\nrun: %s\n---\n\n"
        "# %s\n\n"
        "- Goal: capture and settle Draft Space feedback on P%02d · %s · %s.\n"
        "- Run kind: %s\n"
        "- Structure description: P%02d · %s · %s\n"
        "- Page and Board: `%s`\n"
        "- Scope: P%02d at %s only; every other paragraph is protected.\n"
        "- Sources: current Page source, `%s`, and the closed structure Run's result when present.\n"
        "- Success: the person explicitly accepts or revises P%02d after the note is answered.\n"
        "- Review: P%02d read as one paragraph.\n"
        "- Allocated by: Draft Space feedback composer · %s · %s\n"
        % (paragraph, para["p"], run_id, page.stem, run_id, run_id,
           para["p"], paragraph, para.get("brief") or "no brief in the plan", run_id,
           para["p"], paragraph, para.get("brief") or "no brief in the plan", page.name,
           para["p"], paragraph, "%s/%s" % (plan.parent.name, plan.name) if plan else "the current plan",
           para["p"], para["p"], author, now),
        encoding="utf-8")
    results = working_dir(page.parent, run_id)        # its first pass: the run writes into it while open
    write_card(page.parent, run_id, type="paragraph", target=paragraph, skill="hai-draft-writing",
               agent=author or None, status="running", writes=[], feeds=[])
    return {"id": run_id, "kind": "para", "nn": len(rows) + 1, "ticket": ticket, "results": results,
            "runtime": results / "runtime.yaml", "status": "ready", "version": "", "step": "",
            "covers": {para["p"]}, "target": paragraph, "paragraphs": "P%02d" % para["p"]}


def _already_saved(row: dict, fid: str) -> bool:
    if not row["results"].is_dir():
        return False
    return any(("- Id: %s" % fid) in _read(v) for v in row["results"].glob("v[0-9][0-9][0-9].md"))


def save_feedback(page: Path, payload: dict, read_only: bool = False):
    """Append one Feedback item to the owning Run's journal; return (result, error)."""
    if read_only:
        return None, "This Page is served read-only; notes cannot be saved here"
    paragraph = str(payload.get("paragraph") or "").strip()
    if not _PARAGRAPH_RE.fullmatch(paragraph):
        return None, "Choose a paragraph"
    kind = str(payload.get("kind") or "explore").strip().lower()
    if kind not in KINDS:
        return None, "Kind must be explore, wording, or accept"
    bullet = str(payload.get("bullet") or "").strip()
    if bullet and not _BULLET_RE.fullmatch(bullet):
        return None, "Bullet address is not valid"
    author = " ".join(str(payload.get("author") or "").split())
    if not author or len(author) > 80 or "·" in author:
        return None, "Sign the note with a name (no middle-dot separator, at most 80 characters)"
    comment = str(payload.get("comment") or "").strip()
    if not comment or len(comment) > 8000:
        return None, "Write the note (at most 8,000 characters)"
    fid = str(payload.get("feedback_id") or "").strip()
    if not _ID_RE.fullmatch(fid):
        fid = "fb-" + secrets.token_hex(8)
    now = _now()

    with page_lock(page):
        paras = paragraphs(page)
        if paragraph not in paras:
            return None, "Paragraph is not in the current plan; reload Draft Space"
        para = paras[paragraph]
        if bullet and bullet not in para["bullets"]:
            return None, "Bullet is not in that paragraph; reload Draft Space"
        every = {v["p"] for v in paras.values()}
        rows = run_rows(page, every)
        row, mode = _owning_run(rows, para["p"])
        if mode == "allocate":
            row = _allocate(page, paragraph, para, rows, author, now)
            mode = "append"
        elif _already_saved(row, fid):
            items = feedback_items(page).get(paragraph, [])
            return _result(page, row, row.get("version", ""), row.get("step", ""), "", fid, paragraph,
                           items, None), None

        results = row["results"]
        results.mkdir(parents=True, exist_ok=True)
        versions = sorted(results.glob("v[0-9][0-9][0-9].md"))
        current = results / ("%s.md" % row["version"]) if row["version"] else None
        if current is not None and not current.is_file():
            current = versions[-1] if versions else None
        prior_file = None
        target = bullet or paragraph
        plan = plan_path(page)
        base = "; ".join(filter(None, [
            ("%s/%s saved %s" % (plan.parent.name, plan.name, _saved(plan))) if plan else "",
            "%s saved %s" % (page.name, _saved(page)) if page.is_file() else "",
        ]))
        reopen = mode == "reopen" or (current is not None and
                                      re.search(r"^##[ \t]+Version closure", _read(current), re.M))
        if current is None:
            version = "v001"
            vfile = results / "v001.md"
            text = _version_header(row["id"], version, "none",
                                   "Opened by: Draft Space feedback composer · %s · %s" % (author, now))
            reviewed = "initial state"
        elif reopen:
            prior_file = current
            version = "v%03d" % (int(current.stem[1:]) + 1)
            vfile = results / ("%s.md" % version)
            prior_step = row.get("step") or ("s%03d" % max(_step_numbers(_read(current)) or [0]))
            text = _version_header(
                row["id"], version, current.name,
                "Reopened by: Draft Space feedback composer · %s · %s · kind %s · target %s\n"
                "Protected: the accepted text of this Run's paragraphs stays byte-for-byte until a "
                "completed Step changes it" % (author, now, kind, target))
            reviewed = "%s %s/%s" % (row["id"], current.stem, prior_step)
        else:
            version = current.stem
            vfile = current
            text = _read(current)
            steps = _step_numbers(text)
            reviewed = ("%s %s/s%03d" % (row["id"], version, steps[-1])) if steps else "initial state"

        if vfile.is_file() and _pending_last_step(text):
            step_number = max(_step_numbers(text))
            existing = len(re.findall(r"^####[ \t]+Feedback[ \t]+F\d+", text[text.rfind("## Step s"):], re.M))
            item = _item_block(existing + 1, fid, target, para["p"], kind, author, now, reviewed, comment)
            text = text.rstrip("\n") + "\n\n" + item
            label = "F%02d" % (existing + 1)
        else:
            step_number = (max(_step_numbers(text)) + 1) if _step_numbers(text) else 1
            item = _item_block(1, fid, target, para["p"], kind, author, now, reviewed, comment)
            text = text.rstrip("\n") + "\n" + _step_block(
                step_number, row["id"], reviewed, paragraph, para["p"], para.get("brief", ""),
                base, author, now, comment, item)
            label = "F01"
        step = "s%03d" % step_number
        vfile.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
        _write_runtime(row, page, version, step, vfile, prior_file)
        _write_working(row, version, step, label, kind, paragraph, author, now)
        items = feedback_items(page).get(paragraph, [])
        return _result(page, row, version, step, label, fid, paragraph, items, vfile), None


def _result(page: Path, row: dict, version: str, step: str, label: str, fid: str, paragraph: str,
            items: list[dict], vfile: Path | None) -> dict:
    if vfile is None:
        vfile = row["results"] / ("%s.md" % version) if version else row["results"]
    try:
        shown = str(vfile.relative_to(page.parent))
    except ValueError:
        shown = str(vfile)
    if not label:
        label = next((i["label"] for i in items if i.get("id") == fid), "")
    return {
        "run": row["id"], "run_version": version, "step": step, "feedback": label, "id": fid,
        "file": shown, "paragraph": paragraph,
        "count": len(items), "pending": sum(1 for i in items if i["pending"]),
        "summary": feedback_summary(items), "list_html": feedback_list_html(items),
    }
