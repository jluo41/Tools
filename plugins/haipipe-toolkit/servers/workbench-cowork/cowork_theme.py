"""The cowork theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A cowork topic climbs Block → Job → Run (Tools/blueprints/b13_theme_cowork, Q01, proposed 261007). An
email, a meeting or a checklist step is a row of its Job, not a Task; a Task (`tNN_<doc>/`) is only a
document written with others in rounds, and it opens as the base's Page Task, so the Task level is
left vanilla and its tab is greyed until a Job has one.

    Block  Description: Scope · People · Resources (Related: folded inside the Studio) | Audience Report: the base's Question
           cards under the group bar (each opens on Logic │ Work │ Report, the report's drawing live in Report);
           Questions · Timeline when a report carries an event table (b10 s05-D05, D09)
           | Work Details: its Jobs, All · open · waiting · done | Delivery: delivery/ (every Job's messages
           out) · Reports · Done jobs
    Job    Description: Job · Files | Audience Report: the Block's Questions citing this Job
           | Work Details: Timeline · Checklist · Emails · Meetings | Delivery: its messages out, each with
           its attachments (delivery/<date>-<what>/)

Idea Studio and Runs read as vanilla (studio/ topics; runs/ grouped by type); the theme adds its
run types. It reads the Block through coworkboard.py and writes nothing; no run sends a message.
"""
from src.common import delivery_dir
import re
from pathlib import Path
from urllib.parse import urlencode

from live.coworkboard import DONE, files, header, jobs, notes, people_page, steps, waited
from live.frame import ROUTE, Space, Theme, delivery_view, esc, link, pop, reader, rel, table, work_tree
from live.task_questions import field, read, register, words

_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
_NOBODY = ("us", "nobody", "")


def _run(label, verb):
    return {"label": label, "prompt": f"/haipipe-cowork {verb} {{folder}}"}


BLOCK_RUNS = {"Description": (_run("Update the Block status", "update the Block status of"),
                              _run("Add a person", "add a person to"), _run("Add a resource", "add a resource to")),
              "Audience Report": ({"label": "Ask a Question", "prompt": "/haipipe-report ask {folder}"},
                                  {"label": "Review the questions", "prompt": "/haipipe-report review {folder}"},
                                  {"label": "Write the report", "prompt": "/haipipe-draft-writing {folder}/reports/"},
                                  {"label": "Check a report", "prompt": "/haipipe-draft-review check {folder}/reports/"}),
              "Work Details": (_run("Open a job", "open a job in"), _run("Update a job", "update a job in")),
              "Runs": (_run("Update the Block status", "update the Block status of"),
                       {"label": "Draw", "prompt": "/haipipe-studio draw a topic in {folder}/studio/"}),
              "Delivery": ({"label": "Check a report", "prompt": "/haipipe-draft-review check {folder}/reports/"},)}
JOB_RUNS = {"Description": (_run("Update the Job", "update the job"), _run("Add a file", "add a file to")),
            "Audience Report": ({"label": "Ask a Question", "prompt": "/haipipe-report ask {folder}"},),
            "Work Details": (_run("Add an entry", "add a Timeline entry to"),
                             {"label": "Draft an email", "prompt": "/haipipe-draft draft an email in {folder}/emails/"},
                             _run("Write meeting notes", "write meeting notes in")),
            "Runs": (_run("Update the Job", "update the job"),
                     {"label": "Draft an email", "prompt": "/haipipe-draft draft an email in {folder}/emails/"},
                     _run("Write meeting notes", "write meeting notes in"),
                     {"label": "Review a draft", "prompt": "/haipipe-draft-review review the draft in {folder}/emails/"})}


def _pick(sub, options):
    return sub if sub in options else options[0]


def _waiting(job) -> bool:
    return job["open"] and job["waiting"].strip().lower() not in _NOBODY


