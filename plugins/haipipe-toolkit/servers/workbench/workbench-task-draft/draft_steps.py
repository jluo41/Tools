"""The draft Task's seven step tabs, as b32 s41 draws them: Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise ·
Delivery, named the same in Work and Report (s41 Ⓐ; JL 261015: "So it is the Studio, 1, Plan, ..... and Delivery as
the last one").

Each tab is Operation over Result, as an items or building Task's Stages are (b15 s41, s42): Operation is what a
person does in the step (its Input, read from disk; the Sign it waits for; the prompt, which takes the person's notes
and is copied with them), Result is what the step made, one folded card per topic. Report shows the Results only.
Every open reads the files again, so the canvas and the tabs never drift apart (s41-D28): the newest draft
(`draft/<stem>-draft-v<N>.md`: its header, §1 Structure, §2 Scratch, §3 Draft), `draft/records/`, `draft/previous/`,
`evidence/cards.yaml` and `proposals.md` (haipipe-evidence), the Block's `studio/` topics that name this Task
(s41-D24), and the Block's `delivery/<jNN>/<tNN>/` (s41-D04). Nothing here writes.
"""
from __future__ import annotations

import datetime
import difflib
import importlib.util
import re
from pathlib import Path
from urllib.parse import quote, urlencode

from src.common import delivery_dir, delivery_read_lane_dir
from live.frame import ROUTE, _draw_url, _notes, _reader, _rel, _table, _topic_row, chain, esc, face, pop, studio_inventory, theme_of

# 4 · Display after 3 · Evidence (JL 261020: "Or we want to have a new display view after the 3 - Evidence? ... Please do it")
STEPS = ("Studio", "1 · Plan", "2 · Write", "3 · Evidence", "4 · Display", "5 · Revise", "Delivery")
SKILLS = Path(__file__).resolve().parents[3] / "skills"
RUBRIC = SKILLS / "1_base/draft/haipipe-draft-review/ref/evaluation-rubric.md"
VERSION = re.compile(r"-draft-v(\d+(?:\.\d+)*)\.md$")
# the face fields a Section's Story hands its plan (haipipe-paper-draft): the plan's frame before §1 exists
CONTRACT = ("reader-question", "entry-state", "exit-state", "must-establish", "must-refuse", "transition-out",
            "story-row")
CHIPS = {"done": '<span class="st st-ok">✓ done</span>', "next": '<span class="st st-warn">→ next</span>',
         "sign": '<span class="st st-warn">✍ sign</span>', "asked": '<span class="st st-warn">🔶 asked</span>',
         "send": '<span class="st st-warn">✍ send</span>', "optional": '<span class=st>· optional</span>',
         "pass": '<span class="st st-warn">🔁 pass {k}</span>',
         "todo": '<span class=st>· later</span>'}
INK = {"cite": "#1971c2", "value": "#7048e8", "need": "#e03131"}    # CITE blue, VALUE violet, needed red (s41-D07)


def _cards_module():
    """haipipe-evidence's cards.py (the card format, its order and checks), found from this file; None without it."""
    path = SKILLS / "1_base/evidence/haipipe-evidence/scripts/cards.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("haipipe_evidence_cards", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


CARDS = _cards_module()


# ── reading the Task's files ───────────────────────────────────────────────────────────────────
def _version(p: Path) -> tuple:
    m = VERSION.search(p.name)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def _header(text: str) -> dict:
    """The `key: value` lines between a file's title and its first `## ` part."""
    head = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = re.match(r"^([A-Za-z][\w-]*):[^\S\n]*(.*)$", line)
        if m:
            head[m.group(1).lower()] = m.group(2).strip()
    return head


def read_draft(folder: Path) -> dict:
    """The newest draft: its file, version, header and parts (§1 Structure, §2 Scratch, §3 Draft; a draft written
    without the numbered parts keeps its own parts as the text); {} when the Task has none."""
    d = folder / "draft"
    files = sorted((p for p in d.glob("*-draft-v*.md") if VERSION.search(p.name)), key=_version) if d.is_dir() else []
    if not files:
        return {}
    f = files[-1]
    text = f.read_text(encoding="utf-8", errors="replace")
    out = {"file": f, "version": "v" + VERSION.search(f.name).group(1), "head": _header(text),
           "structure": None, "scratch": None, "draft": None, "text": [], "notes": [],
           "previous": sorted((d / "previous").glob("*-draft-v*.md"), key=_version) if (d / "previous").is_dir() else []}
    for part in re.split(r"(?m)^## ", text)[1:]:
        title, _, body = part.partition("\n")
        title, body, low = title.strip(), body.strip(), title.strip().lower()
        key = ("structure" if re.match(r"1\s*·", title) or low.startswith("structure") else
               "scratch" if re.match(r"2\s*·", title) or low.startswith("scratch") else
               "draft" if re.match(r"3\s*·", title) else "")
        if key and out[key] is None:
            out[key] = (title, body)
        elif low.startswith("notes"):
            out["notes"].append((title, body))
        else:
            out["text"].append((title, body))
    if out["draft"]:
        out["text"] = [out["draft"]]
    return out


def _signed(d: dict) -> bool:
    return str(d.get("head", {}).get("approved", "")).startswith(("✅", "yes", "signed"))


def _paragraphs(body: str) -> list:
    """(paragraph, [(S<n>, role, words)]) for each `### ` paragraph of §1, the overview left out."""
    out, cur = [], None
    for line in body.splitlines():
        h = re.match(r"^###\s+(.*\S)", line)
        if h:
            cur = None if h.group(1).lower().startswith("structure overview") else (h.group(1), [])
            if cur:
                out.append(cur)
            continue
        b = re.match(r"^- B\d+ · (S\d+[a-z]*) · (?:\[([^\]]+)\]\s*)?(.*\S)", line)   # S3a: a split sentence
        if cur is not None and b:
            cur[1].append((b.group(1), b.group(2) or "", b.group(3)))
    return out


def _evidence(folder: Path) -> dict:
    """The Task's evidence/: its cards in narrative order, each item's state, the proposals, the problems."""
    ev = folder / "evidence"
    path = ev / "cards.yaml"
    out = {"path": path if path.is_file() else None, "cards": [], "proposals": [], "problems": [],
           "props_path": ev / "proposals.md" if (ev / "proposals.md").is_file() else None}
    if out["props_path"]:
        out["proposals"] = [(m.group(1) == "x", m.group(2).strip()) for m in re.finditer(
            r"(?m)^- \[([ x])\] (.*?)(?:<!--.*-->)?$", out["props_path"].read_text(encoding="utf-8", errors="replace"))]
    if not out["path"] or CARDS is None:
        return out
    try:
        cards = CARDS.order(CARDS.load(path))
    except Exception as e:                          # a card list that does not read: say so, never break the frame
        out["problems"] = [f"cards.yaml does not read: {e}"]
        return out
    try:
        project = CARDS.project_root(folder)
    except ValueError:
        project = None
    for card, label in cards:
        src, kind = card.get("source", ""), card.get("kind", "")
        try:
            title = card.get("title") or (CARDS.title_of(CARDS.resolve(project, kind, src)) if project and src else src)
        except Exception:
            title = src
        items = []
        for it in card.get("items", []):
            state, value = ("need", "") if it.get("need") else ("have", "")
            if it.get("run") and project:
                try:
                    res = CARDS.resolve(project, kind, f"{src}.{it['run']}")
                    if kind == "cite":
                        value = " · ".join(CARDS.paper(res))
                    elif it.get("key"):
                        value = CARDS.work_value(res, it["file"], it["key"])
                except Exception as e:
                    state, value = "missing", str(e)
            items.append({**it, "state": state, "value": value})
        out["cards"].append({"label": label, "kind": kind, "source": src, "title": title, "items": items})
    if project:
        try:
            out["problems"] = CARDS.check([c for c, _ in cards], project)
        except Exception as e:
            out["problems"] = [str(e)]
    return out


def _marks(ev: dict) -> dict:
    """Each anchor's words → (ink, the card names that back them): boxed in the text with the names beside them."""
    out = {}
    for c in ev["cards"]:
        for it in c["items"]:
            ink = INK["need"] if it["state"] != "have" else INK.get(c["kind"], INK["value"])
            for phrase in it.get("anchor") or []:
                prev = out.get(phrase, (ink, []))
                out[phrase] = (INK["need"] if INK["need"] in (prev[0], ink) else ink,
                               prev[1] + ([c["label"]] if c["label"] not in prev[1] else []))
    return out


def _studio_topics(folder: Path, root: Path) -> list:
    """(source, topic, drawings) for each Block Studio topic whose face names this Task (s41-D24). A face that names
    Tasks by their Job (`jNN_…/tNN_…`) counts only for those, since two versions often share a Section's name
    (j01_…/t01_introduction and j02_…/t01_introduction); a face that names no Job counts by the Task's name."""
    block = chain(folder, root).get("Block")
    if not block:
        return []
    path = folder.resolve().relative_to(block.resolve()).as_posix()
    out = []
    for source, topic, drawings in studio_inventory(block, root):
        md = _notes(topic)
        text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
        named = {m.rstrip("/") for m in re.findall(r"j\d{2}_[\w.-]+/t\d{2}_[\w.-]+", text)}
        if (path in named) if named else folder.name in text:
            out.append((source, topic, drawings))
    return out


def _delivery_rows(folder: Path, root: Path) -> list:
    """The Block's delivery/delivery.md rows that name this Task's part or its draft: (date, for, status)."""
    block = chain(folder, root).get("Block")
    md = block / "delivery" / "delivery.md" if block else None
    if not md or not md.is_file():
        return []
    part = delivery_dir(folder).relative_to(block / "delivery").as_posix()
    rows = []
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and (part in line or folder.name in line) and not set(cells[0]) <= set("-: "):
            rows.append((cells[0], cells[1], cells[-1]))
    return rows


# ── the look: the items and building Tasks' boxes (b15 s41, s42), drawn here so a base type needs no theme ───────
def _kv(rows) -> str:
    """A name/value table, the names in a shaded column that does not wrap."""
    cell = "padding:5px 10px;border:1px solid var(--line);vertical-align:top"
    body = "".join(f'<tr><th style="{cell};background:var(--wash);font-weight:600;text-align:left;white-space:nowrap;'
                   f'width:1%">{k}</th><td style="{cell};overflow-wrap:anywhere">{v}</td></tr>' for k, v in rows)
    return f'<table style="border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:14px"><tbody>{body}</tbody></table>'


def _fold(title: str, body: str, open_: bool = False) -> str:
    """A Result card: its title, folded until opened."""
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head>'
            f'<b>{esc(title)}</b></span></summary><div class=work-body style="max-height:85vh;overflow-y:auto">'
            f'{body}</div></details>')


def _not_yet(what: str) -> str:
    return f"<p class=space-empty>{esc(what)}</p>"


def _part(name: str) -> str:
    return f'<h3 style="margin:18px 0 6px">{name}</h3>'


def _code(path: Path | None, root: Path) -> str:
    """A file as a link to the Page reader, or a dash."""
    return pop(_reader(path, root), path.name, f"{path.name} ↗") if path and path.is_file() else '<span class=mut>—</span>'


def _task_session(folder: Path, root: Path) -> str:
    """A Task's own session name, read from its folders: `<Board>: <job>-<task>`, the Job's date stamp left out, e.g.
    `Paper-LLMRecPhy-Quick: j01-jamaim-full-t01-introduction` (JL 261020: "Paper-LLMRecPhy-Quick: j01jamaim-full-t01-intro")."""
    c = chain(folder, root)
    slug = lambda f: re.sub(r"_v\d{4}(?=_|$)", "", f.name).replace("_", "-")
    name = "-".join(([slug(c["Job"])] if c.get("Job") else []) + [slug(folder)])
    return f'{c["Block"].name}: {name}' if c.get("Block") else name


def _session(folder: Path, root: Path) -> str:
    """The Claude Code session this Task's work runs in, one per Task, shared by all its step prompts (JL 261020:
    "这个是 introduction，就要专门为 introduction 开一个 session ... 这些 task 应该 share 一个 session"): the Task
    face's `session:` line, else the Task's own name; never its Job's, which names the whole version."""
    md = face(folder)
    name = _header(md.read_text(encoding="utf-8", errors="ignore")).get("session", "") if md else ""
    return name.strip() or _task_session(folder, root)


def _prompt_box(prompt: str, folder: Path, root: Path, key: str, title: str = "Prompt") -> str:
    """The prompt, yours to add to (b15 s41-D14): what you type under it is copied with it as `user feedback:`; it
    stays in this browser until you copy it. Last come the lines that send it to the Task's session (`session:` on
    its face or its Job's), so pasted into any session it still runs where this Task's work lives (JL 261020: "every
    time I copy it, and I paste it to any session, it will trigger that session to work")."""
    k = f"{_rel(folder, root)}#{key}"
    who = _session(folder, root)
    # where it runs, said once: a session knows how to reach or start another (JL 261020: "没有必要说那么详细 ...
    # 你就直接说我要靠这个 call session 去干什么"), so the Task's own session gets it the first time too
    tail = f'Run this in the Claude session "{who}"; start it if it is not running.' if who else ""
    return (f'<details class=run-prompt-box open><summary>{esc(title)} '
            f'<button type=button class="run-copy work-act" data-copy="{esc(prompt)}"'
            + (f' data-tail="{esc(tail)}"' if tail else "") + '>Copy prompt</button></summary>'
            f'<pre class=run-prompt style="margin-bottom:0;border-bottom-left-radius:0;border-bottom-right-radius:0">'
            f'{esc(prompt)}</pre>'
            '<label style="display:block;margin:0;padding:4px 10px 0;background:var(--wash)">'
            '<code>user feedback:</code></label>'
            f'<textarea class=run-notes rows=3 data-key="notes:{esc(k)}" placeholder="notes, a row, a sentence to change" '
            'style="width:100%;box-sizing:border-box;margin:0;border:1px solid var(--line);border-top:0;'
            'background:var(--wash);font:13px/1.45 ui-monospace,Menlo,monospace;padding:6px 10px"></textarea>'
            + (f'<pre class=run-prompt style="margin:0;border-top:0;border-top-left-radius:0;border-top-right-radius:0;'
               f'color:var(--mut);white-space:pre-wrap">{esc(tail)}</pre>' if tail else "") + '</details>')


def _editor(folder: Path, root: Path, title: str, view: str = "revise", open_: bool = True) -> str:
    """Your own changes, typed in place: the Page's Revise boxes (outline_revise.py, one box per paragraph, its
    sentences a line each, Why · Reset · Save into `## 3 · Draft`), embedded and open (JL 261020: "How could I write
    my own changes? that is my question"; "it is kind of hard to me to modify the content, right?")."""
    src = _editor_src(folder, root, view)
    if not src:
        return ""
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head>'
            f'<b>{esc(title)}</b></span><span class=topic-pop>{pop(src.replace("&embed=1", ""), title, "↗")}</span>'
            f'</summary><iframe class=space-frame title="{esc(title)}" src="{esc(src)}" style="{FIT_STYLE}" onload="{FIT}">'
            '</iframe></details>')


def _editor_src(folder: Path, root: Path, view: str = "revise") -> str:
    """The Page's own editor for this Task's draft, embedded: its Revise boxes, or its Scratch; or "" with no Block."""
    block, md = chain(folder, root).get("Block"), face(folder)
    if not block or not md or not face(block):
        return ""
    return "/_board/draft?" + urlencode({"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(),
                                         "embed": "1", "space": "bullet", "view": view})


# the frame as tall as what it holds, no inner scroll, no border (JL 261020 on 5 · Revise, then 4 · Revise: "The UI here is still not
# good"): it follows its page as you type or open a Scratch note
FIT_STYLE = "height:160px;min-height:0;border:0"
FIT = ("(function(f){try{var d=f.contentDocument,fit=function(){f.style.height=(d.body.scrollHeight+8)+'px';};"
       "fit();new f.contentWindow.ResizeObserver(fit).observe(d.body);}catch(e){}})(this)")


def _step_box(title: str, state: str, body: str, open_: bool = False, k: int = 0) -> str:
    # every Operation folded until opened, its chip still saying where the step is (JL 261020: "please make all the
    # operation to be hidden by default")
    return (f'<details class="topic work-task items-step"{" open" if open_ else ""}><summary>'
            f'<span class=related-head><b>{esc(title)}</b> {CHIPS[state].format(k=k + 1)}</span></summary>'
            f'<div class=work-body>{body}</div></details>')


def _inline(text: str, marks: dict) -> str:
    """One line of Markdown as read: **bold**, `code`, each ⟦pending⟧ mark in red, each evidence anchor boxed in
    its card's ink with the card names beside it (s41-D07: "highlight it as well, and link it to the Evidence card")."""
    s, held = esc(text), []
    for phrase, (ink, labels) in sorted(marks.items(), key=lambda kv: -len(kv[0])):
        p = esc(phrase)
        if p in s:
            held.append(f'<mark style="background:{ink}1f;border:1px solid {ink}66;border-radius:3px;padding:0 2px;'
                        f'color:inherit">{p}</mark><sup style="color:{ink};font-weight:600"> {esc(", ".join(labels))}</sup>')
            s = s.replace(p, f"\x00{len(held) - 1}\x00")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"⟦([^⟧]*)⟧", r'<span style="color:#e03131;font-weight:600">⟦\1⟧</span>', s)
    return re.sub("\x00(\\d+)\x00", lambda m: held[int(m.group(1))], s)


def _sentence(item: str, marks: dict) -> str:
    """A §3 line, `B1 · S1 · text`: its sentence number small and grey, then the sentence."""
    m = re.match(r"^B\d+ · (S\d+[a-z]*) · (.*)$", item)
    return (f'<span class=mut style="font-size:12px">{esc(m.group(1))}</span> {_inline(m.group(2), marks)}' if m
            else _inline(item, marks))


