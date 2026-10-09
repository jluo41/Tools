"""Open and close a Page Run (JL 260928: records at the two ends, only text between).

    page.py open-run <page> --kind section --slug readability-cleanup [--target C1] [--goal …]
        writes ONE ticket, runs/<name>.md, status open. Nothing else.
    … while the run is open, only the Page's text changes (Draft, Evidence Markdown, Page) …
    page.py close-run <page> <run> [--summary …]
        writes the run's next pass runs/<name>/passes/pNN-<MMDD>/ (runtime.yaml, and for a
        Revise run its Before / After ledger v001.md; an older flat run writes results/<name>/),
        marks the ticket closed, updates the card run.yaml, and adds one line to the Page's log.

A Revise run opened by the workbench keeps the paragraph's text at open in its
ticket (`## Before`), so the ledger compares that with the text at close.
"""
from __future__ import annotations

import datetime as dt
import difflib
import re
from pathlib import Path

from . import run_names
from .outline_version import latest_outline, plan_dir, record_path
from .plan_shape import iter_plan_bullets
from .run_folders import find_ticket, is_folder_run, ticket_dir, working_dir, write_card

# The skills each kind uses; the Runs panel shows the same (run-cards.md `🧩 SKILL`).
SKILLS = {
    "context": ["haipipe-page-context"], "structure": ["haipipe-page-structure"],
    "scratch": ["haipipe-page-scratch"], "section": ["haipipe-page-writing", "haipipe-writing"],
    "paragraph": ["haipipe-page-writing", "haipipe-writing"], "revise": ["haipipe-page-revise"],
    "auto-write": ["haipipe-page-writing", "haipipe-writing"], "evidence-embed": ["haipipe-page-evidence"],
    "citation": ["haipipe-page-evidence"], "value": ["haipipe-page-evidence"],
    "display": ["haipipe-page-evidence", "haipipe-display"], "check": ["haipipe-page-check"],
}
OPERATION = {"citation": "evidence-item", "value": "evidence-item", "display": "evidence-item",
             "check": "check", "context": "context"}
_FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def _page(target) -> tuple[Path, str]:
    target = Path(target).resolve()          # `.` must still name the Page folder (JL 261004)
    if target.is_file():
        return target.parent, target.stem
    return target, target.name


def _now() -> dt.datetime:
    return dt.datetime.now().astimezone().replace(microsecond=0)


def taken_names(folder: Path) -> set[str]:
    names = set()
    runs, results = folder / "runs", folder / "results"
    if runs.is_dir():
        names |= {p.stem for p in runs.rglob("*") if p.is_file()}
        names |= {p.name for p in runs.iterdir() if p.is_dir()}      # a run's own folder (0.122)
    if results.is_dir():
        names |= {p.name for p in results.iterdir() if p.is_dir()}
    return names


def front(text: str) -> dict:
    found = _FRONT.match(text or "")
    fields = {}
    for line in (found.group(1) if found else "").splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def _set_front(text: str, **values) -> str:
    found = _FRONT.match(text)
    lines = found.group(1).splitlines() if found else []
    keys = [line.partition(":")[0].strip() for line in lines]
    for key, value in values.items():
        line = "%s: %s" % (key, value)
        if key in keys:
            lines[keys.index(key)] = line
        else:
            lines.append(line)
    body = text[found.end():] if found else text
    return "---\n%s\n---\n%s" % ("\n".join(lines), body)


def find_open(folder: Path, kind: str, target: str) -> str | None:
    """The open run of this kind for this target, if any (newest first)."""
    runs = folder / "runs"
    found = (list(runs.glob("run-%s-*.md" % kind)) + [t for t in runs.glob("run-%s-*/run-%s-*.md" % (kind, kind))
                                                     if t.parent.name == t.stem]) if runs.is_dir() else []
    for ticket in sorted(found, key=lambda t: t.stem, reverse=True):
        fields = front(ticket.read_text(encoding="utf-8", errors="replace"))
        if fields.get("status", "open") == "open" and fields.get("target", "") == target:
            return ticket.stem
    return None


