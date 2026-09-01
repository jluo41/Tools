"""🏷 Labeling · live, receipt-first view of one page-local labeling/ job.

The surface is deliberately read-only.  It reports metadata from canonical
artifacts, never protected item text, and it never upgrades an observed file
to a passed gate.  The embedded page chat is transport; the subjective-label
workflow remains the only writer of labeling events and receipts.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse


PHASES = (
    ("P0", "Contract"), ("P1", "Round"), ("P2", "Freeze"),
    ("P3", "Test"), ("P4", "Scan"), ("P5", "Audit"),
)

P0_FILES = (
    "config.yaml", "corpus/manifest.json", "test/sealed/status.json",
    "register.md", "policy/versions/G_00/manifest.yaml",
)


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def _yaml_scalar(path: Path, key: str) -> str:
    """Read one simple YAML scalar without introducing a runtime dependency."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    hit = re.search(r"(?m)^\s*%s:\s*([^#\n]+)" % re.escape(key), text)
    return hit.group(1).strip().strip("'\"") if hit else ""


def _truth(value) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "pass", "passed", "valid"}


def _job_root(page_src: Path) -> tuple[Path, str]:
    """Return the canonical root, with a read-only bridge for the old FT layout."""
    lane = page_src.parent / "labeling"
    if (lane / "config.yaml").is_file() or not lane.is_dir():
        return lane, "canonical page-local lane"
    legacy = sorted(lane.glob("field-tests/*/run/config.yaml"))
    if legacy:
        return legacy[-1].parent, "legacy nested field-test · migrate to labeling/"
    return lane, "canonical page-local lane"


def inspect(page_src: Path) -> dict:
    root, location_note = _job_root(page_src)
    p0 = {rel: (root / rel).is_file() for rel in P0_FILES}
    round_dirs = sorted(
        (p for p in (root / "rounds").glob("round_*") if p.is_dir()),
        key=lambda p: p.name,
    ) if (root / "rounds").is_dir() else []
    checkpoints = [(r, _read_json(r / "checkpoint.json"))
                   for r in round_dirs if (r / "checkpoint.json").is_file()]
    open_rounds = [r.name for r in round_dirs if not (r / "checkpoint.json").is_file()]
    latest_round, latest = checkpoints[-1] if checkpoints else (None, {})

    handoff = root / "handoff" / "label-v1.yaml"
    handoff_status = _yaml_scalar(handoff, "status") if handoff.is_file() else ""
    eval_lock = root / "test" / "final" / "lock.json"
    eval_registry = root / "evaluation" / "registry.yaml"
    eval_summary = root / "evaluation" / "summary.md"
    prod_runs = sorted(p for p in (root / "production").glob("run_*") if p.is_dir()) \
        if (root / "production").is_dir() else []
    audits = sorted(p for p in (root / "audit").glob("final_*") if p.is_dir()) \
        if (root / "audit").is_dir() else []
    latest_prod = prod_runs[-1] if prod_runs else None
    latest_audit = audits[-1] if audits else None
    dstar = root / "corpus" / "final" / "D_star.jsonl"
    dstar_manifest = root / "corpus" / "final" / "manifest.yaml"

    if latest_audit and (latest_audit / "receipt.json").is_file():
        phase_i = 5
    elif latest_prod:
        phase_i = 4
    elif eval_lock.is_file() or eval_summary.is_file():
        phase_i = 3
    elif handoff.is_file():
        phase_i = 2
    elif checkpoints or round_dirs or all(p0.values()):
        phase_i = 1
    else:
        phase_i = 0

    config = root / "config.yaml"
    simulation = _truth(_yaml_scalar(config, "simulation_only"))
    human_id = _yaml_scalar(config, "human_id")
    authority_mode = _yaml_scalar(config, "mode")
    creates_gold = _yaml_scalar(config, "creates_human_gold")
    missing_human = all(p0.values()) and not human_id
    authority_hold = missing_human or simulation or "simulation" in authority_mode.lower() \
        or (creates_gold and not _truth(creates_gold))
    authority_reason = ("config does not name one identified human semantic authority"
                        if missing_human else
                        "a simulation/proxy cannot create human gold or sign Freeze")

    gates = latest.get("stopping_gates") or latest.get("gates") or {}
    gate_pass = {name: _truth((gates.get(name) or {}).get("pass"))
                 for name in ("quality", "stability", "coverage", "risk")}
    stop_signoff = _truth(latest.get("human_stop_signoff")) \
        or _truth((latest.get("stopping_gates") or {}).get("human_stop_signoff"))

    open_cells = ((latest.get("coverage") or {}).get("open_cells") or
                  ((gates.get("coverage") or {}).get("open_cells")) or [])
    open_cells = [str(x) for x in open_cells]
    checkpoint_rel = ((latest_round / "checkpoint.json").relative_to(root).as_posix()
                      if latest_round else "P0 Contract artifacts")

    missing = [rel for rel, present in p0.items() if not present]
    if not root.exists():
        next_action = "P0 Contract · create the page-local labeling/ job through /subjective-label"
    elif missing:
        next_action = "P0 Contract · supply: " + ", ".join(missing)
    elif authority_hold:
        target = (" · target register cell(s): " + ", ".join(open_cells)) if open_cells else ""
        next_action = ("HOLD · owner: one identified real human semantic authority + "
                       "Checkpoint Keeper · preserve: %s · next: start a new "
                       "real-authority Building lineage%s" % (checkpoint_rel, target))
    elif open_rounds:
        next_action = "P1 Round · resume " + open_rounds[0] + " at its first missing canonical event"
    elif checkpoints and not (all(gate_pass.values()) and stop_signoff):
        next_action = "P1 Round · derive one bounded next action from the newest checkpoint and register"
    elif not handoff.is_file():
        next_action = "P2 Freeze · the identified human and Keeper must sign one immutable Label Handoff"
    elif handoff_status and handoff_status != "valid":
        next_action = "HOLD · Label Handoff is present but does not declare status: valid"
    elif not (eval_registry.is_file() and eval_lock.is_file() and eval_summary.is_file()):
        next_action = "P3 Test · freeze the evaluation registry, lock T*, then score closed predictions"
    elif not latest_prod:
        next_action = "P4 Scan · freeze one production manifest before attempts begin"
    elif not latest_audit:
        next_action = "P5 Audit · freeze and run the independent probability audit"
    elif not (dstar.is_file() and dstar_manifest.is_file()):
        next_action = "P5 Audit · close repairs and materialize D* from reconciled terminal rows"
    else:
        next_action = "COMPLETE candidate · rehash G6 and verify the audit receipt before claiming D*"

    if missing:
        first_failed = "G0 Contract → Round · missing " + ", ".join(missing)
    elif authority_hold:
        first_failed = "G2 Round → Freeze · " + authority_reason
    elif not checkpoints:
        first_failed = "G1 Round close · no Keeper-closed checkpoint exists"
    elif not (all(gate_pass.values()) and stop_signoff):
        failed = [name for name, passed in gate_pass.items() if not passed]
        if not stop_signoff:
            failed.append("human STOP signoff")
        first_failed = "G2 Round → Freeze · " + ", ".join(failed) + " remains open"
    elif not (handoff.is_file() and handoff_status == "valid" and eval_registry.is_file()):
        owed = []
        if not handoff.is_file():
            owed.append("Label Handoff absent")
        elif handoff_status != "valid":
            owed.append("Label Handoff status is not valid")
        if not eval_registry.is_file():
            owed.append("evaluation registry absent")
        first_failed = "G3 Freeze → Test · " + ", ".join(owed)
    elif not (eval_lock.is_file() and eval_summary.is_file()):
        first_failed = "G4 Test → Scan · T* lock and passing evaluation summary are required"
    elif not latest_prod or not (latest_prod / "run_report.md").is_file():
        first_failed = "G5 Scan → Audit · reconciled production run report absent"
    elif not latest_audit or not (latest_audit / "receipt.json").is_file() \
            or not (dstar.is_file() and dstar_manifest.is_file()):
        first_failed = "G6 Audit → Complete · valid audit receipt and D* manifest are required"
    else:
        first_failed = "None observed · G6 still requires workflow rehash before a completion claim"

    g2_reported = bool(checkpoints and all(gate_pass.values()) and stop_signoff)
    gate_rows = [
        ("G0", "Contract → Round", sum(p0.values()), len(p0), False,
         "required files observed; hashes are not revalidated by this surface"),
        ("G1", "Round close", len(checkpoints), len(round_dirs), False,
         (latest.get("state") or latest.get("closed") or "no checkpoint") if checkpoints else "no checkpoint"),
        ("G2", "Round → Freeze", 1 if g2_reported else 0, 1, g2_reported,
         "checkpoint reports four gates + human STOP" if g2_reported else "stopping evidence remains open"),
        ("G3", "Freeze → Test", 1 if handoff.is_file() and eval_registry.is_file() else 0, 1,
         handoff_status == "valid" and eval_registry.is_file(),
         "handoff + evaluation registry observed; checksum validation still owed"),
        ("G4", "Test → Scan", sum(p.is_file() for p in (eval_lock, eval_summary)), 2, False,
         "T* lock and evaluation summary must both exist"),
        ("G5", "Scan → Audit", 1 if latest_prod and (latest_prod / "run_report.md").is_file() else 0, 1, False,
         "latest production run report observed" if latest_prod else "no production run"),
        ("G6", "Audit → Complete", 1 if latest_audit and (latest_audit / "receipt.json").is_file() else 0, 1, False,
         "audit receipt observed; this view never certifies it" if latest_audit else "no final audit"),
    ]

    return {
        "root": root, "location_note": location_note, "phase_i": phase_i,
        "p0": p0, "round_dirs": round_dirs, "checkpoints": checkpoints,
        "open_rounds": open_rounds, "latest_round": latest_round,
        "latest": latest, "handoff": handoff, "handoff_status": handoff_status,
        "prod_runs": prod_runs, "audits": audits, "dstar": dstar,
        "dstar_manifest": dstar_manifest, "human_id": human_id,
        "authority_mode": authority_mode, "authority_hold": authority_hold,
        "authority_reason": authority_reason,
        "simulation": simulation, "gate_pass": gate_pass,
        "stop_signoff": stop_signoff, "gate_rows": gate_rows,
        "next_action": next_action, "first_failed": first_failed,
    }


_CSS = """
:root{--bg:#fbfbfa;--fg:#202124;--mut:#72747b;--line:#dddeda;--card:#f2f2ee;
 --accent:#8055a5;--ok:#26734d;--hold:#a34b24}
@media(prefers-color-scheme:dark){:root{--bg:#17181a;--fg:#ececea;--mut:#a1a19c;
 --line:#303238;--card:#202226;--accent:#c59be8;--ok:#72c796;--hold:#ee956f}}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;height:100vh;
 display:grid;grid-template-rows:minmax(280px,56%) minmax(220px,44%)}
#work{overflow:auto;padding:14px 16px;border-bottom:2px solid var(--line)}
header{display:flex;justify-content:space-between;gap:12px;align-items:start}
h1{font-size:17px;margin:0}.mut{color:var(--mut);font-size:12px}.path{font:12px ui-monospace,Menlo,monospace}
.phase{display:grid;grid-template-columns:repeat(6,minmax(72px,1fr));gap:5px;margin:12px 0}
.ph{border:1px solid var(--line);border-radius:8px;padding:7px;background:var(--card);color:var(--mut)}
.ph.now{border-color:var(--accent);color:var(--accent);font-weight:700}.ph.past{color:var(--ok)}
.decision{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.next,.failed{background:var(--card);padding:9px 11px;border-radius:5px}
.next{border-left:4px solid var(--accent)}.failed{border-left:4px solid var(--hold)}
.grid{display:grid;grid-template-columns:minmax(270px,1.2fr) minmax(250px,1fr);gap:10px}
.box{border:1px solid var(--line);border-radius:9px;padding:9px 11px;background:var(--card)}
.box h2{font-size:13px;margin:0 0 6px}.gate{display:grid;grid-template-columns:34px minmax(120px,1fr) auto;gap:7px;
 padding:5px 0;border-top:1px solid var(--line);align-items:baseline}.gate:first-of-type{border-top:0}
.obs{color:var(--mut);font-size:11px}.hold{color:var(--hold)}.ok{color:var(--ok)}
.talk{display:flex;align-items:center;justify-content:space-between;padding:5px 10px;background:var(--card);border-bottom:1px solid var(--line)}
.talk b{font-size:13px}.talk button{border:1px solid var(--accent);color:var(--accent);background:transparent;
 border-radius:6px;padding:4px 9px;cursor:pointer}#chat{border:0;width:100%;height:calc(100% - 37px);display:block}
@media(max-width:700px){body{grid-template-rows:minmax(360px,60%) minmax(220px,40%)}.grid,.decision{grid-template-columns:1fr}.phase{overflow:auto;grid-template-columns:repeat(6,96px)}}
"""


def render(page_src: Path, path_q: str, file_q: str) -> str:
    state = inspect(page_src)
    phase = "".join(
        '<div class="ph %s"><b>%s</b><br>%s</div>' %
        ("past" if i < state["phase_i"] else "now" if i == state["phase_i"] else "",
         pid, name)
        for i, (pid, name) in enumerate(PHASES)
    )
    gates = "".join(
        '<div class=gate><b>%s</b><span>%s<div class=obs>%s</div></span>'
        '<span class="%s">%s/%s observed</span></div>' %
        (gid, html.escape(name), html.escape(str(note)), "ok" if reported else "obs", seen, total)
        for gid, name, seen, total, reported, note in state["gate_rows"]
    )
    latest = state["latest"]
    authority = state["human_id"] or "not declared/readable"
    if state["authority_mode"]:
        authority += " · " + state["authority_mode"]
    hold_class = "hold" if state["authority_hold"] else ""
    root_display = str(state["root"].relative_to(page_src.parent)) \
        if state["root"].is_relative_to(page_src.parent) else str(state["root"])
    artifact = (
        f"{len(state['checkpoints'])} closed checkpoint(s) · "
        f"{len(state['open_rounds'])} open round(s) · "
        f"handoff {'present' if state['handoff'].is_file() else 'absent'} · "
        f"production {len(state['prod_runs'])} · audits {len(state['audits'])}"
    )
    chat_url = path_q + ("&" if "?" in path_q else "?") + "pane=chat"
    prompt = (
        "Use /subjective-label for this labeling page. Derive both frontiers from "
        "canonical artifacts under labeling/, name the first failed G0-G6 assertion, "
        "and take at most one bounded next action. Stop at any human gate or HOLD. "
        "Never treat this chat transcript or model consensus as human gold."
    )
    ctx = json.dumps({"prompt": prompt}, ensure_ascii=False)
    return f"""<!doctype html><meta charset=utf-8>
<title>🏷 Labeling · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<section id=work>
<header><div><h1>🏷 Labeling · {html.escape(page_src.stem)}</h1>
<div class=mut>canonical receipts above · Studio Chat below · chat is transport, not authority</div></div>
<div class="path mut">{html.escape(root_display)}/<br>{html.escape(state['location_note'])}</div></header>
<div class=phase>{phase}</div>
<div class=decision><div class=failed><b>First failed / blocked gate</b><br>{html.escape(state['first_failed'])}</div>
<div class=next><b>One honest next action</b><br>{html.escape(state['next_action'])}</div></div>
<div class=grid>
 <div class=box><h2>Gates · observed files are not certified passes</h2>{gates}</div>
 <div class=box><h2>Authority and artifacts</h2>
  <p class="{hold_class}"><b>Human authority:</b> {html.escape(authority)}</p>
  <p><b>Latest checkpoint:</b> {html.escape(state['latest_round'].name if state['latest_round'] else 'none')}</p>
  <p><b>Reported Building gates:</b> {html.escape(', '.join(k + (' ✓' if v else ' ·') for k,v in state['gate_pass'].items()) or 'none')}</p>
  <p><b>Inventory:</b> {html.escape(artifact)}</p>
  <p class=mut>Protected item text, sealed ids, and per-item judgments are intentionally not rendered here.</p>
 </div>
</div></section>
<section><div class=talk><b>💬 Studio Chat · discuss or run the routed action</b>
<button id=prefill type=button>Prefill safe status ask</button></div>
<iframe id=chat src="{html.escape(chat_url, quote=True)}" title="labeling chat"></iframe></section>
<script>(function(){{'use strict';var C={ctx};document.getElementById('prefill').onclick=function(){{
 var f=document.getElementById('chat'),t=null;try{{t=f.contentDocument.querySelector('#chat textarea');}}catch(e){{}}
 if(!t)return;t.focus();t.value=C.prompt;t.dispatchEvent(new f.contentWindow.Event('input',{{bubbles:true}}));
 this.textContent='Prefilled · review, then send';}};}})();</script>"""


class LabelingMixin:
    """The 🏷 tab. Read-only presenter over the labeling/ lane."""

    def labeling_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0], path_q, file_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_labeling(self, p):
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/labeling?path=%s&file=%s" %
                (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
