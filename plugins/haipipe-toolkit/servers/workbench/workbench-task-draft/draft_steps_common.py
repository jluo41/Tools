"""The small parts every draft step uses (draft_steps.py): reading the newest draft, its marks, and the boxes, folds,
prompts and sentence text each step draws with; draft_steps re-exports them all."""
from __future__ import annotations

import contextvars
import importlib.util
import re
from pathlib import Path

from live.frame import _draw_url, _notes, _reader, _rel, chain, esc, face, pop


# set while the focus page draws a step (focus_draft.py): each Result card is then a section, never a fold
FLAT = contextvars.ContextVar("draft_steps_flat", default=False)
SKILLS = Path(__file__).resolve().parents[3] / "skills"
VERSION = re.compile(r"-draft-v(\d+(?:\.\d+)*)\.md$")
CHIPS = {"done": '<span class="st st-ok">✓ done</span>', "next": '<span class="st st-warn">→ next</span>',
         "sign": '<span class="st st-warn">✍ sign</span>', "asked": '<span class="st st-warn">🔶 asked</span>',
         "send": '<span class="st st-warn">✍ send</span>', "optional": '<span class=st>· optional</span>',
         "pass": '<span class="st st-warn">🔁 pass {k}</span>',
         "todo": '<span class=st>· later</span>',
         # § 3 written on an unsigned plan: out of order, back to 1 · Plan (JL 261111, haipipe-draft § The Plan gate)
         "early": '<span class="st st-warn">❗ before the sign</span>'}
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
        b = re.match(r"^- B\d+[a-z]* · (S\d+[a-z]*) · (?:\[([^\]]+)\]\s*)?(.*\S)", line)   # S3a: a split sentence
        if cur is not None and b:
            cur[1].append((b.group(1), b.group(2) or "", b.group(3)))
    return out


class _Marks(dict):
    """phrase → (ink, card names) over the whole text, and `by_sentence`: S id → the same map for the items that name
    that sentence in `for` ("*" for an item that names none). A sentence boxes only its own items' anchors, so a short
    anchor such as "1 percent" (S36a) is not boxed inside "1.41 percent" in S5b (MISQ t05, 261022)."""
    by_sentence: dict


def _add_mark(out: dict, phrase: str, ink: str, label: str):
    prev = out.get(phrase, (ink, []))
    out[phrase] = (INK["need"] if INK["need"] in (prev[0], ink) else ink, prev[1] + ([label] if label not in prev[1] else []))


def _marks(ev: dict) -> dict:
    """Each anchor's words → (ink, the card names that back them): boxed in the text with the names beside them."""
    out = _Marks()
    out.by_sentence = {}
    for c in ev["cards"]:
        for it in c["items"]:
            ink = INK["need"] if it["state"] != "have" else INK.get(c["kind"], INK["value"])
            sids = ["S" + str(n).lstrip("S") for n in it.get("for") or []] or ["*"]
            for phrase in map(str, it.get("anchor") or []):   # a bare number in YAML (3.35) reads as a float
                _add_mark(out, phrase, ink, c["label"])
                for sid in sids:
                    _add_mark(out.by_sentence.setdefault(sid, {}), phrase, ink, c["label"])
    return out


# ── the look: the items and building Tasks' boxes (b15 s41, s42), drawn here so a base type needs no theme ───────
def _kv(rows) -> str:
    """A name/value table, the names in a shaded column that does not wrap."""
    cell = "padding:5px 10px;border:1px solid var(--line);vertical-align:top"
    body = "".join(f'<tr><th style="{cell};background:var(--wash);font-weight:600;text-align:left;white-space:nowrap;'
                   f'width:1%">{k}</th><td style="{cell};overflow-wrap:anywhere">{v}</td></tr>' for k, v in rows)
    return f'<table style="border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:14px"><tbody>{body}</tbody></table>'


def _word(word: str) -> str:
    """A card's state word on the focus page's bar (JL 261106: "every closed bar shows a state word on its right"); the
    old page's folds keep their own look, so it is drawn only there (FLAT)."""
    if not FLAT.get() or not word:
        return ""
    from live.ui_parts import word_span
    return word_span(word)


