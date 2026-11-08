"""The cowork theme's own parts on the shared work page (focus_page.page_module finds this module as live.cowork_focus;
b13, the plan of 261106). A cowork Block coordinates one topic with people; its Jobs have no Tasks, so the shared
Status (Tasks and Runs) and Findings (Run headlines, Values) say little. This adds what a cowork page is about:

  Findings  👥 People      a side tab per person or role, from j00_people's table (who they are, what they own, how
                           to reach them); a Job shows the ones its files name
            ✉️ Messages    side tabs Emails · Meetings · Drafts; a draft not sent yet is its waiting line
            ⏳ Next move   the Block's open Jobs, a side tab each: who has the move and since when, what is next
  Status    a Block: its Jobs by state, waiting on us · waiting on them · on hold · done, a numbered bar each
            a Job: who it waits on and for how long, its timeline (dated entries, emails, meetings, sends), its steps
            a Task (a document written in rounds): each round, who has the move, its Runs
  Delivery  each message the page sent, its draft, its copy page and its attachments, a side tab each

[(title, word, html, waits)] each: a title plain words with its emoji, a word the closed bar's state, a waits line
the one thing that waits on the person ("" when none). Read-only: nothing here writes.
"""
from __future__ import annotations

import re
from pathlib import Path

from live.coworkboard import DONE, REFERENCE, jobs, notes, people_page, steps
from live.frame import _file_url, esc, pop, reader
from live.ui_parts import _kv, _side_tabs

HOLD = "⏸"
_NOBODY = ("us", "nobody", "")
_ROUND_RUN = re.compile(r"^run-(?:write|revise|draft|edit)-")
_HEAD = re.compile(r"(?m)^(To|Cc|Subject|From|How):\s*(.+?)\s*$")

VIEW_SKILLS = {"mindmap": (("haipipe-mindmap", "draws and refreshes this map"),),
               "standing": (("haipipe-cowork", "keeps each Job's state, who has the move and since when"),
                            ("haipipe-job", "keeps a Job's face and its Tasks in order")),
               "findings": (("haipipe-cowork", "keeps the people, the emails, the meetings and the next move"),
                            ("haipipe-report", "writes each Question's answer for you to agree"),
                            ("haipipe-delivery", "keeps each message sent in delivery/"),
                            ("haipipe-draft", "writes a document in rounds, as a Task"))}

# a theme's own words for a view at a level (focus_page reads CAPTIONS, 261108): a cowork Job has no Tasks, so the
# shared "Where its Tasks stand" reads wrong
CAPTIONS = {("Block", "standing"): "Each Job by who has the move: us, them, or done; then the Studio topics.",
            ("Job", "standing"): "Who has the move, since when, and what happened so far.",
            ("Job", "mindmap"): "This Job as a map: what happened, who has the move, and what is left.",
            ("Task", "standing"): "Each round of the document, who has the move now, and its Runs."}

CSS = """<style>
.cw-rows{list-style:none;margin:0;padding:0;font-size:14px}.cw-rows li{display:flex;flex-wrap:wrap;align-items:baseline;
gap:2px 10px;padding:6px 2px;border-bottom:1px solid var(--line)}.cw-rows li:last-child{border-bottom:0}
.cw-rows .d{flex:none;min-width:84px;font-size:12.5px;color:var(--muted);font-variant-numeric:tabular-nums}
.cw-rows .t{flex:1 1 220px;min-width:0;overflow-wrap:anywhere}.cw-rows small{margin-left:auto;font-size:12px;color:var(--muted)}
.cw-rows .you{color:light-dark(#b35c00,#ffc078)}.cw-next{margin:2px 0 10px;font-size:15px;line-height:1.5}
.cw-sub{margin:14px 0 4px;font-size:13px;font-weight:600}.cw-verbs{margin:8px 0 0;font-size:13px}
@media(max-width:600px){.cw-rows small{margin-left:0;flex-basis:100%}}
</style>"""


# ── what is on disk ─────────────────────────────────────────────────────────────────────────────────────────────
def block_of(folder: Path, level: str) -> Path:
    return {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)


