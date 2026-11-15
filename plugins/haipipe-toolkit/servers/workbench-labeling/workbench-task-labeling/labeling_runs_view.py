"""The Quality and Delivery Spaces and the Runs panel: the workflow map, the SOP, Run tables and Run
cards."""
from __future__ import annotations

import re
from pathlib import Path

from live.labeling_job import PHASES
from live.labeling_hold import _preparation_module
from live.labeling_model import (SPACES, _card, _esc, _g0_retroactive_block, _job_where, _later, _md_inline,
    _md_table, _meaning_allowed, _open_definition_run, _round_words, _row, _run_name, _space_mapping_ref, _when)
from live.labeling_embedding_view import _engine_command, _unique_labels, _wf_cell
from live.labeling_rounds_view import _chat_prompt, _meaning_prompt, _round_draw, _run_type_skills


_RUN_WORDS = {  # the same words as the `in words` column of ref-space-mapping.md's Workflow map
    "corpus-contract": "Set up the job", "definition-discussion": "Discuss the label meanings",
    "discovery-search": "Search outside evidence",
    "guideline-seed": "Draft a guideline candidate", "test-reserve": "Hold back test items",
    "embedding-build": "Build a map", "round-prepare": "Draw one round",
    "weak-prelabel": "Pre-label one prepared round", "human-calibration": "You label one round",
    "guideline-learn": "Draft a guideline from accepted judgments",
    "round-measure": "Measure one completed judgment set", "round-close": "Close a measured round",
    "handoff-freeze": "Freeze a stopped labeling lineage", "test-gold-lock": "Lock blind answers for the final test",
    "executor-predict": "Have one registered model predict the test",
    "executor-score": "Score one closed set of predictions",
    "executor-select": "Select from the complete scorecard set", "scan-preflight": "Check one frozen production plan",
    "scan-shard": "Label one frozen corpus shard", "risk-route": "Route risky production items to review",
    "human-review": "You label one production risk queue",
    "reconcile": "Reconcile reviewed items into a candidate corpus",
    "audit-sample": "Draw from one frozen audit design", "audit-human-gold": "Blind-label one audit sample",
    "audit-analyze": "Analyze one completed audit sample", "dstar-materialize": "Publish an accepted audited corpus",
}


