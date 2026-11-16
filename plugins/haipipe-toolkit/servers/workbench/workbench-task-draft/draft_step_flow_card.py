"""5 · Revise: a paragraph's Logic card, drawn from its review line so it reads at a glance (JL 261115: "the logic here
is less readable").

The line: `Flow C1.P4: 7/10 · s15 <step> → s16 <step> → … · <the problem> · weakest join s19 to s20, <why>`.
The card: the problem first, in full; then one row per step with its sentence id; the weakest join drawn as a ✂ row
between the two steps it names. Nothing is clipped. An older line without these parts shows as it was written.
"""
from __future__ import annotations

import re

from live.frame import esc

STEP = re.compile(r"^\s*((?:C\d+\.P\d+\.)?[Ss]\d+[a-z]*)\s*[:·]?\s*(.*)$")
CSS = """<style>
.lg-flow{margin:4px 0 0;display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:13px;line-height:1.4}
.lg-flow .fs{font:500 11px ui-monospace,Menlo,monospace;color:var(--mut);padding-top:1px}
.lg-flow .cut{grid-column:1/-1;color:#8a3b2b;font-size:12px;padding:1px 0 1px 18px}
.lg-prob{margin:3px 0 4px;font-weight:500}
</style>"""


def parse(text: str) -> dict:
    """{score, problem, steps: [(sid, words)], weak: (a, b, why) or None}; steps is [] when the line has no `→`."""
    every = [p.strip() for p in text.split(" · ") if p.strip()]       # the weakest join is one part, wherever it sits
    weak = next((p[len("weakest join "):] for p in every if p.lower().startswith("weakest join ")), "")
    parts = [p for p in every if not p.lower().startswith("weakest join ")]
    score = next((p for p in parts if re.fullmatch(r"(?:\w+\s+)?\d{1,2}/10", p)), "")
    chain = next((p for p in parts if "→" in p), "")
    shape = next((p for p in parts if p.lower().startswith("shape:")), "")
    fix = next((p for p in parts if p.lower().startswith("fix:")), "")
    problem = " · ".join(p for p in parts if p not in (score, chain, shape, fix))
    roles = {}
    for role, ids in re.findall(r"(topic|support|hand-off|handoff|turn|example)\s+([^,;]+)", shape[6:], re.I):
        a = re.findall(r"[Ss]\d+[a-z]*", ids)
        if " to " in ids and len(a) == 2:
            lo, hi = int(re.sub(r"\D", "", a[0])), int(re.sub(r"\D", "", a[1]))
            a = [f"s{k}" for k in range(lo, hi + 1)]
        for x in a:
            roles[x.lower()] = role.lower().replace("handoff", "hand-off")
    steps = []
    for step in (chain.split("→") if chain else []):
        m = STEP.match(step)
        steps.append((m.group(1).lower(), m.group(2).strip()) if m else ("", step.strip()))
    w = re.match(r"\s*([Ss]\d+[a-z]*)\s+to\s+([Ss]\d+[a-z]*)\s*,?\s*(.*)$", weak) if weak else None
    return {"score": score, "problem": problem, "steps": steps, "roles": roles, "fix": fix[4:].strip(),
            "weak": (w.group(1).lower(), w.group(2).lower(), w.group(3).strip()) if w else
                    (("", "", weak.strip()) if weak else None)}


MAP_CSS = """<style>
.pmap-box{margin:4px 0 10px}
.pmap-box .pm{width:auto;min-width:0;grid-template-columns:minmax(150px,230px) minmax(0,1fr);gap:0 48px;padding:6px 2px}
.pmap-box .pm-root{padding:10px 14px}.pmap-box .pm-root b{font-size:15px;margin:0;line-height:1.4}
.pmap-box .pm-root .pm-id{margin-bottom:2px}.pmap-box .pm-root .pm-sc{display:block;margin-top:4px;font-size:12px;color:var(--mut)}
.pmap-box .pm-para{display:block;margin:0}
.pmap-box .pm-pnode{display:flex;align-items:baseline;gap:0;border:0;background:none;padding:3px 0;font-size:14px;line-height:1.5;white-space:normal}
.pmap-box .pm-pnode .pm-s,.pmap-box .pm-pnode .pm-role{flex:none}.pmap-box .pm-pnode .pm-t{flex:0 1 auto;min-width:0}
.pmap-box .pm-cut{flex:0 1 auto;color:#b45309;font-size:12px;margin-left:8px;padding:0 6px;border:1px solid #f0c48a;border-radius:8px}
.rv-flow .pmap-box .pm{grid-template-columns:minmax(110px,150px) minmax(0,1fr);gap:0 28px}.rv-flow .pmap-box .pm-root b{font-size:13.5px}
.rv-flow .pmap-box .pm-pnode{font-size:13px}.rv-flow .pmap-box .pm-role{min-width:0}
</style>"""


