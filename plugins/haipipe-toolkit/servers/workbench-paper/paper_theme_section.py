"""A paper Section's Task views: the base's Page Task with the paper's lines over it (the reader contract, its SUB-* rows,
◆ Ready, the Review Items that land on it). Moved from paper_theme.py, which re-exports every name here so
`from live.paper_theme import section_spaces` keeps working."""
from __future__ import annotations

from src.common import delivery_read_lane_dir
import re
from pathlib import Path

from live.frame import Space, esc, face, pop, reader, table, vanilla
from live.paper_theme import _st
from live.task_draft import draft_task_spaces


READINESS = Path(__file__).resolve().parents[2] / "skills/2_theme/paper/haipipe-paper/ref/submission-readiness.md"
CONTRACT = ("reader-question", "entry-state", "exit-state", "must-establish", "must-refuse", "transition-in",
            "transition-out", "story-row", "section_kind", "structure-source", "structure-division")
SUB_PREFIX = {"introduction": "SUB-INTRO", "methods": "SUB-METHOD", "results": "SUB-RESULT", "discussion": "SUB-DISC"}


def _header(md):
    """The face's `key: value` lines above its first `## ` heading."""
    out = {}
    for line in (md.read_text(encoding="utf-8", errors="replace").splitlines() if md else []):
        if line.startswith("## "):
            break
        key, sep, value = line.partition(":")
        if sep and key.strip() and " " not in key.strip():
            out[key.strip()] = value.strip()
    return out


def _contract(md):
    """◆ Scope: the reader contract, read from the face's header (haipipe-paper-draft's fields)."""
    head = _header(md)
    rows = [(esc(k), esc(head[k]) if head.get(k) else '<span class=mut>—</span>') for k in CONTRACT]
    return ('<h3>◆ The reader contract</h3><p class=mut>read from the face\'s header; a stale story-row sends '
            'the Section back to its Story</p>' + table(("field", "value"), rows))


