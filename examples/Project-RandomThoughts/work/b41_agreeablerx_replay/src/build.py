import re, json, html, os, datetime, glob, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))   # run from anywhere: sources here, page to ../delivery, Jobs to ../jNN_<day>/
def parse(path):
    t = open(path, encoding="utf-8").read()
    sec = lambda name: (re.search(r"(?ms)^## " + name + r"\s*\n(.*?)(?=^## |\Z)", t) or [None, ""])[1]
    sessions = []
    for line in sec("Sessions").splitlines():
        m = re.match(r"- \**([\w.-]+)\**: (.*)", line.strip())
        if m:
            sessions.append({"name": m.group(1), "text": m.group(2)})
    phases = []
    for line in sec("Phases").splitlines():
        m = re.match(r"\d+\.\s*\**(\d{4}-\d\d-\d\d \d\d:\d\d) to ((?:\d{4}-\d\d-\d\d )?\d\d:\d\d) · ([^.*]+)\.\**\s*(.*)", line.strip())
        if m:
            end = m.group(2) if len(m.group(2)) > 5 else m.group(1)[:11] + m.group(2)
            phases.append({"start": m.group(1), "end": end, "title": m.group(3).strip(), "text": m.group(4).strip()})
    decs = []
    for b in re.split(r"(?m)^### ", sec("Decisions"))[1:]:
        head, _, body = b.partition("\n")
        hp = [x.strip() for x in head.split(" · ")]
        f = {k.lower(): v.strip() for k, v in re.findall(r"(?m)^- (Asked|Decided|Area|Done):\s*(.*)$", body)}
        decs.append({"time": hp[0], "session": hp[1] if len(hp) > 1 else "", "title": " · ".join(hp[2:]),
                     "asked": f.get("asked", ""), "decided": f.get("decided", ""), "area": f.get("area", ""), "done": f.get("done", "")})
    opens = [re.sub(r"^- ", "", l.strip()) for l in sec("Open").splitlines() if l.strip().startswith("- ")]
    return sessions, phases, decs, opens
A, B = parse("decisions-A.md"), parse("decisions-B.md")
names = [x["name"] for x in A[0] + B[0]]
def full(tok):
    tok = tok.strip()
    if tok == "all seven":                         # the seven Section sessions of log B
        return ", ".join(x["name"] for x in B[0])
    return next((n for n in names if n == tok or n.endswith("-" + tok) or re.search(r"-" + re.escape(tok) + r"(_|$)", n)), tok)
for d in A[2] + B[2]:
    d["session"] = ", ".join(full(t) for t in re.split(r",\s*|\s+and\s+", d["session"]) if t.strip())
data = {"sessions": A[0] + B[0], "phases": sorted(A[1] + B[1], key=lambda p: p["start"]),
        "decisions": sorted(A[2] + B[2], key=lambda d: d["time"]), "open": A[3] + B[3]}
print({k: len(v) for k, v in data.items()})
open("data.json", "w").write(json.dumps(data, ensure_ascii=False))
tpl = open("page.tpl.html", encoding="utf-8").read()
def render(mode=None):
    return (tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
               .replace("/*MODE*/null", json.dumps(mode)))
page = render()
open("../delivery/website/replay.html", "w", encoding="utf-8").write(page)   # a standalone local page: open it in a browser

# Studio topics, one per part of the replay: s01 who worked on what, s02.. one per day, then what is still open.
# A face is a Studio topic's (hai-studio new_topic.py): its fields, then Decided (sNN-DNN rows) and Open.
def face(nn, slug, title, covers, topic, decided=(), opened=(), body="", mode=None):
    name = f"s{nn:02d}-{slug}"
    head = f"s{nn:02d} · {title}"
    out = [head, "=" * len(head), "view: overview", "", "**At:** b41", "",
           "**Delivery type:** draft", "", f"**Covers:** {covers}", "", f"**Topic:** {topic}", ""]
    if body: out += [body, ""]
    out += ["", "Decided", "-------", ""]
    for k, (line, more) in enumerate(decided, 1):
        out += ["  \n".join([f"s{nn:02d}-D{k:02d} · {line}"] + more), ""]
    if opened:
        out += ["", "Open", "----", ""] + [f"{k}. {o}" for k, o in enumerate(opened, 1)] + [""]
    os.makedirs(f"../{name}", exist_ok=True)
    open(f"../{name}/{name}.md", "w", encoding="utf-8").write("\n".join(out))
    open(f"../{name}/{name}.html", "w", encoding="utf-8").write(render(mode))
    print(name, len(decided))

def row(d):
    more = []
    if d["asked"]: more.append(f"JL asked: {d['asked']}")
    if d["done"]: more.append(f"Built: {d['done']}")
    more.append(f"Session: {d['session']}" + (f" · {d['area']}" if d["area"] else ""))
    return (f"{d['time'][11:]} {d['title']}: {d['decided'] or d['title']}", more)

