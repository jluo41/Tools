"""The draft Task's seven step tabs, as b32 s41 draws them: Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise ·
Delivery, named the same in Work and Report (s41 Ⓐ; JL 261015: "So it is the Studio, 1, Plan, ..... and Delivery as
the last one").

Each tab is Operation over Result, as an items or building Task's Stages are (b15 s41, s42): Operation is what a
person does in the step (its Input, read from disk; the Sign it waits for; the prompt, which takes the person's notes
and is copied with them), Result is what the step made, one folded card per topic. Report shows the Results only.
Every open reads the files again, so the canvas and the tabs never drift apart (s41-D28): the newest draft
(`draft/<stem>-draft-v<N>.md`: its header, §1 Structure, §2 Scratch, §3 Draft), `draft/records/`, `draft/previous/`,
`evidence/cards.yaml` and `proposals.md` (haipipe-evidence), the Block's Studio topics (`sNN-<topic>/`) that name
this Task (s41-D24), and the Block's `delivery/<jNN>/<tNN>/` (s41-D04). Nothing here writes.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote, urlencode

from src.common import delivery_dir, delivery_read_lane_dir
from live.frame import ROUTE, _draw_url, _notes, _reader, _rel, _table, _topic_row, chain, esc, face, pop, studio_inventory, theme_of

# the step modules beside this file; every name they hold stays reachable as draft_steps.<name>, as callers use it
from live.draft_steps_assets import (  # noqa: F401
    CARDS_CSS, CARDS_JS, EV_CSS, EX_CSS, FIT, FIT_STYLE, NOTES_CSS, NOTES_JS, OFF_CSS, WRITE_JS)
from live.draft_steps_common import (  # noqa: F401
    _add_mark, _canvas_card, CARDS, _cards_module, CHIPS, _code, _drawn_inside, FLAT, _fold, _header, INK, _inline,
    _kv, _Marks, _marks, _md, _not_yet, _paragraphs, _part, _parts, _plan_tree, _poss, _prompt_box, PROMPT_HEAD,
    read_draft, _sentence, _session, _signed, SKILLS, _source, _step_box, _sx_row, _task_session, VERSION, _version,
    _word)
from live.draft_step_plan import (  # noqa: F401
    _bullet_block, _cap, CONTRACT, _examples, _examples_card, _kind_of, _mapview, _para_span, _paragraph_marks,
    _plan, plan_act, _plan_map, RUBRIC, _rubric_card, _served)
from live.draft_step_evidence import (  # noqa: F401
    CALLS, _calls, _card_folds, _display_card, DISPLAY_INK, _display_step, _displays, _embed_displays, _ev_card,
    EV_STATE, _evidence_row, _evidence_step, _field, MARK, _num, _open_fold, OPEN_KIND, _open_points, _open_row,
    REFS, _s_ids, _s_key, _sx_attr, _sx_bar, _sx_board, _sx_fill, _sx_key, SX_OLD, _sx_paras, SX_SLOT,
    _text_and_evidence, _text_rows, _units)
from live.draft_step_revise import (  # noqa: F401
    _answered_by, AXIS_NAME, _before_passes, _bib_ref, _by_sentence, card_act, _change, _chosen, _comments,
    _comments_path, _ev_item, _ev_side_card, _first_para, _first_pass_title, _flow_card, _is_report, _listed,
    _logic_card, note_act, _note_card, NOTE_LABEL, NOTE_TARGET, _old_new, _options, _paragraph_plan, _plan_cell,
    _proposed_cards, _reading_key, _review_chips, _review_report, _revise, _revise_card, _revise_passes,
    RUBRIC_AXES, _score_ink, _sentence_lines, STATE_CHIP, _text_and_cards, VERDICT_CHIP)

# 4 · Display after 3 · Evidence (JL 261020: "Or we want to have a new display view after the 3 - Evidence? ... Please do it")
STEPS = ("Studio", "1 · Plan", "2 · Write", "3 · Evidence", "4 · Display", "5 · Revise", "Delivery")


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
            title = card.get("title") or (CARDS.title_of(CARDS.resolve(project, kind, src, folder)) if project and src else src)
        except Exception:
            title = src
        items = []
        for it in card.get("items", []):
            state, value = ("need", "") if it.get("need") else ("have", "")
            if it.get("run") and project:
                try:
                    res = CARDS.resolve(project, kind, f"{src}.{it['run']}", folder)
                    it = {**it, "result": res}
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


def _editor(folder: Path, root: Path, title: str, view: str = "revise", open_: bool = True) -> str:
    """Your own changes, typed in place: the Page's Revise boxes (outline_revise.py, one box per paragraph, its
    sentences a line each, Why · Reset · Save into `## 3 · Draft`), embedded and open (JL 261020: "How could I write
    my own changes? that is my question"; "it is kind of hard to me to modify the content, right?")."""
    src = _editor_src(folder, root, view)
    if not src:
        return ""
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head>'
            f'<b>{esc(title)}</b></span><span class=topic-pop>{pop(src.replace("&embed=1", ""), title, "↗")}</span>'
            f'{_word("yours to edit")}</summary><iframe class=space-frame title="{esc(title)}" src="{esc(src)}" style="{FIT_STYLE}" onload="{FIT}">'
            '</iframe></details>')