def _sub_rows(md):
    """◆ Requirement: the Section's SUB-* rows (submission-readiness.md), by its section_kind, folded."""
    prefix = SUB_PREFIX.get(_header(md).get("section_kind", "").strip().lower())
    if not prefix or not READINESS.is_file():
        return ""
    rows = [[c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            for line in READINESS.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.startswith(f"| `{prefix}-")]
    body = table(("id", "criterion", "axes"), [(esc(r[0]), esc(r[1]), esc(r[2])) for r in rows if len(r) > 2])
    return (f'<details class=topic><summary><b>◆ {esc(prefix)}-* · this Section at submission</b>'
            f'<span class=topic-meta>{len(rows)} rows, judged on the four axes at G4</span></summary>'
            f'<div style="padding:8px 14px">{body}</div></details>')


def _ready(folder, md):
    """◆ Delivery: ready for the build (outline approved · every display has preview.pdf · its PDF
    compiles), shown apart from done (the Page CHECK)."""
    stem = md.stem if md else folder.name
    try:
        from src.outline_version import latest_outline, plan_dir
        plan = latest_outline(plan_dir(folder), stem)
    except Exception:
        plan = None
    approved = _header(plan).get("approved", "") if plan else ""
    units = sorted(d for d in folder.glob("results/run-display-*/payload/Display*") if d.is_dir())
    previews = sum((d / "preview.pdf").is_file() for d in units)
    pdf = (delivery_read_lane_dir(folder, "latex") / f"{stem}.pdf").is_file()
    checks = sorted(folder.glob("runs/run-check-*.md"))
    lights = [_st(bool(approved) and not approved.startswith("⬜"), "outline approved"),
              _st(previews == len(units), "every display has its preview.pdf"),   # the lamp is the state; no tally
              _st(pdf, f"{stem}.pdf compiles")]
    done = (f"the Page CHECK {esc(checks[-1].stem)}, its verdict in Runs" if checks
            else "no Page CHECK yet")
    # a card group, as the base's Delivery cards (div.topic > .st-bar), before its lanes (JL 261007)
    return ('<h2>◆ Ready</h2>'
            f'<div class=topic><div class=st-bar><span><b>ready for the build</b> {" · ".join(lights)}</span></div></div>'
            f'<div class=topic><div class=st-bar><span><b>done</b> <span class=mut>{done}; the version\'s '
            f'submit (G4) is the Job\'s</span></span></div></div>')


def _round_pages(folder):
    """The comments of this Section's version (haipipe-paper-comments): a report of type comments in the
    version's reports/qNN_<kind>-<MMDD>/ (JL 261007: "a special type of report … in the reports/"), and
    the older layouts still read: RD<NN>-… and CM<NN>-… in the Board's B<x>-<desk>-Round/ or the version."""
    board, version = folder.parent.parent, folder.parent
    found = [p for kind in ("RD", "CM") for p in list(board.glob(f"B[a-z]-*-Round/{kind}*/{kind}*.md"))
             + list(version.glob(f"{kind}*/{kind}*.md"))]
    found += [q for q in version.glob("reports/q[0-9][0-9]_*/q[0-9][0-9]_*.md")   # a comments report (JL 261007)
              if re.search(r"(?m)^page-type:\s*(comments|round)\b", q.read_text(encoding="utf-8", errors="replace"))]
    return sorted({p.resolve() for p in found if p.stem == p.parent.name})


def _review_items(folder):
    """[(round page, row)]: the rows of each Round page's `## Review Items` table whose `lands on` starts
    with this Section's stem (the Round's table, agreed by JL 261007; haipipe-paper-comments)."""
    out = []
    for page in _round_pages(folder):
        text = page.read_text(encoding="utf-8", errors="replace")
        if "## Review Items" not in text:
            continue
        lines = [l for l in text.split("## Review Items", 1)[1].split("\n## ", 1)[0].splitlines() if l.startswith("|")]
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
        rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
        if not rows:
            continue
        head = [h.lower() for h in rows[0]]
        for r in rows[1:]:
            row = dict(zip(head, r))
            if row.get("lands on", "").startswith(folder.name):
                out.append((page, row))
    return out


def _reviews(folder, root):
    """◆ Comments: the Review Items of the version's comments Pages that land on this Section (Review-<slug>, citing the
    points it answers: R1.1 · E1.2 · A1.2), Review Item │ Work │ Report."""
    items = _review_items(folder)
    if not items:
        return ('<p class=space-empty>No Review Items yet. A comments Page\'s Review Items (Review-&lt;slug&gt;, citing '
                'R1.1 · E1.2 · A1.2) show here once its comments Page lists them.</p>')
    rows = [(f'<b>{esc(r.get("item", ""))}</b> <span class=mut>cites {esc(r.get("cites", ""))} · '
             f'{esc(r.get("lands on", ""))}</span>',
             f'{esc(r.get("work", "") or "—")} <span class=mut>· {esc(r.get("state", ""))}</span>',
             pop(reader(page, root), page.stem, f'{page.stem} › {r.get("reply", "") or "no reply yet"} ↗'))
            for page, r in items]
    return table(("Review Item", "Work", "Report"), rows)


def section_spaces(folder, root, sub):
    """A Section's six Spaces: the base's Page Task, each paper line added to the Space it belongs to;
    the subspaces stay the base's."""
    from dataclasses import replace
    out = draft_task_spaces(folder, root, sub)
    md = face(folder)
    d, a, w, plan = out["Description"], out["Audience Report"], out["Delivery"], out["Work Details"]
    if d.open == "Scope":
        base = vanilla("Task", folder, root, sub).get("Description")
        out["Description"] = replace(d, html=_contract(md) + (base.html if base else ""))
    if plan.open == "1 · Plan":                   # the Requirement is a card of 1 · Plan (b32 s41 Ⓐ)
        out["Work Details"] = replace(plan, html=plan.html + _sub_rows(md))
    elif plan.open == "3 · Evidence":             # a Section's evidence follows the paper's rules (haipipe-paper 1.15)
        out["Work Details"] = replace(plan, html=plan.html.replace("/haipipe-evidence ", "/haipipe-paper-evidence "))
    if sub == "Comments":                         # ◆ the paper's own view, after the Page's three
        a = Space(html=_reviews(folder, root), open="Comments", run_types=())
    out["Audience Report"] = replace(a, subspaces=tuple(draft_task_spaces(folder, root, "")["Audience Report"].subspaces)
                                     + ("Comments",), note="")   # no read-only note in the Runs panel (JL 261008)
    out["Delivery"] = replace(w, html=_ready(folder, md) + w.html)   # ◆ Ready over the base's cards
    return out