for p in glob.glob("../s[0-9][0-9]-*/"):          # rebuilt each time: a day or a part that is gone leaves no topic behind
    shutil.rmtree(p)
face(1, "sessions", "Who worked on what", "the eleven sessions, what each owned and when it ran",
     "Each Claude Code session wrote only in its own folders and messaged the others for the rest.",
     body="\n".join(f"- **{x['name']}**: {x['text']}" for x in data["sessions"]), mode={"view": "sessions"})
days = sorted({d["time"][:10] for d in data["decisions"]} | {p["start"][:10] for p in data["phases"]})
for i, day in enumerate(days, 2):
    dt = datetime.date.fromisoformat(day)
    ph = [p for p in data["phases"] if p["start"].startswith(day)]
    face(i, f"{dt.strftime('%b').lower()}{dt.day:02d}", f"{dt.strftime('%a %b')} {dt.day}",
         "; ".join(p["title"] for p in ph) or "decisions carried on from the day before",
         " ".join(f"{p['title']} ({p['start'][11:]} to {p['end'][11:]}). {p['text']}" for p in ph) or "Work carried on from the day before.",
         decided=[row(d) for d in data["decisions"] if d["time"].startswith(day)], mode={"view": "days", "day": day})
face(len(days) + 2, "still-open", "Still open", "what was asked or proposed and not settled by the end of the log",
     "Some of these may have been settled after the log ends.", opened=data["open"], mode={"view": "open"})

# The Block's own sections (workbench page/job_task_views/work_sections.py): board.md's ## Review Content and ## Findings embed these.
# Overview: the week and who worked; Findings: one file per decision Area, most decisions first, then what is open.
os.makedirs("review", exist_ok=True)
for p in glob.glob("review/*.md"):
    os.remove(p)
AREA_ICON = {"draft lab": "🧪", "paper text": "✍️", "process & coordination": "🤝", "review & scoring": "🔎",
             "evidence & displays": "📊", "page layout": "🖼️", "versions & delivery": "📦", "code quality": "🧹"}
def short(n):
    """A session's chip name, as the replay page wrote it."""
    if n.startswith("Pp-AgreeableRx"): return "Main paper"
    if n == "WorkBench-Paper-UI": return "Workbench UI"
    if n == "AgreeableRx-Appendix": return "Appendix"
    m = re.match(r"^AgreeableRx-(t\d\d)_(.+)$", n)
    return f"{m.group(1)} {m.group(2).replace('-', ' ').replace('_', ' ').capitalize()}" if m else n
def entry(d, when=None, area=True):
    """One decision as one row the workbench draws as a card: its time and title, then labelled lines (Session and Area
    become chips; Decided, JL asked and Built become blocks)."""
    more = [f"  - Decided: {d['decided'] or d['title']}"] + ([f"  - JL asked: {d['asked']}"] if d["asked"] else []) + \
           ([f"  - Built: {d['done']}"] if d["done"] else []) + \
           [f"  - Session: {', '.join(short(x.strip()) for x in d['session'].split(','))}"] + \
           ([f"  - Area: {d['area']}"] if area and d["area"] else [])
    return "\n".join([f"- **{when or d['time'][11:]}** · {d['title']}"] + more)
def session_row(x):
    """One session: its short name and role on the line; its full name and when it ran inside."""
    role = re.split(r";\s*first |;\s*\d{4}-", x["text"])[0].split(";")[0].strip().rstrip(".")
    span = re.search(r"first (\d{4}-\d\d-\d\d \d\d:\d\d), last (\d{4}-\d\d-\d\d \d\d:\d\d)", x["text"])
    ran = f" · {span.group(1)[5:10]} → {span.group(2)[5:10]}" if span else ""
    return "\n".join([f"- **{short(x['name'])}** · {role[:1].upper()}{role[1:]}{ran}", f"  - {x['name']}"]
                     + ([f"  - Ran {span.group(1)[5:]} → {span.group(2)[5:]}"] if span else []))
open("review/sessions.md", "w", encoding="utf-8").write("# 👥 Sessions\n\n" + "\n".join(map(session_row, data["sessions"])) + "\n")
week_rows = []
for day in sorted({d["time"][:10] for d in data["decisions"]} | {p["start"][:10] for p in data["phases"]}):
    dt = datetime.date.fromisoformat(day)
    titles = [p["title"] for p in data["phases"] if p["start"].startswith(day)]
    if not titles:                                   # no phase began that day: the one still running
        titles = [next(p["title"] for p in reversed(data["phases"]) if p["start"][:10] < day) + " (carried on)"]
    week_rows.append(f"- **{dt.strftime('%a %b')} {dt.day}** · " + " · ".join(titles))
