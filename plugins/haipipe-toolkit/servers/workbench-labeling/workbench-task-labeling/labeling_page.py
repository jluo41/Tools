"""One labeling page: the brief over each Space, its view steps, the shell band, and `render`."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from live.labeling_job import PHASES
from live.labeling_hold import _page_heading, generated_page_url
from live.labeling_model import (SPACES, _STEP_STATE, _current_policy, _esc, _g0_repair_request,
    _g0_retroactive_block, _hold_words, _md_table, _meaning_allowed, _next_step, _open_definition_run, _round_words,
    _script_json, _space_mapping_ref, _spaces, _view_model)
from live.labeling_embedding_view import _thousands
from live.labeling_data_view import _code_spans, _data_space
from live.labeling_rounds_view import _labeling_space, _quality_space
from live.labeling_runs_view import _delivery_space, _drawers, _run_types, _runs_panel

ASSETS = Path(__file__).parent / "page-assets"
_CSS = (ASSETS / "labeling.css").read_text(encoding="utf-8")
_JS = (ASSETS / "labeling.js").read_text(encoding="utf-8")
_PANEL_CSS_AFTER = (ASSETS / "labeling-panel.css").read_text(encoding="utf-8")     # after the shared PANEL_CSS


# ── The detail of each Space and View (view-structure.md): a brief at the top of every Space,
#    the fuller Contract, Definition, Rounds and Guideline blocks, and the steps of every View.
#    Each block reads a job file or a row of ref-space-mapping.md; none shows item text, and
#    none treats an observed file as a passed gate.

def _facts(pairs: list[tuple[str, str]]) -> str:
    """A Space's brief: label over value, in one wrapping row."""
    return "<dl class=brief>" + "".join(
        f'<div><dt>{_esc(k)}</dt><dd>{v}</dd></div>' for k, v in pairs if v) + "</dl>"


def _space_brief(vm: dict, sid: str) -> str:
    """Where this Space stands, from the job's files: counts and states, never item text."""
    root, canonical, cal = vm["root"], vm["canonical"] or {}, vm["cal"] or {}
    manifest, sealed = vm["manifest"], vm["sealed"]
    if not (root / "config.yaml").is_file():
        prep = vm.get("preparation") or {}
        done = len({r["operation"] for r in prep.get("runs") or [] if r.get("status") == "complete"})
        return _facts([("job", "no Contract yet"),
                       ("corpus preparation", ("done" if done >= 5 else "in progress" if done else "not started")
                        if prep.get("attached") else "not attached")]) \
            if sid == "data" else ""
    rounds = cal.get("rounds") or []
    labeled = sum(int(r.get("finals") or 0) for r in rounds)
    if sid == "data":
        emb = vm.get("embedding") or {}
        n_dev = manifest.get("n_eligible")
        return _facts([
            ("items", _esc(_thousands(manifest.get("n_items"))) if manifest.get("n_items") is not None else ""),
            ("to label", _esc(_thousands(n_dev)) if n_dev is not None else ""),
            ("held back", _esc(_thousands(manifest.get("n_sealed", sealed.get("n_items")))) if sealed else ""),
            ("contract", '<span class=ok>valid</span>' if canonical.get("p0_contract_integrity_valid")
             else '<span class=warn>not valid</span>'),
            ("embedding builds", _esc(len(emb.get("builds") or [])) if isinstance(emb, dict) else "0"),
        ])
    if sid == "labeling":
        current = cal.get("current_round") or {}
        policy = _current_policy(root)
        return _facts([
            ("meanings (G0)", '<span class=ok>confirmed</span>' if canonical.get("g0_passed")
             else '<span class=warn>not confirmed</span>'),
            ("meaning changes", _esc(canonical.get("meaning_revisions") or 0)),
            ("rounds", _esc(len(rounds))),
            ("open round", _esc(f"{_round_words(current['round_id'])} · {current.get('finals', 0)} of "
                                f"{current.get('batch_size', 0)}") if current.get("round_id") else "none"),
            ("labeled", _esc(labeled)),
            ("guideline", _esc(policy) if policy else "none"),
        ])
    if sid == "quality":
        scorecards = list((root / "evaluation" / "scorecards").glob("*")) if (root / "evaluation" / "scorecards").is_dir() else []
        audits = sorted((root / "audit").glob("final_*")) if (root / "audit").is_dir() else []
        return _facts([
            ("held-back test", _esc(f"{sealed.get('n_items')} items · " + (
                "locked" if (root / "test" / "final" / "lock.json").is_file() else "sealed, not locked"))
             if sealed else "none"),
            ("models scored", _esc(len(scorecards)) if scorecards else "none"),
            ("audits", _esc(len(audits)) if audits else "none"),
        ])
    if sid == "delivery":
        runs = sorted((root / "production").glob("run_*")) if (root / "production").is_dir() else []
        return _facts([
            ("handoff", '<span class=ok>frozen</span>' if (root / "handoff" / "label-v1.yaml").is_file() else "not frozen"),
            ("production runs", _esc(len(runs)) if runs else "none"),
            ("final labels", '<span class=ok>released</span>' if (root / "corpus" / "final" / "D_star.jsonl").is_file()
             else "not released"),
        ])
    return ""


