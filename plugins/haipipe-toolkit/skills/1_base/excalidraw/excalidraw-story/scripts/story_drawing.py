"""A paper's story as one drawing: its research questions as steps, each with what supports it and what is missing.

Asked 261019 on Physician-SPACE's Paper-LLMRecPhy-Quick (JL: "In the story studio s02-story, I think we might need to list
the research questions, and how could we support them"; "should we have a things named /excalidraw-story?"; "This
is more like the story, do you get it."). Drawn the way excalidraw-ideation draws s01 (one big main frame, small
frames that explain it, as stairs; JL 261013), and read from the telling's face on every build, so the drawing can
never say what the story does not.

    python story_drawing.py draw <studio/sNN-story-<desk>-<idea>>     redraw one (what the topic's builder calls)
    python story_drawing.py make <studio/sNN-story-<desk>-<idea>>     its forwarding builder

    ① 📖 the paper's question (main)                    ② the narrative, if the questions are answered
       the chain of question names                            ③ ✅ RQ1 · its card: why it matters, now,
        └─▶ ✅ RQ1 · name · its research question                  if answered, its E rows and T rows
             └─▶ 🔶 RQ2 · …                                       ④ 🔶 RQ2 · … one card each, as stairs
                  └─▶ ⬜ RQ3 · … (red, dashed: nothing supports it yet)
          ⑤ from here to the send (small, below): each Run to make, who starts it, then G0 · ⑥ what we will not claim

What it reads from the face (haipipe-paper-story's contract): the title line; `**The paper's question**:`; `**G0:**`;
`**The story, question by question**`, the questions in reading order; `**The narrative, if the questions are
answered**`, the chain of what the paper can say (JL 261019: "the quesiton can be the narrative as well"; "if these
questions or hypothese be answered, wht is the narrative behind we can have?");
§2's numbered Pitch; §3's `#### 3.N · Question N · RQn` blocks (Name, Research question, Why it matters, Answer state, If answered,
Hypotheses with their
E rows, Potential claims with Now, Potential work with their T and D rows); §5's E table (`support state`) and its
`**We will not claim**:` list; §7's T table (`state`, `starts`). A state is the first mark of its line: ✅ answered,
🔶 partly, ⬜ missing (red), ❗ contradicted (red). The writer is haipipe-studio's canvas.write, so a person's marks
survive a rebuild.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = next(p for p in HERE.parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-studio/scripts"))
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-ideation/scripts"))
from draw import GREY, INK, RED, Drawing, canvas  # noqa: E402
from ideation_drawing import box, finish, move  # noqa: E402   one look with s01: a box of lines, a small frame
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-job/scripts"))
from job_ladder import LANE_W, LANE_X, STAGGER, results_lanes, results_layout  # noqa: E402   one rule
#   with a Job's results: beside ①, top to bottom, inside its top and bottom or past both equally (JL 261014, 261019)

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
ROLES = ("core", "mechanism", "tension", "ethics", "framing", "governing", "answering", "set aside")   # theory rows
SHIFT, RQ_W, STEP_GAP = 160, 1300, 110
MAIN_K = 3.0                       # the main frame three times the size of the rest: the signboard (JL 261020)
CARD_W = canvas.FRAME_MAX[0]       # each frame of a question's row as wide as a frame may be (JL 261019: "as wide
CARD_T = CARD_W / 1500             #   as possible"), its words scaled to it; more words go in the next frame right
ROW_GAP = 220                      # between the panels of one question's frame
ROW_VGAP = 420                     # between the frames stacked on the right: room for Excalidraw's frame names,
                                   #   drawn at screen size above each frame (JL 261020: "这里都糊成一团了")
MARK = {"established": "✅", "provisional": "🔶", "absent": "⬜", "contradicted": "❗", "gated": "⬜",
        "done": "✅", "ticket next": "⬜", "not started": "⬜"}


# ── what the drawing reads ─────────────────────────────────────────────────────────────────────────────────
def mark(s: str) -> str:
    """The state mark a line starts with, else ''; an older face's 🔨 (in work) reads as 🔶."""
    m = re.match(r"\s*(✅|🔶|⬜|❗|🔨)", str(s))
    return ("🔶" if m.group(1) == "🔨" else m.group(1)) if m else ""


def missing(s: str) -> bool:
    return mark(s) in ("⬜", "❗")


def unmark(s: str) -> str:
    return re.sub(r"^\s*(✅|🔶|⬜|❗|🔨)\s*", "", str(s))


def table(lines: list[str], first: str) -> list[dict]:
    """The Markdown table whose header starts with `| first |`, one dict per row."""
    for i, ln in enumerate(lines):
        if ln.startswith(f"| {first} |"):
            head = [h.strip().lower() for h in ln.strip().strip("|").split("|")]
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(head, [c.strip() for c in row.strip().strip("|").split("|")])))
            return rows
    return []


def section(lines: list[str], head: str) -> list[str]:
    """The lines under a `### N · head` heading, to the next `### `."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("### "):
            on = re.sub(r"^###\s+\d+\s*·\s*", "", ln).strip().lower().startswith(head.lower())
            continue
        if on:
            out.append(ln)
    return out


def items(lines: list[str], start: str) -> list[str]:
    """The list under the first line starting with `start`: `- x` or `1. x`, wrapped lines joined."""
    out, on = [], not start                          # no start line: the list starts at once
    for ln in lines:
        if start and ln.startswith(start):
            on = True
            continue
        if not on:
            continue
        m = re.match(r"^(?:-|\d+\.)\s+(.*)$", ln)
        if m:
            out.append(m.group(1).strip())
        elif ln.startswith("  ") and out:
            out[-1] += " " + ln.strip()
        elif ln.strip() and out:
            break
        elif out:
            break
    return out


def plain(s: str) -> str:
    """Markdown marks off; a ⟦pending E4⟧ mark as (pending E4), which the drawing's font can show."""
    s = re.sub(r"⟦([^⟧]*)⟧", r"(\1)", s)
    return re.sub(r"\*\*(.+?)\*\*", r"\1", re.sub(r"`([^`]*)`", r"\1", s)).strip()