def _md(text: str, marks: dict) -> str:
    """A part of the draft as a reader sees it: paragraphs, ### headings and lists."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        while lines and lines[0].startswith("#"):
            h = lines.pop(0).lstrip("#").strip()
            p_ = re.match(r"(C\d+\.P\d+)\b", h)
            out.append(f'<h4{(" data-p=" + chr(34) + p_.group(1) + chr(34)) if p_ else ""} style="margin:12px 0 4px">'
                       f'{_inline(h, marks)}</h4>')
        if not lines:
            continue
        if re.match(r"^\s*(?:[-*]|\d+\.)\s", lines[0]):
            items = []
            for line in lines:
                if re.match(r"^\s*(?:[-*]|\d+\.)\s", line):
                    items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s", "", line))
                elif items:
                    items[-1] += " " + line.strip()
            out.append("<ul>" + "".join(
                f'<li{(" data-s=" + chr(34) + m.group(1) + chr(34)) if (m := re.match(r"^B[0-9]+ · (S[0-9]+[a-z]?) · ", i)) else ""}>'
                f"{_sentence(i, marks)}</li>" for i in items) + "</ul>")
        else:
            out.append(f'<p style="line-height:1.6">{_inline(" ".join(x.strip() for x in lines), marks)}</p>')
    return "".join(out)


def _source(path: Path | None, root: Path, empty: str) -> str:
    """A Markdown file shown as it is, with a link to the Page reader; or why there is none."""
    if not path or not path.is_file():
        return f'<p class=space-empty>{esc(empty)}</p>'
    return (f'<p class=space-reads>{pop(_reader(path, root), path.name, _rel(path, root) + " ↗")}</p>'
            f'<pre class=space-source>{esc(path.read_text(encoding="utf-8", errors="replace"))}</pre>')


LANE_ICON = {"web": "🌐", "latex": "📄", "word": "📝", "slide": "🖥", "render": "🖼"}


def delivery_cards(folder: Path, root: Path, md: Path | None) -> str:
    """One card per kind of delivery (JL 261007: "each card is a type of delivery … the card and the preview of the
    results, the embedded content"), from the Page's own read-only check (workbench-task-draft/delivery.py
    check_delivery). Its head: the kind, its state (current · stale · not built), its files as ↗ links; its body:
    the result embedded (the web page, the PDF, Word through the PDF twin the build writes beside the .docx, the
    deck), a LaTeX piece with no PDF yet shown as it is, or "not built yet: run Build"."""
    stem = md.stem if md else folder.name
    try:
        from live.delivery import check_delivery
        lanes = check_delivery(md).get("lanes", []) if md else []
    except Exception:                               # no Page engine: no cards, never no page
        lanes = []
    url = lambda f: "/" + quote(_rel(f, root))
    cards = []
    for lane in lanes:
        key = lane.get("lane", "")
        ldir = delivery_read_lane_dir(folder, key)
        files = sorted(f for f in ldir.rglob("*") if f.is_file() and not f.name.startswith(".")) if ldir.is_dir() else []
        state = lane.get("state", "")
        legacy_note = ('<p class="mut dl-note">Old local output: read only; rebuild from source into Block Delivery.</p>'
                       if lane.get("legacy") else "")
        mark = {"pass": "st-ok", "stale": "st-warn"}.get(state, "mut")
        word = {"pass": "current", "stale": "stale", "not-built": "not built"}.get(state, state)
        show = {"web": [ldir / "index.html"], "latex": [ldir / f"{stem}.pdf"], "word": [ldir / f"{stem}.pdf"],
                "slide": [ldir / f"{stem}-deck.html"]}.get(key, [f for f in files if f.suffix in (".pdf", ".html")][:1])
        shown = next((f for f in show if f.is_file()), None)
        links = " · ".join(pop(url(f), f.name, f.relative_to(ldir).as_posix()) for f in files)
        head = (f'<div class=st-bar><span><b>{LANE_ICON.get(key, "")} {esc(lane.get("label", key))}</b> '
                f'<span class={mark}>{esc(word)}</span></span><span class=mut>{links}</span></div>')
        if shown:
            body = f'<iframe class=dl-frame loading=lazy title="{esc(shown.name)}" src="{esc(url(shown))}"></iframe>'
        elif key == "latex" and (ldir / f"{stem}.tex").is_file():     # no PDF compiled yet: the piece itself
            body = (f'<p class="mut dl-note">{esc(stem)}.pdf is not compiled yet; the piece:</p>'
                    f'<pre class="space-source dl-src">{esc((ldir / f"{stem}.tex").read_text(encoding="utf-8", errors="replace"))}</pre>')
        elif files:
            body = '<p class="mut dl-note">built; no preview for this kind yet</p>'
        else:
            body = '<p class="mut dl-note">not built yet: run Build</p>'
        cards.append(f'<div class=topic>{head}{legacy_note}{body}</div>')
    return ("<h2>Deliveries</h2>" + "".join(cards) if cards else
            '<p class=space-empty>Nothing built yet: delivery/ holds no files. Run Build.</p>')


# ── the seven steps ─────────────────────────────────────────────────────────────────────────────
def _section(folder: Path, md: Path | None) -> str:
    """The Section's own name: its face's heading after the tag (t00_abstract · Abstract → Abstract)."""
    title = next((line[2:].strip() for line in md.read_text(encoding="utf-8", errors="ignore").splitlines()
                  if line.startswith("# ")), "") if md else ""
    return title.split(" · ", 1)[1].strip() if " · " in title else (title or folder.name)


def _built(folder: Path) -> list:
    out = delivery_dir(folder)
    return [f for f in out.rglob("*") if f.is_file() and not f.name.startswith(".") and "render" not in
            f.relative_to(out).parts] if out.is_dir() else []


def _pages(folder: Path) -> list:
    """The newest rendered version's page pictures, `render/<name>-v<N>/p-<k>.png` (haipipe-delivery word_round)."""
    render = delivery_dir(folder) / "render"
    dirs = sorted((d for d in render.iterdir() if d.is_dir()), key=lambda d: d.stat().st_mtime) if render.is_dir() else []
    return sorted(dirs[-1].glob("p-*.png"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0)) if dirs else []


def facts(folder: Path, root: Path) -> dict:
    """Everything the seven steps read, once per open."""
    md = face(folder)
    d = read_draft(folder)
    ev = _evidence(folder)
    rows = _delivery_rows(folder, root)
    status = [r[2].lower() for r in rows]
    stem = md.stem if md else folder.name
    records = folder / "draft" / "records"
    return {"md": md, "stem": stem, "head": _header(md.read_text(encoding="utf-8", errors="ignore")) if md else {},
            "section": _section(folder, md), "t": _rel(folder, root), "draft": d, "ev": ev,
            "topics": _studio_topics(folder, root), "built": _built(folder), "pages": _pages(folder),
            "displays": _displays(folder, d),
            "rows": rows, "sent": "sent" in status, "back": "back" in status,
            "records": sorted(records.glob("*.md")) if records.is_dir() else [],
            "revise": records / f"{stem}-revise.md", "feedback": records / f"{stem}-feedback.md",
            "context": records / f"{stem}-context.md", "requirement": records / f"{stem}-requirement.md"}


def states(f: dict) -> dict:
    """Each step's chip, from the files: done, next, waiting on a person (sign, send), asked, optional or later."""
    d, ev = f["draft"], f["ev"]
    written = bool(d and d["text"])
    needed = any(it["state"] != "have" for c in ev["cards"] for it in c["items"])
    open_asks = any(not ticked for ticked, _ in ev["proposals"])
    return {"Studio": "done" if f["topics"] else "optional",
            "1 · Plan": ("done" if _signed(d) else "sign") if d and d["structure"] else "next",
            "2 · Write": "done" if written else ("next" if d and d["structure"] else "todo"),
            "3 · Evidence": (("asked" if needed or open_asks or any(o["kind"] != "none" for o in _open_points(d))
                              else "done") if ev["cards"] else
                             "next" if written or (d and d["structure"]) else "todo"),
            # a display waits on a person to accept it; a Section that calls none needs none
            "4 · Display": (("done" if all(x["ok"] for x in f["displays"]) else
                             "sign" if all(x.get("built") for x in f["displays"]) else "next" if written else "todo")
                            if f["displays"] else "optional"),
            "5 · Revise": ("pass" if d.get("previous") or f["revise"].is_file() else "next") if written else "todo",
            "Delivery": (("done" if f["sent"] else "send") if f["built"] else "next" if written else "todo")}


def current(st: dict) -> str:
    """The tab a bare link opens: the first step that waits on a person or comes next; the Studio is optional."""
    return next((s for s in STEPS[1:] if st[s] in ("next", "sign", "send")), STEPS[1])


def _drawn_inside(f: dict) -> set:
    """The topics another topic of this Task draws inside its own canvas (its face's `examples:`), so a tab shows
    them once, there (JL 261020, of s22 and s26: "should we merge them into the same one to save space?")."""
    import os
    out = set()
    for _, topic, _ in f["topics"]:
        md = _notes(topic)
        m = re.search(r"(?m)^\s*examples:\s*(\S+)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
        if m:
            out.add(Path(os.path.normpath(topic / m.group(1))))
    return out


def _topic_rows(f: dict, root: Path) -> str:
    inside = _drawn_inside(f)
    return "".join(_topic_row(t, dr, root, source) for source, t, dr in f["topics"] if t not in inside)


def _studio(f: dict, folder: Path, root: Path, st: str) -> tuple:
    block = chain(folder, root).get("Block")
    theme = theme_of(folder, root)
    studio = (ROUTE + "?" + urlencode({"path": _rel(block, root), **({"theme": theme} if theme != "vanilla" else {}),
                                       "studio": "1"})) if block else ""
    names = " · ".join(t.name for _, t, _ in f["topics"])
    topic = esc(names) if names else '<span class=mut>none yet</span>'
    related = block / "related" / "related.md" if block else None
    rows = [("Task", f'<code>{esc(folder.name)}</code> · {esc(f["section"])}'), ("Topic", topic),
            ("Related", _code(related, root)), ("Chat", esc(f["head"].get("session") or "Claude or Codex, this Task"))]
    sid = f["topics"][0][1].name.split("-", 1)[0] if f["topics"] else "a new topic"
    prompt = (f"/haipipe-studio {_rel(block, root) if block else f['t']} {sid}: talk with me about {f['section']}'s "
              f"argument and sketch it on the canvas; write no text yet; what we settle goes into the Task's §1.")
    op = _step_box("🎨 Studio · talk and sketch", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "studio"))
    # each topic its own card, not cards in a "logic sketch" box (JL 261020: "I want this to be of the item itself,
    # not box of box")
    result = ((_topic_rows(f, root) if f["topics"] else _not_yet(f"No Studio topic for {folder.name} yet."))
              + (f'<p>{pop(studio, "the Block Studio", "Open the Block Studio ↗")}</p>' if studio else ""))
    run = {"label": "run-draw-<sNN>", "doing": "talk and sketch", "prompt": prompt, "skills": ["haipipe-studio"]}
    return op, result, (run,)


def _plan_tree(body: str) -> tuple:
    """§1 as its mind map reads it: ([(C<n>, its name)], {paragraph: the question it hands on}, [(paragraph, its job,
    [(S<n>, role, words, note)])]). The names and questions come from the Structure Overview's `- C2 · …` and
    `→ C1.P2: …` lines."""
    parts, asks, paras, cur, last, para = [], {}, [], None, None, None
    for line in body.splitlines():
        h = re.match(r"^###\s+(.*\S)", line)
        if h:
            p_ = h.group(1).split(" · ", 1)
            cur = None if h.group(1).lower().startswith("structure overview") else (p_[0], p_[-1], [])
            if cur:
                paras.append(cur)
            continue
        if cur is None:                                  # the overview: each part's name, each paragraph's hand-on
            c = re.match(r"^- (C\d+) · (.*\S)", line)
            p_ = re.match(r"^- (C\d+\.P\d+) · ", line)
            q = re.match(r"^\s+→ C\d+\.P\d+:\s*(.*\S)", line)
            if c:
                parts.append((c.group(1), c.group(2)))
            para = p_.group(1) if p_ else para
            if q and para:
                asks[para] = q.group(1)
            continue
        b = re.match(r"^- B\d+ · (S\d+[a-z]*) · (?:\[([^\]]+)\]\s*)?(.*\S)", line)
        n = re.match(r"^\s+Note:\s*(.*\S)", line)
        if b:
            last = [b.group(1), b.group(2) or "", b.group(3), ""]
            cur[2].append(last)
        elif n and last and cur[2] and cur[2][-1] is last:
            last[3] = n.group(1)
    return parts, asks, paras


def _plan_map(d: dict, ev: dict, section: str, task: str = "") -> str:
    """§1 drawn as a mind map (JL 261020: "merge them together, how do you think you can draw the mind map for the plan?
    ... To show what is this paper about?"): the Section and its arc in the middle; its parts (C1, C2, …) when it has
    more than one; its paragraphs, with the question each hands to the next on the arrow between them; each Bullet a
    leaf with its role and its evidence cards. A Bullet's note shows on hover; a ⟦check⟧ in it shows in red."""
    parts, asks, paras = _plan_tree(d["structure"][1])
    cards = {}
    for c in ev["cards"]:
        for it in c["items"]:
            ink = INK["need"] if it["state"] != "have" else INK.get(c["kind"], INK["value"])
            for k in it.get("for") or []:                  # 6, "6b" and "S6b" all name S6b's sentence
                got = cards.setdefault("S" + str(k).lstrip("S"), {})
                got[c["label"]] = INK["need"] if INK["need"] in (got.get(c["label"]), ink) else ink

    def para_html(i, pid, job, bullets):
        leaves = []
        for s, role, words, note in bullets:
            flag = re.search(r"⟦[^⟧]*⟧", note)
            flag = f' <span class=pm-flag>{esc(flag.group(0))}</span>' if flag and flag.group(0) not in words else ""
            chips = "".join(f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(lab)}</span>'
                            for lab, ink in cards.get(s, {}).items())
            leaves.append(f'<li data-s="{esc(s)}"{(" title=" + chr(34) + esc(note) + chr(34)) if note else ""}>'
                          f'<span class=pm-s draggable=true>{esc(s)}</span>{_editable("role", role, esc(role), "span class=pm-role")}'
                          f'<span class=pm-w>{_editable("words", words, _inline(words, {}), "span class=pm-t")}'
                          f'{flag}{chips}</span></li>')
        # a point or a paragraph added where it goes (JL 261020: "How could I add the P here or add the S here?")
        leaves.append('<li class=pm-add><button type=button class=pm-plus data-add=point>＋ point</button></li>')
        ask = (f'<div class=pm-q>{_editable("ask", asks.get(pid, ""), esc(asks.get(pid, "")), "span", pid)}</div>'
               if i < len(paras) - 1 else "")
        return (f'<div class=pm-para data-p="{esc(pid)}"><div class="pm-node pm-pnode"><span class=pm-id>{esc(pid)}</span>'
                f'{_editable("para", job, esc(job), "b")}</div><ul class=pm-leaves>{"".join(leaves)}</ul></div>{ask}'
                f'<div class=pm-addp><button type=button class=pm-plus data-add=para data-after="{esc(pid)}">＋ paragraph'
                '</button></div>')

    one = len(parts) <= 1
    name = f"{parts[0][0]} · {parts[0][1]}" if one and parts else section
    arc = d["head"].get("arc") or ""
    body = []
    if one:
        body = [para_html(i, *p) for i, p in enumerate(paras)]
    else:
        for cid, cname in parts:
            mine = [(i, p) for i, p in enumerate(paras) if p[0].split(".")[0] == cid]
            if mine:
                body.append(f'<div class=pm-part><div class="pm-node pm-cnode"><span class=pm-id>{esc(cid)}</span>'
                            f'<b>{esc(cname)}</b></div><div>{"".join(para_html(i, *p) for i, p in mine)}</div></div>')
    # editable in place where it is read (JL 261020: "how could I operate and edit it?"): plan_act writes §1
    return (PLAN_CSS + f'<div class=pm-edit data-task="{esc(task)}" data-file="{esc(d["file"].name)}">'
            '<span class=pm-msg role=status></span><div class=pm><svg class=pm-wires aria-hidden=true></svg>'
            f'<div class="pm-node pm-root"><b>{esc(name)}</b>' + (_editable("arc", arc, esc(arc), "p") if arc else "")
            + f'</div><div>{"".join(body)}</div></div></div>' + PLAN_JS)


def _editable(what: str, raw: str, shown: str, tag: str, p: str = "") -> str:
    """One piece of the map a person types into: it shows `shown`, and while typed in, its words as written."""
    name = tag.split()[0]
    return (f'<{tag} data-edit={what}{(" data-p=" + chr(34) + esc(p) + chr(34)) if p else ""} '
            f'data-raw="{esc(raw)}" contenteditable=plaintext-only spellcheck=false>{shown}</{name}>')


