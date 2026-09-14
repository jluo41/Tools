#!/usr/bin/env python3
"""Standalone 🏷 Labeling presenter for one Page-local subjective-label job.

This module intentionally lives with the domain plugin, not in haipipe-page.
It reads safe receipts and Run envelopes only.  The current Codex task is the
interaction transport; semantic writes still go through the family workflow.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path


PHASES = (("P0", "Contract"), ("P1", "Round"), ("P2", "Freeze"),
          ("P3", "Test"), ("P4", "Scan"), ("P5", "Audit"))
STATUS_ORDER = {"running": 0, "failed": 1, "blocked": 2, "planned": 3,
                "complete": 4, "superseded": 5}


@lru_cache(maxsize=1)
def _job_module():
    path = Path(__file__).with_name("job.py")
    spec = importlib.util.spec_from_file_location("subjective_label_job_for_page", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("subjective-label status engine is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def applicable(page_src: Path) -> bool:
    return page_src.is_file() and page_src.name != "S-Label-Dash.md" \
        and (page_src.parent / "labeling").is_dir()


def _safe_file(path: Path, root: Path) -> bool:
    try:
        return path.is_file() and not path.is_symlink() \
            and path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def _field(path: Path, name: str, root: Path) -> str:
    if not _safe_file(path, root):
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")[:65536]
    hit = re.search(rf"(?m)^{re.escape(name)}:\s*([^#\n]+)", text)
    return hit.group(1).strip().strip("'\"")[:240] if hit else ""


def _runs(root: Path) -> list[dict[str, str]]:
    tickets = root / "runs"
    results = root / "results"
    ids = set()
    if tickets.is_dir():
        ids.update(path.stem for path in tickets.glob("*.yaml") if _safe_file(path, root))
    if results.is_dir():
        ids.update(path.parent.name for path in results.glob("*/runtime.yaml")
                   if _safe_file(path, root))
    rows = []
    for run_id in ids:
        ticket = tickets / f"{run_id}.yaml"
        runtime = results / run_id / "runtime.yaml"
        result = results / run_id / "result.yaml"
        status = _field(runtime, "status", root) or "held"
        rows.append({
            "run": run_id,
            "phase": _field(ticket, "phase", root) or "—",
            "operation": _field(ticket, "operation", root)
                         or _field(runtime, "operation", root) or "unknown",
            "target": _field(ticket, "target", root)
                      or _field(runtime, "target", root) or "—",
            "status": status,
            "outcome": _field(result, "outcome", root)
                       or _field(runtime, "outcome", root) or "No safe outcome yet",
            "ticket": "present" if _safe_file(ticket, root) else "missing",
            "result": "present" if _safe_file(result, root) else "missing",
        })
    return sorted(rows, key=lambda row: (STATUS_ORDER.get(row["status"].lower(), 9),
                                         row["run"]), reverse=False)


def _count_files(directory: Path, root: Path, pattern: str = "*") -> int:
    if not directory.is_dir() or directory.is_symlink():
        return 0
    return sum(1 for path in directory.glob(pattern) if _safe_file(path, root))


def _phase_index(state: dict) -> int:
    phase = str(state.get("phase") or "P0")
    return next((i for i, (name, _) in enumerate(PHASES) if name == phase), 0)


def _metric(label: str, value: object) -> str:
    return (f'<div class="metric"><span>{html.escape(label)}</span>'
            f'<b>{html.escape(str(value))}</b></div>')


def render(page_src: Path) -> str:
    if not applicable(page_src):
        raise ValueError("Page has no direct labeling/ lane")
    root = page_src.parent / "labeling"
    state = _job_module().status(root)
    runs = _runs(root)
    current = next(
        (row for row in runs
         if row["status"].lower() not in {"complete", "done", "superseded"}),
        None,
    )
    phase_i = _phase_index(state)
    phase_strip = "".join(
        f'<div class="phase {"past" if i < phase_i else "now" if i == phase_i else ""}">'
        f'<b>{pid}</b><span>{name}</span></div>'
        for i, (pid, name) in enumerate(PHASES)
    )
    integrity = state.get("integrity_errors") or []
    failed = state.get("first_blocked_frontier") or "No failed frontier reported"
    next_action = state.get("next_action") or "derive the next workflow action"
    run_rows = "".join(
        '<button class="run" type="button" data-run="%s">'
        '<code>%s</code><span>%s · %s</span><b class="%s">%s</b>'
        '<small>%s</small></button>' % (
            html.escape(row["run"], quote=True), html.escape(row["run"]),
            html.escape(row["phase"]), html.escape(row["operation"]),
            html.escape(row["status"].lower()), html.escape(row["status"]),
            html.escape(row["outcome"]),
        ) for row in runs
    ) or '<p class="empty">No allocated Labeling Run yet.</p>'
    current_text = current["run"] if current else "none"
    prompt = (f"Use /subjective-label on {page_src.parent.as_posix()}. "
              f"Current frontier: {failed}. Next action: {next_action}. "
              "Operate exactly one bounded action and stop at the human gate.")
    config = root / "config.yaml"
    authority = _field(config, "human_id", root) or state.get("human_id") or "not declared"
    policies = sum(1 for path in (root / "policy/versions").glob("G_*")
                   if path.is_dir() and not path.is_symlink()) \
        if (root / "policy/versions").is_dir() else 0
    rounds = sum(1 for path in (root / "rounds").glob("round_*")
                 if path.is_dir() and not path.is_symlink()) \
        if (root / "rounds").is_dir() else 0
    checkpoints = _count_files(root / "rounds", root, "round_*/checkpoint.json")
    production = sum(1 for path in (root / "production").glob("run_*")
                     if path.is_dir() and not path.is_symlink()) \
        if (root / "production").is_dir() else 0
    audits = sum(1 for path in (root / "audit").glob("final_*")
                 if path.is_dir() and not path.is_symlink()) \
        if (root / "audit").is_dir() else 0
    integrity_html = "".join(f"<li>{html.escape(str(item))}</li>" for item in integrity) \
        or "<li>No P0 integrity error reported.</li>"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🏷 Labeling · {html.escape(page_src.stem)}</title><style>{_CSS}</style></head>
<body><header><div><h1>🏷 Labeling</h1><p>{html.escape(page_src.stem)}</p></div>
<div class="tags"><span>{html.escape(str(state.get("phase") or "P0"))}</span>
<span>👤 {html.escape(str(authority))}</span><span>⚙ {len(runs)} rl Runs</span></div></header>
<nav role="tablist" aria-label="Labeling spaces">
<button class="on" data-space="workflow">🧭 Workflow</button>
<button data-space="data">🗃 Data</button><button data-space="guideline">📘 Guideline</button>
<button data-space="human">🧑 Human</button><button data-space="quality">🧪 Quality</button></nav>
<main>
<section class="space on" data-panel="workflow"><h2>Workflow Space</h2>
<div class="phases">{phase_strip}</div><div class="decision"><article><b>First blocked frontier</b>
<p>{html.escape(str(failed))}</p></article><article><b>One next action</b>
<p>{html.escape(str(next_action))}</p></article></div>
<div class="grid"><article><h3>Current Labeling Run</h3>{_metric("Run", current_text)}
{_metric("Actual allocated", len(runs))}<p class="muted">Episodes and gates are not Runs.</p></article>
<article><h3>Integrity</h3><ul>{integrity_html}</ul></article></div>
<article><h3>Run envelopes</h3>{run_rows}</article></section>
<section class="space" data-panel="data"><h2>Data Space</h2><div class="grid">
<article>{_metric("corpus manifest", "present" if (root / "corpus/manifest.json").is_file() else "missing")}
{_metric("development items", "protected")}{_metric("embedding manifests", _count_files(root / "cache/embeddings", root, "*/manifest.json"))}</article>
<article>{_metric("production episodes", production)}{_metric("D*", "present" if (root / "corpus/final/D_star.jsonl").is_file() else "not yet")}</article></div>
<p class="guard">Protected item text and sealed identifiers are never rendered here.</p></section>
<section class="space" data-panel="guideline"><h2>Guideline Space</h2><div class="grid">
<article>{_metric("policy versions", policies)}{_metric("current", _field(root / "policy/current", "policy", root) or ((root / "policy/current").read_text(encoding="utf-8").strip() if _safe_file(root / "policy/current", root) else "none"))}</article>
<article>{_metric("meaning receipt", "valid" if state.get("meaning_receipt_valid") else "open")}
{_metric("Label Handoff", "present" if (root / "handoff/label-v1.yaml").is_file() else "not yet")}</article></div></section>
<section class="space" data-panel="human"><h2>Human Space</h2><div class="grid">
<article>{_metric("semantic authority", authority)}{_metric("meaning confirmation", "confirmed" if state.get("meaning_receipt_valid") else "owed")}</article>
<article>{_metric("round episodes", rounds)}{_metric("closed checkpoints", checkpoints)}</article></div>
<p class="guard">Only the named human creates gold or signs STOP/FREEZE. Chat transports the decision; receipts make it real.</p></section>
<section class="space" data-panel="quality"><h2>Quality Space</h2><div class="grid">
<article>{_metric("sealed reservation", "present" if (root / "test/sealed/status.json").is_file() else "missing")}
{_metric("active custodian", state.get("sealed_custodian") or "missing")}
{_metric("source custody", "provenance only · recorded" if state.get("source_custodian_provenance") else "not recorded")}
{_metric("evaluation summary", "present" if (root / "evaluation/summary.md").is_file() else "not yet")}</article>
<article>{_metric("production episodes", production)}{_metric("audit episodes", audits)}</article></div></section>
</main><footer><div><b>💬 Codex Chat transport</b><p>Continue the work in this Codex task; the plugin remains receipt-first and read-only.</p></div>
<button id="copy" type="button" data-prompt="{html.escape(prompt, quote=True)}">Copy next-action prompt</button><span id="copied" role="status"></span></footer>
<script>{_JS}</script></body></html>'''


_CSS = r'''
:root{--bg:#fff;--fg:#202124;--mut:#6f7278;--line:#dedfe3;--card:#f7f7f8;--acc:#8055a5;--ok:#27734c;--bad:#a34b24}
@media(prefers-color-scheme:dark){:root{--bg:#17181a;--fg:#ececea;--mut:#a4a5aa;--line:#303238;--card:#202226;--acc:#c59be8;--ok:#72c796;--bad:#ee956f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding-bottom:90px}header{display:flex;justify-content:space-between;gap:12px;padding:13px 16px;border-bottom:1px solid var(--line)}h1{margin:0;font-size:18px}header p{margin:2px 0 0;color:var(--mut)}.tags{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}.tags span{border:1px solid var(--line);border-radius:6px;padding:3px 7px;background:var(--card);font:11px ui-monospace,monospace}nav{display:flex;overflow:auto;gap:3px;padding:7px 10px 0;border-bottom:1px solid var(--line)}nav button{border:0;border-bottom:2px solid transparent;background:none;color:var(--mut);padding:8px 10px;white-space:nowrap;font-weight:650}nav button.on{color:var(--acc);border-bottom-color:var(--acc)}main{padding:14px 16px}.space{display:none}.space.on{display:block}h2{font-size:16px;margin:0 0 12px}h3{font-size:13px;margin:0 0 7px}.phases{display:grid;grid-template-columns:repeat(6,minmax(72px,1fr));gap:5px;overflow:auto}.phase{border:1px solid var(--line);border-radius:8px;padding:7px;background:var(--card);color:var(--mut)}.phase span{display:block;font-size:11px}.phase.now{border-color:var(--acc);color:var(--acc)}.phase.past{color:var(--ok)}.decision,.grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:10px}article{border:1px solid var(--line);border-radius:9px;padding:10px 12px;background:var(--card)}article p{margin:5px 0}.decision article:first-child{border-left:4px solid var(--bad)}.decision article:last-child{border-left:4px solid var(--acc)}.metric{display:flex;justify-content:space-between;gap:12px;padding:5px 0;border-top:1px solid var(--line)}.metric:first-child{border-top:0}.metric b{text-align:right}.run{display:grid;grid-template-columns:minmax(170px,1fr) minmax(130px,1fr) auto;gap:7px;width:100%;text-align:left;border:0;border-top:1px solid var(--line);padding:8px 0;background:none;color:inherit}.run small{grid-column:1/-1;color:var(--mut)}.run .complete{color:var(--ok)}.run .failed,.run .blocked,.run .held{color:var(--bad)}.muted,.guard{color:var(--mut)}.guard{border:1px dashed var(--line);border-radius:8px;padding:10px}footer{position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 16px;border-top:1px solid var(--line);background:var(--bg)}footer p{margin:2px 0;color:var(--mut);font-size:12px}footer button{border:1px solid var(--acc);background:var(--acc);color:#fff;border-radius:7px;padding:8px 11px}#copied{font-size:12px;color:var(--ok)}
@media(max-width:700px){.grid,.decision{grid-template-columns:1fr}.phases{grid-template-columns:repeat(6,90px)}header{display:block}.tags{justify-content:flex-start;margin-top:7px}.run{grid-template-columns:1fr auto}.run span{grid-column:1/-1}footer{align-items:flex-start}footer p{display:none}}
'''

_JS = r'''(function(){'use strict';var buttons=[].slice.call(document.querySelectorAll('nav button'));var panels=[].slice.call(document.querySelectorAll('.space'));function show(name){buttons.forEach(function(b){var on=b.dataset.space===name;b.classList.toggle('on',on);b.setAttribute('aria-selected',String(on));});panels.forEach(function(p){p.classList.toggle('on',p.dataset.panel===name);});try{localStorage.setItem('labeling-space:'+location.pathname,name);}catch(e){}}buttons.forEach(function(b){b.onclick=function(){show(b.dataset.space);};});try{show(localStorage.getItem('labeling-space:'+location.pathname)||'workflow');}catch(e){show('workflow');}var copy=document.getElementById('copy'),status=document.getElementById('copied');if(copy)copy.onclick=function(){navigator.clipboard.writeText(copy.dataset.prompt||'').then(function(){status.textContent='Copied';},function(){status.textContent='Copy unavailable';});};})();'''