def joined(lines: list[str], start: str) -> str:
    """A bold-label paragraph that may wrap onto further lines: its words after the label, to the next blank line."""
    for i, ln in enumerate(lines):
        if ln.startswith(start):
            out = [ln[len(start):]]
            for nx in lines[i + 1:]:
                if not nx.strip() or nx.startswith(("#", "- ", "**", "|")) or re.match(r"^\d+\. ", nx):
                    break
                out.append(nx.strip())
            return plain(" ".join(out))
    return ""


def questions(lines: list[str]) -> list[dict]:
    """Every `#### 3.N · Question N · RQn` block: its fields, hypotheses, claims and work (a claim's `from` may name
    several hypotheses: `from 1a, 1b`)."""
    qs, cur, part = [], None, None
    for ln in lines:
        m = re.match(r"^#### 3\.\d+ · Question (\d+) · (RQ\d+)", ln)
        if m:
            cur = {"n": int(m[1]), "rq": m[2], "hyp": [], "claims": [], "work": []}
            qs.append(cur)
            part = None
            continue
        if ln.startswith(("### ", "#### ")):
            cur = None
            continue
        if cur is None:
            continue
        m = re.match(r"^- \*\*(Name|Research question|Question|Why it matters|Why the paper needs it|Answer state|"
                     r"If answered|Section)\*\*: (.*)$", ln)
        if m:                                          # an older block's "Why the paper needs it" is its why
            cur["why it matters" if m[1] == "Why the paper needs it" else m[1].lower()] = plain(m[2])
            continue
        m = re.match(r"^\*\*(Hypotheses|Potential claims|Potential contributions|Potential work)\*\*$", ln.strip())
        if m:
            part = m[1]
            continue
        if part == "Hypotheses":
            m = re.match(r"^- \*\*(\w+)\*\* · (.+?) · tested by (.+)$", ln)
            if m:
                name, _, what = m[2].partition(": ")
                cur["hyp"].append({"code": m[1], "name": name, "what": what, "tested": re.findall(r"E(?:work|cite)?\d+", m[3])})
        elif part == "Potential claims":
            m = re.match(r"^- \*\*(\w+)\*\* · (C\d+) · from [^·]+? · (.+)$", ln)
            if m:
                name, _, what = m[3].partition(": ")
                cur["claims"].append({"code": m[1], "c": m[2], "name": name, "what": what})
            m = re.match(r"^\s+- \*\*(Role|Now|If it fails)\*\*: (.*)$", ln)
            if m and cur["claims"]:
                cur["claims"][-1][m[1].lower()] = plain(m[2])
        elif part == "Potential work":
            m = re.match(r"^- \*\*([TD]\d+)\*\* · for ([^·]+?)(?: · (.+))?$", ln)
            if m:
                cur["work"].append(m[1])
    return sorted(qs, key=lambda q: q["n"])


def board_of(topic: Path) -> Path | None:
    for p in (topic, *topic.parents):
        if (p / "board.md").is_file():
            return p
    return None


def report_questions(topic: Path) -> list[dict]:
    """The question blocks a Board keeps in its Questions' reports (board.md `## Questions`, each `report:`), as
    haipipe-paper-story allows; what excalidraw-workflow reads too."""
    board = board_of(topic)
    if not board:
        return []
    m = re.search(r"## Questions\s*\n+```yaml\n(.*?)\n```", (board / "board.md").read_text(encoding="utf-8"), re.S)
    if not m:
        return []
    import yaml
    qs = []
    for q in (yaml.safe_load(m[1]) or {}).get("questions", []) or []:
        rp = board / str(q.get("report", ""))
        if q.get("report") and rp.is_file():
            qs += questions(rp.read_text(encoding="utf-8").splitlines())
    return sorted(qs, key=lambda q: q["n"])


def table_questions(lines: list[str]) -> list[dict]:
    """An older face's §3 table, one row a question: `| RQ | question | why the paper needs it | answer form | … |
    answer state |`; its Task and Discovery cells name its work, its claim cell its E rows."""
    qs = []
    for r in table(lines, "RQ"):
        n = re.search(r"\d+", r.get("rq", ""))
        if not n:
            continue
        cells = " ".join(r.get(k, "") for k in ("task", "discovery"))
        tested = re.findall(r"E(?:work|cite)?\d+", " ".join(r.get(k, "") for k in r if "claim" in k or "evidence" in k))
        qs.append({"n": int(n.group()), "rq": r["rq"], "name": r.get("name", ""), "hyp": [{"tested": tested}] if tested else [],
                   "claims": [], "work": re.findall(r"\b[TD]\d+\b", cells),
                   "research question": plain(r.get("question", "")),
                   "why it matters": plain(r.get("why it matters") or r.get("why the paper needs it", "")),
                   "answer state": plain(r.get("answer state", "")),
                   "section": plain(next((r[k] for k in r if "section" in k), ""))})
    return qs


GENERIC = ("one prospective paper", "the current telling", "the story")