def _editor_src(folder: Path, root: Path, view: str = "revise") -> str:
    """The Page's own editor for this Task's draft, embedded: its Revise boxes, or its Scratch; or "" with no Block."""
    block, md = chain(folder, root).get("Block"), face(folder)
    if not block or not md or not face(block):
        return ""
    return "/_board/draft?" + urlencode({"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(),
                                         "embed": "1", "space": "bullet", "view": view})


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
        # folded until opened: one line per delivery, its state and its files, and the preview on a click (JL 261021:
        # "你这个东西 by default 它不能够 hide 吗？"); a folded preview is not loaded until then
        cards.append(f'<details class="topic dl-card"><summary class=dl-sum>{head}</summary>'
                     f'{legacy_note}{body}</details>')
    css = '<style>.topic>.dl-sum{align-items:center}.dl-sum .st-bar{flex:1}</style>'   # the ▸ is .topic's own
    return (css + "<h2>Deliveries</h2>" + "".join(cards) if cards else
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
    # a sentence, not only the `### C1.P1` headings an empty § 3 is laid out with
    written = bool(d and any(re.search(r"(?m)^(?![ \t]*(?:#|<!--))[ \t]*\S", b) for _, b in d["text"]))
    needed = any(it["state"] != "have" for c in ev["cards"] for it in c["items"])
    open_asks = any(not ticked for ticked, _ in ev["proposals"])
    return {"Studio": "done" if f["topics"] else "optional",
            "1 · Plan": ("done" if _signed(d) else "sign") if d and d["structure"] else "next",
            "2 · Write": (("done" if _signed(d) else "early") if written else
                          ("next" if d and d["structure"] else "todo")),
            "3 · Evidence": (("asked" if needed or open_asks or any(o["kind"] != "none" for o in _open_points(d))
                              else "done") if ev["cards"] else
                             "next" if written or (d and d["structure"]) else "todo"),
            # a display waits on a person to accept it; a Section that calls none needs none
            "4 · Display": (("done" if all(x["ok"] for x in f["displays"]) else
                             "sign" if all(x.get("built") for x in f["displays"]) else "next" if written else "todo")
                            if f["displays"] else "optional"),
            # waits only while the newest pass still has a proposed card; an applied or written pass is done
            "5 · Revise": (("pass" if _proposed_cards(f["revise"]) else "done") if f["revise"].is_file()
                           else "next") if written else "todo",
            "Delivery": (("done" if f["sent"] else "send") if f["built"] else "next" if written else "todo")}


def current(st: dict) -> str:
    """The tab a bare link opens: the first step that waits on a person or comes next; the Studio is optional."""
    return next((s for s in STEPS[1:] if st[s] in ("next", "sign", "send")), STEPS[1])


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
    # the Section's own topic (its name carries the Section's), else a new one: a topic that only lists this Task, as a
    # paper checklist does, is not where its argument is sketched (r01: the letter's prompt targeted s05-paper-checklist)
    slug = folder.name.split("_", 1)[-1]
    own = [t for _, t, _ in f["topics"] if slug and slug in t.name]
    sid = own[0].name.split("-", 1)[0] if own else "a new topic"
    prompt = (f"/haipipe-studio {_rel(block, root) if block else f['t']} {sid}: talk with me about {_poss(f['section'])} "
              f"argument and sketch it on the canvas; write no text yet; what we settle goes into the Task's §1.")
    op = _step_box("🎨 Studio · talk and sketch", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "studio"))
    # each topic its own card, not cards in a "logic sketch" box (JL 261020: "I want this to be of the item itself,
    # not box of box")
    result = ((_topic_rows(f, root) if f["topics"] else _not_yet(f"No Studio topic for {folder.name} yet."))
              + (f'<p>{pop(studio, "the Block Studio", "Open the Block Studio ↗")}</p>' if studio else ""))
    run = {"label": "run-draw-<sNN>", "doing": "talk and sketch", "prompt": prompt, "skills": ["haipipe-studio"]}
    return op, result, (run,)


