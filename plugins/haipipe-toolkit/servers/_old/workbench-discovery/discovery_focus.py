"""The discovery theme's own parts on the shared work page (261106 plan, 261108). focus_page.py gives a discovery
Block, Job and Task the work shape (Report MindMap · Status · Findings; Work the same views, ⚙️ Process then 📊
Results) and asks this module, live.discovery_focus, for what discovery adds:

  parts          Findings, before 📦 Delivery: 📚 Papers, a side tab per Paper Run (its readout, reading depth, claim
                 support, citation check; a Card whose verification line says NEEDS is the waiting line under the closed
                 bar); 📖 Evidence Bib, a side tab per Task (its built bibex entries, and where it was handed over);
                 🧾 Synthesis, a side tab per Task that wrote summary.md, verdict.md or landscape.md
  status         a Task's Status: its Papers, Evidence Bib and Synthesis, then its Runs (a Task page has no Findings view);
                 a Block and a Job keep the shared bars
  headline       a Task's line in a Job's 📌 Headlines: its synthesis's first sentence, else its newest Paper Run's
  delivery_tabs  📦 Delivery's tabs: the Evidence Bib it hands over, then a shared lane (Models · Data · Website) only
                 when it holds files
  VIEW_SKILLS    the skills each view's work calls on (the rail's Skills)

Each part is (title, word, html, waits): a title in plain words with its emoji, the closed bar's state word, the body,
and the one line that waits on the person (""). Carries over the old Discovery page's Papers, Tasks and BibTeX
(discovery_views.py). Reads the folder contract of haipipe-discovery (ref/paper-run-contract.md). Read-only.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from live import frame
from live.discoveryboard import file_url, run_results
from live.frame import esc
from live.ui_parts import _kv, _side_tabs

CARD_LINE = re.compile(r"(?m)^- (cite|subject|venue|verification|citation verification|placeholder):[ \t]*(.+?)\s*$")
RUN_NAME = re.compile(r"^r\d{2,}_([a-z]+?)(\d{4})_(.+)$")
SYNTHESIS = ("summary.md", "verdict.md", "landscape.md")
DEPTH = {"abstract": "abstract read", "full-text": "full text read", "metadata-only": "metadata only"}
ENTRY = re.compile(r"(?m)^[ \t]*@(\w+)\s*[({]\s*([^,\s]+)\s*,")
CSS = """<style>
.dp-title{margin:0 0 6px;font-size:16px;line-height:1.45;font-weight:600;color:var(--ink);overflow-wrap:anywhere}
.dp-title .pb-pill{margin-left:8px;font-weight:400;vertical-align:2px}
.dp-you{color:var(--pb-you,#b35c00);font-weight:600}
.dp-entries{list-style:none;margin:6px 0 8px;padding:0!important;font-size:13.5px;line-height:1.45}
.dp-entries li{padding:5px 0;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.dp-entries li:last-child{border-bottom:0}
.dp-entries code{font-size:12.5px;margin-right:6px}
.dp-bib{max-height:260px;overflow:auto;margin:6px 0 0;padding:8px 10px;border:1px solid var(--line);border-radius:6px;
 font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.dp-syn h4{margin:12px 0 4px;font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.dp-syn h4:first-child{margin-top:0}
</style>"""

# the skills each view's work calls on (focus_page.page_skills reads it: the rail's Skills, 261106)
VIEW_SKILLS = {
    "findings": (("haipipe-discovery", "admits a paper as one numbered Run and builds the Evidence Bib"),
                 ("haipipe-discovery-review", "reads one paper into its Card, facts and Bib entry"),
                 ("haipipe-discovery-synthesize", "writes a Task's synthesis from its Results")),
    "standing": (("haipipe-discovery-inquiry", "moves a Task through scope, acquire, synthesize and close"),),
    "mindmap": (("haipipe-search", "finds the papers a Task may admit"),),
}


# ── what is on disk ─────────────────────────────────────────────────────────────────────────────────────────────
def _yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) if path.is_file() else {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _block_of(folder: Path, level: str) -> Path:
    return {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)


def tasks_of(folder: Path, root: Path, level: str) -> list:
    """The Task Pages a page answers for: a Block's through its Jobs, a Job's own, a Task itself."""
    inside = lambda p: root in p.resolve().parents
    if level == "Task":
        return [folder]
    jobs = [j for j in frame.children(folder, "Block") if inside(j)] if level == "Block" else [folder] if level == "Job" else []
    return [t for j in jobs for t in frame.children(j, "Job") if inside(t)]


def _section(text: str, name: str) -> str:
    m = re.search(rf"(?ms)^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", text)
    return " ".join(m.group(1).split("\n\n", 1)[0].split()) if m else ""


def label_of(run: str) -> str:
    """A Paper Run's name in words: r01_example2024_policy -> Example 2024 · policy."""
    m = RUN_NAME.match(run)
    if not m:
        return re.sub(r"^rp?\d+_", "", run).replace("_", " ")
    return f"{m.group(1).capitalize()} {m.group(2)} · {m.group(3).replace('_', ' ')}"


def paper(task: Path, run: str, result: Path) -> dict:
    """One Paper Run's Result: its Card's title, lines, readout and reuse; its receipt's status, reading and Bib check."""
    card = result / f"{run}.md"
    text = card.read_text(encoding="utf-8", errors="replace") if card.is_file() else ""
    lines = {k: v for k, v in CARD_LINE.findall(text)}
    rt = _yaml(result / "runtime.yaml")
    subject = rt.get("subject") if isinstance(rt.get("subject"), dict) else {}
    analysis = rt.get("analysis") if isinstance(rt.get("analysis"), dict) else {}
    bib = rt.get("bib") if isinstance(rt.get("bib"), dict) else {}
    checked = bib.get("verification") if isinstance(bib.get("verification"), dict) else {}
    title = re.search(r"(?m)^#\s+(.+)$", text)
    check = lines.get("verification") or lines.get("citation verification") or ""
    url = re.search(r"https?://[^\s)\]]+", lines.get("subject", "")) or None
    return {"run": run, "task": task, "result": result, "card": card if card.is_file() else None,
            "title": (title.group(1).strip() if title else str(subject.get("title") or run)),
            "cite": lines.get("cite", "").lstrip("@"), "venue": lines.get("venue") or str(subject.get("venue") or ""),
            "authors": str(subject.get("authors") or ""), "check": check,
            "needs": check.upper().startswith("NEEDS"), "verified": str(checked.get("status") or "pending"),
            "status": str(rt.get("status") or "no receipt"), "depth": str(analysis.get("reading_depth") or ""),
            "support": str(analysis.get("claim_support") or ""), "readout": _section(text, "Readout"),
            "reuse": _section(text, "Reuse"), "placeholder": bool(rt.get("placeholder")),
            "url": url.group(0) if url else str(subject.get("canonical_url") or ""),
            "bib": result / f"{run}.bib" if (result / f"{run}.bib").is_file() else None}


def papers_of(task: Path) -> list:
    """A Task's Paper Runs, in Run order: every runs/rNN_<author><year>_<slug>/result/ (or an older results/<run>/),
    never a Page Run (rpNN) or a collection Run."""
    return [paper(task, run, result) for run, result in run_results(task) if not run.startswith("rp")]


def paper_word(p: dict) -> str:
    """A paper's state word: its status unless complete; then whether it waits for you, is verified, or how deep it
    was read."""
    if p["status"] != "complete":
        return p["status"].replace("_", " ")
    if p["needs"]:
        return "waits for you"
    if p["verified"] == "verified":
        return "verified"
    return DEPTH.get(p["depth"], "read")


def bib_path(task: Path) -> Path:
    """The Task's derived Evidence Bib (paper_runs.default_bib_path): draft/evidence/bibex/<page stem>.bib, or outline/
    on an older Page."""
    page = str(_yaml(task / "discovery.yaml").get("page") or f"{task.name}.md")
    home = "outline" if (task / "outline").is_dir() and not (task / "draft").is_dir() else "draft"
    return task / home / "evidence" / "bibex" / f"{Path(page).stem}.bib"


def handed_over(task: Path) -> list:
    """The .bib files this Task handed over: under its address in its Block's delivery/ (haipipe-delivery)."""
    part = task.parent.parent / "delivery" / task.parent.name / task.name
    return sorted(part.rglob("*.bib")) if part.is_dir() else []


def _states(delivery: Path) -> dict:
    """{path under delivery/: its status} from delivery.md's rows (`… | \\`<path>\\` (vN, from …) | draft |`)."""
    table = delivery / "delivery.md"
    out = {}
    for line in table.read_text(encoding="utf-8", errors="replace").splitlines() if table.is_file() else []:
        m = re.search(r"`([^`\n]+)`[^|\n]*\|\s*(\w[\w ]*?)\s*\|\s*$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


# ── the parts ───────────────────────────────────────────────────────────────────────────────────────────────────
def _link(path: Path, root: Path, label: str, words: str) -> str:
    """A file in the pop-out: a .md in the reader, any other text through the Discovery reader, as itself otherwise."""
    block = next((p for p in [path, *path.parents] if (p / "board.md").is_file()), None)
    url = frame._file_url(path, root) if path.suffix == ".md" or block is None else (file_url(block, path, root)
                                                                                      or frame._file_url(path, root))
    return frame.pop(url, label, words)


def paper_panel(p: dict, root: Path, level: str) -> str:
    from live import focus_page as F
    read = " · ".join(x for x in (DEPTH.get(p["depth"], p["depth"]), f'claim {p["support"]}' if p["support"] else "") if x)
    check = (f'<span class=dp-you>{esc(p["check"])}</span>' if p["needs"] else esc(p["check"] or "not stated"))
    signed = "yes" if p["verified"] == "verified" else "not yet"            # only a person signs it, in runtime.yaml
    rows = [("Cite", f'<code>@{esc(p["cite"])}</code>' if p["cite"] else ""), ("Authors", esc(p["authors"])),
            ("Venue", esc(p["venue"])), ("Read", esc(read)), ("Citation check", check), ("Signed", signed),
            ("Reuse", esc(p["reuse"]))]
    if level != "Task":
        rows.append(("Task", f'<a href="{esc(F.page_url(p["task"], root))}">{esc(F.page_title(p["task"]))}</a>'))
    if p["status"] != "complete":
        rows.insert(0, ("Status", esc(p["status"])))
    links = [frame.pop(F.run_url(p["result"].parent if p["result"].name == "result" else p["result"], root),
                       f'{p["task"].name} · {p["run"]}', "Open the Run ↗")]
    if p["card"]:
        links.append(_link(p["card"], root, p["run"], "Card ↗"))
    if p["bib"]:
        links.append(_link(p["bib"], root, p["run"] + ".bib", "BibTeX ↗"))
    if p["url"]:
        links.append(f'<a href="{esc(p["url"])}" target=_blank rel=noopener>Source ↗</a>')
    return (f'<p class=dp-title>{esc(p["title"])}' + ('<span class=pb-pill>placeholder</span>' if p["placeholder"] else "")
            + '</p>' + (f'<p class=find-a>{esc(p["readout"])}</p>' if p["readout"] else "")
            + _kv(rows) + '<div class=find-verbs>' + " · ".join(links) + '</div>')


def papers_part(tasks: list, root: Path, level: str, key: str = "") -> tuple | None:
    """📚 Papers: a side tab per Paper Run, its state word; the first one that waits for a check under the closed bar."""
    papers = [p for t in tasks for p in papers_of(t)]
    if not papers:
        return None
    labels = [label_of(p["run"]) for p in papers]
    labels = [f"{x} ({p['task'].parent.name[:3]}.{p['task'].name[:3]})" if labels.count(x) > 1 else x
              for x, p in zip(labels, papers)]
    words = [paper_word(p) for p in papers]
    waiting = [x for x, p in zip(labels, papers) if p["needs"]]
    done = sum(p["status"] == "complete" for p in papers)
    word = (f"{len(waiting)} wait{'s' if len(waiting) == 1 else ''} for you" if waiting
            else "all read" if done == len(papers) else f"{done} of {len(papers)} read")
    waits = f"🙋 {waiting[0]}: its verification waits for you" if waiting else ""
    body = CSS + _side_tabs(f"dP{key}x", list(zip(labels, words)), [paper_panel(p, root, level) for p in papers])
    return ("📚 Papers", word, body, waits)


def _entries(text: str) -> list:
    """[(key, title, year)] of a Bib's entries, in file order."""
    out = []
    starts = [m for m in ENTRY.finditer(text) if m.group(1).lower() not in ("comment", "preamble", "string")]
    for m, nxt in zip(starts, starts[1:] + [None]):
        body = text[m.end(): nxt.start() if nxt else len(text)]
        field = lambda n: " ".join(re.sub(r"[{}]", "", (re.search(rf"(?is)\b{n}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*$", body, re.M)
                                                       or [None, ""])[1]).split())
        out.append((m.group(2), field("title"), field("year")))
    return out


def bib_panel(task: Path, root: Path) -> tuple:
    """(word, panel) of one Task's Evidence Bib: built from its complete Results, current or not, and handed over."""
    path = bib_path(task)
    want = sorted({p["cite"] for p in papers_of(task) if p["status"] == "complete" and p["cite"]})
    if not path.is_file():
        return ("not built" if want else "no Result yet",
                f'<p class=mut>{"Not built yet" if want else "No Result yet"}: paper_runs.py build-bib writes it from '
                'the complete Results.</p>')
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = _entries(text)
    have = sorted(k for k, _, _ in entries)
    word = "built" if have == want else "out of date"
    by_key = {p["cite"]: p["run"] for p in papers_of(task)}
    table = ('<ul class=dp-entries>' + "".join(                     # a list, not a table: it reads at phone width too
        f'<li><code>@{esc(k)}</code> {esc(t)}' + (f' ({esc(y)})' if y else "")
        + (f' <small>{esc(by_key[k][:3])}</small>' if by_key.get(k) else "") + '</li>' for k, t, y in entries) + '</ul>')
    delivery = task.parent.parent / "delivery"
    states = _states(delivery)
    sent = [f'{_link(f, root, f.name, f.name)} <small>{esc(states.get(f.relative_to(delivery).as_posix(), "handed over"))}</small>'
            for f in handed_over(task)]
    stale = ("" if word == "built" else
             f'<p class=dp-you>Out of date: its Results hold {", ".join("@" + k for k in want)}; rebuild it.</p>')
    return word, (stale + f'<div class=find-verbs>{_link(path, root, path.name, "Open " + path.name + " ↗")}'
                  + (" · Handed over: " + " · ".join(sent) if sent else "") + '</div>' + table
                  + f'<details class=find-more><summary>The BibTeX</summary><pre class=dp-bib>{esc(text.strip())}</pre></details>')


def bib_part(tasks: list, root: Path, key: str = "") -> tuple | None:
    """📖 Evidence Bib: a side tab per Task that has a Paper Run or a built Bib."""
    from live import focus_page as F
    held = [t for t in tasks if papers_of(t) or bib_path(t).is_file()]
    if not held:
        return None
    built = [bib_panel(t, root) for t in held]
    words = [w for w, _ in built]
    word = ("built" if all(w == "built" for w in words) else "out of date" if "out of date" in words
            else f'{words.count("built")} of {len(words)} built')
    return ("📖 Evidence Bib", word, CSS + _side_tabs(f"dB{key}x", [(F.page_title(t), w) for t, w in zip(held, words)],
                                                     [p for _, p in built]), "")


def synthesis_part(tasks: list, root: Path, key: str = "") -> tuple | None:
    """🧾 Synthesis: a side tab per Task that wrote one, the record itself (summary.md, verdict.md, landscape.md)."""
    from live import focus_page as F
    items, panels = [], []
    for t in tasks:
        found = [t / n for n in SYNTHESIS if (t / n).is_file()]
        if not found:
            continue
        kind = str(_yaml(t / "discovery.yaml").get("discovery_type") or found[0].stem).replace("-", " ")
        body = "".join((f'<h4>{esc(f.stem)}</h4>' if len(found) > 1 else "")   # its own # title: the tab names it
                       + F.markdown(re.sub(r"\A\s*# .*\n", "", f.read_text(encoding="utf-8", errors="replace")), t, root)
                       for f in found)
        items.append((F.page_title(t), kind))
        panels.append('<div class=find-verbs>' + " · ".join(_link(f, root, f.name, f.name + " ↗") for f in found)
                      + f'</div><div class=dp-syn>{body}</div>')
    if not items:
        return None
    word = "written" if len(items) == len(tasks) else f"{len(items)} of {len(tasks)} written"
    return ("🧾 Synthesis", word, CSS + _side_tabs(f"dS{key}x", items, panels), "")


def headline(task: Path, root: Path) -> str:
    """A Task's one line for a Job's 📌 Headlines (the shared Job Findings asks): its synthesis's first sentence
    (summary.md, verdict.md, landscape.md), else its newest Paper Run's headline, else ""."""
    from live import focus_page as F
    task = Path(task)
    for name in SYNTHESIS:
        f = task / name
        if not f.is_file():
            continue
        body = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8", errors="replace"), flags=re.S)
        for para in re.split(r"\n\s*\n", body):
            text = " ".join(re.sub(r"\*\*|`|^\s*(?:[-*]|\d+\.)\s+", "", ln).strip() for ln in para.splitlines()).strip()
            if text and not para.lstrip().startswith(("#", "|", "```", "<")):
                return re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0][:200]
    for run, result in reversed([(r, res) for r, res in run_results(task) if not r.startswith("rp")]):
        said = F.run_headline(result.parent if result.name == "result" else result)
        if said:
            return said
    return ""


def parts(folder: Path, root: Path, level: str) -> list:
    """The discovery Findings parts of a Block, Job or Task: [(title, word, html, waits)]."""
    folder, root = Path(folder).resolve(), Path(root).resolve()
    tasks = tasks_of(folder, root, level)
    key = re.sub(r"\W", "", folder.name)[:6]
    return [x for x in (papers_part(tasks, root, level, key), bib_part(tasks, root, key), synthesis_part(tasks, root, key)) if x]


def status(folder: Path, root: Path, level: str) -> list:
    """A Task's Status bars: its Papers, Evidence Bib and Synthesis (what its Runs returned), then its Runs (where each
    stands). A Block or a Job keeps the shared bars ([])."""
    if level != "Task":
        return []
    from live import focus_page as F
    folder, root = Path(folder).resolve(), Path(root).resolve()
    out = [(esc(t), w, h, x) for t, w, h, x in parts(folder, root, level)]
    runs = F.runs_section(folder, root)
    if runs:
        out.append((runs[0], runs[1], runs[2], ""))
    return out


def delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """📦 Delivery's tabs (JL 261108: "a Delivery lane written by a Run"): the Evidence Bib this page hands over, each
    file with its delivery.md status; then a shared lane only when it holds files. [(tab, word, panel)]."""
    from live import focus_page as F
    folder, root = Path(folder).resolve(), Path(root).resolve()
    rows, seen = [], set()
    for deliv, _ in F.delivery_sources(folder, root):
        block = next((p for p in [deliv, *deliv.parents] if (p / "board.md").is_file()), deliv.parent)
        states = _states(block / "delivery")
        for f in sorted(deliv.rglob("*.bib")):
            if f in seen:
                continue
            seen.add(f)
            rel = f.relative_to(block / "delivery").as_posix() if (block / "delivery") in f.parents else f.name
            small = " · ".join(x for x in (rel.rsplit("/", 1)[0] if "/" in rel else "", states.get(rel, "handed over")) if x)
            rows.append(f'<li>{_link(f, root, f.name, f.name)} <small>{esc(small)}</small></li>')
    bib = ("Evidence Bib", "ready" if rows else "nothing yet",
           f'<ul class=find-r>{"".join(rows)}</ul>' if rows else '<p class=mut>Nothing handed over yet.</p>')
    return [bib] + [t for t in F.delivery_tabs(folder, root) if t[1] != "nothing yet"]