def _job_link(job, block, root):
    return link(ROUTE + "?" + urlencode({"path": rel(block / job["name"], root)}), job["name"])


def _questions(board_text):
    rows, _ = register(board_text, "Questions", "questions")
    return [r for r in rows if words(r.get("id"))]


def _question_rows(rows, block, root):
    out = []
    for r in rows:
        qid = words(r.get("id"))
        work = r.get("work") if isinstance(r.get("work"), list) else []
        paths = [w if isinstance(w, str) else words(w.get("path")) for w in work if isinstance(w, (str, dict))]
        cited = " · ".join(link(reader(block / p, root), p) for p in paths if p and (block / p).is_file())
        report = block / words(r.get("report")) if words(r.get("report")) else None
        status = field(read(report, block), "answer-status") if report and report.is_file() else ""
        out.append((esc(qid + " " + (words(r.get("title")) or words(r.get("question")))),
                    cited or '<span class=mut>—</span>',
                    link(reader(report, root), status or "report") if report and report.is_file()
                    else '<span class=mut>no report yet</span>'))
    return out


def _deliveries(job_dir, block):
    """One message we send per `delivery/<date>-<what>/` of a Job: its draft (.md) and its attachments
    (JL 261009: "add it to the delivery"), newest first."""
    out, d = [], delivery_dir(job_dir)
    sends = (owner / "delivery" / "delivery.md") if (owner := next((b for b in (job_dir, *job_dir.parents)
                                                                       if (b / "board.md").is_file()), None)) else None
    marked = read(sends, block) if sends and sends.is_file() else ""
    for p in sorted(d.iterdir(), reverse=True) if d.is_dir() else []:
        if p.name.startswith((".", "_")):
            continue
        found = sorted(f for f in (p.iterdir() if p.is_dir() else [p]) if f.is_file() and not f.name.startswith("."))
        md = next((f for f in found if f.suffix == ".md"), None)
        text = read(md, block) if md else ""
        if (p.is_dir() and not re.match(r"\d{4}-\d{2}-\d{2}", p.name)) or (
                p.is_file() and not re.search(r"(?m)^(Subject|To):", text)):
            continue      # a built table, form or notes folder, not a <date>-<what>/ message: the cards above list it
        title = re.search(r"(?m)^#\s+(.+)$", text) or re.search(r"(?m)^Subject:\s*(.+)$", text)
        page = md.with_suffix(".html") if md and md.with_suffix(".html").is_file() else None   # email_page.py's
        named = re.search(r"(?m)^Attach:\s*(.+)$", text)                                       # copy page
        date = _DATE.search(p.name) or _DATE.search(text)
        out.append({"date": date.group(1) if date else "",
                    "md": md, "page": page, "title": title.group(1).strip() if title else p.name,
                    "draft": bool(re.search(r"(?m)^\s*status:\s*draft\b", text)) or "draft" in (md.name if md else ""),
                    # sent is a person's word (haipipe-delivery): its draft says so, or delivery.md has its row sent
                    "sent": bool(re.search(r"(?m)^\s*status:\s*sent\b", text)) or bool(re.search(
                        r"(?m)^\|.*" + re.escape(p.name) + r".*\|\s*sent\s*\|\s*$", marked)),
                    "attach": [p / n.strip() for n in named.group(1).split(";") if n.strip()] if named
                              else [f for f in found if md is None or f.stem != md.stem]})
    return out


def _delivery_rows(job_dir, block, root, with_job=False):
    rows = []
    for m in _deliveries(job_dir, block):
        msg = (pop("/" + rel(m["page"], root), m["title"]) if m["page"]          # the page to copy from
               else link(reader(m["md"], root), m["title"]) if m["md"] else esc(m["title"]))
        files_ = " · ".join(pop("/" + rel(f, root), f.name) for f in m["attach"]) or '<span class=mut>none</span>'
        row = (esc(m["date"] or "—"), msg, files_, "draft ✎ not sent" if m["draft"] else "sent" if m["sent"]
               else '<span class=mut>not marked sent</span>')
        rows.append(((_job_link({"name": job_dir.name}, block, root),) if with_job else ()) + row)
    return rows