def _write(f: dict, folder: Path, root: Path, st: str, editor: bool = True) -> tuple:
    """Stage 2 · Write. With `editor=False` (the Draft view, where the sentence board already shows the text) your
    own editor is one folded box instead of a second copy of the text beside it."""
    d, ev = f["draft"], f["ev"]
    plan = ("§1, signed" if _signed(d) else "§1, not signed yet" if d and d["structure"] else
            "no §1 yet: the Section's contract")
    now = (f'{_code(d["file"], root)} · {esc(d["head"].get("version") or d["version"])}' if d else
           '<span class=mut>no draft yet</span>')
    # examples first (JL 261022: "你应该先找 example，看看别人是怎么写 abstract 的，然后再看怎么写 ... 在 write 的时候，你应该
    # 先找到相应的 example，这样我们就可以 follow 别人的参考了"): the published papers' same Section, read before a word
    try:
        exs = _examples(f, root)
    except Exception:
        exs = []
    tops = list(dict.fromkeys(e["topic"].name for e in exs))
    rows = [("Plan", esc(plan)), ("Studio", esc(" · ".join(t.name for _, t, _ in f["topics"]) or "no topic")),
            ("Examples", esc(f'{len(exs)} papers · {" · ".join(e["short"] for e in exs)} ({", ".join(tops)})') if exs
             else '<span class=mut>none yet: found and read first</span>'),
            ("Writes", "§3 Draft, from §1 and its Scratch (1 · Plan), following the examples, no rules yet"), ("Now", now)]
    follow = (f"first read the {len(exs)} examples in {', '.join(tops)} and note, for each paragraph or heading, the move "
              "and length they share; then " if exs else
              f"first find 3 to 4 published papers of the venue whose {f['section']} we could follow and read each one's "
              f"{f['section']} whole into a Studio topic sNN-{folder.name}-examples (/excalidraw-read), noting the move "
              "and length each paragraph or heading shares; then ")
    prompt = (f"/haipipe-draft {f['t']} write: {follow}redraft {f['section']} from my notes, its Scratch and §1, "
              "following them; keep every sentence I typed; name each place ours departs from the examples and why; no "
              "rules yet; mark each claim that waits for evidence." if d and d["text"] else
              f"/haipipe-draft {f['t']} write: {follow}scratch §2 from the plan, then write §3 for {f['section']} "
              "following them; name each place ours departs and why; mark claims you cannot support yet.")
    # the drafting ask, open (JL 261020: "add the prompt to help the structure and drafting"); the structure ask is
    # 1 · Plan's, beside the Scratch
    op = _step_box("✍️ Stage 2 · Write", st, "<h4>Input</h4>" + _kv(rows)
                   + _prompt_box(prompt, folder, root, "write", "✍️ Prompt · draft"))
    try:                                           # the examples beside the writing, as 1 · Plan shows them
        shown = _examples_card(exs, d, f, folder, root, own=True)
    except Exception as e:
        shown = _fold("📚 Examples", _not_yet(f"The examples do not read: {e}"))
    if not d or not d["text"]:
        return op, shown + _not_yet("No text yet."), ()
    own = _text_and_editor(d, ev, root, folder) if editor else _editor(folder, root, "✍️ Write it yourself", open_=False)
    cards = shown + own + "".join(_fold(f"🗒 {t}", _md(b, {}), word="a note")
                                                                     for t, b in d["notes"])
    return op, cards, ()


