"""The cowork theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A cowork topic climbs Block → Job → Run (Tools/blueprints/b01_haipipe-toolkit/j13_theme_cowork, Q01, proposed 261007). An
email, a meeting or a checklist step is a row of its Job, not a Task; a Task (`tNN_<doc>/`) is only a
document written with others in rounds, and it opens as the base's Page Task, so the Task level is
left vanilla and its tab is greyed until a Job has one.

    Block  Description: Scope · People · Resources · Related | Audience Report: Question │ Work │ Report
           | Work Details: its Jobs, All · open · waiting · done | Delivery: Reports · Done jobs
    Job    Description: Job · Files | Audience Report: the Block's Questions citing this Job
           | Work Details: Timeline · Checklist · Emails · Meetings

Idea Studio and Runs read as vanilla (studio/ topics; runs/ grouped by type); the theme adds its
run types. It reads the Block through coworkboard.py and writes nothing; no run sends a message.
"""
import re
from pathlib import Path
from urllib.parse import urlencode

from live.coworkboard import DONE, files, header, jobs, notes, people_page, steps, waited
from live.frame import ROUTE, Space, Theme, esc, link, reader, rel, table
from live.task_questions import field, read, register, words

_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
_NOBODY = ("us", "nobody", "")


def _run(label, verb):
    return {"label": label, "prompt": f"/haipipe-cowork {verb} {{folder}}"}


BLOCK_RUNS = {"Description": (_run("Update the Block status", "update the Block status of"),
                              _run("Add a person", "add a person to"), _run("Add a resource", "add a resource to")),
              "Audience Report": ({"label": "Ask a Question", "prompt": "/haipipe-question-asking {folder}"},
                                  {"label": "Review the questions", "prompt": "/haipipe-question-review {folder}"},
                                  {"label": "Write the report", "prompt": "/haipipe-page-writing {folder}/reports/"},
                                  {"label": "Check a report", "prompt": "/haipipe-page-check {folder}/reports/"}),
              "Work Details": (_run("Open a job", "open a job in"), _run("Update a job", "update a job in")),
              "Runs": (_run("Update the Block status", "update the Block status of"),
                       {"label": "Draw", "prompt": "/workbench-studio draw a topic in {folder}/studio/"}),
              "Delivery": ({"label": "Check a report", "prompt": "/haipipe-page-check {folder}/reports/"},)}
JOB_RUNS = {"Description": (_run("Update the Job", "update the job"), _run("Add a file", "add a file to")),
            "Audience Report": ({"label": "Ask a Question", "prompt": "/haipipe-question-asking {folder}"},),
            "Work Details": (_run("Add an entry", "add a Timeline entry to"),
                             {"label": "Draft an email", "prompt": "/haipipe-writing draft an email in {folder}/emails/"},
                             _run("Write meeting notes", "write meeting notes in")),
            "Runs": (_run("Update the Job", "update the job"),
                     {"label": "Draft an email", "prompt": "/haipipe-writing draft an email in {folder}/emails/"},
                     _run("Write meeting notes", "write meeting notes in"),
                     {"label": "Review a draft", "prompt": "/haipipe-writing review the draft in {folder}/emails/"})}


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


def _block(block, root, sub):
    text = read(block / "board.md", block)
    head = header(text, block)
    rows, _ = jobs(block, root)
    out = {}

    d_sub = _pick(sub, ("Scope", "People", "Resources", "Related"))
    if d_sub == "Scope":
        body = None                                                     # vanilla: the face's fields
    elif d_sub == "People":
        page = people_page(block)
        body = (f'<p class=mut>{link(reader(page, root), rel(page, root))}</p><pre>{esc(read(page, block))}</pre>'
                if page.is_file() else '<p class=mut>No people page yet (j00_people/j00_people.md).</p>')
    elif d_sub == "Resources":
        res, _ = register(text, "Related resources", "resources")
        found = [(link(words(r.get("url")), words(r.get("title"))), esc(", ".join(r.get("questions") or [])))
                 for r in res if words(r.get("title")) and words(r.get("url")).startswith(("http://", "https://"))]
        found += [(link(reader(block / j["name"] / d / f["name"], root), f"{d}/{f['name']}")
                   if f["name"].endswith(".md") else esc(f"{d}/{f['name']}"), esc(j["name"]))
                  for j in rows for d in ("materials", "design") for f in j[d]]
        found += [(esc(p.strip()), "OneDrive") for p in head["onedrive"].split(",") if p.strip()]
        body = table(("resource", "for"), found)
    else:
        related = block / "related" / "related.md"
        body = (f'<p>{link(reader(related, root), "related/related.md")}</p>' if related.is_file()
                else '<p class=mut>No related/related.md yet.</p>')
    out["Description"] = Space(html=body or "", subspaces=("Scope", "People", "Resources", "Related"), open=d_sub,
                               run_types=BLOCK_RUNS["Description"])

    out["Audience Report"] = Space(html=table(("Question", "Work", "Report"), _question_rows(_questions(text), block, root)),
                                   run_types=BLOCK_RUNS["Audience Report"])

    w_sub = _pick(sub, ("All", "open", "waiting", "done"))
    keep = {"All": lambda j: True, "open": lambda j: j["open"], "waiting": _waiting,
            "done": lambda j: j["state"].startswith(DONE)}[w_sub]
    job_rows = [(_job_link(j, block, root), esc(j["state"] or "—"),
              esc(j["waiting"] if j["open"] else "—") + (f' <span class=mut>· {esc(j["days"])} days</span>'
                                                         if _waiting(j) and j["days"] is not None else ""),
              esc(j["next"] or "—")) for j in rows if keep(j)]
    out["Work Details"] = Space(html=table(("Job", "state", "waiting on", "next"), job_rows),
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
    else:
        html = ""                                                       # vanilla: delivery/
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

    citing = [r for r in _questions(read(block / "board.md", block))
              if any((w if isinstance(w, str) else words(w.get("path")) if isinstance(w, dict) else "")
                     .startswith(job_dir.name + "/") for w in (r.get("work") if isinstance(r.get("work"), list) else []))]
    out["Audience Report"] = Space(
        html='<p class=mut>The Block\'s Questions that cite this Job.</p>'
             + table(("Question", "Work", "Report"), _question_rows(citing, block, root)),
        run_types=JOB_RUNS["Audience Report"])

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
    return out


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

THEME = Theme(name="cowork", label="CoWork", icon="🤝", guide="cowork", spaces=spaces, run_names=RUN_NAMES)