PLAN_CSS = """<style>
/* the map grows to its widest Point and its box scrolls sideways; a Point never wraps (JL 261021: "怎么让这个 structure
   的宽度能够无限延伸 ... 我就是想让它一直不要有这个 break") */
.pm{position:relative;display:grid;grid-template-columns:250px auto;gap:0 64px;align-items:center;padding:8px 4px;
 width:max-content;min-width:100%;box-sizing:border-box}
.pm-wires{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}
.pm-wires path{fill:none;stroke:var(--mut);stroke-opacity:.45;stroke-width:1.4}
.pm-node{position:relative;background:var(--card);border:1.5px solid var(--fg);border-radius:10px}
.pm-root{padding:14px 16px;font-size:13px;line-height:1.5}.pm-root b{display:block;font-size:17px;margin-bottom:6px}
.pm-root p{margin:0;color:var(--mut)}
.pm-para{display:grid;grid-template-columns:230px auto;gap:0 56px;align-items:center;margin:4px 0}
.pm-pnode,.pm-cnode{padding:9px 12px;font-size:14.5px;line-height:1.35}.pm-id{display:block;font-size:11.5px;color:var(--mut)}
.pm-part{display:grid;grid-template-columns:180px auto;gap:0 48px;align-items:center;margin:8px 0}
.pm-part .pm-para{grid-template-columns:210px auto;gap:0 48px}.pm-part .pm-q{width:210px}
.pm-leaves{list-style:none;margin:0;padding:0}
.pm-leaves li{position:relative;padding:3px 0;line-height:1.5;font-size:14px;white-space:nowrap}
.pm-s{display:inline-block;min-width:30px;font-size:12px;color:var(--mut)}
.pm-role{display:inline-block;min-width:86px;box-sizing:border-box;text-align:center;margin-right:7px;padding:0 6px;border:1px solid var(--line);border-radius:9px;font-size:11.5px;color:var(--mut)}
.pm-card{display:inline-block;margin-left:2px;padding:0 5px;border:1px solid;border-radius:3px;font-size:11px;font-weight:600}
.pm-flag{color:#e03131;font-weight:600}
.pm-edit{position:relative}.pm-msg{position:absolute;right:4px;top:0;font-size:12px;color:var(--mut)}
[data-edit]{outline:none;border-radius:3px;cursor:text}[data-edit]:hover{background:var(--wash)}
[data-edit]:focus{background:#fff3bf;color:var(--fg)}.pm-role[data-edit]{border-radius:9px}.pm-role:empty{border-style:dashed}
.pm-q [data-edit]::before{content:"↓ "}.pm-s{cursor:grab}.pm-leaves li.pm-drop{box-shadow:0 -2px 0 var(--acc)}
.pm-pnode.pm-drop{border-color:var(--acc)}[data-edit].pm-bad{outline:1.5px dashed #e03131;outline-offset:2px}
.pm-err{color:#e03131;font-size:12px;font-weight:600;font-style:normal}.pm-leaves li.pm-new .pm-s{visibility:hidden}
.pm-q{width:230px;box-sizing:border-box;margin:2px 0;padding:2px 8px 2px 14px;font-size:12.5px;font-style:italic;color:var(--mut);line-height:1.4}
.pm-q [data-edit]:empty::before{content:"↓ ＋ question";opacity:.7}
.pm-plus{border:0;background:none;padding:1px 4px;font:12px/1.4 system-ui,sans-serif;color:var(--mut);opacity:.6;cursor:pointer}
.pm-plus:hover{opacity:1;color:var(--acc)}.pm-leaves li.pm-add{padding:1px 0 0 30px}
.pm-addp{width:230px;box-sizing:border-box;padding:0 0 2px 10px}.pm-part .pm-addp{width:210px}
/* the ＋ marks stay hidden until the mouse is over their paragraph or their gap (JL 261020: "能不能让它默认隐身，等我鼠标
   移过去的时候再显示出来"); they keep their room, so nothing moves; a touch screen, with no hover, always shows them */
@media(hover:hover){.pm-leaves li.pm-add,.pm-addp,.pm-q [data-edit]:empty::before{opacity:0;transition:opacity .12s}
 .pm-para:hover li.pm-add,.pm-addp:hover,.pm-para:hover+.pm-addp,.pm-para:hover+.pm-q+.pm-addp,.pm-q:hover+.pm-addp,
 .pm-add:focus-within,.pm-addp:focus-within{opacity:1}
 .pm-para:hover+.pm-q [data-edit]:empty::before,.pm-q:hover [data-edit]:empty::before,.pm-q [data-edit]:empty:focus::before{opacity:.7}}
.pm-pnode [data-edit]:empty{display:block;min-height:1.35em;border-bottom:1px dashed var(--line)}
@media(max-width:1000px){.pm,.pm-para,.pm-part,.pm-part .pm-para{grid-template-columns:minmax(0,1fr);gap:8px}.pm-wires{display:none}
 .pm{width:auto}
 .pm-leaves{padding-left:14px;border-left:2px solid var(--line)}.pm-q,.pm-part .pm-q,.pm-addp,.pm-part .pm-addp{width:auto}}
</style>"""
# the branches drawn after layout, so a leaf that wraps still gets its wire: the Section to each part (or straight to
# each paragraph), each part to its paragraphs, each paragraph to each of its Bullets
PLAN_JS = """<script>
(function(){if(window.__pmMap)return;window.__pmMap=1;
 function wire(a,b,o,leaf){var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
  var x1=p.right-o.left,y1=p.top+p.height/2-o.top,x2=q.left-o.left-6,y2=(leaf?q.top+12:q.top+q.height/2)-o.top,m=(x1+x2)/2;
  return '<path d="M'+x1+','+y1+' C'+m+','+y1+' '+m+','+y2+' '+x2+','+y2+'"/>';}
 function draw(){document.querySelectorAll('.pm').forEach(function(m){var svg=m.querySelector('.pm-wires');
  if(!m.offsetParent||getComputedStyle(svg).display==='none')return;
  var o=m.getBoundingClientRect(),root=m.querySelector('.pm-root'),d='';
  svg.setAttribute('width',o.width);svg.setAttribute('height',o.height);
  m.querySelectorAll('.pm-part').forEach(function(pt){d+=wire(root,pt.querySelector('.pm-cnode'),o);});
  m.querySelectorAll('.pm-para').forEach(function(pa){var p=pa.querySelector('.pm-pnode'),pt=pa.closest('.pm-part');
   d+=wire(pt?pt.querySelector('.pm-cnode'):root,p,o);
   pa.querySelectorAll('.pm-leaves>li:not(.pm-add)').forEach(function(l){d+=wire(p,l,o,true);});});
  svg.innerHTML=d;});}
 window.addEventListener('resize',draw);window.addEventListener('load',draw);setTimeout(draw,60);
 document.addEventListener('toggle',function(){setTimeout(draw,0);},true);
 window.pmDraw=draw;document.addEventListener('input',function(e){if(e.target.closest&&e.target.closest('.pm'))draw();});
})();
</script>""" + """<script>
(function(){if(window.__pmEdit)return;window.__pmEdit=1;
 function host(el){return el.closest('.pm-edit');}
 function say(el,t,bad){var m=host(el).querySelector('.pm-msg');m.textContent=t||'';m.style.color=bad?'#c92a2a':'';
  if(t&&!bad)setTimeout(function(){if(m.textContent===t)m.textContent='';},1800);}
 /* a refusal is said where the person typed, and the words they typed stay, outlined red (JL 261020: "why the
    content is not saved here?") */
 function bad(el,msg){var x=el.parentNode.querySelector(':scope > .pm-err');if(!x){x=document.createElement('span');x.className='pm-err';el.after(x);}
  x.textContent=' not saved: '+msg;el.classList.add('pm-bad');say(el,'not saved: '+msg,true);if(window.pmDraw)window.pmDraw();}
 function post(el,body){var h=host(el);body.task=h.dataset.task;body.file=h.dataset.file;say(el,'…');
  return fetch('/_board/draft-plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){if(j.file)h.dataset.file=j.file;
    if(!j.ok){var e=new Error(j.err||'not saved');e.reload=/newer/.test(j.err||'');throw e;}
    el.classList.remove('pm-bad');var x=el.parentNode&&el.parentNode.querySelector(':scope > .pm-err');if(x)x.remove();
    say(el,'saved');return j;});}
 /* the map again from the server, after a point was added, taken out or moved */
 function refresh(h,then){fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(t){
  var n=new DOMParser().parseFromString(t,'text/html').querySelector('.pm-edit[data-task="'+h.dataset.task+'"]');
  if(n){h.innerHTML=n.innerHTML;h.dataset.file=n.dataset.file;}if(window.pmDraw)window.pmDraw();if(then)then();});}
 /* a new point or paragraph refused because the draft changed under the page: the map reloads, and what was typed
    comes back in the same paragraph, outlined red, so clicking away adds it to the newest draft */
 var AGAIN='the draft changed under this page; click away to add it again';
 function again(h,what,pid,txt,role){refresh(h,function(){var pa=h.querySelector('.pm-para[data-p="'+pid+'"]');
  if(!pa){say(h.querySelector('.pm-msg')||h,'not saved: '+pid+' is gone in the newest draft',true);return;}
  if(what==='para'){var row=pa.nextElementSibling;while(row&&!row.classList.contains('pm-addp'))row=row.nextElementSibling;
   var b=row&&row.querySelector('[data-add=para]');if(!b)return;b.click();var e=h.querySelector('.pm-newp [data-edit]');e.textContent=txt;bad(e,AGAIN);return;}
  var pts=pa.querySelectorAll('li[data-s]');newpoint(pa.querySelector('li.pm-add'),pts.length?pts[pts.length-1].dataset.s:'',pid);
  var n=pa.querySelector('li.pm-new');n.querySelector('.pm-role').textContent=role||'';var w=n.querySelector('.pm-t');w.textContent=txt;bad(w,AGAIN);});}
 function words(el){return el.innerText.replace(/\\s+/g,' ').trim();}
 function newpoint(before,after,pid){var n=document.createElement('li');n.className='pm-new';n.dataset.after=after||'';n.dataset.p=pid;
  n.innerHTML='<span class=pm-s>+</span><span class=pm-role data-edit=role data-raw="" contenteditable=plaintext-only></span>'+
   '<span class=pm-w><span class=pm-t data-edit=words data-raw="" contenteditable=plaintext-only></span></span>';
  before.parentNode.insertBefore(n,before);n.querySelector('.pm-t').focus();if(window.pmDraw)window.pmDraw();}
 /* ＋ point: a new point last in its paragraph; ＋ paragraph: a new paragraph after this one, named first */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pm-edit [data-add]');if(!b)return;e.preventDefault();
  if(b.dataset.add==='point'){var ul=b.closest('.pm-leaves'),pts=ul.querySelectorAll('li[data-s]');
   newpoint(b.closest('li'),pts.length?pts[pts.length-1].dataset.s:'',b.closest('.pm-para').dataset.p);return;}
  var row=b.closest('.pm-addp'),n=document.createElement('div');n.className='pm-para pm-newp';n.dataset.after=b.dataset.after;
  n.innerHTML='<div class="pm-node pm-pnode"><span class=pm-id>＋</span><b data-edit=newpara data-raw="" contenteditable=plaintext-only></b></div><ul class=pm-leaves></ul>';
  row.after(n);n.querySelector('[data-edit]').focus();if(window.pmDraw)window.pmDraw();});
 document.addEventListener('focusin',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el||el._html!=null)return;
  el._html=el.innerHTML;if(!el.classList.contains('pm-bad'))el.textContent=el.dataset.raw;});
 document.addEventListener('keydown',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el)return;
  if(e.key==='Escape'){e.preventDefault();el.textContent=el.dataset.raw;el.blur();return;}
  if(e.key!=='Enter')return;e.preventDefault();
  /* Enter after a point: a new point below it, in the same paragraph */
  var li=el.dataset.edit==='words'&&el.closest('li');
  if(li&&words(el)){el.blur();newpoint(li.nextSibling,li.dataset.s||li.dataset.after||'',li.closest('.pm-para').dataset.p);}else el.blur();});
 document.addEventListener('focusout',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el)return;
  var h=host(el),li=el.closest('li'),v=words(el),was=el.dataset.raw,html=el._html;el._html=null;
  if(el.dataset.edit==='newpara'){var np=el.closest('.pm-newp');if(!v){np.remove();if(window.pmDraw)window.pmDraw();return;}
   post(el,{what:'addpara',after:np.dataset.after,value:v}).then(function(){refresh(h);})
    .catch(function(err){if(err.reload)again(h,'para',np.dataset.after,v);else bad(el,err.message);});return;}
  if(li&&li.classList.contains('pm-new')){
   if(e.relatedTarget&&li.contains(e.relatedTarget))return;          /* from the role to the words of the new point */
   var t=words(li.querySelector('.pm-t'));if(!t){li.remove();if(window.pmDraw)window.pmDraw();return;}
   var role=words(li.querySelector('.pm-role'));
   post(el,{what:'add',after:li.dataset.after,p:li.dataset.p,value:t,role:role})
    .then(function(){refresh(h);}).catch(function(err){if(err.reload)again(h,'point',li.dataset.p,t,role);else bad(el,err.message);});return;}
  if(v===was){el.innerHTML=html!=null?html:el.innerHTML;return;}
  var body={what:el.dataset.edit,was:was,value:v};if(li)body.s=li.dataset.s;
  if(el.dataset.p)body.p=el.dataset.p;else if(el.dataset.edit==='para')body.p=el.closest('.pm-para').dataset.p;
  /* a point emptied is taken out */
  if(el.dataset.edit==='words'&&!v)body.what='drop';
  post(el,body).then(function(j){if(body.what==='drop'){refresh(h);return;}el.dataset.raw=v;el.innerHTML=j.html!=null?j.html:v;
    if(window.pmDraw)window.pmDraw();})
   .catch(function(err){bad(el,err.message);});});
 /* a point dragged by its S label: onto another point to go before it, onto a paragraph to go last in it */
 var drag=null;
 document.addEventListener('dragstart',function(e){var s=e.target.closest&&e.target.closest('.pm-edit .pm-s');if(!s)return;
  drag=s.closest('li');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',drag.dataset.s);});
 function spot(e){return drag&&e.target.closest&&(e.target.closest('.pm-leaves li[data-s]')||e.target.closest('.pm-pnode'));}
 document.addEventListener('dragover',function(e){var t=spot(e);document.querySelectorAll('.pm-drop').forEach(function(x){x.classList.remove('pm-drop');});
  if(!t||t===drag||host(t)!==host(drag))return;e.preventDefault();t.classList.add('pm-drop');});
 document.addEventListener('drop',function(e){var t=spot(e);document.querySelectorAll('.pm-drop').forEach(function(x){x.classList.remove('pm-drop');});
  if(!t||t===drag)return;e.preventDefault();var h=host(drag),body={what:'move',s:drag.dataset.s,p:t.closest('.pm-para').dataset.p};
  if(t.tagName==='LI')body.before=t.dataset.s;drag=null;
  post(t,body).then(function(){refresh(h);}).catch(function(err){say(t,'not saved: '+err.message,true);if(err.reload)refresh(h);});});
 document.addEventListener('dragend',function(){drag=null;});
})();
</script>"""



def _bullet_block(lines: list, s: str, lo: int, hi: int) -> tuple:
    """(start, end) of the §1 Bullet `S<s>` between lines lo and hi: its line and its indented Note and More lines."""
    for i in range(lo, hi):
        if re.match(r"^- B\d+ · " + re.escape(s) + r" · ", lines[i]):
            j = i + 1
            while j < hi and lines[j].startswith((" ", "\t")) and lines[j].strip():
                j += 1
            return i, j
    return None


def _para_span(lines: list, pid: str, lo: int, hi: int) -> tuple:
    """(heading, end) of `### <pid> · …` in §1."""
    for i in range(lo, hi):
        if re.match(r"^###\s+" + re.escape(pid) + r"\b", lines[i]):
            j = i + 1
            while j < hi and not lines[j].startswith(("### ", "## ")):
                j += 1
            return i, j
    return None