def map_html(text: str, inline, para=None, score: str = "") -> str:
    """The paragraph drawn as the Structure view draws it (JL 261115: "why not just have the thins like the mindmap
    graph like we have in the structure"; "what I want is like this"): the paragraph's box on the left, a curve to one
    row per sentence, each row its id, its Bullet's role and its point from § 1. `para` is (paragraph, its name,
    [(sentence, role, point, note)]) from § 1; the Flow line adds only the ★ on the box and, on the sentence after the
    weakest join, "weak link from sNN: <why>" in words. Read-only (no `.pm-edit`, so nothing here writes); '' with no § 1 paragraph."""
    if not para or not para[2]:
        return ""
    pid, job, bullets = para
    f = parse(text)
    cut = f["weak"][1] if f["weak"] and f["weak"][0] else ""
    why = _plain_why(f["weak"][2]) if f["weak"] else ""
    rows = []
    for s, role, words, note in bullets:
        # the weak link said in words on its row (JL 261115, of a bare ✂: "what does this mean?")
        mark = (f'<span class=pm-cut>weak link from {esc(f["weak"][0])}{": " + esc(why) if why else ""}</span>'
                if s.lower() == cut else "")
        rows.append(f'<div class=pm-para data-p="{esc(s)}"><div class="pm-node pm-pnode"><span class=pm-s>{esc(s)}</span>'
                    f'<span class=pm-role>{esc(role)}</span><span class=pm-t>{inline(words, {})}</span>{mark}</div></div>')
    sc = re.search(r"\d{1,2}/10", score or f["score"] or "")
    return (MAP_CSS + '<div class=pm><svg class=pm-wires aria-hidden=true></svg>'
            f'<div class="pm-node pm-root"><span class=pm-id>{esc(pid)}</span><b>{esc(job)}</b>'
            + (f'<span class=pm-sc>★{sc.group(0)}</span>' if sc else "") + f'</div><div>{"".join(rows)}</div></div>')


def _plain_why(why: str) -> str:
    """The weakest join's reason without the two quoted fragments it starts from (JL 261115: the ✂ line with two quotes
    was not understood): `from "…" to "…", from reuse to model size` reads `from reuse to model size`."""
    w = re.sub(r'^\s*from\s+["“][^"”]*["”]\s+to\s+["“][^"”]*["”]\s*,?\s*', "", why or "")
    return w.strip(" ,.;") or (why or "").strip()


def body(text: str, inline) -> str:
    """The card's inner rows (after its head)."""
    f = parse(text)
    if not f["steps"]:                                   # an older line: as written, never clipped
        return (f'<div class="lg-text">{inline(text.partition(" · weakest join ")[0], {})}</div>'
                + (f'<div class="lg-text mut">weakest join {esc(f["weak"][2])}</div>' if f["weak"] else ""))
    out = [CSS]
    if f["problem"]:
        out.append(f'<div class="lg-prob">{inline(f["problem"], {})}</div>')
    rows, cut = [], f["weak"]
    for i, (sid, words) in enumerate(f["steps"]):
        rows.append(f'<span class=fs>{esc(sid)}</span><span>{inline(words, {})}</span>')
        nxt = f["steps"][i + 1][0] if i + 1 < len(f["steps"]) else ""
        if cut and cut[0] and sid == cut[0] and nxt == cut[1]:
            rows.append(f'<span class=cut>✂ weakest join: {inline(cut[2], {})}</span>')
            cut = None
    out.append('<div class="lg-flow">' + "".join(rows) + '</div>')
    if f["fix"]:
        out.append(f'<div class="lg-text"><span class=lg-lab>Fix</span> {inline(f["fix"], {})}</div>')
    if cut:                                              # a join the steps do not show: under them, as written
        out.append(f'<div class="lg-text mut">✂ weakest join {esc(" to ".join(x for x in cut[:2] if x))} {inline(cut[2], {})}</div>')
    return "".join(out)
