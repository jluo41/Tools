"""One Design item's card: its closed row (Design · Rationale · Evaluation), the open
card's three columns, and the task block above the cards.

Split out of design_page.py; design_page.py re-exports every name here."""
from __future__ import annotations

from pathlib import Path

from live.design import (
    LINK_SLOT, _escape, design_chat_copy, design_next_run, design_number, design_picture, design_title, with_link,
)
from live.design_page_chain import _SUPPORT_ROLES, _chain_html, _level_of, _page_words, evidence_chain
from live.design_page_elements import _elements_html
from live.design_page_evaluation import _evaluation_col, _rule_checks
from live.design_page_runs import _actions, _design_runs_list


def _rationale_col(item: dict, root: Path | None, goal: dict | None = None) -> str:
    """The open card's middle column: why this design. The design move stays open;
    under it two folds: first the Design elements, each part of the design and what supports
    it, then the Evidence chain those supports come from. How the design was made (its Design
    Runs) sits with the design, in the first column."""
    out = ('<h4 class=colh>Design move</h4>'
           f'<p class=goal>{_escape(item["goal"]) or "<span class=mut>No design move recorded.</span>"}</p>')
    ev = evidence_chain(item)
    for label, (summary, body) in (("Design elements", _elements_html(item, goal or {}, ev)),
                                   ("Evidence chain", _chain_html(item, root, ev))):
        out += f'<details class=sub><summary>{label} · <span class=mut>{_escape(summary)}</span></summary>{body}</details>'
    return out


def _sms_bubble(text: str) -> str:
    """The SMS as the patient sees it, with the `{LINK}` slot where the platform puts the link."""
    return _escape(with_link(text.strip())).replace(LINK_SLOT, f'<span class=link>{LINK_SLOT}</span>')


def shared_rules(items: list[dict]) -> list[str]:
    """The rules every live design keeps, in the order the first one lists them."""
    live = [i for i in items if i["state"] != "declined" and i["acceptance"]]
    if not live:
        return []
    return [r for r in live[0]["acceptance"] if all(r in i["acceptance"] for i in live[1:])]


def _task_block(snapshot: dict, items: list[dict], aim: dict | None = None) -> str:
    """The Design Goal in brief, above the cards: the task, then the objective,
    the audience, how success is measured and the baseline every design is read against,
    then the acceptance checks every design keeps. The full input is the Design Goal Space."""
    row, aim = snapshot["goal"]["row"], aim or {}
    rules = shared_rules(items)
    head = _escape(design_title(row)) if row else _escape(snapshot["title"])
    lines = [(label, aim.get(key, "")) for label, key in (("Objective", "objective"), ("Audience", "target audience"),
                                                           ("Measured by", "success metrics"), ("Baseline", "baseline"))]
    if not any(v for _, v in lines) and row:
        lines = [("Audience", row["audience"]), ("Patient task", row["job"]), ("Channel", row["venue"])]
    if not row:
        lines = [("", "No design task line names this folder yet.")]
    if rules:
        lines.append(("Every design keeps", " · ".join(rules)))
    body = "".join(f'<div class=tl><span class=mut>{_escape(k)}</span>{_escape(v)}</div>' for k, v in lines if v)
    return f'<div class=task><div class=taskhead>{head}</div>{body}</div>'