def _block(block, root, sub):
    text = read(block / "board.md", block)
    head = header(text, block)
    rows, _ = jobs(block, root)
    out = {}

    d_sub = _pick(sub, ("Scope", "People", "Resources"))       # Related folds inside the Studio (b10 s04-D05)
    if d_sub == "Scope":
        body = None                                                     # vanilla: the face's fields
    elif d_sub == "People":
        page = people_page(block)
        body = (f'<p class=mut>{link(reader(page, root), rel(page, root))}</p><pre>{esc(read(page, block))}</pre>'
                if page.is_file() else '<p class=mut>No people page yet (j00_people/j00_people.md).</p>')
    else:
        res, _ = register(text, "Related resources", "resources")
        found = [(link(words(r.get("url")), words(r.get("title"))), esc(", ".join(r.get("questions") or [])))
                 for r in res if words(r.get("title")) and words(r.get("url")).startswith(("http://", "https://"))]
        found += [(link(reader(block / j["name"] / d / f["name"], root), f"{d}/{f['name']}")
                   if f["name"].endswith(".md") else esc(f"{d}/{f['name']}"), esc(j["name"]))
                  for j in rows for d in ("materials", "design") for f in j[d]]
        found += [(esc(p.strip()), "OneDrive") for p in head["onedrive"].split(",") if p.strip()]
        body = table(("resource", "for"), found)
    out["Description"] = Space(html=body or "", subspaces=("Scope", "People", "Resources"), open=d_sub,
                               run_types=BLOCK_RUNS["Description"])

    # the Report: the base's Question cards under the group bar, the same code as every theme (b10 s05-D05); a
    # report that carries an event table adds a Timeline view above the list, a lens and not a group (s05-D09)
    from .timeline_view import group_timeline
    events = group_timeline(block, root, _questions(text))
    a_sub = ("Timeline" if sub == "Timeline" else "Questions") if events else ""
    out["Audience Report"] = Space(html=events if a_sub == "Timeline" else "",       # "": the base's cards
                                   subspaces=("Questions", "Timeline") if events else (), open=a_sub,
                                   run_types=BLOCK_RUNS["Audience Report"])

    w_sub = _pick(sub, ("All", "open", "waiting", "done"))
    keep = {"All": lambda j: True, "open": lambda j: j["open"], "waiting": _waiting,
            "done": lambda j: j["state"].startswith(DONE)}[w_sub]
    # the base's Work tree (b10 s32-D19, JL 261012: "show the job to the task to the run results"), the Jobs this
    # view keeps; each Job card says its state, who it waits on and what is next (work_meta)
    kept = [block / j["name"] for j in rows if keep(j)]
    out["Work Details"] = Space(html=work_tree("Block", block, root, THEME, jobs=kept) or table(("Job",), []),
                                subspaces=("All", "open", "waiting", "done"), open=w_sub,
                                run_types=BLOCK_RUNS["Work Details"])
    out["Runs"] = Space(run_types=BLOCK_RUNS["Runs"])

    v_sub = sub if sub in ("Reports", "Done jobs") else ""
    if v_sub == "Reports":
        answered = [r for r in _questions(text) if words(r.get("report"))
                    and field(read(block / words(r.get("report")), block), "answer-status") in ("answered", "closed")]
        html = table(("Question", "Work", "Report"), _question_rows(answered, block, root))
    elif v_sub == "Done jobs":
        html = table(("Job", "title", "since"), [(_job_link(j, block, root), esc(j["title"]), esc(j["since"] or "—"))
                                                  for j in rows if j["state"].startswith(DONE)])
    else:          # the base's result cards under the group bar (b10 s32-D18), then every Job's messages out
        sent = [r for j in rows for r in _delivery_rows(block / j["name"], block, root, with_job=True)]
        html = (delivery_view(block, root, THEME)
                + ("<h3>Messages</h3>" + table(("Job", "date", "message", "attachments", "state"), sent)
                   if sent else ""))
    out["Delivery"] = Space(html=html, subspaces=("delivery/", "Reports", "Done jobs"), open=v_sub or "delivery/",
                            run_types=BLOCK_RUNS["Delivery"])
    return out