def _short(title: str) -> str:
    """A face's title without its `jNN ·` / `tNN ·` label."""
    return re.sub(r"^[a-z]\d+\s*[·:-]\s*", "", title or "").strip()


def _ancestry(rel: Path) -> list:
    """j02_x/t01_y -> [j02_x, j02_x/t01_y]: a Job, then its Task."""
    return [Path(*rel.parts[:k]) for k in range(1, len(rel.parts) + 1)]


def _title_of(folder: Path) -> str:
    """A Job's or Task's title in words, from its face's first heading; its folder name when it has none."""
    face = folder / f"{folder.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    return _short((re.search(r"(?m)^#\s+(.+)$", text) or [None, folder.name])[1].strip())


def _jobs(block: Path, root: Path) -> list:
    rows, _ = jobs(block, root)
    for j in rows:
        j["short"] = _short(j["title"])
        j["ours"] = j["open"] and j["waiting"].strip().lower() == "us"
        j["theirs"] = j["open"] and j["waiting"].strip().lower() not in _NOBODY
    return rows


def _days(n) -> str:
    return "" if n is None else "today" if n == 0 else f"{n} day" if n == 1 else f"{n} days"


def _state_group(j: dict) -> str:
    if j["state"].startswith(DONE):
        return "done"
    if j["state"].startswith(REFERENCE):
        return "reference"
    if j["state"].startswith(HOLD):
        return "hold"
    return "ours" if j["ours"] else "theirs" if j["theirs"] else "open"


def _items(job: Path, block: Path, root: Path) -> list:
    """A Job's dated items, newest first (cowork_theme.timeline_items), its Timeline.md lines called notes; a note on a
    day that already has an email, a meeting or a send is that item's twin and is left out (b13 review r01)."""
    from live.cowork_theme import timeline_items
    items = timeline_items(job, block, root, notes(job / "emails", block, root, job.name),
                           notes(job / "meetings", block, root, job.name))
    dated = {d for d, k, _ in items if k != "entry" and d}
    return [(d, "note" if k == "entry" else "sent" if k == "delivery" else k, h) for d, k, h in items
            if not (k == "entry" and d in dated)]


def _job_url(job: Path, root: Path) -> str:
    from live import focus_page as F
    return F.page_url(job, root)


def _job_link(job: Path, root: Path, title: str) -> str:
    return pop(_job_url(job, root), job.name, title)


def people(block: Path) -> list:
    """[(name, {column: cell})] from the first table of the people page (j00_people.md, an older PEOPLE.md); a row
    still to fill ("(to add)") is left out."""
    page = people_page(block)
    if not page.is_file():
        return []
    heads, out = [], []
    for line in page.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.lstrip().startswith("|"):
            if heads:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        if not heads:
            heads = cells
            continue
        name = re.sub(r"\*\*|`", "", cells[0]).strip() if cells else ""
        if name and not name.startswith(("(", "<", "…")):
            out.append((name, {h: c for h, c in zip(heads[1:], cells[1:]) if c and c not in ("…", "-", "—")}))
    return out


def _bare(name: str) -> str:
    return re.split(r"\s*[(,]", name, maxsplit=1)[0].strip().lower()


def _moves(name: str, rows: list) -> list:
    """The open Jobs whose next move is this person's or role's."""
    key = _bare(name)
    return [j for j in rows if j["theirs"] and key and (key in j["waiting"].lower() or _bare(j["waiting"]) == key)]


def _job_text(job: Path) -> str:
    texts = [job / f"{job.name}.md", job / "Timeline.md"]
    texts += [p for sub in ("emails", "meetings") for p in sorted((job / sub).glob("*")) if p.suffix in (".md", ".txt")]
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in texts if p.is_file()).lower()


def _sends(folder: Path, block: Path) -> list:
    """The messages a folder sent: its delivery/<date>-<what>/ sends (cowork_theme._deliveries), each with its folder."""
    from live.cowork_theme import _deliveries
    out = []
    for m in _deliveries(folder, block):
        m["from"] = folder
        out.append(m)
    return out


def _job_dirs(folder: Path, block: Path, level: str) -> list:
    """The Jobs a page speaks for: a Block's every jNN_, a Job itself."""
    return sorted(p for p in block.iterdir() if p.is_dir() and re.match(r"j\d\d_", p.name)) if level == "Block" else [folder]


