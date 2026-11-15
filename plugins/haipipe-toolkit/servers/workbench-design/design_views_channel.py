"""A design as its reader sees it: a phone for an SMS, tick boxes for a checklist, answer boxes for a
questionnaire, a UI design's screen (split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_reader as R
from live.frame import esc, rel


def phone(message: str, small: bool = False, label: str = "Text message") -> str:
    """An SMS (or a push, a reminder) as the reader sees it: one bubble on a phone, the {LINK} where the platform puts it."""
    body = esc(message or "—").replace("{LINK}", '<span style="color:var(--acc);text-decoration:underline">{LINK}</span>')
    w, f = ("190px", "12.5px") if small else ("280px", "14.5px")
    return (f'<div style="border:1px solid var(--line);border-radius:18px;padding:10px 10px 14px;margin:4px 0;'
            f'max-width:{w};background:var(--bg)"><div class=mut style="text-align:center;font-size:11px;margin-bottom:8px">'
            f'{esc(label)}</div><div style="background:var(--acc-soft);border-radius:16px 16px 16px 4px;padding:7px 10px;'
            f'font-size:{f};white-space:pre-wrap;word-break:break-word">{body}</div></div>')


# a design is drawn in its channel (a questionnaire drawn as a text message reads as the wrong thing):
# the goal's venue picks the look (venue/venue-<name>/README.md); no venue is an SMS (the older Blocks)
PHONE_LABEL = {"": "Text message", "sms": "Text message", "push": "Push notification", "reminder": "Reminder"}
CARD_LABEL = {"checklist": "Checklist", "questionnaire": "Questionnaire", "email": "Email", "report": "Report",
              "dashboard": "Dashboard", "ui-card": "In-app card"}
_ITEM = re.compile(r"^\s*(?:[-*]\s+)?(?:\[\s?[xX ]?\s?\]|☐|☑|\d+[.)])\s*(.+)$")
_DONE = re.compile(r"^\s*(?:you are done|done when|done)\b[:\s]*", re.I)
_ANSWER = re.compile(r"^\s*answer\s*:\s*(.+)$", re.I)


def _parse(message: str) -> tuple:
    """(title, intro lines, items as (text, answer kind), done line) from a design.md body."""
    title, intro, items, done = "", [], [], ""
    for raw in (message or "").splitlines():
        line = raw.rstrip()
        if not line.strip() or set(line.strip()) <= set("-─=_"):
            continue
        a = _ANSWER.match(line)
        if a and items:
            items[-1] = (items[-1][0], a.group(1).strip())
            continue
        if _DONE.match(line):
            done = line.strip()
            continue
        m = _ITEM.match(line)
        if m:
            items.append((m.group(1).strip(), ""))
        elif not title:
            title = line.strip().lstrip("#").strip()
        elif not items:
            intro.append(line.strip())
        else:
            done = done or line.strip()
    return title, intro, items, done


def _channel_card(label: str, title: str, intro: list, rows: str, done: str, small: bool) -> str:
    w, f = ("230px", "12px") if small else ("420px", "14px")
    return (f'<div style="border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:4px 0;max-width:{w};'
            f'background:var(--bg);font-size:{f}"><div class=mut style="font-size:11px;margin-bottom:6px">{esc(label)}</div>'
            + (f'<div style="font-weight:600;margin-bottom:6px">{esc(title)}</div>' if title else "")
            + "".join(f'<div class=mut style="margin-bottom:6px">{esc(t)}</div>' for t in intro)
            + rows + (f'<div class=mut style="margin-top:8px;font-size:12px">{esc(done)}</div>' if done else "") + "</div>")


def checklist_card(message: str, small: bool = False) -> str:
    """A checklist as the reader works through it: a tick box per item, the day labels as written, the done line."""
    title, intro, items, done = _parse(message)
    rows = "".join('<div style="display:flex;gap:8px;align-items:flex-start;margin:4px 0">'
                   '<span style="flex:none;width:14px;height:14px;border:1.5px solid var(--mut,#888);border-radius:3px;'
                   f'margin-top:2px"></span><span>{esc(t)}</span></div>' for t, _ in items)
    return _channel_card("Checklist", title, intro, rows, done, small)


def _answer_box(kind: str) -> str:
    k = (kind or "sentence").lower()
    box = 'border:1px solid var(--line);border-radius:6px;background:var(--bg);'
    if k.startswith("time"):
        return f'<div style="{box}width:90px;height:24px;margin:4px 0 0;padding:2px 8px" class=mut>__ : __</div>'
    if k.startswith(("yes", "y/n")):
        return '<div class=mut style="margin-top:4px">○ Yes &nbsp; ○ No</div>'
    if k.startswith("choice"):
        opts = [o.strip() for o in k.split(":", 1)[-1].split("/") if o.strip()]
        return '<div class=mut style="margin-top:4px">' + " &nbsp; ".join(f"○ {esc(o)}" for o in opts) + "</div>"
    lines = 3 if "sentences" in k or "paragraph" in k else 2
    return f'<div style="{box}height:{lines * 18}px;margin-top:4px"></div>'


def questionnaire_card(message: str, small: bool = False) -> str:
    """A questionnaire as the reader fills it in: each question numbered, an answer box under it (its kind:
    sentence · sentences · time · yes-no · choice: a / b), the done line. Never a tick box: the reader writes."""
    title, intro, items, done = _parse(message)
    rows = "".join(f'<div style="margin:8px 0"><div><b>{i}.</b> {esc(t)}</div>{_answer_box(kind)}</div>'
                   for i, (t, kind) in enumerate(items, 1))
    return _channel_card("Questionnaire", title, intro, rows, done, small)


FENCED = R.FENCED


def words_of(text: str) -> str:
    """A design's words: the fenced block when its text has one (a note around it, such as a character count, is not
    the design), else the text as written; the rule release.py's words_of keeps for the delivery (the design example
    exposed it, 261108: a phone showed the fence and the count note)."""
    m = FENCED.search(text or "")
    return m.group(1).strip() if m else (text or "").strip()


def draft_files(d: dict) -> list:
    """A design's drafts in order, each (its Run, its design.md): draft 1 is the generate's result/, then one per pass of
    run-revise-d<NN> that wrote a design.md (a revise keeps its draft in its pass, never in a result/)."""
    out = []
    for r in d["drafts"]:
        passes = sorted((r["path"] / "passes").glob("*/design.md")) if r["type"] == "revise" else []
        out += [(r, f) for f in passes] or [(r, r["path"] / "result" / "design.md")]   # an older revise kept result/
    return out


def as_read(message: str, venue: str = "", small: bool = False) -> str:
    """A design in its channel's look: a phone for an SMS, a push or a reminder; tick boxes for a checklist;
    answer boxes for a questionnaire; a card named by its channel for the rest."""
    message = words_of(message)
    v = (venue or "").strip().lower()
    if v in PHONE_LABEL:
        return phone(message, small, PHONE_LABEL[v])
    if v == "checklist":
        return checklist_card(message, small)
    if v == "questionnaire":
        return questionnaire_card(message, small)
    w = "230px" if small else "420px"
    return (f'<div style="border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:4px 0;max-width:{w};'
            f'background:var(--bg)"><div class=mut style="font-size:11px;margin-bottom:6px">{esc(CARD_LABEL.get(v, v.title()))}'
            f'</div><div style="white-space:pre-wrap;word-break:break-word">{esc(message or "—")}</div></div>')


def screen_of(task: Path | None, root: Path) -> Path | None:
    """A UI design's rendered screen: the first PNG in its Task's screens/ (render_screen.py writes it), or None."""
    shots = sorted((task / "screens").glob("*.png")) if task and (task / "screens").is_dir() else []
    return shots[0] if shots else None


def as_it_reads(message: str, task: Path | None, root: Path, small: bool = False, venue: str | None = None) -> str:
    """A design as its reader sees it: a UI design's screen (its screens/ PNG), else drawn in its goal's channel
    (b03; a checklist and a questionnaire are not messages)."""
    png = screen_of(task, root)
    if png is None:
        return as_read(message, R.venue_of(task) if venue is None else venue, small)
    w = "190px" if small else "280px"
    return (f'<a href="/{esc(rel(png, root))}" target=_blank rel=noopener>'
            f'<img loading=lazy alt="{esc(png.stem)}" src="/{esc(rel(png, root))}" style="max-width:{w};border:1px solid var(--line)"></a>')
