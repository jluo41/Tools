"""HaiChat — the console's agent path, over WebSocket.

The Genie-pattern drawer in the SPA talks to this router: one interactive
ClaudeSDKClient per browser session (multi-turn memory, streamed deltas,
visible tool calls, human approval of EVERY tool via can_use_tool). Runs on
the Claude Agent SDK with the local Claude Code login (subscription/OAuth) —
never a pay-per-token API key.

Ported from the REACH D01 demo bridge (examples/.../D01_demo_chat_ui/backend/
app.py) and made portable: the endpoint-predict engine is registered as an
explicit stdio MCP server (resolved the same way console_api resolves it), so
nothing here depends on a repo's .mcp.json or skills directory.

STANDALONE MODE ONLY: embedded beside a HAI-Chat thread the drawer is hidden —
the Mattermost thread is HaiChat there, and haichat-me-agent is the agent.

The score is ALWAYS produced by the prediction endpoint. The agent narrates it;
it never computes or edits it.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from console_api import ENGINE  # same engine the deterministic buttons use
from console_api import ep      # the engine module, used as a library

router = APIRouter()

SYSTEM_PROMPT = """You are HaiChat, the assistant inside an in-lab clinical model console.

The human is a clinician exploring de-identified patients and prediction models. You are
not just answering questions about the console — you can OPERATE it. Every message you
receive carries a <console> block telling you what the clinician has on screen right now
and what they have just done.

