"""Revise view: one box per paragraph, pre-filled with its current Draft, edit in place.

JL 260922: "我想让每一个 paragraph 是一个方框，然后你把现在的 draft（也就是更新后的
draft）copy 过去 … 这样我就可以在上面改了." So each paragraph is one text box
holding its Draft sentences. JL 261020 took the frame and the row under it away ("i don't
like the box, could you remove it?"; "We might don't need this as well"): the box reads as plain text, a thin
line at its left while you type, and it saves when you leave it (or Cmd+Enter); Esc puts back what it held. The Draft a
reader sees in Reading view is the Draft field of each Outline Bullet, so on
Save the box goes back to the paragraph's Bullets: since JL 261020 the box shows each sentence a row ("we want to
make it each sentence a row"), and a Save cuts it into sentences and gives each Bullet the run of sentences, in
order, that reads most like what it held ("more easier and free style"; `_text_to_bullets`); nothing is dropped.
Since JL 261020 ("could we make each sentences to be auto generate the sentence id as well?") each row shows its
sentence id and carries its Bullet, so a Save knows which sentence each row is (`_rows_to_bullets`); a row the person
makes is a new Bullet with the id before it plus the next free letter (S2 → S2a), its point in `## 1 · Structure`
and its sentence in `## 3 · Draft`; no Bullet is ever renumbered. "+ paragraph" (`add_paragraph`, JL: "How could I
add a new paragraph?") puts an empty paragraph after one, which opens on one empty row. Nothing else in the Outline
moves.

Every Save writes the changed Draft fields back into the selected Outline
Markdown under the page lock, guarded by the Bullet and Draft tokens the page was
rendered with. Records only at the two ends (JL 260928): the first Save on a
paragraph opens its Revise run, `run-revise-<c1-p2>` (one ticket in
`runs/`, which keeps the paragraph's text before the Save as its Before); later
Saves change only the Draft (a Why note is kept in that ticket). `page.py
close-run` writes the Before / After ledger into the run's pass `runs/<run>/passes/` when the person
says close (haipipe-draft-writing (ref/revise.md)). The Runs panel lists the run under Revise edits.

Nothing here touches Page Content; `page.py adopt` copies the Drafts into it when the person asks.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import tempfile

from src.outline_version import plan_dir, latest_outline, record_path, version_tag
from src.run_folders import find_ticket, ticket_dir, ticket_rel, working_dir, write_card
from src.plan_shape import iter_plan_bullets, render_bullet
from src.plan_layout import (SCRATCH_TARGET, _assemble, _sections, from_canonical, is_sectioned,
                             overview_lines, set_overview, to_canonical)
from src.run_lifecycle import find_open, open_run
from live.outline_preview import (bullet_token, draft_path, page_lock, read_drafts,
                                  reader_prose, record_token, write_drafts)

_ADDRESS_RE = re.compile(r"^C\d+\.P\d+$")
_BULLET_RE = re.compile(r"^C\d+\.P\d+\.B\d+$")
MAX_TEXT = 40000


def _now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


_REALIZES_RE = re.compile(r"(?m)^([^\n]*?)<!--\s*realizes:\s*(C\d+\.P\d+\.[BS]\d+)\s*-->\s*$")


def page_realizations(page_src: Path) -> dict[str, str]:
    """Bullet address -> the Page Content sentence(s) that realize it.

    The same reading the Table and Reading views fall back to when an Outline
    Bullet has no Draft field: the box starts from these sentences, and they
    are the ledger's Before when a Save writes the first Draft over them.
    """
    try:
        text = page_src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    found: dict[str, list[str]] = {}
    for match in _REALIZES_RE.finditer(text):
        address = re.sub(r"\.S(\d+)$", r".B\1", match.group(2))
        prose = reader_prose(match.group(1)).strip()
        if prose:
            found.setdefault(address, []).append(prose)
    return {address: " ".join(lines) for address, lines in found.items()}


def _effective(records: dict, realized: dict, address: str) -> str:
    draft = " ".join(((records.get(address) or {}).get("text", "")).split())
    return draft or " ".join(realized.get(address, "").split())


from live.outline_revise_text import (  # noqa: F401  (moved; names kept importable here)
    _PROTECT_RE, _END_RE, split_sentences, box_text, _SID_RE, sentence_id, screen_rows,
    _words, _text_to_bullets, _like, _rows_to_bullets)
from live.outline_revise_view import (  # noqa: F401  (moved; names kept importable here)
    _e, revise_rows_html, assets_html, _ASSETS)


# ------------------------------------------------------------------- saving

def _clean_line(value: str, address: str) -> str:
    text = " ".join(value.split())
    if "<!--" in text or text.startswith(("> Comment ", "## ", "- ")):
        raise ValueError("%s: Draft accepts prose, not hidden address records" % address)
    return text


def _card(number: int, address: str, before: str, after: str, why: str) -> str:
    kind = "first draft" if not before else "deletion" if not after else "wording"
    return (
        "##### R%02d · %s\n\n"
        "###### Target\n%s\n\n"
        "###### Before\n%s\n\n"
        "###### After\n%s\n\n"
        "###### Why\n%s\n\n"
        "###### Decision\naccept\n\n"
        "###### Preference status\nedited directly by the person in Draft Space → Revise\n"
        % (number, kind, address, before or "(no draft)", after or "(removed)", why)
    )


def _point(sentence: str, words: int = 8) -> str:
    """The plan point of a sentence typed in Revise: its first words, for the person to rename."""
    text = re.sub(r"\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", sentence)
    ws = reader_prose(text).split()
    return "[Added] " + " ".join(ws[:words]).rstrip(".,;:") + (" …" if len(ws) > words else "")


def _new_ids(plan_text: str, paragraph: str, inserts: list) -> list:
    """Give each new sentence its Bullet number (the paragraph's highest + 1, never renumbering) and its sentence id:
    the id before it with the next free letter (S2 → S2a, then S2b), page-wide; none on a plan that has none."""
    blocks = list(iter_plan_bullets(plan_text))
    sids = [sentence_id(b["head"]) for b in blocks]
    taken = {s for s in sids if s}
    order = [m.group(1) for m in re.finditer(r"(?m)^### (C\d+\.P\d+)\b", to_canonical(plan_text))]
    earlier = set(order[:order.index(paragraph)]) if paragraph in order else set()
    numbers = [int(b["bullet"][1:]) for b in blocks if b["paragraph"] == paragraph]
    next_b = max(numbers, default=0) + 1
    out = []
    for after, sentences in inserts:
        if after:
            at = next(k for k, b in enumerate(blocks) if b["address"] == after)
            prior = [s for s in sids[:at + 1] if s]
        else:
            prior = [s for b, s in zip(blocks, sids) if s and b["paragraph"] in earlier]
        base = int(re.findall(r"S(\d+)", prior[-1])[-1]) if prior else 0
        made = []
        for sentence in sentences:
            sid = ""
            if taken:
                letter = next(c for c in "abcdefghijklmnopqrstuvwxyz" if "S%d%s" % (base, c) not in taken)
                sid = "S%d%s" % (base, letter)
                taken.add(sid)
            made.append({"address": "%s.B%d" % (paragraph, next_b), "number": next_b, "sid": sid, "text": sentence})
            next_b += 1
        out.append((after, made))
    return out


def _insert_bullets(plan: Path, paragraph: str, inserts: list) -> None:
    """Write the new Bullets into the plan, each run right after the Bullet it follows (None: before the paragraph's
    first): its point in `## 1 · Structure`, its sentence in `## 3 · Draft`."""
    raw = plan.read_text(encoding="utf-8", errors="replace")
    lines = to_canonical(raw).split("\n")
    head, spans, i = None, {}, 0
    while i < len(lines):
        line = lines[i]
        heading = re.match(r"^### (C\d+\.P\d+)\b", line)
        if heading or (line.startswith("## ") and head is not None):
            if head is not None:
                break
            if heading and heading.group(1) == paragraph:
                head = i
            i += 1
            continue
        bullet = re.match(r"^- (?:\[[ xX]\]\s*)?(?:B|S)(\d+)\s*·", line)
        if head is not None and bullet:
            j = i + 1
            while j < len(lines) and lines[j].startswith("  ") and not re.match(r"^- ", lines[j]):
                j += 1
            spans["%s.B%s" % (paragraph, bullet.group(1))] = (i, j)
            i = j
            continue
        i += 1
    if head is None:
        raise ValueError("%s is not in the plan; reload" % paragraph)
    placed = []
    for after, made in inserts:
        block = []
        for bullet in made:
            block += render_bullet("- B%d · " % bullet["number"], bullet["sid"] + " · " if bullet["sid"] else "",
                                   _point(bullet["text"]), [], bullet["text"], "")
        placed.append((spans[after][1] if after else head + 1, block))
    for at, block in sorted(placed, key=lambda x: -x[0]):
        lines[at:at] = block
    _atomic(plan, from_canonical(raw, "\n".join(lines)))


def _atomic(plan: Path, text: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent, prefix=".outline-", delete=False) as tmp:
        tmp.write(text)
        temporary = Path(tmp.name)
    temporary.replace(plan)


def add_paragraph(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """An empty paragraph right after `after`, in the same section (JL 261020: "How could I add a new paragraph?").

    Its address takes the page's highest paragraph number + 1, so no paragraph, Run or Evidence record is renumbered
    (the views number paragraphs by position). Its heading goes into the three sections and the Structure Overview;
    the Revise view opens it on one empty row, and Structure renames it."""
    if read_only:
        return None, "This host is read-only; paragraphs cannot be added"
    after = str(payload.get("after") or "").strip()
    if not _ADDRESS_RE.match(after):
        return None, "after must be a C<n>.P<m> address"
    title = "New paragraph"
    with page_lock(page_src):
        plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        raw = plan.read_text(encoding="utf-8", errors="replace")
        lines = to_canonical(raw).split("\n")
        heads = [(k, m.group(1)) for k, line in enumerate(lines) if (m := re.match(r"^### (C\d+\.P\d+)\b", line))]
        at = next((k for k, address in heads if address == after), None)
        if at is None:
            return None, "%s is not in the plan; reload" % after
        new = "%s.P%d" % (after.split(".")[0], max(int(a.split(".P")[1]) for _k, a in heads) + 1)
        heading = "### %s · %s" % (new, title)
        end = next((k for k in range(at + 1, len(lines)) if lines[k].startswith(("### ", "## "))), len(lines))
        while end > at + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = ["", heading]
        text = from_canonical(raw, "\n".join(lines))
        if is_sectioned(text):
            entries = overview_lines(text)
            k = next((n for n, e in enumerate(entries) if re.match(r"^- %s\b" % re.escape(after), e)), None)
            if k is not None:
                k += 1
                while k < len(entries) and entries[k].strip().startswith("→"):
                    k += 1
                entries[k:k] = ["- %s · %s" % (new, title)]
                text = set_overview(text, entries)
            header, sections, order, tail = _sections(text)
            if "scratch" in sections:
                body = sections["scratch"][1]
                k = next((n for n, line in enumerate(body)
                          if (m := SCRATCH_TARGET.match(line)) and m.group(1) == after), None)
                if k is not None:
                    stop = next((n for n in range(k + 1, len(body)) if body[n].startswith("### ")), len(body))
                    while stop > k + 1 and not body[stop - 1].strip():
                        stop -= 1
                    body[stop:stop] = ["", heading]
                    text = _assemble(header, sections, order, tail)
        _atomic(plan, text)
        log = record_path(plan_dir(page_src.parent), page_src.stem, "log")
        if log.is_file():
            with log.open("a", encoding="utf-8") as fh:
                fh.write("\n### %s · Paragraph added in Draft Space\n- **Headings**: %s after %s\n"
                         % (dt.datetime.now().strftime("%y%m%d %H%M"), new, after))
    return {"paragraph": new, "after": after, "outline": str(plan)}, None


def _display_name(run_id: str) -> str:
    """The name people read, as the Runs panel shows it."""
    try:
        from live.runs_panel import display_name
    except ImportError:
        return run_id
    return display_name(run_id)


def _note_why(folder: Path, run_id: str, paragraph: str, why: str) -> None:
    """Keep the person's reason in the open run's own ticket (not in results/ or the log)."""
    ticket = find_ticket(folder, run_id) or folder / "runs" / (run_id + ".md")
    if ticket.is_file():
        text = ticket.read_text(encoding="utf-8")
        if "\n## Why\n" not in text:
            text = text.rstrip("\n") + "\n\n## Why\n"
        ticket.write_text(text.rstrip("\n") + "\n- %s: %s\n" % (paragraph, why), encoding="utf-8")


def _screen(blocks: dict, paragraph: str, fresh: dict, realized: dict) -> tuple[list[str], list[dict]]:
    """-> (the paragraph's Bullet addresses in plan order, the rows the editor shows)."""
    addresses = [a for a in blocks if a.startswith(paragraph + ".")]
    return addresses, screen_rows([{"address": a, "bullet_id": blocks[a]["bullet"], "sid": sentence_id(blocks[a]["head"]),
                                    "text": _effective(fresh, realized, a)} for a in addresses])


def _id_clash(text: str) -> str:
    """Why a save must wait, or "": a sentence in `## 3 · Draft` whose id differs from its point's (the same B) in
    `## 1 · Structure`. A save writes every §3 id from §1 by B, so a §1 whose B numbers were shifted would silently
    relabel the text (t01, 261020: a point put in after S2 took B3, and the save made S3 into S2a)."""
    if not is_sectioned(text):
        return ""
    ids, part, para = {"1": {}, "3": {}}, None, None
    for line in text.splitlines():
        m = re.match(r"^## (\d+)\s*·", line)
        h = re.match(r"^### (C\d+\.P\d+)\b", line)
        b = re.match(r"^- B(\d+) · (S\d+[a-z]*) · ", line)
        if m:
            part = m.group(1)
        elif h:
            para = h.group(1)
        elif b and para and part in ids:
            ids[part][(para, b.group(1))] = b.group(2)
    for (para, n), sid in ids["3"].items():
        planned = ids["1"].get((para, n))
        if planned and planned != sid:
            return ("Not saved: %s.B%s is %s in the plan but %s in the text; the plan's B numbers shifted, "
                    "fix them first" % (para, n, planned, sid))
    return ""


def save_revise(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """Map the typed rows onto the paragraph's Bullets, add a Bullet per new sentence, save, extend the Revise Run.

    `rows` ([{b, text}], each row naming the Bullet it was drawn from) is what the editor sends; without it the
    `text` alone is matched to the Bullets by likeness and no Bullet is added."""
    if read_only:
        return None, "This host is read-only; Revise saves are disabled"
    paragraph = str(payload.get("paragraph") or "").strip()
    if not _ADDRESS_RE.match(paragraph):
        return None, "paragraph must be a C<n>.P<m> address"
    text = payload.get("text")
    if not isinstance(text, str) or len(text) > MAX_TEXT:
        return None, "text must be a string of at most 40,000 characters"
    rows = payload.get("rows")
    if rows is not None and not (isinstance(rows, list) and all(
            isinstance(r, dict) and isinstance(r.get("text", ""), str) and isinstance(r.get("b", ""), str)
            for r in rows) and sum(len(r.get("text", "")) for r in rows) <= MAX_TEXT):
        return None, "rows must list the typed rows, each {b, text}, at most 40,000 characters"
    listed = payload.get("bullets")
    if not isinstance(listed, list) or not all(isinstance(b, dict) for b in listed) or (not listed and rows is None):
        return None, "bullets must list the paragraph's Bullets as rendered"
    why = str(payload.get("why") or "").strip()
    if len(why) > 500 or "<!--" in why:
        return None, "why must be one short line"
    addresses = [str(b.get("address") or "").strip() for b in listed]
    if not all(_BULLET_RE.match(a) and a.startswith(paragraph + ".") for a in addresses):
        return None, "every listed Bullet must sit inside %s" % paragraph
    with page_lock(page_src):
        plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        plan_text = plan.read_text(encoding="utf-8", errors="replace")
        clash = _id_clash(plan_text)
        if clash:
            return None, clash
        blocks = {b["address"]: b for b in iter_plan_bullets(plan_text)}
        current = [a for a in blocks if a.startswith(paragraph + ".")]
        if current != addresses:
            return None, "%s's points changed since this page was opened; reload before saving" % paragraph
        if not addresses and not re.search(r"(?m)^### %s\b" % re.escape(paragraph), to_canonical(plan_text)):
            return None, "%s is not in the plan; reload" % paragraph
        records = read_drafts(page_src)
        realized = page_realizations(page_src)
        for item in listed:
            address = str(item.get("address"))
            if str(item.get("bullet") or "") != bullet_token(blocks[address]):
                return None, "Point %s changed; reload and review before saving" % address
            if str(item.get("record") or "") != record_token(records.get(address)):
                return None, "Draft %s changed in another editor; reload before saving" % address
        before = [_effective(records, realized, a) for a in addresses]
        try:
            if rows is None:
                mapped, inserts = _text_to_bullets(text, addresses, before), []
            else:
                mapped, inserts = _rows_to_bullets(rows, addresses, before)
            mapped = {a: _clean_line(t, a) for a, t in mapped.items()}
            inserts = [(after, [_clean_line(s, paragraph) for s in sentences]) for after, sentences in inserts]
        except ValueError as exc:
            return None, str(exc)
        changed = []
        for address, old in zip(addresses, before):
            if old == mapped[address]:
                continue
            changed.append({"address": address, "before": old, "after": mapped[address]})
        if not changed and not inserts:
            fresh = read_drafts(page_src)
            shown = _screen(blocks, paragraph, fresh, realized)[1]
            return {"paragraph": paragraph, "changed": [], "run": "", "step": "",
                    "text": "\n".join(r["text"] for r in shown), "rows": shown,
                    "bullets": [{"address": a, "bullet": bullet_token(blocks[a]),
                                 "record": record_token(fresh.get(a))} for a in addresses],
                    "message": "nothing changed"}, None
        # The paragraph as it reads before this Save: a new Revise run keeps it as its Before.
        before_text = "\n".join("%s · %s" % (a, b or "") for a, b in zip(addresses, before))
        if changed:
            for item in changed:
                records[item["address"]] = {**records.get(item["address"], {}),
                                            "plan": version_tag(plan),
                                            "text": item["after"]}
            write_drafts(page_src, records)
        if inserts:
            made = _new_ids(plan.read_text(encoding="utf-8", errors="replace"), paragraph, inserts)
            try:
                _insert_bullets(plan, paragraph, made)
            except ValueError as exc:
                return None, str(exc)
            changed += [{"address": b["address"], "before": "", "after": b["text"]} for _a, bs in made for b in bs]
        fresh = read_drafts(page_src)
        blocks = {b["address"]: b for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace"))}
        addresses, shown = _screen(blocks, paragraph, fresh, realized)
        # Records only at the two ends (JL 260928): the first Save opens the run (its ticket
        # keeps the Before); later Saves change only the Draft; close-run writes the run's pass.
        run_id = find_open(page_src.parent, "revise", paragraph)
        if not run_id:
            run_id = open_run(page_src, "revise", target=paragraph, goal=why,
                              by="person · Draft Space › Revise", before=before_text)["run"]
        elif why:
            _note_why(page_src.parent, run_id, paragraph, why)
    return {
        "paragraph": paragraph,
        "run": run_id, "name": run_id, "step": "", "summary": "",
        "result": "", "outline": str(draft_path(page_src)),
        "version": version_tag(plan),
        "text": "\n".join(r["text"] for r in shown), "rows": shown,
        "bullets": [{"address": a, "bullet": bullet_token(blocks[a]), "record": record_token(fresh.get(a))}
                    for a in addresses],
        "changed": [{"address": c["address"], "text": c["after"]} for c in changed],
    }, None
