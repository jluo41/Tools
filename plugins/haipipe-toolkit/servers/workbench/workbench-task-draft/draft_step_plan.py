"""1 · Plan of the draft Task (draft_steps.py): the plan's mind map, its in-place edits (plan_act), the examples and
the rubric card, and the step itself (_plan); draft_steps re-exports them all."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live.frame import _draw_url, _notes, _rel, _table, chain, esc, face, pop
from live.draft_steps_assets import EX_CSS, OFF_CSS
from live.draft_steps_common import (
    _canvas_card, _code, _drawn_inside, _fold, _header, INK, _inline, _kv, _not_yet, _paragraphs, _plan_tree,
    _prompt_box, read_draft, _signed, SKILLS, _source, _step_box, _word)


RUBRIC = SKILLS / "1_base/draft/haipipe-draft-review/ref/evaluation-rubric.md"
# the face fields a Section's Story hands its plan (haipipe-paper-draft): the plan's frame before §1 exists
CONTRACT = ("reader-question", "entry-state", "exit-state", "must-establish", "must-refuse", "transition-out",
            "story-row")


def _mapview():
    """haipipe-mindmap's mapview.py, the structure map this §1 shares with a Studio topic's mind map (JL 261026)."""
    import sys
    from host_paths import skill_dir
    scripts = str(skill_dir("haipipe-mindmap") / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import mapview
    return mapview


def _paragraph_marks(d: dict, kind: str) -> dict:
    """{C1.P3: its mark} for each paragraph outside 4 to 7 sentences (JL 261112: "unless having good reason, we might
    make sure they are between 4~7 sentences"): red with its count to fix, muted when its plan gives a `reason:`.
    Only a paper Section (`section_kind:`, the Abstract and the exempt kinds left out), read by haipipe-draft's rule."""
    try:
        from src.paragraph_length import RANGE, off_range
        text = d["file"].read_text(encoding="utf-8", errors="ignore") if d and d.get("file") else ""
    except Exception:
        return {}
    rng = f"{RANGE[0]} to {RANGE[1]}"
    return {pid: (f'<span class=pm-okr title="{esc(why)}">{n} sentences · reason given</span>' if why else
                  f'<span class=pm-off title="a paragraph holds {rng} sentences">❗ {n} sentences ({rng})</span>')
            for pid, n, why in off_range(text, kind)} if kind else {}


def _plan_map(d: dict, ev: dict, section: str, task: str = "", kind: str = "") -> str:
    """§1 drawn as a mind map (JL 261020: "merge them together, how do you think you can draw the mind map for the plan?
    ... To show what is this paper about?"): the Section and its arc in the middle; its parts (C1, C2, …) when it has
    more than one; its paragraphs, with the question each hands to the next on the arrow between them; each Bullet a
    leaf with its role and its evidence cards. A Bullet's note shows on hover; a ⟦check⟧ in it shows in red. Drawn by
    haipipe-mindmap's shared map (mapview.render), the one a Studio topic's mind map is drawn by too."""
    parts, asks, paras = _plan_tree(d["structure"][1])
    cards = {}
    for c in ev["cards"]:
        for it in c["items"]:
            ink = INK["need"] if it["state"] != "have" else INK.get(c["kind"], INK["value"])
            for k in it.get("for") or []:                  # 6, "6b" and "S6b" all name S6b's sentence
                got = cards.setdefault("S" + str(k).lstrip("S"), {})
                got[c["label"]] = INK["need"] if INK["need"] in (got.get(c["label"]), ink) else ink

    def chips(s, words, note):                             # a ⟦check⟧ in the note in red, then the evidence cards
        flag = re.search(r"⟦[^⟧]*⟧", note)
        flag = f' <span class=pm-flag>{esc(flag.group(0))}</span>' if flag and flag.group(0) not in words else ""
        return flag + "".join(f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(lab)}</span>'
                              for lab, ink in cards.get(s, {}).items())

    marks = _paragraph_marks(d, kind)
    return (OFF_CSS if marks else "") + _mapview().render(
        section, d["head"].get("arc") or "", parts, asks, paras, task=task, file=d["file"].name,
        inline=lambda words: _inline(words, {}), chips=chips, pnode=(lambda pid: marks.get(pid, "")) if marks else None)


def _kind_of(folder: Path) -> str:
    """A paper Section's `section_kind:` from its face; "" for any other page."""
    face_ = folder / f"{folder.name}.md"
    m = re.search(r"(?m)^section_kind:\s*(\S.*?)\s*$", face_.read_text(encoding="utf-8", errors="ignore")) if face_.is_file() else None
    return m.group(1) if m else ""