def open_run(page, kind: str, slug: str = "", *, target: str = "", goal: str = "", by: str = "",
             before: str | None = None, day=None) -> dict:
    """Write the ticket of a new run; return {run, ticket}."""
    folder, stem = _page(page)
    if kind not in run_names.KINDS:
        raise ValueError("kind must be one of: %s" % ", ".join(run_names.KINDS))
    slug = slug or (run_names.target_slug(target) if target else run_names.slugify(goal))
    if not slug:
        raise ValueError("give --slug, --target or --goal so the run has a readable name")
    name = run_names.mint(kind, slug, day=day, taken=taken_names(folder))
    ticket = ticket_dir(folder, name) / (name + ".md")
    ticket.parent.mkdir(parents=True, exist_ok=True)
    now = _now()
    fields = {"run": name, "kind": kind, "family": "page",
              "operation": OPERATION.get(kind, "interactive-writing"),
              "target": target, "goal": goal.replace("\n", " "),
              "skills": " · ".join(SKILLS.get(kind, [])),
              "status": "open", "started_at": now.isoformat(), "started_by": by}
    if kind == "scratch":
        fields["mode"] = "scratch"
    elif kind == "revise":
        fields["mode"] = "revise"
    lines = ["---"] + ["%s: %s" % (k, v) for k, v in fields.items() if v != ""] + ["---", "",
             "# %s" % name, ""]
    if goal:
        lines += ["- Goal: %s" % goal]
    if target:
        lines += ["- Target: %s" % target]
    lines += ["- While open, only the Page's text changes; its pass (runs/%s/passes/) and the log "
              "are written when it closes." % name]
    if before is None and kind == "revise" and target:
        # Opened from the command line: snapshot the target's Drafts now, so close-run can
        # count what the Run changed (JL 261004: a CLI Revise used to record 0 changes).
        before = "\n".join("%s · %s" % (a, " ".join(d.split()))
                           for a, d in paragraph_drafts(folder, stem, target).items())
    if before is not None:
        lines += ["", "## Before", "", "```text", before.rstrip(), "```"]
    ticket.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if ticket.parent.name == name:                 # one folder per Run: its card opens with it
        write_card(folder, name, type=kind, target=target or None, skill=" · ".join(SKILLS.get(kind, [])) or None,
                   agent=by or None, status="running", writes=[], feeds=[])
    return {"run": name, "ticket": ticket.relative_to(folder).as_posix()}


def paragraph_drafts(folder: Path, stem: str, paragraph: str) -> dict[str, str]:
    """{`C1.P2.B1`: its Draft sentence} for the target, from the current plan. The target
    is a paragraph (`C1.P2`), a whole division (`C1`) or one Bullet (`C1.P2.B1`); a
    division target used to match nothing, so its Run counted 0 changes (JL 261004)."""
    plan = latest_outline(plan_dir(folder), stem)
    if plan is None:
        return {}
    return {b["address"]: str(b.get("draft") or "").strip()
            for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace"))
            if paragraph in {b.get("paragraph"), b.get("division"), b.get("address")}}


def _before(ticket_text: str) -> dict[str, str]:
    """The `## Before` block of a Revise ticket: `C1.P2.B1 · sentence` lines."""
    found = re.search(r"(?ms)^## Before\s*\n+```text\n(.*?)\n```", ticket_text)
    out = {}
    for line in (found.group(1).splitlines() if found else []):
        address, sep, text = line.partition(" · ")
        if sep and re.fullmatch(r"C\d+\.P\d+\.B\d+", address.strip()):
            out[address.strip()] = text.strip()
    return out


def _whys(ticket_text: str, goal: str) -> str:
    notes = re.findall(r"(?m)^- C\d+\.P\d+: (.+)$", ticket_text.split("\n## Why\n", 1)[1]) \
        if "\n## Why\n" in ticket_text else []
    return "; ".join([goal] + notes if goal else notes) or "Edited directly in Draft Space → Revise."


def _card(number: int, address: str, before: str, after: str, why: str) -> str:
    kind = "first draft" if not before else "deletion" if not after else "wording"
    return ("##### R%02d · %s\n\n###### Target\n%s\n\n###### Before\n%s\n\n###### After\n%s\n\n"
            "###### Why\n%s\n\n###### Decision\naccept\n\n###### Preference status\n"
            "edited directly by the person in Draft Space → Revise\n"
            % (number, kind, address, before or "(no draft)", after or "(removed)", why))


def _ledger(run: str, target: str, before: dict, after: dict, why: str, opened: str, closed: str) -> tuple[str, int]:
    """The run's change ledger, in the Step format the All-runs view draws as red/green cards."""
    addresses = sorted(set(before) | set(after), key=lambda a: [int(n) for n in re.findall(r"\d+", a)])
    flat = lambda s: " ".join(s.split())       # a multi-line Draft (a table) compares as one line
    changes = [(a, before.get(a, ""), after.get(a, "")) for a in addresses
               if flat(before.get(a, "")) != flat(after.get(a, ""))]
    cards = "".join(_card(i, a, b, c, why) for i, (a, b, c) in enumerate(changes, 1))
    text = ("Run: %s\nVersion: v001\nState: closed\nTarget: %s\n\n## Step s001\n\n"
            "### Human feedback\nDirect edits of %s in Draft Space → Revise, %s to %s.\n\n"
            "### Saved result\n\n#### Inputs\n- Before: the text when the run opened, kept in its ticket (the Page's own sentence where no Draft existed)\n"
            "- After: the Draft at close\n- Target: %s\n\n#### Summary\n%d sentence%s changed in %s.\n\n"
            "#### Track changes\n\n%s"
            % (run, target, target, opened[:16], closed[:16], target, len(changes),
               "" if len(changes) == 1 else "s", target, cards))
    return text, len(changes)