def plan_act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """One change a person makes on the §1 mind map (JL 261020: "how could I operate and edit it?"), written into the
    newest draft's `## 1 · Structure`: a point's words or role, a paragraph's name, the question it hands on, the arc,
    or a point added, taken out or moved. A new point takes the id after the one above it (S4a), so the text's S
    numbers stay put until Write redrafts. Refused when the words changed on disk since the page showed them (`was`),
    or when §1 is signed. A newer draft than the page showed takes a change of words, still checked by `was`, but
    refuses one that places by S ids (add, move, a new paragraph), which a new version may number differently (JL
    261020, of a rename lost when v0.4 was written under an open page: "why the content is not saved here?")."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    folder = (root / str(p.get("task") or "").strip("/")).resolve()
    if not (folder.is_dir() and root in folder.parents and face(folder)):
        return 400, {"ok": False, "err": "no such Task"}
    d = read_draft(folder)
    if not d:
        return 404, {"ok": False, "err": "no draft yet"}
    if p.get("file") and str(p["file"]) != d["file"].name and str(p.get("what")) in ("add", "move", "addpara"):
        return 409, {"ok": False, "err": f"{d['file'].name} is newer; the map reloads", "file": d["file"].name}
    if _signed(d):
        return 409, {"ok": False, "err": "§1 is signed; clear the ✅ on approved: to change it"}
    norm = lambda x: " ".join(str(x or "").split())
    what, value, was = str(p.get("what") or ""), norm(p.get("value")), norm(p.get("was"))
    s, pid = str(p.get("s") or ""), str(p.get("p") or "")
    if any(c in value for c in "\n<>") or len(value) > 2000:
        return 400, {"ok": False, "err": "plain words only"}
    text = d["file"].read_text(encoding="utf-8")
    lines = text.split("\n")
    top = next((i for i, x in enumerate(lines) if re.match(r"^## 1\s*·", x)), None)
    if top is None:
        return 404, {"ok": False, "err": "no ## 1 · Structure"}
    hi = next((i for i in range(top + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    gone = lambda: (409, {"ok": False, "err": "it changed on disk; reload"})
    html = esc(value)
    if what in ("words", "role", "drop"):
        at = _bullet_block(lines, s, top, hi)
        if not at or not value and what == "words":
            return gone() if not at else (400, {"ok": False, "err": "empty: take the point out instead"})
        m = re.match(r"^(- B\d+ · \S+ · )(?:\[([^\]]*)\]\s*)?(.*?)\s*$", lines[at[0]])
        role, words = m.group(2) or "", m.group(3)
        if norm(role if what == "role" else words) != was:
            return gone()
        if what == "drop":
            del lines[at[0]:at[1]]
        else:
            role, words = (value, words) if what == "role" else (role, value)
            lines[at[0]] = m.group(1) + (f"[{role}] " if role else "") + words
            html = esc(value) if what == "role" else _inline(value, {})
    elif what == "para":
        if not pid or not value:
            return 400, {"ok": False, "err": "a paragraph needs a name"}
        hit = 0
        for i, x in enumerate(lines):           # its heading in every part, and its overview line
            m = re.match(r"^(###\s+|- )(" + re.escape(pid) + r") · (.*?)\s*$", x)
            if m and norm(m.group(3)) == was:
                lines[i], hit = f"{m.group(1)}{pid} · {value}", hit + 1
        if not hit:
            return gone()
    elif what == "ask":
        cur, end, order, found = None, None, [], False
        for i in range(top, hi):
            if lines[i].startswith("### ") and order:          # the overview ends at the first paragraph
                break
            m = re.match(r"^- (C\d+\.P\d+) · ", lines[i])
            cur = m.group(1) if m else (None if re.match(r"^(- |###)", lines[i]) else cur)
            order += [m.group(1)] if m else []
            end = i + 1 if cur == pid and lines[i].strip() else end
            q = re.match(r"^(\s+→ C\d+\.P\d+:\s*)(.*?)\s*$", lines[i])
            if cur == pid and q:
                if norm(q.group(2)) != was:
                    return gone()
                if value:
                    lines[i] = q.group(1) + value
                else:
                    del lines[i]
                found = True
                break
        if not found:                           # none yet: the question it hands to the paragraph after it
            nxt = order[order.index(pid) + 1] if pid in order and order.index(pid) + 1 < len(order) else None
            if was or end is None or not nxt:
                return gone()
            if value:
                lines.insert(end, f"  → {nxt}: {value}")
    elif what == "arc":
        i = next((i for i in range(top) if re.match(r"^arc:", lines[i])), None)
        if i is None or norm(lines[i][4:]) != was:
            return gone()
        lines[i] = f"arc: {value}"
    elif what == "add":
        after = str(p.get("after") or "")
        if not value:
            return 400, {"ok": False, "err": "a new point needs words"}
        span = _para_span(lines, pid, top, hi) if pid else None
        at = _bullet_block(lines, after, *(span or (top, hi))) if after else None
        if (pid and not span) or (after and not at) or not (at or span):
            return gone()
        if not span:
            head = max(i for i in range(top, at[0] + 1) if lines[i].startswith("### "))
            span = _para_span(lines, lines[head].split()[1], top, hi)
        to = at[1] if at else span[1]
        while not at and to > span[0] + 1 and not lines[to - 1].strip():
            to -= 1
        # the id after the point above it (S4a), so the text's S numbers stay put until Write redrafts
        prev = [x for x in re.findall(r"(?m)^- B\d+ · (S\d+[a-z]*) · ", "\n".join(lines[top:to]))]
        ids = set(re.findall(r"(?m)^- B\d+ · (S\d+[a-z]*) · ", "\n".join(lines[top:hi])))
        m = re.match(r"S(\d+)([a-z]?)", prev[-1]) if prev else None
        num = m.group(1) if m else "0"
        letter = chr(ord(m.group(2)) + 1) if m and m.group(2) else "a"
        while f"S{num}{letter}" in ids:
            letter = chr(ord(letter) + 1)
        sid = f"S{num}{letter}" if prev or ids else "S1"
        bs = [int(x) for x in re.findall(r"(?m)^- B(\d+) · ", "\n".join(lines[span[0]:span[1]]))]
        role = norm(p.get("role"))
        lines.insert(to, f"- B{max(bs, default=0) + 1} · {sid} · " + (f"[{role}] " if role else "") + value)
    elif what == "addpara":
        after = str(p.get("after") or "")
        m = re.match(r"C(\d+)\.P(\d+)$", after)
        if not value:
            return 400, {"ok": False, "err": "a paragraph needs a name"}
        if not m or not _para_span(lines, after, top, hi):
            return gone()
        n, new = int(m.group(2)), f"C{m.group(1)}.P{int(m.group(2)) + 1}"
        # the paragraphs after it move down one, wherever the file names them (its parts, Scratch and Draft)
        bump = lambda x: f"C{x.group(1)}.P{int(x.group(2)) + 1}" if int(x.group(2)) > n else x.group(0)
        lines[top:] = [re.sub(r"\bC(\d+)\.P(\d+)\b", bump, x) for x in lines[top:]]
        hi = next((i for i in range(top + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        # the overview: its line after this one's, taking over the question this one handed on
        o = next((i for i in range(top, hi) if re.match(r"^- " + re.escape(after) + r" · ", lines[i])), None)
        if o is not None:
            e = o + 1
            while e < hi and lines[e].startswith((" ", "\t")) and lines[e].strip():
                e += 1
            q = [i for i in range(o + 1, e) if re.match(r"^\s+→ C\d+\.P\d+:", lines[i])]
            moved = [lines.pop(i) for i in reversed(q)][::-1]
            e -= len(moved)
            lines[e:e] = [f"- {new} · {value}"] + moved
            hi += 1
        span = _para_span(lines, after, top, hi)
        lines[span[1]:span[1]] = [f"### {new} · {value}", ""]
        # its Scratch slot, so a note can go under it
        s2 = next((i for i in range(len(lines)) if re.match(r"^## 2\s*·", lines[i])), None)
        if s2 is not None:
            e2 = next((i for i in range(s2 + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            sp = _para_span(lines, after, s2, e2)
            if sp:
                lines[sp[1]:sp[1]] = [f"### {new} · {value}", ""]
    elif what == "move":
        at = _bullet_block(lines, s, top, hi)
        if not at or not _para_span(lines, pid, top, hi):
            return gone()
        block = lines[at[0]:at[1]]
        del lines[at[0]:at[1]]
        hi -= len(block)
        span = _para_span(lines, pid, top, hi)
        before = _bullet_block(lines, str(p.get("before") or ""), span[0], span[1]) if p.get("before") else None
        if before:
            to = before[0]
        else:                                   # last in the paragraph, before its trailing blank lines
            to = span[1]
            while to > span[0] + 1 and not lines[to - 1].strip():
                to -= 1
        own = "\n".join(lines[span[0]:span[1]])
        if re.search(r"(?m)^- B" + re.match(r"- B(\d+)", block[0]).group(1) + r" · ", own):   # its B taken there
            n = max((int(x) for x in re.findall(r"(?m)^- B(\d+) · ", own)), default=0) + 1
            block[0] = re.sub(r"^- B\d+", f"- B{n}", block[0])
        lines[to:to] = block
    else:
        return 400, {"ok": False, "err": "unknown change"}
    d["file"].write_text("\n".join(lines), encoding="utf-8")
    return 200, {"ok": True, "html": html, "file": d["file"].name}

def _examples(f: dict, root: Path) -> list:
    """The published papers this Section is read against (JL 261020: "这里可不可以找一些 examples? ... 找几篇相关文章的
    introduction"): each reading (excalidraw-read's `reads/<pNN-…>/reading.yaml`) under a Studio topic of this Task,
    or under the topic a Section canvas names by `examples:`; its name, size and each paragraph's move, for the
    rubric's table, and its topic, whose drawing the Examples card opens. One dict per paper, in the topic's order."""
    try:
        import yaml
    except ImportError:
        return []
    import os
    tops = []
    for _, topic, _ in f["topics"]:
        md = _notes(topic)
        m = re.search(r"(?m)^examples:\s*(\S+)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
        for t in [topic] + ([Path(os.path.normpath(topic / m.group(1)))] if m else []):
            if (t / "reads").is_dir() and t not in tops:
                tops.append(t)
    out = []
    for top in tops:
        names = {}
        face_ = _notes(top)
        y = re.search(r"(?ms)^```yaml\n(.*?)^```", face_.read_text(encoding="utf-8", errors="ignore")) if face_ else None
        try:
            for p in ((yaml.safe_load(y.group(1)) or {}).get("related") or {}).get("papers") or [] if y else []:
                names[str(p.get("id"))] = p.get("item") or ""
        except Exception:
            pass
        for r in sorted(top.glob("reads/*/reading.yaml")):
            try:
                y = yaml.safe_load(r.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            sec, paras = y.get("section") or {}, {}
            for lg in y.get("logic") or []:                 # a paragraph may carry two moves (Desai's P3)
                m = re.match(r"P(\d+)\s*·\s*(.*)", str(lg.get("text") or ""))
                if m:
                    size = next((re.sub(r"^Size:\s*(P\d+\s*)?", "", h).split(",")[0] for h in lg.get("how") or []
                                 if str(h).startswith("Size:")), "")
                    old = paras.get(int(m.group(1)), ("", ""))
                    paras[int(m.group(1))] = ((old[0] + " · " if old[0] else "") + m.group(2), old[1] or size)
            out.append({"short": names.get(r.parent.name.split("-", 1)[0]) or r.parent.name, "topic": top,
                        "section": sec.get("name", ""), "size": (sec.get("key") or [""])[0], "paras": paras})
    return out


def _served(path: Path | None, root: Path) -> str:
    """The URL the host serves a file at; "" for one it does not serve, as a file reached through the root's `Tools/`
    link, whose real path lies outside the root (the examples' PDFs, the rubric)."""
    try:
        return "/" + quote(_rel(path, root)) if path else ""
    except ValueError:
        return ""


def _examples_card(exs: list, d: dict, f: dict, folder: Path, root: Path) -> str:
    """The Studio topic that reads the published papers, opened straight onto its drawing (JL 261020: "could you make
    things here to be the excalidraw using the /excalidraw-read, but we still use the one from the sNN studio"; "here I
    will expect it to be a frame of the sNN studio"): excalidraw-read's topic canvas, one row per paper, its passages
    shot from the PDF and linked to our paragraphs. With no such topic, the prompt that makes one."""
    if not exs:
        job = face(chain(folder, root).get("Job") or folder)
        desk = ((d or {}).get("head", {}).get("desk", "") or f["head"].get("desk", "") or
                (_header(job.read_text(encoding="utf-8", errors="ignore")).get("desk", "") if job else "")).split(":")[0]
        ask = (f"/excalidraw-read {f['t']}: find 3 to 4 published {desk.strip() or 'venue'} papers whose {f['section']} "
               f"we could follow (two close to our topic, two its author guide quotes); read each PDF's {f['section']} "
               f"whole into a Studio topic sNN-{folder.name}-examples (reads/pNN-<author><year>/reading.yaml, with "
               "shots), each passage linked to the paragraph of ours it feeds.")
        return _fold("📚 Examples", _not_yet("No example papers yet.") + f'<p><button type=button class="run-copy '
                     f'work-act" data-copy="{esc(ask)}">Copy prompt · find examples</button></p>')
    inside = _drawn_inside(f)
    canvas = [(s, t, dr) for s, t, dr in f["topics"] if any(e["topic"] in inside for e in exs) and dr
              and _notes(t) and re.search(r"(?m)^\s*examples:", _notes(t).read_text(encoding="utf-8", errors="ignore"))]
    if canvas:                                     # one canvas, ours and the examples side by side (s22 draws s26)
        return "".join(_canvas_card(s, t, dr, root) for s, t, dr in canvas)
    out = []
    for top in dict.fromkeys(e["topic"] for e in exs):
        n = sum(e["topic"] == top for e in exs)
        sec = next(e["section"] for e in exs if e["topic"] == top) or f["section"]
        title = f"📚 Examples · how {n} published papers write their {sec}"
        drawing = top / f"{top.name}.excalidraw"
        if not drawing.is_file():
            out.append(_fold(title, _not_yet(f"{top.name} has no drawing yet.")))
            continue
        url = _draw_url(drawing, root)
        out.append(f'<details class="topic work-task"><summary><span class=related-head><b>{esc(title)}</b> '
                   f'<span class=mut>· {esc(top.name)}</span></span><span class=topic-pop>{pop(url, top.name, "↗")}</span>'
                   f'</summary><iframe class=st-frame title="{esc(top.name)}" data-src="{esc(url)}" '
                   'referrerpolicy=no-referrer></iframe></details>')
    return "".join(out)


def _rubric_card(exs: list, d: dict, f: dict, root: Path) -> str:
    """The requirement and the rubric as one review (JL 261020: "这个 rubric 你有没有想过怎么能把它改得更好一些？比如找
    一些相关的论文，把它们是怎么写的也放到这下面，做成一个 review"): the desk's rule for this Section, ours beside each
    example paragraph by paragraph, and the four axes a reviewer judges by."""
    head = (d or {}).get("head", {})
    rows = [(k, esc(head[h])) for k, h in (("Desk rule", "structure-division"), ("Desk", "desk")) if head.get(h)]
    body = _kv(rows) if rows else ""
    if f["requirement"].is_file():
        body += _source(f["requirement"], root, "")
    if exs and d and d.get("structure"):
        _, _, paras = _plan_tree(d["structure"][1])
        words = sum(len(m.group(1).split()) for _, b in d.get("text", [])
                    for m in re.finditer(r"(?m)^- B\d+ · S\d+[a-z]* · (.*)$", b))
        n = max([len(paras)] + [max(e["paras"] or [0]) for e in exs])
        ours = {i + 1: f'<b>{esc(job)}</b><br><span class=mut>{esc(" · ".join(r for _, r, _, _ in bs if r))}</span>'
                for i, (_, job, bs) in enumerate(paras)}
        cell = lambda e, k: (f'{esc(e["paras"][k][0])}<br><span class=mut>{esc(e["paras"][k][1])}</span>'
                             if k in e["paras"] else '<span class=mut>—</span>')
        table = _table([""] + [f"Ours · {d['version']}"] + [e["short"] for e in exs],
                       [["Size", esc(f"{len(paras)} paragraphs · {words} words")] + [esc(e["size"]) for e in exs]]
                       + [[f"P{k}", ours.get(k, '<span class=mut>—</span>')] + [cell(e, k) for e in exs]
                          for k in range(1, n + 1)])
        ask = (f"/haipipe-draft {f['t']} revise: review {f['section']} as its desk's reviewer against the desk rule, the "
               f"four axes and the {len(exs)} example papers in {exs[0]['topic'].name}, paragraph by paragraph; each "
               "finding a Revise card (Why, Original, Expected), naming the example it follows.")
        body += (f'<h4 style="margin:12px 0 4px">Ours beside the examples</h4><div class=ex-review>{table}</div>'
                 f'<p><button type=button class="run-copy work-act" data-copy="{esc(ask)}">Copy prompt · review against '
                 'the examples</button></p>')
    if RUBRIC.is_file():
        axes = [(f"<b>{esc(a)}</b>", esc(q)) for a, q in re.findall(
            r"(?m)^\|\s*([A-Z][a-z]+)\s*\|\s*([^|]+?)\s*\|", RUBRIC.read_text(encoding="utf-8", errors="replace"))
            if a != "Axis"]
        alt = _served(root / "Tools" / RUBRIC.relative_to(SKILLS.parents[2]), root)
        body += ('<h4 style="margin:12px 0 4px">The four axes</h4>' + _table(("axis", "the question"), axes)
                 + '<p class=mut style="margin:4px 0">MEETS · NEEDS WORK · N/A · NOT VERIFIABLE (never a pass)'
                 + (f' · <a href="{esc(alt)}" target=_blank>{esc(RUBRIC.name)} ↗</a>' if alt else "") + '</p>')
    return EX_CSS + _fold("📏 Requirement and Rubric", body or _not_yet("No requirement yet."))


EX_CSS = """<style>
.ex-review td{vertical-align:top;font-size:13px;line-height:1.45}
@media(max-width:1000px){.ex-review{overflow-x:auto}}
</style>"""


def _plan(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, head = f["draft"], f["head"]
    paras = _paragraphs(d["structure"][1]) if d and d["structure"] else []
    bullets = [b for _, bs in paras for b in bs]
    plan = (f'§1 Structure · {len(paras)} paragraphs · {len(bullets)} Bullets · approved: '
            f'{esc((d["head"].get("approved") or "⬜"))}' if d and d["structure"] else
            '<span class="st st-warn">not written yet</span>')
    desk = (d or {}).get("head", {}).get("desk", "") if d else ""
    rows = [("Task", f'<code>{esc(folder.name)}</code> · {esc(f["section"])}'),
            ("Section", esc(head.get("reader-question") or f["section"])),
            ("Requirement", esc(desk) if desk else _code(f["requirement"], root)),
            ("Context", _code(f["context"], root) if f["context"].is_file() else '<span class=mut>not gathered yet</span>'),
            ("Plan", plan)]
    sign = ""
    if st == "sign":
        sign = (f'<p class=sign-row><span class="st st-warn">✍ Sign</span> you read §1, then type ✅ on '
                f'<code>approved:</code> in {_code(d["file"], root)}; no skill signs</p>')
    elif st == "done":
        sign = f'<p><span class="st st-ok">✓ signed</span> {esc(d["head"].get("approved", ""))}</p>'
    # each Point a short head (JL 261020: "I think the buleet point should not be too large"; the plan's own 4-11 word
    # rule, which 12 of t01's 18 Points broke)
    # and each paragraph a short name (JL 261020: "you might want to update the content of this as well", a 20-word name)
    prompt = (f"/haipipe-draft {f['t']} structure: revise §1 of {f['section']} from my notes and its Scratch, each "
              "paragraph a short name and each Point a short head, 4 to 8 words (numbers and wording in its Note), then stop for my Sign."
              if paras or (d and d["structure"]) else
              f"/haipipe-draft {f['t']} structure: gather the context, write §1 Structure for {f['section']}, each "
              "paragraph a short name and each Point a short head, 4 to 8 words (numbers and wording in its Note), then stop for my Sign.")
    op = _step_box("📐 Stage 1 · Plan", st, "<h4>Input</h4>" + _kv(rows) + sign + _prompt_box(prompt, folder, root, "plan"))
    if paras:
        # one card, the paragraphs and their Bullets together, as a mind map (JL 261020: "merge them together")
        cards = _fold(f"📐 §1 Structure · {d['version']}", _plan_map(d, f["ev"], f["section"], _rel(folder, root)),
                      open_=True)
    else:
        cards = _not_yet("No §1 Structure yet.")
    try:                                           # an example that does not read: say so, never break the frame
        exs = _examples(f, root)
        cards += _examples_card(exs, d, f, folder, root)
    except Exception as e:
        exs = []
        cards += _fold("📚 Examples", _not_yet(f"The examples do not read: {e}"))
    contract = [(esc(k), esc(head[k])) for k in CONTRACT if head.get(k)]
    if contract:
        cards += _fold("🧭 The Section's contract, from its Story", _kv(contract), open_=not paras)
    try:
        cards += _rubric_card(exs, d, f, root)
    except Exception as e:
        cards += _fold("📏 Requirement and Rubric", _not_yet(f"The rubric does not read: {e}"))
    recs = f["records"]
    cards += _fold("🗂 Records", _table(("record", "bytes"), [(_code(r, root), esc(r.stat().st_size)) for r in recs])
                   if recs else _not_yet("No records yet."))
    return op, cards, ()


def _write(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, ev = f["draft"], f["ev"]
    plan = ("§1, signed" if _signed(d) else "§1, not signed yet" if d and d["structure"] else
            "no §1 yet: the Section's contract")
    now = (f'{_code(d["file"], root)} · {esc(d["head"].get("version") or d["version"])}' if d else
           '<span class=mut>no draft yet</span>')
    rows = [("Plan", esc(plan)), ("Studio", esc(" · ".join(t.name for _, t, _ in f["topics"]) or "no topic")),
            ("Writes", "§3 Draft, from §1 and its Scratch (1 · Plan), no rules yet"), ("Now", now)]
    prompt = (f"/haipipe-draft {f['t']} write: redraft {f['section']} from my notes, its Scratch and §1; keep every "
              "sentence I typed; no rules yet; mark each claim that waits for evidence." if d and d["text"] else
              f"/haipipe-draft {f['t']} write: scratch §2 from the plan, then write §3 for {f['section']}; mark claims "
              "you cannot support yet.")
    # the drafting ask, open (JL 261020: "add the prompt to help the structure and drafting"); the structure ask is
    # 1 · Plan's, beside the Scratch
    op = _step_box("✍️ Stage 2 · Write", st, "<h4>Input</h4>" + _kv(rows)
                   + _prompt_box(prompt, folder, root, "write", "✍️ Prompt · draft"))
    if not d or not d["text"]:
        return op, _not_yet("No text yet."), ()
    cards = _text_and_editor(d, ev, root, folder) + "".join(_fold(f"🗒 {t}", _md(b, {})) for t, b in d["notes"])
    return op, cards, ()


def _text_card(d: dict, ev: dict, root: Path) -> str:
    """The text as it reads, a sentence a line with its S number and its evidence boxed: Write's Result, and Revise's
    too (JL 261020, on Revise's "No Revise cards yet": "I think things here should be in the Results here")."""
    marks = _marks(ev)
    body = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks)
                   for t, b in d["text"])
    return _fold(f"✍️ The text · {d['version']}", f'<p class=space-reads>{_code(d["file"], root)}</p>' + body, open_=True)


def _text_and_editor(d: dict, ev: dict, root: Path, folder: Path) -> str:
    """The text as it reads on the left, your own editor on the right (JL 261020: "I want to put the "Write it
    yourself" in the right of the "The Text" itself ... just like the Text + Evidence Panel and Text + Revising
    Panel"). The row you point at or type in lights its sentence on the left, and a sentence you point at lights its
    row; once a box saves, the left reads the text again."""
    src = _editor_src(folder, root, "revise")
    if not src:
        return _text_card(d, ev, root)
    marks = _marks(ev)
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks)
                   for t, b in d["text"])
    right = (f'<h4 style="margin:0 0 4px">✍️ Write it yourself {pop(src.replace("&embed=1", ""), "Write it yourself", "↗")}</h4>'
             f'<iframe class=space-frame title="Write it yourself" src="{esc(src)}" style="{FIT_STYLE}" '
             f'onload="{FIT};window.wrHook&&window.wrHook(this)"></iframe>')
    body = (f'<p class=space-reads>{_code(d["file"], root)}</p><span class=wr-msg role=status>Loading the editor…</span>'
            f'<div class="rv-split wr-split"><div class=rv-left>{text}</div><div class=rv-right>{right}</div></div>')
    return CARDS_CSS + _fold(f"✍️ The text · {d['version']}", body, open_=True) + WRITE_JS