def _workflow_map(vm: dict) -> str:
    """Run-type rows × Space columns, projected from ref-space-mapping.md, with this job's Run counts."""
    ref = _space_mapping_ref()
    if ref is None:
        return _card("Workflow map", "<p class=mut>ref-space-mapping.md is not reachable from this Board.</p>")
    mapping_text = ref.read_text(encoding="utf-8")
    headers, rows = _md_table(mapping_text, "Workflow map")
    if not headers:
        return _card("Workflow map", "<p class=mut>ref-space-mapping.md has no Workflow map table.</p>")
    col = {h.lower(): i for i, h in enumerate(headers)}
    spaces = [h for h in headers if h in {"Data", "Labeling", "Quality", "Delivery"}]
    counts: dict[str, int] = {}
    for r in vm["runs"]:
        counts[str(r["operation"])] = counts.get(str(r["operation"]), 0) + 1
    names = dict(PHASES)
    labels = ["Run type", "Started by", *spaces, "Writes to", "On this job"]
    body, last = [], None
    for cells in rows:
        cell = lambda name: cells[col[name]] if name in col and col[name] < len(cells) else ""  # noqa: E731
        tag = cell("compatibility tag")
        if tag != last:
            group = f"{tag} · {names.get(tag, tag)} · compatibility capability"
            body.append(f'<tr class=phaserow><td colspan={len(labels)}>{_esc(group)}</td></tr>')
            last = tag
        op = cell("run type").strip("`")
        started = cell("started by")
        n = counts.get(op, 0)
        tds = [
            f'<td data-label="{labels[0]}"><b>{_esc(cell("in words"))}</b><div class=mut><code>{_esc(op)}</code></div></td>',
            f'<td data-label="{labels[1]}" class="{"mut" if started == "not built yet" else ""}">{_md_inline(started)}</td>',
            *(f'<td data-label="{sp}"{" class=empty" if cell(sp.lower()) in ("", "—") else ""}>'
              f'{_wf_cell(cell(sp.lower()))}</td>' for sp in spaces),
            f'<td data-label="{labels[-2]}">{_md_inline(cell("writes to"))}</td>',
            f'<td data-label="{labels[-1]}" class=num>{n or ""}</td>',
        ]
        body.append(f'<tr{" class=live" if n else ""}>{"".join(tds)}</tr>')
    table = ('<div class=scroll><table class=wfmap><thead><tr>'
             + "".join(f"<th>{_esc(h)}</th>" for h in labels)
             + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")
    prep_headers, prep_rows = _md_table(mapping_text, "Corpus Preparation Run Types")
    prep_col = {h.lower(): i for i, h in enumerate(prep_headers)}
    prep_counts: dict[str, int] = {}
    for run in (vm.get("preparation") or {}).get("runs") or []:
        prep_counts[run["operation"]] = prep_counts.get(run["operation"], 0) + 1
    prep_body = []
    for cells in prep_rows:
        operation = cells[prep_col["run type"]].strip("`")
        prep_body.append("<tr>" + "".join((
            f'<td><b>{_esc(cells[prep_col["in words"]])}</b><div class=mut><code>{_esc(operation)}</code></div></td>',
            '<td>source owner · Data → Preparation</td>',
            f'<td><code>{_esc(cells[prep_col["skill"]].strip("`"))}</code></td>',
            f'<td class=num>{prep_counts.get(operation) or ""}</td>',
        )) + "</tr>")
    prep_table = ('<div class=scroll><table class=wfmap><thead><tr>'
                  '<th>Run type</th><th>Owner and view</th><th>Skill</th><th>On this source</th>'
                  '</tr></thead><tbody>' + "".join(prep_body) + '</tbody></table></div>')
    return _card("Corpus Preparation Runs", prep_table) + _card("Workflow map", table)


def _sop_state(op: str, vm: dict, runs_by_op: dict, not_built: set) -> str:
    """Where this job is on one SOP step: done, running, not yet, or not built yet."""
    if op == "gate G0":
        return "done" if (vm.get("canonical") or {}).get("meaning_receipt_valid") else "not yet"
    if op in ("", "—"):
        return ""
    preparation = _preparation_module()
    root = vm.get("root")
    established_job = bool(vm.get("canonical")) or (root is not None and (root / "config.yaml").is_file())
    if (preparation and op in preparation.RUN_TYPES
            and not (vm.get("preparation") or {}).get("linked")
            and established_job):
        return "legacy source"
    runs = runs_by_op.get(op) or []
    running = [r for r in runs if r["status"] == "running"]
    if running:
        return "running · " + ", ".join(_run_name(r["run"]) for r in running)
    done = [r for r in runs if r["status"].startswith("complete")]
    if done:
        return "done · " + ", ".join(_run_name(r["run"]) for r in done)
    if runs:
        return runs[-1]["status"]
    return "not built yet" if op in not_built else "not yet"


def _sop(vm: dict) -> str:
    """The SOP from ref-space-mapping.md: the steps one labeling job walks, and where this job is."""
    ref = _space_mapping_ref()
    if ref is None:
        return ""
    text = ref.read_text(encoding="utf-8")
    headers, rows = _md_table(text, "SOP")
    if not headers:
        return ""
    col = {h.lower(): i for i, h in enumerate(headers)}
    wf_headers, wf_rows = _md_table(text, "Workflow map")
    wf = {h.lower(): i for i, h in enumerate(wf_headers)}
    not_built = {r[wf["run type"]].strip("`") for r in wf_rows
                 if "run type" in wf and "started by" in wf and r[wf["started by"]] == "not built yet"}
    runs_by_op: dict = {}
    for r in (vm.get("runs") or []) + ((vm.get("preparation") or {}).get("runs") or []):
        runs_by_op.setdefault(str(r["operation"]), []).append(r)
    labels = ["#", "Step", "You do", "The chat or engine does", "Where", "Run", "This job"]
    states = []
    for cells in rows:
        cell = lambda name, c=cells: c[col[name]] if name in col and col[name] < len(c) else ""  # noqa: E731
        states.append(_sop_state(cell("run type").strip("`"), vm, runs_by_op, not_built))
    now = next((i for i, st in enumerate(states) if st.startswith("running")), None)
    if now is None:
        now = next((i for i, st in enumerate(states) if st == "not yet"), None)
    body = []
    for i, cells in enumerate(rows):
        cell = lambda name, c=cells: c[col[name]] if name in col and col[name] < len(c) else ""  # noqa: E731
        st = states[i] + (" (now)" if i == now else "")
        cls = "now" if i == now else ("done" if st.startswith("done") else "")
        values = [cell("step"), f"<b>{_md_inline(cell('what happens'))}</b>", _md_inline(cell("you do")),
                  _md_inline(cell("the chat or engine does")), _md_inline(cell("where")),
                  _md_inline(cell("run type")), _esc(st)]
        body.append(f'<tr{f" class={cls}" if cls else ""}>' + "".join(
            f'<td data-label="{_esc(h)}"{" class=num" if h == "#" else ""}>{v}</td>' for h, v in zip(labels, values)) + "</tr>")
    table = ('<div class=scroll><table class="wfmap sop"><thead><tr>'
             + "".join(f"<th>{_esc(h)}</th>" for h in labels)
             + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")
    return _card("SOP · how a labeling job runs", table)
_STATUS_WORDS = {"complete": "done", "running": "in progress", "failed": "failed"}


def _run_title(run: dict, build_names: dict[str, str]) -> str:
    """'Build a map: MiniLM · reply + context', 'Draw a round: round 1'; the Run id stays under it."""
    op = str(run.get("operation") or "")
    words = _RUN_WORDS.get(op, op)
    target = str(run.get("target") or "")
    if not target:
        old = re.match(r"^rl\d+_[^_]+_(.+)$", str(run.get("run") or ""))
        target = old.group(1) if old else ""
    target = target.replace("_", "-")
    if op == "embedding-build" and target in build_names:
        return f"{words}: {build_names[target]}"
    if re.fullmatch(r"round-0*\d+", target):
        return f"{words}: {_round_words(target.replace('-', '_'))}"
    return words


def _outcome_words(text) -> str:
    """A Run's recorded outcome with the method's jargon softened for reading; the record is untouched."""
    text = str(text or "")
    if text == "P0 contract landed; human meaning confirmation remains open":
        return "Job set up; the meaning still had to be confirmed then"
    if text == "judging":
        return "you are labeling"
    text = re.sub(r"(\d+) items drawn from (\d+) eligible", r"\1 items picked from \2 to label", text)
    return (text.replace("development items embedded", "items embedded")
            .replace(" sealed left out", " held-back test items left out"))


def _blocked_words(text: str) -> str:
    """The first failed gate, said as what the job waits for."""
    text = str(text or "")
    if text.startswith("G1 Round close"):
        return "the current round to be fully labeled and then closed (closing a round is not built yet)"
    if "meaning confirmation" in text:
        return "you to read the label meanings and confirm them (Labeling → Definition)"
    return text


def _run_table(vm: dict) -> str:
    """Page-local and linked source-owned Runs: what ran, its state, its result."""
    runs = ((vm.get("preparation") or {}).get("runs") or []) + vm["runs"]
    if not runs:
        return ""
    builds = ((vm.get("embedding") or {}).get("builds")) or []
    build_names = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                                  for b in builds])
    rows = "".join(
        '<tr>'
        f'<td><b>{_esc(_run_title(r, build_names))}</b>'
        f'<div class=mut><code>{_esc(r["run"])}</code></div></td>'
        f'<td class="{"ok" if r["status"] == "complete" else "warn"}">{_esc(_STATUS_WORDS.get(str(r["status"]), str(r["status"])))}</td>'
        f'<td class=mut>{_esc(_outcome_words(r["outcome"]) or ("results/" + r["run"] + "/" if r.get("family") == "corpus" else ""))}</td></tr>'
        for r in runs
    )
    return ('<div class=scroll><table class=runs><thead><tr><th>What ran</th><th>State</th>'
            f'<th>Result</th></tr></thead><tbody>{rows}</tbody></table></div>')