def _all_sends(folder: Path, block: Path, level: str) -> list:
    if level == "Task":
        return _sends(folder, block)
    out = []
    for j in _job_dirs(folder, block, level):
        out += _sends(j, block)
        for t in sorted(j.glob("t[0-9]*_*")):
            if t.is_dir():
                out += _sends(t, block)
    return sorted(out, key=lambda m: m["date"], reverse=True)


# ── Findings: 👥 People · ✉️ Messages · ⏳ Next move ──────────────────────────────────────────────────────────────
def people_part(folder: Path, root: Path, level: str, rows: list) -> tuple | None:
    block = block_of(folder, level)
    found = people(block)
    if level == "Job" and folder.name != "j00_people":           # a Job: the people its own files name
        text = _job_text(folder)
        found = [(n, c) for n, c in found if _bare(n) and _bare(n) in text]
    if not found:
        return None
    own = level == "Job" and folder.name != "j00_people"         # a Job: only its own move counts here
    home = level == "Job" and folder == people_page(block).parent    # the people Job itself: a list, no move, no self-link
    tabs, panels, moving = [], [], 0
    for name, cells in found:
        moves = [] if home else [j for j in _moves(name, rows) if not own or j["name"] == folder.name]
        moving += bool(moves)
        side = cells.get("Side") or cells.get("side") or ""
        tabs.append((name, "has the move" if moves else side))
        panel = _kv([(k, esc(v)) for k, v in cells.items()])
        if moves:
            panel += '<h4 class=cw-sub>Has the move in</h4><ul class=cw-rows>' + "".join(
                f'<li><span class=t>{_job_link(block / j["name"], root, j["short"])}</span>'
                f'<small>since {esc(j["since"] or "—")}{" · " + _days(j["days"]) if j["days"] is not None else ""}</small></li>'
                for j in moves) + '</ul>'
        panels.append(panel)
    page = people_page(block)
    if not home:
        panels = [p + f'<div class=cw-verbs>{pop(reader(page, root), "People", "Open the people page ↗")}</div>' for p in panels]
    word = f"{moving} {'has' if moving == 1 else 'have'} the move" if moving else "reference"
    return "👥 People", word, CSS + _side_tabs("cwP" + folder.name[:3] + "x", tabs, panels), ""


def _note_rows(items: list, root: Path, with_job: bool) -> str:
    return '<ul class=cw-rows>' + "".join(
        f'<li><span class=d>{esc(n["date"] or "—")}</span><span class=t>{pop(reader(n["path"], root), n["title"])}</span>'
        + (f'<small>{esc(n["job"])}</small>' if with_job else "")
        + (' <small class=you>draft ✎ not sent</small>' if n.get("draft") else "") + '</li>' for n in items) + '</ul>'


def messages_part(folder: Path, root: Path, level: str) -> tuple | None:
    block = block_of(folder, level)
    emails, meetings = [], []
    for j in _job_dirs(folder, block, level):
        short = _title_of(j)
        for kind, bucket in (("emails", emails), ("meetings", meetings)):
            for n in notes(j / kind, block, root, short):
                n["path"] = j / kind / n["name"]
                bucket.append(n)
    sends = _all_sends(folder, block, level)
    unsent = [{"date": m["date"], "title": m["title"], "path": m["md"], "job": _title_of(m["from"]),
               "draft": True} for m in sends if m["draft"] and not m["sent"] and m["md"]]
    drafts = [n for n in emails if n["draft"]] + unsent
    if not (emails or meetings or drafts):
        return None
    emails.sort(key=lambda n: (n["date"], n["name"]), reverse=True)
    meetings.sort(key=lambda n: (n["date"], n["name"]), reverse=True)
    many = level == "Block"
    tabs = [("Emails", f"newest {emails[0]['date']}" if emails and emails[0]["date"] else "none yet"),
            ("Meetings", f"newest {meetings[0]['date']}" if meetings and meetings[0]["date"] else "none yet"),
            ("Drafts", "waits for you to send" if drafts else "none to send")]
    panels = [_note_rows(emails, root, many) if emails else '<p class=mut>No email here yet.</p>',
              _note_rows(meetings, root, many) if meetings else '<p class=mut>No meeting note here yet.</p>',
              _note_rows(drafts, root, many) if drafts else '<p class=mut>Nothing waits to be sent.</p>']
    word = (f"{len(drafts)} draft{'s wait' if len(drafts) > 1 else ' waits'} for you" if drafts
            else f"newest {max((n['date'] for n in emails + meetings if n['date']), default='—')}")
    waits = f"🙋 a draft waits for you to send: {drafts[0]['title']}" if drafts else ""
    return "✉️ Messages", word, CSS + _side_tabs("cwM" + folder.name[:3] + "x", tabs, panels), waits


