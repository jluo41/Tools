"""The points the text and its plan leave unsure (OPEN n), moved out of draft_step_evidence.py (700-line rule);
draft_step_evidence re-exports every name."""
from __future__ import annotations

import re

from live.frame import esc
from live.sentence_id import sid as _sid


def _s_key(s: str) -> tuple:
    m = re.match(r"[Ss]?(\d+)([a-z]?)$", str(s))
    return (int(m.group(1)), m.group(2)) if m else (10 ** 6, "")


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
        for m in re.finditer(r"(?m)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · (.*)$", body):
            for mk in MARK.findall(m.group(2)):
                low = mk.strip().lower()
                kind = ("check" if low.startswith("check") else
                        "pending" if low.startswith("pending") or (len(low.split()) <= 2 and ":" not in low) else "find")
                out.append({"s": _sid(m.group(1)), "kind": kind,
                            "what": re.sub(r"^(check|pending)\b\s*:?\s*", "", mk.strip(), flags=re.I)})
    if d and d.get("structure"):
        for m in re.finditer(r"(?ms)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · .*?(?=^- B\d+[a-z]* · |^#{2,4} |\Z)", d["structure"][1]):
            e = re.search(r"(?m)^\s*Evidence:\s*none\b\s*·?\s*(.*)$", m.group(0))
            if e:
                out.append({"s": _sid(m.group(1)), "kind": "none", "what": e.group(1).strip()})
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
    # a label carries no count (AGENTS.md § Page words): each point shows its own mark where it sits
    return (f'<details class="topic work-task"><summary><span class=related-head><b>❓ Open points</b></span></summary>'
            f'<div class=work-body><table class="rv-rows ev-list" style="border-collapse:collapse;width:100%">{rows}'
            '</table></div></details>')