# what is happening, in a corner of the screen while it happens (JL 261020: "when it is loading, could you state that
# status?"): loading the editor, saving, updating the text, saved; a refusal stays, in red
WRITE_JS = """<style>
.wr-msg{position:fixed;right:24px;bottom:20px;z-index:20;padding:6px 12px;border:1px solid var(--line);border-radius:6px;
 background:var(--card);color:var(--fg);font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,.12);max-width:420px}
.wr-msg:empty{display:none}.wr-msg.bad{color:#c92a2a;border-color:#c92a2a}.wr-split .rv-left.wr-old{opacity:.55}
</style><script>
(function(){if(window.__wrSplit)return;window.__wrSplit=1;
 function say(sp,t,bad,ms){var m=sp.parentNode.querySelector('.wr-msg');if(!m)return;m.textContent=t||'';m.classList.toggle('bad',!!bad);
  clearTimeout(m._t);if(ms)m._t=setTimeout(function(){m.textContent='';},ms);}
 function row(sp,s){try{return s?sp.querySelector('iframe').contentDocument.querySelector('.revise-rows>div[data-s="'+s+'"]'):null;}catch(e){return null;}}
 /* a sentence lit on both sides; from the editor, the text scrolls on its own to show it */
 function light(sp,s,on,scroll){var t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]'),r=row(sp,s);
  if(r)r.classList.toggle('wr-lit',on);if(!t)return;t.classList.toggle('rv-lit',on);var l=t.closest('.rv-left');
  if(on&&scroll&&l.scrollHeight>l.clientHeight&&(t.offsetTop<l.scrollTop||t.offsetTop+t.offsetHeight>l.scrollTop+l.clientHeight))
   l.scrollTo({top:Math.max(0,t.offsetTop-l.clientHeight/3),behavior:'smooth'});}
 /* the text again from the server once a box saved: its new words, their evidence boxed */
 function refresh(sp){var l=sp.querySelector('.rv-left');say(sp,'Updating the text…');l.classList.add('wr-old');
  fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(h){
   var n=new DOMParser().parseFromString(h,'text/html').querySelector('.wr-split .rv-left');
   if(n)l.innerHTML=n.innerHTML;l.classList.remove('wr-old');say(sp,'✓ Saved',false,2000);})
  .catch(function(){l.classList.remove('wr-old');say(sp,'Saved, but the text did not update; reload the page',true);});}
 window.wrHook=function(f){var sp=f.closest('.wr-split'),d;try{d=f.contentDocument;}catch(e){return;}
  if(!sp||!d||!d.body||d.__wr||d.location.href==='about:blank')return;d.__wr=1;var cur='';
  say(sp,d.querySelector('.revise-rows')?'':'The editor did not load; reload the page',!d.querySelector('.revise-rows'));
  var st=d.createElement('style');st.textContent='.revise-rows>div.wr-lit{background:#fff3bf;border-radius:3px}';d.head.appendChild(st);
  function on(s){if(!s||s===cur)return;light(sp,cur,false);cur=s;light(sp,cur,true,true);}
  function at(){var x=d.getSelection(),n=x&&x.anchorNode;while(n&&!(n.parentNode&&n.parentNode.classList&&n.parentNode.classList.contains('revise-rows')))n=n.parentNode;
   return n&&n.getAttribute?n.getAttribute('data-s'):'';}
  d.addEventListener('mouseover',function(e){var r=e.target.closest&&e.target.closest('.revise-rows>div[data-s]');if(r)on(r.getAttribute('data-s'));});
  d.addEventListener('keyup',function(){on(at());});d.addEventListener('click',function(){on(at());});
  /* the text follows the typing at once (JL 261020: "I see it will need to wait for a while"); the save, when the
     box is left, then reads it again with its evidence boxed */
  d.addEventListener('input',function(e){var r=e.target.closest&&e.target.closest('.revise-rows');if(!r)return;
   [].forEach.call(r.children,function(x){var s=x.getAttribute('data-s'),t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]');
    if(!t)return;var w=x.innerText.replace(/\\s+/g,' ').trim(),l=t.firstElementChild;
    if(t.dataset.typed!==w){t.dataset.typed=w;t.textContent=' '+w;if(l&&l.classList.contains('mut'))t.insertBefore(l,t.firstChild);}});});
  /* the mouse gone from the editor: back to the row being typed in, or nothing lit */
  d.documentElement.addEventListener('mouseleave',function(){var s=at();if(cur&&cur!==s){light(sp,cur,false);cur='';}on(s);});
  /* the editor's own status line, said in the corner: Saving…, then the text again, or why it did not save */
  new MutationObserver(function(ms){var b=null;ms.forEach(function(m){var t=m.target.nodeType===1?m.target:m.target.parentNode;
    b=(t&&t.closest&&t.closest('.revise-status'))||b;});if(!b)return;var t=b.textContent.trim();
    if(b.classList.contains('err')&&t)say(sp,t,true);else if(/^Saving|^Adding/.test(t))say(sp,t);
    else if(/^Saved/.test(t))refresh(sp);else if(/^Nothing changed/.test(t))say(sp,'Nothing changed',false,1500);})
   .observe(d.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['class']});};
 document.querySelectorAll('.wr-split iframe').forEach(function(f){try{if(f.contentDocument.readyState==='complete')window.wrHook(f);}catch(e){}});
 document.addEventListener('mouseover',function(e){var t=e.target.closest&&e.target.closest('.wr-split .rv-left li[data-s]');
  if(t)light(t.closest('.wr-split'),t.dataset.s,true);});
 document.addEventListener('mouseout',function(e){var t=e.target.closest&&e.target.closest('.wr-split .rv-left li[data-s]');
  if(t&&!t.contains(e.relatedTarget))light(t.closest('.wr-split'),t.dataset.s,false);});
})();
</script>"""


def _canvas_card(source: Path, topic: Path, drawings: list, root: Path) -> str:
    """A Section canvas opened straight onto its drawing, no topic row inside the card (JL 261020: "could I open
    this, and the content here is shown directly? ... No need to have box in box")."""
    if not drawings:
        return _fold(f"🎨 The Section canvas · {topic.name}", _not_yet("No drawing yet."))
    url = _draw_url(drawings[0], root)
    return (f'<details class="topic work-task"><summary><span class=related-head><b>🎨 The Section canvas · '
            f'{esc(topic.name)}</b></span><span class=topic-pop>{pop(url, topic.name, "↗")}</span></summary>'
            f'<iframe class=st-frame title="{esc(topic.name)}" data-src="{esc(url)}" referrerpolicy=no-referrer>'
            '</iframe></details>')


EV_STATE = {"have": '<span title="have">✅</span>', "need": '<span title="asked">❓</span>',
            "missing": '<span title="not found">❗</span>'}


def _s_ids(it: dict) -> list:
    """An item's sentences, `for: [2, 4]` (or "2a"), as the text's ids: S2, S4."""
    return ["S" + str(n).lstrip("S") for n in it.get("for") or []]


def _s_key(s: str) -> tuple:
    m = re.match(r"S?(\d+)([a-z]?)$", str(s))
    return (int(m.group(1)), m.group(2)) if m else (10 ** 6, "")


def _num(v) -> str:
    """A value read from a Run as a reader writes it: 73931, 0.7169, 19."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else f"{x:.4g}"


def _evidence_row(c: dict, it: dict, n: int, sentences: bool = False, brief: bool = False) -> str:
    """One item as a row: its id, the card's label and its place in the card (CITE 1.4), in the card's ink and as the
    text's mark names it (JL 261020: "should the evidence item have some index as well?"; the card's title on hover);
    have or asked; the words it backs with the value read, and under them what backs them (the paper, the Run and its
    key, or what is still asked). Hovering a row lights its sentences. In a card's own list (`sentences`), the sentences
    it backs follow its id. Beside the text (`brief`) the row is one line and what backs it shows on hover, so the cards
    keep closer to their sentences; the card's own fold shows it all."""
    ink = INK.get(c["kind"], INK["value"])
    value = it.get("value")
    words = " · ".join(f"“{esc(a)}”" for a in it.get("anchor") or []) or esc(it.get("cite") or "")
    if c["kind"] != "cite" and it["state"] == "have" and value not in ("", None):
        words += f" <b>= {esc(_num(value))}</b>"
    fact = it.get("fact")
    fact = ", ".join(map(str, fact)) if isinstance(fact, list) else str(fact or "")
    if it["state"] == "missing":
        detail = esc(str(value))
    elif c["kind"] == "cite" and it["state"] == "have":
        detail = esc(" · ".join(x for x in (str(value or it.get("cite") or ""), fact) if x))
    else:
        where = ((f'<code>{esc(c["source"])}.{esc(it["run"])}</code>' + (f' · {esc(it["file"])}' if it.get("file") else "")
                  + (f' <code>{esc(it["key"])}</code>' if it.get("key") else "")) if it.get("run") else "")
        detail = " · ".join(x for x in (esc(it.get("what") or it.get("need") or fact), where) if x)
    title = c["title"] + (f" · {c['source']}" if c["source"] else "")
    hover = f' title="{esc(re.sub("<[^>]+>", "", detail))}"' if brief and detail else ""
    return (f'<tr data-s="{esc(" ".join(_s_ids(it)))}"{hover}>'
            f'<td style="white-space:nowrap;width:1%;padding:5px 8px 5px 0"><b style="color:{ink};font-size:12.5px" '
            f'title="{esc(title)}">{esc(c["label"])}.{n}</b></td>'
            + (f'<td class=mut style="white-space:nowrap;width:1%;padding:5px 8px 5px 0;font-size:12.5px">'
               f'{esc(" · ".join(_s_ids(it)) or "—")}</td>' if sentences else "")
            + f'<td style="width:1%;padding:5px 8px 5px 0">{EV_STATE[it["state"]]}</td>'
            f'<td style="padding:5px 0;line-height:1.5">{words}'
            + (f'<br><span class=mut style="font-size:12.5px">{detail}</span>' if detail and not brief else "") + '</td></tr>')


# the text and the cards as 5 · Revise lays them out, one column with no gap between sentences and the cards at their
# sentences (JL 261020: "I want it to be left to be the orignal text, and the right to be the evidence";
# "我想要保证这个 draft 在 revise、evidence、display 这里都保持一样的风格 ... 所以句子跟句子之间不要有空格"); only the cards' own look here
EV_CSS = """<style>
.ev-card{padding:4px 12px;margin:0 0 8px}.ev-card td{vertical-align:top}
.ev-card tr+tr td,.ev-list tr+tr td{border-top:1px solid var(--line)}.ev-list td{vertical-align:top}
</style>"""


def _card_folds(ev: dict) -> str:
    """Each Evidence card on its own, folded under the text (JL 261020: "To show each evidenence card seperately?"): its
    label in its ink, its title and where it comes from; opened, a row per item, CITE 1.4 and the sentences it backs."""
    out = []
    for c in ev["cards"]:
        ink = INK.get(c["kind"], INK["value"])
        rows = "".join(_evidence_row(c, it, n, sentences=True) for n, it in enumerate(c["items"], 1))
        out.append(f'<details class="topic work-task"><summary><span class=related-head><b style="color:{ink}">'
                   f'{esc(c["label"])}</b> · {esc(c["title"])}'
                   + (f' <span class=mut>· {esc(c["source"])}</span>' if c["source"] else "") + '</span></summary>'
                   f'<div class=work-body><table class="rv-rows ev-list" style="border-collapse:collapse;width:100%">'
                   f'{rows}</table></div></details>')
    return "".join(out)


def _ev_card(s: str, rows: list) -> str:
    return (f'<div class="rv-card ev-card" data-s="{esc(s)}"><table class=rv-rows style="border-collapse:collapse;'
            f'width:100%">{"".join(rows)}</table></div>')


def _text_rows(d: dict, marks: dict, right: dict, rest_head: str) -> str:
    """The text as one column, read on with no gap between sentences, and beside it the cards, `right[S]` at sentence
    S's line (CARDS_JS `align`): each pushed down only to clear the card above it, so the text never moves for a card;
    the column stays beside the cards and scrolls itself to the sentence a card lights, as 5 · Revise's (JL 261020:
    "我不想让句子跟句子之间有这么大的空格 ... 在 revise、evidence、display 这里都保持一样的风格"). Used by 3 · Evidence and
    4 · Display; a card for a sentence the text no longer has, or for none, ends the column."""
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks)
                   for t, b in d["text"])
    have = {m for _, b in d["text"] for m in re.findall(r"(?m)^- B\d+ · (S\d+[a-z]?) · ", b)}
    order = sorted(right, key=lambda s: _s_key(s) if s else (10 ** 7, ""))
    cards = "".join(right[s] for s in order if s in have)
    rest = [s for s in order if s not in have]
    if rest:
        cards += f'<h4 style="margin:12px 0 4px">{esc(rest_head)}</h4>' + "".join(
            f'<p class=mut style="margin:6px 0 2px">{esc(s + " is not in the text") if s else "no sentence named"}</p>'
            + right[s] for s in rest)
    return f'<div class="rv-split ev-split"><div class=rv-left>{text}</div><div class=rv-right>{cards}</div></div>'


# ── what the text and its plan leave unsure ───────────────────────────────────────────────────────
# 3 · Evidence shows every point still open beside its sentence, card or no card (JL 261021: "我们的 evidence 该怎么把这些
# 不确定的 ... 都加上去"): the writer's own marks in §3 and each §1 point that says it has no evidence. OPEN <n> in
# reading order; the Evidence prompt turns each into a card item, or leaves it as the paper's own reasoning.
OPEN_KIND = {"check": ("❓", "to check", "#e03131"), "find": ("❓", "to find", "#e03131"),
             "pending": ("⏳", "waits on a Run", "#e67700"), "none": ("⚪", "no evidence", "#868e96")}
MARK = re.compile(r"⟦([^⟦⟧]*(?:⟦[^⟦⟧]*⟧[^⟦⟧]*)*)⟧")


def _open_points(d: dict | None) -> list:
    """[{s, kind, what}] in reading order: each ⟦…⟧ in a §3 sentence (⟦check: …⟧ a source named but not yet verified,
    ⟦pending …⟧ or a one- or two-word ⟦x⟧ a value a Run has not given, any other a source still to find), then each §1
    point whose evidence line says `Evidence: none · <why>`."""
    out = []
    for _, body in (d or {}).get("text", []):
        for m in re.finditer(r"(?m)^- B\d+ · (S\d+[a-z]?) · (.*)$", body):
            for mk in MARK.findall(m.group(2)):
                low = mk.strip().lower()
                kind = ("check" if low.startswith("check") else
                        "pending" if low.startswith("pending") or (len(low.split()) <= 2 and ":" not in low) else "find")
                out.append({"s": m.group(1), "kind": kind,
                            "what": re.sub(r"^(check|pending)\b\s*:?\s*", "", mk.strip(), flags=re.I)})
    if d and d.get("structure"):
        for m in re.finditer(r"(?ms)^- B\d+ · (S\d+[a-z]?) · .*?(?=^- B\d+ · |^#{2,4} |\Z)", d["structure"][1]):
            e = re.search(r"(?m)^\s*Evidence:\s*none\b\s*·?\s*(.*)$", m.group(0))
            if e:
                out.append({"s": m.group(1), "kind": "none", "what": e.group(1).strip()})
    return sorted(out, key=lambda o: _s_key(o["s"]))


def _open_row(o: dict, n: int, sentences: bool = False) -> str:
    icon, word, ink = OPEN_KIND[o["kind"]]
    return (f'<tr data-s="{esc(o["s"])}"><td style="white-space:nowrap;width:1%;padding:5px 8px 5px 0">'
            f'<b style="color:{ink};font-size:12.5px">OPEN {n}</b></td>'
            + (f'<td class=mut style="white-space:nowrap;width:1%;padding:5px 8px 5px 0;font-size:12.5px">{esc(o["s"])}</td>'
               if sentences else "")
            + f'<td style="width:1%;padding:5px 8px 5px 0">{icon}</td><td style="padding:5px 0;line-height:1.5">'
            f'<span style="color:{ink}">{word}</span>' + (f' · <span class=mut>{esc(o["what"])}</span>' if o["what"] else "")
            + '</td></tr>')