def _fold(title: str, body: str, open_: bool = False, word: str = "") -> str:
    """A Result card: its title, folded until opened. On the focus page (FLAT set, focus_draft.py) the same card is a
    section under its heading, open, with no box (b32 s42, JL 261031: "under each view, we will have the sections"),
    its state word on its bar; a card that holds only "not yet" carries no word (its body says so)."""
    if FLAT.get():
        return f'<section class=fd-sec><h3 class=fd-h>{esc(title)}{_word(word)}</h3>{body}</section>'
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
    `Paper-Example-B: j01-jamaim-full-t01-introduction` (JL 261020: "Paper-Example-B: j01jamaim-full-t01-intro")."""
    c = chain(folder, root)
    slug = lambda f: re.sub(r"_v\d{4}(?=_|$)", "", f.name).replace("_", "-")
    # a Job's own work panel (insight's Job steps, 261022) names the Job once, never `<job>-<job>`
    name = "-".join(([slug(c["Job"])] if c.get("Job") and c["Job"] != folder else []) + [slug(folder)])
    return f'{c["Block"].name}: {name}' if c.get("Block") else name


def _session(folder: Path, root: Path) -> str:
    """The Claude Code session this Task's work runs in, one per Task, shared by all its step prompts (JL 261020:
    "这个是 introduction，就要专门为 introduction 开一个 session ... 这些 task 应该 share 一个 session"): the Task
    face's `session:` line, else the Task's own name; never its Job's, which names the whole version."""
    md = face(folder)
    name = _header(md.read_text(encoding="utf-8", errors="ignore")).get("session", "") if md else ""
    return name.strip() or _task_session(folder, root)


def _prompt_box(prompt: str, folder: Path, root: Path, key: str, title: str = "Prompt") -> str:
    """The step's prompt in the one Prompt box every theme shares (servers/workbench/ui_parts.prompt_box; JL 261101,
    b15 s58 C1): the prompt, one "your notes" row copied with it (kept in this browser, the same key as before), and
    the line that sends it to the Task's session (`session:` on its face), so pasted into any session it still runs
    where this Task's work lives (JL 261020)."""
    from live.ui_parts import prompt_box               # here, not at the top: ui_parts reads nothing of draft_steps
    k = f"{_rel(folder, root)}#{key}"
    step, asks = PROMPT_HEAD.get(key, (re.sub(r"^(?:Prompt|Copy prompt)\b[:· ]*", "", title).strip() or key, ""))
    return prompt_box(prompt, None, _session(folder, root), step=step, asks=asks, key=f"notes:{k}")


PROMPT_HEAD = {"plan": ("Plan", "shape the structure"), "write": ("Write", "draft or rewrite the text"),
               "evidence": ("Evidence", "find each item's evidence"), "display": ("Display", "make the displays"),
               "revise": ("Revise", "one revise pass"), "studio": ("Studio", "talk and sketch"),
               "delivery-build": ("Build", "the Section's web, LaTeX and Word files"),
               "delivery-render": ("Render", "the pages as Word lays them out"),
               "delivery-send": ("Check", "the built files before you send"),
               "delivery-back": ("Read back", "the copy that came back")}


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
            # a quiet underline in the card's ink, filled only while its sentence is read (JL 261024: more readable)
            held.append(f'<mark class=ev-mark style="--ink:{ink}">{p}</mark>'
                        f'<sup style="color:{ink};font-weight:600"> {esc(", ".join(labels))}</sup>')
            s = s.replace(p, f"\x00{len(held) - 1}\x00")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"⟦([^⟧]*)⟧", r'<span style="color:#e03131;font-weight:600">⟦\1⟧</span>', s)
    # a citation reads as its keys, quiet and small (JL 261021: "读起来比较乱糟糟的"), not as LaTeX
    s = re.sub(r"\\citep\{([^}]*)\}", lambda m: '<span class=cite>[' + "; ".join(
        k.strip() for k in m.group(1).split(",") if k.strip()) + "]</span>", s)
    s = re.sub("\x00(\\d+)\x00", lambda m: held[int(m.group(1))], s)
    # a citation inside a marked phrase reads the same way (JL 261024: "\\citep{Wang_2022}" showed raw in S6)
    return re.sub(r"\\citep\{([^}]*)\}", lambda m: '<span class=cite>[' + "; ".join(
        k.strip() for k in m.group(1).split(",") if k.strip()) + "]</span>", s)


def _sentence(item: str, marks: dict) -> str:
    """A §3 line, `B1 · S1 · text`: its sentence number small and grey, then the sentence, each in its own span, so the
    text column can hang the numbers in a gutter on the left (CARDS_CSS)."""
    m = re.match(r"^B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", item)
    if m and isinstance(marks, _Marks):
        marks = {**marks.by_sentence.get("*", {}), **marks.by_sentence.get(m.group(1), {})}
    return (f'<span class="mut s-no" style="font-size:12px">{esc(m.group(1))}</span> '
            f'<span class=s-tx>{_inline(m.group(2), marks)}</span>' if m else _inline(item, marks))


