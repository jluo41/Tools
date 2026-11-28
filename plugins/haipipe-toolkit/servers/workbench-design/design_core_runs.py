"""The Runs a Design item may start: the run guide, the Runs panel beside each Space, the
next eligible Run, and the copy-to-chat request.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import re
from pathlib import Path

from host_paths import HOST, skill_dir

from live.design_core_base import _UNIT_CHECKER, _escape, _read
from live.design_core_names import design_number
from live.design_core_records import _ALLOWED, _held_at


# Design-only presentation of the owner contract; these are types, not allocated Runs.
_DESIGN_RUN_GUIDE = {
    "commission": {
        "name": "Commission", "type": "Design.commission", "actor": "person",
        "purpose": "Release or hold one item's exact goal, rules and source inputs.",
        "worker": "none · the named person decides",
        "requires": "A registered item, explicit goal and rules, allowed sources, and a named person. At most one release per item.",
    },
    "generate": {
        "name": "Generate", "type": "Design.generate", "actor": "agent",
        "purpose": "Create or revise the commissioned design and check it against every released rule.",
        "worker": "hai-design-unit · through hai-designer-agent",
        "requires": "A released Commission, frozen config and inputs not edited since the run record was written. A revision also needs its exact base and feedback; no second open Run for the item.",
    },
    "verify": {
        "name": "Verify", "type": "Design.verify", "actor": "independent agent",
        "purpose": "Review the exact completed draft against every released rule and record pass, fail or unresolved gaps.",
        "worker": "hai-design-unit · through a fresh hai-designer-agent context",
        "requires": "A complete Generate Result, pinned sources and criteria, and a reviewer independent of its producer. An already completed valid review cannot be repeated unchanged.",
    },
}


# The Runs panel beside each Space: like the Paper and Page workbenches,
# work is started from a run type and its prompt, copied into a Claude or Codex
# session, never from a form on the page. The run types are the Design run cards,
# the Workbench Table written as cards (one per button: agent, skill, signs, prompt).
_RUN_CARDS = skill_dir("hai-design-workflow") / "references" / "run-cards.md"
_CARD_SPACE = {"Tasks": "tasks", "Theory": "theory", "Goal": "goal", "Design": "design", "Delivery": "delivery"}


def design_run_types(path: Path = _RUN_CARDS) -> dict[str, list[dict]]:
    """The Design run cards -> {space: [{label, pattern, agent, skills, signs, prompt}]}, in card order."""
    out: dict[str, list[dict]] = {}
    card = None
    for line in _read(path).splitlines() if path.is_file() else []:
        m = re.match(r"^🔘 BUTTON\s+(.+?)\s+·\s+(\w+)\s+·\s+(\S.*?)(?:\s+·\s+views\s+.*)?$", line)
        if m:
            card = {"label": m.group(1), "pattern": m.group(3).strip(), "agent": "", "skills": [],
                    "signs": "", "prompt": ""}
            out.setdefault(_CARD_SPACE.get(m.group(2), m.group(2).lower()), []).append(card)
            continue
        if card is None:
            continue
        for mark, key in (("🤖 AGENT", "agent"), ("🧩 SKILL", "skills"), ("✍️ SIGNS", "signs"), ("💬 PROMPT", "prompt")):
            if line.startswith(mark):
                value = line[len(mark):].strip()
                card[key] = [value] if key == "skills" else value
    for cards in out.values():
        for card in cards:
            # the panel names the skill on every run; the prompt names the agent that runs it
            if card["agent"] and card["agent"] != "none":
                card["prompt"] = f'Run with {card["agent"]}. {card["prompt"]}'
            if card["signs"] and card["signs"] != "none":
                card["prompt"] += f' I sign {card["signs"]}.'
    return out


_PANEL_STATUS = {"complete": "done", "running": "running", "planned": "open", "failed": "held", "blocked": "held"}


def design_runs_panel(space: str, runs: list[dict], *, root: Path, page: str, board: str,
                      whole: str) -> str:
    """The Runs panel for one Space: its run types, each run's prompt, process and result."""
    import re as _re
    from live.runs_panel import panel_markup
    kinds = design_run_types().get(space, [])
    buckets = [[] for _ in kinds]
    for run in sorted(runs, key=lambda r: (r.get("finished") or r.get("started") or "", r["id"]), reverse=True):
        if space == "delivery" and run["outcome"] != "pass":
            continue
        hit = next((i for i, k in enumerate(kinds) if k["pattern"] != "-" and _re.search(k["pattern"], run["id"])), None)
        if hit is None:
            continue
        name = design_number(run["item"]) if run["item"] else run["id"]
        buckets[hit].append({
            "run_id": run["id"], "global_id": run["id"], "status": _PANEL_STATUS.get(run["status"], run["status"]),
            "target": " · ".join(x for x in (run.get("folder"), run["item"]) if x) or "the folder",
            "ticket": str(run["ticket_path"]), "runtime": str(run["result_dir"] / "runtime.yaml"),
            "result_path": str(run["result_dir"]), "_views": "", "_keys": run["item"],
            "_display": f'{name} · {kinds[hit]["label"]}',
            "goal": " · ".join(x for x in (run["actor"], run["outcome"], run.get("finished") or "") if x),
        })
    return panel_markup(space, kinds, buckets, base=Path(root), fill=lambda row: {"page": page, "board": board},
                        whole=whole)