def _ticket(j: dict) -> str:
    """A Job's ticket, a link when its face gives the office's url."""
    return (f'<a href="{esc(j["url"])}" target=_blank rel=noopener>{esc(j["ticket"])}</a>' if j["url"] and j["ticket"]
            else esc(j["ticket"]))


def _open_steps(job: Path, block: Path) -> list:
    return [s for s in steps(job / "CHECKLIST.md", block, job.name) if not s["done"]]


def _move_panel(j: dict, block: Path, root: Path) -> str:
    who = "us" if j["ours"] else j["waiting"]
    since = (j["since"] or "—") + (f" · {_days(j['days'])}" if j["days"] is not None else "")
    ticket = _ticket(j)
    body = (f'<p class=cw-next>{esc(j["next"])}</p>' if j["next"] else "") + _kv(
        [("Has the move", esc(who)), ("Since", esc(since)), ("Ticket", ticket)])
    left = _open_steps(block / j["name"], block)
    if left:
        body += '<h4 class=cw-sub>Steps still open</h4><ul class=cw-rows>' + "".join(
            f'<li><span class=d>☐ {esc(s["number"])}</span><span class=t>{esc(s["text"])}</span></li>' for s in left) + '</ul>'
    return body + f'<div class=cw-verbs>{_job_link(block / j["name"], root, "Open the Job ↗")}</div>'


def next_part(folder: Path, root: Path, level: str, rows: list) -> tuple | None:
    """The Block's open Jobs, ours first, then theirs by the longest wait (it carries over the old Waiting on view)."""
    if level != "Block":
        return None                                  # a Job's own move is its Status's first bar
    block = folder
    live = [j for j in rows if _state_group(j) in ("ours", "theirs", "open", "hold")]
    if not live:
        return None
    live.sort(key=lambda j: (not j["ours"], -(j["days"] or 0)))
    tabs = [(j["short"], ("ours" if j["ours"] else j["waiting"] if j["theirs"] else "on hold" if _state_group(j) == "hold"
                         else "open") + (f" · {_days(j['days'])}" if j["days"] is not None else "")) for j in live]
    panels = [_move_panel(j, block, root) for j in live]
    ours = [j for j in live if j["ours"]]
    theirs = sum(1 for j in live if j["theirs"])
    word = (f"{len(ours)} wait{'s' if len(ours) == 1 else ''} for you" if ours else "") + (
        (" · " if ours else "") + f"{theirs} on them" if theirs else "")
    waits = (f"🙋 {ours[0]['short']}: ours since {ours[0]['since'] or '—'}"
             + (f", {ours[0]['next']}" if ours[0]["next"] else "")) if ours else ""
    return "⏳ Next move", word or "open", CSS + _side_tabs("cwNx", tabs, panels), waits


def headlines_part(folder: Path, root: Path, level: str) -> tuple | None:
    """A Job's 📌 Headlines: each meeting's Decided and Next lines, newest first (b13 review r01: a done Job's
    Findings opens with what it settled)."""
    if level != "Job":
        return None
    block = block_of(folder, level)
    tabs, panels = [], []
    for n in notes(folder / "meetings", block, root, folder.name):
        text = (folder / "meetings" / n["name"]).read_text(encoding="utf-8", errors="ignore")
        said = [(k, v.strip()) for k, v in re.findall(r"(?m)^(Decided|Next):\s*(.+)$", text)]
        if said:
            tabs.append((n["title"], n["date"] or "undated"))
            panels.append(_kv([(k, esc(v)) for k, v in said])
                          + f'<div class=cw-verbs>{pop(reader(folder / "meetings" / n["name"], root), n["title"], "Read the notes ↗")}</div>')
    if not tabs:
        return None
    title = "📌 Headlines" if not any(folder.glob("t[0-9]*_*/")) else "📌 Meeting headlines"   # a Task's Headlines come first
    return title, f"newest {tabs[0][1]}", CSS + _side_tabs("cwH" + folder.name[:3] + "x", tabs, panels), ""