def _open_fold(opens: list) -> str:
    """Every open point in one list, the sentence beside each, the ones to check or find first."""
    if not opens:
        return ""
    rank = {"check": 0, "find": 0, "pending": 1, "none": 2}
    rows = "".join(_open_row(o, n, sentences=True) for n, o in
                   sorted(enumerate(opens, 1), key=lambda x: (rank[x[1]["kind"]], x[0])))
    count = lambda *k: sum(o["kind"] in k for o in opens)
    title = (f"❓ Open points · {count('check', 'find')} to check or find · {count('pending')} wait on a Run · "
             f"{count('none')} with no evidence")
    return (f'<details class="topic work-task"><summary><span class=related-head><b>{esc(title)}</b></span></summary>'
            f'<div class=work-body><table class="rv-rows ev-list" style="border-collapse:collapse;width:100%">{rows}'
            '</table></div></details>')


def _text_and_evidence(d: dict, ev: dict, root: Path, opens: list = ()) -> str:
    """The text on the left, read on as one column, and at each sentence on the right its card: a row per item that backs
    it, then the points still open there (OPEN n). An item backing two sentences shows beside both; a sentence the cards
    name that the text no longer has, or an item naming none, ends the column. With no text yet, the cards alone."""
    by, one = {}, []
    for c in ev["cards"]:
        for n, it in enumerate(c["items"], 1):
            one.append({"kind": c["kind"], "label": f'{c["label"]}.{n}', "items": [it]})
            for s in _s_ids(it) or [""]:
                by.setdefault(s, []).append(_evidence_row(c, it, n, brief=True))
    for n, o in enumerate(opens, 1):
        by.setdefault(o["s"], []).append(_open_row(o, n))
    if not d or not d["text"]:
        order = sorted(by, key=lambda s: _s_key(s) if s else (10 ** 7, ""))
        return EV_CSS + CARDS_CSS + "".join(_ev_card(s, by[s]) for s in order) + CARDS_JS
    marks = _marks({"cards": one})      # each mark names its item, CITE 1.4, as its row does
    body = (f'<p class=space-reads>{_code(d["file"], root)} · {_code(ev["path"], root)}</p>'
            + _text_rows(d, marks, {s: _ev_card(s, rows) for s, rows in by.items()}, "Cards for no sentence in this text"))
    return EV_CSS + CARDS_CSS + _fold(f"🔎 The text and its Evidence · {d['version']}", body, open_=True) + CARDS_JS