def _view_steps(vm: dict, sid: str, vid: str) -> str:
    """Steps in this view: every Run type the Workflow map gives this View, in step order, with
    what it writes and its state on this job (its latest Run, else `not built yet` or `not started`)."""
    ref = _space_mapping_ref()
    if not ref or (not (vm["root"] / "config.yaml").is_file() and (sid, vid) != ("data", "preparation")):
        return ""   # before the Contract only Preparation has steps to show
    text = ref.read_text(encoding="utf-8")
    space = next((name for key, name, _ in SPACES if key == sid), "")
    view = next((vname for key, _, views in SPACES if key == sid for v, vname in views if v == vid), "")
    runs_by_op: dict[str, list[dict]] = {}
    for r in vm["runs"]:
        runs_by_op.setdefault(str(r["operation"]), []).append(r)
    rows = []
    # A job set up from an already-fenced source never acquires source-owned Preparation Runs.
    legacy_prep = (vm["root"] / "config.yaml").is_file() and not (vm.get("preparation") or {}).get("attached")
    if (sid, vid) == ("data", "preparation") and not legacy_prep:
        headers, cells = _md_table(text, "Corpus Preparation Run Types")
        col = {h.lower(): i for i, h in enumerate(headers)}
        for row in cells:
            rows.append((row[col["step"]], row[col["run type"]].strip("`"), row[col["in words"]],
                         row[col["writes to"]] if "writes to" in col else "", False))
        for r in (vm.get("preparation") or {}).get("runs") or []:
            runs_by_op.setdefault(str(r["operation"]), []).append(r)
    headers, cells = _md_table(text, "Workflow map")
    col = {h.lower(): i for i, h in enumerate(headers)}
    for row in cells:
        if row[col["view"]].strip() == f"{space} · {view}":
            rows.append((row[col["step"]], row[col["run type"]].strip("`"), row[col["in words"]],
                         row[col["writes to"]], row[col["started by"]].strip() == "not built yet"))
    if not rows:
        return ""
    body = []
    for step, op, words, writes, unbuilt in rows:
        mine = runs_by_op.get(op) or []
        if mine:
            last = mine[-1]
            cls, word = _STEP_STATE.get(str(last["status"]).split(" ")[0], ("mut", str(last["status"])))
            state = f'<span class={cls}>{_esc(word)}</span> · <code>{_esc(last.get("name") or last["run"])}</code>'
            if len(mine) > 1:
                state += f' <span class=mut>· {len(mine)} runs</span>'
        elif unbuilt:
            state = '<span class=mut>not built yet</span>'
        elif (sid, vid) == ("data", "preparation") and legacy_prep:
            state = '<span class=mut>not used: this job was set up from a fenced source</span>'
        else:
            state = '<span class=mut>not started</span>'
        body.append(f'<tr><td class=num>{_esc(step)}</td><td>{_esc(words)}<br><code class=mut>{_esc(op)}</code></td>'
                    f'<td>{_code_spans(writes)}</td><td>{state}</td></tr>')
    return ('<div class="card steps-card"><h2>Steps in this view</h2><div class=scroll><table class=steptable>'
            '<thead><tr><th>Step</th><th>Run type</th><th>Writes</th><th>On this job</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div></div>')


def _shell_links(path_q: str, standalone: bool) -> str:
    """The line under the title: `all labeling jobs`, back to the Board level. A Page opened
    without a Board has none (no `all boards · board index` line: the Board tab already has them)."""
    if standalone or not path_q:
        return ""
    return (f'<div class="wb-links mut"><a href="/_board/labeling-board?path={_esc(quote(path_q))}">'
            'all labeling jobs</a></div>')


def _shell_band(vm: dict, hold: bool) -> str:
    """The band under the title: where this job stands, read from its files (no item text)."""
    canonical, cal = vm["canonical"] or {}, vm["cal"] or {}
    phase = canonical.get("phase") or cal.get("phase") or ""
    parts = [f"{phase} {dict(PHASES).get(phase, '')}".strip() if phase else "no Contract yet"]
    current = cal.get("current_round") or {}
    rounds = cal.get("rounds") or []
    if current.get("round_id"):
        parts.append(f"{_round_words(current['round_id'])}: {current.get('finals', 0)} of "
                     f"{current.get('batch_size', 0)} labeled")
    elif rounds:
        parts.append(f"{_round_words(rounds[-1].get('round_id'))} {rounds[-1].get('state') or ''}".strip())
    else:
        parts.append("no round yet")
    current_policy = vm["root"] / "policy" / "current"
    policy = current_policy.read_text(encoding="utf-8").strip() if current_policy.is_file() else ""
    parts.append(f"guideline {policy}" if policy else "no guideline yet")
    state = vm["state"]
    reason = canonical.get("hold_reason") or state.get("authority_reason")
    parts.append(f'<span class=warn>HOLD · {_esc(_hold_words(reason))}</span>' if hold and reason else
                 '<span class=warn>HOLD</span>' if hold else "no HOLD")
    return " · ".join(x if x.startswith("<span") else _esc(x) for x in parts)