def parts(folder: Path, root: Path, level: str) -> list:
    """A cowork page's Findings parts, before 📦 Delivery: 📌 Headlines (a Job's meetings: Decided, Next), 👥 People,
    ✉️ Messages, ⏳ Next move (a Block only); a part with nothing in it is left out."""
    folder, root = Path(folder), Path(root)
    block = block_of(folder, level)
    if level not in ("Block", "Job") or not (block / "board.md").is_file():
        return []
    rows = _jobs(block, root)
    found = [headlines_part(folder, root, level), people_part(folder, root, level, rows), messages_part(folder, root, level),
             next_part(folder, root, level, rows)]
    found = [p for p in found if p]
    # a waiting item shows once per page, under the first section that holds it (b13 review r01): the next move of a
    # Job whose draft already waits under Messages is named in its tab, not waited on again
    if any(p[0] == "✉️ Messages" and p[3] for p in found):
        drafting = [j["short"] for j in rows if j["ours"] and any(n["draft"] for n in notes(block / j["name"] / "emails", block, root))]
        found = [(t_, w, h, "" if t_ == "⏳ Next move" and any(x.startswith(f"🙋 {s}:") for s in drafting) else x)
                 for t_, w, h, x in found]
    return found


# ── Status ───────────────────────────────────────────────────────────────────────────────────────────────────────
GROUPS = (("ours", "🙋 Waiting on us"), ("theirs", "⏳ Waiting on them"), ("open", "🟡 Open"), ("hold", "⏸️ On hold"),
          ("done", "✅ Done"))


def _job_row(j: dict, block: Path, root: Path) -> str:
    job = block / j["name"]
    who = ("us" if j["ours"] else j["waiting"]) if j["open"] else ""
    note = (f"{who} · {_days(j['days'])}" if who and j["days"] is not None else who or
            (f"since {j['since']}" if j["since"] else ""))
    items = _items(job, block, root)
    tree = _timeline_rows(items[:8]) if items else '<p class=mut>No dated entry yet.</p>'   # its next is on the row
    return (f'<details class=job-row><summary><a href="{esc(_job_url(job, root))}" data-pop="{esc(job.name)}" '
            f'title="{esc(job.name)}"><b>{esc(j["short"])}</b></a>'
            + (f'<span class=hl>{esc(j["next"])}</span>' if j["next"] and j["open"] else "")
            + f'<small>{esc(note)}</small></summary><div class=job-tree>{tree}</div></details>')


def _timeline_rows(items: list) -> str:
    return '<ul class=cw-rows>' + "".join(
        f'<li><span class=d>{esc(d or "—")}</span><span class=t>{h}</span><small>{esc(k)}</small></li>'
        for d, k, h in items) + '</ul>'


def block_status(block: Path, root: Path) -> list:
    rows = _jobs(block, root)
    out = []
    for key, title in GROUPS:
        members = [j for j in rows if _state_group(j) == key]
        if not members:
            continue
        if key == "theirs":
            members.sort(key=lambda j: -(j["days"] or 0))
        longest = max((j["days"] for j in members if j["days"] is not None), default=None)
        word = {"ours": f"{len(members)} wait{'s' if len(members) == 1 else ''} for you",
                "theirs": f"longest {_days(longest)}" if longest is not None else f"{len(members)} waiting",
                "open": "open", "hold": "on hold", "done": "done"}[key]
        waits = (f"🙋 {members[0]['short']}: {members[0]['next'] or 'the next move is ours'}" if key == "ours" else "")
        out.append((esc(title), word, CSS + "".join(_job_row(j, block, root) for j in members), waits))
    return out