def _log(folder: Path, stem: str, line: str, receipt: str) -> None:
    log = Path(record_path(plan_dir(folder), stem, "log"))
    entry = "### %s · %s\n  Receipt: %s\n\n" % (dt.datetime.now().strftime("%y%m%d %H%M"), line, receipt)
    if log.is_file():
        text = log.read_text(encoding="utf-8")
        first = re.search(r"(?m)^### ", text)
        at = first.start() if first else len(text)
        text = text[:at] + entry + text[at:]
    else:
        log.parent.mkdir(parents=True, exist_ok=True)
        text = "# %s · log\npage: %s\nkind: log · authored · dated records · append-only · newest-first\n\n%s" % (
            stem, stem, entry)
    log.write_text(text, encoding="utf-8")


def close_run(page, run: str, *, summary: str = "", by: str = "", why: str = "") -> dict:
    """Write the run's results/ and log line; mark its ticket closed."""
    folder, stem = _page(page)
    ticket = find_ticket(folder, run)
    if ticket is None:
        raise ValueError("no ticket for %s on this Page (runs/%s/%s.md or runs/%s.md)" % (run, run, run, run))
    text = ticket.read_text(encoding="utf-8", errors="replace")
    fields = front(text)
    if fields.get("status", "open") not in {"open", "running"}:
        raise ValueError("%s is not open (status: %s)" % (run, fields.get("status")))
    kind = fields.get("kind") or run_names.kind_of(run) or ""
    target = fields.get("target", "")
    now = _now()
    folder_run = is_folder_run(folder, run)
    # One folder per Run: close finishes the open pass (an interactive run wrote into it while
    # open), else makes the next one; an older flat run keeps results/<name>/.
    result = working_dir(folder, run, day=now.strftime("%m%d"))
    result_rel = result.relative_to(folder).as_posix()
    changes = None
    if kind == "revise":
        ledger, changes = _ledger(run, target, _before(text), paragraph_drafts(folder, stem, target),
                                  why or _whys(text, fields.get("goal", "")),
                                  fields.get("started_at", ""), now.isoformat())
        (result / "v001.md").write_text(ledger.rstrip("\n") + "\n", encoding="utf-8")
        summary = summary or "%d change%s to %s" % (changes, "" if changes == 1 else "s", target)
    journal = result / "v001.md"
    if journal.is_file() and "## Version closure" not in journal.read_text(encoding="utf-8"):
        journal.write_text(journal.read_text(encoding="utf-8").rstrip("\n") +
                           "\n\n## Version closure\n\n### Human close\n\n%s closed the run on %s.\n"
                           % (by or fields.get("started_by", "") or "The person", now.date().isoformat()),
                           encoding="utf-8")
    if journal.is_file() and not (result / "working.md").is_file():
        (result / "working.md").write_text("# %s\n\n- State: closed.\n- Target: %s.\n- Summary: %s\n"
                                           % (run, target or "the Page", summary or "closed"), encoding="utf-8")
    runtime = ["run: %s" % run, "kind: %s" % kind, "family: page",
               "operation: %s" % fields.get("operation", ""), "target: %s" % target,
               "mode: %s" % fields.get("mode", ""), "version: v001", "step: s001",
               "interaction: %s" % ("human-revise" if kind == "revise" else "human-feedback"),
               "version_file: %s/v001.md" % result_rel,
               "ticket: %s" % ticket.relative_to(folder).as_posix(), "status: complete",
               "started_at: '%s'" % fields.get("started_at", ""), "closed_at: '%s'" % now.isoformat(),
               "closed_by: %s" % (by or fields.get("started_by", "")),
               "skills: %s" % fields.get("skills", ""), "summary: %s" % (summary or "closed")]
    (result / "runtime.yaml").write_text("\n".join(runtime) + "\n", encoding="utf-8")
    ticket.write_text(_set_front(text, status="closed", closed_at=now.isoformat()), encoding="utf-8")
    if folder_run:
        write_card(folder, run, status="done")
    _log(folder, stem, "%s closed: %s" % (run, summary or "closed"), "%s/" % result_rel)
    return {"run": run, "result": "%s/" % result_rel, "changes": changes, "summary": summary}