def _drawers(vm: dict) -> dict[str, str]:
    """Workflow (Phases, SOP, map) and All runs; no button opens them, only ?drawer=workflow|allruns."""
    state, canonical = vm["state"], vm["canonical"] or {}
    capability_rows = []
    for pid, name in PHASES:
        if pid == "P0":
            status = "contract valid" if canonical.get("p0_contract_integrity_valid") else "HOLD · contract"
        elif pid == "P1":
            status = "partial · G0 passed" if canonical.get("g0_passed") else "partial · blocked by G0"
        else:
            status = ""
        capability_rows.append(_row(f"{pid} · {name}", _esc(status)))
    phases = _card("Phases", "".join(capability_rows)
                   + _row("waiting for", _esc(_blocked_words(state["first_failed"])))
                   + _row("code", f'<code>{_esc(state["first_failed"])}</code>'))
    return {"workflow": phases + _sop(vm) + _workflow_map(vm),
            "allruns": _card("All runs", _run_table(vm))}


def _run_types(vm: dict) -> dict[str, list[dict]]:
    """Each Space's built Run types and the views that list them, from the Workflow map's `view` column.

    A view shows only its own types (JL 260927). A type the map marks `not built yet` stays in the map
    only, unless this job already has a Run of it; a type with no view yet (`Scan (future)`) shows nowhere.
    """
    ref = _space_mapping_ref()
    mapping_text = ref.read_text(encoding="utf-8") if ref else ""
    headers, rows = _md_table(mapping_text, "Workflow map") if ref else ([], [])
    col = {h.lower(): i for i, h in enumerate(headers)}
    runs_by_op: dict[str, list[dict]] = {}
    for r in vm["runs"]:
        runs_by_op.setdefault(str(r["operation"]), []).append(r)
    space_ids = {name: sid for sid, name, _ in SPACES}
    view_ids = {sid: {vname: vid for vid, vname in views} for sid, _, views in SPACES}
    skills = _run_type_skills()
    out: dict[str, list[dict]] = {sid: [] for sid, _, _ in SPACES}
    for cells in rows:
        def cell(name, c=cells):
            return c[col[name]].strip() if name in col and col[name] < len(c) else ""
        op = cell("run type").strip("`")
        space_name, _, view_names = cell("view").partition(" · ")
        sid = space_ids.get(space_name.strip())
        views = [view_ids[sid][v.strip()] for v in view_names.split(",") if sid and v.strip() in view_ids[sid]]
        if not op or not views or (cell("started by") == "not built yet" and op not in runs_by_op):
            continue
        out[sid].append({"op": op, "words": cell("in words") or _RUN_WORDS.get(op, op),
                         "views": views, "runs": runs_by_op.get(op, []),
                         "skills": skills.get(op, []), "built": cell("started by") != "not built yet",
                         "step": int(cell("step")) if cell("step").isdigit() else 99})
    prep_runs: dict[str, list[dict]] = {}
    for run in (vm.get("preparation") or {}).get("runs") or []:
        prep_runs.setdefault(run["operation"], []).append(run)
    prep_headers, prep_rows = _md_table(mapping_text, "Corpus Preparation Run Types") if ref else ([], [])
    prep_col = {h.lower(): i for i, h in enumerate(prep_headers)}
    for cells in prep_rows:
        if (vm["root"] / "config.yaml").is_file() and not (vm.get("preparation") or {}).get("attached"):
            continue  # an existing legacy job cannot acquire retrospective source-owned Runs
        op = cells[prep_col["run type"]].strip("`")
        words = cells[prep_col["in words"]]
        skill = cells[prep_col["skill"]].strip("`")
        step = int(cells[prep_col["step"]])
        out["data"].append({"op": op, "words": words, "views": ["preparation"],
                            "runs": prep_runs.get(op, []), "family": "corpus",
                            "skills": [skill], "built": True, "step": step - 100})
    for types in out.values():
        types.sort(key=lambda t: t["step"])
    return out