def render(page_src: Path, path_q: str, file_q: str, page_q: str,
           board_dir: Path | None, *, standalone: bool = False) -> str:
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS
    vm = _view_model(page_src)
    state, canonical, config = vm["state"], vm["canonical"], vm["config"]
    if not standalone and not generated_page_url(path_q, file_q, page_q, board_dir):
        raise ValueError("Labeling Workbench requires the matching generated Page URL")
    hold = bool(state["authority_hold"] or state["next_action"].startswith("HOLD"))
    next_line, next_space = _next_step(vm)
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    title = (construct.get("question") or construct.get("name")
             or (_page_heading(page_src) if vm.get("job") else "") or page_src.stem)
    spaces = _spaces(vm)

    panels = {
        "data": _data_space(vm), "labeling": _labeling_space(vm),
        "quality": _quality_space(vm), "delivery": _delivery_space(vm),
    }
    types = _run_types(vm)
    drawers = _drawers(vm)
    space_buttons = "".join(
        f'<button class=space type=button role=tab id=tab-{sid} aria-controls=panel-{sid} '
        f'aria-selected=false data-space={sid}>{_esc(name)}</button>'
        for sid, name, _ in spaces
    )
    sections = []
    for sid, name, views in spaces:
        chips = "".join(
            f'<button class=chip type=button data-space={sid} data-view={vid}>{_esc(vname)}</button>'
            for vid, vname in views
        )
        panes = "".join(
            f'<div class=pane data-space={sid} data-view={vid} hidden>{panels[sid][vid]}{_view_steps(vm, sid, vid)}</div>'
            for vid, _ in views
        )
        sections.append(
            f'<section class=panel id=panel-{sid} role=tabpanel aria-labelledby=tab-{sid} data-space={sid} hidden>'
            f'<div class=split><div class=space-main><div class=views role=group>{chips}</div>'
            f'{_space_brief(vm, sid)}{panes}</div>'
            f'{_runs_panel(vm, sid, types[sid])}</div></section>'
        )

    cal = vm["cal"] or {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    boot = {
        "mode": "page" if standalone else "board",
        "path": path_q, "file": file_q, "page": page_q,
        "identity": f"{path_q}|{file_q}",
        "human_id": authority.get("human_id") or "",
        "hold": hold,
        "next": next_line,
        "phase": canonical.get("phase") if canonical else None,
        "g0_open": bool(canonical and (canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"
                                       or canonical.get("first_blocked_frontier") == "G0 · label meanings missing"
                                       or canonical.get("g0_retroactive_block") or _g0_repair_request(vm))),
        "g0_retroactive_block": _g0_retroactive_block(vm),
        "g0_repair_request": _g0_repair_request(vm),
        "missing_meanings": canonical.get("meaning_definitions_missing") or [],
        "definition_open": bool(_open_definition_run(vm) and _meaning_allowed(vm)),
        "default_space": next_space,
        "question": construct.get("question") or construct.get("name") or "",
        "schema": cal.get("schema") or {},
        "rounds": cal.get("rounds") or [],
        "current_round": cal.get("current_round"),
        "batch_default": ((config.get("rounds") or {}).get("round1") or {}).get("human_batch_size") or 20,
        "spaces": {sid: [vid for vid, _ in views] for sid, _, views in spaces},
    }
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(page_src.stem)}</title><style>{_CSS}{PANEL_CSS}{SPLIT_CSS}{_PANEL_CSS_AFTER}</style></head><body>'
        f'<h1 class=pagetitle title="{_esc(next_line)}">🏷 {_esc(title)}</h1>'
        f'{_shell_links(path_q, standalone)}'
        f'<div class=wb-band>{_shell_band(vm, hold)}</div>'
        f'<section class=drawer data-drawer-panel=workflow hidden>{drawers["workflow"]}</section>'
        f'<section class=drawer data-drawer-panel=allruns hidden>{drawers["allruns"]}</section>'
        f'<nav class=spaces role=tablist aria-label="Labeling Spaces">{space_buttons}</nav>'
        + "".join(sections) +
        f'<script type=application/json id=labeling-boot>{_script_json(boot)}</script>'
        f'<script>{PANEL_JS}</script><script>{_JS}</script></body></html>'
    )
    from live.workbench_guide import mount_guide
    return mount_guide(document, "labeling", {"path": path_q, "file": file_q},
                       "nav.spaces", "section.panel")