def _timeline(job_dir, block, root, emails, meetings, checklist):
    """Every dated thing in one Job, newest first: Timeline.md lines, emails, meetings, done steps."""
    items = []
    for line in read(job_dir / "Timeline.md", block).splitlines():
        found = _DATE.search(line)
        if found:
            rest = line.replace(found.group(1), "", 1).strip(" -|:*\t")
            items.append((found.group(1), "entry", esc(rest)))
    for kind, rows in (("email", emails), ("meeting", meetings)):
        for n in rows:
            state = " <b>draft ✎</b>" if n.get("draft") else ""
            items.append((n["date"], kind, link(reader(job_dir / (kind + "s") / n["name"], root), n["title"]) + state))
    for m in _deliveries(job_dir, block):
        items.append((m["date"], "delivery", (link(reader(m["md"], root), m["title"]) if m["md"] else esc(m["title"]))
                      + (" <b>draft ✎</b>" if m["draft"] else "")))
    items.sort(key=lambda x: x[0], reverse=True)
    undated = sum(1 for s in checklist if not s["done"])
    shown = table(("date", "item", ""), [(esc(d or "—"), esc(k), h) for d, k, h in items])
    return shown + (f'<p class=mut>{undated} checklist steps open: see Checklist.</p>' if undated else "")


def _job(job_dir, root, sub):
    block = job_dir.parent
    page = job_dir / f"{job_dir.name}.md"
    text = read(page, block)
    out = {}

    d_sub = _pick(sub, ("Job", "Files"))
    if d_sub == "Job":
        since = field(text, "since")
        days = waited(since)
        rows = [(esc(k), esc(field(text, k)) + (f' <span class=mut>· {days} days</span>' if k == "since" and days is not None else ""))
                for k in ("state", "waiting-on", "since", "next", "ticket", "url") if field(text, k)]
        body = (f'<p class=mut>{link(reader(page, root), rel(page, root))}</p>' + table(("field", "value"), rows)
                if text else f'<p class=mut>No job page: {esc(page.name)} is missing.</p>')
    else:
        found = [(link(reader(job_dir / sub_dir / f["name"], root), f"{sub_dir}/{f['name']}")
                  if f["name"].endswith(".md") else esc(f"{sub_dir}/{f['name']}"), esc(sub_dir))
                 for sub_dir in ("materials", "design") for f in files(job_dir / sub_dir, block, root)]
        body = table(("file", "folder"), found)
    out["Description"] = Space(html=body, subspaces=("Job", "Files"), open=d_sub, run_types=JOB_RUNS["Description"])

    # "": the base's cards under the group bar, the Block's Questions whose work: names this Job (b10 s05-D17)
    out["Audience Report"] = Space(html="", run_types=JOB_RUNS["Audience Report"])

    emails = notes(job_dir / "emails", block, root, job_dir.name)
    meetings = notes(job_dir / "meetings", block, root, job_dir.name)
    checklist = steps(job_dir / "CHECKLIST.md", block, job_dir.name)
    w_sub = _pick(sub, ("Timeline", "Checklist", "Emails", "Meetings"))
    if w_sub == "Timeline":
        body = _timeline(job_dir, block, root, emails, meetings, checklist)
    elif w_sub == "Checklist":
        body = table(("step", "", "what"), [(esc(s["number"] or "—"), "☑" if s["done"] else "☐", esc(s["text"]))
                                             for s in checklist])
    else:
        rows, kind = (emails, "emails") if w_sub == "Emails" else (meetings, "meetings")
        body = table(("date", kind[:-1], "state"),
                      [(esc(n["date"] or "—"), link(reader(job_dir / kind / n["name"], root), n["title"]),
                        "draft ✎" if n.get("draft") else "") for n in rows])
    out["Work Details"] = Space(html=body, subspaces=("Timeline", "Checklist", "Emails", "Meetings"), open=w_sub,
                                run_types=JOB_RUNS["Work Details"])
    out["Runs"] = Space(run_types=JOB_RUNS["Runs"])
    sent = _delivery_rows(job_dir, block, root)
    cards = delivery_view(job_dir, root, THEME)                # this Job's part, as result cards (b10 s32-D18)
    out["Delivery"] = Space(html=cards + ("<h3>Messages</h3>" + table(("date", "message", "attachments", "state"), sent)
                                          if sent else "" if cards else
                                          '<p class=mut>Nothing to send yet: a message and its attachments go in '
                                          'delivery/&lt;date&gt;-&lt;what&gt;/.</p>'))
    return out