def _run_ask(vm: dict, run: dict) -> str:
    """The Run's prompt: what it did and where its Ticket and Result are."""
    if run.get("family") == "corpus":
        return (f"Review Corpus Preparation Run {run['run']} at {run['owner']}. "
                f"Ticket: runs/{run['run']}.yaml · Result: results/{run['run']}/")
    words = _RUN_WORDS.get(run["operation"], run["operation"])
    return (f"{words}{' · ' + run['target'] if run.get('target') else ''} on the labeling job at {_job_where(vm)}. "
            f"Run {run['run']} · Ticket: runs/{run['run']}.yaml · Result: results/{run['run']}/")


def _run_again(vm: dict, run: dict, *, built: bool = True) -> tuple[str, str]:
    """Resume an open Run or Rerun a closed one; both only copy a prompt."""
    if not built:
        return "", ""  # historical Ticket remains readable; this build has no worker
    if run.get("family") != "corpus" and _g0_retroactive_block(vm):
        return "", ""  # a released round without earlier confirmation is history
    if run["operation"] == "corpus-contract" and run.get("family") != "corpus":
        return "", ""  # the Page's Contract is already bound to this job
    if run.get("family") == "corpus":
        prep = vm.get("preparation") or {}
        if (not vm.get("page_ready", True) or prep.get("error") or prep.get("linked")
                or (vm["root"] / "config.yaml").is_file()):
            return "", ""
        action = "Resume" if run["status"] == "running" else "Rerun"
        return action, (f"{action} the {run['operation']} Corpus Preparation Run for {run['target']} "
                        f"at {run['owner']} through /haipipe-labeling-preparation. "
                        + (f"Keep Ticket {run['run']}." if action == "Resume" else
                           f"Reuse {run['run']} for identical accepted inputs, or allocate a new full run-corpus name for changed inputs."))
    where = _job_where(vm)
    if run["operation"] == "definition-discussion":
        if not _meaning_allowed(vm):
            return "", ""
        active = _open_definition_run(vm)
        if active:
            return (("Resume", _meaning_prompt(vm, run["run"]))
                    if active["run"] == run["run"] else ("", ""))
        return "Rerun", _meaning_prompt(vm)
    if run["operation"] == "human-calibration":
        cal = vm.get("cal") or {}
        current = cal.get("current_round") or {}
        round_id = current.get("round_id") or ""
        if (run["status"] == "running" and current.get("open_item")
                and run.get("target") == round_id.replace("_", "-")
                and not (vm.get("canonical") or {}).get("hold")):
            return "Resume", _chat_prompt(vm, current, _round_draw(vm["root"], round_id), run=run)
        judged = next((r for r in cal.get("rounds") or []
                       if r.get("round_id", "").replace("_", "-") == run.get("target")
                       and r.get("state") == "judged" and r.get("calibration_status") == "running"), None)
        if run["status"] == "running" and judged and not (vm.get("canonical") or {}).get("hold"):
            config = vm.get("config") or {}
            authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
            command = _engine_command("calibration.py", "finalize", "--job-root", where,
                                      "--round", judged["round_id"], "--human-id",
                                      (authority or {}).get("human_id") or "<configured-human-id>")
            return "Resume", (f"Finish the interrupted {run['run']} Result. All items in "
                              f"{judged['round_id']} have final events, but its runtime is still running. "
                              f"Verify the event log, then run: {command}. Do not repeat a judgment.")
        return "", ""  # a stale or finished batch cannot be resumed or rerun
    if run["operation"] in {"round-prepare", "embedding-build"}:
        return "", ""  # these start through checked view actions, not a generic prompt
    if run["status"] == "running":
        return "Resume", (f"Resume Run {run['run']} on the labeling job at {where} through /haipipe-labeling. "
                          "Keep the same Ticket and Result name.")
    return "Rerun", (f"Start a new {run['operation']} Run{' for target ' + run['target'] if run.get('target') else ''} on the labeling job "
                     f"at {where} through /haipipe-labeling. Give it a new full run-labeling name; {run['run']} stays as it is.")