def read(topic: Path) -> dict:
    face = topic / f"{topic.name}.md"
    if not face.is_file():
        raise SystemExit(f"{face}: no face")
    lines = face.read_text(encoding="utf-8").splitlines()
    qs = questions(lines) or report_questions(topic) or table_questions(lines)     # the face, its Board's reports,
    if not qs:                                                                      #   or an older §3 table
        raise SystemExit(f"{face.name}: no '#### 3.N · Question N · RQn' block, in the face or its Board's reports, "
                         "and no '| RQ |' table (haipipe-paper-story §3)")
    title = re.sub(r"^#\s*", "", lines[0]).strip()                 # "# s02-story-… · The Story: …", "s02 · Story: …"
    title = re.sub(rf"^({re.escape(topic.name)}|s\d+)\s*·\s*", "", title)
    title = re.sub(r"^(The\s+)?(Story|current telling)(:\s*|$)", "", title, flags=re.I).strip()
    board = board_of(topic)
    if not title or title.lower() in GENERIC:
        title = board.name if board else topic.name
    one = lambda key: next((plain(ln.split(":**", 1)[1]) for ln in lines if ln.startswith(f"**{key}:**")), "")
    spine = ""
    if board:
        sm = re.search(r"(?m)^spine:\s*(.+)$", (board / "board.md").read_text(encoding="utf-8"))
        spine = plain(sm[1]) if sm else ""
    asked = re.search(r"(?:^|[:;.]\s*)([^:;.?]+\?)", spine)      # the spine's question, when it asks one
    asked = asked[1].strip() if asked else ""
    asks = [(x.get("research question") or x.get("question", "")).split(" (RQ")[0] for x in qs]
    first = next((t for t in asks if t.rstrip().endswith("?")), "")    # the first that is a question
    ident = next((plain(lines[i + 1]) for i, ln in enumerate(lines)     # else the face's one-sentence identity
                  if re.match(r"^#+\s.*one-sentence identity", ln, re.I) and i + 1 < len(lines)), "") or \
        joined(lines, "**One sentence**:")
    q = joined(lines, "**The paper's question**:") or (asked[:1].upper() + asked[1:]) or first or ident or asks[0]
    if len(q.split()) > 40:                                        # a long identity sentence: its first words
        q = " ".join(q.split()[:40]) + " …"
    told = [plain(x) for x in items(lines, "**The story, question by question**")]
    if len(told) == len(qs):                          # the questions as the narrative: each step titled by its own
        for rq, s in zip(qs, told):
            rq["told"] = s[:s.index("?") + 1] if "?" in s else rq.get("name", "")
    E = {r["e"]: r for r in table(lines, "E")}
    T = {r["t"]: r for r in table(lines, "T")}
    V = [r for r in table(lines, "V")]                          # §9, the venues, from the target to the fallbacks
    blocks, cur = [], None                                      # §9's `#### V1 · …` blocks: the target in detail
    for ln in section(lines, "Venues"):                         #   (JL 261019), then how the paper meets it and why
        m = re.match(r"^####\s+V1\s*·\s*(.+)$", ln)            #   it is doable, each a frame (JL 261020)
        if m:
            cur = {"title": plain(m[1]), "lines": []}
            blocks.append(cur)
            continue
        if ln.startswith("#### "):
            cur = None
        elif cur is not None:
            cur["lines"].append(ln)
    vblocks = [{"title": b["title"], "items": [plain(x) for x in items(b["lines"], "")]} for b in blocks]
    theory = table(section(lines, "Stakes"), "theory")             # §4's theories, each with its role and questions,
    derived = table(section(lines, "Research Questions"), "theory")   # §3's hypothesis development: each its codes
    for r in theory:                                               #   (JL 261020: "for the s02, of the MISQ, where is
        name = r.get("theory", "").lower()                         #   the theory? ????")
        codes = []
        for dr in derived:
            parts = [p.strip() for p in re.split(r",| or ", dr.get("theory", "").lower()) if p.strip()]
            if any(p in name for p in parts) or name in dr.get("theory", "").lower():
                codes += re.findall(r"\b\d[a-z]\b", dr.get("hypotheses", ""))
        r["codes"] = list(dict.fromkeys(codes))
    said = joined(lines, "- **Theory**")
    said = re.sub(r"\s*\([^()]*\)", "", said)                      # its one-line claim, without the asides
    claim = (re.search(r"Said for a reviewer in one line:\s*([^;.]+)", said)      # the reviewer's line first
             or re.search(r"The contribution:\s*([^;.]+)", said))
    return {"title": title[:1].upper() + title[1:], "question": q or title, "g0": one("G0"), "qs": qs, "E": E,
            "theory": theory, "theory_claim": claim[1].strip() if claim else "",
            "T": T, "V": V, "vdetail": vblocks[0] if vblocks else None, "vmore": vblocks[1:],
            "pitch": [plain(x) for x in items(section(lines, "Pitch"), "")],
            "refuse": [plain(x) for x in items(lines, "**We will not claim**")],
            "narrative": [plain(x) for x in items(lines, "**The narrative, if the questions are answered**")]}


def e_mark(r: dict) -> str:
    s = (r.get("support state") or "").lower()
    return next((v for k, v in MARK.items() if k in s), "⬜")


def t_mark(r: dict) -> str:
    if "state" not in r:                              # an older §7 table says no state: no mark, never a guess
        return ""
    s = (r.get("state") or "").strip().lower()
    return "✅" if s.startswith("done") else "🔶" if s.startswith(("partly", "partial", "running")) else "⬜"


