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
# A face is a Studio topic's (haipipe-studio new_topic.py): its fields, then Decided (sNN-DNN rows) and Open.
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

# The Block's own sections (workbench page/work_sections.py): board.md's ## Review Content and ## Findings embed these.
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
    order = sorted({n for d in data["decisions"] for n in [x.strip() for x in d["session"].split(",")]},
                   key=lambda n: (0 if n.startswith("Pp-") else 99 if n == "WorkBench-Paper-UI" else 50
                                  if n.endswith("Appendix") else 10 + int((re.search(r"t(\d\d)", n) or [0, 40])[1])))
    colours = ["#e4002b", "#0072ce", "#00a651", "#f68b1f", "#8e3a96", "#00a0b0", "#a6192e", "#5b6b7f", "#c99700",
               "#d0006f", "#2e7d32", "#6d4c41"]
    decs = data["decisions"]
    left, step, top, lane = 150, 9, 46, 34
    height = top + lane * len(order) + 44
    y = {n: top + lane * i + lane // 2 for i, n in enumerate(order)}
    x, at = [], left + 20
    for i, d in enumerate(decs):                             # a day is at least 84 px, so its name never overlaps
        if i and d["time"][:10] != decs[i - 1]["time"][:10]:
            first = next(k for k in range(i - 1, -1, -1) if k == 0 or decs[k - 1]["time"][:10] != decs[i - 1]["time"][:10])
            at = max(at + step, x[first] + 84)
        elif i:
            at += step
        x.append(at)
    width = x[-1] + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           'font-family="-apple-system,Segoe UI,sans-serif" font-size="12">']
    day_of = [d["time"][:10] for d in decs]
    k = 0
    while k < len(decs):                                     # one band per day, its name on top
        j = k
        while j < len(decs) and day_of[j] == day_of[k]:
            j += 1
        dt = datetime.date.fromisoformat(day_of[k])
        x0, x1 = x[k] - step / 2, (x[j] if j < len(decs) else x[j - 1] + step) - step / 2   # up to the next day
        shade = "#f3f5f8" if dt.day % 2 == 0 else "#ffffff"
        out.append(f'<rect x="{x0:.0f}" y="24" width="{x1 - x0:.0f}" height="{height - 24}" fill="{shade}"/>')
        out.append(f'<text x="{x0 + 4:.0f}" y="16" fill="#5f6368" font-weight="600">{dt.strftime("%a %b")} {dt.day}</text>')
        k = j
    for i, n in enumerate(order):                            # each session's line, from its first decision to its last
        xs = [x[t] for t, d in enumerate(decs) if n in [s.strip() for s in d["session"].split(",")]]
        c = colours[i % len(colours)]
        out.append(f'<text x="{left - 8}" y="{y[n] + 4}" text-anchor="end" fill="{c}" font-weight="600">'
                   f'{html.escape(short(n))}</text>')
        out.append(f'<line x1="{min(xs)}" y1="{y[n]}" x2="{max(xs)}" y2="{y[n]}" stroke="{c}" stroke-width="5" '
                   'stroke-linecap="round"/>')
    for i, n in enumerate(order):                            # its name again at its first station of each day, so a
        seen = set()                                         # reader scrolled to Friday still knows which line is which
        for t, d in enumerate(decs):
            if n in [s.strip() for s in d["session"].split(",")] and day_of[t] not in seen:
                seen.add(day_of[t])
                out.append(f'<text x="{x[t] - 3}" y="{y[n] - 8}" fill="{colours[i % len(colours)]}" font-size="10" '
                           f'font-weight="600">{html.escape(short(n))}</text>')
    for t, d in enumerate(decs):                             # a station per decision; a shared one is an interchange
        names = [s.strip() for s in d["session"].split(",") if s.strip() in y]
        tip = html.escape(f"{d['time'][5:]} · {d['title']}: {d['decided']}")
        if len(names) > 1:
            ys = sorted(y[n] for n in names)
            out.append(f'<rect x="{x[t] - 4}" y="{ys[0] - 5}" width="8" height="{ys[-1] - ys[0] + 10}" rx="4" '
                       f'fill="#fff" stroke="#1b1c1f" stroke-width="1.5"><title>{tip}</title></rect>')
        for n in names:
            out.append(f'<circle cx="{x[t]}" cy="{y[n]}" r="3.6" fill="#fff" stroke="#1b1c1f" stroke-width="1.3">'
                       f'<title>{tip}</title></circle>')
    ly = height - 14                                         # the legend: what a line and a station mean
    out.append(f'<g font-size="12" fill="#5f6368"><line x1="{left - 120}" y1="{ly - 4}" x2="{left - 96}" y2="{ly - 4}" '
               'stroke="#0072ce" stroke-width="5" stroke-linecap="round"/>'
               f'<text x="{left - 88}" y="{ly}">one session</text>'
               f'<circle cx="{left + 10}" cy="{ly - 4}" r="3.6" fill="#fff" stroke="#1b1c1f" stroke-width="1.3"/>'
               f'<text x="{left + 20}" y="{ly}">one decision (hover it)</text>'
               f'<rect x="{left + 176}" y="{ly - 13}" width="8" height="18" rx="4" fill="#fff" stroke="#1b1c1f" '
               f'stroke-width="1.5"/><text x="{left + 192}" y="{ly}">a decision sessions shared</text></g>')
    out.append("</svg>")
    return "\n".join(out)
open("review/map.svg", "w", encoding="utf-8").write(transit_map())