def work_meta(folder, root):
    """A cowork Job's card in the Work tree: its state, who it waits on (and how long) and what is next."""
    folder = Path(folder)
    if not (folder.parent / "board.md").is_file():
        return ""
    rows, _ = jobs(folder.parent, Path(root))
    j = next((r for r in rows if r["name"] == folder.name), None)
    if j is None:
        return ""
    wait = (f'waiting on {esc(j["waiting"])}' + (f' · {esc(j["days"])} days' if j["days"] is not None else "")
            if _waiting(j) else "")
    return " · ".join(x for x in (esc(j["state"]), wait, f'next: {esc(j["next"])}' if j["next"] else "") if x)


def work_body(folder, root):
    """An opened cowork Job card in the Work tree: its timeline, every dated email, meeting, entry and send."""
    job_dir, root = Path(folder), Path(root)
    block = job_dir.parent
    if not (block / "board.md").is_file():
        return ""
    return _timeline(job_dir, block, root, notes(job_dir / "emails", block, root, job_dir.name),
                     notes(job_dir / "meetings", block, root, job_dir.name),
                     steps(job_dir / "CHECKLIST.md", block, job_dir.name))


def spaces(level, folder, root, sub):
    folder, root = Path(folder), Path(root)
    if level == "Block" and (folder / "board.md").is_file():
        return _block(folder, root, sub)
    if level == "Job" and (folder.parent / "board.md").is_file():
        return _job(folder, root, sub)
    return {}                                                            # a Page Task: the base's own


# each button's Run (haipipe-run rule 6)
RUN_NAMES = {"Update the Block status": "run-face-<bNN>", "Add a person": "run-add-person-<name>",
             "Add a resource": "run-add-resource-<slug>", "Ask a Question": "run-ask-<qNN>",
             "Review the questions": "run-review-questions", "Write the report": "run-report-<qNN>",
             "Check a report": "run-check-<qNN>", "Open a job": "run-add-<jNN>", "Update a job": "run-face-<jNN>",
             "Draw": "run-draw-<sNN>", "Update the Job": "run-face-<jNN>", "Add a file": "run-add-file-<slug>",
             "Add an entry": "run-add-entry-<slug>", "Draft an email": "run-email-<slug>",
             "Write meeting notes": "run-meeting-<slug>", "Review a draft": "run-review-email-<slug>"}

# the Report's suggested groups, the kinds of question cowork keeps asking (b10 s05-D07): what the study needs from
# a partner, what already works, what blocks it
THEME = Theme(name="cowork", label="CoWork", icon="🤝", guide="cowork", spaces=spaces, run_names=RUN_NAMES,
              report_groups=("Needs", "Works", "Blockers"), work_meta=work_meta, work_body=work_body)