# ── ① the main frame: the questions as steps ──────────────────────────────────────────────────────────────
def main_frame(d: Drawing, S: dict) -> tuple[dict, dict, dict]:
    """The signboard: the paper's question and its research questions as steps, drawn MAIN_K times the size of every
    other frame, so the main frame reads first and the rest explain it (JL 261020: "你可以把它变得很大 ... 就跟我们招牌
    一样 ... 它是主，其他都是次，我们要做到主次分明")."""
    K = MAIN_K
    qs = S["qs"]
    sh, rw, gap, m = round(SHIFT * K), round(RQ_W * K), round(STEP_GAP * K), round(40 * K)
    # with §4's theories, each step reads on to its right, as one table: its theories, hypotheses and claims (JL
    # 261020: "每个 C 内部的东西，比如像这个 … how it fits together，其实可以放到这个大里面去 ... 让它变得越大越好")
    fit = {q["rq"]: [theories_of(S, q["rq"]) or ["none named"],
                     [f"{held(S, h)} {h['code']} {h['name']}" for h in q["hyp"] if h.get("name")] or ["none"],
                     [f"{mark(c.get('now', '')) or '⬜'} {c['c']} {c['name']}" for c in q["claims"]] or ["none"]]
           for q in qs} if S.get("theory") else {}
    tw, tg = [round(w * K) for w in (560, 820, 640)], round(50 * K)
    tx0 = round(140 * K) + (len(qs) - 1) * sh + rw + round(100 * K)          # right of the farthest step
    tend = tx0 + sum(tw) + 2 * tg
    width = (tend + m) if fit else round(140 * K) + (len(qs) - 1) * sh + rw + round(80 * K)
    heading = f"📖 {S['title']}"
    f = d.frame(f"① {heading}", width)
    Drawing.room(f)
    canvas.signboard(f, K)
    hb = d.para(m, round(22 * K), heading, width - m - 700, round(44 * K))   # short of the size badge, top right
    done = sum(1 for q in qs if mark(q.get("answer state", "")) == "✅")
    part = sum(1 for q in qs if mark(q.get("answer state", "")) == "🔶")
    sub = f"{done} answered · {part} partly · {len(qs) - done - part} not yet, in red"
    sy = hb + round(20 * K)
    y = d.para(m, sy, sub, width - 2 * m, round(26 * K), GREY) + round(52 * K)
    keyed = bool(S["narrative"]) or so_far(S) == S["question"]   # the question is the key point: no second one
    if not keyed:                       # with a narrative, the answer so far heads it, and this frame keeps the
        key = so_far(S)                 # long research questions (JL 261019: "相对比较长 ... 比较易懂的")
        kh = Drawing.height(key, width - 2 * m - 60, round(32 * K)) + round(44 * K)
        d.key(m, y, width - 2 * m, kh)
        d.para(m + 30, y + round(22 * K), key, width - 2 * m - 60, round(32 * K))
        y += kh + round(70 * K)
    qw = min(round(1500 * K), width - 2 * m)
    if keyed:                                                      # the paper's question is the key point
        qh = Drawing.height(S["question"], qw - 60, round(44 * K)) + round(44 * K)
        d.key(m, y, qw, qh)
        d.para(m + 30, y + round(22 * K), S["question"], qw - 60, round(44 * K))
    else:
        qh = box(d, m, y, qw, [(S["question"], round(44 * K), INK)], sw=4)
    root = {"right": m + qw, "mid": y + qh / 2}
    spine_x, spine_top = round(70 * K), y + qh
    y += qh + gap
    mids, ends = [], {}
    texts = [(q.get("research question") or q.get("told") or q.get("question", "")).split(" (RQ")[0] for q in qs]
    total, asked = sum(len(t.split()) for t in texts), len(S["question"].split())
    fitwords = sum(len(it.split()) for cols in fit.values() for col in cols for it in col)
    room = round(150 * K) - min(asked, 40) - fitwords              # a signboard holds MAP_WORDS × K words (⑦):
    per = max(10, room // len(qs)) if total > room else 10 ** 6   #   the question, the table, then each step's share
    if fit:                                                        # the table's column names over the first step
        for cx, c in zip((tx0, tx0 + tw[0] + tg, tx0 + tw[0] + tw[1] + 2 * tg), ("Theories", "Hypotheses", "Claims")):
            d.para(cx, y - round(80 * K), c, 900, round(28 * K), GREY)
    for i, q in enumerate(qs):
        x = round(140 * K) + i * sh
        st = mark(q.get("answer state", "")) or "⬜"
        hole = missing(q.get("answer state", "⬜"))
        formal = q.get("research question") or q.get("told") or q.get("question", "")
        formal = formal.split(" (RQ")[0]                          # the sub-questions stay in the card
        words = formal.split()
        if len(words) > per:                                       # many long questions: each keeps its first words,
            formal = " ".join(words[:per]) + " …"                 #   the card keeps the whole question
        named = f"{q['rq']} · {q['name']}" if q.get("name") else q["rq"]
        h = box(d, x, y, rw, [(f"{st} {named}", round(34 * K), RED if hole else INK),
                              (formal, round(28 * K), INK)], sw=4, dashed=hole)
        mid = y + round(40 * K)
        row = h
        if fit:                                                    # the step read on: theories, hypotheses, claims
            d.line([(tx0, y - round(20 * K)), (tend, y - round(20 * K))], GREY, arrow=False)
            d.line([(x + rw + 10, mid), (tx0 - 20, mid)], GREY, arrow=False, dashed=True)
            cx = tx0
            for col, w in zip(fit[q["rq"]], tw):
                yy = y
                for it in col:
                    yy = d.para(cx, yy, it, w - 30, round(24 * K)) + round(4 * K)
                row, cx = max(row, yy - y), cx + w + tg
        mids.append(mid)
        ends[q["rq"]] = {"right": tend if fit else x + rw, "mid": mid}
        d.line([(spine_x, mid), (x - 8, mid)], sw=4)
        y += row + gap
    d.line([(spine_x, spine_top), (spine_x, mids[-1])], arrow=False, sw=4)
    return finish(d, f, y - gap + m, small=False), root, ends


def held(S: dict, h: dict) -> str:
    """A hypothesis's mark from the evidence rows that test it: ✅ all in hand, 🔶 some, ⬜ none yet."""
    marks = [e_mark(S["E"].get(e, {})) for e in h.get("tested", [])]
    return "✅" if marks and all(m == "✅" for m in marks) else "🔶" if any(m in "✅🔶" for m in marks) else "⬜"


def circ(n: int) -> str:
    return CIRCLED[n] if n < len(CIRCLED) else f"({n + 1})"


def role_of(r: dict) -> str:
    """A §4 theory row's role, one of ROLES, or '' when its role cell names none."""
    return next((k for k in ROLES if k in (r.get("role") or "").lower()), "")


def theories_of(S: dict, rq: str) -> list[str]:
    """The theories §4's table says serve a question, those set aside left out."""
    return [r.get("theory", "") for r in S.get("theory", [])
            if role_of(r) != "set aside" and re.search(rf"\b{rq}\b", r.get("questions", ""))]


def keyed(d: Drawing, y: float, W: int, text: str, size: int, x0: int = 0) -> float:
    """A key box across the frame (or across a panel at x0) holding one paragraph; the y under it."""
    kh = Drawing.height(text, W - 140, size) + 36
    d.key(x0 + 40, y, W - 80, kh)
    return d.para(x0 + 70, y + 18, text, W - 140, size) + 18 + 28


# A question is one wide frame, read left to right in three panels (JL 261020: "these are too words, you can add the
# new frames to the rigth of them"; then "for each RQ here, could we just have one frame, one very wide frame for each
# RQ?"): its card, then what we expect and why (the hypotheses, each with its theory), then what the paper can say
# (the claims). Each panel is a frame's width, its words scaled to it; the frame is marked canvas.columns, so ⑨ judges
# a wall of text per panel.
def card_panel(d: Drawing, q: dict, S: dict, x0: int, W: int = CARD_W) -> float:
    """The question's card: its sub-questions, why it matters, the answer now, the theories behind it and its Runs."""
    k = CARD_T
    st = mark(q.get("answer state", "")) or "⬜"
    hole = missing(q.get("answer state", "⬜"))
    title = f"{st} {q['rq']} · {q['name']}" if q.get("name") else f"{st} {q['rq']}"
    y = d.para(x0 + 40, 22, title, W - 80, round(40 * k), RED if hole else INK) + 16
    subs = re.search(r"\((RQ\d+a\b.*)\)\s*$", q.get("research question", ""))       # "RQ1a selection: …" or "RQ1a: …"
    if subs:
        y = d.para(x0 + 40, y, subs.group(1), W - 80, round(22 * k), GREY) + 18
    y = keyed(d, y, W, f"Why it matters: {q.get('why it matters', '❓ the face gives no reason')}", round(26 * k), x0)
    now = unmark(q.get("answer state", "⬜ no answer state in the face"))
    y = d.para(x0 + 40, y, "Now", W - 80, round(28 * k), RED if hole else INK) + 6
    for part in re.split(r"(?<=[.;])\s+(?=[A-Z0-9])", now):         # the answer now, a line a finding
        y = d.para(x0 + 70, y, f"· {part}", W - 110, round(23 * k), RED if hole else INK) + 8
    y += 10
    th = theories_of(S, q["rq"])
    if th:
        y = d.para(x0 + 40, y, "Theory  " + " · ".join(th), W - 80, round(22 * k), GREY) + 8
    runs = [t for t in q["work"] if t.startswith("T")]
    if runs:
        y = d.para(x0 + 40, y, "Work  " + " · ".join(f"{t_mark(S['T'].get(t, {}))} {t}" for t in runs), W - 80,
                   round(22 * k), GREY)
    return y


def hyp_panel(d: Drawing, q: dict, S: dict, x0: int, W: int = CARD_W) -> float:
    """What we expect, and why: each hypothesis, the theory it comes from (the closing bracket of its sentence in the
    face) and the evidence rows that test it, marked."""
    k = CARD_T
    y = d.para(x0 + 40, 22, "What we expect, and why", W - 80, round(34 * k)) + 16
    hyps = [h for h in q["hyp"] if h.get("name")]
    inhand = sum(1 for h in hyps if held(S, h) != "⬜")
    theories = theories_of(S, q["rq"])
    y = keyed(d, y, W, f"{len(hyps)} hypotheses" + (f" from {len(theories)} theories" if theories else "") +
              f": {inhand} with evidence in hand, {len(hyps) - inhand} waiting for a Run.", round(26 * k), x0)
    for h in q["hyp"]:
        what = h.get("what", "")
        m = re.search(r"\s*\(([^()]*)\)\s*$", what)
        why = m[1] if m and re.search(r"[a-z]{4}", m[1]) else ""      # "(3g)" alone names a code, not a theory
        what = what[:m.start()].rstrip() if why else what
        tested = " · ".join(f"{e_mark(S['E'].get(e, {}))} {e}" for e in h["tested"])
        low = " · ".join(x for x in (f"theory: {why}" if why else "", f"tested by {tested}" if tested else "") if x)
        mk = held(S, h) if h.get("name") else ""
        rows = [(f"{mk} {h.get('code', '')} · {h.get('name', '')}".strip(), round(30 * k), INK),
                (what, round(22 * k), INK)]
        rows += [(low, round(19 * k), GREY)] if low else []
        y += box(d, x0 + 40, y, W - 80, rows, sw=2 if mk != "⬜" else 1.5, dashed=mk == "⬜") + 24
    return y


def say_panel(d: Drawing, q: dict, S: dict, x0: int, W: int = CARD_W) -> float:
    """What the paper can say: if the question is answered as expected, then each claim, where it stands, and what the
    paper becomes if it fails."""
    k = CARD_T
    y = d.para(x0 + 40, 22, "What the paper can say", W - 80, round(34 * k)) + 16
    if q.get("if answered"):
        y = keyed(d, y, W, f"If answered: {q['if answered']}", round(24 * k), x0)
    for c in q["claims"]:
        hole = missing(c.get("now", ""))
        rows = [(f"{c['c']} · {c['name']}", round(30 * k), INK), (c.get("what", ""), round(22 * k), INK)]
        rows += [(f"Now: {unmark(c['now'])}", round(20 * k), RED if hole else GREY)] if c.get("now") else []
        rows += [(f"If it fails: {c['if it fails']}", round(19 * k), GREY)] if c.get("if it fails") else []
        y += box(d, x0 + 40, y, W - 80, rows, sw=2 if not hole else 1.5, dashed=hole) + 24
    return y


def question_frame(d: Drawing, n: int, q: dict, S: dict, W: int = CARD_W) -> dict:
    """One question as one wide frame: the card, then the hypotheses and the claims when the face gives them, each a
    panel W wide, an arrow from each panel to the next."""
    st = mark(q.get("answer state", "")) or "⬜"
    title = f"{st} {q['rq']} · {q['name']}" if q.get("name") else f"{st} {q['rq']}"
    panels = [card_panel]
    panels += [hyp_panel] if any(h.get("name") for h in q["hyp"]) else []
    panels += [say_panel] if q["claims"] or q.get("if answered") else []
    f = d.frame(f"{circ(n)} {title}", len(panels) * W + (len(panels) - 1) * ROW_GAP)
    if len(panels) > 1:
        canvas.large(f)                                            # wider than a screen on purpose: zoom to read
        canvas.columns(f, len(panels))
    bottom = 0
    for i, draw_panel in enumerate(panels):
        x0 = i * (W + ROW_GAP)
        bottom = max(bottom, draw_panel(d, q, S, x0, W))
        if i:
            d.line([(x0 - ROW_GAP + 20, 90), (x0 - 20, 90)], sw=3)
    return finish(d, f, bottom)


# ── ② the pitch, ③ what we will not claim, ④ from here to the send ────────────────────────────────────────
def so_far(S: dict) -> str:
    """§2 Pitch's "The answer so far" item, the key of the story."""
    return next((p for p in S["pitch"] if p.lower().startswith("the answer so far")),
                S["pitch"][2] if len(S["pitch"]) > 2 else S["question"])


def list_frame(d: Drawing, n: int, title: str, lines: list[str], numbered: bool = False, key: str = "",
               W: int = 1500) -> dict:
    f = d.frame(f"{circ(n)} {title}", W)
    if W > canvas.FRAME_MAX[0]:
        canvas.large(f)
    k = min(W, CARD_W) / 1500                                      # beside the cards, the narrative reads at their size
    d.text(40, 22, title, round(44 * k))
    y = round(110 * k)
    if key:                                                        # what is answered now, over what could be said
        kh = Drawing.height(key, W - 140, round(28 * k)) + 40
        d.key(40, y, W - 80, kh)
        d.para(70, y + 20, key, W - 140, round(28 * k))
        y += kh + 40
    for i, s in enumerate(lines, 1):
        y = d.para(40, y, (f"{i}. " if numbered else "· ") + s, W - 80, round(26 * k), RED if missing(s) else INK) + 14
    return finish(d, f, y)


def path_frame(d: Drawing, n: int, S: dict, max_w: int = 2400) -> dict:
    """Each Run still to make, as stairs: what it is, where, and who starts it; then G0 when it is not marked."""
    todo = [(t, r) for t, r in S["T"].items() if "state" in r and t_mark(r) != "✅"]
    steps = [(f"{t} · {r.get('work') or r.get('name', '')}",          # the short table, or §7's full one
              f"{r.get('starts', '')} · {r.get('where') or r.get('feeds', '')}",
              bool(re.search(r"\bstarts\b", r.get("starts", "").lower()))) for t, r in todo]
    if S["g0"] and mark(S["g0"]) != "✅":
        steps.append(("⬜ G0", "a person's mark on the story", False))
    BW, DY = 250, 70                                               # each step lower and further right, no overlap
    X = max(BW + 20, min(330, (max_w - 80 - BW) // max(1, len(steps) - 1)))   # as wide as the main frame
    W = max(1600, 80 + (len(steps) - 1) * X + BW)
    title = "From here to the send"
    f = d.frame(f"{circ(n)} {title}", W)
    d.text(40, 22, title, 44)
    key = (f"{len(todo)} Run{'' if len(todo) == 1 else 's'} to make, then G0. " if todo else "Every Run is made. ") + \
          "A Run that costs new model calls waits for a person to start it (red)."
    kh = Drawing.height(key, W - 140, 30) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 30)
    y = 100 + kh + 50
    prev, bottom = None, y
    for i, (top, low, new_calls) in enumerate(steps):            # new_calls: its `starts` says "<person> starts"
        x, yy = 40 + i * X, y + i * DY
        h = box(d, x, yy, BW, [(top, 24, RED if new_calls else INK), (low, 20, GREY)],
                sw=2.5 if i == len(steps) - 1 else 1.5, dashed=new_calls)
        if prev:
            d.line([(prev[0] + BW + 6, prev[1] + 30), (x - 6, yy + 30)], sw=2)
        prev, bottom = (x, yy), max(bottom, yy + h)
    return finish(d, f, bottom)


def theory_frame(d: Drawing, n: int, S: dict, W: int = CARD_W) -> dict:
    """§4's theories as stairs, by role: the core lens first, then the mechanisms, the tension, the ethics, the
    framing, the lenses for governing and answering, and those set aside (grey, dashed); each its idea in one line,
    the questions it serves and the hypotheses it gives (§3's hypothesis development)."""
    k = CARD_T                                                     # read at the size of the question rows
    title = "Why the questions hang together: the theory"
    f = d.frame(f"{circ(n)} {title}", W)
    y = d.para(40, 22, title, W - 80, round(40 * k)) + 16
    if S.get("theory_claim"):
        y = keyed(d, y, W, f"The claim: {S['theory_claim']}", round(26 * k)) + 12
    rows = sorted(S["theory"], key=lambda r: ROLES.index(role_of(r)) if role_of(r) else 4)
    SH = 24                                                        # each a step right
    for i, r in enumerate(rows):
        role = role_of(r) or "theory"
        aside = role == "set aside"
        top = f"{role} · {r.get('theory', '')}: {r.get('the idea in one line', '')}"
        if aside:
            low = r.get("role", "")
        else:
            low = " · ".join(x for x in (f"for {r.get('questions', '')}",
                                         f"hypotheses {', '.join(r['codes'])}" if r.get("codes") else "") if x)
        h = box(d, 40 + i * SH, y, W - 80 - SH * (len(rows) - 1),
                [(top, round(24 * k), GREY if aside else INK), (low, round(20 * k), GREY)],
                sw=2.5 if role == "core" else 1.2, dashed=aside)
        y += h + 12
    return finish(d, f, y)


def venue_frame(d: Drawing, n: int, S: dict) -> dict:
    """§9's venues as stairs, from the target down to the fallbacks: each its kind, the questions it would lead with,
    and what it still needs; a venue with no haipipe-paper-venue desk record is red and dashed."""
    W, BW, SH = 1960, 1320, 64
    title = "Where the story could go"
    f = d.frame(f"{circ(n)} {title}", W)
    d.text(40, 22, title, 44)
    key = "From the target down to the fallbacks. A venue changes which questions lead, not the questions."
    kh = Drawing.height(key, W - 140, 28) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 28)
    y = 100 + kh + 40
    for i, r in enumerate(S["V"]):
        none = (r.get("desk record") or "").strip().lower() in ("", "none", "none yet")
        top = f"{r.get('v', '')} · {r.get('venue', '')} · {r.get('kind', '')}"
        low = f"leads with {r.get('leads with', '')} · still needs: {r.get('still needs', '')}"
        h = box(d, 40 + i * SH, y, BW, [(top, 24, RED if none else INK), (low, 20, GREY)],
                sw=2.5 if i == 0 else 1.2, dashed=none)
        y += h + 14
    vd = S.get("vdetail")
    if vd:                                                      # the target in detail, under the list (JL 261019)
        y += 26
        rows = [(f"{S['V'][0].get('v', 'V1') if S['V'] else 'V1'} in detail · {vd['title']}", 26, INK)]
        rows += [(f"· {x}", 20, INK) for x in vd["items"]]
        y += box(d, 40, y, W - 80, rows, sw=2.5) + 14
    return finish(d, f, y)


def draw(topic: Path, out: Path | None = None) -> Path:
    topic = Path(topic).resolve()
    S = read(topic)
    d = Drawing()
    big, root, ends = main_frame(d, S)
    story = S["narrative"] or S["pitch"]
    head = "The narrative, if the questions are answered" if S["narrative"] else "The pitch"
    key = so_far(S) if S["narrative"] else ""

    told = list_frame(d, 1, head, story, numbered=True, key=key, W=CARD_W) if story else None
    n, rows = 2, []                                                # one wide frame per question
    for q in S["qs"]:
        rows.append([question_frame(d, n, q, S)])
        n += 1
    cards = [r[0] for r in rows]
    refuse = list_frame(d, n, "What we will not claim", S["refuse"]) if S["refuse"] else None
    n += 1 if refuse else 0
    theory = theory_frame(d, n, S) if S["theory"] else None
    n += 1 if theory else 0
    stated = any("state" in r for r in S["T"].values())             # an older §7 table says no state: no path
    # once the paper has a plan (haipipe-paper-plan's s03, s04), the Runs to make and the dates are its, not the
    # story's (JL 261020: "is this more like the plan? right? Maybe we can drop it")
    plan = sorted(p.name for p in topic.parent.glob("s0[34]-paper-*") if p.is_dir())
    path = path_frame(d, n, S, big["width"]) if stated and not plan else None   # under the main frame, no wider
    n += 1 if path else 0
    venues = venue_frame(d, n, S) if S["V"] else None
    n += 1 if venues else 0
    vmore = []                                                     # the target's further blocks, right of the venues
    for b in (S.get("vmore") or []) if venues else []:
        vmore.append(list_frame(d, n, f"V1 · {b['title']}", b["items"], W=CARD_W))
        n += 1
    # the left column, as stairs: the main frame at the origin, then below it what is missing, the theory, what we
    # will not claim, the venues, each a step lower and further right
    move(d.els, big, 0, 0)
    y, step = big["height"] + 320, 0
    for fr in (path, theory, refuse, venues):
        if fr:
            move(d.els, fr, 40 + 260 * step, y)
            y, step = fr["y"] + fr["height"] + 200, step + 1
    for prev, f in zip([venues] + vmore, vmore):
        move(d.els, f, prev["x"] + prev["width"] + ROW_GAP, prev["y"])
    # beside the main frame, top to bottom as a Job's results: each row as near its step as it can, inside ①'s top
    # and bottom, or one run centred on ① that rises above it as far as it hangs below (JL 261014; 261019: "也是上下排，
    # 但是你可以宽一些 … 就跟我们那 job"); every other one a step right (错位); a row's frames side by side
    H = big["height"]
    blocks = ([told] if told else []) + cards
    anchors = ([root] if told else []) + [ends[q["rq"]] for q in S["qs"]]
    hs = ([told["height"]] if told else []) + [max(f["height"] for f in r) for r in rows]
    tops = results_layout([a["mid"] - 40 for a in anchors], hs, 0, H, ROW_VGAP)
    links = [(a["mid"], a["mid"] if y + 40 <= a["mid"] <= y + h - 40 else y + 40)
             for a, y, h in zip(anchors, tops, hs)]
    lanes = results_lanes(links)
    low_end = max(y + h for y, h in zip(tops, hs))                 # clear only the frames below ① the rows reach
    left = max([big["width"]] + [f["x"] + f["width"] for f in (path, theory, refuse, venues, *vmore)
                                 if f and f["y"] < low_end + 200])
    base = left if low_end > H + 280 else big["width"]
    x0 = base + LANE_X + LANE_W * len(lanes) + 120
    for k, (f, y) in enumerate(zip(blocks, tops)):
        move(d.els, f, x0 + (STAGGER if k % 2 else 0), y)
    for r in rows:                                                 # the rest of a row to the right of its card
        for prev, f in zip(r, r[1:]):
            move(d.els, f, prev["x"] + prev["width"] + ROW_GAP, prev["y"])
    d.fid = None
    for r in rows + ([[venues] + vmore] if vmore else []):
        for prev, f in zip(r, r[1:]):
            d.line([(prev["x"] + prev["width"] + 14, prev["y"] + 90), (f["x"] - 14, f["y"] + 90)], sw=3)
    acts = [(big, "The questions, in reading order")]               # the rows named at the left (excalidraw-studio ③)
    acts += [((told or cards[0]), "What each question needs, what we expect and why, what the paper can say")] \
        if cards else []
    acts += [(path, "What is missing")] if path else []
    acts += [(theory, "Why the questions hang together")] if theory else []
    acts += [(venues, "Where it could go")] if venues else []
    acts = [(f, f"Act {i} · {name}") for i, (f, name) in enumerate(acts, 1)]
    if plan:                                                        # one line where the path was: where it went
        g0 = f" · G0 {mark(S['g0'])}" if S["g0"] else ""
        d.para(40, big["height"] + 60, f"The Runs to make and the dates to the send: {', '.join(plan)}{g0}",
               big["width"] - 80, 44)
    for f, name in acts:
        if any(f is g for g in (big, path, theory, venues)):
            d.para(f["x"] - 820, f["y"] + 20, name, 760, 44)
        else:
            d.text(f["x"], f["y"] - 300, name, 64)                  # well above the frame's own name
    for k, (f, a, (m, hit)) in enumerate(zip(blocks, anchors, links)):   # each step to its card, straight when
        if k in lanes:                                                   #   level, else along its own lane, so no
            lx = base + LANE_X + LANE_W * lanes[k]                       #   two lines cross
            pts = [(a["right"] + 10, m), (lx, m), (lx, hit), (f["x"] - 14, hit)]
        else:
            pts = [(a["right"] + 10, m), (f["x"] - 14, m)]
        d.line(pts, sw=3 if f is told else 1.5)
    if told:
        d.text(root["right"] + 30, root["mid"] - 80, "if answered", 56)
    if path:
        px = path["x"] + 300
        d.line([(px, big["height"] + 14), (px, path["y"] - 14)], sw=5)
        d.text(px + 20, big["height"] + 130, "what is missing", 36)
    builder = next(iter(sorted(topic.glob("build_*.py"))), None)
    out = out or topic / f"{topic.name}.excalidraw"
    d.write(out, builder.name if builder else Path(__file__).name)
    sys.path.insert(0, str(SKILLS / "1_base/project/haipipe-studio/scripts"))
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


# ── a topic's builder ──────────────────────────────────────────────────────────────────────────────────────
def scripts_from(topic: Path) -> str:
    """This folder, relative to the topic: through the SPACE's Tools link, or inside the Tools SPACE itself."""
    here_rel = HERE.relative_to(SKILLS.parents[2])
    for p in (topic, *topic.parents):
        for base in (p / "Tools", p):
            if (base / here_rel).is_dir():
                return Path(os.path.relpath(base / here_rel, topic)).as_posix()
    return str(HERE)


def make(topic: Path, force: bool = False) -> Path:
    topic = Path(topic).resolve()
    if not topic.is_dir():
        raise SystemExit(f"{topic} is not a folder; make the topic first (haipipe-paper-story)")
    m = re.match(r"s(\d\d)-(.+)$", topic.name)
    builder = topic / (f"build_s{m.group(1)}_{m.group(2).replace('-', '_')}.py" if m else "build.py")
    if builder.exists() and not force:
        raise SystemExit(f"{builder.name} exists; --force replaces it (keep a copy first if it holds drawing code)")
    builder.write_text(
        f'"""{topic.name}: drawn by excalidraw-story\'s story_drawing.py from this face (its research questions, '
        "their E and T rows, the pitch and what we will not claim); a person's marks on the drawing are kept.\n\n"
        f'    python {builder.name}\n"""\n'
        "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
        f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
        "import story_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    print(story_drawing.draw(HERE))\n",
        encoding="utf-8")
    return builder


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one story topic").add_argument("topic", type=Path)
    m = sub.add_parser("make", help="the topic's forwarding builder")
    m.add_argument("topic", type=Path)
    m.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    print(draw(a.topic) if a.cmd == "draw" else make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