def job_status(job: Path, root: Path) -> list:
    block = job.parent
    j = next((r for r in _jobs(block, root) if r["name"] == job.name), None)
    if j is None:
        return []
    out = []
    group = _state_group(j)
    since = (j["since"] or "—") + (f" · {_days(j['days'])}" if j["days"] is not None else "")
    ticket = _ticket(j)
    if group == "reference":                          # the people Job: one list of roles, nothing to wait on
        found = people(block)
        return [("📇 Who to ask, by role", "reference", CSS + '<ul class=cw-rows>' + "".join(
            f'<li><span class=t><b>{esc(n)}</b> {esc(c.get("Role here", ""))}</span><small>{esc(c.get("Side", ""))}</small></li>'
            for n, c in found) + '</ul>', "")] if found else []
    facts = _kv([("Has the move", esc("us" if j["ours"] else j["waiting"])), ("Since", esc(since)),
                 ("Next", "" if j["next"] and j["next"] in j["state"] else esc(j["next"])),   # the lead says it
                 ("Ticket", ticket)])
    if group in ("ours", "theirs", "open", "hold"):   # done: the lead's state line says it, no bar repeats it
        title, word, waits = {
            "ours": ("🙋 Waiting on us", f"waits for you · {_days(j['days'])}" if j["days"] is not None else "waits for you",
                     "🙋 the next move is ours"),
            "theirs": ("⏳ Waiting on them", f"{j['waiting']}" + (f" · {_days(j['days'])}" if j["days"] is not None else ""), ""),
            "open": ("🟡 Open", "open", ""), "hold": ("⏸️ On hold", "on hold", "")}[group]
        out.append((esc(title), word, CSS + facts, waits))
    items = _items(job, block, root)
    if items:
        out.append(("🗓️ Timeline", f"newest {items[0][0]}" if items[0][0] else "undated", CSS + _timeline_rows(items), ""))
    checklist = steps(job / "CHECKLIST.md", block, job.name)
    if checklist:
        done = sum(1 for s in checklist if s["done"])
        out.append(("☑️ Steps", f"{done} of {len(checklist)} done", CSS + '<ul class=cw-rows>' + "".join(
            f'<li><span class=d>{"☑" if s["done"] else "☐"} {esc(s["number"])}</span><span class=t>{esc(s["text"])}</span>'
            + ('' if s["done"] else '<small>open</small>') + '</li>' for s in checklist) + '</ul>', ""))
    from live import focus_page as F
    tasks = F.tasks_section(job, root)
    if tasks:
        out.append((tasks[0], tasks[1], tasks[2], "", tasks[3]))
    return out