YOU HAVE NO FILES, NO SHELL, NO SUBAGENTS. You cannot read the disk, grep a dataset, or
spawn a helper. Two tool families are your entire world: `mcp__console__*` (the
clinician's screen) and `mcp__endpoint-predict__*` (the patient store and the model). If
a question cannot be answered with those, say so plainly instead of reaching.

WHAT YOU CAN DO TO THE CONSOLE (mcp__console__*)
- open_view / focus_view / set_panel / highlight — yours to use freely. Use them.
  A claim the clinician can SEE is worth more than a claim they must go hunting for:
  if you say "there is a 6-hour CGM gap on day 3", `highlight` those rows.
- close_view / select_model / run_model / generate_checklist / switch_patient — these
  WAIT for the clinician's explicit Allow. Ask for them when they are the right move;
  do not be shy about it, but do not fire them speculatively either.

HOW TO BEHAVE IN SOMEONE ELSE'S WINDOW
- Point before you open. Highlighting a row in a tab they already have open is better
  than opening another tab. Prefer focus_view over open_view when the tab exists.
- Do not open more than two views to answer one question. Tabs appearing under a
  clinician's hands is startling; earn each one.
- Never split the layout unless the clinician asked for a side-by-side.
- Narrate what you are doing in one short clause ("opening the Record layer —"), so
  the movement on screen is never a surprise.

RULES YOU MUST NOT BREAK
- The score comes from the endpoint, VERBATIM. Never compute, estimate, re-round, or
  restate a score as your own number. `run_model` returns the real result — read it.
- Always surface the data-gaps report when a prediction ran on missing/empty tables. A
  partial-data run must never be presented as a clean one.
- Do not give treatment advice. This is in-lab exploration on de-identified research
  data, not care.
- THE PATIENT BOUNDARY IS ABSOLUTE. When the patient changes you will see a loud
  PATIENT CHANGED marker. After it, carry NOTHING across: no number, no table, no
  finding, no impression from the previous patient. Fetch what you need again. If the
  clinician explicitly asks you to compare two patients, you may — but you must name
  both patients explicitly in every sentence that mixes them.
- Be concise and clinician-readable. Lead with the finding, then the caveats.
"""

# The lab profile keeps every clinical guardrail (it costs nothing when there is
# no endpoint) and adds the skill/toolbelt contract on top.
LAB_SYSTEM_PROMPT = SYSTEM_PROMPT + """

── LAB MODE ──────────────────────────────────────────────────────────────────
This console is mounted for a LABELING/RESEARCH cohort, not clinical scoring —
there is no prediction endpoint here, so do not offer to score. You are the
executor the ✏️ Annotate view delegates to, and you now have the repo's SKILLS
and a real toolbelt beyond the console:
- Skill — invoke a project skill by name (e.g. /sl-status, /sl-iterate,
  /haipipe-data). Prefer a skill over ad-hoc shell when one fits the task.
- Read / Grep / Glob — inspect the repo and the label store freely.
- Bash / Write / Edit / Task — these ACT on the world, so each one WAITS for the
  researcher's Allow. Name what you are about to do in one clause before you use
  it, exactly as you narrate a console move.
Your job is to help run and adjudicate the subjective-labeling loop.

── GROUP MODE = THE LABELING FORGE ─────────────────────────────────────────────
When the <console> block says `mode: GROUP`, you are NOT looking at one patient —
there is none. The researcher is developing a labeling INSTRUMENT (a guideline)
over the whole CORPUS named in that block. The corpus is fixed; the guideline is
what you are forging. The patient-boundary rules above do not apply in group mode.
The forge runs the subjective-label loop, and the ✏️ Annotate view's ▶ steps reach
you as requests to run the matching skill:
  /sl-init      cold-start: recommend dimensions, elicit intent, seed guideline V0
  /sl-iterate   one round: probe → panel labels → analyze → surface CONFLICTS
  /sl-validate  benchmark the gallery against a public dataset (κ vs human)
  /sl-scale     batch-label the full corpus with the converged gallery
  /sl-status    where the project stands, κ trajectory, next step
The researcher is the PI/adjudicator, never a bulk labeler: surface conflicts and
boundary cases for THEM to rule on; do not label the corpus one row at a time by
hand. Narrate, then run the skill, letting each write pass the Allow gate.
"""

# ── the gate, in two tiers ───────────────────────────────────────────────────────
#
# The line is NOT "harmless". It is: read-only, instantly reversible, and with no
# consequence outside this browser tab. Opening a tab moves nobody's care. Running a
# model hits a real endpoint and produces a clinical number; changing the model
# selection means the clinician presses ▶ Run and scores something other than what they
# believe they chose; closing a tab destroys a pane they may be mid-sentence in.
#
# Both tiers go through can_use_tool. NOTHING is listed in `allowed_tools` — that would
# shadow the callback entirely and silently retire the gate (the SDK even ships a
# CanUseToolShadowedWarning for exactly this mistake).

ALLOWED_AUTO = [
    # the console: navigating and pointing. Reversible, cosmetic, and always VISIBLE —
    # the drawer chips each one and the tab wears a 🤖 until the clinician clicks it.
    "mcp__console__get_state",
    "mcp__console__open_view",
    "mcp__console__focus_view",
    "mcp__console__set_panel",
    "mcp__console__highlight",
    # the engine's READS. Gating these was pure friction with no safety in it: they read
    # the same de-identified record the clinician is already staring at, they change
    # nothing, and the agent cannot answer a single question without them. Making a
    # clinician click Allow three times to look at a chart does not make anyone safer —
    # it just trains them to click Allow without reading. The gate is for ACTIONS.
    "mcp__endpoint-predict__list_patients",
    "mcp__endpoint-predict__get_patient",
    "mcp__endpoint-predict__list_models",
    "mcp__endpoint-predict__ping",
    # prepare_payload is NOT here, and not gated either — it is simply useless to the
    # agent: a CGM payload is the whole ~1.4M-character series, which the CLI spills to
    # a file the agent (having no file tools) cannot read. It would burn a turn to
    # produce nothing. run_model returns the gaps report anyway, which is the only part
    # of the payload the agent actually needs.
]

ALLOWED_GATED = [
    # everything that ACTS: hits a real endpoint, writes clinical content, changes what
    # the clinician's ▶ Run would do, destroys a pane, or re-binds the whole workspace.
    "mcp__console__run_model",
    "mcp__console__generate_checklist",
    "mcp__console__select_model",
    "mcp__console__switch_patient",
    "mcp__console__close_view",
    # NOTE: endpoint-predict__predict_for_patient is deliberately in NEITHER list.
    # Scoring goes through mcp__console__run_model, which presses the console's own
    # ▶ Run — so every score the agent produces lands in the run history the clinician
    # can see, badged 🤖. A score the reader cannot find is the thing this console
    # exists to prevent, and a second scoring path is exactly how you get one.
]

ALLOWED = ALLOWED_AUTO + ALLOWED_GATED

# env the engine subprocess needs — the same cohort this console was launched
# with. Includes the dataset-store forms (INLAB_DATASETS / INLAB_DATASET_STORE)
# as well as the single-store back-compat one, so the agent's endpoint-predict
# reaches the same patients the buttons do regardless of how the cohort was set.
ENGINE_ENV_KEYS = [
    "INLAB_DATASETS", "INLAB_DATASET_STORE", "INLAB_PATIENT_STORE",
    "INLAB_ENDPOINT_STORE", "INLAB_REGISTRY",
    "INLAB_ENDPOINT_URL", "INLAB_ENDPOINT_TOKEN", "INLAB_ENDPOINT_TIMEOUT_SEC",
]


# ── agent profile ────────────────────────────────────────────────────────────
#
# The console serves two cohorts with different safety models, so the agent has
# two profiles, chosen by env like every other cohort choice here:
#
#   clinical (default) — scoring a patient. The agent may touch ONLY the console
#     and the endpoint; the sandbox above (tools=[], setting_sources=[]) denies
#     everything else. This is exactly right for producing a clinical number.
#   lab                — a labeling/research workspace with no scoring endpoint.
#     Here the agent IS the executor the Annotate view delegates to: it loads
#     the repo's skills (/sl-iterate, /sl-status, /haipipe-data, …) and gets a
#     real toolbelt. Reads run free; anything that ACTS (Bash/Write/Edit/Task)
#     still blocks on the researcher's Allow — the same gate clinical writes use.
AGENT_PROFILE = os.environ.get("INLAB_AGENT_PROFILE", "clinical").strip().lower()

# built-in Claude Code tools the lab profile turns on (clinical keeps tools=[])
LAB_TOOLS = ["Skill", "Task", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "TodoWrite"]
LAB_AUTO = {"Read", "Grep", "Glob", "Skill", "TodoWrite"}  # read-only / load-instructions
LAB_GATED = {"Bash", "Write", "Edit", "Task"}              # act on the world → Allow/Deny


def _skills_root() -> str | None:
    """Where the lab agent runs — the repo whose .claude/skills it loads. Override
    with INLAB_AGENT_CWD; else walk up to the first dir carrying .claude/skills."""
    env = os.environ.get("INLAB_AGENT_CWD")
    if env:
        return str(Path(env).expanduser().resolve())
    for base in Path(__file__).resolve().parents:
        if (base / ".claude" / "skills").is_dir():
            return str(base)
    return None


CHECKLIST_PROMPT = """You are writing an in-lab review checklist for ONE de-identified patient.

The reader has just looked at this patient's record and (maybe) a model score. Turn that
into a short list of next steps that are IMPORTANT and DOABLE.

Every item must be:
- CONCRETE — a single step someone can actually perform ("pull the 2015-04-09 creatinine
  result and confirm the unit", not "review labs").
- GROUNDED — the `why` cites a specific fact from the record or the run below.
- DOABLE — completable in one sitting by the named owner.
- RANKED — high priority only for things that change how the score should be read.

Hard rules:
- This is de-identified research data, NOT care. Do NOT prescribe drugs, doses, or
  treatment. Items are review / verification / data-gap / monitoring / discussion steps.
- Never restate a risk score as your own estimate, and never invent a number.
- Empty or missing tables that the model needed are the most important items: a score
  computed on partial data must be flagged before anyone reads it.
- If the record supports fewer than 5 real items, return fewer. Do not pad.

Return ONLY a JSON object, no prose, no code fence:
{"items":[{"title":"...","why":"...","priority":"high|medium|low",
           "category":"data-gap|verify|monitor|discuss|follow-up",
           "owner":"clinician|patient|data-team","effort":"e.g. 5 min"}],
 "caveats":["..."]}
Return 3-7 items, most important first.
"""


def _strip_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        t = t.rsplit("```", 1)[0]
    i, j = t.find("{"), t.rfind("}")
    return t[i:j + 1] if i != -1 and j != -1 else t


# ── the console as a tool surface ────────────────────────────────────────────────
#
# An IN-PROCESS MCP server (create_sdk_mcp_server): the handlers are plain coroutines
# that close over the live WebSocket and RPC the browser. That works — without
# deadlocking — because the SDK dispatches every control request in its OWN task
# (_internal/query.py: `self.spawn_task(self._handle_control_request(request))`), so a
# handler blocking on the browser's reply never stalls the loop that must deliver it.
# It is the same reason the existing can_use_tool gate works.
#
# These tools do not TOUCH the console's state. They marshal a ConsoleAction to the
# browser, which runs it through the very same `dispatch` a rail click goes through
# (web/src/Console.tsx). One reducer, two drivers.

VIEW_NAMES = ["raw", "source", "record", "internal", "external", "model",
              "checklist", "annotate", "health"]
VIEWS = " | ".join(VIEW_NAMES)

# Schemas are EXPLICIT JSON Schema, not TypedDict.
#
# `TypedDict` + `NotRequired` does NOT survive: the SDK hands the class straight through
# and the conversion downstream marks EVERY key required. The symptom is nasty precisely
# because the agent behaves correctly — asked to ring a time window, it is refused with
# `'row' is a required property`, and (rightly) will not invent a placeholder row rather
# than ring an arbitrary one. So the highlight silently never happens. An explicit schema
# is passed through verbatim, and `required` means what it says.

NO_ARGS: dict[str, Any] = {"type": "object", "properties": {}}


def _schema(props: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": props, "required": required}


VIEW_PROP = {"type": "string", "enum": VIEW_NAMES}

VIEW_ARGS = _schema({
    "view": VIEW_PROP,
    "where": {"type": "string", "enum": ["here", "side"],
              "description": "'here' (default) puts it as a tab in the focused pane; "
                             "'side' splits a NEW pane beside it — only when asked."},
}, ["view"])

ONE_VIEW = _schema({"view": VIEW_PROP}, ["view"])

PANEL_ARGS = _schema({
    "view": {"type": "string", "enum": ["raw", "source", "record", "model"]},
    "table": {"type": "string", "description": "Source/Record: the table to open (e.g. CGM)"},
    "file": {"type": "string", "description": "Raw: the file to expand"},
    "tab": {"type": "string", "enum": ["card", "run"],
            "description": "Model: its card, or its run tab"},
    "open_run": {"type": "integer", "description": "Model: open a past run by its id"},
}, ["view"])

HIGHLIGHT_ARGS = _schema({
    "view": VIEW_PROP,
    "note": {"type": "string",
             "description": "what you are pointing AT — shown to the clinician"},
    "table": {"type": "string", "description": "which table to ring rows in (e.g. CGM)"},
    "start": {"type": "string",
              "description": "start of the time window, in the table's own format "
                             "(e.g. '05/19/2027 04:01:31 PM'). Usually what you want."},
    "end": {"type": "string", "description": "end of the time window"},
    "row": {"type": "integer", "minimum": 1,
            "description": "ALTERNATIVE to start/end: the 1-based row number the grid "
                           "shows. Omit this entirely when giving a time window."},
}, ["view"])

MODEL_ARGS = _schema({"package": {"type": "string"}}, ["package"])

RUN_ARGS = _schema({
    "patient_id": {"type": "string",
                   "description": "the patient you believe you are scoring — the console "
                                  "REFUSES the run if it has moved on to another"},
    "package": {"type": "string", "description": "the endpoint package to score with"},
}, ["patient_id", "package"])

PATIENT_ARGS = _schema({
    "patient_id": {"type": "string"},
    "why": {"type": "string", "description": "shown to the clinician on the Allow card"},
}, ["patient_id", "why"])


def build_console_mcp(ui):
    """The `console` MCP server. `ui(action, timeout)` marshals one action to the
    browser and returns what the browser did with it."""
    from claude_agent_sdk import create_sdk_mcp_server, tool

    def out(payload: dict) -> dict:
        return {"content": [{"type": "text", "text": json.dumps(payload, default=str)}],
                "is_error": not payload.get("ok", True)}

    @tool("get_state",
          "What the clinician has on screen RIGHT NOW: open tabs, the focused view, the "
          "selected patient and model, which tables are open, the run history with its "
          "scores, and checklist progress. Free to call — it changes nothing.", NO_ARGS)
    async def get_state(a):
        return out(await ui({"type": "state/read"}))

    @tool("open_view",
          f"Open a console view as a tab. view: {VIEWS}. where: 'here' (default, a tab in "
          "the focused pane) or 'side' (a NEW pane beside it — only when the clinician "
          "asked for a side-by-side).", VIEW_ARGS)
    async def open_view(a):
        return out(await ui({"type": "view/open", "view": a["view"],
                             "where": a.get("where", "here")}))

    @tool("focus_view",
          f"Switch to a view that is ALREADY open. Prefer this over open_view when the "
          f"tab exists — it does not move the layout. view: {VIEWS}.", ONE_VIEW)
    async def focus_view(a):
        return out(await ui({"type": "view/focus", "view": a["view"]}))

    @tool("close_view",
          f"Close a tab. Asks the clinician first — it may be a pane they are reading. "
          f"view: {VIEWS}.", ONE_VIEW)
    async def close_view(a):
        return out(await ui({"type": "view/close", "view": a["view"]}))

    @tool("set_panel",
          "Navigate INSIDE a view: open a table in the Source/Record layer (table=), "
          "expand a file in Raw (file=), switch the Model view between its card and its "
          "run tab (tab='card'|'run'), or open a past run (open_run=<id>).", PANEL_ARGS)
    async def set_panel(a):
        act: dict[str, Any] = {"type": "panel/set", "view": a["view"]}
        for k in ("table", "file", "tab"):
            if a.get(k) is not None:
                act[k] = a[k]
        if a.get("open_run") is not None:
            act["openRun"] = a["open_run"]
        return out(await ui(act))

    @tool("highlight",
          "POINT at the data. Rings rows in a table and scrolls them into view, with a "
          "note. Name EITHER a time window (start= and end=, matched against the table's "
          "datetime column — this is usually what you want) OR row=<the 1-based row "
          "number the grid shows>. Send exactly ONE of the two: OMIT `row` entirely when "
          "you are giving a time window — do not pass row=0 as a placeholder. This is "
          "your best move: it makes a claim checkable at a glance without opening "
          "anything new.",
          HIGHLIGHT_ARGS)
    async def highlight(a):
        return out(await ui({
            "type": "highlight/set", "view": a["view"],
            "table": a.get("table"), "row": a.get("row"),
            "from": a.get("start"), "to": a.get("end"), "note": a.get("note"),
        }))

    @tool("select_model",
          "Select a model in the console. Asks the clinician first: a silent swap means "
          "they press ▶ Run and score a model other than the one they believe they "
          "chose.", MODEL_ARGS)
    async def select_model(a):
        return out(await ui({"type": "model/select", "package": a["package"]}))

    @tool("run_model",
          "Press the console's ▶ Run button: score the patient with the model, through "
          "the console itself, so the run lands in the clinician's visible run history. "
          "Name the patient and the package EXPLICITLY — they are printed on the Allow "
          "card the clinician sees, and the console refuses the call if it has moved on "
          "since. Returns the endpoint's answer VERBATIM; report it, never restate it.",
          RUN_ARGS)
    async def run_model(a):
        return out(await ui({"type": "run/start", "patient_id": a["patient_id"],
                             "package": a["package"]}, timeout=180))

    @tool("generate_checklist",
          "Write the review checklist for the selected patient, from their record and the "
          "last run. Asks the clinician first — it writes clinical content into their "
          "workspace.", NO_ARGS)
    async def generate_checklist(a):
        return out(await ui({"type": "checklist/generate"}, timeout=180))

    @tool("switch_patient",
          "Bind the whole console to a DIFFERENT patient. Asks the clinician first. This "
          "resets their workspace (chart, checklist, tables) and hard-ends the current "
          "patient's line of reasoning: after it, carry NOTHING across. `why` is shown to "
          "the clinician — say why this patient, in one line.", PATIENT_ARGS)
    async def switch_patient(a):
        return out(await ui({"type": "patient/select", "patient_id": a["patient_id"]},
                            timeout=60))

    return create_sdk_mcp_server(
        name="console", version="0.1.0",
        tools=[get_state, open_view, focus_view, close_view, set_panel, highlight,
               select_model, run_model, generate_checklist, switch_patient],
    )


def _group_header(snap: dict, events: list[str]) -> str:
    """GROUP mode: the agent orients to the CORPUS it is developing labels over, not a
    patient. No patient-change marker, no model/run lines — there is no scoring here."""
    lines = [
        "mode: GROUP — the labeling forge. You are developing a labeling guideline over",
        "a whole corpus, not scoring one patient. There is NO selected patient here.",
    ]
    ds, n = snap.get("dataset"), snap.get("n_humans")
    lines.append(f"corpus: {ds or '— none selected —'}" + (f"  ({n} humans)" if n else ""))

    tabs = snap.get("tabs") or []
    focused = snap.get("focused_view")
    if tabs:
        lines.append("tabs: " + ", ".join(
            (t + "*" if t == focused else t) for t in tabs) + "   (* = focused)")
    mine = snap.get("agent_opened") or []
    if mine:
        lines.append("you opened (unread by them): " + ", ".join(mine))
    if events:
        lines.append("since your last message the researcher: " + "; ".join(events[-8:]))
    return "<console>\n" + "\n".join(lines) + "\n</console>\n\n"


def _console_header(snap: dict, events: list[str], prev_patient: str | None) -> str:
    """What the human has on screen, and what they just did — in ~120 tokens.

    This rides on the message the clinician sends, ATOMICALLY. It is deliberately not a
    debounced side-channel: if the model selection could arrive out of band, a click
    followed quickly by Enter would let the agent score the PREVIOUS model and report it
    as fact.
    """
    if not snap:
        return ""
    # GROUP is a different orientation entirely — hand off to its own header.
    if (snap.get("scope") or "individual") == "group":
        return _group_header(snap, events)
    lines = []

    pid = snap.get("patient_id")
    if prev_patient and pid and pid != prev_patient:
        lines += [
            f"⚠️ PATIENT CHANGED: {prev_patient} → {pid}",
            f"Everything earlier in this conversation is about {prev_patient}. Carry NOTHING",
            f"across — no number, no table, no finding. Re-fetch anything you need for {pid}.",
            "",
        ]

    lines.append(f"patient: {pid or '— none selected —'}"
                 + (f" ({snap['cohort']})" if snap.get("cohort") else "")
                 + (f" · as-of {snap['index_date']}" if snap.get("index_date") else ""))
    if snap.get("not_scoreable_reason"):
        lines.append(f"⚠️ not scoreable: {snap['not_scoreable_reason']}")

    tabs = snap.get("tabs") or []
    focused = snap.get("focused_view")
    if tabs:
        lines.append("tabs: " + ", ".join(
            (t + "*" if t == focused else t) for t in tabs) + "   (* = focused)")
    mine = snap.get("agent_opened") or []
    if mine:
        lines.append("you opened (unread by them): " + ", ".join(mine))

    if snap.get("model"):
        lines.append(f"model selected: {snap['model']}"
                     + ("" if snap.get("model_live") else "  (endpoint NOT running)"))

    nav = snap.get("nav") or {}
    looking = []
    if (nav.get("source") or {}).get("table"):
        looking.append(f"Source→{nav['source']['table']}")
    if (nav.get("record") or {}).get("table"):
        looking.append(f"Record→{nav['record']['table']}")
    if (nav.get("raw") or {}).get("file"):
        looking.append(f"Raw→{nav['raw']['file']}")
    if looking:
        lines.append("looking at: " + ", ".join(looking))

    for r in (snap.get("runs") or [])[:3]:
        who = "you" if r.get("origin") == "agent" else "the clinician"
        bits = [f"run #{r['id']} ({who}): {r['model']} → {r['status']}"]
        if r.get("forecast_mae") is not None:
            bits.append(f"MAE {r['forecast_mae']} mg/dL")
        elif r.get("score") is not None:
            bits.append(f"{r['score']}" + (f" ({r['band']})" if r.get("band") else ""))
        lines.append("  ".join(bits))

    cl = snap.get("checklist")
    if cl:
        lines.append(f"checklist: {cl['items']} items, {cl['done']} done")

    if events:
        lines.append("since your last message the clinician: " + "; ".join(events[-8:]))

    return "<console>\n" + "\n".join(lines) + "\n</console>\n\n"


@router.post("/api/checklist")
async def checklist(req: Request):
    """Generate an in-lab review checklist from the record + (optional) last run.

    NOT a tool-calling agent: the context is assembled deterministically here (the same
    engine the buttons use) and handed to the model as text, so there is nothing for the
    agent to reach for and no approval gate to run. One short turn, one JSON object.
    """
    body = await req.json()
    pid = body.get("patient_id")
    if not pid:
        return JSONResponse({"error": "patient_id is required"}, status_code=400)

    try:
        chart = ep.tool_get_patient({"patient_id": pid})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)}, status_code=400)

    run = body.get("run") or {}
    gaps = run.get("gaps") or {}
    basis = {
        "index_date": chart.get("index_date"),
        "model": run.get("model"),
        "score": run.get("score"),
        "band": run.get("band"),
        "empty_tables": gaps.get("empty_tables") or [],
        "missing_tables": gaps.get("missing_tables") or [],
    }

    context = {
        "patient_id": pid,
        "as_of": chart.get("index_date"),
        "age_at_index": chart.get("age_at_index"),
        "summary": chart.get("summary"),
        "post_index_rows_hidden": chart.get("post_index_rows_hidden"),
        # the curated chart, trimmed: enough to ground an item, small enough to be cheap
        "chart": {t: rows[:12] for t, rows in (chart.get("source_tables") or {}).items()
                  if rows},
        "last_run": basis if run else None,
    }

    try:
        from claude_agent_sdk import (
            AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock,
        )
    except ImportError as e:
        return JSONResponse({"error": f"agent unavailable: {e}"}, status_code=503)

    options = ClaudeAgentOptions(
        system_prompt=CHECKLIST_PROMPT,
        mcp_servers={},          # no tools: the context is already assembled
        permission_mode="default",
        max_turns=1,
        model=os.environ.get("INLAB_AGENT_MODEL") or None,
    )

    text = ""
    try:
        async with ClaudeSDKClient(options=options) as client:
            await client.query("Patient context:\n" + json.dumps(context, default=str))
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for b in msg.content:
                        if isinstance(b, TextBlock):
                            text += b.text
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": f"generation failed: {e}"}, status_code=502)

    try:
        parsed = json.loads(_strip_fence(text))
    except json.JSONDecodeError:
        return JSONResponse({"error": "the model did not return JSON", "raw": text[:2000]},
                            status_code=502)

    return JSONResponse({
        "patient_id": pid,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "items": parsed.get("items", []),
        "caveats": parsed.get("caveats", []),
        "basis": basis,
    })


FOLLOW_PROMPT = """The clinician just did something in the console. You were NOT asked a
question — you are looking over their shoulder.

Say something ONLY if you can see something genuinely worth flagging right now: a data
gap that would distort a score, a run whose result contradicts what they seem to expect,
a table that is empty when the model needs it. One or two sentences, no preamble.

If there is nothing worth interrupting for — which is most of the time — reply with
exactly: NOOP

Do not narrate what they did back at them. Do not greet. Do not offer to help."""


@router.websocket("/ws/haichat")
async def haichat(sock: WebSocket):
    await sock.accept()

    try:  # imported lazily so the deterministic REST path works without the SDK
        from claude_agent_sdk import (
            AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient,
            PermissionResultAllow, PermissionResultDeny, ResultMessage,
            StreamEvent, TextBlock, ToolResultBlock, ToolUseBlock,
        )
    except ImportError as e:
        await sock.send_json({"type": "error",
                              "message": f"agent unavailable: claude-agent-sdk not installed ({e})"})
        await sock.close()
        return

    pending: dict[str, asyncio.Future] = {}      # approval cards
    pending_ui: dict[str, asyncio.Future] = {}   # console actions in flight
    # what the browser last told us it has on screen — used ONLY to explain a refusal
    # and to detect a patient change; never as the source of a patient/model for a run.
    seen: dict[str, Any] = {"snapshot": {}, "patient": None}

    async def ui(action: dict, timeout: float = 30.0) -> dict:
        """Marshal one ConsoleAction to the browser and wait for it to be applied.

        This blocks the calling TOOL, not the socket: the SDK runs each control request
        in its own task, and the receive loop below stays free to read the ui_result we
        are waiting on. Awaiting a turn inline in that loop would deadlock this — which
        is exactly why run_turn is a detached task.
        """
        req_id = uuid.uuid4().hex[:8]
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        pending_ui[req_id] = fut
        try:
            await sock.send_json({"type": "ui_call", "id": req_id, "action": action})
            res = await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError:
            return {"ok": False, "error": "the console did not respond in time"}
        except Exception as e:  # noqa: BLE001 — socket gone
            return {"ok": False, "error": f"the console is unreachable: {e}"}
        finally:
            pending_ui.pop(req_id, None)
        if isinstance(res.get("state"), dict):
            seen["snapshot"] = res["state"]
        return res

    async def can_use_tool(tool_name: str, tool_input: dict, ctx: Any):
        """The gate. Two tiers, one callback, no bypass.

        Nothing is in `allowed_tools` — listing a tool there auto-approves it BEFORE this
        callback ever runs, which would retire the gate silently. So the auto-allow tier
        is an early return from inside the gate, where it stays auditable and where the
        allowlist is enforced in the same place.
        """
        # the lab profile widens both tiers with the research toolbelt; clinical
        # keeps only the console + engine reads.
        auto = ALLOWED_AUTO + list(LAB_AUTO) if AGENT_PROFILE == "lab" else ALLOWED_AUTO
        gated = ALLOWED_GATED + list(LAB_GATED) if AGENT_PROFILE == "lab" else ALLOWED_GATED

        if tool_name in auto:
            # navigation / reads: reversible, no consequence outside this browser tab.
            # The clinician still SEES it — the drawer chips every one, and the tab
            # carries a 🤖 until they click it.
            return PermissionResultAllow()

        if tool_name not in gated:
            return PermissionResultDeny(
                message=f"{tool_name} is not permitted in this console.")

        req_id = uuid.uuid4().hex[:8]
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        pending[req_id] = fut
        await sock.send_json({"type": "approval_request", "id": req_id,
                              "tool": tool_name, "input": tool_input})
        try:
            approved = await asyncio.wait_for(fut, timeout=300)
        except asyncio.TimeoutError:
            approved = False
        finally:
            pending.pop(req_id, None)
        if approved:
            return PermissionResultAllow()
        return PermissionResultDeny(message="The clinician declined this tool call.")

    lab = AGENT_PROFILE == "lab"
    options = ClaudeAgentOptions(
        system_prompt=LAB_SYSTEM_PROMPT if lab else SYSTEM_PROMPT,
        mcp_servers={
            # the same engine the ▶ Run button uses, as an explicit stdio MCP server —
            # buttons and agent reach the endpoint through the SAME code, or the demo lies
            "endpoint-predict": {
                "type": "stdio",
                "command": sys.executable,
                "args": [str(ENGINE / "server.py")],
                "env": {k: os.environ[k] for k in ENGINE_ENV_KEYS if k in os.environ},
            },
            # the console itself, IN-PROCESS: handlers that hold this socket and drive the
            # clinician's UI through the same reducer her own clicks go through
            "console": build_console_mcp(ui),
        },
        # clinical: NO BUILT-IN TOOLS. `[]` sends `--tools ""`, which disables Bash / Read
        # / Write / Grep / Task / WebFetch outright; the MCP servers above are unaffected.
        # The clinical assistant is not a coding agent — it has a console and an endpoint,
        # and that is all it should touch. lab: the research toolbelt, every ACTING member
        # of which the gate above still blocks on Allow.
        tools=LAB_TOOLS if lab else [],
        # clinical: load NO filesystem settings — unset, the CLI would read the operator's
        # ~/.claude/settings.json, whose permission allowlist and `defaultMode` apply
        # BEFORE can_use_tool and could silently retire the gate. lab: load the PROJECT's
        # .claude (its skills + CLAUDE.md) only — not "user", so the operator's global
        # permission allowlist never shadows the researcher's Allow/Deny.
        setting_sources=["project"] if lab else [],
        # lab needs a cwd so "project" resolves to the repo that carries the skills;
        # clinical loads nothing, so cwd is irrelevant (None = process cwd).
        cwd=_skills_root() if lab else None,
        # Two more things would silently BYPASS the gate:
        #   1. allowed_tools — auto-approves listed tools before can_use_tool runs.
        #   2. permission_mode other than "default" (e.g. "auto"/"bypassPermissions").
        # So: no allowed_tools, and permission_mode pinned — in BOTH profiles.
        permission_mode="default",
        can_use_tool=can_use_tool,
        include_partial_messages=True,
        # navigating the console costs turns; a skill run costs many more — give lab a
        # larger budget so a /sl-iterate is not cut off mid-loop.
        max_turns=60 if lab else 20,
        model=os.environ.get("INLAB_AGENT_MODEL") or None,
    )

    async def run_turn(client, text: str, quiet: bool = False):
        """quiet=True is a Follow turn: the agent was not asked anything, so it is
        allowed to have nothing to say. Its deltas are withheld and a NOOP answer leaves
        no trace at all — an assistant that mutters on every click gets muted."""
        await client.query(text)
        said = ""
        async for msg in client.receive_response():
            # token-level deltas keep the drawer alive instead of freezing for 30s
            if isinstance(msg, StreamEvent):
                if quiet:
                    continue
                ev = msg.event or {}
                if ev.get("type") == "content_block_delta":
                    delta = ev.get("delta") or {}
                    if delta.get("type") == "text_delta" and delta.get("text"):
                        await sock.send_json({"type": "delta", "text": delta["text"]})
                continue

            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, ToolUseBlock):
                        await sock.send_json({"type": "tool_call", "tool": b.name,
                                              "input": b.input})
                    elif isinstance(b, ToolResultBlock):
                        content = b.content
                        if isinstance(content, list):
                            content = " ".join(
                                c.get("text", "") for c in content if isinstance(c, dict))
                        await sock.send_json({"type": "tool_result",
                                              "content": str(content)[:4000],
                                              "is_error": bool(b.is_error)})
                    elif isinstance(b, TextBlock) and b.text.strip():
                        said += b.text
                        if not quiet:
                            # the settled block — the UI swaps its streamed draft for this
                            await sock.send_json({"type": "assistant", "text": b.text})
            elif isinstance(msg, ResultMessage):
                nothing_to_say = quiet and said.strip().upper().strip(".!") == "NOOP"
                if quiet and not nothing_to_say and said.strip():
                    await sock.send_json({"type": "assistant", "text": said})
                await sock.send_json({"type": "done", "duration_ms": msg.duration_ms,
                                      "cost_usd": msg.total_cost_usd,
                                      "num_turns": msg.num_turns,
                                      "quiet": quiet})

    turn: asyncio.Task | None = None

    async def guarded_turn(client, text: str, quiet: bool = False):
        try:
            await run_turn(client, text, quiet)
        except Exception as e:  # noqa: BLE001
            await sock.send_json({"type": "error", "message": str(e)})

    def framed(snap: dict, events: list[str], body: str) -> str:
        """The console header + the message. The patient-change marker is computed HERE,
        against the last patient we actually saw, so it fires whether the clinician
        switched patients or the agent did."""
        header = _console_header(snap, events, seen["patient"])
        if snap.get("patient_id"):
            seen["patient"] = snap["patient_id"]
        seen["snapshot"] = snap or seen["snapshot"]
        return header + body

    try:
        async with ClaudeSDKClient(options=options) as client:
            await sock.send_json({"type": "ready"})
            while True:
                raw = await sock.receive_text()
                msg = json.loads(raw)
                kind = msg.get("type")

                if kind == "approval_response":
                    fut = pending.get(msg.get("id"))
                    if fut and not fut.done():
                        fut.set_result(bool(msg.get("approved")))
                    continue

                if kind == "ui_result":
                    fut = pending_ui.get(msg.get("id"))
                    if fut and not fut.done():
                        fut.set_result({k: v for k, v in msg.items()
                                        if k not in ("type", "id")})
                    continue

                if kind == "interrupt":
                    await client.interrupt()
                    continue

                if kind in ("user", "follow"):
                    if turn and not turn.done():
                        if kind == "follow":
                            continue          # they are mid-answer; the click can wait
                        await sock.send_json({
                            "type": "error",
                            "message": "still working on the previous message",
                        })
                        continue

                    snap = msg.get("snapshot") or {}
                    events = msg.get("events") or []

                    if kind == "follow":
                        body = (FOLLOW_PROMPT + "\n\nWhat they just did: "
                                + "; ".join(events))
                        text = framed(snap, [], body)
                    else:
                        text = framed(snap, events, msg.get("text", ""))

                    # DO NOT await the turn here. can_use_tool and the console tools both
                    # block on Futures that only THIS loop can resolve (approval_response
                    # / ui_result). Awaiting inline deadlocks: the loop could not read the
                    # reply to the very question the turn is waiting on.
                    turn = asyncio.create_task(
                        guarded_turn(client, text, quiet=(kind == "follow")))
    except WebSocketDisconnect:
        # Unblock EVERYTHING waiting on this socket, or a tool hangs on a browser that is
        # gone and the turn task never finishes; then cancel the in-flight turn so the SDK
        # subprocess does not linger.
        for fut in pending.values():
            if not fut.done():
                fut.set_result(False)  # an abandoned prompt counts as "deny"
        for fut in pending_ui.values():
            if not fut.done():
                fut.set_result({"ok": False, "error": "the console was closed"})
        if turn and not turn.done():
            turn.cancel()
    except Exception as e:  # noqa: BLE001 — e.g. the claude CLI missing
        try:
            await sock.send_json({"type": "error", "message": f"agent unavailable: {e}"})
        except Exception:
            pass