def _bullet_block(lines: list, s: str, lo: int, hi: int) -> tuple:
    """(start, end) of the §1 Bullet `S<s>` between lines lo and hi: its line and its indented Note and More lines."""
    for i in range(lo, hi):
        if re.match(r"^- B\d+[a-z]* · " + re.escape(s) + r" · ", lines[i]):
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
        m = re.match(r"^(- B\d+[a-z]* · \S+ · )(?:\[([^\]]*)\]\s*)?(.*?)\s*$", lines[at[0]])
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
        prev = [x for x in re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", "\n".join(lines[top:to]))]
        ids = set(re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", "\n".join(lines[top:hi])))
        m = re.match(r"S(\d+)([a-z]?)", prev[-1]) if prev else None
        num = m.group(1) if m else "0"
        letter = chr(ord(m.group(2)) + 1) if m and m.group(2) else "a"
        while f"S{num}{letter}" in ids:
            letter = chr(ord(letter) + 1)
        sid = f"S{num}{letter}" if prev or ids else "S1"
        bs = [int(x) for x in re.findall(r"(?m)^- B(\d+)[a-z]* · ", "\n".join(lines[span[0]:span[1]]))]
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
        if re.search(r"(?m)^- B" + re.match(r"- B(\d+)[a-z]*", block[0]).group(1) + r" · ", own):   # its B taken there
            n = max((int(x) for x in re.findall(r"(?m)^- B(\d+)[a-z]* · ", own)), default=0) + 1
            block[0] = re.sub(r"^- B\d+[a-z]*", f"- B{n}", block[0])
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


def _examples_card(exs: list, d: dict, f: dict, folder: Path, root: Path, own: bool = False) -> str:
    """The Studio topic that reads the published papers, opened straight onto its drawing (JL 261020: "could you make
    things here to be the excalidraw using the /excalidraw-read, but we still use the one from the sNN studio"; "here I
    will expect it to be a frame of the sNN studio"): excalidraw-read's topic canvas, one row per paper, its passages
    shot from the PDF and linked to our paragraphs. With no such topic, the prompt that makes one."""
    if not exs:
        job = face(chain(folder, root).get("Job") or folder)
        desk = ((d or {}).get("head", {}).get("desk", "") or f["head"].get("desk", "") or
                (_header(job.read_text(encoding="utf-8", errors="ignore")).get("desk", "") if job else "")).split(":")[0]
        ask = (f"/excalidraw-read {f['t']}: find 3 to 6 papers published in {desk.strip() or 'the target venue'} itself "
               f"(only that journal, JL 261022: \"MUST NMI\"; each named by its title first) of the same article type, whose "
               f"{f['section']} we could follow; make a Studio topic sNN-{folder.name}-examples (/haipipe-studio) holding "
               f"a screenshot of each paper's {f['section']} (reads/pNN-<author><year>/shots/section.jpg), drawn by "
               "excalidraw-read ref/section_screens.py; say how each is written, never what the study found.")
        return _fold("📚 Examples", _not_yet("No example papers yet.") + f'<p><button type=button class="run-copy '
                     f'work-act" data-copy="{esc(ask)}">Copy prompt · find examples</button></p>')
    inside = _drawn_inside(f)
    canvas = [(s, t, dr) for s, t, dr in f["topics"] if any(e["topic"] in inside for e in exs) and dr
              and _notes(t) and re.search(r"(?m)^\s*examples:", _notes(t).read_text(encoding="utf-8", errors="ignore"))]
    if canvas:                                     # one canvas, ours and the examples side by side (s22 draws s26);
        # 2 · Write opens it first and says what it holds (JL 261022, of s22: "I want things like this")
        n = len(exs)
        return "".join(_canvas_card(s, t, dr, root, f"📚 Our text beside {n} published examples · {t.name}" if own
                                    else "", open_=own) for s, t, dr in canvas)
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
        out.append(f'<details class="topic work-task"><summary><span class=related-head><b>{esc(title)}</b></span>'
                   f'<span class=topic-pop>{pop(url, top.name, "↗")}</span>{_word("drawn")}'
                   f'</summary><iframe class=st-frame title="{esc(top.name)}" data-src="{esc(url)}" '
                   'referrerpolicy=no-referrer></iframe></details>')
    return "".join(out)


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


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
                    for m in re.finditer(r"(?m)^- B\d+[a-z]* · S\d+[a-z]* · (.*)$", b))
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
            if a not in ("Axis", "Score")]             # its score table's head is not an axis (r03)
        alt = _served(root / "Tools" / RUBRIC.relative_to(SKILLS.parents[2]), root)
        body += ('<h4 style="margin:12px 0 4px">The four axes</h4>' + _table(("axis", "the question"), axes)
                 + '<p class=mut style="margin:4px 0">MEETS · NEEDS WORK · N/A · NOT VERIFIABLE (never a pass)'
                 + (f' · <a href="{esc(alt)}" target=_blank>{esc(RUBRIC.name)} ↗</a>' if alt else "") + '</p>')
    return EX_CSS + _fold("📏 Requirement and Rubric", body or _not_yet("No requirement yet."),
                          word="beside the examples" if exs and d and d.get("structure") else "set" if body else "")


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
        cards = _fold(f"📐 §1 Structure · {d['version']}", _plan_map(d, f["ev"], f["section"], _rel(folder, root), _kind_of(folder)),
                      open_=True, word="signed" if _signed(d) else "not signed yet")   # the wait is said once, in Process (r02)
    else:
        cards = _not_yet("No §1 Structure yet.")
    try:                                           # an example that does not read: say so, never break the frame
        exs = _examples(f, root)
        cards += _examples_card(exs, d, f, folder, root)
    except Exception as e:
        exs = []
        cards += _fold("📚 Examples", _not_yet(f"The examples do not read: {e}"))
    contract = [(esc(_cap(k.replace("-", " "))), esc(head[k])) for k in CONTRACT if head.get(k)]   # words, not keys (r03)
    if contract:
        cards += _fold("🧭 The Section's contract, from its Story", _kv(contract), open_=not paras)
    try:
        cards += _rubric_card(exs, d, f, root)
    except Exception as e:
        cards += _fold("📏 Requirement and Rubric", _not_yet(f"The rubric does not read: {e}"))
    recs = f["records"]
    cards += _fold("🗂 Records", _table(("record", "bytes"), [(_code(r, root), esc(r.stat().st_size)) for r in recs])
                   if recs else _not_yet("No records yet."), word=(f"{len(recs)} kept" if recs else ""))
    return op, cards, ()