def _parts(d: dict) -> dict:
    """{C<n>: its name} from §1's Structure Overview (`- C1 · Agreeableness and the Tension in Prescribing`)."""
    return dict(_plan_tree(d["structure"][1])[0]) if d and d.get("structure") else {}


def _sx_row(left: str, key: str, cls: str = "") -> str:
    """One row of the sentence board: the sentence (or a paragraph's heading) on the left, an empty slot on the right
    that `_sx_fill` fills with the cards on it."""
    return (f'<div class="rv-split sx-row{(" " + cls) if cls else ""}"><div class=rv-left>{left}</div>'
            f'<div class=rv-right data-slot="{esc(key)}"></div></div>')


def _md(text: str, marks: dict, parts: dict = None, rows: bool = False) -> str:
    """A part of the draft as a reader sees it: paragraphs, ### headings and lists. With `parts`, each subsection's
    name stands above its first paragraph (JL 261113: "I didn't see the subsection here"). With `rows`, every sentence
    is its own row with a slot for its cards, and every paragraph heading one for the paragraph's (JL 261113: "the
    sentences will be the basic unit"); each sentence carries its full address, C1.P2.S2, in `data-a`."""
    out, part, pid = [], None, ""
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        while lines and lines[0].startswith("#"):
            h = lines.pop(0).lstrip("#").strip()
            p_ = re.match(r"(C\d+\.P\d+)\b", h)
            c_ = p_ and p_.group(1).split(".")[0]
            if parts and c_ in parts and c_ != part:
                part = c_
                h3 = f'<h3 class=rv-part data-c="{c_}" data-p="{c_}">{esc(c_)} · {esc(parts[c_])}</h3>'
                # the Section's own row, with a slot for cards on the whole Section (JL 261113: "for the section or for
                # the paragraph, could we add the cards as well?")
                out.append(_sx_row(h3, c_, "sx-c") if rows else h3)
            h4 = (f'<h4{(" data-p=" + chr(34) + p_.group(1) + chr(34)) if p_ else ""} style="margin:12px 0 4px">'
                  f'{_inline(h, marks)}</h4>')
            if p_:
                pid = p_.group(1)
            out.append(_sx_row(h4, pid, "sx-p") if rows and p_ else h4)
        if not lines:
            continue
        if re.match(r"^\s*(?:[-*]|\d+\.)\s", lines[0]):
            items = []
            for line in lines:
                if re.match(r"^\s*(?:[-*]|\d+\.)\s", line):
                    items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s", "", line))
                elif items:
                    items[-1] += " " + line.strip()
            if rows:
                for i in items:
                    m = re.match(r"^B[0-9]+[a-z]* · (S[0-9]+[a-z]?) · ", i)
                    a = (f"{pid}.{m.group(1)}" if pid else m.group(1)) if m else ""
                    out.append(_sx_row(f'<ul><li data-s="{m.group(1)}" data-a="{esc(a)}">{_sentence(i, marks)}</li></ul>', a)
                               if m else f"<ul><li>{_sentence(i, marks)}</li></ul>")
                continue
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


def _poss(name: str) -> str:
    """A name's possessive: "Introduction's", "Response to the reviewers'" (r01: "reviewers's")."""
    return name + ("'" if name.endswith("s") else "'s")


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
        b = re.match(r"^- B\d+[a-z]* · (S\d+[a-z]*) · (?:\[([^\]]+)\]\s*)?(.*\S)", line)
        n = re.match(r"^\s+Note:\s*(.*\S)", line)
        if b:
            last = [b.group(1), b.group(2) or "", b.group(3), ""]
            cur[2].append(last)
        elif n and last and cur[2] and cur[2][-1] is last:
            last[3] = n.group(1)
    return parts, asks, paras


def _canvas_card(source: Path, topic: Path, drawings: list, root: Path, title: str = "", open_: bool = False) -> str:
    """A Section canvas opened straight onto its drawing, no topic row inside the card (JL 261020: "could I open
    this, and the content here is shown directly? ... No need to have box in box"); `title` names what it shows when
    it is the examples beside our text (2 · Write)."""
    head = title or f"🎨 The Section canvas · {topic.name}"
    if not drawings:
        return _fold(head, _not_yet("No drawing yet."))
    url = _draw_url(drawings[0], root)
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head><b>'
            f'{esc(head)}</b></span><span class=topic-pop>{pop(url, topic.name, "↗")}</span>{_word("drawn")}</summary>'
            f'<iframe class=st-frame title="{esc(topic.name)}" data-src="{esc(url)}" referrerpolicy=no-referrer>'
            '</iframe></details>')
