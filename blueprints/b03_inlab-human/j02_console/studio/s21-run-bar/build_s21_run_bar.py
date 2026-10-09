"""s21 · The run bar: each step of the Model view's run bar (▶ Run · Interpret · Message · Judge · Feedback) with who does
it (the endpoint, a toolkit skill's persona, the human) and the route it calls; the two runs shot on the fixtures; and
every HaiChat tool with the ConsoleAction it dispatches and whether it waits for Allow/Deny, read from haichat_api.py.
A rebuild keeps whatever a person drew.

    python build_s21_run_bar.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import APP, GREEN, RED, Sheet, header, save  # noqa: E402

CHANGES = [("261009", "fixed: a call the gate refuses shows as ⛔ refused in the drawer, with the gate's reason"),
           ("261009", "the message step reads the patient from the dataset on screen, not one fixed store")]
STEPS = [
    ["▶ Run", "the endpoint's own number: POST to its /invocations through endpoint-predict", "the endpoint (no LLM)",
     "POST /api/predict"],
    ["🔍 Interpret", "a reading of the forecast for the clinician", "LLM · persona of haipipe-individual-inference-report",
     "POST /api/message (slot interpretation)"],
    ["✉️ Message", "the message a patient would get, written blind to what was observed",
     "LLM · persona of haipipe-individual-inference-report", "POST /api/message"],
    ["⚖️ Judge", "rubric scores of that message", "LLM · persona of haipipe-individual-inference-judge", "POST /api/judge"],
    ["🩺 Feedback", "the human's verdict, append-only", "the human", "POST /api/feedback"],
]


def agent_tools():
    """[(tool, the ConsoleAction it dispatches, auto | gated)] from haichat_api.py."""
    src = (APP / "haichat_api.py").read_text(encoding="utf-8")
    auto = set(re.findall(r'"mcp__console__(\w+)"', src.split("ALLOWED_AUTO = [", 1)[1].split("]", 1)[0]))
    gated = set(re.findall(r'"mcp__console__(\w+)"', src.split("ALLOWED_GATED = [", 1)[1].split("]", 1)[0]))
    out = []
    blocks = re.split(r'@tool\(\s*"', src)[1:]
    for b in blocks:
        name = b.split('"', 1)[0]
        act = re.search(r'"type":\s*"([a-z]+/[a-z]+)"', b.split("@tool(", 1)[0])
        out.append([name, act.group(1) if act else "(reads the console state)",
                    "gated: Allow/Deny" if name in gated else "auto" if name in auto else "? in neither list"])
    return out


def main():
    s = Sheet()
    f = s.frame("1 · The run bar", 0, 0, 1960, 100)
    y = header(s, f, "s21 · The run bar: from the endpoint's number to the human's verdict",
               "Left of the divider is the endpoint's number, made without an LLM. Everything right of it is downstream of\n"
               "that number, each step gated on the one before. Compose and Judge never see what was observed (the wall).",
               CHANGES)
    y = s.table(40, y, [("step", 160, 16), ("what it makes", 620, 62), ("who does it", 560, 56), ("route", 520, 52)],
                STEPS, f)
    y += 40
    w = 900
    s.text(40, y, "▶ Run on the glucose forecast stub (a trajectory)", 18, f)
    s.text(40 + w + 60, y, "▶ Run on the risk stub (a score and a band)", 18, f)
    h1 = s.image(HERE / "shots" / "run_cgm_forecast.png", 40, y + 30, w, f)
    h2 = s.image(HERE / "shots" / "run_risk_score.png", 40 + w + 60, y + 30, w, f)
    y += 30 + max(h1, h2, 40) + 50
    s.text(40, y, "HaiChat's tools: each one dispatches the same ConsoleAction a click does (actions.ts), one reducer",
           22, f)
    tools = agent_tools()
    y = s.table(40, y + 40, [("tool (mcp__console__…)", 360, 36), ("ConsoleAction", 420, 42), ("gate", 360, 36)],
                tools, f, red=lambda r: r[2].startswith("?"))
    y += 30
    s.text(40, y, "✎ 261009 a tool in neither list (prepare_payload) or a Deny now reaches the drawer as ⛔ refused, "
                  "never a chip that looks as if it ran (shot in s32)", 16, f, GREEN)
    y += 30
    s.text(40, y, "? this vocabulary could drive the toolkit's workbench too: an MCP whose tools are its actions "
                  "(j04 Q02 · b01 j05_chat Q02)", 16, f, RED)
    save(s, f, y + 40, HERE / "s21-run-bar.excalidraw", "build_s21_run_bar.py")


if __name__ == "__main__":
    main()