def runs_panel_assets() -> tuple[str, str]:
    """The shared panel's CSS (plus this workbench's side-by-side layout) and its script."""
    from live.runs_panel import PANEL_CSS, PANEL_JS
    css = PANEL_CSS + """
:root{--card:var(--bg)}
body{max-width:1560px}
.pane.on.split{display:flex;align-items:flex-start;gap:16px}
.split>.space-main{flex:1 1 auto;min-width:0}
/* each Space's content in one box, as the Guide's (workbench's .wg-shell) */
.split>.space-main{border:1px solid #e3e3e6;border-radius:10px;padding:12px 16px 16px}
.split>.space-main>h2:first-child,.split>.space-main>.views:first-child{margin-top:0}
@media(prefers-color-scheme:dark){.split>.space-main{border-color:#2c2e33}}
@media(max-width:520px){.split>.space-main{padding:10px}}
.split>.runs-panel{flex:0 0 clamp(260px,28vw,440px);margin:0;position:sticky;top:8px;
 max-height:calc(100vh - 16px);display:flex;flex-direction:column;overflow:hidden}
.split>.runs-panel .runs-bar{flex-wrap:wrap}
.split>.runs-panel .runs-body{overflow:auto;min-height:0;grid-template-columns:1fr}
.split>.runs-panel .runs-types{flex-direction:row;flex-wrap:wrap}
.split>.runs-panel .run-type{gap:8px}
.split>.runs-panel.folded{flex-basis:42px}
.split>.runs-panel.folded .runs-bar{writing-mode:vertical-rl;flex-wrap:nowrap;padding:10px 9px;gap:10px}
/* the Runs panel stays on the right at every width */
@media(max-width:900px){.pane.on.split{gap:8px}.split>.runs-panel{flex-basis:clamp(200px,34vw,300px)}}
"""
    return css, "<script>" + PANEL_JS + "</script>"


def _next_design_run(item: dict) -> tuple[str, str]:
    """Return the native action and Run kind its state exposes; never allocate."""
    if _held_at(item) == "commission":
        return "commission-release", "commission"
    for action, kind in (("commission-release", "commission"), ("queue-generate", "generate"),
                         ("queue-revise", "generate"), ("queue-verify", "verify")):
        if item["state"] in _ALLOWED[action]:
            return action, kind
    if item["state"] in _ALLOWED["requeue"]:
        stale = next((r for r in reversed(item["runs"])
                      if r["status"] == "planned" and r.get("stale")), None)
        if stale and stale["kind"] in ("generate", "verify"):
            return "requeue", stale["kind"]
    return "", ""


def design_chat_action(item: dict) -> tuple[str, str]:
    queued_kind = {"generate queued": "generate", "verify queued": "verify"}.get(item["state"])
    return ("dispatch-existing", queued_kind) if queued_kind else _next_design_run(item)