def _text_card(d: dict, ev: dict, root: Path) -> str:
    """The text as it reads, a sentence a line with its S number and its evidence boxed: Write's Result, and Revise's
    too (JL 261020, on Revise's "No Revise cards yet": "I think things here should be in the Results here")."""
    marks = _marks(ev)
    body = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks, _parts(d))
                   for t, b in d["text"])
    return _fold(f"✍️ The text · {d['version']}", f'<p class=space-reads>{_code(d["file"], root)}</p>' + body, open_=True,
                 word=_pending_word(d))


def _text_and_editor(d: dict, ev: dict, root: Path, folder: Path) -> str:
    """The text as it reads on the left, your own editor on the right (JL 261020: "I want to put the "Write it
    yourself" in the right of the "The Text" itself ... just like the Text + Evidence Panel and Text + Revising
    Panel"). The row you point at or type in lights its sentence on the left, and a sentence you point at lights its
    row; once a box saves, the left reads the text again."""
    src = _editor_src(folder, root, "revise")
    if not src:
        return _text_card(d, ev, root)
    marks = _marks(ev)
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "") + _md(b, marks, _parts(d))
                   for t, b in d["text"])
    text = _embed_displays(text, d, _displays(folder, d), root)
    right = (f'<h4 style="margin:0 0 4px">✍️ Write it yourself {pop(src.replace("&embed=1", ""), "Write it yourself", "↗")}</h4>'
             f'<iframe class=space-frame title="Write it yourself" src="{esc(src)}" style="{FIT_STYLE}" '
             f'onload="{FIT};window.wrHook&&window.wrHook(this)"></iframe>')
    body = (f'<p class=space-reads>{_code(d["file"], root)}</p><span class=wr-msg role=status>Loading the editor…</span>'
            f'<div class="rv-split wr-split"><div class=rv-left>{text}</div><div class=rv-right>{right}</div></div>')
    return CARDS_CSS + _fold(f"✍️ The text · {d['version']}", body, open_=True, word=_pending_word(d)) + WRITE_JS


def _pending_word(d: dict) -> str:
    """The text's word: how many ⟦…⟧ marks still wait in it (a claim waiting for evidence, a check), else none open."""
    n = sum(len(re.findall(r"⟦[^⟧]*⟧", b)) for _, b in d.get("text", []))
    return f'{n} mark{"s" if n != 1 else ""} open' if n else "no marks open"


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
         f"/haipipe-draft {t} deliver: on my ok, page.py bump (the next draft version), page.py adopt, cards.py bib "
         f"--write (the .bib from the cited Runs), then page.py export --author \"<the author>\" (web, LaTeX, Word); "
         f"check that no citation prints as ?, and read both PDFs."),
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
    from live.address_links import page_linker
    link = page_linker(folder, root)            # every bNN.jNN.tNN.rNN a link (address_links, JL 261103)
    return link(work), link(ask + edit + _part("Result") + result), step, runs