def _skills_line(skills: list[str]) -> str:
    if not skills:
        return ""
    names = " · ".join(f"<code>{_esc(skill)}</code>" for skill in skills)
    return f'<p class=run-skill>Run Type skills {names}</p>'


def _run_card(vm: dict, run: dict, skills: list[str] | None = None, *, built: bool = True,
              index: int = 0) -> str:
    """One Run's card in the shared Runs panel (`index` is its run type's place there).

    Labeling draws its own card so Resume and Rerun stay gated by HOLD, G0 and the
    round's state; the shared panel's script reads only the `run-card data-type` hooks."""
    action, again = _run_again(vm, run, built=built)
    ask = again or _run_ask(vm, run)
    status = str(run["status"])
    blocked_g0 = run.get("family") != "corpus" and _g0_retroactive_block(vm)
    blocked_discussion = (run["operation"] == "definition-discussion" and status == "running"
                          and not _meaning_allowed(vm))
    blocked_history = status == "running" and (blocked_discussion or blocked_g0)
    words = "blocked history" if blocked_history else _STATUS_WORDS.get(status, status)
    times = " → ".join(x for x in (_when(run.get("started_at")), _when(run.get("finished_at"))) if x)
    process = " · ".join(x for x in (times, _outcome_words(run.get("outcome"))) if x)
    files = "".join(f"<li><code>{_esc(p)}</code></li>" for p in run.get("artifacts") or [])
    legacy = (f'<p class=run-skill>Legacy Ticket on disk <code>{_esc(run["run"])}</code></p>'
              if run["name"] != run["run"] else "")
    action_button = (f'<button type=button class=run-copy data-copy="{_esc(again)}">{action}</button>'
                     if again else "")
    blocked_note = ('<p class=warn>This discussion cannot continue after round release. '
                    'Its earlier turns remain on disk.</p>'
                    if blocked_discussion else
                    '<p class=warn>This Run cannot continue: G0 cannot authorize the released round. '
                    'Its Ticket and Result remain on disk.</p>' if blocked_g0 else "")
    review_only = not built or bool(blocked_note) or not again
    prompt_header = ('<details class=run-prompt-box><summary>Record</summary>' if review_only else
                     '<details class=run-prompt-box><summary>Prompt '
                     f'<button type=button class=run-copy data-copy="{_esc(ask)}">Copy</button></summary>')
    return (
        f'<article class=run-card data-op="{_esc(run["operation"])}" data-type="{index}" data-run="{_esc(run["run"])}" '
        f'data-name="{_esc(run["label"])}" data-target="{_esc(run.get("target") or "")}" '
        f'data-targets="{_esc(run.get("target") or "")}" data-state="{_esc(status.split(" ")[0])}" data-views="" hidden>'
        f'<header><b title="{_esc(run["run"])}">{_esc(run["name"])}</b>'
        f'<span class="run-state st-{_esc("blocked" if blocked_history else status.split(" ")[0])}">{_esc(words)}</span>'
        f'{action_button}</header>{blocked_note}'
        f'{_skills_line(skills or [])}{legacy}'
        f'{prompt_header}'
        f'<pre class=run-prompt>{_esc(ask)}</pre></details>'
        f'<h4>Running process</h4><div class=run-process>{_esc(process)}</div>'
        f'<h4>Results</h4><div class=run-results><code>{_esc(run.get("owner") + "/" if run.get("family") == "corpus" else "")}results/{_esc(run["run"])}/</code>'
        f'{f"<ul>{files}</ul>" if files else ""}</div>'
        '</article>'
    )


