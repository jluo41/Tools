"""A Design item's Runs drawn: the run table rows, its checks and draft text, the
buttons its state licenses, and the short run list on a card.

Split out of design_page.py; design_page.py re-exports every name here."""
from __future__ import annotations

import re
from pathlib import Path

from live.design import _STEP, _escape, _held_at, _read, _relative_href, _stale_names


def _href(root: Path, path: Path | None, label: str) -> str:
    if path is None:
        return f"<code>{_escape(label)}</code>"
    href = _relative_href(root, path)
    if not href:
        return f"<code>{_escape(label)}</code>"
    return f'<a href="{_escape(href)}"><code>{_escape(label)}</code></a>'


def _whole_word(word: str, flags: int = 0) -> re.Pattern:
    """The word standing alone, never a piece of a hyphenated compound."""
    return re.compile(rf"(?<![\w-]){word}(?![\w-])", flags)


_CONTRACT_WORDS = ((_whole_word("candidates", re.I), "drafts"),
                   (_whole_word("candidate", re.I), "draft"),
                   (_whole_word("Tickets"), "run records"),
                   (_whole_word("Ticket"), "run record"))


def plain_words(recorded: str) -> str:
    """Read a recorded sentence in the reader's words.

    A Run's target, written when the files said `candidate`, keeps its own
    bytes; the surface says `draft`.
    """
    for pattern, word in _CONTRACT_WORDS:
        recorded = pattern.sub(word, recorded or "")
    return recorded


def _rule_words(run: dict, acceptance: list[str]) -> dict[str, str]:
    """criterion id -> the rule as a reader wrote it (rNN -> rule N), else the criterion in words."""
    words = {}
    for c in run["criteria"]:
        cid = str(c.get("id"))
        hit = re.match(r"^r(\d{2})[a-z]?$", cid)
        n = int(hit.group(1)) if hit else 0
        words[cid] = acceptance[n - 1] if hit and 0 < n <= len(acceptance) else _criterion_words(c)
    return words


def _checks_details(run: dict, acceptance: list[str] | None = None) -> str:
    if not run["checks"]:
        return ""
    words = _rule_words(run, acceptance or [])
    failed = any(c.get("status") != "pass" for c in run["checks"])
    rows = "".join(
        f'<tr><td>{_escape(words.get(str(c.get("criterion")), c.get("criterion")))}</td>'
        f'<td class="{"ok" if c.get("status") == "pass" else "bad"}">{_escape(c.get("status"))}</td>'
        f'<td class=mut>{_escape(c.get("evidence"))}</td></tr>'
        for c in run["checks"])
    return (f'<details{" open" if failed else ""}><summary>checks {run["checks_passed"]}/{len(run["checks"])}</summary>'
            f'<table><tr><th>rule</th><th>status</th><th>why</th></tr>{rows}</table></details>')


def _artifact_details(run: dict) -> str:
    if not run["artifacts"]:
        return ""
    art = run["artifacts"][0]
    return f'<details><summary>draft text</summary><pre class=text>{_escape(art["text"])}</pre></details>'


def _revise_of(run: dict) -> tuple[str, str]:
    """(base run, feedback text) when a Generate revises an earlier draft."""
    base = next((i for i in run["inputs"] if i["role"] == "base"), None)
    note = next((i for i in run["inputs"] if i["role"] == "feedback"), None)
    text = _read(note["file"]).split("\n\n", 2)[-1].strip() if note and note["file"].is_file() else ""
    return (base["run_id"] if base else "", text)


def run_short(run_id: str) -> str:
    """A run said briefly: `rd13` for an old name, `verify 09-18` for a current one."""
    hit = re.match(r"^run-design-([a-z]+)-(\d{2})(\d{2})-", str(run_id))
    return f"{hit.group(1)} {hit.group(2)}-{hit.group(3)}" if hit else str(run_id).split("_")[0]


def _run_rows(root: Path, runs: list[dict], acceptance: list[str] | None = None) -> str:
    rows = []
    for run in runs:
        status = run["status"]
        status_cls = ("bad" if status in ("failed", "blocked") or (run["kind"] == "verify" and run["verdict"] == "fail")
                      else "mut" if status == "superseded" else ("ok" if status == "complete" else ""))
        status_text = "planned · queued for agent" if status == "planned" and run["mode"] == "agent" else status
        # Explain historical outcomes without changing the recorded Run identity.
        outcome = {"adopt": "ready", "decline": "not delivered"}.get(run["outcome"], run["outcome"])
        if run["kind"] in ("generate", "verify") and run["checks"]:
            outcome = f'{run["verdict"] or status} {run["checks_passed"]}/{len(run["checks"])}'
        next_step = {"adopt": "delivery"}.get(run["route"], run["route"] or "")
        if run["status"] == "complete" and run["kind"] == "adopt" and run["outcome"] in ("adopt", "decline"):
            next_step = "closed"
        detail = _checks_details(run, acceptance) + _artifact_details(run)
        base, why = _revise_of(run) if run["kind"] == "generate" else ("", "")
        if why:
            detail = f'<div class=mut>feedback: “{_escape(why)}”</div>' + detail
        if run["failure"]:
            detail = f'<div class={"mut" if status == "superseded" else "bad"}>{_escape(run["failure"])}</div>' + detail
        if run["words"] and run["kind"] != "adopt":
            detail = f'<div class=mut>“{_escape(run["words"])}”</div>' + detail
        rows.append(
            f'<tr><td>{_href(root, run["ticket_path"], run["id"])}</td>'
            f'<td>{_escape(run["step"])}{(" · revise of " + _escape(run_short(base))) if base else ""}'
            f'<div class=mut><code>Design.{_escape(run["kind"])}</code> · {_escape(plain_words(run["target"]))}</div></td>'
            f'<td>{_escape(run["actor"])} <span class=mut>{_escape(run["mode"])}</span></td>'
            f'<td class=mut>{_escape(run["finished"] or run["started"] or "—")}</td>'
            f'<td class="{status_cls}">{_escape(status_text)}</td><td class="{"bad" if run["verdict"] == "fail" else ""}">{_escape(outcome)}</td>'
            f'<td class=mut>{_escape(next_step)}</td></tr>'
            + (f'<tr><td></td><td colspan=6>{detail}</td></tr>' if detail else ""))
    return "".join(rows)