open("review/week.md", "w", encoding="utf-8").write("# 🗓️ The week\n\n" + "\n".join(week_rows) + "\n")
TAKE, _at = {}, None                                 # src/takeaways.md: `## <area>` then `- line`, read first
for line in (open("takeaways.md", encoding="utf-8").read().splitlines() if os.path.exists("takeaways.md") else []):
    if line.startswith("## "):
        _at = line[3:].strip()
    elif line.startswith("- ") and _at:
        TAKE.setdefault(_at, []).append(line[2:].strip())
areas = {}
for d in data["decisions"]:
    areas.setdefault(d["area"] or "other", []).append(d)
for k, (area, ds) in enumerate(sorted(areas.items(), key=lambda a: -len(a[1])), 1):
    slug = re.sub(r"[^a-z0-9]+", "-", area.lower()).strip("-")
    title = f"{AREA_ICON.get(area, '📌')} {area[:1].upper()}{area[1:]}"
    lead = "\n".join(f"- {t}" for t in TAKE.get(area, []))
    open(f"review/area-{k:02d}-{slug}.md", "w", encoding="utf-8").write(
        f"# {title}\n\n" + (lead + "\n" if lead else "") + "- **📜 The decisions**\n"
        + "\n".join(entry(d, when=d["time"][5:], area=False) for d in ds) + "\n")
open("review/still-open.md", "w", encoding="utf-8").write(
    "# Still open\n\n" + "".join(f"- {t}\n" for t in TAKE.get("open", [])) + "- **🙋 Each open item**\n"
    + "\n".join(f"- 🙋 {o}" for o in data["open"]) + "\n")
# Plan + Results: one section per day, a timeline: each phase (one line that opens to its summary), then the decisions
# made in it; decisions before the day's first phase carry on from the phase before
def when(stamp, day):
    """A phase's end as the day's section reads it: HH:MM on the same day, else its weekday too (Mon 16:46)."""
    return stamp[11:] if stamp[:10] == day else datetime.date.fromisoformat(stamp[:10]).strftime('%a ') + stamp[11:]
for day in sorted({d["time"][:10] for d in data["decisions"]} | {p["start"][:10] for p in data["phases"]}):
    dt = datetime.date.fromisoformat(day)
    lines = [f"# 📅 {dt.strftime('%a %b')} {dt.day}", ""]
    ph = [p for p in data["phases"] if p["start"].startswith(day)]
    ds = [d for d in data["decisions"] if d["time"].startswith(day)]
    early = [d for d in ds if not ph or d["time"] < ph[0]["start"]]
    if early:                                        # after midnight, before the day's first phase: the one carried on
        before = [p for p in data["phases"] if p["start"][:10] < day]
        name = (before[-1]["title"] + " (carried on)") if before else "Before the first phase"
        lines += [f"- **{early[0]['time'][11:]} → {early[-1]['time'][11:]} · {name}**"] + [entry(d) for d in early]
    for k, p in enumerate(ph):
        end = p["end"][11:] if p["end"][:10] == day else p["end"][5:]
        lines += [f"- **{p['start'][11:]} → {when(p['end'], day)} · {p['title']}**", f"  - {p['text']}"]
        nxt = ph[k + 1]["start"] if k + 1 < len(ph) else "9999"
        lines += [entry(d) for d in ds if p["start"] <= d["time"] < nxt]
    open(f"review/day-{day}.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("review", len(areas) + 3)

# 🗺️ The map (the method of trace-canvas, github.com/CallSymmetryEcho/trace-canvas): one coloured line per session,
# one station per decision in time order, a decision two sessions share joins their lines, a shaded band per day.
# Drawn as a picture in the workbench's Overview, never a separate site.
def transit_map():
    """The week as a transit map, drawn by the workbench's own work_map.transit_svg: one line per session, a station
    per decision; a click opens the decision in the workbench pop-out."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../../plugins/haipipe-toolkit/servers/workbench/page"))
    from work_map import transit_svg
    names = sorted({n.strip() for d in data["decisions"] for n in d["session"].split(",")},
                   key=lambda n: (0 if n.startswith("Pp-") else 99 if n == "WorkBench-Paper-UI" else 50
                                  if n.endswith("Appendix") else 10 + int((re.search(r"t(\d\d)", n) or [0, 40])[1])))
    entries = [{"time": d["time"], "lanes": [n.strip() for n in d["session"].split(",")],
                "tip": f"{d['time'][5:]} · {d['title']}: {d['decided']}",
                "card": {"tm": d["time"][5:], "ti": d["title"],
                         "chips": [short(n.strip()) for n in d["session"].split(",")] + [d["area"]],
                         "blocks": [["Decided", d["decided"]], ["JL asked", d["asked"]], ["Built", d["done"]]]}}
               for d in data["decisions"]]
    return transit_svg([(n, short(n)) for n in names], entries, noun="decision", lane_noun="session")
open("review/map.svg", "w", encoding="utf-8").write(transit_map())