def _card_columns(item: dict, text: str, picture: bool) -> str:
    """One card's closed row: one short line per column, Design · Rationale ·
    Evaluation. The sentences behind each line are the open card's; the closed row only
    names the design, what it rests on, and where its evaluation stands."""
    pages = sorted((r for r in item.get("evidence_rows", []) if r["role"] in _SUPPORT_ROLES),
                   key=lambda r: "WKID?".index(_level_of(r)))
    rests = (f'<span class=mut>Rests on</span> {_escape(_page_words(pages[0]))}'
             + (f' <span class=mut>· +{len(pages) - 1}</span>' if len(pages) > 1 else "")
             if pages else '<span class=mut>From the design goal alone</span>')
    head, rules = _rule_checks(item)
    checked = "not checked yet" not in head
    all_pass = 'class="g ok"' in rules and 'class="g bad"' not in rules and 'class="g mut"' not in rules
    accept = (('<span class="ok">✓</span> ' if all_pass else '<span class="bad">✗</span> ')
              + '<span class=mut>acceptance</span>' if checked else '<span class=mut>acceptance not checked</span>')
    effect = ' <span class=mut>· effect not tested yet</span>' if item["expected"] else ""
    # The state's emoji sits right after the number, so six rows scan at a glance;
    # the word is said only when the emoji alone does not say it (ready needs no word).
    word = "" if item["state"] == "ready" else item["state"]
    word += (" · waiting on " + item["waiting"]) if item["waiting"] else ""
    state_html = (' <span class="mut st">' + _escape(word.strip(" ·")) + "</span>") if word else ""
    return (f'<span class=c1><span class=line><b>{_escape(design_number(item["id"]))}</b>'
            f' <span class=glyph title="{_escape(item["state"])}">{_escape(item["glyph"])}</span>'
            f' <b>· {_escape(item["title"])}</b>'
            f'{state_html}</span></span>'
            f'<span class=c2><span class=line>{rests}</span></span>'
            f'<span class=c3><span class=line>{accept}{effect}</span></span>')


def _item_card(root: Path, item: dict, human: str, selected: bool, *, writable: bool = True, chat_prompt: str = "",
               extra: str = "", aim: dict | None = None) -> str:
    meta = " · ".join(x for x in (item["type"], item["audience"], item["job"]) if x)
    if item.get("ready"):
        ready = item["ready"]
        size = len(ready["text"].strip().replace(LINK_SLOT, ""))
        text, note = ready["text"], f'Ready for Delivery · {size} characters · passed independent review'

    elif item["latest"]:
        lat = item["latest"]
        verdict = f' · {lat["verdict"]}' if lat["verdict"] and lat["status"] == "complete" else ""
        text, note = lat["text"], f'Latest draft · {_escape(lat["status"])}{_escape(verdict)}'

    else:
        text, note = "", "No draft yet"
    picture = design_picture(root, item)
    if picture:
        # A screen is read as its picture; its source stays one click away.
        design = (picture + f'<div class=mut>{note}</div>'
                  f'<details><summary>the HTML behind this screen</summary><pre class=src>{_escape(text)}</pre></details>')
    elif text and (item["type"] or "").lower() == "sms":
        # An SMS is read as the patient sees it: one bubble on a phone, the link where the system puts it.
        design = (f'<div class=phone><div class=from>Text message</div><div class=bubble>{_sms_bubble(text)}</div></div>'
                  f'<div class=mut>{note}</div>')
    else:
        design = (f'<pre class=text>{_escape(text)}</pre>' if text else "") + f'<div class=mut>{note}</div>'
    actions, fold = _actions(item, human) if writable else ("", "")
    # just "Design Runs": the emoji and the acceptance count already say how far it got
    runs = (f'<details class=runsfold><summary>Design Runs</summary>'
            f'{_design_runs_list(item) or "<div class=mut>No run yet.</div>"}</details>')
    if actions and fold:
        actions = (f'<details class=decide{" open" if selected else ""}><summary>{_escape(fold)}</summary>'
                   f'<div class=act>{actions}</div></details>')
    elif actions:
        actions = f'<div class=act>{actions}</div>'
    # Open, the card keeps the closed row's three columns: the design with its
    # buttons, then its rationale, then its evaluation. The design column stays in view.
    body = (f'<div class=cardgrid><div class="col pic">{design}{runs}{actions}<div class=msg></div></div>'
            f'<div class="col why">{_rationale_col(item, root, aim)}</div>'
            f'<div class="col eval">{_evaluation_col(item, aim)}</div></div>')
    # One fixed-height row per item that opens into a fixed-height card: the row
    # names the item, previews the design in one line, and says where it stands.
    return (
        f'<section class="item{" sel" if selected else ""}" id="item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
        f'<details class="itemfold cardrow"{" open" if selected else ""}><summary>{_card_columns(item, text, bool(picture))}</summary>'
        f'<div class=itembody><div class=mut>{_escape(meta)} · <code>{_escape(item["id"])}</code> in the files</div>'
        f'{design_next_run(item, human, writable=writable)}{design_chat_copy(chat_prompt)}{body}{extra}</div></details></section>'
    )