_CRITERION_WORDS = {"max_chars": "≤ {v} characters", "contains": "contains '{v}'", "excludes": "does not contain '{v}'",
                    "starts_with": "starts with '{v}'", "ends_with": "ends with '{v}'"}


def _criterion_words(c: dict) -> str:
    """One compiled criterion as a reader says it."""
    form = _CRITERION_WORDS.get(str(c.get("kind")))
    return form.format(v=c.get("value")) if form else str(c.get("description") or c.get("id") or "")


def _actions(item: dict, human: str) -> tuple[str, str]:
    """The buttons an item's state licenses, and the line that folds them.

    A form that asks for a name, words, or feedback is folded under its line
    (closed by default); a single agent-queue button has no line and stays in view.
    """
    state = item["state"]
    person = f'<input class=name name=actor placeholder="your name" value="{_escape(human if human != "person" else "")}">'
    words = '<input class=words name=words placeholder="your words, one sentence (kept on record)">'
    feedback = '<input class=words name=feedback placeholder="what to change (feedback for the revise Run)">'
    held_at = _held_at(item)
    if state in ("not commissioned", "commission open") or held_at == "commission":
        return (f'{person}{words}<button class=do data-action=commission-release>Release commission</button>'
                f'<button class="do bad" data-action=commission-hold>Hold</button>'), "Release or hold the commission"
    if state in ("commissioned", "revise requested"):
        return '<button class=do data-action=queue-generate>Queue Generate · agent</button>', ""
    if state in ("generated", "verify invalid"):
        return '<button class=do data-action=queue-verify>Queue Verify · independent agent</button>', ""
    if state == "queued run out of date":
        return ('<button class=do data-action=requeue>Queue again with today\'s insight files</button>'
                f'<div class=mut>changed since it was queued: {_escape(", ".join(_stale_names(item)))}</div>'), ""
    if state in ("generate failed", "verify failed"):
        return f'{feedback}<button class=do data-action=queue-revise>Queue revise · agent</button>', "Queue a revise, with feedback"
    if state == "ready":
        return '<span class="ok">ready for Delivery</span>', ""
    if state == "blocked":
        return (f'<span class=bad>{_escape(item["waiting"])}</span>'
                '<span class=mut>Repair the named inputs or records through the Design workflow; '
                'the caller must resolve the blocked Run before work resumes.</span>'), ""
    if state == "records invalid":
        return (f'<span class=bad>{_escape(item["waiting"])}</span>'
                '<span class=mut>Inspect the records check before handing off this design. '
                'Preserve the recorded versions; changed content needs a new Run.</span>'), ""
    if state == "legacy hold":
        return '<span class=mut>Historical decision; register a new Design Item to continue.</span>', ""
    if state in ("generate queued", "verify queued", "generating", "verifying"):
        return '<span class=mut>queued for the agent</span>', ""
    return "", ""


def _design_runs_list(item: dict) -> str:
    """This design's own runs as a short list that fits the column: the step,
    its outcome, who and when, the person's words when they gave a decision; the run id
    small underneath. The insight board's runs sit behind its pages, not here."""
    rows = []
    for r in item["runs"]:
        bad = r["status"] in ("failed", "blocked")
        outcome = r["outcome"] or ("planned · queued for agent" if r["status"] == "planned" and r["mode"] == "agent"
                                   else r["status"])
        if r["checks"]:
            outcome += f' {r["checks_passed"]}/{len(r["checks"])}'
        when = r["finished"] or r["started"] or ""
        words = f'<div class=said>“{_escape(r["words"])}”</div>' if r["words"] else ""
        rows.append(f'<li{" class=old" if r["status"] == "superseded" else ""}><div class=rl>'
                    f'<b>{_escape(_STEP.get(r["kind"], r["kind"]))}</b>'
                    f'<span class="{"bad" if bad else "ok" if r["status"] == "complete" else "mut"}">{_escape(outcome)}</span>'
                    f'<span class=mut>{_escape(r["actor"])} · {_escape(when)}</span></div>'
                    f'{words}<code class=rid>{_escape(r["id"])}</code></li>')
    return f'<ul class=runs>{"".join(rows)}</ul>' if rows else ""
