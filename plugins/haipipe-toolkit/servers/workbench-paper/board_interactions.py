"""A paper Board's interactions (haipipe-interaction forms) on its pages: each form as a folded row with its one
button, the answers of a saved form, and the forms and sign lines that wait on you."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _section
from live.board_read import _waits, face_sections


def answers_of(answer_md: Path) -> list:
    """[(Q id and title, the picked option's words, the note)] of a saved answer_collection.md."""
    text = answer_md.read_text(encoding="utf-8", errors="ignore")
    out = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        title = block.splitlines()[0].strip()
        own = re.search(r"(?m)^> decision:\s*(.+)$", block)        # the person's own decision (a form, or the chat)
        if own and re.search(r"(?m)^Answer: my own decision", block):
            out.append((title, "my own decision: " + own.group(1).strip(), ""))
            continue
        got = re.search(r"(?m)^Answer:\s*([A-Z])\b(.*)$", block)
        if not got:
            continue
        opt = re.search(rf"(?m)^- \[[ x]\] {got.group(1)} · (.+)$", block)
        note = re.search(r"(?m)^> note:\s*(.+)$", block)
        changed = "changed" in got.group(2)
        out.append((title, f"{got.group(1)} · {opt.group(1) if opt else ''}" + (" (changed from my pick)" if changed else ""),
                    note.group(1).strip() if note else ""))
    return out


def _decided(topic: Path) -> list:
    from live import frame
    face_md = frame._notes(topic)
    text = face_md.read_text(encoding="utf-8", errors="ignore") if face_md else ""
    body = next((b for n, b in face_sections(text) if n.strip().lower() == "decided"), "")
    return [ln.strip() for ln in body.splitlines() if re.match(r"^\s*-?\s*s\d+-D\d+", ln)]


def ix_answered(items: list, root: Path) -> str:
    """Report: the forms answered about this part, newest first, each a folded row; open, one line per question: the
    pick, and the note."""
    done = sorted((r for r in items if r.get("state") == "answered" and r.get("answers")),
                  key=lambda r: r.get("received", ""), reverse=True)
    body = "".join(ix_item(r, root, "".join(
        f'<div class=fd-row><span class=n>{esc(q)}</span><span class=d>{esc(pick)}'
        + (f'<br><i>note: {esc(note)}</i>' if note else '') + '</span></div>' for q, pick, note in answers_of(r["answers"])))
        for r in done)
    return _section("Interactions", body) if body else ""


IX_CSS = """<style>details.ix-fold{border-bottom:1px solid var(--line)}details.ix-fold>summary{display:flex;align-items:center;
gap:10px;padding:8px 2px;cursor:pointer;list-style:none}details.ix-fold>summary::-webkit-details-marker{display:none}
details.ix-fold>summary::before{content:"▸";color:var(--muted);font-size:12px;width:12px}details.ix-fold[open]>summary::before{content:"▾"}
details.ix-fold>summary b{flex:1;font-weight:600}details.ix-fold .ix-state{font-size:12.5px;color:var(--muted);white-space:nowrap}
details.ix-fold .ix-state.wait{color:#b35c00;font-weight:600}details.ix-fold .ix-body{padding:0 0 10px 22px;font-size:13.5px}
details.ix-fold .ix-body ol{margin:6px 0;padding-left:20px}
@media(max-width:600px){details.ix-fold>summary{flex-wrap:wrap}details.ix-fold>summary b{flex:1 1 calc(100% - 22px)}
 details.ix-fold>summary .ix-state{margin-left:22px}}</style>"""


def ix_item(r: dict, root: Path, body: str = "") -> str:
    """One interaction, folded (JL 261031: "how could we make the intereactions to be collapased as well? if we don't
    want to see all the details"): its title, state and date, and its one button on the row; open, who asked and about
    what, then its questions with their applied flags (or, given, `body`). No counts on the row."""
    waiting = r.get("state") == "waiting"
    target = r.get("form") if waiting else (r.get("form") or r.get("answers"))   # the answered form, not its raw Markdown
    date = (r.get("received") or "")[:10]
    if not date and target is not None and Path(target).is_file():
        import datetime as _dt
        date = _dt.date.fromtimestamp(Path(target).stat().st_mtime).isoformat()
    button = (f'<a class=fd-btn data-pop="{esc(r["title"])}" href="/{quote(ds._rel(Path(target), root))}" '
              f'onclick="event.stopPropagation()">{"Answer" if waiting else "See answers"}</a>') if target else ""
    if not body:
        flags = {}
        applied = Path(r["path"]) / "applied.md"
        if applied.is_file():
            for m in re.finditer(r"(?m)^(Q\d+) · (applied|in progress) · (\d{4}-\d{2}-\d{2})", applied.read_text(encoding="utf-8", errors="ignore")):
                flags[m.group(1)] = ("✅ applied " if m.group(2) == "applied" else "⏳ in progress ") + m.group(3)
        about = r["topic"].name if r.get("topic") is not None else r.get("about", "")
        body = (f'<p class=mut>asked by {esc(Path(r["page"]).name)}' + (f' · about {esc(about)}' if about else '')
                + f' · <code>{esc(r["run"])}</code></p><ol>' + "".join(
                    f'<li><b>{esc(q)}</b> {esc(ask)}' + (f' <span class=mut>{esc(flags[q])}</span>' if q in flags else '') + '</li>'
                    for q, _, ask in r.get("asks", [])) + '</ol>')
    state = ("waiting for you" if waiting else "answered") + (f" · {date}" if date else "")
    return (IX_CSS + f'<details class=ix-fold><summary><b>{esc(r["title"])}</b><span class="ix-state{" wait" if waiting else ""}">'
            f'{esc(state)}</span>{button}</summary><div class=ix-body>{body}</div></details>')


def ix_waiting(topic, text: str, items: list, item_html, md) -> str:
    """Work: the forms waiting about this part (each with its Answer button), then its sign lines and the decisions an
    agent proposed that no one has confirmed."""
    body = "".join(item_html(r) for r in items if r.get("state") == "waiting") if item_html else ""
    lines = _waits(text) + ([ln for ln in _decided(topic) if re.search(r"proposed by (?:the )?agent", ln, re.I)]
                            if topic is not None else [])
    body += "".join(f'<div class=fd-ask><span>{md(ln.lstrip("- "), topic)}</span></div>' for ln in lines)
    return _section("Interactions", body) if body else ""