def _evidence_step(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, ev = f["draft"], f["ev"]
    items = [it for c in ev["cards"] for it in c["items"]]
    have = sum(it["state"] == "have" for it in items)
    open_asks = sum(not t for t, _ in ev["proposals"])
    opens = _open_points(d)
    rows = [("Reads", esc(f"§1 at the plan · the text {d['version']} as a reader" if d else "§1 at the plan")),
            ("Cards", (_code(ev["path"], root) + esc(f" · {len(ev['cards'])} cards · {len(items)} items: {have} have, "
                                                     f"{len(items) - have} asked or missing")) if ev["path"] else
             '<span class=mut>no evidence/cards.yaml yet</span>'),
            ("Asks", (_code(ev["props_path"], root) + esc(f" · {open_asks} to tick, {len(ev['proposals']) - open_asks} "
                                                          "ticked")) if ev["props_path"] else '<span class=mut>none</span>'),
            ("Open", esc(f"{len(opens)} points: {sum(o['kind'] in ('check', 'find') for o in opens)} to check or find, "
                         f"{sum(o['kind'] == 'pending' for o in opens)} wait on a Run, "
                         f"{sum(o['kind'] == 'none' for o in opens)} with no evidence") if opens else '<span class=mut>none</span>'),
            ("Check", ('<span class="st st-ok">every address resolves</span>' if not ev["problems"] else
                       f'<span class="st st-warn">{len(ev["problems"])} to fix</span>') if ev["path"] else
             '<span class=mut>—</span>')]
    prompt = (f"/haipipe-evidence {f['t']}: a card for each claim in {f['section']}'s plan (have, ask a Job, ask a "
              f"person, soften), the asks in proposals.md; then read {f['section']} as a reader for claims the plan "
              "missed. Give every open point an item: each ⟦check⟧ its source verified, each source still to find a "
              "need with a proposal, each ⟦pending⟧ the Run it waits on, and each 'Evidence: none' a reader could "
              "doubt a source or our own value; leave the paper's own reasoning as it is. Stop for my tick.")
    op = _step_box("🔎 Stage 3 · Evidence", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "evidence"))
    cards = (_text_and_evidence(d, ev, root, opens) + _card_folds(ev) + _open_fold(opens) if ev["cards"] or opens else
             _not_yet("No Evidence cards yet."))
    if ev["proposals"]:
        lines = "".join(f'<li>{"☑" if t else "☐"} {_inline(line, {})}</li>' for t, line in ev["proposals"])
        cards += _fold("✍ Asks, for you to tick", f'<p class=space-reads>{_code(ev["props_path"], root)}</p>'
                       f'<ul style="list-style:none;padding-left:4px">{lines}</ul>', open_=open_asks > 0)
    if ev["problems"]:
        cards += _fold("❗ What does not resolve", "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in ev["problems"]) + "</ul>")
    return op, cards, ()


# ── 4 · Display ───────────────────────────────────────────────────────────────────────────────────
# A display (a figure or a table) is one unit, display/Display<n>-<slug>/ (haipipe-display), built on evidence cards and
# accepted by a person; it has its own step after 3 · Evidence (JL 261020: "If we have the display, hwo do we make it?
# will it be the DISPLAY X? Or we want to have a new display view after the 3 - Evidence? ... Please do it"; b34 s41
# Open 1). DISPLAY <n> is the unit's own number, as CITE <n> and VALUE <n> are the cards'.
DISPLAY_INK = "#e8590c"
CALLS = re.compile(r"\b(?:e?(?:Table|Figure)\s+\d+[A-Za-z]?|Overview Figure)\b")
REFS = re.compile(r"\\(?:ref|cref|Cref|autoref)\{([^}]+)\}")


def _field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^\s*{name}\s*:\s*(.+?)\s*$", text)
    return m.group(1).strip() if m else ""


def _units(folder: Path) -> list:
    """The Task's display units by number: display/Display<n>-<slug>/ (their one home, b34 s41 Ⓐ), and a unit that is
    still only in a display Run's newest pass (runs/run-display-*/passes/<pass>/payload/), where display/ has none of
    that name. What its README says: claim, kind, the name the text calls it by (`shown as:`, else the Table or Figure
    its Placement names), its \\label, built_on, accepted, status."""
    found = {}
    for p in sorted((folder / "runs").glob("run-display-*/passes/*/payload/Display*")) + sorted((folder / "display").glob("Display*")):
        if p.is_dir():
            found[p.name] = p                       # the newest pass, then display/, wins
    out = []
    for name, p in found.items():
        m = re.match(r"Display(\d+)-(.+)$", name)
        if not m:
            continue
        readme = p / "README.md"
        text = readme.read_text(encoding="utf-8", errors="replace") if readme.is_file() else ""
        tex = (p / "float.tex").read_text(encoding="utf-8", errors="replace") if (p / "float.tex").is_file() else ""
        place = re.search(r"(?ms)^##\s*Placement\s*\n(.*?)(?=^## |\Z)", text)
        head = re.search(r"(?m)^# (.+)$", text)
        # the name the text calls it by: `shown as:`, else a Table or Figure in its `label:`, its heading or its Placement
        hit = next((h for h in (CALLS.search(x) for x in (_field(text, "label"), head.group(1) if head else "",
                                                           place.group(1) if place else "")) if h), None)
        shown = _field(text, "shown as") or (hit.group(0) if hit else "")
        status = re.search(r"(?ms)^##\s*Status\s*\n+\s*(\S.*?)\s*$", text)
        pic = next((x for x in (p / "preview.png", p / "assets" / "figure.png", p / "assets" / "figure.svg") if x.is_file()), None)
        out.append({"n": int(m.group(1)), "slug": m.group(2), "dir": p, "readme": readme if readme.is_file() else None,
                    "claim": _field(text, "claim"), "shown": shown, "labels": set(re.findall(r"\\label\{([^}]+)\}", text + tex)),
                    "kind": _field(text, "kind") or ("table" if (p / "assets" / "table-body.tex").is_file() else "figure" if pic else ""),
                    "built_on": _field(text, "built_on"), "accepted": _field(text, "accepted"),
                    "layout": _field(text, "layout"), "made_by": _field(text, "made by"),
                    "status": (status.group(1) if status else _field(text, "status")).split(" (")[0], "pic": pic,
                    "pdf": p / "preview.pdf" if (p / "preview.pdf").is_file() else None,
                    "built": bool(pic or (p / "preview.pdf").is_file() or any((p / "assets").glob("*")))})
    return sorted(out, key=lambda u: u["n"])


def _calls(d: dict | None) -> dict:
    """What the text calls a display by, and its sentences in order: {"Table 1": ["S1", "S5"]}; a \\ref{label} too."""
    out = {}
    for _, body in (d or {}).get("text", []):
        for m in re.finditer(r"(?m)^- B\d+ · (S\d+[a-z]?) · (.*)$", body):
            for name in CALLS.findall(m.group(2)) + REFS.findall(m.group(2)):
                out.setdefault(name, []).append(m.group(1)) if m.group(1) not in out.get(name, []) else None
    return out


def _displays(folder: Path, d: dict | None) -> list:
    """Each display of the Section: every unit with the sentences that call it (by its `shown as` name or its \\label),
    then every name the text calls that no unit answers, not made yet."""
    calls, out, used = _calls(d), [], set()
    for u in _units(folder):
        names = [n for n in calls if (u["shown"] and n.lower() == u["shown"].lower()) or n in u["labels"]]
        used.update(names)
        words = u["slug"].replace("-", " ")
        out.append({**u, "label": f"DISPLAY {u['n']}", "names": names, "made": True,
                    "title": f"{u['shown']} · {words}" if u["shown"] else words,
                    "calls": sorted({s for n in names for s in calls[n]}, key=_s_key),
                    "ok": bool(u["accepted"]) and not u["accepted"].startswith("⬜")})
    out += [{"label": name, "names": [name], "made": False, "title": name, "calls": ss, "ok": False}
            for name, ss in calls.items() if name not in used]
    return out


def _display_card(x: dict, root: Path, big: bool = False) -> str:
    """One display: its DISPLAY number in orange, what the text calls it, accepted or not; its picture; its claim.
    Opened on its own (`big`), the picture at full width and the README's fields: built on, the sentences, the files."""
    chip = ('<span class="st st-ok">✓ accepted</span>' if x["ok"] else
            '<span class="st st-warn">✍ to accept</span>' if x.get("built") else
            '<span class=st>⬜ planned, not built</span>' if x["made"] else '<span class=st>⬜ not made yet</span>')
    head = (f'<b style="color:{DISPLAY_INK}">{esc(x["label"])}</b> · {esc(x["title"])} {chip}' if x["made"] else
            f'<b style="color:{DISPLAY_INK}">{esc(x["title"])}</b> {chip}')
    pic = ""
    if x.get("pic"):
        u = "/" + quote(_rel(x["pic"], root))
        pic = (f'<a href="{esc(u)}" target=_blank><img src="{esc(u)}" alt="{esc(x["title"])}" style="display:block;'
               f'max-width:100%;max-height:{"none" if big else "260px"};margin:8px 0 4px;border:1px solid var(--line)"></a>')
    elif x.get("pdf"):
        pic = f'<p style="margin:6px 0">{_code(x["pdf"], root)}</p>'
    body = head + pic + (f'<p class=mut style="margin:4px 0">{esc(x["claim"])}</p>' if x.get("claim") else "")
    if big:
        rows = [("Called by", esc(", ".join(x["calls"])) or '<span class=mut>no sentence yet</span>')]
        if x["made"]:
            rows += [("Kind", esc(x["kind"]) or "—"), ("Layout", esc(x["layout"]) or "—"),
                     ("Built on", esc(x["built_on"]) or '<span class=mut>not named yet</span>'), ("Made by", esc(x["made_by"]) or "—"),
                     ("Status", esc(x["status"]) or "—"), ("Accepted", esc(x["accepted"]) or '<span class=mut>not yet: only you write it</span>'),
                     ("Unit", _code(x["readme"], root) if x["readme"] else f'<code>{esc(_rel(x["dir"], root))}/</code>')]
        body += _kv(rows)
    return f'<div class="rv-card ev-card" data-s="{esc(x["calls"][0] if x["calls"] else "")}">{body}</div>'


def _display_step(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, xs = f["draft"], f["displays"]
    made = [x for x in xs if x["made"]]
    names = [x["names"][0] if x["names"] else x["label"] for x in xs]
    rows = [("Calls", esc(" · ".join(f"{x['title'] if not x['made'] else x['label']} ({', '.join(x['calls']) or 'no sentence'})"
                                     for x in xs)) or '<span class=mut>the text calls no Table or Figure yet</span>'),
            ("Units", esc(f"{len(made)} made: {sum(x['built'] for x in made)} built, {sum(x['ok'] for x in made)} accepted")
             if made else '<span class=mut>none yet in display/</span>'),
            ("Built on", _code(f["ev"]["path"], root) if f["ev"]["path"] else '<span class=mut>no evidence/cards.yaml yet</span>'),
            ("Accept", "only you write <code>accepted:</code> in a unit's README")]
    prompt = (f"/haipipe-display {f['t']}: for each display {f['section']} calls ({', '.join(names) or 'none yet'}), make or "
              "update its unit in display/Display<n>-<slug>/ (README: claim, kind, shown as, built_on its evidence cards; "
              "recipe, intake, assets, preview), its numbers read from the Runs its cards name; then check the numbers "
              "against the cards, and stop for my accept.")
    op = _step_box("🖼 Stage 4 · Display", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "display"))
    if not xs:
        return op, _not_yet("No display yet: the text calls no Table or Figure, and display/ is empty."), ()
    result = ""
    if d and d["text"]:
        marks = {n: (DISPLAY_INK if x["made"] else INK["need"], [x["label"]] if x["made"] else ["not made"])
                 for x in xs for n in x["names"]}
        right = {}
        for x in xs:
            right[x["calls"][0] if x["calls"] else ""] = right.get(x["calls"][0] if x["calls"] else "", "") + _display_card(x, root)
        body = (f'<p class=space-reads>{_code(d["file"], root)}</p>'
                + _text_rows(d, marks, right, "Displays no sentence calls"))
        result = EV_CSS + CARDS_CSS + _fold(f"🖼 The text and its displays · {d['version']}", body, open_=True) + CARDS_JS
    # each display on its own, folded, its picture at full width
    for x in xs:
        result += (f'<details class="topic work-task"><summary><span class=related-head><b style="color:{DISPLAY_INK}">'
                   f'{esc(x["label"] if x["made"] else x["title"])}</b>' + (f' · {esc(x["title"])}' if x["made"] else " · not made yet")
                   + '</span></summary><div class=work-body>' + _display_card(x, root, big=True) + '</div></details>')
    return op, result, ()


def _revise_passes(path: Path) -> list:
    """`draft/records/<stem>-revise.md` as its passes, newest first: [(title, [(head, {why, original, expected,
    state})])]. A Revise run rewrites the file as one `## Pass <k> · …` part, the latest only (JL 261020: "always keep
    the latest version"); an older file may still hold several, and only the newest shows. A file with none is one pass, named by its "Pass <k>,
    on draft v<N>" line (JL 261020: "everytime to run you will have many things new")."""
    text = path.read_text(encoding="utf-8", errors="replace")

    def cards(body: str) -> list:
        return [(m.group(1).strip(), {**{k.lower(): v.strip() for k, v in re.findall(
                    r"(?m)^(Why|Original|Expected|State):[^\S\n]*(.*)$", m.group(2))}, "body": m.group(2)})
                for m in re.finditer(r"(?ms)^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)", body)]
    parts = [(t.strip(), b) for t, _, b in (x.partition("\n") for x in re.split(r"(?m)^## ", text)[1:])
             if t.strip().lower().startswith("pass")]
    head = _before_passes(text)                  # cards above the first `## Pass` are a pass of their own, never lost
    if head.strip() and re.search(r"(?m)^### ", head):
        parts = [(_first_pass_title(text), head)] + parts
    passes = [(t, cards(b)) for t, b in parts]
    num = lambda t: int(re.search(r"\d+", t).group(0)) if re.search(r"\d+", t) else 0
    return sorted(passes, key=lambda x: -num(x[0]))


def _before_passes(text: str) -> str:
    """The part of a cards file above its first `## Pass` heading (the whole file when it has none)."""
    m = re.search(r"(?m)^## Pass", text)
    return text[:m.start()] if m else text


def _first_pass_title(text: str) -> str:
    """The name of the cards above the first `## Pass` heading: from its "Pass <k>, on draft v<N>" line, else Pass 1."""
    m = re.search(r"Pass (\d+), on draft (v\d+(?:\.\d+)*)", _before_passes(text))
    return f"Pass {m.group(1)} · on draft {m.group(2)}" if m else "Pass 1"


STATE_CHIP = {"proposed": '<span class="st st-warn">🔶 proposed</span>', "accepted": '<span class="st st-ok">✓ accepted</span>',
              "written": '<span class="st st-ok">✓ written</span>', "rejected": '<span class=st>✗ rejected</span>'}


def _old_new(old: str, new: str) -> str:
    """Original → Expected as one run of words: the words taken out struck in red, the words put in green."""
    a, b = old.split(), new.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op == "equal":
            out.append(esc(" ".join(a[i1:i2])))
        if op in ("delete", "replace"):
            out.append(f'<del style="color:#c92a2a;background:#fff5f5">{esc(" ".join(a[i1:i2]))}</del>')
        if op in ("insert", "replace"):
            out.append(f'<ins style="color:#2b8a3e;background:#ebfbee;text-decoration:none">{esc(" ".join(b[j1:j2]))}</ins>')
    return " ".join(out)


def _paragraph_plan(text: str):
    """A Section question's paragraph plan, "4 paragraphs, about 400 words: P1 the shift (S1 to S4) · P2 …", as (lead,
    {P1: its job}, note after it); None when it names fewer than two paragraphs."""
    m = re.match(r"^([^:]{0,80}):\s*(?=P\d+\s)", text)
    lead, rest = (m.group(1).strip(), text[m.end():]) if m else ("", text)
    items = [list(x) for x in re.findall(r"(?:^|·)\s*(P\d+)\s+(.*?)(?=\s*·\s*P\d+\s|$)", rest.strip())]
    if len(items) < 2:
        return None
    note, cut = "", re.search(r"\.\s+(?=[A-Z])", items[-1][1])     # a sentence after the last paragraph is a note
    if cut:
        note, items[-1][1] = items[-1][1][cut.end():].strip(), items[-1][1][:cut.start()]
    return lead, {k: v.strip().rstrip(".") for k, v in items}, note


def _plan_cell(text: str, changed: bool) -> str:
    if not text:
        return '<span class=mut>—</span>'
    body = re.sub(r"\((S\d+[^)]*)\)", r'<span class=mut>(\1)</span>', esc(text))     # its sentences, quiet
    return f'<span style="background:#ebfbee;border-radius:3px;padding:0 3px">{body}</span>' if changed else body


def _change(head: str, original: str, expected: str) -> str:
    """A card's change: an Edit's or Review's words old → new; a Section question's paragraph plans side by side, a row
    per paragraph, now against proposed, the changed ones tinted (JL 261020: "You can make it like the table?"); a
    question that names no paragraphs keeps its now and proposed lines."""
    if head.lower().startswith("section question"):
        now, new = _paragraph_plan(original), _paragraph_plan(expected)
        if now and new:
            keys = sorted(set(now[1]) | set(new[1]), key=lambda k: int(k[1:]))
            rows = [(f"<b>{esc(k)}</b>", _plan_cell(now[1].get(k, ""), False),
                     _plan_cell(new[1].get(k, ""), new[1].get(k, "") != now[1].get(k, ""))) for k in keys]
            heads = ("", "now" + (f" · {now[0]}" if now[0] else ""), "proposed" + (f" · {new[0]}" if new[0] else ""))
            notes = "".join(f'<p class=mut style="margin:4px 0">{esc(n)}</p>' for n in (now[2], new[2]) if n)
            return _table(tuple(esc(h) for h in heads), rows) + notes
        return (f'<p style="margin:4px 0"><span class=mut>now</span> {esc(original)}</p>'
                f'<p style="margin:4px 0"><span class=mut>proposed</span> {_listed(expected)}</p>')
    rows = _by_sentence(head, original, expected)
    return rows or f'<p style="margin:4px 0;line-height:1.6">{_old_new(original, expected)}</p>'


def _by_sentence(head: str, original: str, expected: str) -> str:
    """A change over several sentences, sentence by sentence (JL 261020: "I think this should be sentence by sentence"):
    a row per old sentence, its S, its words old → new. Each new sentence goes to the old one it reads most like; an
    old one that gets none shows struck, with the sentence it went into. "" when the change holds one old sentence."""
    from live.outline_revise import split_sentences
    old, new = split_sentences(original), split_sentences(expected)
    if len(old) < 2:
        return ""
    m = re.search(r"\bS(\d+)(?:\s*(?:to|–|-)\s*S?(\d+))?", head)
    first = int(m.group(1)) if m else None
    labels = ([f"S{first + i}" for i in range(len(old))] if m and m.group(2) and int(m.group(2)) - first + 1 == len(old)
              else [f"S{first}" if m and i == 0 else "" for i in range(len(old))])
    words = lambda t: [w.strip(".,;:()[]{}\"'“”").lower() for w in t.split()]
    like = [[difflib.SequenceMatcher(None, words(o), words(n)).ratio() for n in new] for o in old]
    # each new sentence's old one: the earliest that reads nearly as much like it as the best does, so sentences joined
    # into one stay at the first of them (S6 to S8 → S6); never before the one the sentence above went to, so the rows
    # keep reading order (a short new sentence split off S10 is not drawn back to S7 by a few shared words)
    home, at = [], 0
    for j in range(len(new)):
        best = max(like[k][j] for k in range(at, len(old)))
        at = min(i for i in range(at, len(old)) if like[i][j] >= 0.6 * best)
        home.append(at)
    rows = []
    for i, o in enumerate(old):
        mine = [new[j] for j in range(len(new)) if home[j] == i]
        if mine:
            change = _old_new(o, " ".join(mine))
        else:
            j = max(range(len(new)), key=lambda j: like[i][j]) if new else None
            went = (f'→ into {labels[home[j]] or "the sentence above"}' if j is not None and like[i][j] >= 0.15
                    else "→ taken out")
            change = (f'<del style="color:#c92a2a;background:#fff5f5">{esc(o)}</del> '
                      f'<span class=mut>{esc(went)}</span>')
        rows.append(f'<tr data-s="{esc(labels[i])}"><td class=mut style="white-space:nowrap;width:1%;padding:4px 8px 4px 0;'
                    f'vertical-align:top">{esc(labels[i] or "·")}</td><td style="padding:4px 0;line-height:1.6">{change}</td></tr>')
    return ('<table class=rv-rows style="border-collapse:collapse;width:100%;margin:4px 0">'
            + "".join(rows).replace("<tr", '<tr style="border-top:1px solid var(--line)"') + "</table>")


def _listed(text: str) -> str:
    """A proposal of several parts, "a new paragraph of 3 sentences after P1: S5 as its opener · "…" · "…"", as its lead
    and then one part a line, so each proposed sentence reads on its own."""
    lead, sep, rest = text.partition(": ")
    parts = [x.strip() for x in (rest if sep else text).split(" · ") if x.strip()]
    if len(parts) < 2:
        return esc(text)
    return ((esc(lead) + ":" if sep else "") + '<ul style="margin:4px 0 0;padding-left:20px">'
            + "".join(f'<li style="margin:2px 0">{esc(x)}</li>' for x in parts) + "</ul>")


def _revise_card(head: str, c: dict, task: str, title: str) -> str:
    """One Revise card a person acts on (JL 261020: "我想要那种可以交互的感觉"): its kind, sentence and job, its state;
    why; the change; then ✓ Accept · ✗ Reject · ✎ Edit, or ↺ Undo once decided. Hovering it lights its sentence in the
    text above. A click writes only the card's State (or its edited Expected) in the cards file (card_act)."""
    state = c.get("state", "proposed").split()[0].lower() if c.get("state") else "proposed"
    target = (re.match(r"[^·]+·\s*(S\d+[a-z]?)\b", head) or [None, ""])[1]
    para = (re.match(r"[^·]+·\s*(C\d+\.P\d+)\b", head) or [None, ""])[1]
    buttons = ('<p class=rv-acts style="margin:6px 0 0">'
               '<button type=button class=work-act data-card-act=accept>✓ Accept</button> '
               '<button type=button class=work-act data-card-act=reject>✗ Reject</button> '
               '<button type=button class=work-act data-card-act=edit>✎ Edit</button> '
               '<button type=button class=work-act data-card-act=undo>↺ Undo</button> '
               '<button type=button class=work-act data-card-act=save>Save the words</button> '
               '<button type=button class=work-act data-card-act=cancel>Cancel</button> '
               '<span class="rv-msg mut"></span></p>')
    # each item its own card, one light box (JL 261020: "I still want each of them to have a card"), and no box around
    # the pass, so never a box in a box ("I don't want this", of the cards inside the pass's frame)
    return (f'<div class="rv-card" data-task="{esc(task)}" data-pass="{esc(title)}" data-card="{esc(head)}" '
            f'data-state="{esc(state)}" data-s="{esc(target)}" data-p="{esc(para)}">'
            f'<div><b>{esc(head)}</b> <span class=rv-chip>{STATE_CHIP.get(state, esc(state))}</span></div>'
            f'<p class=mut style="margin:4px 0">{esc(c.get("why", ""))}</p>'
            f'<div class=rv-change>{_change(head, c.get("original", ""), c.get("expected", ""))}</div>'
            f'<div class=rv-edit contenteditable=true spellcheck=false>{esc(c.get("expected", ""))}</div>'
            f'{buttons}</div>')


CARDS_CSS = """<style>
.rv-card .rv-edit{display:none;margin:6px 0;padding:6px 10px;border-left:2px solid var(--acc);background:var(--wash);outline:none;line-height:1.6}
.rv-card.editing .rv-edit{display:block}.rv-card.editing .rv-change{display:none}
.rv-card [data-card-act=undo],.rv-card [data-card-act=save],.rv-card [data-card-act=cancel]{display:none}
.rv-card:not([data-state=proposed]) [data-card-act=undo]{display:inline-block}
.rv-card:not([data-state=proposed]) [data-card-act=accept],.rv-card:not([data-state=proposed]) [data-card-act=reject],
.rv-card:not([data-state=proposed]) [data-card-act=edit]{display:none}
.rv-card.editing [data-card-act]{display:none}.rv-card.editing [data-card-act=save],.rv-card.editing [data-card-act=cancel]{display:inline-block}
/* a plain box: no coloured side bar, no hover tint (JL 261020: "this is too AI"); the chip says the state */
.rv-card{border:1px solid var(--line);border-radius:3px;background:var(--card);padding:10px 14px;margin:0 0 12px}
.rv-card[data-state=rejected]{opacity:.55}
/* a card already written into the text has nothing left to decide */
.rv-card[data-state=written] .rv-acts{display:none}
li.rv-lit,h4.rv-lit,tr.rv-lit td{background:#fff3bf;border-radius:3px}
.rv-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:start}
.rv-right .rv-card{cursor:pointer}
.rv-split .rv-left{position:sticky;top:0;max-height:78vh;overflow-y:auto;padding-right:8px}
@media(max-width:1000px){.rv-split{grid-template-columns:minmax(0,1fr)}.rv-split .rv-left{position:static;max-height:none}}
</style>"""
CARDS_JS = """<script>
(function(){if(window.__rvCards)return;window.__rvCards=1;
 var CHIP={proposed:'<span class="st st-warn">🔶 proposed</span>',accepted:'<span class="st st-ok">✓ accepted</span>',
           rejected:'<span class=st>✗ rejected</span>',written:'<span class="st st-ok">✓ written</span>'};
 function msg(c,t,bad){var m=c.querySelector('.rv-msg');m.textContent=t||'';m.style.color=bad?'#c92a2a':'';}
 /* a card's sentences in the text: data-s holds one id (a Revise card) or several (an Evidence card), else its paragraph */
 function targets(c){var sp=c.closest('.rv-split'),root=sp?sp.querySelector('.rv-left'):document,out=[];
  (c.dataset.s||'').split(' ').forEach(function(s){var t=s&&root.querySelector('li[data-s="'+s+'"]');if(t)out.push(t);});
  var h=!out.length&&c.dataset.p&&root.querySelector('h4[data-p="'+c.dataset.p+'"]');if(h)out.push(h);return out;}
 function target(c){return targets(c)[0]||null;}
 /* a card's sentence lights in the text, which scrolls on its own to show it (the text stays beside the cards) */
 function lit(c,on){var ts=targets(c),t=ts[0];if(!t)return;ts.forEach(function(x){x.classList.toggle('rv-lit',on);});var left=t.closest('.rv-left');
  if(on&&left&&left.scrollHeight>left.clientHeight&&(t.offsetTop<left.scrollTop||t.offsetTop+t.offsetHeight>left.scrollTop+left.clientHeight))
   left.scrollTo({top:Math.max(0,t.offsetTop-left.clientHeight/3),behavior:'smooth'});}
 /* each card beside the sentence it changes (JL 261020: "one in the left, and one in the right"): pushed down to its
    sentence's line, never up over the card before it; one column on a narrow screen */
 function align(){document.querySelectorAll('.rv-split').forEach(function(sp){var cards=sp.querySelectorAll('.rv-right .rv-card');
  cards.forEach(function(c){c.style.marginTop='';});
  if(getComputedStyle(sp).gridTemplateColumns.split(' ').length<2||!sp.offsetParent)return;
  cards.forEach(function(c){var t=target(c);if(!t)return;var gap=t.getBoundingClientRect().top-c.getBoundingClientRect().top;
   if(gap>0)c.style.marginTop=gap+'px';});});}
 window.addEventListener('resize',align);window.addEventListener('load',align);setTimeout(align,60);
 document.addEventListener('toggle',function(){setTimeout(align,0);},true);
 document.addEventListener('click',function(e){if(!e.target.closest||e.target.closest('[data-card-act],.rv-edit,a'))return;
  var c=e.target.closest('.rv-right .rv-card'),t=c&&target(c);if(!t)return;
  t.scrollIntoView({behavior:'smooth',block:'center'});t.classList.add('rv-lit');setTimeout(function(){t.classList.remove('rv-lit');},1400);});
 function rowlit(r,on){var sp=r.closest('.rv-split');if(!sp)return;
  r.dataset.s.split(' ').forEach(function(s){var t=s&&sp.querySelector('.rv-left li[data-s="'+s+'"]');if(t)t.classList.toggle('rv-lit',on);});}
 /* the other way: a sentence in the text lights the card rows that name it */
 function sentlit(li,on){var sp=li.closest('.rv-split');if(sp)sp.querySelectorAll('.rv-right tr[data-s~="'+li.dataset.s+'"]')
  .forEach(function(r){r.classList.toggle('rv-lit',on);});}
 document.addEventListener('mouseover',function(e){if(!e.target.closest)return;var li=e.target.closest('.rv-left li[data-s]');if(li){sentlit(li,true);return;}
  var r=e.target.closest('.rv-rows tr[data-s]');if(r&&r.dataset.s){var rc=r.closest('.rv-card');if(rc)lit(rc,false);rowlit(r,true);return;}
  var c=e.target.closest('.rv-card');if(c)lit(c,true);});
 document.addEventListener('mouseout',function(e){if(!e.target.closest)return;var li=e.target.closest('.rv-left li[data-s]');if(li&&!li.contains(e.relatedTarget))sentlit(li,false);
  var r=e.target.closest('.rv-rows tr[data-s]');if(r&&!r.contains(e.relatedTarget))rowlit(r,false);});
 document.addEventListener('mouseout',function(e){var c=e.target.closest&&e.target.closest('.rv-card');if(c&&!c.contains(e.relatedTarget))lit(c,false);});
 /* ✓ Accept all shows while a card is still proposed */
 function scope(x){return x&&(x.closest('.rv-board')||x.closest('.rv-right'));}
 function allbtn(right){var b=right&&right.querySelector('[data-cards-all]');
  if(b)b.style.display=right.querySelector('.rv-card[data-state=proposed]')?'':'none';}
 /* one card's act, written in the cards file; resolves true once saved */
 function send(c,act,b){var ed=c.querySelector('.rv-edit');
  var body={task:c.dataset.task,pass:c.dataset.pass,card:c.dataset.card,was:c.dataset.state,
            state:{accept:'accepted',reject:'rejected',undo:'proposed',save:c.dataset.state}[act]};
  if(act==='save')body.expected=ed.innerText;
  if(b)b.disabled=true;msg(c,'…');
  return fetch('/_board/draft-card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){if(b)b.disabled=false;
     if(!j.ok){msg(c,j.err||'not saved',true);return false;}
     c.dataset.state=j.state;c.querySelector('.rv-chip').innerHTML=CHIP[j.state]||j.state;
     if(j.change){c.querySelector('.rv-change').innerHTML=j.change;}c.classList.remove('editing');msg(c,j.note||'');
     allbtn(scope(c));align();return true;})
   .catch(function(err){if(b)b.disabled=false;msg(c,String(err),true);return false;});}
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-card-act]');if(!b)return;e.preventDefault();
  var c=b.closest('.rv-card'),act=b.dataset.cardAct,ed=c.querySelector('.rv-edit');
  if(act==='edit'){c.classList.add('editing');c.dataset.before=ed.innerText;ed.focus();align();return;}
  if(act==='cancel'){ed.innerText=c.dataset.before||ed.innerText;c.classList.remove('editing');align();return;}
  send(c,act,b);});
 /* every card still proposed, one after another (a card's write reads the file the one before it wrote); the cards
    already decided stay as they are (JL 261020: "I will just accept all the changes here") */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-cards-all]');if(!b)return;e.preventDefault();
  var right=scope(b),cs=[].slice.call(right.querySelectorAll('.rv-card[data-state=proposed]'));b.disabled=true;
  cs.reduce(function(p,c){return p.then(function(){return send(c,'accept');});},Promise.resolve())
   .then(function(){b.disabled=false;allbtn(right);});});
})();
</script>"""


def _reading_key(head: str, d: dict) -> tuple:
    """Where a card sits in the text: the Section first, then a paragraph's first sentence, then its own sentence."""
    m = re.match(r"[^·]+·\s*(?:S(\d+)([a-z]?)|(C\d+\.P\d+)|(C\d+))\b", head)
    if not m:
        return (10 ** 6, "")
    if m.group(1):
        return (int(m.group(1)), m.group(2))
    if m.group(4):
        return (-1, "")
    body = "\n".join(b for _, b in (d or {}).get("text", []))
    sec = re.search(r"(?ms)^### " + re.escape(m.group(3)) + r"\b.*?^- B\d+ · S(\d+)", body)
    return (int(sec.group(1)) - 0.5, "") if sec else (10 ** 6, "")


def _text_and_cards(d: dict, ev: dict, root: Path, path: Path, task: Path) -> str:
    """The text on the left and its Revise cards on the right, in reading order (JL 261020: "How do you think we can
    merge them together, one in the left, and one in the right? so we can link to the original text as well"). Only the
    newest pass ("always keep the latest version"); it ends with the prompt that writes the accepted cards into the
    text as the next version.

    The text is one column with no space between its sentences, the same text 2 · Write, 3 · Evidence and 4 · Display
    show (JL 261020: "我不想让句子跟句子之间有这么大的空格 ... 在 revise、evidence、display 这里都保持一样的风格"): a card
    is placed at its sentence's line and pushed down only to clear the card above it (CARDS_JS `align`), the text
    never moves for a card, and it stays in view while the cards scroll. A card on the whole Section sits above, the
    full width."""
    marks = _marks(ev)
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks)
                   for t, b in d["text"])
    passes = _revise_passes(path)[:1] if path.is_file() else []
    title, cs = passes[0] if passes else ("", [])
    t = _rel(task, root)
    whole = lambda h: re.match(r"[^·]+·\s*C\d+\s*·", h)        # `Section question · C1 · …`, not `· C1.P2 · …`
    cs = [(h, c) for h, c in cs if not _is_report(h)]
    cards = sorted(cs, key=lambda x: _reading_key(x[0], d))
    # the pass's review report is its own section above this one (_review_report; JL 261021: "把那些比较详细的 review
    # report 单独作为一个新的 section ... 我还要之前的那个 revised card section")
    top = "".join(_revise_card(h, c, t, title) for h, c in cards if whole(h))
    right = "".join(_revise_card(h, c, t, title) for h, c in cards if not whole(h))
    some = any((c.get("state") or "proposed").split()[0].lower() == "proposed" for _, c in cs)
    head = (f'<h4 style="margin:0 0 8px">🃏 Revise cards · {esc(title)} <button type=button class=work-act '
            f'data-cards-all=accept style="margin-left:8px{"" if some else ";display:none"}">✓ Accept all</button></h4>'
            if cs else '<p class=space-empty>No Revise cards yet.</p>')
    tail = (f'<p><button type=button class="run-copy work-act" data-copy="{esc(f"/haipipe-draft {t} apply: write the accepted cards of {title} into ## 3 · Draft as the next version (the old one to previous/), mark each one written, and leave the rejected ones as they are.")}">Copy: apply the accepted cards</button></p>'
            if cs else "")
    body = (f'<p class=space-reads>{_code(d["file"], root)}' + (f' · {_code(path, root)}' if path.is_file() else "") + '</p>'
            f'<div class=rv-board>{head}{top}<div class=rv-split><div class=rv-left>{text}</div>'
            f'<div class=rv-right>{right}{tail}</div></div></div>')
    return CARDS_CSS + _fold(f"✍️ The text and its Revise cards · {d['version']}", body, open_=True) + CARDS_JS


