"""The draft Task's Studio and Delivery views, and its branches on the map."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote
from live import draft_steps as ds
from live.frame import esc, face
from live.ui_parts import _file_link, _section, _when
from live.focus_draft_words import CAPTIONS, WIDE
from live.focus_draft_assets import CSS, JS, borrowed_css
from live.focus_draft_steps import SECTION_VERBS, _facts, _runs, boxes_of, quiet, work_views
from live.focus_draft_report import paragraphs, report_views, responds_to, review_points

# ── Studio and Delivery ─────────────────────────────────────────────────────────────────────────────
def studio_inventory(folder: Path, root: Path) -> list:
    """(source, topic, drawings) of the Block topics whose face names this Task: what the base Studio lists."""
    try:
        return ds._studio_topics(folder, root)
    except Exception:
        return []


def studio_top(folder: Path, root: Path) -> str:
    """Above the base Studio's rows: the Studio step's prompt as a verb (talk and sketch); "none yet" when no topic
    names this Task."""
    f, st, k = _facts(folder, root)
    op, _, _ = ds._studio(f, folder, root, st["Studio"])
    # only the step's Copy prompt box, as the Section Studio drawing settled (s40 r03, pick B: "Copy prompt only, no
    # new-topic button"); it was worked out and then dropped, so the Studio showed no prompt (found 261105)
    prompt = quiet(boxes_of(op))                 # r02: Studio said it was empty twice; the base Studio says it once
    return CSS + prompt + JS


READER = (".pdf", ".docx", ".html")             # what a reader opens; .tex, .json and -view.html stay in Files only


PREVIEW_CSS = ("<style>.fd-prev{display:block;width:100%;height:calc(100vh - 300px);min-height:620px;border:1px solid "
               "var(--line);border-radius:6px;background:#fff}.fd-prev-h{font-size:13px;color:var(--muted);margin:0 0 8px}"
               "</style>")


def build_prompts(folder: Path, root: Path) -> list:
    """The Section's Delivery prompts (build, render the pages, check, read back), each a Prompt box with Copy prompt,
    the session line copied but not shown."""
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        op, _, _ = ds._delivery_step(f, folder, root, st["Delivery"])
    finally:
        ds.FLAT.reset(token)
    return [quiet(b) for b in re.findall(r"<!--pb-prompt-->.*?<!--/pb-prompt-->", op, re.S)]


def preview(f: Path | None, root: Path, also: Path | None = None, ask: str = "") -> str:
    """One built file, previewed in the page (JL 261007: "the card and the preview of the results, the embedded
    content"; JL 261031: "I thnk we want to make it to be previewed here"): its name, state and built time, Open ↗ to a
    new tab, then the file itself; Word through the PDF twin the build writes beside the .docx (`also`)."""
    if not f or not f.is_file():                 # r01: "Ask the agent builds it" named no control; its Copy prompt is here
        return ('<p class=mut>Not built yet.</p>' + ask
                if ask else '<p class=mut>Not built yet.</p>')
    url = "/" + quote(ds._rel(f, root))
    state = "draft" if "-draft" in f.stem else "built"
    extra = f' · {_file_link(also, root)}' if also and also.is_file() else ""
    return (PREVIEW_CSS + f'<p class=fd-prev-h>{esc(f.name)}{extra} · {state} · {_when(f)} · '
            f'<a href="{esc(url)}" target=_blank rel=noopener>Open ↗</a></p>'
            f'<iframe class=fd-prev src="{esc(url)}" loading=lazy title="{esc(f.name)}"></iframe>')


def delivery_html(folder: Path, root: Path) -> str:
    """A Section's Delivery › Files: each lane's reader files (current or not built), the rendered pages, the sends,
    the Runs, and last the prompts (build, render, check, read back). The send itself waits on the version page."""
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        op, _, _ = ds._delivery_step(f, folder, root, st["Delivery"])
    finally:
        ds.FLAT.reset(token)
    try:
        from live.delivery import check_delivery
        lanes = check_delivery(f["md"]).get("lanes", []) if f["md"] else []
    except Exception:
        lanes = []
    url = lambda p: "/" + quote(ds._rel(p, root))
    rows = []
    for lane in lanes:
        key = lane.get("lane", "")
        ldir = ds.delivery_read_lane_dir(folder, key)
        files = sorted(p for p in ldir.rglob("*") if p.is_file() and p.suffix in READER and not p.name.startswith(".")
                       and not p.stem.endswith("-view")) if ldir.is_dir() else []
        state = {"pass": "current", "stale": "stale", "not-built": "not built"}.get(lane.get("state", ""), lane.get("state", ""))
        cls = "fd-ok" if state == "current" else "fd-you" if state == "stale" else ""
        links = " · ".join(_file_link(p, root) for p in files) or "nothing built"
        rows.append(f'<div class=fd-row><span class=n>{esc(ds.LANE_ICON.get(key, ""))} {esc(lane.get("label", key))}</span>'
                    f'<span class=d>{links}</span><span class="w {cls}">{esc(state)}</span></div>')
    pics = "".join(f'<a data-pop="{esc(p.stem)}" href="{esc(url(p))}"><img src="{esc(url(p))}" alt="{esc(p.stem)}" '
                   f'style="width:200px;margin:4px;border:1px solid var(--line)"></a>' for p in f["pages"])
    sends = "".join(f'<div class=fd-row><span class=n>{esc(a)}</span><span class=d>{esc(b)}</span><span class=w>{esc(c)}</span></div>'
                    for a, b, c in f["rows"])
    states = [lane.get("state", "") for lane in lanes]
    # each lane row shows its own state; the bar says "current" or "stale" only, never "N of M current" or "nothing built yet"
    built = ("" if not states or all(x == "not-built" for x in states) else
             "current" if all(x == "pass" for x in states) else "stale" if "stale" in states else "")
    try:
        asks = "".join(build_prompts(folder, root))
    except Exception:
        asks = ""
    return (CSS + _section("Built files", "".join(rows) or '<p class=mut>Nothing built yet.</p>', built)
            + _section("The pages, as Word lays them out", pics, f'{len(f["pages"])} pages' if f["pages"] else "")
            + _section("Sends", sends, "sent" if any("sent" in str(c).lower() for _, _, c in f["rows"]) else "")
            + _runs(folder, root, "Delivery")
            + _section("🤖 Ask the agent", asks, built) + JS)


def section_delivery_views(folder: Path, root: Path) -> dict:
    """A Section's Delivery view-button-list: PDF · Word · Web · Files, each lane previewed in the page."""
    name = face(folder).stem if face(folder) else folder.name
    lane = lambda key: ds.delivery_read_lane_dir(folder, key)

    def gap() -> str:
        """JL 261102: the PDF printed draft v0.1 while the plan beside it was v0.3, and the page did not say so."""
        try:
            from src.page_adopt import content_gap
            g = content_gap(folder)
        except Exception:
            return ""
        return (f'<div class=fd-ask role=status><span>⚠️ This prints {esc(g["printed"])}; the current draft is '
                f'{esc(g["current"])}. It is behind: {esc(g["why"])}, then export, before reading it as final.'
                '</span></div>') if g else ""
    def ask() -> str:                            # the build's own Copy prompt, where a lane is not built yet
        try:
            return build_prompts(folder, root)[0]
        except Exception:
            return ""
    return {"pdf": ("PDF", lambda: CSS + gap() + preview(lane("latex") / f"{name}.pdf", root, ask=ask()) + JS),
            "word": ("Word", lambda: CSS + gap() + preview(lane("word") / f"{name}.pdf", root, lane("word") / f"{name}.docx", ask()) + JS),
            "web": ("Web", lambda: CSS + gap() + preview(lane("web") / "index.html", root, ask=ask()) + JS),
            "files": ("Built files", lambda: delivery_html(folder, root))}


def aim(folder: Path) -> str:
    """The Task's Aim: a Section's `reader-question:` (its face has no goal)."""
    md = face(folder)
    m = re.search(r"(?m)^reader-question:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    return m.group(1).strip() if m else ""


SENT = re.compile(r"^- B\d+ · (S\d+[a-z]*) · (?:\[[^\]]+\]\s*)?(.*\S)")


def branches(folder: Path, root: Path) -> list:
    """A draft Task's MindMap is its paper content (JL 261031: "I think the mindmap here should be the paper content"):
    each paragraph of §1 Structure, under it each point (its Bullet's head), and the point's sentence from §3 Draft
    unfolded beneath it. Steps, files and Runs are not on it: they are Report › Status, Delivery and Work › Runs."""
    import mmbuild
    d = ds.read_draft(folder)
    if not d or not (d.get("text") or d.get("structure")):
        return content_branches(folder) + answers_branch(folder, root)   # r02: Text showed the adopted Content while
    said, order = {}, []                                 # the map said "Nothing to map yet"; §3: S<n> -> its sentence
    for _, body in d["text"]:
        para = None
        for line in body.splitlines():
            h = re.match(r"^###\s+(.*\S)", line)
            if h:
                para = h.group(1)
                order.append((para, []))
                continue
            m = SENT.match(line)
            if m and para:
                said[m.group(1)] = m.group(2)
                order[-1][1].append(m.group(1))
    plan = ds._paragraphs(d["structure"][1]) if d.get("structure") else []
    points = {head: bullets for head, bullets in plan}
    out = []
    for k, (head, ids) in enumerate(order or [(h, [b[0] for b in bs]) for h, bs in plan]):
        pid, _, rest = head.partition(" · ")
        name = rest.split(" · ")[0].strip() or pid
        planned = {sid: words for sid, _, words in points.get(head, [])}
        sids = ids or list(planned)
        kids = [mmbuild.built(f"{folder}/c/{k}/{sid}", f"[{sid}] {planned.get(sid) or ' '.join(said.get(sid, '').split()[:8])}",
                              [], [said[sid]] if sid in said else [])
                for sid in sids]
        out.append(mmbuild.built(f"{folder}/c/{k}", f"[{pid}] {name}", kids))
    return (out or content_branches(folder)) + answers_branch(folder, root)


def content_branches(folder: Path) -> list:
    """The adopted Content as the map, when no draft holds a plan or a text: each paragraph, each sentence under it, the
    same text Report › Text shows."""
    import mmbuild
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    out = []
    for k, (pid, name, text) in enumerate(p for p in paragraphs(folder) if p[2]):
        sents = [re.sub(r"\\cite[pt]?\{([^}]*)\}", lambda m: "[" + m.group(1).replace(",", ", ") + "]", x)
                 for x in split_sentences(text)]               # a citation command reads as its keys, as on Text
        kids = [mmbuild.built(f"{folder}/c/{k}/S{j}", f"[S{j}] {' '.join(x.split()[:8])}", [], [x])
                for j, x in enumerate(sents, 1)]
        out.append(mmbuild.built(f"{folder}/c/{k}", f"[{pid}] {name or pid}", kids))
    return out


def answers_branch(folder: Path, root: Path) -> list:
    """A response letter's map: the comments it answers, each point with who raised it, where it lands, its reply
    paragraph and its state (r01: "put each Review Item beside its reply in MindMap")."""
    import mmbuild
    report = responds_to(folder)
    if report is None:
        return []
    from live.frame import reader
    names = {pid.split(".")[-1]: name for pid, name, _ in paragraphs(folder)}
    kids = [mmbuild.built(f"{folder}/answers/report", f"[report] [{report.parent.name}]({reader(report, root)})")]
    for i, (point, who, lands, reply, state) in enumerate(review_points(report, folder)):
        kids.append(mmbuild.built(f"{folder}/answers/{i}", f"[{state or 'open'}] {point}",
                                  [mmbuild.built(f"{folder}/answers/{i}/who", f"[raised by] {who}")] * bool(who)
                                  + [mmbuild.built(f"{folder}/answers/{i}/lands", f"[lands on] {lands}")] * bool(lands)
                                  + [mmbuild.built(f"{folder}/answers/{i}/reply",
                                                   f"[reply] {reply}: {names[reply]}" if reply in names else
                                                   f"[reply] {reply}" if reply else "[reply] not written yet")]))
    return [mmbuild.built(f"{folder}/answers", "Comments it answers", kids)]


def parts(folder: Path, root: Path, url) -> dict:
    """What the base focus page asks of a draft Task (its one hook): Work's views, their words and the open one,
    Report's views, Studio's topics, Delivery, the Aim and the captions."""
    from live.address_links import linked_views, page_linker
    link = page_linker(folder, root)                    # every bNN.jNN.tNN.rNN a link (address_links, JL 261103)
    work, _, waiting = work_views(folder, root)         # a view button carries only its name (AGENTS § Page words):
    work = linked_views(work, link)                     # no "pass 1" / "done" state word on it, so no words map
    work["runs"] = ("Runs", None)                       # the base fills it with the Task's Runs
    return {"work": work, "words": {}, "open": waiting, "report": linked_views(report_views(folder, root, url), link),
            "delivery_views": section_delivery_views(folder, root),
            "studio": studio_inventory(folder, root), "studio_top": lambda: studio_top(folder, root), "delivery": lambda: delivery_html(folder, root),
            "aim": aim(folder), "captions": CAPTIONS, "verbs": SECTION_VERBS, "css": WIDE + borrowed_css() + JS}