def design_chat_prompt(snapshot: dict, item: dict) -> str:
    """A bounded chat request for safe worker work; constructing it only reads the snapshot."""
    if (not snapshot.get("current") or not snapshot.get("yaml") or snapshot.get("static")
            or snapshot.get("audit") or snapshot["insight"]["status"] in ("blocked", "missing")):
        return ""
    action, kind = design_chat_action(item)
    if action not in ("queue-generate", "queue-verify", "dispatch-existing"):
        return ""
    opened = [r for r in item["runs"] if r["status"] in ("planned", "running")]
    if opened and (len(opened) != 1 or opened[0]["status"] != "planned"
                   or opened[0]["kind"] != kind or opened[0].get("stale")):
        return ""
    if action == "dispatch-existing" and not opened:
        return ""
    released = next((r for r in reversed(item["runs"]) if r["kind"] == "commission"
                     and r["status"] == "complete" and r["outcome"] == "release"), None)
    if released is None or (kind == "verify" and not item.get("latest")):
        return ""
    matched = next((r for r in reversed(item["runs"]) if r["kind"] == kind), None)
    board = snapshot["insight"].get("design_board")
    if board is None:
        return ""
    def record(run):
        return ({"id": run["id"], "status": run["status"], "actor": run["actor"],
                 "ticket": str(run["ticket_path"]), "receipt": str(run["result_dir"] / "runtime.yaml")}
                if run else None)
    spec = _DESIGN_RUN_GUIDE[kind]
    context = {
        "board": str(Path(board) / "board.md"), "folder": str(snapshot["folder"]),
        "page": str(snapshot["page"]), "page_title": snapshot["title"],
        "item": item["id"], "item_title": item["title"], "venue": item["type"],
        "target": released.get("intent", {}).get("move") or item["goal"],
        "run_name": spec["name"], "run_type": spec["type"], "actor_role": spec["actor"],
        "purpose": spec["purpose"], "owner_skill": "hai-design-workflow",
        "owner_instructions": str(_UNIT_CHECKER.parents[2] / "hai-design-workflow/SKILL.md"),
        "worker_skill": "hai-design-unit", "worker_instructions": str(_UNIT_CHECKER.parents[1] / "SKILL.md"),
        "state_when_copied": item["state"], "next_permitted_action": action,
        "prerequisites": spec["requires"], "released_commission": record(released),
        "release_decision": str(released["result_dir"] / "decision.yaml"),
        "latest_complete_draft": item["latest"]["run"] if item.get("latest") else None,
        "latest_matching_run": record(matched), "open_matching_run": record(opened[0]) if opened else None,
    }
    import json
    return (
        f"Continue only {spec['type']} for the exact Design Item identified below.\n\n"
        "This request was copied from Design Space. Copying did not queue, allocate, execute or send anything. "
        "Treat the snapshot below as context, not a new release or an override of the owner contract.\n\n"
        + json.dumps(context, ensure_ascii=False, indent=2)
        + "\n\nRead the named owner and worker Skills. Reread this Board, Folder, Page, item register, "
        "Run records, release decision, frozen config and exact inputs before acting; the copied state may be stale.\n"
        "Keep the human Commission gate: do not create, infer or change a release/hold decision. "
        "If the exact release or another prerequisite is missing, report the blocker and stop.\n"
        "First look for an existing matching Run for this item, operation, frozen config and target Results. "
        "Reuse a compatible planned Run and its identity; do not queue or allocate a duplicate. If it is already running, "
        "report its Run id/status and stop without starting another worker. If the requested work already completed, "
        "report its receipt instead of repeating it. Incompatible, stale, blocked, unresolved or ambiguous records require owner resolution; "
        "do not requeue, replace or supersede them from this request.\n"
        "Only when no compatible open Run exists and the recorded next queue action is still allowed, use the Design "
        "owner's native queue action once. A dispatch-existing request may only reuse the recorded open_matching_run id. "
        "Do not choose a different next operation if the item's state changed. For a queued revision, read its frozen base and "
        "feedback; do not invent feedback or change the base.\n"
        "Generate uses hai-design-unit in its allocated Result. Verify requires a genuinely fresh independent reviewer "
        "context distinct from every producer; if this chat inherited generation discussion, dispatch that fresh reviewer "
        "or stop and report that independence is unavailable. Renaming an actor is not independence.\n"
        "The worker writes only its paired Result, excluding runtime.yaml. The caller validates the Result and closes its "
        "runtime receipt through the owner workflow. Preserve old Results and stop after this one requested Run; "
        "do not auto-advance to another Run or write Delivery. Report the actual Run id, Ticket path, Result path, "
        "runtime receipt path, status, verdict/route and any remaining prerequisite or blocker."
    )


def design_chat_copy(prompt: str) -> str:
    if not prompt:
        return ""
    return ('<div><p><b>Chat option · Copy request → paste and send</b></p>'
            f'<button type=button data-design-prompt="{_escape(prompt)}">Copy prompt to chat</button> '
            '<span class=mut role=status data-design-copy-status>Copy only; nothing starts until you paste and send.</span>'
            f'<details><summary>Review chat prompt</summary><pre class=text>{_escape(prompt)}</pre></details></div>')