def rounds(task: Path) -> list:
    """[(run, pass folder, title, summary, [files])]: each round of a document written in rounds, a pass of its
    write (revise, draft, edit) soft Run, oldest first."""
    out = []
    for run in sorted(p for p in (task / "runs").glob("run-*") if p.is_dir() and _ROUND_RUN.match(p.name)):
        for p in sorted((run / "passes").glob("p*/pass.md")):
            text = p.read_text(encoding="utf-8", errors="ignore")
            title = (re.search(r"(?m)^#\s+(.+)$", text) or [None, p.parent.name])[1].strip()
            summary = (re.search(r"(?ms)^## Summary\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1].strip()
            changed = (re.search(r"(?ms)^## Changed\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1]
            files = [run / f for f in re.findall(r"`([^`]+)`", changed) if (run / f).is_file()]
            out.append((run, p.parent, title, "" if summary.startswith("<") else summary, files))
    return out


CHAIN_CSS = """<style>
.cw-chain{list-style:none;display:flex;flex-wrap:wrap;align-items:stretch;gap:8px 0;margin:4px 0 14px;padding:0}
.cw-chain li{display:flex;align-items:center}.cw-chain li+li::before{content:"→";margin:0 8px;color:var(--muted)}
.cw-chain .box{border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:13px;line-height:1.4;max-width:220px}
.cw-chain .box b{display:block;font-weight:600}.cw-chain .box small{color:var(--muted)}
.cw-chain .box.you{border-color:light-dark(#ffa94d,#b35c00)}.cw-chain .box.next{border-style:dashed}
</style>"""


def _mmdd(folder: Path) -> str:
    m = re.match(r"^p\d+-(\d\d)(\d\d)$", folder.name)
    return f"{m.group(1)}-{m.group(2)}" if m else ""


def _chain(task: Path, root: Path, found: list, nxt: str) -> str:
    """The rounds as one chain, oldest first: each version sent, what came back before the next (the Job's emails in
    between), the choice that waits on the person (a waiting form under the Task), then the next version."""
    from live import focus_page as F
    job, block = task.parent, task.parent.parent
    mails = [n for n in notes(job / "emails", block, root, job.name) if not n["draft"] and n["date"]]
    mails.sort(key=lambda n: n["date"])
    boxes = []
    for k, (run, folder, title, summary, files) in enumerate(found):
        day, after = _mmdd(folder), _mmdd(found[k + 1][1]) if k + 1 < len(found) else "99-99"
        links = " · ".join(pop(_file_url(f, root), f.name, f.stem.replace("_", " ")) for f in files if f.suffix == ".md")
        boxes.append(f'<li><div class=box><b>{esc(title)}</b><small>{esc(day)}</small>'
                     + (f'<br>{links}' if links else "") + '</div></li>')
        for n in (n for n in mails if day < n["date"][5:] < after):
            boxes.append(f'<li><div class=box><b>{pop(reader(job / "emails" / n["name"], root), n["title"])}</b>'
                         f'<small>{esc(n["date"][5:])} · came back</small></div></li>')
    for r in (r for r in F.interactions(task, root) if r["state"] == "waiting" and r["page"] == task):
        ask = r["asks"][0][2] if r["asks"] else r["title"]
        boxes.append(f'<li><div class="box you"><b>? {esc(r["title"])}</b><small>{esc(ask)}</small></div></li>')
    if nxt:
        last = re.split(r",\s*then\s+", nxt)[-1]                       # "pick …, then write v3" -> "write v3"
        boxes.append(f'<li><div class="box next"><b>{esc(last)}</b><small>next</small></div></li>')
    return CHAIN_CSS + '<ol class=cw-chain>' + "".join(boxes) + '</ol>'


def task_status(task: Path, root: Path) -> list:
    """A document written in rounds: its newest round's headline first, the rounds as a chain and newest first, its
    Runs (b13 review r01)."""
    found = rounds(task)
    if not found:
        return []                                    # a Task that is no document in rounds: the shared Status
    from live import focus_page as F
    from live.task_questions import field, read
    text = read(task / f"{task.name}.md", task)
    who, nxt = field(text, "waiting-on"), field(text, "next")
    run, folder, title, summary, files = found[-1]
    head = F.run_headline(run) or title
    links = " · ".join(pop(_file_url(f, root), f.name) for f in files)
    out = [("📌 " + esc(head), "waits for you" if who.strip().lower() == "us" else who or "current", CSS
            + (f'<p class=cw-next>{esc(summary)}</p>' if summary else "") + (f'<div class=cw-verbs>{links}</div>' if links else "")
            + f'<div class=cw-verbs>{pop(F.run_url(run, root), task.name + " · " + run.name, "Open " + run.name + " ↗")}</div>', "")]
    tabs, panels = [], []
    for run, folder, title, summary, files in reversed(found):           # newest first
        tabs.append((title, _mmdd(folder) or folder.name))
        links = " · ".join(pop(_file_url(f, root), f.name) for f in files)
        panels.append((f'<p class=cw-next>{esc(summary)}</p>' if summary else "") + (f'<div class=cw-verbs>{links}</div>' if links else ""))
    out.append(("📝 Rounds", f"newest {_mmdd(found[-1][1])}" if _mmdd(found[-1][1]) else "rounds",
                CSS + _chain(task, root, found, nxt) + _side_tabs("cwRx", tabs, panels), ""))
    runs = F.runs_section(task, root)
    if runs:
        out.append(runs + ("",))
    return out


def status(folder: Path, root: Path, level: str) -> list:
    """A cowork page's Status bars, in place of the shared ones: a Block's Jobs by state, a Job's move, timeline and
    steps, a Task's rounds; [] leaves the shared bars (a Task that is no document in rounds)."""
    folder, root = Path(folder), Path(root)
    block = block_of(folder, level)
    if not (block / "board.md").is_file():
        return []
    if level == "Block":
        return block_status(folder, root)
    if level == "Job":
        return job_status(folder, root)
    if level == "Task":
        return task_status(folder, root)
    return []


# ── MindMap: a Job with no Tasks ─────────────────────────────────────────────────────────────────────────────────
KIND_WORD = {"note": "", "email": "email", "meeting": "meeting", "sent": "sent"}


def map_branches(folder: Path, root: Path, level: str) -> list:
    """[(branch, [leaves])] for a page the shared map cannot read (focus_page.parts_mindmap asks when it has nothing,
    261108): a cowork Job's newest dated items, who has the move, its next step and its open steps; the people Job its
    roles. Short labels in words."""
    import html as _html
    folder, root = Path(folder), Path(root)
    block = block_of(folder, level)
    if level != "Job" or not (block / "board.md").is_file():
        return []
    j = next((r for r in _jobs(block, root) if r["name"] == folder.name), None)
    if j is None:
        return []
    if _state_group(j) == "reference":
        roles = [f"{n} · {c.get('Side')}" if c.get("Side") else n for n, c in people(block)]
        return [("👥 Who to ask", roles)] if roles else []
    out = []
    items = _items(folder, block, root)
    plain = lambda h: " ".join(_html.unescape(re.sub(r"<[^>]+>", "", h)).split())
    if items:
        out.append(("🗓️ What happened", [f"{d} · {plain(h)}" + (f" ({KIND_WORD[k]})" if KIND_WORD.get(k) else "")
                                         for d, k, h in items[:6]]))
    if j["open"]:
        who = "us" if j["ours"] else j["waiting"]
        out.append(("⏳ Who has the move", [f"{who} · since {j['since'] or '—'}" + (f" · {_days(j['days'])}" if j["days"] is not None else "")]))
    else:
        out.append(("✅ Done", [f"since {j['since']}" if j["since"] else "nothing left to do"]))
    if j["next"] and j["open"]:
        out.append(("➡️ Next", [j["next"]]))
    left = _open_steps(folder, block)
    if left:
        out.append(("☐ Steps still open", [s["text"] for s in left]))
    return out


# ── 📦 Delivery: the messages sent ────────────────────────────────────────────────────────────────────────────────
def delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """[(tab, word, panel)] in place of the shared lanes: each message this page and the pages below it sent
    (delivery/jNN_<job>/[tNN_<task>/]<date>-<what>/), its draft's head, its copy page and its attachments."""
    folder, root = Path(folder), Path(root)
    block = block_of(folder, level)
    if not (block / "board.md").is_file():
        return []
    tabs = []
    for m in _all_sends(folder, block, level):
        head = dict(_HEAD.findall(m["md"].read_text(encoding="utf-8", errors="ignore"))) if m["md"] else {}
        word = "draft ✎ not sent" if m["draft"] and not m["sent"] else "sent" if m["sent"] else "not marked sent"
        where = " › ".join(_title_of(block / q) for q in _ancestry(m["from"].relative_to(block)))
        body = _kv([("Date", esc(m["date"] or "—")), ("From", esc(where)), ("To", esc(head.get("To", ""))),
                    ("Cc", esc(head.get("Cc", ""))), ("Subject", esc(head.get("Subject", ""))), ("State", esc(word))])
        files = " · ".join(pop(_file_url(f, root), f.name) for f in m["attach"] if f.is_file())
        verbs = [pop("/" + m["page"].relative_to(root).as_posix(), m["title"], "Open the copy page ↗")] if m["page"] else []
        verbs += [pop(reader(m["md"], root), m["md"].name, "Read the draft ↗")] if m["md"] else []
        tabs.append((m["title"], word, body + (f'<h4 class=cw-sub>Attachments</h4><div class=cw-verbs>{files}</div>' if files else "")
                     + f'<div class=cw-verbs>{" · ".join(verbs)}</div>'))
    if not tabs:
        tabs.append(("Messages", "nothing yet", '<p class=mut>Nothing sent from here yet.</p>'))
    return tabs