_CORPUS_ORDER = ("source-normalize", "unit-recipe", "unit-materialize",
                 "unit-check", "initial-group-reserve")


def _next_preparation_operation(vm: dict) -> str | None:
    prep = vm.get("preparation") or {}
    if (not vm.get("page_ready", True) or not prep.get("attached") or prep.get("linked")
            or prep.get("error") or (vm["root"] / "config.yaml").is_file()):
        return None
    completed = {r.get("operation") for r in prep.get("runs") or [] if r.get("status") == "complete"}
    return next((op for op in _CORPUS_ORDER if op not in completed), None)


def _runs_panel(vm: dict, sid: str, types: list[dict]) -> str:
    """One Space's Runs panel, on the right: the shared panel (live.runs_panel), folded at first.

    Each Run type's "+ New Run" prompt is gated here: empty while its step is not next, a gate
    is not passed, or the job is on HOLD, and then the panel offers no "+ New Run"."""
    from live.runs_panel import panel_markup
    where = _job_where(vm)
    kinds, buckets = [], []
    for t in types:
        if t.get("family") == "corpus":
            prep = vm.get("preparation") or {}
            owner = (prep.get("reference") or prep.get("owner_reference") or {}).get("owner")
            prompt = (f"Start the next {t['op']} Corpus Preparation Run for the Page at {where} "
                      f"through /haipipe-labeling-preparation. "
                      + (f"Source owner: {owner}. " if owner else
                         "First attach the source preparation owner to this Page. ")
                      + "Record a full run-corpus Ticket and Result.")
            if t["op"] != _next_preparation_operation(vm):
                prompt = ""
        elif t["op"] == "corpus-contract":
            prep = vm.get("preparation") or {}
            if (prep.get("linked") and not prep.get("error")
                    and not (vm["root"] / "config.yaml").is_file()):
                package = (prep.get("reference") or {}).get("package") or ""
                prompt = (f"Use /haipipe-labeling to create the Labeling Contract for the Page "
                          f"in {vm['root'].parent} from the accepted Corpus Preparation package "
                          f"at {package}. Labeling folder: {where}. Confirm the target trait, "
                          "job ID, identified semantic human, and sealed-test custodian; "
                          "validate the package and custody boundary before writing one "
                          "run-labeling-corpus-contract Ticket and Result. Do not show protected IDs.")
            else:
                prompt = ""
        elif t["op"] == "definition-discussion":
            prompt = _meaning_prompt(vm) if _meaning_allowed(vm) and not _open_definition_run(vm) else ""
        elif t["op"] == "human-calibration":
            current = (vm.get("cal") or {}).get("current_round") or {}
            prompt = (_chat_prompt(vm, current, _round_draw(vm["root"], current["round_id"]))
                      if current.get("round_id") and current.get("open_item")
                      and not current.get("calibration_run")
                      and not (vm.get("canonical") or {}).get("hold") else "")
        else:
            prompt = ""  # embedding-build and round-prepare start through checked view actions
        kinds.append({"label": t["words"], "op": t["op"], "prompt": prompt, "skills": t.get("skills") or [],
                      "views": " ".join(t["views"]), "built": t.get("built", True)})
        # newest first; a Run waiting for the person counts as waiting in the shared panel
        buckets.append([dict(r, _run=r, status="waiting" if r["status"] == "running"
                             and r.get("worker_kind") == "human" else r["status"])
                        for r in reversed(t["runs"])])

    def card(row: dict, index: int, kind: dict, base: Path, fill: dict) -> str:
        return _run_card(vm, row["_run"], kind["skills"], built=kind["built"], index=index)

    return panel_markup(sid, kinds, buckets, base=vm["root"].parent, fill=lambda row: {},
                        whole="this job", folded=True, card=card)


def _delivery_space(vm: dict) -> dict[str, str]:
    state = vm["state"]
    handoff = (_card("Label handoff", _row("status", _esc(state["handoff_status"] or "present")))
               if state["handoff"].is_file() else _later("P2 Freeze"))
    final = (_card("Final labels", _row("D*", "materialized"))
             if state["dstar"].is_file() else _later("P5 Audit"))
    runs = sorted((vm["root"] / "production").glob("run_*")) if (vm["root"] / "production").is_dir() else []
    scan = _card("Scan", _row("production runs", _esc(len(runs)))) if runs else _later("P4 Scan")
    return {"handoff": handoff, "scan": scan, "final": final}