def _is_report(head: str) -> bool:
    return head.lower().startswith(("revise review report", "current draft review report"))


# the base rubric's four axes, then sentence-to-sentence flow and the anti-AI audit (JL 261021: "你这个 rubric 怎么没有
# 分数？... 句子连贯性、反 AI 写法"), then the venue's own rule
RUBRIC_AXES = ("Mechanics", "Function", "Evidence", "Readability", "Coherence", "Anti-AI", "Venue")
AXIS_NAME = {"Anti-AI": "Anti-AI writing"}
VERDICT_CHIP = {"MEETS": "st st-ok", "NEEDS WORK": "st st-warn", "NOT VERIFIABLE": "st st-warn", "N/A": "st"}


def _review_report(path: Path) -> str:
    """The newest pass's review report as its own section, above the text and its cards (JL 261021: "above the section
    of 'The text and its Revise cards' you should give me the section 'Revise Review Report' and tell me for each
    rubric, how you feel about this draft"; "把那些比较详细的 review report 单独作为一个新的 section"). One row per axis
    of haipipe-draft-review's rubric (Mechanics, Function, Evidence, Readability, and the venue's own rule), each with
    its verdict (MEETS · NEEDS WORK · NOT VERIFIABLE · N/A), how the draft reads, and the smallest fix; then the
    paragraphs now against what the cards propose. Nothing here is accepted: the cards are the changes."""
    passes = _revise_passes(path)[:1] if path.is_file() else []
    if not passes:
        return ""
    title, cs = passes[0]
    rep = next((c for h, c in cs if _is_report(h)), None)
    if rep is None:
        return ""
    body = rep.get("body", "")
    field = lambda k: (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) or [None, ""])[1].strip()
    rows, scores = [], []
    for axis in RUBRIC_AXES:
        v = field(axis)
        if not v:
            continue
        verdict, _, rest = v.partition(" · ")
        sc = re.match(r"(\d+(?:\.\d+)?)/(10|5) · ", rest)     # `6/10 · …`: the reviewer's score (an older pass: /5)
        if sc:
            scores.append(float(sc.group(1)) * (2 if sc.group(2) == "5" else 1))
            rest = rest[sc.end():]
        reading, _, fix = rest.partition(" · Fix: ")
        chip = (f'<span class="{VERDICT_CHIP.get(verdict.strip().upper(), "st")}" style="white-space:nowrap">'
                f'{esc(verdict.strip())}</span>')
        rows.append((f"<b>{esc(AXIS_NAME.get(axis, axis))}</b>", chip,
                     f'<b>{sc.group(1)}</b><span class=mut>/{sc.group(2)}</span>' if sc else '<span class=mut>—</span>',
                     _inline(reading, {}), _inline(fix, {}) if fix else '<span class=mut>—</span>'))
    table = _change("Section question", field("Now"), field("Proposed")) if field("Now") and field("Proposed") else ""
    out = ((f'<p class=mut style="margin:0 0 6px">{_inline(field("Reviewer"), {})}</p>' if field("Reviewer") else "")
           + (f'<p style="margin:0 0 8px;line-height:1.6">{_inline(field("Verdict"), {})}</p>' if field("Verdict") else "")
           + (f'<p style="margin:0 0 6px"><b>Score {sum(scores) / len(scores):.1f} of 10</b> <span class=mut>· the mean '
              f'of {len(scores)} rows; a reading aid, never a pass mark</span></p>' if scores else "")
           + (_table(("rubric", "verdict", "score", "how the draft reads", "smallest fix"), rows) if rows else "")
           + (f'<p style="margin:8px 0 0;line-height:1.6"><span class=mut>The cards below:</span> '
              f'{_inline(field("Cards"), {})}</p>' if field("Cards") else "")
           + (f'<h4 style="margin:14px 0 4px">The paragraphs, now and as the cards propose</h4>{table}' if table else ""))
    return _fold(f"📋 Revise Review Report · {title}", out, open_=True)


def card_act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """A person's ✓ Accept, ✗ Reject, ↺ Undo or edited Expected on one Revise card (b32 s41-D32): writes only that card's
    `State:` (with the time) and, for an edit, its `Expected:` in `draft/records/<stem>-revise.md`. The text itself is
    changed by the pass that applies the accepted cards. Refused when the card changed on disk since the page showed
    it (`was`), so a person never writes over an agent's new pass."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    folder = (root / str(p.get("task") or "").strip("/")).resolve()
    md = face(folder) if folder.is_dir() and root in folder.parents else None
    if md is None:
        return 400, {"ok": False, "err": "no such Task"}
    path = folder / "draft" / "records" / f"{md.stem}-revise.md"
    state, head, title = str(p.get("state") or ""), str(p.get("card") or ""), str(p.get("pass") or "")
    if not path.is_file():
        return 404, {"ok": False, "err": f"no {path.name}"}
    if state not in ("proposed", "accepted", "rejected"):
        return 400, {"ok": False, "err": "a card is proposed, accepted or rejected"}
    text = path.read_text(encoding="utf-8")
    start, end = 0, len(text)
    sec = re.search(r"(?m)^## " + re.escape(title) + r"[^\S\n]*$", text) if title else None
    if sec:
        nxt = re.search(r"(?m)^## ", text[sec.end():])
        start, end = sec.end(), sec.end() + nxt.start() if nxt else len(text)
    elif title == _first_pass_title(text):       # the cards above the first `## Pass` heading
        end = len(_before_passes(text))
    else:
        return 409, {"ok": False, "err": "the pass changed on disk; reload"}
    seg = text[start:end]
    found = list(re.finditer(r"(?ms)^### " + re.escape(head) + r"[^\S\n]*\n(.*?)(?=^### |^## |\Z)", seg))
    if len(found) != 1:
        return 409, {"ok": False, "err": "the card changed on disk; reload"}
    body = found[0].group(1)
    cur = re.search(r"(?m)^State:[^\S\n]*(\S*)", body)
    now = (cur.group(1).lower() if cur and cur.group(1) else "proposed")
    if p.get("was") and str(p["was"]) != now:
        return 409, {"ok": False, "err": f"it is {now} on disk now; reload", "state": now}
    line = "State: proposed" if state == "proposed" else f"State: {state} · {datetime.datetime.now():%Y-%m-%d %H:%M}"
    body = re.sub(r"(?m)^State:.*$", line, body, count=1) if cur else body.rstrip("\n") + f"\n{line}\n\n"
    change = None
    if p.get("expected") is not None:
        words = " ".join(str(p["expected"]).split())
        if not words:
            return 400, {"ok": False, "err": "the new words are empty"}
        body = (re.sub(r"(?m)^Expected:.*$", lambda m: "Expected: " + words, body, count=1)
                if re.search(r"(?m)^Expected:", body) else body.rstrip("\n") + f"\nExpected: {words}\n\n")
        orig = re.search(r"(?m)^Original:[^\S\n]*(.*)$", body)
        change = _change(head, orig.group(1) if orig else "", words)
    seg = seg[:found[0].start(1)] + body + seg[found[0].end(1):]
    path.write_text(text[:start] + seg + text[end:], encoding="utf-8")
    return 200, {"ok": True, "state": state, "change": change}


def _revise(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, ev = f["draft"], f["ev"]
    revise_n = len(re.findall(r"(?m)^#{2,4} ", f["revise"].read_text(encoding="utf-8", errors="replace"))) \
        if f["revise"].is_file() else 0
    paras = _paragraphs(d["structure"][1]) if d and d["structure"] else []
    section = (f"{f['section']} · {len(paras)} paragraphs · {sum(len(b) for _, b in paras)} Bullets" if paras else
               f"{f['section']} · " + " · ".join(t for t, _ in (d or {}).get("text", [])) if d else f["section"])
    rows = [("Section", esc(section)),
            ("Draft", esc(f"{d['version']} · {len(d['previous'])} older in previous/") if d else '<span class=mut>—</span>'),
            ("Cards", esc(f"{len(ev['cards'])} Evidence · {revise_n} Revise")),
            ("Mode", "quick: no full review; the rubric only on ask")]
    job = face(chain(folder, root).get("Job") or folder)      # the draft's desk, else its version's (desk: jamaim)
    desk = ((d or {}).get("head", {}).get("desk", "") or f["head"].get("desk", "")
            or (_header(job.read_text(encoding="utf-8", errors="ignore")).get("desk", "") if job else "")).split(":")[0].strip()
    who = (f"a reviewer for {desk}" if " " in desk else f"a reviewer for the {desk} desk" if desk else
           "the reviewer this Section's venue would send")
    # think as the reviewer first (JL 261020: "think about yourself，就是你是一个什么样的 reviewer，你是怎么审这篇文章的")
    prompt = (f"/haipipe-draft {f['t']} revise: first think as {who}: who you are, what you look for, and how you "
              f"will review {f['section']} (the argument and its paragraphs first, then claims and evidence, then "
              "sentences); say it in three lines. Then read the Section and my notes, and rewrite "
              f"draft/records/{f['stem']}-revise.md as one new pass (## Pass <k> · <date> · on draft {d['version'] if d else 'v<N>'}), "
              "the latest only: carry over the cards of the last pass still undecided and still true, drop the rest "
              "(git keeps them). The pass opens with `### Revise review report`, one line each: Reviewer (those three "
              "lines), Verdict, then Mechanics, Function, Evidence, Readability, Coherence (sentence to sentence), Anti-AI "
              "(run haipipe-draft-review's cli/anti_slop.py audit and read its ref/ai-tells.md) and Venue, each "
              "`<MEETS | NEEDS WORK | NOT VERIFIABLE | N/A> · <0-10>/10 · how the draft reads · Fix: the smallest fix` "
              "(haipipe-draft-review ref/evaluation-rubric.md, its score bands and its Revise review overlay), "
              "and Cards, how the cards' own text scores on that audit, "
              "then Now and Proposed (the paragraphs as `P1 <job> (S1 to S4) · P2 …`); then Section questions on the "
              "structure, then Edit and Review cards, each with Why, Original, Expected and State: proposed. Rebuild "
              "the canvas.")
    # folded until opened: the text and its cards are what Revise is read for (JL 261020: "could you make this hidden
    # by default?")
    op = _step_box("🔁 Stage 5 · Revise", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "revise"),
                   open_=False, k=len(d["previous"]) if d else 0)
    canvas = [x for x in f["topics"] if (_notes(x[1]) and "canvas:" in _notes(x[1]).read_text(encoding="utf-8", errors="ignore"))]
    # the text, then its Revise cards by pass, then the canvas (JL 261020: "between these two, you should also add a
    # new one about the Revision card")
    cards = _text_and_cards(d, ev, root, f["revise"], folder) if d and d["text"] else ""
    if not cards:
        cards = _not_yet("No text yet.")
    cards = _review_report(f["revise"]) + cards
    if f["feedback"].is_file():
        cards += _fold("💬 Your marks from the canvas", _source(f["feedback"], root, ""))
    cards += "".join(_canvas_card(s, t, dr, root) for s, t, dr in canvas)
    # the rules every pass follows and the author's rulings, each with his words, kept across passes in their own file
    # (JL 261021: "可以在这里面再加一个 section，说明一下我们 revise 的规则是什么 ... 作者提出来的那些 revise 意见 ... 在这里也记录一下")
    rules = f["revise"].with_name(f"{f['stem']}-revise-rules.md")
    if rules.is_file():
        text = re.sub(r"\A#[^\n]*\n", "", rules.read_text(encoding="utf-8", errors="replace"))
        cards += _fold("📜 Revise rules · how a pass runs, and the author's rulings",
                       f'<p class=space-reads>{_code(rules, root)}</p>' + _md(text, {}))
    if d and d["previous"]:
        cards += _fold("🕘 Older versions", "<ul>" + "".join(f"<li>{_code(p, root)}</li>" for p in reversed(d["previous"]))
                       + "</ul>")
    return op, cards, ()


def _delivery_step(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d = f["draft"]
    out = delivery_dir(folder)
    where = _rel(out, root) + "/"
    built, pages = f["built"], f["pages"]
    to = next((r[1] for r in f["rows"] if "onedrive" in r[1].lower()), "")
    sub = {"build": "done" if built else ("next" if d and d["text"] else "todo"),
           "render": "done" if pages else ("next" if built else "todo"),
           "send": "done" if f["sent"] else ("send" if built else "todo"),
           "back": "done" if f["back"] else ("next" if f["sent"] else "todo")}
    t, s = f["t"], f["section"]
    boxes = [
        ("build", "📤 1 of 4 · build", [("Text", esc(f"the text {d['version']}" if d else "no draft yet")),
                                       ("Builds", "tex · docx · pdf"), ("Into", f"<code>{esc(where)}</code>"),
                                       ("Rule", "built, never edited by hand")],
         f"/haipipe-draft {t} deliver: build {s} into docx and pdf, and check it both ways."),
        ("render", "🖼 2 of 4 · render the pages", [("Files", esc(f"{len(built)} built") if built else '<span class=mut>none yet</span>'),
                                                   ("Makes", "<code>render/&lt;name&gt;-v&lt;N&gt;/p-&lt;k&gt;.png</code>"),
                                                   ("Why", "you see it as Word lays it out")],
         f"/haipipe-delivery render the newest {s} file of {t}, then show me the pages."),
        ("send", "✉️ 3 of 4 · check, then Send", [("Folder", f"<code>{esc(where)}</code>"),
                                                  ("To", esc(to) if to else '<span class=mut>not named yet</span>'),
                                                  ("State", "sent" if f["sent"] else "not sent: only you mark it sent")],
         f"/haipipe-draft {t} check: judge the built {s} read-only before I send it."),
        ("back", "📥 4 of 4 · read back, then another round?", [("From", esc(to) if to else '<span class=mut>—</span>'),
                                                               ("Saves", "the next <code>-v&lt;N&gt;</code>, rendered, its new comments"),
                                                               ("Next", "round n+1 in this Section's topic, or stop")],
         f"/haipipe-delivery pull {s} of {t} back: save it as the next version, render it, list the new comments."),
    ]
    op = "".join(_step_box(title, sub[k], "<h4>Input</h4>" + _kv(rows) + _prompt_box(p, folder, root, f"delivery-{k}"))
                 for k, title, rows, p in boxes)
    pics = ("".join(f'<a href="/{esc(quote(_rel(p, root)))}" target=_blank><img src="/{esc(quote(_rel(p, root)))}" '
                    f'alt="{esc(p.stem)}" style="width:230px;margin:4px;border:1px solid var(--line)"></a>' for p in pages))
    cards = (delivery_cards(folder, root, f["md"])
             + (_fold("🖼 The pages, as Word lays them out", pics, open_=True) if pages else "")
             + (_fold("✉️ Sends, from the Block's delivery.md", _table(("date", "for", "status"),
                      [(esc(a), esc(b), esc(c)) for a, b, c in f["rows"]])) if f["rows"] else ""))
    return op, cards, ()


STEP_VIEWS = {"Studio": _studio, "1 · Plan": _plan, "2 · Write": _write, "3 · Evidence": _evidence_step, "4 · Display": _display_step,
              "5 · Revise": _revise, "Delivery": _delivery_step}


def _running(f: dict, step: str) -> str:
    """What an agent is running for this step now, under Operation (JL 261021: "如果在跑的话，能不能在这个页面里面显示正在
    running？ ... 在 operation 下面要不要加 status"): from `draft/records/<stem>-running.md`, one line per open run,
    `- [<step>] <what> · since <time>`, which the agent writes when the run starts and removes when it ends. A line
    left behind shows its start time, so a stale one is plain to see."""
    path = f["revise"].with_name(f"{f['stem']}-running.md")
    if not path.is_file():
        return ""
    rows = re.findall(r"(?m)^- \[(.+?)\] (.+?) · since (.+?)\s*$", path.read_text(encoding="utf-8", errors="replace"))
    return "".join(f'<p class=run-now style="margin:0 0 8px;padding:6px 10px;border:1px solid var(--line);'
                   f'border-radius:3px">⏳ <b>Running now</b> · {esc(what)} <span class=mut>· since {esc(t)}</span></p>'
                   for s, what, t in rows if s.strip() == step)


def step_view(folder: Path, root: Path, step: str) -> tuple:
    """(Work html, Report html, the open step, its own run types) for one step tab; a bare link opens the step that
    comes next."""
    f = facts(folder, root)
    st = states(f)
    step = step if step in STEPS else current(st)
    op, result, runs = STEP_VIEWS[step](f, folder, root, st[step])
    # your own changes are typed in 2 · Write, its editor beside the text (_text_and_editor); 5 · Revise keeps only the
    # cards (JL 261020: "remove this Change it yourself in the Revise, as that will be in the Writing")
    edit = ""
    # Scratch is planning, so it sits in 1 · Plan, written where it is read (JL 261020: "for the scratch, it doesnt
    # work anymore"; "I think we should move the scratch here"): the Page's own Scratch view, a note per paragraph,
    # opened by its heading
    if step == "1 · Plan" and f["draft"] and f["draft"]["structure"]:
        edit += _editor(folder, root, "📝 Scratch · your notes, a paragraph each", view="scratch", open_=False)
    work = _part("Operation") + _running(f, step) + op + edit + _part("Result") + result
    # Report keeps the prompts of the two writing steps (JL 261020: "we should also need to think about to add the
    # prompt to help the structure and drafting, right?")
    ask = op if step in ("1 · Plan", "2 · Write", "5 · Revise") else ""
    return work, ask + edit + _part("Result") + result, step, runs