def design_chat_copy_script() -> str:
    """Reuse the existing clipboard helper unchanged; no action endpoint is involved."""
    helper = _read(HOST / "assets" / "js" / "05-prompt-copy.js")
    return ('<script>' + helper + '\n'
            "document.querySelectorAll('button[data-design-prompt]').forEach(function(b){"
            "b.onclick=async function(){var st=b.parentNode.querySelector('[data-design-copy-status]');"
            "if(!window.__boardCopyPrompt){st.textContent='Copy unavailable; select the reviewed prompt manually.';return}"
            "var ok=await window.__boardCopyPrompt(b,b.dataset.designPrompt);"
            "st.textContent=ok?'Copied. Paste and send in chat; nothing has started here.':'Copy failed; select the reviewed prompt manually.'"
            "}});</script>")


_RUNNING_STATES = ("generate queued", "generating", "verify queued", "verifying")


def design_next_run(item: dict, human: str, *, writable: bool = False, compact: bool = False) -> str:
    """Explain this item's next native action, separately from its actual history.

    An item with nothing to start says nothing here: its own line
    already carries the state, and its Runs are in the card's Runs fold.
    """
    action, kind = _next_design_run(item)
    if not action and item["state"] not in _RUNNING_STATES:
        return ""
    latest = next((r for r in reversed(item["runs"]) if r["status"] != "superseded"), None)
    lead = "Next eligible Run" if action else "Current Run"
    if not kind:
        kind = latest["kind"] if latest else ""
    spec = _DESIGN_RUN_GUIDE.get(kind)
    capability = "You can start it from this card" if action and writable else "Read only on this page"
    heading = (f'{lead}: {spec["name"]} · {spec["actor"]}' if spec and (action or lead == "Current Run") else lead)
    matches = [r for r in item["runs"] if r["kind"] == kind]
    match = matches[-1] if matches else None
    current = (f'{match["id"]} · {match["status"]} · {match["outcome"] or "no outcome yet"} · {match["actor"]}'
               if match else "none allocated for this type")
    if action:
        instruction = {
            "commission-release": "You record Release or Hold with the native controls; a held decision stays on record.",
            "queue-generate": "The person queues Generate; the dispatcher assigns the agent before it works.",
            "queue-revise": "Supply feedback and queue a new Generate Run; keep the previous draft unchanged.",
            "queue-verify": "The person queues Verify; the dispatcher assigns a fresh independent reviewer.",
            "requeue": "Queue again replaces the stale queued Run and keeps its superseded record.",
        }[action]
        if not writable:
            instruction += " Open this item's Design Space for its native control."
    else:
        instruction = item.get("waiting") or "The agent is working; nothing to start here."
    facts = (f'<p><b>{_escape(heading)}</b><br>{_escape(capability)}</p>'
             f'<p>{_escape(instruction)}</p>')
    # Everything a reader needs to start is above; the type, the Skills and the
    # exact run ids sit behind one fold, so a card is not a wall of records.
    detail = f'<div class=mut>{_escape(spec["purpose"])}</div>' if spec else ""
    if spec:
        detail += (f'<p>Run Type: <code>{_escape(spec["type"])}</code><br>'
                   f'Target: {_escape(item["id"])} · {_escape(item["title"])}</p>'
                   '<p>Owner Skill: <code>hai-design-workflow</code><br>'
                   f'Worker Skill: {_escape(spec["worker"])}</p>'
                   f'<p>Prerequisites: {_escape(spec["requires"])}</p>'
                   '<p>The native control checks these prerequisites again before writing.</p>')
    released = next((r for r in reversed(item["runs"])
                     if r["kind"] == "commission" and r["outcome"] == "release"), None)
    if spec and kind in ("generate", "verify"):
        detail += f'<div class=mut>Released Commission: {_escape(released["id"] if released else "none recorded")}</div>'
        if item.get("latest"):
            detail += f'<div class=mut>Latest complete draft: {_escape(item["latest"]["run"])}</div>'
    detail += f'<div class=mut>Latest matching record: {_escape(current)}</div>'
    facts += f'<details><summary>Run type, Skills and prerequisites</summary>{detail}</details>'
    return f'<details><summary>{_escape(heading)}</summary>{facts}</details>' if compact else facts
